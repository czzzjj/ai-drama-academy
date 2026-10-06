#!/usr/bin/env python3
"""h3_frame_grid.py — H3 帧网格换算与校验（N = 17k+5，k=7…21，24 fps）

用途：
  送 MiniMax H3 生成之前，把"想要的秒数"换算成合法帧数，并校验 video-prompts.md 每镜的
  `- 帧数:` 是否落在 H3 帧网格上、是否在训练区间内、是否与 `- 时长:` 一致。
  只报告事实与可直接执行的改法（改成几帧/几秒、或拆成两段），不做任何审美判断。

溯源：T-2（H3 帧网格 17k+5、训练区间 124–362 帧、单次上限 ≈15.1s、低于 124 帧动作异常）、
      A1（碎镜症根因②：不知道 H3 能连续生成 5.2–15.1s、自我设限 ≤3s；"任何 ≤3s 的镜必须给出理由"）。

帧网格（学院补注，见 00-orientation/client-dossier.md T-2）：
  N = 17k + 5，k = 7…21 → 124 … 362 帧；按 24 fps → 5.17 … 15.08 s（共 15 个合法值）。
  < 124 帧：低于训练下限，动作表现异常 → 不得送 H3（改 124 帧，或改本地生成并在分镜填短镜理由）。
  > 362 帧：超过单次上限 → 必须拆成两段（更长则拆成 N 段）。

输入格式：70-playbooks/format-contracts.md §2「视频提示词（video-prompts.md）」——
  每镜一个 `## SHOT-nnn`，其下元数据行 `- 时长: 10.83`、`- 帧数: 260`。
  解析统一使用 academy_common.parse_video_prompts（不在本脚本重复实现）。
  输入容错（只为不漏检，不放宽契约）：
    - 文件带 UTF-8 BOM：去 BOM 后解析，并报 warn FMT-bom（academy_common 会漏读首行 → 其他脚本漏检首镜）；
    - 疑似镜头标题但不合契约（`## SHOT-12` / `### SHOT-013` / `## shot-014` …）：报 error FMT-shot-heading
      （academy_common 不认这些标题 → 该镜在所有脚本里都"不存在"，不报就是漏检）；
    - 键名加粗/带反引号（`- **帧数**: 260`）、值带反引号/括号注释/全角数字（`` `260` ``、`260帧（10.83s）`、`１０．８３`）：
      按值校验，同时报 warn FMT-meta-key / FMT-value（其他脚本按契约读不到）；
    - `nan` / `inf` / ≤0 的时长按"不是数字"处理（不会被当成通过）。

判定（--check）：
  error  T2-frames-missing    帧数缺失或不是整数
  error  T2-frames-offgrid    帧数不在 17k+5 网格上
  error  T2-frames-below-min  帧数 < 124（训练下限）
  error  T2-frames-above-max  帧数 > 362（单次上限，须拆段）
  error  T2-duration-missing  时长缺失、不是有限数字或 ≤0
  error  T2-duration-mismatch |帧数/24 − 时长| > 容差（默认 0.05s）
  error  FMT-shot-heading     疑似镜头标题不合契约，该镜未被解析
  error  FMT-no-shots         文件中没有任何 `## SHOT-nnn`
  warn   FMT-bom / FMT-meta-key / FMT-value / FMT-dup-shot   格式偏差（已按值校验）
  info   T2-ok                该镜帧数与时长一致且合法

用法示例：
  python3 h3_frame_grid.py --table                       # 打印完整网格 k / 帧数 / 秒
  python3 h3_frame_grid.py --seconds 10.3                # ≥10.3s 的最小合法帧数 + 最近网格值
  python3 h3_frame_grid.py --seconds 16                  # 超过 15.08s → 提示必须拆成两段
  python3 h3_frame_grid.py --frames 290                  # 校验某个帧数是否合法并给出相邻合法值
  python3 h3_frame_grid.py --check season-01/ep03/video-prompts.md
  python3 h3_frame_grid.py --check video-prompts.md --json
  python3 h3_frame_grid.py --selftest

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
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "H3 帧网格校验（T-2 / A1）"
GRID = ac.grid_frames()
MIN_SEC = ac.frames_to_seconds(ac.H3_MIN_FRAMES)   # 5.1667
MAX_SEC = ac.frames_to_seconds(ac.H3_MAX_FRAMES)   # 15.0833
DISPLAY_TOL = 0.005   # 文档里时长保留两位小数：5.17 实为 124 帧（5.1667s），吸附时容忍显示舍入
MAX_INPUT_SEC = 3600.0

RE_STRICT_HEADING = re.compile(r"^##\s+(SHOT-\d{3})\b")          # 与 academy_common.parse_video_prompts 一致
RE_SHOTLIKE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(?:镜头|镜号|镜)?\s*[:：]?\s*shot\s*[-_－—–]?\s*(\d+)", re.I)
RE_SHOT_TOKEN = re.compile(r"shot\s*[-_－—–]?\s*\d+", re.I)
RE_META_LIKE = re.compile(r"^\s*[-*+]\s*[*_`]*\s*(帧数|时长)\s*[*_`]*\s*[:：]")


# ------------------------------------------------------------------ 基础换算

def snap_up(sec: float) -> int | None:
    """≥ sec 的最小合法帧数（容忍两位小数显示舍入；超过 362 帧返回 None）。"""
    return ac.snap_seconds_up(sec - DISPLAY_TOL)


def k_of(n: int) -> int:
    return (n - 5) // 17


def sec_s(n: int) -> str:
    return f"{ac.frames_to_seconds(n):.2f}"


def fmt_n(n: int) -> str:
    return f"{n} 帧（k={k_of(n)}，{sec_s(n)}s）"


def neighbors(n: int) -> tuple[int | None, int | None]:
    lower = max((g for g in GRID if g <= n), default=None)
    upper = min((g for g in GRID if g >= n), default=None)
    return lower, upper


def split_parts(sec: float) -> int:
    return max(2, math.ceil(sec / MAX_SEC - 1e-9))


def split_head(sec: float) -> str:
    p = split_parts(sec)
    return "必须拆成两段" if p == 2 else f"必须拆成 {p} 段（两段每段仍超过 15.08s）"


def split_plan(sec: float) -> str:
    """超过上限时的拆段建议：按 ceil(秒/15.08) 段均分，每段吸附到网格。"""
    parts = split_parts(sec)
    each = snap_up(sec / parts)
    if each is None:   # 理论上不会发生（每段 ≤15.08s）
        return f"拆成 {parts} 段（每段 ≤362 帧 / 15.08s）"
    return (f"拆成 {parts} 段，每段 ≈{sec / parts:.2f}s → 各用 {fmt_n(each)}；"
            f"拆点放在拍与拍之间，不得切断一个连续动作（P10/M1：连续动作不得切新镜）")


def grid_rows() -> list[dict]:
    return [{"k": k_of(n), "frames": n, "seconds": round(ac.frames_to_seconds(n), 2)} for n in GRID]


def table_text() -> str:
    out = ["H3 帧网格（N=17k+5，24 fps）", "  k   帧数    秒"]
    for r in grid_rows():
        out.append(f"  {r['k']:>2}  {r['frames']:>4}  {r['seconds']:>6.2f}")
    out.append(f"  共 {len(GRID)} 个合法值；<{ac.H3_MIN_FRAMES} 帧低于训练下限，>{ac.H3_MAX_FRAMES} 帧必须拆段（T-2）")
    return "\n".join(out)


# ------------------------------------------------------------------ 输入容错（只为不漏检）

def read_doc(path: Path) -> tuple[str, bool]:
    """读 UTF-8 文本；返回 (去 BOM 后的文本, 是否带 BOM)。UnicodeDecodeError 交给调用方。"""
    text = path.read_text(encoding="utf-8")
    return (text[1:], True) if text.startswith("﻿") else (text, False)


def parse_prompts(path: Path, text: str, had_bom: bool) -> list[dict]:
    """academy_common.parse_video_prompts 的 BOM 兼容包装：带 BOM 时解析去 BOM 的临时副本（行号不变）。"""
    if not had_bom:
        return ac.parse_video_prompts(path)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / path.name
        tmp.write_text(text, encoding="utf-8")
        shots = ac.parse_video_prompts(tmp)
    for s in shots:
        s["file"] = str(path)
    return shots


def bom_finding(path: Path) -> ac.Finding:
    return ac.Finding("warn", "FMT-bom",
                      f"{path.name} 以 UTF-8 BOM 开头（format-contracts §0.1：UTF-8 无 BOM）。本脚本已去 BOM 解析，"
                      f"但 academy_common 的其他脚本会漏读首行（首镜标题/表头）→ 漏检。去掉 BOM："
                      f"`sed -i '1s/^\\xEF\\xBB\\xBF//' {path.name}`，或编辑器另存为「UTF-8（无 BOM）」",
                      path.name)


def scan_bad_headings(text: str) -> list[tuple[int, str, str, str | None]]:
    """代码块外、像镜头标题却不合 `## SHOT-nnn` 的行 → [(行号, 原文, 建议 ID, 上一个合法镜号)]。围栏规则与 academy_common 相同。"""
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


def stray_meta(text: str, start: int, end: int, key: str) -> tuple[int, str] | None:
    """在本镜区段 [start, end) 的代码块外找 `帧数`/`时长` 的非契约写法（写在 h3 之后、用 * 列表、加粗…）。"""
    in_code = False
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if i <= start or i >= end or in_code:
            continue
        m = RE_META_LIKE.match(ln)
        if m and m.group(1) == key:
            return i, ln.strip()
    return None


def _norm_key(k: str) -> str:
    return re.sub(r"[\s*_`]", "", unicodedata.normalize("NFKC", k)).lower()


def meta_get(meta: dict, key: str) -> tuple[str | None, str | None]:
    """按契约键取值；键名加粗/带反引号/全角时按规范化键名兜底。返回 (值, 实际键名)。"""
    if key in meta:
        return meta[key], key
    for k, v in meta.items():
        if _norm_key(k) == _norm_key(key):
            return v, k
    return None, None


def _clean_value(v: str) -> str:
    s = unicodedata.normalize("NFKC", str(v)).strip()
    s = s.strip("`*_\"' ")
    s = re.sub(r"\s*\(.*\)\s*$", "", s)    # 末尾括号注释（NFKC 后全角括号已变半角）
    return s.strip("`*_\"' ")


def parse_frames(v: str | None) -> tuple[int | None, bool]:
    """返回 (帧数, 是否契约写法)。契约写法 = 纯整数（可带 帧/f/frames 单位）。"""
    if v is None:
        return None, True
    m = re.fullmatch(r"\s*(\d+)\s*(帧|f|frames)?\s*", str(v))
    if m:
        return int(m.group(1)), True
    m = re.fullmatch(r"(\d+)(?:\.0+)?\s*(?:帧|f|frames)?", _clean_value(v), re.I)
    return (int(m.group(1)), False) if m else (None, False)


def parse_seconds(v: str | None) -> tuple[float | None, bool]:
    """返回 (秒, 是否契约写法)。非有限值（nan/inf）与 ≤0 一律返回 None。"""
    if v is None or ac.is_empty(v):
        return None, True
    x, plain = ac.to_float(v), True
    if x is None:
        plain = False
        s = re.sub(r"\s*(s|秒|sec|secs|seconds)$", "", _clean_value(v), flags=re.I)
        try:
            x = float(s)
        except ValueError:
            return None, False
    if not math.isfinite(x) or x <= 0:
        return None, plain
    return x, plain


def shown(raw: str | None) -> str:
    return "无此行" if raw is None else f"'{raw}'"


# ------------------------------------------------------------------ 三种模式

def analyze_seconds(sec: float) -> list[ac.Finding]:
    fs: list[ac.Finding] = []
    where = f"--seconds {sec:g}"
    up = snap_up(sec)
    if up is None:
        fs.append(ac.Finding("error", "T2-split-required",
                             f"{sec:g}s 超过单次上限 362 帧（15.08s），{split_head(sec)}：{split_plan(sec)}；"
                             f"或删拍把这一段压到 ≤15.08s（362 帧）", where,
                             {"seconds": sec, "parts": split_parts(sec), "split": split_plan(sec)}))
        return fs
    near = ac.snap_seconds_nearest(sec)
    on_grid = abs(ac.frames_to_seconds(up) - sec) <= DISPLAY_TOL
    msg = (f"{sec:g}s 已在网格上 = {fmt_n(up)}" if on_grid else
           f"≥{sec:g}s 的最小合法值：{fmt_n(up)}；最近合法值：{fmt_n(near)}"
           f"（写入提示词：`- 帧数: {up}`、`- 时长: {sec_s(up)}`）")
    fs.append(ac.Finding("info", "T2-snap", msg, where,
                         {"seconds": sec, "min_grid_frames": up, "min_grid_seconds": round(ac.frames_to_seconds(up), 2),
                          "nearest_frames": near, "nearest_seconds": round(ac.frames_to_seconds(near), 2)}))
    if sec + DISPLAY_TOL < MIN_SEC:
        fs.append(ac.Finding("warn", "A1-below-min",
                             f"{sec:g}s 低于 H3 训练下限 124 帧（5.17s），送 H3 只能用 124 帧。"
                             f"若这是有意的短镜（插入/反应），在分镜 `短镜理由` 写明并改本地生成（D2）；"
                             f"否则把它并入相邻段，做成 8–15s 的长段多拍（A1、P10）", where))
    return fs


def analyze_frames(n: int) -> list[ac.Finding]:
    where = f"--frames {n}"
    if n < ac.H3_MIN_FRAMES:
        return [ac.Finding("error", "T2-frames-below-min",
                           f"{n} 帧（{sec_s(n)}s）低于训练下限 124 帧：改为 `- 帧数: 124`（5.17s），"
                           f"或该镜不送 H3（纯色卡/插入镜本地生成，D2）", where, {"frames": n})]
    if n > ac.H3_MAX_FRAMES:
        s = ac.frames_to_seconds(n)
        return [ac.Finding("error", "T2-frames-above-max",
                           f"{n} 帧（{sec_s(n)}s）超过单次上限 362 帧（15.08s），{split_head(s)}：{split_plan(s)}",
                           where, {"frames": n, "parts": split_parts(s)})]
    if not ac.is_grid_frames(n):
        lo, hi = neighbors(n)
        return [ac.Finding("error", "T2-frames-offgrid",
                           f"{n} 帧不在 17k+5 网格上：改为 {fmt_n(hi)}（向上，不丢内容）或 {fmt_n(lo)}（向下，需压缩动作）",
                           where, {"frames": n, "lower": lo, "upper": hi})]
    return [ac.Finding("info", "T2-ok", f"{fmt_n(n)} 合法", where, {"frames": n})]


def check_prompts(path: str | Path, tol: float = 0.05) -> list[ac.Finding]:
    path = Path(path)
    text, had_bom = read_doc(path)
    shots = parse_prompts(path, text, had_bom)
    fs: list[ac.Finding] = []
    if had_bom:
        fs.append(bom_finding(path))
    bad_heads = scan_bad_headings(text)
    for ln, raw, sug, prev in bad_heads:
        spill = (f"；其下的元数据/代码块会被算到上一镜 {prev} 头上，{prev} 的结论在改正前不可信" if prev else "")
        fs.append(ac.Finding("error", "FMT-shot-heading",
                             f"标题「{raw}」没有被识别为镜头（契约：`## SHOT-nnn`——两个 #、大写 SHOT、三位数字），"
                             f"这一镜的帧数/时长未被任何脚本校验{spill}。改为 `## {sug}` 后重跑",
                             f"{path.name}:{ln}", {"line": ln, "heading": raw, "suggest": sug, "absorbed_by": prev}))
    if not shots:
        if not bad_heads:
            fs.append(ac.Finding("error", "FMT-no-shots",
                                 f"{path.name} 中没有找到 `## SHOT-nnn` 段落：按 70-playbooks/format-contracts.md §2 写每镜标题",
                                 str(path)))
        return fs

    n_lines = len(text.splitlines())
    starts = sorted(s["line"] for s in shots)
    first_line: dict[str, int] = {}
    for s in shots:
        where = f"{s['shot']} · {path.name}:{s['line']}"
        if s["shot"] in first_line:
            fs.append(ac.Finding("warn", "FMT-dup-shot",
                                 f"{s['shot']} 与第 {first_line[s['shot']]} 行重复（集内镜号必须唯一）：两处都已校验，"
                                 f"但对账/装配只会认其中一处。重新编号或删掉旧版本（E2：改号走全仓替换）", where))
        else:
            first_line[s["shot"]] = s["line"]
        end = next((x for x in starts if x > s["line"]), n_lines + 1)
        meta = s["meta"]
        raw_f, key_f = meta_get(meta, "帧数")
        raw_d, key_d = meta_get(meta, "时长")
        for want, got in (("帧数", key_f), ("时长", key_d)):
            if got is not None and got != want:
                fs.append(ac.Finding("warn", "FMT-meta-key",
                                     f"键名写成了 `{got}`，契约是 `- {want}: …`（其他脚本按精确键名读取，会当作缺失）。"
                                     f"本脚本已按 `{want}` 校验；改回 `- {want}: …`", where))
        n, f_plain = parse_frames(raw_f)
        dur, d_plain = parse_seconds(raw_d)
        for want, raw, ok, val in (("帧数", raw_f, f_plain, n), ("时长", raw_d, d_plain, dur)):
            if raw is not None and val is not None and not ok:
                fs.append(ac.Finding("warn", "FMT-value",
                                     f"`- {want}:` 的值写成 '{raw}'，已按 {val:g} 校验；契约要求纯数字"
                                     f"（`- {want}: {val:g}`，不带反引号/括号注释/全角数字），否则其他脚本读不到", where))
        data = {"shot": s["shot"], "file": str(path), "line": s["line"], "frames_raw": raw_f, "duration_raw": raw_d}

        def stray_hint(key: str) -> str:
            hit = stray_meta(text, s["line"], end, key)
            return (f"（第 {hit[0]} 行有「{hit[1]}」，但不是写在 h3 代码块之前的 `- {key}: 值` 列表行，academy_common 读不到："
                    f"把它挪到 `## {s['shot']}` 与 ```h3 之间并写成 `- {key}: …`）") if hit else ""

        if dur is None:
            hint = (f"按帧数应写 `- 时长: {sec_s(n)}`" if n is not None and ac.is_grid_frames(n)
                    else "先定时长，再用 `--seconds` 吸附到网格")
            fs.append(ac.Finding("error", "T2-duration-missing",
                                 f"`- 时长:` 缺失、不是有限数字或 ≤0（{shown(raw_d)}）{stray_hint('时长') if raw_d is None else ''}："
                                 f"{hint}", where, data))

        if n is None:
            verb = "补" if raw_f is None else "改为"
            if dur is not None:
                up = snap_up(dur)
                fix = (f"{verb} `- 帧数: {up}` 并把时长改为 {sec_s(up)}（≥{dur:.2f}s 的最小网格值）" if up
                       else f"时长 {dur:.2f}s 超过 15.08s，{split_head(dur)}：{split_plan(dur)}")
                data.update({"recommended_frames": up})
            else:
                fix = "补 `- 时长:` 与 `- 帧数:`（用 `--seconds` 换算）"
            fs.append(ac.Finding("error", "T2-frames-missing",
                                 f"`- 帧数:` 缺失或不是整数（{shown(raw_f)}）{stray_hint('帧数') if raw_f is None else ''}：{fix}",
                                 where, data))
            continue

        # 帧数存在：越界 / 离网格 / 与时长不一致
        target = dur if dur is not None else ac.frames_to_seconds(n)
        up = snap_up(target)
        near = ac.snap_seconds_nearest(target)
        data.update({"frames": n, "duration": dur, "recommended_frames": up, "nearest_frames": near})
        if n < ac.H3_MIN_FRAMES:
            fs.append(ac.Finding("error", "T2-frames-below-min",
                                 f"帧数 {n}（{sec_s(n)}s）低于训练下限 124 帧（T-2：低于 124 帧动作表现异常）。"
                                 f"改为 `- 帧数: 124`、`- 时长: 5.17`；若这是纯色卡/字卡/插入镜，"
                                 f"则不送 H3，改本地确定性生成（D2）并从 video-prompts.md 删除此镜、在分镜填短镜理由",
                                 where, data))
            continue
        if n > ac.H3_MAX_FRAMES:
            s_n = ac.frames_to_seconds(n)
            fs.append(ac.Finding("error", "T2-frames-above-max",
                                 f"帧数 {n}（{sec_s(n)}s）超过单次上限 362 帧，{split_head(s_n)}：{split_plan(s_n)}",
                                 where, data))
            continue
        if not ac.is_grid_frames(n):
            lo, hi = neighbors(n)
            if up is not None:
                fix = (f"按时长 {target:.2f}s：改为 `- 帧数: {up}` 并把 `- 时长:` 同步改为 {sec_s(up)}"
                       f"（≥原时长的最小网格值）")
                alt = lo if up != lo else hi
                if alt is not None and alt != up:
                    fix += f"；或 {fmt_n(alt)}（同步改时长为 {sec_s(alt)}）"
            else:
                fix = f"时长 {target:.2f}s 超过上限，{split_head(target)}：{split_plan(target)}"
            fs.append(ac.Finding("error", "T2-frames-offgrid",
                                 f"帧数 {n} 不在 17k+5 网格上（相邻合法值 {lo}={sec_s(lo)}s / {hi}={sec_s(hi)}s）。{fix}",
                                 where, {**data, "lower": lo, "upper": hi}))
            continue
        if dur is None:
            continue
        diff = abs(ac.frames_to_seconds(n) - dur)
        data["diff"] = round(diff, 3)
        if diff > tol + 1e-9:
            fix = f"若帧数是对的：把 `- 时长:` 改为 {sec_s(n)}"
            if up is not None and up != n:
                fix += f"；若时长是对的：把 `- 帧数:` 改为 {up} 并把时长改为 {sec_s(up)}"
            elif up is None:
                fix += f"；若时长是对的：{dur:.2f}s 超过上限，{split_head(dur)}：{split_plan(dur)}"
            fs.append(ac.Finding("error", "T2-duration-mismatch",
                                 f"帧数 {n} = {sec_s(n)}s，但 `- 时长:` 写 {dur:.2f}s（差 {diff:.2f}s > {tol:.2f}s）。{fix}；"
                                 f"并同步 storyboard.md 的 时长(s)（P7 双文档对账）", where, data))
            continue
        fs.append(ac.Finding("info", "T2-ok", f"{fmt_n(n)}，与时长 {dur:.2f}s 一致", where, data))
    return fs


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[tuple[bool, str]] = []

    def check(cond: bool, label: str):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    def errs(fs):
        return {(f.code, f.where.split(" · ")[0]) for f in fs if f.level == "error"}

    def warns(fs):
        return {(f.code, f.where.split(" · ")[0]) for f in fs if f.level == "warn"}

    # 1. 网格本身（T-2）
    check(len(GRID) == 15 and GRID[0] == 124 and GRID[-1] == 362 and all((n - 5) % 17 == 0 for n in GRID),
          "网格 = 17k+5，k=7..21，124..362 共 15 个值")
    check(f"{MIN_SEC:.2f}" == "5.17" and f"{MAX_SEC:.2f}" == "15.08", "124 帧 = 5.17s，362 帧 = 15.08s（24 fps）")
    check(all(snap_up(float(f"{ac.frames_to_seconds(n):.2f}")) == n for n in GRID),
          "两位小数显示值（如 5.17 / 8.71 / 9.42）吸附回原帧数，不多跳一格")

    # 2. --seconds
    fs = analyze_seconds(10.3)
    snap = next(f for f in fs if f.code == "T2-snap")
    check(snap.data["min_grid_frames"] == 260 and snap.data["nearest_frames"] == 243,
          "--seconds 10.3 → 最小 260 帧（10.83s），最近 243 帧（10.12s）")
    fs = analyze_seconds(16)
    check([f.code for f in fs if f.level == "error"] == ["T2-split-required"] and "拆成两段" in fs[0].msg,
          "--seconds 16 → error T2-split-required（超过单次上限，必须拆成两段）")
    fs = analyze_seconds(45)
    check(fs[0].code == "T2-split-required" and fs[0].data["parts"] == 3 and "拆成 3 段" in fs[0].msg
          and "必须拆成两段" not in fs[0].msg,
          "--seconds 45 → 拆成 3 段（不自相矛盾地说'两段'）")
    fs = analyze_seconds(100)
    check(fs[0].data["parts"] == 7 and "拆成 7 段" in fs[0].msg, "--seconds 100 → 拆成 7 段，每段给出网格帧数")
    fs = analyze_seconds(3)
    check(any(f.code == "A1-below-min" and f.level == "warn" for f in fs)
          and next(f for f in fs if f.code == "T2-snap").data["min_grid_frames"] == 124,
          "--seconds 3 → warn A1-below-min，最小合法 124 帧")
    fs = analyze_seconds(15.08)
    check(not any(f.level == "error" for f in fs), "--seconds 15.08 → 362 帧，不要求拆段")
    fs = analyze_seconds(15.085)
    check("15.085s 已在网格上" in fs[0].msg, "--seconds 15.085 → 原样回显输入（不再显示成 15.09s 又说在网格上）")

    # 3. --frames
    check([f.code for f in analyze_frames(260)] == ["T2-ok"], "--frames 260 合法")
    f290 = analyze_frames(290)[0]
    check(f290.code == "T2-frames-offgrid" and f290.data["lower"] == 277 and f290.data["upper"] == 294,
          "--frames 290 → offgrid，相邻 277 / 294")
    check(analyze_frames(100)[0].code == "T2-frames-below-min", "--frames 100 → below-min")
    check(analyze_frames(400)[0].code == "T2-frames-above-max", "--frames 400 → above-max")

    # 4. fixtures
    good = check_prompts(ac.FIXTURES / "good" / "video-prompts.md")
    check(not any(f.level in ("error", "warn") for f in good), "fixtures/good/video-prompts.md → 0 error、0 warn")
    bad = check_prompts(ac.FIXTURES / "bad" / "video-prompts.md")
    check(errs(bad) == {("T2-frames-offgrid", "SHOT-003"), ("T2-frames-below-min", "SHOT-005")},
          "fixtures/bad：SHOT-003 帧数 290 离网格、SHOT-005 帧数 100 低于下限（且仅此两条 error）")
    b3 = next(f for f in bad if f.code == "T2-frames-offgrid")
    check(b3.data["recommended_frames"] == 294 and "294" in b3.msg and "12.25" in b3.msg,
          "SHOT-003 建议改为 294 帧 / 12.25s（≥12.00s 的最小网格值）")

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def doc(name: str, body: str, raw: bytes | None = None) -> Path:
            p = tdp / name
            p.parent.mkdir(parents=True, exist_ok=True)
            if raw is not None:
                p.write_bytes(raw)
            else:
                p.write_text(body, encoding="utf-8")
            return p

        # 5. 合成：时长不一致 / 帧数缺失 / 时长超上限
        p = doc("video-prompts.md", "\n".join([
            "# synth", "",
            "## SHOT-001", "- 时长: 11.00", "- 帧数: 260", "", "```h3", "summary:", "  x", "```", "",
            "## SHOT-002", "- 时长: 9.00", "", "```h3", "summary:", "  x", "```", "",
            "## SHOT-003", "- 时长: 16.00", "- 帧数: 384", "", "```h3", "summary:", "  x", "```", "",
            "## SHOT-004", "- 时长: 5.17", "- 帧数: 124", "", "```h3", "summary:", "  x", "```", "",
        ]) + "\n")
        fs = check_prompts(p)
        check(errs(fs) == {("T2-duration-mismatch", "SHOT-001"), ("T2-frames-missing", "SHOT-002"),
                           ("T2-frames-above-max", "SHOT-003")},
              "合成：260 帧配 11.00s → mismatch；缺帧数 → missing；384 帧 → above-max；124 帧/5.17s 通过")
        miss = next(f for f in fs if f.code == "T2-frames-missing")
        check(miss.data.get("recommended_frames") == 226 and "（无此行）" in miss.msg,
              "缺帧数且时长 9.00s → 建议 226 帧（9.42s），消息写'无此行'而不是 'None'")

        # 6. 对抗：BOM / CRLF（契约 §0.1 要求 UTF-8 无 BOM、LF；不能因此漏检）
        bad_bytes = (ac.FIXTURES / "bad" / "video-prompts.md").read_bytes()
        body = ("## SHOT-003\n- 时长: 12.00\n- 帧数: 290\n\n```h3\nsummary:\n  x\n```\n\n"
                "## SHOT-004\n- 时长: 10.83\n- 帧数: 260\n")
        p = doc("bom.md", "", b"\xef\xbb\xbf" + body.encode("utf-8"))
        fs = check_prompts(p)
        check(("T2-frames-offgrid", "SHOT-003") in errs(fs) and ("FMT-bom", "bom.md") in warns(fs),
              "BOM 开头且首镜即坏镜 → 仍报 SHOT-003 离网格（修复前：首镜被吞、exit 0 假通过）+ warn FMT-bom")
        p = doc("crlf.md", "", bad_bytes.replace(b"\n", b"\r\n"))
        check(errs(check_prompts(p)) == errs(bad), "CRLF 版 bad fixture → 与 LF 版结果一致")

        # 7. 对抗：不合契约的镜头标题（academy_common 不认 → 修复前整镜静默消失）
        p = doc("heads.md", "\n".join([
            "## SHOT-12", "- 时长: 12.00", "- 帧数: 290", "",
            "### SHOT-013", "- 时长: 4.00", "- 帧数: 96", "",
            "## shot-014", "- 时长: 4.00", "- 帧数: 96", "",
            "## 镜头 SHOT-015", "- 时长: 4.00", "",
            "## SHOT-016 · 苏晓冲刺（返工）", "- 时长: 10.83", "- 帧数: 260", "",
            "````markdown", "## SHOT-099", "- 帧数: 999", "```h3", "summary:", "```", "````", "",
            "## 说明：SHOT-001 到 SHOT-005 的共同约束", "",
        ]) + "\n")
        fs = check_prompts(p)
        heads = [f for f in fs if f.code == "FMT-shot-heading"]
        check(len(heads) == 4 and {f.data["suggest"] for f in heads} == {"SHOT-012", "SHOT-013", "SHOT-014", "SHOT-015"},
              "`## SHOT-12` / `### SHOT-013` / `## shot-014` / `## 镜头 SHOT-015` → 4 条 error FMT-shot-heading，并给出规范 ID")
        check(("T2-ok", "SHOT-016") in {(f.code, f.where.split(' · ')[0]) for f in fs}
              and not any("SHOT-099" in f.msg or "共同约束" in f.msg for f in fs),
              "带后缀的合法标题照常校验；代码块里的示例标题、说明性标题不误报")
        p = doc("fw-head.md", "# SHOT-001 到 SHOT-010 总览\n\n## ＳＨＯＴ－０１２\n- 时长: 12.00\n- 帧数: 290\n")
        fs = check_prompts(p)
        hd = [f for f in fs if f.code == "FMT-shot-heading"]
        check(len(hd) == 1 and hd[0].data["suggest"] == "SHOT-012",
              "全角标题 `## ＳＨＯＴ－０１２` → FMT-shot-heading；区间标题「# SHOT-001 到 SHOT-010 总览」不误报")
        p = doc("absorb.md", "## SHOT-001\n- 时长: 10.83\n- 帧数: 260\n\n## SHOT-2\n- 时长: 12.00\n- 帧数: 290\n")
        fs = check_prompts(p)
        hd = next((f for f in fs if f.code == "FMT-shot-heading"), None)
        check(hd is not None and hd.data["absorbed_by"] == "SHOT-001" and "SHOT-001 头上" in hd.msg,
              "坏标题下的元数据被并进上一镜（SHOT-001 被误报离网格）→ FMT-shot-heading 明确指出 SHOT-001 结论不可信")

        # 8. 对抗：键名/值的非契约写法 → 按值校验 + warn（修复前：误报缺失 / NaN 被当成通过）
        p = doc("values.md", "\n".join([
            "## SHOT-001", "- **帧数**: 260", "- **时长**: 10.83", "",
            "## SHOT-002", "- 帧数: `260`", "- 时长: `10.83`", "",
            "## SHOT-003", "- 时长: 10.83s", "- 帧数: 260帧（10.83s）", "",
            "## SHOT-004", "- 时长：１０．８３", "- 帧数：２６０", "",
            "## SHOT-005", "- 时长: nan", "- 帧数: 260", "",
            "## SHOT-006", "- 时长: 10.83", "", "```h3", "summary:", "  x", "```", "- 帧数: 290", "",
            "## SHOT-007", "- 时长: 0", "- 帧数: 260", "",
            "## SHOT-007", "- 时长: 10.83", "- 帧数: 260", "",
        ]) + "\n")
        fs = check_prompts(p)
        e, w = errs(fs), warns(fs)
        check(not any(c[1] in ("SHOT-001", "SHOT-002", "SHOT-003", "SHOT-004") for c in e)
              and {("FMT-meta-key", "SHOT-001"), ("FMT-value", "SHOT-002"), ("FMT-value", "SHOT-003"),
                   ("FMT-value", "SHOT-004")} <= w,
              "加粗键名 / 反引号值 / `260帧（10.83s）` / 全角数字 → 按值通过，只出 FMT warn")
        check(("T2-duration-missing", "SHOT-005") in e and not any(f.code == "T2-ok" and "SHOT-005" in f.where for f in fs),
              "时长 nan → T2-duration-missing（修复前：'与时长 nans 一致' 假通过）")
        s6 = next(f for f in fs if f.code == "T2-frames-missing" and "SHOT-006" in f.where)
        check("代码块之前" in s6.msg and "第 " in s6.msg and "- 帧数: 290" in s6.msg,
              "元数据写在 h3 代码块之后 → T2-frames-missing 并指出那一行、要求挪到代码块之前")
        check(("T2-duration-missing", "SHOT-007") in e and ("FMT-dup-shot", "SHOT-007") in w,
              "时长 0 → duration-missing；重复镜号 → warn FMT-dup-shot")

        # 9. 路径含空格与中文
        p = doc("第 3 集 素材/video prompts.md", "## SHOT-001\n- 时长: 12.00\n- 帧数: 290\n")
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + ["--check", str(p)], capture_output=True, text=True)
        check(r.returncode == 1 and "T2-frames-offgrid" in r.stdout, "路径含空格与中文 → 正常解析（exit 1，报离网格）")

        # 10. CLI 契约：退出码与 --json
        r = subprocess.run(me + ["--check", str(ac.FIXTURES / "good" / "video-prompts.md"), "--json"],
                           capture_output=True, text=True)
        ok_json = False
        try:
            ok_json = json.loads(r.stdout)["ok"] is True
        except Exception:
            pass
        check(r.returncode == 0 and ok_json, "CLI good → 退出码 0，--json 可解析且 ok=true")
        r = subprocess.run(me + ["--check", str(ac.FIXTURES / "bad" / "video-prompts.md")], capture_output=True, text=True)
        check(r.returncode == 1 and "T2-frames-offgrid" in r.stdout, "CLI bad → 退出码 1，报告含 T2-frames-offgrid")
        r = subprocess.run(me + ["--check", str(tdp / "nope.md")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 文件不存在 → 退出码 2")
        r = subprocess.run(me, capture_output=True, text=True)
        check(r.returncode == 2, "CLI 无参数 → 退出码 2")
        bad_cli = [["--seconds", "nan"], ["--seconds", "inf"], ["--seconds", "0"], ["--frames", "0"],
                   ["--tol", "nan", "--table"], ["--seconds", "1e308"]]
        codes = [subprocess.run(me + a, capture_output=True, text=True).returncode for a in bad_cli]
        check(codes == [2] * len(bad_cli), f"CLI 非法数值（nan/inf/0/1e308/--tol nan）→ 全部退出码 2（实得 {codes}）")
        binp = doc("bin.md", "", b"\xff\xfe\x00\x01")
        r = subprocess.run(me + ["--check", str(binp)], capture_output=True, text=True)
        check(r.returncode == 2 and "UTF-8" in r.stderr, "CLI 非 UTF-8 文件 → 退出码 2 并说明编码")

    failed = [lbl for ok, lbl in results if not ok]
    print(f"\nselftest {'PASS' if not failed else 'FAIL'}：{len(results) - len(failed)}/{len(results)} 通过")
    return 0 if not failed else 1


# ------------------------------------------------------------------ CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seconds", type=float, help="目标秒数：输出 ≥S 的最小合法帧数与最近合法帧数")
    ap.add_argument("--frames", type=int, help="校验一个帧数是否在网格上且在 124–362 内")
    ap.add_argument("--table", action="store_true", help="打印完整网格（k / 帧数 / 秒）")
    ap.add_argument("--check", nargs="+", metavar="VIDEO_PROMPTS_MD", help="校验 video-prompts.md 每镜的帧数与时长")
    ap.add_argument("--tol", type=float, default=0.05, help="|帧数/24 − 时长| 的容差秒数（默认 0.05）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="运行自测（fixtures + 合成/对抗样例），全部通过退出 0")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.seconds is None and a.frames is None and not a.table and not a.check:
        ap.print_usage(sys.stderr)
        ac.die("至少给出 --seconds / --frames / --table / --check 之一（或 --selftest）")
    if a.seconds is not None and not (math.isfinite(a.seconds) and 0 < a.seconds <= MAX_INPUT_SEC):
        ac.die(f"--seconds 必须是 (0, {MAX_INPUT_SEC:g}] 内的有限数字（收到 {a.seconds}）")
    if a.frames is not None and a.frames < 1:
        ac.die(f"--frames 必须 ≥ 1（收到 {a.frames}）")
    if not math.isfinite(a.tol) or a.tol < 0:
        ac.die(f"--tol 必须是 ≥0 的有限数字（收到 {a.tol}）")

    findings: list[ac.Finding] = []
    extra: dict = {}
    if a.table:
        extra["grid"] = grid_rows()
        extra["summary"] = table_text()
    if a.seconds is not None:
        findings += analyze_seconds(a.seconds)
    if a.frames is not None:
        findings += analyze_frames(a.frames)
    for p in a.check or []:
        if not Path(p).is_file():
            ac.die(f"找不到文件：{p}")
        try:
            findings += check_prompts(p, a.tol)
        except UnicodeDecodeError:
            ac.die(f"{p} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8（无 BOM）后重跑")
    return ac.emit(TITLE, findings, a.json, extra or None)


if __name__ == "__main__":
    sys.exit(main())
