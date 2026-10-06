# 11 · 声音设计：分层、静场与剪辑点

> 一句话世界模型：H3 在同一次生成里联合建模人声、音效和音乐，产出的声轨只能往上叠，不能拆轨。所以生成阶段只要三样：干净的对白、≤3 个点名声源、无配乐。层次、连续环境、静场和配乐全部放到后期，按"对白 → 环境 → 拟音 → 设计音效 → 音乐"的顺序重建，并和剪辑点对齐 ｜ 浓缩案例：GAP-3, GAP-6, D5, D3, A1, A3 ｜ 对应技能：sound-design, edit-and-assemble, video-prompting-h3, shot-qc

> 证据等级：委托方只做过"对白 + 基础拟音 + 非叙事配乐"〔委托方实证·GAP-3〕，没有做过分层声音设计，也没有节拍↔剪辑点的方法〔委托方实证·GAP-6〕。本篇只有 D3、D5、T-4、A1、A3 是委托方实证，其余都是〔外部调研〕或〔学院推断〕，禁止写成"经验表明"。

## 核心判决

**T11.1 · 不写音乐字段 ≠ 无配乐。每条生成提示词都必须显式写 `non_diegetic_music: N/A`。** 唯一例外：这一颗本身就是设计好的音乐段落（如 MV 式蒙太奇），而且整场只有这一颗。
为什么：显式写 N/A 的 14 次都没有配乐，省略的 3 次中有 2 次自带了配乐〔外部调研·F-ZEN-07〕；"不写声音字段不等于静音"〔外部调研·S-H3-11〕。每颗自带的配乐都会在剪点处换调、换速，把 A1 的"片段式"放大〔委托方实证·A1；学院推断，验证法见 R-SND-06〕。`prompt_lint.py` 对空 `non_diegetic_music` 报 `VP-music`。

**T11.2 · 生成声轨不能拆，只能叠。所以 `overall_soundscape` 最多点名 3 个声源：对白、1 个关键动作声、1 条环境床；更细的层留给后期素材库。**
为什么：H3 官方原文 "No separation between voice, sound effects, and music — all jointly modeled"〔外部调研·F-CRAFT-11〕。写进去的声源都会被生成出来：音频槽写 "drone" 会带出低频轰鸣〔外部调研·S-H3-08〕；声景写门铃和开门，4 次中有 3 次把景别拉成了远景〔外部调研·S-ZEN-17〕。也就是说，声音词连画面都会改。"3"这个上限来自 Murch 的同类声 2.5 层律〔外部调研·F-CRAFT-05〕，对应判据 R-SND-02。

**T11.3 · 后期按固定顺序搭建：静音看一遍、列"缺失清单" → 对白 → 环境床 → 拟音 → 设计音效/冲击声 → 音乐 → 总线平衡。** 不许倒过来做：先铺音乐，会把缺掉的环境声和拟音盖住。
为什么：这是 Krotos 七部分模型给出的搭建顺序〔外部调研·S-CRAFT-02〕；给 AI 视频补声音，第一步是静音看片，写下 "what's absent"，最后一步是记录配方（工具、提示词、参数）〔外部调研·F-CRAFT-07〕。

**T11.4 · 密度有上限。同一时刻同类声 ≤2 层；可分辨的声源总数 ≤5 层，并且要分散在"对白—音效—音乐"光谱上。戏剧焦点切换时，必须撤掉一层。**
为什么：Murch 说 "three is the borderline"。声音都挤在光谱同一区域时，只有约 2.5 层能分辨；均匀分布时上限约 5 层。《现代启示录》终混时同一时刻最多保留五层，各层按戏剧焦点隐现〔外部调研·F-CRAFT-05〕。另有原文 "Less is often more; avoid treating every action with an equal-weight sound layer."〔外部调研·S-CRAFT-02〕。手机外放下上限是否仍为 5 层，目前是〔学院推断：做 3/5/7 层三个混音版本，请冷观众复述能分辨的声源〕。

**T11.5 · 静场是要设计的一层，不是什么都不放。每个爆发段之后留 ≥1s 余波静场：撤掉音乐，只留环境床、呼吸或余响。静场要有 room tone，不能是数字零。**
为什么：A3 的修正要求段内有速度层次，"冲刺快切 → 对峙慢推 → 爆发一击 → 余波静场"〔委托方实证·A3〕；撤掉一层本身就是强调（T11.4）。数字零放在剪点上，听起来像"掉了个洞"〔学院推断：用 silencedetect 列出 < -60 dB 且 ≥0.5s 的段，逐条对照 `sound-plan.md` 的静场登记，见 R-SND-01、R-SND-07〕。

**T11.6 · 剪点靠声音缝合。对白场默认至少一处约 0.5s 的 L-cut 切到听者；换场用 0.5–2s 的 J-cut 让下一场的声音先进来；环境床跨切点做交叉淡化。**
为什么：J/L-cut 的时长经验，以及"两人对话默认用 L-cut 切到听者，好的表演在反应里"〔外部调研·F-CRAFT-06〕；"A well-placed ambience swell or whoosh can hide a jump cut and make two disparate shots read as one continuous action."〔外部调研·S-CRAFT-02〕。原生音频短段之间综合响度相差 8.9 LU，0.5s 边界上 RMS 跳变超过 30 dB〔外部调研·F-PIPE-02〕。不缝的话，每个剪点都会被耳朵听成"换了一个片段"。对应判据 R-SND-05。

**T11.7 · 配乐在后期按场铺一条连续音轨，对白出现时用侧链把音乐压下去；关键切点（接触、爆发一击）落在重拍上，偏差 ≤2 帧。**
为什么：GAP-6 是"没有音乐节拍↔剪辑点的系统方法"〔委托方实证·GAP-6〕；A3 的修正明确要求"音乐节拍对齐切点"〔委托方实证·A3〕；音乐要 "matched to the beat, not the whole scene"〔外部调研·S-CRAFT-03〕；让位（ducking）用 ffmpeg `sidechaincompress`〔外部调研·F-CRAFT-04〕。"后期铺一条轨能消除剪点处的音乐断裂"目前仍是推断〔学院推断：同一场分别做"逐镜生成配乐"和"后期一条轨"两版，独立评审盲听并记录断裂次数，见 R-SND-06、R-SND-03〕。

**T11.8 · 字幕文字一律取自剧本，转写只用来定位时间和查缺句。要判"多了一句/少了一句/错了一字"，必须有双通道证据：转写，加上抽帧看嘴或亲耳听。**
为什么：转写工具在无对白镜上幻觉出"字幕by索兰娅"，还把一声低笑的气声误听成"救我"〔委托方实证·D5〕；这类句子原样出现在 Whisper 喂噪声得到的公开幻觉数据集里〔外部调研·F-COMFY-15〕；实跑中"诸君，且听龙吟"被转成了"朱军且听龙银"〔外部调研·F-PIPE-12〕。H3 片头约 0.5s 内会出现乱语或截断〔外部调研·F-H3-24〕，所以剪辑入点放在开口前约 0.25s，出点在台词结束后留约 0.4s〔外部调研·F-ZEN-22〕。

**T11.9 · 先分清对白坏在哪：缺句改时长，赶词、重讲、假起头先换 seed。**
为什么：容量不够属于结构性缺陷，同一镜换 3 个 seed，每次缺的句子都不同〔委托方实证·D3〕；说话节奏绑在 seed 上，同一 seed 换提示词，逐字时间完全一致〔外部调研·F-H3-19〕。另外，音频在采样过程中最后收敛，8 步时音色最弱〔外部调研·F-H3-09〕，所以 turbo 预览里的声音不能作为验收依据。

**T11.10 · 每个说话角色全季绑定一个固定的音色来源（参考音频或外配音色 ID）。同性别的两个说话人盲听分不出来，就改用外配，不要接着赌生成。**
为什么：H3 两个男声的音色相似度约 0.50〔外部调研·S-ZEN-17〕。`ref_audio` 只驱动嘴型和呼吸，生成出来的音高仍偏高约两个半音〔外部调研·S-H3-09〕。有人报告 Ref2VA 挂音频后，身份相似度跌到 0.0884〔外部调研·F-H3-24，他人未复现〕，所以挂音频参考之后必须重做正脸比对。外配可以走 Speech T2A，它给 word 级毫秒时间戳，能直接对齐字幕〔外部调研·F-H3-30〕。音色参考的写法：`<Audio 1> is the voice-timbre reference for <Subject 1> (S1).`〔外部调研·S-ZEN-29〕。对应判据 R-SEA-13、R-SEA-14。

**T11.11 · 响度有好几套口径，不能混用。交付默认整体 -16 LUFS ±1、真峰 ≤ -1 dBTP，另加一条"对白段与整体响度相差 ≤5 LU"；两遍 loudnorm 之后，测编码成品的实际值。**
为什么：委托方已按 -16 LUFS 交付〔委托方实证·T-4〕，这个值落在 GY/T 377 的 -15 LKFS ±2 LU 范围内，该标准还要求真峰 ≤ -1 dBTP〔外部调研·F-COMFY-11〕。EBU R128 的 -23 是广播口径〔外部调研·F-CRAFT-02〕；AES TD1008 的语音 -18 / 音乐 -16 是平台归一化用的，不是交付目标〔外部调研·F-CRAFT-03〕。整体达标不等于台词清楚：Netflix 发现按全节目测量合规的内容，对白集中在 -27 左右，建议 LSR ≤5 LU〔外部调研·F-CRAFT-01〕。单遍 loudnorm 实测落在 -12.33，两遍才到 -15.79〔外部调研·F-ZEN-21〕。对应判据 R-SND-09。

**T11.12 · 每条非生成的音乐、音效都要进许可台账。默认禁用：BBC RemArc 音效、任何 NC 或 ND 曲目、在 YouTube 以外使用的 YouTube 音频库标准曲目。**
为什么：CC BY-ND 曲目配到画面上即构成衍生作品〔外部调研·F-CRAFT-20〕；BBC RemArc 许可禁止上传社交平台〔外部调研·F-CRAFT-26〕；Freesound 只有 CC0 和 CC BY 可以商用〔外部调研·F-CRAFT-21〕；Sonniss 可商用、免署名，但禁止用于 AI 训练〔外部调研·F-CRAFT-22〕；Pixabay 可商用、免署名〔外部调研·F-CRAFT-25〕；YouTube 音频库官方页没有说明能否在站外使用〔外部调研·F-CRAFT-23〕。MiniMax Music 3 的许可存在冲突：[`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) 第四部分按 CC BY-NC 处理，认定不可商用；F-H3-31 核对的结果是 Music3 社区许可，允许商用，但有 2000 万美元收入门槛和 UI 署名要求。裁决更新之前，一律按不可商用处理，使用前上报人类拍板点④（R-PUB-12）。对应判据 R-SND-10。

## 机制解释

1. **为什么同一 pass 出的声音反而要在后期重建。** 联合建模意味着每一颗的声音都是独立随机出来的：环境床的音色、底噪、混响，在每个剪点都重新抽一次。单颗听没有问题，连起来就是"每 8 秒换一个房间"。这是 A1"片段式"在听觉上的版本：画面碎，声音也碎。修法不是让生成更准，而是在后期铺一条跨切点的连续环境床和一条连续配乐，让耳朵把几个片段听成同一场戏（T11.6、T11.7）。
2. **为什么层数有上限。** 在 Murch 的光谱上，对白（Encoded，被"读"）和音乐（Embodied，被"感受"）可以同时成立，因为它们走不同的感知通道；两个同类声音（两种脚步、两种风声）挤在同一区域，就会混成"一群"，每个都失去意义〔外部调研·S-CRAFT-01〕。所以加一层之前要先问：它在光谱的哪个位置？跟谁抢？同一时刻抢同一频段，必须有一个让路〔外部调研·S-CRAFT-03〕。
3. **为什么撤掉一层就是强调。** 观众的注意力按"变化"分配（见 [`10-theory/05-rhythm-engineering.md`](05-rhythm-engineering.md)）。持续高密度没有变化，只会让人疲劳；撤掉一层就是一次变化，注意力会被推到剩下的那一层上（通常是对白或一次击中声）。
4. **为什么剪点要用声音缝。** 画面和声音在同一帧一起切，大脑会收到两次"新想法开始了"的信号。声音提前进来（J）或延后离开（L），大脑收到的是"同一个想法还在继续"〔外部调研·S-CRAFT-04〕。R6"快剪从长镜里取"是让短 CUT 不显碎的第一个工具，声音缝合是第二个。
5. **为什么手机上不能只靠声音传信息。** 超过 30% 的受访者静音观看，依赖字幕〔外部调研·F-PLAT-11〕。钩子、反转、台词要点这类关键信息，必须靠画面加字幕就能看懂；声音负责情绪和连续感，不能是唯一的信息来源（见 [`10-theory/01-vertical-drama-physiology.md`](01-vertical-drama-physiology.md)）。

## 本管线下的变体

**层模型：哪一层在哪个阶段做**

| 层 | 生成阶段（H3 提示词） | 后期 | 素材来源 / 工具 | 判据 |
|---|---|---|---|---|
| 对白 | `<d>[Chinese] …</d>`，由稳定说话人 ID 引出；多人镜加闭嘴句 | 保留生成对白，或整句换成外配；字幕逐字取自剧本 | `dialogue_capacity.py`、`transcript_reconcile.py` | R-PRF-05、R-SEA-13 |
| 环境床 | 只写 1 条，保证生成声轨不是数字零 | 每场一条连续的 room tone 或环境声，跨切点交叉淡化 | Sonniss、Freesound（CC0 / CC BY） | R-SND-01 |
| 拟音 | 最多 1 个关键动作声（接触相的击中声） | 只给画面里看得见的动作配；材质与画面一致；击中声落在接触帧 | Sonniss | R-SND-08 |
| 设计音效 | 不写（whoosh、冲击声、能量声会抢对白，还会改画面） | 用于爆发点、跳切掩护 | Sonniss、Freesound | R-SND-04 |
| 音乐 | `non_diegetic_music: N/A` | 每场一条连续轨；对白处侧链压低；重拍对齐切点 | Pixabay、Incompetech（须署名）、FMA 的 CC BY 曲目 | R-SND-06、R-SND-03 |
| 静场 | 无对白的段落写清"无人说话"；社区绕法是在静默处写 `silently`〔外部调研·S-H3-13，无官方回复〕 | 登记时间码；保留 room tone | silencedetect | R-SND-07 |

**生成阶段写法（Ref2VA 末两段示例，恰好 3 个点名声源）**

```h3
overall_soundscape: Close, dry dialogue from (S1). A steady low wind across the rocky clearing. One sharp crack of steel on stone as the blade hits.
non_diegetic_music: N/A
```

**后期链（只用标准 ffmpeg 滤镜和本仓库脚本）**

1. 静音审片 → `sound-plan.md` 写缺失清单、声音层表（时间码 × 层）、静场登记、配乐轨与节拍时间码、配方（工具 / 提示词 / 参数）。
2. 数字静音段：`ffmpeg -i rough.mp4 -af silencedetect=noise=-60dB:d=0.5 -f null -`，输出逐条对照静场登记（R-SND-01）。
3. 让位：`sidechaincompress` 以对白为侧链输入，默认值是 threshold 0.125、ratio 2、attack 20 ms、release 250 ms〔外部调研·F-CRAFT-04〕，从默认值起调，调完的参数写进 `sound-plan.md`。
4. 响度：第一遍 `loudnorm=print_format=json` 测量，第二遍 `linear=true` 并带上 measured_I / measured_LRA / measured_TP / measured_thresh〔外部调研·F-CRAFT-04〕。
5. 验收：`python3 50-rubrics/scripts/loudness_verify.py final/ep03.mp4 --min 90 --max 110`。注意：脚本只查整体 LUFS、真峰、LRA，**不查对白段与整体的差值**。对白段要单独截出来跑 ebur128，作为 R-SND-09 的证据。
6. 对白对账：剧本 ↔ 视频提示词 ↔ 转写三方对账（P7），用 `transcript_reconcile.py`；有疑点的句子补抽帧看嘴（P8、M10）。

**镜级声音自查（交 shot-qc 之前，逐颗过一遍）**
- `non_diegetic_music: N/A` 已写，`prompt_lint.py` 没有报 `VP-music`（T11.1）。
- `overall_soundscape` 点名的声源 ≤3，而且没有会被画出来的声源词（T11.2）。
- 有 `<d>` 的镜里，没有写 say / sentence / word / line 这类描述"说话"的叙述句，否则这些句子可能被念出来〔外部调研·F-H3-19〕。
- 片头约 0.5s 若有乱语，剪辑入点后移〔外部调研·F-H3-24〕；片尾 1.2–1.7s 的崩解段，画面和声音一起裁掉〔外部调研·F-H3-18〕。
- 无对白镜的音轨先跑 silencedetect，确认没有人声后再决定要不要转写（T11.8）。
- 生成对白和剧本逐字对账：缺句走 T11.9 的"改时长"，赶词或重讲走"换 seed"。

## 常见误用

| 误用 | 后果 | 案例卡 |
|---|---|---|
| 省略 `non_diegetic_music`，或在里面写抽象情绪词 | 每颗自带配乐，剪点处调性和速度跳变，"片段式"被放大 | [`60-casebook/cards/A1-fragmented-shots.md`](../60-casebook/cards/A1-fragmented-shots.md) |
| `overall_soundscape` 里堆风、鸟、人群、钟、脚步、鼓等 5 个以上声源 | 声音互相掩盖；人群声会招来人群画面；声音词把景别拉远 | [`60-casebook/cards/B2-crowd-leak.md`](../60-casebook/cards/B2-crowd-leak.md) |
| 把 ASR 结果直接当字幕，或单凭转写判"多了一句" | 幻觉文字进入字幕，或误判后无谓重出 | [`60-casebook/cards/D5-qc-tools-lie.md`](../60-casebook/cards/D5-qc-tools-lie.md) |
| 对白缺句时反复换 seed | 结构性缺陷，换 seed 无解 | [`60-casebook/cards/D3-dialogue-capacity.md`](../60-casebook/cards/D3-dialogue-capacity.md) |
| 整体 -16 LUFS 达标就宣布声音合格 | 对白被音乐压住；用代理指标顶替观感 | [`60-casebook/cards/F2-proxy-metrics.md`](../60-casebook/cards/F2-proxy-metrics.md) |
| 给慢镜打斗配一条史诗长音乐来"补气势" | 慢上加慢，速度层次被音乐抹平 | [`60-casebook/cards/A3-slow-motion-default.md`](../60-casebook/cards/A3-slow-motion-default.md) |
| 用 turbo（4–8 步）预览的声音判断音色和对白好坏 | 音频最后收敛，低步数时音色最弱，会误判 | [`60-casebook/cards/D5-qc-tools-lie.md`](../60-casebook/cards/D5-qc-tools-lie.md) |
| 用 whoosh 或冲击声去修"片段式"，不回头改分镜 | 声音只能缝合剪点，救不了没有因果的段落划分 | [`60-casebook/cards/F3-patch-iteration.md`](../60-casebook/cards/F3-patch-iteration.md) |
| 用 BBC 音效、NC 或 ND 曲目"先用着" | 发布即侵权，作品被下架 | 合规问题，见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) 第四部分 |

## → 行为改变

1. 下次写任何 H3 提示词，`non_diegetic_music:` 一律写 `N/A`。写完 `overall_soundscape` 后数一遍点名声源，超过 3 个就删到"对白 + 1 个动作声 + 1 条环境床"，并删掉会被生成成画面的声源词（人群、门铃、引擎）（R-SND-02）。
2. 下次进入后期，**先**静音看一遍粗剪，写出缺失清单，**再**按"对白 → 环境 → 拟音 → 设计音效 → 音乐"的顺序搭建。禁止先铺音乐。
3. 下次排剪辑单，音频入出点和画面入出点分开记录：每场对白戏至少一处 L-cut，每次换场至少一处 J-cut，每个爆发段后登记 ≥1s 的余波静场（R-SND-05、R-SND-07）。
4. 下次配乐，**改为**每场铺一条连续轨，对白处用侧链压低；把打斗段接触切点、爆发切点和重拍的时间码列成对照表，偏差超过 2 帧，就挪切点或挪音乐（R-SND-03）。
5. 下次做对白 QC，静音段先跑 silencedetect，再决定是否转写；"多一句 / 少一句 / 错一字"的判决必须附抽帧看嘴的证据；字幕只从剧本取（D5、R-SND-01）。
6. 下次开新季，先在角色表里给每个说话角色绑定音色来源；同场同性别的两个说话人先做盲听辨认，分不清就改外配（R-SEA-13、R-SEA-14）。
7. 下次 verify，`loudness_verify.py` 全绿之后，再单独测对白段响度，与整体相差超过 5 LU 判不通过；任何非生成素材在许可台账里没有记录，就不进时间线（R-SND-09、R-SND-10）。

## 自测

1. 判断：H3 提示词不写 `non_diegetic_music` 段，等于告诉模型"不要音乐"。
<details><summary>答案</summary>错。显式写 N/A 的 14 次都没有配乐，省略的 3 次中有 2 次自带配乐（F-ZEN-07）；`prompt_lint.py` 对此报 `VP-music`。逐镜自带的配乐会在每个剪点处断裂，放大 A1 的片段感。正确做法是写 `N/A`，配乐在后期按场铺一条连续轨（T11.1、T11.7）。</details>

2. 简答：一颗 10s 打斗段的 `overall_soundscape` 写着 "wind, crowd murmuring, temple bell, footsteps, sword clashes, epic drums"。指出问题并改写。
<details><summary>答案</summary>① 点名 6 个声源，超过 3 个的上限（T11.2、R-SND-02）；② "crowd murmuring" 会招来人群画面并扩写（B2），声源词还会把景别拉远（S-ZEN-17）；③ "temple bell" 会把钟画出来（提到什么就长什么）；④ "epic drums" 是音乐，不该出现在生成声轨里，应写进后期配乐轨，`non_diegetic_music: N/A`。改写示例：`Short sharp breaths from (S1). A steady low wind across the clearing. The ring of steel on steel at each contact.` 脚步和其余层留给后期拟音。</details>

3. 简答：成片 `loudness_verify.py` 全绿（-16.2 LUFS，真峰 -1.3 dBTP），人类却说"听不清台词"。下一步查什么？
<details><summary>答案</summary>整体响度只是下限（F2）。依次查：① 单独测对白段响度，与整体相差是否超过 5 LU（R-SND-09，Netflix LSR 口径，F-CRAFT-01）；② 音乐有没有在对白处被侧链压下（R-SND-04）；③ 对白出现时同时点名的声源是否超过 3 个、同类声是否超过 2 层（T11.4）；④ 生成声轨里有没有逐镜自带的配乐在和对白抢频段（T11.1）。</details>

4. 判断：转写显示某个无对白镜里有一句"谢谢观看"，说明 H3 擅自加了台词，必须重出。
<details><summary>答案</summary>错。这正是 D5 的情形：这类句子原样出现在 Whisper 喂噪声的幻觉数据集里（F-COMFY-15）。要判这一句真实存在，需要双通道证据：抽帧看嘴有没有动，加上亲耳听或 silencedetect 确认这段有人声。只有两个通道都确认，才判定需要重出（T11.8）。</details>

5. 简答：两个男角色同场对话，生成后听不出哪句是谁说的。按本篇，下一步做什么？
<details><summary>答案</summary>先做盲听辨认，每人 3 句（R-SEA-14）。H3 两个男声的相似度约 0.50（S-ZEN-17），分不清就改外配，例如 Speech T2A，它带 word 级时间戳，可直接对齐字幕（F-H3-30）；或者用 `<Audio N>` 音色参考绑定（S-ZEN-29）。如果挂了音频参考，必须重做正脸比对，因为有报告称身份相似度会跌到 0.0884（F-H3-24）。同时确认非说话人的闭嘴句写了（R-PRF-05）。绑定结果写进季圣经的角色表，全季不变（T11.10）。</details>
