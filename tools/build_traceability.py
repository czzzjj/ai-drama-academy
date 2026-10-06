#!/usr/bin/env python3
"""溯源总表生成器（build traceability）。

把「委托方档案编号 → 判据 → 技能 → 找错题」四层链条汇成一张表，写入 60-casebook/traceability.md。
数据来源（只读）：
  (a) 50-rubrics/checklists/*.md ：编号列匹配 R-<STAGE>-nn 的表格行，读其「溯源」列；
  (b) 60-casebook/cards/*.md     ：frontmatter 的 id / skills / drills；
  (c) 60-casebook/drills/answers/*.md ：「对应案例」行里出现的编号（无该行则退化为全文）→ 该找错题训练哪些编号；
  (d) 20-craft/*/SKILL.md         ：正文里出现的档案编号 → 该技能管哪些编号。
追踪的档案编号：A1–A5、B1–B4、C1、C2、D1–D5、E1–E4、F1–F4、P1–P10、M1–M10、GAP-1–GAP-7。
匹配规则：P1 不匹配 P10；C1-1..C1-7（E3-1..E3-3 同理）计入 C1（E3）。

用法：
  python3 tools/build_traceability.py            # 重新生成 60-casebook/traceability.md
  python3 tools/build_traceability.py --check    # 文件过期（与现有源不一致）则退出 1，不写文件
退出码：0 通过 / 1 过期（--check）/ 2 用法错误或源缺失。
生成结果不含时间戳，同一份源必得同一份输出。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "60-casebook" / "traceability.md"
COMMAND = "python3 tools/build_traceability.py"

STAGES = "SCR|SB|VP|BRD|KF|VID|CUT|SND|COL|PRF|PUB|SEA"
RE_R = re.compile(rf"R-(?:{STAGES})-\d{{2}}")
RE_DR = re.compile(r"(?<![A-Za-z0-9_-])DR-\d{2}(?![A-Za-z0-9_])")

# 追踪的编号（展示顺序）
TRACKED = (
    [f"A{i}" for i in range(1, 6)]
    + [f"B{i}" for i in range(1, 5)]
    + ["C1", "C2"]
    + [f"D{i}" for i in range(1, 6)]
    + [f"E{i}" for i in range(1, 5)]
    + [f"F{i}" for i in range(1, 5)]
    + [f"P{i}" for i in range(1, 11)]
    + [f"M{i}" for i in range(1, 11)]
    + [f"GAP-{i}" for i in range(1, 8)]
)
CASE_IDS = set(TRACKED[:24])  # A1–F4：有案例卡的编号

# 子编号并入父编号：C1-1..C1-7 → C1；E3-1..E3-3 → E3
RE_ID = re.compile(
    r"(?<![A-Za-z0-9_-])"
    r"(?:(?P<sub>C1|E3)-[1-9]|(?P<gap>GAP-[1-7])|(?P<plain>P(?:10|[1-9])|M(?:10|[1-9])|[A-F][1-9]))"
    r"(?![A-Za-z0-9_])"
)


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def find_ids(text: str) -> set:
    """文本里出现的、在 TRACKED 内的档案编号（C1-n 并入 C1）。"""
    found = set()
    tracked = set(TRACKED)
    for m in RE_ID.finditer(text):
        if m.group("sub"):
            cand = m.group("sub")
        else:
            cand = m.group("gap") or m.group("plain")
        if cand in tracked:
            found.add(cand)
    return found


def parse_frontmatter(text: str) -> dict:
    """极简 frontmatter：`key: value` 与 `key: [a, b]`。"""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    data = {}
    for raw in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not m:
            continue
        val = re.sub(r"\s+#.*$", "", m.group(2)).strip()
        if val.startswith("[") and val.endswith("]"):
            data[m.group(1)] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            data[m.group(1)] = val.strip("'\"")
    return data


def split_row(line: str) -> list:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


# ---------------------------------------------------------------- collectors

def collect_rubrics(warnings: list) -> dict:
    """(a) → {档案编号: {R-xxx-nn}}，并返回判据总数。"""
    by_id = {i: set() for i in TRACKED}
    all_r = set()
    for f in sorted((ROOT / "50-rubrics" / "checklists").glob("*.md")):
        header = None
        for n, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not ln.strip().startswith("|"):
                header = None
                continue
            cells = split_row(ln)
            if "编号" in cells and "溯源" in cells:
                header = cells
                continue
            if header is None or set(ln.replace("|", "").strip()) <= set("-: "):
                continue
            rid = cells[0]
            if not RE_R.fullmatch(rid):
                continue
            if len(cells) != len(header):
                warnings.append(f"{rel(f)}:{n} {rid} 列数 {len(cells)} ≠ 表头 {len(header)}，溯源列可能错位")
            idx = header.index("溯源")
            trace = cells[idx] if idx < len(cells) else ""
            all_r.add(rid)
            for tid in find_ids(trace):
                by_id[tid].add(rid)
    return {"by_id": by_id, "all": all_r}


def collect_cards(warnings: list) -> dict:
    """(b) → {案例id: {"skills": [...], "drills": [...]}}。"""
    cards = {}
    for f in sorted((ROOT / "60-casebook" / "cards").glob("*.md")):
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        cid = fm.get("id", "")
        if not cid:
            warnings.append(f"{rel(f)} 缺少 frontmatter id")
            continue
        cards[cid] = {"skills": list(fm.get("skills", [])), "drills": list(fm.get("drills", []))}
    return cards


def collect_answers() -> dict:
    """(c) → {档案编号: {DR-nn}}。以「对应案例」行为准；无该行则取全文。"""
    by_id = {i: set() for i in TRACKED}
    for f in sorted((ROOT / "60-casebook" / "drills" / "answers").glob("DR-*.md")):
        text = f.read_text(encoding="utf-8")
        lines = [ln for ln in text.splitlines() if "对应案例" in ln]
        scope = "\n".join(lines) if lines else text
        for tid in find_ids(scope):
            by_id[tid].add(f.stem)
    return by_id


def collect_skills() -> dict:
    """(d) → {档案编号: {skill-name}}。"""
    by_id = {i: set() for i in TRACKED}
    for f in sorted((ROOT / "20-craft").glob("*/SKILL.md")):
        for tid in find_ids(f.read_text(encoding="utf-8")):
            by_id[tid].add(f.parent.name)
    return by_id


# ---------------------------------------------------------------- render

def dr_key(s: str):
    m = re.fullmatch(r"DR-(\d+)", s)
    return (0, int(m.group(1))) if m else (1, s)


def render(rub: dict, cards: dict, ans: dict, skl: dict) -> str:
    rows, gap_r, gap_s, gap_d = [], [], [], []
    notes_card_skill, notes_card_drill = [], []

    for tid in TRACKED:
        rs = sorted(rub["by_id"][tid])
        card = cards.get(tid, {"skills": [], "drills": []})
        sk = sorted(set(card["skills"]) | skl[tid])
        dr = sorted(set(card["drills"]) | ans[tid], key=dr_key)
        if not rs:
            gap_r.append(tid)
        if not sk:
            gap_s.append(tid)
        if not dr:
            gap_d.append(tid)
        # 一致性：卡片声明 ↔ 技能正文 / 答案文件
        for s in card["skills"]:
            if s not in skl[tid]:
                notes_card_skill.append(f"{tid}：卡片 skills 列了 `{s}`，但 `20-craft/{s}/SKILL.md` 正文没有出现 {tid}")
        if tid in cards:
            for d in card["drills"]:
                if d not in ans[tid]:
                    notes_card_drill.append(f"{tid}：卡片 drills 列了 {d}，但 `{d}` 答案的「对应案例」行没有 {tid}")
        rows.append(
            "| {tid} | {r} | {s} | {d} |".format(
                tid=tid,
                r=(f"{len(rs)} 条：" + ", ".join(rs)) if rs else "—",
                s=", ".join(f"`{x}`" for x in sk) if sk else "—",
                d=", ".join(dr) if dr else "—",
            )
        )

    out = [
        "# 溯源总表（档案编号 → 判据 → 技能 → 找错题）",
        "",
        "> **本文件由脚本生成，请勿手改。** 改源（判据溯源列 / 案例卡 frontmatter / 技能正文 / 找错题答案）后，用下面的命令重新生成；`--check` 用于确认没有过期。",
        ">",
        "> ```bash",
        f"> {COMMAND}            # 重新生成本文件",
        f"> {COMMAND} --check    # 过期则退出码 1",
        "> ```",
        ">",
        f"> 数据源：`50-rubrics/checklists/*.md`（{len(rub['all'])} 条判据，读「溯源」列）、`60-casebook/cards/*.md`（frontmatter 的 skills/drills）、"
        "`60-casebook/drills/answers/*.md`（「对应案例」行）、`20-craft/*/SKILL.md`（正文提及的编号）。",
        "> 规则：C1-1..C1-7 计入 C1，E3-1..E3-3 计入 E3；P1 不含 P10。"
        "技能列 = 卡片 frontmatter 声明 ∪ 技能正文提及；找错题列 = 卡片声明 ∪ 答案「对应案例」行提及。",
        "",
        "| 编号 | 判据（R-） | 技能 | 找错题 |",
        "|---|---|---|---|",
        *rows,
        "",
        "## 覆盖缺口",
        "",
        f"- **零判据的编号（{len(gap_r)}）**：" + (", ".join(gap_r) if gap_r else "无"),
        f"- **零技能的编号（{len(gap_s)}）**：" + (", ".join(gap_s) if gap_s else "无"),
        f"- **零找错题的编号（{len(gap_d)}）**：" + (", ".join(gap_d) if gap_d else "无"),
        "",
        "处理：零判据 = 档案里的这条经验还没被固化成可判真假的检查句；零技能 = 没有任何技能把它变成生成/验收动作；"
        "零找错题 = 没有训练题让 agent 练习识别它。补缺口时改源文件，不要改本表。",
        "",
        "## 一致性提示（卡片声明了、但技能正文/答案没有回指的）",
        "",
        '卡片是单向声明；下列是卡片写了、对端却没有回指的项。答案「对应案例」行里多出来的次要案例（卡片没列）是设计如此，不在此报。',
        "",
    ]
    notes = notes_card_skill + notes_card_drill
    out += [f"- {n}" for n in notes] if notes else ["- 无"]
    out.append("")
    return "\n".join(out)


def build() -> tuple:
    warnings: list = []
    for d in ("50-rubrics/checklists", "60-casebook/cards", "60-casebook/drills/answers", "20-craft"):
        if not (ROOT / d).is_dir():
            print(f"源目录缺失：{d}", file=sys.stderr)
            sys.exit(2)
    rub = collect_rubrics(warnings)
    cards = collect_cards(warnings)
    ans = collect_answers()
    skl = collect_skills()
    return render(rub, cards, ans, skl), warnings


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 60-casebook/traceability.md（溯源总表）")
    ap.add_argument("--check", action="store_true", help="只检查文件是否过期，不写入；过期退出 1")
    args = ap.parse_args()

    content, warnings = build()
    for w in warnings:
        print(f"WARN  {w}", file=sys.stderr)

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else None
        if current != content:
            why = "不存在" if current is None else "内容与现有源不一致"
            print(f"STALE {rel(OUT)}：{why}。请运行 `{COMMAND}` 重新生成。")
            return 1
        print(f"OK    {rel(OUT)} 是最新的")
        return 0

    OUT.write_text(content, encoding="utf-8")
    print(f"写入 {rel(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
