#!/usr/bin/env python3
"""参考槽顺序检查 slot_order_check —— 改 references / 导出 ComfyUI 绑定列表后、prepare 之前必跑。

用途：
  逐镜检查参考图槽位编号（video-prompts.md 的 `references`，或 ComfyUI 导出的绑定列表 JSON）：
    · 编号必须从 1 起唯一且连续（"绑定顺序必须从 1 起唯一连续"校验，E1）；
    · 占位槽（ID 含 PLACEHOLDER/占位；或元数据 `- 占位:` 指定；或本镜自己的 REF-SHOTnnn-START 而起始帧尚未产出）
      必须排在**末位**（E1 修正：其余参考 1..N-1 + 占位 N，生产期删掉占位后天然连续；起始帧产出后再提回顺序 1）；
    · --simulate-remove-placeholder：打印"删掉占位槽之后编号变成什么"，不连续即报错——复现委托方一次 18 镜、一次 16 镜
      集体失败的现场（占位槽在第 1 位，删掉后剩余从 2 起）；
    · first_frame 应为本镜自己的 REF-SHOT<同号>-START（T-3：起始帧顺序 1 送 first_frame；P4 起始帧驱动）；
    · 给 --bindings 时，再核对导出的绑定列表本身，以及它与 references 的参考图顺序是否一致（不一致 → <Picture N> 指错图）。
  脚本只报告编号事实与可直接照抄的重排方案，不判断参考图选得好不好。

溯源：E1（槽位顺序连续性：占位起始帧槽排在 1 位，删除后剩余从 2 起 → 18 镜/16 镜集体失败）, T-3（起始帧=REF-SHOTxxx-START 顺序 1
     送 first_frame）；另 P4、T-2（<Picture N> 编号与引用顺序一致）。

规则代码（SLOT-）：
  SLOT-number          error  条目缺编号（references 写成 'N=ID'；绑定项缺 order）
  SLOT-unique          error  编号重复
  SLOT-contiguous      error  编号不是从 1 起连续（从 2 起 = E1 现场）
  SLOT-placeholder-pos error  占位槽不在末位（附重排方案与 <Picture N> 改写表）
  SLOT-placeholder-ref warn   提示词 <Picture N> 指向占位槽：删除占位后该引用悬空
  SLOT-own-start       info   本镜起始帧出现在 references 非末位，且无法确认是否已产出（加 --assets-dir 核实）
  SLOT-sim             error  （--simulate-remove-placeholder）删除占位后编号不连续；info：删除后仍连续
  SLOT-first-frame     warn   first_frame 为空，或不是 REF-SHOT<同号>-START
  SLOT-bind-mismatch   error  绑定列表与 references 的参考图集合相同但顺序不同；warn：集合不同
  SLOT-format          info   绑定项未写 order，按列表顺序视为 1..N
                       warn   references 用了全角 ＝ / 逗号分隔（已按纠正后的编号核对）；first_frame/参考 ID 写成了路径或带扩展名
  FMT-shot-heading     error  疑似镜头标题不合 `## SHOT-nnn`：该镜的 references 完全没被检查（与 h3_frame_grid 同码）
  FMT-bom              warn   文件以 UTF-8 BOM 开头（已去 BOM 解析）

  判定口径：ID 含 PLACEHOLDER/占位/待产/未产出，或以 TBD/TODO 为独立段（REF-TBD、X-TODO-1；CHR-TODOROKI 不算）→ 占位；
  `- 占位:` 可写槽号、ID、'N=ID' 或 '是'，写 否/无/no 视同未声明；参考 ID 与 first_frame 比较前去掉目录与图片扩展名。

输入格式：70-playbooks/format-contracts.md §2 视频提示词（元数据 first_frame / references / 可选 占位）
          （相对本文件：../../70-playbooks/format-contracts.md）
  --bindings JSON（ComfyUI 导出的绑定列表；本脚本的扩展输入，契约 §2 规则 2 的同一规则）：
    {"SHOT-002": [{"order": 1, "ref": "CHR-SUXIAO-BOARD"}, {"order": 2, "ref": "REF-SHOT001-START"}], ...}
    或单镜列表 [{"order": 1, "ref": "…"}, …]（配合 --shot SHOT-002）；
    键名也接受 index/slot/position 与 id/image/name/value；可加 "placeholder": true 标记占位槽；纯字符串列表按顺序视为 1..N。

用法示例：
  python3 50-rubrics/scripts/slot_order_check.py season-01/ep03/video-prompts.md
  python3 50-rubrics/scripts/slot_order_check.py season-01/ep03/video-prompts.md --simulate-remove-placeholder \\
      --assets-dir season-01/ep03/assets
  python3 50-rubrics/scripts/slot_order_check.py season-01/ep03/video-prompts.md --bindings exports/bindings.json
  python3 50-rubrics/scripts/slot_order_check.py --bindings exports/SHOT-012.json --shot SHOT-012 --json
  python3 50-rubrics/scripts/slot_order_check.py --selftest

退出码：0 无 error / 1 有 error / 2 用法或环境错误（文件不存在、JSON 无法解析、两种输入都没给）
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import academy_common as ac  # noqa: E402
from academy_common import Finding  # noqa: E402

TITLE = "参考槽顺序检查 slot_order_check"
PICTURE_RE = re.compile(r"<Picture (\d+)>")
NOT_PRODUCED = re.compile(r"PLACEHOLDER|占位|待产|未产出|待定|(?:^|[-_./\s])(?:TBD|TODO)(?:$|[-_./\s])", re.I)
NEG_VALUE = re.compile(r"^\s*(?:否|无|不|没有|no|none|false|off|n/?a|0)\s*$", re.I)
IMG_EXT = re.compile(r"\.(?:png|jpe?g|webp|bmp|gif|tiff?|exr)$", re.I)
RE_STRICT_HEADING = re.compile(r"^##\s+(SHOT-\d{3})\b")              # 与 academy_common.parse_video_prompts 一致
RE_SHOTLIKE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(?:镜头|镜号|镜)?\s*[:：]?\s*shot\s*[-_－—–]?\s*(\d+)", re.I)
RE_SHOT_TOKEN = re.compile(r"shot\s*[-_－—–]?\s*\d+", re.I)


def own_start(shot_id: str) -> str:
    m = re.match(r"SHOT-(\d{3})", shot_id or "")
    return f"REF-SHOT{m.group(1)}-START" if m else ""


def ref_key(ref: str) -> str:
    """比较用的参考 ID：去目录、去图片扩展名、去空白、大写（assets/kf/REF-SHOT001-START.png → REF-SHOT001-START）。"""
    r = unicodedata.normalize("NFKC", (ref or "").strip()).replace("\\", "/")
    r = r.rsplit("/", 1)[-1]
    return IMG_EXT.sub("", r).strip().upper()


def _empty(v: str | None) -> bool:
    return ac.is_empty(v) or bool(re.fullmatch(r"[\s—–\-－─_]*", v or ""))


def fix_refs(raw: str) -> tuple[str, list[str]]:
    """references 的全角/逗号写法 → 契约写法；返回 (纠正后的串, 问题列表)。"""
    if _empty(raw):
        return raw, []
    issues, s = [], raw
    if "＝" in s:
        issues.append("全角等号 ＝")
        s = s.replace("＝", "=")
    s2 = re.sub(r"\s*[，,、]\s*(?=[0-9０-９]+\s*=)", "; ", s)
    if s2 != s:
        issues.append("用逗号/顿号分隔条目")
    return s2, issues


def _read(path: str | Path) -> tuple[str, bool]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        ac.die(f"{path} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8（无 BOM）后重跑")
    return (text[1:], True) if text.startswith("\ufeff") else (text, False)


def _parse_prompts_compat(path: str | Path) -> tuple[list[dict], str, bool]:
    """academy_common.parse_video_prompts 的 BOM 兼容包装（行号不变）。"""
    path = Path(path)
    text, bom = _read(path)
    if not bom:
        return ac.parse_video_prompts(path), text, False
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / path.name
        tmp.write_text(text, encoding="utf-8")
        shots = ac.parse_video_prompts(tmp)
    for s in shots:
        s["file"] = str(path)
    return shots, text, True


def _bad_headings(text: str) -> list[tuple[int, str, str, str | None, bool]]:
    bad, in_code, prev = [], False, None
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            sw = RE_STRICT_HEADING.match(ln)
            if sw:      # 上一个 ``` 没闭合（或外层用了 ````）：这一镜被吞进代码块，完全没被解析
                bad.append((i, ln.strip(), sw.group(1), prev, True))
            continue
        ok = RE_STRICT_HEADING.match(ln)
        if ok:
            prev = ok.group(1)
            continue
        n_ln = unicodedata.normalize("NFKC", ln)
        m = RE_SHOTLIKE_HEADING.match(n_ln)
        if m and len(RE_SHOT_TOKEN.findall(n_ln)) == 1:
            bad.append((i, ln.strip(), f"SHOT-{int(m.group(1)):03d}", prev, False))
    return bad


def _fmt(slots: list[dict]) -> str:
    return "; ".join(f"{s['order']}={s['ref']}" + ("(占位)" if s["ph"] else "") for s in slots) or "（空）"


def _contig(nums: list[int]) -> bool:
    return sorted(nums) == list(range(1, len(nums) + 1))


def _assets_index(d: str | Path | None) -> set | None:
    if not d:
        return None
    p = Path(d)
    if not p.is_dir():
        ac.die(f"--assets-dir 不是目录：{d}")
    return {f.stem.upper() for f in p.rglob("*") if f.is_file()}


def mark_placeholders(slots: list[dict], shot: dict | None, shot_id: str, assets: set | None) -> list[Finding]:
    """就地标注 slots[i]['ph'] / ['why']；返回 info 级提示。"""
    notes = []
    meta = shot["meta"] if shot else {}
    explicit = set()
    raw_ph = unicodedata.normalize("NFKC", meta.get("占位", ""))
    if not _empty(raw_ph) and not NEG_VALUE.match(raw_ph):
        for tok in re.split(r"[;；,，、\s]+", raw_ph):
            tok = tok.strip()
            if not tok or _empty(tok) or NEG_VALUE.match(tok):
                continue
            m = re.match(r"^(\d+)\s*=\s*(.+)$", tok)              # '3=REF-SHOT010-START'
            if m:
                explicit.update({int(m.group(1)), ref_key(m.group(2))})
            else:
                explicit.add(int(tok) if tok.isdigit() else ref_key(tok))
    own = own_start(shot_id)
    ff = meta.get("first_frame", "")
    ff_missing = shot is not None and (_empty(ff) or bool(NOT_PRODUCED.search(ff)))
    for s in slots:
        ref = s["ref"]
        if s.get("ph"):
            s["why"] = s.get("why") or "绑定项标记 placeholder"
        elif NOT_PRODUCED.search(ref):
            s["ph"], s["why"] = True, "ID 含 PLACEHOLDER/占位/待产"
        elif s["order"] in explicit or ref_key(ref) in explicit:
            s["ph"], s["why"] = True, "元数据 占位 指定"
        elif own and ref_key(ref) == own:
            if explicit and ("是" in explicit or "YES" in explicit or "TRUE" in explicit):
                s["ph"], s["why"] = True, "元数据 占位 指定本镜起始帧"
            elif ff_missing:
                s["ph"], s["why"] = True, "本镜起始帧尚未产出（first_frame 为空/待产）"
            elif assets is not None and own not in assets:
                s["ph"], s["why"] = True, f"--assets-dir 中找不到 {own}.*（起始帧尚未产出）"
            elif assets is None and s is not slots[-1] and not (s["order"] == 1 and ref_key(ff) == own):
                notes.append(Finding("info", "SLOT-own-start", f"本镜起始帧 {own} 在第 {s['order']} 槽：若它尚未产出，它就是占位槽，"
                                     "必须放末位（E1）→ 加 --assets-dir 让脚本核实是否已产出", shot_id))
    return notes


def check_slots(label: str, slots: list[dict], shot: dict | None, shot_id: str, where: str, simulate: bool,
                sim_log: list[str], source: str) -> list[Finding]:
    F: list[Finding] = []

    def add(level, code, msg, **data):
        F.append(Finding(level, code, msg, where, data))

    if not slots:
        return F
    unnum = [s["ref"] for s in slots if s["order"] is None]
    if unnum:
        add("error", "SLOT-number", f"{source} 中这些条目没有编号：{unnum} → 写成 'N=ID'，N 从 1 起连续（E1）")
    nums = [s["order"] for s in slots if s["order"] is not None]
    dup = sorted({n for n in nums if nums.count(n) > 1})
    if dup:
        add("error", "SLOT-unique", f"{source} 编号重复：{dup} → 每个编号只出现一次（E1）", dup=dup)
    ordered = sorted([s for s in slots if s["order"] is not None], key=lambda s: s["order"])
    pics = sorted({int(n) for n in PICTURE_RE.findall((shot or {}).get("h3") or "")})

    # 占位槽位置
    ph = [s for s in ordered if s["ph"]]
    non = [s for s in ordered if not s["ph"]]
    ph_bad = bool(ph) and any(not s["ph"] for s in ordered[ordered.index(ph[0]):])
    if ph_bad:
        new = [dict(s, order=i + 1) for i, s in enumerate(non + ph)]
        remap = {s["order"]: n["order"] for s, n in zip(non + ph, new) if s["order"] != n["order"]}
        rewrite = [f"<Picture {o}>→<Picture {remap[o]}>" for o in pics if o in remap]
        add("error", "SLOT-placeholder-pos",
            f"占位槽 {', '.join(str(s['order']) + '=' + s['ref'] + '（' + s['why'] + '）' for s in ph)} 不在末位（E1：生产期删掉占位后"
            f"剩余槽从 2 起 → 一次 18 镜、一次 16 镜集体失败）→ 改为 {_fmt(new)}"
            + (f"；并同步改写提示词 {', '.join(rewrite)}（按此表一次性映射，勿逐条查找替换以免串号）" if rewrite else "")
            + "；起始帧产出并验收后再把它提回顺序 1（T-3）", proposal=_fmt(new), rewrite=rewrite)
    if ph and pics:
        hit = [s["order"] for s in ph if s["order"] in pics]
        if hit:
            add("warn", "SLOT-placeholder-ref", f"提示词引用了占位槽 {', '.join(f'<Picture {n}>' for n in hit)}：删除占位后该引用悬空"
                " → 起始帧产出前不要在正文引用它，或用已存在的参考图替代", refs=hit)

    # 连续性
    if nums and not dup and not _contig(nums):
        e1 = "；编号从 2 起——与 E1 现场同型（占位槽在第 1 位被删除）" if min(nums) == 2 else ""
        if min(nums) == 0:
            e1 = "；编号从 0 起——若导出格式本身是 0 基下标（index），先 +1 换算再导出；ComfyUI 侧\"绑定顺序必须从 1 起\"校验会拒绝 0"
        fixed = [dict(s, order=i + 1) for i, s in enumerate(ordered)]
        add("error", "SLOT-contiguous", f"{source} 编号为 {sorted(nums)}，不是从 1 起连续{e1} → 按现有顺序重编号为 {_fmt(fixed)}；"
            f"然后逐个核对提示词中的 <Picture N>（当前引用 {pics or '无'}）指向的仍是同一资产", nums=sorted(nums))

    # 删除占位模拟
    if simulate:
        rest = [s["order"] for s in ordered if not s["ph"]]
        if ph:
            ok = _contig(rest)
            sim_log.append(f"  {label}：{_fmt(ordered)} → 删除占位后 {rest} {'✓ 连续' if ok else '✗ 不连续'}")
            if not ok:
                add("error", "SLOT-sim", f"删除占位槽后编号为 {rest}，不是从 1 起连续 → 生产期\"绑定顺序必须从 1 起唯一连续\"校验会失败"
                    f"（E1）→ 先按 SLOT-placeholder-pos 的方案把占位放末位", remaining=rest)
            else:
                add("info", "SLOT-sim", f"删除占位槽后编号为 {rest}，仍连续", remaining=rest)
        else:
            sim_log.append(f"  {label}：{_fmt(ordered)} → 无占位槽，删除后不变")
    return F


def check_first_frame(shot: dict, where: str) -> list[Finding]:
    ff, own = shot["meta"].get("first_frame", ""), own_start(shot["shot"])
    if _empty(ff) or NOT_PRODUCED.search(ff):
        return [Finding("warn", "SLOT-first-frame", f"first_frame 为空/待产：送 H3 的镜 run 前必须以已验收关键帧 {own} 作 first_frame"
                        "（P4 起始帧驱动；T-3）；若本镜是纯色卡/静帧插入，它不该出现在 video-prompts（D2）", where)]
    if ref_key(ff) == own and ff.strip().upper() != own:
        return [Finding("warn", "SLOT-format", f"first_frame 写成了路径/文件名「{ff}」→ 契约写参考 ID '{own}'（路径由素材目录约定解析，"
                        "写死路径会在改号/搬目录后残留，E2）", where, {"first_frame": ff})]
    if ref_key(ff) != own:
        return [Finding("warn", "SLOT-first-frame", f"first_frame={ff} 不是本镜起始帧 {own}（T-3：起始帧=REF-SHOT<同号>-START 送 "
                        "first_frame）→ 若是复制粘贴/改号残留，改为本镜 ID 并全仓复查（E2）", where, {"first_frame": ff})]
    return []


def load_bindings(path: str | Path, shot_opt: str | None) -> tuple[dict, list[Finding]]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))      # 容忍 BOM（Windows 导出常见）
    except UnicodeDecodeError:
        ac.die(f"--bindings 不是 UTF-8 编码：{path}（format-contracts §0.1）→ 导出为 UTF-8 后重跑")
    except (OSError, ValueError) as e:
        ac.die(f"--bindings 无法读取/解析：{path}（{e}）")
    notes: list[Finding] = []
    label_default = shot_opt or f"bindings:{Path(path).name}"
    if isinstance(data, dict) and data and all(re.match(r"^SHOT-\d{3}$", str(k).strip(), re.I) for k in data):
        groups = {str(k).strip().upper(): v for k, v in data.items()}
        odd = [k for k in data if not re.match(r"^SHOT-\d{3}$", k)]
        if odd:
            notes.append(Finding("warn", "SLOT-format", f"绑定 JSON 的镜号键写成了 {odd[:3]}（已按大写 SHOT-nnn 读入）→ 导出模板统一写 SHOT-nnn",
                                 Path(path).name))
    elif isinstance(data, dict) and isinstance(data.get("bindings", data.get("slots")), list):
        groups = {label_default: data.get("bindings", data.get("slots"))}
    elif isinstance(data, list):
        groups = {label_default: data}
    else:
        ac.die(f"--bindings 格式不认识：{path}（需 {{\"SHOT-002\": [...]}} 或 [{{\"order\": 1, \"ref\": \"…\"}}, …]）")
    out = {}
    for label, items in groups.items():
        if not isinstance(items, list):
            ac.die(f"--bindings 中 {label} 不是列表")
        slots, implicit = [], False
        for i, it in enumerate(items):
            if isinstance(it, str):
                slots.append({"order": i + 1, "ref": it, "ph": False})
                implicit = True
                continue
            if not isinstance(it, dict):
                ac.die(f"--bindings 中 {label} 第 {i + 1} 项既不是对象也不是字符串")
            order = next((it[k] for k in ("order", "index", "slot", "position") if k in it), None)
            ref = next((str(it[k]) for k in ("ref", "id", "image", "name", "value") if it.get(k) is not None), "?")
            try:
                order = None if isinstance(order, bool) or order is None else int(str(order).strip())
            except (TypeError, ValueError):
                order = None
            slots.append({"order": order, "ref": ref, "ph": bool(it.get("placeholder"))})
        if implicit:
            notes.append(Finding("info", "SLOT-format", f"{label} 的绑定项未写 order，按列表顺序视为 1..{len(slots)}", label))
        out[label] = slots
    return out, notes


def analyze(prompts: str | Path | None = None, bindings: str | Path | None = None, simulate: bool = False,
            assets_dir: str | Path | None = None, shot_opt: str | None = None) -> tuple[list[Finding], dict]:
    if not prompts and not bindings:
        ac.die("至少给 video-prompts.md 或 --bindings 其一")
    for p in (prompts, bindings):
        if p and not Path(p).is_file():
            ac.die(f"文件不存在：{p}")
    assets = _assets_index(assets_dir)
    findings: list[Finding] = []
    sim_log: list[str] = []
    shots = {}
    if prompts:
        lst, ptext, bom = _parse_prompts_compat(prompts)
        pname = Path(prompts).name
        if bom:
            findings.append(Finding("warn", "FMT-bom", f"{pname} 以 UTF-8 BOM 开头（format-contracts §0.1）：已去 BOM 解析；其他按契约读首行"
                                    f"的工具会漏读首镜 → 去掉 BOM：`sed -i '1s/^\\xEF\\xBB\\xBF//' {pname}`", pname))
        bad_heads = _bad_headings(ptext)
        for ln, raw, sug, prev, swallowed in bad_heads:
            msg = (f"镜头标题「{raw}」落在代码块里（上一个 ``` 没闭合，或外层套了 ````）：这一镜完全没被解析" + (f"，被吞进了 {prev} 的代码块，{prev} 的结论也不可信" if prev else "") + " → 在上一镜禁令句后补一行 ``` 闭合代码块（或去掉外层围栏）后重跑" if swallowed else
                   f"标题「{raw}」没有被识别为镜头（契约：`## SHOT-nnn`），这一镜的 references 完全没被检查"
                   + (f"，其元数据可能被并进上一镜 {prev}" if prev else "") + f" → 改为 `## {sug}` 后重跑")
            findings.append(Finding("error", "FMT-shot-heading", msg, f"{pname}:{ln}",
                                    {"heading": raw, "suggest": sug, "in_code": swallowed}))
        if not lst and not bad_heads:
            ac.die(f"{prompts} 中没有解析到任何 '## SHOT-nnn' 镜（格式见 format-contracts.md §2）")
        for s in lst:
            shots[s["shot"]] = s
            where = f"{s['shot']} {pname}:{s['line']}"
            raw_refs = s["meta"].get("references", "")
            fixed, issues = fix_refs(raw_refs)
            if issues:
                findings.append(Finding("warn", "SLOT-format", f"references 写法不合契约（{'、'.join(issues)}）：「{raw_refs}」→ 改为半角 "
                                        "'1=ID; 2=ID'（分号分隔）；本次已按纠正后的编号检查（prompt_lint 会就此报 VP-picture error）",
                                        where, {"raw": raw_refs}))
            slots = [{"order": n, "ref": r, "ph": False} for n, r in ac.parse_references(fixed)]
            pathy = [x["ref"] for x in slots if IMG_EXT.search(x["ref"]) or "/" in x["ref"] or "\\" in x["ref"]]
            if pathy:
                findings.append(Finding("warn", "SLOT-format", f"references 里写了路径/文件名 {pathy} → 契约写参考 ID（如 "
                                        f"'{ref_key(pathy[0])}'）；本次已按去扩展名后的 ID 比对（E2：写死路径会在改号/搬目录后残留）", where))
            findings.extend(mark_placeholders(slots, s, s["shot"], assets))
            findings.extend(check_slots(s["shot"], slots, s, s["shot"], where, simulate, sim_log, "references"))
            findings.extend(check_first_frame(s, where))
    if bindings:
        groups, notes = load_bindings(bindings, shot_opt)
        findings.extend(notes)
        bname = Path(bindings).name
        for label, slots in groups.items():
            sid = label if re.match(r"^SHOT-\d{3}$", label) else (shot_opt or "")
            shot = shots.get(sid)
            where = f"{label} {bname}"
            findings.extend(mark_placeholders(slots, shot, sid, assets))
            findings.extend(check_slots(f"{label}（绑定）", slots, shot, sid, where, simulate, sim_log, "绑定列表"))
            if shot is not None:
                own = own_start(sid)
                b_ids = [ref_key(x["ref"]) for x in sorted([x for x in slots if x["order"] is not None], key=lambda x: x["order"])
                         if not (x["order"] == 1 and ref_key(x["ref"]) == own and not x["ph"])]
                r_ids = [ref_key(r) for _, r in sorted([t for t in ac.parse_references(fix_refs(shot["meta"].get("references", ""))[0])
                                                        if t[0] is not None])]
                if set(b_ids) == set(r_ids) and b_ids != r_ids:
                    findings.append(Finding("error", "SLOT-bind-mismatch", f"绑定列表的参考图顺序 {b_ids} 与 references 顺序 {r_ids} 不同"
                                            "（T-2：<Picture N> 按 references 编号 → 会指向错误的图）→ 按 references 重新导出绑定，"
                                            "或先改 references 与提示词再导出", where))
                elif set(b_ids) != set(r_ids):
                    only_b, only_r = sorted(set(b_ids) - set(r_ids)), sorted(set(r_ids) - set(b_ids))
                    findings.append(Finding("warn", "SLOT-bind-mismatch", f"绑定列表与 references 不是同一组参考图：仅绑定有 {only_b or '无'}，"
                                            f"仅 references 有 {only_r or '无'}（E4：参考图与提示词必须同一事实）→ 以验收后的那份为准，"
                                            "回写另一份", where))
            elif prompts and sid:
                findings.append(Finding("warn", "SLOT-bind-mismatch", f"绑定列表中的 {sid} 在 {Path(prompts).name} 里不存在 → 核对镜号（E2 改号残留？）",
                                        where))
            elif prompts:
                findings.append(Finding("warn", "SLOT-format", f"{bname} 是单镜列表但没给 --shot：只检查了列表本身，没有与 references 核对顺序 → "
                                        "加 --shot SHOT-nnn 重跑（顺序不一致 = <Picture N> 指错图，T-2）", where))

    bad_shots = sorted({f.where.split()[0] for f in findings if f.level == "error"
                        and f.code in ("SLOT-contiguous", "SLOT-placeholder-pos", "SLOT-sim")})
    summary = []
    if simulate:
        summary.append("删除占位槽模拟（--simulate-remove-placeholder）：")
        summary.extend(sim_log or ["  （没有任何槽位）"])
    if len(bad_shots) >= 2:
        summary.append(f"集体失败模式：{len(bad_shots)} 镜同型（{', '.join(bad_shots[:8])}{'…' if len(bad_shots) > 8 else ''}）——委托方实证 E1："
                       "一次 18 镜、一次 16 镜集体失败。根因在生成 references 的模板/脚本（占位槽默认排第 1 位）→ 批量修模板：占位槽一律放末位，"
                       "再整体重跑本检查，而不是逐镜手改。")
    elif bad_shots:
        summary.append(f"E1 型失败：{bad_shots[0]}。")
    if assets is None and prompts:
        summary.append("（未给 --assets-dir：本镜起始帧是否已产出只按 first_frame 元数据判断）")
    return findings, {"summary": "\n".join(summary), "simulation": sim_log, "e1_shots": bad_shots}


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[bool] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        results.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  —— {detail}" if detail and not cond else ""))

    good, bad, own = ac.FIXTURES / "good", ac.FIXTURES / "bad", ac.FIXTURES / "slot_order_check"

    f, _ = analyze(good / "video-prompts.md", simulate=True)
    check("good: 0 error 0 warn", not [x for x in f if x.level in ("error", "warn")], str([(x.code, x.msg[:40]) for x in f]))
    f, _ = analyze(good / "video-prompts.md", bindings=own / "bindings-good.json", shot_opt="SHOT-002")
    check("good + 一致的绑定列表: 0 error", not [x for x in f if x.level == "error"], str([(x.code, x.msg[:60]) for x in f]))

    f, _ = analyze(bad / "video-prompts.md")
    c3 = [x for x in f if x.where.startswith("SHOT-003") and x.code == "SLOT-contiguous"]
    check("bad SHOT-003: references 从 2 起 → SLOT-contiguous error，并点名 E1 现场",
          bool(c3) and c3[0].level == "error" and "E1 现场" in c3[0].msg)
    check("bad SHOT-003: 给出重编号方案 1=CHR-SUXIAO-BOARD; 2=CHR-STONEGOD-BOARD",
          bool(c3) and "1=CHR-SUXIAO-BOARD; 2=CHR-STONEGOD-BOARD" in c3[0].msg)
    check("bad SHOT-005: first_frame 为空 → SLOT-first-frame warn",
          any(x.where.startswith("SHOT-005") and x.code == "SLOT-first-frame" and x.level == "warn" for x in f))

    f, ex = analyze(own / "video-prompts.md", simulate=True)

    def codes(shot: str, level: str = "error") -> set:
        return {x.code for x in f if x.where.startswith(shot) and x.level == level}
    check("own SHOT-010: 起始帧占位在第 1 位 → SLOT-placeholder-pos + SLOT-sim error",
          {"SLOT-placeholder-pos", "SLOT-sim"} <= codes("SHOT-010"), str(codes("SHOT-010")))
    pp = [x for x in f if x.where.startswith("SHOT-010") and x.code == "SLOT-placeholder-pos"]
    check("own SHOT-010: 方案 = 占位放末位 + <Picture 2>→<Picture 1> 改写表",
          bool(pp) and "1=CHR-SUXIAO-BOARD; 2=CHR-STONEGOD-BOARD; 3=REF-SHOT010-START(占位)" in pp[0].msg
          and "<Picture 2>→<Picture 1>" in pp[0].msg, pp[0].msg if pp else "")
    check("own SHOT-010: 正文引用占位槽 <Picture 1> → SLOT-placeholder-ref warn", "SLOT-placeholder-ref" in codes("SHOT-010", "warn"))
    check("own SHOT-011: 占位在末位 → 0 error，模拟删除后仍连续",
          not codes("SHOT-011") and "SLOT-sim" in codes("SHOT-011", "info"), str(codes("SHOT-011")))
    check("own SHOT-012: PLACEHOLDER 在中间 → SLOT-placeholder-pos + SLOT-sim error",
          {"SLOT-placeholder-pos", "SLOT-sim"} <= codes("SHOT-012"))
    check("own SHOT-013: 元数据 占位: 1 → SLOT-placeholder-pos error", "SLOT-placeholder-pos" in codes("SHOT-013"))
    check("own SHOT-014: first_frame 指向别的镜 → SLOT-first-frame warn", "SLOT-first-frame" in codes("SHOT-014", "warn"))
    check("own: ≥2 镜同型 → 摘要报告集体失败模式", "集体失败模式" in ex["summary"], ex["summary"][-200:])

    f, _ = analyze(own / "video-prompts.md", bindings=own / "bindings.json")
    b12 = [x for x in f if x.where.startswith("SHOT-012 bindings.json")]
    check("bindings(dict): SHOT-012 导出后编号 [1,3] → SLOT-contiguous error",
          any(x.code == "SLOT-contiguous" and x.level == "error" for x in b12), str([(x.code, x.level) for x in b12]))
    check("bindings(dict): SHOT-010 placeholder:true 在第 1 位 → SLOT-placeholder-pos error",
          any(x.where.startswith("SHOT-010 bindings.json") and x.code == "SLOT-placeholder-pos" for x in f))
    f, _ = analyze(bindings=own / "bindings-list.json", shot_opt="SHOT-010")
    check("bindings(list)+--shot: 只剩 2,3 → SLOT-contiguous error（E1 现场）",
          any(x.code == "SLOT-contiguous" and "E1 现场" in x.msg for x in f))

    with tempfile.TemporaryDirectory() as td:
        # 复现 18 镜集体失败：每镜占位起始帧槽都排在第 1 位
        lines = ["# 18 镜集体失败复现\n"]
        for i in range(1, 19):
            lines.append(f"## SHOT-{i:03d}\n- 时长: 8.00\n- 帧数: 192\n- first_frame: —\n"
                         f"- references: 1=REF-SHOT{i:03d}-START; 2=CHR-SUXIAO-BOARD; 3=REF-SHOT{max(i - 1, 1):03d}-START\n")
        vp = Path(td) / "video-prompts.md"
        vp.write_text("\n".join(lines), encoding="utf-8")
        f, ex = analyze(vp, simulate=True)
        sims = [x for x in f if x.code == "SLOT-sim" and x.level == "error"]
        check("synthetic 18 镜：删除占位模拟 18 镜全部 SLOT-sim error，摘要报集体失败",
              len(sims) == 18 and "18 镜同型" in ex["summary"], f"{len(sims)} / {ex['summary'][:80]}")
        # --assets-dir：起始帧已产出 → 不是占位
        (Path(td) / "assets").mkdir()
        (Path(td) / "assets" / "REF-SHOT001-START.png").write_bytes(b"x")
        vp2 = Path(td) / "vp2.md"
        vp2.write_text("## SHOT-001\n- first_frame: REF-SHOT001-START\n- references: 1=REF-SHOT001-START; 2=CHR-A-BOARD\n"
                       "## SHOT-002\n- first_frame: REF-SHOT002-START\n- references: 1=REF-SHOT002-START; 2=CHR-A-BOARD\n",
                       encoding="utf-8")
        f, _ = analyze(vp2, assets_dir=Path(td) / "assets")
        check("--assets-dir: 已产出的起始帧在第 1 位合法；未产出的在第 1 位 → error",
              not [x for x in f if x.where.startswith("SHOT-001") and x.level == "error"]
              and any(x.where.startswith("SHOT-002") and x.code == "SLOT-placeholder-pos" for x in f))
        mism = Path(td) / "mism.json"
        mism.write_text(json.dumps({"SHOT-002": [{"order": 1, "ref": "CHR-STONEGOD-BOARD"},
                                                 {"order": 2, "ref": "CHR-SUXIAO-BOARD"},
                                                 {"order": 3, "ref": "REF-SHOT001-START"}]}), encoding="utf-8")
        f, _ = analyze(good / "video-prompts.md", bindings=mism)
        check("bindings 顺序与 references 不同 → SLOT-bind-mismatch error",
              any(x.code == "SLOT-bind-mismatch" and x.level == "error" for x in f))

        # ---- 对抗回归
        adv = ("## SHOT-001\n- first_frame: assets/keyframes/REF-SHOT001-START.png\n"
               "- references: 1=REF-SHOT001-START.png; 2=CHR-TODOROKI-BOARD\n\n"
               "## SHOT-002\n- first_frame: REF-SHOT002-START\n- references: 1=CHR-A-BOARD，2=CHR-B-BOARD；3=REF-SHOT001-START\n"
               "- 占位: 3=REF-SHOT001-START\n\n"
               "## SHOT-003\n- first_frame: REF-SHOT003-START\n- references: 1＝REF-TBD-START; 2＝CHR-A-BOARD\n- 占位: 否\n")
        (Path(td) / "adv.md").write_bytes(("﻿" + adv).replace("\n", "\r\n").encode("utf-8"))
        f, ex = analyze(Path(td) / "adv.md", simulate=True)

        def at(shot: str, code: str) -> list:
            return [x for x in f if x.where.startswith(shot) and x.code == code]
        check("对抗：CHR-TODOROKI-BOARD 不是占位（TODO 须为独立段）；REF-TBD-START 是",
              "CHR-TODOROKI-BOARD(占位)" not in " ".join(ex["simulation"]) and bool(at("SHOT-003", "SLOT-placeholder-pos")),
              str(ex["simulation"]))
        check("对抗：first_frame 写成路径 .png → SLOT-format warn，不误报'不是本镜起始帧'",
              bool(at("SHOT-001", "SLOT-format")) and not at("SHOT-001", "SLOT-first-frame"))
        check("对抗：references 全角逗号/等号 → SLOT-format warn，按纠正后编号核对（不报 SLOT-number / SLOT-contiguous）",
              len(at("SHOT-002", "SLOT-format")) == 1 and not at("SHOT-002", "SLOT-contiguous")
              and not at("SHOT-003", "SLOT-number"))
        check("对抗：`占位: 3=REF-…` 被识别（末位，删后 [1, 2] 连续）；`占位: 否` 不当占位",
              any("SHOT-002" in ln and "删除占位后 [1, 2] ✓" in ln for ln in ex["simulation"]))
        check("对抗：BOM+CRLF 首行即 ## SHOT-001 仍被检查", bool(at("SHOT-001", "SLOT-format")) and any(x.code == "FMT-bom" for x in f))
        (Path(td) / "adv2.md").write_text(adv + "\n## SHOT-4\n- references: 1=X\n", encoding="utf-8")
        f, _ = analyze(Path(td) / "adv2.md")
        check("对抗：`## SHOT-4` → FMT-shot-heading，并点明其元数据被并进上一镜 SHOT-003（修复前：静默覆盖 SHOT-003 的 references）",
              any(x.code == "FMT-shot-heading" and "SHOT-003" in x.msg and "SHOT-004" in x.msg for x in f))
        bj = Path(td) / "b.json"
        bj.write_bytes("﻿".encode("utf-8") + json.dumps({"shot-002": [{"index": 0, "ref": "CHR-A"},
                                                                          {"index": 1, "ref": "CHR-B"}]}).encode("utf-8"))
        f, _ = analyze(bindings=bj)
        check("对抗：绑定 JSON 带 BOM + 小写镜号键 → 读入并报 SLOT-format；0 基 index → SLOT-contiguous 提示'从 0 起'",
              any(x.code == "SLOT-format" for x in f) and any(x.code == "SLOT-contiguous" and "从 0 起" in x.msg for x in f))
        bl = Path(td) / "list.json"
        bl.write_text(json.dumps([{"order": 1, "ref": "CHR-STONEGOD-BOARD"}, {"order": 2, "ref": "CHR-SUXIAO-BOARD"}]), encoding="utf-8")
        f, _ = analyze(good / "video-prompts.md", bindings=bl)
        check("对抗：单镜列表 + 提示词但没给 --shot → SLOT-format warn（修复前：静默跳过与 references 的核对）",
              any(x.code == "SLOT-format" and "--shot" in x.msg for x in f))

        me = [sys.executable, str(Path(__file__).resolve())]
        p = subprocess.run(me + [str(good / "video-prompts.md")], capture_output=True, text=True)
        check("CLI good → 退出码 0", p.returncode == 0, p.stdout[-200:])
        p = subprocess.run(me + [str(own / "video-prompts.md"), "--simulate-remove-placeholder", "--json"],
                           capture_output=True, text=True)
        try:
            js = json.loads(p.stdout)
            okj = p.returncode == 1 and js["simulation"] and js["counts"]["error"] > 0
        except (ValueError, KeyError):
            okj = False
        check("CLI own --simulate --json → 退出码 1 且含 simulation", okj, p.stdout[:200])
        p = subprocess.run(me, capture_output=True, text=True)
        check("CLI 无输入 → 退出码 2", p.returncode == 2)
        bad_json = Path(td) / "bad.json"
        bad_json.write_text("{not json", encoding="utf-8")
        p = subprocess.run(me + ["--bindings", str(bad_json)], capture_output=True, text=True)
        check("CLI 坏 JSON → 退出码 2", p.returncode == 2)

    print(f"SELFTEST {'PASS' if all(results) else 'FAIL'}（{sum(results)}/{len(results)}）")
    return 0 if all(results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompts", nargs="?", help="video-prompts.md")
    ap.add_argument("--bindings", help="ComfyUI 导出的绑定列表 JSON")
    ap.add_argument("--shot", help="单镜绑定列表对应的镜号，如 SHOT-012")
    ap.add_argument("--simulate-remove-placeholder", action="store_true", help="打印删除占位槽后的编号并检查连续性（E1 复现）")
    ap.add_argument("--assets-dir", help="素材目录：用 REF-SHOTnnn-START.* 是否存在判断起始帧是否已产出")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="用 fixtures 与合成样例自测")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.prompts and not a.bindings:
        ap.print_usage(sys.stderr)
        ac.die("需要 video-prompts.md 或 --bindings（或 --selftest）")
    if a.shot:
        a.shot = a.shot.strip().upper()
    if a.shot and not re.match(r"^SHOT-\d{3}$", a.shot):
        ac.die(f"--shot 需形如 SHOT-012：{a.shot}")
    findings, extra = analyze(a.prompts, a.bindings, a.simulate_remove_placeholder, a.assets_dir, a.shot)
    return ac.emit(TITLE, findings, a.json, extra)


if __name__ == "__main__":
    sys.exit(main())
