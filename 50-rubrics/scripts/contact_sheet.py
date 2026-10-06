#!/usr/bin/env python3
"""contact_sheet.py — 镜头接触表（抽帧拼图）+ 关键帧并排 + 区域放大裁剪：给"需目视"验收产出证据

用途：
  对生成视频（单镜 clip）或成片抽 N 帧（默认 12）拼成一张接触表 JPG。抽帧规则固定：
  在全片均匀分布，且**必含**首帧、中点帧、最后 0.5s 内的帧（尾部崩解检查，P8）。
  每格烧录 帧号 / 时间 / 角色（FIRST / MID / TAIL；尾部格橙框）；drawtext 不可用时不烧录，
  时间戳只写进 JSON 旁车并在报告里说明。
  --keyframe：把起始关键帧放在第 1 格（青框），与视频首/中/尾帧并排比对背景元素清单（B4）。
  --crop：对每个抽样帧导出同一区域的整数倍放大裁剪（最近邻放大，不"脑补"细节），并拼成裁剪表（C2）。
  脚本只产出证据、报告事实，不判断"好不好看"；结论由 agent 逐格目视后写进 qc/<SHOT>.md。

溯源：P8（视频验收固定环节：逐段抽帧核验 无烧录文字/无克隆/无穿模/尾部无崩解）、
      B4（重复伪影"第二骨架"：抽帧对比关键帧与视频前中后段背景元素清单）、
      D1（烧录字幕：抽帧核验无烧录文字）、
      C2（验收放水：高风险资产必须留下裁剪特写等逐特征证据，不得只写"通过"）、C1-7（方位/对比属性单独放大）。

输入格式：
  视频文件（.mp4 .mov .mkv .webm .m4v .avi）或含视频的目录（--recursive 递归）；关键帧为图片（.png .jpg .jpeg .webp）。
  镜号 / 参考图命名见 70-playbooks/format-contracts.md §0.4（SHOT-012、REF-SHOT012-START）——
  --keyframe-dir 按镜号自动配对 `*SHOT012*START*` / `*SHOT-012*`；
  验收记录引用证据的写法见 format-contracts.md §6（qc/<SHOT-nnn>.md 的「证据」行）。

输出（默认写在视频旁，--out-dir 可改）：
  <stem>.contact.jpg           接触表（默认 4 列）
  <stem>.contact.json          旁车：每格帧号/时间/角色、探测信息、尾部窗口、裁剪文件清单、目视清单
  <stem>.crops/<name>/*.png    --crop 的逐帧放大裁剪；<stem>.crop-<name>.jpg 为带标签的裁剪拼图

判定：
  visual P8-contact-sheet    接触表已生成 → 需目视逐格核对（清单见报告）
  visual B4-keyframe         第 1 格为关键帧 → 需目视比对背景元素清单
  visual C2-crop             放大裁剪已生成 → 需目视逐特征核对
  info   P8-probe            分辨率 / 帧率 / 帧数 / 时长
  info   P8-no-drawtext      drawtext 不可用或失败：格内无时间戳，见 JSON 旁车
  info   B4-keyframe-aspect  关键帧宽高比与视频不同（T-1：板图/关键帧 1696×2528，视频 9:16）
  info   B4-keyframe-unmatched  --keyframe-dir 中找不到该镜的关键帧
  warn   T2-aspect           视频偏离 9:16 超过 --aspect-tol（默认 2%：生成器尺寸取 16/32 倍数，
                             T-1 的剪辑尺寸 480×864 实为 5:9，偏 1.2%，单镜层面不报；成片 1% 硬线见 loudness_verify.py）
  warn   P8-no-clips         目录中没有视频文件
  warn   P8-frame-count      抽到的帧数与预期不符（容器帧数 ≠ 解码帧数），格内帧号以 JSON 为准
  error  P8-unreadable       视频无法探测 / 解码 / 抽帧
  error  C2-crop-oob         裁剪区超出该镜画面
  error  B4-keyframe-missing --keyframe 指定的图片不存在或无法读取
  error  P8-render-failed    接触表/裁剪图写不出（输出目录不可写、磁盘满等环境问题）→ 退出码 2
  info   P8-no-border        ffmpeg 缺 drawbox：尾部格/关键帧格不加色框（格序见 JSON）
  info   P8-out-renamed      多个输入同名（如递归目录 + --out-dir）：输出名加上级目录前缀，避免互相覆盖

鲁棒性约定：每格统一转 rgb24 再拼图（RGBA/灰度/16 位关键帧不会让拼图中途重建而丢格）；
  单图输出一律 -update 1（文件名含 % 不被当成序列模板）；缺 select/scale/tile 滤镜 → 退出码 2。

用法示例：
  python3 contact_sheet.py season-01/ep03/assets/clips/SHOT-004.mp4
  python3 contact_sheet.py SHOT-004.mp4 --keyframe assets/keyframes/REF-SHOT004-START.png --out-dir qc/SHOT-004
  python3 contact_sheet.py SHOT-004.mp4 --crop face=180:220:160:160 --crop sword=40:500:200:120
  python3 contact_sheet.py season-01/ep03/assets/clips/ --keyframe-dir season-01/ep03/assets/keyframes --json
  python3 contact_sheet.py --selftest

退出码：0 通过（只有 visual/info/warn）/ 1 发现 error / 2 用法或环境错误（缺 ffmpeg 或必需滤镜、路径不存在、参数非法、输出写不出）。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "接触表 / 关键帧比对 / 放大裁剪（P8 / B4 / D1 / C2）"
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TAIL_SEC = 0.5          # P8：尾部崩解检查窗口
ASPECT_9_16 = 9 / 16
PAD = 4
BG = "0x202020"
TAIL_COLOR = "orange"
KEY_COLOR = "cyan"


# ------------------------------------------------------------------ ffmpeg 小工具（academy_common 只有 run / ffprobe_json）

_FILTERS: set | None = None


def ff_filters() -> set:
    """ffmpeg 已编译的滤镜名集合（用于降级判断）。"""
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


REQUIRED_FILTERS = ("select", "scale", "tile")      # 缺了无法出接触表 → 退出码 2；drawtext/drawbox/pad 缺失只降级


def need_ffmpeg():
    missing = [t for t in ("ffmpeg", "ffprobe") if not ac.have(t)]
    if missing:
        ac.die(f"找不到 {' / '.join(missing)}：安装 ffmpeg（含 ffprobe）并加入 PATH 后重跑")
    flt = ff_filters()
    lack = [f for f in REQUIRED_FILTERS if flt and f not in flt]
    if lack:
        ac.die(f"ffmpeg 缺少必需滤镜 {' / '.join(lack)}：换用完整版 ffmpeg（含 libavfilter 全部内置滤镜）后重跑")


def _ratio(s, default: float = 0.0) -> float:
    try:
        s = str(s).replace(":", "/")
        if "/" in s:
            a, b = s.split("/", 1)
            a, b = float(a), float(b)
            return a / b if b else default
        return float(s)
    except (TypeError, ValueError):
        return default


def _rotation(v: dict) -> int:
    rot = v.get("tags", {}).get("rotate")
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = sd["rotation"]
    try:
        return int(round(float(rot))) % 360 if rot is not None else 0
    except (TypeError, ValueError):
        return 0


def probe_video(path: Path) -> dict:
    info = ac.ffprobe_json(path)
    vs = [s for s in info.get("streams", []) if s.get("codec_type") == "video"
          and not s.get("disposition", {}).get("attached_pic")]
    if not vs:
        raise RuntimeError("文件中没有视频流")
    v = vs[0]
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    rot = _rotation(v)
    if rot in (90, 270):
        w, h = h, w
    sar = _ratio(v.get("sample_aspect_ratio", "1:1"), 1.0) or 1.0
    fps = _ratio(v.get("avg_frame_rate", "0/0")) or _ratio(v.get("r_frame_rate", "0/0")) or 24.0
    dur = float(v.get("duration") or info.get("format", {}).get("duration") or 0.0)
    if w <= 0 or h <= 0:
        raise RuntimeError("无法读取画面尺寸")
    return {"width": w, "height": h, "sar": round(sar, 4), "dar": round(w * sar / h, 4), "fps": round(fps, 3),
            "duration": round(dur, 3), "codec": v.get("codec_name", ""), "rotation": rot}


def frame_times(path: Path, fps: float) -> list[float]:
    """逐帧显示时间（秒，相对首帧）。需要解码一遍，生成镜 ≤15s 很快。"""
    p = ac.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                "frame=best_effort_timestamp_time", "-of", "csv=p=0", str(path)])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe 逐帧探测失败")
    raw: list[float | None] = []
    for ln in p.stdout.splitlines():
        ln = ln.strip().strip(",")
        if not ln:
            continue
        try:
            raw.append(float(ln.split(",")[0]))
        except ValueError:
            raw.append(None)
    times = [t if t is not None else i / fps for i, t in enumerate(raw)]
    if not times:
        return []
    t0 = times[0]
    return [round(t - t0, 6) for t in times]


def _rnd(x: float) -> int:
    return int(math.floor(x + 0.5))


# ------------------------------------------------------------------ 抽帧规则（P8）

def pick_frames(times: list[float], n: int, tail_count: int = 2, tail_sec: float = TAIL_SEC,
                fps: float = 24.0) -> list[dict]:
    """返回 [{frame, t, roles}]：均匀 n 帧，强制包含首帧、中点帧、最后 tail_sec 内 tail_count 帧。"""
    F = len(times)
    if F == 0:
        return []
    last = F - 1
    mid = last // 2
    fd = (times[last] - times[last - 1]) if F >= 2 else 1.0 / fps
    if fd <= 0:
        fd = 1.0 / fps
    end_t = times[last] + fd
    window = [i for i in range(F) if times[i] >= end_t - tail_sec - 1e-6]
    if len(window) <= tail_count:
        tails = list(window)
    else:
        tails = sorted({window[_rnd((len(window) - 1) * (j + 1) / tail_count)] for j in range(tail_count)})
    required = sorted({0, mid, *tails})
    n = max(n, len(required))
    if F <= n:
        chosen = list(range(F))
    else:
        chosen = sorted({_rnd(i * last / (n - 1)) for i in range(n)})
        for r in required:
            if r in chosen:
                continue
            cands = [c for c in chosen if c not in required]
            near = min(cands, key=lambda c: (abs(c - r), c))
            chosen.remove(near)
            chosen.append(r)
            chosen.sort()
    wset = set(window)
    out = []
    for i in chosen:
        roles = []
        if i == 0:
            roles.append("first")
        if i == mid:
            roles.append("mid")
        if i in wset:
            roles.append("tail")
        out.append({"frame": i, "t": round(times[i], 3), "roles": roles or ["even"]})
    return out


# ------------------------------------------------------------------ 渲染

def _ff(args: list[str]) -> subprocess.CompletedProcess:
    return ac.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + args)


def _ff_one(args: list[str], out: Path) -> subprocess.CompletedProcess:
    """写单张图：-update 1 让 image2 按字面文件名写（名字含 % 时不被当成序列模板）。"""
    return _ff(args + ["-frames:v", "1", "-update", "1", str(out)])


def extract_frames(clip: Path, frames: list[int], td: Path) -> list[Path]:
    expr = "+".join(f"eq(n\\,{i})" for i in frames)
    base = ["-i", str(clip), "-map", "0:v:0", "-vf", f"select='{expr}'"]
    out = str(td / "f_%03d.png")
    p = _ff(base + ["-fps_mode", "passthrough", out])
    if p.returncode != 0:                       # ffmpeg < 5.1 没有 -fps_mode
        p = _ff(base + ["-vsync", "0", out])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[-400:] or "ffmpeg 抽帧失败")
    return sorted(td.glob("f_*.png"))


def _label_text(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9#+. _-]", "", s)


def make_tile(src: Path, dst: Path, tw: int, th: int, label: str, border: str | None,
              use_text: bool, fit: bool = False, scale: bool = True) -> tuple[bool, bool]:
    """缩放 + 边框 + 标签 → (是否烧录了文字, 是否加了色框)。drawtext / drawbox / pad 失败逐级降级。
    末尾统一 format=rgb24：关键帧可能是 RGBA / 灰度 / 16 位 PNG，若与视频帧像素格式不同，
    拼图时 ffmpeg 会在中途重建滤镜图，tile 只输出后半段（实测 RGBA 关键帧格整格丢失）。"""
    flt = ff_filters()
    geo = []
    if scale and fit:
        geo += [f"scale={tw}:{th}:force_original_aspect_ratio=decrease"]
        geo += ([f"pad={tw}:{th}:(ow-iw)/2:(oh-ih)/2:color={BG}"] if (not flt or "pad" in flt)
                else [f"scale={tw}:{th}"])
    elif scale:
        geo.append(f"scale={tw}:{th}")
    box = [f"drawbox=x=0:y=0:w=iw:h=ih:color={border}:t=5"] if border else []
    fs = max(12, min(28, tw // 14))
    txt = [f"drawtext=text='{_label_text(label)}':x=6:y=6:fontsize={fs}:fontcolor=white"
           f":box=1:boxcolor=black@0.65:boxborderw=4"] if use_text else []
    attempts = [(geo + box + txt, bool(txt), bool(box)), (geo + box, False, bool(box)), (geo + txt, bool(txt), False),
                (geo, False, False)]
    if fit:      # pad 不可用/失败时的最后退路：拉伸到格子尺寸（报告里已有宽高比提示）
        attempts.append(([f"scale={tw}:{th}"], False, False))
    seen = set()
    for chain, has_txt, has_box in attempts:
        key = tuple(chain)
        if key in seen:
            continue
        seen.add(key)
        p = _ff_one(["-i", str(src), "-vf", ",".join(chain + ["format=rgb24"])], dst)
        if p.returncode == 0 and dst.exists():
            return has_txt, has_box or not border
    raise RuntimeError(f"生成格子失败：{src.name}（{p.stderr.strip()[-160:]}）")


def tile_sheet(tiles_dir: Path, prefix: str, count: int, cols: int, out_jpg: Path):
    cols = max(1, min(cols, count))
    rows = math.ceil(count / cols)
    src = ["-framerate", "1", "-start_number", "0", "-i", str(tiles_dir / f"{prefix}_%03d.png")]
    for layout in (f"tile={cols}x{rows}:padding={PAD}:margin={PAD}:color={BG}", f"tile={cols}x{rows}"):
        p = _ff_one(src + ["-vf", layout, "-q:v", "3"], out_jpg)
        if p.returncode == 0 and out_jpg.exists():
            return
    raise RuntimeError(f"拼接接触表失败：{p.stderr.strip()[-300:]}")


def image_size(path: Path) -> tuple[int, int]:
    info = ac.ffprobe_json(path)
    s = next(s for s in info["streams"] if s.get("codec_type") == "video")
    return int(s["width"]), int(s["height"])


# ------------------------------------------------------------------ 输入

def parse_crop(spec: str, k: int) -> dict:
    name = f"crop{k}"
    if "=" in spec:
        name, spec = spec.split("=", 1)
        name = name.strip()
    parts = spec.strip().split(":")
    if len(parts) != 4 or not all(re.fullmatch(r"\d+", p.strip()) for p in parts):
        raise ValueError(f"--crop 需写成 [名字=]x:y:w:h（整数像素），收到 '{spec}'")
    x, y, w, h = (int(p) for p in parts)
    if w <= 0 or h <= 0:
        raise ValueError(f"--crop 宽高必须 > 0：'{spec}'")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", name):
        raise ValueError(f"--crop 名字只能用英文/数字/_/-：'{name}'")
    return {"name": name, "x": x, "y": y, "w": w, "h": h}


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
                fs.append(ac.Finding("warn", "P8-no-clips",
                                     f"目录中没有视频文件（{'/'.join(sorted(VIDEO_EXTS))}）：确认路径是否指向 clips 目录，"
                                     f"或加 --recursive", str(p)))
            clips += found
        else:
            clips.append(p)
    return clips, fs


def match_keyframe(clip: Path, kdir: Path) -> Path | None:
    m = re.search(r"SHOT-?(\d{3})", clip.stem, re.I)
    if not m or not kdir.is_dir():
        return None
    num = m.group(1)
    cands = [p for p in sorted(kdir.iterdir()) if p.is_file() and p.suffix.lower() in IMAGE_EXTS
             and re.search(rf"SHOT-?{num}(?!\d)", p.stem, re.I)]
    cands.sort(key=lambda p: (0 if "START" in p.stem.upper() else 1, p.name))
    return cands[0] if cands else None


# ------------------------------------------------------------------ 主流程（单镜）

def _render_failed(e: Exception, out_dir: Path, where: str) -> ac.Finding:
    return ac.Finding("error", "P8-render-failed",
                      f"接触表/裁剪图写不出：{str(e)[:200]}——检查输出目录 {out_dir} 可写、磁盘空间、"
                      f"`ffmpeg -filters` 是否含 scale/tile/select 后重跑（环境问题，退出码 2）", where)


def contact_one(clip: Path, out_dir: Path | None = None, n: int = 12, cols: int = 4, tile_width: int = 270,
                tail_count: int = 2, keyframe: Path | None = None, crops: list[dict] | None = None,
                use_text: bool = True, aspect_tol: float = 0.02, stem: str | None = None
                ) -> tuple[list[ac.Finding], dict]:
    fs: list[ac.Finding] = []
    where = clip.name
    rec: dict = {"clip": str(clip)}
    try:
        pr = probe_video(clip)
        times = frame_times(clip, pr["fps"])
        if not times:
            raise RuntimeError("解码得到 0 帧")
    except Exception as e:  # noqa: BLE001
        fs.append(ac.Finding("error", "P8-unreadable",
                             f"无法探测/解码：{str(e)[:200]}——重新导出或重新下载该镜后再验收（坏文件不得放行）", where))
        return fs, rec
    pr["frames"] = len(times)
    if pr["duration"] <= 0:                     # 部分容器（mkv/webm/裸流）没有时长元数据
        pr["duration"] = round(len(times) / pr["fps"], 3) if pr["fps"] else 0.0
    rec["probe"] = pr
    fs.append(ac.Finding("info", "P8-probe",
                         f"{pr['width']}×{pr['height']}，{pr['fps']} fps，{pr['frames']} 帧，{pr['duration']:.2f}s", where,
                         dict(pr)))
    dev = abs(pr["dar"] / ASPECT_9_16 - 1)
    if dev > aspect_tol:
        fs.append(ac.Finding("warn", "T2-aspect",
                             f"画幅 {pr['width']}×{pr['height']}（DAR {pr['dar']}，偏离 9:16 {dev:.1%}）：确认生成/导出分辨率是否送错；"
                             f"成片须 9:16（loudness_verify.py 按 1% 判 error）", where, {"deviation": round(dev, 4)}))

    picks = pick_frames(times, n, tail_count, TAIL_SEC, pr["fps"])
    use_text = use_text and "drawtext" in ff_filters()
    out_dir = Path(out_dir) if out_dir else clip.parent
    stem = stem or clip.stem
    jpg, side = out_dir / f"{stem}.contact.jpg", out_dir / f"{stem}.contact.json"
    tw = max(64, tile_width - tile_width % 2)
    th = max(2, 2 * _rnd(tw / pr["dar"] / 2))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        fs.append(_render_failed(e, out_dir, where))
        return fs, rec

    tiles_meta: list[dict] = []
    text_ok, border_ok = use_text, True
    crop_records: list[dict] = []
    tail_tiles: list[int] = []
    with tempfile.TemporaryDirectory(prefix="contact_") as tds:
        td = Path(tds)
        # 关键帧可读性（先拷进临时目录：原名里的 % / 空格 / 中文都不会进 ffmpeg 参数）
        kf_local, kw, kh = None, 0, 0
        if keyframe is not None:
            if not keyframe.is_file():
                fs.append(ac.Finding("error", "B4-keyframe-missing",
                                     f"关键帧不存在：{keyframe}——核对 first_frame（REF-SHOTxxx-START）的文件路径", where))
                keyframe = None
            else:
                try:
                    kf_local = td / f"keyframe{keyframe.suffix.lower()}"
                    shutil.copyfile(keyframe, kf_local)
                    kw, kh = image_size(kf_local)
                except Exception as e:  # noqa: BLE001
                    fs.append(ac.Finding("error", "B4-keyframe-missing",
                                         f"关键帧无法读取：{keyframe}（{str(e)[:120]}）——重新导出 PNG/JPG 后重跑", where))
                    keyframe = None
        try:
            frames = extract_frames(clip, [p["frame"] for p in picks], td)
        except Exception as e:  # noqa: BLE001
            fs.append(ac.Finding("error", "P8-unreadable", f"抽帧失败：{str(e)[:200]}——重新导出该镜后重跑", where))
            return fs, rec
        if len(frames) != len(picks):
            fs.append(ac.Finding("warn", "P8-frame-count",
                                 f"抽到 {len(frames)} 帧，预期 {len(picks)} 帧（容器帧数与解码帧数不一致）：格内帧号可能错位，"
                                 f"以 JSON 为准并用 psnr_scan.py 复核", where))
            picks = picks[:len(frames)]
        try:
            k = 0
            if keyframe is not None:
                t_ok, b_ok = make_tile(kf_local, td / f"t_{k:03d}.png", tw, th, "KEYFRAME", KEY_COLOR, use_text,
                                       fit=True)
                text_ok, border_ok = text_ok and t_ok, border_ok and b_ok
                tiles_meta.append({"tile": 1, "roles": ["keyframe"], "path": str(keyframe)})
                k += 1
                kd = round(kw / kh, 4)
                if abs(kd / pr["dar"] - 1) > 0.01:
                    how = ("已等比缩放加边" if (not ff_filters() or "pad" in ff_filters())
                           else "已被拉伸到格子尺寸（ffmpeg 缺 pad 滤镜，形状有变形）")
                    fs.append(ac.Finding("info", "B4-keyframe-aspect",
                                         f"关键帧 {kw}×{kh}（宽高比 {kd}）与视频（{pr['dar']}）不同，第 1 格{how}："
                                         f"比对时注意取景范围差异，只比背景元素有无/数量，不比边缘", where))
            for p, f in zip(picks, frames):
                roles = p["roles"]
                label = f"#{p['frame']} {p['t']:.2f}s {'+'.join(r.upper() for r in roles if r != 'even')}".strip()
                border = TAIL_COLOR if "tail" in roles else None
                t_ok, b_ok = make_tile(f, td / f"t_{k:03d}.png", tw, th, label, border, use_text)
                text_ok, border_ok = text_ok and t_ok, border_ok and b_ok
                tiles_meta.append({"tile": k + 1, "frame": p["frame"], "t": p["t"], "roles": roles})
                if "tail" in roles:
                    tail_tiles.append(k + 1)
                k += 1
            tile_sheet(td, "t", k, cols, jpg)

            for c in crops or []:
                if c["x"] + c["w"] > pr["width"] or c["y"] + c["h"] > pr["height"]:
                    fs.append(ac.Finding("error", "C2-crop-oob",
                                         f"裁剪区 {c['name']}={c['x']}:{c['y']}:{c['w']}:{c['h']} 超出画面 "
                                         f"{pr['width']}×{pr['height']}：按本镜分辨率改坐标（先看 {jpg.name} 定位）", where))
                    continue
                zoom = max(1, min(8, _rnd(400 / max(c["w"], c["h"]))))
                cdir = out_dir / f"{stem}.crops" / c["name"]
                cdir.mkdir(parents=True, exist_ok=True)
                files = []
                for j, (p, f) in enumerate(zip(picks, frames)):
                    tmp_raw = td / f"r_{j:03d}.png"
                    pc = _ff_one(["-i", str(f), "-vf", f"crop={c['w']}:{c['h']}:{c['x']}:{c['y']},"
                                  f"scale=iw*{zoom}:ih*{zoom}:flags=neighbor,format=rgb24"], tmp_raw)
                    if pc.returncode != 0 or not tmp_raw.exists():
                        raise RuntimeError(f"裁剪失败：{pc.stderr.strip()[-200:]}")
                    raw = cdir / f"f{p['frame']:05d}_t{p['t']:.2f}.png"
                    shutil.copyfile(tmp_raw, raw)
                    files.append(str(raw))
                    t_ok, b_ok = make_tile(tmp_raw, td / f"c_{j:03d}.png", 0, 0, f"#{p['frame']} {p['t']:.2f}s",
                                           TAIL_COLOR if "tail" in p["roles"] else None, use_text, scale=False)
                    border_ok = border_ok and b_ok
                csheet = out_dir / f"{stem}.crop-{c['name']}.jpg"
                tile_sheet(td, "c", len(files), cols, csheet)
                for old in list(td.glob("c_*.png")) + list(td.glob("r_*.png")):
                    old.unlink()
                crop_records.append({"name": c["name"], "rect": [c["x"], c["y"], c["w"], c["h"]], "zoom": zoom,
                                     "sheet": str(csheet), "files": files})
        except Exception as e:  # noqa: BLE001  （输出不可写、磁盘满、滤镜运行失败）
            fs.append(_render_failed(e, out_dir, where))
            return fs, rec

    checklist = [
        "无烧录文字/字幕/水印（D1；纯色画面出现 LAVCE 类水印见 D2）",
        "无克隆脸：同框人物脸/发型/体型可区分，人数与分镜一致（B3）",
        "无穿模、无肢体崩坏、无多余肢体",
        f"尾部无崩解：第 {', '.join(map(str, tail_tiles)) or '—'} 格 = 最后 {TAIL_SEC}s（P8）",
    ]
    if keyframe is not None:
        checklist.append("背景元素与第 1 格关键帧一致：先列关键帧背景元素清单，再逐格找新增/消失元素（B4 第二骨架）")
    rec.update({
        "contact_sheet": str(jpg), "sidecar": str(side), "tiles": tiles_meta, "cols": max(1, min(cols, len(tiles_meta))),
        "tile_size": [tw, th], "tail_window_sec": TAIL_SEC, "tail_tiles": tail_tiles,
        "labels_burned": bool(text_ok), "borders_drawn": bool(border_ok), "keyframe": str(keyframe) if keyframe else None,
        "crops": crop_records, "visual_checklist": checklist,
    })
    try:
        side.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        fs.append(_render_failed(e, out_dir, where))
        return fs, rec

    if not text_ok:
        fs.append(ac.Finding("info", "P8-no-drawtext",
                             f"ffmpeg drawtext 不可用或失败，格内未烧录时间戳：各格帧号/时间见 {side.name} 的 tiles（按格序）", where))
    if not border_ok:
        fs.append(ac.Finding("info", "P8-no-border",
                             f"ffmpeg drawbox 不可用或失败，尾部格/关键帧格没有色框：尾部格 = 第 "
                             f"{', '.join(map(str, tail_tiles)) or '—'} 格（见 {side.name} 的 tail_tiles）", where))
    fs.append(ac.Finding("visual", "P8-contact-sheet",
                         f"需目视：打开 {jpg} 逐格核对 " + "；".join(f"{'①②③④⑤'[i]}{c}" for i, c in enumerate(checklist))
                         + f"。逐格结论 + 证据路径写入 qc/<SHOT>.md（C2：不得只写'通过'）；任一项不过 → 同提示词换 seed 重出"
                           f"（B4 实证：4 seed 抽帧选优），仅尾部崩解可在崩解前截断。", where,
                         {"contact_sheet": str(jpg), "sidecar": str(side), "tail_tiles": tail_tiles}))
    if keyframe is not None:
        fs.append(ac.Finding("visual", "B4-keyframe",
                             f"需目视：{jpg.name} 第 1 格为关键帧 {keyframe.name}——写出其背景元素清单（物体/人物/建筑/光源），"
                             f"逐格比对首/中/尾格是否新增或消失元素；出现关键帧中不存在的元素 → 换 seed 重出", where))
    for c in crop_records:
        fs.append(ac.Finding("visual", "C2-crop",
                             f"需目视：{Path(c['sheet']).name}（{c['name']} 区域 ×{c['zoom']} 放大，{len(c['files'])} 帧）"
                             f"逐特征核对必现/禁用项与方位属性（C2 / C1-7），把裁剪图路径写进验收记录", where,
                             {"sheet": c["sheet"], "dir": str(Path(c["files"][0]).parent) if c["files"] else ""}))
    return fs, rec


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


def _avg_rgb(img: Path, x: int, y: int, w: int, h: int) -> tuple[int, int, int]:
    """图片某矩形区域的平均 RGB（自测用：确认拼图第 k 格确实是预期内容）。"""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(img), "-vf",
                        f"crop={w}:{h}:{x}:{y},scale=1:1:flags=area,format=rgb24", "-frames:v", "1",
                        "-f", "rawvideo", "-"], capture_output=True)
    b = p.stdout[:3]
    return (b[0], b[1], b[2]) if len(b) == 3 else (-1, -1, -1)


def selftest() -> int:
    need_ffmpeg()
    results: list[tuple[bool, str]] = []

    def check(cond, label):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    # 1. 抽帧规则（纯逻辑）
    t260 = [i / 24 for i in range(260)]
    pk = pick_frames(t260, 12)
    fr = [p["frame"] for p in pk]
    check(len(pk) == 12 and 0 in fr and 129 in fr and 259 in fr,
          "260 帧（10.83s）抽 12 帧：含首帧 #0、中点 #129、末帧 #259")
    tails = [p for p in pk if "tail" in p["roles"]]
    check(len(tails) >= 2 and all(p["t"] >= 260 / 24 - TAIL_SEC - 1e-6 for p in tails),
          "至少 2 帧落在最后 0.5s 内且标 tail（P8 尾部崩解检查）")
    check(fr == sorted(set(fr)), "帧号严格递增且不重复")
    check([p["frame"] for p in pick_frames([i / 24 for i in range(8)], 12)] == list(range(8)),
          "短于 N 帧的片段取全部帧")

    venc = _venc()
    with tempfile.TemporaryDirectory(prefix="contact_selftest_") as tds:
        td = Path(tds)
        clip = _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24:d=3"] + venc, td / "SHOT-004.mp4")

        # 2. 基本接触表
        fs, rec = contact_one(clip, td / "qc", n=12, cols=4, tile_width=270)
        jpg, side = td / "qc" / "SHOT-004.contact.jpg", td / "qc" / "SHOT-004.contact.json"
        check(jpg.is_file() and side.is_file(), "写出 <stem>.contact.jpg 与 <stem>.contact.json")
        check(not [f for f in fs if f.level == "error"] and any(f.code == "P8-contact-sheet" and f.level == "visual"
                                                                for f in fs),
              "合成 9:16 片段：0 error，含 visual P8-contact-sheet")
        js = json.loads(side.read_text(encoding="utf-8"))
        frames = [t["frame"] for t in js["tiles"]]
        check(len(js["tiles"]) == 12 and frames[0] == 0 and 35 in frames and frames[-1] == 71,
              "72 帧片段：12 格，含 #0 / 中点 #35 / 末帧 #71")
        check(all(t["t"] >= 3.0 - TAIL_SEC - 1e-6 for t in js["tiles"] if "tail" in t["roles"])
              and len(js["tail_tiles"]) >= 2, "JSON 记录尾部格（最后 0.5s）≥2 格")
        w, h = image_size(jpg)
        check((w, h) == (2 * PAD + 4 * 270 + 3 * PAD, 2 * PAD + 3 * 480 + 2 * PAD),
              f"接触表尺寸 = 4 列 × 3 行 × 270×480 + 间距（实得 {w}×{h}）")
        check(js["labels_burned"] == ("drawtext" in ff_filters()), "有 drawtext 则烧录标签，JSON 如实记录")

        # 3. 关键帧第 1 格（宽高比不同 → 等比加边 + info）
        kf = _synth(["-f", "lavfi", "-i", "smptebars=s=339x505", "-frames:v", "1"], td / "REF-SHOT004-START.png")
        fs, rec = contact_one(clip, td / "qc2", keyframe=kf)
        check(len(rec["tiles"]) == 13 and rec["tiles"][0]["roles"] == ["keyframe"],
              "--keyframe：13 格，第 1 格为关键帧")
        check(any(f.code == "B4-keyframe" and f.level == "visual" for f in fs)
              and any(f.code == "B4-keyframe-aspect" for f in fs), "关键帧比对 visual + 宽高比差异 info")
        check(match_keyframe(clip, td) == kf, "--keyframe-dir 按镜号把 SHOT-004 配对到 REF-SHOT004-START.png")

        # 3b. RGBA 关键帧（ComfyUI 常出 RGBA PNG）：像素格式与视频帧不同也不能丢格（回归：曾整格丢失）
        kfa = _synth(["-f", "lavfi", "-i", "color=c=red:s=339x505,format=rgba", "-frames:v", "1"], td / "kf_rgba.png")
        fs, rec = contact_one(clip, td / "qc2b", keyframe=kfa)
        r0, g0, b0 = _avg_rgb(Path(rec["contact_sheet"]), PAD + 60, PAD + 120, 150, 240)
        check(len(rec["tiles"]) == 13 and r0 > 180 and g0 < 80 and b0 < 80,
              f"RGBA 关键帧：拼图第 1 格确为关键帧（红色，实测 RGB {r0},{g0},{b0}），13 格不丢")

        # 3c. 文件名 / 输出目录含 % 空格 中文：按字面写出，不被当成序列模板（回归：曾崩溃或写成别名）
        odd = td / "镜头 %d 目录"
        odd.mkdir()
        oclip = odd / "SHOT-009 %d 第一版.mp4"
        oclip.write_bytes(clip.read_bytes())
        fs, rec = contact_one(oclip, odd / "qc 100%", crops=[parse_crop("face=10:20:60:40", 1)])
        check(not [f for f in fs if f.level == "error"] and (odd / "qc 100%" / "SHOT-009 %d 第一版.contact.jpg").is_file()
              and Path(rec["crops"][0]["sheet"]).is_file(), "路径含 % / 空格 / 中文：接触表与裁剪图按字面文件名写出")

        # 3d. 缺 drawbox / pad 滤镜（猴子补丁模拟精简版 ffmpeg）→ 降级不崩溃
        global _FILTERS, _ff
        real_filters, real_ff = ff_filters(), _ff
        try:
            _FILTERS = set(real_filters) - {"drawbox", "pad"}
            _ff = (lambda args: subprocess.CompletedProcess(args, 1, "", "No such filter")
                   if any(("drawbox=" in a or "pad=" in a) for a in args) else real_ff(args))
            fs, rec = contact_one(clip, td / "qc_nf", keyframe=kfa)
            check(len(rec.get("tiles", [])) == 13 and any(f.code == "P8-no-border" for f in fs)
                  and not [f for f in fs if f.level == "error"], "缺 drawbox/pad：13 格照出，报 info P8-no-border，不崩溃")
        finally:
            _FILTERS, _ff = real_filters, real_ff

        # 4. 裁剪放大（C2）
        fs, rec = contact_one(clip, td / "qc3", crops=[parse_crop("face=10:20:60:40", 1)])
        cr = rec["crops"][0]
        cw, ch = image_size(Path(cr["files"][0]))
        check(len(cr["files"]) == 12 and cr["zoom"] == 7 and (cw, ch) == (420, 280) and Path(cr["sheet"]).is_file(),
              "--crop face=10:20:60:40 → 12 张 ×7 最近邻放大裁剪（420×280）+ 裁剪拼图")
        check(any(f.code == "C2-crop" and f.level == "visual" for f in fs), "裁剪产出 visual C2-crop")
        fs, _ = contact_one(clip, td / "qc4", crops=[parse_crop("250:0:100:100", 1)])
        check(any(f.code == "C2-crop-oob" and f.level == "error" for f in fs), "裁剪区超出 270×480 → error C2-crop-oob")
        bad_spec = False
        try:
            parse_crop("10:20:30", 1)
        except ValueError:
            bad_spec = True
        check(bad_spec, "--crop 语法错误 → ValueError（CLI 退出 2）")

        # 5. drawtext 降级
        fs, rec = contact_one(clip, td / "qc5", use_text=False)
        check(rec["labels_burned"] is False and any(f.code == "P8-no-drawtext" for f in fs)
              and all("t" in t for t in rec["tiles"]), "无 drawtext：不烧录，JSON 仍给每格时间，报告说明降级")

        # 6. 非 9:16 / 短片段 / 坏文件
        wide = _synth(["-f", "lavfi", "-i", "testsrc2=s=480x270:r=24:d=1"] + venc, td / "wide.mp4")
        fs, _ = contact_one(wide, td / "qc6")
        check(any(f.code == "T2-aspect" and f.level == "warn" for f in fs), "16:9 片段 → warn T2-aspect")
        t1 = _synth(["-f", "lavfi", "-i", "testsrc2=s=480x864:r=24", "-frames:v", "6"] + venc, td / "t1.mp4")
        fs, _ = contact_one(t1, td / "qc6b")
        check(not any(f.code == "T2-aspect" for f in fs), "T-1 剪辑尺寸 480×864（偏 1.2%）在单镜默认容差 2% 内，不告警")
        short = _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24", "-frames:v", "8"] + venc, td / "short.mp4")
        fs, rec = contact_one(short, td / "qc7")
        check(len(rec.get("tiles", [])) == 8, "8 帧片段 → 8 格（全取）")
        broken = td / "broken.mp4"
        broken.write_bytes(b"not a video at all")
        fs, _ = contact_one(broken, td / "qc8")
        check(any(f.code == "P8-unreadable" and f.level == "error" for f in fs), "坏文件 → error P8-unreadable")

        # 7. CLI 契约
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + [str(clip), "--out-dir", str(td / "cli"), "--json"], capture_output=True, text=True)
        ok_json = False
        try:
            j = json.loads(r.stdout)
            ok_json = j["ok"] is True and j["counts"]["visual"] >= 1 and len(j["clips"]) == 1
        except Exception:
            pass
        check(r.returncode == 0 and ok_json, "CLI 单镜 → 退出码 0，--json 可解析（ok=true，visual≥1）")
        clips_dir = td / "clips"
        clips_dir.mkdir()
        for nm in ("SHOT-001.mp4", "SHOT-002.mp4"):
            (clips_dir / nm).write_bytes(clip.read_bytes())
        r = subprocess.run(me + [str(clips_dir)], capture_output=True, text=True)
        check(r.returncode == 0 and (clips_dir / "SHOT-001.contact.jpg").is_file()
              and (clips_dir / "SHOT-002.contact.jpg").is_file(), "CLI 目录输入 → 每镜一张接触表")
        sub = clips_dir / "sub"
        sub.mkdir()
        (sub / "SHOT-001.mp4").write_bytes(clip.read_bytes())
        r = subprocess.run(me + [str(clips_dir), "--recursive", "--out-dir", str(td / "cli_dup")],
                           capture_output=True, text=True)
        check(r.returncode == 0 and "P8-out-renamed" in r.stdout and (td / "cli_dup" / "SHOT-001.contact.jpg").is_file()
              and (td / "cli_dup" / "sub__SHOT-001.contact.jpg").is_file(),
              "递归目录 + --out-dir 同名镜 → 第二个改名 sub__SHOT-001，不互相覆盖")
        r = subprocess.run(me + [str(broken), "--out-dir", str(td / "cli2")], capture_output=True, text=True)
        check(r.returncode == 1 and "P8-unreadable" in r.stdout, "CLI 坏文件 → 退出码 1")
        for fx in ("good", "bad"):
            r = subprocess.run(me + [str(ac.FIXTURES / fx)], capture_output=True, text=True)
            check(r.returncode == 0 and "P8-no-clips" in r.stdout, f"CLI fixtures/{fx}（无视频）→ 0 error，warn P8-no-clips")
        r = subprocess.run(me + [str(ac.FIXTURES / "good")], capture_output=True,
                           env=dict(os.environ, PYTHONIOENCODING="gbk"))
        check(r.returncode == 0 and b"Traceback" not in r.stderr,
              "stdout 为 GBK（Windows cmd 重定向，E3-1）→ 报告照出，不因 ⚠️ 等图标崩溃（回归）")
        r = subprocess.run(me + [str(td / "nope.mp4")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 路径不存在 → 退出码 2")
        r = subprocess.run(me + [str(clip), "--crop", "1:2:3"], capture_output=True, text=True)
        check(r.returncode == 2, "CLI --crop 语法错误 → 退出码 2")
        r = subprocess.run(me, capture_output=True, text=True)
        check(r.returncode == 2, "CLI 无参数 → 退出码 2")

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
    ap.add_argument("-n", "--frames", type=int, default=12, help="每镜抽帧数（默认 12；必含首/中/尾 0.5s）")
    ap.add_argument("--tail", type=int, default=2, help="最后 0.5s 内至少抽几帧（默认 2）")
    ap.add_argument("--cols", type=int, default=4, help="接触表列数（默认 4）")
    ap.add_argument("--tile-width", type=int, default=270, help="每格宽度像素（默认 270）")
    ap.add_argument("--keyframe", help="起始关键帧图片（仅单镜输入）：放在第 1 格比对背景元素（B4）")
    ap.add_argument("--keyframe-dir", help="关键帧目录：按镜号自动配对 *SHOT012*START*（多镜输入用）")
    ap.add_argument("--crop", action="append", default=[], metavar="[NAME=]X:Y:W:H",
                    help="对每个抽样帧导出该区域放大裁剪（可重复；像素坐标基于该镜分辨率）")
    ap.add_argument("--out-dir", help="输出目录（默认写在视频旁）")
    ap.add_argument("--recursive", action="store_true", help="目录输入时递归查找视频")
    ap.add_argument("--aspect-tol", type=float, default=0.02, help="单镜画幅偏离 9:16 的告警容差（默认 0.02）")
    ap.add_argument("--no-drawtext", action="store_true", help="不烧录时间戳（等同 drawtext 不可用时的降级）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="运行自测（ffmpeg lavfi 合成素材），全部通过退出 0")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.inputs:
        ap.print_usage(sys.stderr)
        ac.die("需要视频文件或目录（或 --selftest）")
    need_ffmpeg()
    if not 3 <= a.frames <= 64:
        ac.die("--frames 取值 3–64")
    if not 1 <= a.cols <= 16 or not 64 <= a.tile_width <= 1080 or not 1 <= a.tail <= 12:
        ac.die("--cols 1–16，--tile-width 64–1080，--tail 1–12")
    try:
        crops = [parse_crop(s, i + 1) for i, s in enumerate(a.crop)]
    except ValueError as e:
        ac.die(str(e))
    if len({c["name"] for c in crops}) != len(crops):
        ac.die("--crop 名字重复")
    clips, findings = collect_clips(a.inputs, a.recursive)
    if a.keyframe and len(clips) != 1:
        ac.die("--keyframe 只能配单个视频；多镜请用 --keyframe-dir")
    kdir = Path(a.keyframe_dir) if a.keyframe_dir else None
    if kdir is not None and not kdir.is_dir():
        ac.die(f"--keyframe-dir 不是目录：{kdir}")
    records = []
    used: set = set()
    for clip in clips:
        kf = Path(a.keyframe) if a.keyframe else None
        if kdir is not None:
            kf = match_keyframe(clip, kdir)
            if kf is None:
                findings.append(ac.Finding("info", "B4-keyframe-unmatched",
                                           f"{kdir} 中找不到该镜关键帧（按 SHOTnnn / SHOT-nnn 匹配）：用 --keyframe 手动指定",
                                           clip.name))
        out_dir = Path(a.out_dir) if a.out_dir else clip.parent
        stem = clip.stem
        key = (str(out_dir.resolve()), stem)
        if key in used:                          # 递归目录 / 多输入 + --out-dir：同名镜会互相覆盖
            stem = f"{clip.parent.name}__{clip.stem}"
            k2 = 2
            while (str(out_dir.resolve()), stem) in used:
                stem, k2 = f"{clip.parent.name}__{clip.stem}_{k2}", k2 + 1
            findings.append(ac.Finding("info", "P8-out-renamed",
                                       f"输出目录里已有同名镜 {clip.stem}：本镜输出改名为 {stem}.contact.jpg（防覆盖）；"
                                       f"建议每集/每目录分别指定 --out-dir", str(clip)))
        used.add((str(out_dir.resolve()), stem))
        fs, rec = contact_one(clip, out_dir, a.frames, a.cols, a.tile_width,
                              a.tail, kf, crops, not a.no_drawtext, a.aspect_tol, stem=stem)
        findings += fs
        records.append(rec)
    summary = f"共 {len(clips)} 个视频；接触表 {sum(1 for r in records if r.get('contact_sheet'))} 张"
    rc = ac.emit(TITLE, findings, a.json, {"clips": records, "summary": summary})
    return 2 if any(f.code == "P8-render-failed" for f in findings) else rc


if __name__ == "__main__":
    sys.exit(main())
