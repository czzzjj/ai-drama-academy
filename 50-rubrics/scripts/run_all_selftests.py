#!/usr/bin/env python3
"""run_all_selftests.py — 汇总运行 50-rubrics/scripts/ 下全部检查脚本的 --selftest（CONVENTIONS §8.6，CI 跑它）

用途：
  自动发现本目录下除 academy_common.py 与本文件之外的每个 *.py，逐个运行 `python3 <script> --selftest`
  （每个脚本有超时，默认 300s），打印汇总表（脚本 / PASS·FAIL·SKIP / 秒），任一 FAIL → 退出码 1。
  媒体类脚本（源码里定义了 need_ffmpeg()：它们的自测要用 ffmpeg lavfi 合成素材）：
    - 找不到 ffmpeg/ffprobe → 记 SKIP 并写明原因（绝不静默跳过）；
    - --quick → 主动跳过媒体类，记 SKIP「--quick」，报告末尾再说一遍跳过了哪些。
  脚本只报告自测事实，不改任何文件。

溯源：CONVENTIONS.md §8（脚本公约：每个脚本必须支持 --selftest，退出码 0 = 通过；run_all_selftests.py 汇总）、
      E3（环境怪癖：缺依赖必须明确报告降级，不得静默）。

输入格式：无（扫描本文件所在目录）。

用法示例：
  python3 50-rubrics/scripts/run_all_selftests.py
  python3 50-rubrics/scripts/run_all_selftests.py --quick              # 跳过 ffmpeg 媒体类自测（并明确列出）
  python3 50-rubrics/scripts/run_all_selftests.py --json --timeout 600
  python3 50-rubrics/scripts/run_all_selftests.py --only prompt_lint dialogue_capacity
  python3 50-rubrics/scripts/run_all_selftests.py --selftest           # 只测本汇总器自身

退出码：0 全部 PASS/SKIP / 1 有 FAIL（含超时）/ 2 用法或环境错误。
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDE = {"academy_common.py", Path(__file__).name}
RE_MEDIA = re.compile(r"^def need_ffmpeg\(", re.M)


def discover(only: list[str] | None = None) -> list[Path]:
    out = sorted(p for p in HERE.glob("*.py") if p.name not in EXCLUDE)
    if only:
        want = {o[:-3] if o.endswith(".py") else o for o in only}
        out = [p for p in out if p.stem in want]
    return out


def is_media(path: Path) -> bool:
    try:
        return bool(RE_MEDIA.search(path.read_text(encoding="utf-8-sig", errors="replace")))
    except OSError:
        return False


def run_one(path: Path, timeout: int) -> dict:
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-B", str(path), "--selftest"], capture_output=True, text=True,
                           errors="replace", timeout=timeout, cwd=str(HERE))
        status = "PASS" if p.returncode == 0 else "FAIL"
        tail = (p.stdout + p.stderr).strip().splitlines()[-12:]
        reason = "" if status == "PASS" else f"退出码 {p.returncode}"
    except subprocess.TimeoutExpired:
        status, tail, reason = "FAIL", [], f"超时（>{timeout}s）"
    return {"script": path.name, "status": status, "seconds": round(time.monotonic() - t0, 1), "reason": reason,
            "tail": tail if status == "FAIL" else []}


def run_all(timeout: int = 300, quick: bool = False, only: list[str] | None = None) -> list[dict]:
    have_ff = bool(shutil.which("ffmpeg")) and bool(shutil.which("ffprobe"))
    rows = []
    for p in discover(only):
        media = is_media(p)
        if media and quick:
            rows.append({"script": p.name, "status": "SKIP", "seconds": 0.0, "media": True,
                         "reason": "--quick：媒体类自测（需 ffmpeg lavfi 合成素材）已按要求跳过", "tail": []})
            continue
        if media and not have_ff:
            rows.append({"script": p.name, "status": "SKIP", "seconds": 0.0, "media": True,
                         "reason": "找不到 ffmpeg/ffprobe：媒体类自测无法运行（装 ffmpeg 并加入 PATH 后重跑）", "tail": []})
            continue
        r = run_one(p, timeout)
        r["media"] = media
        rows.append(r)
    return rows


def table(rows: list[dict]) -> str:
    w = max([len(r["script"]) for r in rows] + [6])
    out = [f"{'脚本'.ljust(w - 2)}  结果  秒数    说明", "-" * (w + 30)]
    for r in rows:
        out.append(f"{r['script'].ljust(w)}  {r['status']:<4}  {r['seconds']:>6.1f}  {r['reason']}")
    n = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "SKIP")}
    out.append("-" * (w + 30))
    out.append(f"合计 {len(rows)}：PASS {n['PASS']} / FAIL {n['FAIL']} / SKIP {n['SKIP']}")
    skipped = [r["script"] for r in rows if r["status"] == "SKIP"]
    if skipped:
        out.append(f"注意：以下脚本未运行自测（SKIP ≠ PASS）：{', '.join(skipped)}")
    for r in rows:
        if r["status"] == "FAIL" and r["tail"]:
            out.append(f"\n--- {r['script']} 输出末尾 ---\n" + "\n".join(r["tail"]))
    return "\n".join(out)


def selftest() -> int:
    ok = []
    found = [p.name for p in discover()]
    ok.append(bool(found) and "academy_common.py" not in found and Path(__file__).name not in found)
    print(f"{'PASS' if ok[-1] else 'FAIL'}  发现 {len(found)} 个脚本，排除 academy_common.py 与自身")
    media = [p.name for p in discover() if is_media(p)]
    ok.append("contact_sheet.py" in media and "prompt_lint.py" not in media)
    print(f"{'PASS' if ok[-1] else 'FAIL'}  媒体类识别（need_ffmpeg）：{media}")
    rows = run_all(quick=True, only=["contact_sheet"])
    ok.append(len(rows) == 1 and rows[0]["status"] == "SKIP" and "--quick" in rows[0]["reason"])
    print(f"{'PASS' if ok[-1] else 'FAIL'}  --quick → 媒体类记 SKIP 并写明原因")
    ok.append("SKIP ≠ PASS" in table(rows))
    print(f"{'PASS' if ok[-1] else 'FAIL'}  汇总表明确列出未运行的脚本")
    print(f"SELFTEST {'PASS' if all(ok) else 'FAIL'}（{sum(ok)}/{len(ok)}）")
    return 0 if all(ok) else 1


def main(argv=None) -> int:
    for st in (sys.stdout, sys.stderr):          # E3-1：非 UTF-8 控制台不因中文/符号崩溃
        try:
            st.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--timeout", type=int, default=300, help="每个脚本自测的超时秒数（默认 300）")
    ap.add_argument("--quick", action="store_true", help="跳过需要 ffmpeg 的媒体类自测（报告中明确列为 SKIP）")
    ap.add_argument("--only", nargs="+", metavar="SCRIPT", help="只跑这些脚本（名字可不带 .py）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="只测本汇总器自身（不跑其他脚本的自测）")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.timeout <= 0:
        print("用法/环境错误：--timeout 必须 > 0", file=sys.stderr)
        return 2
    rows = run_all(a.timeout, a.quick, a.only)
    if not rows:
        print("用法/环境错误：没有发现任何脚本（--only 写错了？）", file=sys.stderr)
        return 2
    failed = any(r["status"] == "FAIL" for r in rows)
    if a.json:
        print(json.dumps({"ok": not failed, "quick": a.quick, "results": rows}, ensure_ascii=False, indent=2))
    else:
        print("== 全部脚本自测 run_all_selftests ==")
        print(table(rows))
        print(f"结果：{'不通过' if failed else '通过'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
