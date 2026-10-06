#!/usr/bin/env python3
"""asset_exists.py — 素材存在性 / 旧集号路径残留 / 行尾审计 / 字节级改名预演（渲染前全量复查）

用途：
  渲染前把"素材不存在"拦在 verify 之前，并给"整季重编号"一个可预演、可复查的流程：
  (a) 剪辑单（任何含 `CUT | 来源` 表头的 .md）：每个 `来源` 相对剪辑单所在目录必须存在且非空（error）；
      纯色卡 `local:black` / `local:white` / `local:#RRGGBB` 合法并做语法校验（D2：纯色画面本地生成，不送生成器）。
  (b) 通扫给定目录下全部 .md：Markdown 链接与反引号里的相对媒体路径
      （png jpg jpeg webp mp4 mov wav mp3 m4a srt ass）不存在 → error。
      依次相对 md 所在目录及其上级（直到扫描根）解析；围栏代码块（``` / ~~~，按 CommonMark 匹配同字符且不短于
      开栏的闭栏，嵌套的 ````markdown 示例块不会提前结束）、HTML 注释 <!-- -->、URL、含 nnn/xxx/<>/{}/* 的模板占位不查；
      行内代码按 CommonMark 反引号串配对（``…`x.png`…`` 里的路径照查）；反引号里只查带目录的路径
      （`assets/boards/x.png`），单独文件名（`final.mp4`）视为命名约定不查（链接一律查）。缩进代码块不识别（按正文处理）。
      --bare 另查表格/正文里的裸路径（不存在 → warn）。
  (c) --stale-token TOKEN（可重复，如 ep03、S01E03）：逐文件列出出现次数与行号（warn）；
      出现在素材路径里的 → error（路径存在也报：它可能悄悄指向了旧集的同名素材）。
  (d) 行尾审计：CRLF / 混合行尾 / 孤立 CR / UTF-8 BOM → warn（format-contracts §0.1：UTF-8 + LF；E2"行尾零扰动"）。
  (e) --rename OLD NEW：字节级替换计划（默认 dry-run，只展示逐文件次数与示例行）；加 --apply 才写盘，
      写后校验 LF/CRLF 计数不变；先写同目录临时文件再原子替换（中途失败不会留下半截文件），只读文件不碰、报 error；
      文件/目录名含 OLD 的只提示用 git mv，不改名。--apply 时先替换、再做 (a)–(d) 复查。
  只报告事实与下一步动作。

溯源：E2（整季重编号后 4 份文档残留 143 处旧路径 → 渲染校验报 30 条"素材不存在"；修正 = 二进制级替换保持行尾零扰动
      + 全仓 grep 复查 + 重渲）、D2（纯黑画面交给 H3 会被加 LAVCE 水印 → 纯色卡本地生成，剪辑单写 local:）、
      T-3（后期链：剪辑单 → 渲染 → verify；三步闸门 prepare 校验在 run 之前）。

输入格式：70-playbooks/format-contracts.md §4「剪辑单（edit-list.md）」——表头 `CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字`，
  `来源` 为相对本集目录的路径或 `local:black|white|#RRGGBB`；§0.1 UTF-8 + LF；§7 改集号走"全仓替换 + 本脚本全量复查 + 重渲"。
  表格解析统一使用 academy_common.find_rows（与 parse_edit_list 同一解析器）。

判定：
  error E2-missing-asset   剪辑单来源不存在
  error E2-empty-asset     来源/引用文件大小为 0
  error E2-source-is-dir   来源是目录
  error E2-source-empty    来源单元格为空
  error D2-local-syntax    local: 写法不合法
  error E2-missing-ref     .md 链接/反引号里的媒体路径不存在
  error E2-stale-path      素材路径含 --stale-token（路径存在也报）
  error FMT-utf8           显式给出的文件不是 UTF-8
  warn  E2-stale-token     文件中出现 --stale-token（计数 + 行号）
  warn  E2-crlf / E2-mixed-eol / E2-cr-eol / E2-bom   行尾 / BOM 审计
  warn  E2-missing-bare    （--bare）裸路径不存在
  warn  E2-source-url / E2-source-absolute / E2-backslash   来源写法不可移植
  warn  FMT-edit-list      文件名像剪辑单但没有 `CUT | 来源` 表
  warn  FMT-dup-cut        同一剪辑单里 CUT 号重复（format-contracts §0.4：ID 集内唯一）
  error E2-rename-failed   --apply 写盘失败（只读/权限/磁盘）：该文件未改，其余文件照常替换
  info  E2-rename-plan / E2-rename-applied / E2-rename-path   改名预演 / 已执行 / 路径名含旧 token
  info  E2-scan-stats      扫描统计

用法示例：
  python3 asset_exists.py season-01/ep04/edit-list.md
  python3 asset_exists.py season-01/ --stale-token ep03 --stale-token S01E03
  python3 asset_exists.py season-01/ --rename ep03 ep04                  # dry-run：只看替换计划
  python3 asset_exists.py season-01/ --rename ep03 ep04 --apply          # 字节级替换 + 复查
  python3 asset_exists.py season-01/ep04/ --bare --json
  python3 asset_exists.py --selftest

退出码：0 通过（无 error）/ 1 发现 error / 2 用法或环境错误（路径不存在、--rename 参数非法）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import academy_common as ac  # noqa: E402

TITLE = "素材存在性 / 旧路径残留 / 行尾审计（E2 / D2 / T-3）"
MEDIA_EXTS = ("png", "jpg", "jpeg", "webp", "mp4", "mov", "wav", "mp3", "m4a", "srt", "ass")
TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv", ".srt", ".ass", ".py", ".sh", ".toml",
             ".ini", ".cfg"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
LOCAL_RE = re.compile(r"^local:(black|white|#[0-9A-Fa-f]{6})$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LINK_RE = re.compile(r"!?\[(?:[^\]\\]|\\.)*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
CODE_RE = re.compile(r"`([^`\n]+)`")
_EXCL = r"\s`'\"<>|*?，。；：、（）()\[\]{};,"
PATH_TOKEN = re.compile(rf"[^{_EXCL}]+?\.(?:{'|'.join(MEDIA_EXTS)})(?![\w-]|\.\w)", re.I)
PLACEHOLDER = re.compile(r"[<>{}*?…]|\.\.\.(?!/)|nnn|NNN|xxx|XXX")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:(?![\\/])")
MAX_TEXT = 20 * 1024 * 1024


# ------------------------------------------------------------------ 收集

def collect(inputs: list[str]) -> tuple[list[tuple[Path, Path, bool]], list[tuple[Path, bool]]]:
    """→ md 列表 [(md, 扫描根, 是否显式给出)]，文本列表 [(file, 是否显式)]。"""
    mds, texts, seen = [], [], set()
    for s in inputs:
        p = Path(s)
        if not p.exists():
            ac.die(f"找不到路径：{s}")
        if p.is_dir():
            for dp, dns, fns in os.walk(p):
                dns[:] = sorted(d for d in dns if d not in SKIP_DIRS)
                for fn in sorted(fns):
                    f = Path(dp) / fn
                    if f in seen:
                        continue
                    if f.suffix.lower() in TEXT_EXTS:
                        seen.add(f)
                        texts.append((f, False))
                        if f.suffix.lower() == ".md":
                            mds.append((f, p, False))
        elif p not in seen:
            seen.add(p)
            texts.append((p, True))
            if p.suffix.lower() == ".md":
                mds.append((p, p.parent, True))
    return mds, texts


def read_text(path: Path) -> tuple[str | None, bool]:
    try:
        data = path.read_bytes()
    except OSError:
        return None, False
    if len(data) > MAX_TEXT:
        return None, True
    try:
        return data.decode("utf-8-sig"), True
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace"), False


def rel(p: Path) -> str:
    """相对当前目录显示；要往上跳 2 层以上才到的（扫描的是别处）直接给绝对路径，免得满屏 ../../"""
    try:
        r = os.path.relpath(p)
    except ValueError:
        return str(p)
    return str(Path(p).resolve()) if r.startswith(os.pardir + os.sep + os.pardir + os.sep) else r


# ------------------------------------------------------------------ 路径检查

def norm_cell(cell: str) -> str:
    s = (cell or "").strip()
    m = re.fullmatch(r"!?\[[^\]]*\]\(\s*<?([^)>]+?)>?\s*\)", s)
    if m:
        s = m.group(1)
    s = s.strip().strip("`").strip()
    if s.startswith("<") and s.endswith(">"):
        s = s[1:-1].strip()
    return s


def resolve(token: str, bases: list[Path]) -> tuple[Path | None, Path]:
    """依次在 bases 下找；返回 (找到的路径或 None, 首选解析路径)。"""
    t = token.replace("\\", "/")
    if os.path.isabs(t):
        p = Path(t)
        return (p if p.exists() else None), p
    first = bases[0] / t
    for b in bases:
        c = b / t
        if c.exists():
            return c, first
    return None, first


def bases_for(md: Path, root: Path, extra: list[Path]) -> list[Path]:
    out, d = [md.parent], md.parent.resolve()
    r = root.resolve()
    while d != r and r in d.parents:
        d = d.parent
        out.append(d)
    return out + [e for e in extra if e not in out]


def stale_hits(text: str, tokens: list[str], icase: bool) -> list[str]:
    return [t for t in tokens if (t.lower() in text.lower() if icase else t in text)]


def check_source(cell: str, md: Path, where: str, tokens: list[str], icase: bool) -> list[ac.Finding]:
    s = norm_cell(cell)
    if ac.is_empty(s):
        return [ac.Finding("error", "E2-source-empty",
                           "来源为空：填相对本集目录的素材路径；纯色画面写 local:black / local:white / local:#RRGGBB（D2）", where)]
    lm = re.match(r"^local\s*[:：]\s*(.*)$", s, re.I)
    if lm:
        if LOCAL_RE.fullmatch(s):
            return []
        val, hints = lm.group(1).strip(), []
        if "：" in s[:lm.start(1)]:
            hints.append("全角冒号「：」改半角「:」")
        if not s.startswith("local"):
            hints.append("关键字 local 须小写")
        if re.match(r"^local\s+[:：]|^local\s*[:：]\s+", s, re.I):
            hints.append("冒号前后不要空格")
        if val.lower() in ("black", "white") and val != val.lower():
            hints.append("black / white 须小写")
        if val.startswith("#") and not re.fullmatch(r"#[0-9A-Fa-f]{6}", val):
            hints.append("颜色须写 # + 6 位十六进制（#fff 要写成 #FFFFFF）")
        fixed = (f"local:{val.lower()}" if val.lower() in ("black", "white")
                 else f"local:{val}" if re.fullmatch(r"#[0-9A-Fa-f]{6}", val) else "")
        return [ac.Finding("error", "D2-local-syntax",
                           f"来源 '{s}' 不合法：" + ("；".join(hints) + "。" if hints else "")
                           + (f"改为 {fixed}。" if fixed else "")
                           + "纯色卡只能写 local:black / local:white / local:#RRGGBB——D2：纯色画面本地生成，不送生成器",
                           where, {"source": s, "suggest": fixed or None})]
    if re.match(r"^[a-z][a-z0-9+.-]*://", s, re.I):
        return [ac.Finding("warn", "E2-source-url", f"来源是 URL '{s}'：先下载到 assets/ 再引用（渲染不得依赖网络）", where)]
    fs = []
    if "\\" in s:
        fs.append(ac.Finding("warn", "E2-backslash", f"来源 '{s}' 用了反斜杠：改为 /（跨平台）", where))
    if os.path.isabs(s.replace("\\", "/")):
        fs.append(ac.Finding("warn", "E2-source-absolute", f"来源 '{s}' 是绝对路径：改为相对本集目录（换机即失效）", where))
    found, want = resolve(s, [md.parent])
    stale = stale_hits(s, tokens, icase)
    st_note = f"；路径含旧 token {', '.join(stale)}（E2 改集号残留：用 --rename 预览批量替换）" if stale else ""
    if found is None:
        fs.append(ac.Finding("error", "E2-missing-asset",
                             f"来源 {s} 不存在（解析为 {rel(want)}）：把素材放到该路径，或把来源改成实际路径"
                             f"{case_hint(want)}{st_note}", where,
                             {"source": s, "resolved": str(want), "stale": stale}))
    elif found.is_dir():
        fs.append(ac.Finding("error", "E2-source-is-dir", f"来源 {s} 是目录：写到具体文件", where))
    elif found.stat().st_size == 0:
        fs.append(ac.Finding("error", "E2-empty-asset", f"来源 {s} 大小为 0（下载/渲染中断）：重新生成或重新拷贝", where))
    elif stale:
        fs.append(ac.Finding("error", "E2-stale-path",
                             f"来源 {s} 存在，但含已声明的旧 token {', '.join(stale)}：确认是否悄悄指向了旧集同名素材；"
                             f"若确应引用旧集，去掉该 --stale-token", where, {"source": s, "stale": stale}))
    return fs


def code_spans(ln: str) -> list[tuple[int, int, str]]:
    """CommonMark 行内代码：n 个反引号开、恰好 n 个反引号闭 → [(起, 止, 内容)]；未闭合的反引号串按字面处理。"""
    out, i, n = [], 0, len(ln)
    while i < n:
        if ln[i] != "`" or (i > 0 and ln[i - 1] == "\\"):
            i += 1
            continue
        j = i
        while j < n and ln[j] == "`":
            j += 1
        run, k, close = j - i, j, -1
        while k < n:
            if ln[k] == "`":
                m = k
                while m < n and ln[m] == "`":
                    m += 1
                if m - k == run:
                    close = k
                    break
                k = m
            else:
                k += 1
        if close < 0:
            i = j
            continue
        body = ln[j:close]
        if len(body) > 2 and body[0] == " " and body[-1] == " ":
            body = body[1:-1]
        out.append((i, close + run, body))
        i = close + run
    return out


def _strip_comments(ln: str, in_comment: bool, spans: list[tuple[int, int, str]]) -> tuple[str, bool]:
    """去掉 HTML 注释（可跨行）；代码段里的 <!-- 不算。被去掉的字符换成空格，列号不变。"""
    out, i = list(ln), 0
    while i < len(ln):
        if in_comment:
            e = ln.find("-->", i)
            stop = len(ln) if e < 0 else e + 3
            for k in range(i, stop):
                out[k] = " "
            if e < 0:
                return "".join(out), True
            in_comment, i = False, stop
            continue
        b = ln.find("<!--", i)
        if b < 0:
            break
        if any(a <= b < z for a, z, _ in spans):
            i = b + 4
            continue
        in_comment, i = True, b
    return "".join(out), in_comment


def scan_refs(text: str, bare: bool) -> list[tuple[int, str, str]]:
    """→ [(行号, 路径, 来源类型 link|code|bare)]，跳过围栏代码块与 HTML 注释。"""
    out, fence, in_comment = [], None, False
    for i, ln in enumerate(text.splitlines(), 1):
        m = FENCE_RE.match(ln)
        if fence is None:
            if m and not in_comment and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)))
                continue
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not m.group(2).strip():
                fence = None
            continue
        spans = code_spans(ln)
        ln, in_comment = _strip_comments(ln, in_comment, spans)
        spans = [sp for sp in code_spans(ln)]
        masked = list(ln)
        for a, z, body in spans:
            for k in range(a, z):
                masked[k] = " "
            for tm in PATH_TOKEN.finditer(body):
                if re.search(r"[/\\]", tm.group(0)):          # 单独文件名（`final.mp4`）= 命名约定，不当引用
                    out.append((i, tm.group(0), "code"))
        masked_ln = "".join(masked)
        link_spans = []
        for lm in LINK_RE.finditer(masked_ln):
            link_spans.append(lm.span())
            t = lm.group(1).strip("<>").split("#", 1)[0].split("?", 1)[0]
            t = unquote(t)
            if t.lower().endswith(tuple("." + e for e in MEDIA_EXTS)):
                out.append((i, t, "link"))
        if bare:
            for tm in PATH_TOKEN.finditer(masked_ln):
                if not any(a <= tm.start() < b for a, b in link_spans) and re.search(r"[/\\]", tm.group(0)):
                    out.append((i, tm.group(0), "bare"))
    return out


def case_hint(want: Path) -> str:
    """缺失时看同目录有没有只差大小写的文件（Windows/macOS 能过、Linux 渲染机不能过）。"""
    try:
        if want.parent.is_dir():
            for q in want.parent.iterdir():
                if q.name != want.name and q.name.lower() == want.name.lower():
                    return f"；同目录有大小写不同的 {q.name}：Linux 渲染机区分大小写，把路径改成与文件名一致"
    except OSError:
        pass
    return ""


def _where_dir(d: Path) -> str:
    r = rel(d)
    return "./" if r == "." else r


def check_md(md: Path, root: Path, explicit: bool, o: argparse.Namespace, extra_bases: list[Path],
             stats: dict) -> list[ac.Finding]:
    fs: list[ac.Finding] = []
    text, utf8 = read_text(md)
    if text is None:
        return fs
    if not utf8:
        fs.append(ac.Finding("error" if explicit else "warn", "FMT-utf8",
                             "不是 UTF-8 编码：转成 UTF-8 后重跑（format-contracts §0.1）", rel(md)))
    tokens, icase = o.stale_token, o.ignore_case
    rows = ac.find_rows(text, ["CUT", "来源"])
    done: set = set()
    if rows:
        stats["edit_lists"] += 1
    elif "edit-list" in md.name.lower() or "剪辑单" in md.name:
        fs.append(ac.Finding("warn", "FMT-edit-list",
                             "文件名像剪辑单，但没有 `CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字` 表头（format-contracts §4）", rel(md)))
    ids: dict = {}
    for r in rows:
        cid = (r.get("CUT") or "").strip()
        if not ac.is_empty(cid):
            ids.setdefault(cid, []).append(r["_line"])
    for cid, lns in ids.items():
        if len(lns) > 1:
            fs.append(ac.Finding("warn", "FMT-dup-cut",
                                 f"{cid} 重复出现在行 {', '.join(map(str, lns))}：CUT 号集内唯一（format-contracts §0.4），"
                                 f"重编号后再渲染，否则验收记录/字幕对账无法指认", rel(md), {"cut": cid, "lines": lns}))
    for r in rows:
        stats["sources"] += 1
        where = f"{rel(md)}:{r['_line']} · {r.get('CUT', '?')}"
        fs += check_source(r.get("来源", ""), md, where, tokens, icase)
        done.add((r["_line"], norm_cell(r.get("来源", ""))))
    bases = bases_for(md, root, extra_bases)
    for ln, tok, kind in scan_refs(text, o.bare):
        if (ln, tok) in done or PLACEHOLDER.search(tok) or SCHEME.match(tok):
            continue
        done.add((ln, tok))
        stats["refs"] += 1
        where = f"{rel(md)}:{ln}"
        found, want = resolve(tok, bases)
        stale = stale_hits(tok, tokens, icase)
        st_note = f"；路径含旧 token {', '.join(stale)}（E2）" if stale else ""
        if found is None:
            lvl, code = ("warn", "E2-missing-bare") if kind == "bare" else ("error", "E2-missing-ref")
            scope = (f"相对 {_where_dir(md.parent)} " if len(bases) == 1
                     else f"相对 {_where_dir(md.parent)} 及其上级（直到 {_where_dir(root)}）均")
            fs.append(ac.Finding(lvl, code, f"引用的媒体 {tok} 不存在（{scope}未找到）：补齐素材或改正路径"
                                 f"{case_hint(want)}{st_note}", where,
                                 {"ref": tok, "kind": kind, "resolved": str(want), "stale": stale}))
        elif found.is_file() and found.stat().st_size == 0:
            fs.append(ac.Finding("error", "E2-empty-asset", f"引用的媒体 {tok} 大小为 0：重新生成或重新拷贝", where))
        elif stale and kind != "bare":
            fs.append(ac.Finding("error", "E2-stale-path",
                                 f"引用 {tok} 存在，但含已声明的旧 token {', '.join(stale)}：确认是否指向了旧集素材", where,
                                 {"ref": tok, "stale": stale}))
    return fs


# ------------------------------------------------------------------ 旧 token / 行尾 / 改名

def stale_report(texts: list[tuple[Path, bool]], tokens: list[str], icase: bool) -> tuple[list[ac.Finding], dict]:
    fs, agg = [], {t: {} for t in tokens}
    for f, _ in texts:
        text, _ = read_text(f)
        if text is None:
            continue
        lines = text.splitlines()
        for t in tokens:
            needle = t.lower() if icase else t
            hit = [(i, (ln.lower() if icase else ln).count(needle)) for i, ln in enumerate(lines, 1)]
            hit = [(i, c) for i, c in hit if c]
            n = sum(c for _, c in hit)
            if not n:
                continue
            ls = [i for i, _ in hit]
            agg[t][rel(f)] = {"count": n, "lines": ls}
            fs.append(ac.Finding("warn", "E2-stale-token",
                                 f"'{t}' 出现 {n} 处（行 {', '.join(map(str, ls[:15]))}{' …' if len(ls) > 15 else ''}）："
                                 f"确认是否为改集号残留；批量替换先 --rename {t} <新> 预览，再 --apply（行尾零扰动）",
                                 rel(f), {"token": t, "count": n, "lines": ls}))
    return fs, agg


def eol_audit(texts: list[tuple[Path, bool]]) -> list[ac.Finding]:
    fs = []
    for f, _ in texts:
        try:
            data = f.read_bytes()
        except OSError:
            continue
        if len(data) > MAX_TEXT:
            continue
        crlf = data.count(b"\r\n")
        lf = data.count(b"\n") - crlf
        cr = data.count(b"\r") - crlf
        tip = "契约要求 UTF-8 + LF（format-contracts §0.1）；统一行尾请单独提交，不要与内容替换混在一起（E2 行尾零扰动）"
        d = {"lf": lf, "crlf": crlf, "cr": cr}
        if crlf and (lf or cr):
            fs.append(ac.Finding("warn", "E2-mixed-eol", f"混合行尾：LF {lf} / CRLF {crlf} / CR {cr}：{tip}", rel(f), d))
        elif crlf:
            fs.append(ac.Finding("warn", "E2-crlf", f"CRLF 行尾（{crlf} 行）：{tip}", rel(f), d))
        elif cr:
            fs.append(ac.Finding("warn", "E2-cr-eol", f"孤立 CR 行尾（{cr} 处）：{tip}", rel(f), d))
        if data.startswith(b"\xef\xbb\xbf"):
            fs.append(ac.Finding("warn", "E2-bom", f"UTF-8 BOM：去掉 BOM（会让首行表头/标题解析失败）", rel(f)))
    return fs


def rename_plan(texts: list[tuple[Path, bool]], old: str, new: str) -> list[dict]:
    ob = old.encode("utf-8")
    plan = []
    for f, _ in texts:
        try:
            data = f.read_bytes()
        except OSError:
            continue
        n = data.count(ob)
        if not n:
            continue
        samples = []
        for i, ln in enumerate(data.splitlines(), 1):
            if ob in ln and len(samples) < 5:
                before = ln.decode("utf-8", "replace").replace("\ufeff", "").strip()
                samples.append({"line": i, "before": before[:160], "after": before.replace(old, new)[:160]})
        plan.append({"file": f, "count": n, "samples": samples})
    return plan


def rename_apply(plan: list[dict], old: str, new: str) -> list[ac.Finding]:
    fs = []
    ob, nb = old.encode("utf-8"), new.encode("utf-8")
    for item in plan:
        f = item["file"]
        if not os.access(f, os.W_OK):
            fs.append(ac.Finding("error", "E2-rename-failed",
                                 f"文件只读，未替换（{item['count']} 处 '{old}' 仍在）：确认该文件确应改动后解除只读再 --apply",
                                 rel(f)))
            continue
        tmp = None
        real = Path(os.path.realpath(f))               # 符号链接：改链接指向的文件，不把链接本身换成普通文件
        try:
            data = real.read_bytes()
            out = data.replace(ob, nb)
            fd, tmp = tempfile.mkstemp(prefix=f".{real.name}.", suffix=".tmp", dir=str(real.parent))
            with os.fdopen(fd, "wb") as fh:          # 先写临时文件再原子替换：中途失败不留半截文件
                fh.write(out)
            shutil.copymode(real, tmp)
            os.replace(tmp, real)
            tmp = None
            back = real.read_bytes()
        except OSError as e:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
            fs.append(ac.Finding("error", "E2-rename-failed",
                                 f"写盘失败（{e.strerror or e}），该文件未替换：检查权限/磁盘后重跑 --apply"
                                 f"（其余文件已替换，git diff 核对）", rel(f)))
            continue
        same_eol = (back.count(b"\r\n") == data.count(b"\r\n") and back.count(b"\n") == data.count(b"\n")
                    and back.count(b"\r") == data.count(b"\r"))
        if back != out or not same_eol:
            fs.append(ac.Finding("error", "E2-rename-eol", "替换后行尾计数变化或写盘不一致：git diff 检查并还原", rel(f)))
        else:
            fs.append(ac.Finding("info", "E2-rename-applied",
                                 f"已字节级替换 '{old}' → '{new}' {item['count']} 处（LF/CRLF 计数不变）", rel(f)))
    return fs


def rename_paths(inputs: list[str], old: str) -> list[ac.Finding]:
    fs = []
    for s in inputs:
        p = Path(s)
        it = [p] if p.is_file() else [Path(dp) / n for dp, dns, fns in os.walk(p) for n in dns + fns
                                       if not any(x in SKIP_DIRS for x in Path(dp).parts)]
        for q in it:
            if old in q.name:
                fs.append(ac.Finding("info", "E2-rename-path",
                                     f"路径名含 '{old}'：本脚本只改文件内容，不改文件/目录名——用 git mv 改名后重跑本脚本复查",
                                     rel(q)))
    return fs


# ------------------------------------------------------------------ 主流程

def run_checks(o: argparse.Namespace) -> tuple[list[ac.Finding], dict]:
    findings: list[ac.Finding] = []
    extra: dict = {}
    mds, texts = collect(o.inputs)
    if o.rename:
        old, new = o.rename
        plan = rename_plan(texts, old, new)
        extra["rename"] = {"old": old, "new": new, "apply": bool(o.apply),
                           "plan": [{"file": rel(p["file"]), "count": p["count"], "samples": p["samples"]} for p in plan]}
        if o.apply:
            findings += rename_apply(plan, old, new)
        else:
            for p in plan:
                ex = "；".join(f"L{s['line']}: {s['before'][:60]} → {s['after'][:60]}" for s in p["samples"][:2])
                findings.append(ac.Finding("info", "E2-rename-plan",
                                           f"dry-run：将替换 '{old}' → '{new}' {p['count']} 处（字节级，行尾不动）。例：{ex}",
                                           rel(p["file"]), {"count": p["count"], "samples": p["samples"]}))
        findings += rename_paths(o.inputs, old)
        total = sum(p["count"] for p in plan)
        extra["rename"]["total"] = total
    stats = {"md": len(mds), "text": len(texts), "edit_lists": 0, "sources": 0, "refs": 0}
    extra_bases = [Path(b) for b in o.base]
    for md, root, explicit in mds:
        findings += check_md(md, root, explicit, o, extra_bases, stats)
    for f, explicit in texts:
        if explicit and f.suffix.lower() != ".md":
            _, ok = read_text(f)
            if not ok:
                findings.append(ac.Finding("error", "FMT-utf8", "不是 UTF-8 编码：转成 UTF-8 后重跑", rel(f)))
    if o.stale_token:
        fs, agg = stale_report(texts, o.stale_token, o.ignore_case)
        findings += fs
        extra["stale"] = agg
    findings += eol_audit(texts)
    extra["scanned"] = stats
    findings.insert(0, ac.Finding("info", "E2-scan-stats",
                                  f"扫描 md {stats['md']} 个 / 文本 {stats['text']} 个；剪辑单 {stats['edit_lists']} 个（来源 "
                                  f"{stats['sources']} 条）；媒体引用 {stats['refs']} 条"))
    lines = []
    for t, per in (extra.get("stale") or {}).items():
        n = sum(v["count"] for v in per.values())
        inpath = sum(1 for f in findings if f.code in ("E2-stale-path", "E2-missing-asset", "E2-missing-ref")
                     and t in (f.data.get("stale") or []))
        lines.append(f"旧 token '{t}'：共 {n} 处 / {len(per)} 个文件（其中 {inpath} 处在素材路径里）")
    if o.rename:
        r = extra["rename"]
        lines.append(f"改名 '{r['old']}' → '{r['new']}'：{r['total']} 处 / {len(r['plan'])} 个文件"
                     + ("，已写盘并复查" if o.apply else "，dry-run 未写盘（确认后加 --apply）"))
    miss = sum(1 for f in findings if f.code in ("E2-missing-asset", "E2-missing-ref"))
    lines.append(f"素材不存在 {miss} 条（E2 实证：143 处残留 → 30 条素材不存在；渲染前清零）")
    extra["summary"] = "\n".join(lines)
    return findings, extra


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", help="edit-list.md / 任意 .md / 目录（递归）")
    ap.add_argument("--stale-token", action="append", default=[], metavar="TOKEN",
                    help="已作废的旧 token（可重复，如 ep03、S01E03）")
    ap.add_argument("-i", "--ignore-case", action="store_true", help="旧 token 匹配忽略大小写（--rename 恒为字节级区分大小写）")
    ap.add_argument("--rename", nargs=2, metavar=("OLD", "NEW"), help="字节级替换计划（默认 dry-run）")
    ap.add_argument("--dry-run", action="store_true", help="只展示替换计划（默认行为）")
    ap.add_argument("--apply", action="store_true", help="真正写盘（仅与 --rename 一起用）")
    ap.add_argument("--bare", action="store_true", help="另查表格/正文中的裸媒体路径（不存在 → warn）")
    ap.add_argument("--base", action="append", default=[], metavar="DIR", help="额外的路径解析基准目录（可重复）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--selftest", action="store_true", help="运行自测（fixtures/asset_exists + 临时目录），全部通过退出 0")
    return ap


# ------------------------------------------------------------------ 自测

def selftest() -> int:
    results: list[tuple[bool, str]] = []

    def check(cond, label):
        results.append((bool(cond), label))
        print(f"{'PASS' if cond else 'FAIL'}  {label}")

    def run(*args: str):
        return run_checks(build_parser().parse_args(list(args)))

    def codes(fs, level=None):
        return sorted(f.code for f in fs if level is None or f.level == level)

    fx = ac.FIXTURES / "asset_exists"
    # 1. 共享 fixtures：0 error
    for d in ("good", "bad"):
        fs, _ = run(str(ac.FIXTURES / d))
        check(not codes(fs, "error"), f"fixtures/{d}（无剪辑单、无媒体引用）→ 0 error")
    # 2. 自带 fixtures
    fs, _ = run(str(fx / "good"))
    check(not codes(fs, "error") and not codes(fs, "warn"),
          "fixtures/asset_exists/good：local:black/white/#0B0B0B 合法、assets/ep04.srt 存在、占位与代码块不查 → 0 error 0 warn")
    fs, ex = run(str(fx / "bad"), "--stale-token", "ep03")
    errs = codes(fs, "error")
    check(errs.count("E2-missing-asset") == 2 and errs.count("D2-local-syntax") == 2
          and errs.count("E2-source-empty") == 1 and errs.count("E2-missing-ref") == 2,
          f"fixtures/asset_exists/bad：2 来源缺失 + 2 local: 语法错 + 1 空来源 + 2 引用缺失（实得 {errs}）")
    st = ex["stale"]["ep03"]
    check(sum(v["count"] for v in st.values()) == 5 and len(st) == 2 and any(f.code == "E2-stale-token" for f in fs)
          and "其中 2 处在素材路径里" in ex["summary"], "--stale-token ep03：5 处 / 2 个文件，其中 2 处在素材路径里")
    m2 = next(f for f in fs if f.code == "E2-missing-asset" and "CUT-002" in f.where)
    check("ep03" in m2.msg and "--rename" in m2.msg, "缺失来源含旧 token → 消息提示 --rename 预览")

    with tempfile.TemporaryDirectory(prefix="asset_selftest_") as tds:
        td = Path(tds)
        ep = td / "season-01" / "ep04"
        (ep / "assets" / "clips").mkdir(parents=True)
        (ep / "assets" / "boards").mkdir(parents=True)
        (td / "season-01" / "ep03" / "assets" / "clips").mkdir(parents=True)
        (ep / "assets" / "clips" / "SHOT-001.mp4").write_bytes(b"\x00\x00\x00\x18ftypmp42")
        (ep / "assets" / "clips" / "SHOT-003.mp4").write_bytes(b"")
        (ep / "assets" / "boards" / "CHR-A.png").write_bytes(b"\x89PNG")
        (td / "season-01" / "ep03" / "assets" / "clips" / "SHOT-002.mp4").write_bytes(b"old")
        el = ep / "edit-list.md"
        el.write_bytes(("| CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字 |\n|---|---|---|---|---|---|\n"
                        "| CUT-001 | assets/clips/SHOT-001.mp4 | 0.00 | 8.00 | — | — |\n"
                        "| CUT-002 | ../ep03/assets/clips/SHOT-002.mp4 | 0.00 | 5.00 | — | — |\n"
                        "| CUT-003 | `assets/clips/SHOT-003.mp4` | 0.00 | 5.00 | — | — |\n"
                        "| CUT-004 | assets/clips | 0.00 | 5.00 | — | — |\n"
                        "| CUT-005 | local:#1a2B3c | 0.00 | 1.00 | — | 未完待续 |\n"
                        "| CUT-006 | https://example.com/x.mp4 | 0.00 | 1.00 | — | — |\n").encode("utf-8"))
        (ep / "qc").mkdir()
        (ep / "qc" / "SHOT-001.md").write_bytes("# QC\r\n- 证据: `assets/boards/CHR-A.png`\r\n".encode("utf-8"))
        (ep / "notes.md").write_bytes(("板图 ![a](assets/boards/CHR-A.png \"t\") 与 [b](<assets/boards/CHR%20B.png>)\n"
                                       "旧 `../ep03/assets/clips/SHOT-002.mp4`\r\n"
                                       "裸路径 assets/clips/SHOT-404.mp4 只在 --bare 下查\n").encode("utf-8"))
        (ep / "bom.md").write_bytes(b"\xef\xbb\xbf# t\n")
        (ep / "names.md").write_text("产物：`final.mp4`、`animatic.mp4`；链接 [成片](final.mp4)\n", encoding="utf-8")

        fs, ex = run(str(td / "season-01"), "--stale-token", "ep03")
        e = {(f.code, f.where.split(":")[0].split("/")[-1], f.where.split("· ")[-1]) for f in fs if f.level == "error"}
        check(("E2-stale-path", "edit-list.md", "CUT-002") in e, "来源存在但含旧 token ep03 → error E2-stale-path（悄悄指向旧集）")
        check(("E2-empty-asset", "edit-list.md", "CUT-003") in e and ("E2-source-is-dir", "edit-list.md", "CUT-004") in e,
              "0 字节来源 → E2-empty-asset；来源是目录 → E2-source-is-dir")
        check(not any("CUT-001" in f.where or "CUT-005" in f.where for f in fs if f.level == "error"),
              "存在的来源与 local:#1a2B3c → 无 error")
        check(any(f.code == "E2-source-url" for f in fs), "URL 来源 → warn E2-source-url")
        check(not any(f.code == "E2-missing-ref" and "SHOT-001.md" in f.where for f in fs),
              "qc/SHOT-001.md 中 `assets/boards/CHR-A.png` 按上级（集目录）解析到 → 不误报")
        check(any(f.code == "E2-missing-ref" and "CHR B.png" in f.msg for f in fs),
              "链接 <assets/boards/CHR%20B.png> URL 解码后不存在 → error E2-missing-ref")
        check(not any(f.code == "E2-missing-bare" for f in fs), "默认不查裸路径")
        nm = [f for f in fs if f.code == "E2-missing-ref" and "names.md" in f.where]
        check(len(nm) == 1 and "final.mp4" in nm[0].msg,
              "反引号里的单独文件名 `final.mp4` 是命名约定不查；链接 [成片](final.mp4) 照查 → 1 条")
        eol = {(f.code, Path(f.where).name) for f in fs if f.level == "warn"}
        check(("E2-crlf", "SHOT-001.md") in eol and ("E2-mixed-eol", "notes.md") in eol and ("E2-bom", "bom.md") in eol,
              "行尾审计：CRLF / 混合行尾 / BOM 各报 warn")
        fs, _ = run(str(td / "season-01"), "--bare")
        check(any(f.code == "E2-missing-bare" and f.level == "warn" and "SHOT-404" in f.msg for f in fs),
              "--bare：裸路径不存在 → warn E2-missing-bare")

        # 3. --rename dry-run 不写盘；--apply 字节级替换、行尾零扰动
        before = {p: p.read_bytes() for p in ep.rglob("*.md")}
        fs, ex = run(str(ep), "--rename", "ep03", "ep04")
        check(all(p.read_bytes() == b for p, b in before.items()) and ex["rename"]["total"] == 2
              and any(f.code == "E2-rename-plan" for f in fs), "--rename ep03 ep04（dry-run）：计划 2 处，文件一字未改")
        crlf_before = sum(b.count(b"\r\n") for b in before.values())
        lf_before = sum(b.count(b"\n") for b in before.values())
        fs, ex = run(str(ep), "--rename", "ep03", "ep04", "--apply")
        after = {p: p.read_bytes() for p in ep.rglob("*.md")}
        check(sum(b.count(b"\r\n") for b in after.values()) == crlf_before
              and sum(b.count(b"\n") for b in after.values()) == lf_before
              and not any(b"ep03" in b for b in after.values()), "--apply：ep03 全部替换，LF/CRLF 计数逐字节不变")
        check(any(f.code == "E2-rename-applied" for f in fs)
              and any(f.code == "E2-missing-asset" and "../ep04/assets/clips/SHOT-002.mp4" in f.msg for f in fs),
              "--apply 后立即复查：新路径 ../ep04/assets/clips/SHOT-002.mp4 不存在 → error（提示补素材/改路径）")
        fs, _ = run(str(td / "season-01"), "--rename", "ep03", "ep04")
        check(any(f.code == "E2-rename-path" and f.where.endswith("ep03") for f in fs), "目录名含 ep03 → info：用 git mv 改名")

        # 3b. Markdown 边界（回归）：嵌套围栏 / HTML 注释 / 双反引号 / 全角冒号 / 重复 CUT / 大小写
        md = td / "md-edge"
        (md / "assets" / "clips").mkdir(parents=True)
        (md / "assets" / "clips" / "SHOT-002.mp4").write_bytes(b"x")
        (md / "notes.md").write_text(
            "````markdown\n```h3\n示例 `assets/clips/SHOT-404.mp4`\n```\n````\n"
            "<!-- 旧 `assets/clips/SHOT-407.mp4`\n仍在注释里 `assets/clips/SHOT-408.mp4` -->\n"
            "嵌套 ``code with `assets/clips/SHOT-409.mp4` inside`` 结束；代码里的 `<!--` 不开注释 `assets/clips/SHOT-410.mp4`\n",
            encoding="utf-8")
        (md / "edit-list.md").write_text(
            "| CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字 |\n|---|---|---|---|---|---|\n"
            "| CUT-001 | local：black | 0 | 1 | — | — |\n| CUT-001 | assets/clips/SHOT-002.MP4 | 0 | 1 | — | — |\n",
            encoding="utf-8")
        fs, _ = run(str(md))
        refs = sorted(f.data.get("ref", "") for f in fs if f.code == "E2-missing-ref")
        check(refs == ["assets/clips/SHOT-409.mp4", "assets/clips/SHOT-410.mp4"],
              f"嵌套 ````/``` 围栏与 HTML 注释里的路径不查；``…`x`…`` 与注释标记后的路径照查（实得 {refs}）")
        ls = [f for f in fs if f.code == "D2-local-syntax"]
        check(ls and "全角冒号" in ls[0].msg and "local:black" in ls[0].msg and not any(
              f.code == "E2-missing-asset" and "local" in f.msg for f in fs), "local：black（全角冒号）→ D2-local-syntax 并给出改法")
        check(any(f.code == "FMT-dup-cut" and f.level == "warn" for f in fs), "CUT-001 重复 → warn FMT-dup-cut")
        check(any(f.code == "E2-missing-asset" and "大小写不同的 SHOT-002.mp4" in f.msg for f in fs),
              "SHOT-002.MP4 vs 实际 SHOT-002.mp4 → 缺失并提示大小写差异")

        # 3c. --apply 写盘失败（只读 / 中途出错）→ error，不崩溃，不留半截文件
        rw = td / "rw"
        rw.mkdir()
        (rw / "a.md").write_bytes(b"ep03 a\r\n")
        (rw / "b.md").write_bytes(b"ep03 b\n")
        real_access, real_replace = os.access, os.replace
        try:
            os.access = lambda path, mode: False if Path(path).name == "a.md" else real_access(path, mode)
            os.replace = lambda a, b: (_ for _ in ()).throw(OSError(28, "No space left on device")) \
                if Path(b).name == "b.md" else real_replace(a, b)
            fs, _ = run(str(rw), "--rename", "ep03", "ep04", "--apply")
        finally:
            os.access, os.replace = real_access, real_replace
        check(sum(f.code == "E2-rename-failed" and f.level == "error" for f in fs) == 2
              and (rw / "a.md").read_bytes() == b"ep03 a\r\n" and (rw / "b.md").read_bytes() == b"ep03 b\n"
              and sorted(x.name for x in rw.iterdir()) == ["a.md", "b.md"],
              "--apply 遇只读 / 写盘失败 → error E2-rename-failed，原文件逐字节不变、无临时文件残留（回归：曾崩溃）")

        # 4. CLI 契约
        me = [sys.executable, "-B", str(Path(__file__).resolve())]
        r = subprocess.run(me + [str(fx / "good"), "--json"], capture_output=True, text=True)
        ok = False
        try:
            ok = json.loads(r.stdout)["ok"] is True
        except Exception:
            pass
        check(r.returncode == 0 and ok, "CLI good --json → 退出码 0，ok=true")
        r = subprocess.run(me + [str(fx / "bad"), "--stale-token", "ep03"], capture_output=True, text=True)
        check(r.returncode == 1 and "E2-missing-asset" in r.stdout and "旧 token 'ep03'" in r.stdout, "CLI bad → 退出码 1")
        r = subprocess.run(me + [str(fx / "bad")], capture_output=True, env=dict(os.environ, PYTHONIOENCODING="gbk"))
        check(r.returncode == 1 and b"Traceback" not in r.stderr and "结果".encode("gbk") in r.stdout,
              "stdout 为 GBK（Windows cmd 重定向，E3-1）→ 报告照出、退出码 1，不因 ❌ 等图标崩溃（回归）")
        r = subprocess.run(me + [str(td / "nope")], capture_output=True, text=True)
        check(r.returncode == 2, "CLI 路径不存在 → 退出码 2")
        r = subprocess.run(me + [str(ep), "--apply"], capture_output=True, text=True)
        check(r.returncode == 2, "CLI --apply 不带 --rename → 退出码 2")
        r = subprocess.run(me + [str(ep), "--rename", "a\nb", "c"], capture_output=True, text=True)
        check(r.returncode == 2, "CLI --rename 含换行 → 退出码 2")
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
    ap = build_parser()
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.inputs:
        ap.print_usage(sys.stderr)
        ac.die("需要 edit-list.md / .md 文件或目录（或 --selftest）")
    if a.apply and not a.rename:
        ac.die("--apply 只能与 --rename OLD NEW 一起用")
    if a.apply and a.dry_run:
        ac.die("--apply 与 --dry-run 不能同时给")
    if a.rename:
        old, new = a.rename
        if not old or old == new or any(c in old + new for c in "\r\n"):
            ac.die("--rename OLD NEW：OLD 非空、OLD≠NEW、两者都不能含换行符")
    for t in a.stale_token:
        if not t.strip():
            ac.die("--stale-token 不能为空")
    for b in a.base:
        if not Path(b).is_dir():
            ac.die(f"--base 不是目录：{b}")
    findings, extra = run_checks(a)
    return ac.emit(TITLE, findings, a.json, extra)


if __name__ == "__main__":
    sys.exit(main())
