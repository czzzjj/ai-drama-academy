#!/usr/bin/env python3
"""segment_rhythm.py — 分镜段/拍/镜节奏结构检查（设计阶段，送 H3 之前）

用途：
  读 storyboard.md，按"段（SEQ）→ 镜（SHOT）→ 拍"三层统计节奏结构，拦截委托方真实踩过的结构性坑：
  碎镜（镜太短、均长太短）、超过 H3 单次上限的镜、拍数过多导致空间跳变、说不出因果的运镜。
  只报告事实（时长、拍数、比例、句式是否成立）与改法（合并/拆分/补理由/改写因果句），
  不判断"节奏好不好看"——那是审片与冷观众的事。

溯源：A1（碎镜症：29 镜均长 2.96s；"任何 ≤3s 的镜必须给出理由"；段长 ≥5s 起步，124 帧硬下限）、
      A4（运镜与叙事脱钩：运镜审查用"因为发生了 X，所以镜头做了 Y"因果句过一遍）、
      A5（空间调度混乱③：节拍太多 → 空间连续跳变）、
      P10 / M1（长段多拍：8–15s 段、段内 2–3 拍、一条完整动作链，连续动作不切新镜）、
      T-2（H3 训练区间 124–362 帧 = 5.17–15.08s）。

判定（逐镜）：
  error  A1-short-no-reason   时长 < 5.17s（124 帧下限）且 `短镜理由` 为空或只是占位（—、——、无、待定、TBD…）
  info   A1-short-with-reason 时长 < 5.17s 且写了短镜理由（提醒：不送 H3 / 本地生成）
  error  T2-over-max          时长 > 15.08s（362 帧单次上限）→ 拆镜
  error  A1-duration-missing  时长缺失、不是有限数字（nan/inf）或 ≤0
  warn   A5-beats-many        拍数 > 3（A5③ 空间连续跳变风险）
  warn   P10-beats-missing    拍数为空或不是正整数
  info   P10-beats-chain      `内容` 中 → 串起的链节数 ≠ 拍数（仅提示核对）
  error  A4-cause             `运镜因果` 不是"因为 X，所以 Y"句式（所在表缺这一列时只报 FMT-columns，不逐镜重复报）
  warn   P10-seq-missing      段号为空（每镜必须归属一个段）
  error  FMT-dup-shot / FMT-columns / FMT-empty / FMT-header   镜号重复 / 某张分镜表缺契约列 / 表内无行 / 表头笔误
  warn   FMT-bom / FMT-value / FMT-shot-id   BOM / 值带反引号等非契约写法（已按值检查）/ 镜号不是 SHOT-nnn
判定（全局）：
  error  A1-mean-short        平均镜长 < 5.0s → "碎镜症（A1 实证：29 镜均长 2.96s）"
  warn   A1-short-share       < 5s 的短镜占比 > 20%
  info   A1-stats             镜数、段数、均长、有效拍数（Σ拍数）、短镜占比

输入格式：70-playbooks/format-contracts.md §1「分镜表（storyboard.md）」——
  表头 `段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由`（列顺序不限）。
  解析统一使用 academy_common.parse_storyboard / parse_md_tables。
  输入容错（只为不漏检/不误报，不放宽契约，偏差一律报 FMT-*）：UTF-8 BOM（academy_common 会因此读不到首行表头）、
  值带反引号/加粗/全角数字、表格末尾的模板空行、多张分镜表各自缺列。

用法示例：
  python3 segment_rhythm.py season-01/ep03/storyboard.md
  python3 segment_rhythm.py storyboard.md --json
  python3 segment_rhythm.py storyboard.md --min-mean 5.0 --max-short-share 0.2 --max-beats 3
  python3 segment_rhythm.py --selftest

退出码：0 通过 / 1 发现问题（存在 error）/ 2 用法或环境错误。
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "段/拍/镜节奏结构（A1 / A4 / A5 / P10）"
MIN_SEC = ac.frames_to_seconds(ac.H3_MIN_FRAMES)   # 5.1667 → 文档写作 5.17
MAX_SEC = ac.frames_to_seconds(ac.H3_MAX_FRAMES)   # 15.0833 → 文档写作 15.08
DISPLAY_TOL = 0.005
REQUIRED_COLS = ["段号", "镜号", "时长(s)", "拍数", "运镜因果", "短镜理由"]
RE_CAUSE = re.compile(r"因[为為](.+?)所以(.+)", re.S)
RE_PUNCT_ONLY = re.compile(r"^[\s，,。.、；;：:…—\-]*$")
RE_DASHES = re.compile(r"^[\s\-—–―－~～_]+$")
REASON_PLACEHOLDERS = {"无", "(无)", "无理由", "待定", "待补", "待填", "略", "tbd", "todo", "?", "none", "null", "n/a", "na"}
RE_SHOT_ID = re.compile(r"^SHOT-\d{3}$")
RE_SHOT_LOOSE = re.compile(r"^\s*shot\s*[-_－—–]?\s*0*(\d{1,4})(?!\d)", re.I)


@dataclass
class Params:
    min_mean: float = 5.0          # A1：均长 < 5.0s → 碎镜症
    short_sec: float = 5.0         # 统计"短镜占比"的阈值（A1、format-contracts §1：< 5s 必填短镜理由）
    max_short_share: float = 0.20  # 〔学院推断〕短镜占比上限
    max_beats: int = 3             # P10：段内 2–3 拍为常态；A5③


def snap_up(sec: float) -> int | None:
    return ac.snap_seconds_up(sec)        # academy_common 已内置 0.005s 显示容差


def sec_s(n: int) -> str:
    return f"{ac.frames_to_seconds(n):.2f}"


def cause_ok(s: str) -> bool:
    if ac.is_empty(s):
        return False
    m = RE_CAUSE.search(s)
    return bool(m) and not RE_PUNCT_ONLY.match(m.group(1)) and not RE_PUNCT_ONLY.match(m.group(2))


def split_text(dur: float, beats: int | None) -> str:
    parts = max(2, math.ceil(dur / MAX_SEC - 1e-9))
    each = snap_up(dur / parts)
    if each is None:
        return f"拆成 {parts} 镜（每镜 ≤15.08s）"
    if parts == 2:
        how = f"在第 {max(1, (beats or 2) // 2)} 拍后" if beats and beats >= 2 else "在拍与拍之间"
    else:
        how = "按拍"
    return (f"{how}拆成 {parts} 镜（每镜 ≈{dur / parts:.2f}s → {each} 帧 / {sec_s(each)}s），"
            f"不切断连续动作（P10）；或删拍压到 ≤15.08s（362 帧）")


# ------------------------------------------------------------------ 输入容错（只为不漏检/不误报）

def read_doc(path: Path) -> tuple[str, bool]:
    text = path.read_text(encoding="utf-8")
    return (text[1:], True) if text.startswith("﻿") else (text, False)


def parse_compat(path: Path, text: str, had_bom: bool) -> list[dict]:
    """academy_common.parse_storyboard 的 BOM 兼容包装：带 BOM 时解析去 BOM 的临时副本（行号不变）。"""
    if not had_bom:
        return ac.parse_storyboard(path)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / path.name
        tmp.write_text(text, encoding="utf-8")
        shots = ac.parse_storyboard(tmp)
    for s in shots:
        s["file"] = str(path)
    return shots


def bom_finding(path: Path) -> ac.Finding:
    return ac.Finding("warn", "FMT-bom",
                      f"{path.name} 以 UTF-8 BOM 开头（format-contracts §0.1：UTF-8 无 BOM）。本脚本已去 BOM 解析，"
                      f"但 academy_common 的其他脚本会读不到首行表头 → 整表漏检。去掉 BOM："
                      f"`sed -i '1s/^\\xEF\\xBB\\xBF//' {path.name}`，或编辑器另存为「UTF-8（无 BOM）」", path.name)


def _nk(s: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s)).lower()


ALIAS = {"时长(秒)": "时长(s)", "时长": "时长(s)", "时长s": "时长(s)", "时长(sec)": "时长(s)", "镜头": "镜号",
         "镜头号": "镜号", "shot": "镜号", "节拍": "拍数", "拍": "拍数", "段": "段号", "运镜理由": "运镜因果",
         "短镜原因": "短镜理由", "台词": "对白"}


def near_miss(header: list[str]) -> dict[str, str]:
    """{契约列名: 表里的近似写法}（全角括号、多空格、常见别名）。"""
    want = {_nk(c): c for c in ac.STORYBOARD_COLS}
    out = {}
    for h in header:
        tgt = want.get(_nk(h)) or ALIAS.get(_nk(h))
        if tgt and tgt != h and tgt not in header:
            out[tgt] = h
    return out


def header_hints(text: str) -> list[str]:
    """academy_common 认不出的"分镜表"（表头笔误 / 全角竖线）→ 每张表一条可执行改法。
    这些表的行会被 academy_common 整表跳过，不报就是漏检（哪怕同文件里还有一张正常的表）。"""
    out = []
    for t in ac.parse_md_tables(text):
        if "镜号" in t["header"] and "时长(s)" in t["header"]:
            continue   # 认得出的表：个别列笔误由 FMT-columns 报
        nm = near_miss(t["header"])
        present = {c for c in ac.STORYBOARD_COLS if c in t["header"]} | set(nm)
        if nm and {"镜号", "时长(s)"} <= present:
            fixes = "；".join(f"`{v}` → `{k}`" for k, v in nm.items())
            out.append(f"第 {t['line']} 行分镜表头与契约不一致：{fixes}（format-contracts §1：列名逐字一致，括号用半角）；"
                       f"修正前这张表的 {len(t['rows'])} 行未被任何脚本检查")
    in_code = False
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and "｜" in ln and "镜号" in ln and "时长" in ln:
            out.append(f"第 {i} 行表格用了全角竖线「｜」：改为半角「|」（format-contracts §0.3）；修正前这张表未被任何脚本检查")
    return out


def _clean_value(v: str) -> str:
    s = unicodedata.normalize("NFKC", str(v)).strip().strip("`*_\"' ")
    return re.sub(r"\s*\(.*\)\s*$", "", s).strip("`*_\"' ")


def parse_number(v: str | None) -> tuple[float | None, bool, str]:
    """返回 (数值, 是否契约写法, 无法使用的原因)。nan/inf → None。"""
    if v is None or ac.is_empty(v):
        return None, True, "缺失"
    x, plain = ac.to_float(v), True
    if x is None:
        plain = False
        try:
            x = float(re.sub(r"\s*(s|秒|sec|secs|seconds|拍)$", "", _clean_value(v), flags=re.I))
        except ValueError:
            return None, False, "不是数字"
    if not math.isfinite(x):
        return None, plain, "不是有限数字"
    return x, plain, ""


def blank_reason(v: str | None) -> bool:
    if ac.is_empty(v):
        return True
    t = unicodedata.normalize("NFKC", v).strip().rstrip("。.").lower()
    return bool(RE_DASHES.match(t)) or t in REASON_PLACEHOLDERS


def canon_id(raw: str) -> tuple[str, bool]:
    s = (raw or "").strip()
    if RE_SHOT_ID.match(s):
        return s, True
    m = RE_SHOT_LOOSE.match(unicodedata.normalize("NFKC", s))
    return (f"SHOT-{int(m.group(1)):03d}", False) if m else (s, False)


# ------------------------------------------------------------------ 分析

def load(path: Path, fs: list[ac.Finding]) -> list[dict] | None:
    """解析分镜并附上原始单元格/所在表头；表头笔误时报 FMT-header 并返回 None；根本不是分镜时 die。"""
    text, had_bom = read_doc(path)
    if had_bom:
        fs.append(bom_finding(path))
    tables = [t for t in ac.parse_md_tables(text) if "镜号" in t["header"] and "时长(s)" in t["header"]]
    hints = header_hints(text)
    for h in hints:
        fs.append(ac.Finding("error", "FMT-header", h, path.name))
    if not tables:
        if hints:
            return None
        ac.die(f"{path} 中没有分镜表（表头需含 `镜号` 与 `时长(s)`，见 70-playbooks/format-contracts.md §1）")
    row_of: dict[int, tuple[dict, dict]] = {}
    for t in tables:
        missing = [c for c in REQUIRED_COLS if c not in t["header"]]
        if missing:
            nm = near_miss(t["header"])
            hints = [f"`{nm[c]}` → `{c}`" for c in missing if c in nm]
            fs.append(ac.Finding("error", "FMT-columns",
                                 f"第 {t['line']} 行的分镜表缺契约列：{', '.join(missing)}"
                                 + (f"（疑似笔误：{'；'.join(hints)}）" if hints else "")
                                 + "。按 format-contracts §1 补齐列（空值写 —）后重跑；缺列对应的逐镜检查已跳过",
                                 f"{path.name}:{t['line']}", {"missing": missing}))
        for r in t["rows"]:
            row_of[r["_line"]] = (t, r)
    out = []
    for s in parse_compat(path, text, had_bom):
        t, raw = row_of.get(s["line"], ({"header": []}, {}))
        if all(ac.is_empty(raw.get(c)) for c in ("镜号", "时长(s)", "拍数", "内容", "运镜因果")):
            continue   # 模板空行
        dur, d_plain, d_why = parse_number(raw.get("时长(s)"))
        beats, b_plain, _ = parse_number(raw.get("拍数"))
        if dur is not None and dur <= 0:
            dur, d_why = None, "≤0"
        b_int = int(beats) if beats is not None and beats == int(beats) and beats >= 1 else None
        out.append({**s, "dur": dur, "dur_why": d_why, "dur_plain": d_plain, "beats_n": b_int,
                    "beats_plain": b_plain, "raw": raw, "hdr": set(t["header"])})
    return out


def analyze(path: str | Path, p: Params) -> tuple[list[ac.Finding], dict]:
    path = Path(path)
    fs: list[ac.Finding] = []
    shots = load(path, fs)
    empty_extra = {"segments": [], "stats": {}, "summary": ""}
    if shots is None:
        return fs, empty_extra
    if not shots:
        fs.append(ac.Finding("error", "FMT-empty", "分镜表没有任何镜行：先填表再检查", path.name))
        return fs, empty_extra

    seen: dict[str, int] = {}
    for s in shots:
        raw, hdr = s["raw"], s["hdr"]
        sid, id_ok = canon_id(s["shot"])
        where = f"{s['shot'] or '?'} · {path.name}:{s['line']}"
        dur, beats = s["dur"], s["beats_n"]
        data = {"shot": s["shot"], "seq": s["seq"], "duration": dur, "beats": beats, "line": s["line"]}

        if ac.is_empty(s["shot"]):
            sid = ""
            fs.append(ac.Finding("error", "FMT-shot-id", "镜号为空：填集内唯一的 SHOT-nnn（三位数字）", where, data))
        elif not id_ok:
            fs.append(ac.Finding("warn", "FMT-shot-id",
                                 f"镜号 '{s['shot']}' 不合契约 `SHOT-nnn`（三位数字）" + (f"：改为 {sid}" if sid != s["shot"].strip() else "")
                                 + "，否则与 video-prompts.md 的 `## SHOT-nnn` 对不上（P7）", where, data))
        if sid and sid in seen:
            fs.append(ac.Finding("error", "FMT-dup-shot",
                                 f"镜号 {s['shot']} 与第 {seen[sid]} 行重复（集内必须唯一）：重新编号并全仓同步替换（E2）",
                                 where, data))
        elif sid:
            seen[sid] = s["line"]
        if "段号" in hdr and ac.is_empty(s["seq"]):
            fs.append(ac.Finding("warn", "P10-seq-missing",
                                 "段号为空：每镜必须归属一个段（一段 = 一条完整动作链/一场戏的一个单元，P10）。填 SEQ-nn",
                                 where, data))

        # 时长
        if dur is None:
            fs.append(ac.Finding("error", "A1-duration-missing",
                                 f"时长(s) {s['dur_why']}（'{raw.get('时长(s)', '')}'）：填 >0 的秒数（两位小数），"
                                 f"并用 h3_frame_grid.py --seconds 吸附到网格", where, data))
        else:
            if not s["dur_plain"]:
                fs.append(ac.Finding("warn", "FMT-value",
                                     f"时长(s) 写成 '{raw.get('时长(s)')}'，已按 {dur:g} 检查；契约要求纯数字（{dur:g}），"
                                     f"否则其他脚本读不到", where, data))
            if dur + DISPLAY_TOL < MIN_SEC:
                if blank_reason(s["short_reason"]):
                    got = "" if ac.is_empty(s["short_reason"]) else f"（只写了占位「{s['short_reason']}」）"
                    nocol = "" if "短镜理由" in hdr else "（表中没有 `短镜理由` 列）"
                    fs.append(ac.Finding("error", "A1-short-no-reason",
                                         f"{dur:.2f}s < 5.17s（H3 124 帧下限，T-2）且未填短镜理由{got}{nocol}"
                                         f"（A1：任何 ≤3s 的镜必须给出理由）。"
                                         f"改法任选：①并入同段相邻镜，做成一条 8–15s 的长段多拍（P10）；②改为 ≥5.17s（124 帧）；"
                                         f"③若确为插入/纯色卡等本地生成镜，在 `短镜理由` 写明且不送 H3（D2）",
                                         where, data))
                else:
                    fs.append(ac.Finding("info", "A1-short-with-reason",
                                         f"{dur:.2f}s < 5.17s，短镜理由：「{s['short_reason']}」。确认此镜不进 video-prompts.md"
                                         f"（本地生成）；若要送 H3，只能出 124 帧（5.17s）",
                                         where, data))
            elif dur - DISPLAY_TOL > MAX_SEC:
                fs.append(ac.Finding("error", "T2-over-max",
                                     f"{dur:.2f}s > 15.08s（H3 单次上限 362 帧，T-2）：{split_text(dur, beats)}",
                                     where, data))

        # 拍数
        if "拍数" in hdr:
            if beats is None:
                fs.append(ac.Finding("warn", "P10-beats-missing",
                                     f"拍数为空或不是正整数（'{raw.get('拍数', '')}'）："
                                     f"按 `内容` 中 → 串起的动作节数填一个整数（段内 2–3 拍为常态，P10）",
                                     where, data))
            else:
                if not s["beats_plain"]:
                    fs.append(ac.Finding("warn", "FMT-value",
                                         f"拍数写成 '{raw.get('拍数')}'，已按 {beats} 检查；契约要求纯整数", where, data))
                if beats > p.max_beats:
                    fs.append(ac.Finding("warn", "A5-beats-many",
                                         f"拍数 {beats} > {p.max_beats}（A5③：节拍太多 → 空间连续跳变）。减到 2–3 拍，多出的拍移到下一镜"
                                         f"或删去重复接近/翻滚/换向；若必须保留，在 `内容` 中写明空间如何不跳变（format-contracts §1）",
                                         where, data))
                content = s["content"] or ""
                if "→" in content:
                    chain = content.count("→") + 1
                    if chain != beats:
                        fs.append(ac.Finding("info", "P10-beats-chain",
                                             f"`内容` 用 → 串了 {chain} 节，拍数写 {beats}：核对二者是否一致（不一致时以实际动作链为准改拍数）",
                                             where, {**data, "chain": chain}))

        # 运镜因果（A4）
        if "运镜因果" in hdr and not cause_ok(s["camera_cause"]):
            cc = s["camera_cause"] if not ac.is_empty(s["camera_cause"]) else "（空）"
            fs.append(ac.Finding("error", "A4-cause",
                                 f"运镜因果「{cc}」不是\"因为 X，所以 Y\"句式（A4：说不出叙事理由 = 炫技或脱钩）。"
                                 f"改写为：因为<画面中发生的事件>，所以镜头<{s['camera'] or '怎么动'}>；静止镜写\"因为……，所以不动\"；"
                                 f"写不出事件，就把运镜改为固定",
                                 where, data))

    # 段汇总
    segs: dict[str, dict] = {}
    for s in shots:
        key = s["seq"] if not ac.is_empty(s["seq"]) else "（无段号）"
        g = segs.setdefault(key, {"seq": key, "shots": [], "duration": 0.0, "beats": 0, "beats_unknown": 0,
                                  "duration_unknown": 0})
        g["shots"].append(s["shot"])
        if s["dur"] is None:
            g["duration_unknown"] += 1
        else:
            g["duration"] += s["dur"]
        if s["beats_n"] is None:
            g["beats_unknown"] += 1
        else:
            g["beats"] += s["beats_n"]
    for g in segs.values():
        g["duration"] = round(g["duration"], 2)
        g["n_shots"] = len(g["shots"])

    # 全局（只用有效时长）
    durs = [s["dur"] for s in shots if s["dur"] is not None]
    n = len(durs)
    mean = sum(durs) / n if n else 0.0
    total = sum(durs)
    beats_total = sum(s["beats_n"] for s in shots if s["beats_n"] is not None)
    short = [s for s in shots if s["dur"] is not None and s["dur"] < p.short_sec - 1e-9]
    share = len(short) / n if n else 0.0
    stats = {"shots": len(shots), "segments": len(segs), "total_sec": round(total, 2), "mean_sec": round(mean, 2),
             "effective_beats": beats_total, "beats_per_min": round(beats_total / total * 60, 1) if total else 0.0,
             "short_shots": [s["shot"] for s in short], "short_share": round(share, 3),
             "invalid_duration_shots": [s["shot"] for s in shots if s["dur"] is None]}

    merge = merge_candidates(shots, p)
    merge_txt = ("；可合并候选：" + "；".join(merge)) if merge else ""
    if n and mean < p.min_mean - 1e-9:
        fs.append(ac.Finding("error", "A1-mean-short",
                             f"碎镜症（A1 实证：29 镜均长 2.96s）：本集 {n} 镜均长 {mean:.2f}s < {p.min_mean:g}s。"
                             f"把同一动作链上的相邻短镜合并成 8–15s 的长段多拍（段内 2–3 拍，P10/M1）{merge_txt}",
                             "全局", stats))
    if n and share > p.max_short_share + 1e-9:
        fs.append(ac.Finding("warn", "A1-short-share",
                             f"< {p.short_sec:g}s 的短镜 {len(short)}/{n} = {share:.0%} > {p.max_short_share:.0%}："
                             f"{', '.join(stats['short_shots'])}。逐个确认是否有短镜理由且不送 H3；"
                             f"无理由的并入相邻镜{merge_txt}",
                             "全局", stats))
    bad_n = len(stats["invalid_duration_shots"])
    fs.append(ac.Finding("info", "A1-stats",
                         f"{len(shots)} 镜 / {len(segs)} 段；总长 {total:.2f}s；均长 {mean:.2f}s"
                         + (f"（{bad_n} 镜时长无效，未计入）" if bad_n else "")
                         + f"；有效拍数 {beats_total}（{stats['beats_per_min']} 拍/分钟）；短镜占比 {share:.0%}",
                         "全局", stats))

    seg_list = list(segs.values())
    return fs, {"segments": seg_list, "stats": stats, "summary": seg_table(seg_list)}


def merge_candidates(shots: list[dict], p: Params) -> list[str]:
    """同段内连续的短镜（<short_sec）→ 合并候选（合计时长吸附到网格）。"""
    out, run = [], []

    def flush():
        if len(run) >= 2:
            tot = sum(x["dur"] for x in run)
            up = snap_up(tot)
            tgt = f"{up} 帧 / {sec_s(up)}s" if up else "超过 15.08s，合并后再按拍拆两镜"
            out.append(f"{run[0]['seq']} 的 {run[0]['shot']}…{run[-1]['shot']}（{len(run)} 镜共 {tot:.2f}s → {tgt}）")

    prev_seq = None
    for s in shots:
        is_short = s["dur"] is not None and s["dur"] < p.short_sec - 1e-9
        if is_short and run and s["seq"] == prev_seq and not ac.is_empty(s["seq"]):
            run.append(s)
        else:
            flush()
            run = [s] if is_short else []
        prev_seq = s["seq"]
    flush()
    return out[:6] + ([f"……另有 {len(out) - 6} 组"] if len(out) > 6 else [])


def _pad(v, w: int, right: bool = False) -> str:
    """按终端显示宽度补齐（中日韩全角字符占 2 列）。"""
    s = str(v)
    fill = " " * max(0, w - sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s))
    return fill + s if right else s + fill


def seg_table(segs: list[dict]) -> str:
    out = ["段汇总：", "  " + _pad("段号", 12) + _pad("镜数", 6, True) + _pad("总时长s", 10, True)
           + _pad("拍数", 6, True) + "  镜号"]
    for g in segs:
        beats = f"{g['beats']}" + (f"+?{g['beats_unknown']}" if g["beats_unknown"] else "")
        dur = f"{g['duration']:.2f}" + (f"+?{g['duration_unknown']}" if g["duration_unknown"] else "")
        shots = ", ".join(g["shots"]) if len(g["shots"]) <= 4 else f"{g['shots'][0]} … {g['shots'][-1]}"
        out.append("  " + _pad(g["seq"], 12) + _pad(g["n_shots"], 6, True) + _pad(dur, 10, True)
                   + _pad(beats, 6, True) + "  " + shots)
    return "\n".join(out)


# ------------------------------------------------------------------ 自测

HEADER = ("| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |\n"
          "|---|---|---|---|---|---|---|---|---|---|\n")


def row(seq, shot, dur, beats, cause="因为异响出现，所以推近", reason="—", content="走→停"):
    return f"| {seq} | {shot} | {dur} | {beats} | {content} | 缓推 | {cause} | — | — | {reason} |\n"


def selftest() -> int:
    results: list[tuple[bool, str]] = []
    p = Params()

    def check(cond: bool, label: str):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    def codes(fs, level):
        return {(f.code, f.where.split(" · ")[0]) for f in fs if f.level == level}

    G, B = ac.FIXTURES / "good" / "storyboard.md", ac.FIXTURES / "bad" / "storyboard.md"
    gfs, gx = analyze(G, p)
    check(not codes(gfs, "error"), "fixtures/good → 0 error")
    check(("A1-short-with-reason", "SHOT-004") in codes(gfs, "info"), "good SHOT-004 3.00s 有短镜理由 → 只出 info")
    check(gx["stats"]["shots"] == 4 and gx["stats"]["effective_beats"] == 8 and len(gx["segments"]) == 3,
          "good 统计：4 镜 / 3 段 / 有效拍数 8")

    bfs, bx = analyze(B, p)
    expect = {("A1-short-no-reason", "SHOT-001"), ("A4-cause", "SHOT-003"),
              ("T2-over-max", "SHOT-004"), ("A1-short-no-reason", "SHOT-005")}
    check(codes(bfs, "error") == expect,
          "fixtures/bad → error 恰为：SHOT-001 短镜无理由、SHOT-003 运镜因果「很酷」、SHOT-004 16s 超上限、SHOT-005 4.2s 无理由")
    check(("A5-beats-many", "SHOT-003") in codes(bfs, "warn"), "bad SHOT-003 5 拍 → A5-beats-many")
    check(("A1-short-share", "全局") in codes(bfs, "warn") and bx["stats"]["short_share"] == 0.4,
          "bad 短镜占比 2/5 = 40% → A1-short-share")
    over = next(f for f in bfs if f.code == "T2-over-max")
    check("192 帧" in over.msg, "bad SHOT-004 16s → 建议拆成 2×192 帧（8.00s）")

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def doc(name: str, body: str = "", raw: bytes | None = None) -> Path:
            q = tdp / name
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_bytes(raw if raw is not None else body.encode("utf-8"))
            return q

        # A1 实证复现：29 镜均长 2.96s
        rows = []
        for k in range(29):
            d = 2.96 if k == 28 else (2.46 if k % 2 == 0 else 3.46)
            rows.append(row(f"SEQ-{k // 5 + 1:02d}", f"SHOT-{k + 1:03d}", f"{d:.2f}", 1, content="出刀"))
        a1 = doc("a1.md", "# A1 复现\n\n" + HEADER + "".join(rows))
        fs, x = analyze(a1, p)
        mean_f = next((f for f in fs if f.code == "A1-mean-short"), None)
        check(mean_f is not None and abs(x["stats"]["mean_sec"] - 2.96) < 0.005 and x["stats"]["shots"] == 29,
              "A1 复现：29 镜均长 2.96s → error A1-mean-short（碎镜症）")
        check(mean_f is not None and "可合并候选" in mean_f.msg and "SEQ-01 的 SHOT-001…SHOT-005" in mean_f.msg,
              "A1 复现：报告给出同段连续短镜的合并候选（SEQ-01 SHOT-001…005）")
        check(sum(1 for f in fs if f.code == "A1-short-no-reason") == 29, "A1 复现：29 个短镜均无理由 → 29 条 A1-short-no-reason")

        # 边界与格式
        edge = doc("edge.md", HEADER
                   + row("SEQ-01", "SHOT-001", "5.17", 2)
                   + row("SEQ-01", "SHOT-002", "5.10", 2)
                   + row("SEQ-02", "SHOT-003", "15.08", 3, content="a→b→c")
                   + row("SEQ-02", "SHOT-004", "15.09", 2)
                   + row("SEQ-03", "SHOT-005", "8.00", "", cause="所以推近，因为她回头")
                   + row("SEQ-03", "SHOT-006", "8.00", 2, cause="因为，所以")
                   + row("—", "SHOT-006", "8.00", 2, content="a→b→c"))
        fs, _ = analyze(edge, p)
        e, w = codes(fs, "error"), codes(fs, "warn")
        check(("A1-short-no-reason", "SHOT-002") in e and not any(c[1] == "SHOT-001" for c in e),
              "边界：5.17s 通过，5.10s 无理由 → A1-short-no-reason")
        check(("T2-over-max", "SHOT-004") in e and not any(c[1] == "SHOT-003" for c in e),
              "边界：15.08s 通过，15.09s → T2-over-max")
        check(("P10-beats-missing", "SHOT-005") in w, "拍数为空 → P10-beats-missing")
        check(("A4-cause", "SHOT-005") in e and ("A4-cause", "SHOT-006") in e,
              "「所以…因为…」倒装、「因为，所以」空壳 → A4-cause")
        check(("FMT-dup-shot", "SHOT-006") in e and ("P10-seq-missing", "SHOT-006") in w,
              "镜号重复 → FMT-dup-shot；段号为 — → P10-seq-missing")
        check(any(f.code == "P10-beats-chain" for f in fs), "内容 → 链节数 ≠ 拍数 → P10-beats-chain info")

        cols = doc("cols.md", "| 镜号 | 时长(s) |\n|---|---|\n| SHOT-001 | 8.00 |\n")
        fs, _ = analyze(cols, p)
        check(any(f.code == "FMT-columns" for f in fs) and not any(f.code == "A4-cause" for f in fs),
              "缺契约列 → FMT-columns，且不再逐镜重复报 A4-cause（修复前：每镜一条'运镜因果（空）'）")

        # 对抗：占位理由 / 非有限时长 / 非契约值写法 / 镜号 / 多表 / 模板空行
        adv = doc("adv.md", "# 分镜\n\n" + HEADER
                  + row("SEQ-01", "SHOT-001", "3.00", 1, reason="——")
                  + row("SEQ-01", "SHOT-002", "nan", 2, content="a→b")
                  + row("SEQ-01", "SHOT-003", "-3", 2, content="a→b")
                  + row("SEQ-01", "SHOT-004", "8.00", "2-3", content="a→b", cause="因為石神倒下，所以拉回")
                  + row("SEQ-01", "SHOT-005", "inf", 2, content="a→b")
                  + row("SEQ-01", "SHOT-006", "`8.00`", "**2**", content="a→b")
                  + row("SEQ-01", "SHOT-8", "8.00", 2, content="a→b")
                  + row("SEQ-01", "SHOT-008", "8.00", 2, content="a→b")
                  + row("SEQ-01", "SHOT-009", "4.00", 1, reason="TBD")
                  + row("SEQ-01", "SHOT-010", "45.00", 6, content="a→b→c→d→e→f")
                  + "|  |  |  |  |  |  |  |  |  |  |\n"
                  + "\n## 第二段（另一张表，缺列）\n\n| 段号 | 镜号 | 时长(s) | 拍数 | 内容 |\n|---|---|---|---|---|\n"
                  + "| SEQ-02 | SHOT-011 | 8.00 | 2 | a→b |\n")
        fs, x = analyze(adv, p)
        e, w = codes(fs, "error"), codes(fs, "warn")
        check(("A1-short-no-reason", "SHOT-001") in e and ("A1-short-no-reason", "SHOT-009") in e,
              "短镜理由只写 `——` / `TBD` → 视为未填 → A1-short-no-reason（修复前：'——'被当成理由放行）")
        check({("A1-duration-missing", s) for s in ("SHOT-002", "SHOT-003", "SHOT-005")} <= e
              and not any(c == ("A1-short-no-reason", "SHOT-003") for c in e),
              "时长 nan / -3 / inf → A1-duration-missing（修复前：nan 静默通过、-3 被报成短镜、inf 报'infs'）")
        check("nan" not in x["summary"] and "inf" not in x["summary"] and x["stats"]["mean_sec"] == 11.5
              and x["stats"]["invalid_duration_shots"] == ["SHOT-002", "SHOT-003", "SHOT-005"],
              "统计只用有效时长（8 镜共 92s → 均长 11.50s），段汇总无 nan/inf，并列出时长无效的镜")
        b4 = next((f for f in fs if f.code == "P10-beats-missing" and "SHOT-004" in f.where), None)
        check(b4 is not None and "'2-3'" in b4.msg and not any(c[1] == "SHOT-004" for c in e),
              "拍数 '2-3' → 警告里显示原值；运镜因果用繁体「因為」也认")
        check(("FMT-value", "SHOT-006") in w and not any(c[1] == "SHOT-006" for c in e),
              "时长 `8.00`、拍数 **2** → 按值检查 + FMT-value（修复前：误报时长缺失）")
        check(("FMT-shot-id", "SHOT-8") in w and ("FMT-dup-shot", "SHOT-008") in e,
              "镜号 SHOT-8 → FMT-shot-id（建议 SHOT-008），与 SHOT-008 视为重复")
        o10 = next((f for f in fs if f.code == "T2-over-max" and "SHOT-010" in f.where), None)
        check(o10 is not None and "拆成 3 镜" in o10.msg, "45s → 拆成 3 镜（每镜网格帧数）")
        check(any(f.code == "FMT-columns" and "运镜因果" in f.msg for f in fs) and ("A4-cause", "SHOT-011") not in e,
              "第二张表缺列 → 单独报 FMT-columns（修复前：按全部表头的并集判断，漏报），且该表不逐镜报 A4")
        check(not any(f.where.startswith("?") for f in fs) and x["stats"]["shots"] == 11,
              "表格里的模板空行被跳过")

        # 对抗：BOM / CRLF / 表头笔误 / 全角竖线 / 路径含空格与中文
        bad_b = B.read_bytes()
        bom = doc("bom.md", raw=b"\xef\xbb\xbf" + bad_b.split(b"\n", 2)[2])
        fs, _ = analyze(bom, p)
        check(codes(fs, "error") == expect and ("FMT-bom", "bom.md") in codes(fs, "warn"),
              "BOM + 表头在首行 → 结果与无 BOM 一致 + FMT-bom（修复前：'没有分镜表' 退出 2）")
        crlf = doc("crlf.md", raw=bad_b.replace(b"\n", b"\r\n"))
        fs, _ = analyze(crlf, p)
        check(codes(fs, "error") == expect, "CRLF 版 bad 分镜 → 结果与 LF 版一致")
        fw = doc("fw.md", HEADER.replace("时长(s)", "时长（s）").replace("运镜因果", "运镜 因果") + row("SEQ-01", "SHOT-001", "3.00", 1))
        fs, _ = analyze(fw, p)
        check(any(f.code == "FMT-header" and "`时长（s）` → `时长(s)`" in f.msg and "`运镜 因果` → `运镜因果`" in f.msg for f in fs),
              "表头 `时长（s）` / `运镜 因果` → error FMT-header，逐列给出改法")
        two = doc("two.md", HEADER + row("SEQ-01", "SHOT-001", "8.00", 2, content="a→b") + "\n"
                  + HEADER.replace("时长(s)", "时长（s）") + row("SEQ-02", "SHOT-002", "2.00", 1, cause="很酷")
                  + row("—", "—", "8.00", 2, content="a→b"))
        fs, x = analyze(two, p)
        check(any(f.code == "FMT-header" and "第 5 行" in f.msg and "2 行未被任何脚本检查" in f.msg for f in fs)
              and x["stats"]["shots"] == 1,
              "两张表、第二张表头 `时长（s）` → error FMT-header（修复前：第二张表被整表跳过、exit 0 假通过）")
        emp = doc("emp.md", HEADER + row("SEQ-01", "—", "8.00", 2, content="a→b") + row("SEQ-01", "—", "8.00", 2, content="a→b"))
        fs, _ = analyze(emp, p)
        check(sum(1 for f in fs if f.code == "FMT-shot-id" and f.level == "error") == 2
              and not any(f.code == "FMT-dup-shot" for f in fs),
              "镜号写 `—` → error FMT-shot-id「镜号为空」，两行空镜号不互报重复")
        fwp = doc("fwp.md", HEADER.replace("|", "｜") + row("SEQ-01", "SHOT-001", "3.00", 1).replace("|", "｜"))
        fs, _ = analyze(fwp, p)
        check(any(f.code == "FMT-header" and "全角竖线" in f.msg for f in fs), "整表用全角竖线 ｜ → FMT-header 指出改为半角")

        # CLI 契约
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + [str(G), "--json"], capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
            okj = j["ok"] is True and j["stats"]["shots"] == 4 and len(j["segments"]) == 3
        except Exception:
            okj = False
        check(r.returncode == 0 and okj, "CLI good → 退出码 0，--json 含 stats/segments")
        r = subprocess.run(me + [str(B)], capture_output=True, text=True)
        check(r.returncode == 1 and "段汇总" in r.stdout and "A4-cause" in r.stdout, "CLI bad → 退出码 1，打印段汇总表")
        sp = doc("第 3 集 素材/story board.md", HEADER + row("SEQ-01", "SHOT-001", "2.00", 1))
        r = subprocess.run(me + [str(sp)], capture_output=True, text=True)
        check(r.returncode == 1 and "A1-short-no-reason" in r.stdout, "CLI 路径含空格与中文 → 正常检查")
        r = subprocess.run(me + [str(fw)], capture_output=True, text=True)
        check(r.returncode == 1 and "FMT-header" in r.stdout, "CLI 表头笔误 → 退出码 1（文档问题），不是 2")
        r = subprocess.run(me + [str(tdp / "nope.md")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 文件不存在 → 退出码 2")
        notable = doc("notable.md", "# 空\n没有表\n")
        r = subprocess.run(me + [str(notable)], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 文件里没有分镜表 → 退出码 2")
        cs = [subprocess.run(me + [str(G)] + a, capture_output=True, text=True).returncode
              for a in (["--min-mean", "nan"], ["--short-sec", "inf"], ["--max-short-share", "nan"])]
        check(cs == [2, 2, 2], f"CLI 非有限参数 → 退出码 2（实得 {cs}）")

    failed = [lbl for ok, lbl in results if not ok]
    print(f"\nselftest {'PASS' if not failed else 'FAIL'}：{len(results) - len(failed)}/{len(results)} 通过")
    return 0 if not failed else 1


# ------------------------------------------------------------------ CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard", nargs="?", help="storyboard.md")
    ap.add_argument("--min-mean", type=float, default=5.0, help="平均镜长下限秒（默认 5.0，A1）")
    ap.add_argument("--short-sec", type=float, default=5.0, help="统计短镜占比的阈值秒（默认 5.0）")
    ap.add_argument("--max-short-share", type=float, default=0.20, help="短镜占比上限（默认 0.20，学院推断）")
    ap.add_argument("--max-beats", type=int, default=3, help="单镜拍数上限（默认 3，P10/A5）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="运行自测（fixtures + A1 实证复现 + 对抗样例），全部通过退出 0")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.storyboard:
        ap.print_usage(sys.stderr)
        ac.die("需要 storyboard.md 路径（或 --selftest）")
    if not Path(a.storyboard).is_file():
        ac.die(f"找不到文件：{a.storyboard}")
    if (not all(math.isfinite(v) for v in (a.min_mean, a.short_sec, a.max_short_share))
            or a.min_mean <= 0 or a.short_sec <= 0 or not (0 <= a.max_short_share <= 1) or a.max_beats < 1):
        ac.die("参数越界：全部为有限数字；--min-mean/--short-sec > 0，0 ≤ --max-short-share ≤ 1，--max-beats ≥ 1")
    p = Params(a.min_mean, a.short_sec, a.max_short_share, a.max_beats)
    try:
        fs, extra = analyze(a.storyboard, p)
    except UnicodeDecodeError:
        ac.die(f"{a.storyboard} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8（无 BOM）后重跑")
    extra["params"] = asdict(p)
    return ac.emit(TITLE, fs, a.json, extra)


if __name__ == "__main__":
    sys.exit(main())
