#!/usr/bin/env python3
"""burnin_text_scan.py — 烧录字幕 / 文字水印扫描（OCR 优先，无 OCR 时降级为启发式 + 目视）

用途：
  每 --interval 秒（默认 0.5s）抽一帧，查生成器自行烧进画面的字幕/文字/水印。
  ① 有 OCR 后端（按序尝试 rapidocr_onnxruntime → paddleocr → easyocr → pytesseract+tesseract）时：
     逐帧 OCR，报告 文字 + 置信度 + bbox + 出现时间；置信 ≥ 0.5 且 ≥ 2 个有效字符 → error，其余 → visual；
     已知水印词（默认 LAVCE，D2 实证；--watermark-token 可追加）单独标 D2-watermark。
  ② 无 OCR 后端：明确报告"未检测到 OCR 后端，降级为启发式 + 目视"，改算"文字可能性"启发式——
     ffmpeg 输出灰度 raw 帧（宽 270），统计底部 30% 区域内"强水平相邻像素跳变"的峰值条带密度，
     与本片自身基线（时间对比）和同帧上部区域（空间对比）比较，任一成立 → visual「疑似字幕/文字：抽帧目视确认」：
       时间：底部得分 > max(基线×2.5, 绝对下限 0.08)；基线取本片底部得分的下四分位（P25）而不是中位数——
             实测文字占一半抽样时中位数被文字抬高、阈值越过文字本身，整段漏报；P25 对文字占比 <75% 稳健；
       空间：底部得分 ≥ 2×下限 且 ≥ 同帧上部得分 2 倍（文字笔画集中在底部条带）。
     基线本身 ≥ 下限且 ≥ 上部中位 2 倍 → visual「整段底部持续高文字密度」（全程字幕时时间对比失效）。
     近纯色帧（≥90% 行没有任何强跳变，如纯黑/纯白字卡）上只要出现峰值 ≥0.01 的笔画 → visual「近纯色画面上出现
     文字样笔画」——这正是 D2 现场（纯黑字卡中段被加 LAVCE）：小号水印在 270 宽灰度帧里只有 0.02–0.05，
     远低于 0.08 下限，按通用阈值会整段漏报（实测居中 28px / 角落 40px@1080p 两种都漏）。
     启发式**永远不单独判 error**（D5：工具会骗人，单通道不判决）。
  两种模式都写出一张"底部条带接触图"（被标记的格红框）供 agent 目视；上部/近纯色帧有标记时另写一张
  "整帧接触图"（只含被标记的抽样，水印多在画面中部/角落，底部条带里看不到）。
  --mode final：成片里的硬字幕/叠层字卡是设计内容，OCR 文字降为 visual（与剪辑单 字幕/画面文字 核对），水印仍 error。

溯源：D1（烧录字幕：生成器自行加字 → 视频验收固定"抽帧核验无烧录文字"）、
      D2（纯黑字卡交给 H3 → 中段帧被加 "LAVCE" 文字水印）、P8（视频验收：逐段抽帧核验无烧录文字）、
      D5（QC 工具会骗你：单通道不判决，启发式只出目视证据）。

输入格式：视频文件（.mp4 .mov .mkv .webm .m4v .avi）或含视频的目录。
  禁令句与"画面文字交给剪辑叠层"的契约见 70-playbooks/format-contracts.md §2 规则 5（D1）与 §4 剪辑单 `画面文字` 列。

输出（默认写在视频旁，--out-dir 可改）：<stem>.burnin-strip.jpg（底部 30% 条带接触图，4 列，标记格红框，格内烧录时间）；
  有上部/近纯色标记时另有 <stem>.burnin-frames.jpg（被标记抽样的整帧）。单图一律 -update 1 写出（文件名含 % 不出错）。

判定：
  error  D1-burnin-text          OCR 置信 ≥ 0.5 且 ≥ 2 字符（clip 模式）
  error  D2-watermark            OCR 文本含已知水印词（LAVCE 等），置信 ≥ 0.5
  visual D2-watermark-lowconf    OCR 文本含已知水印词但置信 < 0.5
  visual D1-ocr-lowconf          OCR 低置信或不足 2 字符
  visual D1-text-final           （final 模式）OCR 检出文字：与剪辑单 字幕/画面文字 逐字核对
  visual D1-heuristic-bottom     启发式：底部疑似字幕/文字
  visual D2-heuristic-upper      启发式：上部区域文字密度突增（疑似水印/文字）
  visual D1-heuristic-persistent 启发式：整段底部持续高文字密度（可能全程字幕，时间对比失效）
  visual D2-heuristic-flat       启发式：近纯色画面上出现文字样笔画（D2 纯色卡水印）
  warn   D1-strip-failed         条带/整帧接触图写不出（输出目录不可写、缺滤镜）——证据缺失，需另行抽帧
  warn   D1-ocr-degraded         未检测到/无法使用 OCR 后端，已降级（每次运行报告一次）
  info   D1-scan-stats           抽样数、两区中位得分、阈值
  warn   P8-no-clips             目录中没有视频文件
  error  P8-unreadable           视频无法探测/解码

用法示例：
  python3 burnin_text_scan.py season-01/ep03/assets/clips/SHOT-004.mp4
  python3 burnin_text_scan.py season-01/ep03/assets/clips/ --out-dir qc/burnin --json
  python3 burnin_text_scan.py final/ep03.mp4 --mode final --interval 1.0
  python3 burnin_text_scan.py SHOT-005.mp4 --watermark-token LAVCE --watermark-token SORA
  python3 burnin_text_scan.py SHOT-004.mp4 --ocr none          # 强制启发式（对照/省时）
  python3 burnin_text_scan.py --selftest

退出码：0 通过（无 error）/ 1 发现 error（OCR 高置信文字或水印、坏文件）/ 2 用法或环境错误。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "烧录字幕 / 文字水印扫描（D1 / D2）"
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
DEFAULT_WATERMARKS = ["LAVCE"]          # D2 实证
OCR_ORDER = ["rapidocr", "paddleocr", "easyocr", "tesseract"]
HEUR_W = 270                            # 启发式灰度帧宽度
BOTTOM = 0.30                           # 底部条带比例
EDGE_THR = 40                           # 强跳变：相邻像素灰度差 ≥ 40/255
FLOOR = 0.08                            # 绝对下限（峰值条带中强跳变像素占比）
RATIO = 2.5                             # 相对本片中位数的倍数
CONF_ERR = 0.5
STRIP_MAX = 48
FLAT_ROWS = 0.90                        # ≥90% 行没有强跳变 → 近纯色帧（纯黑/纯白/纯色卡，D2）
FLAT_TEXT = 0.01                        # 近纯色帧上峰值条带密度 ≥ 0.01 → 文字样笔画（D2 LAVCE 实测 0.02–0.05）


# ------------------------------------------------------------------ ffmpeg 小工具

_FILTERS: set | None = None


def ff_filters() -> set:
    global _FILTERS
    if _FILTERS is None:
        _FILTERS = set()
        try:
            p = ac.run(["ffmpeg", "-hide_banner", "-filters"], timeout=60)
            for ln in p.stdout.splitlines():
                m = re.match(r"^\s*[A-Z.|]{2,3}\s+(\w+)\s+\S*->\S*", ln)
                if m:
                    _FILTERS.add(m.group(1))
        except Exception:
            pass
    return _FILTERS


REQUIRED_FILTERS = ("fps", "scale", "format")    # 抽灰度帧必需；crop/tile/select/drawbox/drawtext 缺失只影响接触图（降级）


def need_ffmpeg():
    missing = [t for t in ("ffmpeg", "ffprobe") if not ac.have(t)]
    if missing:
        ac.die(f"找不到 {' / '.join(missing)}：安装 ffmpeg（含 ffprobe）并加入 PATH 后重跑")
    flt = ff_filters()
    lack = [f for f in REQUIRED_FILTERS if flt and f not in flt]
    if lack:
        ac.die(f"ffmpeg 缺少必需滤镜 {' / '.join(lack)}：换用完整版 ffmpeg 后重跑")


def probe(path: Path) -> dict:
    info = ac.ffprobe_json(path)
    vs = [s for s in info.get("streams", []) if s.get("codec_type") == "video"
          and not s.get("disposition", {}).get("attached_pic")]
    if not vs:
        raise RuntimeError("文件中没有视频流")
    v = vs[0]
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    rot = v.get("tags", {}).get("rotate")
    for sd in v.get("side_data_list", []) or []:
        rot = sd.get("rotation", rot)
    try:
        if rot is not None and int(round(float(rot))) % 180 == 90:
            w, h = h, w
    except (TypeError, ValueError):
        pass
    if w <= 0 or h <= 0:
        raise RuntimeError("无法读取画面尺寸")
    dur = float(v.get("duration") or info.get("format", {}).get("duration") or 0.0)
    return {"width": w, "height": h, "duration": round(dur, 3)}


def rate_str(interval: float) -> str:
    """fps 滤镜速率。配合 round=up：第 k 个抽样 = 时刻 k×interval 处（或其前最近）的那一帧；
    默认 round=near 会取到 k×interval 之后近半个间隔的帧，报告的时间戳就错了（实测）。"""
    fr = Fraction(1 / interval).limit_denominator(1000)
    return f"{fr.numerator}/{fr.denominator}"


# ------------------------------------------------------------------ OCR 后端（有则用，无则降级）

def _poly_bbox(box) -> list[int]:
    try:
        pts = [(float(p[0]), float(p[1])) for p in box]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return [int(min(xs)), int(min(ys)), int(max(xs) - min(xs)), int(max(ys) - min(ys))]
    except Exception:  # noqa: BLE001
        try:
            x0, y0, x1, y1 = (float(v) for v in box)
            return [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]
        except Exception:  # noqa: BLE001
            return [0, 0, 0, 0]


def _load_rapidocr():
    from rapidocr_onnxruntime import RapidOCR  # type: ignore
    eng = RapidOCR()

    def fn(path: Path) -> list[dict]:
        res, _ = eng(str(path))
        return [{"text": str(t), "conf": float(s), "bbox": _poly_bbox(b)} for b, t, s in (res or [])]
    return fn


def _load_paddleocr():
    from paddleocr import PaddleOCR  # type: ignore
    try:
        eng = PaddleOCR(use_angle_cls=False, lang="ch", show_log=False)
    except (TypeError, ValueError):
        eng = PaddleOCR(lang="ch")

    def fn(path: Path) -> list[dict]:
        res = eng.ocr(str(path))
        out = []
        for page in res or []:
            if isinstance(page, dict):          # paddleocr 3.x
                texts, scores = page.get("rec_texts", []), page.get("rec_scores", [])
                polys = page.get("rec_polys") or page.get("rec_boxes") or []
                for k, t in enumerate(texts):
                    out.append({"text": str(t), "conf": float(scores[k]) if k < len(scores) else 0.0,
                                "bbox": _poly_bbox(polys[k]) if k < len(polys) else [0, 0, 0, 0]})
            else:                               # paddleocr 2.x
                for item in page or []:
                    box, (t, s) = item[0], item[1]
                    out.append({"text": str(t), "conf": float(s), "bbox": _poly_bbox(box)})
        return out
    return fn


def _load_easyocr():
    import easyocr  # type: ignore
    reader = easyocr.Reader(["ch_sim", "en"], gpu=False, verbose=False)

    def fn(path: Path) -> list[dict]:
        return [{"text": str(t), "conf": float(c), "bbox": _poly_bbox(b)} for b, t, c in reader.readtext(str(path))]
    return fn


def _load_tesseract():
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
    if not shutil.which("tesseract"):
        raise RuntimeError("找不到 tesseract 可执行文件")
    try:
        langs = set(pytesseract.get_languages(config=""))
    except Exception:  # noqa: BLE001
        langs = {"eng"}
    lang = "+".join(x for x in ("chi_sim", "eng") if x in langs) or None

    def fn(path: Path) -> list[dict]:
        d = pytesseract.image_to_data(Image.open(path), lang=lang, output_type=pytesseract.Output.DICT)
        lines: dict = {}
        for k, t in enumerate(d.get("text", [])):
            try:
                conf = float(d["conf"][k])
            except (TypeError, ValueError):
                conf = -1
            if not str(t).strip() or conf < 0:
                continue
            key = (d["block_num"][k], d["par_num"][k], d["line_num"][k])
            ln = lines.setdefault(key, {"words": [], "confs": [], "x0": 1e9, "y0": 1e9, "x1": 0, "y1": 0})
            ln["words"].append(str(t))
            ln["confs"].append(conf / 100)
            x, y, w, h = d["left"][k], d["top"][k], d["width"][k], d["height"][k]
            ln["x0"], ln["y0"] = min(ln["x0"], x), min(ln["y0"], y)
            ln["x1"], ln["y1"] = max(ln["x1"], x + w), max(ln["y1"], y + h)
        return [{"text": " ".join(v["words"]), "conf": sum(v["confs"]) / len(v["confs"]),
                 "bbox": [int(v["x0"]), int(v["y0"]), int(v["x1"] - v["x0"]), int(v["y1"] - v["y0"])]}
                for v in lines.values()]
    return fn


LOADERS = {"rapidocr": _load_rapidocr, "paddleocr": _load_paddleocr, "easyocr": _load_easyocr,
           "tesseract": _load_tesseract}


def load_ocr(choice: str = "auto") -> tuple[tuple[str, object] | None, list[str]]:
    """返回 ((后端名, fn) 或 None, 尝试记录)。任何导入/初始化异常都只记录，不抛出。"""
    if choice == "none":
        return None, ["--ocr none：按要求不使用 OCR"]
    order = OCR_ORDER if choice == "auto" else [choice]
    notes = []
    for name in order:
        try:
            return (name, LOADERS[name]()), notes
        except Exception as e:  # noqa: BLE001  (ImportError、模型下载失败、二进制缺失……)
            notes.append(f"{name}: {type(e).__name__}: {str(e)[:80]}")
    return None, notes


# ------------------------------------------------------------------ 启发式（纯标准库）

def gray_frames(clip: Path, interval: float, w: int, h: int) -> tuple[list[bytes], int, int]:
    W = HEUR_W
    H = max(8, 2 * int(round(W * h / w / 2)))
    p = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(clip), "-map", "0:v:0", "-vf",
                        f"fps=fps={rate_str(interval)}:round=up,scale={W}:{H},format=gray",
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, timeout=1800)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace").strip()[-300:] or "ffmpeg 抽灰度帧失败")
    size = W * H
    return [p.stdout[i * size:(i + 1) * size] for i in range(len(p.stdout) // size)], W, H


def _row_counts(buf: bytes, W: int, y0: int, y1: int) -> list[int]:
    out = []
    for y in range(y0, y1):
        r = buf[y * W:(y + 1) * W]
        out.append(sum(1 for a, b in zip(r, r[1:]) if a - b >= EDGE_THR or b - a >= EDGE_THR))
    return out


def _peak(rc: list[int], W: int, win: int) -> float:
    if not rc:
        return 0.0
    win = max(1, min(win, len(rc)))
    s = best = sum(rc[:win])
    for i in range(win, len(rc)):
        s += rc[i] - rc[i - win]
        best = max(best, s)
    return best / (win * (W - 1))


def frame_scores(buf: bytes, W: int, H: int) -> tuple[float, float, float]:
    """(底部 30% 峰值条带强跳变密度, 上部 70% 同口径密度, 无强跳变行占比)。条带高 ≈ 3.5% 画高 ≈ 一行字幕。"""
    y0 = int(H * (1 - BOTTOM))
    win = max(4, int(round(H * 0.035)))
    rc = _row_counts(buf, W, 0, H)
    flat = sum(1 for c in rc if c == 0) / len(rc) if rc else 0.0
    return _peak(rc[y0:], W, win), _peak(rc[:y0], W, win), flat


def _quantile(vals: list[float], q: float) -> float:
    s = sorted(vals)
    if not s:
        return 0.0
    pos = q * (len(s) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def heuristic_flags(scores: list[tuple], floor: float = FLOOR, ratio: float = RATIO) -> dict:
    """时间对比（基线 = P25×ratio，下限 floor）+ 空间对比（底部 ≥ 2×floor 且 ≥ 同帧上部 2 倍）
    + 近纯色帧规则（≥FLAT_ROWS 行无强跳变、却有 ≥FLAT_TEXT 的笔画条带，D2）。scores 元素为 (底, 上[, 平坦行占比])。"""
    if not scores:
        return {"med_bottom": 0, "med_upper": 0, "base_bottom": 0, "base_upper": 0, "thr_bottom": floor,
                "thr_upper": floor, "bottom": [], "upper": [], "flat": [], "flat_frames": 0, "persistent": False}
    b, u = [s[0] for s in scores], [s[1] for s in scores]
    fl = [s[2] if len(s) > 2 else 0.0 for s in scores]
    mb, mu = statistics.median(b), statistics.median(u)
    bb, bu = _quantile(b, 0.25), _quantile(u, 0.25)
    tb, tu = max(bb * ratio, floor), max(bu * ratio, floor)
    bottom = [i for i, s in enumerate(scores) if s[0] > tb or (s[0] >= 2 * floor and s[0] >= 2 * s[1])]
    upper = [i for i, s in enumerate(scores) if s[1] > tu]
    taken = set(bottom) | set(upper)
    flat = [i for i, s in enumerate(scores)
            if fl[i] >= FLAT_ROWS and max(s[0], s[1]) >= FLAT_TEXT and i not in taken]
    return {"med_bottom": round(mb, 4), "med_upper": round(mu, 4), "base_bottom": round(bb, 4),
            "base_upper": round(bu, 4), "thr_bottom": round(tb, 4), "thr_upper": round(tu, 4),
            "bottom": bottom, "upper": upper, "flat": flat, "flat_frames": sum(1 for x in fl if x >= FLAT_ROWS),
            "persistent": bb >= floor and bb >= 2 * mu}


def _ranges(idx: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for i in idx:
        if out and i - out[-1][-1] <= 1:
            out[-1].append(i)
        else:
            out.append([i])
    return out


# ------------------------------------------------------------------ OCR 结果 → 发现项

def _norm(s: str) -> str:
    return re.sub(r"[\W_]+", "", s or "")


def ocr_findings(hits: list[dict], where: str, mode: str, watermarks: list[str], strip_name: str) -> list[ac.Finding]:
    """hits: [{t, text, conf, bbox}] → 按 (规则, 文本) 合并成发现项。"""
    groups: dict = {}
    for h in hits:
        norm = _norm(h["text"])
        if not norm:
            continue
        tok = next((w for w in watermarks if _norm(w).upper() and _norm(w).upper() in norm.upper()), None)
        conf = float(h["conf"])
        if tok:
            code, level = ("D2-watermark", "error") if conf >= CONF_ERR else ("D2-watermark-lowconf", "visual")
        elif conf >= CONF_ERR and len(norm) >= 2:
            code, level = ("D1-burnin-text", "error") if mode == "clip" else ("D1-text-final", "visual")
        else:
            code, level = "D1-ocr-lowconf", "visual"
        g = groups.setdefault((code, norm), {"level": level, "times": [], "best": h, "token": tok})
        g["times"].append(h["t"])
        if conf > float(g["best"]["conf"]):
            g["best"] = h
    fs = []
    for (code, norm), g in groups.items():
        b = g["best"]
        ts = sorted(set(g["times"]))
        tt = "、".join(f"{t:.2f}s" for t in ts[:8]) + ("…" if len(ts) > 8 else "")
        box = ",".join(map(str, b.get("bbox", [])))
        head = f"「{b['text']}」（置信 {float(b['conf']):.2f}，bbox {box}，出现于 {tt}）"
        if code == "D2-watermark":
            msg = (f"检出已知水印 {g['token']}：{head}——D2 实证：纯色/空画面交给 H3 会被加水印；纯色卡改本地生成"
                   f"（剪辑单来源写 local:black），其余镜换 seed 重出；先在 {strip_name} 目视确认（D5）")
        elif code == "D2-watermark-lowconf":
            msg = f"疑似已知水印 {g['token']}（低置信）：{head}——需目视：打开 {strip_name} 与该时刻原帧确认"
        elif code == "D1-burnin-text":
            msg = (f"检出烧录文字 {head}：该镜重出——确认 video-prompts.md 该镜 h3 代码块末行为禁令句"
                   f"（D1/M8），画面文字一律交剪辑叠层；重出前先在 {strip_name} 目视确认（D5 双通道）")
        elif code == "D1-text-final":
            msg = (f"成片检出文字 {head}：若为剪辑叠加的硬字幕/字卡（设计内容），与剪辑单 字幕/画面文字 列逐字核对（P7）；"
                   f"不在剪辑单里的文字 → 回查来源镜并重出")
        else:
            msg = f"OCR 低置信或过短文字 {head}：需目视确认是否为画面文字（{strip_name} 对应格 + 原帧）"
        fs.append(ac.Finding(g["level"], code, msg, f"{where} @ {ts[0]:.2f}s",
                             {"text": b["text"], "conf": round(float(b["conf"]), 3), "bbox": b.get("bbox"), "times": ts}))
    return fs


# ------------------------------------------------------------------ 条带接触图

def write_strip(clip: Path, out: Path, interval: float, n_samples: int, flagged: list[int], cols: int = 4,
                use_text: bool = True, only: list[int] | None = None) -> dict:
    """底部 30% 条带接触图；only=被标记抽样序号 → 改出这些抽样的整帧接触图（水印多在中部/角落）。"""
    keep = list(range(n_samples))
    note = "全部抽样帧"
    if only is not None:
        keep = sorted(set(i for i in only if 0 <= i < n_samples))[:STRIP_MAX]
        note = "仅被标记抽样（整帧）"
    elif n_samples > STRIP_MAX:
        near = sorted({j for i in flagged for j in (i - 1, i, i + 1) if 0 <= j < n_samples})
        if near:
            keep, note = near[:STRIP_MAX], "仅标记帧及其前后相邻帧"
        else:
            step = math.ceil(n_samples / STRIP_MAX)
            keep, note = list(range(0, n_samples, step)), f"每 {step} 个抽样取 1 个"
    if len(keep) < n_samples and len(keep) == STRIP_MAX and flagged:
        note += f"（截断为 {STRIP_MAX} 格）"
    cols = max(1, min(cols, len(keep)))
    rows = math.ceil(len(keep) / cols)
    vf = [f"fps=fps={rate_str(interval)}:round=up"]
    if len(keep) < n_samples:
        vf.append("select='" + "+".join(f"eq(n\\,{i})" for i in keep) + "'")
    vf += (["scale=360:-2"] if only is not None
           else ["crop=iw:trunc(ih*0.3/2)*2:0:ih-trunc(ih*0.3/2)*2", "scale=360:-2"])
    fl = [i for i in flagged if i in set(keep)][:200]
    box = []
    if fl:
        en = "+".join(f"between(t\\,{i * interval - 0.01:.3f}\\,{i * interval + 0.01:.3f})" for i in fl)
        box = [f"drawbox=x=0:y=0:w=iw:h=ih:color=red:t=6:enable='{en}'"]
    txt = (["drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=3"]
           if use_text and "drawtext" in ff_filters() else [])
    tile = [f"tile={cols}x{rows}:padding=4:margin=4:color=0x202020"]
    attempts, seen = [], set()
    for chain, t_ok, b_ok in ((vf + box + txt + tile, bool(txt), True), (vf + box + tile, False, True),
                              (vf + txt + tile, bool(txt), not box), (vf + tile, False, not box)):
        if tuple(chain) not in seen:                 # drawtext / drawbox 缺失或失败逐级降级
            seen.add(tuple(chain))
            attempts.append((chain, t_ok, b_ok))
    for chain, t_ok, b_ok in attempts:
        p = ac.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(clip), "-map", "0:v:0",
                    "-vf", ",".join(chain), "-frames:v", "1", "-update", "1", "-q:v", "3", str(out)])
        if p.returncode == 0 and out.exists():
            return {"path": str(out), "samples": [round(i * interval, 3) for i in keep], "cols": cols,
                    "labels_burned": t_ok, "marks_drawn": b_ok, "note": note}
    raise RuntimeError(f"接触图生成失败：{p.stderr.strip()[-200:]}")


# ------------------------------------------------------------------ 主流程（单镜）

def extract_samples(clip: Path, interval: float, td: Path, max_w: int = 1080) -> list[Path]:
    p = ac.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(clip), "-map", "0:v:0", "-vf",
                f"fps=fps={rate_str(interval)}:round=up,scale='min({max_w},iw)':-2", "-start_number", "0",
                str(td / "s_%05d.png")])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[-300:])
    return sorted(td.glob("s_*.png"))


def scan_clip(clip: Path, out_dir: Path | None, interval: float = 0.5, mode: str = "clip",
              ocr: tuple[str, object] | None = None, watermarks: list[str] | None = None, floor: float = FLOOR,
              ratio: float = RATIO, use_text: bool = True) -> tuple[list[ac.Finding], dict]:
    where = clip.name
    watermarks = DEFAULT_WATERMARKS if watermarks is None else watermarks
    try:
        pr = probe(clip)
        frames, W, H = gray_frames(clip, interval, pr["width"], pr["height"])
        if not frames:
            raise RuntimeError("抽样得到 0 帧")
    except Exception as e:  # noqa: BLE001
        return [ac.Finding("error", "P8-unreadable", f"无法探测/解码：{str(e)[:200]}——重新导出或重新下载后再验收",
                           where)], {"clip": str(clip)}
    fs: list[ac.Finding] = []
    scores = [frame_scores(f, W, H) for f in frames]
    hf = heuristic_flags(scores, floor, ratio)
    out_dir = Path(out_dir) if out_dir else clip.parent
    strip_path = out_dir / f"{clip.stem}.burnin-strip.jpg"
    frames_path = out_dir / f"{clip.stem}.burnin-frames.jpg"

    hits: list[dict] = []
    ocr_err = None
    if ocr is not None:
        name, fn = ocr
        with tempfile.TemporaryDirectory(prefix="burnin_") as tds:
            try:
                for k, sp in enumerate(extract_samples(clip, interval, Path(tds))):
                    for it in fn(sp) or []:
                        hits.append(dict(it, t=round(k * interval, 3)))
            except Exception as e:  # noqa: BLE001
                ocr_err = f"{name} 运行失败：{type(e).__name__}: {str(e)[:120]}"
    ocr_times = {h["t"] for h in hits}
    flagged = sorted(set(hf["bottom"]) | set(hf["upper"]) | set(hf["flat"])
                     | {int(round(t / interval)) for t in ocr_times})
    whole = sorted(set(hf["upper"]) | set(hf["flat"]))          # 水印多在中部/角落：另出整帧图
    strip, fsheet = {"path": None}, {"path": None}
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        strip = write_strip(clip, strip_path, interval, len(frames), flagged, use_text=use_text)
        if whole:
            fsheet = write_strip(clip, frames_path, interval, len(frames), whole, use_text=use_text, only=whole)
    except Exception as e:  # noqa: BLE001
        fs.append(ac.Finding("warn", "D1-strip-failed",
                             f"接触图写不出（{str(e)[:160]}）：检查 {out_dir} 可写与磁盘空间；证据缺失时用 contact_sheet.py "
                             f"另行抽帧目视，不得据此判「无字幕」", where))
        strip = strip if strip.get("path") else {"path": None, "error": str(e)[:200]}
    sname = strip_path.name if strip.get("path") else "（条带图生成失败，用 contact_sheet.py 抽帧）"
    fname = (frames_path.name if fsheet.get("path")
             else "contact_sheet.py 对该时段抽帧（整帧图未生成）")

    fs.append(ac.Finding("info", "D1-scan-stats",
                         f"{len(frames)} 个抽样（每 {interval:g}s）；启发式底部 中位 {hf['med_bottom']:.3f} / 基线 "
                         f"{hf['base_bottom']:.3f} / 阈值 {hf['thr_bottom']:.3f}，上部 中位 {hf['med_upper']:.3f} / 阈值 "
                         f"{hf['thr_upper']:.3f}"
                         + (f"；OCR={ocr[0]} 检出 {len(hits)} 条" if ocr and not ocr_err else ""), where))
    if ocr_err:
        fs.append(ac.Finding("warn", "D1-ocr-degraded", f"{ocr_err}——本镜降级为启发式 + 目视", where))
    fs += ocr_findings(hits, where, mode, watermarks, sname)

    final_tip = "；成片中若为设计硬字幕/字卡则忽略（与剪辑单核对）" if mode == "final" else ""
    for g in _ranges([i for i in hf["bottom"] if round(i * interval, 3) not in ocr_times]):
        a, b = g[0] * interval, g[-1] * interval
        best = max(g, key=lambda i: scores[i][0])
        fs.append(ac.Finding("visual", "D1-heuristic-bottom",
                             f"疑似字幕/文字：抽帧目视确认 {a:.2f}–{b:.2f}s（底部 30% 文字密度峰值 {scores[best][0]:.3f}，"
                             f"本片基线 {hf['base_bottom']:.3f}，阈值 {hf['thr_bottom']:.3f}，同帧上部 {scores[best][1]:.3f}）"
                             f"——打开 {sname} 红框格；确为烧录字幕 → 该镜重出（D1 禁令句须在 h3 末行）{final_tip}",
                             f"{where} @ {a:.2f}s", {"times": [round(i * interval, 3) for i in g],
                                                     "scores": [round(scores[i][0], 4) for i in g]}))
    for g in _ranges([i for i in hf["upper"] if round(i * interval, 3) not in ocr_times]):
        a, b = g[0] * interval, g[-1] * interval
        best = max(g, key=lambda i: scores[i][1])
        fs.append(ac.Finding("visual", "D2-heuristic-upper",
                             f"上部区域文字密度突增 {a:.2f}–{b:.2f}s（峰值 {scores[best][1]:.3f}，本片基线 {hf['base_upper']:.3f}）："
                             f"疑似水印/文字，也可能是换景或高纹理——打开 {fname} 红框格整帧目视（D2：LAVCE 水印出现在中段帧）",
                             f"{where} @ {a:.2f}s", {"times": [round(i * interval, 3) for i in g]}))
    for g in _ranges([i for i in hf["flat"] if round(i * interval, 3) not in ocr_times]):
        a, b = g[0] * interval, g[-1] * interval
        best = max(g, key=lambda i: max(scores[i][0], scores[i][1]))
        fs.append(ac.Finding("visual", "D2-heuristic-flat",
                             f"近纯色画面上出现文字样笔画 {a:.2f}–{b:.2f}s（≥{FLAT_ROWS:.0%} 行无强边缘，笔画峰值 "
                             f"{max(scores[best][0], scores[best][1]):.3f}）：疑似生成器自加水印/文字（D2 实证：纯黑字卡中段帧被加"
                             f" LAVCE）——打开 {fname} 红框格目视；确为水印 → 纯色卡改本地生成（剪辑单来源写 local:black / "
                             f"local:#RRGGBB），不送生成器{final_tip}", f"{where} @ {a:.2f}s",
                             {"times": [round(i * interval, 3) for i in g],
                              "scores": [round(max(scores[i][0], scores[i][1]), 4) for i in g]}))
    if hf["persistent"] and not hits:
        fs.append(ac.Finding("visual", "D1-heuristic-persistent",
                             f"整段底部持续高文字密度（基线 {hf['base_bottom']:.3f} ≥ 下限 {floor:g} 且 ≥ 上部中位 2 倍）："
                             f"可能是全程字幕（时间对比法失效）或底部高纹理——打开 {sname} 目视确认{final_tip}", where))
    rec = {"clip": str(clip), "interval": interval, "samples": len(frames),
           "scores": [[round(s[0], 4), round(s[1], 4)] for s in scores],
           "flat_rows": [round(s[2], 3) for s in scores], "heuristic": hf,
           "ocr_backend": ocr[0] if ocr and not ocr_err else None, "ocr_hits": hits, "strip": strip,
           "frames_sheet": fsheet}
    return fs, rec


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


# ------------------------------------------------------------------ 自测

def _synth(args: list[str], out: Path) -> Path:
    p = ac.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + args + [str(out)])
    if p.returncode != 0:
        raise RuntimeError(f"合成失败：{p.stderr.strip()[-300:]}")
    return out


def _venc() -> list[str]:
    p = ac.run(["ffmpeg", "-hide_banner", "-encoders"])
    if "libx264" in p.stdout:
        return ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18"]
    return ["-c:v", "mpeg4", "-q:v", "2", "-pix_fmt", "yuv420p"]


def _text_layer(enable: str, use_drawtext: bool) -> str:
    """底部字幕样内容：有 drawtext 用真字，否则用一排细竖条 + 横条模拟笔画。"""
    if use_drawtext:
        return (f"drawtext=text='SUBTITLE TEST 2026 OK':fontsize=26:fontcolor=white:borderw=2:bordercolor=black"
                f":x=(w-tw)/2:y=h*0.84:enable='{enable}'")
    bars = [f"drawbox=x={30 + i * 13}:y=ih*0.84:w=3:h=18:color=white:t=fill:enable='{enable}'" for i in range(22)]
    bars += [f"drawbox=x={30 + i * 26}:y=ih*0.84+8:w=9:h=2:color=white:t=fill:enable='{enable}'" for i in range(11)]
    return ",".join(bars)


def selftest() -> int:
    need_ffmpeg()
    results: list[tuple[bool, str]] = []

    def check(cond, label):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    # 1. OCR 结果 → 发现项（纯逻辑，用假 OCR 输出）
    hits = [{"t": 1.0, "text": "就是现在！", "conf": 0.91, "bbox": [40, 520, 200, 30]},
            {"t": 1.5, "text": "就是现在", "conf": 0.88, "bbox": [40, 520, 200, 30]},
            {"t": 1.5, "text": "A", "conf": 0.95, "bbox": [1, 1, 5, 5]},
            {"t": 2.0, "text": "字幕", "conf": 0.30, "bbox": [0, 0, 9, 9]},
            {"t": 2.5, "text": "lavce", "conf": 0.80, "bbox": [100, 300, 80, 20]},
            {"t": 3.0, "text": "LAVCE.", "conf": 0.35, "bbox": [100, 300, 80, 20]}]
    fs = ocr_findings(hits, "X.mp4", "clip", DEFAULT_WATERMARKS, "X.burnin-strip.jpg")
    codes = {(f.code, f.level) for f in fs}
    check(("D1-burnin-text", "error") in codes and sum(f.code == "D1-burnin-text" for f in fs) == 1,
          "OCR「就是现在」置信 0.91（两次出现合并为一条）→ error D1-burnin-text")
    check(("D1-ocr-lowconf", "visual") in codes and not any(f.level == "error" and "「A」" in f.msg for f in fs),
          "单字符 / 低置信文字 → visual，不判 error")
    check(("D2-watermark", "error") in codes and ("D2-watermark-lowconf", "visual") in codes,
          "已知水印 LAVCE（大小写/标点不敏感）：置信 0.80 → error D2-watermark；0.35 → visual")
    fs = ocr_findings(hits, "X.mp4", "final", DEFAULT_WATERMARKS, "X.burnin-strip.jpg")
    check(any(f.code == "D1-text-final" and f.level == "visual" for f in fs)
          and any(f.code == "D2-watermark" and f.level == "error" for f in fs)
          and not any(f.code == "D1-burnin-text" for f in fs), "final 模式：普通文字降为 visual，水印仍 error")
    half = [(0.0, 0.08)] * 3 + [(0.22, 0.08)] * 3
    hf = heuristic_flags(half)
    check(hf["bottom"] == [3, 4, 5] and statistics.median(s[0] for s in half) * RATIO > 0.22,
          "文字占一半抽样：中位数×2.5 会越过文字得分（整段漏报），P25 基线仍标出 3 帧")
    hf = heuristic_flags([(0.17, 0.30)] * 8)
    check(hf["bottom"] == [] and not hf["persistent"], "整段均匀纹理（底 0.17 / 上 0.30，如草地+树冠）→ 不标记")
    hf = heuristic_flags([(0.03, 0.30)] * 6 + [(0.17, 0.30)] * 2)
    check(hf["bottom"] == [6, 7], "底部得分从 0.03 突增到 0.17（> 基线×2.5 与下限）→ 时间对比标出")
    check(load_ocr("none")[0] is None, "--ocr none → 不加载后端（降级路径）")
    be, notes = load_ocr("auto")
    print(f"      （本机 OCR 后端：{be[0] if be else '无'}；尝试记录：{'; '.join(notes) or '—'}）")

    # 2. 启发式（合成：只有 1–2s 底部有字幕样内容）
    venc = _venc()
    has_dt = "drawtext" in ff_filters()
    base = ["-f", "lavfi", "-i", "color=c=0x2a4058:s=360x640:r=24:d=3", "-f", "lavfi", "-i",
            "testsrc2=s=200x200:r=24:d=3"]
    with tempfile.TemporaryDirectory(prefix="burnin_selftest_") as tds:
        td = Path(tds)
        variants = [("bars", False)] + ([("drawtext", True)] if has_dt else [])
        clip = None
        for tag, use_dt in variants:
            clip = _synth(base + ["-filter_complex", "[0:v]noise=alls=8:allf=t[bg];[bg][1:v]overlay=x=80:y=80,"
                                  + _text_layer("between(t,1,2)", use_dt) + ",format=yuv420p"] + venc,
                          td / f"SHOT-00{len(tag)}.mp4")
            fs, rec = scan_clip(clip, td / "out", 0.5, "clip", None)
            times = [round(i * 0.5, 2) for i in rec["heuristic"]["bottom"]]
            check(times == [1.0, 1.5, 2.0],
                  f"[{tag}] 启发式恰好标记 1.0/1.5/2.0s 三个抽样（实得 {times}；得分 {[s[0] for s in rec['scores']]}）")
            check(any(f.code == "D1-heuristic-bottom" and f.level == "visual" for f in fs)
                  and not any(f.level == "error" for f in fs), f"[{tag}] 启发式 → visual，永不单独判 error")
            check(not rec["heuristic"]["upper"], f"[{tag}] 上部有 testsrc2 动态图案也不误标")
            st = rec["strip"]
            check(st.get("path") and Path(st["path"]).is_file() and len(st["samples"]) == 6,
                  f"[{tag}] 写出底部条带接触图（6 格）")
        if not has_dt:
            print("      （本机 ffmpeg 无 drawtext：已用细竖条 drawbox 模拟字形笔画）")

        # 3. 全程字幕 → 时间对比失效 → persistent
        full = _synth(base + ["-filter_complex", "[0:v]noise=alls=8:allf=t[bg];[bg][1:v]overlay=x=80:y=80,"
                              + _text_layer("gte(t,0)", has_dt) + ",format=yuv420p"] + venc, td / "full.mp4")
        fs, rec = scan_clip(full, td / "out", 0.5, "clip", None)
        check(any(f.code == "D1-heuristic-persistent" for f in fs), "全程字幕 → visual D1-heuristic-persistent")

        # 3b. D2 现场：纯黑字卡中段被加小号文字水印（通用 0.08 下限会整段漏报；回归）
        if has_dt:
            wm = "drawtext=text='LAVCE':fontsize=28:fontcolor=white@0.6:x=(w-tw)/2:y=(h-th)/2:enable='between(t,1,2)'"
        else:
            wm = ",".join(f"drawbox=x={200 + i * 9}:y=420:w=2:h=16:color=white:t=fill:enable='between(t,1,2)'"
                          for i in range(8))
        card = _synth(["-f", "lavfi", "-i", "color=c=black:s=480x864:r=24:d=3", "-vf", wm + ",format=yuv420p"] + venc,
                      td / "SHOT-099 %d 片尾.mp4")
        fs, rec = scan_clip(card, td / "out 100%", 0.5, "clip", None)
        fl = [f for f in fs if f.code == "D2-heuristic-flat"]
        check(len(fl) == 1 and fl[0].level == "visual" and fl[0].data["times"] == [1.0, 1.5, 2.0]
              and not any(f.level == "error" for f in fs),
              f"纯黑字卡 1–2s 中部小号水印 → visual D2-heuristic-flat @1.0/1.5/2.0s（实得 "
              f"{fl[0].data['times'] if fl else '—'}；笔画峰值 {[max(x) for x in rec['scores']]}）")
        check((rec.get("frames_sheet") or {}).get("path") and Path(rec["frames_sheet"]["path"]).is_file()
              and Path(rec["strip"]["path"]).name == "SHOT-099 %d 片尾.burnin-strip.jpg",
              "整帧接触图写出；文件名含 % 空格 中文按字面写出（回归：曾被当成序列模板写成别名）")
        blank = _synth(["-f", "lavfi", "-i", "color=c=black:s=480x864:r=24:d=3", "-vf", "format=yuv420p"] + venc,
                       td / "black.mp4")
        fs, rec = scan_clip(blank, td / "out", 0.5, "clip", None)
        check(not rec["heuristic"]["flat"] and not any(f.level == "visual" for f in fs), "纯黑无字 → 不标记")

        # 3c. 精简版 ffmpeg 缺 drawbox：条带图降级为无红框，不丢证据
        real_run = ac.run
        try:
            ac.run = (lambda cmd, timeout=600: subprocess.CompletedProcess(cmd, 1, "", "No such filter: 'drawbox'")
                      if any("drawbox=" in c for c in cmd) else real_run(cmd, timeout))
            fs, rec = scan_clip(card, td / "out_nobox", 0.5, "clip", None)
            check(rec["strip"].get("path") and rec["strip"].get("marks_drawn") is False
                  and not any(f.code == "D1-strip-failed" for f in fs), "缺 drawbox → 条带图照出（无红框），标记见 JSON")
        finally:
            ac.run = real_run

        # 4. 干净片段 → 无标记
        clean = _synth(["-f", "lavfi", "-i", "mandelbrot=s=360x640:r=24", "-t", "3"] + venc, td / "clean.mp4")
        fs, rec = scan_clip(clean, td / "out", 0.5, "clip", None)
        check(not rec["heuristic"]["bottom"] and not any(f.level in ("error", "visual") for f in fs),
              "无文字的 mandelbrot 片段 → 无标记")

        # 5. 注入假 OCR 后端：端到端
        fake = ("fake", lambda p: [{"text": "LAVCE", "conf": 0.9, "bbox": [10, 10, 50, 12]}]
                if int(p.stem.split("_")[1]) == 2 else [])
        fs, rec = scan_clip(clean, td / "out", 0.5, "clip", fake)
        check(any(f.code == "D2-watermark" and f.level == "error" and "1.00s" in f.msg for f in fs)
              and rec["ocr_backend"] == "fake", "假 OCR 在第 3 个抽样（1.00s）读到 LAVCE → error D2-watermark")
        boom = ("boom", lambda p: (_ for _ in ()).throw(RuntimeError("model missing")))
        fs, rec = scan_clip(clean, td / "out", 0.5, "clip", boom)
        check(any(f.code == "D1-ocr-degraded" for f in fs) and rec["ocr_backend"] is None,
              "OCR 后端运行时报错 → warn 降级，不崩溃")

        # 6. 坏文件 + CLI 契约
        broken = td / "broken.mp4"
        broken.write_bytes(b"garbage")
        fs, _ = scan_clip(broken, td / "out", 0.5)
        check(any(f.code == "P8-unreadable" and f.level == "error" for f in fs), "坏文件 → error P8-unreadable")
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + [str(clip), "--ocr", "none", "--out-dir", str(td / "cli"), "--json"],
                           capture_output=True, text=True)
        ok = False
        try:
            j = json.loads(r.stdout)
            ok = (j["ok"] is True and j["ocr"]["backend"] is None and j["counts"]["visual"] >= 1
                  and any(f["code"] == "D1-ocr-degraded" for f in j["findings"]))
        except Exception:
            pass
        check(r.returncode == 0 and ok, "CLI --ocr none --json：退出码 0，报告降级（warn D1-ocr-degraded）+ visual")
        r = subprocess.run(me + [str(clip), "--ocr", "none", "--out-dir", str(td / "cli")], capture_output=True, text=True)
        check("未检测到 OCR 后端" in r.stdout or "降级为启发式" in r.stdout, "人类报告写明\"降级为启发式 + 目视\"")
        r = subprocess.run(me + [str(broken)], capture_output=True, text=True)
        check(r.returncode == 1, "CLI 坏文件 → 退出码 1")
        for fx in ("good", "bad"):
            r = subprocess.run(me + [str(ac.FIXTURES / fx)], capture_output=True, text=True)
            check(r.returncode == 0 and "P8-no-clips" in r.stdout, f"CLI fixtures/{fx}（无视频）→ 0 error")
        r = subprocess.run(me + [str(ac.FIXTURES / "good")], capture_output=True,
                           env=dict(os.environ, PYTHONIOENCODING="gbk"))
        check(r.returncode == 0 and b"Traceback" not in r.stderr,
              "stdout 为 GBK（Windows cmd 重定向，E3-1）→ 报告照出，不因 ⚠️ 等图标崩溃（回归）")
        r = subprocess.run(me + [str(td / "nope.mp4")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 路径不存在 → 退出码 2")
        r = subprocess.run(me + [str(clip), "--interval", "0"], capture_output=True, text=True)
        check(r.returncode == 2, "CLI --interval 0 → 退出码 2")

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
    ap.add_argument("--interval", type=float, default=0.5, help="抽样间隔秒（默认 0.5）")
    ap.add_argument("--mode", choices=["clip", "final"], default="clip",
                    help="clip=生成镜（OCR 文字→error）；final=成片（硬字幕是设计，OCR 文字→visual）")
    ap.add_argument("--ocr", choices=["auto", "none"] + OCR_ORDER, default="auto",
                    help="OCR 后端（默认 auto：rapidocr→paddleocr→easyocr→tesseract；none=只用启发式）")
    ap.add_argument("--watermark-token", action="append", default=[], help="追加已知水印词（默认已含 LAVCE）")
    ap.add_argument("--floor", type=float, default=FLOOR, help=f"启发式绝对下限（默认 {FLOOR}）")
    ap.add_argument("--ratio", type=float, default=RATIO, help=f"启发式相对本片基线（P25）的倍数（默认 {RATIO}）")
    ap.add_argument("--out-dir", help="条带接触图输出目录（默认写在视频旁）")
    ap.add_argument("--recursive", action="store_true", help="目录输入时递归查找视频")
    ap.add_argument("--no-drawtext", action="store_true", help="条带图不烧录时间戳")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="运行自测（ffmpeg lavfi 合成素材 + 假 OCR），全部通过退出 0")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.inputs:
        ap.print_usage(sys.stderr)
        ac.die("需要视频文件或目录（或 --selftest）")
    need_ffmpeg()
    if not 0.04 <= a.interval <= 60 or a.floor <= 0 or a.ratio <= 1:
        ac.die("--interval 取 0.04–60 秒；--floor > 0；--ratio > 1")
    clips, findings = collect_clips(a.inputs, a.recursive)
    backend, notes = (None, []) if not clips else load_ocr(a.ocr)
    if clips and backend is None:
        why = "按要求未使用 OCR（--ocr none）" if a.ocr == "none" else "未检测到 OCR 后端"
        findings.append(ac.Finding("warn", "D1-ocr-degraded",
                                   f"{why}，降级为启发式 + 目视：启发式只给 visual 证据，不能单独判定无字幕；"
                                   f"装 rapidocr_onnxruntime（pip）后重跑可得逐字结果。尝试记录：{'; '.join(notes) or '—'}"))
    wm = DEFAULT_WATERMARKS + [w for w in a.watermark_token if w not in DEFAULT_WATERMARKS]
    records = []
    for c in clips:
        fs, rec = scan_clip(c, Path(a.out_dir) if a.out_dir else None, a.interval, a.mode, backend, wm,
                            a.floor, a.ratio, not a.no_drawtext)
        findings += fs
        records.append(rec)
    strips = [r[k]["path"] for r in records for k in ("strip", "frames_sheet") if (r.get(k) or {}).get("path")]
    summary = (f"OCR 后端：{backend[0] if backend else '无（启发式 + 目视）'}；共 {len(clips)} 个视频；"
               f"条带接触图：{', '.join(strips) or '—'}")
    return ac.emit(TITLE, findings, a.json, {"clips": records, "summary": summary,
                                             "ocr": {"backend": backend[0] if backend else None, "tried": notes,
                                                     "watermark_tokens": wm}})


if __name__ == "__main__":
    sys.exit(main())
