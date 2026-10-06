---
id: F1
title: 自证循环
group: F 质量与学习论
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [screening-review, cold-audience-test, production-director, shot-qc]
drills: [DR-16, DR-20]
---
# F1 · 自证循环

> 一句话：**同一个会话写提示词、选 seed、写验收、下结论，它的盲区是同一个盲区。** 自己验自己，验出来的永远是"我做了我说要做的事"，验不出"观众看懂了"。外部视角不是锦上添花，它是唯一能看见盲区的传感器。

## 症状（含人类主创原话，逐字引用档案）

- agent 自己的验收全绿：渲染 rc=0、全镜采用、运镜统计达标、响度达标〔委托方实证·F1〕；工程侧 check/render/verify 全绿、-16 LUFS、无坏帧、无烧录字幕、字幕逐字对账、成片报告齐备〔委托方实证·T-4〕。
- 同一时期人类主创看片的原话（逐字）：
  - 「片段式、剧情跳跃、无法理解」〔委托方实证·A1〕
  - 「无电影级运镜」〔委托方实证·A4〕
  - 「几乎没有做 BOSS 打斗」〔委托方实证·A2〕
  - 「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」〔委托方实证·A5〕
- 档案转述（无「」原话）：人类主创每次看片都说"不达标"〔委托方实证·F1〕；连续打回多轮，至今未到"可发布"线〔委托方实证·T-4〕。
- agent 自己的困惑（agent 原话，不是人类原话）："为什么每次都要人类指出问题？我怎样才能自己先发现？"〔委托方实证·G4〕；连"为什么一直达不到要求"也回答不了〔委托方实证·T-4〕。
- **自检识别特征**：报告里写着"通过/达标"，而支撑它的证据全是脚本输出；第一个说"看不懂"的永远是人类。出现这两条，就是自证循环。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

| agent 的"全绿"项 | 谁定义 / 谁执行 | 实际证明了什么 | 同期人类看到的 |
|---|---|---|---|
| 渲染 rc=0、verify 全绿、无坏帧 | agent / agent | 文件能播、没坏 | 「片段式、剧情跳跃、无法理解」（29 镜、均长 2.96s〔A1〕） |
| 全镜采用 | agent 选 seed / agent 验收 | 没有一镜被自己拒掉 | — |
| 运镜统计达标（固定镜头=0） | agent 从"无运镜"反馈翻译出的指标 / agent | 每镜相机都在动 | 「无电影级运镜」〔A4〕 |
| 响度 -16 LUFS | agent / agent | 音量合规 | 声音只有对白+基础拟音+配乐〔GAP-3〕 |
| 字幕逐字对账、无烧录字幕 | agent / agent | 字与声一致、生成器没加字 | — |

- 执行结构：前三集首轮起〔A1〕，到 r1→r5 打斗实验〔F3〕，全部由同一个 agentos 生成、验收、出报告〔F1〕。审片阶段（自我放映 / 独立评审 / 冷观众）在档案中**没有任何一次执行记录**；冷观众测试是明确空白〔委托方实证·GAP-2〕。
- 资产层的同构小样本：同一批 BOSS 尼加狄板图，第一次验收判"通过"，复验才发现"黑臂对比不足"是硬伤〔委托方实证·C2、C1-7〕。第二遍检查拦下了错误，但当时第二遍是偶然，不是制度，且仍是同一会话。
- 把"全绿"当结论的直接代价：每一轮的起点都是"上一轮已达标"，于是人类主创成了全流程唯一的外部传感器，每个问题都要等人类看片才浮出〔G4〕。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 用自己的标准验收自己的产出 → 闭环自欺〔委托方实证·F1〕。
2. 技术闸门只覆盖"不出错"，不覆盖"出彩"〔委托方实证·F1〕。上表每一项都属于 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) 的 L0；L1（看得懂）从未测过。

### 方法论原因
3. **验收清单是生成指令的镜像。** 清单问的是"对白是否逐字""禁令句是否在""相机是否非固定"，也就是"我做了我说要做的吗"。生成时没想到的维度（因果可不可读、谁在哪、为什么切），验收时同样想不到。〔学院推断；验证法：把委托方历轮验收项逐条归到 Q1–Q8，统计落在 Q1 叙事与钩子 / Q2 空间 / Q6 节奏与速度 的条数，预测≈0。〕
4. **只做过逐镜验收，没做过一次"当观众连续看"。** 29 镜均长 2.96s〔A1〕在逐镜抽帧/PSNR/转写里每一镜都合格，碎镜症只在连续观看时才暴露。〔学院推断；验证法：对同一成片分别做逐镜 QC 与一次不暂停放映，比较两者报出的 A1 类问题数。〕
5. **审片阶段整段缺席。** 流程只有"制作"在认真运转〔G7；[`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §1〕；人类拍板点③ 看到的是未经任何外部视角的片子，所以"每次都要人类指出"是流程结构的必然，不是运气。
6. **"改完自评已修复"被计为通过。** r1→r5 每轮修完，由同一会话判断是否修好〔F3〕；「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」〔A5〕中的"又"说明修好过的维度在后续轮次退化，而自评没有拦住。
7. **报告措辞把 L0 升格成质量结论。** "全绿"在报告里等于"达标"，下一轮的起点因此是错的〔F2〕。

### 外部调研补强的根因
8. **自我偏好是结构性的。** LLM 评审给自己产出的分高于人类认为同等质量的他人产出；自我识别能力与自我偏好强度线性相关〔外部调研·S-CASE-23〕。同一会话评自己 = 系统性偏高。
9. **无外部反馈的自我纠错不可靠**，有时改完更差〔外部调研·S-CASE-24〕。
10. **评审输入会污染结论。** CALM 列出 12 类评审偏差，含 Refinement-Aware（知道答案"改过一轮"就给分更高）与 Bandwagon（"多数人认为"）〔外部调研·S-CASE-25〕。把"第 5 版""指标全绿"写进评审输入 = 预设了结论。
11. **对比有位置偏差。** 交换两个答案顺序后结论一致的比例，GPT-4 仅 65.0%〔外部调研·S-CASE-21〕；只换顺序 Vicuna-13B 就在 80 题中 66 题"赢了"ChatGPT〔外部调研·S-CASE-22〕。多模态评审在两两比较上接近人类，在绝对打分上偏离大〔外部调研·S-CASE-27〕；视频语言模型幻觉普遍，认出事实强于认出幻觉〔外部调研·S-CASE-29〕。
12. **生成器的短板恰好落在自检盲区。** 多镜头音视频基准评测 19 个模型，结论是现有系统是 "pixel renderers rather than storytellers"，导演级控制与细粒度音画同步最弱〔外部调研·S-PIPE-11〕；另一基准结论是 "visual interpolators rather than true world models"〔外部调研·S-PIPE-12〕。委托方查得最密的是像素/技术层，而生成器最常出错的是叙事/导演层：**查得最严的地方，恰是最不容易出错的地方。**
13. **工业化的自证循环长这样**：VLM 审核默认 60 分及格、重试到上限后自动选最高分继续〔外部调研·S-PIPE-15〕。这是反例，不是模板。
14. **外部视角是行业默认工序**：约 90% 大规模上映片做试映、平均 3 次〔外部调研·S-CASE-19〕；Pixar Braintrust 由同行定期给出坦率笔记，并在动画制作前用 animatic 测故事〔外部调研·S-CASE-20〕；独立审查优先交给未参与当前版本的 reviewer，自检必须如实声明是自检〔外部调研·S-ZEN-12〕。

## 修正过程（做了什么、第几轮、结果）

1. 委托方得出的是**修正方向**，没有执行记录：外部视角三件套 = 冷观众测试 + 自我放映 + 独立评审〔委托方实证·F1〕。教训原文："质量不是'符合我的清单'，是'目标观众的反应'。"〔F1〕
2. 已执行的半步：C2 之后，高风险资产加"第二遍复验"〔委托方实证·C2〕。它证明了第二双眼睛有效（黑臂弱对比被拦下），但复验者仍是同一会话。
3. 学院落地（全部是〔学院推断〕，尚未被委托方生产实证）：三件套写成 [`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md) 与 [`20-craft/cold-audience-test/SKILL.md`](../../20-craft/cold-audience-test/SKILL.md)，交付声明按 L0–L3 分级（[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)）。
4. **协议有效性的验证法（回放实验）**：把委托方前三集首轮成片（或其接触表 + 转写）交给隔离评审会话，不给任何人类反馈；若它能独立报出 A1 碎镜 / A2 打斗缺席 / A4 运镜无动机 / A5 空间混乱中的 ≥3 类，协议有效；报不出的那一类 → 补评审判据，再跑一次。结果写回本卡。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [自动] 成片报告含交付声明且写明级别；`grep -nE '达标|可发布|质量通过' final-report.md` 有命中时，`review/self-screening.md`、`review/independent-review.md`、`review/cold-audience/` 必须同时存在，否则不通过（无专用脚本：grep + 文件存在检查）〔F1、F2〕→ [`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)
2. [自动] 审片证据里引用的接触表/截图真实存在且非空：`python3 50-rubrics/scripts/asset_exists.py review/` 无 `E2-missing-ref` / `E2-empty-asset`〔F1、C2〕。
3. [目视] `review/self-screening.md` 在打开任何制作文档**之前**写成，字段齐：观看方式（1×、不暂停、只开成片）、第一次困惑的时间码、第一次想划走的时间码、主因果链复述（谁想要什么 → 阻碍 → 做了什么 → 结果）〔F1〕。
4. [目视] `review/independent-review.md` 由隔离会话产出，首行写明输入清单，并声明"未见生成提示词 / 修改轮次 / 指标面板 / 作者通过理由"；每条 finding 含 时间码、证据、观众影响、严重度（blocker / major / minor / note）；结论取 APPROVE / APPROVE_WITH_NOTES / REVISE / PROVISIONAL 之一〔S-ZEN-12、S-CASE-25〕。
5. [目视] 独立评审含 ≥1 道幻觉探针（问一个确定不存在的物体或事件）；评审答"有" → 本次评审作废重做〔S-CASE-29〕。
6. [目视] 新旧版对比按两两比较做，交换顺序各跑一次，两次结论一致才计入；不一致 → 标"无法判定"交人类〔S-CASE-21、S-CASE-27〕。
7. [冷观众] ≥3 名冷观众中 ≥2/3 正确复述本集主因果链，且无断点被 ≥2 人同时标记；用 agent 替身时报告必须写"替身测试，置信度降级"〔GAP-2；definition-of-done L1〕→ [`90-curriculum/cold-audience-protocol.md`](../../90-curriculum/cold-audience-protocol.md)
8. [目视] 人类主创每指出一个审片包没有先报出的问题，当轮在 `review/defects.md` 的 `首次发现者` 列记为"人类"，并补一条判据 + 一道找错题 + 一条记忆〔G4〕。

## → 行为改变（下次……）

**下次交付成片前，按顺序执行"外部视角协议"；任一步缺证据，交付声明只能写"技术合格（L0），观感未验证"。**

1. **封存 L0**：脚本报告存入 `review/l0-report.json`。从这一刻起，它只能出现在报告的"L0 技术闸门"栏，禁止出现在"观感"栏。
2. **自我放映**：只打开 `final.mp4`，1× 速度，从头到尾不暂停，不打开分镜、提示词、剪辑单。看完先写 `review/self-screening.md`，写完才允许打开文档对照。每个困惑点要先判定性质：**悬念**（观众知道自己不知道什么）可以保留；**困惑**（观众不知道发生了什么）必须修。
3. **独立评审**：新开会话，优先换模型。
   - 输入白名单：成片（或 `contact_sheet.py` 接触表 + 按剧本取字的字幕）、学院判据、季圣经中的一句话梗概。
   - 输入黑名单：生成提示词、分镜表、"第 N 版"、"全部指标已绿"、作者的通过理由、人类以往的反馈原话。
   - 评审先独立写出"本集应当让观众明白的 3 件事"，再看片对照（reference-guided〔S-CASE-21〕）。
   - 评审起手式（原样使用）：
     ```text
     你是未参与本片制作的评审。你只看到成片和判据。先写出"一个陌生观众看完本集应当能说出的 3 件事"，
     再看片。每条问题写：时间码 | 现象 | 证据（帧/台词）| 对观众的影响 | 严重度。
     不得写"AI 味""不够电影感"这类无证据评价。无法读取媒体的项写"未验证"，不得推断。
     最后回答探针题：{一个确定不存在的物体} 在片中出现了吗？
     ```
4. **冷观众**：按 [`20-craft/cold-audience-test/SKILL.md`](../../20-craft/cold-audience-test/SKILL.md) 执行；每轮优先 5 人（单人约发现 31% 的问题，5 人约 85%〔外部调研·S-CASE-14〕），最少 3 人。主持者只催对方说话，不引导〔外部调研·S-CASE-13〕。
5. **回流**：每条 finding 写进 `review/defects.md`，按 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3 路由到病灶阶段修，不在视频提示词里打补丁（见 [`60-casebook/cards/F3-patch-iteration.md`](F3-patch-iteration.md)）。
6. **禁止**：同一会话既生成又给出最终"通过"；"改完自评已修复"计入通过（修复须由脚本复测或独立评审新旧对比确认）；报告中用"全绿"指代质量；为讨好测试观众改结局（Ebert 对试映的批评〔外部调研·S-CASE-19〕：冷观众测的是"看懂没有"，不是投票定剧情）。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 通用于任何"agent 生成 + agent 验收"的管线。换模型不会消除它：基准里 19 个模型共享叙事层短板〔S-PIPE-11〕，换生成器只换掉像素层问题。
- ★ 对 agent 自身同样成立：本卡要求的"隔离会话评审"也适用于评审学院自己的产出（剧本、分镜、判据）。
- ☆ 人类冷观众暂不可得时，persona 化多模态模型可以做冷观众预演，但不能替代真人；方向仍由人类创意负责人拍板〔外部调研·S-PIPE-13〕。替身结果只能支撑"L1（替身，置信度降级）"。
- ☆ 独立评审会话的成本约等于一次额外会话，远低于一轮 r1→r5 式返工（〔学院推断〕；验证法：记录下一集的返工轮数与评审耗时）。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)（自我放映 + 8 维自查 + 独立评审）、[`20-craft/cold-audience-test/SKILL.md`](../../20-craft/cold-audience-test/SKILL.md)、[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（审片阶段闸门）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（证据先于结论）。
- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)。
- 判据：[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)、[`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/season.md`](../../50-rubrics/checklists/season.md)。
- 协议：[`90-curriculum/cold-audience-protocol.md`](../../90-curriculum/cold-audience-protocol.md)、[`00-orientation/eight-questions.md`](../../00-orientation/eight-questions.md)（G4）。
- 找错题：[`60-casebook/drills/DR-16.md`](../drills/DR-16.md)（自证循环）、[`60-casebook/drills/DR-20.md`](../drills/DR-20.md)（综合复盘）。
- 相邻案例：[`60-casebook/cards/F2-proxy-metrics.md`](F2-proxy-metrics.md)、[`60-casebook/cards/F3-patch-iteration.md`](F3-patch-iteration.md)、[`60-casebook/cards/F4-skills-not-ability.md`](F4-skills-not-ability.md)、[`60-casebook/cards/C2-lenient-acceptance.md`](C2-lenient-acceptance.md)（资产层的同构案例）、[`60-casebook/cards/D5-qc-tools-lie.md`](D5-qc-tools-lie.md)（单通道不判决）。
