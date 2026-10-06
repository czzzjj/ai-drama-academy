#!/usr/bin/env python3
"""学院检查脚本共用库（只依赖标准库）。

所有解析规则以 70-playbooks/format-contracts.md 为准。改这里 = 改契约，必须同步改模板与 fixtures。

提供：
- Markdown 管道表解析（按表头名取列）
- 分镜表 / 视频提示词 / 锚点卡 / 剪辑单 解析
- H3 帧网格（17k+5，k=7..21，24fps）               溯源：T-2
- 中文台词字数计数与对白容量核算基准（7.5 字/秒）   溯源：T-2, D3, P9
- 统一的发现项（Finding）与报告/退出码约定           见 CONVENTIONS.md §8
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ------------------------------------------------------------------ 常量（委托方实证）

H3_FPS = 24                      # 由 124 帧≈5.17s、362 帧≈15.08s 反推，见 T-2
H3_K_MIN, H3_K_MAX = 7, 21       # 17k+5 → 124 .. 362 帧
H3_MIN_FRAMES, H3_MAX_FRAMES = 124, 362
SPEECH_RATE_CPS = 7.5            # H3 实测中文语速（字/秒），T-2 / D3
H3_SECTIONS = [
    "subject_definitions", "summary", "retention_analysis",
    "detailed_description", "overall_soundscape", "non_diegetic_music",
]
BAN_LINE = "No captions, subtitles, or dialogue text overlays appear at any moment."   # D1
REALTIME_LINE = "Real-time speed throughout, no slow motion"                           # A3
LAYOUT_VALUES = {"LEFT", "RIGHT", "CENTER", "FG", "BG"}
EMPTY = {"", "—", "-", "–", "无", "N/A", "n/a"}

# 已知 ASR 在静音/无对白音轨上的幻觉输出（D5，第一条为委托方实证，其余为社区常见报告，以 80-sources 为准）
KNOWN_ASR_HALLUCINATIONS = [
    "字幕by索兰娅",
    "请不吝点赞",
    "订阅 转发 打赏",
    "明镜与点点栏目",
    "谢谢观看",
    "字幕由Amara.org社区提供",
]

# ------------------------------------------------------------------ 报告

@dataclass
class Finding:
    level: str            # "error" | "warn" | "info" | "visual"（需目视）
    code: str             # 规则代码，如 "D3-capacity"
    msg: str
    where: str = ""       # 文件:行 或 SHOT-xxx
    data: dict = field(default_factory=dict)


def emit(title: str, findings: list[Finding], as_json: bool = False, extra: dict | None = None) -> int:
    """打印报告并返回退出码：有 error → 1，否则 0。"""
    errors = [f for f in findings if f.level == "error"]
    if as_json:
        out = {"title": title, "ok": not errors, "counts": {
            lv: sum(1 for f in findings if f.level == lv) for lv in ("error", "warn", "info", "visual")},
            "findings": [asdict(f) for f in findings]}
        if extra:
            out.update(extra)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"== {title} ==")
        icon = {"error": "❌", "warn": "⚠️ ", "info": "ℹ️ ", "visual": "👁 "}
        for f in findings:
            loc = f" [{f.where}]" if f.where else ""
            print(f"{icon.get(f.level, '-')} {f.code}{loc}: {f.msg}")
        if extra and extra.get("summary"):
            print(extra["summary"])
        print(f"结果：{'通过' if not errors else '不通过'}（{len(errors)} 错误，"
              f"{sum(1 for f in findings if f.level == 'warn')} 警告，"
              f"{sum(1 for f in findings if f.level == 'visual')} 需目视）")
    return 1 if errors else 0


def die(msg: str) -> "None":
    print(f"用法/环境错误：{msg}", file=sys.stderr)
    sys.exit(2)


# ------------------------------------------------------------------ Markdown 表格

def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, i = [], "", 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if s[i] == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += s[i]
        i += 1
    cells.append(cur.strip())
    return cells


def _is_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?", line.strip()))


def parse_md_tables(text: str) -> list[dict]:
    """返回 [{header: [...], rows: [{col: val, '_line': n}], line: n}]，跳过代码块内的表。"""
    tables, lines, i, in_code = [], text.splitlines(), 0, False
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if not in_code and ln.strip().startswith("|") and i + 1 < len(lines) and _is_sep(lines[i + 1]):
            header = _split_row(ln)
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = _split_row(lines[j])
                row = {h: (cells[k] if k < len(cells) else "") for k, h in enumerate(header)}
                row["_line"] = j + 1
                rows.append(row)
                j += 1
            tables.append({"header": header, "rows": rows, "line": i + 1})
            i = j
            continue
        i += 1
    return tables


def find_rows(text: str, required: list[str]) -> list[dict]:
    """取所有表头包含 required 全部列名的表的行。"""
    out = []
    for t in parse_md_tables(text):
        if all(c in t["header"] for c in required):
            out.extend(t["rows"])
    return out


def is_empty(v: str | None) -> bool:
    return v is None or v.strip() in EMPTY


# ------------------------------------------------------------------ 分镜表

STORYBOARD_COLS = ["段号", "镜号", "时长(s)", "拍数", "内容", "运镜", "运镜因果", "起始帧方位", "对白", "短镜理由"]


def parse_layout(s: str) -> dict:
    """'神=LEFT; 苏晓=RIGHT' → {'神': 'LEFT', '苏晓': 'RIGHT'}"""
    out = {}
    if is_empty(s):
        return out
    for part in re.split(r"[;；,，]", s):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip().upper()
    return out


def parse_dialogue(s: str) -> list[tuple[str, str]]:
    """'苏晓：就是现在！ / 神：……' → [('苏晓', '就是现在！'), ('神', '……')]"""
    if is_empty(s):
        return []
    out = []
    for seg in re.split(r"\s+/\s+", s.strip()):
        m = re.match(r"^\s*([^：:]{1,20})[：:]\s*(.+)$", seg)
        out.append((m.group(1).strip(), m.group(2).strip()) if m else ("?", seg.strip()))
    return out


def to_float(v: str) -> float | None:
    try:
        return float(str(v).strip().rstrip("s").rstrip("秒"))
    except (TypeError, ValueError):
        return None


def parse_storyboard(path: str | Path) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    rows = find_rows(text, ["镜号", "时长(s)"])
    shots = []
    for r in rows:
        shots.append({
            "seq": r.get("段号", ""), "shot": r.get("镜号", ""),
            "dur": to_float(r.get("时长(s)", "")), "beats": to_float(r.get("拍数", "")),
            "content": r.get("内容", ""), "camera": r.get("运镜", ""), "camera_cause": r.get("运镜因果", ""),
            "layout": parse_layout(r.get("起始帧方位", "")), "layout_raw": r.get("起始帧方位", ""),
            "dialogue": parse_dialogue(r.get("对白", "")), "short_reason": r.get("短镜理由", ""),
            "line": r["_line"], "file": str(path),
        })
    return shots


# ------------------------------------------------------------------ 视频提示词

def parse_video_prompts(path: str | Path) -> list[dict]:
    """每镜：{shot, meta{}, h3(text), h3_line, sections{name: text}, section_order[], line}"""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    shots, cur, in_code, code_lang, buf = [], None, False, "", []
    for i, ln in enumerate(lines, 1):
        if not in_code:
            m = re.match(r"^##\s+(SHOT-\d{3})\b", ln)
            if m:
                cur = {"shot": m.group(1), "meta": {}, "h3": None, "h3_line": None,
                       "sections": {}, "section_order": [], "line": i, "file": str(path)}
                shots.append(cur)
                continue
            if cur is not None:
                mm = re.match(r"^-\s*([^:：]+?)\s*[:：]\s*(.*)$", ln)
                if mm and cur["h3"] is None:
                    cur["meta"][mm.group(1).strip()] = mm.group(2).strip()
                    continue
            if ln.strip().startswith("```"):
                in_code, code_lang, buf = True, ln.strip()[3:].strip(), []
                start = i
                continue
        else:
            if ln.strip().startswith("```"):
                in_code = False
                if cur is not None and code_lang == "h3" and cur["h3"] is None:
                    cur["h3"] = "\n".join(buf)
                    cur["h3_line"] = start + 1
                    _split_sections(cur)
                continue
            buf.append(ln)
    return shots


def _split_sections(shot: dict):
    name, acc = None, []
    for ln in shot["h3"].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", ln)
        if m and m.group(1) in H3_SECTIONS:
            if name:
                shot["sections"][name] = "\n".join(acc).strip()
            name, acc = m.group(1), [m.group(2)]
            shot["section_order"].append(name)
        elif name:
            acc.append(ln)
    if name:
        shot["sections"][name] = "\n".join(acc).strip()


def parse_references(s: str) -> list[tuple[int | None, str]]:
    """'1=CHR-A-BOARD; 2=REF-SHOT011-START' → [(1,'CHR-A-BOARD'), (2,'REF-SHOT011-START')]"""
    out = []
    if is_empty(s):
        return out
    for part in re.split(r"[;；]", s):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d+)\s*=\s*(.+)$", part)
        out.append((int(m.group(1)), m.group(2).strip()) if m else (None, part))
    return out


RE_DIALOGUE = re.compile(r"<d>\s*\[Chinese\]\s*(.*?)\s*</d>", re.S)


def dialogue_from_h3(h3: str) -> list[str]:
    return [m.strip() for m in RE_DIALOGUE.findall(h3 or "")]


# ------------------------------------------------------------------ 锚点卡 / 剪辑单

def parse_anchors(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    anchors, cur = {}, None
    for i, ln in enumerate(text.splitlines(), 1):
        m = re.match(r"^##\s+ANCHOR:\s*([A-Z]{3}-[A-Z0-9-]+)\s*$", ln)
        if m:
            cur = {"id": m.group(1), "line": i, "fields": {}}
            anchors[cur["id"]] = cur
            continue
        if cur:
            mm = re.match(r"^-\s*([^:：]+?)\s*[:：]\s*(.*)$", ln)
            if mm:
                key, val = mm.group(1).strip(), mm.group(2).strip()
                if key == "锚点句 EN":
                    bt = re.match(r"^`(.+)`$", val)
                    val = bt.group(1) if bt else val
                cur["fields"][key] = val
    return anchors


def parse_edit_list(path: str | Path) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    return find_rows(text, ["CUT", "来源"])


# ------------------------------------------------------------------ 字数与帧网格

RE_HAN = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
RE_LATIN_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
RE_DIGIT = re.compile(r"[0-9０-９]")


def speech_chars(text: str) -> float:
    """台词"可读字数"：汉字计 1；阿拉伯数字逐位计 1（读作中文数字时约 1 字/位）；
    拉丁单词计 2（〔学院推断〕：英文词在中文语流中约占 2 个汉字时长）。标点、空白、省略号不计。"""
    if not text:
        return 0.0
    return len(RE_HAN.findall(text)) + len(RE_DIGIT.findall(text)) + 2 * len(RE_LATIN_WORD.findall(text))


def grid_frames() -> list[int]:
    return [17 * k + 5 for k in range(H3_K_MIN, H3_K_MAX + 1)]


def frames_to_seconds(n: int) -> float:
    return n / H3_FPS


def is_grid_frames(n: int) -> bool:
    return n in grid_frames()


def snap_seconds_up(sec: float) -> int | None:
    """返回 ≥ sec 的最小合法帧数；超过 362 帧返回 None（需拆段）。"""
    for n in grid_frames():
        if frames_to_seconds(n) + 1e-9 >= sec:
            return n
    return None


def snap_seconds_nearest(sec: float) -> int:
    return min(grid_frames(), key=lambda n: abs(frames_to_seconds(n) - sec))


# ------------------------------------------------------------------ ffmpeg

def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def run(cmd: list[str], timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ffprobe_json(path: str | Path) -> dict:
    p = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout)


def media_duration(path: str | Path) -> float:
    info = ffprobe_json(path)
    return float(info.get("format", {}).get("duration", 0.0))


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
