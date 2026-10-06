#!/usr/bin/env python3
"""学院检查脚本共用库（只依赖标准库）。

所有解析规则以 70-playbooks/format-contracts.md 为准。改这里 = 改契约，必须同步改模板与 fixtures。

提供：
- Markdown 管道表解析（按表头名取列）
- 分镜表 / 视频提示词 / 锚点卡 / 剪辑单 解析（一律 utf-8-sig 读入：BOM 安全；围栏按 CommonMark 配对）
- 模式（Ref2VA 六段 / FL2VA 三段）、尾部余量、对白分句/标记容错与问题清单（dialogue_sep_issues / dialogue_tag_issues）
- H3 帧网格（17k+5，k=7..21，24fps）               溯源：T-2
- 中文台词字数计数与对白容量核算基准（7.5 字/秒）   溯源：T-2, D3, P9
- 统一的发现项（Finding）与报告/退出码约定           见 CONVENTIONS.md §8
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ------------------------------------------------------------------ 常量（委托方实证）

H3_FPS = 24                      # 由 124 帧≈5.17s、362 帧≈15.08s 反推，见 T-2
H3_K_MIN, H3_K_MAX = 7, 21       # 17k+5 → 124 .. 362 帧
H3_MIN_FRAMES, H3_MAX_FRAMES = 124, 362
SPEECH_RATE_CPS = 7.5            # H3 实测中文语速（字/秒），T-2 / D3
H3_SECTIONS = [                  # Ref2VA（参考生视频，MiniMaxH3ReferenceToVideo）六段方言，T-2 / F-H3-03
    "subject_definitions", "summary", "retention_analysis",
    "detailed_description", "overall_soundscape", "non_diegetic_music",
]
H3_SECTIONS_FL2VA = [            # FL2VA（首/尾帧，MiniMaxH3ImageToVideo）三段方言，F-H3-02 / S-H3-01
    "integrated_multimodal_description", "overall_soundscape", "non_diegetic_music",
]
H3_MODES = {"REF2VA": "Ref2VA", "FL2VA": "FL2VA"}
DISPLAY_TOL = 0.005              # 文档时长写两位小数：124 帧 = 5.1667s 写作 5.17，吸附时容忍显示舍入
BAN_LINE = "No captions, subtitles, or dialogue text overlays appear at any moment."   # D1
REALTIME_LINE = "Real-time speed throughout, no slow motion"                           # A3
LAYOUT_VALUES = {"LEFT", "RIGHT", "CENTER", "FG", "BG"}
EMPTY = {"", "—", "——", "-", "–", "－", "无", "无对白", "N/A", "n/a", "N/a", "NA", "None", "none", "NONE"}

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
    safe_stdio()
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


def safe_stdio() -> None:
    """stdout/stderr 是 GBK/cp936 等非 UTF-8 编码时（Windows cmd 重定向，E3-1），❌⚠️👁 无法编码会抛
    UnicodeEncodeError；改为替换成 ?，报告与退出码照常。"""
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def read_text(path: str | Path) -> str:
    """读 UTF-8 文本并去掉 BOM（utf-8-sig）。BOM 会让首行表头/`## SHOT-`/`## ANCHOR:` 静默消失。"""
    return Path(path).read_text(encoding="utf-8-sig")


def has_bom(path: str | Path) -> bool:
    return Path(path).read_bytes()[:3] == b"\xef\xbb\xbf"


def die(msg: str) -> "None":
    safe_stdio()
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


RE_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def fence_step(line: str, fence: tuple[str, int] | None) -> tuple[tuple[str, int] | None, bool, str]:
    """CommonMark 围栏状态机。fence = None（不在代码块）或 (字符, 长度)。
    返回 (新状态, 本行是否为围栏行, 开围栏的 info 串)。N 个反引号/波浪号开的块只被 ≥N 个同种字符、且其后只有空白的行关闭，
    所以 ````markdown 块里的 ```h3 不会提前关块。"""
    m = RE_FENCE.match(line)
    if not m:
        return fence, False, ""
    run, rest = m.group(1), m.group(2)
    if fence is None:
        if run[0] == "`" and "`" in rest:        # 反引号围栏的 info 串不能含反引号（那是行内代码）
            return None, False, ""
        return (run[0], len(run)), True, rest.strip()
    if run[0] == fence[0] and len(run) >= fence[1] and not rest.strip():
        return None, True, ""
    return fence, False, ""


def parse_md_tables(text: str) -> list[dict]:
    """返回 [{header: [...], rows: [{col: val, '_line': n}], line: n}]，跳过代码块内的表。"""
    tables, lines, i, fence = [], text.splitlines(), 0, None
    while i < len(lines):
        ln = lines[i]
        fence, is_fence, _ = fence_step(ln, fence)
        if is_fence or fence is not None:
            i += 1
            continue
        if ln.strip().startswith("|") and i + 1 < len(lines) and _is_sep(lines[i + 1]):
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
    return v is None or v.strip() in EMPTY or v.strip().lower() in {"n/a", "none", "na"}


# ------------------------------------------------------------------ 分镜表

STORYBOARD_COLS = ["段号", "镜号", "时长(s)", "拍数", "内容", "运镜", "运镜因果", "起始帧方位", "对白", "短镜理由"]


LAYOUT_ALIASES = {"左": "LEFT", "左侧": "LEFT", "右": "RIGHT", "右侧": "RIGHT", "中": "CENTER", "中间": "CENTER",
                  "居中": "CENTER", "中央": "CENTER", "CENTRE": "CENTER", "前景": "FG", "背景": "BG",
                  "FOREGROUND": "FG", "BACKGROUND": "BG"}


def _pairs(s: str) -> list[tuple[str, str]]:
    """'a=b; c＝d，e=f' → [('a','b'), ...]：分号/逗号（半角/全角）分隔，等号可全角。"""
    out = []
    for part in re.split(r"[;；,，]", (s or "").replace("＝", "=")):
        if "=" in part:
            k, v = part.split("=", 1)
            out.append((k, v))
    return out


def norm_layout_value(v: str) -> str:
    """左/LEFT→LEFT，右→RIGHT，中/CENTER→CENTER，前景/FG→FG，背景/BG→BG；不认识的值原样大写。"""
    u = unicodedata.normalize("NFKC", v or "").strip().upper()
    return LAYOUT_ALIASES.get(u, LAYOUT_ALIASES.get((v or "").strip(), u))


def parse_layout(s: str) -> dict:
    """'神=LEFT; 苏 晓＝右' → {'神': 'LEFT', '苏晓': 'RIGHT'}（名字去空白，值归一，见 norm_layout_value）"""
    out = {}
    if is_empty(s):
        return out
    for k, v in _pairs(s):
        k = re.sub(r"\s+", "", k)
        if k:
            out[k] = norm_layout_value(v)
    return out


def parse_mapping(s: str) -> dict:
    """'S1=苏晓; S2＝石 神' → {'S1': '苏晓', 'S2': '石神'}（容错同 parse_layout，值不改大小写）"""
    out = {}
    if is_empty(s):
        return out
    for k, v in _pairs(s):
        k = k.strip()
        if k:
            out[k] = re.sub(r"\s+", "", v)
    return out


# 句间分隔：契约写 ' / '；也接受无空格 '/' 或全角 '／'，但只在其后紧跟「说话人：」时才切（台词里的 / 不误切）
RE_DIALOGUE_SEP = re.compile(r"\s+/\s+|\s*[/／]\s*(?=[^\s：:/／][^：:/／]{0,19}[：:])")


def dialogue_sep_issues(s: str) -> list[str]:
    """对白格里不合契约的句间分隔（无空格 / 、全角 ／）原文列表；空 = 合契约。"""
    if is_empty(s):
        return []
    return [m.group(0) for m in RE_DIALOGUE_SEP.finditer(s.strip()) if not re.fullmatch(r"\s+/\s+", m.group(0))]


def parse_dialogue(s: str) -> list[tuple[str, str]]:
    """'苏晓：就是现在！ / 神：……' → [('苏晓', '就是现在！'), ('神', '……')]（也切 '/' '／' + 说话人，见 RE_DIALOGUE_SEP）"""
    if is_empty(s):
        return []
    out = []
    for seg in RE_DIALOGUE_SEP.split(s.strip()):
        if not seg.strip():
            continue
        m = re.match(r"^\s*([^：:]{1,20})[：:]\s*(.+)$", seg)
        out.append((m.group(1).strip(), m.group(2).strip()) if m else ("?", seg.strip()))
    return out


def to_float(v: str) -> float | None:
    """'10.83' / '10.83s' / '10.83秒' → 10.83；nan / inf / 非数字 → None。"""
    try:
        x = float(str(v).strip().rstrip("s").rstrip("秒"))
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def parse_storyboard(path: str | Path) -> list[dict]:
    text = read_text(path)
    rows = find_rows(text, ["镜号", "时长(s)"])
    shots = []
    for r in rows:
        shots.append({
            "seq": r.get("段号", ""), "shot": r.get("镜号", ""),
            "dur": to_float(r.get("时长(s)", "")), "beats": to_float(r.get("拍数", "")),
            "content": r.get("内容", ""), "camera": r.get("运镜", ""), "camera_cause": r.get("运镜因果", ""),
            "layout": parse_layout(r.get("起始帧方位", "")), "layout_raw": r.get("起始帧方位", ""),
            "dialogue": parse_dialogue(r.get("对白", "")), "dialogue_raw": r.get("对白", ""), "short_reason": r.get("短镜理由", ""),
            "line": r["_line"], "file": str(path),
        })
    return shots


# ------------------------------------------------------------------ 视频提示词

RE_SHOT_HEADING = re.compile(r"^##\s+(SHOT-\d{3})\b")
RE_ANY_HEADING = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
RE_SHOTLIKE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(?:镜头|镜号|镜)?\s*[:：]?\s*shot\s*[-_－—–]?\s*(\d+)", re.I)
RE_SHOT_TOKEN = re.compile(r"shot\s*[-_－—–]?\s*\d+", re.I)


class ShotList(list):
    """parse_video_prompts 的返回值：就是 list[dict]，另带 `_suspects`（= suspect_shot_headings 的结果）。"""
    _suspects: list


def suspect_shot_headings(text: str) -> list[dict]:
    """代码块外、像镜头标题却不合 `## SHOT-nnn` 的行（`## SHOT-3` / `### SHOT-004` / `## shot-014` / 全角）
    → [{line, text, suggest, prev}]。区间标题（一行含 ≥2 个 SHOT 号）不算。"""
    out, fence, prev = [], None, None
    for i, ln in enumerate(text.splitlines(), 1):
        fence, is_fence, _ = fence_step(ln, fence)
        if is_fence or fence is not None:
            continue
        ok = RE_SHOT_HEADING.match(ln)
        if ok:
            prev = ok.group(1)
            continue
        n_ln = unicodedata.normalize("NFKC", ln)
        m = RE_SHOTLIKE_HEADING.match(n_ln)
        if m and len(RE_SHOT_TOKEN.findall(n_ln)) == 1:
            out.append({"line": i, "text": ln.strip(), "suggest": f"SHOT-{int(m.group(1)):03d}", "prev": prev})
    return out


def parse_video_prompts(path: str | Path) -> list[dict]:
    """每镜：{shot, meta{}, meta_lines{}, meta_dups[], h3(text), h3_line, sections{name: text}, section_order[], line, file}
    规则：代码块外**任何** Markdown 标题都结束当前镜（不合契约的镜头标题不会把其下元数据并进上一镜）；
    同一镜内同名元数据只认第一条（后来的记入 meta_dups，不覆盖）；围栏按 CommonMark 配对。
    返回 ShotList（list 子类），`_suspects` 为疑似镜头标题列表。"""
    text = read_text(path)
    lines = text.splitlines()
    shots, cur, fence, code_lang, buf, start = ShotList(), None, None, "", [], 0
    for i, ln in enumerate(lines, 1):
        new_fence, is_fence, info = fence_step(ln, fence)
        if fence is None and not is_fence:
            m = RE_SHOT_HEADING.match(ln)
            if m:
                cur = {"shot": m.group(1), "meta": {}, "meta_lines": {}, "meta_dups": [], "h3": None, "h3_line": None,
                       "sections": {}, "section_order": [], "line": i, "file": str(path)}
                shots.append(cur)
                continue
            if RE_ANY_HEADING.match(ln):
                cur = None
                continue
            if cur is not None and cur["h3"] is None:
                mm = re.match(r"^-\s*([^:：]+?)\s*[:：]\s*(.*)$", ln)
                if mm:
                    k, v = mm.group(1).strip(), mm.group(2).strip()
                    if k in cur["meta"]:
                        cur["meta_dups"].append({"key": k, "value": v, "line": i, "first_line": cur["meta_lines"][k]})
                    else:
                        cur["meta"][k], cur["meta_lines"][k] = v, i
            continue
        if fence is None and is_fence:          # 开围栏
            fence, code_lang, buf, start = new_fence, (info.split() or [""])[0], [], i
            continue
        if is_fence:                             # 关围栏
            fence = None
            if cur is not None and code_lang == "h3" and cur["h3"] is None:
                cur["h3"] = "\n".join(buf)
                cur["h3_line"] = start + 1
                _split_sections(cur)
            continue
        buf.append(ln)
    shots._suspects = suspect_shot_headings(text)
    return shots


def _split_sections(shot: dict):
    known = set(H3_SECTIONS) | set(H3_SECTIONS_FL2VA)
    name, acc = None, []
    for ln in shot["h3"].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", ln)
        if m and m.group(1) in known:
            if name:
                shot["sections"][name] = "\n".join(acc).strip()
            name, acc = m.group(1), [m.group(2)]
            shot["section_order"].append(name)
        elif name:
            acc.append(ln)
    if name:
        shot["sections"][name] = "\n".join(acc).strip()


def h3_mode(meta: dict) -> str | None:
    """元数据 `- 模式:` → 'Ref2VA' / 'FL2VA'；缺失返回 None；不认识的值返回原文。"""
    raw = (meta or {}).get("模式", "")
    if is_empty(raw):
        return None
    key = re.sub(r"[\s\-_]", "", unicodedata.normalize("NFKC", raw).split("（")[0].split("(")[0]).upper()
    return H3_MODES.get(key, raw.strip())


def tail_margin(meta: dict) -> float:
    """元数据 `- 尾部余量: 1.3`（秒）→ 1.3；缺失/非法 → 0.0。声明时 提示词时长 = 分镜时长 + 尾部余量（F-H3-18）。"""
    x = to_float((meta or {}).get("尾部余量", ""))
    return x if x is not None and x > 0 else 0.0


def parse_references(s: str) -> list[tuple[int | None, str]]:
    """'1=CHR-A-BOARD; 2=REF-SHOT011-START' → [(1,'CHR-A-BOARD'), (2,'REF-SHOT011-START')]"""
    out = []
    if is_empty(s):
        return out
    for part in re.split(r"[;；，]", s.replace("＝", "=")):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d+)\s*=\s*(.+)$", part)
        out.append((int(m.group(1)), m.group(2).strip()) if m else (None, part))
    return out


RE_DIALOGUE = re.compile(r"<d>\s*\[(?i:chinese)\]\s*(.*?)\s*</d>", re.S)     # 语言标记大小写不敏感
RE_D_BLOCK = re.compile(r"<d>(.*?)</d>", re.S)
RE_D_LANG = re.compile(r"^\s*[\[［【]\s*([A-Za-z][A-Za-z \-]*?)\s*[\]］】]\s*")


def dialogue_text(inner: str) -> str | None:
    """<d> 内文 → 台词：去掉 [Chinese]（任意大小写/全角括号）；无语言标记的保留全文；其他语言标记返回 None。"""
    m = RE_D_LANG.match(inner or "")
    if m:
        if m.group(1).strip().lower() != "chinese":
            return None
        inner = inner[m.end():]
    return (inner or "").strip()


def dialogue_from_h3(h3: str) -> list[str]:
    """h3 中全部中文 <d> 台词（含缺语言标记的 <d>，只取文本）。"""
    out = []
    for m in RE_D_BLOCK.finditer(h3 or ""):
        t = dialogue_text(m.group(1))
        if t is not None:
            out.append(t)
    return out


def dialogue_tag_issues(h3: str) -> list[dict]:
    """不合契约 `<d>[Chinese] 台词</d>`（同一行闭合）的标记 → [{kind, text, line}]，line 从 h3 首行计 1。
    kind：no-lang 缺语言标记 / lang-case [chinese] 大小写 / lang-bracket 全角括号 / tag-case <D> 或带空格 /
          multiline 跨行闭合 / unclosed 未闭合 / stray-close 多余 </d> / empty 空台词。"""
    h3 = h3 or ""
    out = []

    def line_of(off: int) -> int:
        return h3.count("\n", 0, off) + 1

    for m in RE_D_BLOCK.finditer(h3):
        inner, snip = m.group(1), m.group(0)
        if "\n" in inner:
            out.append({"kind": "multiline", "text": snip, "line": line_of(m.start())})
        lm = RE_D_LANG.match(inner)
        if not lm:
            out.append({"kind": "no-lang", "text": snip, "line": line_of(m.start())})
        else:
            tag = lm.group(0).strip()
            if tag[0] != "[" or tag[-1] != "]":
                out.append({"kind": "lang-bracket", "text": snip, "line": line_of(m.start())})
            elif lm.group(1).strip().lower() == "chinese" and lm.group(1).strip() != "Chinese":
                out.append({"kind": "lang-case", "text": snip, "line": line_of(m.start())})
        if dialogue_text(inner) == "":
            out.append({"kind": "empty", "text": snip, "line": line_of(m.start())})
    rest = RE_D_BLOCK.sub(lambda m: " " * len(m.group(0)), h3)
    for m in re.finditer(r"<d>", rest):
        out.append({"kind": "unclosed", "text": rest[m.start():m.start() + 40].split("\n")[0], "line": line_of(m.start())})
    for m in re.finditer(r"</d>", rest):
        out.append({"kind": "stray-close", "text": "</d>", "line": line_of(m.start())})
    for m in re.finditer(r"<\s*/?\s*[dD]\s*>", rest):
        if m.group(0) not in ("<d>", "</d>"):
            out.append({"kind": "tag-case", "text": m.group(0), "line": line_of(m.start())})
    return sorted(out, key=lambda x: x["line"])


# ------------------------------------------------------------------ 锚点卡 / 剪辑单

def parse_anchors(path: str | Path) -> dict:
    """`## ANCHOR: CHR-X`（冒号可全角）→ {id: {id, line, fields{}}}。代码块外任何标题都结束当前卡；
    锚点句 EN 剥一到两层反引号。"""
    text = read_text(path)
    anchors, cur, fence = {}, None, None
    for i, ln in enumerate(text.splitlines(), 1):
        fence, is_fence, _ = fence_step(ln, fence)
        if is_fence or fence is not None:
            continue
        m = re.match(r"^##\s+ANCHOR\s*[:：]\s*([A-Z]{3}-[A-Z0-9-]+)\s*$", ln)
        if m:
            cur = {"id": m.group(1), "line": i, "fields": {}}
            anchors[cur["id"]] = cur
            continue
        if RE_ANY_HEADING.match(ln):
            cur = None
            continue
        if cur:
            mm = re.match(r"^-\s*([^:：]+?)\s*[:：]\s*(.*)$", ln)
            if mm:
                key, val = mm.group(1).strip(), mm.group(2).strip()
                if key == "锚点句 EN":
                    bt = re.match(r"^`{1,2}\s*(.+?)\s*`{1,2}$", val)
                    val = bt.group(1) if bt else val
                cur["fields"][key] = val
    return anchors


def parse_edit_list(path: str | Path) -> list[dict]:
    text = read_text(path)
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
    """返回 ≥ sec 的最小合法帧数（容忍 DISPLAY_TOL=0.005s 显示舍入：5.17 → 124 帧，不是 141）；超过 362 帧返回 None（需拆段）。"""
    for n in grid_frames():
        if frames_to_seconds(n) + DISPLAY_TOL + 1e-9 >= sec:
            return n
    return None


def snap_seconds_nearest(sec: float) -> int:
    """最近的合法帧数；与某网格值相差 ≤ DISPLAY_TOL 时直接取该值（两位小数显示值吸附回原帧数）。"""
    for n in grid_frames():
        if abs(frames_to_seconds(n) - sec) <= DISPLAY_TOL + 1e-9:
            return n
    return min(grid_frames(), key=lambda n: abs(frames_to_seconds(n) - sec))


# ------------------------------------------------------------------ ffmpeg

def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def run(cmd: list[str], timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)


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
