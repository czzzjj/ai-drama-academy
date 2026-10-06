# 13 · 表演指导：把情绪翻译成可拍的身体变化

> 一句话世界模型：生成器不会"演"，只会执行看得见的身体变化。给角色一个任务动词，把情绪拆成按生理顺序发生的"从 A 到 B"（眉 → 眼 → 嘴 → 呼吸 → 肩、手），每镜不超过 2–3 个表情拍；不说话的人闭嘴，静止的人也要呼吸、眨眼。拿不准的时候，用中性脸加上下文镜，让观众自己读出情绪（库里肖夫） ｜ 浓缩案例：GAP-5, A5, D3, F2, F4 ｜ 对应技能：performance-direction, video-prompting-h3, keyframe-freeze, storyboard-long-take, edit-and-assemble, shot-qc

> 证据等级：委托方在表演指导上是空白，"如何用提示词驱动微表情、呼吸、身体语言，只有零散经验"〔委托方实证·GAP-5〕。H3 官方提示词文档没有表情章节〔外部调研·S-H3-09〕，评测也指出它在多镜头中角色表情偏少〔外部调研·F-CASE-10〕。本篇的写法全部来自外部调研（多为其他模型或小样本），在 H3 上一律视为待复测假设。

## 核心判决

**T13.1 · 演动作，不演情绪。每个有表演的镜，先给角色定一个任务动词（说服、逼问、试探、隐瞒、求饶），再从动词推出身体动作；禁止把 sad、angry、happy、scared 这类裸情绪词当表情指令。**
为什么：Weston 的原话是 "Although we can't decide how to feel, we can decide what to do."，所以要给可以演的动作 "to persuade, to plead, or even to belittle"〔外部调研·F-CRAFT-15〕。斯坦尼斯拉夫斯基把任务称为 "a decoy for feeling"〔外部调研·F-CRAFT-16〕。基础情绪词 "usually results in over-exaggerated, cartoonish expressions"〔外部调研·F-CRAFT-17〕。对应判据 R-PRF-01。

**T13.2 · 不可见的内心状态（"神色一凛""心中一震"）必须翻译成看得见的身体部位变化，否则等于没写。** 翻译用下文的"情绪 → 可拍动作表"。
为什么：zenstory 把"不可见内部状态"列为四类高风险写法之一，要求改写成日常高频的整体动作组合〔外部调研·F-ZEN-27〕；提示词要用 throat、jaw、lip corner、brow 这类解剖部位词〔外部调研·F-CRAFT-18〕。

**T13.3 · 表情写成变化，不写成状态：每个表情拍写"从 A 到 B"，并写明镜末停在什么状态。**
为什么：社区实测的有效写法是 `expression shifts from blank and neutral into dawning realization and slight shock ... settling into a held, wide-eyed stillness by the end`〔外部调研·S-H3-08〕；"The strongest part…is not the largest smile. It is the transition into it."，情绪弧分为压抑 → 泄露 → 释放 → 恢复，最后几秒必须有明确收束〔外部调研·S-CRAFT-20〕。对应判据 R-PRF-02。

**T13.4 · 按生理顺序写：眉 → 眼 → 嘴，真笑先到眼睛；同时写出"不准动的部位"，防止模型自动补一个笑。情绪转换可以藏在遮蔽里（闭眼 → 变化 → 睁眼），并先往反方向走一拍。**
为什么：这套生理顺序、"不准动部位"清单和遮蔽转换都出自一部 9:16 Ref2VA 连载短剧的分镜表演技能〔外部调研·S-H3-09〕。对应判据 R-PRF-03。

**T13.5 · 一镜最多 2–3 个表情拍，超过就拆：拆成同一次生成里的多个 `[Shot]`，或拆成多次生成。武打的打击拍不受这个上限约束（R4）。**
为什么：7 秒特写写了 9 拍，相邻帧 PSNR 37–42 dB，脸基本没动；拆成三颗 2–3 秒的镜，降到 22–23 dB，表情都到位了〔外部调研·F-H3-16〕。打击拍可以密：8–9 招按顺序、按真速度打完〔外部调研·F-H3-17〕。拍太多也是空间混乱的根因之一〔委托方实证·A5③〕。对应判据 R-PRF-04、R-PRF-08。

**T13.6 · 反应镜按公式写：先点名情绪，再写两处在当前景别下看得见的泄露，最后写"约 1.5 秒内落下，然后定住"。** 点名情绪词是允许的，前提是它后面跟着可见泄露；T13.1 禁止的是只有情绪词。
为什么：这种写法单模型盲评清晰 3.9/5、自然 4.0/5；只写情绪词，自然度 2.8；逐段写可见反应链，强度只有 1.9〔外部调研·F-ZEN-12〕。〔学院推断：样本小，而且评判者是同一个模型，不是独立人评。验证法：同一反应镜按三种写法各出 3 个 seed，请独立评审盲评。〕

**T13.7 · 画面里有 ≥2 人、而且有对白时，不说话的人必须写闭嘴句，或者让他背身、出画。H3 会把整颗镜当作说话人的镜，说完话后的眨眼、吞咽放到下一镜去。**
为什么：不写闭嘴句，3 次中有 2 次口型落在不说话的人脸上；加上 "does not speak; his lips remain completely closed"，3/3 正确；不说话的人背身或出画时，12/12 正确〔外部调研·F-ZEN-08〕。画外音也要跟一句嘴唇闭合句〔外部调研·F-ZEN-04〕。H3 会把整颗镜都当成那个人在说话〔外部调研·S-H3-09〕。`prompt_lint.py` 报 `VP-lipsync`。对应判据 R-PRF-05。

**T13.8 · 静止 ≠ 冻结。静着的人要写呼吸、眨眼、重心微移；禁止写 `completely still` 和 "holds one pose completely rigid"。**
为什么：可用的写法是 `standing in place, breathing softly, hair and clothing stirring in the air, blinking and shifting her weight a little as people naturally do`〔外部调研·S-H3-08〕；`completely still` 在禁用字表上〔外部调研·S-H3-09〕；"holds one single pose completely rigid" 让整镜运镜位移从 98–108% 画宽掉到 22%〔外部调研·F-H3-15〕；社区还报告 H3 几乎不眨眼〔外部调研·S-H3-13〕。

**T13.9 · 每个有表演的镜都要写视线目标：看谁、看哪儿，直视、回避还是扫视。多人镜的视线方向必须和起始帧方位一致（画面左的人看向画面右）。**
为什么：如果要看的东西不在画面里，人物就会看镜头〔外部调研·S-H3-09〕；视线是表情的一部分，"lost in thought" 和直视镜头是两种完全不同的戏〔外部调研·S-CRAFT-21〕；方位由起始帧钉死〔委托方实证·A5①〕。对应判据 R-PRF-06。

**T13.10 · 微表情特写只用固定机位，不叠加运镜：`static, on a tripod, with no camera movement whatsoever`。**
为什么：Seedance 微表情案例要求 "locked-off camera, static shot, no panning, no zoom"，因为运动会掩盖脸部的不一致〔外部调研·F-CRAFT-18〕；H3 的运镜作用于整次生成，表情镜里的运镜会和表情抢预算〔外部调研·S-H3-09〕。对应判据 R-PRF-09。

**T13.11 · 拿不准的时候，用中性脸加上下文镜（看见了什么），让观众自己读，而不是硬写一个夸张表情。表演的最后一步靠剪辑：反应慢半拍就用插入镜盖过去，转折太平就把两端拉近、中间插一刀。**
为什么：库里肖夫效应：同一张无表情的脸接不同画面，观众读出不同情绪，"the face was exactly the same"；2016 年 36 名被试的实验再次确认〔外部调研·F-STORY-16〕。AI 会把情绪推到极端〔外部调研·F-CRAFT-17〕。"改四版的成本远高于剪一次"〔外部调研·S-H3-09〕。

**T13.12 · 表演是观众最先骂 AI 剧的地方，所以它是首要验收项，地位高于画质。验收看两条：每个情绪转折至少落在一个可见的形体动作上；冷观众能说出角色此刻"想要什么"。**
为什么：《山海奇镜》的差评集中在"面部表情太僵硬""没有灵魂"〔外部调研·F-CASE-02〕；《三星堆·未来启示录》要靠持续的人工干预才保住"表情细腻"〔外部调研·F-CASE-04〕；红果 2026-07 起，对 AI 仿真人剧的"表情变化"门槛更高〔外部调研·F-PLAT-15〕。委托方的教训是：指标全绿不等于观感达标〔委托方实证·F2〕。对应判据 R-PRF-07、R-PRF-10。

## 机制解释

1. **为什么情绪词会失败。** 情绪词是对结果的概括，不是动作。模型只能把它映射成训练数据里最典型的样子，也就是夸张的表情包脸；要么就被其他指令平均掉，脸不动。身体部位加方向（"inner brows draw together"）是可以执行、也可以核对的目标。
2. **为什么拍数有上限。** 一次生成要在 5–15 秒内分配全部变化。表情拍太多，每一拍分到的帧不够把变化做完，模型会取平均值，于是"每一拍都做了一点，合起来等于没动"（F-H3-16 的 37–42 dB）。打击拍不同：它是全身大幅度、高频的动作，训练数据里本来就密。
3. **为什么生理顺序有效。** 真实表情从上往下展开，而且眼睛先于嘴。按这个顺序写，模型拿到的是一条有因果的动作链，而不是同时发生的几个状态。"不准动的部位"用来堵住模型自动补全的习惯（嘴一动，就顺带补出一个笑）。
4. **为什么中性脸更稳。** 观众读情绪靠上下文，不只靠脸（库里肖夫）。生成器最不稳定的就是大幅度表情（变形、恐怖谷），最稳定的是微小变化和中性状态。把情绪的重量从脸上移到"上下文镜 + 剪辑节奏"上，就是避开模型的短板。
5. **为什么口型会落错人。** H3 的声音是对的，但口型会落在画面里最显眼的正脸上〔外部调研·F-PIPE-10〕，所以必须明确告诉它谁闭嘴，或者把不说话的人从正脸位置移开。

## 本管线下的变体

**情绪 → 可拍动作表**（前三行出自 S-H3-09，第四行出自 S-CRAFT-20，其余是〔学院推断：词汇综合自 S-CRAFT-20 / S-CRAFT-21，需在 H3 上用 R-PRF-08 的 PSNR 法复测〕）

| 情绪 | 可拍的变化链（按顺序） | 提示词片段（EN） |
|---|---|---|
| 困惑 | 眉头内侧聚拢下压 → 头偏约 10° → 视线在两点之间来回一次 | `her inner brows draw together and down, her head tilts slightly, her eyes flick once between the letter and his face` |
| 震惊 | 头往后一缩 → 上眼睑全开 → 吸气，肩停在高处 | `his head jerks back slightly, his upper eyelids fly fully open, he sucks in a breath and his shoulders freeze high` |
| 释然 | 眉松 → 吐气 → 肩落 → 眼神重新聚焦 → 嘴角上扬 | `her brows unknit, she lets out a long breath, her shoulders drop, her eyes refocus on him, and only then the corners of her mouth lift` |
| 压抑 | 嘴唇压紧，视线受控 → 喉部吞咽 | `her lips press together while her gaze remains controlled; her throat moves as she swallows` |
| 克制的愤怒 | 下颌收紧 → 鼻腔短促呼气 → 指节攥白 | `his jaw tightens, a short exhale through the nose, his knuckles whiten around the hilt` |
| 恐惧 | 屏息 → 视线躲向门口 → 身体后让半步 | `she holds her breath, her gaze darts to the door, she leans back half a step` |
| 决意 | 慢慢抬眼 → 视线定住不眨 → 下颌收紧 | `she slowly raises her eyes and holds an unblinking stare, her jaw set` |
| 心虚、隐瞒 | 视线滑开 → 挤出一个没到眼睛的笑 | `his gaze slides away, a forced smile that does not reach his eyes` |

**表演卡（每个有表演的镜一张，写在分镜旁；字段是〔学院推断〕，综合自 S-CRAFT-18、S-CRAFT-19、S-CRAFT-20）**
任务动词（一个）｜ 阻碍 ｜ 表情拍（≤3 个，每个都写成"从 A 到 B"，按生理顺序）｜ 视线目标 ｜ 呼吸 ｜ 形体动作（至少一个）｜ 不准动的部位 ｜ 镜末收束状态。任务动词往上追溯到季圣经里角色的最高任务（F-CRAFT-16，见 [`10-theory/14-season-architecture.md`](14-season-architecture.md)）。

**H3 写法要点**
- 反应镜（T13.6）：`(S2) is visibly stunned: her eyes widen and her breath catches; within about one and a half seconds her face settles and holds still, eyes fixed on the blade.`
- 非说话人：`(S2) does not speak; her lips remain completely closed.`（R-PRF-05）
- 对白镜要给表演留白：台词按 4.1 字/秒的规划语速排时长，不按 7.5 字/秒的上限塞满（R3），留出开口前和说完后的反应时间（D3、F-ZEN-06）。对白塞满整镜，表演就没有呼吸。
- 镜内拆表情拍：同一次生成里写 `[Shot 1]`、`[Shot 2] At 00:03.000`，整颗机位静止，每个切点挂关键帧（见 [`10-theory/06-long-take-multi-beat.md`](06-long-take-multi-beat.md) T06.8）。

**三类镜的表演写法差异**

| 镜类 | 表演预算 | 写法要点 | 主要风险 |
|---|---|---|---|
| 反应镜（无对白） | 1–2 个表情拍 | T13.6 公式；锁机位；视线落在刺激物上 | 脸不动（PSNR 过高），或表情夸张 |
| 对白镜 | ≤1 个表情拍，加说完后的一拍反应 | 台词按 4.1 字/秒排时长；写非说话人闭嘴句；"说完后"的拍子放到下一镜 | 赶词、口型落错人、没有呼吸 |
| 动作镜 | 表情拍 ≤1，打击拍可以密 | 表情写在动作的起点和后果相（咬牙发力、受击后的喘息），不写在中段 | 动作中段的表情会被运动抹掉 |

**验收**
- 表情是否真的发生：`python3 50-rubrics/scripts/psnr_scan.py clip.mp4 --json`，读 `P8-psnr-stats` 的中位 PSNR。表情镜中位值 ≥37 dB，说明脸基本没动（R-PRF-08，阈值待本管线复测）；整颗都报 `P8-freeze`，按冻结处理。
- 口型落在谁脸上：`python3 50-rubrics/scripts/contact_sheet.py clip.mp4 --crop mouth=X:Y:W:H`，逐格看嘴。单格静帧不能用来判定动作〔外部调研·S-H3-09〕。
- 读不读得出：冷观众说出角色此刻"想要什么"，与表演卡上的任务动词一致（R-PRF-10，见 [`20-craft/cold-audience-test/SKILL.md`](../20-craft/cold-audience-test/SKILL.md)）。

## 常见误用

| 误用 | 后果 | 案例卡 |
|---|---|---|
| 写 "she looks sad / angry"，或写"神色一凛" | 表情包式夸张，或者脸不动 | [`60-casebook/cards/F4-skills-not-ability.md`](../60-casebook/cards/F4-skills-not-ability.md)（套用了词汇，能力没有落地） |
| 一镜塞 5 个以上表情拍 | 被平均抹平，PSNR 37–42 dB | [`60-casebook/cards/A5-spatial-chaos.md`](../60-casebook/cards/A5-spatial-chaos.md)（拍太多，同一个病根） |
| 台词塞满整镜，没留反应和呼吸 | 赶词，表演没有落点，说完的拍子被截掉 | [`60-casebook/cards/D3-dialogue-capacity.md`](../60-casebook/cards/D3-dialogue-capacity.md) |
| 表情特写叠一个推镜"增加电影感" | 运动吃掉表情；运镜没有动机 | [`60-casebook/cards/A4-unmotivated-camera.md`](../60-casebook/cards/A4-unmotivated-camera.md) |
| 看一张静帧就判"表情到位了" | 单格不能判动作，验收放水 | [`60-casebook/cards/C2-lenient-acceptance.md`](../60-casebook/cards/C2-lenient-acceptance.md) |
| 表演不对就整镜重抽四版 | 成本高于剪一刀；修点不修面 | [`60-casebook/cards/F3-patch-iteration.md`](../60-casebook/cards/F3-patch-iteration.md) |
| 多人对白镜只写说话人，不写其他人在干什么 | 口型落错人，其他人僵住或看镜头 | — （F-ZEN-08，R-PRF-05） |
| 情绪全靠大特写的脸，不给上下文镜 | 脸部变形或恐怖谷，观众读不出原因 | — （T13.11） |
| "表演"这一维不在自查清单里，技术全绿就交付 | 观众说"没有灵魂" | [`60-casebook/cards/F2-proxy-metrics.md`](../60-casebook/cards/F2-proxy-metrics.md) |

## → 行为改变

1. 下次写有人物的镜，**先**填表演卡（任务动词、视线、呼吸、形体动作、不准动的部位、镜末状态），**再**写提示词。提示词写完，grep 一遍 sad / angry / happy / scared / upset，命中的改写成"从 A 到 B"的部位变化链（R-PRF-01、R-PRF-02）。
2. 下次数拍，表情拍超过 3 个就拆成多个 `[Shot]` 或多次生成；拆的理由写进分镜（R-PRF-04）。
3. 下次写反应镜，按"点名情绪 + 两处可见泄露 + 约 1.5 秒内落下定住"的公式写，并把它当作待复测假设，记录 seed 和结果（T13.6）。
4. 下次画面里有 ≥2 人并且有对白，每个不说话的人都写闭嘴句；能让他背身或出画的，优先这样做（R-PRF-05）。
5. 下次写静止的人物，改写成呼吸、眨眼、重心微移；**禁止** `completely still`（T13.8）。
6. 下次遇到情绪特写拿不准，**改为**中性脸加一颗上下文镜（看到的东西），在剪辑里决定节奏，不靠重抽来追表情（T13.11）。
7. 下次验收表情镜，用 `psnr_scan.py` 的中位 PSNR 和嘴部裁剪接触表留证据；交付前请冷观众或独立评审说出角色"想要什么"（R-PRF-08、R-PRF-10）。

## 自测

1. 判断：反应镜里出现了 "stunned" 这个情绪词，违反了 T13.1，必须删掉。
<details><summary>答案</summary>错。T13.1 禁止的是**只有**情绪词。T13.6 的反应镜公式本来就是"点名情绪 + 两处可见泄露 + 约 1.5 秒内落下定住"，盲评中优于只写情绪词（自然度 4.0 对 2.8，F-ZEN-12）。只要情绪词后面跟着可见泄露，就保留。</details>

2. 简答：一颗 8s 特写写着"她先疑惑，然后震惊，接着愤怒，最后强忍泪水，转身离开"。指出问题并给出改法。
<details><summary>答案</summary>① 4 个表情拍再加一个空间拍（转身），超过 2–3 拍的上限，会被平均抹平（F-H3-16，R-PRF-04）；② 全是情绪名词，没有身体部位变化（T13.1、T13.2）。改法：拆成两颗：第一颗"困惑 → 震惊"，按眉 → 眼 → 嘴写变化链，锁机位；第二颗"压抑 → 转身"，写嘴唇压紧、喉部吞咽、转身。"愤怒"这一拍能删就删，或者交给中性脸加上下文镜。每颗写镜末收束状态。</details>

3. 简答：两人对话镜生成后，台词是 S1 说的，嘴却在 S2 脸上动。原因是什么？怎么修？
<details><summary>答案</summary>口型会落到画面里最显眼的正脸上（F-PIPE-10）。修法：加 `(S2) does not speak; her lips remain completely closed.`（3/3 正确，F-ZEN-08），或者让 S2 背身、出画（12/12）。验收时用 `contact_sheet.py --crop` 截嘴部逐格看（R-PRF-05）。</details>

4. 判断：为了让角色"定住"产生压迫感，提示词写 "she holds one single pose completely rigid"，这是精确的表演指令。
<details><summary>答案</summary>错。这是不可能完成的指令，会拖垮整镜：运镜位移从 98–108% 画宽掉到 22%（F-H3-15）；`completely still` 也在禁用字表上（S-H3-09）。改写成呼吸、眨眼、重心微移；压迫感交给机位、光比（见 12 篇）和对手的动作。</details>

5. 简答：人类看完说"表演没有灵魂"，可本镜各项技术检查全绿。按本篇，依次查什么？
<details><summary>答案</summary>① 表演卡有没有任务动词，冷观众能不能说出角色"想要什么"（R-PRF-10）；② 中位 PSNR 是否 ≥37 dB，也就是脸到底动没动（R-PRF-08）；③ 表情拍是不是超过 3 个（R-PRF-04）；④ 情绪转折有没有落在形体动作上（R-PRF-07）；⑤ 视线目标是否写明、是否在看镜头（R-PRF-06）；⑥ 对白是否塞满整镜，没给反应留白（D3）。把这类笼统反馈拆成可查维度的方法，与 DR-21（反馈翻译）相同。</details>
