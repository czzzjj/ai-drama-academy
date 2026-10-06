# 12 · 色彩与光：色彩剧本、动机光与跨镜一致性

> 一句话世界模型：本管线里，光和色在起始帧阶段就定死了（M2），所以色彩设计必须在关键帧之前完成。每个段在色彩剧本里占一格（色相 / 饱和 / 明度 / 光比 / 色温，加 3–5 个色名），每场写一句"光从哪边来、什么色温"，逐字写进该场每一张关键帧。光只写落在人身上的效果，不写灯具。一致性靠定调图、颜色匹配和统一 LUT 保证，不交给模型自由发挥 ｜ 浓缩案例：GAP-4, M2, P4, P5, B3, D2, A5 ｜ 对应技能：visual-bible, keyframe-freeze, asset-boards, edit-and-assemble, shot-qc

> 证据等级：委托方的色彩"依赖模型自由发挥，没有系统化的色彩剧本"〔委托方实证·GAP-4〕。本篇的方法来自外部调研和学院推断；委托方实证只有四条："起始帧决定灯光"（P4、M2），"斜光柱"（B3），"纯黑守不住"（D2）。

## 核心判决

**T12.1 · 光和色在起始帧里定，视频提示词改不动。色彩设计必须在写冻结提示词之前完成；视频提示词只逐字重复同一句光态，不新增光源，不改色温。**
为什么：方向、构图、灯光、角色形态全部由起始帧锚定〔委托方实证·P4〕；画面级的东西（史诗感、方向、构图、灯光）由起始帧决定，提示词救不了〔委托方实证·M2〕。视频阶段如果用文字改光，就和图打架；模型会执行所有指令，指令一打架就乱编〔委托方实证·A5④〕。

**T12.2 · 每集先写色彩剧本：每个段（`SEQ-nn`）一格，写明主色相、饱和（高/中/低）、明度（高/中/低）、光比档、色温；季圣经里另有一条季级色彩弧。没有色彩剧本，不出关键帧。**
为什么：色彩脚本用来 "map out the emotional beats of a story"，皮克斯是 "the first to create a color script for each of its films"〔外部调研·F-CRAFT-14〕；委托方的缺口正是"依赖模型自由发挥"〔委托方实证·GAP-4〕。对应判据 R-COL-01。

**T12.3 · 色彩跟着情绪走。情绪不同的相邻两段，色相、饱和、明度、光比四项至少有一项不同；全集只用一套 look（例如通篇青橙），判不通过。**
为什么：《玩具总动员》到了危险段落，色彩转为 "bleak and muddy"〔外部调研·F-CRAFT-14〕。青橙的价值是靠颜色把肤色从青色背景里分离出来〔外部调研·S-CRAFT-16〕，它是按节拍取用的工具，不是默认 LUT。对应判据 R-COL-03。

**T12.4 · 每一格点名 3–5 个具体颜色（如 `ash grey, ember orange, bruise purple`），逐字写进该段每张关键帧的冻结提示词。禁止用 "cinematic colors""moody palette" 这类评价词代替颜色。**
为什么：Sora 2 官方指南：点名 3–5 个颜色锚点，可以稳定跨镜头的调色板〔外部调研·F-CRAFT-08〕。评价性形容词无法执行，要写事件、写可见状态〔委托方实证·M3〕；`prompt_lint.py` 对这类词报 `VP-adjective`。对应判据 R-COL-02。

**T12.5 · 每场写一句光：主光源（画面内可见或可推断：窗、门、灯、屏、火、月、车灯）+ 方向 + 色温。这句话逐字写进该场每一张关键帧；补光色温与主光源一致。**
为什么：动机光是 "light within a shot that can be justified"，月光偏冷，烛光偏暖〔外部调研·F-CRAFT-13〕。一组实测中，关键帧统一画风词、每场加一句光与色温、再挂一张定调图之后，同场 13 张关键帧的平均亮度离散度从 18.3 降到 6.6，冷暖离散度从 9.3 降到 4.2〔外部调研·F-ZEN-15〕。对应判据 R-COL-04。

**T12.6 · 光只写"落在人和物上的效果"，不写灯具、光柱、光束这类物件。要写 "warm light from one side"，不写"落地灯的光"。**
为什么：提到什么就长什么，共用段里写到的灯具会在每一颗里长出来〔外部调研·S-H3-09、F-H3-22〕。委托方的三人镜就被加了一道不存在的具象斜光柱，修正后的判据是光效只允许写"打在脸上的环境光"这类被动描述〔委托方实证·B3〕。`prompt_lint.py` 对 flashlight / spotlight / light beam / god rays 报 `VP-light`。如果实景光源必须入画，由关键帧把它画出来，并在场景板上标出位置；视频提示词不再提它。

**T12.7 · 光向是空间线索。同一场的所有关键帧，主光方向必须一致，并且与场景板的标注一致；光向翻转按越轴处理。**
为什么：光向和轴线一样，由起始帧钉死〔委托方实证·P4、A5①〕；外部的连续性账本把"光向色温"和 180° 轴侧并列登记〔外部调研·S-H3-10〕。〔学院推断：光向翻转会被观众读成换了地方或换了时间。验证法：同一场做翻光、不翻光两版，请冷观众复述"是不是同一个地方"。〕对应判据 R-COL-05。

**T12.8 · 光比档按情绪选：紧张、危险段用低调（约 8:1，远侧脸落进深影），轻松段用高调（约 1:1）。提示词里写可见结果，不写比值数字。**
为什么：低调光约 8:1，用于惊悚和暗黑剧；高调光接近 1:1，用于喜剧〔外部调研·F-CRAFT-12〕。H3 不执行数字度量（"约二十厘米后停住"无效），但执行可见的终点〔外部调研·F-ZEN-11〕。〔学院推断：比值数字同样会被忽略；中间档 2:1、4:1 是插值，没有来源。验证法：同一张关键帧分别写 "8:1" 和 "the far side of her face falls into deep shadow"，各出 3 个 seed，去色后比较明暗分布。〕对应判据 R-COL-06。

**T12.9 · 暗部要按手机竖屏调：低调段的关键帧缩到 270 宽、去色之后，脸和表情仍要看得清；看不清就提亮脸，不提亮环境。**
为什么：9:16 靠脸讲戏（见 [`10-theory/01-vertical-drama-physiology.md`](01-vertical-drama-physiology.md)）。外部调研没有找到权威的竖屏手机调色指南，所以本条是〔学院推断：用冷观众断点记录验证，暗场处没人标"看不清"即通过〕。对应判据 R-COL-08。

**T12.10 · 跨镜一致性靠工程手段，不靠再抽一次。每场定一张色彩参考帧，同场的关键帧和视频帧都向它做颜色匹配；全集统一一份 `.cube`，在 render 阶段施加；参数写进剪辑单备注。**
为什么：ColorMatchV2 提供 mkl、hm、reinhard 等方法，strength 取值 0–10；它是 GPL-3.0，只能调用，不能拷贝代码〔外部调研·F-CRAFT-31〕。ffmpeg `lut3d` 支持 .cube〔外部调研·S-CRAFT-08〕。同场挂已通过的关键帧做链式参考〔委托方实证·P5〕；背景板会让运镜约减半，但场景漂移降到约 1/4〔外部调研·F-H3-11〕，光和色的稳定也是这份收益的一部分。对应判据 R-COL-07、R-SEA-16。

**T12.11 · 先写情绪意图，再推出光和色。删掉没有叙事动机的技术参数（光圈、焦距、机身型号）。**
为什么：一次 A/B 测试的结论是"更多的技术细节并没有帮助。它反而起到了负面作用"〔外部调研·F-CRAFT-19〕（单一厂商在 Seedance 上的测试，H3 上待测）。

**T12.12 · 纯黑、纯色、闪白、字卡一律不交给生成器。夜戏写成低调光下仍可见的形体，不写 "pitch black"。**
为什么：纯黑字卡交给 H3 后，中段被模型加上了 "LAVCE" 水印〔委托方实证·D2〕。〔学院推断：要求生成器出接近纯黑的画面，同样会诱发它自己往里填内容。夜戏改写成"月光从右侧勾出肩线，其余落进深蓝阴影"这类有可见主体的写法。验证法：抽帧查有没有自填文字和伪影。〕

## 机制解释

1. **为什么起始帧决定光。** 不论 FL2VA 还是 Ref2VA，起始帧都是构图和光的起点。视频阶段用文字另写一套光，模型面对的是两条互相矛盾的指令，结果就是闪烁、漂移，或者两套光各出现一半。所以光的设计越晚，修改成本越高。修关键帧的成本约是修视频的 1/18〔外部调研·S-PIPE-04〕。
2. **为什么写色名比写形容词稳。** 色名是在像素上可以核对的目标（"有没有 ember orange"），形容词只是评价（"够不够 moody"）。没写到的变量，每次采样都会重抽。点名 3–5 个颜色、加一句光，就把重抽的空间收窄了：F-ZEN-15 的离散度下降就是这个机制。〔学院推断：少于 3 个，模型会自己补色；多于 5 个，颜色之间会打架。验证法：同场 2 / 4 / 7 个色名各出一组，比较离散度。〕
3. **为什么光写效果、不写灯具。** 生成器会把名词登记为画面内容。ComfyUI 官方 H3 指南的建议是把禁令写成正向状态〔外部调研·S-COMFY-08〕。光是物体表面的状态，灯是一个物件：写"暖光从左侧落在她脸上"是在描述状态；写"落地灯"，模型就会把灯画出来。
4. **为什么光向关系到空间。** 观众在一场戏里靠三条线索定位：人物左右、视线方向、光从哪边来。前两条已经由单轴定侧锁住（M4），光向一翻，第三条线索就和前两条冲突了。
5. **为什么手机让暗部更危险。** 手机屏幕小，观看环境亮，自动亮度会压暗部。〔学院推断：低调画面在手机上先丢的是暗部的脸，所以"脸可辨"是低调段的底线。外部没有权威来源，验证见 R-COL-08。〕

## 本管线下的变体

**色彩剧本格（写在 `visual-bible.md`，每段一行；示例为通用占位，不是委托方剧情）**

| SEQ | 情绪节拍 | 主色相 | 饱和 | 明度 | 光比档 | 色温 | 3–5 色名 | 光句（逐字进该段每张关键帧） |
|---|---|---|---|---|---|---|---|---|
| SEQ-01 | 对峙、压迫 | 青灰 | 低 | 低 | 低调 | 冷 | slate grey, moss green, cold steel blue | `cold overcast light falls from the upper left; the far side of each face sinks into deep shadow` |
| SEQ-02 | 爆发 | 橙红 | 高 | 中 | 低调 | 暖 | ember orange, soot black, ash white | `hot orange light from the burning ground below lights their faces from beneath, the upper left still cold` |
| SEQ-03 | 余波 | 灰蓝 | 低 | 中 | 中 | 冷 | ash grey, muted teal, pale bone | `soft grey light falls evenly from the upper left; faint warm glow fades on the right` |

- 场内主光向保持一致（上表三段都是"左上"）。SEQ-02 的新光源由事件引起（地面燃烧），而且必须在关键帧里看得见；不能凭空出现。
- **冻结提示词的组成顺序**：锚点句 EN（逐字）→ 构图与方位 → 光句（逐字）→ 色名（逐字）→ 禁令。视频提示词直接复制同一句光句；改写会让模型重抽，就像改写身份描述会重抽脸〔外部调研·S-H3-09〕。
- **关键帧规格**：送 first_frame 的关键帧用 9:16（1536×2752），或在送入前显式裁成 9:16（见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) 第三部分）。2:3 的图被拉伸后，光影形状也会一起变形。
- **验收证据**：
  - 同场光向：同场关键帧用 ffmpeg `tile` 或 `hstack` 拼成一张，标出光向（R-COL-05）。
  - 光比档：用 `scale=270:-1,format=gray` 出去色缩略图，存为 `kf-poster270-gray.png`（R-COL-06、R-COL-08）。
  - 视频是否保住关键帧的光：`python3 50-rubrics/scripts/contact_sheet.py clip.mp4 --keyframe REF-SHOT012-START.png`，把首、中、尾帧和关键帧并排对照。
  - 跨镜跳色：先查同场相邻 CUT 的肤色和白平衡（R-COL-07）。修正顺序是颜色匹配 → 统一 `.cube`（ffmpeg `lut3d=file=look.cube:interp=tetrahedral`）→ 都不行才回关键帧。〔学院推断：ColorMatchV2 的 strength 从 0.5–1.0 起试，按同场拼图目视确认。〕
- **跨集**：同一场景在不同集重复出现时，光向和色温不变；如果剧情改了时段，就在季圣经里登记为场景变体（R-SEA-16，见 [`10-theory/14-season-architecture.md`](14-season-architecture.md)）。

**关键帧光色自查（交关键帧验收之前，逐张过一遍）**
- 冻结提示词里有本场的光句（光源 + 方向 + 色温），并且与色彩剧本格逐字一致（R-COL-04）。
- 冻结提示词里有本段的 3–5 个色名，逐字一致（R-COL-02）。
- grep lamp / torch / lantern / spotlight / beam / rays 无命中；`prompt_lint.py` 没有报 `VP-light`（T12.6）。
- 同场拼图中，光向和场景板标注一致（R-COL-05）。
- 去色缩略图的明暗分布与声明的光比档相符；低调段 270 宽时脸仍可辨（R-COL-06、R-COL-08）。
- 画面内没有被模型自行加上的光源、光柱或文字；有就按 C1 的三件套处理：正向句 + 绝对否定句 + 多 seed（见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) R1）。

**季级色彩弧（写在季圣经，每集一格）**：每集一个主导色温和饱和档，标出全季最冷、最暗的一集（通常是主角最低谷）和最暖、最饱和的一集（通常是最大的回报）。〔学院推断：季弧给每集色彩剧本定上下界，防止相邻集的 look 雷同。验证法：把各集代表关键帧排成一行，请独立评审判断能否看出情绪走向。〕

## 常见误用

| 误用 | 后果 | 案例卡 |
|---|---|---|
| 不写光和色，交给模型自由发挥 | 每张关键帧重抽色温和亮度，成片跳色；对应 GAP-4 | [`60-casebook/cards/C2-lenient-acceptance.md`](../60-casebook/cards/C2-lenient-acceptance.md)（验收"看一眼差不多"会把跳色放行） |
| 写 "a beam of light / spotlight / torch" 来营造氛围 | 生成出具象光柱、手电和灯具 | [`60-casebook/cards/B3-clone-faces.md`](../60-casebook/cards/B3-clone-faces.md) |
| 同场两张关键帧一张光从左来、一张从右来 | 观众读成换了地方，空间感碎 | [`60-casebook/cards/A5-spatial-chaos.md`](../60-casebook/cards/A5-spatial-chaos.md) |
| 视频提示词另写一套光（"lit by moonlight" 配一张暖光起始帧） | 指令打架，画面闪烁或漂移；提示词与产出不一致 | [`60-casebook/cards/E4-prompt-output-mismatch.md`](../60-casebook/cards/E4-prompt-output-mismatch.md) |
| 全片套同一个青橙 LUT，就说"有统一调色了" | 指标统一了，情绪却没有变化 | [`60-casebook/cards/F2-proxy-metrics.md`](../60-casebook/cards/F2-proxy-metrics.md) |
| 色名和光句只写在视频提示词里，关键帧提示词里没有 | 起始帧已经定了别的光，文字救不回来 | [`60-casebook/cards/C1-banned-items-violated.md`](../60-casebook/cards/C1-banned-items-violated.md)（生成器按图自由发挥，忽略文字） |
| 低调段一路压暗到看不清脸 | 手机上什么都读不出来，观众划走 | — （R-COL-08，学院推断） |
| 片尾黑场、闪白、字卡交给 H3 | 被模型加上文字或水印 | [`60-casebook/cards/D2-solid-black-fails.md`](../60-casebook/cards/D2-solid-black-fails.md) |

## → 行为改变

1. 下次接到一集，**先**写色彩剧本表：每段一格、3–5 个色名、一句光；**再**写冻结提示词。没有这张表，不出关键帧（R-COL-01、R-COL-02）。
2. 下次写冻结提示词，光只写"光从哪边落在谁身上、什么色温"。写完 grep 一遍 lamp / torch / lantern / spotlight / beam / rays，命中的改写成效果描述（R-COL-04）。
3. 下次验收同场关键帧，**改为**并排拼图，看光向和肤色。光向不一致的回关键帧阶段重出，不放行到视频（R-COL-05）。
4. 下次做低调段，每张关键帧缩到 270 宽、去色，看脸。看不清就提亮脸，不提亮环境（R-COL-08）。
5. 下次发现跨镜跳色，**先**用场景参考帧做颜色匹配或统一 `.cube`，参数写进剪辑单备注；**禁止**为了色差直接重抽视频（R-COL-07）。
6. 下次写视频提示词，光句从该场关键帧提示词逐字复制，不新增光源，不改色温（T12.1）。
7. 下次需要黑场、闪白、字卡，一律本地生成，在剪辑里叠加（D2）。

## 自测

1. 判断：起始帧是暖色室内光，为了让这一镜更有"夜的感觉"，在视频提示词里加一句 "cold moonlight floods the room"。
<details><summary>答案</summary>错。光由起始帧决定（P4、M2），视频阶段另写一套光会和图打架（A5④），结果是闪烁、漂移，或者两套光各占一半，还违反了提示词与产出一致（E4）。要改光，回到色彩剧本格改光句，重出关键帧（T12.1）。</details>

2. 简答：某关键帧冻结提示词写着 "a dim room lit by a single floor lamp, beams of light through the window, moody cinematic colors"。逐处指出问题并改写。
<details><summary>答案</summary>① "floor lamp" 是灯具，会被画出来（T12.6）；② "beams of light" 会生成具象光柱（B3，`VP-light`）；③ "moody cinematic colors" 是评价词，不是颜色（T12.4，`VP-adjective`）；④ 没有方向、色温和光比档（T12.5、T12.8）。改写示例：`warm low light falls across her face from the right; the left side of the room fades into deep blue shadow; palette: amber, walnut brown, ink blue`。</details>

3. 简答：同一场 8 张关键帧并排后，亮度和冷暖忽高忽低。按本篇，依次做什么？
<details><summary>答案</summary>① 确认这 8 张是否逐字写了同一句光（光源 + 方向 + 色温）和同一组色名，缺的补上（T12.5、R-COL-04）；② 挂一张定调图做参考，F-ZEN-15 中这样做使亮度离散度从 18.3 降到 6.6；③ 仍有残差，就用场景参考帧做颜色匹配（T12.10）；④ 光向不一致的单张，回关键帧阶段重出（R-COL-05）。</details>

4. 判断：全片统一套一个青橙 LUT，满足"色彩一致性"，所以色彩剧本可以省略。
<details><summary>答案</summary>错。一致性（同场不跳色）和色彩剧本（不同情绪节拍用不同色彩）是两件事。全集同一套 look，R-COL-03 判不通过。青橙是把人物从背景里分离出来的工具，应按节拍取用（S-CRAFT-16）。</details>

5. 简答：为什么本篇要求光比写成 "the far side of her face falls into deep shadow"，而不是 "8:1 lighting ratio"？这条结论的证据等级是什么？
<details><summary>答案</summary>H3 对数字度量不执行，对可见终点执行（F-ZEN-11 的厘米数实验），所以学院推断比值数字也会被忽略。证据等级是〔学院推断〕，验证法：同一张关键帧分别写数字比值和可见描述，各出 3 个 seed，去色比较明暗分布（T12.8）。</details>
