# 20-craft · 技能总表

> 17 个技能 = 17 个可装载的执行单元。每个 `SKILL.md` 的 frontmatter 只有 `name` / `description`（运行时据此触发），正文固定六节：何时用 / 何时不用、输入 → 输出、步骤、判据、失败模式、关联。格式见 [`CONVENTIONS.md`](../CONVENTIONS.md) §5.2；名称固定见 §6。
> 装载规则：**一次只按当前阶段装载 1–3 个技能**；阶段闸门与拍板点由 production-director 掌控。技能给出"怎么做"，判据在 [`50-rubrics/`](../50-rubrics/)，脚本在 [`50-rubrics/scripts/`](../50-rubrics/scripts/)，模板在 [`70-playbooks/templates/`](../70-playbooks/templates/)。

## 1. 流水线顺序

```
production-director（全程：阶段闸门、病灶路由、人类拍板点①–④）
  └─ 开发/预制作：casting-and-canon ─┬─ script-doctor ─┬─ visual-bible
                                      └────────────────┴──→ asset-boards
  └─ 设计：storyboard-long-take / action-choreography / performance-direction / sound-design（并行，同一张分镜表）
  └─ 制作：keyframe-freeze → video-prompting-h3 → shot-qc（逐镜，结构性缺陷回流上游）
  └─ 后期：edit-and-assemble
  └─ 审片：screening-review → cold-audience-test（L1/L2 证据）
  └─ 发布：publish-prep（合规先行 → 拍板点④）
multi-episode-arc：横跨整季——开发阶段写季圣经，每集开工前继承检查、交付后季级对账
```

硬规则：
1. 任何反馈先进 screening-review 的翻译协议，再按 [`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) §3 路由回病灶阶段的技能；禁止直接在下游补丁（F3）。
2. 生成前 6 个脚本全 0 error 才进生成；出片后 4 个脚本 + 目视证据才进剪辑；成片 2 个脚本 + 审片证据才写交付声明（[`50-rubrics/scripts/README.md`](../50-rubrics/scripts/README.md) §5）。
3. 交付声明只写证据支持的级别（[`50-rubrics/definition-of-done.md`](../50-rubrics/definition-of-done.md)）。

## 2. 技能一览

| 技能 | 阶段 | 输入 → 输出 | 关键案例 | 关键脚本 / 清单 |
|---|---|---|---|---|
| [`production-director`](production-director/SKILL.md) | 全程 | 题材/原著 → 阶段计划、闸门记录、拍板点上报 | F1–F4, G7 | 全部脚本链；全部清单 |
| [`casting-and-canon`](casting-and-canon/SKILL.md) | 开发 | 原著 → `anchors.md`（锚点句 EN、必现、禁用、来源依据） | P1, C1, B1 | `prompt_lint.py --anchors`；R-SEA-10/12 |
| [`script-doctor`](script-doctor/SKILL.md) | 开发/预制作 | 原著/梗概 → `episode-script.md`（钩子、信息密度、对白容量） | D3, A1, GAP-1 | `dialogue_capacity.py`；R-SCR |
| [`visual-bible`](visual-bible/SKILL.md) | 预制作 | 题材 + 风格库 → `visual-bible.md`（色彩剧本、光态） | GAP-4, M2 | R-COL |
| [`asset-boards`](asset-boards/SKILL.md) | 预制作 | 锚点卡 → 板图（多 seed + 逐特征验收） | P2, C1, C2 | `contact_sheet.py --crop`；R-BRD |
| [`storyboard-long-take`](storyboard-long-take/SKILL.md) | 设计 | 剧本 → `storyboard.md`（段/拍/镜、运镜因果、起始帧方位） | A1, A4, A5, P10 | `segment_rhythm.py`、`direction_audit.py`；R-SB |
| [`action-choreography`](action-choreography/SKILL.md) | 设计 | 打斗段 → 七相动作链、交手回合、战术链 | A2, A3 | `segment_rhythm.py`、`prompt_lint.py`（VP-realtime） |
| [`performance-direction`](performance-direction/SKILL.md) | 设计 + 出片验收 | 剧本情绪 → 表演卡（任务动词、表情链、视线、闭嘴句） | GAP-5, B3, D3 | `prompt_lint.py`（VP-lipsync）、`psnr_scan.py`；R-PRF-01–10 |
| [`sound-design`](sound-design/SKILL.md) | 设计 + 后期 | 分镜 → `sound-plan.md`、soundscape 字段、终混、许可台账 | GAP-3, GAP-6, D5 | `loudness_verify.py`、`prompt_lint.py`（VP-music）；R-SND-01–10 |
| [`keyframe-freeze`](keyframe-freeze/SKILL.md) | 制作 | 分镜 + 板图 → 冻结提示词 + 起始关键帧（9:16，海报级验收） | P3, P4, M2 | `contact_sheet.py`；R-KF |
| [`video-prompting-h3`](video-prompting-h3/SKILL.md) | 制作 | 分镜 + 关键帧 → `video-prompts.md`（模式 Ref2VA/FL2VA、禁令包、对白标记） | D1–D4, A3, A5, B2, B3, E1 | `h3_frame_grid.py`、`prompt_lint.py`、`direction_audit.py`、`slot_order_check.py`；R-VP |
| [`shot-qc`](shot-qc/SKILL.md) | 制作 | 出片 → `qc/SHOT-nnn.md` + 证据文件；随机/结构判定 | P8, D5, B4, C2 | `contact_sheet.py`、`psnr_scan.py`、`burnin_text_scan.py`、`transcript_reconcile.py`；R-VID-01–23 |
| [`edit-and-assemble`](edit-and-assemble/SKILL.md) | 后期 | 已验收镜 → `edit-list.md`、1080×1920 成片、AIGC 标识、`review/l0-report.json` | E2, D2, P7 | `asset_exists.py`、`loudness_verify.py`、`psnr_scan.py --mode final`；R-CUT-01–16 |
| [`screening-review`](screening-review/SKILL.md) | 审片 | 成片 → 自我放映、Q1–Q8 评分卡、独立评审、交付声明 | F1, F2, F3 | `contact_sheet.py`（证据帧）；R-CUT-15–22 |
| [`cold-audience-test`](cold-audience-test/SKILL.md) | 审片 | 成片 → ≥3 份冷观众记录、断点路由缺陷单 | F1, GAP-2 | R-CUT-19、R-SEA-20、R-PUB-22 |
| [`publish-prep`](publish-prep/SKILL.md) | 发布 | 成片 + 许可台账 → `publish-kit.md`（合规表先行）、物料、回流记录 | GAP-1, B3 | `contact_sheet.py`、`ffprobe`；R-PUB-01–25 |
| [`multi-episode-arc`](multi-episode-arc/SKILL.md) | 全季 | 原著 + 季结构 → `season-bible.md`、`episode-map.md`、版本化锚点、状态账本 | GAP-7, B1, E2 | `prompt_lint.py`（VP-anchor）、`asset_exists.py --rename`；R-SEA-01–20 |

## 3. 模板对照（[`70-playbooks/templates/`](../70-playbooks/templates/)）

| 模板 | 主要使用技能 |
|---|---|
| `season-bible.md` | multi-episode-arc、production-director |
| `episode-script.md` | script-doctor、multi-episode-arc |
| `anchor-card.md` | casting-and-canon、multi-episode-arc |
| `visual-bible.md` | visual-bible |
| `storyboard.md` | storyboard-long-take、action-choreography、performance-direction |
| `keyframe-prompt.md` | keyframe-freeze、performance-direction |
| `video-prompt-h3.md` | video-prompting-h3、sound-design |
| `qc-record.md`、`defect-ticket.md` | shot-qc、screening-review、cold-audience-test |
| `edit-list.md`、`final-report.md` | edit-and-assemble、screening-review |
| `review-memo.md` | screening-review |
| `cold-audience-sheet.md` | cold-audience-test |
| `publish-kit.md` | publish-prep |

## 4. 装载提示

- 技能 ≠ 能力（F4）：装载后用对应找错题自测（[`60-casebook/drills/README.md`](../60-casebook/drills/README.md)），答不出根因就别开工。
- 每个技能的"失败模式"表都链接案例卡；遇到同症状先读卡，再执行该技能的防线步骤。
- 技能之间冲突时以 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) 的 R1–R7 立场为准。
