#!/usr/bin/env python3
"""dialogue_capacity.py — 对白容量核算（设计阶段，送 H3 之前）

用途：
  在分镜/提示词定稿前，逐镜核算"这一镜的时长装不装得下这些台词"。H3 的对白与画面同 pass 生成，
  台词超出镜长容量时会随机缺句，而且**换 seed 无解**（D3：同一镜换 3 个 seed 各缺不同句）。
  本脚本只报告数字与改法（改几秒/几帧、删哪一句、删到几个字），不判断台词好坏。
  同时给出 storyboard.md 与 video-prompts.md 两侧台词的逐镜对账（P7 双文档对账）。

溯源：D3（对白容量物理约束：先 7.5s 不够，按"殇月句 4.34s + 一字一顿句 ~6.5s ≈ 10.3s"重算后按 11s 重产才齐）、
      P9（对白容量核算：镜长按台词字数÷7.5 字/秒 + 留白，设计阶段核算）、M5（7.5 字/秒，设计阶段核算）、
      T-2（H3 实测中文语速 ≈ 7.5 字/秒；帧网格 124–362 帧）、P7（双文档对账：分镜↔视频提示词台词逐字一致）。

容量模型（全部常数可用命令行覆盖）：
  chars      = Σ academy_common.speech_chars(台词)          汉字计 1、数字逐位计 1、拉丁词计 2；标点/省略号不计
                                                           台词里 ≤12 字的括号舞台提示（「（咬牙）」）不计——不念出来
  speak_time = chars ÷ rate                                rate 默认 7.5 字/秒〔委托方实证·T-2/D3〕
  pause_time = 停顿记号数 × pause_sec                        记号：「……」「…」「——」「...」「。。。」；pause_sec 默认 0.6s
                                                           〔学院推断〕用于刻画一字一顿 / 迟疑式念法
  gap_time   = (句数 − 1) × gap_sec                         gap_sec 默认 0.3s（换人/换句的气口）〔学院推断〕
  margin     = 表演留白，默认 1.0s                           〔学院推断〕对应 D3 判据"一口气读完不轧词的余量"
  hard       = speak_time + pause_time + gap_time           台词本身的物理时长
  required   = hard + margin                               该镜最少需要的时长（判定用）
  利用率     = required ÷ 时长

  一字一顿上界（建议值用）：识别出一字一顿句（≥2 个停顿记号、每顿之间 ≤2 字）时，该句按
  max(模型估值, stagger_sec) 代入得 required_obs；stagger_sec 默认 6.5s〔委托方实证·D3："一字一顿句 ~6.5s"〕。
  判定（error/warn）仍按 required；**建议时长**取 snap_seconds_up(required_obs)，因为 D3 的教训正是
  "按模型估短 → 缺句 → 换 seed 无解 → 二次延长"。required_obs 超过 15.08s 时退回模型值并提示把一字一顿句单独成镜。

判定：
  error  D3-capacity   hard > 时长：台词本身就装不下 → "容量不足 · 换 seed 无解（D3 结构性缺陷）"
  error  D3-margin     hard ≤ 时长 < required：台词勉强装得下，但表演留白 < margin（轧词/缺句风险）
  error  D3-split      required > 15.08s（362 帧单次上限）且无法靠加时长解决：拆镜或删句
  error  D3-duration-missing  有对白但时长缺失 / 不是有限数字 / ≤0
  error  FMT-header / FMT-columns / FMT-shot-heading   分镜表头不合契约、缺 `对白` 列、提示词镜头标题不合契约（该镜未被核算）
  warn   D3-tight      利用率 > 0.85：没有呼吸余量
  warn   D3-rushed     （规划检查）按自然语速 --natural-rate（默认 4.1 字/秒〔外部调研·F-ZEN-05〕zenstory H3 中文对白 20 次
                       探测）算出的需求（同一公式：字数÷自然语速 + 停顿 + 换句 + 留白）> 时长：7.5 字/秒是塞得下的上限，
                       不是好听的语速。7.5 的 error 判定不变；本项只提示"会被念得很赶"
  warn   D3-stagger    检测到一字一顿句：模型估值不确定，给出按 D3 实测（~6.5s/句）代入的上界
  warn   D3-d-stage    提示词 <d> 内含括号舞台提示：H3 可能把它念出来
  warn   FMT-d-tag / FMT-d-unclosed   `<d>` 未写 `[Chinese]` / 未闭合（已尽量计入容量）
  warn   FMT-bom / FMT-value / FMT-shot-id / FMT-dup-shot / FMT-dialogue-sep   格式偏差（已按值核算）
  warn   P7-dialogue-diff / P7-duration-diff / P7-shot-missing / P7-no-h3   两文档不一致（同时给 --storyboard 与 --prompts）
  info   D3-ok / D3-no-dialogue / D3-need / P7-unpaired

  建议值：时长按 snap_seconds_up 吸附到 H3 帧网格（17k+5）；超过 15.08s 则提示"拆镜或删句"。

如何验证本模型（〔学院推断〕部分）：每次 H3 出片后用 transcript_reconcile.py 对账，把"缺句镜"的 required/时长
  回填到 40-memory；若出现 D3-ok 却缺句，调大 --margin / --pause-sec；若 D3-margin 的镜全部齐句，可调小 --margin。
  已知校准点：D3 实例中 11s 齐句（台词 ≈10.3s，实际余量 ≈0.7s），即默认 margin=1.0 + gap=0.3 偏保守；
  档案算式自身不闭合（4.34 + 6.5 = 10.84 ≠ 10.3），若取 10.3 − 4.34 ≈ 6.0s 作一字一顿句实测，可用 --stagger-sec 6.0。

输入格式：70-playbooks/format-contracts.md
  §1 storyboard.md 的 `时长(s)` 与 `对白` 列（多句 ` / ` 分隔，每句 `说话人：台词`，无对白写 `—`）；
  §2 video-prompts.md 每镜 `- 时长:`（缺失时退用 `- 帧数:`÷24）与 h3 代码块中的 `<d>[Chinese] 台词</d>`；
     声明 `- 尾部余量: 1.3` 时，可用时长 = 时长 − 尾部余量（尾部会在剪辑中裁掉，台词必须在余量前说完；两文档时长对账也按此口径）。
  解析统一使用 academy_common（parse_storyboard / parse_video_prompts / dialogue_from_h3 / parse_dialogue / speech_chars）。
  输入容错（只为不漏检/不误报，不放宽契约，偏差一律报 FMT-* warn）：BOM；句间分隔写成无空格 `/` 或全角 `／`
  （按说话人重新切句）；无对白写成 `——` / `无对白`；`<d>[chinese]…</d>`、`<d>台词</d>`；`nan`/`inf` 时长；
  镜号 `SHOT-10`（按 SHOT-010 配对）。

用法示例：
  python3 dialogue_capacity.py --storyboard ep03/storyboard.md
  python3 dialogue_capacity.py --storyboard ep03/storyboard.md --prompts ep03/video-prompts.md
  python3 dialogue_capacity.py --prompts ep03/video-prompts.md --json
  python3 dialogue_capacity.py --text "殇月：月落之时，我会回来找你 / 苏晓：我……记……住……了。" --seconds 7.5
  python3 dialogue_capacity.py --text "就是现在！"                 # 不给 --seconds：只算需求与建议帧数
  python3 dialogue_capacity.py --storyboard sb.md --margin 0.7 --pause-sec 0.8 --stagger-sec 6.0
  python3 dialogue_capacity.py --storyboard sb.md --natural-rate 4.3          # 按本项目配音实测语速做规划检查
  python3 dialogue_capacity.py --selftest

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

TITLE = "对白容量核算（D3 / P9 / M5）"
MAX_SEC = ac.frames_to_seconds(ac.H3_MAX_FRAMES)
DISPLAY_TOL = 0.005
D3_STAGGER_OBSERVED_SEC = 6.5   # 〔委托方实证·D3〕"一字一顿句 ~6.5s"
NATURAL_RATE_CPS = 4.1          # 〔外部调研·F-ZEN-05〕zenstory H3 中文对白自然语速；7.5（T-2）是容量上限
PAUSE_RE = re.compile(r"……|…|——|\.{3,}|。{3,}")

RE_INLINE_SEP = re.compile(r"\s*[/／]\s*(?=[^\s：:/／][^：:/／]{0,19}[：:])")   # 无空格 / 或全角 ／ 后接「说话人：」
RE_STAGE = re.compile(r"[（(【\[][^（）()【】\[\]]{1,12}[）)】\]]")            # 短括号舞台提示
RE_D_ANY = re.compile(r"<d>(.*?)</d>", re.S | re.I)
RE_D_OPEN = re.compile(r"<d>", re.I)
RE_LANG_TAG = re.compile(r"^\s*\[[A-Za-z][A-Za-z \-]*\]\s*")
RE_DASHES = re.compile(r"^[\s\-—–―－~～_]+$")
PLACEHOLDERS = {"无对白", "无台词", "无对话", "没有对白", "暂无", "(无)", "none", "null", "nil"}
RE_STRICT_HEADING = re.compile(r"^##\s+(SHOT-\d{3})\b")          # 与 academy_common.parse_video_prompts 一致
RE_SHOTLIKE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(?:镜头|镜号|镜)?\s*[:：]?\s*shot\s*[-_－—–]?\s*(\d+)", re.I)
RE_SHOT_TOKEN = re.compile(r"shot\s*[-_－—–]?\s*\d+", re.I)
RE_SHOT_ID = re.compile(r"^SHOT-\d{3}$")
RE_SHOT_LOOSE = re.compile(r"^\s*shot\s*[-_－—–]?\s*0*(\d{1,4})(?!\d)", re.I)


@dataclass
class Params:
    rate: float = ac.SPEECH_RATE_CPS
    pause_sec: float = 0.6
    gap_sec: float = 0.3
    margin: float = 1.0
    warn_util: float = 0.85
    stagger_sec: float = D3_STAGGER_OBSERVED_SEC
    natural_rate: float = NATURAL_RATE_CPS


@dataclass
class Assessment:
    n_lines: int
    chars: float
    pauses: int
    speak: float
    pause_t: float
    gap_t: float
    margin: float
    hard: float
    required: float


# ------------------------------------------------------------------ 模型

def snap_up(sec: float) -> int | None:
    return ac.snap_seconds_up(sec)        # academy_common 已内置 0.005s 显示容差


def sec_s(n: int) -> str:
    return f"{ac.frames_to_seconds(n):.2f}"


def count_pauses(text: str) -> int:
    return len(PAUSE_RE.findall(text or ""))


def assess(lines: list[str], p: Params) -> Assessment:
    chars = sum(ac.speech_chars(t) for t in lines)
    pauses = sum(count_pauses(t) for t in lines)
    speak = chars / p.rate
    pause_t = pauses * p.pause_sec
    gap_t = max(len(lines) - 1, 0) * p.gap_sec
    hard = speak + pause_t + gap_t
    return Assessment(len(lines), chars, pauses, speak, pause_t, gap_t, p.margin, hard, hard + p.margin)


def line_cost(text: str, p: Params) -> float:
    return ac.speech_chars(text) / p.rate + count_pauses(text) * p.pause_sec


def is_stagger(text: str) -> bool:
    """一字一顿：≥2 个停顿记号，且每两个记号之间（及首尾）的可读字数 ≤2。"""
    if count_pauses(text) < 2:
        return False
    runs = [ac.speech_chars(r) for r in PAUSE_RE.split(text)]
    return all(r <= 2 for r in runs)


def recommend(a: Assessment, lines: list[str], p: Params) -> dict:
    """建议帧数：无一字一顿句 → snap(required)；有 → snap(required_obs)（D3 实测上界），超上限时退回模型值。"""
    stag = [t for t in lines if is_stagger(t)]
    extra = sum(max(0.0, p.stagger_sec - line_cost(t, p)) for t in stag)
    req_obs = a.required + extra
    rec_model = snap_up(a.required)
    rec_obs = snap_up(req_obs) if stag else rec_model
    rec = rec_obs if (stag and rec_obs is not None) else rec_model
    return {"rec": rec, "rec_model": rec_model, "req_obs": req_obs, "stagger": bool(stag) and extra > 0,
            "obs_over_max": bool(stag) and extra > 0 and rec_obs is None}


def short(text: str, n: int = 14) -> str:
    return text if len(text) <= n else text[:n] + "…"


def breakdown(a: Assessment, p: Params) -> str:
    return (f"{a.chars:g} 字÷{p.rate:g}={a.speak:.2f}s + 停顿 {a.pauses}×{p.pause_sec:g}={a.pause_t:.2f}s"
            f" + 换句 {max(a.n_lines - 1, 0)}×{p.gap_sec:g}={a.gap_t:.2f}s + 留白 {a.margin:.2f}s = {a.required:.2f}s")


def rec_text(a: Assessment, r: dict, p: Params) -> str:
    rec, rm = r["rec"], r["rec_model"]
    if rec is None:
        return f"需求 {a.required:.2f}s 超过 15.08s 单次上限：拆镜（把后几句移到下一镜）或删句"
    if r["stagger"] and rec != rm:
        return (f"把时长改为 {sec_s(rec)}s（{rec} 帧）：本模型需 {a.required:.2f}s（最小网格 {rm} 帧 / {sec_s(rm)}s），"
                f"但本镜含一字一顿句，按 D3 实测 ≈{p.stagger_sec:g}s/句 取上界 {r['req_obs']:.2f}s"
                f"（D3：按模型估短会再缺句、换 seed 无解）；同步改 storyboard 与 video-prompts")
    txt = (f"把时长改为 {sec_s(rec)}s（{rec} 帧，≥需求 {a.required:.2f}s 的最小网格值），同步改 storyboard 与 video-prompts")
    if r["obs_over_max"]:
        txt += (f"；注意：按 D3 实测一字一顿句 ≈{p.stagger_sec:g}s 代入需 {r['req_obs']:.2f}s > 15.08s，"
                f"建议把一字一顿句单独成镜")
    return txt


def fix_text(a: Assessment, dur: float, lines: list[str], p: Params, r: dict) -> str:
    parts = [rec_text(a, r, p)]
    if len(lines) > 1:
        for i, t in enumerate(lines):
            rest = assess(lines[:i] + lines[i + 1:], p)
            if rest.required <= dur + 1e-9:
                parts.append(f"或删去第 {i + 1} 句「{short(t)}」（删后需 {rest.required:.2f}s，利用率 {rest.required / dur:.0%}）")
    budget = (dur - a.pause_t - a.gap_t - p.margin) * p.rate
    max_chars = math.floor(budget + 1e-9)
    if 0 < max_chars < a.chars:
        parts.append(f"或把台词总字数删减到 ≤{max_chars} 字（当前 {a.chars:g} 字，停顿与句数不变）")
    return "；".join(parts)


def split_msg(a: Assessment, p: Params) -> str:
    cap = math.floor((MAX_SEC - a.pause_t - a.gap_t - p.margin) * p.rate + 1e-9)
    per = f"单镜（15.08s）在当前停顿/句数下最多约 {cap} 字，" if cap > 0 else ""
    return (f"台词需 {a.required:.2f}s，超过 H3 单次上限 15.08s（362 帧）：任何时长都装不下。{per}"
            f"按说话人轮次拆成两镜（当前 {a.chars:g} 字），或删句")


def evaluate(shot: str, where: str, dur: float | None, lines: list[str], p: Params, source: str) -> tuple[list[ac.Finding], dict]:
    """核算一镜，返回 (findings, 汇总行)。"""
    fs: list[ac.Finding] = []
    if dur is not None and (not math.isfinite(dur) or dur <= 0):
        dur = None   # nan / inf / 0 / 负数按"缺失"处理
    a = assess(lines, p)
    util = (a.required / dur) if dur else None
    r = recommend(a, lines, p)
    rec = r["rec"]
    row = {"shot": shot, "source": source, "duration": dur, **{k: (round(v, 3) if isinstance(v, float) else v)
                                                                for k, v in asdict(a).items()},
           "utilization": round(util, 3) if util is not None else None,
           "recommended_frames": rec, "recommended_seconds": round(ac.frames_to_seconds(rec), 2) if rec else None,
           "model_recommended_frames": r["rec_model"],
           "stagger_upper_required": round(r["req_obs"], 3) if r["stagger"] else None}
    data = dict(row)

    stagger_fs: list[ac.Finding] = []
    for t in lines:
        if is_stagger(t):
            cost = line_cost(t, p)
            alt = a.required - cost + max(cost, p.stagger_sec)
            alt_up = snap_up(alt)
            alt_txt = (f"若按 D3 实测一字一顿句 ≈{p.stagger_sec:g}s 整句代入，本镜需 ≈{alt:.2f}s"
                       + (f"（{alt_up} 帧 / {sec_s(alt_up)}s）" if alt_up else "（超过 15.08s：一字一顿句单独成镜）")
                       + (f"，已超过当前时长 {dur:.2f}s" if dur is not None and alt > dur + 1e-9 else ""))
            stagger_fs.append(ac.Finding("warn", "D3-stagger",
                                 f"「{short(t, 20)}」是一字一顿句：本模型估 {cost:.2f}s（{ac.speech_chars(t):g} 字 + "
                                 f"{count_pauses(t)} 顿×{p.pause_sec:g}s，〔学院推断〕）；{alt_txt}。"
                                 f"下一步：按上界定时长，或先单句试生成实测后用 --pause-sec / --stagger-sec 回填校准",
                                 where, {**data, "stagger_line": t, "model_sec": round(cost, 2),
                                         "observed_upper_required": round(alt, 2), "observed_upper_frames": alt_up}))

    if dur is None:
        hint = f"按台词至少需 {a.required:.2f}s" + (f"，建议 {rec} 帧 / {sec_s(rec)}s" if rec else "（超过 15.08s：拆镜）")
        fs.append(ac.Finding("error", "D3-duration-missing",
                             f"时长缺失、不是有限数字或 ≤0，无法核算容量：补时长；{hint}", where, data))
        return fs + stagger_fs, row

    if a.hard > dur + 1e-9:
        fs.append(ac.Finding("error", "D3-capacity",
                             f"容量不足 · 换 seed 无解（D3 结构性缺陷）：不含留白台词本身已需 {a.hard:.2f}s > 时长 {dur:.2f}s；"
                             f"含留白共需 {a.required:.2f}s（{breakdown(a, p)}）。改法：{fix_text(a, dur, lines, p, r)}", where, data))
    elif a.required > dur + 1e-9:
        fs.append(ac.Finding("error", "D3-margin",
                             f"容量不足（留白）：台词本身 {a.hard:.2f}s 装得下，但只剩 {dur - a.hard:.2f}s 留白"
                             f" < {p.margin:g}s（D3 判据：一口气读完不轧词的余量）。需 {a.required:.2f}s。"
                             f"改法：{fix_text(a, dur, lines, p, r)}", where, data))
    elif util is not None and util > p.warn_util + 1e-9:
        up = snap_up(a.required / p.warn_util)
        fix = (f"把时长加到 {sec_s(up)}s（{up} 帧）可降到 ≤{p.warn_util:.0%}" if up
               else "删减台词（时长已近上限）")
        fs.append(ac.Finding("warn", "D3-tight",
                             f"利用率 {util:.0%} > {p.warn_util:.0%}：没有呼吸余量（{breakdown(a, p)} / 时长 {dur:.2f}s）。{fix}",
                             where, data))
    else:
        fs.append(ac.Finding("info", "D3-ok", f"需 {a.required:.2f}s / 时长 {dur:.2f}s，利用率 {util:.0%}（{breakdown(a, p)}）",
                             where, data))

    if a.required > MAX_SEC + 1e-9 and not any(f.code == "D3-split" for f in fs):
        fs.append(ac.Finding("error", "D3-split", split_msg(a, p), where, data))
    return fs + stagger_fs, row


def natural_check(where: str, dur: float | None, lines: list[str], p: Params) -> tuple[list[ac.Finding], float | None]:
    """规划检查：按自然语速重算需求；> 时长 → warn D3-rushed。返回 (findings, 自然语速需求秒)。"""
    if not lines:
        return [], None
    a = assess(lines, Params(p.natural_rate, p.pause_sec, p.gap_sec, p.margin))
    if dur is None or not math.isfinite(dur) or dur <= 0 or a.required <= dur + 1e-9:
        return [], a.required
    up = snap_up(a.required)
    fix = f"按自然语速定镜长：{up} 帧 / {sec_s(up)}s" if up else "超过 15.08s：拆镜或删句"
    return [ac.Finding("warn", "D3-rushed",
                       f"按自然语速需 {a.required:.2f}s（{breakdown(a, Params(p.natural_rate, p.pause_sec, p.gap_sec, p.margin))}）"
                       f"> 时长 {dur:.2f}s；7.5 字/秒是塞得下的上限，不是好听的语速（自然语速 {p.natural_rate:g} 字/秒为外部实测"
                       f"〔外部调研·F-ZEN-05〕，待本管线复测）→ {fix}，或删减台词", where,
                       {"natural_rate": p.natural_rate, "natural_required": round(a.required, 3), "duration": dur,
                        "natural_recommended_frames": up})], a.required


# ------------------------------------------------------------------ 输入容错（只为不漏检/不误报）

def read_doc(path: Path) -> tuple[str, bool]:
    text = path.read_text(encoding="utf-8")
    return (text[1:], True) if text.startswith("﻿") else (text, False)


def parse_compat(parser, path: Path, text: str, had_bom: bool) -> list[dict]:
    """academy_common 解析器的 BOM 兼容包装：带 BOM 时解析去 BOM 的临时副本（行号不变）。"""
    if not had_bom:
        return parser(path)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / path.name
        tmp.write_text(text, encoding="utf-8")
        out = parser(tmp)
    for s in out:
        s["file"] = str(path)
    return out


def bom_finding(path: Path) -> ac.Finding:
    return ac.Finding("warn", "FMT-bom",
                      f"{path.name} 以 UTF-8 BOM 开头（format-contracts §0.1：UTF-8 无 BOM）。本脚本已去 BOM 解析，"
                      f"但 academy_common 的其他脚本会漏读首行（首镜标题/表头）→ 漏检。去掉 BOM："
                      f"`sed -i '1s/^\\xEF\\xBB\\xBF//' {path.name}`，或编辑器另存为「UTF-8（无 BOM）」", path.name)


def scan_bad_headings(text: str) -> list[tuple[int, str, str, str | None]]:
    bad, in_code, prev = [], False, None
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        ok = RE_STRICT_HEADING.match(ln)
        if ok:
            prev = ok.group(1)
            continue
        n_ln = unicodedata.normalize("NFKC", ln)        # 全角 ＳＨＯＴ－０１２ 也要抓
        m = RE_SHOTLIKE_HEADING.match(n_ln)
        if m and len(RE_SHOT_TOKEN.findall(n_ln)) == 1:  # 「# SHOT-001 到 SHOT-010 总览」这类区间标题不算
            bad.append((i, ln.strip(), f"SHOT-{int(m.group(1)):03d}", prev))
    return bad


def canon_id(raw: str) -> tuple[str, bool]:
    """返回 (规范镜号, 是否本来就合契约)。'SHOT-10' → ('SHOT-010', False)。"""
    s = (raw or "").strip()
    if RE_SHOT_ID.match(s):
        return s, True
    m = RE_SHOT_LOOSE.match(unicodedata.normalize("NFKC", s))
    return (f"SHOT-{int(m.group(1)):03d}", False) if m else (s, False)


def _norm_key(k: str) -> str:
    return re.sub(r"[\s*_`]", "", unicodedata.normalize("NFKC", k)).lower()


def meta_get(meta: dict, key: str) -> str | None:
    if key in meta:
        return meta[key]
    return next((v for k, v in meta.items() if _norm_key(k) == _norm_key(key)), None)


def _clean_value(v: str) -> str:
    s = unicodedata.normalize("NFKC", str(v)).strip().strip("`*_\"' ")
    return re.sub(r"\s*\(.*\)\s*$", "", s).strip("`*_\"' ")


def parse_seconds(v: str | None) -> tuple[float | None, bool]:
    """返回 (秒, 是否契约写法)；nan/inf/≤0 → None。"""
    if v is None or ac.is_empty(v):
        return None, True
    x, plain = ac.to_float(v), True
    if x is None:
        plain = False
        try:
            x = float(re.sub(r"\s*(s|秒|sec|secs|seconds)$", "", _clean_value(v), flags=re.I))
        except ValueError:
            return None, False
    return (x if math.isfinite(x) and x > 0 else None), plain


def is_blank_cell(pairs: list[tuple[str, str]]) -> bool:
    """整格占位（`——`、`无对白`、`（无）`…）视为无对白；带说话人的「神：……」是有意的沉默句，照常核算。"""
    if len(pairs) != 1 or pairs[0][0] != "?":
        return False
    t = unicodedata.normalize("NFKC", pairs[0][1]).strip().rstrip("。.").lower()
    return bool(RE_DASHES.match(t)) or t in PLACEHOLDERS


def spoken(t: str) -> str:
    """去掉短括号舞台提示（不念出来）；若去掉后无可念内容，保留原文。"""
    s = RE_STAGE.sub("", t).strip()
    return s if (ac.speech_chars(s) > 0 or count_pauses(s) > 0) else t.strip()


def clean_pairs(pairs: list[tuple[str, str]]) -> tuple[list[str], bool, list[str]]:
    """返回 (可核算台词列表, 是否重新切句, 被去掉舞台提示的原句)。"""
    if is_blank_cell(pairs):
        return [], False, []
    out, resplit, staged = [], False, []
    for _, text in pairs:
        parts = RE_INLINE_SEP.split(text)
        if len(parts) > 1:
            resplit = True
        segs = [parts[0]] + [t for p_ in parts[1:] for _, t in ac.parse_dialogue(p_)]
        for t in segs:
            sp = spoken(t)
            if sp != t.strip():
                staged.append(t.strip())
            if sp:
                out.append(sp)
    return out, resplit, staged


def prompt_lines(h3: str) -> tuple[list[str], list[str], int, list[str]]:
    """返回 (台词, 不合契约的 <d> 原文, 未闭合 <d> 数, 含括号舞台提示的台词)。合契约的 <d> 由 academy_common 解析。"""
    strict = ac.dialogue_from_h3(h3)
    found = list(RE_D_ANY.finditer(h3))
    bad = [i["text"] for i in ac.dialogue_tag_issues(h3) if i["kind"] in ("no-lang", "lang-case", "lang-bracket")]
    raw = strict if not bad else [RE_LANG_TAG.sub("", m.group(1)).strip() for m in found]
    unclosed = max(0, len(RE_D_OPEN.findall(h3)) - len(found))
    lines, staged = [], []
    for t in raw:
        sp = spoken(t)
        if sp != t.strip():
            staged.append(t.strip())
        if sp:
            lines.append(sp)
    return lines, bad, unclosed, staged


def _nk(s: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s)).lower()


ALIAS = {"时长(秒)": "时长(s)", "时长": "时长(s)", "时长s": "时长(s)", "时长(sec)": "时长(s)", "镜头": "镜号",
         "镜头号": "镜号", "shot": "镜号", "台词": "对白"}


def header_hints(text: str) -> list[str]:
    """academy_common 认不出的"分镜表"（表头笔误 / 全角竖线）→ 每张表一条可执行改法（这些表会被整表跳过）。"""
    want = {_nk(c): c for c in ac.STORYBOARD_COLS}
    out = []
    for t in ac.parse_md_tables(text):
        if "镜号" in t["header"] and "时长(s)" in t["header"]:
            continue
        fixes, targets = [], set()
        for h in t["header"]:
            tgt = want.get(_nk(h)) or ALIAS.get(_nk(h))
            if tgt:
                targets.add(tgt)
                if h != tgt:
                    fixes.append(f"`{h}` → `{tgt}`")
        if fixes and {"镜号", "时长(s)"} <= targets:
            out.append(f"第 {t['line']} 行分镜表头与契约不一致：{'；'.join(fixes)}"
                       f"（format-contracts §1：列名逐字一致，括号用半角）；修正前这张表的 {len(t['rows'])} 行对白未被核算")
    in_code = False
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and "｜" in ln and "镜号" in ln and "时长" in ln:
            out.append(f"第 {i} 行表格用了全角竖线「｜」：改为半角「|」（format-contracts §0.3）；修正前这张表的对白未被核算")
    return out


# ------------------------------------------------------------------ 文档 → 镜

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    return "".join(ch for ch in s if ch.isalnum()).lower()


def load_storyboard(path: Path) -> tuple[list[dict], list[ac.Finding]]:
    text, had_bom = read_doc(path)
    fs: list[ac.Finding] = [bom_finding(path)] if had_bom else []
    tables = [t for t in ac.parse_md_tables(text) if "镜号" in t["header"] and "时长(s)" in t["header"]]
    hints = header_hints(text)
    for h in hints:
        fs.append(ac.Finding("error", "FMT-header", h, path.name))
    if not tables:
        if hints:
            return [], fs
        ac.die(f"{path} 中没有分镜表（表头需含 `镜号` 与 `时长(s)`，见 format-contracts §1）")
    if not any("对白" in t["header"] for t in tables):
        fs.append(ac.Finding("error", "FMT-columns",
                             "分镜表缺 `对白` 列：对白容量无法核算（format-contracts §1：多句 ` / ` 分隔，无对白写 —）。补列后重跑",
                             f"{path.name}:{tables[0]['line']}"))
    raw_rows = {r["_line"]: r for t in tables for r in t["rows"]}
    out, seen = [], {}
    for s in parse_compat(ac.parse_storyboard, path, text, had_bom):
        raw = raw_rows.get(s["line"], {})
        if all(ac.is_empty(raw.get(c)) for c in ("镜号", "时长(s)", "对白", "内容")):
            continue   # 模板空行
        sid, ok = canon_id(s["shot"])
        where = f"{s['shot'] or '?'} · {path.name}:{s['line']}"
        if ac.is_empty(s["shot"]):
            sid = f"（第 {s['line']} 行无镜号）"
            fs.append(ac.Finding("warn", "FMT-shot-id", "镜号为空：填集内唯一的 SHOT-nnn（三位数字），否则无法与提示词对账（P7）",
                                 where))
        elif not ok:
            fs.append(ac.Finding("warn", "FMT-shot-id",
                                 (f"镜号 '{s['shot']}' 不合契约 `SHOT-nnn`（三位数字）：改为 {sid}；本脚本已按 {sid} 与提示词配对"
                                  if sid != s["shot"].strip() else
                                  f"镜号 '{s['shot']}' 为空或不合契约 `SHOT-nnn`：填写集内唯一的 SHOT-nnn"), where))
        if sid in seen:
            fs.append(ac.Finding("warn", "FMT-dup-shot",
                                 f"镜号 {sid} 与第 {seen[sid]} 行重复（集内必须唯一）：两行都已核算，但双文档对账只用最后一行。"
                                 f"重新编号（E2：改号走全仓替换）", where))
        seen.setdefault(sid, s["line"])
        dur, plain = parse_seconds(raw.get("时长(s)"))
        if dur is not None and not plain:
            fs.append(ac.Finding("warn", "FMT-value",
                                 f"时长(s) 写成 '{raw.get('时长(s)')}'，已按 {dur:g} 核算；契约要求纯数字（{dur:g}），否则其他脚本读不到",
                                 where))
        lines, resplit, staged = clean_pairs(s["dialogue"])
        resplit = resplit or bool(ac.dialogue_sep_issues(s.get("dialogue_raw", "")))   # academy_common 已切句，偏差照报
        if resplit:
            fs.append(ac.Finding("warn", "FMT-dialogue-sep",
                                 f"对白多句没有用 ` / `（半角斜杠、两侧空格）分隔：已按说话人切成 {len(lines)} 句核算；"
                                 f"改成「说话人：台词 / 说话人：台词」，否则其他脚本会读成 1 句", where))
        out.append({"shot": sid, "dur": dur, "lines": lines, "where": where, "src": "storyboard",
                    "h3_missing": False, "staged": staged})
    return out, fs


def load_prompts(path: Path) -> tuple[list[dict], list[ac.Finding]]:
    text, had_bom = read_doc(path)
    fs: list[ac.Finding] = [bom_finding(path)] if had_bom else []
    bad_heads = scan_bad_headings(text)
    for ln, raw, sug, prev in bad_heads:
        spill = (f"；其下的 <d> 台词不归属任何镜（academy_common 遇到任何标题即结束上一镜，不会再算到上一镜 {prev} 头上）" if prev else "")
        fs.append(ac.Finding("error", "FMT-shot-heading",
                             f"标题「{raw}」没有被识别为镜头（契约：`## SHOT-nnn`），这一镜的 <d> 台词未被核算/对账{spill}。"
                             f"改为 `## {sug}` 后重跑", f"{path.name}:{ln}", {"suggest": sug, "absorbed_by": prev}))
    shots = parse_compat(ac.parse_video_prompts, path, text, had_bom)
    if not shots and not bad_heads:
        ac.die(f"{path} 中没有 `## SHOT-nnn` 段落（见 format-contracts §2）")
    out, seen = [], {}
    for s in shots:
        where = f"{s['shot']} · {path.name}:{s['line']}"
        if s["shot"] in seen:
            fs.append(ac.Finding("warn", "FMT-dup-shot",
                                 f"{s['shot']} 与第 {seen[s['shot']]} 行重复：两处都已核算，但双文档对账只用后一处。删掉旧版本或重新编号",
                                 where))
        seen.setdefault(s["shot"], s["line"])
        dur, _ = parse_seconds(meta_get(s["meta"], "时长"))
        if dur is None:
            fr = _clean_value(meta_get(s["meta"], "帧数") or "")
            m = re.fullmatch(r"(\d+)\s*(?:帧|f|frames)?", fr, re.I)
            if m and int(m.group(1)) > 0:
                dur = ac.frames_to_seconds(int(m.group(1)))
        tail = ac.tail_margin(s["meta"])
        if dur is not None and tail and dur - tail > 0:
            dur -= tail          # 尾部余量会在剪辑中裁掉：可用时长 = 时长 − 余量（与分镜时长同口径）
        lines, bad, unclosed, staged = prompt_lines(s["h3"]) if s["h3"] is not None else ([], [], 0, [])
        if bad:
            fs.append(ac.Finding("warn", "FMT-d-tag",
                                 f"{len(bad)} 处 `<d>` 未按契约写成 `<d>[Chinese] 台词</d>`（如「{short(bad[0], 40)}」）："
                                 f"H3 可能不按中文念或整句不念（T-2 方言）。改成 `<d>[Chinese] …</d>`；本脚本已把它计入容量", where))
        if unclosed:
            fs.append(ac.Finding("warn", "FMT-d-unclosed",
                                 f"{unclosed} 个 `<d>` 没有闭合 `</d>`：该句未计入容量。补上 `</d>` 后重跑", where))
        for t in staged:
            fs.append(ac.Finding("warn", "D3-d-stage",
                                 f"<d> 内含括号舞台提示「{short(t, 24)}」：H3 可能把括号里的字念出来（实际更长、台词也错）。"
                                 f"把表演提示移到 <d> 之外（如 `[S1] grits her teeth and says: <d>[Chinese] …</d>`）；"
                                 f"容量已按去掉括号核算", where))
        out.append({"shot": s["shot"], "dur": dur, "lines": lines, "where": where, "src": "prompts",
                    "h3_missing": s["h3"] is None, "staged": staged})
    return out, fs


def analyze_docs(sb: list[dict] | None, vp: list[dict] | None, p: Params) -> tuple[list[ac.Finding], list[dict]]:
    fs: list[ac.Finding] = []
    rows: list[dict] = []
    silent: list[str] = []
    sb_map = {s["shot"]: s for s in (sb or [])}
    vp_map = {s["shot"]: s for s in (vp or [])}
    both = sb is not None and vp is not None

    def same(a: dict, b: dict) -> bool:
        return (norm("".join(a["lines"])) == norm("".join(b["lines"])) and len(a["lines"]) == len(b["lines"])
                and a["dur"] is not None and b["dur"] is not None and abs(a["dur"] - b["dur"]) <= 0.01)

    units = []
    for s in sb or []:
        o = vp_map.get(s["shot"])
        if o is not None and same(s, o):
            units.append({**s, "src": "storyboard+prompts", "where": f"{s['where']} = {o['where'].split(' · ')[1]}"})
        else:
            units.append(s)
    for s in vp or []:
        o = sb_map.get(s["shot"])
        if not (o is not None and same(o, s)):
            units.append(s)
    order = {"storyboard": 0, "storyboard+prompts": 0, "prompts": 1}
    units.sort(key=lambda u: (u["shot"], order[u["src"]]))

    for u in units:
        if not u["lines"]:
            label = f"{u['shot']}({u['src']}{'，无 h3 代码块' if u.get('h3_missing') else ''})" if both or u.get("h3_missing") \
                else u["shot"]
            silent.append(label)
            continue
        f, row = evaluate(u["shot"], u["where"], u["dur"], u["lines"], p, u["src"])
        nf, nreq = natural_check(u["where"], u["dur"], u["lines"], p)
        row["natural_required"] = round(nreq, 3) if nreq is not None else None
        fs += f + nf
        rows.append(row)

    if both:
        for shot in sorted(set(sb_map) | set(vp_map)):
            a, b = sb_map.get(shot), vp_map.get(shot)
            if a and b:
                if b.get("h3_missing"):
                    if a["lines"]:
                        fs.append(ac.Finding("warn", "P7-no-h3",
                                             f"video-prompts.md 中 {shot} 没有 ```h3 代码块（或代码块未标注 h3），分镜台词"
                                             f"「{short(' / '.join(a['lines']), 30)}」无法与 <d> 对账：补齐六段 h3 代码块并逐字写入 "
                                             f"`<d>[Chinese] …</d>`（P7）", b["where"]))
                elif norm("".join(a["lines"])) != norm("".join(b["lines"])) or len(a["lines"]) != len(b["lines"]):
                    sa = " / ".join(a["lines"]) or "—"
                    sv = " / ".join(b["lines"]) or "—"
                    fs.append(ac.Finding("warn", "P7-dialogue-diff",
                                         f"两文档台词不一致：分镜「{sa}」≠ 提示词 <d>「{sv}」。以剧本/分镜为准把两侧改成逐字一致"
                                         f"（P7 双文档对账），再重跑本脚本核算容量", shot,
                                         {"storyboard": a["lines"], "prompts": b["lines"]}))
                if a["dur"] is not None and b["dur"] is not None and abs(a["dur"] - b["dur"]) > 0.01:
                    fs.append(ac.Finding("warn", "P7-duration-diff",
                                         f"两文档时长不一致：分镜 {a['dur']:.2f}s vs 提示词 {b['dur']:.2f}s，容量核算以哪侧为准不确定。"
                                         f"统一为同一网格值（用 h3_frame_grid.py --seconds 吸附）", shot,
                                         {"storyboard": a["dur"], "prompts": b["dur"]}))
            elif b and not a:
                fs.append(ac.Finding("warn", "P7-shot-missing",
                                     f"{shot} 在 video-prompts.md 中有、storyboard.md 中没有：先在分镜补这一行（P7），再写提示词",
                                     b["where"]))
            elif a and not b and a["lines"]:
                fs.append(ac.Finding("info", "P7-unpaired",
                                     f"{shot} 有对白但提示词尚未写此镜，台词未对账（写提示词时逐字照抄分镜对白）", a["where"]))
    if silent:
        fs.append(ac.Finding("info", "D3-no-dialogue", f"无对白、不核算：{', '.join(silent)}", ""))
    return fs, rows


def _pad(v, w: int, right: bool = False) -> str:
    """按终端显示宽度补齐（中日韩全角字符占 2 列）。"""
    s = str(v)
    fill = " " * max(0, w - sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s))
    return fill + s if right else s + fill


def table_text(rows: list[dict]) -> str:
    if not rows:
        return "（没有含对白的镜）"
    cols = [("镜号", 10, False), ("来源", 20, False), ("时长s", 7, True), ("句", 4, True), ("字", 5, True),
            ("顿", 4, True), ("需求s", 8, True), ("利用率", 8, True)]
    out = ["对白容量汇总：", "  " + "".join(_pad(n, w, r) for n, w, r in cols) + "  建议网格（含一字一顿上界）"]
    for r in rows:
        dur = f"{r['duration']:.2f}" if r["duration"] is not None else "—"
        util = f"{r['utilization']:.0%}" if r["utilization"] is not None else "—"
        rec = f"{r['recommended_frames']} 帧/{r['recommended_seconds']:.2f}s" if r["recommended_frames"] else "拆镜/删句"
        vals = [r["shot"], r["source"], dur, r["n_lines"], f"{r['chars']:g}", r["pauses"], f"{r['required']:.2f}", util]
        out.append("  " + "".join(_pad(v, w, rr) for v, (_, w, rr) in zip(vals, cols)) + "  " + rec)
    return "\n".join(out)


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[tuple[bool, str]] = []
    p = Params()

    def check(cond: bool, label: str):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    def codes(fs, level):
        return {(f.code, f.where.split(" · ")[0]) for f in fs if f.level == level}

    def run_docs(sbp=None, vpp=None, params=p):
        fs0, sb, vp = [], None, None
        if sbp:
            sb, f1 = load_storyboard(sbp)
            fs0 += f1
        if vpp:
            vp, f2 = load_prompts(vpp)
            fs0 += f2
        fs, rows = analyze_docs(sb, vp, params)
        return fs0 + fs, rows

    # 1. 计数
    check(count_pauses("我……记……住……了。") == 3 and count_pauses("等等——你说什么…") == 2 and count_pauses("……") == 1,
          "停顿记号计数：「……」算 1 顿，「——」「…」各 1 顿")
    check(is_stagger("我……记……住……了。") and not is_stagger("我……我不知道你在说什么……"),
          "一字一顿识别：「我……记……住……了」是，普通迟疑句不是")

    # 2. fixtures
    G, B = ac.FIXTURES / "good", ac.FIXTURES / "bad"
    gfs, _ = run_docs(G / "storyboard.md", G / "video-prompts.md")
    check(not codes(gfs, "error") and not codes(gfs, "warn"),
          "fixtures/good（分镜+提示词）→ 0 error，0 warn")
    bfs, brows = run_docs(B / "storyboard.md", B / "video-prompts.md")
    check(codes(bfs, "error") == {("D3-capacity", "SHOT-002")}, "fixtures/bad → 唯一 error 为 SHOT-002 D3-capacity")
    check(("P7-dialogue-diff", "SHOT-003") in codes(bfs, "warn"),
          "fixtures/bad → SHOT-003 分镜无对白、提示词有 <d>受死吧！</d> → P7-dialogue-diff")
    check(("D3-stagger", "SHOT-002") in codes(bfs, "warn"), "fixtures/bad → SHOT-002「我……记……住……了」→ D3-stagger")
    r2 = next(r for r in brows if r["shot"] == "SHOT-002")
    check(r2["chars"] == 45 and r2["pauses"] == 3 and abs(r2["required"] - 9.10) < 0.01
          and r2["model_recommended_frames"] == 226 and r2["recommended_frames"] == 328,
          "bad SHOT-002：45 字 + 3 顿 → 模型需 9.10s（226 帧）；含一字一顿句 → 建议取 D3 上界 328 帧（13.67s）")
    sb_bad, _ = load_storyboard(B / "storyboard.md")
    s2 = next(s for s in sb_bad if s["shot"] == "SHOT-002")
    f75, _ = evaluate("SHOT-002", "bad@7.5", 7.5, s2["lines"], p, "storyboard")
    cap75 = next((f for f in f75 if f.code == "D3-capacity"), None)
    check(cap75 is not None and cap75.data["recommended_frames"]
          and ac.frames_to_seconds(cap75.data["recommended_frames"]) >= 10.3 and "13.67s" in cap75.msg,
          f"D3 复现（bad SHOT-002 按档案原镜长 7.5s）→ D3-capacity「换 seed 无解」，建议网格值 ≥10.3s"
          f"（得 {cap75.data['recommended_frames'] if cap75 else '?'} 帧）")

    # 3. D3 原始数字复现（合成文本，字数/顿数构造为与档案时长对齐）
    shangyue = "月落之时，我会回来找你，你记住今天说过的每一个字，等到那天，我们湖边再见。"
    stagger = "我……一……定……会……等……你……回……来……的。"
    c1, c2 = line_cost(shangyue, p), line_cost(stagger, p)
    check(abs(c1 - 4.34) < 0.1 and 5.9 <= c2 <= 6.6 and abs((c1 + c2) - 10.3) < 0.1,
          f"D3 复现：殇月句 {c1:.2f}s（档案 4.34s）+ 一字一顿句 {c2:.2f}s（档案 ~6.5s）= {c1 + c2:.2f}s（档案 ≈10.3s）")
    lines = [shangyue, stagger]
    f75, _ = evaluate("D3", "D3@7.5", 7.5, lines, p, "synthetic")
    cap = next((f for f in f75 if f.code == "D3-capacity"), None)
    check(cap is not None, "D3 复现：7.5s → D3-capacity「容量不足 · 换 seed 无解」（档案：先 7.5s 不够）")
    check(cap is not None and cap.data["recommended_frames"] and ac.frames_to_seconds(cap.data["recommended_frames"]) >= 10.3,
          f"D3 复现：建议网格值 ≥10.3s（得 {cap.data['recommended_frames'] if cap else '?'} 帧 / "
          f"{sec_s(cap.data['recommended_frames']) if cap and cap.data['recommended_frames'] else '?'}s）")
    f11, _ = evaluate("D3", "D3@11", 11.0, lines, p, "synthetic")
    check(not any(f.code == "D3-capacity" for f in f11) and any(f.code == "D3-margin" for f in f11),
          "D3 复现：11s → 台词物理可装下（无 D3-capacity，与'按 11s 重产才齐'一致），仅默认 1.0s 留白不足 → D3-margin（保守）")
    f11b, _ = evaluate("D3", "D3@11", 11.0, lines, Params(margin=0.4), "synthetic")
    check(not any(f.level == "error" for f in f11b), "D3 复现：--margin 0.4（档案实际余量 ≈0.7s 内）时 11s 通过")

    # 4. 利用率 / 超上限 / 快速计算
    tight = "一" * 31
    ft, _ = evaluate("T", "tight", 5.88, [tight], p, "synthetic")
    check([f.code for f in ft] == ["D3-tight"], "31 字 / 5.88s → 利用率 87% → D3-tight warn")
    fl, _ = evaluate("L", "long", 12.0, ["一" * 120], p, "synthetic")
    check(any(f.code == "D3-capacity" and "超过 15.08s" in f.msg for f in fl) and any(f.code == "D3-split" for f in fl),
          "120 字 → 需 17s > 15.08s → D3-capacity + D3-split（拆镜或删句）")
    check(any(f.code == "D3-split" and "最多约 105 字" in f.msg for f in fl),
          "D3-split 给出单镜字数上限：(15.08−1.0)×7.5 → 105 字")
    fo, _ = evaluate("Q", "quick", 5.17, ["就是现在！"], p, "text")
    check([f.code for f in fo] == ["D3-ok"], "快速计算：「就是现在！」/ 5.17s → D3-ok")
    for bad_dur in (0.0, float("nan"), float("inf"), -3.0):
        fz, _ = evaluate("Z", "zero", bad_dur, ["甲", "乙"], p, "synthetic")
        check([f.code for f in fz] == ["D3-duration-missing"], f"时长 {bad_dur} → D3-duration-missing（不崩溃、不假通过）")
    fd, _ = evaluate("S", "drop", 6.58, s2["lines"], p, "synthetic")
    check(any("删去第 2 句" in f.msg for f in fd if f.code == "D3-capacity"),
          "bad SHOT-002 / 6.58s 的改法里给出「删去第 2 句」可行项")
    fe, _ = evaluate("E", "en", 3.0, ["Run, you fool, run now before it is too late!"], p, "synthetic")
    check([f.code for f in fe] == ["D3-margin"] and fe[0].data["chars"] == 20,
          "纯英文台词 10 词 → 按 20 字计 2.67s，3s 装得下但留白不足 → D3-margin")

    nf, _ = natural_check("rushed", 5.88, [tight], p)
    check([f.code for f in nf] == ["D3-rushed"] and "不是好听的语速" in nf[0].msg,
          "31 字 / 5.88s：7.5 字/秒只到 D3-tight，按自然语速 4.1 字/秒需 8.56s → D3-rushed warn")
    fl = ac.FIXTURES / "fl2va"
    ffs, _ = run_docs(fl / "storyboard.md", fl / "video-prompts.md")
    check(not codes(ffs, "error") and not codes(ffs, "warn"),
          "fixtures/fl2va：提示词 8.00s 声明尾部余量 1.30 → 按 6.70s 与分镜对账，0 warn（不报 P7-duration-diff）")

    # 5. 合成：提示词有、分镜无；时长不一致
    HDR = ("| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |\n"
           "|---|---|---|---|---|---|---|---|---|---|\n")

    def sbrow(shot, dur, dlg):
        return f"| SEQ-01 | {shot} | {dur} | 2 | x | 推 | 因为a，所以b | — | {dlg} | — |\n"

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def doc(name: str, body: str = "", raw: bytes | None = None) -> Path:
            q = tdp / name
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_bytes(raw if raw is not None else body.encode("utf-8"))
            return q

        sbp = doc("storyboard.md", HDR + sbrow("SHOT-001", "8.00", "甲：你好。"))
        vpp = doc("video-prompts.md", "## SHOT-001\n- 时长: 8.71\n- 帧数: 209\n\n```h3\ndetailed_description:\n"
                  "  [S1] says: <d>[Chinese] 你好。</d>\n```\n\n## SHOT-002\n- 时长: 5.17\n- 帧数: 124\n\n```h3\nsummary:\n  x\n```\n")
        fs, _ = run_docs(sbp, vpp)
        check(("P7-duration-diff", "SHOT-001") in codes(fs, "warn") and any(f.code == "P7-shot-missing" for f in fs),
              "合成：两侧时长 8.00/8.71 → P7-duration-diff；提示词多出 SHOT-002 → P7-shot-missing")

        # 6. 对抗：对白格的各种写法
        sbp = doc("adv-sb.md", HDR
                  + sbrow("SHOT-001", "8.00", "——")
                  + sbrow("SHOT-002", "8.00", "无对白")
                  + sbrow("SHOT-003", "6.00", "苏晓：你给我站住！/石神：凡人，你也配？/苏晓：配不配，打过才知道！")
                  + sbrow("SHOT-004", "nan", "苏晓：月落之时我会回来找你")
                  + sbrow("SHOT-005", "8.00", "苏 晓：（咬牙）就是现在！")
                  + sbrow("SHOT-006", "8.00", "苏晓：就是现在！ ／ 石神：滚！")
                  + sbrow("SHOT-007", "8.00", "苏晓：甲")
                  + sbrow("SHOT-007", "8.00", "苏晓：乙乙乙")
                  + sbrow("SHOT-10", "8.00", "苏晓：你好")
                  + sbrow("SHOT-011", "`8.00`", "苏晓：你好")
                  + sbrow("SHOT-012", "8.00", "神：……")
                  + "|  |  |  |  |  |  |  |  |  |  |\n")
        vpp = doc("adv-vp.md", "\n".join([
            "## SHOT-13", "- 时长: 4.00", "", "```h3", "x: <d>[Chinese] 一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五</d>", "```", "",
            "## SHOT-001", "- 时长: 8.00", "", "```h3", "detailed_description:", "  nothing", "```", "",
            "## SHOT-005", "- 时长: 8.00", "", "```h3", "detailed_description:", "  [S1] says: <d>[Chinese] 就是现在！</d>", "```", "",
            "## SHOT-006", "- 时长: 8.00", "", "```h3", "detailed_description:",
            "  [S1] says: <d>[chinese] 就是现在！</d> [S2] says: <d>滚！</d> [S1]: <d>[Chinese] （冷笑）走着瞧", "```", "",
            "## SHOT-010", "- 时长: 8.00", "", "```h3", "detailed_description:", "  [S1] says: <d>[Chinese] 你好</d>", "```", "",
            "## SHOT-011", "- 时长: 8.00", "- 帧数: 192", "",
        ]) + "\n")
        fs, rows = run_docs(sbp, vpp)
        e, w = codes(fs, "error"), codes(fs, "warn")
        silent = next((f.msg for f in fs if f.code == "D3-no-dialogue"), "")
        rowmap = {}
        for r in rows:
            rowmap.setdefault(r["shot"], []).append(r)
        check("SHOT-001(storyboard+prompts)" in silent and "SHOT-002(storyboard)" in silent
              and not any(c[1] in ("SHOT-001", "SHOT-002") for c in w),
              "对白写 `——` / `无对白` → 视为无对白（修复前：被当成台词核算，并误报 P7 台词不一致）")
        check(rowmap["SHOT-003"][0]["n_lines"] == 3 and rowmap["SHOT-003"][0]["chars"] == 18
              and ("FMT-dialogue-sep", "SHOT-003") in w,
              "无空格 `/` 分隔的 3 句 → 按 3 句 18 字核算（不把说话人名算进台词）+ warn FMT-dialogue-sep")
        check(("D3-duration-missing", "SHOT-004") in e, "时长 nan → D3-duration-missing（修复前：'利用率 nan%' 的 D3-ok 假通过）")
        check(not any(c[1] == "SHOT-005" for c in w) and rowmap["SHOT-005"][0]["chars"] == 4,
              "分镜「（咬牙）就是现在！」vs 提示词「就是现在！」→ 舞台提示不计字、不误报 P7")
        r6 = [r for r in rowmap["SHOT-006"] if "prompts" in r["source"]]
        check(("FMT-dialogue-sep", "SHOT-006") in w and ("FMT-d-tag", "SHOT-006") in w and ("FMT-d-unclosed", "SHOT-006") in w
              and r6 and r6[0]["n_lines"] == 2 and not any(c == ("P7-dialogue-diff", "SHOT-006") for c in w),
              "全角 `／` 分隔 + `<d>[chinese]` / `<d>滚！</d>` → 两侧都按 2 句核算、P7 一致；未闭合 <d> → warn")
        check(("FMT-dup-shot", "SHOT-007") in w, "分镜镜号重复 → warn FMT-dup-shot")
        check(("FMT-shot-id", "SHOT-10") in w and not any(f.code == "P7-shot-missing" and "SHOT-010" in f.where for f in fs),
              "分镜 `SHOT-10` → warn FMT-shot-id，并按 SHOT-010 与提示词配对（不误报 P7-shot-missing）")
        check(("FMT-value", "SHOT-011") in w and ("P7-no-h3", "SHOT-011") in w and "SHOT-011" in rowmap,
              "时长写成 `8.00` → 按值核算 + FMT-value；提示词该镜无 h3 代码块 → P7-no-h3（不再说'台词不一致'）")
        check("SHOT-012" in rowmap and rowmap["SHOT-012"][0]["pauses"] == 1,
              "带说话人的「神：……」是沉默句：照常按 1 顿核算")
        check(any(f.code == "FMT-shot-heading" and f.data.get("suggest") == "SHOT-013" for f in fs),
              "提示词标题 `## SHOT-13` → error FMT-shot-heading（修复前：该镜 45 字 / 4s 的容量问题静默消失）")
        check(not any("?" == f.where.split(" · ")[0] for f in fs), "表格末尾的模板空行被跳过，不产生 '?' 镜")

        # 7. 对抗：BOM / CRLF / 缺 对白 列 / 表头笔误 / 路径含空格与中文
        bad_sb = (B / "storyboard.md").read_bytes()
        hdr_first = b"\xef\xbb\xbf" + bad_sb.split(b"\n", 2)[2]          # 去掉标题行，让表头成为第一行
        bom_sb = doc("bom-sb.md", raw=hdr_first)
        fs, _ = run_docs(bom_sb)
        check(("D3-capacity", "SHOT-002") in codes(fs, "error") and ("FMT-bom", "bom-sb.md") in codes(fs, "warn"),
              "BOM + 表头在首行 → 仍核出 SHOT-002 D3-capacity（修复前：'没有分镜表' 退出 2）")
        crlf = doc("crlf-sb.md", raw=bad_sb.replace(b"\n", b"\r\n"))
        fs, _ = run_docs(crlf)
        check(codes(fs, "error") == {("D3-capacity", "SHOT-002")}, "CRLF 版 bad 分镜 → 结果与 LF 版一致")
        nocol = doc("nocol.md", "| 段号 | 镜号 | 时长(s) |\n|---|---|---|\n| SEQ-01 | SHOT-001 | 8.00 |\n")
        fs, _ = run_docs(nocol)
        check(any(f.code == "FMT-columns" and f.level == "error" for f in fs),
              "分镜缺 `对白` 列 → error FMT-columns（修复前：全部当无对白、假通过）")
        fw = doc("fw.md", HDR.replace("时长(s)", "时长（s）") + sbrow("SHOT-001", "6.00", "甲：你好"))
        fs, _ = run_docs(fw)
        check(any(f.code == "FMT-header" and "`时长（s）` → `时长(s)`" in f.msg for f in fs),
              "表头 `时长（s）`（全角括号）→ error FMT-header 并给出逐字改法")
        two = doc("two.md", HDR + sbrow("SHOT-001", "8.00", "甲：你好") + "\n"
                  + HDR.replace("时长(s)", "时长（s）") + sbrow("SHOT-002", "2.00", "甲：" + "一二三四五六七八九十" * 3))
        fs, rows2 = run_docs(two)
        check(any(f.code == "FMT-header" and f.level == "error" and "第 5 行" in f.msg for f in fs)
              and [r["shot"] for r in rows2] == ["SHOT-001"],
              "两张表、第二张表头 `时长（s）` → error FMT-header（修复前：第二张表的超容量对白被整表跳过、假通过）")
        check(count_pauses("我。。。记住了") == 1, "「。。。」也算 1 个停顿记号")
        sp = doc("第 3 集 素材/story board.md", HDR + sbrow("SHOT-001", "3.00", "甲：" + "一二三四五六七八九十" * 3))

        # 8. CLI 契约
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + ["--storyboard", str(G / "storyboard.md"), "--prompts", str(G / "video-prompts.md"), "--json"],
                           capture_output=True, text=True)
        try:
            okj = json.loads(r.stdout)["ok"] is True
        except Exception:
            okj = False
        check(r.returncode == 0 and okj, "CLI good → 退出码 0，--json ok=true")
        r = subprocess.run(me + ["--storyboard", str(B / "storyboard.md")], capture_output=True, text=True)
        check(r.returncode == 1 and "D3-capacity" in r.stdout, "CLI bad → 退出码 1，含 D3-capacity")
        r = subprocess.run(me + ["--storyboard", str(sp)], capture_output=True, text=True)
        check(r.returncode == 1 and "D3-capacity" in r.stdout, "CLI 路径含空格与中文 → 正常核算")
        r = subprocess.run(me + ["--storyboard", str(fw)], capture_output=True, text=True)
        check(r.returncode == 1 and "FMT-header" in r.stdout, "CLI 表头笔误 → 退出码 1（文档问题），不是 2")
        r = subprocess.run(me + ["--text", "殇月：" + shangyue + " / 苏晓：" + stagger, "--seconds", "7.5"],
                           capture_output=True, text=True)
        check(r.returncode == 1 and "换 seed 无解" in r.stdout, "CLI --text … --seconds 7.5 → 退出码 1")
        r = subprocess.run(me + ["--text", "苏晓：你好/石神：滚", "--json"], capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
            okt = r.returncode == 0 and j["shots"][0]["n_lines"] == 2
        except Exception:
            okt = False
        check(okt, "CLI --text 无空格 `/` 分隔 → 按 2 句核算")
        r = subprocess.run(me + ["--seconds", "7.5"], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 只给 --seconds 不给 --text → 退出码 2")
        r = subprocess.run(me + ["--storyboard", str(tdp / "nope.md")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 文件不存在 → 退出码 2")
        bad_cli = [["--text", "甲：你好", "--seconds", "nan"], ["--text", "甲：你好", "--rate", "nan"],
                   ["--text", "甲：你好", "--margin", "inf"], ["--text", "甲：你好", "--stagger-sec", "-1"],
                   ["--text", "——"]]
        cs = [subprocess.run(me + a, capture_output=True, text=True).returncode for a in bad_cli]
        check(cs == [2] * len(bad_cli), f"CLI 非法数值 / 只有占位符的 --text → 全部退出码 2（实得 {cs}）")

    failed = [lbl for ok, lbl in results if not ok]
    print(f"\nselftest {'PASS' if not failed else 'FAIL'}：{len(results) - len(failed)}/{len(results)} 通过")
    return 0 if not failed else 1


# ------------------------------------------------------------------ CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--storyboard", help="storyboard.md（取 时长(s) 与 对白 列）")
    ap.add_argument("--prompts", help="video-prompts.md（取 - 时长: 与 <d>[Chinese] …</d>）")
    ap.add_argument("--text", help="快速计算：台词文本（多句用 ' / ' 分隔，可带 '说话人：'）")
    ap.add_argument("--seconds", type=float, help="快速计算：镜长（秒），与 --text 一起用")
    ap.add_argument("--rate", type=float, default=ac.SPEECH_RATE_CPS, help="语速 字/秒（默认 7.5，T-2/D3 实测）")
    ap.add_argument("--pause-sec", type=float, default=0.6, help="每个停顿记号（……/…/——）的秒数（默认 0.6，学院推断）")
    ap.add_argument("--gap-sec", type=float, default=0.3, help="句间/换人气口秒数（默认 0.3，学院推断）")
    ap.add_argument("--margin", type=float, default=1.0, help="表演留白秒数（默认 1.0，学院推断）")
    ap.add_argument("--warn-util", type=float, default=0.85, help="利用率警告阈值（默认 0.85）")
    ap.add_argument("--stagger-sec", type=float, default=D3_STAGGER_OBSERVED_SEC,
                    help="一字一顿句实测时长上界，用于建议值（默认 6.5，D3 实证）")
    ap.add_argument("--natural-rate", type=float, default=NATURAL_RATE_CPS,
                    help="规划检查用的自然语速 字/秒（默认 4.1，外部调研 F-ZEN-05；7.5 是容量上限）→ 超出报 warn D3-rushed")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="运行自测（fixtures + D3 实证复现 + 对抗样例），全部通过退出 0")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    nums = [a.rate, a.pause_sec, a.gap_sec, a.margin, a.warn_util, a.stagger_sec, a.natural_rate]
    if (not all(math.isfinite(x) for x in nums) or a.rate <= 0 or a.natural_rate <= 0 or a.pause_sec < 0 or a.gap_sec < 0 or a.margin < 0
            or a.stagger_sec < 0 or not (0 < a.warn_util <= 1.5)):
        ac.die("参数越界：全部为有限数字；--rate > 0，--pause-sec/--gap-sec/--margin/--stagger-sec ≥ 0，0 < --warn-util ≤ 1.5")
    p = Params(a.rate, a.pause_sec, a.gap_sec, a.margin, a.warn_util, a.stagger_sec, a.natural_rate)
    if a.seconds is not None and a.text is None:
        ac.die("--seconds 只能与 --text 一起用（文档模式的时长取自文档）")
    if a.text is None and not a.storyboard and not a.prompts:
        ap.print_usage(sys.stderr)
        ac.die("至少给出 --storyboard / --prompts / --text 之一（或 --selftest）")
    if a.seconds is not None and not (math.isfinite(a.seconds) and a.seconds > 0):
        ac.die("--seconds 必须是 > 0 的有限数字")

    findings: list[ac.Finding] = []
    rows: list[dict] = []
    if a.text is not None:
        lines, _, _ = clean_pairs(ac.parse_dialogue(a.text))
        if not lines:
            ac.die("--text 为空或只有占位符（—/——/无对白）")
        f, row = evaluate("--text", "--text", a.seconds, lines, p, "text")
        if a.seconds is None:   # 只算需求，不判时长
            f = [x for x in f if x.code != "D3-duration-missing"]
            rec = row["recommended_frames"]
            f.append(ac.Finding("info", "D3-need",
                                f"需 {row['required']:.2f}s（{breakdown(assess(lines, p), p)}）→ "
                                + (f"建议 {rec} 帧 / {sec_s(rec)}s" if rec else "超过 15.08s：拆镜或删句")
                                + ("（含一字一顿句，按 D3 实测上界取值）" if row["stagger_upper_required"] else ""),
                                "--text", row))
            if row["model_recommended_frames"] is None and not any(x.code == "D3-split" for x in f):
                f.append(ac.Finding("error", "D3-split", split_msg(assess(lines, p), p), "--text", row))
        nf, nreq = natural_check("--text", a.seconds, lines, p)
        row["natural_required"] = round(nreq, 3) if nreq is not None else None
        findings += f + nf
        rows.append(row)

    sb = vp = None
    for opt, loader in (("storyboard", load_storyboard), ("prompts", load_prompts)):
        path = getattr(a, opt)
        if not path:
            continue
        if not Path(path).is_file():
            ac.die(f"找不到文件：{path}")
        try:
            data, lf = loader(Path(path))
        except UnicodeDecodeError:
            ac.die(f"{path} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8（无 BOM）后重跑")
        findings += lf
        if opt == "storyboard":
            sb = data
        else:
            vp = data
    if sb is not None or vp is not None:
        f, r = analyze_docs(sb, vp, p)
        findings += f
        rows += r

    extra = {"params": asdict(p), "shots": rows, "summary": table_text(rows)}
    return ac.emit(TITLE, findings, a.json, extra)


if __name__ == "__main__":
    sys.exit(main())
