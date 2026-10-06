---
name: script-doctor
description: 逐集剧本诊断与改写：3 秒首钩、20 秒内首个反转、≤30 秒一个情绪拐点、每场价值变化、集末具体悬念、动作行可被生成器执行、对白按 7.5 字/秒硬上限与 ≈4.1 字/秒规划语速双速核算容量，并锁定"字幕逐字取自剧本"。Use when writing or revising an episode script, before storyboarding, or when feedback says "看不懂 / 没钩子 / 节奏拖 / 台词缺句". 触发词：剧本诊断、开场钩子、首反转、集末悬念、卡点、信息密度、对白容量、语速、台词缺句、场景价值变化、script doctor, hook, cliffhanger, dialogue capacity, pacing. 不负责分镜的段/拍/镜切分（→ storyboard-long-take）、季级伏笔账本（→ multi-episode-arc）、打斗招式设计（→ action-choreography）。
---
# 剧本医生（script-doctor）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。语速双标准的裁决见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R3。

## 何时用 / 何时不用
- **必须用**：每集剧本定稿前（阶段 1 第一道闸门）；冷观众或人类反馈"看不懂 / 不想追 / 拖"；`dialogue_capacity.py` 在分镜阶段报 error 时（病灶在剧本，回这里删句或拆场）。
- **不用**：只调整镜头时长与运镜（→ [`storyboard-long-take`](../storyboard-long-take/SKILL.md)）；但若调整镜长是为了装台词，先回本技能确认台词本身是否该删。
- 判决：委托方从未测过"看得懂"〔委托方实证·GAP-2〕，剧本层的钩子/因果是 L1 的源头；在剪辑里加字卡解释是禁止的补丁（production-lifecycle 路由表）。

## 输入 → 输出
- 输入：`season-bible.md`、`episode-map.md`（本集集末问句 + 卡点类型）、`benchmarks.md`（≥3 部对标）、原著章节。
- 输出：`season-01/ep03/script.md`（模板 [`70-playbooks/templates/episode-script.md`](../../70-playbooks/templates/episode-script.md)），每场含：场号、估时、开场状态 → 收场状态、动作行（△）、对白、`[画面文字]` 标签；文末附"诊断表"：

```markdown
| 项 | 本集 | 对标 1 | 对标 2 | 对标 3 | 判定 |
|---|---|---|---|---|---|
| 首钩时间 | 00:02 剑落地 | 00:01 | 00:03 | 00:02 | ✅ |
| 首转折时间 | 00:17 | … | … | … | ✅ |
| 集末卡点类型 | 闯入：门外脚步停住 | … | … | … | ✅ |
| 主因果链 | 苏晓想救妹 → 神拦路 → 佯攻抓隙 → 斩断神臂却放出封印 | — | — | — | ✅ |
```

## 步骤
1. **先写一句主因果链**：谁想要什么 → 阻碍 → 做了什么 → 结果；四项各指向至少一场（R-SCR-07）。写不出 → 不进入下一步，回 `episode-map.md` 改梗概。
2. **首钩（0–3s 目标，5s 硬线）**：第一场第一拍必须是画面内可见事件（冲突 / 危险 / 反常画面），不是片名、风景或旁白（R-SCR-01）；去掉全部台词与字卡，只读动作行仍知道"出了什么事"（R-SCR-02）。发布侧要求开场 3s 内冲突主张可见（R-PUB-17）。
3. **首反转 ≤20s**：第一个"预期被打破"按估时落在 20s 内（R-SCR-03）；本集至少 1 次**有对手的反转**——由对立方行动造成，不是巧合或旁白宣布（R-SCR-04）。
4. **情绪拐点密度**：在估时轴上标出每个情绪拐点，相邻间隔全部 ≤30s（R-SCR-05）；超了就删场、并场或前移冲突，不靠剪辑加速。
5. **每场价值变化**：每场写"开场状态 → 收场状态"，二者必须不同（安全→危险、信任→怀疑）；写不出的场删除或并入相邻场（R-SCR-09）。
6. **信息密度与可执行性**：
   - 删去全部对白后，只读 △ 动作行仍能复述主因果链 ≥3 项（R-SCR-08）；
   - 动作行禁止未拆解评价词（史诗、震撼、华丽、电影感、氛围感、压迫感），改写成可见事件（"冲击环从接触点炸开"，R-SCR-11）〔委托方实证·M3〕；
   - 禁止生成器难执行的写法：不可见内部状态（"神色一凛"）、否定式动作（"没有接话"）——改成可见替代（"他移开视线，手指收紧"，R-SCR-12）；
   - 禁止台词直接宣告情绪（"我好生气"），除非标注为设计（R-SCR-17）；
   - 人群只写背景氛围"远处模糊的人影"，不给人群动作、道具、台词（R-SCR-19）。
7. **打斗场**：每场打斗写成 ≥3 环战术链 + ≥1 个交手回合（R-SCR-10），细节交 [`action-choreography`](../action-choreography/SKILL.md)。"含蓄处理"不是打斗的写法〔委托方实证·A2〕。
8. **精确文字外置**：字卡、UI、logo、招牌内容、纯色画面一律标 `[画面文字]` 并注明"剪辑叠层 / 本地生成"（R-SCR-13），绝不写进要送生成器的动作行〔委托方实证·D2〕。
9. **对白双速核算（R3）**——每场跑：
   `python3 50-rubrics/scripts/dialogue_capacity.py --text "<该场全部台词>" --seconds <该场估时>`
   - **7.5 字/秒 = 硬容量上限**：超过 → error，结构性缺陷，换 seed 无解〔委托方实证·D3、T-2〕；处置只能是删句、拆场、加时长。
   - **≈4.1 字/秒 = 规划语速**：超过 → warn（会赶词、没有表演呼吸）〔外部调研·S-ZEN-17〕；设计阶段按此排时长，并为每句加开口延迟与说完留白（对白镜实测比计划长 1.5–2.5s）。
   - 禁止调 `--rate` 高于 7.5 或 `--margin` 低于 1.0 来消 error（R-SB-16）。
   - 一字一顿 / 迟疑台词用 `……` 标出停顿，按 ~6.5s/句上界留时长（R-SCR-15）。
   - 旁白 VO/OS 总估时 ≤ 全集对白估时 30%（R-SCR-16）。
10. **字幕逐字原则**：剧本台词即字幕母本。分镜 `对白` 列、提示词 `<d>` 与剪辑单 `字幕` 列必须逐字等于本稿（R-CUT-11）；转写只用于定位时间与查缺句，**永不**用转写文字当字幕〔委托方实证·D5；外部调研·S-COMFY-14、S-COMFY-16〕。台词改动只在本稿改，再向下游同步（P7 双文档对账）。
11. **集末悬念**：最后 10s（估时）停在一个能写成一句问句的具体未解问题上，标注卡点类型（揭示 / 反转 / 期限 / 闯入，R-SCR-06）；与 episode-map 一致，相邻两集卡点类型不同（R-SEA-06）。冷观众验收见 R-PUB-22。
12. **对标并排**：首钩时间、首转折时间、集末卡点类型与 ≥3 部对标同项并排，本集三项不晚于对标中位（R-SCR-20）。
13. **交接**：把定稿 `script.md` 交 [`storyboard-long-take`](../storyboard-long-take/SKILL.md)；分镜阶段再跑一次 `dialogue_capacity.py --storyboard`（R-SB-14），那时的 error 回到本技能步骤 9 处置。

## 判据
- 钩子与结构：R-SCR-01、R-SCR-02、R-SCR-03、R-SCR-04、R-SCR-05、R-SCR-06、R-SCR-07、R-SCR-09、R-SCR-20、R-PUB-17、R-PUB-22。
- 可执行性：R-SCR-08、R-SCR-10、R-SCR-11、R-SCR-12、R-SCR-13、R-SCR-17、R-SCR-18、R-SCR-19。
- 对白：R-SCR-14、R-SCR-15、R-SCR-16、R-SB-14、R-SB-15、R-SB-16、R-CUT-11。
- Q 维度：Q1 叙事与钩子（主）、Q6 节奏与速度、Q8 声音与对白。

## 失败模式
- **台词说不完 / 缺句，换 seed 也没用** → [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md)：防线 = 步骤 9 双速核算在剧本阶段就跑。
- **"片段式、剧情跳跃、无法理解"** → [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)：防线 = 步骤 1 主因果链 + 步骤 5 每场价值变化（因果先在剧本里连上）。
- **打斗被写成"含蓄"而缺席** → [`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)：防线 = 步骤 7 战术链 + 交手回合。
- **ASR 幻觉字被当成字幕** → [`60-casebook/cards/D5-qc-tools-lie.md`](../../60-casebook/cards/D5-qc-tools-lie.md)：防线 = 步骤 10 字幕逐字取自剧本。
- **字卡/纯色画面交生成器被污染** → [`60-casebook/cards/D2-solid-black-fails.md`](../../60-casebook/cards/D2-solid-black-fails.md)：防线 = 步骤 8 `[画面文字]` 外置。
- **技术全绿但没人看得懂** → [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md)：防线 = 步骤 2/3/11 钩子在剧本阶段就可检。

## 关联
- 理论：[`10-theory/01-vertical-drama-physiology.md`](../../10-theory/01-vertical-drama-physiology.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)、[`10-theory/13-performance-direction.md`](../../10-theory/13-performance-direction.md)。
- 相邻技能：上游 [`production-director`](../production-director/SKILL.md)、`multi-episode-arc`；下游 [`storyboard-long-take`](../storyboard-long-take/SKILL.md)、[`action-choreography`](../action-choreography/SKILL.md)、`performance-direction`、`cold-audience-test`。
- 找错题：DR-01（碎镜）、DR-02（打斗缺席）、DR-11（对白容量）、DR-13（QC 工具会骗人）。
- → 行为改变：下次写完一场戏，先跑 `dialogue_capacity.py --text`，再写下一场；禁止把"台词装不下"留给分镜或生成阶段处理。
