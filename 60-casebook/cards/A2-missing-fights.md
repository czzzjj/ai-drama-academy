---
id: A2
title: 打斗缺席
group: A 叙事与节奏
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [action-choreography, storyboard-long-take, video-prompting-h3]
drills: [DR-02, DR-21]
---
# A2 · 打斗缺席

> 一句话：**含蓄 ≠ 缺席。** 为了躲开 AI 肢体崩坏而改用"动作瞬间 + 反应镜头"，结果把交手本身砍掉了——把防御性策略当成了叙事语言。修法不是"少打"，而是**打击拍要密、空间拍要少**。

## 症状（含人类主创原话，逐字引用档案）

- 人类主创原话：「几乎没有做 BOSS 打斗」「全是几个简单动作的慢镜头」〔委托方实证·A2〕。
- 同类反馈：「苏晓冲击镜头过于耿直，没有运镜和合理的打斗逻辑」〔委托方实证·A4〕——"打斗逻辑"在人类口中指因果链（谁为什么出手 → 对方怎么应 → 空间怎么变 → 后果是什么），不是"招式不够多"（见 [`00-orientation/glossary.md`](../../00-orientation/glossary.md) B 表）。
- 观感层面：观众看到"有人出手"和"有人倒下"，但没看到**双方接触与应对**；承诺了 BOSS 战却没有任何可见交手回合 = [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) 的阻断缺陷（Q3）。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 场合：季级短剧前三集中被剧本承诺的 BOSS 战〔委托方实证·T-4、A2〕。
- 当时的拍法："动作瞬间 + 反应镜头"的含蓄策略——出招一镜、受击/反应另一镜，交手过程不出现在画面里〔委托方实证·A2〕。
- 之后做了 r1→r5 五轮打斗实验，每轮只修最新一条反馈（运镜 → 特效 → 史诗 → 空间），人类主创每轮都说"仍不够"〔委托方实证·F3、T-4〕。r5 解决了空间（A5），打斗本身是否被认可，档案未记录。
- 档案中唯一写明的战术链样例：诱敌 → 落空 → 抓隙 → 狂暴 → 闪避 → 击飞〔委托方实证·A2〕。

## 根因（分条；区分"直接原因"与"方法论原因"）

**直接原因**
1. **防御性策略替代了叙事**：为规避肢体崩坏，只拍"瞬间 + 反应"，把交手整体砍掉〔委托方实证·A2〕。生成器风险被转嫁成了观众损失。
2. **打与被打不在同一次生成里**：出招与受击分两镜，接触本身从不出现；外部做法相反——动作与反应同框〔外部调研·S-STORY-16，成龙原则第 4 条"动作与反应在同一画面"〕。
3. **接触只写一个动词**：H3 双人接触镜只写一个动词时物理/戏剧评分最差（2.2/5、2.2/5）；一镜写全"接近—接触—施力—结果"最好（5/4/4）〔外部调研·S-PIPE-03〕。
4. **一镜只放一个简单动作 + 帧数下限 = 慢镜**：H3 镜 ≥124 帧（5.17s），若只装一个出招，模型把"时长读成事件速度"，一招被拉成月球重力〔外部调研·S-H3-11〕——这正是「全是几个简单动作的慢镜头」的生成机制〔学院推断：验证法=同起始帧、158 帧，A 写单招、B 写三招 + 后果，各 3 seed，用 `contact_sheet.py` 数"预备→接触"所占帧数，A 显著更长则成立〕。详见 [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)。

**方法论原因**
5. **把"拍数少"误读成"打击少"**：P10 的"段内 2–3 拍"与 A5 的"拍太多 → 空间跳变"被一并理解为"动作要少"。学院裁决（R4）：区分三种拍——**空间拍**（位置/朝向/相对站位改变）≤2–3/镜；**表情拍** ≤2–3/镜；**打击拍**（原地攻防）可以密〔外部调研·S-H3-09：约 3 秒写 8–9 招，4 份提示词 × 2 seed 全部按顺序、真速度打出，作者标 partly，置信度低〕。
6. **没有动作设计阶段**：打斗直接从剧本一句"二人激战"跳到视频提示词，没有七相动作链、交手回合、战术链这层设计；病灶在预制作，却在生成阶段补〔委托方实证·G7；见 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) 路由表"打斗缺席 → 1 动作设计"〕。
7. **写招式而不是写处境**：中文动作理论的顺序是"规定情境 + 人物性格 → 套招"〔外部调研·S-STORY-32，仅书目〕；成龙原则"先处劣势""利用环境"〔外部调研·S-STORY-16〕；港片用场地道具升级打斗〔外部调研·S-STORY-19〕。没有处境，就没有"逻辑"。
8. **写了模型做不出的编排**：精确拦截、三步以上手部编排链、厘米级位移是高风险写法；应写高频整体动作与接触点〔外部调研·S-ZEN-25〕。这一点恰恰是委托方担心崩坏的真正可控面——**改写法，不是砍打斗**。

## 修正过程（做了什么、第几轮、结果）

1. 委托方提出的修正：细粒度动作链 + 真实接触（七相：意图 intention → 预备 anticipation → 发力 exertion → 接触 contact → 反应 reaction → 回收 recovery → 后果 consequence）；打斗写成战术链（诱敌→落空→抓隙→狂暴→闪避→击飞）而不是抽象描述〔委托方实证·A2〕。
2. r1→r5 实验期间，这套方法论逐步形成，但每轮修复是"打地鼠"式的〔委托方实证·F3〕；A2 **未闭环**。
3. 学院补强（〔学院推断〕，验证法见判据）：
   - **每个 H3 动作镜 = 一组港式套招**：三个流畅动作 + 第四个动作作桥接，下一镜从第四个动作的姿态开始〔外部调研·S-STORY-17〕；每个新镜从上一镜最后一击开始〔外部调研·S-STORY-21〕。
   - **节奏用停-爆-停**：静止对峙 → 一串爆发 → 定格反应；每个镜头先做到"不可能看错"〔外部调研·S-STORY-18〕。
   - **接触写全四段**：`approaches → makes contact → drives through → result`，并给可见后果（退步、兵器脱手、地裂）〔外部调研·S-PIPE-03；委托方实证·M3〕。
   - **"拆武打戏的理由改成换角度，而不是节拍太多"**〔外部调研·S-H3-09〕：同一次命中可从两个角度各生成一次，剪辑时动作重叠接〔外部调研·S-STORY-16"两次好击打 = 一次伟大击打"；具体做法为学院推导〕。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [目视] 剧本承诺的每场打斗，至少一个镜头内**同框可见**完整交手回合（我攻 → 你挡/闪 → 我变招），含接触与反应；证据：`contact_sheet.py` 接触表上标出攻/挡/变招的格号。〔A2〕→ video 清单（阻断）
2. [目视] 动作设计文档里每场打斗有战术链（≥3 环，`→` 串联）+ 每次接触的七相中至少"预备 → 发力 → 接触 → 反应 → 后果"五相；写不出战术链 = 只有动作没有逻辑。〔A2〕→ storyboard 清单
3. [自动] 分镜 `拍数` 只计空间拍 + 表情拍：`segment_rhythm.py` 对打斗段报的 P10-beats-chain（info，链节数 ≠ 拍数）是预期结果，**禁止**为消掉它把打击拍计入 `拍数`（那会触发 A5-beats-many 并误导减拍）。〔A2、A5③、R4〕→ storyboard 清单
4. [自动] 打斗镜提示词含 strike/slash/punch/kick/block/dodge 等动作词时，`prompt_lint.py` 的 VP-realtime 必须为 0 error（含 `Real-time speed throughout, no slow motion`）。〔A2、A3〕→ video-prompt 清单
5. [目视] 提示词中每次接触写全"接近—接触—施力—结果"，禁止单动词接触（`he hits the god`）；出招与受击写在同一次生成、双人同框中全景以上。〔A2；外部调研·S-PIPE-03、S-STORY-16〕→ video-prompt 清单
6. [目视] 每次接触后画面里有可见后果（位移、失衡、道具/环境变化），不是只有特效光。〔A2、M3〕→ video 清单
7. [冷观众] 冷观众能复述打斗的战术链（谁先出手、怎么落空、怎么反制、为什么赢）；只能说"他们打了一架" = 不通过。〔A2；学院推断：阈值沿用 definition-of-done L1 的 2/3 规则，待首次冷观众测试校准〕→ final-cut 清单

## → 行为改变（下次……）

- 下次剧本出现打斗时，**先**在预制作写 `action-design.md`：处境（谁处劣势、场地里有什么可用）→ 战术链 → 每次接触的七相；**再**分镜；禁止从"激战"一词直接写视频提示词。
- 下次担心肢体崩坏时，**改为**改写法（高频整体动作、接触点、中远景双人同框、写全四段接触），**禁止**用"瞬间 + 反应镜头"替代交手。
- 下次排打斗镜时，按"三招 + 一桥"装满一次生成；下一镜的起始帧取上一镜第四个动作的姿态；拆镜理由只能是"换角度"，不能是"招太多"。
- 下次被要求"减拍"时，**先**问减的是哪种拍：减空间拍（换边、绕后、翻滚换向），**保留**打击拍。
- 下次听到"没有打斗逻辑"，**禁止**加招式；**改为**补因果链与后果，并做 A/B 两版（补战术链版 vs 补环境后果版）让人类选（G6）。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ "含蓄 ≠ 缺席"、交手回合、七相、战术链对一切对抗戏成立：武打、枪战、追逐、争吵中的推搡（掌掴宜一镜写全〔外部调研·S-PIPE-03〕）。
- ★ 打击拍 vs 空间拍的区分对任何首帧驱动模型成立；但"打击拍可以密"的外部证据样本小（S-H3-09 标 partly），换模型/换场景前先用 2 seed 小样复测。
- ☆ 部分模型官方建议"优先慢、轻、连续的小动作，避免冲刺、大跳、剧烈翻滚"〔外部调研·S-VGEN-11〕——换到这类模型时，打击拍密度要先测；但仍不得退回"不打"，而是改为分段生成再剪。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/action-choreography/SKILL.md`](../../20-craft/action-choreography/SKILL.md)（七相、交手回合、战术链、三招一桥）、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（拍数口径）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（接触四段写法、实时速度句）、[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)（反馈翻译）。
- 理论：[`10-theory/04-action-design.md`](../../10-theory/04-action-design.md)、[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)。
- 判据清单：[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)。
- 脚本：[`50-rubrics/scripts/segment_rhythm.py`](../../50-rubrics/scripts/segment_rhythm.py)、[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-02.md`](../../60-casebook/drills/DR-02.md)（打斗缺席）、[`60-casebook/drills/DR-21.md`](../../60-casebook/drills/DR-21.md)（反馈翻译："打斗逻辑"）。
- 相邻案例：[`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)、[`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)、[`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)、[`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)。
