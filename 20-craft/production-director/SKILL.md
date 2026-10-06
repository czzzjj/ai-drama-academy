---
name: production-director
description: 六阶段闸门总调度：把一集/一季 AI 竖屏短剧从开发→预制作→制作→后期→审片→发布逐阶段推进，每阶段先交齐产物、过闸门清单再放行，只在 4 个人类拍板点打扰人类，把缺陷单按病灶路由回产生它的阶段修，最后按 L0–L2 写交付声明。Use when starting a new episode/season, deciding "what stage are we in / can we move on", routing a defect, or writing a delivery declaration. 触发词：开新集、开新季、制作流程、阶段闸门、能不能进下一步、缺陷回流、病灶路由、交付声明、人类拍板、production pipeline, stage gate, defect routing, delivery declaration, G7. 不负责具体某一阶段的手艺（剧本诊断、分镜、提示词、镜头 QC、剪辑、审片各有专门技能），也不替人类做题材与是否发布的决定。
---
# 制作总调度（production-director）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。本技能回答 G7「生产是否应该有工业流程」：有，六阶段 + 闸门 + 病灶路由，定义见 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md)。

## 何时用 / 何时不用
- **必须用**：开一集或一季的第一步；任何"要不要进下一阶段"的判断；收到任何人类反馈或审片缺陷时（先路由，再动手）；写 `final-report.md` 交付声明之前。
- **不用**：只改一镜提示词措辞（→ [`video-prompting-h3`](../video-prompting-h3/SKILL.md)）；只做单镜验收（→ `shot-qc`）。但若该改动源于缺陷单，仍先走本技能的路由步骤。
- 判决：委托方历史产线只有"2 制作"在认真运转，0/1/4/5 缺席，所以缺陷全在 2 被发现又在 2 打补丁〔委托方实证·F3、G7〕。本技能的存在就是禁止这种结构。

## 输入 → 输出
| 阶段 | 必交产物（`season-01/ep03/` 下） | 模板 | 闸门（清单 + 脚本） | 主技能 |
|---|---|---|---|---|
| 0 开发 | `season-bible.md`、`episode-map.md`、`benchmarks.md` | [`70-playbooks/templates/season-bible.md`](../../70-playbooks/templates/season-bible.md) | R-SEA-01 – R-SEA-08、R-SCR-20 | `multi-episode-arc`、[`script-doctor`](../script-doctor/SKILL.md) |
| 1 预制作 | `script.md`、`visual-bible.md`、`anchors.md`、`assets/boards/`、`storyboard.md`、`action-design.md`、`sound-plan.md`、`animatic.mp4` | `episode-script.md`、`visual-bible.md`、`anchor-card.md`、`storyboard.md` | R-SCR、R-SB、R-BRD、R-COL-01 – R-COL-03、R-PRF-01 – R-PRF-04；`dialogue_capacity.py`、`segment_rhythm.py` 必须 0 error | casting / visual-bible / asset-boards / storyboard / action |
| 2 制作 | `keyframes/`、`video-prompts.md`、`clips/`、`qc/<SHOT>.md` | `keyframe-prompt.md`、`video-prompt-h3.md`、`qc-record.md` | R-KF、R-VP、R-VID；`prompt_lint.py`、`direction_audit.py`、`slot_order_check.py`、`h3_frame_grid.py` | [`keyframe-freeze`](../keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../video-prompting-h3/SKILL.md)、`shot-qc` |
| 3 后期 | `edit-list.md`、`final.mp4`、`review/l0-report.json` | `edit-list.md` | R-CUT-01 – R-CUT-15、R-SND；`asset_exists.py`、`loudness_verify.py` | `edit-and-assemble`、`sound-design` |
| 4 审片 | `review/self-screening.md`、`quality-scorecard.md`、`independent-review.md`、`cold-audience/*.md`、`defects.md` | `review-memo.md`、`cold-audience-sheet.md`、`defect-ticket.md` | R-CUT-16 – R-CUT-22；L1/L2 | `screening-review`、`cold-audience-test` |
| 5 发布 | `publish-kit.md`、`post-release-notes.md` | `publish-kit.md` | R-PUB-01 – R-PUB-25 | `publish-prep` |

总产物：`final-report.md`（模板 [`70-playbooks/templates/final-report.md`](../../70-playbooks/templates/final-report.md)），第一节是交付声明。

## 步骤
1. **立项定位**：建 `season-01/epNN/` 目录（英文 kebab-case，E3-1 中文路径会吞输出〔委托方实证·E3-1〕）；写 `final-report.md` 骨架，第一行先写"当前阶段：0"。验：目录名无中文。
2. **阶段 0 开发**：按 `season-bible.md` 模板交齐世界规则、角色表、伏笔账本、episode-map（每集集末问句 + 卡点类型）、≥3 部对标拆解。验：R-SEA-01、R-SEA-02、R-SEA-06、R-SCR-20。**人类拍板点①**：只给人类看季结构、题材、对标三件，附一句话推荐。
3. **阶段 1 预制作（病灶最多的阶段）**：依序调度 [`script-doctor`](../script-doctor/SKILL.md) → [`visual-bible`](../visual-bible/SKILL.md) → [`casting-and-canon`](../casting-and-canon/SKILL.md) → [`asset-boards`](../asset-boards/SKILL.md) → [`storyboard-long-take`](../storyboard-long-take/SKILL.md) ⇄ [`action-choreography`](../action-choreography/SKILL.md) → `sound-design`（声音蓝图）。每个子技能交出产物后立刻跑其 `[自动]` 条目：
   - `python3 50-rubrics/scripts/dialogue_capacity.py --storyboard season-01/ep03/storyboard.md`（0 error，warn 已处置，R-SB-14 – R-SB-16）
   - `python3 50-rubrics/scripts/segment_rhythm.py season-01/ep03/storyboard.md`（0 error，R-SB-01 – R-SB-03、R-SB-06、R-SB-08）
4. **animatic 闸门**：用冻结关键帧或占位图按分镜时长排幻灯式粗剪，配临时对白（按 ≈4.1 字/秒规划语速占位，R3）与节拍标记，自己连续看一遍，记"第一次困惑时间点"（R-SB-23）。**人类拍板点②**：给 animatic + 分镜表 + 对白容量报告 + 动作设计。禁止：R-SB 任一 `[自动]` 条目未过的镜进入 prepare。
5. **阶段 2 制作**：每镜走 prepare → confirm → run 三步闸门〔委托方实证·P6、M9〕，不裸跑。顺序固定：关键帧过 R-KF（`qc/<SHOT>.md` 结论"通过"，R-KF-19）→ 才写视频提示词 → `prompt_lint.py` + `direction_audit.py` + `slot_order_check.py` + `h3_frame_grid.py --check` 全 0 error → 才生成 → `shot-qc` 出 `qc/<SHOT>.md`。
6. **阶段 3 后期**：`edit-and-assemble` 交 `edit-list.md`、`final.mp4`；跑 `python3 50-rubrics/scripts/asset_exists.py season-01/ --stale-token ep02` 与 `python3 50-rubrics/scripts/loudness_verify.py final/ep03.mp4 --min 90 --max 110`（`--min/--max` 取季圣经，R-CUT-06）；汇总成 `review/l0-report.json`（R-CUT-15）。
7. **阶段 4 审片（禁止跳过）**：先写 `review/self-screening.md`（打开任何制作文档之前，R-CUT-17）→ Q1–Q8 评分卡 → 隔离会话独立评审（R-CUT-18）→ ≥3 份冷观众记录（R-CUT-19）。问题一律写成缺陷单（`defect-ticket.md` 模板），进入步骤 8。**人类拍板点③**：人类看到的必须是已过三轮外部视角的成片 + 审片包。
8. **病灶路由（每条缺陷单必做）**：按下表把缺陷送回**产生它的阶段**，在缺陷单写"看见于 / 病灶阶段 / 回到哪里修 / 下游重跑范围"。修完后从病灶阶段起**向下游重跑全部闸门**，不得只重出单镜。

| 看见的症状 | 病灶阶段 → 回哪修 | 禁止 | 溯源 |
|---|---|---|---|
| 片段式、剧情跳跃 | 1 分镜：重做段/拍结构 | 剪辑里调转场 | A1 |
| 打斗缺席 / 慢镜 | 1 动作设计：战术链 + 交手回合 | 提示词加 "epic fight" | A2, A3 |
| 运镜耿直 | 1 分镜：重写运镜因果 | 堆 primitives | A4 |
| 人物乱跑 | 1 分镜 + 2 起始帧：单轴定侧、重出起始帧 | 视频提示词多写方位词 | A5 |
| 脸漂移 | 1 锚点卡/板图 + 2 参考链 | 只换 seed | B1 |
| 装饰物/文字被加 | 2 提示词 + 验收 | 写 negative_prompt | C1, D1 |
| 对白缺句 | 1 剧本/分镜：核容量 | 换 seed | D3 |
| 符号画错 | 1 锚点卡：对抗约束 | 重复"正确描述" | D4 |
| 纯色/文字卡污染 | 3 后期：本地生成 + 叠层 | 继续让生成器出 | D2 |
| 技术全绿但人类说不行 | 4 审片缺席：补审片 | 再加技术指标 | F1, F2 |
| 每轮修一点修不完 | 4 审片：Q1–Q8 全量自查 | 只修最新一条 | F3 |
| 看不懂 / 没人追 | 0 开发 + 1 剧本：钩子、首反转、集末悬念 | 剪辑里加字卡解释 | GAP-1 |

9. **人类反馈翻译**：收到"没有运镜""打斗逻辑""不电影"一类反馈，先按 [`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md) §12 映射到 Q 维度，再做 §11 全维度自查（不只修被点名的那条，F3），然后才进步骤 8。
10. **交付声明**：按 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §4 写 `final-report.md` 第一节：达到级别、各级证据路径、未验证项（R-CUT-16）。只有 L0 证据时只能写"技术合格（L0），观感未验证"，禁止"达标 / 可发布 / 质量通过"〔委托方实证·F1、F2〕。L2 还要求 R-CUT-20（Q1–Q8 每维 ≥2）与 R-CUT-21（R-PUB 合规行全真）。
11. **阶段 5 发布**：`publish-prep` 交 `publish-kit.md`；合规 R-PUB-01 – R-PUB-16 每行填"已确认/未确认 + 确认人 + 日期"（R-PUB-16）。**人类拍板点④**：是否发布。H3 地域许可、MiniMax 商用授权、Qwen-Image 商用许可（R-PUB-09 – R-PUB-11）由人类拍板，agent 不得自行判"可商用"〔外部调研·S-H3-14、S-COMFY-01〕。

## 判据
- 阶段闸门：R-SEA-01、R-SEA-02（0）；R-SB-23（animatic）；R-KF-19（关键帧→视频的放行）；R-CUT-15（L0 报告）；R-CUT-16（交付声明）；R-CUT-17、R-CUT-18、R-CUT-19、R-CUT-20、R-CUT-21（审片与 L1/L2）；R-PUB-16（发布合规表）。
- 全片维度：Q1–Q8 全部；声明 L2 时任何阻断缺陷（quality-model §9）存在即不得声明。
- 若某阶段产物缺失，则该阶段闸门判"不通过"，不允许用下游产物"倒推补写"上游文档（E4 提示词≠产出的来源之一）。

## 失败模式
- **技术全绿就交付** → [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md)：本技能防线 = 步骤 7 审片不可跳过 + 步骤 10 交付声明分级。
- **拿代理指标当质量**（运镜占比、均长、通过率）→ [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)：防线 = L0 证据只能写"观感未验证"。
- **每轮只修人类点名的那一条** → [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)：防线 = 步骤 8 病灶路由 + 步骤 9 全维度自查 + 从病灶阶段向下游重跑。
- **装了技能但能力没变** → [`60-casebook/cards/F4-skills-not-ability.md`](../../60-casebook/cards/F4-skills-not-ability.md)：防线 = 每阶段以产物和闸门结果放行，而不是"已装载某技能"。
- **改集号后路径残留、素材失效** → [`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md)：防线 = 步骤 6 `asset_exists.py --stale-token`，R-SEA-18。
- **提示词与产出不一致还被采用** → [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)：防线 = 回写纪律（R-VP-25、R-VID-18）作为阶段 2 放行条件。
- **碎镜在剪辑里修** → [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)：防线 = 路由表把 A1 送回阶段 1 分镜。

## 关联
- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)。
- 流程定义：[`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md)；"够好了"：[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)；证据冲突立场：[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md)。
- 相邻技能：全部 16 个技能由本技能调度；最常交接的是 [`script-doctor`](../script-doctor/SKILL.md)、[`storyboard-long-take`](../storyboard-long-take/SKILL.md)、`screening-review`、`multi-episode-arc`。
- 找错题：DR-16（自证循环）、DR-17（代理指标）、DR-18（补丁式迭代）、DR-20（综合复盘）、DR-22（病灶路由）——见 [`60-casebook/drills/README.md`](../../60-casebook/drills/README.md)。
- → 行为改变：下次收到"这集不行"时，先写缺陷单并标病灶阶段，再动手；禁止直接打开 `video-prompts.md` 改词。
