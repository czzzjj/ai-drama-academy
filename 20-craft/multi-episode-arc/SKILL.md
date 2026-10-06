---
name: multi-episode-arc
description: 管理一季的跨集连续性：先写季圣经（世界规则、角色表、主线支线、伏笔账本、原著取舍表）与 episode-map 交接契约，排角色弧线与集末卡点链，执行"前三集"规则，用版本化锚点卡、服装/伤势状态账本和固定音色绑定守住外观与声音连续，并在每集开工前后做季级对账。Use when starting a season, writing or adapting multiple episodes, before each episode's production, when changing costumes/injuries/voices across episodes, or when episodes feel disconnected. 触发词：季圣经、分集、多集、连续性、角色弧线、伏笔、回收、卡点、集末钩子、前三集、锚点版本、服装状态、音色绑定、season bible, episode map, series arc, foreshadowing ledger, cliffhanger chain, continuity, anchor versioning, costume state, voice binding。不负责单集内的剧本诊断（script-doctor）、单个角色锚点卡的建立（casting-and-canon）、商业模式与付费卡点的决定（人类拍板点①）。
---
# 季级连续性（multi-episode-arc）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。委托方只做过单集返工（GAP-7），季级方法为〔外部调研〕+〔学院推断〕；身份漂移与改号残留为〔委托方实证·B1、E2〕。本技能贯穿整季：开发阶段启动，每集开工前后各执行一次对账。

## 何时用 / 何时不用

- **用**：开发阶段（季结构由人类拍板点①确认后）写季圣经；每集进入预制作前做"继承检查"；每集交付后做"季级对账"；任何外观、伤势、服装、音色的跨集变化。
- **不用**：单集内部的钩子、节奏、对白容量——那是 script-doctor。
- **不用**：自行决定付费模式、门槛集、集数——商业模式由人类定，本技能只执行（T14.8）。
- **警告**：不要拿短季、单元剧的成功证明季播追更可行（T14.12）〔外部调研·S-CASE-12〕。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| 原著 / 题材、人类拍板点①的季结构与商业模式 | `season-bible.md`（五节）| [`70-playbooks/templates/season-bible.md`](../../70-playbooks/templates/season-bible.md) |
| 季圣经 | `episode-map.md`：每集一行交接契约 | 同上 |
| casting-and-canon 的锚点卡 | 锚点版本登记 + 变体卡（服装 / 伤势 / 时段） | [`70-playbooks/templates/anchor-card.md`](../../70-playbooks/templates/anchor-card.md) |
| 各集成片与 QC | 状态账本、伏笔账本更新；季级对账记录 | season-bible.md |
| 单集剧本 | 继承检查后的 `episode-script.md` | [`70-playbooks/templates/episode-script.md`](../../70-playbooks/templates/episode-script.md) |

## 步骤

1. **季圣经五节**：世界规则（能力 / 代价 / 禁忌）、角色表（含"音色"列、区分特征列）、主线与支线、伏笔账本、原著取舍表。改编作品的原著取舍表登记每个被砍情节，并确认被砍情节没有被后续集引用。验：R-SEA-01、R-SEA-19。〔外部调研·S-ZEN-03、S-ZEN-05〕
2. **季引擎四件事**：主角核心欲望、可反复出现的阻碍、倒计时、观众心里悬着的问题；每集至少一个带价值的状态转变（T14.2）。写在季圣经首段，作为每集剧本诊断的上位约束。
3. **episode-map 交接契约**：每集一行：一句话梗概 + 进入状态 + 当集追求 + 阻力 + 方向性转折 + 结果 + 信息释放 + 出去的压力 + 下一集必须继承的事实 + 集末问句 + 卡点类型。验：R-SEA-02。
4. **角色弧线表**：每个主要角色：季初状态 → 每集变化 → 季末状态；每集至少推进一个主要角色一步，主角不得连续 3 集不动。验：R-SEA-03。
5. **伏笔账本**：一条一行：埋设（集 / 镜）→ 计划回收集 → 实际回收（集 / 镜）→ 状态（未回收 / 已回收 / 作废）。主角每次脱困必须指向一条更早埋设的伏笔或已建立的规则（禁止机械降神）。每集交付后更新"实际回收"列。验：R-SEA-04、R-SEA-05。
6. **卡点链**：每集停在峰值或揭晓前一秒；类型四选一：揭示 / 反转 / 期限 / 闯入；相邻两集类型不同；同一反转机制（如"身份揭晓"）全季限次。属主声明了付费 / 门槛集时，门槛集停在揭晓前一秒，悬念只依赖观众已认识的人物与规则。验：R-SEA-06、R-SEA-07；集末 10s 问题由 cold-audience-test 取证（R-PUB-22）。
7. **前三集规则**：第 1 集内兑现第一个大回报（观众亲眼看到主角核心能力或核心冲突），首钩 ≤5 秒；第 2、3 集各升级一次阻碍并保持同一个悬置问题。每集开头复现上一集最后一拍，让只看本集的观众接得上。验：R-SEA-08、R-SEA-09、R-SEA-20。
8. **锚点版本化**：锚点句 EN 全季逐字一致，登记版本号（`CHR-SUXIAO v1`）；任何外观变化（服装、伤势、时段、天气）登记为变体卡，写明生效集范围与回到基线的条件；禁止在某集提示词里临时改锚点句。每集开工前比对：`grep -F` 本集 `anchors.md` 每条锚点句与季圣经登记版本，逐字相同；再跑 `python3 50-rubrics/scripts/prompt_lint.py video-prompts.md --anchors anchors.md --storyboard storyboard.md`（`VP-anchor`）。验：R-SEA-10。〔委托方实证·B1、P1〕
9. **状态账本**：登记伤痕、服装破损、道具持有与位置、关系状态；本集起始状态 = 上集结束状态 + 账本中登记的时间跳变。每集至少 1 个主角正脸镜与板图逐特征比对（shot-qc 步骤 3）。验：R-SEA-11、R-SEA-15。
10. **区分度与音色绑定**：主要角色两两在脸型 / 发型 / 体型 / 服装主色中至少有可见差异（平台已把高频 AI 脸列为治理对象）；每个有台词角色绑定固定音色来源（参考音频或外配音色 ID）并写进角色表；同场两个同性别说话人盲听各 3 句能区分，否则改外配。验：R-SEA-12、R-SEA-13、R-SEA-14。〔外部调研·S-ZEN-17、S-PLAT-07〕
11. **色彩与光态跨集一致**：每个场景的主色与光态登记在色彩剧本（visual-bible 产出），跨集回到同一场景时逐项比对。验：R-SEA-16。
12. **规格与改号**：每集成片时长在季规格内（委托方现规格 90–110s，`loudness_verify.py --min 90 --max 110`）；整季改集号 / 镜号走 edit-and-assemble 步骤 10（`asset_exists.py --rename` 预演 → `--apply` → 全量复查 → 重渲）。验：R-SEA-17、R-SEA-18。〔委托方实证·E2〕
13. **每集交付后季级对账**：更新伏笔账本、状态账本、弧线表、episode-map 的"实际"列；只看本集的冷观众复述结果写回 episode-map；与计划偏离的地方在下一集开发前修订季圣经（先改圣经，再改下游）。

## 判据

- 圣经与结构：R-SEA-01、R-SEA-02、R-SEA-03、R-SEA-04、R-SEA-05、R-SEA-06、R-SEA-07、R-SEA-08、R-SEA-09、R-SEA-19。
- 连续性：R-SEA-10、R-SEA-11、R-SEA-12、R-SEA-13、R-SEA-14、R-SEA-15、R-SEA-16。
- 规格与卫生：R-SEA-17、R-SEA-18；可读性：R-SEA-20、R-PUB-22。
- 质量维度：主 **Q1 叙事与钩子**（季引擎、卡点链、前三集）与 **Q7 一致性与连续性**（锚点、状态、音色）；**Q8**（音色区分）。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| 第 3 集主角脸变成另一个人 | [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md) | 步骤 8 锚点句逐字版本化 + 步骤 9 每集正脸比对 |
| 两个主要角色越来越像 | [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md) | 步骤 10 区分度四项至少一项可见差异 |
| 禁用项（宝石、铠甲）在后几集回潮 | [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md) | 禁用项随锚点卡版本走，变体卡不得丢禁用行 |
| 改集号后旧路径残留，下一集引用上一集素材 | [`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md) | 步骤 12 稳定 ID + 字节级改名流程 |
| 每集各自修补，季整体越改越散 | [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md) | 步骤 13：偏离先改季圣经，再改下游 |
| 单集看不懂前情 | [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md) | 步骤 7 开头复现上集最后一拍；R-SEA-20 冷观众取证 |

## 关联

- 理论：[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)（T14.1–T14.12）、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)（商业模式变量）、[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)（T11.10 音色）。
- 相邻技能：[`20-craft/production-director/SKILL.md`](../production-director/SKILL.md)（拍板点①）、[`20-craft/casting-and-canon/SKILL.md`](../casting-and-canon/SKILL.md)（锚点卡源头）、[`20-craft/script-doctor/SKILL.md`](../script-doctor/SKILL.md)（单集执行）、[`20-craft/visual-bible/SKILL.md`](../visual-bible/SKILL.md)（色彩剧本）、[`20-craft/sound-design/SKILL.md`](../sound-design/SKILL.md)（音色绑定）、[`20-craft/cold-audience-test/SKILL.md`](../cold-audience-test/SKILL.md)（只看本集测试）。
- 外部来源：〔外部调研·S-ZEN-03、S-ZEN-05、S-ZEN-15、S-ZEN-21、S-CASE-12〕。
- 找错题：[`60-casebook/drills/DR-06.md`](../../60-casebook/drills/DR-06.md)、[`60-casebook/drills/DR-14.md`](../../60-casebook/drills/DR-14.md)、[`60-casebook/drills/DR-20.md`](../../60-casebook/drills/DR-20.md)。
- 判据清单：[`50-rubrics/checklists/season.md`](../../50-rubrics/checklists/season.md)。

## → 行为改变

- 下次接到多集项目，先写季圣经与 episode-map，再写第 1 集剧本；没有伏笔账本不开第 2 集。
- 下次任何一集要改角色外观，先建变体卡登记生效集范围，禁止在提示词里临时改锚点句。
- 下次每集开工前，先逐字比对锚点句与季圣经版本、读状态账本，再写分镜。
- 下次发现剧情与计划偏离，先改季圣经，再改下游各集。
