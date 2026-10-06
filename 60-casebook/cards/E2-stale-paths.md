---
id: E2
title: 改集号后路径残留
group: E 流程工程
scope: 工程细节
severity: 一般
provenance: 委托方实证
skills: [edit-and-assemble, production-director]
drills: [DR-14]
---
# E2 · 改集号后路径残留

> 一句话：**改名是一次迁移。** 要做的是：先预演、再执行、执行后全量复查，三步都靠脚本。旧路径比"素材不存在"更危险的情况，是它**仍然存在**：那样它会悄悄指向旧集的素材。

## 症状（含人类主创原话，逐字引用档案）

- 整季重编号之后，4 份操作文档里残留 143 处旧素材路径，渲染校验报出 30 条"素材不存在"〔委托方实证·E2〕。
- 档案没有保留人类主创关于本案的「」逐字原话。本案在渲染校验阶段被拦下。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 规模：4 份文档、143 处残留，校验只报出 30 条〔委托方实证·E2〕。
- **143 与 30 的差值**：〔学院推断〕剩下约 113 处，要么在不参与渲染的文档里，要么旧路径**仍然能解析到旧集的同名文件**，所以没有报错。后一种会把旧集素材悄悄渲染进新集，比报错更糟。**验证方法**：对改名前的仓库快照跑 `asset_exists.py <季目录> --stale-token <旧集号>`，统计报 `E2-stale-path` 的路径中仍然存在的有多少。
- 修正时特别强调了"保持行尾零扰动"〔委托方实证·E2〕。委托方环境里有 Windows cmd（见 E3），文本模式替换可能把 LF 改成 CRLF，从而让表格解析和 diff 全部失真〔学院推断〕。

## 根因（分条；区分"直接原因"与"方法论原因"）

1. **直接原因**：同一条素材路径被硬写在多份文档里（分镜、提示词、剪辑单、报告），重编号时只改了一部分。
2. **方法论原因**：把改名当成"编辑"，没有当成"迁移"。没有替换计划（每个文件改几处），也没有改后的全量复查，靠渲染失败才发现。
3. **方法论原因**：校验只查"在不在"，不查"是不是这一集的"。存在但属于旧集的路径能通过存在性检查。
4. **外部佐证**：zenstory 剪辑工具把"来源 ID 可解析""素材比剪辑单新（需重测字幕时间）"列为 check 阶段的检查项；它的进入条件是素材文件当前可读，job 成功或 adapter 返回成功都不算数〔外部调研·S-ZEN-11〕。另一份资料把"版本和执行状态冒充内容权威"列为六类常见返工原因之一〔外部调研·S-ZEN-23〕。

## 修正过程（做了什么、第几轮、结果）

- 委托方：二进制级替换勘误，保持行尾零扰动；全仓 grep 复查；重新渲染〔委托方实证·E2〕。
- 学院固化为三步（[`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §7）：
  1. 预演：`asset_exists.py season-01/ --rename ep03 ep04`。默认 dry-run，只列出每个文件的替换次数和示例行。
  2. 执行：同一条命令加 `--apply`。字节级替换，写后校验 LF/CRLF 计数不变，先写临时文件再原子替换。文件名或目录名里含旧集号的，脚本只提示，改名用 `git mv`。
  3. 复查：`asset_exists.py season-01/ --stale-token ep03 --stale-token S01E03`，然后重新渲染，再跑 `loudness_verify.py`。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 渲染前跑 `asset_exists.py <剪辑单或本季目录>`，以下规则码为 0：`E2-missing-asset`、`E2-empty-asset`、`E2-missing-ref`、`E2-source-empty`〔E2、T-3〕。
- [自动] 任何改集号、改镜号之后跑 `--stale-token <旧号>`，`E2-stale-path` 为 0。路径存在也要报，因为它可能指向旧集〔E2〕。
- [自动] `E2-crlf`、`E2-mixed-eol`、`E2-bom` 为 0。全仓统一 UTF-8 + LF〔E2；format-contracts §0.1〕。
- [自动] 改名一律走 `--rename` 预演 → `--apply`。**禁止**用编辑器全局替换或逐条手改〔E2〕。
- [目视] 重渲后抽看被改过路径的 CUT 前后帧，确认画面属于新集〔E2〕。

## → 行为改变（下次……）

- 下次改集号、镜号、资产 ID，先预演再执行，执行后跑 `--stale-token`。三步做完才允许渲染。
- 下次看到存在性检查全绿，不要认为路径都对：还要确认路径属于本集。
- 下次替换某个素材（换版覆盖，B4），立刻全仓搜索旧文件名，把引用一并替换，再跑 `asset_exists.py`。
- 下次新建文档引用素材，只写相对本集目录的路径。**禁止**写绝对路径和反斜杠（会报 `E2-source-absolute`、`E2-backslash`）。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ☆ 143、30、4 份这些数字属于本项目。
- ★ "改名 = 迁移，先预演、后执行、再复查"，以及"存在 ≠ 正确"，适用于任何多文档引用同一批素材的管线。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)（剪辑单来源、渲染前复查）、[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（改名迁移流程）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)。
- 判据清单：[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/season.md`](../../50-rubrics/checklists/season.md)。
- 脚本：[`50-rubrics/scripts/asset_exists.py`](../../50-rubrics/scripts/asset_exists.py)、[`50-rubrics/scripts/loudness_verify.py`](../../50-rubrics/scripts/loudness_verify.py)。
- 找错题：[`60-casebook/drills/DR-14.md`](../../60-casebook/drills/DR-14.md)（槽位 / 路径）。
- 相邻案例：[`60-casebook/cards/E1-slot-order.md`](E1-slot-order.md)、[`60-casebook/cards/E3-environment-quirks.md`](E3-environment-quirks.md)（行尾与 Windows 环境）、[`60-casebook/cards/B4-duplicate-artifacts.md`](B4-duplicate-artifacts.md)（换版后的引用替换）。
