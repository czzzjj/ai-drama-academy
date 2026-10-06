---
name: screening-review
description: 对一集成片做审片：先在不看任何制作文档的前提下自我放映并记下第一次困惑时间码，再按 Q1–Q8 逐段打分（每个分数挂时间码与证据），把任何反馈按"症状→维度→设计层→两个 A/B 假设"翻译并在全片搜同类，再开隔离会话做盲评对抗评审（抵消 LLM 评审偏差），最后写审片备忘与交付声明。Use when an episode is assembled, after any human/cold-audience feedback, before claiming L1/L2, or when tempted to declare a cut finished. 触发词：审片、自我放映、全片自查、8维评分、质量评分卡、独立评审、对抗评审、盲评、反馈翻译、交付声明、仍不够、screening, self-review, quality scorecard, independent review, adversarial review, LLM-as-judge bias, feedback triage, delivery declaration。不负责找陌生观众（cold-audience-test）、单镜缺陷取证（shot-qc）、修复本身（回到病灶阶段的对应技能）。
---
# 审片评审（screening-review）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。评分锚点见 [`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md)，级别见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)。本技能回答委托方最痛的三案：自证循环（F1）、代理指标（F2）、补丁式迭代（F3）〔委托方实证〕。

## 何时用 / 何时不用

- **用**：edit-and-assemble 产出 L0 成片后、交人类拍板点③之前；收到任何反馈（人类、冷观众、独立评审）后；返工后复评。
- **用**：人类只说"仍不够 / 还是不行"——直接走步骤 6 的最低分优先，不猜。
- **不用**：L0 未过（响度、画幅、素材缺失）——先回 edit-and-assemble；审片不替技术 verify。
- **不用**：作为"冷观众"——你看过制作文档，永远不是冷观众；冷观众由 cold-audience-test 执行。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| `final/epNN.mp4`（只开成片） | `review/self-screening.md`（观看方式、第一次困惑时间码、出戏点） | [`70-playbooks/templates/review-memo.md`](../../70-playbooks/templates/review-memo.md) |
| 成片 + 抽帧 + 转写 | `review/quality-scorecard.md`（Q1–Q8 × 段，分数 + 时间码 + 证据） | quality-model §10 |
| 反馈原话 | `review/defects.md`（逐字一行）+ 缺陷单 | [`70-playbooks/templates/defect-ticket.md`](../../70-playbooks/templates/defect-ticket.md) |
| 隔离会话产出 | `review/independent-review.md` | review-memo.md |
| 以上全部 | `final-report.md` 第一节交付声明 | [`70-playbooks/templates/final-report.md`](../../70-playbooks/templates/final-report.md) |

## 步骤

1. **自我放映（先于一切文档）**：在打开剧本、分镜、提示词之前，1× 速、不暂停、只开成片看一遍；再关声音看一遍。立即写 `review/self-screening.md`：观看方式、**第一次困惑的时间码**（没有写"无"）、每个出戏点（时间码 + 一句症状）、能否用一句话复述主因果链（谁想要什么 → 阻碍 → 做了什么 → 结果）。悬念 ≠ 困惑：困惑点要么修，要么写明为什么是设计。验：R-CUT-17。
2. **逐段 8 维打分**：按 SEQ 逐段对 Q1 叙事与钩子、Q2 空间与调度、Q3 动作与物理、Q4 特效与事件、Q5 美术与密度、Q6 节奏与速度、Q7 一致性与连续性、Q8 声音与对白 打 0–3；**先写时间码与证据文件，再写分数**，写不出证据记 0。维度分 = 最差段的分（短板原则）。3 分必须有外部点名证据（冷观众或独立评审主动提到），否则记 2。证据引用的帧拼图用 `python3 50-rubrics/scripts/contact_sheet.py final/epNN.mp4 --out-dir review/frames` 产出。验：R-CUT-20、R-CUT-22。
3. **阻断缺陷表**：逐行填 definition-of-done §3 的 9 类阻断（复述失败、漂移、空间混乱、无交手、自加文字、缺句、克隆脸、禁用项、缺 AIGC 标识）："无"或"已修复 + 证据"。任何一行存在 → 不得声明 L2。
4. **技术指标只占一列**：`review/l0-report.json` 全绿只能在评分卡"阻断"列写"无技术原因阻断"，禁止据此给任何维度 ≥2。〔委托方实证·F2〕
5. **反馈翻译协议**（收到任何一条反馈都走）：
   - ① 原话逐字写进 `review/defects.md`；
   - ② **症状 → 维度**：用 quality-model §12 映射表归主维度 + 次维度（「无电影级运镜」→ Q2/Q6，不是"运镜数量"）；
   - ③ **维度 → 设计层**：判定病灶在剧本 / 分镜 / 起始帧 / 提示词 / 生成 / 剪辑 / 声音哪一层（[`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3）；
   - ④ **两个 A/B 假设**：写出两种设计层解释（例："打斗逻辑"= A 交手回合缺席 / B 战术链因果不清），对同一段各做一版最小样，交人类选，结果写进记忆；
   - ⑤ **全片同类搜索**：在全片所有段搜同类缺陷（跑对应脚本 + 看全部同类段接触表），写镜号列表或"已搜，无"；为空不得标"已修"。
   验：quality-model §11 第 1–4 步；找错题 DR-21、DR-22。〔委托方实证·F3、A2、A4〕
6. **最低分优先**：人类只说"仍不够"→ 评分卡最低分维度为本轮主修；多维并列最低 → 先修上游（Q1 → Q2/Q3 → Q6 → 其他）。修复回到病灶阶段（不是换 seed），修后重跑全集 `[自动]` 链（生成前 6 + 出片后 4 + 成片 2 个脚本，`--json` 与上一轮对比，新出现的 error 代码 = 回归），并 **8 维全部重打分**，任一维低于上轮 = 回归，不得提交。
7. **独立对抗评审（隔离会话）**：新开一个会话（不是本会话的子思路），只给：成片（或抽帧序列 + 转写）、quality-model、阶段清单。**不给**：生成提示词、修改轮次、指标面板、作者的通过理由、缺陷单。评审首行列出输入清单并声明"未见提示词 / 轮次 / 指标 / 作者理由"。验：R-CUT-18。偏差对抗〔外部调研·S-CASE-21、S-CASE-22、S-CASE-23、S-CASE-25、S-CASE-27〕：
   - **自偏好**：评审模型不得与生成文本 / 提示词作者同一会话；能换模型就换模型。
   - **位置偏差**：两版比较时交换顺序各评一次，不一致记"无差异"。
   - **冗长偏差**：要求评审先列时间码证据再给分，篇幅不计分。
   - **绝对分不可靠**：跨轮比较与 3 分判定一律用两两对照（"本轮 vs 上轮，哪版 Q2 更好，指出时间码"）。
   - **对抗指令**：明确要求评审"找出至少 3 处会让观众出戏的地方，没有就证明"。
   - **自我纠错无效**：同一会话自评自改不算复评〔外部调研·S-CASE-24〕。
8. **取低分**：自评与独立评审不一致的维度取低分；评审提出的"阻断"级意见必须修复并再次隔离复评。
9. **写审片备忘与交付声明**：`final-report.md` 第一节 = 交付声明：达到级别（L0 / L1 / L2）、每级证据路径、未验证项、Q1–Q8 本轮 / 上轮分数与变化。只有 L0 → 写"技术合格（L0），观感未验证"；L1 需 cold-audience-test 证据（R-CUT-19）；L2 需每维 ≥2 + 无阻断 + 独立评审通过 + 合规（R-CUT-21）。提交说明写分数变化，禁止写"已按意见修改 X"。验：R-CUT-16。
10. **回流**：本轮人类指出、而自查没先发现的问题 → 在对应阶段清单提议新增一条 R-xxx（溯源写对应案例编号），并写成找错题素材（quality-model §11 第 10 步）。

## 判据

- 审片包：R-CUT-15（L0 报告）、R-CUT-16（交付声明分级）、R-CUT-17（自我放映先于文档）、R-CUT-18（隔离会话声明）、R-CUT-19（L1 冷观众）、R-CUT-20（Q1–Q8 每维 ≥2 且挂时间码）、R-CUT-21（L2 合规）、R-CUT-22（证据文件存在）。
- 质量维度：Q1–Q8 全部；Q1 是 L2 / L3 的必要维度；Q2 与 Q7 是独立闸门，不得以"情绪对了"放过（R7）。
- 外部视角：R-PRF-10（读得出角色想要什么）。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| agent 自写自验，报告"全部通过"，人类一看就打回 | [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md) | 步骤 1 先放映后读文档；步骤 7 隔离会话；取低分 |
| 运镜数量、PSNR、响度全绿当"质量" | [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md) | 步骤 4：技术只进"阻断"列；分数必须挂观看证据 |
| r1→r5 每轮只修最新一条，修好一个暴露另一个 | [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md) | 步骤 5⑤ 全片同类搜索 + 步骤 6 8 维重打分与回归判定 |
| 装了技能、背得出规则，片子仍不好 | [`60-casebook/cards/F4-skills-not-ability.md`](../../60-casebook/cards/F4-skills-not-ability.md) | 评分只认时间码证据与外部点名，不认"已遵循技能" |
| 「片段式、剧情跳跃、无法理解」 | [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md) | 步骤 1 第一次困惑时间码 + 一句话复述因果链 |
| 「无电影级运镜」被理解成"加运镜数量" | [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md) | 步骤 5② 归 Q2/Q6 + ④ 两个设计层假设 A/B |
| 空间乱被"情绪很燃"抵消 | [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md) | Q2 独立闸门；阻断表逐行 |

## 关联

- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/01-vertical-drama-physiology.md`](../../10-theory/01-vertical-drama-physiology.md)。
- 评分与级别：[`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md) §0、§9–§12；[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)。
- 相邻技能：[`20-craft/edit-and-assemble/SKILL.md`](../edit-and-assemble/SKILL.md)（上游 L0）、[`20-craft/cold-audience-test/SKILL.md`](../cold-audience-test/SKILL.md)（L1 外部视角）、[`20-craft/production-director/SKILL.md`](../production-director/SKILL.md)（病灶路由与拍板点③）、[`20-craft/publish-prep/SKILL.md`](../publish-prep/SKILL.md)（L2 合规）。
- 找错题：[`60-casebook/drills/DR-16.md`](../../60-casebook/drills/DR-16.md)、[`60-casebook/drills/DR-17.md`](../../60-casebook/drills/DR-17.md)、[`60-casebook/drills/DR-18.md`](../../60-casebook/drills/DR-18.md)、[`60-casebook/drills/DR-19.md`](../../60-casebook/drills/DR-19.md)、[`60-casebook/drills/DR-20.md`](../../60-casebook/drills/DR-20.md)、[`60-casebook/drills/DR-21.md`](../../60-casebook/drills/DR-21.md)、[`60-casebook/drills/DR-22.md`](../../60-casebook/drills/DR-22.md)。
- 判据清单：[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)（R-CUT-15–22）。

## → 行为改变

- 下次成片出来，先关掉所有文档放映一遍写第一次困惑时间码，再打开任何制作文档。
- 下次收到反馈，先逐字记下、归维度、写两个设计层假设，再全片搜同类；禁止直接打开被点名那一镜的提示词。
- 下次想写"已完成 / 达标"，先确认手上有独立会话的评审文件与冷观众记录，没有就只写 L0。
- 下次评审自己的片子，换会话、隐藏提示词与轮次、交换顺序比对，取低分。
