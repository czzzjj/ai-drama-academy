---
id: F2
title: 数字达标 ≠ 观感达标
group: F 质量与学习论
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [screening-review, shot-qc, edit-and-assemble, storyboard-long-take, cold-audience-test]
drills: [DR-17, DR-21]
---
# F2 · 数字达标 ≠ 观感达标

> 一句话：**代理指标不达标，说明一定有问题；代理指标达标，对质量一个字也没说。** 指标是地板，不是天花板。每个数字都必须配一条"它证明不了什么"和一条配对的观感检查，否则不得出现在质量结论里。

## 症状（含人类主创原话，逐字引用档案）

- "固定运镜=0"全绿，人类主创说：「无电影级运镜」；同一时期还说：「苏晓冲击镜头过于耿直，没有运镜和合理的打斗逻辑」〔委托方实证·F2、A4〕。
- "无坏帧 / 无烧录 / 全采用"全绿，人类主创说：「片段式、剧情跳跃、无法理解」〔委托方实证·F2、A1〕。
- 打斗相关指标没有一项报警，人类主创说：「全是几个简单动作的慢镜头」〔委托方实证·A2、A3〕。
- agent 的困惑（agent 原话）："为什么技术上全绿，观感还是不行？"〔委托方实证·G2〕
- **自检识别特征**：你为一条观感反馈新增了一个数字，然后用"该数字已达标"宣布反馈关闭。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

| 代理指标（全绿） | 它实际测的 | 同期人类原话 | 指标看不见的东西 |
|---|---|---|---|
| 固定镜头 = 0 | 每镜相机有位移 | 「无电影级运镜」 | 运镜的动机：为什么此刻这样动〔A4③〕 |
| 无坏帧 / 无烧录 / 全采用 | 文件没坏、画面没被加字、没有镜被拒 | 「片段式、剧情跳跃、无法理解」 | 29 镜均长 2.96s，因果链被切断〔A1〕 |
| 渲染 rc=0、verify 全绿 | 能播、规格对 | 「几乎没有做 BOSS 打斗」 | 打斗被"动作瞬间+反应镜头"替代〔A2〕 |
| 响度 -16 LUFS | 音量合规 | （无直接反馈） | 只有对白+基础拟音+配乐，没有层次〔GAP-3〕 |
| 每镜嵌入专业 primitives 句式 | 提示词里有专业词 | 「苏晓冲击镜头过于耿直，没有运镜和合理的打斗逻辑」 | 词汇在场 ≠ 设计在场〔F4、A4②〕 |

- 指标的来历：人类说"没有运镜"，agent 把它翻译成"相机位移次数"，于是"固定镜头=0"被造出来并被满足〔委托方实证·A4①、G6〕。
- "全镜采用"：每一镜都被采用，即验收这一关**从未行使过拒绝权**〔F1〕。外部对照：专业团队公开的素材比约 300:1（数百次 10–20 秒生成剪成 1.5 分钟）〔外部调研·S-CASE-05〕。〔学院推断：100% 采用率本身就是验收失效的信号；验证法：统计下一集每镜 seed 数与 `qc/*.md` 中"不通过"条数。〕

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 把可量化的代理指标（proxy metrics）当成了质量本身〔委托方实证·F2〕。
2. 每个指标只有"通过"语义，没有"它证明不了什么"的声明；报告里的"全绿"因此被读成"达标"〔F1〕。

### 方法论原因
3. **按"能测"挑指标，不按"与观众反应相关"挑。** 响度、坏帧、烧录字幕有现成工具，所以先被测；因果可读、空间可读没有工具，所以没人测。〔学院推断；验证法：列出委托方全部自动检查项，标注每项对应的观众问题，预测无一项对应"看不看得懂"。〕
4. **反馈被翻译到参数层。** "运镜"对人类是镜头语言设计（景别、视点、何时动、为何动、在哪切），被翻译成相机位移计数〔G6；[`00-orientation/glossary.md`](../../00-orientation/glossary.md) B 表〕。指标一旦成为目标，就以最省力的方式被满足：每镜加一个运动词。
5. **被满足的指标反过来伤害质量。** 为凑"非固定"套用 primitives 运镜词〔A4②〕；同类左右维度词（truck/arc/orbit）与起始帧轴线冲突，正是 r4「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」的直接原因〔A5①〕。〔学院推断：r4 的换边词来自修运镜那一轮；验证法同 [`60-casebook/cards/A5-spatial-chaos.md`](A5-spatial-chaos.md) 根因 6，对 r1–r4 提示词跑 `direction_audit.py` 比较 `DIR-camera` 命中数。〕
6. **层级错配。** 观众判断按"情绪 > 故事 > 节奏 > 视线 > 二维平面 > 三维空间"排序，页面给出的权重只有情绪一项 51%〔外部调研·S-STORY-13〕。委托方的指标全部落在这条序列的最末端，甚至在序列之外（文件规格）。
7. **替代修正也会退化成代理。** A4 的修正把"运镜计数"换成"运镜因果句"〔A4〕；但 `segment_rhythm.py` 的 `A4-cause` 只能查句式"因为 X，所以 Y"在不在，查不了 X 是否真的发生、Y 是否真的在那一刻发生。句式存在 = 新的代理。

### 外部调研补强的根因
8. **最好的自动视频指标也只测技术层。** VideoScore 在 37.6K 个视频的人类多维打分上训练，与人评 Spearman 达 77.1，但不评叙事〔外部调研·S-CASE-30〕。多镜头基准的结论：生成系统是 "pixel renderers rather than storytellers"〔外部调研·S-PIPE-11〕、"visual interpolators rather than true world models"〔外部调研·S-PIPE-12〕。像素层指标越漂亮，越说明短板在别处。
9. **观众先骂的不是画质。** 《山海奇镜》差评集中在"面部表情太僵硬"等表演问题，好评说"有看大片的感觉"〔外部调研·S-CASE-01〕。AI 影展的门槛是"fully contained, linear narrative"，评叙事不评技术演示〔外部调研·S-CASE-09〕。
10. **"执行状态冒充内容权威"是常见返工原因**〔外部调研·S-ZEN-23〕：跑完了、出图了、全采用了，都不是"过关了"。剧本盲评量表明确"文本更长、格式正确、用了更多物件或数字都不自动加分"〔外部调研·S-ZEN-19〕。
11. **自动分数闸门的反例**：VLM 打分 60 分及格、重试到上限自动放行〔外部调研·S-PIPE-15〕——把代理指标直接接到放行开关上。

## 修正过程（做了什么、第几轮、结果）

1. 委托方的结论是教训，不是已执行的修正："指标是下限不是上限；学院必须教'指标之上的观感判断'，并给观感验收方法（看片法/对照法/冷观众）"〔委托方实证·F2〕。
2. 唯一执行过、并被实测的"去代理化"：r5 把空间问题从"多写方位词"改为设计规则（单轴定侧 + 方位词审计），空间维度实测达标〔委托方实证·A5、M4〕。它成功的原因是先改设计，再用脚本守住设计，而不是先造指标。
3. 学院落地（〔学院推断〕）：达标四级 L0–L3，L0 = 全部自动项（[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)）；成片报告分栏；下表"指标登记表"成为报告固定附件。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [自动] 成片报告分"L0 技术闸门"与"L1–L3 观感闸门"两栏；观感栏出现"全绿 / 指标达标 / rc=0"等字样即不通过（无专用脚本：grep）〔F2、F1〕→ [`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)
2. [目视] 报告引用的每个数字指标在指标登记表中有一行，四列齐全：能证明 / 证明不了 / 配对观感检查 / 证据文件。缺配对检查的指标不得出现在任何质量结论句中〔F2〕。
3. [自动] `python3 50-rubrics/scripts/segment_rhythm.py storyboard.md` 无 `A1-mean-short`、`A4-cause` error〔A1、A4〕→ [`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)；**并且** [目视] 随机抽 ≥3 镜，把运镜因果句与 `contact_sheet.py` 接触表对照：X 在画面中发生了，Y 恰在 X 那一刻发生。只过前者 = 只过了句式。
4. [自动]+[目视] 全集 `qc/*.md` 中"不通过"条数为 0、且每镜只出过 1 个 seed → 判"验收无拒绝权"警报：由独立会话复验任意 3 镜，复验发现问题 → 本集全部验收记录作废重做〔F1、C2；〔学院推断〕〕。
5. [目视] 静音放映：关掉声音和字幕看一遍，写出主因果链；写不出 → 画面没有在讲故事，是台词和字幕在讲〔〔学院推断〕；验证法：与冷观众复述结果对照，二者结论一致率记入本卡〕。
6. [冷观众] 冷观众复述主因果链与空间关系（谁在谁左边、从哪进来）；L1 阈值见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)〔F1、A5〕。

## → 行为改变（下次……）

**下次写成片报告时，先填这张"指标登记表"；任何指标若"配对观感检查"一栏为空，就只能写进 L0 栏，不得用于证明质量。**

| 指标（脚本） | 能证明 | 证明不了 | 配对观感检查（证据） |
|---|---|---|---|
| verify 全绿（`loudness_verify.py`） | 能播、响度/真峰/画幅合规、无黑场冻结 | 好看、看得懂 | 自我放映记录 + 冷观众复述 |
| 无死段/跳变（`psnr_scan.py`） | 没有冻结、镜内无突变 | 节奏对不对 | 自我放映中"拖/赶"的时间码 |
| 无烧录文字（`burnin_text_scan.py`） | 画面没被生成器加字 | 画面讲清了事 | 静音放映复述 |
| 台词三方对账（`transcript_reconcile.py`） | 台词都在 | 台词演出来了（语气、停顿、口型） | 听感记录 + 口型接触表 |
| 运镜计数 / 因果句存在（`segment_rhythm.py`） | 相机在动、句式在 | 运镜有动机 | 接触表核对 X 与 Y 同刻发生 |
| 平均镜长 ≥5s（`segment_rhythm.py` `A1-mean-short`） | 生成单位合规 | 因果链完整 | 冷观众复述 + 第一次困惑点 |
| 方位审计通过（`direction_audit.py`） | 文字不与起始帧矛盾 | 观众知道谁在哪 | 冷观众空间题 |
| 对白容量通过（`dialogue_capacity.py`） | 装得下 | 不赶、有表演留白 | 听感 + `D3-rushed` 处置记录 |
| 锚点句逐字（`prompt_lint.py` `VP-anchor`） | 提示词一致 | 画面一致 | 正脸与板图并排裁剪（`contact_sheet.py --crop`） |
| 全镜采用 | 没有废镜 | 验收有效 | 拒绝率 + 独立复验 |

1. **下次收到观感反馈时**，先按 [`00-orientation/glossary.md`](../../00-orientation/glossary.md) B 表把它翻译到设计层，再给它设计一条观感检查，最后才允许加一个数字作为守门下限。**禁止**用新增的数字"关闭"一条观感反馈。
2. **下次读到自己报告里的"全绿"时**，改写为："L0：n/n 自动项通过（只证明没出错）；观感：L1 证据见……/未验证"。
3. **下次设计任何自动检查时**，同一提交里写清它的"证明不了"一栏；脚本只报事实，审美判决留给目视与冷观众（[`CONVENTIONS.md`](../../CONVENTIONS.md) §8.5）。
4. **下次某个指标改善而人类反馈未变时**，判定该指标与问题无关，停止优化它，回到 [`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md) 找真正失分的维度。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 通用。换生成器、换题材都成立；生成器越强，像素层指标越容易全绿，代理指标的误导性只增不减〔S-PIPE-11〕。
- ★ 发布后的平台数据（完播、留存曲线的 dips/spikes〔外部调研·S-CASE-16〕）也是代理，只是离观众更近。委托方从未发布〔GAP-1〕，这里无一手经验；用法见 [`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)。
- ☆ 登记表中的脚本名是本管线专有的；换管线时保留四列结构，替换脚本名。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（运镜因果）、[`20-craft/cold-audience-test/SKILL.md`](../../20-craft/cold-audience-test/SKILL.md)。
- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)。
- 判据：[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)、[`50-rubrics/quality-model.md`](../../50-rubrics/quality-model.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`30-taste/judgment-cards.md`](../../30-taste/judgment-cards.md)（看片法/对照法）。
- 找错题：[`60-casebook/drills/DR-17.md`](../drills/DR-17.md)（代理指标）、[`60-casebook/drills/DR-21.md`](../drills/DR-21.md)（反馈翻译："没有运镜""打斗逻辑"）。
- 相邻案例：[`60-casebook/cards/F1-self-verification-loop.md`](F1-self-verification-loop.md)、[`60-casebook/cards/A4-unmotivated-camera.md`](A4-unmotivated-camera.md)、[`60-casebook/cards/A1-fragmented-shots.md`](A1-fragmented-shots.md)、[`60-casebook/cards/A5-spatial-chaos.md`](A5-spatial-chaos.md)。
