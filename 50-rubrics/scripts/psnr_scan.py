#!/usr/bin/env python3
"""psnr_scan.py — 相邻帧 PSNR 扫描：找死段/冻结、镜内跳变、成片切点

用途：
  把视频与"自身错开一帧"的副本逐帧比 PSNR（ffmpeg psnr 滤镜，stats_file 逐帧 psnr_avg；inf 记 99 dB），
  得到相邻帧相似度曲线，报告两类事实：
  (a) 死段/冻结：连续 ≥ --freeze-min 对（默认 12 对 ≈ 0.5s@24fps）PSNR ≥ --freeze-db（默认 45 dB）
      → warn「死段/冻结（若非设计静场需重出或剪掉）」；
  (b) 跳变/切点：PSNR ≤ --cut-db（默认 18 dB），或比本片中位数低 > 3 个稳健 z 分（MAD）且落差 ≥ --min-drop dB；
      若本片中位 ≤ --cut-db + --min-drop/2（默认 21 dB：高颗粒/雨雪/快动作/闪烁镜），绝对阈值对本片无信息量，
      停用、只用稳健 z 判据，并报 info P8-low-baseline——实测 noise=45 的 testsrc2 中位 16.3 dB，143 对全 ≤18 dB，
      旧规则把整镜并成一个假"跳变"；快速平移镜（中位 13.5 dB）则报出 15 个 z≈-2 的假跳变
      → --mode clip（单个生成镜）：warn「镜内跳变：疑似崩解或换景」；
        --mode final（成片）：info「切点」（预期剪辑点）；给 --edit-list 时与剪辑单切点逐一对齐，
        不在剪辑单切点上的跳变 → warn，剪辑单上的 local: 纯色卡静止 → info（设计静场）。
  成片模式另报检出切点数与平均镜长（A1：平均 < 5s 告警；给 --edit-list 时扣除 local: 纯色卡——设计黑卡不是镜）。输出时间戳（秒）与紧凑 ASCII 走势线。
  脚本只报告事实与下一步动作，不判断"好不好看"；跳变是否为崩解需用 contact_sheet.py 抽帧目视（D5：双通道）。

溯源：P8（视频验收固定环节"PSNR 相邻帧扫描（找死段/切点）"+"成片切点逐帧目视"）、
      A1（碎镜症：29 镜均长 2.96s；切点密度即碎镜程度）、D5（工具会骗人：单通道不判决，跳变须抽帧复核）。

输入格式：
  视频文件（.mp4 .mov .mkv .webm .m4v .avi）或含视频的目录。
  --edit-list：70-playbooks/format-contracts.md §4「剪辑单（edit-list.md）」，
  表头 `CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字`，按行序累加 (出点−入点) 得到成片中的预期切点；
  解析统一使用 academy_common.find_rows（与 parse_edit_list 同一解析器），但按 utf-8-sig 读入：
  带 BOM 的剪辑单首行表头不会丢（BOM 不是空白，表头行会被当成正文）。剪辑单无有效行 → 按无剪辑单处理。

判定：
  warn  P8-freeze           死段/冻结（连续高 PSNR）
  info  P8-freeze-designed  冻结段落在剪辑单 local: 纯色卡区间内（设计静场）
  warn  P8-jump             （clip 模式）镜内跳变
  info  P8-cut              （final 模式，无剪辑单）检出切点
  info  P8-cut-expected     （final + 剪辑单）检出切点与剪辑单切点吻合
  warn  P8-cut-unexpected   （final + 剪辑单）跳变不在任何剪辑单切点上
  info  P8-cut-undetected   （final + 剪辑单）剪辑单切点处未检出明显跳变（同景接同景/叠化时正常）
  info  A1-shot-stats       （final）检出镜数与平均镜长
  warn  A1-mean-short       （final）平均镜长 < 5s
  info  P8-psnr-stats       帧数、PSNR 中位/最小值
  info  P8-low-baseline     本镜相邻帧 PSNR 中位已接近 --cut-db（高颗粒/快动作/闪烁）：本镜停用绝对阈值，只用稳健 z
  warn  P8-too-short        帧数 < 2，无法比较
  warn  P8-no-clips         目录中没有视频文件
  warn  P8-edit-duration    （final + 剪辑单）剪辑单总长与成片相差 > 0.5s
  warn  FMT-edit-list       剪辑单缺表或某行入点/出点无效
  error P8-unreadable       视频无法探测/解码

用法示例：
  python3 psnr_scan.py season-01/ep03/assets/clips/SHOT-004.mp4
  python3 psnr_scan.py season-01/ep03/assets/clips/ --json > qc/psnr.json
  python3 psnr_scan.py final/ep03.mp4 --mode final --edit-list season-01/ep03/edit-list.md
  python3 psnr_scan.py SHOT-004.mp4 --freeze-db 45 --freeze-min 12 --cut-db 18
  python3 psnr_scan.py --selftest

退出码：0 通过（只有 warn/info）/ 1 发现 error（无法解码）/ 2 用法或环境错误。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "相邻帧 PSNR 扫描：死段 / 跳变 / 切点（P8 / A1）"
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
INF_DB = 99.0
BARS = "▁▂▃▄▅▆▇█"
SPARK_LO, SPARK_HI = 10.0, 50.0
SIGMA_FLOOR = 0.75        # 稳健 σ 下限（dB），防止静态片 MAD≈0 时任何小抖动都算跳变
MIN_MEAN_SHOT = 5.0       # A1：任何 <5s 的镜要理由；均长 < 5s 即碎镜


# ------------------------------------------------------------------ ffmpeg 小工具

def need_ffmpeg():
    missing = [t for t in ("ffmpeg", "ffprobe") if not ac.have(t)]
    if missing:
        ac.die(f"找不到 {' / '.join(missing)}：安装 ffmpeg（含 ffprobe）并加入 PATH 后重跑")


def ff_has_filter(name: str) -> bool:
    p = ac.run(["ffmpeg", "-hide_banner", "-filters"], timeout=60)
    return any(re.match(rf"^\s*[A-Z.|]{{2,3}}\s+{name}\s", ln) for ln in p.stdout.splitlines())


def _ratio(s, default: float = 0.0) -> float:
    try:
        a, b = str(s).replace(":", "/").split("/", 1) if "/" in str(s) or ":" in str(s) else (s, 1)
        a, b = float(a), float(b)
        return a / b if b else default
    except (TypeError, ValueError):
        return default


def probe(path: Path) -> dict:
    info = ac.ffprobe_json(path)
    vs = [s for s in info.get("streams", []) if s.get("codec_type") == "video"
          and not s.get("disposition", {}).get("attached_pic")]
    if not vs:
        raise RuntimeError("文件中没有视频流")
    v = vs[0]
    fps_s = v.get("avg_frame_rate", "0/0")
    if not _ratio(fps_s):
        fps_s = v.get("r_frame_rate", "24/1")
    fps = _ratio(fps_s) or 24.0
    dur = float(v.get("duration") or info.get("format", {}).get("duration") or 0.0)
    return {"fps": round(fps, 3), "fps_frac": str(Fraction(fps).limit_denominator(1001)), "duration": round(dur, 3),
            "width": int(v.get("width") or 0), "height": int(v.get("height") or 0)}


def parse_stats(text: str) -> list[float]:
    """ffmpeg psnr stats_file → 每行 psnr_avg（inf → 99）。"""
    out = []
    for ln in text.splitlines():
        m = re.search(r"psnr_avg:(\S+)", ln)
        if not m:
            continue
        v = m.group(1).lower()
        try:
            x = INF_DB if v in ("inf", "+inf", "nan") else float(v)
        except ValueError:
            continue
        out.append(min(x, INF_DB))
    return out


def psnr_series(clip: Path, fps_frac: str) -> list[float]:
    """第 i 个值 = 帧 i 与帧 i+1 的 PSNR（dB）。时间戳统一重排为 N/fps，避免 pts 抖动导致错配。"""
    fc = (f"[0:v]split[a0][b0];[a0]setpts=N/({fps_frac}*TB)[a];"
          f"[b0]trim=start_frame=1,setpts=N/({fps_frac}*TB)[b];"
          f"[a][b]psnr=stats_file=psnr.log:shortest=1")
    with tempfile.TemporaryDirectory(prefix="psnr_") as td:
        # stats_file 用相对名 + cwd，避免在滤镜参数里转义路径（Windows 盘符冒号等）
        p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-v", "error", "-i", str(Path(clip).resolve()),
                            "-filter_complex", fc, "-an", "-sn", "-f", "null", "-"],
                           capture_output=True, text=True, timeout=1800, cwd=td)
        log = Path(td) / "psnr.log"
        if p.returncode != 0 or not log.exists():
            raise RuntimeError(p.stderr.strip()[-300:] or "ffmpeg psnr 失败")
        return parse_stats(log.read_text(encoding="utf-8", errors="replace"))


# ------------------------------------------------------------------ 分析

def robust_stats(series: list[float], freeze_db: float) -> tuple[float | None, float | None]:
    vals = [v for v in series if v < freeze_db]
    if len(vals) < 5:
        return (statistics.median(series) if series else None), None
    med = statistics.median(vals)
    mad = statistics.median([abs(v - med) for v in vals])
    return med, max(1.4826 * mad, SIGMA_FLOOR)


def find_freezes(series: list[float], fps: float, freeze_db: float, freeze_min: int) -> list[dict]:
    out, i, n = [], 0, len(series)
    while i < n:
        if series[i] >= freeze_db:
            j = i
            while j + 1 < n and series[j + 1] >= freeze_db:
                j += 1
            if j - i + 1 >= freeze_min:
                # 对 i..j 表示帧 i..j+1 静止
                out.append({"pair_start": i, "pair_end": j, "first_frame": i, "last_frame": j + 1,
                            "frames": j - i + 2, "start": round(i / fps, 3), "end": round((j + 2) / fps, 3),
                            "duration": round((j - i + 2) / fps, 3)})
            i = j + 1
        else:
            i += 1
    return out


def low_baseline(med: float | None, freeze_db: float, cut_db: float, min_drop: float) -> bool:
    return med is not None and med < freeze_db and med <= cut_db + min_drop / 2


def find_jumps(series: list[float], fps: float, freeze_db: float, cut_db: float, z_thr: float,
               min_drop: float) -> tuple[list[dict], float | None, float | None]:
    med, sigma = robust_stats(series, freeze_db)
    # 本片常态已贴近 cut-db（高颗粒/快动作）→ 绝对阈值无信息量，停用，只用稳健 z（见 low_baseline）
    abs_on = not low_baseline(med, freeze_db, cut_db, min_drop)
    cand = []
    for i, v in enumerate(series):
        if v >= freeze_db:
            continue
        z = (v - med) / sigma if (sigma and med is not None) else None
        abs_hit = abs_on and v <= cut_db
        if abs_hit or (z is not None and z < -z_thr and med - v >= min_drop):
            cand.append(i)
    events, k = [], 0
    while k < len(cand):
        g = [cand[k]]
        while k + 1 < len(cand) and cand[k + 1] - g[-1] <= 1:
            k += 1
            g.append(cand[k])
        i_min = min(g, key=lambda i: series[i])
        z = (series[i_min] - med) / sigma if (sigma and med is not None) else None
        events.append({"pair": i_min, "frame": i_min + 1, "t": round((i_min + 1) / fps, 3),
                       "span": [round((g[0] + 1) / fps, 3), round((g[-1] + 1) / fps, 3)],
                       "psnr": round(series[i_min], 2), "z": round(z, 1) if z is not None else None,
                       "reason": "abs" if series[i_min] <= cut_db else "z"})
        k += 1
    return events, med, sigma


def edit_list_cuts(path: Path) -> tuple[list[float], list[tuple[float, float, str]], float, list[ac.Finding]]:
    """剪辑单 → (成片内预期切点秒数, local: 纯色卡区间, 总长, 解析告警)。"""
    fs, cuts, locals_, t = [], [], [], 0.0
    text = Path(path).read_text(encoding="utf-8-sig")       # BOM 安全；解析器与 ac.parse_edit_list 相同
    rows = ac.find_rows(text, ["CUT", "来源"])
    if not rows:
        fs.append(ac.Finding("warn", "FMT-edit-list", "剪辑单里没有 `CUT | 来源 | 入点 | 出点` 表（format-contracts §4）",
                             str(path)))
    for r in rows:
        tin, tout = ac.to_float(r.get("入点", "")), ac.to_float(r.get("出点", ""))
        cut = r.get("CUT", "?")
        if tin is None or tout is None or tout <= tin:
            shown = " / ".join("（缺列）" if r.get(k) is None else (r.get(k) or "（空）") for k in ("入点", "出点"))
            fs.append(ac.Finding("warn", "FMT-edit-list",
                                 f"{cut} 入点/出点无效（{shown}）：入点、出点写秒数两位小数且出点 > 入点"
                                 f"（format-contracts §4）；该行之后的预期切点时间不可靠，先修剪辑单", f"{path}:{r['_line']}"))
            continue
        src = r.get("来源", "").strip().strip("`")
        if re.match(r"^local\s*[:：]", src, re.I):    # 写法错误（全角冒号等）由 asset_exists.py 报；这里只认"是纯色卡"
            locals_.append((t, t + (tout - tin), cut))
        t += tout - tin
        cuts.append(round(t, 3))
    total = cuts[-1] if cuts else 0.0
    return cuts[:-1], locals_, total, fs


def sparkline(series: list[float], width: int, freezes: list[dict], events: list[dict]) -> tuple[str, str]:
    n = len(series)
    if n == 0:
        return "", ""
    width = max(1, min(width, n))
    fz = set()
    for f in freezes:
        fz.update(range(f["pair_start"], f["pair_end"] + 1))
    ev = {e["pair"] for e in events}
    line, marks = [], []
    for b in range(width):
        s, e = b * n // width, max(b * n // width + 1, (b + 1) * n // width)
        v = min(series[s:e])
        x = (min(max(v, SPARK_LO), SPARK_HI) - SPARK_LO) / (SPARK_HI - SPARK_LO)
        line.append(BARS[min(7, int(x * 7.999))])
        rng = set(range(s, e))
        marks.append("^" if rng & ev else ("F" if rng & fz else " "))
    return "".join(line), "".join(marks)


def analyze(series: list[float], fps: float, where: str, mode: str = "clip", freeze_db: float = 45.0,
            freeze_min: int = 12, cut_db: float = 18.0, z_thr: float = 3.0, min_drop: float = 6.0,
            edit: tuple | None = None, cut_tol: float | None = None, width: int = 72) -> tuple[list[ac.Finding], dict]:
    fs: list[ac.Finding] = []
    n = len(series)
    dur = (n + 1) / fps
    if n == 0:
        fs.append(ac.Finding("warn", "P8-too-short", "帧数 < 2，无法做相邻帧比较：确认导出是否完整", where))
        return fs, {"frames": n + 1}
    freezes = find_freezes(series, fps, freeze_db, freeze_min)
    events, med, sigma = find_jumps(series, fps, freeze_db, cut_db, z_thr, min_drop)
    spark, marks = sparkline(series, width, freezes, events)
    rec = {"frames": n + 1, "fps": fps, "duration": round(dur, 3), "median": round(med, 2) if med is not None else None,
           "sigma": round(sigma, 2) if sigma else None, "min": round(min(series), 2), "freezes": freezes,
           "events": events, "sparkline": spark, "marks": marks}
    fs.append(ac.Finding("info", "P8-psnr-stats",
                         f"{n + 1} 帧 / {dur:.2f}s；相邻帧 PSNR 中位 {rec['median']} dB，最小 {rec['min']} dB；"
                         f"冻结段 {len(freezes)}，跳变 {len(events)}", where))
    if low_baseline(med, freeze_db, cut_db, min_drop):
        fs.append(ac.Finding("info", "P8-low-baseline",
                             f"本镜相邻帧 PSNR 中位 {med:.1f} dB 已接近 --cut-db {cut_db:g}（高颗粒/雨雪/快动作/闪烁）："
                             f"本镜停用绝对阈值，只按稳健 z（比中位低 >{z_thr:g}σ 且 ≥{min_drop:g} dB）判跳变，灵敏度下降——"
                             f"用 contact_sheet.py 抽帧目视补足（D5 双通道）", where, {"median": round(med, 2)}))

    locals_ = edit[1] if edit else []
    for f in freezes:
        w = f"{where} @ {f['start']:.2f}s"
        designed = [c for (a, b, c) in locals_ if f["start"] >= a - 0.1 and f["end"] <= b + 0.1]
        if designed:
            fs.append(ac.Finding("info", "P8-freeze-designed",
                                 f"静止 {f['start']:.2f}–{f['end']:.2f}s 落在剪辑单 {designed[0]} 的 local: 纯色卡内（设计静场）",
                                 w, f))
            continue
        tip = "；成片中的设计定格/字卡可忽略，其余回查对应镜" if mode == "final" else ""
        fs.append(ac.Finding("warn", "P8-freeze",
                             f"死段/冻结 {f['start']:.2f}–{f['end']:.2f}s（{f['duration']:.2f}s，{f['frames']} 帧 "
                             f"PSNR≥{freeze_db:g} dB）：若非设计静场需重出或剪掉（剪到 {f['start']:.2f}s 前，"
                             f"或该段换 seed 重出）{tip}", w, f))

    if mode == "clip":
        for e in events:
            a, b = max(0.0, e["t"] - 0.2), min(dur, e["t"] + 0.2)
            ztxt = "" if e["z"] is None else f"，z={e['z']}"
            fs.append(ac.Finding("warn", "P8-jump",
                                 f"镜内跳变 t={e['t']:.2f}s（PSNR {e['psnr']:.1f} dB，本镜中位 {rec['median']}{ztxt}）"
                                 f"：疑似崩解或换景——用 "
                                 f"contact_sheet.py 抽 {a:.2f}–{b:.2f}s 帧目视（D5：单通道不判决）；崩解 → 换 seed 重出"
                                 f"或在 {e['t']:.2f}s 前截断", f"{where} @ {e['t']:.2f}s", e))
    else:
        tol = cut_tol if cut_tol is not None else max(0.1, 2.0 / fps)
        if edit:
            exp_cuts, _, total, _ = edit
            matched = set()
            for e in events:
                hit = [c for c in exp_cuts if abs(c - e["t"]) <= tol]
                if hit:
                    matched.add(hit[0])
                    fs.append(ac.Finding("info", "P8-cut-expected",
                                         f"切点 t={e['t']:.2f}s 与剪辑单切点 {hit[0]:.2f}s 吻合（PSNR {e['psnr']:.1f} dB）："
                                         f"按 P8 逐帧目视该切点前后 2 帧", f"{where} @ {e['t']:.2f}s", e))
                else:
                    fs.append(ac.Finding("warn", "P8-cut-unexpected",
                                         f"跳变 t={e['t']:.2f}s 不在任何剪辑单切点上（±{tol:.2f}s；PSNR {e['psnr']:.1f} dB）："
                                         f"可能是镜内崩解/换景，或剪辑单入出点与成片不符——抽帧目视并核对剪辑单",
                                         f"{where} @ {e['t']:.2f}s", e))
            for c in exp_cuts:
                if c not in matched:
                    fs.append(ac.Finding("info", "P8-cut-undetected",
                                         f"剪辑单切点 {c:.2f}s 未检出明显跳变（同景接同景/叠化时正常；否则核对入出点与渲染）",
                                         f"{where} @ {c:.2f}s"))
            if total and abs(total - dur) > 0.5:
                fs.append(ac.Finding("warn", "P8-edit-duration",
                                     f"剪辑单总长 {total:.2f}s 与成片 {dur:.2f}s 相差 {abs(total - dur):.2f}s："
                                     f"剪辑单与渲染不一致，先对齐再判切点", where))
        else:
            for e in events:
                fs.append(ac.Finding("info", "P8-cut",
                                     f"切点 t={e['t']:.2f}s（PSNR {e['psnr']:.1f} dB）：预期剪辑点——与剪辑单核对，"
                                     f"并按 P8 逐帧目视切点前后 2 帧", f"{where} @ {e['t']:.2f}s", e))
        shots = len(events) + 1
        mean = dur / shots
        n_loc = len(locals_)                    # 剪辑单 local: 纯色卡（片尾黑卡等）是设计静场，不是"镜"，不计入均长（A1）
        t_loc = sum(b - a for a, b, _ in locals_)
        loc_txt = ""
        if n_loc and shots - n_loc >= 1 and dur - t_loc > 0:
            mean = (dur - t_loc) / (shots - n_loc)
            loc_txt = f"，扣除 {n_loc} 段 local: 纯色卡（{t_loc:.2f}s）后有效 {shots - n_loc} 镜"
        rec["shots_detected"], rec["mean_shot"] = shots, round(mean, 2)
        fs.append(ac.Finding("info", "A1-shot-stats",
                             f"检出 {shots} 个镜段（{len(events)} 个切点）{loc_txt}，平均 {mean:.2f}s/镜（叠化/同景切可能漏检）",
                             where))
        if mean < MIN_MEAN_SHOT:
            fs.append(ac.Finding("warn", "A1-mean-short",
                                 f"平均镜长 {mean:.2f}s < {MIN_MEAN_SHOT:g}s（A1 实证：29 镜均长 2.96s，人类主创原话「片段式、剧情跳跃、无法理解」）："
                                 f"回到分镜按段合并为 8–15s 长段多拍（segment_rhythm.py 复查）", where))
    return fs, rec


# ------------------------------------------------------------------ 输入

def collect_clips(paths: list[str], recursive: bool) -> tuple[list[Path], list[ac.Finding]]:
    clips, fs = [], []
    for s in paths:
        p = Path(s)
        if not p.exists():
            ac.die(f"找不到路径：{s}")
        if p.is_dir():
            it = p.rglob("*") if recursive else p.iterdir()
            found = sorted(q for q in it if q.is_file() and q.suffix.lower() in VIDEO_EXTS)
            if not found:
                fs.append(ac.Finding("warn", "P8-no-clips", "目录中没有视频文件：确认路径，或加 --recursive", str(p)))
            clips += found
        else:
            clips.append(p)
    return clips, fs


def scan_clip(clip: Path, opts: dict, edit: tuple | None) -> tuple[list[ac.Finding], dict]:
    try:
        pr = probe(clip)
        series = psnr_series(clip, pr["fps_frac"])
    except Exception as e:  # noqa: BLE001
        return [ac.Finding("error", "P8-unreadable",
                           f"无法探测/解码：{str(e)[:200]}——重新导出或重新下载后再验收", clip.name)], {"clip": str(clip)}
    fs, rec = analyze(series, pr["fps"], clip.name, edit=edit, **opts)
    rec.update({"clip": str(clip), "psnr": [round(v, 2) for v in series]})
    return fs, rec


def summary_text(records: list[dict]) -> str:
    if not any(r.get("sparkline") for r in records):
        return ""
    lines = [f"走势线：每格取该时段最小 PSNR，{BARS[0]}≤{SPARK_LO:g}dB … {BARS[-1]}≥{SPARK_HI:g}dB；标记 F=冻结 ^=跳变/切点"]
    for r in records:
        if not r.get("sparkline"):
            continue
        name = Path(r["clip"]).name
        head = f"{name}  0s ▕"
        lines.append(f"{head}{r['sparkline']}▏{r['duration']:.2f}s")
        lines.append(" " * len(head) + r["marks"])
    return "\n".join(lines)


# ------------------------------------------------------------------ 自测

def _synth(args: list[str], out: Path) -> Path:
    p = ac.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + args + [str(out)])
    if p.returncode != 0:
        raise RuntimeError(f"合成失败：{p.stderr.strip()[-300:]}")
    return out


def _venc() -> list[str]:
    p = ac.run(["ffmpeg", "-hide_banner", "-encoders"])
    if "libx264" in p.stdout:
        return ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16"]
    return ["-c:v", "mpeg4", "-q:v", "2", "-pix_fmt", "yuv420p"]


def selftest() -> int:
    need_ffmpeg()
    if not ff_has_filter("psnr"):
        ac.die("ffmpeg 缺 psnr 滤镜，无法自测")
    results: list[tuple[bool, str]] = []

    def check(cond, label):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    # 1. 纯逻辑
    check(parse_stats("n:1 mse_avg:0.00 psnr_avg:inf psnr_y:inf\nn:2 mse_avg:3.1 psnr_avg:33.21 psnr_y:34\n") == [99.0, 33.21],
          "stats_file 解析：inf → 99，数值原样")
    ser = [30.0] * 20 + [99.0] * 15 + [30.0] * 5 + [9.0] + [30.0] * 10
    fz = find_freezes(ser, 24, 45, 12)
    check(len(fz) == 1 and fz[0]["first_frame"] == 20 and fz[0]["frames"] == 16, "合成序列：一段 16 帧冻结")
    ev, med, sg = find_jumps(ser, 24, 45, 18, 3.0, 6.0)
    check(len(ev) == 1 and ev[0]["frame"] == 41 and med == 30.0 and sg == SIGMA_FLOOR,
          "合成序列：一处跳变（帧 41），静态序列 σ 取下限 0.75 dB")
    ser2 = [30.0] * 30 + [22.5] + [30.0] * 30
    ev2, _, _ = find_jumps(ser2, 24, 45, 18, 3.0, 6.0)
    check(len(ev2) == 1 and ev2[0]["reason"] == "z", "高于 cut-db 但低于中位 7.5 dB（>3z 且 ≥6 dB）→ 稳健 z 检出")
    ser3 = [30.0] * 30 + [26.0] + [30.0] * 30
    check(not find_jumps(ser3, 24, 45, 18, 3.0, 6.0)[0], "只低 4 dB（< --min-drop 6）→ 不算跳变")
    grain = [16.6 + 0.05 * ((i * 7) % 5) for i in range(140)]
    check(not find_jumps(grain, 24, 45, 18, 3.0, 6.0)[0],
          "高颗粒镜：相邻帧全在 16.6–16.8 dB（≤ cut-db 但无落差）→ 不并成假跳变（回归）")
    check([e["frame"] for e in find_jumps(grain[:70] + [9.0] + grain[70:], 24, 45, 18, 3.0, 6.0)[0]] == [71],
          "高颗粒镜中真切点（9 dB，比中位低 7.6 dB）仍检出")
    fast = [13.5 + (((i * 5) % 7) - 3) * 0.9 for i in range(140)]
    check(not find_jumps(fast, 24, 45, 18, 3.0, 6.0)[0],
          "快动作镜：中位 13.5 dB、在 10.8–16.2 dB 间起伏 → 不报 z≈-2 的假跳变（回归）")
    sp, mk = sparkline(ser, 25, fz, ev)
    check(len(sp) == 25 and "^" in mk and "F" in mk and BARS[-1] in sp, "走势线长度=宽度，含 F 与 ^ 标记")

    venc = _venc()
    with tempfile.TemporaryDirectory(prefix="psnr_selftest_") as tds:
        td = Path(tds)
        # 2. testsrc2 2s + 冻结 1s（tpad clone）+ mandelbrot 1s
        clip = _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24:d=2", "-f", "lavfi", "-i", "mandelbrot=s=270x480:r=24",
                       "-filter_complex", "[0:v]tpad=stop_mode=clone:stop_duration=1[a];"
                       "[1:v]trim=duration=1,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]",
                       "-map", "[v]"] + venc, td / "SHOT-007.mp4")
        opts = dict(mode="clip", freeze_db=45.0, freeze_min=12, cut_db=18.0, z_thr=3.0, min_drop=6.0)
        fs, rec = scan_clip(clip, opts, None)
        fr = [f for f in fs if f.code == "P8-freeze"]
        check(len(fr) == 1 and abs(fr[0].data["start"] - 2.0) <= 0.1 and abs(fr[0].data["duration"] - 1.0) <= 0.12,
              f"冻结段 ≈ 2.0s 起、≈1.0s 长（实得 {fr[0].data['start'] if fr else '—'}s / "
              f"{fr[0].data['duration'] if fr else '—'}s）→ warn P8-freeze")
        jp = [f for f in fs if f.code == "P8-jump"]
        check(len(jp) == 1 and jp[0].level == "warn" and abs(jp[0].data["t"] - 3.0) <= 0.1,
              f"clip 模式：唯一跳变 ≈ 3.0s（实得 {jp[0].data['t'] if jp else '—'}s）→ warn P8-jump")
        check(not [f for f in fs if f.level == "error"] and rec["frames"] == 96 and len(rec["psnr"]) == 95,
              "96 帧 → 95 个相邻帧 PSNR，0 error")

        fs, rec = scan_clip(clip, dict(opts, mode="final"), None)
        check(any(f.code == "P8-cut" and f.level == "info" for f in fs) and not any(f.code == "P8-jump" for f in fs),
              "final 模式：同一跳变报 info P8-cut（预期剪辑点）")
        check(any(f.code == "A1-mean-short" for f in fs) and rec["shots_detected"] == 2,
              "final 模式：2 个镜段、均长 2.0s → warn A1-mean-short")

        el = td / "edit-list.md"
        el.write_text("| CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字 |\n|---|---|---|---|---|---|\n"
                      "| CUT-001 | assets/a.mp4 | 0.00 | 2.00 | — | — |\n"
                      "| CUT-002 | local:black | 0.00 | 1.00 | — | — |\n"
                      "| CUT-003 | assets/b.mp4 | 0.00 | 1.00 | — | — |\n", encoding="utf-8")
        edit = edit_list_cuts(el)
        check(edit[0] == [2.0, 3.0] and edit[1][0][:2] == (2.0, 3.0) and edit[2] == 4.0,
              "剪辑单解析：预期切点 2.00/3.00s，local:black 区间 2–3s，总长 4.00s")
        fs, _ = scan_clip(clip, dict(opts, mode="final"), edit)
        check(any(f.code == "P8-cut-expected" for f in fs) and any(f.code == "P8-freeze-designed" for f in fs)
              and not any(f.code in ("P8-cut-unexpected", "P8-freeze") for f in fs),
              "剪辑单对齐：3.00s 切点吻合；冻结段落在 local:black 内 → info（设计静场）")
        check(any(f.code == "P8-cut-undetected" and "2.00" in f.msg for f in fs),
              "剪辑单 2.00s 切点（接纯色卡、画面冻结开始）无跳变 → info P8-cut-undetected")
        st = next(f for f in fs if f.code == "A1-shot-stats")
        check("扣除 1 段 local: 纯色卡" in st.msg and "平均 3.00s" in st.msg,
              "A1 均长扣除剪辑单 local: 纯色卡（设计黑卡不算镜；回归：曾把片尾黑卡算进碎镜）")
        bom = td / "edit-list-bom.md"
        bom.write_bytes(b"\xef\xbb\xbf" + el.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
        check(edit_list_cuts(bom)[:3] == edit[:3], "带 BOM + CRLF 的剪辑单解析结果与原文件一致（回归：BOM 曾让首行表头丢失）")
        el.write_text("| CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字 |\n|---|---|---|---|---|---|\n"
                      "| CUT-001 | assets/a.mp4 | 0.00 | 1.50 | — | — |\n"
                      "| CUT-002 | assets/b.mp4 | 0.00 | 2.50 | — | — |\n", encoding="utf-8")
        fs, _ = scan_clip(clip, dict(opts, mode="final"), edit_list_cuts(el))
        check(any(f.code == "P8-cut-unexpected" and f.level == "warn" for f in fs),
              "剪辑单切点在 1.50s，而 3.00s 有跳变 → warn P8-cut-unexpected")

        # 3. 全静止 / 单帧 / 坏文件
        still = _synth(["-f", "lavfi", "-i", "color=c=0x334455:s=270x480:r=24:d=2"] + venc, td / "still.mp4")
        fs, rec = scan_clip(still, opts, None)
        check(len(rec["freezes"]) == 1 and rec["freezes"][0]["frames"] == 48 and not rec["events"],
              "纯色 2s：整段冻结 48 帧，无跳变，不崩溃")
        one = _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24", "-frames:v", "1"] + venc, td / "one.mp4")
        fs, _ = scan_clip(one, opts, None)
        check(any(f.code == "P8-too-short" for f in fs), "单帧 → warn P8-too-short")
        broken = td / "broken.mp4"
        broken.write_bytes(b"\x00" * 64)
        fs, _ = scan_clip(broken, opts, None)
        check(any(f.code == "P8-unreadable" and f.level == "error" for f in fs), "坏文件 → error P8-unreadable")

        # 4. CLI 契约
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + [str(clip), "--json"], capture_output=True, text=True)
        ok = False
        try:
            j = json.loads(r.stdout)
            ok = j["ok"] is True and len(j["clips"][0]["psnr"]) == 95 and j["counts"]["warn"] >= 2
        except Exception:
            pass
        check(r.returncode == 0 and ok, "CLI --json：退出码 0，含逐帧 psnr 序列与 warn")
        r = subprocess.run(me + [str(clip)], capture_output=True, text=True)
        check(r.returncode == 0 and "▕" in r.stdout and "^" in r.stdout, "CLI 人类报告含 ASCII 走势线")
        r = subprocess.run(me + [str(broken)], capture_output=True, text=True)
        check(r.returncode == 1, "CLI 坏文件 → 退出码 1")
        for fx in ("good", "bad"):
            r = subprocess.run(me + [str(ac.FIXTURES / fx)], capture_output=True, text=True)
            check(r.returncode == 0 and "P8-no-clips" in r.stdout, f"CLI fixtures/{fx}（无视频）→ 0 error")
        r = subprocess.run(me + [str(ac.FIXTURES / "good")], capture_output=True,
                           env=dict(os.environ, PYTHONIOENCODING="gbk"))
        check(r.returncode == 0 and b"Traceback" not in r.stderr,
              "stdout 为 GBK（Windows cmd 重定向，E3-1）→ 报告照出，不因 ⚠️ 等图标崩溃（回归）")
        r = subprocess.run(me + [str(clip), "--edit-list", str(el)], capture_output=True, text=True)
        check(r.returncode == 2, "CLI --edit-list 只能配 --mode final → 退出码 2")
        empty_el = td / "empty-edit-list.md"
        empty_el.write_text("# 剪辑单\n还没写表\n", encoding="utf-8")
        r = subprocess.run(me + [str(clip), "--mode", "final", "--edit-list", str(empty_el)], capture_output=True, text=True)
        check(r.returncode == 0 and "FMT-edit-list" in r.stdout and "P8-cut " in r.stdout
              and "P8-cut-unexpected" not in r.stdout, "剪辑单无有效行 → warn 并按无剪辑单报 P8-cut（不误报 unexpected）")
        r = subprocess.run(me + [str(td / "nope.mp4")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 路径不存在 → 退出码 2")

    failed = [lbl for ok, lbl in results if not ok]
    print(f"\nselftest {'PASS' if not failed else 'FAIL'}：{len(results) - len(failed)}/{len(results)} 通过")
    return 0 if not failed else 1


# ------------------------------------------------------------------ CLI


def _safe_stdio():
    """stdout 被重定向到 GBK/cp936 等非 UTF-8 编码时（Windows cmd 重定向，E3-1），报告里的 ❌⚠️👁 无法编码会让
    academy_common.emit 抛 UnicodeEncodeError；改为替换成 ?，报告与退出码照常。"""
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv: list[str] | None = None) -> int:
    _safe_stdio()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", help="视频文件或目录")
    ap.add_argument("--mode", choices=["clip", "final"], default="clip",
                    help="clip=单个生成镜（跳变→warn）；final=成片（跳变→info 切点）")
    ap.add_argument("--freeze-db", type=float, default=45.0, help="冻结阈值 dB（默认 45）")
    ap.add_argument("--freeze-min", type=int, default=12, help="冻结最少连续帧对数（默认 12 ≈ 0.5s@24fps）")
    ap.add_argument("--cut-db", type=float, default=18.0, help="绝对跳变阈值 dB（默认 18）")
    ap.add_argument("--z", type=float, default=3.0, help="稳健 z 分阈值（默认 3）")
    ap.add_argument("--min-drop", type=float, default=6.0, help="z 判据下还需低于中位数的最小 dB（默认 6）")
    ap.add_argument("--edit-list", help="（final）剪辑单 edit-list.md：与预期切点对齐")
    ap.add_argument("--cut-tol", type=float, help="（final）切点对齐容差秒（默认 max(0.1, 2 帧)）")
    ap.add_argument("--width", type=int, default=72, help="走势线宽度（默认 72）")
    ap.add_argument("--recursive", action="store_true", help="目录输入时递归查找视频")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON（含逐帧 psnr 序列）")
    ap.add_argument("--selftest", action="store_true", help="运行自测（ffmpeg lavfi 合成素材），全部通过退出 0")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.inputs:
        ap.print_usage(sys.stderr)
        ac.die("需要视频文件或目录（或 --selftest）")
    need_ffmpeg()
    if not ff_has_filter("psnr"):
        ac.die("ffmpeg 缺 psnr 滤镜：换用完整版 ffmpeg 后重跑")
    if a.freeze_min < 1 or a.width < 8 or a.z <= 0 or a.min_drop < 0:
        ac.die("--freeze-min ≥1，--width ≥8，--z >0，--min-drop ≥0")
    if a.edit_list and a.mode != "final":
        ac.die("--edit-list 只用于 --mode final（成片切点对齐）")
    edit = None
    findings: list[ac.Finding] = []
    if a.edit_list:
        if not Path(a.edit_list).is_file():
            ac.die(f"找不到剪辑单：{a.edit_list}")
        try:
            edit = edit_list_cuts(Path(a.edit_list))
        except UnicodeDecodeError:
            ac.die(f"{a.edit_list} 不是 UTF-8 编码（format-contracts §0.1）")
        findings += edit[3]
        if not edit[2]:                            # 没有任何有效行：对齐无意义，按无剪辑单处理
            findings.append(ac.Finding("warn", "FMT-edit-list",
                                       "剪辑单没有任何有效 CUT 行：本次不做切点对齐，跳变按普通切点（P8-cut）报告——"
                                       "修好剪辑单后带 --edit-list 重跑", a.edit_list))
            edit = None
    clips, fs = collect_clips(a.inputs, a.recursive)
    findings += fs
    opts = dict(mode=a.mode, freeze_db=a.freeze_db, freeze_min=a.freeze_min, cut_db=a.cut_db, z_thr=a.z,
                min_drop=a.min_drop, cut_tol=a.cut_tol, width=a.width)
    records = []
    for c in clips:
        f2, rec = scan_clip(c, opts, edit)
        findings += f2
        records.append(rec)
    return ac.emit(TITLE, findings, a.json, {"clips": records, "summary": summary_text(records)})


if __name__ == "__main__":
    sys.exit(main())
