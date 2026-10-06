#!/usr/bin/env python3
"""loudness_verify.py — 成片技术验收（verify）：响度 / 真峰 / LRA / 画幅 / 时长 / 音视频流 / 黑场 / 冻结 / 坏帧

用途：
  T-3 后期链最后一步 verify 的可执行版本：一遍 ffmpeg 解码同时跑 ebur128（无则 loudnorm）、blackdetect、
  freezedetect，并收集解码器报错（坏帧），输出一张可直接贴进「成片报告」的 verify 表。
  目标值：整体响度 --lufs -16（±--lufs-tol 1.0，T-4 委托方交付值），真峰 ≤ --tp-max -1.0 dBTP，
  画幅 9:16（±--aspect-tol 1%，error），有视频流、有音频流；--min/--max 给了才查时长
  （T-4 的单集 90–110s 是示例，不是默认值）；黑场 ≥0.5s → warn（--allow-black 表示设计淡入淡出 → info），
  冻结 → warn。LRA 只报告（--lra-max 给了才告警）。
  只报告事实与改法，不判断"好不好看"——技术全绿 ≠ 可发布（F1/F2：数字达标 ≠ 观感达标）。

溯源：T-3（后期链：剪辑单 → 渲染 → verify：时长/响度/真峰/坏帧）、
      T-4（交付现状：响度 -16 LUFS、无坏帧；单集约 90–110 秒，竖屏 9:16）、
      T-2（竖屏 9:16）、F2（数字达标 ≠ 观感达标：本表全绿只是下限）。

输入格式：成片视频文件（.mp4 .mov .mkv .webm .m4v .avi）或含成片的目录。
  成片与剪辑单 / 成片报告的关系见 70-playbooks/format-contracts.md §4（剪辑单）与 §6（验收记录写法）。

判定：
  error T3-no-video       没有视频流
  error T3-aspect         画幅偏离 9:16 超过 --aspect-tol（默认 1%）
  error T3-no-audio       没有音频流
  error T4-lufs           整体响度超出 目标 ±容差
  error T4-true-peak      真峰 > --tp-max
  error T4-duration       时长超出 --min/--max
  error T3-decode-error   解码/解封装报错（坏帧、坏包）
  error T3-unreadable     文件无法探测
  warn  T3-black          黑场 ≥ --black-min 秒（--allow-black 时降为 info T3-black-designed）
  warn  T3-freeze         冻结段（freezedetect，≥ --freeze-sec 秒）
  warn  T3-av-duration    音视频流时长相差 > 0.2s
  warn  T4-lra            LRA > --lra-max（仅在给出 --lra-max 时）
  warn  T3-no-meter       ffmpeg 缺 blackdetect / freezedetect，对应项未检
  info  T3-verify         逐项实测值（verify 表见报告末尾 / JSON 的 verify 字段）
  warn  P8-no-clips       目录中没有视频文件

用法示例：
  python3 loudness_verify.py final/ep03.mp4
  python3 loudness_verify.py final/ep03.mp4 --min 90 --max 110          # 按 T-4 单集规格查时长
  python3 loudness_verify.py final/ep03.mp4 --allow-black --json        # 片头片尾有设计淡入淡出
  python3 loudness_verify.py final/ --lufs -14 --lufs-tol 1 --tp-max -1.0
  python3 loudness_verify.py --selftest

退出码：0 通过（无 error）/ 1 发现 error / 2 用法或环境错误（缺 ffmpeg 或缺 ebur128+loudnorm、路径不存在）。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "成片技术验收 verify（T-3 / T-4）"
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
ASPECT_9_16 = 9 / 16
DECODE_ERR = re.compile(r"corrupt|error while decoding|concealing|error submitting packet|invalid data found|"
                        r"invalid nal|non-existing pps|missing picture|decode_slice_header error|"
                        r"left block unavailable|out of range intra", re.I)
OWN_FILTERS = re.compile(r"^\[(Parsed_|blackdetect|freezedetect|ebur128|loudnorm|out#|vost#|AVFilterGraph|graph )", re.I)


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


def need_ffmpeg():
    missing = [t for t in ("ffmpeg", "ffprobe") if not ac.have(t)]
    if missing:
        ac.die(f"找不到 {' / '.join(missing)}：安装 ffmpeg（含 ffprobe）并加入 PATH 后重跑")
    if not ({"ebur128", "loudnorm"} & ff_filters()):
        ac.die("ffmpeg 既没有 ebur128 也没有 loudnorm 滤镜，无法测响度：换用完整版 ffmpeg")


def _ratio(s, default: float = 0.0) -> float:
    try:
        s = str(s).replace(":", "/")
        if "/" in s:
            a, b = s.split("/", 1)
            return float(a) / float(b) if float(b) else default
        return float(s)
    except (TypeError, ValueError):
        return default


def probe_all(path: Path) -> dict:
    info = ac.ffprobe_json(path)
    fmt_dur = float(info.get("format", {}).get("duration") or 0.0)
    vs = [s for s in info.get("streams", []) if s.get("codec_type") == "video"
          and not s.get("disposition", {}).get("attached_pic")]
    aus = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
    out: dict = {"duration": round(fmt_dur, 3), "video": None, "audio": None}
    if vs:
        v = vs[0]
        w, h = int(v.get("width") or 0), int(v.get("height") or 0)
        rot = v.get("tags", {}).get("rotate")
        for sd in v.get("side_data_list", []) or []:
            rot = sd.get("rotation", rot)
        try:
            rot = int(round(float(rot))) % 360 if rot is not None else 0
        except (TypeError, ValueError):
            rot = 0
        if rot in (90, 270):
            w, h = h, w
        sar = _ratio(v.get("sample_aspect_ratio", "1:1"), 1.0) or 1.0
        out["video"] = {"codec": v.get("codec_name", ""), "width": w, "height": h, "sar": round(sar, 4),
                        "dar": round(w * sar / h, 4) if h else 0.0, "rotation": rot,
                        "fps": round(_ratio(v.get("avg_frame_rate", "0/0")) or _ratio(v.get("r_frame_rate", "0/0")), 3),
                        "duration": round(float(v.get("duration") or fmt_dur), 3)}
    if aus:
        a = aus[0]
        out["audio"] = {"codec": a.get("codec_name", ""), "sample_rate": int(a.get("sample_rate") or 0),
                        "channels": int(a.get("channels") or 0),
                        "duration": round(float(a.get("duration") or fmt_dur), 3)}
    return out


def _num(s: str) -> float:
    s = s.strip().lower()
    if s in ("-inf", "inf", "nan"):
        return float("-inf") if s.startswith("-") else float("nan")
    return float(s)


def parse_ebur128(log: str) -> dict:
    tail = log[log.rfind("Summary:"):] if "Summary:" in log else ""
    out = {}
    for key, rx in (("I", r"I:\s+(-?inf|-?\d+(?:\.\d+)?)\s+LUFS"), ("LRA", r"LRA:\s+(-?\d+(?:\.\d+)?)\s+LU\b"),
                    ("TP", r"Peak:\s+(-?inf|-?\d+(?:\.\d+)?)\s+dBFS")):
        m = re.search(rx, tail)
        if m:
            out[key] = _num(m.group(1))
    return out


def parse_loudnorm(log: str) -> dict:
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", log, re.S)
    if not m:
        return {}
    try:
        j = json.loads(m.group(0))
        return {"I": _num(j["input_i"]), "TP": _num(j["input_tp"]), "LRA": _num(j["input_lra"])}
    except (ValueError, KeyError):
        return {}


def parse_black(log: str) -> list[dict]:
    return [{"start": float(a), "end": float(b), "duration": float(c)} for a, b, c in
            re.findall(r"black_start:\s*([\d.]+)\s+black_end:\s*([\d.]+)\s+black_duration:\s*([\d.]+)", log)]


def parse_freeze(log: str, duration: float) -> list[dict]:
    out, cur = [], None
    for key, val in re.findall(r"lavfi\.freezedetect\.freeze_(start|duration|end):\s*([\d.]+)", log):
        v = float(val)
        if key == "start":
            cur = {"start": v}
            out.append(cur)
        elif cur is not None:
            cur[key] = v
    for f in out:
        f.setdefault("end", duration)
        f.setdefault("duration", round(f["end"] - f["start"], 3))
    return out


def decode_errors(log: str) -> list[str]:
    return [ln.strip() for ln in log.splitlines()
            if ln.startswith("[") and not OWN_FILTERS.match(ln) and DECODE_ERR.search(ln)]


def measure(path: Path, has_v: bool, has_a: bool, black_min: float, black_pix: float, freeze_sec: float,
            freeze_noise: str, duration: float) -> dict:
    flt = ff_filters()
    parts, maps, notes = [], [], []
    if has_v:
        vchain = []
        if "blackdetect" in flt:
            vchain.append(f"blackdetect=d={black_min}:pix_th={black_pix}")
        else:
            notes.append("blackdetect")
        if "freezedetect" in flt:
            vchain.append(f"freezedetect=n={freeze_noise}:d={freeze_sec}")
        else:
            notes.append("freezedetect")
        parts.append(f"[0:v:0]{','.join(vchain) or 'null'}[vout]")
        maps += ["-map", "[vout]"]
    meter = None
    if has_a:
        meter = "ebur128" if "ebur128" in flt else "loudnorm"
        achain = ("ebur128=peak=true:framelog=verbose" if meter == "ebur128"
                  else "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json")
        parts.append(f"[0:a:0]{achain}[aout]")
        maps += ["-map", "[aout]"]
    if not parts:
        return {"notes": notes, "log": ""}

    def go(fc: str) -> subprocess.CompletedProcess:
        return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-filter_complex", fc] + maps
                              + ["-f", "null", "-"], capture_output=True, text=True, errors="replace", timeout=3600)
    fc = ";".join(parts)
    p = go(fc)
    if p.returncode != 0 and "framelog" in p.stderr:          # 旧版 ebur128 没有 framelog 选项
        p = go(fc.replace(":framelog=verbose", ""))
    log = p.stderr
    loud = (parse_ebur128(log) if meter == "ebur128" else parse_loudnorm(log)) if meter else {}
    return {"meter": meter, "loud": loud, "black": parse_black(log), "freeze": parse_freeze(log, duration),
            "decode_errors": decode_errors(log), "notes": notes, "rc": p.returncode,
            "tail": "\n".join(log.strip().splitlines()[-3:])}


# ------------------------------------------------------------------ 判定

def _fmt(x: float | None, unit: str = "") -> str:
    if x is None:
        return "—"
    if isinstance(x, float) and math.isinf(x):
        return f"-inf{unit}"
    return f"{x:.1f}{unit}"


def verify(path: Path, o: argparse.Namespace) -> tuple[list[ac.Finding], dict]:
    where = path.name
    fs: list[ac.Finding] = []
    rows: list[list[str]] = []
    try:
        pr = probe_all(path)
    except Exception as e:  # noqa: BLE001
        return [ac.Finding("error", "T3-unreadable", f"无法探测：{str(e)[:200]}——重新渲染/导出成片后再 verify",
                           where)], {"file": str(path)}
    v, a, dur = pr["video"], pr["audio"], pr["duration"]

    # 视频流 + 画幅
    if v is None:
        fs.append(ac.Finding("error", "T3-no-video", "没有视频流：检查渲染命令的 -map / 输出容器", where))
        rows.append(["视频流", "无", "必须有", "不通过"])
        rows.append(["画幅", "—", "9:16", "不通过"])
    else:
        rows.append(["视频流", f"{v['codec']} {v['width']}×{v['height']} {v['fps']:g}fps", "必须有", "通过"])
        dev = abs(v["dar"] / ASPECT_9_16 - 1) if v["dar"] else 1.0
        ok = dev <= o.aspect_tol
        rows.append(["画幅", f"DAR {v['dar']}（偏差 {dev:.1%}）", f"9:16 ±{o.aspect_tol:.0%}", "通过" if ok else "不通过"])
        if not ok:
            fs.append(ac.Finding("error", "T3-aspect",
                                 f"画幅 {v['width']}×{v['height']}（DAR {v['dar']}）偏离 9:16 {dev:.1%} > {o.aspect_tol:.0%}："
                                 f"重新导出为 1080×1920 或 720×1280（scale+pad/crop，不要拉伸）"
                                 + ("；注：T-1 剪辑尺寸 480×864 实为 5:9（偏 1.2%）" if (v["width"], v["height"]) == (480, 864)
                                    else ""), where, {"dar": v["dar"], "deviation": round(dev, 4)}))

    # 时长
    lim = []
    if o.min is not None:
        lim.append(f"≥{o.min:g}s")
    if o.max is not None:
        lim.append(f"≤{o.max:g}s")
    d_ok = (o.min is None or dur >= o.min) and (o.max is None or dur <= o.max)
    rows.append(["时长", f"{dur:.2f}s", " ".join(lim) or "（未指定）", ("通过" if d_ok else "不通过") if lim else "—"])
    if not d_ok:
        fs.append(ac.Finding("error", "T4-duration",
                             f"时长 {dur:.2f}s 超出 {' '.join(lim)}：回剪辑单增删 CUT 或调整入出点后重渲（时长差 "
                             f"{(o.min - dur) if (o.min is not None and dur < o.min) else (dur - o.max):.2f}s）", where))

    # 音频流
    if a is None:
        fs.append(ac.Finding("error", "T3-no-audio", "没有音频流：检查渲染命令是否丢了音轨（-map 0:a / 混音输出）", where))
        rows.append(["音频流", "无", "必须有", "不通过"])
    else:
        rows.append(["音频流", f"{a['codec']} {a['sample_rate']}Hz {a['channels']}ch", "必须有", "通过"])

    m = measure(path, v is not None, a is not None, o.black_min, o.black_pix, o.freeze_sec, o.freeze_noise,
                v["duration"] if v else dur)
    if m.get("notes"):
        fs.append(ac.Finding("warn", "T3-no-meter", f"ffmpeg 缺 {' / '.join(m['notes'])} 滤镜，对应项未检：换完整版 ffmpeg 后重跑",
                             where))
    loud = m.get("loud", {})
    if a is not None:
        I, TP, LRA = loud.get("I"), loud.get("TP"), loud.get("LRA")
        if I is None:
            fs.append(ac.Finding("error", "T4-lufs", f"响度测量失败（{m.get('meter')}）：{m.get('tail', '')[:200]}", where))
            rows.append(["整体响度", "测量失败", f"{o.lufs:g}±{o.lufs_tol:g} LUFS", "不通过"])
        else:
            okI = not math.isinf(I) and abs(I - o.lufs) <= o.lufs_tol
            rows.append(["整体响度", _fmt(I, " LUFS"), f"{o.lufs:g}±{o.lufs_tol:g} LUFS", "通过" if okI else "不通过"])
            if not okI:
                norm = f"用 loudnorm 两遍法归一（I={o.lufs:g}:TP={min(o.tp_max - 0.5, -1.5):g}:LRA=11）后重导出"
                if a["duration"] < 0.4:
                    why = (f"音频只有 {a['duration']:.2f}s，短于 BS.1770 积分响度的 0.4s 测量块，读数无意义："
                           f"检查渲染是否把音轨截断（-shortest / 入出点），修好后复测")
                elif math.isinf(I) or I <= -69.5:     # -70 LUFS = ebur128 绝对门限：门限以下全被丢弃
                    why = ("音轨静音或近静音（-70 LUFS 是 BS.1770 绝对门限）：先查混音是否丢轨/被静音（对白、音效、配乐"
                           "是否都在，-map 0:a 是否选对音轨），不要直接加几十 dB 增益；音轨修好后再" + norm)
                else:
                    why = f"需 {o.lufs - I:+.1f} dB；" + norm
                fs.append(ac.Finding("error", "T4-lufs", f"整体响度 {_fmt(I, ' LUFS')}，目标 {o.lufs:g}±{o.lufs_tol:g}：{why}",
                                     where, {"I": None if math.isinf(I) else I}))
        if TP is not None:
            okT = math.isinf(TP) or TP <= o.tp_max
            rows.append(["真峰", _fmt(TP, " dBTP"), f"≤{o.tp_max:g} dBTP", "通过" if okT else "不通过"])
            if not okT:
                fs.append(ac.Finding("error", "T4-true-peak",
                                     f"真峰 {TP:.1f} dBTP > {o.tp_max:g}：归一时设 TP={min(o.tp_max - 0.5, -1.5):g} 或在母线加真峰限幅后"
                                     f"重导出（有损编码可能再抬高真峰，留余量后复测）", where, {"TP": TP}))
        if LRA is not None:
            okL = o.lra_max is None or LRA <= o.lra_max
            rows.append(["响度范围 LRA", _fmt(LRA, " LU"), f"≤{o.lra_max:g} LU" if o.lra_max is not None else "（仅报告）",
                         ("通过" if okL else "注意") if o.lra_max is not None else "—"])
            if not okL:
                fs.append(ac.Finding("warn", "T4-lra", f"LRA {LRA:.1f} LU > {o.lra_max:g}：对白段与动作段响度差过大，"
                                                       f"检查混音动态（压缩/对白提升）", where))
    else:
        rows.append(["整体响度", "—（无音频）", f"{o.lufs:g}±{o.lufs_tol:g} LUFS", "不通过"])

    # 黑场 / 冻结
    blacks = [b for b in m.get("black", []) if b["duration"] >= o.black_min - 1e-6]
    if v is not None and "blackdetect" not in m.get("notes", []):
        rows.append(["黑场", f"{len(blacks)} 段 / 共 {sum(b['duration'] for b in blacks):.2f}s",
                     f"无 ≥{o.black_min:g}s 黑场" + ("（允许设计黑场）" if o.allow_black else ""),
                     "通过" if not blacks else ("注意" if not o.allow_black else "设计")])
    for b in blacks:
        w = f"{where} @ {b['start']:.2f}s"
        if o.allow_black:
            fs.append(ac.Finding("info", "T3-black-designed", f"黑场 {b['start']:.2f}–{b['end']:.2f}s（{b['duration']:.2f}s），"
                                                              f"按 --allow-black 视为设计淡入淡出", w, b))
        else:
            fs.append(ac.Finding("warn", "T3-black",
                                 f"黑场 {b['start']:.2f}–{b['end']:.2f}s（{b['duration']:.2f}s）：若是设计淡入淡出/片尾黑卡，加 "
                                 f"--allow-black 重跑；否则回剪辑单查空档或丢失素材（asset_exists.py 复查来源）", w, b))
    freezes = m.get("freeze", [])
    if v is not None and "freezedetect" not in m.get("notes", []):
        rows.append(["冻结", f"{len(freezes)} 段 / 共 {sum(f['duration'] for f in freezes):.2f}s", f"无 ≥{o.freeze_sec:g}s 冻结",
                     "通过" if not freezes else "注意"])
    for f in freezes:
        inblack = any(b["start"] - 0.1 <= f["start"] and f["end"] <= b["end"] + 0.2 for b in m.get("black", []))
        fs.append(ac.Finding("info" if (inblack and o.allow_black) else "warn", "T3-freeze",
                             f"冻结 {f['start']:.2f}–{f['end']:.2f}s（{f['duration']:.2f}s）"
                             + ("，与黑场重合" if inblack else "")
                             + "：若非设计定格/字卡，用 psnr_scan.py --mode final 定位到镜后重出或剪掉",
                             f"{where} @ {f['start']:.2f}s", f))

    # 坏帧 / 音画时长
    errs = m.get("decode_errors", [])
    rows.append(["坏帧/解码报错", f"{len(errs)} 条", "0 条", "通过" if not errs else "不通过"])
    if errs:
        fs.append(ac.Finding("error", "T3-decode-error",
                             f"解码/解封装报错 {len(errs)} 条（例：{errs[0][:120]}）：重新渲染成片；若来源镜本身损坏，"
                             f"先用 contact_sheet.py / psnr_scan.py 定位并替换该镜", where, {"sample": errs[:5]}))
    if v is not None and a is not None and abs(v["duration"] - a["duration"]) > 0.2:
        fs.append(ac.Finding("warn", "T3-av-duration",
                             f"视频 {v['duration']:.2f}s 与音频 {a['duration']:.2f}s 相差 {abs(v['duration'] - a['duration']):.2f}s："
                             f"检查尾部是否有无声画面/无画声音（渲染加 -shortest 或补齐）", where))
    nfail = sum(1 for r in rows if r[3] == "不通过")
    fs.append(ac.Finding("info", "T3-verify", f"verify 表 {len(rows)} 项，不通过 {nfail} 项（表见报告末尾）", where,
                         {"rows": rows}))
    for f in fs:          # 严格 JSON：±inf / nan 一律写 null（json.dumps 默认会输出非标准的 -Infinity）
        f.data = {k: (None if isinstance(x, float) and (math.isinf(x) or math.isnan(x)) else x) for k, x in f.data.items()}
    rec = {"file": str(path), "probe": pr, "loudness": {k: (None if (isinstance(x, float) and (math.isinf(x) or math.isnan(x)))
                                                              else x) for k, x in loud.items()},
           "meter": m.get("meter"), "black": m.get("black", []), "freeze": freezes, "decode_errors": errs[:20],
           "verify": [dict(zip(["项目", "实测", "目标", "结果"], r)) for r in rows]}
    return fs, rec


def table_md(rec: dict) -> str:
    if not rec.get("verify"):
        return ""
    lines = [f"verify：{rec['file']}", "| 项目 | 实测 | 目标 | 结果 |", "|---|---|---|---|"]
    lines += [f"| {r['项目']} | {r['实测']} | {r['目标']} | {r['结果']} |" for r in rec["verify"]]
    lines.append("（技术全绿只是下限，不等于可发布：F2）")
    return "\n".join(lines)


def collect(paths: list[str], recursive: bool) -> tuple[list[Path], list[ac.Finding]]:
    files, fs = [], []
    for s in paths:
        p = Path(s)
        if not p.exists():
            ac.die(f"找不到路径：{s}")
        if p.is_dir():
            it = p.rglob("*") if recursive else p.iterdir()
            found = sorted(q for q in it if q.is_file() and q.suffix.lower() in VIDEO_EXTS)
            if not found:
                fs.append(ac.Finding("warn", "P8-no-clips", "目录中没有视频文件：确认成片路径，或加 --recursive", str(p)))
            files += found
        else:
            files.append(p)
    return files, fs


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", help="成片文件或目录")
    ap.add_argument("--lufs", type=float, default=-16.0, help="整体响度目标 LUFS（默认 -16，T-4）")
    ap.add_argument("--lufs-tol", type=float, default=1.0, help="响度容差 LU（默认 1.0）")
    ap.add_argument("--tp-max", type=float, default=-1.0, help="真峰上限 dBTP（默认 -1.0）")
    ap.add_argument("--lra-max", type=float, help="LRA 上限 LU（给了才告警）")
    ap.add_argument("--aspect-tol", type=float, default=0.01, help="画幅偏离 9:16 的容差（默认 0.01 = 1%%）")
    ap.add_argument("--min", type=float, help="最短时长秒（T-4 单集示例 90）")
    ap.add_argument("--max", type=float, help="最长时长秒（T-4 单集示例 110）")
    ap.add_argument("--allow-black", action="store_true", help="黑场为设计淡入淡出/片尾黑卡：降为 info")
    ap.add_argument("--black-min", type=float, default=0.5, help="黑场最短时长秒（默认 0.5）")
    ap.add_argument("--black-pix", type=float, default=0.10, help="blackdetect pix_th（默认 0.10）")
    ap.add_argument("--freeze-sec", type=float, default=1.0, help="冻结最短时长秒（默认 1.0）")
    ap.add_argument("--freeze-noise", default="-60dB", help="freezedetect 噪声阈值（默认 -60dB）")
    ap.add_argument("--recursive", action="store_true", help="目录输入时递归查找")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON（含 verify 表）")
    ap.add_argument("--selftest", action="store_true", help="运行自测（ffmpeg lavfi 合成素材），全部通过退出 0")
    return ap


# ------------------------------------------------------------------ 自测

def _synth(args: list[str], out: Path) -> Path:
    p = ac.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + args + [str(out)])
    if p.returncode != 0:
        raise RuntimeError(f"合成失败：{p.stderr.strip()[-300:]}")
    return out


def selftest() -> int:
    need_ffmpeg()
    results: list[tuple[bool, str]] = []

    def check(cond, label):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    enc = ac.run(["ffmpeg", "-hide_banner", "-encoders"]).stdout
    venc = (["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23"] if "libx264" in enc
            else ["-c:v", "mpeg4", "-q:v", "4", "-pix_fmt", "yuv420p"])
    aenc = ["-c:a", "aac", "-b:a", "192k"]
    # sine 源振幅固定 1/8（-18.06 dBFS 峰值）；1 kHz 双声道同相正弦：LUFS = 峰值 dBFS（BS.1770 K 加权在 1 kHz 约 +0.69 dB，
    # 正好抵消 -0.691 常数；单声道 0 dBFS 正弦 = -3.01 LUFS，双声道再 +3.01）。→ 加 2.04 dB 得 -16.0 LUFS。
    gain = -16.0 - 20 * math.log10(1 / 8)

    def av(name: str, size: str = "270x480", g: float = gain, vsrc: str | None = None, extra_a: str = "",
           d: float = 4.0) -> Path:
        v = vsrc or f"testsrc2=s={size}:r=24:d={d}"
        return _synth(["-f", "lavfi", "-i", v, "-f", "lavfi", "-i", f"sine=f=1000:sample_rate=48000:d={d}",
                       "-filter_complex", f"[1:a]pan=stereo|c0=c0|c1=c0,volume={g:.4f}dB{extra_a}[a]",
                       "-map", "0:v", "-map", "[a]"] + venc + aenc + ["-shortest"], td / name)

    def run_v(path: Path, *args: str):
        o = build_parser().parse_args([str(path), *args])
        return verify(path, o)

    with tempfile.TemporaryDirectory(prefix="verify_selftest_") as tds:
        td = Path(tds)
        good = av("good.mp4")
        fs, rec = run_v(good)
        I = rec["loudness"].get("I")
        check(I is not None and abs(I - (-16.0)) <= 0.5,
              f"9:16 testsrc2 + 1kHz 正弦（理论 -16.0 LUFS）实测 {I} LUFS（±0.5 内）")
        TP = rec["loudness"].get("TP")
        check(TP is not None and -16.8 <= TP <= -14.5, f"真峰实测 {TP} dBTP ≈ 正弦峰值 -16 dBFS")
        check(not [f for f in fs if f.level == "error"], "合格成片 → 0 error")
        check(all(r["结果"] in ("通过", "—") for r in rec["verify"]) and len(rec["verify"]) >= 8,
              f"verify 表 {len(rec['verify'])} 项全部通过")

        wide = av("wide.mp4", size="480x270")
        fs, _ = run_v(wide)
        check(any(f.code == "T3-aspect" and f.level == "error" for f in fs), "16:9 文件 → error T3-aspect")
        t1 = av("t1.mp4", size="480x864")
        fs, _ = run_v(t1)
        check(any(f.code == "T3-aspect" and "5:9" in f.msg for f in fs), "480×864（T-1 剪辑尺寸，偏 1.2%）按默认 1% → error 并注明")
        fs, _ = run_v(t1, "--aspect-tol", "0.015")
        check(not any(f.code == "T3-aspect" for f in fs), "显式 --aspect-tol 0.015 → 放行 480×864")

        loud = av("loud.mp4", g=gain + 8)
        fs, rec = run_v(loud)
        check(any(f.code == "T4-lufs" and f.level == "error" and "-8" in f.msg for f in fs),
              f"+8 dB（约 -8 LUFS，实测 {rec['loudness'].get('I')}）→ error T4-lufs，给出增益")
        burst = "0.9*sin(2*PI*1000*t)*lt(mod(t\\,1)\\,0.002)"      # 每秒 2 ms 满幅猝发：真峰超标、响度几乎不变
        peaky = av("peaky.mp4", extra_a=f",aeval='val(0)+{burst}|val(1)+{burst}':c=same")
        fs, rec = run_v(peaky)
        check(any(f.code == "T4-true-peak" for f in fs) and not any(f.code == "T4-lufs" for f in fs),
              f"-16 LUFS + 每秒 2ms 猝发 → 只报 error T4-true-peak（TP {rec['loudness'].get('TP')}，I {rec['loudness'].get('I')}）")

        silent = _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24:d=3", "-f", "lavfi", "-i",
                         "anullsrc=r=48000:cl=stereo", "-t", "3"] + venc + aenc, td / "成片 %d 静音.mp4")
        fs, rec = run_v(silent)
        lf = [f for f in fs if f.code == "T4-lufs"]
        check(lf and "静音" in lf[0].msg and "+54" not in lf[0].msg,
              "静音音轨（-70 LUFS 门限）→ error T4-lufs 提示查丢轨/静音，不给 +54 dB 增益（回归）；路径含 % 中文空格")
        global _FILTERS
        real_f = ff_filters()
        try:
            _FILTERS = set(real_f) - {"ebur128"}
            fs, rec = run_v(silent)
            check(rec["meter"] == "loudnorm" and any(f.code == "T4-lufs" for f in fs)
                  and json.loads(json.dumps([f.data for f in fs] + [rec["loudness"]]),
                                 parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c))) is not None,
                  "无 ebur128 → loudnorm 兜底；静音读数 -inf 在 JSON 里写 null（回归：曾输出非标准 -Infinity）")
            fs, rec = run_v(good)
            check(rec["meter"] == "loudnorm" and abs((rec["loudness"].get("I") or 0) + 16.0) <= 0.5
                  and not [f for f in fs if f.level == "error"], f"loudnorm 兜底测合格成片 → {rec['loudness'].get('I')} LUFS，0 error")
            _FILTERS = set(real_f) - {"blackdetect", "freezedetect"}
            fs, rec = run_v(good)
            check(any(f.code == "T3-no-meter" and f.level == "warn" for f in fs) and not [f for f in fs if f.level == "error"],
                  "缺 blackdetect/freezedetect → warn T3-no-meter，其余照测")
        finally:
            _FILTERS = real_f

        noa = _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24:d=2"] + venc, td / "noaudio.mp4")
        fs, rec = run_v(noa)
        check(any(f.code == "T3-no-audio" for f in fs), "无音轨 → error T3-no-audio")
        aonly = _synth(["-f", "lavfi", "-i", "sine=f=1000:d=2", "-c:a", "aac"], td / "audio.m4a")
        fs, _ = run_v(aonly)
        check(any(f.code == "T3-no-video" for f in fs), "无视频流 → error T3-no-video")

        blk = av("black.mp4", vsrc="color=c=black:s=270x480:r=24:d=1[k];testsrc2=s=270x480:r=24:d=3[t];[k][t]concat=n=2:v=1:a=0")
        fs, _ = run_v(blk)
        check(any(f.code == "T3-black" and f.level == "warn" for f in fs), "片头 1s 黑场 → warn T3-black")
        fs, _ = run_v(blk, "--allow-black")
        check(any(f.code == "T3-black-designed" and f.level == "info" for f in fs) and not any(f.code == "T3-black" for f in fs),
              "--allow-black → info T3-black-designed")
        frz = av("freeze.mp4", vsrc="testsrc2=s=270x480:r=24:d=2.5,tpad=stop_mode=clone:stop_duration=1.5")
        fs, _ = run_v(frz)
        fz = [f for f in fs if f.code == "T3-freeze"]
        check(fz and fz[0].level == "warn" and abs(fz[0].data["start"] - 2.5) <= 0.2, "尾部 1.5s 定格 → warn T3-freeze ≈2.5s 起")
        fs, _ = run_v(good, "--min", "5", "--max", "110")
        check(any(f.code == "T4-duration" and f.level == "error" for f in fs), "4s 文件配 --min 5 → error T4-duration")

        ts = td / "c.ts"
        _synth(["-f", "lavfi", "-i", "testsrc2=s=270x480:r=24:d=4", "-f", "lavfi", "-i", "sine=f=1000:d=4"]
               + venc + ["-c:a", "aac", "-f", "mpegts"], ts)
        b = bytearray(ts.read_bytes())
        for k in range(40):
            off = int(len(b) * 0.4) + k * 997
            b[off:off + 16] = bytes((k * 37 + j * 11) % 256 for j in range(16))
        bad = td / "corrupt.ts"
        bad.write_bytes(bytes(b))
        fs, _ = run_v(bad)
        check(any(f.code == "T3-decode-error" and f.level == "error" for f in fs), "损坏的 TS → error T3-decode-error（坏帧）")
        check(not decode_errors("[Parsed_ebur128_0 @ 0x1] Summary:\n[blackdetect @ 0x2] black_start:0\n"),
              "自家滤镜日志不算解码报错")
        check(parse_freeze("lavfi.freezedetect.freeze_start: 2\n", 4.0) == [{"start": 2.0, "end": 4.0, "duration": 2.0}],
              "冻结持续到片尾（无 freeze_end）→ 以片长收尾")

        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + [str(good), "--json"], capture_output=True, text=True)
        ok = False
        try:
            j = json.loads(r.stdout)
            ok = j["ok"] is True and j["files"][0]["verify"][0]["项目"] == "视频流"
        except Exception:
            pass
        check(r.returncode == 0 and ok, "CLI 合格成片 --json → 退出码 0，含 verify 表")
        r = subprocess.run(me + [str(good)], capture_output=True, text=True)
        check(r.returncode == 0 and "| 整体响度 |" in r.stdout, "CLI 人类报告含 Markdown verify 表")
        r = subprocess.run(me + [str(wide)], capture_output=True, text=True)
        check(r.returncode == 1 and "T3-aspect" in r.stdout, "CLI 16:9 → 退出码 1")
        for fx in ("good", "bad"):
            r = subprocess.run(me + [str(ac.FIXTURES / fx)], capture_output=True, text=True)
            check(r.returncode == 0 and "P8-no-clips" in r.stdout, f"CLI fixtures/{fx}（无视频）→ 0 error")
        r = subprocess.run(me + [str(ac.FIXTURES / "good")], capture_output=True,
                           env=dict(os.environ, PYTHONIOENCODING="gbk"))
        check(r.returncode == 0 and b"Traceback" not in r.stderr,
              "stdout 为 GBK（Windows cmd 重定向，E3-1）→ 报告照出，不因 ⚠️ 等图标崩溃（回归）")
        r = subprocess.run(me + [str(td / "nope.mp4")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 路径不存在 → 退出码 2")
        r = subprocess.run(me + [str(good), "--min", "10", "--max", "5"], capture_output=True, text=True)
        check(r.returncode == 2, "CLI --min > --max → 退出码 2")

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
    ap = build_parser()
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.inputs:
        ap.print_usage(sys.stderr)
        ac.die("需要成片文件或目录（或 --selftest）")
    need_ffmpeg()
    if a.min is not None and a.max is not None and a.min > a.max:
        ac.die("--min 不能大于 --max")
    if a.lufs_tol < 0 or a.aspect_tol < 0 or a.black_min <= 0 or a.freeze_sec <= 0:
        ac.die("--lufs-tol / --aspect-tol 不能为负，--black-min / --freeze-sec 必须 > 0")
    files, findings = collect(a.inputs, a.recursive)
    recs = []
    for f in files:
        fs, rec = verify(f, a)
        findings += fs
        recs.append(rec)
    summary = "\n\n".join(t for t in (table_md(r) for r in recs) if t)
    return ac.emit(TITLE, findings, a.json, {"files": recs, "summary": summary})


if __name__ == "__main__":
    sys.exit(main())
