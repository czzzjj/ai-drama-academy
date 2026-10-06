---
name: edit-and-assemble
description: 把验收通过的长镜装配成可交付成片：按契约写 edit-list.md（CUT/来源/入点/出点/字幕/画面文字），快剪从≥124 帧长镜里取段、出点避开尾部崩解窗，纯色卡与文字叠层一律本地生成，按 GB 45438 程序化叠加 AI 显式标识并写入 AIGC 元数据，字幕逐字取自剧本，渲染 1080×1920 后跑 asset_exists 与 loudness_verify，改集号走字节级替换与全量复查。Use when assembling an episode, writing or changing the edit list, adding title cards/subtitles/AI labels, rendering, or renumbering episodes/shots. 触发词：剪辑、装配、剪辑单、字幕、字卡、黑场、AI标识、渲染、成片、改集号、路径残留、edit list, assemble, cut, subtitles, title card, AIGC label, render, deliverable 1080x1920, renumber。不负责镜头是否合格（shot-qc）、声音分层与混音设计（sound-design）、全片观感评审（screening-review）、发布物料（publish-prep）。
---
# 剪辑装配（edit-and-assemble）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。剪辑单契约见 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §4、交付规格见 §0.6。委托方的剪辑单 + 叠层 + verify 流程是正面资产〔委托方实证·P7〕；AIGC 标识为〔外部调研〕。

## 何时用 / 何时不用

- **用**：本集全部镜过了 shot-qc 之后装配；任何改 CUT、字幕、字卡、标识的时候；改集号 / 镜号 / 目录名时（必须走步骤 10）。
- **不用**：想靠剪辑救"看不懂"——叙事断裂回 script-doctor / storyboard（病灶路由）；剪辑只能救节奏与表演慢半拍（插入镜）。
- **不用**：让生成器出黑场、字卡、标题、标识（D2：一律本地生成）。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| `qc/SHOT-nnn.md`（结论、崩解起点、条件） | `edit-list.md`：`CUT \| 来源 \| 入点 \| 出点 \| 字幕 \| 画面文字`（可加备注列：音频偏移、所属段） | [`70-playbooks/templates/edit-list.md`](../../70-playbooks/templates/edit-list.md) |
| `storyboard.md` 的 `对白` 列 | `字幕` 列（逐字） | 同上 |
| `sound-plan.md`、终混音轨 | 渲染成片 `final/epNN.mp4`（1080×1920，含 AIGC 元数据） | — |
| 脚本报告 | `review/l0-report.json`；`final-report.md` 的技术段 | [`70-playbooks/templates/final-report.md`](../../70-playbooks/templates/final-report.md) |

## 步骤

1. **只收已验收的镜**：每个生成来源必须有 `qc/SHOT-nnn.md` 且结论为通过 / 有条件通过；有条件通过的条件（如"出点 ≤ 8.40s"）直接成为该 CUT 的约束。没有 QC 记录的素材禁止进剪辑单。〔委托方实证·C2〕
2. **写剪辑单（契约表头逐字）**：`CUT-nnn` 连续编号；`来源` 写相对本集目录的路径；入出点两位小数。生成单位（镜）≥124 帧、剪辑单位（CUT）可以很短：快剪从长镜里取多个 CUT（同一 `来源` 多行），不另生成短镜（R6）。验：R-CUT-12；`python3 50-rubrics/scripts/psnr_scan.py final/epNN.mp4 --mode final --edit-list edit-list.md`（`A1-mean-short` 报出时，每个 <5s CUT 都必须指向一条 ≥124 帧生成镜的取段）。
3. **出点避开尾部崩解**：每个来自生成镜的 CUT，出点 ≤ 镜长 − 声明的 `尾部余量`（1.3–1.5s），且早于 QC 记录的崩解起点。验：R-CUT-13。〔外部调研·S-H3-09；委托方实证·P8〕
4. **切点**：动作中切（cutting on action）、同轴；每个切点前后各 2 帧导出目视，无闪帧 / 跳帧 / 误剪。J/L cut 按 sound-design 的音频偏移备注执行（每场对白 ≥1 处 L-cut，换场 ≥1 处 J-cut）。验：R-CUT-14、R-SND-05。〔外部调研·S-STORY-10〕
5. **纯色卡与叠层文字本地生成**：黑场 / 白场 / 色卡写 `local:black`、`local:white`、`local:#RRGGBB`；片名、字卡、人名条写在 `画面文字` 列，由剪辑程序（ffmpeg `drawtext` / `color` 源）叠加，绝不送生成器。验：R-CUT-09；`python3 50-rubrics/scripts/asset_exists.py edit-list.md`（`D2-local-syntax`）。〔委托方实证·D1、D2〕
6. **AI 显式标识（GB 45438）**：每集（不只第一集）起始画面叠加含"AI / 人工智能"+"生成 / 合成"的文字，例：`本剧由人工智能生成`。规格：位于起始画面的**边或角**，且避开平台 UI 遮挡区；**字高 ≥ 画面短边 5%**（1080 宽 → 字形实高 ≥54px，留余量按 60px 设）；从第 0 帧起显示 **≥2s**（学院默认 2.5s）。片头同时标剧名与许可证号 / 节目编号（《微短剧发展管理办法》第 27、34 条）。验：R-PUB-01、R-PUB-02、R-PUB-03、R-PUB-04、R-PUB-05、R-PUB-07。〔外部调研·S-PLAT-01、S-PLAT-02、S-PLAT-03〕
7. **隐式标识（元数据）**：渲染时写入字段名含 `AIGC` 的 JSON 元数据（例：`-metadata comment='{"AIGC":{"Label":"1","ContentProducer":"<属主>","ProduceID":"S01E03"}}'`，具体键名以 S-PLAT-02 原文为准，属主确认）。渲染后 `ffprobe -show_format final/epNN.mp4` 截取证据。验：R-PUB-06。
8. **字幕逐字取自剧本**：`字幕` 列 = 分镜 `对白` 列逐字，不取自转写；转写只用来定时间。字幕位置避开安全区（默认上 14% / 下 35% / 左右 6% 禁区内不放关键文字）。验：R-CUT-11、R-CUT-10（成片 OCR 文字都能在 `字幕` 或 `画面文字` 列逐字找到）、R-PUB-19。〔委托方实证·P7、D5〕
9. **渲染与 verify**：交付稿统一 **1080×1920 严格 9:16**；768×1344、480×864 只能做中间稿。渲染前 `python3 50-rubrics/scripts/asset_exists.py season-01/ --stale-token epNN-1`（全部来源存在、无旧集号残留、无 CRLF）；渲染后 `python3 50-rubrics/scripts/loudness_verify.py final/epNN.mp4 --min <季规格下限> --max <季规格上限>`（`T4-lufs`、`T4-true-peak`、`T3-aspect`、`T3-black`、`T3-freeze`、`T3-decode-error`）。每段黑场 / 冻结都对上设计登记。两份报告 `--json` 汇入 `review/l0-report.json`。验：R-CUT-01–R-CUT-08、R-CUT-15。
10. **改号卫生**：集号、镜号是显示编号；资产文件用稳定 ID（`CHR-`、`REF-SHOTnnn-START`）。改号流程：`python3 50-rubrics/scripts/asset_exists.py season-01/ --rename ep03 ep04` 先 dry-run 看替换计划 → 确认后加 `--apply`（字节级替换，行尾零扰动）→ 全仓 `asset_exists.py` 全量复查 → 重渲 → 重跑 verify。禁止手工在编辑器里查找替换。验：R-SEA-18、R-CUT-08。〔委托方实证·E2、E3-1〕
11. **交付声明只写证据支持的级别**：只有 L0 证据时，`final-report.md` 第一节写"技术合格（L0），观感未验证"，全文不出现"达标 / 可发布 / 质量通过"。L1/L2 由 screening-review 与 cold-audience-test 补证。验：R-CUT-16。〔委托方实证·F1、F2〕

## 判据

- 技术（L0，`[自动]`）：R-CUT-01（-16 LUFS ±1）、R-CUT-02（真峰）、R-CUT-03（1080×1920）、R-CUT-04、R-CUT-05、R-CUT-06（时长在季规格内）、R-CUT-07、R-CUT-08、R-CUT-15。
- 剪辑：R-CUT-09（本地卡）、R-CUT-10、R-CUT-11（字幕逐字）、R-CUT-12（快剪取自长镜）、R-CUT-13（避崩解）、R-CUT-14（切点目视）、R-SND-05。
- 合规叠层：R-PUB-01 – R-PUB-07、R-PUB-19。
- 季级：R-SEA-17（时长）、R-SEA-18（改号无残留）。
- 质量维度：**Q6 节奏与速度**（切点、CUT 长度分布）、**Q8 声音与对白**（字幕与声音一致）、**Q5 美术与密度**（无多余文字）；L0 全绿不证明任何一维 ≥2。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| 改集号后剪辑单仍指向旧路径，渲染出错片 | [`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md) | 步骤 10 dry-run → apply → 全量复查 → 重渲 |
| 让生成器出纯黑字卡，结果不黑、带纹理或带字 | [`60-casebook/cards/D2-solid-black-fails.md`](../../60-casebook/cards/D2-solid-black-fails.md) | 步骤 5 `local:` 来源 + 程序化叠字 |
| 成片里出现生成器自带字幕，与真字幕叠两层 | [`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md) | 步骤 8 成片 OCR 对账：每段文字必须在剪辑单里能找到 |
| 为了快剪去生成 2–3 秒短镜，片段感、空间断 | [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md) | 步骤 2：快剪只从长镜取段 |
| 出点落在尾部崩解里，切点处闪噪点（验收没看 TAIL 格） | [`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md) | 步骤 3 出点约束 + 步骤 4 切点帧目视 |
| Windows cmd 下中文路径吞输出，以为渲染成功 | [`60-casebook/cards/E3-environment-quirks.md`](../../60-casebook/cards/E3-environment-quirks.md) | 文件名英文；以脚本退出码与 `--json` 为准，不以控制台沉默为准 |
| verify 全绿即宣称可发布 | [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md) | 步骤 11 交付声明分级 |

## 关联

- 理论：[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)（标识规格）、[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)。
- 裁决：[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R6（短剪 ≠ 碎镜）、第三部分（画幅与响度）、第四部分（AIGC 标识）。
- 相邻技能：[`20-craft/shot-qc/SKILL.md`](../shot-qc/SKILL.md)（上游）、[`20-craft/sound-design/SKILL.md`](../sound-design/SKILL.md)、[`20-craft/screening-review/SKILL.md`](../screening-review/SKILL.md)（下游）、[`20-craft/publish-prep/SKILL.md`](../publish-prep/SKILL.md)（合规复核）。
- 找错题：[`60-casebook/drills/DR-10.md`](../../60-casebook/drills/DR-10.md)、[`60-casebook/drills/DR-14.md`](../../60-casebook/drills/DR-14.md)、[`60-casebook/drills/DR-01.md`](../../60-casebook/drills/DR-01.md)。
- 判据清单：[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/publish.md`](../../50-rubrics/checklists/publish.md)（R-PUB-01–07）。

## → 行为改变

- 下次想要一个 3 秒快切，先在已有长镜里找取段，禁止为短 CUT 单独生成。
- 下次任何集渲染前，先确认第 0 帧起有 ≥54px 字高的 AI 标识叠层与 AIGC 元数据，每一集都要。
- 下次改集号，先 `--rename` 预演，再 `--apply`，再全量 `asset_exists.py`，再重渲。
- 下次写交付声明，先数手上有哪级证据，只有 L0 就只写 L0。
