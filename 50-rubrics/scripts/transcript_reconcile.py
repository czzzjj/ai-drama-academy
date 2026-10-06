#!/usr/bin/env python3
"""台词三方对账 transcript_reconcile —— 视频验收（P8）时、判"缺句/多字/串台"之前必跑；它只给事实，不给重出结论。

用途：
  逐镜做台词三方对账：剧本侧（storyboard.md 的 对白 列）↔ 提示词侧（video-prompts.md 的 <d>）↔ 转写侧
  （transcripts.tsv / .json）。三方都归一化（NFKC、去标点、去空白、英文小写）后逐字比较（difflib 字符级）：
    · 剧本 ≠ 提示词 → error（P7 双文档对账）；说话人经 角色映射 对不上 → error；
    · 转写比剧本缺字/缺句 → error，并显示缺失片段与容量核算（若换 seed 仍缺 → D3 结构性缺陷，回分镜核算容量）；
    · 转写多出的字 → warn；无对白镜出现转写 → warn「先证伪工具（D5）」；命中已知 ASR 幻觉 → warn；
    · 置信度 < 0.6 → visual「低置信：做 3 窗复核 + 抽帧核对口型（D5 双通道）」。
  多给几个转写文件（--transcripts 主转写 w2 w3）即视为同一音轨的错位时间窗：窗间互斥 → 符合误听特征；
  其他窗听到了主窗缺的片段 → 缺字降为 warn。
  铁律：转写是单通道证据。本脚本绝不仅凭转写下"重出"结论；凡涉及是否重出，一律写"需第二通道证据（抽帧/听感）确认后再判"。

溯源：P7（双文档对账）, M10（三方台词对账 + 视频双通道验收）, D3（对白容量：换 seed 各缺不同句、二次延长才补齐）,
     D5（QC 工具会骗人："字幕by索兰娅"幻觉；尾段低笑气声被误听为"救我"，多窗复核后未重出）；另 P8、P9/T-2（7.5 字/秒）。

规则代码（TR-）：
  TR-script-prompt   error  剧本台词 ≠ 提示词 <d>（P7）
  TR-speaker         error  同一句台词的说话人：剧本 ≠ 提示词（[S#] 经 角色映射）
  TR-missing         error  转写比剧本缺字/缺句（显示缺失片段 + 容量核算）；其他窗口听到了该片段 → 降为 warn
  TR-extra           warn   转写比剧本多出的字
  TR-unscripted      warn   无对白镜出现转写：先证伪工具（D5）
  TR-hallucination   warn   命中 academy_common.KNOWN_ASR_HALLUCINATIONS（已知 ASR 幻觉）
  TR-lowconf         visual 置信度 < --low-conf（默认 0.6）
  TR-windows         info   多窗转写对照（窗间一致 / 互斥）
  TR-no-prompt       warn   剧本有台词，提示词文件中没有这一镜
  TR-no-transcript   warn   剧本有台词，转写文件中没有这一镜
  TR-unknown-shot    warn   转写/提示词里的镜号不在分镜表中
  TR-format          warn   转写文件某行格式不符或置信度非法（该行跳过/置信度忽略）；用空格代替 TAB、镜号小写、分镜 对白 句间
                            分隔写成无空格的 / 或全角 ／（已按纠正后的写法对账，偏差照报）
                     info   已忽略括号内舞台提示（（低声）/(beat)）；转写为繁体输出，已按内置常用字表转简体后对账；
                            转写把中文数字写成阿拉伯数字（三年↔3年，数值相同）视为一致
  TR-no-audio        warn   （给 --video-dir 时）视频没有音轨：转写里的文字必为工具编造 / 台词镜丢了音轨（D5、E3）
  FMT-bom            warn   分镜/提示词以 UTF-8 BOM 开头（已去 BOM 解析）

输入格式：70-playbooks/format-contracts.md §5 转写对账输入（TSV：`SHOT-012<TAB>文本<TAB>置信度(可选)`；
          JSON：`{"SHOT-012": {"text": "…", "confidence": 0.62}}` 或 `{"SHOT-012": "…"}`），§1 分镜表 对白 列，
          §2 视频提示词 <d>（相对本文件：../../70-playbooks/format-contracts.md）。
          同一文件中同一镜出现多行 → 文本按行序拼接、置信度取最小值。

--windows 模式（3 窗复核；可选，需要第二个转写工具——本脚本不依赖、不调用它）：
  何时做：TR-lowconf / TR-missing / TR-extra / TR-unscripted / TR-hallucination 任一出现时，先复核再下结论。
  带 --windows 运行时，脚本为每个需要复核的镜打印下面这组命令（--video-dir 给出时自动填视频路径）：
    V="season-01/ep03/shots/SHOT-003.mp4"; O="qc/SHOT-003"; mkdir -p "$O"
    # W1 全长；W2 起点后移 0.4s；W3 前垫 0.4s 静音（让 ASR 的切分边界落在不同位置）
    ffmpeg -v error -y -i "$V" -vn -ac 1 -ar 16000 "$O/w1.wav"
    ffmpeg -v error -y -ss 0.4 -i "$V" -vn -ac 1 -ar 16000 "$O/w2.wav"
    ffmpeg -v error -y -i "$V" -vn -ac 1 -ar 16000 -af "adelay=400:all=1" "$O/w3.wav"
    # 可疑词只在某一段时，加一窗只取它前后各 1s：ffmpeg -v error -y -ss 4.0 -to 6.0 -i "$V" -vn -ac 1 -ar 16000 "$O/w4.wav"
    # 每窗转写（可选工具，任选其一；w2/w3 同理）
    whisper-cli -m models/ggml-large-v3.bin -l zh -f "$O/w1.wav" -otxt -of "$O/w1"            # whisper.cpp
    whisper "$O/w1.wav" --language zh --model medium --output_format json --output_dir "$O"   # openai-whisper
    # 第二通道：口型接触表（每 0.5s 一帧，6×5 张覆盖 15s，够一个 H3 镜；eof_action=pass 保证极短镜也出图）
    ffmpeg -v error -y -i "$V" -vf "fps=2:eof_action=pass,scale=240:-2,tile=6x5" -frames:v 1 "$O/lips.jpg"
    # 视频没有音轨时 w1–w3 会报 "Output file does not contain any stream"：这本身就是证据——转写文字必为工具编造（D5）；
    # 先用 ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$V" 确认（输出为空 = 无音轨）
    # 每窗结果写成契约格式（SHOT-003<TAB>文本<TAB>置信度，置信度可留空），一窗一个文件，然后重跑：
    python3 50-rubrics/scripts/transcript_reconcile.py --storyboard storyboard.md --prompts video-prompts.md \\
        --transcripts transcripts.tsv "$O/w2.tsv" "$O/w3.tsv"
  判读（D5）：3 窗结果互斥且置信度均低 → 工具误听（实证："救我"即此型，复核后未重出）；
             3 窗一致缺同一段 → 更可能真实缺句：换 seed 仍缺 → D3 结构性缺陷，回分镜按 7.5 字/秒核算容量；
             任何结论都需第二通道证据（抽帧口型 / 听感）确认后再判。
  不带任何输入只给 --windows：打印本段说明后退出 0。

用法示例：
  python3 50-rubrics/scripts/transcript_reconcile.py --storyboard season-01/ep03/storyboard.md \\
      --prompts season-01/ep03/video-prompts.md --transcripts season-01/ep03/qc/transcripts.tsv
  python3 50-rubrics/scripts/transcript_reconcile.py --storyboard storyboard.md --prompts video-prompts.md \\
      --transcripts qc/transcripts.tsv --windows --video-dir season-01/ep03/shots
  python3 50-rubrics/scripts/transcript_reconcile.py --storyboard storyboard.md --transcripts t.tsv qc/SHOT-003/w2.tsv qc/SHOT-003/w3.tsv --json
  python3 50-rubrics/scripts/transcript_reconcile.py --selftest

退出码：0 无 error / 1 有 error / 2 用法或环境错误（三方中不足两方、文件不存在或无法解析）
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import academy_common as ac  # noqa: E402
from academy_common import Finding  # noqa: E402

TITLE = "台词三方对账 transcript_reconcile"
SHOT_RE = re.compile(r"^SHOT-\d{3}$")
SPK_RE = re.compile(r"\[(?!Chinese\])([A-Z][A-Za-z]{0,3}\d{1,3})\]")
LINE_D_RE = re.compile(r"<d>\s*\[Chinese\]\s*(.*?)\s*</d>")
RECHECK = {"TR-missing", "TR-extra", "TR-unscripted", "TR-lowconf", "TR-hallucination"}
SECOND = "需第二通道证据（抽帧/听感）确认后再判"


# 常见繁体字 → 简体（一一对应、且不出现在简体文本中的字；ASR 常输出繁体，D5）。表外字不转换，报告里会说明。
_T2S_T = ("這裡裏們個來說為會對時過還沒麼開關國見與學問題東車馬門長風飛發髮書話語讀聽頭點樣場電無實現當從體邊後進動應種經讓謝請愛歡樂師誰嗎給錯錢買賣號雙劍殺戰鬥傷輸贏記歲約齊聖靈龍鳳劉張陳楊黃趙吳孫鄭蘇曉殤妳"
          "認識決斷線紅綠藍顏鐵銀槍彈砲氣魚鳥雞豬貓親媽爺兒戀憶夢島灣漢華燈陽陰雲霧飯餓喫飲寫畫聲響覺聞視緊離別歸處許該於麵隻臺颱檯鐘鍾範製準鬆穀幹醜衝獲歷曆嚮復複髒臟並併幾機極際隊陣陸險難雜雖靜頁順須領顯類館驚鮮麗黨齒亂傳價側倆債僅優內兩冊劃劇勁勝勢勵區協單厲參員圍圓團園圖報塊壓壞壯夠奪奮婦寧寶將專尋導屬帶帳幫廣廢強彎徑徹恆惡態慘慣憑懷戲戶拋挾捨掃掛換揮損搶擁擇擊擔據擠擴擺攔敗敵數斂斬晝暫條棄構樓標橋權歐殘毀滅濕災煙爭牆犧狀獨獸獻環產畢療盡監眾睜矯礎確禮禍稱穩窮競筆節簡糧紀純紙級細終組結絕統絲綁維網緒練縣總繼續罰罵義習聯職肅脫腦腳膽臉舊艱萬葉蓋蘭蟲術衛補裝規觀計訊討訓設訴診詞試詩誕誠誤課調談論諸謀謊證議護變豐貝負財貨責貴費資賊賜質購贈趕躍軍軟輕較輩輪轉辦辭農連週運達違遠適遲選遺鄉醫釋針鈴鋒錄鏈鏡閃閉閒間閣闆闖隨隱韓頂項預頑頓頻願顧飄餘騎騙驗鬧鳴麥龜衆誒唄囉嘍噹嚇嘆嘗囑寢審憂擋兇劊匯叢吶燒燭爐爾牽猶瑪異瘋癒皚盤睏礙祕禱穌窩竊籠緣縫繞纏罷羅脅腸膚艷莊蒼薦蘆虛蝦蠻襲覽訂詳誇誌諾謎謹譜讚豈賭賴趨蹤軌輝轟遞遜鄰鍋鎖鎮鑰閱闊頸颳飢餅餵驅驕鬍鬱鷹鹽黴齡")
_T2S_S = ("这里里们个来说为会对时过还没么开关国见与学问题东车马门长风飞发发书话语读听头点样场电无实现当从体边后进动应种经让谢请爱欢乐师谁吗给错钱买卖号双剑杀战斗伤输赢记岁约齐圣灵龙凤刘张陈杨黄赵吴孙郑苏晓殇你"
          "认识决断线红绿蓝颜铁银枪弹炮气鱼鸟鸡猪猫亲妈爷儿恋忆梦岛湾汉华灯阳阴云雾饭饿吃饮写画声响觉闻视紧离别归处许该于面只台台台钟钟范制准松谷干丑冲获历历向复复脏脏并并几机极际队阵陆险难杂虽静页顺须领显类馆惊鲜丽党齿乱传价侧俩债仅优内两册划剧劲胜势励区协单厉参员围圆团园图报块压坏壮够夺奋妇宁宝将专寻导属带帐帮广废强弯径彻恒恶态惨惯凭怀戏户抛挟舍扫挂换挥损抢拥择击担据挤扩摆拦败敌数敛斩昼暂条弃构楼标桥权欧残毁灭湿灾烟争墙牺状独兽献环产毕疗尽监众睁矫础确礼祸称稳穷竞笔节简粮纪纯纸级细终组结绝统丝绑维网绪练县总继续罚骂义习联职肃脱脑脚胆脸旧艰万叶盖兰虫术卫补装规观计讯讨训设诉诊词试诗诞诚误课调谈论诸谋谎证议护变丰贝负财货责贵费资贼赐质购赠赶跃军软轻较辈轮转办辞农连周运达违远适迟选遗乡医释针铃锋录链镜闪闭闲间阁板闯随隐韩顶项预顽顿频愿顾飘余骑骗验闹鸣麦龟众诶呗啰喽当吓叹尝嘱寝审忧挡凶刽汇丛呐烧烛炉尔牵犹玛异疯愈皑盘困碍秘祷稣窝窃笼缘缝绕缠罢罗胁肠肤艳庄苍荐芦虚虾蛮袭览订详夸志诺谜谨谱赞岂赌赖趋踪轨辉轰递逊邻锅锁镇钥阅阔颈刮饥饼喂驱骄胡郁鹰盐霉龄")
T2S = str.maketrans(_T2S_T, _T2S_S)
CN_NUM = "零〇一二两三四五六七八九十百千万"
DIRECTION_RE = re.compile(r"[（(【\[][^（）()【】\[\]]{0,20}[）)】\]]")       # 括号内舞台提示：（低声）(beat)【停顿】
SPLIT_UNSPACED = re.compile(r"\s*[/／]\s*(?=[^：:/／\s]{1,20}[：:])")             # '月落之时/苏晓：我知道'
NO_AUDIO = "（视频无音轨）"


def strip_directions(s: str) -> tuple[str, list[str]]:
    found = DIRECTION_RE.findall(s or "")
    return (DIRECTION_RE.sub("", s or ""), found)


def cn2int(s: str) -> int | None:
    """'三十二' → 32，'两' → 2，'一百零五' → 105，'三五' → 35（逐位读法）；不是中文数字返回 None。"""
    if not s or any(c not in CN_NUM for c in s):
        return None
    d = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if not any(c in "十百千万" for c in s):
        return int("".join(str(d[c]) for c in s))
    total, sec, num = 0, 0, 0
    for c in s:
        if c in d:
            num = d[c]
        elif c == "万":
            total += (sec + num) * 10000
            sec = num = 0
        else:
            unit = {"十": 10, "百": 100, "千": 1000}[c]
            sec += (num or 1) * unit
            num = 0
    return total + sec + num


def _nkey(name: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", name or ""))


def split_script(dialogue: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], bool]:
    """academy_common.parse_dialogue 只按 ' / '（两侧空格）分句；这里再拆无空格的 / 与全角 ／（后面紧跟 '名字：'）。"""
    out, fixed = [], False
    for spk, text in dialogue:
        parts = SPLIT_UNSPACED.split(text)
        if len(parts) == 1:
            out.append((spk, text))
            continue
        fixed = True
        out.append((spk, parts[0].strip()))
        for seg in parts[1:]:
            m = re.match(r"^\s*([^：:]{1,20})[：:]\s*(.*)$", seg)
            out.append((m.group(1).strip(), m.group(2).strip()) if m else ("?", seg.strip()))
    return out, fixed


def _read(path: str | Path) -> tuple[str, bool]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        ac.die(f"{path} 不是 UTF-8 编码（format-contracts §0.1）：另存为 UTF-8 后重跑")
    return (text[1:], True) if text.startswith("\ufeff") else (text, False)


def _parse_compat(parser, path: str | Path):
    """academy_common 解析器的 BOM 兼容包装：带 BOM 时解析去 BOM 的临时副本（行号不变）。"""
    path = Path(path)
    text, bom = _read(path)
    if not bom:
        return parser(path), False
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / path.name
        tmp.write_text(text, encoding="utf-8")
        out = parser(tmp)
    for s in out:
        if isinstance(s, dict) and "file" in s:
            s["file"] = str(path)
    return out, True


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


def has_audio(path: Path) -> bool | None:
    """有音轨 True / 无音轨 False / 无法判断（无 ffprobe、文件坏）None。"""
    if not ac.have("ffprobe"):
        return None
    try:
        info = ac.ffprobe_json(path)
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError):
        return None
    return any(st.get("codec_type") == "audio" for st in info.get("streams", []))


def windows_guide() -> str:
    doc = __doc__ or ""
    a = doc.find("--windows 模式")
    b = doc.find("用法示例：")
    return doc[a:b].rstrip() if a >= 0 and b > a else "（说明缺失）"


# ------------------------------------------------------------------ 归一化

def norm_map(s: str) -> tuple[str, list[int]]:
    """去标点/空白、NFKC、英文小写；返回 (归一化串, 每个字符在原串中的下标)。"""
    out, idx = [], []
    for i, ch in enumerate(s or ""):
        for c in unicodedata.normalize("NFKC", ch).translate(T2S):        # 繁→简（常用字表，一一对应）
            if unicodedata.category(c)[0] in "LN":
                out.append(c.lower())
                idx.append(i)
    return "".join(out), idx


def norm(s: str) -> str:
    return norm_map(s)[0]


def _mark(orig: str, idx: list[int], i1: int, i2: int, pad: int = 12) -> str:
    a, b = idx[i1], idx[i2 - 1] + 1
    lo, hi = max(0, a - pad), min(len(orig), b + pad)
    return ("…" if lo else "") + orig[lo:a] + "【" + orig[a:b] + "】" + orig[b:hi] + ("…" if hi < len(orig) else "")


# ------------------------------------------------------------------ 读入

def load_transcripts(path: str | Path) -> tuple[dict, list[Finding]]:
    p = Path(path)
    if not p.is_file():
        ac.die(f"转写文件不存在：{path}")
    notes: list[Finding] = []
    out: dict = {}

    warned = set()

    def warn_once(kind: str, msg: str, where: str):
        if kind not in warned:
            warned.add(kind)
            notes.append(Finding("warn", "TR-format", msg, where))

    def put(shot: str, text: str, conf):
        if shot in out:
            out[shot]["text"] += text
            if conf is not None:
                out[shot]["conf"] = conf if out[shot]["conf"] is None else min(out[shot]["conf"], conf)
            out[shot]["rows"] += 1
        else:
            out[shot] = {"text": text, "conf": conf, "rows": 1}

    def conf_of(v, where):
        if v is None or str(v).strip() == "":
            return None
        try:
            c = float(v)
        except (TypeError, ValueError):
            notes.append(Finding("warn", "TR-format", f"置信度不是数字「{v}」，已忽略 → 写 0–1 之间的小数或留空", where))
            return None
        if not 0 <= c <= 1:
            notes.append(Finding("warn", "TR-format", f"置信度 {c} 不在 0–1，已忽略", where))
            return None
        return c

    if p.suffix.lower() == ".json":
        try:
            data = json.loads(p.read_text(encoding="utf-8-sig"))          # 容忍 BOM
        except UnicodeDecodeError:
            ac.die(f"转写 JSON 不是 UTF-8 编码：{path}（format-contracts §0.1）→ 另存为 UTF-8 后重跑")
        except ValueError as e:
            ac.die(f"转写 JSON 无法解析：{path}（{e}）")
        if not isinstance(data, dict):
            ac.die(f"转写 JSON 顶层须为对象 {{\"SHOT-012\": …}}：{path}")
        for k, v in data.items():
            if not SHOT_RE.match(k):
                if SHOT_RE.match(k.strip().upper()):
                    warn_once("case", f"镜号写成了「{k}」等非规范形式（已按大写 SHOT-nnn 读入）→ 统一写 SHOT-nnn", p.name)
                    k = k.strip().upper()
                else:
                    notes.append(Finding("warn", "TR-format", f"键「{k}」不是镜号 SHOT-nnn，已跳过", p.name))
                    continue
            if isinstance(v, dict):
                txt = v.get("text")
                put(k, "" if txt is None else str(txt), conf_of(v.get("confidence", v.get("conf")), f"{k} {p.name}"))
            else:
                put(k, "" if v is None else str(v), None)
    else:
        try:
            raw = p.read_text(encoding="utf-8-sig")                        # 容忍 BOM（否则首行镜号读不出 → 漏镜）
        except UnicodeDecodeError:
            ac.die(f"转写文件不是 UTF-8 编码：{path}（format-contracts §0.1）")
        for i, ln in enumerate(raw.splitlines(), 1):
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) < 2:
                m = re.match(r"^\s*(SHOT-\d{3})\s+(.+?)(?:\s+(0\.\d+|1\.0+))?\s*$", ln, re.I)
                if m:
                    warn_once("space", f"第 {i} 行等用空格代替了 TAB（已按空格拆分读入）→ 改为 'SHOT-nnn<TAB>文本<TAB>置信度'",
                              f"{p.name}:{i}")
                    parts = [m.group(1), m.group(2)] + ([m.group(3)] if m.group(3) else [])
            sid = parts[0].strip() if parts else ""
            if len(parts) >= 2 and not SHOT_RE.match(sid) and SHOT_RE.match(sid.upper()):
                warn_once("case", f"第 {i} 行等镜号写成了「{sid}」（已按大写读入）→ 统一写 SHOT-nnn", f"{p.name}:{i}")
                sid = sid.upper()
            if len(parts) < 2 or not SHOT_RE.match(sid):
                notes.append(Finding("warn", "TR-format", f"第 {i} 行不是 'SHOT-nnn<TAB>文本<TAB>置信度'：「{ln[:40]}」，已跳过",
                                     f"{p.name}:{i}"))
                continue
            put(sid, parts[1].strip(), conf_of(parts[2] if len(parts) > 2 else None, f"{p.name}:{i}"))
        if not out and any(f.code == "TR-format" for f in notes):
            ac.die(f"{path} 中没有任何一行符合 'SHOT-nnn<TAB>文本<TAB>置信度'（format-contracts.md §5）——是不是传错了文件？")
    return out, notes


def prompt_dialogue(shot: dict) -> list[tuple[str | None, str | None, str]]:
    """[(说话人ID, 角色名, 台词)]；说话人取同一行 <d> 之前最后一个 [S#]。"""
    mapping = {}
    for part in re.split(r"[;；,，]", (shot["meta"].get("角色映射", "") or "").replace("＝", "=")):
        if "=" in part:
            k, v = part.split("=", 1)
            mapping[k.strip()] = v.strip()
    texts = ac.dialogue_from_h3(shot.get("h3") or "")
    per_line = []
    for ln in (shot.get("h3") or "").splitlines():
        for m in re.finditer(r"<d>(.*?)</d>", ln):           # 与 academy_common.dialogue_from_h3 同口径
            t = ac.dialogue_text(m.group(1))
            if t is None:
                continue
            ids = SPK_RE.findall(ln[:m.start()])
            sid = ids[-1] if ids else None
            per_line.append((sid, mapping.get(sid or ""), t))
    if len(per_line) == len(texts):
        return per_line
    return [(None, None, t) for t in texts]


# ------------------------------------------------------------------ 对账

def analyze(storyboard: str | Path | None = None, prompts: str | Path | None = None, transcripts: list | None = None,
            low: float = 0.6, windows: bool = False, video_dir: str | Path | None = None) -> tuple[list[Finding], dict]:
    transcripts = list(transcripts or [])
    if sum(bool(x) for x in (storyboard, prompts, transcripts)) < 2:
        ac.die("三方对账至少需要两方：--storyboard / --prompts / --transcripts（只要 3 窗说明请单独用 --windows）")
    for p in (storyboard, prompts):
        if p and not Path(p).is_file():
            ac.die(f"文件不存在：{p}")
    F: list[Finding] = []

    def bom_note(path):
        F.append(Finding("warn", "FMT-bom", f"{Path(path).name} 以 UTF-8 BOM 开头（format-contracts §0.1）：已去 BOM 解析；其他按契约读首行的"
                         f"工具会漏读首镜/表头 → 去掉 BOM：`sed -i '1s/^\\xEF\\xBB\\xBF//' {Path(path).name}`", Path(path).name))
    sb = {}
    if storyboard:
        rows, bom = _parse_compat(ac.parse_storyboard, storyboard)
        if bom:
            bom_note(storyboard)
        F.extend(_storyboard_issues(_read(storyboard)[0], Path(storyboard).name))
        sb = {r["shot"]: r for r in rows}
        if not sb:
            ac.die(f"{storyboard} 中没有找到含 镜号/时长(s) 表头的分镜表（format-contracts.md §1）")
    pr = {}
    if prompts:
        lst, bom = _parse_compat(ac.parse_video_prompts, prompts)
        if bom:
            bom_note(prompts)
        pr = {s["shot"]: s for s in lst}
        if not pr:
            ac.die(f"{prompts} 中没有解析到任何 '## SHOT-nnn' 镜（format-contracts.md §2）")
    vdir = Path(video_dir) if video_dir else None
    if vdir is not None and not vdir.is_dir():
        ac.die(f"--video-dir 不是目录：{video_dir}")
    if vdir is not None and not ac.have("ffprobe"):
        F.append(Finding("info", "TR-no-audio", "未找到 ffprobe：跳过'视频有没有音轨'检查（降级；装 ffmpeg 后重跑可多拿一条 D5 证据）"))
    trs = []
    for t in transcripts:
        d, notes = load_transcripts(t)
        trs.append((Path(t).name, d))
        F.extend(notes)
    main_tr = trs[0][1] if trs else {}
    others = trs[1:]

    order = list(sb) + [k for k in pr if k not in sb] + [k for k in main_tr if k not in sb and k not in pr]
    table, plan = [], {}
    for shot in order:
        fs: list[Finding] = []

        def add(level, code, msg, **data):
            fs.append(Finding(level, code, msg, shot, data))

        script = sb[shot]["dialogue"] if shot in sb else None
        if script:
            script, resplit = split_script(script)
            resplit = resplit or bool(ac.dialogue_sep_issues(sb[shot].get("dialogue_raw", "")))   # common 已切句，偏差照报
            if resplit:
                add("warn", "TR-format", "分镜 对白 列的句间分隔写成了无空格的 / 或全角 ／（已按 '说话人：台词' 重新拆句再对账）→ 改为"
                    " ' / '（两侧各一个空格），否则其他脚本会把下一句的说话人名当成台词")
        pdia = prompt_dialogue(pr[shot]) if shot in pr else None
        s_orig = " / ".join(t for _, t in script) if script is not None else None
        p_orig = " / ".join(re.sub(r"\s+", " ", t) for *_, t in pdia) if pdia is not None else None
        dirs = []
        if s_orig is not None:
            s_orig, d1 = strip_directions(s_orig)
            dirs += d1
        if p_orig is not None:
            p_orig, d2 = strip_directions(p_orig)
            dirs += d2
        if dirs:
            add("info", "TR-format", f"已忽略括号内舞台提示 {sorted(set(dirs))}（不是要说出口的字，不参与逐字对账）；"
                "提示词 <d> 里不要写舞台提示——生成器会把它念出来或烧成字（D1）")
        s_n = norm(s_orig) if s_orig is not None else None
        p_n = norm(p_orig) if p_orig is not None else None
        cell = {"shot": shot, "script": "—", "prompt": "—", "transcript": "—"}

        # ---- 剧本 ↔ 提示词（P7）
        if storyboard and prompts:
            if script is not None and pdia is not None:
                if s_n != p_n:
                    cell["prompt"] = "✗"
                    if not s_n:
                        add("error", "TR-script-prompt", f"分镜 对白=—，但提示词有 <d>「{p_orig}」→ 生成器会照提示词说出来（P7 双文档对账）："
                            "按剧本删掉 <d>；若剧本确要加这句，先改分镜表再改提示词（E4 回写）", prompt=p_orig)
                    elif not p_n:
                        add("error", "TR-script-prompt", f"剧本有台词「{s_orig}」，提示词没有任何 <d> → 生成器不会说这句：按剧本逐字补 "
                            "'[S#] says: <d>[Chinese] 台词</d>'（P7）", script=s_orig)
                    else:
                        sm = difflib.SequenceMatcher(None, s_n, p_n, autojunk=False)
                        only_s = [s_n[i1:i2] for op, i1, i2, _, _ in sm.get_opcodes() if op in ("delete", "replace")]
                        only_p = [p_n[j1:j2] for op, _, _, j1, j2 in sm.get_opcodes() if op in ("insert", "replace")]
                        add("error", "TR-script-prompt", f"剧本↔提示词台词不一致：剧本有、提示词无「{'」「'.join(only_s) or '—'}」；"
                            f"提示词有、剧本无「{'」「'.join(only_p) or '—'}」→ 以剧本为准逐字改 <d>（P7）；若剧本已改，先回写分镜表（E4）",
                            script=s_orig, prompt=p_orig)
                elif s_n:
                    cell["prompt"] = "✓"
                    names = [nm for _, nm, _ in pdia]
                    if len(pdia) == len(script) and all(names):
                        for i, ((spk, _), nm, (sid, _, _)) in enumerate(zip(script, names, pdia), 1):
                            if spk != "?" and _nkey(spk) != _nkey(nm):
                                add("error", "TR-speaker", f"第 {i} 句说话人：剧本「{spk}」，提示词 [{sid}]→{nm}（P7；串台会让口型/声线"
                                    "落到错误角色）→ 改提示词的说话人 ID 或 角色映射", line=i)
            elif script and s_n and pdia is None:
                cell["prompt"] = "缺镜"
                add("warn", "TR-no-prompt", f"剧本有台词「{s_orig}」，但 {Path(prompts).name} 中没有 {shot} → 若本镜送 H3，补提示词并"
                    "逐字嵌入台词；若本镜不送 H3（本地静帧/纯色卡），台词改走剪辑单 字幕/画外音")
            elif script is None and pdia:
                add("warn", "TR-unknown-shot", f"提示词中的 {shot} 不在分镜表里（P7）→ 先在 storyboard.md 补行或删除此镜")
        if s_n:
            cell["script"] = "有"

        # ---- 转写侧
        if trs:
            ref_src, ref_orig, ref_n = ("剧本", s_orig, s_n) if script is not None else \
                (("提示词", p_orig, p_n) if pdia is not None else (None, None, None))
            t = main_tr.get(shot)
            audio = None
            if vdir is not None and (ref_n or (t is not None and norm(t["text"]))):
                vf = vdir / f"{shot}.mp4"
                audio = has_audio(vf) if vf.is_file() else None
                if audio is False:
                    if t is not None and norm(t["text"]):
                        add("warn", "TR-no-audio", f"{vf.name} 没有音轨（ffprobe 无 audio 流），但转写有文字「{t['text']}」→ 这段转写必为工具"
                            "编造（D5），不得据此判缺字/多字；以下转写侧发现仅供排查工具", video=str(vf))
                    if ref_n:
                        add("warn", "TR-no-audio", f"{ref_src}有台词，但 {vf.name} 没有音轨 → 先查生成/导出/封装环节是否丢了音轨"
                            f"（E3 环境问题：换导出参数后用 ffprobe 复核）；台词是否成立：{SECOND}", video=str(vf))
            if ref_src is None:
                if t is not None and norm(t["text"]):
                    add("warn", "TR-unknown-shot", f"转写里有 {shot}「{t['text']}」，但分镜/提示词中都没有这一镜 → 核对镜号（E2 改号残留？）")
            elif t is None:
                if ref_n:
                    cell["transcript"] = "缺"
                    add("warn", "TR-no-transcript", f"{ref_src}有台词「{ref_orig}」，转写文件中没有 {shot} → 补跑转写（P8 视频验收固定环节）")
            else:
                tn = tn_raw = norm(t["text"])
                if audio is False:
                    tn = ""                     # 无音轨：转写是编造，不参与逐字对账（台词按整句缺失计）
                if t["text"] != t["text"].translate(T2S):
                    add("info", "TR-format", "转写为繁体输出（ASR 常见，D5）：已按内置常用字表转简体后再对账；表外繁体字仍可能显示为差异 → "
                        "转写时指定简体（如 whisper 加 --initial_prompt '以下是普通话的句子'）或先用 OpenCC 转换")
                win = [(n, norm(d[shot]["text"]), d[shot]["conf"]) for n, d in others if shot in d]
                if win:
                    texts = [tn] + [w[1] for w in win]
                    agree = len(set(texts)) == 1
                    desc = " / ".join([f"{trs[0][0]}「{t['text']}」({t['conf'] if t['conf'] is not None else '—'})"] +
                                      [f"{n}「{d[shot]['text']}」({c if c is not None else '—'})"
                                       for (n, _, c), (_, d) in zip(win, [o for o in others if shot in o[1]])])
                    add("info", "TR-windows", f"多窗对照：{desc} → {'窗间一致' if agree else '窗间互斥'}", agree=agree)
                if not ref_n:
                    if tn:
                        cell["transcript"] = "多"
                        msg = (f"无对白镜（按{ref_src}）出现转写「{t['text']}」：先证伪工具（D5：静音轨曾被识别为'字幕by索兰娅'）——"
                               "抽帧看口型、回听原音轨，单通道不下结论")
                        suspect = tn
                        if ref_src == "剧本" and p_n:
                            sm = difflib.SequenceMatcher(None, p_n, tn, autojunk=False)
                            same = "".join(tn[b.b:b.b + b.size] for b in sm.get_matching_blocks() if b.size)
                            suspect = "".join(tn[j1:j2] for op, _, _, j1, j2 in sm.get_opcodes() if op in ("insert", "replace"))
                            if same:
                                msg += f"；其中「{same}」与提示词 <d> 一致 → 生成器照提示词说了台词，根因是 TR-script-prompt（P7）"
                            if suspect:
                                msg += f"；「{suspect}」剧本和提示词都没有 → 疑似误听（D5 实证：低笑气声被误听为'救我'），做 3 窗复核"
                        msg += _win_note(suspect, win)
                        msg += f"；是否重出：{SECOND}"
                        add("warn", "TR-unscripted", msg, transcript=t["text"])
                else:
                    r_n, r_idx = norm_map(ref_orig)
                    sm = difflib.SequenceMatcher(None, r_n, tn, autojunk=False)
                    miss, extra, numfmt = [], [], []
                    for op, i1, i2, j1, j2 in sm.get_opcodes():
                        if op == "replace" and tn[j1:j2].isdigit() and cn2int(r_n[i1:i2]) == int(tn[j1:j2]):
                            numfmt.append(f"{r_n[i1:i2]}↔{tn[j1:j2]}")      # 三年↔3年：ASR 数字写法，数值相同
                            continue
                        if op in ("delete", "replace"):
                            miss.append((i1, i2, tn[j1:j2] if op == "replace" else ""))
                        if op in ("insert", "replace"):
                            extra.append(tn[j1:j2])
                    if numfmt:
                        add("info", "TR-format", f"转写把中文数字写成了阿拉伯数字 {numfmt}（数值相同，ASR 书写习惯）→ 视为一致，不计缺字/多字")
                    cap = ""
                    if script is not None and shot in sb and sb[shot]["dur"]:
                        chars = sum(ac.speech_chars(strip_directions(x)[0]) for _, x in script)
                        need = chars / ac.SPEECH_RATE_CPS
                        cap = (f"；容量核算：台词 {chars:g} 字 ÷ {ac.SPEECH_RATE_CPS} 字/秒 = {need:.2f}s，镜长 {sb[shot]['dur']:.2f}s，"
                               f"余量 {sb[shot]['dur'] - need:.2f}s")
                        if need > sb[shot]["dur"]:
                            cap += "（台词超出镜长容量 → D3 结构性缺陷：回分镜删句或拆镜，单镜上限 15.08s，换 seed 补不回来）"
                    for i1, i2, rep in miss:
                        span = r_n[i1:i2]
                        heard = [n for n, wt, _ in win if span in wt]
                        level = "warn" if heard else "error"
                        msg = (f"缺句/缺字：{ref_src}有、转写无「{span}」（{_mark(ref_orig, r_idx, i1, i2)}）"
                               + ("（视频无音轨：转写不可信，整句按缺失计）" if audio is False else "")
                               + (f"，转写在此处为「{rep}」（可能是同音误听，也可能是真实错读）" if rep else "")
                               + "（若换 seed 仍缺→D3 结构性缺陷，回分镜核算容量）" + cap)
                        if heard:
                            msg += f"；窗口 {', '.join(heard)} 听到了该片段 → 主窗漏听可能性高（D5 多窗复核）"
                        elif win:
                            msg += f"；其余 {len(win)} 窗同样缺失（窗间一致缺失 → 更可能真实缺句）"
                        msg += f"；是否重出：{SECOND}"
                        add(level, "TR-missing", msg, missing=span, replaced_by=rep)
                        cell["transcript"] = "缺"
                    for x in extra:
                        if not x:
                            continue
                        add("warn", "TR-extra", f"转写比{ref_src}多出「{x}」→ 先回听原音轨、抽帧核对口型（D5）；与剧本无关的多余人声"
                            f"若属实，再按画面/听感决定处理{_win_note(x, win)}；是否重出：{SECOND}", extra=x)
                        if cell["transcript"] == "—":
                            cell["transcript"] = "多"
                    if not miss and not extra:
                        cell["transcript"] = "✓"
                for h in ac.KNOWN_ASR_HALLUCINATIONS:
                    hn = norm(h)
                    if hn and hn in tn_raw and hn not in (ref_n or ""):          # 剧本本来就有这句（如"谢谢观看"）则不算幻觉
                        add("warn", "TR-hallucination", f"转写命中已知 ASR 幻觉「{h}」（D5 实证：无对白镜音轨被识别为'字幕by索兰娅'）→ "
                            "这是工具在静音/弱音轨上的编造，不是音轨内容；不得据此判缺陷，回听原音轨确认", phrase=h)
                if t["conf"] is not None and t["conf"] < low:
                    add("visual", "TR-lowconf", f"低置信 {t['conf']:.2f} < {low}：做 3 窗复核 + 抽帧核对口型（D5 双通道）→ 加 --windows "
                        f"打印本镜的复核命令；结论{SECOND}", conf=t["conf"])
        F.extend(fs)
        table.append(cell)
        reasons = sorted({f.code for f in fs} & RECHECK)
        if windows and reasons:
            plan[shot] = {"reasons": reasons, "commands": window_commands(shot, video_dir)}

    lines = ["逐镜对账（剧本 有/— ｜ 提示词 ✓一致/✗不一致/缺镜 ｜ 转写 ✓/缺/多/—）："]
    for c in table:
        lines.append(f"  {c['shot']}：剧本 {c['script']} ｜ 提示词 {c['prompt']} ｜ 转写 {c['transcript']}")
    if windows:
        if plan:
            lines.append("3 窗复核计划（--windows；转写工具为可选依赖，本脚本不调用）：")
            for k, v in plan.items():
                lines.append(f"  {k}（原因：{', '.join(v['reasons'])}）")
                lines.extend("    " + c for c in v["commands"])
            lines.append("  判读：窗间互斥且置信度均低 → 工具误听（D5）；窗间一致缺失 → 查 D3 容量。结论" + SECOND + "。")
        else:
            lines.append("3 窗复核计划：本次没有需要复核的镜。")
    lines.append("提醒：转写是单通道证据（D5）。本报告中的任何缺字/多字都不能单独作为重出依据。")
    return F, {"summary": "\n".join(lines), "table": table, "window_plan": plan}


def _win_note(text_n: str, win: list) -> str:
    if not win or not text_n:
        return ""
    present = [n for n, wt, _ in win if text_n in wt]
    if len(present) == len(win):
        return f"；其余 {len(win)} 窗都听到了「{text_n}」→ 更可能音轨里真有此声，抽帧核对口型"
    if not present:
        return f"；其余 {len(win)} 窗都没听到「{text_n}」→ 符合 D5 误听特征（窗间互斥）"
    return f"；其余窗口只有 {len(present)}/{len(win)} 听到「{text_n}」→ 符合 D5 误听特征（窗间互斥）"


def window_commands(shot: str, video_dir: str | Path | None) -> list[str]:
    audio = None
    if video_dir:
        v = str(Path(video_dir) / f"{shot}.mp4")
        vnote = "" if Path(v).is_file() else "   # 未找到该文件：按实际文件名改 V"
        if Path(v).is_file():
            audio = has_audio(Path(v))
    else:
        v, vnote = f"（填 {shot} 的视频路径）", "   # 未给 --video-dir"
    head = f'V={shlex.quote(v)}; O="qc/{shot}"; mkdir -p "$O"{vnote}'          # shlex：路径含空格/中文/引号也安全
    lips = 'ffmpeg -v error -y -i "$V" -vf "fps=2:eof_action=pass,scale=240:-2,tile=6x5" -frames:v 1 "$O/lips.jpg"   # 第二通道：口型接触表'
    if audio is False:
        return [head, "# 该视频没有音轨（ffprobe 无 audio 流）：w1–w3 转写无从做起，转写里的任何文字都是工具编造（D5）；只做口型接触表", lips]
    return [
        head,
        'ffmpeg -v error -y -i "$V" -vn -ac 1 -ar 16000 "$O/w1.wav"',
        'ffmpeg -v error -y -ss 0.4 -i "$V" -vn -ac 1 -ar 16000 "$O/w2.wav"',
        'ffmpeg -v error -y -i "$V" -vn -ac 1 -ar 16000 -af "adelay=400:all=1" "$O/w3.wav"',
        'whisper-cli -m models/ggml-large-v3.bin -l zh -f "$O/w1.wav" -otxt -of "$O/w1"   # 可选工具；w2、w3 同理',
        lips,
    ]


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[bool] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        results.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  —— {detail}" if detail and not cond else ""))

    good, bad, own = ac.FIXTURES / "good", ac.FIXTURES / "bad", ac.FIXTURES / "transcript_reconcile"

    f, ex = analyze(good / "storyboard.md", good / "video-prompts.md", [good / "transcripts.tsv"])
    check("good: 三方 0 error", not [x for x in f if x.level == "error"], str([(x.code, x.where) for x in f if x.level == "error"]))
    check("good: 转写三镜全部 ✓", [c["transcript"] for c in ex["table"]][:3] == ["✓", "✓", "✓"], str(ex["table"]))
    f, _ = analyze(good / "storyboard.md", None, [own / "transcripts-good.json"])
    check("good: JSON 两种写法（对象/纯文本）均可读，0 error 0 warn", not [x for x in f if x.level in ("error", "warn")],
          str([(x.code, x.msg[:50]) for x in f if x.level in ("error", "warn")]))

    f, ex = analyze(bad / "storyboard.md", bad / "video-prompts.md", [bad / "transcripts.tsv"])

    def codes(shot: str, level: str | None = None) -> set:
        return {x.code for x in f if x.where == shot and (level is None or x.level == level)}
    check("bad SHOT-003: 分镜无对白、提示词有 <d> → TR-script-prompt error", "TR-script-prompt" in codes("SHOT-003", "error"))
    miss = [x for x in f if x.code == "TR-missing" and x.where == "SHOT-002"]
    check("bad SHOT-002: 缺「一个字都不许忘等到那一天我们在湖边再见」→ TR-missing error",
          bool(miss) and miss[0].level == "error" and miss[0].data["missing"] == "一个字都不许忘等到那一天我们在湖边再见",
          miss[0].data.get("missing", "") if miss else "")
    check("bad SHOT-002: 缺字报告带 D3 指引与容量核算", bool(miss) and "D3" in miss[0].msg and "7.5 字/秒" in miss[0].msg)
    check("bad SHOT-001: 字幕by索兰娅 → TR-unscripted + TR-hallucination warn",
          {"TR-unscripted", "TR-hallucination"} <= codes("SHOT-001", "warn"), str(codes("SHOT-001")))
    check("bad SHOT-001/003: 置信度 0.31/0.42 → TR-lowconf 需目视",
          "TR-lowconf" in codes("SHOT-001", "visual") and "TR-lowconf" in codes("SHOT-003", "visual"))
    un3 = [x.msg for x in f if x.code == "TR-unscripted" and x.where == "SHOT-003"]
    check("bad SHOT-003: 区分「受死吧」=照提示词说了 与「救我」=疑似误听",
          bool(un3) and "受死吧" in un3[0] and "救我" in un3[0] and "误听" in un3[0], un3[0] if un3 else "")
    check("bad SHOT-002: 提示词缺镜 → TR-no-prompt warn", "TR-no-prompt" in codes("SHOT-002", "warn"))
    alltext = " ".join(x.msg for x in f) + ex["summary"]
    check("bad: 任何输出都不含'需重出'，涉及重出处都写第二通道", "需重出" not in alltext and SECOND in alltext)

    f, ex = analyze(bad / "storyboard.md", bad / "video-prompts.md",
                    [bad / "transcripts.tsv", own / "w2.tsv", own / "w3.tsv"], windows=True)
    w3 = [x for x in f if x.code == "TR-windows" and x.where == "SHOT-003"]
    check("windows: SHOT-003 三窗互斥 → TR-windows info（窗间互斥）", bool(w3) and w3[0].data["agree"] is False)
    un3 = [x.msg for x in f if x.code == "TR-unscripted" and x.where == "SHOT-003"]
    check("windows: SHOT-003「救我」其余窗口没听到 → 标注 D5 误听特征", bool(un3) and "都没听到「救我」" in un3[0]
          and "误听特征" in un3[0], un3[0] if un3 else "")
    m2 = [x for x in f if x.code == "TR-missing" and x.where == "SHOT-002"]
    check("windows: SHOT-002 三窗一致缺失 → 仍为 error 并注明窗间一致", bool(m2) and m2[0].level == "error" and "窗间一致缺失" in m2[0].msg)
    check("windows: 复核计划含 ffmpeg 与 whisper-cli 命令", "SHOT-003" in ex["window_plan"]
          and any("whisper-cli" in c for c in ex["window_plan"]["SHOT-003"]["commands"]))

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "main.tsv").write_text("SHOT-003\t凡人，你也配？配不配，知道。\t0.55\n", encoding="utf-8")
        (tdp / "w2.tsv").write_text("SHOT-003\t凡人你也配配不配打过才知道\t0.71\n", encoding="utf-8")
        f, _ = analyze(good / "storyboard.md", None, [tdp / "main.tsv", tdp / "w2.tsv"])
        mm = [x for x in f if x.code == "TR-missing"]
        check("windows: 主窗缺「打过才」但 w2 听到 → TR-missing 降为 warn",
              bool(mm) and mm[0].level == "warn" and mm[0].data["missing"] == "打过才", str([(x.level, x.data) for x in mm]))
        # 说话人串台
        sbt = tdp / "sb.md"
        sbt.write_text("| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |\n|---|---|---|---|---|---|---|---|---|---|\n"
                       "| SEQ-01 | SHOT-002 | 10.83 | 2 | 殇月立誓 | 缓推 | 因为誓言，所以推近 | 殇月=LEFT; 苏晓=RIGHT | 殇月：我会回来。 | — |\n",
                       encoding="utf-8")
        vpt = tdp / "vp.md"
        vpt.write_text("## SHOT-002\n- 角色映射: S1=苏晓; S2=殇月\n\n```h3\ndetailed_description:\n"
                       "  [S1] says: <d>[Chinese] 我会回来。</d>\n```\n", encoding="utf-8")
        f, _ = analyze(sbt, vpt, None)
        check("说话人：剧本 殇月 / 提示词 [S1]→苏晓 → TR-speaker error", any(x.code == "TR-speaker" and x.level == "error" for x in f))
        # 格式错误行
        (tdp / "fmt.tsv").write_text("SHOT-001\t这里不对劲。\tabc\nbad line\n", encoding="utf-8")
        f, _ = analyze(good / "storyboard.md", None, [tdp / "fmt.tsv"])
        check("TSV 坏行/坏置信度 → TR-format warn 且不崩", sum(1 for x in f if x.code == "TR-format") == 2)

        me = [sys.executable, str(Path(__file__).resolve())]
        p = subprocess.run(me + ["--storyboard", str(good / "storyboard.md"), "--prompts", str(good / "video-prompts.md"),
                                 "--transcripts", str(good / "transcripts.tsv")], capture_output=True, text=True)
        check("CLI good → 退出码 0", p.returncode == 0, p.stdout[-300:])
        p = subprocess.run(me + ["--storyboard", str(bad / "storyboard.md"), "--prompts", str(bad / "video-prompts.md"),
                                 "--transcripts", str(bad / "transcripts.tsv"), "--windows", "--json"],
                           capture_output=True, text=True)
        try:
            js = json.loads(p.stdout)
            okj = p.returncode == 1 and js["counts"]["error"] >= 2 and "window_plan" in js
        except (ValueError, KeyError):
            okj = False
        check("CLI bad --windows --json → 退出码 1，JSON 含 window_plan", okj, p.stdout[:200])
        check("CLI bad 输出不含'需重出'", "需重出" not in p.stdout)
        p = subprocess.run(me + ["--windows"], capture_output=True, text=True)
        check("CLI 只给 --windows → 打印 3 窗说明，退出码 0", p.returncode == 0 and "adelay=400:all=1" in p.stdout)
        p = subprocess.run(me + ["--storyboard", str(good / "storyboard.md")], capture_output=True, text=True)
        check("CLI 只有一方 → 退出码 2", p.returncode == 2)

        # 文档里的 ffmpeg 命令在合成素材上真能跑（lavfi）；没有 ffmpeg/bash 时跳过并注明
        if ac.have("ffmpeg") and shutil.which("bash"):
            vid = tdp / "SHOT-003.mp4"
            r = ac.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=240x432:rate=24:duration=3",
                        "-f", "lavfi", "-i", "sine=frequency=440:duration=3", "-shortest", "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", str(vid)])
            cmds = [c.split("   #")[0] for c in window_commands("SHOT-003", tdp) if not c.startswith("whisper")]
            r2 = subprocess.run(["bash", "-c", " && ".join(cmds)], cwd=td, capture_output=True, text=True)
            outs = [tdp / "qc" / "SHOT-003" / n for n in ("w1.wav", "w2.wav", "w3.wav", "lips.jpg")]
            check("3 窗 ffmpeg 命令在 lavfi 合成素材上可执行，产出 w1/w2/w3.wav + lips.jpg",
                  r.returncode == 0 and r2.returncode == 0 and all(o.is_file() for o in outs), r2.stderr[-300:])
            if all(o.is_file() for o in outs[:3]):
                d = [ac.media_duration(o) for o in outs[:3]]
                check("3 窗时长关系：w2≈全长-0.4s，w3≈全长+0.4s", abs(d[0] - d[1] - 0.4) < 0.05 and abs(d[2] - d[0] - 0.4) < 0.05,
                      str(d))
        else:
            print("SKIP  未找到 ffmpeg 或 bash：跳过 3 窗命令的实跑验证（降级，不影响对账逻辑自测）")

        # ---- 对抗回归（输入现场生成）
        sb_adv = ("| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |\n"
                  "|---|---|---|---|---|---|---|---|---|---|\n"
                  "| SEQ-01 | SHOT-001 | 8.00 | 1 | a | b | c | 苏晓=CENTER | 苏晓：（低声）就是现在！ | — |\n"
                  "| SEQ-01 | SHOT-002 | 8.00 | 1 | a | b | c | 苏晓=LEFT; 殇月=RIGHT | 殇月：等了三十年/苏晓：我知道 | — |\n"
                  "| SEQ-01 | SHOT-003 | 8.00 | 1 | a | b | c | 苏晓=CENTER | 苏 晓：这里不对劲。 | — |\n"
                  "| SEQ-01 | SHOT-004 | 8.00 | 1 | a | b | c | 苏晓=CENTER | 苏晓：谢谢观看，下集再见。 | — |\n"
                  "| SEQ-01 | SHOT-005 | 5.17 | 1 | a | b | c | 殇月=CENTER | 殇月：月落之时我会回来找你你记住今天说过的每一个字一个字都不许忘"
                  "等到那一天我们在湖边再见 | — |\n")
        (tdp / "sb_adv.md").write_bytes(("﻿" + sb_adv).replace("\n", "\r\n").encode("utf-8"))
        vp_adv = ("## SHOT-001\n- 角色映射: S1=苏晓\n```h3\ndetailed_description:\n  [S1] whispers: <d>[Chinese] 就是现在！</d>\n```\n"
                  "## SHOT-002\n- 角色映射: S1=苏晓; S2=殇月\n```h3\ndetailed_description:\n  [S2] says: <d>[Chinese] 等了三十年</d>\n"
                  "  [S1] replies: <d>[Chinese] 我知道</d>\n```\n"
                  "## SHOT-003\n- 角色映射: S1＝苏晓\n```h3\ndetailed_description:\n  [S1] says: <d>[Chinese] 这里不对劲。</d>\n```\n")
        (tdp / "vp_adv.md").write_text(vp_adv, encoding="utf-8")
        (tdp / "t_adv.tsv").write_bytes("﻿SHOT-001\t就是现在！\t0.9\r\nSHOT-002 等了30年。我知道 0.9\r\nshot-003\t這裡不對勁。\t0.9\r\n"
                                        "SHOT-004\t谢谢观看，下集再见。\t0.9\r\nSHOT-005\t月落之时我会回来找你\t0.9\r\n".encode("utf-8"))
        f, ex = analyze(tdp / "sb_adv.md", tdp / "vp_adv.md", [tdp / "t_adv.tsv"])
        cells = {c["shot"]: c for c in ex["table"]}
        errs = [(x.code, x.where) for x in f if x.level == "error"]
        check("对抗：BOM 表头/BOM TSV 首行、空格代替 TAB、小写镜号都读入（各报 FMT-bom / TR-format），SHOT-001~003 三方 ✓",
              all(cells[s]["transcript"] == "✓" and cells[s]["prompt"] == "✓" for s in ("SHOT-001", "SHOT-002", "SHOT-003"))
              and any(x.code == "FMT-bom" for x in f) and sum(1 for x in f if x.code == "TR-format" and x.level == "warn") >= 3,
              str(cells) + str(errs))
        check("对抗：舞台提示（低声）/ 无空格 '/' 分句 / '三十'↔'30' / 繁体转写 / '苏 晓'↔'苏晓' 都不产生 error",
              not [e for e in errs if e[1] in ("SHOT-001", "SHOT-002", "SHOT-003")], str(errs))
        check("对抗：剧本本来就有'谢谢观看' → 不报 TR-hallucination（修复前：合法台词被当幻觉）",
              not any(x.code == "TR-hallucination" and x.where == "SHOT-004" for x in f))
        m5 = [x.msg for x in f if x.code == "TR-missing" and x.where == "SHOT-005"]
        check("对抗：台词超出镜长容量 → TR-missing 附'D3 结构性缺陷：回分镜删句或拆镜'", bool(m5) and "超出镜长容量" in m5[0], str(m5))
        (tdp / "null.json").write_text('{"SHOT-001": null, "SHOT-003": {"text": null}}', encoding="utf-8")
        f, _ = analyze(tdp / "sb_adv.md", None, [tdp / "null.json"])
        check("对抗：JSON 里 null → 当空转写（修复前：变成文字 'None' 被报多字）",
              not any("none" in x.msg.lower() and x.code in ("TR-extra", "TR-missing") for x in f))
        alltext = " ".join(x.msg for x in f) + ex["summary"]
        check("对抗：以上所有输出都不含'需重出'", "需重出" not in alltext)

        if ac.have("ffmpeg") and ac.have("ffprobe") and shutil.which("bash"):
            vd = tdp / "视频 目录"
            vd.mkdir()
            r1 = ac.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=240x432:rate=24:duration=2",
                         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(vd / "SHOT-001.mp4")])            # 无音轨
            r2 = ac.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=240x432:rate=24", "-f", "lavfi",
                         "-i", "sine=frequency=440:duration=1", "-frames:v", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                         "-c:a", "aac", "-shortest", str(vd / "SHOT-003.mp4")])                           # 1 帧
            (tdp / "t_media.tsv").write_text("SHOT-001\t字幕by索兰娅\t0.3\nSHOT-003\t这里不对劲\t0.5\n", encoding="utf-8")
            f, ex = analyze(tdp / "sb_adv.md", None, [tdp / "t_media.tsv"], windows=True, video_dir=vd)
            na = [x for x in f if x.code == "TR-no-audio" and x.where == "SHOT-001"]
            m1 = [x.msg for x in f if x.code == "TR-missing" and x.where == "SHOT-001"]
            check("媒体对抗：无音轨视频 → TR-no-audio（转写必为编造），缺字按整句计、不再把编造文字当'同音误听'",
                  r1.returncode == 0 and len(na) == 2 and bool(m1) and "视频无音轨" in m1[0] and "转写在此处为" not in m1[0],
                  str([x.msg[:60] for x in na]) + str(m1))
            cmds1 = ex["window_plan"].get("SHOT-001", {}).get("commands", [])
            check("媒体对抗：无音轨镜的复核计划不含 w1–w3 抽音频命令（否则 ffmpeg 报 'does not contain any stream'）",
                  bool(cmds1) and not any("w1.wav" in c for c in cmds1) and any("lips.jpg" in c for c in cmds1))
            runs = []
            for shot in ("SHOT-001", "SHOT-003"):
                cmds = [c.split("   #")[0] for c in ex["window_plan"][shot]["commands"]
                        if not c.startswith("whisper") and not c.startswith("#")]
                runs.append(subprocess.run(["bash", "-c", " && ".join(cmds)], cwd=td, capture_output=True, text=True))
            outs = [tdp / "qc" / "SHOT-001" / "lips.jpg", tdp / "qc" / "SHOT-003" / "lips.jpg", tdp / "qc" / "SHOT-003" / "w2.wav"]
            check("媒体对抗：路径含空格+中文、1 帧短镜 → 计划命令全部可执行，口型接触表照出（修复前：fps=2 吞掉唯一一帧，静默不出图）",
                  r2.returncode == 0 and all(r.returncode == 0 for r in runs) and all(o.is_file() for o in outs),
                  " | ".join(r.stderr[-120:] for r in runs))
            real_have = ac.have
            ac.have = lambda tool: False if tool == "ffprobe" else real_have(tool)      # 模拟缺 ffprobe
            try:
                f, _ = analyze(tdp / "sb_adv.md", None, [tdp / "t_media.tsv"], video_dir=vd)
            finally:
                ac.have = real_have
            check("媒体对抗：缺 ffprobe（monkeypatch）→ 不崩，报 info'跳过音轨检查（降级）'，不出 TR-no-audio warn",
                  any(x.code == "TR-no-audio" and x.level == "info" and "降级" in x.msg for x in f)
                  and not any(x.code == "TR-no-audio" and x.level == "warn" for x in f))
        else:
            print("SKIP  未找到 ffmpeg/ffprobe/bash：跳过媒体对抗用例（降级，不影响对账逻辑自测）")

    print(f"SELFTEST {'PASS' if all(results) else 'FAIL'}（{sum(results)}/{len(results)}）")
    return 0 if all(results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--storyboard", help="storyboard.md（剧本侧：对白 列）")
    ap.add_argument("--prompts", help="video-prompts.md（提示词侧：<d>）")
    ap.add_argument("--transcripts", nargs="+", help="转写 TSV/JSON；多给几个 = 同一音轨的错位时间窗（第一个为主转写）")
    ap.add_argument("--low-conf", type=float, default=0.6, help="低置信阈值（默认 0.6）")
    ap.add_argument("--windows", action="store_true", help="为需要复核的镜打印 3 窗复核命令；单独使用则打印说明")
    ap.add_argument("--video-dir", help="视频目录（--windows 时按 <镜号>.mp4 填入命令）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="用 fixtures 与 lavfi 合成素材自测")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.windows and not (a.storyboard or a.prompts or a.transcripts):
        print(windows_guide())
        return 0
    if not 0 < a.low_conf <= 1:
        ac.die("--low-conf 须在 (0, 1]")
    findings, extra = analyze(a.storyboard, a.prompts, a.transcripts, a.low_conf, a.windows, a.video_dir)
    return ac.emit(TITLE, findings, a.json, extra)


if __name__ == "__main__":
    sys.exit(main())
