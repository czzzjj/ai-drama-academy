---
id: F3
title: 补丁式迭代
group: F 质量与学习论
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [screening-review, production-director, storyboard-long-take, video-prompting-h3, keyframe-freeze]
drills: [DR-18, DR-20, DR-22]
---
# F3 · 补丁式迭代

> 一句话：**一条反馈是一个样本，不是一份需求全集。** 只修被点名的那一处，同类缺陷在全片其他位置、在没被点名的维度里原封不动；而每一轮重生成还会把已经修好的维度重新掷一次骰子。修面、修病灶、全量回归，才会收敛。

## 症状（含人类主创原话，逐字引用档案）

- 打斗实验 r1→r5，每轮只修最新一条反馈，主题依次是 运镜 → 特效 → 史诗 → 空间；修好一个暴露另一个；人类主创每轮都说"仍不够"（档案转述，无「」原话）〔委托方实证·F3〕。
- r4 复审，人类主创原话：「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」〔委托方实证·A5〕。"又"字是回归的直接证据：修好过的维度在后续轮次被带坏。
- 五轮之后："质量没有质变"〔委托方实证·T-4〕。
- agent 的困惑（agent 原话，不是人类原话）："为什么每个单点反馈我都改了，整体还是'不对'？"〔委托方实证·G1〕；"为什么'特效''史诗感'这类词，我做了很多具体化努力还是不够？"〔委托方实证·G5〕
- **自检识别特征**：你的修改记录里每一轮只有一个主题；你改的永远是视频提示词；同一句话第二次出现在反馈里。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

| 被修主题（档案顺序） | 当时修在哪一层（档案可见） | 档案记录的后果 | 病灶其实在（路由表） |
|---|---|---|---|
| 运镜 | 视频提示词：套用 primitives 运镜词，统计"固定镜头=0"〔A4②、F2〕 | 「无电影级运镜」仍成立〔A4〕 | 1 分镜：运镜因果 |
| 特效 | 提示词词汇的"具体化努力"〔G5〕 | "还是不够"〔G5〕 | 写事件不写形容词〔M3〕 |
| 史诗 | 同上〔G5〕 | "还是不够"〔G5〕 | 2 起始帧：画面级由起始帧决定〔M2〕 |
| 空间（r4 复审） | — | 「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」 | 1 分镜 + 2 起始帧〔A5〕 |
| 空间（r5） | 单轴定侧 + 方位词全量审计〔A5、M4〕 | 空间维度实测达标；全片仍未到可发布〔T-4〕 | — |

- 档案只确定了 r4 = 空间复审、r5 = 单轴定侧；运镜/特效/史诗具体落在 r1–r3 的哪一轮，档案未记录，本卡不推定。
- **分母对照**：委托方事后列出的质量维度是 叙事 / 空间 / 动作 / 特效 / 美术 / 节奏 / 一致性 / 声音 / 钩子〔F3〕。五轮只碰到其中 4 个主题（运镜、特效、史诗、空间）；叙事、动作、节奏、声音、钩子在五轮里没有任何一轮被当作主题处理，而人类同期反馈里已有「几乎没有做 BOSS 打斗」〔A2〕「全是几个简单动作的慢镜头」〔A2、A3〕。
- 五轮中唯一真正收敛的一次（r5）有两个特征：改的是设计规则而不是提示词措辞；规则作用于全片（"全片单轴优先"）并配了全量审计〔A5〕。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 每轮只修最新一条反馈〔委托方实证·F3〕。
2. **反馈是抽样，不是全集**：人类看到的每个问题背后是一个完整的质量模型〔委托方实证·F3〕；人类一次只说出最刺眼的一两条〔G1 回答，见 [`00-orientation/eight-questions.md`](../../00-orientation/eight-questions.md)〕。

### 方法论原因
3. **没有质量模型 = 没有分母。** 不知道一共几维，就不知道还剩几维；每条反馈都被当成完整需求，修完它就以为"完了"。"什么算够好"没有定义〔G8〕，五轮也就没有退出条件。
4. **修在症状处，不在病灶处。** 运镜、特效、史诗三轮都在视频提示词的措辞上用力〔G5〕，而它们的病灶分别在分镜（运镜因果〔A4〕）、事件设计（M3）、起始帧（M2）。路由表见 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3："缺陷在哪里被看见 ≠ 缺陷在哪里产生"。
5. **没有回归检查。** 修运镜引入的运镜词与起始帧轴线冲突，把空间带坏〔A4②、A5①〕；r4 的"又"说明没有任何闸门在拦"已修好的维度变坏"。〔学院推断：每轮整镜重生成会把其他维度重新随机一次；验证法：保留上一轮已验收的片段作基线，与新版逐维两两比较，统计退化维度数。〕
6. **只修点，不修面。** 修被点名的镜，不在全片搜同类〔G1〕。碎镜、慢镜、打斗缺席都是全片性的〔A1、A2、A3〕，点修永远修不完。
7. **补丁叠加制造指令矛盾。** 每轮往提示词里加一句对策，旧对策不删；模型会执行写下的**所有**指令，指令打架它就乱编〔委托方实证·A5④〕。

### 外部调研补强的根因
8. **"负面补丁淹没动作"是公开记录的六类返工原因之一**〔外部调研·S-ZEN-23〕。同一来源要求每次重写或压缩提示词都填"改写前后回归表"，比对原文覆盖、镜头目的、起止时长、资产、对白，并规定指令优先级：已确认的故事事实与对白 > 镜头覆盖与时长 > 资产身份与连续性 > 视觉方向 > 模型条件 > 装饰性偏好。
9. **重抽只适用于随机失败，且有上限；同一缺陷重复出现必须改结构**（如拆镜）〔外部调研·S-ZEN-24〕。这与委托方 D3 的教训同构："换 seed 无解的问题不是随机问题"〔委托方实证·D3〕。
10. **质量天然是多层的。** 多镜头基准用 20 项指标、四层（全局 / 跨镜 / 镜内 / 参考条件）评一条片子〔外部调研·S-PIPE-11〕；一条反馈最多碰到其中一两项。
11. **一个观察者只能看到一部分问题。** 可用性测试中单个用户约发现 31% 的问题，5 人约 85%，且建议多轮小样本迭代〔外部调研·S-CASE-14〕。〔学院推断：一次看片反馈同样只覆盖缺陷的一部分；验证法：下一集让 3 名冷观众各自独立记录，统计各自报出的问题重叠率。〕
12. **无外部反馈的自我纠错可能越改越差**〔外部调研·S-CASE-24〕；可收敛的多 agent 迭代都带"批评 → 修订 → 核验"与轮数上限（上限 3 轮）〔外部调研·S-PIPE-06〕，或每阶段"生成 → 审查 → 修订"并设迭代上限〔外部调研·S-PIPE-08〕。

## 修正过程（做了什么、第几轮、结果）

1. 委托方的修正方向：建立全片质量模型（8 维），每轮迭代对全维度过关自查，而不是"打地鼠"〔委托方实证·F3〕。档案中没有执行记录。
2. 已被实测有效的"修面"样板：r5 单轴定侧——一条全片规则 + 一个全量审计（方位词 grep）+ 回到起始帧层面钉轴线 → 空间实测达标〔委托方实证·A5、M4〕。
3. 已被实测有效的"改结构"样板：D3 三个 seed 各缺不同句 → 判定为结构性缺陷 → 按台词时长重新核算，镜长 7.5s → 11s 重产才齐〔委托方实证·D3〕。
4. 学院落地（〔学院推断〕）：8 维质量模型 [`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md)；反馈处理协议写进 [`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)；病灶路由由 [`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md) 执行。验证法：下一集记录"反馈条数 → 被归并的缺陷类数 → 返工轮数"，与 r1→r5 对比。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [目视] 每条反馈在 `review/defects.md` 占一行，列齐：反馈原话 | 设计层翻译 | Q 维度 | 病灶阶段 | 全片同类搜索结果（SHOT 列表，或"已搜，无"）| 处置 | 回归结果。"全片同类搜索"为空 → 该条不得标"已修"〔F3、G1〕。
2. [自动] 每轮修改后对**全集**重跑生成前脚本并留档 `--json`：`segment_rhythm.py`、`dialogue_capacity.py`、`h3_frame_grid.py --check`、`prompt_lint.py`、`direction_audit.py`、`slot_order_check.py`；与上一轮 JSON 比较，出现上一轮没有的 error 代码 → 回归，不得提交（比较用 python/jq，无专用脚本）〔F3、A5〕→ [`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)
3. [目视] `review/quality-scorecard.md` 每轮 8 维全部重打分并附证据时间码；任一维低于上一轮 → 记为回归，修复前不得提交〔F3〕。
4. [目视] 被重生成的镜与上一轮已验收版本做两两比较（`contact_sheet.py` 并排，交换顺序各看一次），逐维写"更好 / 相同 / 更差"〔F3、F1〕。
5. [自动] `review/defects.md` 中同一症状第二次出现且处置仍为"重抽" → 不通过：必须改设计（拆镜、减拍、改起始帧、改时长）〔D3；S-ZEN-24〕。
6. [目视] 每次改写提示词附"改写前后回归表"：台词逐字、起止与时长、锚点句、镜头目的四项未丢；被新设计取代的旧补丁句已删除〔S-ZEN-23、A5④〕。
7. [冷观众] 改动涉及剧本或分镜层时，重跑冷观众测试；上一轮被标记的断点不得在原位置复现〔F1〕。

## → 行为改变（下次……）

**下次收到任何一条反馈，按以下 7 步处理；禁止跳过第 4、5、7 步直接改视频提示词。**

1. **原话入表**：反馈原话逐字写进 `review/defects.md`，不概括、不改写。
2. **翻译到设计层**：查 [`00-orientation/glossary.md`](../../00-orientation/glossary.md) B 表；有两种以上解释时，做同一段的 A/B 两个最小样请人类选〔G6〕。
3. **定维度**：归到 Q1–Q8 中的一维或多维（[`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md)）。
4. **全片搜同类**：在全集所有镜、所有已出片中搜同类缺陷，列出 SHOT 编号。被点名的镜只是样本。
5. **定病灶阶段并在那里修**：按 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3 路由；能在分镜、起始帧、剧本修的，禁止在视频提示词里加词。
6. **选处置**：只出现一次、换 seed 有望解决 → 重抽，同一镜最多 2 次；重复出现或换 seed 无解 → 判结构性缺陷，改设计〔D3〕。
7. **全量回归**：判据 2–4 全跑；改动触及剧本/分镜时加跑判据 7。

**每轮交付前**，额外做三件事：
- 8 维全部重打分，**没被反馈点名的维度与被点名的维度同等对待**；
- 在交付说明里主动列出"已知未修问题"（含维度与 SHOT），不要等人类去抽样；
- 同一维度连续 2 轮无改善 → 停止在该层打补丁，上溯一个阶段（提示词 → 起始帧 → 分镜 → 剧本），或在人类拍板点提出结构性改法。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 通用于任何"人类给反馈、agent 迭代"的创作任务（剧本、分镜、剪辑、封面都一样）。
- ★ 换模型不会消除它：生成器越随机，整镜重生成带来的回归越多，全量回归越必要。
- ☆ 判据 2 的脚本清单是本管线专有的；换管线时保留"全集重跑 + 与上一轮比对新 error"的结构。
- ☆ "重抽最多 2 次"是〔学院推断〕的起始值；验证法：统计下一集重抽第 3 次以上的镜中，最终靠改设计解决的比例，比例高则把上限降到 1。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)（反馈翻译协议、8 维自查）、[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（病灶路由、阶段闸门）、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（改写回归表）。
- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)（写事件不写形容词）、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)。
- 判据：[`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md)、[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)。
- 流程：[`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md)、[`00-orientation/eight-questions.md`](../../00-orientation/eight-questions.md)（G1、G5、G7、G8）。
- 找错题：[`60-casebook/drills/DR-18.md`](../drills/DR-18.md)（补丁迭代）、[`60-casebook/drills/DR-20.md`](../drills/DR-20.md)（综合复盘）、[`60-casebook/drills/DR-22.md`](../drills/DR-22.md)（病灶路由）。
- 相邻案例：[`60-casebook/cards/A5-spatial-chaos.md`](A5-spatial-chaos.md)（"又"的现场）、[`60-casebook/cards/A4-unmotivated-camera.md`](A4-unmotivated-camera.md)、[`60-casebook/cards/D3-dialogue-capacity.md`](D3-dialogue-capacity.md)（随机 vs 结构性）、[`60-casebook/cards/F1-self-verification-loop.md`](F1-self-verification-loop.md)、[`60-casebook/cards/F2-proxy-metrics.md`](F2-proxy-metrics.md)。
