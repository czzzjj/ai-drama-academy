---
name: cold-audience-test
description: 组织并记录冷观众测试，为一集取得 L1"看得懂"证据：招募≥3 名未接触任何制作材料的观众（或在报告中注明降级置信度的 agent 替身），单次连续观看后让其复述主因果链、标记断点（看不懂/出戏/拖）、说出想在下一集知道的问题，按记录表留档，按阈值判定，并把每个断点按病灶阶段路由成缺陷单。Use when an episode needs L1 evidence, before human decision point ③, after a rewrite at script/storyboard level, or when the team cannot tell whether the story reads. 触发词：冷观众、陌生观众、试映、复述因果、断点、看不懂、下一集意愿、替身测试、cold audience, test screening, retell, comprehension test, breakpoint, next-episode intent, stand-in viewer。不负责 8 维评分与独立评审（screening-review）、修复缺陷（回病灶阶段技能）、发布后数据（publish-prep）。
---
# 冷观众测试（cold-audience-test）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。委托方从未做过冷观众测试（GAP-2），本技能方法为〔外部调研〕，阈值为〔学院推断，待生产验证〕——每次测试结果都要回写，用来校准阈值。协议全文见 [`90-curriculum/cold-audience-protocol.md`](../../90-curriculum/cold-audience-protocol.md)。

## 何时用 / 何时不用

- **用**：screening-review 自评完成、交人类拍板点③之前（声明 L1 的必要证据）；改动触及剧本或分镜层之后（上一轮断点不得在原位置复现）；季内只看本集的可读性检查（R-SEA-20）。
- **不用**：替代 L0 技术 verify 或 shot-qc——冷观众不负责找穿帮细节。
- **不用**：让看过剧本、分镜、提示词的任何人或会话当冷观众——包括你自己和做过独立评审的会话。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| `final/epNN.mp4`（L0 已过） | `review/cold-audience/viewer-01.md` … 每人一份记录表 | [`70-playbooks/templates/cold-audience-sheet.md`](../../70-playbooks/templates/cold-audience-sheet.md) |
| 各记录表 | `review/cold-audience/summary.md`：复述正确率、断点聚类、下一集问题、判定 | 同上 |
| 断点聚类 | 缺陷单（按病灶阶段） | [`70-playbooks/templates/defect-ticket.md`](../../70-playbooks/templates/defect-ticket.md) |

记录表字段（每人）：`观众编号 | 类型(人类/替身) | 背景(是否看过前集) | 观看方式 | 复述原文(逐字) | 复述判定 | 断点[时间码+原话+类型] | 下一集问题(原话) | 想看下一集(是/否)`。

## 步骤

1. **招募 ≥3 名冷观众**：未读过剧本、未看过分镜 / 样片、未参与讨论；季内测试至少 1 人未看过前集。5 人可发现大部分可用性问题，3 人是最低线〔外部调研·S-CASE-14〕。人数不足时不得把阈值按比例放宽。
2. **替身（只有找不到人类时）**：另开一个从未见过任何制作文档的 agent 会话，只给成片抽帧序列（`python3 50-rubrics/scripts/contact_sheet.py final/epNN.mp4 --out-dir review/cold-audience/frames`）+ 按时间码排列的字幕 / 转写；禁止给剧本、分镜、提示词、作者说明。报告与交付声明必须写"替身测试，置信度降级"；替身结果不能用来声明 L3，也不能单独支撑人类拍板点③的"看得懂"结论。
3. **单次观看，不解释**：1× 速、不暂停、不回看、竖屏手机或 9:16 窗口；观看前只说"请像刷到一样看完"，不介绍剧情、人物、题材。主持人不在观看中回答问题；观众的疑问本身就是断点证据。
4. **立即复述因果链**：看完马上问"用几句话讲讲刚才发生了什么"，逐字记录。按四段判定：谁想要什么 → 遇到什么阻碍 → 做了什么 → 结果如何；四段都对 = 正确，缺一段 = 部分，人物或因果错 = 错误。禁止引导式追问（"你注意到他拿剑了吗？"）。〔外部调研·S-CASE-13、S-CASE-15〕
5. **断点标记**：请观众回忆或在第二遍拖进度条指出"哪里没看懂 / 出戏 / 觉得拖"，每条记时间码 + 原话 + 类型（看不懂 / 出戏 / 拖 / 不信）。第二遍只用于定位，不改第 4 步的复述判定。
6. **下一集问题**：问"你最想在下一集知道什么？想看下一集吗？"逐字记录。说不出具体问题 = 集末钩子未成立（R-PUB-22）。
7. **表演读解（关键表演镜）**：对表演卡标注的关键镜，问"这个角色此刻想要什么？"，与任务动词比对（R-PRF-10）。
8. **汇总判定**（阈值来自 definition-of-done L1 / L3）：
   - **L1 通过**：≥3 份记录中 **≥2/3 正确复述主因果链**，且**无任何断点被 ≥2 人在同一处（±3s）同时标记**。
   - **L3 加分**：≥2/3 回答想看下一集并能说出具体问题。
   - 未通过 → 不得声明 L1；交付声明写"L1 未达成 + 原因 + 断点时间码"。验：R-CUT-19、R-SEA-20、R-PUB-22。
9. **断点路由**：把断点按时间码聚类后，用 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3 判病灶阶段，开缺陷单：
   - "看不懂谁是谁 / 谁在哪" → 分镜（方位、建立镜）或锚点（区分度，R-SEA-12）；
   - "看不懂为什么" → 剧本（因果、信息释放）；
   - "拖" → 分镜（事件密度）或剪辑（CUT 长度）；
   - "出戏 / 假" → 表演、声音或镜头缺陷 → 交 shot-qc 复查。
   禁止在缺陷单里直接写"换 seed"——seed 不修理解问题。
10. **回写与复测**：缺陷修复后，换新的冷观众复测（看过上一版的人不再冷）；上一轮断点不得在原位置复现。测试结果（正确率、断点数）回写 `summary.md`，并在报告里注明阈值仍为学院推断。

## 判据

- R-CUT-19（≥3 份记录、≥2/3 复述正确、无 ≥2 人同处断点；替身注明降级）。
- R-SEA-20（只看本集的冷观众能复述本集主因果链）。
- R-PUB-22（最后 10s 抛出具体未解问题；≥2/3 冷观众能说出它）。
- R-PUB-17（开场 3s 内冲突主张可见——用"你什么时候知道这是个什么故事"提问取证）。
- R-PRF-10（读得出角色想要什么）、R-SND-07（静场处无人标"拖"）。
- 质量维度：主 **Q1 叙事与钩子**；断点类型映射 Q2（谁在哪）、Q6（拖）、Q7（谁是谁）、Q8（听不清）。3 分的"外部点名"证据来自本技能记录（quality-model §0.4）。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| 作者觉得清楚，人类看完「片段式、剧情跳跃、无法理解」 | [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md) | 步骤 4 逐字复述 + 四段判定 |
| agent 拿自己（或看过文档的会话）当观众，结论全是"看得懂" | [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md) | 步骤 1–2 冷的定义；替身隔离与降级声明 |
| 以"完播率 / 时长达标"代替"看得懂" | [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md) | L1 只认复述与断点，不认任何技术指标 |
| 断点修一个冒一个 | [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md) | 步骤 9 聚类后按阶段路由；步骤 10 换人复测 |
| 观众分不清两个角色 | [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md) | 断点"谁是谁" → 锚点区分度缺陷单 |
| 观众说"他们怎么换位置了" | [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md) | 断点"谁在哪" → 分镜 / 起始帧缺陷单，不进提示词微调 |

## 关联

- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/01-vertical-drama-physiology.md`](../../10-theory/01-vertical-drama-physiology.md)、[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)（只看本集也能懂）。
- 协议与级别：[`90-curriculum/cold-audience-protocol.md`](../../90-curriculum/cold-audience-protocol.md)、[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §2 L1/L3。
- 相邻技能：[`20-craft/screening-review/SKILL.md`](../screening-review/SKILL.md)（并行：内部 8 维 + 外部视角）、[`20-craft/production-director/SKILL.md`](../production-director/SKILL.md)（病灶路由）、[`20-craft/script-doctor/SKILL.md`](../script-doctor/SKILL.md)（理解类缺陷的主修方）、[`20-craft/multi-episode-arc/SKILL.md`](../multi-episode-arc/SKILL.md)（下一集问题 = 卡点链证据）。
- 外部来源：〔外部调研·S-CASE-13、S-CASE-14、S-CASE-15、S-CASE-19、S-CASE-20〕。
- 找错题：[`60-casebook/drills/DR-16.md`](../../60-casebook/drills/DR-16.md)、[`60-casebook/drills/DR-22.md`](../../60-casebook/drills/DR-22.md)。

## → 行为改变

- 下次要写"L1 看得懂"，先数 `review/cold-audience/` 里有几份冷观众记录；不足 3 份或全是替身，就不写 L1 或写明降级。
- 下次冷观众复述错了，先把原话逐字记下，再看它卡在因果四段的哪一段，路由到剧本或分镜，而不是重出镜头。
- 下次修完理解类缺陷，换一批没看过的人复测。
