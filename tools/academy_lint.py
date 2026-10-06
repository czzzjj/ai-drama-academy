#!/usr/bin/env python3
"""学院全库自检（academy lint）。

校验 CONVENTIONS.md 中标 🔒 的条款：
  1. 技能 SKILL.md：frontmatter 只有 name/description，name 与目录同名且合法，description ≤1024，
     正文包含必需章节。
  2. 案例卡：frontmatter 键齐全、id 与文件名一致、必需章节齐全。
  3. 判据表：每条 R-xxx 有合法"方式"标签、溯源非空且含合法编号、编号全局唯一。
  4. 编号引用：S-/F-（外部来源）、R-（判据）、DR-（找错题）、EX-（练习）、MEM-/TP-/TJ- 唯一性。
  5. 记忆条目格式。
  6. 相对链接不悬空；文件路径不含中文（E3-1）。

用法：
  python3 tools/academy_lint.py                 # 全库，严格
  python3 tools/academy_lint.py --paths a.md b.md   # 只报告这些文件的问题（构建期自查用）
  python3 tools/academy_lint.py --links-as-warnings # 悬空链接只告警（构建期）
  python3 tools/academy_lint.py --json
退出码：0 通过 / 1 有错误 / 2 用法错误。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STAGES = "SCR|SB|VP|BRD|KF|VID|CUT|SND|COL|PRF|PUB|SEA"
RE_R = re.compile(rf"\bR-(?:{STAGES})-\d{{2}}\b")
RE_S = re.compile(r"\bS-[A-Z]{2,6}-\d{2}\b")
RE_F = re.compile(r"\bF-[A-Z]{2,6}-\d{2}\b")
RE_DR = re.compile(r"\bDR-\d{2}\b")
RE_EX = re.compile(r"\bEX-\d{2}\b")
RE_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
RE_IMG = re.compile(r"\!\[[^\]]*\]\(([^)\s]+)\)")
RE_CJK = re.compile(r"[一-鿿]")

DOSSIER_IDS = (
    {f"T-{i}" for i in range(1, 5)}
    | {f"P{i}" for i in range(1, 11)}
    | {f"M{i}" for i in range(1, 11)}
    | {f"A{i}" for i in range(1, 6)}
    | {f"B{i}" for i in range(1, 5)}
    | {"C1", "C2"} | {f"C1-{i}" for i in range(1, 8)}
    | {f"D{i}" for i in range(1, 6)}
    | {f"E{i}" for i in range(1, 5)} | {f"E3-{i}" for i in range(1, 4)}
    | {f"F{i}" for i in range(1, 5)}
    | {f"G{i}" for i in range(1, 9)}
    | {f"GAP-{i}" for i in range(1, 8)}
)
RE_TRACE_TOKEN = re.compile(
    r"\b(?:T-[1-4]|P(?:10|[1-9])|M(?:10|[1-9])|A[1-5]|B[1-4]|C1-[1-7]|C[12]|D[1-5]|E3-[1-3]|E[1-4]|F[1-4]|G[1-8]|GAP-[1-7])\b"
    r"|\bS-[A-Z]{2,6}-\d{2}\b|\bF-[A-Z]{2,6}-\d{2}\b"
)

SKILL_SECTIONS = ["何时用", "步骤", "判据", "失败模式"]
CASE_KEYS = ["id", "title", "group", "scope", "severity", "provenance", "skills", "drills"]
CASE_SECTIONS = ["症状", "根因", "可固化判据", "行为改变"]
CASE_FILES = {
    "A1": "A1-fragmented-shots", "A2": "A2-missing-fights", "A3": "A3-slow-motion-default",
    "A4": "A4-unmotivated-camera", "A5": "A5-spatial-chaos",
    "B1": "B1-character-drift", "B2": "B2-crowd-leak", "B3": "B3-clone-faces", "B4": "B4-duplicate-artifacts",
    "C1": "C1-banned-items-violated", "C2": "C2-lenient-acceptance",
    "D1": "D1-burned-in-captions", "D2": "D2-solid-black-fails", "D3": "D3-dialogue-capacity",
    "D4": "D4-symbol-errors", "D5": "D5-qc-tools-lie",
    "E1": "E1-slot-order", "E2": "E2-stale-paths", "E3": "E3-environment-quirks", "E4": "E4-prompt-output-mismatch",
    "F1": "F1-self-verification-loop", "F2": "F2-proxy-metrics", "F3": "F3-patch-iteration", "F4": "F4-skills-not-ability",
}
EXAMPLE_DOCS = {"CONVENTIONS.md"}
RE_MEM = re.compile(r"^- \[MEM-(\d{2,3})\]\[[^\]]+\] .+（为什么：.+）〔溯源：[^〕]+〕\s*$")


class Report:
    def __init__(self, only: set[Path] | None, links_as_warnings: bool):
        self.errors: list[dict] = []
        self.warnings: list[dict] = []
        self.only = only
        self.links_as_warnings = links_as_warnings

    def _keep(self, path: Path) -> bool:
        return self.only is None or path.resolve() in self.only

    def err(self, path: Path, msg: str, line: int | None = None):
        if self._keep(path):
            self.errors.append({"file": rel(path), "line": line, "msg": msg})

    def warn(self, path: Path, msg: str, line: int | None = None):
        if self._keep(path):
            self.warnings.append({"file": rel(path), "line": line, "msg": msg})


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def md_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.md"):
        parts = p.relative_to(ROOT).parts
        if parts[0].startswith(".") or "node_modules" in parts:
            continue
        out.append(p)
    return sorted(out)


def parse_frontmatter(text: str) -> tuple[dict | None, str, list[str]]:
    """极简 YAML frontmatter 解析：仅支持 `key: value` 与 `key: [a, b]`。返回 (dict, body, keys_in_order)。"""
    if not text.startswith("---\n"):
        return None, text, []
    end = text.find("\n---", 4)
    if end < 0:
        return None, text, []
    block = text[4:end]
    body = text[end + 4:].lstrip("\n")
    data, keys = {}, []
    cur = None
    for raw in block.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if m:
            cur = m.group(1)
            keys.append(cur)
            val = re.sub(r"\s+#.*$", "", m.group(2)).strip()
            if val.startswith("[") and val.endswith("]"):
                data[cur] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            else:
                data[cur] = val.strip("'\"")
        elif cur and raw.startswith((" ", "\t")):
            data[cur] = (str(data[cur]) + " " + raw.strip()).strip()
    return data, body, keys


def headings(body: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^#{1,6}\s+(.+)$", body, re.M)]


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


# ---------------------------------------------------------------- checks

def check_paths(rep: Report):
    for p in ROOT.rglob("*"):
        parts = p.relative_to(ROOT).parts
        if parts[0].startswith(".git"):
            continue
        if RE_CJK.search(p.name):
            rep.err(p, "文件/目录名含中文（违反 E3-1 公约：一律英文 kebab-case）")


def check_skills(rep: Report):
    craft = ROOT / "20-craft"
    if not craft.exists():
        return
    for d in sorted(x for x in craft.iterdir() if x.is_dir()):
        sk = d / "SKILL.md"
        if not sk.exists():
            rep.err(d, "技能目录缺少 SKILL.md")
            continue
        text = sk.read_text(encoding="utf-8")
        fm, body, keys = parse_frontmatter(text)
        if fm is None:
            rep.err(sk, "缺少 YAML frontmatter")
            continue
        extra = [k for k in keys if k not in ("name", "description")]
        if extra:
            rep.err(sk, f"frontmatter 只允许 name/description，发现多余键：{extra}")
        name = fm.get("name", "")
        if name != d.name:
            rep.err(sk, f"name '{name}' 与目录名 '{d.name}' 不一致")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or "") or len(name) > 64:
            rep.err(sk, f"name 非法（需小写 kebab-case ≤64）：'{name}'")
        desc = fm.get("description", "")
        if not desc:
            rep.err(sk, "description 为空")
        elif len(desc) > 1024:
            rep.err(sk, f"description 超过 1024 字符（{len(desc)}）")
        if desc and not re.search(r"触发|Use when|use when", desc):
            rep.warn(sk, "description 未写触发词（建议含 'Use when' 与 '触发词'）")
        hs = " ".join(headings(body))
        for sec in SKILL_SECTIONS:
            if sec not in hs:
                rep.err(sk, f"正文缺少必需章节：{sec}")
        n = body.count("\n")
        if n > 400:
            rep.warn(sk, f"正文 {n} 行，超过建议的 400 行（长内容请放 references/）")


def check_cases(rep: Report):
    cards = ROOT / "60-casebook" / "cards"
    if not cards.exists():
        return
    seen = {}
    for f in sorted(cards.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, body, _ = parse_frontmatter(text)
        if fm is None:
            rep.err(f, "案例卡缺少 frontmatter")
            continue
        for k in CASE_KEYS:
            if k not in fm:
                rep.err(f, f"案例卡 frontmatter 缺少键：{k}")
        cid = fm.get("id", "")
        expect = CASE_FILES.get(cid)
        if expect is None:
            rep.err(f, f"未知案例 id：{cid}")
        elif f.stem != expect:
            rep.err(f, f"文件名应为 {expect}.md")
        seen[cid] = f
        hs = " ".join(headings(body))
        for sec in CASE_SECTIONS:
            if sec not in hs:
                rep.err(f, f"案例卡缺少必需章节：{sec}")
    missing = sorted(set(CASE_FILES) - set(seen))
    if missing and rep.only is None:
        rep.errors.append({"file": "60-casebook/cards/", "line": None, "msg": f"缺少案例卡：{missing}"})


def collect_defs() -> dict:
    defs = {"R": {}, "S": set(), "F": set(), "DR": set(), "EX": set(), "MEM": {}, "TP": {}, "TJ": {}}
    for f in sorted((ROOT / "80-sources" / "catalog").glob("*.md")) if (ROOT / "80-sources" / "catalog").exists() else []:
        t = f.read_text(encoding="utf-8")
        defs["S"].update(re.findall(r"^#{2,4}\s+(S-[A-Z]{2,6}-\d{2})\b", t, re.M))
        defs["F"].update(re.findall(r"^\|\s*(F-[A-Z]{2,6}-\d{2})\s*\|", t, re.M))
    dr = ROOT / "60-casebook" / "drills"
    if dr.exists():
        defs["DR"].update(p.stem for p in dr.glob("DR-*.md"))
    ex = ROOT / "90-curriculum" / "exercises"
    if ex.exists():
        defs["EX"].update(p.stem for p in ex.glob("EX-*.md"))
    return defs


def check_rubrics(rep: Report, defs: dict):
    cl = ROOT / "50-rubrics" / "checklists"
    if not cl.exists():
        return
    for f in sorted(cl.glob("*.md")):
        lines = f.read_text(encoding="utf-8").splitlines()
        header = None
        for i, ln in enumerate(lines, 1):
            if not ln.strip().startswith("|"):
                header = None
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if "编号" in cells and "溯源" in cells:
                header = cells
                continue
            if header is None or set(ln.replace("|", "").strip()) <= set("-: "):
                continue
            row = dict(zip(header, cells))
            rid = row.get("编号", "")
            if not RE_R.fullmatch(rid):
                continue
            if rid in defs["R"]:
                rep.err(f, f"判据编号重复：{rid}（已在 {rel(defs['R'][rid])} 定义）", i)
            defs["R"][rid] = f
            mode = row.get("方式", "")
            if not re.search(r"\[(自动|目视|冷观众)\]", mode):
                rep.err(f, f"{rid} 方式列必须含 [自动]/[目视]/[冷观众]", i)
            trace = row.get("溯源", "")
            if not trace or trace == "—":
                rep.err(f, f"{rid} 溯源为空（判据不允许凭空写）", i)
            elif not RE_TRACE_TOKEN.search(trace):
                rep.err(f, f"{rid} 溯源列没有合法编号：'{trace}'", i)
            if not row.get("检查句（可判真假）", row.get("检查句", "")):
                rep.err(f, f"{rid} 检查句为空", i)


def check_memory(rep: Report, defs: dict):
    f = ROOT / "40-memory" / "core-memory.md"
    if not f.exists():
        return
    for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if ln.startswith("- [MEM-"):
            m = RE_MEM.match(ln)
            if not m:
                rep.err(f, "记忆条目格式不符：需 `- [MEM-nn][域] 规则（为什么：…）〔溯源：…〕`", i)
                continue
            mid = m.group(1)
            if mid in defs["MEM"]:
                rep.err(f, f"MEM-{mid} 重复", i)
            defs["MEM"][mid] = i
            tr = ln[ln.rfind("〔溯源："):]
            if not RE_TRACE_TOKEN.search(tr):
                rep.err(f, f"MEM-{mid} 溯源无合法编号", i)


def check_unique_defs(rep: Report, defs: dict):
    for kind, pat in (("TP", r"^##\s+(TP-\d{2})\b"), ("TJ", r"^##\s+(TJ-\d{2})\b")):
        base = ROOT / "30-taste"
        if not base.exists():
            continue
        for f in sorted(base.rglob("*.md")):
            for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                m = re.match(pat, ln)
                if m:
                    k = m.group(1)
                    if k in defs[kind]:
                        rep.err(f, f"{k} 重复定义", i)
                    defs[kind][k] = f


def check_refs_and_links(rep: Report, defs: dict):
    for f in md_files():
        raw = f.read_text(encoding="utf-8")
        text = strip_code(raw)
        is_catalog = "80-sources/catalog" in rel(f)
        if "50-rubrics/scripts/fixtures/" in rel(f):  # 脚本 fixtures 故意含坏链接/坏编号，是测试数据
            continue
        if rel(f) in EXAMPLE_DOCS:  # 公约/契约文档中的编号是格式示例，不做引用校验
            continue
        for i, ln in enumerate(text.splitlines(), 1):
            for rid in RE_R.findall(ln):
                if defs["R"] and rid not in defs["R"]:
                    rep.err(f, f"引用了不存在的判据 {rid}", i)
            if not is_catalog:
                for sid in RE_S.findall(ln):
                    if sid not in defs["S"]:
                        rep.err(f, f"引用了不存在的来源条目 {sid}", i)
                for fid in RE_F.findall(ln):
                    if fid not in defs["F"]:
                        rep.err(f, f"引用了不存在的来源事实 {fid}", i)
            for d in RE_DR.findall(ln):
                if defs["DR"] and d not in defs["DR"]:
                    rep.err(f, f"引用了不存在的找错题 {d}", i)
            for e in RE_EX.findall(ln):
                if defs["EX"] and e not in defs["EX"]:
                    rep.err(f, f"引用了不存在的练习 {e}", i)
            for target in RE_LINK.findall(ln) + RE_IMG.findall(ln):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                if not path:
                    continue
                dest = (f.parent / path).resolve()
                if not dest.exists():
                    msg = f"悬空链接：{target}"
                    (rep.warn if rep.links_as_warnings else rep.err)(f, msg, i)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paths", nargs="*", help="只报告这些文件中的问题")
    ap.add_argument("--links-as-warnings", action="store_true", help="悬空链接降级为警告（构建期）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    only = {Path(p).resolve() for p in a.paths} if a.paths else None
    rep = Report(only, a.links_as_warnings)

    defs = collect_defs()
    check_paths(rep)
    check_skills(rep)
    check_cases(rep)
    check_rubrics(rep, defs)
    check_memory(rep, defs)
    check_unique_defs(rep, defs)
    check_refs_and_links(rep, defs)

    summary = {
        "errors": len(rep.errors), "warnings": len(rep.warnings),
        "defined": {"R": len(defs["R"]), "S": len(defs["S"]), "F": len(defs["F"]), "DR": len(defs["DR"]),
                    "EX": len(defs["EX"]), "MEM": len(defs["MEM"]), "TP": len(defs["TP"]), "TJ": len(defs["TJ"])},
    }
    if a.json:
        print(json.dumps({"summary": summary, "errors": rep.errors, "warnings": rep.warnings}, ensure_ascii=False, indent=2))
    else:
        for e in rep.errors:
            print(f"ERROR {e['file']}{':' + str(e['line']) if e['line'] else ''}  {e['msg']}")
        for w in rep.warnings:
            print(f"WARN  {w['file']}{':' + str(w['line']) if w['line'] else ''}  {w['msg']}")
        print(f"\n定义计数：{summary['defined']}")
        print(f"结果：{summary['errors']} 个错误，{summary['warnings']} 个警告")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
