# 05 · 节奏工程

> 节奏是观众感知到的变化密度和变化对比，切镜次数不是节奏。"快"要有"慢"和"静"衬着才读得出来；在 H3 里，时长会被读成事件的速度，所以慢动作往往说明一段里塞的事件太少；生成单位必须长，剪辑单位可以短 ｜ 浓缩案例：A1, A3, P10, M1, GAP-6 ｜ 对应技能：storyboard-long-take, action-choreography, edit-and-assemble, sound-design, screening-review

## 核心判决

**T05.1 节奏 KPI 是有效拍数（观众能感知到的状态改变），不是切镜数，也不是平均镜长。**
为什么：首轮成片 29 个镜、均长 2.96s，人类主创的反馈是「片段式、剧情跳跃、无法理解」「切片太短，切点跳脱感强」〔委托方实证·A1〕。按 29 × 2.96s ≈ 86s 换算，约每分钟 20 刀：刀很多，因果却被切断了。判决来源见 [`00-orientation/glossary.md`](../00-orientation/glossary.md)；`segment_rhythm.py` 在 `A1-stats` 里报告有效拍数（Σ拍数）。

**T05.2 生成单位和剪辑单位分开：每次生成 ≥124 帧（5.17s），承载一条完整的动作链；剪辑的 CUT 可以很短，快剪从长镜里取。**
为什么：短剪不是罪，碎镜症才是〔学院立场见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) R6〕。港片 12 分钟约 490 个镜头，最短约 1/3 秒，靠动作匹配和 180° 规则依然 "totally intelligible"〔外部调研·F-STORY-09〕；H3 低于 124 帧的结果不可信〔委托方实证·T-2〕。判据：R-SB-01、R-SB-03、R-CUT-12。

**T05.3 每个动作段至少有两种速度层次（快 / 慢 / 爆 / 静），每一处"慢"都写明设计理由。**
为什么：全片没有速度层次，"慢"成了默认，人类主创说是「几个简单动作的慢镜头」〔委托方实证·A3〕。判据：R-SB-18；Q6 的 0 分锚点是全片单一速度（见 [`50-rubrics/quality-model.md`](../50-rubrics/quality-model.md)）。

**T05.4 段内节拍按"快 — 慢 — 爆 — 静"设计：冲刺快切 → 对峙慢推 → 爆发一击 → 余波静场。**
为什么：这是委托方 A3 的修正方案〔委托方实证·A3〕；外部对应的是港片的 pause/burst/pause〔外部调研·F-STORY-10〕，以及 "a marked rhythm alternating an exact visceral impact with tingling aftereffects"〔外部调研·S-STORY-18〕。

**T05.5 在 H3 里，时长会被读成事件速度。画面"慢"，先查这一段的事件密度，再查速度词。**
为什么：给摔倒 1.5s，它就演成月球重力；真实摔倒约 0.4–0.6s，余下的时间要给后果〔外部调研·S-H3-11〕。这是 A3 的新增根因（evidence-reconciliation 第二部分）。判据：R-SB-19。

**T05.6 生成器默认偏慢：动作镜要写实时速度句、自带速度的动词和环境运动，三者缺一不可。**
为什么：速度描述含糊时，扩散模型 "will almost always choose slower"；对策是用 strides、darts、charges 这类速度动词，同时写环境运动，否则会出现"慢跑的人配一个静止的背景"〔外部调研·S-VGEN-19〕。委托方的固定句式是 `Real-time speed throughout, no slow motion`〔委托方实证·A3〕。判据：R-VP-03。

**T05.7 刀速按戏的类型分层：对白场约每分钟 6 刀，动作段约每分钟 25 刀；动作段内刀速逐步加快，不靠一刀突变。**
为什么：Murch 的参照是动作段约 25 刀/分、美国片对白场约 6 刀/分（二手转述，置信度中）〔外部调研·F-STORY-08〕；剪辑经验是 "the editing pace slowly increases as the fight progresses"〔外部调研·S-STORY-21〕。不分戏的类型、全片一个刀速，就等于没有节奏。

**T05.8 切点放在动作进行中，不放在两个静止之间。**
为什么：动作剪辑让两个镜头"看起来时间连续"，形成 "a visual bridge"，还能转移观众对剪点的注意〔外部调研·F-STORY-29〕。Q6 的 1 分锚点里就有"切点不在动作中"。

**T05.9 一镜的表情拍不超过 2–3 个，多了会被模型抹平，画面就"死板"。**
为什么：一个 7 秒特写写了 9 拍，相邻帧 PSNR 37–42 dB，脸基本没动；拆成三个 2–3 秒的镜头后降到 22–23 dB，表情才到位〔外部调研·F-H3-16〕。死板有可能是拍写得太多，而不是太少。

**T05.10 声音先于画面或晚于画面切换，是控制时间感的工具：对白场默认用 L-cut 切到听者的反应（约 0.5s），进入大段落时用 J-cut（约 2s）。**
为什么："a half-second overlap in a dialogue scene is often enough"，"a two-second J-cut into a major sequence creates real anticipation"〔外部调研·F-CRAFT-06〕。声音层面的展开见 [`10-theory/11-sound-design.md`](11-sound-design.md)。

**T05.11 生成时不带配乐（`non_diegetic_music: N/A`），配乐在后期作为一条连续音轨铺上，再让"爆"点的剪辑点对齐音乐重拍。**
为什么：委托方 A3 的修正方向包括"音乐节拍对齐切点"〔委托方实证·A3〕，但没有系统方法（GAP-6）；外部也没有找到权威来源（见 [`80-sources/catalog/screenwriting-film-language-action.md`](../80-sources/catalog/screenwriting-film-language-action.md) 空白第 7 条）。已知的事实是：写 `N/A` 的 14 次都没有出配乐〔外部调研·F-ZEN-07〕，不写就会被自动配上泛用音乐〔外部调研·S-H3-11〕。每次生成各配一段音乐，过剪点时音乐必然断。〔学院推断〕验证方法：同一段做两版（对齐重拍 / 不对齐），交给独立评审和 3 名冷观众盲看，记录"带劲 / 拖"的标记。

**T05.12 单集尺度上，相邻情绪拐点的间隔不超过 30s。**
为什么："每 30 秒一个情绪拐点"〔外部调研·F-STORY-19〕（媒体转述的行规）。判据：R-SCR-05。

## 机制解释

1. **剪点就是句号。** Murch 的说法是：决定剪的那一刻，等于在说 "I am going to bring this idea to an end and start something new"〔外部调研·F-STORY-08〕。一个动作切一个镜号，就是在一句话里每个词后面都打句号——刀很多，但观众接不上因果。观众的眨眼只有在影片"起作用"时才会和剪点同步〔外部调研·S-STORY-14〕。
2. **速度是相对的。** 一个动作在全段都快的环境里读不出快。"爆"要有"静"作参照，"快"要有"慢"作参照。所以速度层次是对比结构，不是单一参数。
3. **重量来自停顿。** 打击之后的定格和静场，让观众有时间"感受到"这一下（"Weight comes from the stop, not the drop"〔外部调研·S-H3-11〕）。没有静，爆发就会糊成一团。
4. **为什么 AI 片天然慢。** 生成器求稳，默认选慢〔外部调研·F-VGEN-22〕；作者把时长写得宽松，模型就用慢动作把时长填满〔外部调研·S-H3-11〕。两种偏差叠在一起，就成了 A3。
5. **有效拍和刀速是两个维度。** 有效拍数决定"发生了多少事"，刀速决定"事情以什么颗粒度被呈现"。A1 的问题是刀速高、有效拍低；好的动作段两者都高，而且刀与刀之间有动作匹配。

## 本管线下的变体

### 节奏的三个闸门

| 阶段 | 做什么 | 工具 / 判据 |
|---|---|---|
| 分镜 | 段 / 拍 / 镜三层结构；每镜 ≥5.17s；拍数 ≤3；速度层次标注；事件时长预算 | `segment_rhythm.py`（`A1-short-no-reason`、`A1-mean-short`、`A5-beats-many`、`A4-cause`）；R-SB-01、R-SB-06、R-SB-18、R-SB-19 |
| animatic | 关键帧按分镜时长排起来，配临时对白和节拍标记，连续看一遍，记录第一次困惑和第一次走神的位置 | R-SB-23 |
| 成片 | 切点列表、死段、均长；切点前后各 2 帧目视 | `psnr_scan.py --mode final --edit-list edit-list.md`（`P8-cut-*`、`P8-freeze`、`A1-mean-short`）；R-CUT-12、R-CUT-14 |
| 冷观众 | 记录"拖 / 慢 / 走神 / 跳"的时间点，≥2 人在同一段标记的，回分镜层修 | Q6 `[冷观众]`；[`20-craft/cold-audience-test/SKILL.md`](../20-craft/cold-audience-test/SKILL.md) |

### H3 特有的节奏偏差

- **事件时刻不可控。** 要求 3.0s 和 4.0s 发生的事件，实际都在 2.46s 发生〔外部调研·F-H3-14〕：精确节拍只能在剪辑里定，生成时要留出余量。
- **对白镜比计划长 1.5–2.5s**（开口前有延迟，说完还有拖尾）〔外部调研·F-ZEN-06〕。剪辑时入点放在开口前约 0.25s，出点留约 0.4s 的反应〔外部调研·F-ZEN-22〕。对白场的节奏要在剪辑里收紧，不要在生成时把台词塞得更快（D3）。
- **片尾崩解。** 每个生成镜的最后 1.2–1.7s 不可用〔外部调研·F-H3-18〕，排节奏时只算 `时长 − 尾部余量`（R-CUT-13）。
- **死段要么是设计，要么剪掉。** `psnr_scan.py` 报出的 `P8-freeze`（连续 ≥0.5s、PSNR ≥45 dB）必须在剪辑单里对应到声明过的设计静场，否则就剪掉或重出（R-VID-08、R-CUT-07）。
- **后期变速只能微调。** 加速超过约 106%，观众就会察觉，变速要缓入缓出〔外部调研·F-STORY-27，单一从业者经验〕。〔学院推断〕生成出来的慢动作不能靠后期加速救回来，只能回到提示词补事件密度和速度句后重出。验证方法：拿一个 A3 型慢镜分别做 106% 和 130% 加速，交给冷观众看是否仍然读成"慢镜"。

- **目标均镜长是剪辑口径，不是生成口径。** 外部起点值里的"目标平均镜长 2.5s"（真人剧实测）〔外部调研·S-ZEN-21〕说的是成片 CUT 的均长。生成镜仍然 ≥5.17s，在剪辑时取 2–3s 的 CUT。把 2.5s 当成生成时长，就会退回 A1。
- **镜内调度承担切镜密度。** 生成单元固定在较长的档位时，切镜密度要靠镜内的景别或视点变化、完整的动作与反应交接来承担，否则"观众读到的都是幻灯片"〔外部调研·F-ZEN-18〕。

### 有效拍的统计口径

- 有效拍 = 段内一次状态改变（攻 → 挡、问 → 答、平静 → 惊觉），分镜 `拍数` 列记空间拍和表情拍，打击拍记在 `内容` 的 `→` 链里（R4）。
- 〔学院推断〕有效拍的密度没有通用阈值。用 ≥3 部对标作品同类段落的拍数作参照（与 R-SCR-20 的对标做法一致），本集同类段落不低于对标的中位数。验证方法：对标统计表和本集分镜表并排存档，冷观众"拖"的标记位置要和低拍密度段落对得上，口径才算成立。

## 常见误用

| 误用 | 症状 | 案例 |
|---|---|---|
| 一个动作一个镜号，用多切镜来"提速" | 「片段式、剧情跳跃、无法理解」 | [`60-casebook/cards/A1-fragmented-shots.md`](../60-casebook/cards/A1-fragmented-shots.md) |
| 动作时长写得宽松、不写速度句 | 「几个简单动作的慢镜头」 | [`60-casebook/cards/A3-slow-motion-default.md`](../60-casebook/cards/A3-slow-motion-default.md) |
| 拿均长或切镜数当节奏达标的依据 | 数字达标，观感不达标 | [`60-casebook/cards/F2-proxy-metrics.md`](../60-casebook/cards/F2-proxy-metrics.md) |
| 嫌对白场慢，就把台词塞得更快 | 缺句，换 seed 也无解 | [`60-casebook/cards/D3-dialogue-capacity.md`](../60-casebook/cards/D3-dialogue-capacity.md) |
| 动作段从头到尾一个刀速 | 没有逐步加快，也没有静场，爆发读不出来 | T05.7、T05.4 |
| 每个生成镜各带一段配乐 | 剪点处音乐断裂，和剪辑节奏无关 | T05.11 |
| 把"目标均镜长 2.5s"当成生成镜时长 | 生成 <124 帧，动作异常，回到碎镜症 | T05.2、[`60-casebook/cards/A1-fragmented-shots.md`](../60-casebook/cards/A1-fragmented-shots.md) |
| 一个特写里写 6 个以上表情变化 | 被抹平，脸不动，"死板" | T05.9 |

对应找错题：DR-01（碎镜）、DR-03（慢镜）、DR-11（对白容量）、DR-20（综合复盘）。

## → 行为改变

- 下次排分镜时，**先**定段（8–15s、一条完整动作链），**再**在段内分 2–3 拍；**禁止**一个动作一个镜号。<5.17s 的镜**必须**填短镜理由，并且不送 H3（R-SB-01）〔委托方实证·P10、M1〕。
- 下次设计动作段时，**必须**在分镜里标出快 / 慢 / 爆 / 静的位置；每一处"慢"写明理由，没有理由就改成实时（R-SB-18）。
- 下次看到产出像慢动作时，**先**查事件密度和时长分配（摔倒是否超过 0.6s、后果是否留了时间），**再**查速度句和速度动词；**禁止**只在提示词里加 "fast"。
- 下次剪辑时，**改为**从长镜里取短 CUT 做快剪，切点放在动作进行中；对白场默认用 L-cut 切到听者反应；**禁止**为了提速去生成 <124 帧的镜。
- 下次写提示词时，`non_diegetic_music` **默认**写 `N/A`，配乐在后期作为一条连续音轨铺上（交给 [`20-craft/sound-design/SKILL.md`](../20-craft/sound-design/SKILL.md)）。
- 下次收到"拖""慢""跳""切点跳脱"一类反馈时，**先**按 [`00-orientation/glossary.md`](../00-orientation/glossary.md) 翻译成 Q6 的具体缺陷（段结构、速度层次、切点位置、拐点间隔），**再**回分镜层修；**禁止**只在剪辑里加转场特效。
- 下次声明节奏达标之前，**先**跑 `segment_rhythm.py` 和成片 `psnr_scan.py`，做一次 animatic 或成片的自我放映，标出"拖 / 跳"的位置，再交给冷观众；**禁止**只凭均长达标就宣布节奏合格。

相关：[`20-craft/storyboard-long-take/SKILL.md`](../20-craft/storyboard-long-take/SKILL.md)、[`20-craft/action-choreography/SKILL.md`](../20-craft/action-choreography/SKILL.md)、[`20-craft/edit-and-assemble/SKILL.md`](../20-craft/edit-and-assemble/SKILL.md)、[`20-craft/screening-review/SKILL.md`](../20-craft/screening-review/SKILL.md)、[`50-rubrics/checklists/storyboard.md`](../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/final-cut.md`](../50-rubrics/checklists/final-cut.md)、[`10-theory/06-long-take-multi-beat.md`](06-long-take-multi-beat.md)、[`10-theory/04-action-design.md`](04-action-design.md)。

## 自测

1. 是非：把均长从 2.96s 拉到 6s，就治好了碎镜症。
<details><summary>答案</summary>错。均长是代理指标（F2）。碎镜症的病根是"一个动作一个镜号"，因果链被切断。要用段 / 拍结构重做分镜：一段承载一条完整动作链，节奏 KPI 是有效拍数。剪辑时仍然可以有短 CUT（R6）。</details>

2. 简答：港片 1/3 秒的镜头为什么看得懂，委托方 2.96s 的镜头反而看不懂？
<details><summary>答案</summary>港片的短镜之间有动作匹配，遵守 180° 规则，机位稳定（F-STORY-09），每个镜头都"不可能被误解"（F-STORY-10）。委托方的短镜是独立生成的碎片：没有动作匹配，没有段结构，而且低于 124 帧，生成本身也不可靠（A1、T-2）。</details>

3. 简答：一段"苏晓冲向 BOSS"写了 8s，产出像慢动作。列出至少三个修法。
<details><summary>答案</summary>① 按事件时长重新分配（冲刺几步约 0.5s/步，剩下的时间给接触、后果、静场），提高段内事件密度（S-H3-11）；② 写 `Real-time speed throughout, no slow motion` 和速度动词（charges、darts）；③ 写环境运动（尘土被带起、衣摆拉直，S-VGEN-19）；④ 确认没有用 turbo 或低步数，并在分镜里标出速度层次。</details>

4. 是非：节拍对齐音乐重拍是外部权威方法，可以直接写成判据。
<details><summary>答案</summary>错。目录里没有找到权威来源（STORY 目录空白第 7 条），委托方也只有修正方向（A3），缺乏系统方法（GAP-6）。只能作为〔学院推断〕，附上盲看 A/B 的验证方法。</details>

5. 简答：一个 7 秒特写写了"惊讶 → 怀疑 → 愤怒 → 克制 → 冷笑 → 转身"，产出脸几乎不动。原因和改法？
<details><summary>答案</summary>表情拍超过 2–3 个会被抹平（F-H3-16）。拆成 2–3 个镜头，每镜 1–2 个表情拍；也可以把部分情绪交给上下文镜头（库里肖夫效应，F-STORY-16）或交给声音。</details>
