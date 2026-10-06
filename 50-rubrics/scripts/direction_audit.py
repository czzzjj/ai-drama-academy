#!/usr/bin/env python3
"""方位词全量审计 direction_audit —— 提示词定稿前必跑；审计不通过 = 提示词不得定稿。

用途：
  逐镜列出 video-prompts.md 中**每一处**方位/横向词（含 ±40 字上下文），按"它在指挥谁"分类：
    (a) DIR-camera  相机左右维度运动：truck / arc / orbit / weave / circle / pan / crab / 360 / sideways，
                    以及相机作主语时的 around / behind / left / right / turn。
                    轴线策略=单轴定侧（或未声明，默认单轴）且无 `- 换边:` 元数据 → error（A5 r4→r5：相机只动高度与距离，M4）；
                    已声明 换边 → visual（需起始帧支持证据）；轴线策略为其他值但没写 换边 理由 → warn。
    (b) DIR-side    附着在主体上的 LEFT/RIGHT（"[S1] … on the RIGHT"、"the god on the LEFT"）→ 经 角色映射（S1=苏晓）
                    对到 起始帧方位；无起始帧条目时对 subject_definitions 的 [S#] 声明。矛盾 → error，一致 → info。
    (c) DIR-path    主体路径词：behind / around / weave / flank / circle / sidestep / switch sides / cross over / 绕到身后 / 换边
                    → warn「空间连续跳变风险（A5③）」。
    (d) DIR-check   其余所有命中（turn / toward / front / 角色自身左右 right hand / 台词里的方位词 / 代词无法解析）
                    → visual「需目视核对」。
        DIR-negated 处在否定句里的方位词（never trucks / no orbit / 不绕）→ info，不计矛盾。
  另：DIR-layout  给 --storyboard 时，分镜 起始帧方位 ≠ 提示词 起始帧方位 → error（P7 双文档对账）。
      DIR-mapping 起始帧方位 ≥2 人却缺 角色映射 → error（审计无法把 [S#] 对上起始帧）；映射名不在起始帧方位中 → warn。
      DIR-axis    有人物却未声明 轴线策略，或取值不认识 → warn（按单轴定侧审计）。
      FMT-shot-heading  疑似镜头标题不合 `## SHOT-nnn`（该镜未被审计）→ error；FMT-bom 文件带 BOM → warn（已去 BOM 解析）。
  判定口径（防假通过）：`换边: 否/无/no` 视同未声明；轴线策略 只有明确写"换边/双轴/越轴"才按非单轴审计，
  其余写法（单侧、定侧、single-axis、拼错）一律按单轴定侧审计。起始帧方位 的 `左/右/中`、全角 ＝、名字中的空格先归一再核对，
  并报 DIR-layout warn 让人改回契约写法。名词用法（a delivery truck / frying pan）与角色自身左右（左手 / right hand）记需目视。
      分镜 运镜 列（相机主语）与 内容 列（主体主语）同样逐词审计，where 中标明列名。
  报告最后一行固定为「方位词审计：通过（0 处矛盾）」或「方位词审计：不通过（N 处矛盾）」，N = error 数。
  脚本只报告事实：哪个词、在哪、指挥谁、与哪条声明矛盾；"好不好看"不判。

溯源：A5（空间调度混乱：r4「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」→ r5 单轴定侧 + 方位词全量审计达标）,
     M4（单轴定侧 / 方位词全量审计 / 画面位置称呼）；另 P4（起始帧钉死方位）、P7（双文档对账）、C1-6（角色自身左右需放大核验）。

输入格式：70-playbooks/format-contracts.md §2 视频提示词（元数据 起始帧方位 / 轴线策略 / 角色映射 / 换边）、§1 分镜表
          （相对本文件：../../70-playbooks/format-contracts.md）

用法示例：
  python3 50-rubrics/scripts/direction_audit.py season-01/ep03/video-prompts.md --storyboard season-01/ep03/storyboard.md
  python3 50-rubrics/scripts/direction_audit.py season-01/ep03/video-prompts.md --json > qc/direction_audit.json
  python3 50-rubrics/scripts/direction_audit.py --selftest
  修法速查：(a) 删掉左右运镜，改 push-in / pull-back / tilt up / crane up；(b) 让文字服从起始帧；
            (c) 改同侧直线进退或拆新镜；(d) 打开起始帧/关键帧逐处看。

退出码：0 通过（0 处矛盾）/ 1 有矛盾（error）/ 2 用法或环境错误
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import academy_common as ac  # noqa: E402
from academy_common import Finding  # noqa: E402

TITLE = "方位词全量审计 direction_audit"

# ------------------------------------------------------------------ 词表
EN_PATTERNS = [
    ("cam", r"\btruck(?:s|ed|ing)?\b|\borbit(?:s|ed|ing)?\b|\bpan(?:s|ned|ning)?\b|\bcrab(?:s|bed|bing)?\b"),
    ("deg", r"\b360(?:\s*°|-degrees?|\s+degrees?)?"),
    ("lat", r"\bsideways\b|\blateral(?:ly)?\b"),
    ("pathv", r"\barc(?:s|ed|ing)?\b|\bcircl(?:e|es|ed|ing)\b|\bweav(?:e|es|ed|ing)\b|\bwove\b|\bflank(?:s|ed|ing)?\b"
              r"|\bside-?step(?:s|ped|ping)?\b|\b(?:switch(?:es|ed|ing)?|swap(?:s|ped|ping)?|chang(?:e|es|ed|ing))\s+sides\b"
              r"|\bcross(?:es|ed|ing)?\b(?!-)(?=\s+(?:over\b|to\s+the\s+other\s+side|the\s+(?:axis|line|frame|screen)\b"
              r"|behind\b|in\s+front\b))"),
    ("pathp", r"\baround\b|\bbehind\b"),
    ("side", r"\b(?:left|right)(?:wards?)?\b"),
    ("turn", r"\bturn(?:s|ed|ing)?\b"),
    ("toward", r"\btowards?\b"),
    ("front", r"\bin\s+front\s+of\b|\bfront\b"),
]
CN_PATTERNS = [
    ("cn_cam", r"环绕|横移|侧移|平移|环拍|绕拍|(?:向|往|朝)?[左右]侧?(?:平移|横移|移|摇|甩)|横摇|甩镜|弧线运镜|弧形运镜|三百六十度|360度"),
    ("cn_path", r"(?:绕|闪|转|跑|冲|溜|窜|移|钻)(?:到|至)[^，。；！？\s]{0,6}?(?:身后|背后)|绕到|绕行|绕过|绕|换边|换位"),
    ("cn_pos", r"身后|背后"),
    ("cn_turn", r"[左右]转|转身|转向"),
    ("cn_body", r"[左右](?=[手臂肩腿脚足眼耳脸颊腰膝拳掌肘腕胸肋臀踝指])"),
    ("cn_side", r"(?:向|往|朝)?[左右]"),
]
_GAPW = r"(?:the|a|an|to|its|his|her|their|slowly|quickly|fully|halfway|over|back|out|off|up|further|farther)"
MOTION_VERBS = (
    r"move|moves|moved|moving|run|runs|ran|running|step|steps|stepped|stepping|slip|slips|slipped|slipping|go|goes|went|"
    r"going|get|gets|got|getting|dash|dashes|dashed|dashing|roll|rolls|rolled|rolling|dart|darts|darted|darting|come|comes|"
    r"came|coming|land|lands|landed|landing|leap|leaps|leapt|leaped|leaping|jump|jumps|jumped|jumping|dodge|dodges|dodged|"
    r"dodging|sweep|sweeps|swept|sweeping|travel|travels|traveled|travelled|traveling|travelling|glide|glides|glided|gliding|"
    r"drift|drifts|drifted|drifting|slide|slides|slid|sliding|spin|spins|spun|spinning|whip|whips|whipped|whipping|sprint|"
    r"sprints|sprinted|sprinting|charge|charges|charged|charging|rush|rushes|rushed|rushing|walk|walks|walked|walking|pace|"
    r"paces|paced|pacing|swing|swings|swung|swinging|track|tracks|tracked|tracking|dolly|dollies|dollied|dollying|shift|"
    r"shifts|shifted|shifting|reappear|reappears|reappeared|appear|appears|appeared|vanish|vanishes|vanished|lunge|lunges|"
    r"lunged|lunging|retreat|retreats|retreated|retreating|back|backs|backed|backing")
SMALL_GAP = re.compile(rf"^\s+(?:{_GAPW}\s+){{0,2}}$", re.I)
MOTION_BEFORE = re.compile(rf"\b(?:{MOTION_VERBS})\s+(?:{_GAPW}\s+){{0,2}}$", re.I)

CAMERA_AGENT = re.compile(r"\b(?:camera|cam|lens|POV|viewpoint|push-?in|pull-?back|pull-?out|dolly|crane\s+shot|"
                          r"tracking\s+shot|the\s+shot|framing)\b|镜头|相机|机位", re.I)
PRONOUN = re.compile(r"\b(?:she|he|they|her|him|his|it|its|them)\b|她|他|它", re.I)
ID_RE = re.compile(r"\[([A-Z][A-Za-z]{0,3}\d{1,3})\]")
CLAUSE_BOUND = re.compile(r"[,;:.!?\n，；：。！？→]|\b(?:while|whilst|whereas|as|then|but|until|when|before|after)\b", re.I)
SENT_BOUND = re.compile(r"[.!?\n。！？]")
HARD_BOUND = re.compile(r"[;:.!?\n；：。！？]|\b(?:but|then|while|whilst|whereas|however|until|instead)\b", re.I)
NEG_EN = re.compile(r"\b(?:no|not|never|without|nor|neither)\b|n't", re.I)
NEG_CN = re.compile(r"(?:不|没有|禁止|避免|别|勿)[^，。；！？\n]{0,4}$")
POS_BEFORE = re.compile(r"(?:\b(?:on|at|in|from|to)\s+(?:the\s+)?(?:far\s+|screen\s+|frame\s+|image\s+)?"
                        r"|\b(?:screen|frame)[-\s])$", re.I)
POS_AFTER = re.compile(r"^\s*(?:side|half|third|edge)\s+of\s+(?:the\s+)?(?:frame|screen|image|shot|picture)\b", re.I)
BODY_AFTER = re.compile(r"^(?:-handed\b|[\s-]*(?:hand|hands|arm|arms|forearm|forearms|shoulder|leg|legs|foot|feet|fist|palm|"
                        r"wrist|elbow|knee|hip|eye|eyes|cheek|ear|thigh|shin|brow|temple|wing|claw|paw|horn|flank|side|"
                        r"sleeve|boot|glove)\b)", re.I)
POSS_BEFORE = re.compile(r"(?:\b(?:her|his|its|their|one's)|'s)\s+$", re.I)
SECTION_LINE = re.compile(r"^([a-z_]+):", re.M)

CAMERA_LATERAL = {"cam", "pathv", "lat", "deg", "turn"}
# 名词用法：a delivery truck / a frying pan / in orbit —— 不是运镜
NOUN_BEFORE = re.compile(r"\b(?:a|an|the|this|that|its|his|her|their|my|your|our|in|into|of|frying|delivery|pickup|fire|"
                         r"cooking|iron|dump|garbage|cargo|army|military|old|rusty|wooden|metal|clay|copper|golden|silver)\s+$",
                         re.I)
STRONG_NOUN_BEFORE = re.compile(r"\b(?:frying|delivery|pickup|fire|cooking|dump|garbage|cargo|army|military)\s+$", re.I)
# 只有相机会做的动作：没有其他主语时 "Slow dolly left." 视同相机主语
CAM_ONLY_VERB = re.compile(r"(?:dolly|dollies|dollied|dollying|track|tracks|tracked|tracking|crane|cranes|craned|craning)\b",
                           re.I)
# 否定词后紧跟这些词时视为并列否定清单（never trucks and arcs），'and' 不打断否定作用域
LISTABLE = re.compile(r"(?:trucks?|trucked|trucking|arcs?|arced|arcing|orbits?|orbited|orbiting|pans?|panned|panning|crabs?|"
                      r"circles?|circled|circling|weaves?|weaving|moves?|moving|go|goes|going|turns?|turning|cross|crosses|"
                      r"crossing|switch(?:es)?|switching|swaps?|swapping|sidesteps?|flanks?|side|sides|sideways|lateral(?:ly)?|"
                      r"left|right|on|to|in|at|around|behind|360)", re.I)
AXIS_SWITCH = re.compile(r"换边|双轴|越轴|跨轴|switch|cross", re.I)
AXIS_SINGLE = re.compile(r"单轴|定侧|单侧|同侧|一侧|固定|single|one[- ]?side|fixed", re.I)
NEG_VALUE = re.compile(r"^\s*(?:否|无|不|没有|不用|不需要|不换边|未声明|no|none|false|off|n/?a|0)\s*(?:[（(].*)?$", re.I)
LAYOUT_ALIASES = {"左": "LEFT", "左侧": "LEFT", "右": "RIGHT", "右侧": "RIGHT", "中": "CENTER", "中间": "CENTER", "居中": "CENTER",
                  "中央": "CENTER", "前景": "FG", "背景": "BG", "CENTRE": "CENTER", "MIDDLE": "CENTER", "L": "LEFT", "R": "RIGHT",
                  "FOREGROUND": "FG", "BACKGROUND": "BG"}
RE_STRICT_HEADING = re.compile(r"^##\s+(SHOT-\d{3})\b")              # 与 academy_common.parse_video_prompts 一致
RE_SHOTLIKE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(?:镜头|镜号|镜)?\s*[:：]?\s*shot\s*[-_－—–]?\s*(\d+)", re.I)
RE_SHOT_TOKEN = re.compile(r"shot\s*[-_－—–]?\s*\d+", re.I)


# ------------------------------------------------------------------ 输入容错（只为不漏检/不误报，偏差照报）

def _empty(v: str | None) -> bool:
    return ac.is_empty(v) or bool(re.fullmatch(r"[\s—–\-－─_]*", v or ""))


def _declared(v: str | None) -> bool:
    """`- 换边:` 是否真的声明了豁免：空值、'否/无/no/none' 都不算。"""
    return not _empty(v) and not NEG_VALUE.match(v or "")


def _nkey(name: str) -> str:
    """名字归一：NFKC + 去空白（'苏 晓' == '苏晓'）。"""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", name or ""))


def _name_rx(name: str) -> str:
    return r"\s*".join(re.escape(c) for c in name)


def _storyboard_issues(text: str, name: str) -> list[Finding]:
    """分镜表行宽 ≠ 表头列数（单元格里没转义的 | / 漏写空值 —）→ 该行各列错位；镜号重复 → 只认最后一行。只报事实。"""
    out: list[Finding] = []
    lines = text.splitlines()
    seen: dict[str, int] = {}
    for t in ac.parse_md_tables(text):
        if not all(c in t["header"] for c in ("镜号", "时长(s)")):
            continue
        n = len(t["header"])
        for r in t["rows"]:
            k = len(ac._split_row(lines[r["_line"] - 1]))
            sid = r.get("镜号", "") or "?"
            if k != n:
                out.append(Finding("warn", "FMT-table-row", f"分镜表第 {r['_line']} 行（{sid}）有 {k} 列、表头 {n} 列 → 单元格里的 | 要写成 \\|，"
                                   "空值写 —；这一行之后的列已错位，本脚本对该镜的结论（起始帧方位/对白/时长）在改正前不可信",
                                   f"{sid} {name}:{r['_line']}", {"cells": k, "header": n}))
            if sid in seen:
                out.append(Finding("warn", "FMT-table-row", f"分镜表镜号 {sid} 重复（第 {seen[sid]} 行与第 {r['_line']} 行）→ 集内唯一；"
                                   "本脚本只按最后一行核对", f"{sid} {name}:{r['_line']}"))
            seen[sid] = r["_line"]
    return out


def norm_layout(raw: str) -> tuple[dict, list[str]]:
    """起始帧方位 → {归一名字: LEFT/RIGHT/CENTER/FG/BG}；返回 (结果, 不合契约之处)。"""
    issues: list[str] = []
    if _empty(raw):
        return {}, issues
    s = raw
    if "＝" in s:
        issues.append("全角等号 ＝")
        s = s.replace("＝", "=")
    out = {}
    for part in re.split(r"[;；,，、]", s):
        part = part.strip()
        if not part or _empty(part):
            continue
        if "=" not in part:
            issues.append(f"条目「{part}」没有 '='")
            continue
        k, v = part.split("=", 1)
        k, v = _nkey(k), v.strip()
        vu = unicodedata.normalize("NFKC", v).upper()
        if vu not in ac.LAYOUT_VALUES:
            mapped = LAYOUT_ALIASES.get(v) or LAYOUT_ALIASES.get(vu)
            issues.append(f"{k}={v} 应写成 {mapped}" if mapped else f"{k}={v} 不是 LEFT/RIGHT/CENTER/FG/BG")
            vu = mapped or vu
        out[k] = vu
    return out, issues


def parse_mapping(raw: str) -> dict:
    out = {}
    if _empty(raw):
        return out
    for part in re.split(r"[;；,，、]", raw.replace("＝", "=")):
        if "=" in part:
            k, v = part.split("=", 1)
            if k.strip():
                out[k.strip()] = _nkey(v)
    return out


def _read(path: str | Path) -> tuple[str, bool]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        ac.die(f"{path} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8（无 BOM）后重跑")
    return (text[1:], True) if text.startswith("\ufeff") else (text, False)


def _parse_compat(parser, path: str | Path):
    """academy_common 解析器的 BOM 兼容包装：带 BOM 时解析去 BOM 的临时副本（行号不变）。返回 (结果, 文本, 是否带 BOM)。"""
    path = Path(path)
    text, bom = _read(path)
    if not bom:
        return parser(path), text, False
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / path.name
        tmp.write_text(text, encoding="utf-8")
        out = parser(tmp)
    for s in out:
        if isinstance(s, dict) and "file" in s:
            s["file"] = str(path)
    return out, text, True


def _bom_finding(path: str | Path) -> Finding:
    name = Path(path).name
    return Finding("warn", "FMT-bom", f"{name} 以 UTF-8 BOM 开头（format-contracts §0.1：UTF-8 无 BOM）。本脚本已去 BOM 解析，"
                   f"但其他按契约读首行的工具会漏读首镜/表头 → 去掉 BOM：`sed -i '1s/^\\xEF\\xBB\\xBF//' {name}`，"
                   "或编辑器另存为「UTF-8（无 BOM）」", name)


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


@dataclass
class Hit:
    start: int
    end: int
    cats: set
    lang: str = "en"
    motion: bool = False
    vstart: int = -1

    def span(self) -> tuple[int, int]:
        return (self.vstart if self.vstart >= 0 else self.start), self.end


@dataclass
class Agent:
    kind: str            # camera | subject
    start: int
    end: int
    sid: str | None = None
    name: str | None = None
    pronoun: bool = False
    text: str = ""


# ------------------------------------------------------------------ 扫描

def scan(text: str) -> list[Hit]:
    raw = []
    for cat, pat in EN_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            raw.append((m.start(), m.end(), cat, "en"))
    for cat, pat in CN_PATTERNS:
        for m in re.finditer(pat, text):
            raw.append((m.start(), m.end(), cat, "cn"))
    raw.sort(key=lambda t: (t[0], -(t[1] - t[0])))
    kept, last_end = [], -1
    for s, e, c, lang in raw:
        if s >= last_end:
            kept.append(Hit(s, e, {c}, lang))
            last_end = e
    out: list[Hit] = []
    for h in kept:
        if "side" in h.cats and h.lang == "en" and BODY_AFTER.match(text[h.end:h.end + 20]):
            out.append(h)          # right hand / left forearm：角色自身左右，不与动词合并
            continue
        if out and h.lang == "en" and out[-1].lang == "en":
            prev = out[-1]
            if (h.cats & {"side", "pathp", "deg", "toward"}) and (prev.cats & {"cam", "pathv", "turn", "lat"}) \
                    and SMALL_GAP.match(text[prev.end:h.start]):
                prev.end, prev.motion = h.end, True
                prev.cats |= h.cats
                continue
        if h.lang == "en" and h.cats & {"side", "pathp", "deg", "toward"}:
            lo = max(0, h.start - 40)
            m = MOTION_BEFORE.search(text, lo, h.start)
            if m:
                h.motion, h.vstart = True, m.start()
        out.append(h)
    return out


def _last_bound(rx: re.Pattern, text: str, pos: int, floor: int = 0) -> int:
    s = floor
    for m in rx.finditer(text, floor, pos):
        s = m.end()
    return s


def _ctx40(text: str, s: int, e: int) -> str:
    a, b = max(0, s - 40), min(len(text), e + 40)
    flat = lambda x: x.replace("\n", " ⏎ ")  # noqa: E731
    return ("…" if a else "") + flat(text[a:s]) + "【" + flat(text[s:e]) + "】" + flat(text[e:b]) + ("…" if b < len(text) else "")


def _side_of(word: str) -> str:
    return "LEFT" if "left" in word.lower() or "左" in word else "RIGHT"


# ------------------------------------------------------------------ 每镜上下文

class ShotCtx:
    def __init__(self, shot: dict):
        self.shot = shot
        meta = shot["meta"]
        self.layout, self.layout_issues = norm_layout(meta.get("起始帧方位", ""))
        self.mapping = parse_mapping(meta.get("角色映射", ""))
        self.inv = {v: k for k, v in self.mapping.items()}
        self.axis = meta.get("轴线策略", "")
        self.switch = meta.get("换边", "") if _declared(meta.get("换边", "")) else ""
        self.switch_raw = meta.get("换边", "")
        # 只有明确写了 换边/双轴/越轴 才按非单轴审计；单侧/定侧/拼错/英文 一律按单轴定侧（防假通过）
        self.axis_single = _empty(self.axis) or bool(AXIS_SINGLE.search(self.axis)) or not AXIS_SWITCH.search(self.axis)
        self.axis_unknown = not _empty(self.axis) and not AXIS_SINGLE.search(self.axis) and not AXIS_SWITCH.search(self.axis)
        self.aliases: dict[str, str | None] = {}
        self.declared: dict[str, str] = {}
        sd = shot["sections"].get("subject_definitions", "")
        for ln in sd.splitlines():
            m = re.match(r"^\s*\[([A-Z][A-Za-z]{0,3}\d{1,3})\]\s*(.*)$", ln)
            if not m:
                continue
            sid, rest = m.group(1), m.group(2)
            pm = re.search(r"\b(?:on|at|in)\s+the\s+(?:far\s+)?(LEFT|RIGHT|CENTER|CENTRE)\b", rest, re.I)
            if pm:
                self.declared[sid] = pm.group(1).upper().replace("CENTRE", "CENTER")
            head = re.split(r"[:：,，—–(<]| - ", rest, maxsplit=1)[0]
            head = re.sub(r"\b(?:on|at|in)\s+the\s+(?:far\s+)?(?:left|right|center|centre|foreground|background)\b.*$", "",
                          head, flags=re.I)
            head = re.sub(r"^(?:the|a|an)\s+", "", head.strip(), flags=re.I).strip()
            cands = set()
            if 2 < len(head) <= 40:
                cands.add(head.lower())
                last = head.split()[-1].lower()
                if len(last) > 2 and last not in {"one", "man", "the"}:
                    cands.add(last)
            for c in cands:
                if c in self.aliases and self.aliases[c] != sid:
                    self.aliases[c] = None          # 歧义：两个主体共用同一称呼 → 不解析
                else:
                    self.aliases[c] = sid
        good = [a for a, s in self.aliases.items() if s]
        self.alias_alt = "|".join(re.escape(a) for a in sorted(good, key=len, reverse=True))
        self.alias_rx = re.compile(rf"\b(?:{self.alias_alt})\b", re.I) if good else None
        self.names = sorted(set(self.layout) | set(self.mapping.values()), key=len, reverse=True)

    def agents(self, text: str) -> list[Agent]:
        out = [Agent("camera", m.start(), m.end(), text=m.group(0)) for m in CAMERA_AGENT.finditer(text)]
        for m in ID_RE.finditer(text):
            if m.group(1) != "Chinese":
                out.append(Agent("subject", m.start(), m.end(), sid=m.group(1), name=self.mapping.get(m.group(1)),
                                 text=m.group(0)))
        if self.alias_rx:
            for m in self.alias_rx.finditer(text):
                sid = self.aliases.get(m.group(0).lower())
                out.append(Agent("subject", m.start(), m.end(), sid=sid, name=self.mapping.get(sid or ""), text=m.group(0)))
        for nm in self.names:
            for m in re.finditer(_name_rx(nm), text):
                out.append(Agent("subject", m.start(), m.end(), sid=self.inv.get(nm), name=nm, text=m.group(0)))
        for m in PRONOUN.finditer(text):
            out.append(Agent("subject", m.start(), m.end(), pronoun=True, text=m.group(0)))
        return out

    def expected(self, sid: str | None, name: str | None) -> tuple[str | None, str]:
        if name is None and sid:
            name = self.mapping.get(sid)
        name = _nkey(name) if name else name
        if name and name in self.layout:
            return self.layout[name], f"起始帧方位 {name}={self.layout[name]}"
        if sid and sid in self.declared:
            return self.declared[sid], f"subject_definitions 声明 [{sid}] on the {self.declared[sid]}"
        return None, ""


# ------------------------------------------------------------------ 分类

def _find_agent(agents: list[Agent], hit: Hit, clause_start: int, sent_start: int) -> Agent | None:
    s0 = hit.span()[0]
    c = [a for a in agents if a.start >= clause_start and a.end <= s0]
    if not c:
        c = [a for a in agents if a.start >= sent_start and a.end <= s0]
    return max(c, key=lambda a: (a.end, a.end - a.start)) if c else None


def _negated(text: str, hit: Hit, sent_start: int, ctx: ShotCtx) -> bool:
    if hit.lang == "cn":
        return bool(NEG_CN.search(text[max(0, hit.start - 8):hit.start]))
    lo = max(sent_start, hit.start - 60)
    negs = list(NEG_EN.finditer(text, lo, hit.start))
    if not negs:
        return False
    between = text[negs[-1].end():hit.start]
    if HARD_BOUND.search(between):
        return False
    # 'and' 打断否定作用域（"does not hesitate and circles behind"），除非否定的就是一串方位/运动词（"never trucks and arcs"）
    if re.search(r"\band\b", between):
        first = re.match(r"\s*([A-Za-z0-9]+)", between)
        if not (first and LISTABLE.fullmatch(first.group(1))):
            return False
    subj = r"camera|lens|\[[A-Z][A-Za-z]{0,3}\d{1,3}\]|she|he|they"
    if ctx.alias_rx:
        subj += "|" + ctx.alias_alt
    if re.search(rf",\s*(?:and\s+)?(?:the\s+|a\s+)?(?:{subj})\b", between, re.I):
        return False
    return True


def audit_text(text: str, ctx: ShotCtx, axis_level: str, where_fn, column: str | None = None) -> list[Finding]:
    """逐个命中输出 Finding。column=None 表示 h3 正文；'运镜' 强制相机主语；'内容' 为主体主语。"""
    F: list[Finding] = []
    dialog = [(m.start(), m.end()) for m in re.finditer(r"<d>.*?</d>", text, re.S)]
    agents = ctx.agents(text)
    for h in scan(text):
        s, e = h.span()
        word = text[s:e].replace("\n", " ")
        context = _ctx40(text, s, e)
        where = where_fn(h.start)
        sent_start = _last_bound(SENT_BOUND, text, h.start)
        clause_start = _last_bound(CLAUSE_BOUND, text, s, sent_start)
        cats = h.cats
        data = {"word": word, "context": context, "column": column or "h3"}

        def out(level, code, cls, msg):
            data["class"] = cls
            F.append(Finding(level, code, f"「{word}」{msg} ｜ {context}", where, dict(data)))

        if any(a <= h.start < b for a, b in dialog):
            out("visual", "DIR-check", "d", "台词里的方位词 → 需目视核对：台词说的方向与画面/起始帧方位一致（观众会拿画面验证台词）")
            continue
        if _negated(text, h, sent_start, ctx):
            out("info", "DIR-negated", "neg", "处于否定句（绝对否定写法），不构成矛盾")
            continue

        if column == "运镜":
            agent = Agent("camera", 0, 0, text="运镜列")
        else:
            agent = _find_agent(agents, h, clause_start, sent_start)
            if agent is None and h.lang == "en" and h.vstart >= 0 and CAM_ONLY_VERB.match(text, h.vstart):
                agent = Agent("camera", h.vstart, h.vstart, text=text[h.vstart:h.start].strip())   # "Slow dolly left."
        kind = agent.kind if agent else None
        before, after = text[max(0, h.start - 25):h.start], text[h.end:h.end + 20]
        handed = "side" in cats and bool(BODY_AFTER.match(after) or (not h.motion and POSS_BEFORE.search(before)))
        pos_style = "side" in cats and not h.motion and bool(POS_BEFORE.search(before) or POS_AFTER.match(after))

        # ---- 中文命中
        if h.lang == "cn":
            camera_ctx = column == "运镜" or kind == "camera" or (kind is None and column != "内容" and "cn_cam" in cats)
            if "cn_body" in cats:
                out("visual", "DIR-check", "d-hand", "角色自身左右（左手/右肩…）≠ 画面左右 → 需目视：关键帧放大核验持物手/肢体方位（C1-6），"
                    "与锚点卡 方位属性 一致")
                continue
            if "cn_side" in cats and not camera_ctx:
                nm = next((n for n in ctx.names if re.search(_name_rx(n) + r"\s*(?:在|位于|站在|处于)?\s*(?:画面)?\s*$",
                                                                 text[max(0, h.start - 12):h.start])), None)
                if nm and word[0] not in "向往朝":
                    _side_check(out, ctx, ctx.inv.get(nm), nm, _side_of(word))
                else:
                    out("visual", "DIR-check", "d", "需目视核对：该处左右指画面方位、运动方向还是角色自身左右，与起始帧方位是否一致")
                continue
            if camera_ctx and "cn_side" in cats:
                if word[0] in "向往朝":
                    _camera(out, ctx, axis_level)          # 运镜写"向左/往右" = 左右维度运动
                else:
                    out("visual", "DIR-check", "d", "运镜里的左右若指构图位置（如'推近左侧人物'）属距离维度 → 需目视核对；"
                        "若指运动方向，改写为推/拉/升/降之一")
                continue
            if camera_ctx and cats & {"cn_cam", "cn_path", "cn_turn"}:
                _camera(out, ctx, axis_level)
            elif camera_ctx and "cn_pos" in cats:
                out("visual", "DIR-check", "d", "机位描述（从背后/身后）：不是左右运动，但要核对它与起始帧的轴线同侧 → 需目视")
            elif cats & {"cn_cam", "cn_path"}:
                out("warn", "DIR-path", "c", "主体绕行/换边路径 → 空间连续跳变风险（A5③：r4 '苏晓乱跑'）→ 改为同侧直线进退，保持起始帧方位；"
                    "确需绕行则拆成新镜并重定起始帧")
            else:
                out("visual", "DIR-check", "d", "需目视核对：转身/方位动作与起始帧方位是否一致")
            continue

        # ---- 英文命中
        if cats == {"cam"} and not h.motion and (
                (kind == "camera" and STRONG_NOUN_BEFORE.search(before)) or (kind != "camera" and NOUN_BEFORE.search(before))):
            out("visual", "DIR-check", "d", "名词用法（a truck / frying pan / in orbit），不是运镜 → 需目视确认；"
                "若确指相机运动，改写成 'the camera trucks …' 后重跑")
            continue
        if kind == "camera":
            if cats & CAMERA_LATERAL or (h.motion and cats & {"side", "pathp"}):
                _camera(out, ctx, axis_level)
            else:
                out("visual", "DIR-check", "d", "需目视核对：相机朝向/机位描述与起始帧构图是否一致（推拉 toward 属距离维度，允许）")
            continue
        if "cam" in cats or (kind is None and "deg" in cats):
            _camera(out, ctx, axis_level)
            continue
        if cats & {"pathv", "lat"} or ("pathp" in cats and h.motion):
            who = f"（{agent.text}）" if agent else "（主语不明：若指相机则属 (a) 换边运镜）"
            out("warn", "DIR-path", "c", f"主体路径{who} → 空间连续跳变风险（A5③：重复接近/绕行/换向让空间跳变）→ 改为同侧直线进退"
                "（steps in / drops low / backs away），保持起始帧方位；确需换位则拆新镜并重定起始帧")
            continue
        if "side" in cats:
            if handed:
                out("visual", "DIR-check", "d-hand", "角色自身左右 ≠ 画面左右 → 需目视：关键帧放大核验持物手/肢体方位（C1-6），"
                    "与锚点卡 方位属性 一致")
                continue
            if kind == "subject" and agent is not None and not agent.pronoun and (agent.sid or agent.name):
                if pos_style:
                    _side_check(out, ctx, agent.sid, agent.name, _side_of(word))
                    continue
                if h.motion:
                    exp, _ = ctx.expected(agent.sid, agent.name)
                    d = _side_of(word)
                    if exp in ("LEFT", "RIGHT") and exp != d:
                        out("warn", "DIR-path", "c", f"{agent.text} 起始在 {exp}，却向画面 {d} 移动 → 可能越过对手换边（A5③）"
                            "→ 改为同侧进退或拆新镜")
                    else:
                        out("visual", "DIR-check", "d", "主体横向移动 → 需目视核对不越过对手、不改变左右关系")
                    continue
            if pos_style and agent is not None and agent.pronoun:
                out("visual", "DIR-check", "d", f"代词「{agent.text}」无法解析到 [S#]，方位无法自动核对 → 改用 [S#] 或画面位置称呼"
                    "（A5②）后重跑")
                continue
        out("visual", "DIR-check", "d", "需目视核对：与起始帧方位/镜头动作是否一致；无关则在 QC 记录中注明'已核，无关'")
    return F


def _camera(out, ctx: ShotCtx, axis_level: str) -> None:
    if not ac.is_empty(ctx.switch):
        out("visual", "DIR-camera", "a", f"相机左右维度运动，已声明换边豁免（{ctx.switch}）→ 需目视核对起始帧确实支持该换边，"
            "并在 QC 记录留证据")
    elif ctx.axis_single:
        tag = ctx.axis if not ac.is_empty(ctx.axis) else "未声明（默认单轴定侧）"
        out(axis_level, "DIR-camera", "a", f"相机左右维度运动，与 轴线策略={tag} 矛盾（A5 r4：起始帧钉了左右，trucks/arcs/weaves "
            f"让模型把空间搅乱；r5 相机只动高度与距离后达标，M4）→ 删除，改为 slow push-in / pull-back / tilt up / crane up 之一；"
            "确需换边则元数据加 '- 换边: 设计（理由…；起始帧支持证据…）'")
    else:
        out("warn", "DIR-camera", "a", f"相机左右维度运动；轴线策略={ctx.axis} 但没有 '- 换边:' 理由与起始帧支持证据（A5：换边仅在"
            "设计需要且起始帧支持时允许）→ 补 换边 元数据，或改回单轴定侧")


def _side_check(out, ctx: ShotCtx, sid: str | None, name: str | None, side: str) -> None:
    exp, src = ctx.expected(sid, name)
    who = f"[{sid}]" if sid else ""
    who += f"→{name or ctx.mapping.get(sid or '', '')}" if (name or ctx.mapping.get(sid or "")) else ""
    if exp is None:
        if (name or ctx.mapping.get(sid or "")) and ctx.layout:
            out("warn", "DIR-side", "b", f"{who} 不在 起始帧方位 中，无法核对 → 在元数据 起始帧方位 补上该角色的画面位置")
        else:
            out("visual", "DIR-side", "b", f"{who or '该主体'} 无法对到起始帧方位（缺 角色映射 或 起始帧方位）→ 补元数据后重跑；"
                "现在需目视核对")
        return
    if exp == side:
        out("info", "DIR-side", "b", f"{who} 与 {src} 一致")
    else:
        out("error", "DIR-side", "b", f"{who} 被写在 {side}，但 {src}（A5①：画面左右由起始帧钉死，文字改不动；指令打架模型就搅乱空间）"
            f"→ 改为 'on the {exp}'；若起始帧确实是 {side}，先改 起始帧方位/分镜表并重验关键帧（E4 回写）")


# ------------------------------------------------------------------ 全文件

def analyze(prompts: str | Path, storyboard: str | Path | None = None) -> tuple[list[Finding], dict]:
    for p in (prompts, storyboard):
        if p is not None and not Path(p).is_file():
            ac.die(f"文件不存在：{p}")
    findings: list[Finding] = []
    shots, ptext, bom = _parse_compat(ac.parse_video_prompts, prompts)
    if bom:
        findings.append(_bom_finding(prompts))
    pname = Path(prompts).name
    bad_heads = _bad_headings(ptext)
    for ln, raw, sug, prev, swallowed in bad_heads:
        spill = f"；其下的元数据/代码块不归属任何镜（academy_common 遇到任何标题即结束上一镜，不会再并进上一镜 {prev}）" if prev else ""
        msg = (f"镜头标题「{raw}」落在代码块里（上一个 ``` 没闭合，或外层套了 ````）：这一镜完全没被解析" + (f"，被吞进了 {prev} 的代码块，{prev} 的结论也不可信" if prev else "") + " → 在上一镜禁令句后补一行 ``` 闭合代码块（或去掉外层围栏）后重跑" if swallowed else
               f"标题「{raw}」没有被识别为镜头（契约：`## SHOT-nnn`），这一镜的方位词完全没被审计{spill} → 改为 `## {sug}` 后重跑")
        findings.append(Finding("error", "FMT-shot-heading", msg, f"{pname}:{ln}",
                                {"heading": raw, "suggest": sug, "in_code": swallowed}))
    if not shots and not bad_heads:
        ac.die(f"{prompts} 中没有解析到任何 '## SHOT-nnn' 镜（格式见 format-contracts.md §2）")
    sb, sbtext = {}, ""
    if storyboard:
        rows, sbtext, sbom = _parse_compat(ac.parse_storyboard, storyboard)
        if sbom:
            findings.append(_bom_finding(storyboard))
        findings.extend(_storyboard_issues(sbtext, Path(storyboard).name))
        sb = {r["shot"]: r for r in rows}
        if not sb:
            ac.die(f"{storyboard} 中没有找到含 镜号/时长(s) 表头的分镜表（format-contracts.md §1）")
    per_shot = {}
    for shot in shots:
        ctx = ShotCtx(shot)
        meta, sid = shot["meta"], shot["shot"]
        F: list[Finding] = []
        head = f"{sid} {pname}:{shot['line']}"
        # ---- 元数据层
        if ctx.layout_issues:
            F.append(Finding("warn", "DIR-layout", f"提示词 起始帧方位「{meta.get('起始帧方位', '')}」写法不合契约：{'；'.join(ctx.layout_issues)}"
                             " → 改为 '名=LEFT; 名=RIGHT'（半角 =，取值 LEFT/RIGHT/CENTER/FG/BG）；本次已按归一后的值审计", head))
        if storyboard:
            row = sb.get(sid)
            if row is None:
                F.append(Finding("warn", "DIR-layout", f"分镜表中没有 {sid}，无法核对起始帧方位（P7）→ 在 storyboard.md 补这一行", head))
            else:
                sb_layout, sb_issues = norm_layout(row["layout_raw"])
                sb_where = f"{sid} {Path(storyboard).name}:{row['line']}"
                if sb_issues:
                    F.append(Finding("warn", "DIR-layout", f"分镜 起始帧方位「{row['layout_raw']}」写法不合契约：{'；'.join(sb_issues)}"
                                     " → 改为 '名=LEFT; 名=RIGHT'；本次已按归一后的值核对", sb_where))
                if sb_layout != ctx.layout:
                    F.append(Finding("error", "DIR-layout", f"分镜 起始帧方位「{row['layout_raw']}」≠ 提示词「{meta.get('起始帧方位', '')}」"
                                     f"（P7 双文档对账；A5：方位由起始帧钉死）→ 以已验收起始帧为准，回写不一致的一方（E4）",
                                     sb_where, {"storyboard": sb_layout, "prompt": ctx.layout}))
        if len(ctx.layout) >= 2 and not ctx.mapping:
            F.append(Finding("error", "DIR-mapping", f"起始帧方位有 {len(ctx.layout)} 人（{meta.get('起始帧方位')}）但缺 '- 角色映射:'"
                             "（format-contracts §2 必填）：审计无法把 [S#] 对上起始帧 → 补 '- 角色映射: S1=…; S2=…' 后重跑", head))
        for k, v in ctx.mapping.items():
            if ctx.layout and v not in ctx.layout:
                F.append(Finding("warn", "DIR-mapping", f"角色映射 {k}={v} 不在 起始帧方位（{meta.get('起始帧方位')}）中 → 名字写法统一，"
                                 "或补上该角色的起始位置", head))
        if ctx.layout and _empty(ctx.axis):
            F.append(Finding("warn", "DIR-axis", "有人物却未声明 '- 轴线策略:'，本次按 单轴定侧 审计（A5：全片单轴优先）→ 补 "
                             "'- 轴线策略: 单轴定侧'", head))
        elif ctx.axis_unknown:
            F.append(Finding("warn", "DIR-axis", f"轴线策略「{ctx.axis}」不是契约写法，本次按 单轴定侧 审计（防假通过）→ 改为 "
                             "'单轴定侧'；确需换边则写 '换边' 并补 '- 换边: 设计（理由…；起始帧支持证据…）'", head))
        if not _empty(ctx.switch_raw) and not ctx.switch:
            F.append(Finding("info", "DIR-axis", f"元数据 换边「{ctx.switch_raw}」是否定值，按'未声明换边'审计（不豁免左右运镜）", head))
        # ---- h3 正文
        if shot["h3"] is None:
            F.append(Finding("error", "DIR-layout", "缺 ```h3 代码块，无法审计 → 先修 prompt_lint VP-struct", head))
        else:
            h3 = shot["h3"]
            base = shot["h3_line"]
            secs = [(m.start(), m.group(1)) for m in SECTION_LINE.finditer(h3) if m.group(1) in ac.H3_SECTIONS]

            def where_h3(off: int, _h3=h3, _base=base, _secs=secs) -> str:
                sec = ""
                for o, n in _secs:
                    if o <= off:
                        sec = n
                return f"{sid} {pname}:{_base + _h3.count(chr(10), 0, off)} {sec}".rstrip()
            fs = audit_text(h3, ctx, "error", where_h3)
            # subject_definitions 中的声明本身：缺映射时"与自身声明一致"没有意义 → 降为需目视
            for f in fs:
                if f.code == "DIR-side" and f.level == "info" and "subject_definitions 声明" in f.msg \
                        and f.where.endswith("subject_definitions"):
                    f.level = "visual"
                    f.msg = (f"「{f.data['word']}」只能对上它自身的声明，无法与起始帧方位核对（缺 角色映射，或起始帧方位无此人）"
                             f"→ 补元数据后重跑；现在需目视核对起始帧 ｜ {f.data['context']}")
            F.extend(fs)
        # ---- 分镜 运镜 / 内容 列
        row = sb.get(sid) if storyboard else None
        if row is not None:
            sbn = Path(storyboard).name
            raw_rows = {r["_line"]: r for r in ac.find_rows(sbtext, ["镜号", "时长(s)"])}
            rr = raw_rows.get(row["line"], {})
            for col in ("运镜", "内容"):
                cell = rr.get(col, "")
                if ac.is_empty(cell):
                    continue
                F.extend(audit_text(cell, ctx, "error", lambda off, c=col: f"{sid} {sbn}:{row['line']} {c}列", column=col))
        findings.extend(F)
        cnt = {cls: sum(1 for f in F if f.data.get("class") == cls) for cls in ("a", "b", "c", "d", "d-hand", "neg")}
        per_shot[sid] = {"errors": sum(1 for f in F if f.level == "error"), "hits": cnt}
    n_err = sum(1 for f in findings if f.level == "error")
    verdict = f"方位词审计：{'通过' if n_err == 0 else '不通过'}（{n_err} 处矛盾）"
    lines = []
    for k, v in per_shot.items():
        c = v["hits"]
        lines.append(f"  {k}：相机左右(a) {c['a']} / 主体方位(b) {c['b']} / 主体路径(c) {c['c']} / 需目视(d) "
                     f"{c['d'] + c['d-hand']} / 否定 {c['neg']} → {v['errors']} 处矛盾")
    summary = "逐镜命中：\n" + "\n".join(lines)
    if not storyboard:
        summary += "\n（未给 --storyboard：未做 分镜↔提示词 起始帧方位交叉核对）"
    summary += "\n提示词只有在本审计通过后才算定稿（A5/M4）；需目视项要在 QC 记录中逐条写'已核'。"
    return findings, {"summary": summary, "verdict": verdict, "passed": n_err == 0, "contradictions": n_err,
                      "per_shot": per_shot}


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[bool] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        results.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  —— {detail}" if detail and not cond else ""))

    good, bad, own = ac.FIXTURES / "good", ac.FIXTURES / "bad", ac.FIXTURES / "direction_audit"

    for sbp in (good / "storyboard.md", None):
        f, ex = analyze(good / "video-prompts.md", sbp)
        errs = [(x.code, x.msg[:60]) for x in f if x.level == "error"]
        check(f"good{'+storyboard' if sbp else ''}: 0 error，判定通过", not errs and ex["passed"], str(errs))
    f, ex = analyze(good / "video-prompts.md", good / "storyboard.md")
    side_ok = [x for x in f if x.code == "DIR-side" and x.level == "info"]
    check("good: on the LEFT/RIGHT 经角色映射核对为一致（≥4 处 info）", len(side_ok) >= 4, str(len(side_ok)))
    check("good: 'never moves sideways' 识别为否定句", any(x.code == "DIR-negated" and "sideways" in x.data["word"] for x in f))
    check("good: right hand / right forearm 记为角色自身左右（需目视）",
          sum(1 for x in f if x.data.get("class") == "d-hand") >= 2)

    f, ex = analyze(bad / "video-prompts.md", bad / "storyboard.md")
    e3 = [x for x in f if x.where.startswith("SHOT-003") and x.level == "error" and x.code == "DIR-camera"]
    words = " | ".join(x.data["word"] for x in e3)
    for w in ("trucks left", "arcs around", "orbits 360"):
        check(f"bad SHOT-003: 「{w}」→ DIR-camera error", any(w in x.data["word"] for x in e3), words)
    wv = [x for x in f if x.code == "DIR-path" and "weaves behind" in x.data["word"]]
    check("bad SHOT-003: 「weaves behind」→ DIR-path warn", bool(wv) and wv[0].level == "warn")
    check("bad SHOT-003: 分镜 运镜=环绕 → error", any(x.level == "error" and x.data.get("column") == "运镜" for x in f))
    check("bad SHOT-003: 分镜 内容 绕到身后 → warn", any(x.level == "warn" and "绕到身后" in x.data["word"] for x in f))
    check("bad: 判定不通过（4 处矛盾）", ex["verdict"] == "方位词审计：不通过（4 处矛盾）", ex["verdict"])

    f, ex = analyze(own / "video-prompts.md", own / "storyboard.md")

    def at(shot: str, level: str | None = None, code: str | None = None) -> list:
        return [x for x in f if x.where.startswith(shot) and (level is None or x.level == level)
                and (code is None or x.code == code)]
    s10e = at("SHOT-010", "error")
    check("own SHOT-010: 只有 1 处矛盾 = [S1] 被写在 LEFT（起始帧 苏晓=RIGHT）",
          len(s10e) == 1 and s10e[0].code == "DIR-side" and "subject_definitions" in s10e[0].where,
          str([(x.code, x.where) for x in s10e]))
    check("own SHOT-010: never trucks, arcs or orbits → 3 处否定 info", len(at("SHOT-010", "info", "DIR-negated")) >= 3)
    pw = {x.data["word"] for x in at("SHOT-010", "warn", "DIR-path")}
    check("own SHOT-010: circles behind / 绕到身后 → DIR-path warn", {"circles behind", "绕到身后"} <= pw, str(pw))
    check("own SHOT-010: 台词里的 右 → 需目视", any(x.data.get("class") == "d" and x.data["word"] == "右"
                                               for x in at("SHOT-010", "visual")))
    check("own SHOT-011: 已声明换边 → arcs around 降为需目视，0 error",
          not at("SHOT-011", "error") and len(at("SHOT-011", "visual", "DIR-camera")) >= 2)
    check("own SHOT-012: 缺角色映射 → DIR-mapping error", bool(at("SHOT-012", "error", "DIR-mapping")))
    check("own SHOT-012: 分镜/提示词起始帧方位不一致 → DIR-layout error", bool(at("SHOT-012", "error", "DIR-layout")))

    # ---- 对抗回归（输入在临时目录现场生成）
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        head = ("- 起始帧方位: 石神=LEFT; 苏 晓=RIGHT\n- 角色映射: S1＝苏晓; S2=石神\n")
        body = ("```h3\nsubject_definitions:\n  [S1] the swordswoman on the RIGHT <Picture 1>\n  [S2] the stone god on the LEFT "
                "<Picture 2>\ndetailed_description:\n  {txt}\n" + ac.BAN_LINE + "\n```\n")
        shots = [
            ("SHOT-001", "- 轴线策略: 单轴定侧\n- 换边: 否\n", "The camera trucks left."),
            ("SHOT-002", "- 轴线策略: 单侧\n", "The camera arcs around them."),
            ("SHOT-003", "- 轴线策略: 随意\n", "The camera orbits the pair."),
            ("SHOT-004", "- 轴线策略: 单轴定侧\n", "A delivery truck rumbles past; she holds a frying pan."),
            ("SHOT-005", "- 轴线策略: 单轴定侧\n", "Slow dolly left."),
            ("SHOT-006", "- 轴线策略: 单轴定侧\n", "She does not attack and circles behind him. The camera never trucks and arcs."),
        ]
        vp = "".join(f"## {sid}\n{head}{meta}\n" + body.format(txt=txt) + "\n" for sid, meta, txt in shots)
        (tdp / "vp.md").write_bytes(("﻿" + vp + "## SHOT-7\n- 轴线策略: 单轴定侧\n").replace("\n", "\r\n").encode("utf-8"))
        sb = ("| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |\n|---|---|---|---|---|---|---|---|---|---|\n"
              "| SEQ-01 | SHOT-004 | 8.00 | 2 | 苏晓左手持刀→苏晓右转→苏晓在右 | 镜头从背后推近，向右平移 | 因为x，所以y | 石神=左; 苏晓=右 | — | — |\n")
        (tdp / "sb.md").write_text(sb, encoding="utf-8")
        f, ex = analyze(tdp / "vp.md", tdp / "sb.md")

        def lv(shot: str, code: str, word: str | None = None) -> set:
            return {x.level for x in f if x.where.startswith(shot) and x.code == code
                    and (word is None or word in x.data.get("word", ""))}
        check("对抗 BOM+CRLF：首行即 ## SHOT-001 仍被审计；`## SHOT-7` → FMT-shot-heading",
              bool(lv("SHOT-001", "DIR-camera")) and any(x.code == "FMT-shot-heading" for x in f)
              and any(x.code == "FMT-bom" for x in f))
        check("对抗：`换边: 否` 不豁免 → trucks left 仍是 error（修复前：降为需目视，假通过）",
              lv("SHOT-001", "DIR-camera") == {"error"} and lv("SHOT-001", "DIR-axis") == {"info"})
        check("对抗：轴线策略=单侧 → 按单轴审计报 error（修复前：只给 warn，判定通过）", lv("SHOT-002", "DIR-camera") == {"error"})
        check("对抗：轴线策略=随意（不认识）→ DIR-axis warn + 按单轴报 error",
              lv("SHOT-003", "DIR-camera") == {"error"} and "warn" in lv("SHOT-003", "DIR-axis"))
        check("对抗：a delivery truck / frying pan 是名词 → 需目视，不报 DIR-camera",
              not lv("SHOT-004 vp.md", "DIR-camera") and "visual" in lv("SHOT-004 vp.md", "DIR-check", "truck"))
        check("对抗：'Slow dolly left.'（无主语的相机动作）→ DIR-camera error（修复前：需目视）", lv("SHOT-005", "DIR-camera") == {"error"})
        check("对抗：'does not attack and circles behind' → DIR-path warn（否定只管 attack）；'never trucks and arcs' 两处都算否定",
              lv("SHOT-006", "DIR-path", "circles behind") == {"warn"}
              and lv("SHOT-006", "DIR-negated", "trucks") == {"info"} and lv("SHOT-006", "DIR-negated", "arcs") == {"info"})
        check("对抗：'苏 晓' 与 'S1＝苏晓' 归一后 [S1] on the RIGHT 与起始帧一致（不报 DIR-side error / DIR-mapping）",
              not [x for x in f if x.code in ("DIR-side", "DIR-mapping") and x.level == "error"])
        sbw = [x for x in f if "sb.md" in x.where]
        check("对抗：分镜 起始帧方位写 左/右 → DIR-layout warn（归一后与 LEFT/RIGHT 一致，不报 error）",
              any(x.code == "DIR-layout" and x.level == "warn" for x in sbw)
              and not any(x.code == "DIR-layout" and x.level == "error" for x in sbw))
        check("对抗：内容列 '苏晓左手' → 角色自身左右（需目视），'右转' → 需目视，均不报 DIR-side error",
              any(x.data.get("class") == "d-hand" and x.data.get("word") == "左" for x in sbw)
              and any(x.data.get("word") == "右转" and x.level == "visual" for x in sbw)
              and not any(x.code == "DIR-side" and x.level == "error" for x in sbw))
        check("对抗：运镜列 '从背后推近' → 需目视；'向右平移' → DIR-camera error",
              any(x.data.get("word") == "背后" and x.level == "visual" for x in sbw)
              and any(x.data.get("word") == "向右平移" and x.code == "DIR-camera" and x.level == "error" for x in sbw))

    me = [sys.executable, str(Path(__file__).resolve())]
    p = subprocess.run(me + [str(good / "video-prompts.md"), "--storyboard", str(good / "storyboard.md")],
                       capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    check("CLI good → 退出码 0，最后一行为通过判定", p.returncode == 0 and last == "方位词审计：通过（0 处矛盾）", last)
    p = subprocess.run(me + [str(bad / "video-prompts.md")], capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    check("CLI bad → 退出码 1，最后一行为不通过判定", p.returncode == 1 and last.startswith("方位词审计：不通过"), last)
    p = subprocess.run(me + [str(bad / "video-prompts.md"), "--json"], capture_output=True, text=True)
    try:
        js = json.loads(p.stdout)
        okj = js["passed"] is False and js["verdict"].startswith("方位词审计：不通过")
    except (ValueError, KeyError):
        okj = False
    check("CLI --json 可解析且含 verdict", okj)
    p = subprocess.run(me + ["/nonexistent/video-prompts.md"], capture_output=True, text=True)
    check("CLI 文件不存在 → 退出码 2", p.returncode == 2)

    print(f"SELFTEST {'PASS' if all(results) else 'FAIL'}（{sum(results)}/{len(results)}）")
    return 0 if all(results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompts", nargs="?", help="video-prompts.md")
    ap.add_argument("--storyboard", help="storyboard.md（交叉核对 起始帧方位，并审计 运镜/内容 列）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON（含 verdict 字段）")
    ap.add_argument("--selftest", action="store_true", help="用 fixtures 自测")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.prompts:
        ap.print_usage(sys.stderr)
        ac.die("需要 video-prompts.md 路径（或 --selftest）")
    findings, extra = analyze(a.prompts, a.storyboard)
    rc = ac.emit(TITLE, findings, a.json, extra)
    if not a.json:
        print(extra["verdict"])
    return rc


if __name__ == "__main__":
    sys.exit(main())
