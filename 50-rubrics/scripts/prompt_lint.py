#!/usr/bin/env python3
"""视频提示词静态检查 prompt_lint —— 每次 prepare/confirm/run 之前必跑，0 error 才允许送 H3。

用途：
  逐镜校验 video-prompts.md 的"送生成器前"硬约束：六段结构、禁令包末行、实时速度句、<Picture N> 参考编号、
  锚点句逐字嵌入、对白标记、差异化句、画面位置称呼、评价性形容词、不该交给生成器的内容、negative_prompt、
  具象光柱、人群虚化、符号对抗约束、H3 帧网格。脚本只报告事实，不做审美判决；每条发现都写下一步具体动作。

溯源：D1, D2, D4, A3, A5, B2, B3, C1, P1, M3, M8, T-2（另：E1 参考编号连续、P7 分镜↔提示词时长/拍数对账）

规则代码（VP-）：
  VP-struct            error  缺 h3 块 / 六段缺失、重复或顺序错（固定顺序 = academy_common.H3_SECTIONS，T-2）/ 镜号重复
  VP-ban               error  h3 块最后一个非空行 ≠ academy_common.BAN_LINE（D1 烧录字幕）
  VP-realtime          error  动作镜（分镜拍数 ≥2 或含 strike/slash/punch/kick/leap/charge/dodge/attack/block/swing/
                              fight/lunge/stab）缺 REALTIME_LINE；出现非否定的 slow motion/slowmo（A3）。
                              豁免：元数据 `- 慢动作: 设计选择（理由…）`
                       warn   声明了 慢动作 却仍写实时速度句（指令打架，A5④）
  VP-picture           error  <Picture N> 未在 references 中定义；references 编号缺失/重复/不从 1 连续（E1）；
                              <Picture N> 首次引用顺序不是升序（T-2：编号与引用顺序一致）；<Picture> 写法不规范
                       warn   references 中某编号从未被 <Picture N> 引用
  VP-anchor            error  元数据 锚点 中资产的 锚点句 EN 未逐字出现在 subject_definitions（P1）；锚点卡无此 ID
                       warn   仅空白/换行不同
                       info   非符号锚点的 禁用 项未写进提示词（C1：cfg=1.0 只能靠正向绝对否定句）
  VP-symbol            warn   符号锚点（SYM-* 或 类型=符号）的 禁用 清单项未逐条写进提示词（D4 对抗约束）
  VP-dialogue          error  <d> 不是同一行内闭合的 `<d>[Chinese] 台词</d>`；同一行 <d> 之前没有说话人 ID（如 [S1]）
                       warn   [Chinese] 后空白不规范；台词不含汉字；说话人未在 subject_definitions / 角色映射 中定义
  VP-distinct          error  ≥2 个主体（[S#] 定义或起始帧方位条目）却没有差异化句（B3 克隆脸）
  VP-position          warn   起始帧方位 ≥2 人，但 [S#] 定义未用 "on the LEFT/RIGHT" 画面位置称呼（A5②）
  VP-adjective         warn   未拆解的评价性形容词（M3：写事件不写形容词）
  VP-generator-unsafe  error  要求生成器出纯色画面 / 字卡 / 精确文字 / logo / UI 面板 / 字幕（D2、D1）
  VP-negative          warn   出现 negative_prompt（cfg=1.0 下无效，C1、T-2）
  VP-light             warn   具象光柱物件 flashlight / spotlight / light beam / god rays…（B3 二次案）
  VP-crowd             warn   人群词但全镜没有虚化描述（B2 人群被扩写）
  VP-frames            error  帧数/时长缺失；帧数不在 17k+5 网格（124–362，T-2）；时长与 帧数/24 不符
  VP-sync              error  （给 --storyboard 时）提示词时长 ≠ 分镜时长（P7 双文档对账）
                       warn   提示词 Beat 数 ≠ 分镜拍数；提示词中的镜在分镜表中不存在
  FMT-shot-heading     error  疑似镜头标题但不合 `## SHOT-nnn`（如 `## SHOT-3`、`### SHOT-004`）：该镜未被解析，
                              其下元数据/代码块会被并进上一镜（与 h3_frame_grid 同码）
  FMT-bom              warn   文件以 UTF-8 BOM 开头（契约 §0.1）；本脚本已去 BOM 解析

输入容错（只为不漏检/不误报，不放宽契约；偏差照报）：BOM、CRLF、全角冒号/等号/逗号（references 写成
  `1＝A，2＝B` 时报 VP-picture error 并按纠正后的编号继续核对）、`——` 视同空值、`慢动作: 否/无/no` 视同未声明。

输入格式：70-playbooks/format-contracts.md §2 视频提示词、§3 锚点卡、§1 分镜表
          （相对本文件：../../70-playbooks/format-contracts.md）

用法示例：
  python3 50-rubrics/scripts/prompt_lint.py season-01/ep03/video-prompts.md \\
      --anchors season-01/ep03/anchors.md --storyboard season-01/ep03/storyboard.md
  python3 50-rubrics/scripts/prompt_lint.py season-01/ep03/video-prompts.md --json > qc/prompt_lint.json
  python3 50-rubrics/scripts/prompt_lint.py --selftest
  修完 error 后接着跑：direction_audit.py（方位词审计）→ slot_order_check.py（参考槽）。

退出码：0 无 error / 1 有 error / 2 用法或环境错误（文件不存在、未解析到任何 ## SHOT-nnn）
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import academy_common as ac  # noqa: E402
from academy_common import Finding  # noqa: E402

TITLE = "视频提示词检查 prompt_lint"

# ------------------------------------------------------------------ 词表与正则

ACTION_RE = re.compile(
    r"\b(?:strik(?:e|es|ing)|struck|slash(?:es|ed|ing)?|punch(?:es|ed|ing)?|kick(?:s|ed|ing)?|"
    r"leap(?:s|t|ed|ing)?|charg(?:e|es|ed|ing)|dodg(?:e|es|ed|ing)|attack(?:s|ed|ing)?|block(?:s|ed|ing)?|"
    r"swing(?:s|ing)?|swung|fight(?:s|ing)?|fought|lung(?:e|es|ed|ing)|stab(?:s|bed|bing)?)\b", re.I)
# 名词用法不算动作："a block of stone" / "in charge of" / "a rope swing"
ACTION_NOUN_BEFORE = re.compile(r"(?:\b(?:a|an|the|stone|wooden|ice|building|city|cell|rope|in|of)\s+)$", re.I)
ACTION_NOUN_AFTER = re.compile(r"^\s+(?:of|with\s+(?:energy|power|electricity|tension|emotion))\b", re.I)
ACTION_NOUNISH = {"block", "blocks", "charge", "swing"}
SLOWMO_RE = re.compile(r"\bslow[- ]?mo(?:tion)?\b|\bslowmo\b|\bbullet[- ]time\b|\btime\s+slows(?:\s+down)?\b|\bhalf[- ]speed\b",
                       re.I)
# 否定作用域：同一分句内，否定词之后 ≤6 个词、中间不出现主语/新谓语/连词（"no fear and leaps in slow motion" 不算否定）
NEG_WORD = re.compile(r"\b(?:no|not|never|without|nor|zero|none|neither)\b|n't\b", re.I)
NEG_BREAK = re.compile(
    r"\[[A-Z][A-Za-z]{0,3}\d{1,3}\]|\b(?:she|he|they|it|we|i|you|her|his|its|their|them|him|this|these|those|"
    r"but|then|while|whilst|as|so|yet|when|until|before|after|because|which|who|whose|where|"
    r"is|are|was|were|has|have|had|falls?|appears?|watch(?:es)?|looks?|stands?|walks?|runs?|moves?|turns?|holds?|"
    r"raises?|lifts?|rises?|shines?|glows?|hangs?|sits?|flies|fly|drops?|steps?|enters?|leaves?|opens?)\b",
    re.I)
SLOW_POST_NEG = re.compile(r"^\s*(?:is|are|was|will\s+be|should\s+be|must\s+be|being)?\s*(?:not|never|forbidden|avoided|"
                           r"prohibited|banned|disabled|off|excluded|ruled\s+out)\b|^\s*[:：]\s*(?:none|no|off|否|无)\b", re.I)

ADJ_RE = re.compile(r"\b(epic|spectacular|gorgeous|stunning|cinematic|amazing|awesome|majestic|breathtaking|"
                    r"beautiful(?:ly)?)\b|(华丽|史诗|震撼|炫酷)", re.I)
DIFF_RE = re.compile(
    r"clearly\s+distinct|distinct\s+from\s+each\s+other|visibly\s+distinct|clearly\s+different|"
    r"different\s+(?:faces|builds|heights|hair|hairstyles|silhouettes|body\s+types|ages|face\s+shapes)|"
    r"not\s+(?:twins|identical)|no\s+two\s+(?:\w+\s+){0,2}alike|each\s+(?:with|has)\s+a\s+(?:different|distinct)|"
    r"easily\s+told\s+apart|unmistakably\s+different|长相各异|明显不同", re.I)
POS_RE = re.compile(r"\b(?:on|at|in)\s+the\s+(?:far\s+)?(?:left|right|center|centre|foreground|background)\b", re.I)
LIGHT_RE = re.compile(
    r"\b(?:flash\s?lights?|torch(?:light)?\s+beams?|torch\s?lights?|spot\s?lights?|search\s?lights?|light\s+beams?|"
    r"beams?\s+of\s+light|light\s+shafts?|shafts?\s+of\s+light|god\s*rays|volumetric\s+(?:beams?|rays?)|"
    r"laser\s+beams?)\b|光柱|手电", re.I)
CROWD_RE = re.compile(
    r"\b(?:crowds?|onlookers?|spectators?|villagers?|bystanders?|audiences?|townsfolk|townspeople|passers-?by|"
    r"people\s+in\s+the\s+background|figures\s+in\s+the\s+background)\b|人群|围观|群众|村民", re.I)
BLUR_RE = re.compile(
    r"\b(?:blurr?ed|blurry|out[- ]of[- ]focus|defocused|bokeh|dark\s+silhouettes?|indistinct|faceless|"
    r"no\s+(?:distinct|individual|visible|recognizable)\s+faces?)\b|虚化|无脸|暗形", re.I)
NEGPROMPT_RE = re.compile(r"negative[_ ]?prompts?", re.I)

UNSAFE_RULES = [
    ("纯色画面",
     re.compile(r"\b(?:pure|solid|plain|blank|all)[- ](?:black|white|red|blue|green|grey|gray|colou?r(?:ed)?)"
                r"(?:\s+\w+)?\s+(?:screen|frame|background|backdrop|card|image|field|void|fill)s?\b"
                r"|\b(?:black|white|blank)\s+(?:screen|frame)s?\b|\bfades?\s+(?:out\s+)?to\s+(?:black|white)\b"
                r"|\bsolid[- ]colou?r\s+(?:screen|frame|background|card|image|fill)s?\b|纯黑|纯白|纯色|黑屏|白屏", re.I),
     "纯色画面交给 H3 守不住（D2 实证：片尾纯黑字卡中段被加 'LAVCE' 水印）→ 本镜不送生成器，剪辑单 来源 写 "
     "local:black / local:white / local:#RRGGBB 本地确定性生成"),
    ("字卡/片尾卡",
     re.compile(r"\b(?:end|title|closing|opening|chapter|name)[- ]?cards?\b|\bintertitles?\b|\bend\s+screen\b"
                r"|\btitle\s+(?:text|screen|sequence)\b|\bcredits?\s+roll\b|字卡|片尾卡|标题卡", re.I),
     "字卡交给生成器会被加字/乱字（D2）→ 底图本地生成，文字写进剪辑单 画面文字 列由剪辑叠层"),
    ("精确文字", None,
     "生成器写不对精确文字且会扩写成水印/乱码（D1、D2）→ 从提示词删除文字内容，写进剪辑单 画面文字 列由剪辑程序叠加"),
    ("logo/水印",
     re.compile(r"\blogos?\b|\bwatermarks?\b|\bbrand\s*marks?\b|水印|台标", re.I),
     "logo/水印必须本地叠层（D2：生成器会自造水印）→ 从提示词删除，交剪辑叠层"),
    ("UI 面板",
     re.compile(r"\bUI\b|\bHUD\b|\buser\s+interface\b|\b(?:status|stat|menu|system|game)\s+(?:panel|window|screen|bar)s?\b"
                r"|\bhealth\s+bars?\b|\bpop-?up\s+(?:window|panel)s?\b|界面|面板", re.I),
     "UI 面板/数值界面生成器守不住（D2 清单）→ 本地生成 + 剪辑叠层"),
    ("字幕/叠字",
     re.compile(r"\b(?:subtitles?|captions?|on-screen\s+text|text\s+overlays?|lower\s+thirds?|kinetic\s+typography)\b|字幕",
                re.I),
     "要求生成器出字幕/叠字会被烧录（D1）→ 删除此句；字幕走剪辑单 字幕 列，h3 末行保留禁令句"),
]
QUOTE_RE = re.compile(r"[\"“「『]([^\"”」』\n]{1,80})[\"”」』]")
TEXTISH_BEFORE = re.compile(
    r"(?:\b(?:text|texts|words?|letters?|lettering|sign|signboard|title|caption|reads?|reading|says|saying|"
    r"inscription|inscribed|written|writing|label|banner|plaque|characters|typography)\b|文字|字样|写着)[^.\n]{0,25}$",
    re.I)
TEXT_VERB = re.compile(r"\b(?:text|lettering|typography|words)\s+(?:appears?|reads?|reading|saying|that\s+says|spelling)\b",
                       re.I)
# 引号里的中文台词没写成 <d>：判为对白标记问题而不是"精确文字"（标牌/横幅类名词优先判为文字）
TEXT_NOUN_BEFORE = re.compile(r"\b(?:sign|signboard|banner|plaque|board|screen|scroll|note|letter|inscription|label|poster|"
                              r"tablet|placard|text|words|title|caption|flag|seal|stele)\b[^.\n]{0,30}$", re.I)
SPEECH_BEFORE = re.compile(
    r"(?:\[[A-Z][A-Za-z]{0,3}\d{1,3}\]|\b(?:says?|said|saying|shouts?|shouted|whispers?|whispered|yells?|yelled|asks?|"
    r"asked|cries|cried|murmurs?|murmured|replies|replied|screams?|screamed|calls?|called|roars?|roared|mutters?|"
    r"muttered|exclaims?|exclaimed|answers?|answered|speaks?|spoke|tells?|told|growls?|growled|hiss(?:es|ed)|gasps?|"
    r"gasped|sighs?|sighed))[^.\n]{0,20}$", re.I)

SPEAKER_RE = re.compile(r"\[(?!Chinese\])([A-Z][A-Za-z]{0,3}\d{1,3})\]")
DEF_ID_RE = re.compile(r"^\s*\[([A-Z][A-Za-z]{0,3}\d{1,3})\]")
PICTURE_RE = re.compile(r"<Picture (\d+)>")
PICTURE_LOOSE = re.compile(r"[<＜〈]\s*(?:picture|image|pic|img)(?=[\s\d_\-:：>＞〉])[^>＞〉\n]*[>＞〉]", re.I)
BEAT_RE = re.compile(r"^\s*Beat\s+(\d+)\s*[:：]", re.I | re.M)
HAN_RE = re.compile(r"[㐀-䶿一-鿿]")
NEG_VALUE = re.compile(r"^\s*(?:否|无|不|没有|不用|不需要|不换边|未声明|no|none|false|off|n/?a|0)\s*(?:[（(].*)?$", re.I)
SECTION_LIKE = re.compile(r"^\s*([A-Za-z_]+)\s*([:：])", re.M)
RE_STRICT_HEADING = re.compile(r"^##\s+(SHOT-\d{3})\b")              # 与 academy_common.parse_video_prompts 一致
RE_SHOTLIKE_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(?:镜头|镜号|镜)?\s*[:：]?\s*shot\s*[-_－—–]?\s*(\d+)", re.I)
RE_SHOT_TOKEN = re.compile(r"shot\s*[-_－—–]?\s*\d+", re.I)
RE_STRICT_ANCHOR = re.compile(r"^##\s+ANCHOR:\s*([A-Z]{3}-[A-Z0-9-]+)\s*$")   # 与 academy_common.parse_anchors 一致
RE_ANCHORLIKE = re.compile(r"^\s{0,3}#{1,6}\s*ANCHOR\b", re.I)


# ------------------------------------------------------------------ 输入容错（只为不漏检/不误报）

def _read(path: str | Path) -> tuple[str, bool]:
    """读 UTF-8 文本；返回 (去 BOM 后的文本, 是否带 BOM)。"""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        ac.die(f"{path} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8（无 BOM）后重跑")
    return (text[1:], True) if text.startswith("﻿") else (text, False)


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
    if isinstance(out, list):
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
    """代码块外、像镜头标题却不合 `## SHOT-nnn` 的行 → [(行号, 原文, 建议 ID, 上一个合法镜号)]。围栏规则与 academy_common 相同。"""
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


def _empty(v: str | None) -> bool:
    """academy_common.is_empty 之外，再把 '——' '－' 等纯破折号视同空值。"""
    return ac.is_empty(v) or bool(re.fullmatch(r"[\s—–\-－─_]*", v or ""))


def _declared(v: str | None) -> bool:
    """元数据开关（慢动作 / 换边）是否真的声明了：空值、'否/无/no/none' 都算未声明。"""
    return not _empty(v) and not NEG_VALUE.match(v or "")


def _fix_refs(raw: str) -> tuple[str, list[str]]:
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


# ------------------------------------------------------------------ 小工具

def _mask_dialogue(text: str) -> str:
    """把 <d>…</d> 整段替换为等长空白（保留换行），避免把台词当成提示词指令扫描。"""
    return re.sub(r"<d>.*?</d>", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def _negated(text: str, start: int) -> bool:
    """start 处的词是否处在否定作用域内（同一分句、否定词后 ≤6 词、中间无新主语/谓语/连词）。"""
    seg = text[max(0, start - 90):start]
    cut = max(seg.rfind(c) for c in ".;:!?\n。；：！？")
    if cut >= 0:
        seg = seg[cut + 1:]
    negs = list(NEG_WORD.finditer(seg))
    if not negs:
        return False
    between = seg[negs[-1].end():]
    if len(re.findall(r"[A-Za-z]+", between)) > 6:
        return False
    if NEG_BREAK.search(between) or ACTION_RE.search(between):
        return False
    if re.search(r"(?<!,)\s+and\b", between):
        return False
    return True


def _action_verbs(masked: str) -> list[str]:
    out = set()
    for m in ACTION_RE.finditer(masked):
        w = m.group(0).lower()
        if w in ACTION_NOUNISH and (ACTION_NOUN_BEFORE.search(masked[max(0, m.start() - 20):m.start()])
                                    or ACTION_NOUN_AFTER.match(masked[m.end():m.end() + 30])):
            continue
        out.add(w)
    return sorted(out)


def _line_of(shot: dict, off: int) -> int:
    return (shot.get("h3_line") or shot["line"]) + shot["h3"].count("\n", 0, off)


def _where(shot: dict, line: int | None = None) -> str:
    return f"{shot['shot']} {Path(shot['file']).name}:{line if line is not None else shot['line']}"


def _snap_up(sec: float) -> int | None:
    """ac.snap_seconds_up 的两位小数容差版：契约把时长写成两位小数（124 帧 = 5.1667s 写作 5.17），
    直接吸附会把 5.17 吸到 141 帧；这里先减去 0.005s 的舍入误差。"""
    return ac.snap_seconds_up(max(0.0, sec))    # academy_common 已内置 0.005s 显示容差


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def parse_mapping(s: str) -> dict:
    """'S1=苏晓; S2=石神' → {'S1': '苏晓', 'S2': '石神'}（不改大小写）。"""
    out = {}
    if ac.is_empty(s):
        return out
    for part in re.split(r"[;；,，]", s):
        if "=" in part:
            k, v = part.split("=", 1)
            if k.strip():
                out[k.strip()] = v.strip()
    return out


def _split_ids(s: str) -> list[str]:
    if _empty(s):
        return []
    return [x.strip() for x in re.split(r"[;；,，、]", s) if x.strip() and not _empty(x)]


def _snippet(text: str, s: int, e: int, pad: int = 25) -> str:
    a, b = max(0, s - pad), min(len(text), e + pad)
    return ("…" if a else "") + _ws(text[a:s]) + " 【" + _ws(text[s:e]) + "】 " + _ws(text[e:b]) + ("…" if b < len(text) else "")


# ------------------------------------------------------------------ 逐镜检查

def _anchor_sentence(card: dict) -> str:
    """锚点句 EN：去掉外层多重反引号（``…`` 写法），academy_common 只剥一层。"""
    return re.sub(r"^`+\s*|\s*`+$", "", card["fields"].get("锚点句 EN", "")).strip()


def _anchor_diag(sent: str, sd: str) -> str:
    """锚点句不逐字时，给出最可能的差异类型（只为让修改动作更具体）。"""
    if sent.lower() in sd.lower():
        return "仅大小写不同"
    core = sent.rstrip(" .。,，;；")
    if core and core in sd:
        return "仅句末标点不同"
    if core and core.lower() in sd.lower():
        return "仅大小写与句末标点不同"
    return ""


def _layout(raw: str) -> dict:
    return ac.parse_layout((raw or "").replace("＝", "="))


def lint_shot(shot: dict, anchors: dict | None, sb: dict | None, sb_given: bool, anchors_text: str = "") -> list[Finding]:
    F: list[Finding] = []
    meta, sid = shot["meta"], shot["shot"]

    def add(level, code, msg, line=None, **data):
        F.append(Finding(level, code, msg, _where(shot, line), data))

    # ---------- VP-frames（不依赖 h3）
    _check_frames(shot, add)

    # ---------- VP-sync
    if sb_given:
        if sb is None:
            add("warn", "VP-sync", f"分镜表中没有 {sid}（P7 双文档对账）→ 先在 storyboard.md 补这一行，或删除此镜提示词")
        else:
            pdur, sdur = ac.to_float(meta.get("时长", "")), sb.get("dur")
            if pdur is not None and sdur is not None and abs(pdur - sdur) > 0.01:
                add("error", "VP-sync", f"提示词 时长 {pdur:.2f}s ≠ 分镜 时长(s) {sdur:.2f}s（P7：两份文档必须逐镜一致）"
                    f"→ 先定网格帧数，再把两边都改成同一个值（{sdur:.2f}s 吸附后为 "
                    f"{_snap_up(sdur) or '超上限需拆段'} 帧）", pdur=pdur, sdur=sdur)

    if shot["h3"] is None:
        lang = shot.get("_fence_langs") or []
        if "h3" in lang:
            hint = "；本镜的 ```h3 代码块没有闭合（缺结尾 ```），一直延续到文件末尾 → 在禁令句后补一行 ```"
        else:
            hint = (f"；本镜下有代码块但语言标记是 {', '.join(repr(x) for x in lang)}（必须是小写 ```h3）" if lang else "")
        add("error", "VP-struct", "缺少 ```h3 代码块：本镜无法送生成器 → 按 format-contracts.md §2 补齐六段 h3 块" + hint)
        return F
    h3 = shot["h3"]
    secs = shot["sections"]
    masked = _mask_dialogue(h3)

    # ---------- VP-struct
    order = shot["section_order"]
    missing = [s for s in ac.H3_SECTIONS if s not in order]
    dups = sorted({s for s in order if order.count(s) > 1})
    if missing:
        hint = []
        for s in missing:
            for m in SECTION_LIKE.finditer(h3):
                if m.group(1).lower() != s:
                    continue
                why = []
                if m.group(0)[0].isspace():
                    why.append("有缩进")
                if m.group(1) != s:
                    why.append("大小写不对")
                if m.group(2) == "：":
                    why.append("用了全角冒号 ：")
                if why:
                    hint.append(f"第 {_line_of(shot, m.start())} 行「{m.group(0).strip()}」{'、'.join(why)} → 改为顶格 '{s}:'")
                    break
        add("error", "VP-struct", f"缺少段：{', '.join(missing)}（T-2 六段方言）→ 补齐并顶格写 '段名:'"
            + (f"；{'；'.join(hint)}" if hint else ""), missing=missing)
    if dups:
        add("error", "VP-struct", f"段重复：{', '.join(dups)} → 合并为一段", dups=dups)
    seen = list(dict.fromkeys(order))
    expect = [s for s in ac.H3_SECTIONS if s in seen]
    if seen != expect:
        k = next(i for i, (x, y) in enumerate(zip(seen, expect)) if x != y)
        add("error", "VP-struct",
            f"六段顺序错：当前 {' → '.join(seen)}；第 {k + 1} 段应为 {expect[k]}，实为 {seen[k]} → 按 "
            f"{' → '.join(ac.H3_SECTIONS)} 重排", order=seen)

    # ---------- VP-ban
    nonempty = [ln for ln in h3.splitlines() if ln.strip()]
    last = nonempty[-1].strip() if nonempty else ""
    if last != ac.BAN_LINE:
        if ac.BAN_LINE in h3:
            add("error", "VP-ban", "禁令句存在但不是 h3 块最后一个非空行 → 把它移到末行（M8 禁令包位置固定）")
        else:
            near = next((ln.strip() for ln in reversed(nonempty) if re.search(r"caption|subtitle|overlay|字幕", ln, re.I)), "")
            add("error", "VP-ban", f"h3 块末行缺禁令句（D1：生成器会自行烧录字幕）→ 在最后一行原样加：{ac.BAN_LINE}"
                + (f"（现有近似句「{near}」与标准句不逐字一致，整句替换）" if near else ""), last_line=last)

    # ---------- VP-realtime
    slow_meta = _declared(meta.get("慢动作", ""))
    if not slow_meta and not _empty(meta.get("慢动作", "")):
        add("info", "VP-realtime", f"元数据 慢动作「{meta.get('慢动作')}」按'未声明'处理（否定值不构成 A3 豁免）")
    has_rt = ac.REALTIME_LINE.lower() in _ws(h3).lower()
    verbs = _action_verbs(masked)
    beats = sb.get("beats") if sb else None
    why = []
    if beats is not None and beats >= 2:
        why.append(f"分镜拍数={int(beats)}")
    if verbs:
        why.append("动作词：" + ", ".join(verbs[:6]))
    if why and not has_rt and not slow_meta:
        near = re.search(r"[^\n.]*real[- ]?time[^\n.]*", h3, re.I)
        add("error", "VP-realtime", f"动作镜（{'；'.join(why)}）缺实时速度句（A3：不写就默认慢镜头）→ 在 "
            f"detailed_description 首行加 '{ac.REALTIME_LINE}.'；若慢是设计选择，元数据加 '- 慢动作: 设计选择（理由…）'"
            + (f"（现有近似句「{near.group(0).strip()}」不逐字一致，整句替换）" if near else ""), verbs=verbs)
    for m in SLOWMO_RE.finditer(masked):
        if _negated(masked, m.start()) or SLOW_POST_NEG.match(masked[m.end():m.end() + 40]):
            continue
        ln = _line_of(shot, m.start())
        if slow_meta:
            add("info", "VP-realtime", f"「{m.group(0)}」已由元数据声明豁免（慢动作: {meta.get('慢动作')}）", ln)
        else:
            add("error", "VP-realtime", f"非否定的「{m.group(0)}」（A3：慢必须是设计选择而非默认）→ 删除该词并保留 "
                f"'{ac.REALTIME_LINE}'；若确需慢动作，元数据加 '- 慢动作: 设计选择（理由…）'", ln, text=m.group(0))
    if slow_meta and has_rt:
        add("warn", "VP-realtime", "元数据声明了 慢动作，但提示词仍写 'Real-time speed throughout'：两条指令互相矛盾"
            "（A5④：模型会执行所有指令，打架就乱编）→ 二选一并删除另一条")

    # ---------- VP-picture
    _check_pictures(shot, add)

    # ---------- VP-anchor / VP-symbol
    sd = secs.get("subject_definitions", "")
    ids = _split_ids(meta.get("锚点", ""))
    if ids and anchors is None:
        add("info", "VP-anchor", f"未提供 --anchors：跳过 {', '.join(ids)} 的锚点句逐字核对（P1）→ 加 --anchors anchors.md 重跑")
    elif ids:
        h3_low = _ws(h3).lower()
        for aid in ids:
            a = anchors.get(aid)
            if a is None:
                like = [ln.strip() for ln in anchors_text.splitlines() if aid in ln.upper() and ln.lstrip().startswith("#")]
                add("error", "VP-anchor", f"元数据 锚点 列出了 {aid}，但锚点卡中没有 '## ANCHOR: {aid}' → "
                    + (f"锚点卡里有疑似标题「{like[0]}」但格式不合契约，改为 '## ANCHOR: {aid}'（两个 #、半角冒号）"
                       if like else "先建锚点卡或改正 ID"), anchor=aid)
                continue
            sent = _anchor_sentence(a)
            if not sent:
                add("error", "VP-anchor", f"锚点卡 {aid} 缺 '锚点句 EN' → 先补锚点卡（format-contracts.md §3）", anchor=aid)
            elif sent not in sd:
                if _ws(sent) in _ws(sd):
                    add("warn", "VP-anchor", f"{aid} 锚点句在 subject_definitions 中仅空白/换行不同 → 改成与锚点卡完全一致的一行",
                        anchor=aid)
                elif sent in h3:
                    add("error", "VP-anchor", f"{aid} 锚点句出现在其他段，但不在 subject_definitions（P1）→ 把整句移入对应 [S#] 定义",
                        anchor=aid)
                else:
                    sm = difflib.SequenceMatcher(None, sent, sd, autojunk=False)
                    best = sm.find_longest_match(0, len(sent), 0, len(sd))
                    diag = _anchor_diag(sent, sd)
                    add("error", "VP-anchor",
                        f"{aid} 的锚点句 EN 未逐字出现在 subject_definitions（P1：改写/缩写 = 跨镜一致性失效；"
                        + (f"{diag}" if diag else f"最长逐字重合仅 {best.size}/{len(sent)} 字符")
                        + f"）→ 把锚点卡原句整句粘入对应 [S#] 定义：`{sent}`", anchor=aid)
            # 禁用项（分号分隔；若写成逗号分隔的多条 no X，也逐条拆开）
            bans = []
            for b in re.split(r"[;；]", a["fields"].get("禁用", "")):
                parts = [x for x in re.split(r"\s*[,，、]\s*", b) if x.strip()]
                if len(parts) > 1 and all(re.match(r"\s*(?:no|not|never|without)\b", x, re.I) for x in parts):
                    bans.extend(parts)
                else:
                    bans.append(b)
            bans = [b.strip().rstrip("。.") for b in bans if b.strip()]
            bans = [b for b in bans if not _empty(b)]
            miss = [b for b in bans if _ws(b).lower() not in h3_low]
            is_sym = aid.startswith("SYM-") or "符号" in a["fields"].get("类型", "")
            if miss and is_sym:
                add("warn", "VP-symbol", f"符号锚点 {aid} 的对抗约束未写全（D4：'ф' 被画成十字、火纹被画成霓虹）→ 把这些禁用项"
                    f"逐条原样写进 detailed_description：{'; '.join(miss)}", anchor=aid, missing=miss)
            elif miss:
                add("info", "VP-anchor", f"{aid} 的禁用项未写入提示词：{'; '.join(miss)}（C1：cfg=1.0 下 negative 无效，"
                    f"只能靠正向绝对否定句对抗装饰物）→ 若本镜可见该资产，把它们写进 detailed_description", anchor=aid,
                    missing=miss)

    # ---------- VP-dialogue
    mapping = parse_mapping(meta.get("角色映射", ""))
    def_ids = [m.group(1) for ln in sd.splitlines() for m in [DEF_ID_RE.match(ln)] if m]
    base = shot.get("h3_line") or shot["line"]
    for i, ln in enumerate(h3.splitlines()):
        lno = base + i
        rest = ln
        for m in re.finditer(r"<d>(.*?)</d>", ln):
            inner = m.group(1)
            if not re.match(r"^\s*\[Chinese\]", inner):
                bare = re.sub(r"^\s*[\[［【]\s*chinese\s*[\]］】]\s*", "", inner, flags=re.I).strip()
                add("error", "VP-dialogue", f"对白缺 [Chinese] 标记（必须是半角方括号、首字母大写）：「{m.group(0)}」→ 改为 "
                    f"'<d>[Chinese] {bare}</d>'（T-2 方言）", lno)
            elif not re.match(r"^\[Chinese\] \S", inner) or inner != inner.rstrip():
                add("warn", "VP-dialogue", f"对白标记空白不规范：「{m.group(0)}」→ 写成 '<d>[Chinese] 台词</d>'（[Chinese] 后一个空格）",
                    lno)
            text = re.sub(r"^\s*[\[［【]\s*chinese\s*[\]］】]\s*", "", inner, flags=re.I).strip()
            if not text:
                add("error", "VP-dialogue", "空台词 <d>[Chinese] </d> → 填入分镜表 对白 列的原句，或删掉此标记", lno)
            elif not HAN_RE.search(text):
                add("warn", "VP-dialogue", f"[Chinese] 标记内没有汉字：「{text}」→ 用分镜表 对白 列的中文原句", lno)
            spk = SPEAKER_RE.findall(ln[:m.start()])
            if not spk:
                add("error", "VP-dialogue", f"对白前同一行没有说话人 ID：「{_ws(ln)[:60]}」→ 写成 '[S1] shouts: <d>[Chinese] "
                    f"{text}</d>'（T-2：对白由稳定说话人 ID 引出，否则串台）", lno)
            else:
                s = spk[-1]
                if def_ids and s not in def_ids:
                    add("warn", "VP-dialogue", f"说话人 [{s}] 未在 subject_definitions 中定义 → 补 '[{s}] …' 定义行或改用已定义 ID "
                        f"{def_ids}", lno)
                if mapping and s not in mapping:
                    add("warn", "VP-dialogue", f"说话人 [{s}] 不在元数据 角色映射 中 → 补 '{s}=角色名'，否则转写对账无法核对说话人（P7）",
                        lno)
            rest = rest.replace(m.group(0), " " * len(m.group(0)), 1)
        if "<d>" in rest:
            add("error", "VP-dialogue", "<d> 未在同一行闭合 → 每句对白写成一行 '<d>[Chinese] 台词</d>'", lno)
        if "</d>" in rest:
            add("error", "VP-dialogue", "多余的 </d>（没有对应的 <d>）→ 删除或补全开标记", lno)
        odd = [t for t in re.findall(r"<\s*/?\s*[dD]\s*>", rest) if t not in ("<d>", "</d>")]
        if odd:
            add("error", "VP-dialogue", f"对白标记写法不规范：{odd} → 只能用小写 <d> … </d>", lno)

    # ---------- VP-distinct / VP-position
    layout = _layout(meta.get("起始帧方位", ""))
    uniq_defs = list(dict.fromkeys(def_ids))
    if len(uniq_defs) >= 2 or len(layout) >= 2:
        zone = sd + "\n" + secs.get("detailed_description", "")
        if not DIFF_RE.search(zone):
            add("error", "VP-distinct", f"画面有 ≥2 个主体（[S#] 定义 {len(uniq_defs)} 个、起始帧方位 {len(layout)} 人）但没有差异化句"
                "（B3：同框成克隆脸）→ 在 subject_definitions 末尾加一句，如 'The two figures are clearly distinct: "
                "different faces, hair and builds.'")
    if len(layout) >= 2:
        lacking = []
        for ln in sd.splitlines():
            m = DEF_ID_RE.match(ln)
            if m and not POS_RE.search(ln):
                lacking.append(m.group(1))
        if not uniq_defs:
            add("warn", "VP-position", "起始帧方位有 ≥2 人，但 subject_definitions 没有任何 [S#] 定义行（A5②）→ 每个主体一行 "
                "'[S1] the … on the RIGHT: <锚点句>'")
        elif lacking:
            add("warn", "VP-position", f"{', '.join('[' + x + ']' for x in lacking)} 定义未用画面位置称呼（A5②：宽景中身份要靠"
                f"画面位置，不能只靠名字）→ 按起始帧方位 {meta.get('起始帧方位')} 写成 '[S1] the … on the RIGHT: …'",
                lacking=lacking)

    # ---------- VP-adjective
    adj: dict[str, list[int]] = {}
    anchor_spans = []
    for aid in (ids if anchors else []):
        sent = _anchor_sentence(anchors[aid]) if aid in anchors else ""
        anchor_spans += [(m.start(), m.end()) for m in re.finditer(re.escape(sent), masked)] if sent else []
    in_anchor = []
    for m in ADJ_RE.finditer(masked):
        if any(a <= m.start() < b for a, b in anchor_spans):
            in_anchor.append(m.group(0).lower())
            continue
        adj.setdefault(m.group(0).lower(), []).append(_line_of(shot, m.start()))
    if in_anchor:
        add("info", "VP-adjective", f"锚点句内含评价性形容词 {sorted(set(in_anchor))}：提示词里必须逐字保留（P1），不在此处改；"
            "若要改，改锚点卡并全集同步替换")
    for w, lns in adj.items():
        add("warn", "VP-adjective", f"评价性形容词「{w}」×{len(lns)}（行 {', '.join(map(str, lns))}）：写事件不写形容词（M3）："
            f"把它拆成可见事件+后果（例：'epic fight' → 'her blade hits the stone shin; a ring of dust bursts outward; "
            f"the god's leg buckles'）", lns[0], word=w)

    # ---------- VP-generator-unsafe
    scan = masked.replace(ac.BAN_LINE, " " * len(ac.BAN_LINE))
    hits: dict[str, list[tuple[int, str]]] = {}
    for name, rx, _ in UNSAFE_RULES:
        if rx is None:
            continue
        for m in rx.finditer(scan):
            if not _negated(scan, m.start()):
                hits.setdefault(name, []).append((_line_of(shot, m.start()), m.group(0)))
    for m in QUOTE_RE.finditer(scan):
        before = scan[max(0, m.start() - 40):m.start()]
        before_line = before.rsplit("\n", 1)[-1]
        if HAN_RE.search(m.group(1)) and not TEXT_NOUN_BEFORE.search(before_line) and SPEECH_BEFORE.search(before_line):
            ids_here = SPEAKER_RE.findall(before_line)
            add("error", "VP-dialogue", f"引号里的中文台词没写成对白标记：「{_ws(before_line)[-30:]} {m.group(0)}」→ 改为 "
                f"'[{ids_here[-1] if ids_here else 'S1'}] says: <d>[Chinese] {m.group(1)}</d>'（T-2；不加标记生成器可能把它当画面文字"
                "烧录，D1）", _line_of(shot, m.start()))
            continue
        if TEXTISH_BEFORE.search(before) and not _negated(scan, m.start()):
            hits.setdefault("精确文字", []).append((_line_of(shot, m.start()), m.group(0)))
    for m in TEXT_VERB.finditer(scan):
        if not _negated(scan, m.start()):
            hits.setdefault("精确文字", []).append((_line_of(shot, m.start()), m.group(0)))
    for name, rx, advice in UNSAFE_RULES:
        if name in hits:
            ev = hits[name]
            add("error", "VP-generator-unsafe", f"要求生成器产出「{name}」：" + "、".join(f"行{l}「{t}」" for l, t in ev[:4])
                + f"。改为本地确定性生成 + 剪辑叠层：{advice}", ev[0][0], category=name, evidence=[t for _, t in ev])

    # ---------- VP-negative
    for k, v in meta.items():
        if NEGPROMPT_RE.search(k) or k.lower().startswith("negative"):
            add("warn", "VP-negative", f"元数据含 '{k}'：cfg=1.0 下 negative_prompt 实际无效（C1、T-2）→ 删除该键，"
                f"改写为正向提示词中的绝对否定句 no X（如 'no jewelry at all, no armor'）", key=k)
    for m in NEGPROMPT_RE.finditer(h3):
        add("warn", "VP-negative", "提示词正文出现 negative_prompt：cfg=1.0 下无效（C1、T-2）→ 改写为正向提示词中的绝对否定句 no X",
            _line_of(shot, m.start()))

    # ---------- VP-light
    for m in LIGHT_RE.finditer(masked):
        if _negated(masked, m.start()):
            continue
        add("warn", "VP-light", f"具象光柱物件「{m.group(0)}」（B3 二次案：生成器添加了不存在的具象斜光柱）→ 删掉光源物件，只写被动"
            f"环境光（如 'warm ambient light falling on their faces'），并加 'no flashlight, no torch beam, no spotlight, "
            f"no light beams'", _line_of(shot, m.start()), text=m.group(0))

    # ---------- VP-crowd
    crowd = [m for m in CROWD_RE.finditer(masked) if not _negated(masked, m.start())]
    if crowd and not BLUR_RE.search(masked):
        m = crowd[0]
        add("warn", "VP-crowd", f"人群词「{m.group(0)}」但全镜没有虚化描述（B2：'远处人群低语'被扩写成持发光平板者且扩散变形）→ "
            f"改写为 'heavily blurred, out-of-focus dark silhouettes with no distinct faces'，不给人群任何独立特征；能删则删",
            _line_of(shot, m.start()), words=[x.group(0) for x in crowd])

    # ---------- VP-sync：Beat 数
    if sb and sb.get("beats"):
        nb = len(set(BEAT_RE.findall(h3)))
        if nb and nb != int(sb["beats"]):
            add("warn", "VP-sync", f"提示词有 {nb} 个 Beat，分镜 拍数={int(sb['beats'])}（P7）→ 两边对齐（段内 2–3 拍为常态，P10）")
    return F


def _check_frames(shot: dict, add) -> None:
    meta = shot["meta"]
    dur_raw = meta.get("时长", "")
    dur = ac.to_float(dur_raw)
    fr_raw = meta.get("帧数", "")
    fr = None
    if not _empty(fr_raw):
        try:
            fr = int(round(float(fr_raw)))
        except ValueError:
            fr = None
    if dur is None:
        if _empty(dur_raw):
            add("error", "VP-frames", "缺 '- 时长: 秒' 元数据（T-2）→ 补上，保留两位小数")
        else:
            num = re.sub(r"[^0-9.,]", "", unicodedata.normalize("NFKC", dur_raw)).replace(",", ".")
            add("error", "VP-frames", f"'- 时长:' 无法解析（'{dur_raw}'）→ 写成纯数字秒、半角小数点，如 '- 时长: {num or '10.83'}'")
    if fr is None:
        sug = _snap_up(dur) if dur else None
        digits = re.sub(r"\D", "", unicodedata.normalize("NFKC", fr_raw or ""))
        add("error", "VP-frames", f"缺或无法解析 '- 帧数:'（'{fr_raw}'）→ 写 17k+5 网格帧数（纯数字，不带单位）"
            + (f"，如 '- 帧数: {digits}'" if digits else "") + (f"；按时长 {dur:.2f}s 取 {sug}" if sug else ""))
        return
    probs = []
    if not ac.is_grid_frames(fr):
        if fr < ac.H3_MIN_FRAMES:
            probs.append(f"帧数 {fr} 低于训练下限 124 帧（T-2：低于 ~5s 动作表现异常）")
        elif fr > ac.H3_MAX_FRAMES:
            probs.append(f"帧数 {fr} 超过单次上限 362 帧（15.08s）")
        else:
            probs.append(f"帧数 {fr} 不在 H3 帧网格 17k+5 上")
    if dur is not None and abs(dur - ac.frames_to_seconds(fr)) > 0.05:
        probs.append(f"时长 {dur:.2f}s 与帧数 {fr}（{ac.frames_to_seconds(fr):.2f}s）不符")
    if not probs:
        return
    ref = dur if dur is not None else ac.frames_to_seconds(fr)
    up = _snap_up(ref)
    downs = [n for n in ac.grid_frames() if ac.frames_to_seconds(n) <= ref + 0.005]
    if ac.is_grid_frames(fr):
        fix = f"把时长改为 {ac.frames_to_seconds(fr):.2f}（{fr} 帧）"
    elif up is None:
        fix = "拆成两段，每段 ≤362 帧（15.08s），一段 = 一条完整动作链（P10）"
    elif fr < ac.H3_MIN_FRAMES and ref < 5.17:
        fix = (f"延长到 124 帧（5.17s）以上；若本镜是纯色卡/静帧插入，则根本不送 H3，本地生成（D2）")
    else:
        fix = f"改为 帧数 {up} / 时长 {ac.frames_to_seconds(up):.2f}"
        if downs:
            fix += f"（或向下取 {downs[-1]} / {ac.frames_to_seconds(downs[-1]):.2f}，需删减动作或台词）"
    add("error", "VP-frames", "；".join(probs) + f" → {fix}", frames=fr, dur=dur, snap_up=up)


def _check_pictures(shot: dict, add) -> None:
    meta, h3 = shot["meta"], shot["h3"]
    raw = meta.get("references", "")
    fixed, issues = _fix_refs(raw)
    if issues:
        add("error", "VP-picture", f"references 写法不合契约（{'、'.join(issues)}）：「{raw}」→ 改为半角 '1=ID; 2=ID'（分号分隔）；"
            "下面按纠正后的编号继续核对", raw=raw)
    refs = ac.parse_references(fixed)
    nums = [n for n, _ in refs if n is not None]
    unnum = [r for n, r in refs if n is None]
    if unnum:
        add("error", "VP-picture", f"references 条目缺编号：{unnum} → 写成 'N=参考图ID'，N 从 1 起连续（E1）")
    dup = sorted({n for n in nums if nums.count(n) > 1})
    if dup:
        add("error", "VP-picture", f"references 编号重复：{dup} → 每个编号只能出现一次（E1）")
    uniq = sorted(set(nums))
    if uniq and uniq != list(range(1, len(uniq) + 1)):
        add("error", "VP-picture", f"references 编号 {nums} 不是从 1 起连续（E1：占位槽删除后剩余从 2 起 → 18 镜/16 镜集体失败）"
            f"→ 重编号为 1..{len(uniq)} 并逐个核对 <Picture N> 指向（可先跑 slot_order_check.py）", nums=nums)
    pics = [(int(m.group(1)), m.start()) for m in PICTURE_RE.finditer(h3)]
    defined = set(nums)
    undef = sorted({n for n, _ in pics if n not in defined})
    for n in undef:
        off = next(o for k, o in pics if k == n)
        add("error", "VP-picture", f"<Picture {n}> 未在 references 中定义（已定义：{sorted(defined) or '无'}）→ 在 references "
            f"加 '{n}=参考图ID'，或改用已定义编号", _line_of(shot, off), picture=n)
    first: list[int] = []
    for n, _ in pics:
        if n not in first:
            first.append(n)
    if first != sorted(first):
        add("error", "VP-picture", f"<Picture N> 首次引用顺序为 {first}，必须升序（T-2：编号与引用顺序一致）→ 按首次出现顺序重排 "
            f"references 编号并同步改写 <Picture N>", order=first)
    unref = sorted(defined - set(first))
    if unref:
        add("warn", "VP-picture", f"references 中 {unref} 从未被 <Picture N> 引用：生成器不知道这张图对应谁 → 在对应主体/场景句后加 "
            f"<Picture N>，或从 references 删除并重编号", unreferenced=unref)
    for m in PICTURE_LOOSE.finditer(h3):
        if not PICTURE_RE.fullmatch(m.group(0)):
            n = re.search(r"\d+", unicodedata.normalize("NFKC", m.group(0)))
            add("error", "VP-picture", f"参考图标记写法不规范「{m.group(0)}」→ 只能写 '<Picture {n.group(0) if n else 'N'}>'"
                "（半角尖括号、大写 P、一个空格、数字）", _line_of(shot, m.start()))


# ------------------------------------------------------------------ 入口

def analyze(prompts: str | Path, anchors_path: str | Path | None = None,
            storyboard_path: str | Path | None = None) -> tuple[list[Finding], dict]:
    for p in (prompts, anchors_path, storyboard_path):
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
               f"标题「{raw}」没有被识别为镜头（契约：`## SHOT-nnn`——两个 #、大写 SHOT、三位数字），这一镜完全没被检查{spill}"
               f" → 改为 `## {sug}` 后重跑")
        findings.append(Finding("error", "FMT-shot-heading", msg, f"{pname}:{ln}",
                                {"heading": raw, "suggest": sug, "absorbed_by": prev, "in_code": swallowed}))
    if not shots:
        if bad_heads:
            return findings, {"summary": "没有任何合规的 '## SHOT-nnn' 镜：先按上面的 FMT-shot-heading 改标题。", "per_shot": {}}
        inside = [i for i, ln in enumerate(ptext.splitlines(), 1) if RE_STRICT_HEADING.match(ln.strip())]
        ac.die(f"{prompts} 中没有解析到任何 '## SHOT-nnn' 镜（格式见 format-contracts.md §2）"
               + (f"；第 {inside[0]} 行的镜头标题在代码块围栏内（外层 ```` 或未闭合的 ```）→ 去掉外层围栏" if inside else ""))
    # 每镜区段内非 h3 的代码块语言标记（```H3 / ```json …）→ 给 VP-struct 提示
    lines_all = ptext.splitlines()
    starts = sorted(s["line"] for s in shots) + [len(lines_all) + 1]
    for s in shots:
        if s["h3"] is None:
            end = next(x for x in starts if x > s["line"])
            s["_fence_langs"] = [ln.strip()[3:].strip() or "（无）" for ln in lines_all[s["line"]:end - 1]
                                 if ln.strip().startswith("```") and ln.strip()[3:].strip() not in ("",)]
    anchors, atext = None, ""
    if anchors_path:
        anchors, atext, abom = _parse_compat(ac.parse_anchors, anchors_path)
        if abom:
            findings.append(_bom_finding(anchors_path))
        prev = None
        for i, ln in enumerate(atext.splitlines(), 1):
            ok = RE_STRICT_ANCHOR.match(ln)
            if ok:
                prev = ok.group(1)
            elif RE_ANCHORLIKE.match(unicodedata.normalize("NFKC", ln)):
                sug = re.search(r"([A-Za-z]{3}-[A-Za-z0-9-]+)", unicodedata.normalize("NFKC", ln))
                findings.append(Finding("error", "VP-anchor", f"锚点卡标题「{ln.strip()}」不合契约，没有被识别"
                                        + (f"：其下的 锚点句/禁用 被并进了上一张卡 {prev}，{prev} 的逐字核对结论不可信" if prev else "")
                                        + f" → 改为 '## ANCHOR: {sug.group(1).upper() if sug else 'XXX-ID'}'（两个 #、半角冒号、大写 ID）",
                                        f"{Path(anchors_path).name}:{i}"))
    sb_map = {}
    if storyboard_path:
        rows, sbtext, sbom = _parse_compat(ac.parse_storyboard, storyboard_path)
        if sbom:
            findings.append(_bom_finding(storyboard_path))
        findings.extend(_storyboard_issues(sbtext, Path(storyboard_path).name))
        sb_map = {r["shot"]: r for r in rows}
        if not sb_map:
            ac.die(f"{storyboard_path} 中没有找到含 镜号/时长(s) 表头的分镜表（format-contracts.md §1）")
    for sid, n in Counter(s["shot"] for s in shots).items():
        if n > 1:
            lns = [str(s["line"]) for s in shots if s["shot"] == sid]
            findings.append(Finding("error", "VP-struct", f"镜号 {sid} 出现 {n} 次（行 {', '.join(lns)}；集内唯一）→ 合并或改号，并同步分镜表与"
                                    "参考图 ID（E2）；两处都已逐一检查，但下游只会认其中一处", sid))
    per_shot = {}
    for s in shots:
        fs = lint_shot(s, anchors, sb_map.get(s["shot"]), bool(storyboard_path), atext)
        findings.extend(fs)
        key = s["shot"] if s["shot"] not in per_shot else f"{s['shot']}（第 {s['line']} 行重复）"
        per_shot[key] = {lv: sum(1 for f in fs if f.level == lv) for lv in ("error", "warn", "info", "visual")}
    lines = []
    for k, c in per_shot.items():
        lines.append(f"  {k}：{'不通过' if c['error'] else '通过'}（{c['error']} 错误 / {c['warn']} 警告）")
    summary = "逐镜：\n" + "\n".join(lines)
    if not anchors_path:
        summary += "\n（未给 --anchors：P1 锚点句逐字核对已跳过）"
    if not storyboard_path:
        summary += "\n（未给 --storyboard：动作镜只按动作词判定，未做 P7 时长对账）"
    summary += "\n下一步：0 error 后跑 direction_audit.py 与 slot_order_check.py，再进 prepare。"
    return findings, {"summary": summary, "per_shot": per_shot}


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[bool] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        results.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  —— {detail}" if detail and not cond else ""))

    good, bad, own = ac.FIXTURES / "good", ac.FIXTURES / "bad", ac.FIXTURES / "prompt_lint"

    f, _ = analyze(good / "video-prompts.md", good / "anchors.md", good / "storyboard.md")
    errs = [x for x in f if x.level == "error"]
    check("good: 0 error", not errs, str([(x.code, x.where, x.msg[:50]) for x in errs]))
    check("good: 0 warn", not [x for x in f if x.level == "warn"],
          str([(x.code, x.msg[:50]) for x in f if x.level == "warn"]))

    f, _ = analyze(bad / "video-prompts.md", bad / "anchors.md", bad / "storyboard.md")

    def codes(shot: str, level: str = "error") -> set:
        return {x.code for x in f if x.where.startswith(shot) and x.level == level}

    exp3 = {"VP-struct", "VP-ban", "VP-realtime", "VP-picture", "VP-anchor", "VP-dialogue", "VP-distinct", "VP-frames"}
    check("bad SHOT-003: 结构/禁令/实时/参考/锚点/对白/差异化/帧网格 均报 error", exp3 <= codes("SHOT-003"),
          f"缺 {exp3 - codes('SHOT-003')}")
    check("bad SHOT-003: VP-position + VP-adjective 报 warn", {"VP-position", "VP-adjective"} <= codes("SHOT-003", "warn"),
          str(codes("SHOT-003", "warn")))
    slow = [x for x in f if x.code == "VP-realtime" and "Slow motion" in x.msg]
    check("bad SHOT-003: 非否定 'Slow motion' 单独报 error（A3）", bool(slow) and slow[0].level == "error")
    anc = [x for x in f if x.code == "VP-anchor" and x.level == "error"]
    check("bad SHOT-003: 两个锚点句都缺（P1）", len(anc) == 2, str(len(anc)))
    adjw = {x.data.get("word") for x in f if x.code == "VP-adjective"}
    check("bad SHOT-003: epic/spectacular/gorgeous 被点名", {"epic", "spectacular", "gorgeous"} <= adjw, str(adjw))
    check("bad SHOT-005: VP-generator-unsafe + VP-frames 报 error", {"VP-generator-unsafe", "VP-frames"} <= codes("SHOT-005"),
          str(codes("SHOT-005")))
    cats = {x.data.get("category") for x in f if x.code == "VP-generator-unsafe"}
    check("bad SHOT-005: 纯色画面/字卡/精确文字 三类都识别（D2）", {"纯色画面", "字卡/片尾卡", "精确文字"} <= cats, str(cats))
    check("bad SHOT-005: 禁令句末行存在 → 不报 VP-ban", "VP-ban" not in codes("SHOT-005"))
    fr = [x for x in f if x.code == "VP-frames" and x.where.startswith("SHOT-003")]
    check("bad SHOT-003: 帧数 290 → 建议吸附 294", bool(fr) and "294" in fr[0].msg, fr[0].msg if fr else "")

    f, _ = analyze(own / "video-prompts.md", own / "anchors.md")
    check("own SHOT-020: VP-symbol warn（D4 禁用项缺）", "VP-symbol" in codes("SHOT-020", "warn"))
    sym = [x for x in f if x.code == "VP-symbol"]
    check("own SHOT-020: 缺的是 no plus sign / no second bar",
          bool(sym) and set(sym[0].data["missing"]) == {"no plus sign", "no second bar"}, str(sym[0].data if sym else ""))
    check("own SHOT-020: negative_prompt / 光柱 / 人群 均 warn",
          {"VP-negative", "VP-light", "VP-crowd"} <= codes("SHOT-020", "warn"), str(codes("SHOT-020", "warn")))
    check("own SHOT-020: 慢动作已声明 → 不报 VP-realtime error", "VP-realtime" not in codes("SHOT-020"))
    check("own SHOT-020: <Picture> 顺序 [1,3,2] → VP-picture error",
          any(x.code == "VP-picture" and "升序" in x.msg for x in f if x.where.startswith("SHOT-020")))
    dl = [x.msg for x in f if x.code == "VP-dialogue" and x.where.startswith("SHOT-020") and x.level == "error"]
    check("own SHOT-020: 缺 [Chinese] + 未闭合 <d> 都报 error",
          any("[Chinese]" in m for m in dl) and any("闭合" in m for m in dl), str(dl))
    check("own SHOT-021: 干净镜 0 error 0 warn（否定式光柱/虚化人群/符号禁用写全）",
          not codes("SHOT-021") and not codes("SHOT-021", "warn"), str(codes("SHOT-021") | codes("SHOT-021", "warn")))
    check("own SHOT-022: 慢动作声明 + 实时句并存 → VP-realtime warn", "VP-realtime" in codes("SHOT-022", "warn"))
    check("own SHOT-022: 帧数 192 时长 8.00 合法 → 无 VP-frames", "VP-frames" not in codes("SHOT-022"))

    check("两位小数容差：时长 5.17s 吸附为 124 帧（不是 141）", _snap_up(5.17) == 124 and _snap_up(10.83) == 260
          and _snap_up(12.00) == 294, str((_snap_up(5.17), _snap_up(10.83), _snap_up(12.00))))

    # ---- 对抗回归（输入在临时目录现场生成：BOM/CRLF 字节不会被 git 规范化掉）
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        gtxt = (good / "video-prompts.md").read_text(encoding="utf-8")
        (tdp / "vp.md").write_bytes(("﻿" + gtxt[gtxt.index("## SHOT-002"):]).replace("\n", "\r\n").encode("utf-8"))
        for n in ("anchors.md", "storyboard.md"):
            t = (good / n).read_text(encoding="utf-8")
            t = t[t.index("## ANCHOR") if n == "anchors.md" else t.index("| 段号"):]
            (tdp / n).write_bytes(("﻿" + t).replace("\n", "\r\n").encode("utf-8"))
        f, ex = analyze(tdp / "vp.md", tdp / "anchors.md", tdp / "storyboard.md")
        check("对抗 BOM+CRLF（首行即 ## SHOT / 表头 / ANCHOR）：仍解析出 SHOT-002，0 error，3 条 FMT-bom（修复前：退出码 2）",
              "SHOT-002" in ex["per_shot"] and not [x for x in f if x.level == "error"]
              and sum(1 for x in f if x.code == "FMT-bom") == 3, str([(x.code, x.msg[:40]) for x in f if x.level != "info"]))

        adv = """# adv
## SHOT-001
- 时长：8.00
- 帧数：192
- references: 1=CHR-A-BOARD，2=CHR-B-BOARD
- 起始帧方位: 苏晓＝LEFT; 殇月=RIGHT
- 锚点: ——
- 慢动作: 否

```h3
subject_definitions：
  [S1] the girl on the LEFT <Picture 1>
summary:
  She knows no fear and leaps in slow motion.
retention_analysis:
  Slow motion is not used here. A block of stone; the elder is in charge of the hall.
detailed_description:
  Real-time speed throughout, no slow motion.
  [S1] says "快走" to the woman <Picture 2>.
  No logo, watermark or UI. No flashlight, torch beam or spotlight.
overall_soundscape:
  x
non_diegetic_music:
  x
No captions, subtitles, or dialogue text overlays appear at any moment.
```

## SHOT-002
- 时长: 10,83
- 帧数: 260帧

```h3
subject_definitions:
  a
No captions, subtitles, or dialogue text overlays appear at any moment.

## SHOT-003
- 时长: 8.00
```

## SHOT-4
- 时长: 8.00
"""
        (tdp / "adv.md").write_text(adv, encoding="utf-8")
        f, ex = analyze(tdp / "adv.md")
        msgs = " ".join(x.msg for x in f)
        heads = {x.data.get("suggest"): x.data.get("in_code") for x in f if x.code == "FMT-shot-heading"}
        check("对抗：`## SHOT-4` 与被未闭合 h3 吞掉的 `## SHOT-003` 都报 FMT-shot-heading（修复前：两镜静默消失）",
              heads.get("SHOT-004") is False and heads.get("SHOT-003") is True, str(heads))
        check("对抗：段名用全角冒号 → VP-struct 指明「全角冒号」", any(x.code == "VP-struct" and "全角冒号" in x.msg for x in f))
        slow_err = [x for x in f if x.code == "VP-realtime" and x.level == "error" and x.data.get("text")]
        check("对抗：`慢动作: 否` 不构成豁免；'no fear and leaps in slow motion' 报 error，'Slow motion is not used' 不报",
              len(slow_err) == 1 and slow_err[0].where.endswith(":14")
              and any(x.code == "VP-realtime" and x.level == "info" and "未声明" in x.msg for x in f),
              str([(x.level, x.where, x.msg[:30]) for x in f if x.code == "VP-realtime"]))
        check("对抗：references 用全角逗号 → VP-picture error 点名'逗号'，且 <Picture 2> 不再误报未定义",
              any(x.code == "VP-picture" and "逗号" in x.msg for x in f) and "未在 references 中定义" not in msgs)
        check("对抗：起始帧方位 全角＝ 仍计 2 人 → VP-distinct 照报", any(x.code == "VP-distinct" and "起始帧方位 2 人" in x.msg for x in f))
        check("对抗：引号里的中文台词 → VP-dialogue（不是'精确文字'）",
              any(x.code == "VP-dialogue" and "快走" in x.msg for x in f)
              and not any(x.code == "VP-generator-unsafe" and "快走" in x.msg for x in f))
        check("对抗：'No logo, watermark or UI' / 'No flashlight, torch beam or spotlight' 并列否定不误报",
              not any(x.code in ("VP-generator-unsafe", "VP-light") and x.where.startswith("SHOT-001") for x in f),
              str([(x.code, x.msg[:40]) for x in f if x.code in ("VP-generator-unsafe", "VP-light")]))
        check("对抗：'——' 不当锚点 ID；'a block of stone / in charge of' 不算动作词",
              not any(x.code == "VP-anchor" for x in f) and not any("block" in str(x.data.get("verbs", "")) for x in f))
        check("对抗：时长 '10,83' / 帧数 '260帧' → 给出可照抄的改法",
              "'- 时长: 10.83'" in msgs and "'- 帧数: 260'" in msgs)

        (tdp / "an.md").write_text("## ANCHOR: CHR-A\n- 锚点句 EN: ``A slender girl.``\n- 禁用: no jewelry at all, no armor\n\n"
                                   "## ANCHOR：CHR-B\n- 锚点句 EN: `a stone god`\n- 禁用: no weapon\n", encoding="utf-8")
        (tdp / "vpa.md").write_text("## SHOT-001\n- 时长: 8.00\n- 帧数: 192\n- references: 1=CHR-A-BOARD\n- 锚点: CHR-A; CHR-B\n\n"
                                    "```h3\nsubject_definitions:\n  [S1] a slender girl <Picture 1>\nsummary:\n  x\nretention_analysis:\n"
                                    "  x\ndetailed_description:\n  No jewelry at all, no armor.\noverall_soundscape:\n  x\n"
                                    "non_diegetic_music:\n  x\n" + ac.BAN_LINE + "\n```\n", encoding="utf-8")
        f, _ = analyze(tdp / "vpa.md", tdp / "an.md")
        check("对抗：`## ANCHOR：` 全角冒号 → 报'并进了上一张卡 CHR-A'（修复前：CHR-A 被 CHR-B 的句子覆盖后假通过）",
              any(x.code == "VP-anchor" and "并进了上一张卡 CHR-A" in x.msg for x in f))
        (tdp / "an.md").write_text("## ANCHOR: CHR-A\n- 锚点句 EN: ``A slender girl.``\n- 禁用: no jewelry at all, no armor\n\n"
                                   "## ANCHOR: CHR-B\n- 锚点句 EN: `a stone god`\n- 禁用: no weapon\n", encoding="utf-8")
        f, _ = analyze(tdp / "vpa.md", tdp / "an.md")
        check("对抗：``双反引号``锚点句被正确剥离，差异诊断为'大小写与句末标点'",
              any(x.code == "VP-anchor" and "仅大小写与句末标点不同" in x.msg and "`A slender girl.`" in x.msg for x in f),
              str([x.msg[:80] for x in f if x.code == "VP-anchor"]))

        sb = (good / "storyboard.md").read_text(encoding="utf-8").replace("苏晓佯攻右肩→", "苏晓佯攻右肩|")
        (tdp / "sb_shift.md").write_text(sb, encoding="utf-8")
        f, _ = analyze(good / "video-prompts.md", good / "anchors.md", tdp / "sb_shift.md")
        check("对抗：分镜单元格里没转义的 | → FMT-table-row warn（列错位的根因）",
              any(x.code == "FMT-table-row" and x.where.startswith("SHOT-002") for x in f))

    # CLI：退出码与 --json
    me = [sys.executable, str(Path(__file__).resolve())]
    p = subprocess.run(me + [str(good / "video-prompts.md"), "--anchors", str(good / "anchors.md")], capture_output=True, text=True)
    check("CLI good → 退出码 0", p.returncode == 0, p.stdout[-300:])
    p = subprocess.run(me + [str(bad / "video-prompts.md"), "--json"], capture_output=True, text=True)
    try:
        js = json.loads(p.stdout)
        okj = p.returncode == 1 and js["ok"] is False and js["counts"]["error"] > 0
    except ValueError:
        okj = False
    check("CLI bad --json → 退出码 1 且 JSON 可解析", okj, p.stdout[:200])
    p = subprocess.run(me + [str(own / "no-such-file.md")], capture_output=True, text=True)
    check("CLI 文件不存在 → 退出码 2", p.returncode == 2)

    n_ok = sum(results)
    print(f"SELFTEST {'PASS' if all(results) else 'FAIL'}（{n_ok}/{len(results)}）")
    return 0 if all(results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompts", nargs="?", help="video-prompts.md")
    ap.add_argument("--anchors", help="anchors.md（启用 P1 锚点句逐字核对与 D4 符号禁用项检查）")
    ap.add_argument("--storyboard", help="storyboard.md（启用按拍数判定动作镜与 P7 时长对账）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="用 fixtures 自测")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.prompts:
        ap.print_usage(sys.stderr)
        ac.die("需要 video-prompts.md 路径（或 --selftest）")
    findings, extra = analyze(a.prompts, a.anchors, a.storyboard)
    return ac.emit(TITLE, findings, a.json, extra)


if __name__ == "__main__":
    sys.exit(main())
