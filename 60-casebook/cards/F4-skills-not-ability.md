---
id: F4
title: 学了技能 ≠ 有了能力
group: F 质量与学习论
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [production-director, screening-review, storyboard-long-take, video-prompting-h3]
drills: [DR-19, DR-20]
---
# F4 · 学了技能 ≠ 有了能力

> 一句话：**能力 = 知识 × 实践反馈 × 标准内化，是乘法。** 只装技能等于只做了第一项，另外两项为零，乘积就是零。委托方手里真正管用的每一条方法论，都是用一次失败加一次反馈换来的，没有一条是装出来的。

## 症状（含人类主创原话，逐字引用档案）

- 装了 7 个导演/运镜/分镜技能，每个镜都嵌了专业 primitives 句式，读完了全部参考规范，输出质量没有质变〔委托方实证·F4〕。
- 同时还写过多版方法论文档，做过 r1→r5 五轮打斗实验，"质量没有质变"〔委托方实证·T-4〕。
- 在每镜都嵌入专业运镜句式的同期，人类主创原话：「无电影级运镜」「苏晓冲击镜头过于耿直，没有运镜和合理的打斗逻辑」〔委托方实证·A4〕。
- 档案对这一现象的描述："装了专业运镜技能后，只会机械套用 primitives 词汇"〔委托方实证·A4②〕。
- agent 的困惑（agent 原话，不是人类原话）："为什么学了一堆技能，能力没有质变？"〔委托方实证·G3〕
- **自检识别特征**：提示词里有你说不出"此刻为什么用它"的专业词；你在报告里用"已装载某技能 / 已遵循某规范"证明质量。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

**知识注入的投入**：7 个专业技能、全部参考规范、多版方法论文档、每镜 primitives 句式〔F4、T-4〕。档案中没有任何一项被记录为"带来了某个维度的改善"。

**委托方真正掌握的方法从哪来**（档案可追溯部分）：

| 方法论 | 换来它的失败 / 反馈 | 证据 |
|---|---|---|
| M1 长段多拍 | 29 镜均长 2.96s 被说「片段式、剧情跳跃、无法理解」+ r1–r5 实验 | A1、P10 |
| M2 起始帧海报级 | "文字救不了构图"的实测 | P4 |
| M4 单轴定侧 | r4「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」→ 深挖 → r5 实测 | A5 |
| M5 对白容量 | 同一镜 3 个 seed 各缺不同句 | D3 |
| M6 锚点卡 + 多 seed + 逐特征放大 | C1 七个子案、C2 早期误判 | C1、C2 |
| M7 链式参考 | 苏晓脸漂移成"粗犷成熟脸" | B1 |
| M8 生成禁令包 | 烧录字幕、片尾黑卡被加 "LAVCE"、"ф"被画成十字 | D1、D2、D4 |
| M10 双通道验收 | 静音音轨转出"字幕by索兰娅"、气声误听为"救我" | D5 |

- 读法：档案中能追到来源的方法论，**全部**来自"失败 → 反馈 → 修正"回路；M3、M9 的来源档案未写明。
- 最关键的一行是 M4：A5 的根因是"深挖专业分镜技能后"才定位的〔A5〕。技能里的知识一直都在，直到 r4 的具体失败给了它一个问题，它才变成能力。**知识只在被一个具体失败提问时才转化。**
- 一个未排除的装载因素：技能/插件装改后不重启不生效（装配期一次性扫描）〔委托方实证·E3-3〕。〔学院推断：r1–r5 期间部分技能可能并未被运行时加载，只在被当作文件读取时起作用；验证法：查当时会话的技能清单或启动日志。〕

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 技能是"知识注入"，能力 = 知识 × 实践反馈 × 标准内化，只做了第一项〔委托方实证·F4〕。

### 方法论原因
2. **知识被用在输出层，而不是决策层。** primitives 被当成词汇逐镜嵌入提示词〔A4②〕，而不是用来回答"这一镜为什么存在、为什么此刻这样动"。词汇在场，决策缺席。
3. **没有"做 → 被判分 → 对照标准答案 → 改"的回路。** 唯一的判分者是人类主创，判分不定期、只给样本、不给标准答案〔F1、F3〕；agent 无法从中提取可复用的判断。
4. **没有内化的标准。** 没见过足够多成对的好/坏样例，就无法区分好与坏，也就无法自己先发现问题〔G4、F1〕。
5. **通用技能不知道本管线的物理约束。** 通用电影语言默认"相机听话"；本管线里起始帧钉死轴线〔A5〕、124 帧下限〔T-2〕、cfg=1.0 下 negative 无效〔T-2、C1〕、一次生成只有一个主运镜（[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R5）。照教科书写环绕、横移，正好与起始帧冲突〔A5①〕。
6. **学到的东西存成了文档，没有存成判据。** "多版方法论文档"〔T-4〕不绑定任何检查，下一次生成不会自动重新执行它。对照：r5 的教训被写成方位词全量 grep，于是守住了〔A5〕。〔学院推断；验证法：统计委托方方法论文档中的规则条数，与已有对应自动检查的条数之比。〕

### 外部调研补强的根因
7. **技能包封装的是作者观点，不是校准过的标准。** 一个 31 个剧本技能的仓库，评估档位（S ≥8.5 … C ≤7.4）由作者设定，没有数据校准〔外部调研·S-PIPE-16〕。装上它得到的是一套意见，不是一把尺。
8. **技能文本与实际行为会分叉，而测试照样全绿。** 一个公开的短剧技能套件在评估中发现，上一轮最重的缺陷是"SKILL.md 写的做法与脚本实际行为不一致，而测试全绿"〔外部调研·S-ZEN-18〕。
9. **专业术语对生成器只是概率性有效。** 公开实践中，镜头术语（如 "Hitchcock Zoom"）大约 "six out of 10 times" 有效〔外部调研·S-CASE-05〕。术语写进提示词 ≠ 效果出现在画面里，必须看产出。
10. **判断力靠样例，不靠规则。** 给评审模型 3 个 few-shot 样例，交换顺序一致率从 65.0% 升到 77.5%〔外部调研·S-CASE-21〕；多模态评审在两两比较上接近人类，在绝对打分上偏离大〔外部调研·S-CASE-27〕。所以标准内化要用成对样例训练，而不是背规则表。
11. **别人的实测只是你的假设。** 外部观察只支持其项目内校准，不自动升格为跨项目定律〔外部调研·S-ZEN-24〕；公开的 H3 行为观察自己声明是同一模型判断、非独立人评，应作为"待复测假设"〔外部调研·S-PIPE-03、S-ZEN-17〕。
12. **工具熟练是长期积累。** 一位独立创作者说："Everything I do within these tools is a skill set that's been built up over a decade plus."〔外部调研·S-CASE-06〕

## 修正过程（做了什么、第几轮、结果）

1. 委托方的教训：学院不能只放知识层，必须带训练回路（练习任务 + 自动判分）与标准内化（好/坏样例对照、审美判断训练）〔委托方实证·F4〕。档案中没有执行记录。
2. 已实测有效的转化样板（A5）：具体失败（r4）→ 带着问题回读技能 → 抽出可判真假的规则（相机只动高度与距离）→ 写成可执行检查（方位词 grep）→ 实测达标（r5）〔委托方实证·A5、M4〕。
3. 学院落地（〔学院推断〕）：[`90-curriculum/training-loop.md`](../../90-curriculum/training-loop.md)（加载 → 找错题 → 小任务 → 判分 → 复盘）；找错题 `60-casebook/drills/DR-01`…`DR-22`（题面与答案分离）；练习 `90-curriculum/exercises/`；好/坏样例对 [`30-taste/pairs/`](../../30-taste/pairs/)；装机验证 [`90-curriculum/install-verification.md`](../../90-curriculum/install-verification.md)。验证法：装载学院前后，对同一组找错题与同一个小任务各做一次，用答案文件的打分规则比较得分。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [自动] 装载后首次开工前：`python3 50-rubrics/scripts/run_all_selftests.py` 退出码 0（脚本在本环境真能跑）；[目视] 运行时技能清单里能看到学院技能，装改后已重启〔E3-3〕。
2. [目视] 开工前完成 [`90-curriculum/training-loop.md`](../../90-curriculum/training-loop.md) 规定的最低学分；找错题按答案文件打分（满分 10：根因 4 / 修正 4 / 判据 2），得分记录写入记忆〔F4、G3〕。
3. [目视] 每条新学到的规则（来自技能、规范或外部来源）在投入生产前绑定三样东西：一条可判真假的检查句、一个执行它的脚本规则代码或清单行、一道找错题。三样不全的规则只能算"知识"，不得在提示词里使用它的词汇〔F4〕。
4. [自动] 提示词里的每个专业运镜词在分镜 `运镜因果` 中有对应因果句：`segment_rhythm.py storyboard.md` 无 `A4-cause` error；`prompt_lint.py` 无 `VP-adjective` warn（未拆解的评价性形容词）〔A4、M3〕→ [`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)
5. [目视] 能力证明 A/B：一条新规则进入记忆前，对同一镜做"有 / 无该规则"两版、各 ≥2 seed，由隔离会话两两比较（交换顺序各一次）；看不出差异 → 降级为"待验证假设"，不进核心记忆〔S-CASE-21、S-CASE-27〕。
6. [目视] 每个被人类打回的问题，当轮写成一道找错题（题面不暴露答案）+ 一对好/坏样例 + 一条记忆；用于验证能力的题不得同时用于训练，验证题一旦促成修改即退役〔G4；S-ZEN-18〕。
7. [冷观众] 能力的最终度量是跨集的 L1 通过率（冷观众复述主因果链），逐集记录；装载学院后若 L1 通过率不升，说明知识没有转化〔F1；definition-of-done〕。

## → 行为改变（下次……）

**下次装一个技能、读一份规范或拿到一条外部经验时，不要直接在提示词里用它的词。先做"转化四步"，四步做完它才算能力：**

1. **抽判据**：把它改写成可判真假的检查句（"眯眼去色后主体剪影仍可读"可以；"画面要有电影感"不可以）。
2. **对物理约束**：逐条对照 T-2（帧网格、cfg=1.0、六段方言）与 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1–R7；冲突的部分改写或丢弃，并写明原因。
3. **做 A/B 最小样**：同一镜、有/无两版、各 ≥2 seed，隔离会话两两比较。没有差异，就是装饰。
4. **固化**：通过的写成判据行 + 找错题 + 样例对 + 记忆条目；没通过的写进记忆的"待验证假设"，注明验证法。

另外：
- **下次开工前**，先跑训练回路最低学分，再进生产〔G3〕。
- **下次被打回时**，当轮产出 1 道找错题 + 1 对样例 + 1 条记忆，不留到"以后总结"。
- **下次写提示词时**，每个专业词都要能接上"因为此刻发生了 X，所以用 Y"；接不上就删。
- **禁止**：用"已装载 X 技能 / 已读 Y 规范 / 已嵌入 primitives"作为质量证据；把外部实测数字不经复测写成本管线的规则（R3 的 4.1 字/秒就是先标外部、再由脚本以 warn 级执行的例子）。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 通用，并且适用于本学院自身：装载本学院同样只是"知识注入"。学院不被视为已生效，直到 [`90-curriculum/install-verification.md`](../../90-curriculum/install-verification.md) 的打分任务证明行为确实变了。
- ★ 换模型时，"对物理约束"一步必须重做：上一个生成器上成立的规则可能失效，回到"待验证假设"。
- ☆ 判据 1 的重启要求来自委托方运行时的装配期扫描行为〔E3-3〕；换运行时先确认其加载机制。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（开工前学分闸门）、[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)（打回 → 找错题回流）、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（运镜因果）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（专业词必须有因果）。
- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)（通用电影语言在生成器下的改写）。
- 训练：[`90-curriculum/training-loop.md`](../../90-curriculum/training-loop.md)、[`90-curriculum/install-verification.md`](../../90-curriculum/install-verification.md)、[`30-taste/pairs/`](../../30-taste/pairs/)、[`30-taste/judgment-cards.md`](../../30-taste/judgment-cards.md)、[`40-memory/core-memory.md`](../../40-memory/core-memory.md)。
- 判据：[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)。
- 找错题：[`60-casebook/drills/DR-19.md`](../drills/DR-19.md)（知识≠能力）、[`60-casebook/drills/DR-20.md`](../drills/DR-20.md)（综合复盘）。
- 相邻案例：[`60-casebook/cards/A4-unmotivated-camera.md`](A4-unmotivated-camera.md)（机械套用 primitives）、[`60-casebook/cards/A5-spatial-chaos.md`](A5-spatial-chaos.md)（知识被失败激活的样板）、[`60-casebook/cards/E3-environment-quirks.md`](E3-environment-quirks.md)（装改后需重启）、[`60-casebook/cards/F1-self-verification-loop.md`](F1-self-verification-loop.md)、[`60-casebook/cards/F3-patch-iteration.md`](F3-patch-iteration.md)。
