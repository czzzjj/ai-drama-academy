# 声音设计 / 色彩灯光 / 表演指导 / 免版权素材库

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：36 ｜ 核实方式：逐条 WebFetch 打开核对

## 一句话结论

本专题为委托方三处能力缺口提供外部依据：声音设计（GAP-3）、色彩与灯光（GAP-4）、表演与表情指导（GAP-5）。具体内容有：声音层次与密度规则（Murch、Krotos），三种可量化的响度口径（EBU R128 的 -23、AES TD1008 的 -16/-18、Netflix 对白门限 -27），可直接写进 render/verify 脚本的 ffmpeg 滤镜参数，动机光、光比和色彩脚本方法，动作动词式表演指令，以及一份按许可条款逐条核过的音乐、音效、字体清单。仍缺的有：抖音、快手、视频号等平台的官方响度规格；竖屏手机观看的调色与暗部安全指南；中文微短剧行业关于声音、调色、表演的一手资料；"在 H3 生成阶段不出音乐、后期统一铺乐"能否解决剪辑点音乐断裂，这一点目前只是推断，需要实测。

## 条目

### S-CRAFT-01 · Walter Murch — Dense Clarity / Clear Density（Transom）
- **URL**：https://transom.org/2005/walter-murch/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归作者/Transom，仅可引用观点与短句
- **核实**：✅ 已打开核实
- **摘录**：Walter Murch 于 2005 年在 Transom 发表的长文《Dense Clarity – Clear Density》。他把声音排在一条光谱上：左端是 "Encoded"（最典型的是语言，对应光谱的紫端），右端是 "Embodied"（最典型的是音乐，对应红端）；多数音效落在中间，"half language, half music"。他提出 "Law of Two-and-a-half"：同类声音叠到接近三层时，观众的感知就从"一个个声音"变成"一群声音"，原话 "three is the borderline"。例子是《THX-1138》：一两个机器人的脚步必须对上画面，三个以上就不需要了。如果各层都挤在光谱的同一区域，上限缩到 2.5 层；如果均匀分布在 Encoded 到 Embodied 之间，上限可以翻倍，"five layers is the maximum" 是保持各元素可辨的最大值。《现代启示录》直升机段做了六个预混层，终混时同一时刻最多保留五层，各层 "disappearing and reappearing according to the dramatic focus of the moment"。文中还提到，立体声电影的对白几乎总放在中置声道。
- **对本学院有什么用**：在 overall_soundscape 和后期混音中设密度上限：同类声源同时不超过 2 层，点名声源总数同时不超过 5 层，戏剧焦点切换时撤掉一层。〔学院推断：这些数字来自影院混音经验，没有在 9:16 手机外放上验证过。验证方法：同一片段做 3 层、5 层、7 层三个混音版本，请冷观众复述能分辨出的声源。〕
- **落点模块**：10-theory、20-craft、50-rubrics

### S-CRAFT-02 · Krotos — Film sound design: a how-to guide
- **URL**：https://krotos.studio/blog/film-sound-design
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 Krotos，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：音效软件厂商 Krotos 的博客，把影视声音分成七个部分：Dialogue、Foley、Production FX、Designed FX、Ambience、Music、Mix Bus。建议的搭建顺序是：先对白（叙事主干），再环境（保证连续），再拟音（画内动作），再设计音效与冲击声，然后音乐，最后在总线上做平衡。原文 "Less is often more; avoid treating every action with an equal-weight sound layer."，以及 "A well-placed ambience swell or whoosh can hide a jump cut and make two disparate shots read as one continuous action."。文中只说要按交付规格检查响度，没有给出具体的 LUFS 数值。
- **对本学院有什么用**：声音后期按"对白、环境、拟音、音效、音乐"的顺序搭建。跳切处用环境声的起伏或 whoosh 衔接，用来减轻碎镜硬切的割裂感（对照〔委托方实证·A1〕）。〔学院推断：效果还要用冷观众做对比测试。〕
- **落点模块**：10-theory、20-craft、70-playbooks

### S-CRAFT-03 · HackerNoon — AI video comes out silent: the sound design workflow I run on every shot
- **URL**：https://hackernoon.com/ai-video-comes-out-silent-here-is-the-sound-design-workflow-i-run-on-every-shot
- **类型**：article
- **分类**：🟡 需适配
- **许可**：版权归作者，仅借鉴流程
- **核实**：✅ 已打开核实
- **摘录**：作者给 AI 生成视频补声音的逐镜六步流程。①静音看一遍，"write down what's missing. Not what sounds bad, what sounds absent"，例如 "A torch with no crackle. A hallway with no echo."。②先铺环境床："One continuous room-tone or environment track"，作者用 ElevenLabs 的音效工具生成。③只给画面里看得见的动作配拟音，"Every footstep the camera actually shows, not every footstep implied off-screen"。④音乐最后加，"matched to the beat, not the whole scene"。⑤层级从上到下是对白、拟音、环境、音乐；"If two layers compete for the same frequency space at the same moment, one of them has to lose"。⑥"Log the recipe"：每个声音元素的工具、提示词和参数都记在对应镜头旁边。作者说最后一步最常被跳过。
- **对本学院有什么用**：每集后期固定执行"静音审片 → 列缺失清单 → 铺环境床 → 补可见拟音 → 加音乐 → 冻结声音配方"，配方写进素材元数据，供重渲染时复现。
- **落点模块**：20-craft、70-playbooks、40-memory

### S-CRAFT-04 · FilmDaft — The L-Cut and J-Cut: How Film Editors Use Audio to Control Time
- **URL**：https://filmdaft.com/the-l-cut-and-j-cut-how-film-editors-use-audio-to-control-time/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 FilmDaft，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：J-cut 是下一镜的声音先于画面进入，L-cut 是上一镜的声音延续到下一镜的画面上。时长建议："a half-second overlap in a dialogue scene is often enough"，"a two-second J-cut into a major sequence creates real anticipation"。两人对话建议默认用 L-cut 切到听者，理由是 "Most actors give their best moments in reaction, not in speech."。举例：《现代启示录》直升机声延续到天花板吊扇的画面；《教父》洗礼蒙太奇里，神父的声音和管风琴（L-cut）盖在暴力画面上，枪声则以 J-cut 先于画面出现；《黑暗骑士》结尾 Gordon 的台词连续跨过三个场景。
- **对本学院有什么用**：剪辑单里音频和视频的入出点分开写。对白场至少用一处约 0.5 秒的 L-cut 切到听者反应，进入新段落时用 1–2 秒的 J-cut。〔学院推断：数值出自单篇剪辑博客。验证方法：同一场戏做硬切版和 J/L-cut 版，让冷观众比较"跳"的感觉，对照〔委托方实证·A1〕。〕
- **落点模块**：20-craft、50-rubrics、60-casebook

### S-CRAFT-05 · Auphonic — Dialog Loudness Normalization（Netflix 对白门限 -27 LKFS）
- **URL**：https://auphonic.com/blog/2020/10/08/dialog-loudness-normalization/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：版权归 Auphonic；文中数值为行业规格，可引用
- **核实**：✅ 已打开核实
- **摘录**：Auphonic 2020-10-08 的博文，转述 Netflix 规格："Average loudness must be -27 LKFS +/- 2 LU dialog-gated."。旧规格是 -24 LKFS ±2 LU、按全节目测量；Netflix 团队发现按旧规格合规的内容，对白集中在 -27 LKFS 左右，"Dialog was relatively quiet, while louder music and sound effects lifted the overall loudness of the production"。Netflix 推荐整体响度范围（LRA）4–18 LU，对白 LRA 不超过 7 LU。文章定义了 Loudness-Speech Ratio（LSR，语音段与整体响度之差），并称 "A LSR of 5 LU or less is best for most productions"。页面没有真峰值数值，也没有针对移动端的数字。研究员原稿写的"真峰值 ≤ -2 dBTP"在本页不存在，已删除。
- **对本学院有什么用**：verify 阶段除了整体 -16 LUFS，再加两项对白自检：对白段与整体响度之差不超过 5 LU，对白 LRA 不超过 7 LU，防止音乐和音效压住台词。〔学院推断：阈值借自 Auphonic 与 Netflix，没有在手机短剧上验证过。〕
- **落点模块**：50-rubrics、20-craft、70-playbooks

### S-CRAFT-06 · Production Advice — AES TD1008 streaming loudness recommendations
- **URL**：https://productionadvice.co.uk/td1008/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：文章版权归作者；标准数值可引用
- **核实**：✅ 已打开核实
- **摘录**：这是对 AES TD1008（流媒体与网络电台分发响度建议，原文 26 页）的解读文章。建议的分发响度：语音和 "Assorted"（混合）内容 -18 LUFS，音乐 -16 LUFS。文章强调这些数字 "not for artists, or producers, or recording, mixing & mastering engineers"，只给网络电台和流媒体平台做归一化用。文中还说，多数流媒体服务当前用的是 -14 LUFS。页面没有讨论真峰值，也没有出现"-17 LUFS 折中值"或"移动端增益不足"的说法。研究员原稿里这两点来自搜索摘要，未经页面核实，已删除。AES 原始文档本次没有打开。
- **对本学院有什么用**：-16 LUFS 只是一种口径。以对白为主的集数，可以把 -18 LUFS 作为备选目标做 A/B 对比。〔学院推断：平台的实际归一化值未知，见"空白"一节。〕
- **落点模块**：10-theory、50-rubrics

### S-CRAFT-07 · EBU R 128（v5.0）与 R128 s4（电影化内容）
- **URL**：https://tech.ebu.ch/publications/r128
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：EBU 公开技术文档，PDF 免费下载
- **核实**：✅ 已打开核实（另打开了 s4 页面 https://tech.ebu.ch/publications/r128s4）
- **摘录**：EBU R 128 规定节目响度目标为 -23 LUFS，从 3.0 版起容差收窄到 ±0.5 LU。现行版本是 5.0（2023 年 11 月），新增了对补充文件 s4（Loudness for Cinematic content）的引用。配套标准是 Tech 3341（响度计量）和 Tech 3342（响度范围）。R128 s4 发布于 2023-11-08，针对以对白为主、动态大的电影化内容在广播和流媒体中的归一化。它指出这类内容通常有很大的 LDR，即 "the difference between Programme Loudness (PL) and Dialogue Loudness"，并写明 "not intended as production advice for feature films"。
- **对本学院有什么用**：理论模块区分三种口径：广播 -23、流媒体 -14 到 -18、对白门限 -27。另外把 LDR（节目响度减对白响度）作为剧情内容对白清晰度的量化指标。
- **落点模块**：10-theory、50-rubrics

### S-CRAFT-08 · FFmpeg Filters Documentation — loudnorm / sidechaincompress / lut3d
- **URL**：https://ffmpeg.org/ffmpeg-filters.html
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：FFmpeg 为 LGPL-2.1 或更高版本；启用部分可选组件时整体适用 GPL-2.0 或更高版本（据 https://ffmpeg.org/legal.html 核实）。作为外部工具调用。
- **核实**：✅ 已打开核实（下载全文后逐段核对）
- **摘录**：loudnorm 按 EBU R128 做响度归一化，支持动态和线性两种模式，以及单遍和双遍。I 的范围是 -70 到 -5，默认 -24；LRA 范围 1 到 50，默认 7；TP 范围 -9 到 0，默认 -2。linear 默认为 true，但必须提供 measured_I、measured_LRA、measured_TP、measured_thresh；如果目标 LRA 低于源 LRA，或者增益会让真峰值超过 TP，就退回动态模式。动态模式会把音频上采样到 192 kHz 来测真峰值。print_format 可选 summary、json、none。sidechaincompress 用第二路输入去压第一路，默认值：threshold 0.125、ratio 2、attack 20 ms、release 250 ms、knee 2.82843，detection 默认 rms。lut3d 支持 3dl、cube、dat、m3d、csp 格式，插值方式有 nearest、trilinear、tetrahedral、pyramid、prism。
- **对本学院有什么用**：render/verify 脚本直接调用：双遍 linear loudnorm 做响度，sidechaincompress 让音乐给对白让位（ducking），lut3d 给全片套统一的 .cube 调色。
- **落点模块**：20-craft、70-playbooks、50-rubrics

### S-CRAFT-09 · Google Cloud — The ultimate prompting guide for Veo 3.1
- **URL**：https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：Google 官方博客，版权所有，仅借鉴写法
- **核实**：✅ 已打开核实（同一 URL 另见 S-VGEN-02）
- **摘录**：提示公式是 [Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]。音频写法：对白放在引号里、跟在说话人后面（A woman says, "We have to leave now."）；音效写 "SFX: thunder cracks in the distance"；环境声写 "Ambient noise: the quiet hum of a starship bridge"。光色写在风格段，例如 "lit by the harsh fluorescent overhead lights and the green glow of the monochrome monitor"。情绪用单独一行，例如 "Emotion: Wonder and reverence."。另有首尾帧过渡（示例为 "smooth 180-degree arc shot"）、Ingredients to Video（用多张参考图保持一致），以及时间戳多镜头写法 [00:00-00:02] 到 [00:06-00:08]。文中有一节 "Mastering negative prompts"。时长 4/6/8 秒。
- **对本学院有什么用**：overall_soundscape 拆成对白、SFX、环境三类明确的声源。时间戳分段只借来规划段内节拍，不照搬每 2 秒一镜的密度（对照〔委托方实证·A1〕）。
- **落点模块**：20-craft、40-memory

### S-CRAFT-10 · OpenAI Cookbook — Sora 2 Prompting Guide
- **URL**：https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：OpenAI 官方文档，仅借鉴写法（许可细节见 S-VGEN-01）
- **核实**：✅ 已打开核实
- **摘录**：原文 "Each shot should have one clear camera move and one clear subject action."。动作要写成可数的节拍，例如 "takes four steps to the window, pauses, and pulls the curtain in the final second"。4 秒片段通常容纳一到两句短对白，8 秒可以多几句；对白放在单独标注的 Dialogue 块里。没有对白的镜头，用 "distant traffic hiss" 这类简单声音提示当节奏标记，不必写完整声景。光照不要写 "brightly lit room"，而要写 "soft window light with warm lamp fill, cool rim from hallway"，并点名 3–5 个颜色锚点（如 amber、cream、walnut brown）来稳定跨镜头的调色。短片段更听指令。迭代时一次只改一个变量。可选时长为 4、8、12、16、20 秒。
- **对本学院有什么用**：每个镜头只写一个运镜和一个主体动作，动作按秒计数，台词量按时长限制。每场在提示词里固定 3–5 个色名，作为场级色彩锚点。
- **落点模块**：20-craft、50-rubrics、40-memory

### S-CRAFT-11 · Kling AI — VIDEO 2.6 Native Audio User Guide
- **URL**：https://kling.ai/quickstart/klingai-video-26-audio-user-guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：快手可灵官方文档，仅借鉴写法（同一 URL 另见 S-VGEN-09）
- **核实**：✅ 已打开核实
- **摘录**：公式是 Scene + Element + Movement + Audio + Other（Other 包括风格、情绪、镜头）。音频分为 Dialogue、Singing、Sound Effects、Pure Music 四类。对白规则：说话人用唯一且前后一致的 [Character Name]，不用代词或同义词；情绪标签紧跟说话人，例如 "[Character A, angrily] says, 'Line here.'"；说话人之间用 "Immediately" 这类连接词控制轮次，避免台词重叠。音效模板："[Object: Wooden Door] suddenly [Action: Slams] + [Sound Effect: Bang]"。环境声写成"场景 + 声音元素 + 空间混响"，例如 "Echo in an Open Hall (Reverb), Small Room Acoustics"。语音只支持中文和英文。三人及以上对白效果下降，两人最好。唱歌或对白较多的场景建议用 10 秒时长，不用 5 秒。
- **对本学院有什么用**：每句对白写成"说话人 ID + 语气标签"，单个片段限两人对白，音效写成"物体 + 动作 + 声音"三元组。〔学院推断：这是可灵的规则，H3 上是否同样有效需要对照测试。〕
- **落点模块**：20-craft、40-memory、50-rubrics

### S-CRAFT-12 · MiniMax — MiniMax H3 官方博客
- **URL**：https://www.minimax.io/blog/minimax-h3
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：MiniMax 官方博客；模型权重许可另见其发布（S-H3-02）
- **核实**：✅ 已打开核实（页面日期 2026-07-31）
- **摘录**：H3 可生成最长 15 秒、2K 分辨率、带原生立体声的视频，默认 2K，另有 768p。原文："No separation between voice, sound effects, and music — all jointly modeled"，并称支持 "Native multi-shot modeling"。输入可以是文本、图像、视频、音频，能跨模态参考，示例是 "Reference the Hitchcock camera movement from Video 1, have the character in Image 2 sing, with the vocals matching Audio 3."。价格方面，称 2K 每秒价格不到主流模型的三分之一，768p 不到主流 720p 的一半。博客说计划 "open up the model weights in the coming days"。自述的局限："Visual detail can still be improved in certain scenarios"，多模态理解 "there is significant room to improve"。博客没有提到委托方使用的六段式提示词方言（来源见 S-H3-01）。研究员原稿附带的发布会日期和参考素材数量上限不在本页，已删除。
- **对本学院有什么用**：要知道 H3 的人声、音效、音乐是同一次生成，不能分轨。〔学院推断：生成阶段把 non_diegetic_music 留空、后期整场铺一条连续音乐，可以避免每个剪辑点音乐断裂。验证方法：同一场戏分别做"生成带乐"和"后期铺乐"两版，统计剪辑点上的音乐断裂次数，并请冷观众打分。〕
- **落点模块**：10-theory、20-craft、70-playbooks

### S-CRAFT-13 · Hyperallergic — 25 Years of Pixar's Vibrant, Emotional Color Palettes
- **URL**：https://hyperallergic.com/610771/the-art-of-pixar-chronicle-books/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 Hyperallergic/Pixar，仅借鉴方法
- **核实**：✅ 已打开核实（更正了研究员原稿的人名对应）
- **摘录**：这是一篇介绍《The Art of Pixar》画册的书评。文章说色彩脚本用来 "map out the emotional beats of a story"，并称皮克斯是 "the first to create a color script for each of its films"。Ralph Eggleston（1992 年任《玩具总动员》艺术指导）在长条黑纸上用粉彩画色彩脚本，文中称之为 "stream of consciousness" 式的地图。《玩具总动员》用 "soft blues, bubblegum pinks, and warm yellows"，危险段落转为 "bleak and muddy"。《海底总动员》从 "light aqua" 的浅水到 "dark indigo depths"，中间穿插 "popping oranges, reds, greens and pinks" 的海洋生物。《玩具总动员3》的色彩脚本由 Dice Tsutsumi 用数字方式绘制，焚化炉段落 "burns bright on the page in flaming oranges and reds"。Lou Romano 负责的是《超人总动员》和《飞屋环游记》（研究员原稿把他只对应到《飞屋环游记》，已更正），《超人总动员》用了 60 年代波普风格的几何形和跳色。
- **对本学院有什么用**：每集先出一条"一个节拍一格"的色彩脚本，每格写明主色相、饱和度、明度、色温；整季再排一条色彩弧。关键帧提示词按格取色。
- **落点模块**：10-theory、30-taste、20-craft

### S-CRAFT-14 · StudioBinder — What is Motivated Lighting in Film
- **URL**：https://studiobinder.com/blog/what-is-motivated-lighting-in-film
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 StudioBinder，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：动机光的定义是 "light within a shot that can be justified"，即模仿或强化场景里本来就有的光源。可以作为动机的光源有窗、门、台灯、电脑屏幕、蜡烛、火、月光、车灯。做法分三步：先研究光从哪里进入场景；把画面内可见的实景光源（practicals）纳入画面，作为光的理由；补光的色温要和光源一致（月光偏冷，烛光偏暖）。核心自问："What motivates this light? How can I justify its presence?"。文章认为动机光能让光线符合片中世界的内部逻辑，观众不会去质疑来源不明的光。
- **对本学院有什么用**：每个场景板标出实景光源的位置，每个关键帧提示词写明"光源 + 方向 + 色温"，同一场景内光向保持一致，作为空间连贯的线索。
- **落点模块**：20-craft、50-rubrics、30-taste

### S-CRAFT-15 · StudioBinder — What is Key Light（光比与类型）
- **URL**：https://www.studiobinder.com/blog/what-is-key-light
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 StudioBinder，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：主光是场景的首要光源。低调光几乎不用辅光；如果用，主辅光比 "somewhere around 8:1 in favor of the key"，原文说低调光 "typically used in thrillers, horrors, or dark dramas that have a more serious tone"。高调光的主辅光比 "nearly 1:1"，用于营造 "cheerful, optimistic, and up-beat mood"，"typically be found in comedies, sitcoms, or rom-coms"。调整主光的方法有四种：柔化、反射、拉远距离（阴影更硬）、改变角度。文章还提到伦勃朗光（辅光很少，保留面部反差）、黄金时刻自然光，以及动机光。
- **对本学院有什么用**：把情绪节拍映射到光比档位，写进关键帧提示词。原文只给了两端：1:1 对应轻喜剧，8:1 对应惊悚或暗黑。〔学院推断：中间档 2:1（日常）和 4:1（紧张）是插值，没有来源，需要在 H3 上测试模型是否能区分这几档。〕
- **落点模块**：20-craft、30-taste、50-rubrics

### S-CRAFT-16 · PetaPixel — What is the Orange & Teal Look and Why is it So Popular?
- **URL**：https://petapixel.com/2017/02/23/orange-teal-look-popular-hollywood/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 PetaPixel，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：文章解释青橙调色流行的三个原因。第一，"skin tones (with some obvious exceptions) typically sit somewhere in the orange spectrum"，在阴影和背景里加青色，就能靠颜色而不是景深把人物从背景里分离出来。第二，"Teal and Orange have the highest contrast between their exposure values of any pair of complementary colors on the color wheel"。第三，它模仿了黄金时刻暖光对蓝天的效果。文章没有讨论这种调色的历史来源，也没有批评过度使用。
- **对本学院有什么用**：把青橙当作"人物与环境分离"的工具，按节拍选用，不作为全片默认 LUT，避免全片情绪没有变化。
- **落点模块**：30-taste、20-craft

### S-CRAFT-17 · ComfyUI-KJNodes — ColorMatch / ColorMatchV2 节点（kijai）
- **URL**：https://github.com/kijai/ComfyUI-KJNodes
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：GPL-3.0（已核对仓库 LICENSE）；依赖库 color-matcher 也是 GPL-3.0（已核对 hahnec/color-matcher 的 LICENSE）
- **核实**：✅ 已打开核实（github.com 页面经代理返回 403；改从 raw.githubusercontent.com 读取 LICENSE、requirements.txt 和 nodes/image_nodes.py 源码核对）
- **摘录**：ComfyUI 的常用节点包，requirements.txt 里有 color-matcher。nodes/image_nodes.py 中的 ColorMatch 节点输入 image_ref 和 image_target，method 可选 mkl、hm、reinhard、mvgd、hm-mvgd-hm、hm-mkl-hm（默认 mkl），strength 取值 0–10、默认 1.0。节点描述原文："color-matcher enables color transfer across images which comes in handy for automatic color-grading of photographs, paintings and film sequences as well as light-field and stopmotion corrections."。研究员原稿没提到一点：源码里旧版 ColorMatch 已标 DEPRECATED = True，新版是 ColorMatchV2，多了一个 reinhard_lab_gpu 方法（用 Kornia 在 Lab 空间做 GPU 迁移）。
- **对本学院有什么用**：每场设一张色彩参考帧，在 ComfyUI 里用 ColorMatchV2 把该场所有关键帧和视频帧对齐到参考帧，减少跨镜头的色彩漂移。学院包只引用节点名和参数，不拷贝 GPL 代码。
- **落点模块**：20-craft、70-playbooks

### S-CRAFT-18 · USC Scalar — Directing with Action Verbs!（基于 Judith Weston）
- **URL**：https://scalar.usc.edu/works/experiments-in-game-based-pedagogy/directing-with-action-verbs-game
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：学术教学页，版权归作者，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：南加大游戏化教学项目里的一个卡牌游戏，依据是 Judith Weston 的导演方法。原文："Actions speak louder than words. Verbs describe what someone is doing, so they are active rather than static; they describe experience rather than a conclusion about experience."。引用 Weston 的话："Although we can't decide how to feel, we can decide what to do."。页面的例子是：不要说 "You are sad in this scene"，而要交代情境（被伴侣分手、仍爱着对方），再给可以演的动作，"to persuade, to plead, or even to belittle"。游戏规则：每组拿 12 张动词卡，看一段戏后选出符合演员意图的动词，由评审团投票，多数获胜。
- **对本学院有什么用**：每个镜头给角色写一个任务动词（说服、逼问、试探、求饶），不写情绪形容词，再把动词翻译成看得见的形体节拍。
- **落点模块**：10-theory、20-craft、90-curriculum

### S-CRAFT-19 · Wikipedia — Stanislavski's system
- **URL**：https://en.wikipedia.org/wiki/Stanislavski%27s_system
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：CC BY-SA 4.0（Wikipedia 文本）
- **核实**：✅ 已打开核实
- **摘录**：词条列出斯坦尼斯拉夫斯基体系的核心概念。规定情境：剧作者、导演、设计者给出的全部情境。"魔术般的假如"："When I give a genuine answer to the if, then I do something"。任务（zadacha）："The task is the spur to creative activity, its motivation. The task is a decoy for feeling."。最高任务：贯穿全剧的总目标，把各个小段连成连续的贯穿动作线。小段与节拍按 "reversal points" 划分，也就是出现重大揭示或决定、改变戏剧走向的时刻。后期的形体动作方法重即兴、轻案头分析："The best analysis of a play is to take action in the given circumstances."。节奏（tempo-rhythm）源自他的歌剧工作，潜台词源自他排演契诃夫剧作的经验。
- **对本学院有什么用**：在季、集、场三级分别写"最高任务、场景任务、镜头动作"，节拍按反转点切分，让每条表演指令都能追溯到角色目标。
- **落点模块**：10-theory、90-curriculum

### S-CRAFT-20 · WeShop — Seedance 2.5 micro-expressions: can an AI face feel real
- **URL**：https://www.weshop.ai/solutions/models/seedance-2-5-micro-expressions-can-an-ai-face-feel-real
- **类型**：article
- **分类**：🟡 需适配
- **许可**：版权归 WeShop，仅借鉴写法
- **核实**：✅ 已打开核实
- **摘录**：WeShop 的 Seedance 2.5 微表情案例页。核心观点："The strongest part…is not the largest smile. It is the transition into it."。提示词不写 "look sad" 这类情绪标签，而写可观察的身体变化，例如 "Visible micro-movements of throat, jaw, lip corner, and brow throughout — every stage of suppression readable on her face." 和 "Her lips press together while her gaze remains controlled."。情绪弧分为压抑、泄露、释放、恢复、收束几个阶段，按时间段分节拍。机位要求 "locked-off camera, static shot, no panning, no zoom"，防止运动掩盖面部的不一致。其他建议："Avoid stacking unrelated style labels"；结尾要有明确收束，不要让最后几秒处于未定义状态；生成后检查眼睛、牙齿、手、发际线和脸型的一致性。
- **对本学院有什么用**：情绪特写写成分秒节拍（压抑、泄露、释放），用喉、下颌、嘴角、眉等解剖部位词；这类镜头锁定机位，不叠加运镜。〔学院推断：这是 Seedance 的案例，H3 上需要实测。〕
- **落点模块**：20-craft、50-rubrics、40-memory

### S-CRAFT-21 · BudgetPixel — Beyond the Blank Stare: prompting cinematic expressions
- **URL**：https://budgetpixel.com/blog/beyond-the-blank-stare-how-to-prompt-cinematic-expressions-and-psychological-depth
- **类型**：article
- **分类**：🟡 需适配
- **许可**：版权归作者，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：原文："Using basic words like "sad," "angry," or "happy" usually results in over-exaggerated, cartoonish expressions."，以及 "The AI tends to push facial features to their extremes"。建议改用暗示"眼神背后有故事"的修饰语："a look of quiet determination"、"a pensive, contemplative gaze"、"wistful nostalgia"、"a subtle, knowing smirk"。视线有两种处理：一种是直视镜头、打破第四堵墙的强烈凝视；另一种是看向画外、"lost in thought"。要求抓住瞬间而不是摆拍："caught in a fleeting moment of deep reflection"。表情要和环境匹配，冲突场景的例子是 "a battle-worn, resolute expression, tight jawline, defying the elements"。这些建议面向静帧人像生成。
- **对本学院有什么用**：在提示词 lint 里拦截裸情绪词（sad、angry、happy），改写成带潜台词的表情短语，并写明视线方向。
- **落点模块**：20-craft、50-rubrics、40-memory

### S-CRAFT-22 · AtlasCloud — 氛围感创作技巧指南（Vibe Creating）
- **URL**：https://www.atlascloud.ai/zh/blog/guides/vibe-creating-skill-tutorial
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权归 AtlasCloud，仅借鉴
- **核实**：✅ 已打开核实
- **摘录**：AtlasCloud 的教程，原文："你负责决定'我想感受什么'，而它负责解决'如何拍摄出来'"。示例：把"危险"翻译成浅景深聚焦枪口、低机位、广角畸变；把"孤独"翻译成极端尺度对比、去饱和的灰色调、伸向光的手、暖色回忆对冷色现实。A/B 测试的结论是："更多的技术细节并没有帮助。它反而起到了负面作用"。它的 Skill 提示词写明："默认删除或强调较少的内容：焦距、毫米数、摄像机位置术语、摄像机运动参数、镜号、景深、光圈、曝光、快门、设备说明"，同时"保留原始叙事顺序和情感推进"，并保留用户写的对白、旁白、音乐、音效原文。渲染用的是 Seedance 2.0。
- **对本学院有什么用**：先写情绪意图，再推导运镜和光色，删掉没有叙事动机的技术参数。〔学院推断：这是单一厂商在 Seedance 上做的 A/B，在 H3 上需要对照测试。〕
- **落点模块**：30-taste、20-craft

### S-CRAFT-23 · YouTube Help — Use music and sound effects from the Audio Library
- **URL**：https://support.google.com/youtube/answer/3376882?hl=en
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：YouTube 音频库：标准许可曲目和 CC 曲目；站外使用权限官方页没有说明
- **核实**：✅ 已打开核实
- **摘录**：官方原文："Music and sound effects from the YouTube Audio Library are copyright-safe."。加入 YouTube 合作伙伴计划的频道，可以对使用音频库音乐和音效的视频变现；从音频库下载的版权安全曲目 "won't be claimed by a rights holder through the Content ID system"。使用 Creative Commons 曲目时 "you must credit the artist in your video's description"，页面提供从 License type 列复制署名文本的方法；可以筛选 "Attribution not required"。官方提示 "Only music and sound effects from the Audio Library are known to YouTube to be copyright-safe."。页面没有说能不能在 YouTube 以外的平台使用。第三方 LicenseOrg（https://www.licenseorg.com/guide/music-audio/youtube-audio-library）称标准许可曲目 "restricted to YouTube videos"，CC BY 4.0 曲目 "may be used commercially on any platform with proper attribution"。
- **对本学院有什么用**：标准许可曲目只用于 YouTube 版本。抖音和其他平台只用 CC BY 曲目并自动写署名，或者换用 Pixabay、Sonniss 等允许跨平台的素材。
- **落点模块**：70-playbooks、40-memory、50-rubrics

### S-CRAFT-24 · Pixabay Content License Summary
- **URL**：https://pixabay.com/service/license-summary/
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Pixabay Content License（不是 CC0）；已核对摘要页和 Terms 页
- **核实**：✅ 已打开核实（另打开了 https://pixabay.com/service/terms/）
- **摘录**：摘要页允许的用途："Use Content for free"、"Use Content without having to attribute the author"、"Modify or adapt Content into new works"。禁止的用途：不加创作修改、以数字或实物形式单独出售或分发；含可识别商标、logo、品牌的内容不得商用，尤其不得用于商品；"You cannot use Content in any immoral or illegal way, especially Content which features recognisable people"；不得误导或欺骗性使用；不得用作商标、企业名或服务标志。Terms 页的授权条款是 "download, use, copy, modify or adapt the Content for commercial or non-commercial purposes"，对 Standalone 的定义是 "where no creative effort has been applied to the Content and it remains in substantially the same form"，对音频没有单独条款，也没有提到 Content ID。研究员原稿里"Pixabay 曲目可能下载后被注册 Content ID"出自竞品 Thematic 的说法，没有给出 URL，已移到"空白"一节。
- **对本学院有什么用**：Pixabay 音乐和音效作为跨平台的默认素材源。每首都保存下载时的页面 URL 和许可快照，以备被认领时申诉。
- **落点模块**：70-playbooks、40-memory

### S-CRAFT-25 · Free Music Archive — License Guide
- **URL**：https://freemusicarchive.org/License_Guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：每首曲目单独标 CC 许可（BY / BY-SA / BY-ND / BY-NC / BY-NC-SA / BY-NC-ND / CC0）
- **核实**：✅ 已打开核实
- **摘录**：FMA 曲目使用多种 CC 许可。CC BY 允许商用和改编，须署名；CC BY-SA 允许商用，但衍生作品要用相同许可发布；CC BY-ND 允许商用、不允许改编，原文 "Syncing a track to video/moving images constitutes a derivative work, which is prohibited by this licence."；带 NC 的都不能商用，"A commercial use is one primarily intended for commercial advantage or monetary compensation"；CC0 "No permission is needed"。另有原文："FMA cannot license original work to you for commercial, private, or other use."，也就是说商用资格由每首曲目的权利人决定。
- **对本学院有什么用**：从 FMA 只选 CC BY 或 CC0 曲目，自动拒绝 ND（配到画面上就违规）和 NC 曲目，并逐首记录许可。
- **落点模块**：70-playbooks、50-rubrics

### S-CRAFT-26 · Incompetech（Kevin MacLeod）— FAQ / licensing
- **URL**：https://incompetech.com/music/royalty-free/faq.html
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：CC BY 4.0（免费，须署名）；或付费 Standard License（免署名）
- **核实**：✅ 已打开核实
- **摘录**：Kevin MacLeod 的音乐以 CC BY 4.0 免费使用，署名格式为 "Title Kevin MacLeod (incompetech.com) Licensed under Creative Commons: By Attribution 4.0"（Title 换成曲名）。署名要放在 "a person who wants to know where the music came from should have no difficulty in finding it" 的位置。关于 YouTube，FAQ 原文："Yes, AND you can monetize the videos. Be sure to credit me."。流媒体站点可以用，须署名。无法署名的场合（如 "television broadcast or radio commercial, or some other format where credits are impossible"）可以购买 Standard License。FAQ 页没有写价格，也没有提到抖音或 TikTok。
- **对本学院有什么用**：用 Incompetech 曲目时，自动在简介或片尾写入标准署名串；无法放署名的平台不用这个库。
- **落点模块**：70-playbooks、40-memory

### S-CRAFT-27 · ccMixter
- **URL**：https://ccmixter.org/
- **类型**：asset-library
- **分类**：🟡 需适配
- **许可**：首页的 CC BY-NC 4.0 声明只针对站点文字和图片；曲目按各自的 CC 许可，需要逐首核对
- **核实**：✅ 已打开核实（更正了研究员原稿对许可范围的表述）
- **摘录**：首页原文："This text and images on this site are licensed under a Creative Commons Attribution-Noncommercial 4.0 International License."。这条声明的对象是站点的文字和图片，不是曲目本身，研究员原稿把它写成"站点主体 CC BY-NC 4.0"，范围有误。首页还写着 "you can use our music for free in your social media videos! Just give us credit"，并介绍 dig.ccMixter 可以 "by style, BPM, or instrument" 检索。首页没有写明商用授权的路径。第三方称 dig.ccMixter 有可商用分类，本次没有核实。
- **对本学院有什么用**：默认把 ccMixter 当作不可商用来源。只有逐首确认是 CC BY 或 CC0 时才用，变现剧集优先用其他库。
- **落点模块**：70-playbooks

### S-CRAFT-28 · Freesound — Help / FAQ（licenses）
- **URL**：https://freesound.org/help/faq/
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：每条音效单独标许可：CC0 / CC BY / CC BY-NC；旧上传可能是已退役的 Sampling+
- **核实**：✅ 已打开核实
- **摘录**：Freesound 现在有三种在用许可。CC0："you can do pretty much what you want with the sound"。CC BY："you should always mention the original creators"。CC BY-NC：同样要署名，但 "you can't earn any money"。Sampling+ 已被 Creative Commons 退役，退役前上传的音效仍沿用该许可，Freesound 无法追溯修改。只有 CC0 和 CC BY 可以商用。署名模板："This [video/theatre piece/...] uses these sounds from freesound: 'sound1' by user1 (http://freesound.org/s/soundID/) licensed under ..."；音效很多时可以写 "uses many sounds from freesound, for the full list see: [your-credits-page]"。用户账户里有 "attribution list"，汇总下载过的音效。
- **对本学院有什么用**：只入库 CC0 和 CC BY 音效，自动生成 credits 页，过滤掉 NC 和 Sampling+。
- **落点模块**：70-playbooks、40-memory、50-rubrics

### S-CRAFT-29 · Sonniss — GDC Game Audio Bundle
- **URL**：https://sonniss.com/gameaudiogdc
- **类型**：asset-library
- **分类**：🟢 可直接用
- **许可**：Sonniss 免版税许可：可商用、免署名、禁止单独转售、禁止 AI/ML 训练
- **核实**：✅ 已打开核实
- **摘录**：原文："royalty free and commercially usable"，"No attribution is required"，可用于 "unlimited number of projects for the rest of your lifetime"。适用于游戏、影视、电视、播客、YouTube、TikTok、广告。限制：不得作为单独文件或音效库转售或再分发，但可以作为成品创作的一部分出售；"AI/ML training is strictly prohibited under our license."。归档合集覆盖 2015 到 2024 年：GDC 2024 分 9 部分，2020 年分 14 部分，2019 和 2018 年各 8 部分，2017 年 9 部分，2016 年 6 部分，2015 年 5 部分。
- **对本学院有什么用**：作为后期拟音、冲击声、环境声的主力本地库，素材元数据里标注"禁止用于模型训练"。
- **落点模块**：70-playbooks、40-memory

### S-CRAFT-30 · BBC Sound Effects（RemArc 许可）
- **URL**：https://sound-effects.bbcrewind.co.uk/licensing
- **类型**：asset-library
- **分类**：⚪ 仅借鉴
- **许可**：BBC RemArc 许可：只限非商业的个人或研究用途、正规教育用途；商用须向 Pro Sound Effects 购买
- **核实**：✅ 已打开核实（页面用 JS 渲染，WebFetch 被拒；改用 curl 取该站的前端脚本 /static/js/main.c5b8bbec.js，从中提取许可正文核对；研究员原稿标为未核实，现已补核）
- **摘录**：站点无脚本时的提示文字是：可搜索 "over 30,000 BBC sound effects"，可 "use them in your own personal/educational projects, or licence them for use"。许可正文 "The BBC's Content Licence for RemArc" 中允许的用途：非商业的个人或研究用途；学生或学校、学院、大学教职员的正规教育用途。以下用途须先取得许可并可能收费：工作用途、商业用途、非营利与政府机构用途、"text and data mining, computer analysis or to develop or train artificial intelligence"。禁止事项包括 "Sharing our content. For example, no uploading to social media sites."，以及从内容中获利。下载弹窗写着 "Commercial use of this content is not allowed under the RemArc license."，商用须到 Pro Sound Effects 购买。
- **对本学院有什么用**：把 BBC 音效库列入禁用名单，因为即使不变现，上传社交平台也被禁止。确实需要时改走 Pro Sound Effects 付费授权。
- **落点模块**：70-playbooks、50-rubrics

### S-CRAFT-31 · Adobe Source Han Sans / Source Han Serif（思源黑体 / 思源宋体）
- **URL**：https://github.com/adobe-fonts/source-han-sans
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：SIL OFL 1.1，保留字体名 "Source"；已核对两个仓库的 LICENSE.txt（黑体 Copyright 2014-2025，宋体 2017-2022）
- **核实**：✅ 已打开核实（经 raw.githubusercontent.com 读取 LICENSE.txt 和 README.md）
- **摘录**：思源黑体和思源宋体（https://github.com/adobe-fonts/source-han-serif）都以 SIL OFL 1.1 发布，保留字体名 "Source"，Source 是 Adobe 的商标。OFL 前言："The OFL allows the licensed fonts to be used, studied, modified and redistributed freely as long as they are not sold by themselves."；字体可以和软件捆绑、嵌入、再分发或一起出售，但衍生字体不得使用保留名。第 5 条："The requirement for fonts to remain under this license does not apply to any document created using the Font Software."，即用这些字体制作的画面和视频不受字体许可约束。黑体 README 列出的下载格式有 OTF、OTC、Super OTC、Subset OTF、Variable OTF/TTF/WOFF2。
- **对本学院有什么用**：思源黑体和思源宋体作为硬字幕和程序化叠层字卡的默认字体；仓库内如随附字体文件，同时附上 LICENSE 文本。
- **落点模块**：70-playbooks、40-memory、20-craft

### S-CRAFT-32 · LXGW WenKai 霞鹜文楷
- **URL**：https://github.com/lxgw/LxgwWenKai
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：SIL OFL 1.1，保留名：霞鹜、霞鶩、落霞孤鹜、落霞孤鶩、LXGW；已核对 OFL.txt
- **核实**：✅ 已打开核实（经 raw.githubusercontent.com 读取 OFL.txt 和 README.md）
- **摘录**：一款开源中文楷体，由 Fontworks 的 Klee One 衍生，以 SIL OFL 1.1 发布。README 原文："这款字体无论是个人还是企业都可以自由使用，包括商用，无需付费，也无需另行知会原作者"；可以安装到系统、嵌入软件或 APP、与软件捆绑再分发或一起销售，再分发时须附 OFL.txt 全文；"禁止单独出售字体文件"；未经作者书面授权，衍生字体不得使用保留名。共三个字重（Light、Regular、Medium），另有 Screen、Lite、GB、TC、KR 等变体。作者说明这款字体 "并不太适合大段正文排版"，更适合中等长度的文本。README 还写道：如果单位法务不认可 OFL 1.1、要求传统授权证明，建议改用其他字体。
- **对本学院有什么用**：古风、文艺、回忆类字卡和片名用霞鹜文楷，作为思源之外的风格字体。
- **落点模块**：70-playbooks、30-taste

### S-CRAFT-33 · Smiley Sans 得意黑
- **URL**：https://github.com/atelier-anchor/smiley-sans
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：SIL OFL 1.1，保留名 Smiley / 得意黑；已核对 LICENSE（Copyright 2022--2024 atelierAnchor）
- **核实**：✅ 已打开核实（经 raw.githubusercontent.com 读取 LICENSE 和 README.md）
- **摘录**：得意黑是一款"在人文观感和几何特征中寻找平衡的中文黑体"，"整体字身窄而斜"，细节借鉴手绘美术字。字符覆盖：GB/T 2312-1980 的全部 6763 个汉字和《通用规范汉字表》的全部 8105 个汉字，加上补充字共 8335 个汉字；另有拉丁字母 415 个、西里尔字母 80 个、希腊字母 71 个、假名 174 个。README 说明部分笔画和结构"并未严格遵循中国大陆规范汉字写法"。推荐场景是平面海报、电商文案、"视频标题及字幕"、书报标题、游戏嵌入；不推荐用于正文排版、编程代码、手机界面。
- **对本学院有什么用**：封面大标题、集名卡、钩子字卡用得意黑；对白字幕仍用思源黑体，因为得意黑不遵循规范字形，长句可读性差。
- **落点模块**：70-playbooks、30-taste

### S-CRAFT-34 · 阿里巴巴普惠体 3.0 法律声明
- **URL**：https://www.yuque.com/yiguang-wkqc2/hgpff0/nus9wiinq4aeiegy
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：阿里巴巴专有免费许可（不是 OFL），可商用
- **核实**：✅ 已打开核实（WebFetch 返回 503，改用语雀文档接口取正文核对；另在 alibabafonts.com 前端脚本中确认，该链接就是普惠体 3.0 的 legalStatementLink）
- **摘录**：3.0 版在 2.0 基础上新增了符合 GB18030-2022 的简体中文字库（7 款字重），现有简体中文 9 款字重，越南文、泰文、韩文、日文各 3 款，繁体中文 Big5 和 HK 各 4 款。授权原文："该授权是免费的普通许可，用户可基于合法目的用于商业用途或非商业用途"。未经书面授权不得做的事：对字体"进行仿制、转换、翻译、反编译、反向工程、拆分、破解"；删除、覆盖或修改法律声明；"单独定价出售、出租、出借、转让、转授权"；发布让外界误以为与阿里巴巴有合作、赞助或背书关系的不实信息。从非官方渠道下载造成的损失，阿里巴巴不承担责任。适用中华人民共和国法律，由浙江省杭州市有管辖权的人民法院管辖。
- **对本学院有什么用**：普惠体可以用于字幕、字卡和封面，但不改字体文件、不在仓库里再分发字体文件，只记录官方下载地址。
- **落点模块**：70-playbooks、40-memory

### S-CRAFT-35 · MiSans 字体知识产权许可协议（小米）
- **URL**：https://hyperos.mi.com/font/zh/download/
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：小米专有免费许可：可商用，但须"在软件中特别注明"，且不得改编
- **核实**：✅ 已打开核实（协议正文在本 URL；FAQ 原句在 https://hyperos.mi.com/font/zh/faq/，已一并核对）
- **摘录**：协议授予"一份不可转让的、非独占的、免版税的、可撤销的、全球性的版权许可"，条件有三。一是"您应在软件中特别注明使用了 MiSans 字体"。二是"您不得对 MiSans 字体或其任何单独组件进行改编或二次开发"。三是不得单独将字体或其组件对外租赁、再许可、给予、出借、再分发或售卖；"此限制不适用于您使用 MiSans 字体创作的任何其他作品。如您使用 MiSans 字体创作宣传素材、logo、应用 App 等，您有权分发或出售该作品"。FAQ 页原文："MiSans Global 所有的字体都是供全球免费商用，您可以在任何平台、任何商业项目中使用所有字体"。协议是"可撤销"的；"在软件中特别注明"这一条用在视频作品上该怎么履行，页面没有说明。
- **对本学院有什么用**：用 MiSans 时在片尾或简介的字体致谢里注明 MiSans，不改字形，不随包分发字体文件。〔学院推断："片尾注明"能否满足"在软件中注明"这一条，尚未得到小米确认。〕
- **落点模块**：70-playbooks、40-memory

### S-CRAFT-36 · 站酷字体专题页（站酷快乐体 / 高端黑 / 酷黑等）
- **URL**：https://www.zcool.com.cn/special/zcoolfonts/
- **类型**：asset-library
- **分类**：🟡 需适配
- **许可**：站酷专题页声明"免费授权全社会使用（包括商用）"；没有找到完整授权协议
- **核实**：✅ 已打开核实（只核了专题页文字）
- **摘录**：专题页列出 8 款免费字体：站酷仓耳渔阳体、站酷庆科黄油体、站酷文艺体、站酷小薇LOGO体、站酷酷黑体、站酷意大利体、站酷快乐体、站酷高端黑体，每款都标着"免费授权全社会使用（包括商用）"。页面上每款字体附有设计者信息，但没有写明是否必须署名，也没有更细的限制条款。页面另外提到通过 Hellorf 平台提供"中小企业授权"和企业授权。研究员原稿把它分为"可直接用"，因为没有看到完整协议，已降为"需适配"。
- **对本学院有什么用**：综艺感、喜剧类字卡可以用站酷免费字体，但素材登记时注明"仅依据专题页声明，未见完整协议"，商业变现剧集优先用 OFL 字体。
- **落点模块**：70-playbooks

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-CRAFT-01 | 据 Auphonic 2020 年文章转述：Netflix 规格为 "-27 LKFS +/- 2 LU dialog-gated"，旧规格为 -24 LKFS ±2 LU 全节目测量；推荐整体 LRA 4–18 LU、对白 LRA ≤7 LU；LSR（语音与整体响度之差）≤5 LU 最适合多数作品。该页没有真峰值数值，Netflix 当前规格原页本次没有打开。 | [Auphonic](https://auphonic.com/blog/2020/10/08/dialog-loudness-normalization/) | 中（二手转述，2020 年） |
| F-CRAFT-02 | EBU R 128 的节目响度目标是 -23 LUFS，容差 ±0.5 LU（自 3.0 版起），现行 5.0 版发布于 2023 年 11 月；R128 s4（2023-11-08）针对电影化内容，用 LDR（节目响度减对白响度）描述对白与整体的落差，并声明不作为故事片制作建议。 | [EBU R128](https://tech.ebu.ch/publications/r128)、[EBU R128 s4](https://tech.ebu.ch/publications/r128s4) | 高 |
| F-CRAFT-03 | AES TD1008 的流媒体分发建议：语音与混合内容 -18 LUFS，音乐 -16 LUFS；这些数字给平台做归一化用，不是给混音或母带工程师的交付目标。 | [Production Advice](https://productionadvice.co.uk/td1008/) | 中（解读文章，AES 原文未打开） |
| F-CRAFT-04 | ffmpeg loudnorm 的默认值是 I=-24、LRA=7、TP=-2，linear 默认 true；如果目标 LRA 低于源 LRA，或增益会让真峰值超过 TP，就退回动态模式，动态模式上采样到 192 kHz 测真峰值。sidechaincompress 的默认值是 threshold 0.125、ratio 2、attack 20 ms、release 250 ms，可以用对白轨去压音乐轨。 | [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html) | 高 |
| F-CRAFT-05 | Murch 的 "Law of Two-and-a-half"：同类声音到三层时，感知从"个体"变成"群体"；各层均匀分布在 Encoded（对白）到 Embodied（音乐）光谱上时，上限约为五层，挤在同一区域时只有 2.5 层。《现代启示录》直升机段有六个预混层，终混同一时刻最多五层。 | [Transom / Murch](https://transom.org/2005/walter-murch/) | 高 |
| F-CRAFT-06 | J/L-cut 时长经验："a half-second overlap in a dialogue scene is often enough"，"a two-second J-cut into a major sequence creates real anticipation"；两人对话默认用 L-cut 切到听者反应。 | [FilmDaft](https://filmdaft.com/the-l-cut-and-j-cut-how-film-editors-use-audio-to-control-time/) | 中（单篇剪辑博客） |
| F-CRAFT-07 | 给 AI 视频补声音的顺序：静音审片列"缺失"，铺一条连续环境床，只给可见动作配拟音，音乐最后按节拍加，层级为对白 > 拟音 > 环境 > 音乐，每个声音元素都记录工具、提示词和参数。 | [HackerNoon](https://hackernoon.com/ai-video-comes-out-silent-here-is-the-sound-design-workflow-i-run-on-every-shot) | 中（个人经验） |
| F-CRAFT-08 | Sora 2 官方：每个镜头一个明确运镜加一个明确主体动作；4 秒片段通常容纳一到两句短对白；点名 3–5 个颜色锚点可以稳定跨镜头调色板；无对白镜头用 "distant traffic hiss" 这类简单声音提示当节奏标记。 | [Sora 2 Prompting Guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | 高 |
| F-CRAFT-09 | Veo 3.1 官方音频写法：对白放在引号里、跟在说话人后，音效写 "SFX: ..."，环境声写 "Ambient noise: ..."；支持 [00:00-00:02] 形式的时间戳多镜头提示；情绪可以单写一行 "Emotion: ..."。 | [Veo 3.1 Guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1) | 高 |
| F-CRAFT-10 | 可灵 2.6 官方：说话人用唯一且一致的 [Character Name]，情绪标签紧跟其后；语音只支持中文和英文；三人及以上对白效果下降，两人最好；唱歌或对白场景建议用 10 秒时长。 | [Kling 2.6 Audio Guide](https://kling.ai/quickstart/klingai-video-26-audio-user-guide) | 高 |
| F-CRAFT-11 | MiniMax H3 官方：最长 15 秒、默认 2K、原生立体声；"No separation between voice, sound effects, and music — all jointly modeled"；支持原生多镜头建模。 | [MiniMax H3 Blog](https://www.minimax.io/blog/minimax-h3) | 高 |
| F-CRAFT-12 | 低调光的主辅光比约 8:1，"typically used in thrillers, horrors, or dark dramas"；高调光接近 1:1，见于 "comedies, sitcoms, or rom-coms"。 | [StudioBinder Key Light](https://www.studiobinder.com/blog/what-is-key-light) | 中 |
| F-CRAFT-13 | 动机光规则：光要能在场景里 "justified"（窗、门、灯、屏幕、蜡烛、火、月光、车灯）；补光色温要和光源一致，月光偏冷，烛光偏暖。 | [StudioBinder Motivated Lighting](https://studiobinder.com/blog/what-is-motivated-lighting-in-film) | 高 |
| F-CRAFT-14 | 据 Hyperallergic 书评，皮克斯是 "the first to create a color script for each of its films"，色彩脚本用来 "map out the emotional beats of a story"；《玩具总动员》在危险段落转为 "bleak and muddy"。 | [Hyperallergic](https://hyperallergic.com/610771/the-art-of-pixar-chronicle-books/) | 中（书评转述） |
| F-CRAFT-15 | Weston 动作动词法："Although we can't decide how to feel, we can decide what to do."；不要说 "You are sad in this scene"，而要给可以演的动作 "to persuade, to plead, or even to belittle"。 | [USC Scalar](https://scalar.usc.edu/works/experiments-in-game-based-pedagogy/directing-with-action-verbs-game) | 高 |
| F-CRAFT-16 | 斯坦尼斯拉夫斯基体系：任务是 "a decoy for feeling"；小段与节拍按 "reversal points"（重大揭示或决定）划分；最高任务把各段连成贯穿动作线。 | [Wikipedia](https://en.wikipedia.org/wiki/Stanislavski%27s_system) | 高 |
| F-CRAFT-17 | 用 "sad""angry""happy" 这类基础情绪词生成人像，"usually results in over-exaggerated, cartoonish expressions"；应改写为带潜台词的表情短语，并写明视线方向。 | [BudgetPixel](https://budgetpixel.com/blog/beyond-the-blank-stare-how-to-prompt-cinematic-expressions-and-psychological-depth) | 中（单篇博客，针对静帧） |
| F-CRAFT-18 | Seedance 2.5 微表情案例：用 throat、jaw、lip corner、brow 等解剖部位词，按压抑、泄露、释放、恢复分时段写节拍，机位 "locked-off camera, static shot, no panning, no zoom"，结尾要有明确收束。 | [WeShop](https://www.weshop.ai/solutions/models/seedance-2-5-micro-expressions-can-an-ai-face-feel-real) | 中（厂商案例页） |
| F-CRAFT-19 | AtlasCloud 的 A/B 结论："更多的技术细节并没有帮助。它反而起到了负面作用"；它的 Skill 默认删除焦距、机位术语、镜号、景深、光圈等，保留叙事顺序、情感推进和用户写的声音内容。 | [AtlasCloud](https://www.atlascloud.ai/zh/blog/guides/vibe-creating-skill-tutorial) | 低（单一厂商在 Seedance 上的测试） |
| F-CRAFT-20 | FMA：CC BY-ND 曲目 "Syncing a track to video/moving images constitutes a derivative work, which is prohibited"；"FMA cannot license original work to you"，商用资格逐首由权利人决定。 | [FMA License Guide](https://freemusicarchive.org/License_Guide) | 高 |
| F-CRAFT-21 | Freesound 现有三种在用许可 CC0、CC BY、CC BY-NC，另有已退役但仍存在于旧上传中的 Sampling+；只有 CC0 和 CC BY 可以商用，CC BY 按固定模板署名。 | [Freesound FAQ](https://freesound.org/help/faq/) | 高 |
| F-CRAFT-22 | Sonniss GDC 合集可商用、免署名，可用于 TikTok、YouTube、影视；禁止单独转售，"AI/ML training is strictly prohibited"。 | [Sonniss GDC](https://sonniss.com/gameaudiogdc) | 高 |
| F-CRAFT-23 | YouTube 音频库的版权安全曲目在 YouTube 上可以变现，"won't be claimed ... through the Content ID system"；CC 曲目须在描述中署名；官方页没有说明能否在站外使用。 | [YouTube Help](https://support.google.com/youtube/answer/3376882?hl=en) | 高 |
| F-CRAFT-24 | 第三方解读：YouTube 音频库标准许可曲目 "restricted to YouTube videos"，CC BY 4.0 曲目 "may be used commercially on any platform with proper attribution"。 | [LicenseOrg](https://www.licenseorg.com/guide/music-audio/youtube-audio-library) | 中（第三方，无官方佐证） |
| F-CRAFT-25 | Pixabay Content License：可商用、无需署名、可修改；禁止未经创作修改的单独出售或分发、含商标内容商用、不道德或违法使用（尤其涉及可识别人物）、误导性使用、用作商标；对音频没有单独条款。 | [Pixabay License Summary](https://pixabay.com/service/license-summary/)、[Pixabay Terms](https://pixabay.com/service/terms/) | 高 |
| F-CRAFT-26 | BBC 音效库 RemArc 许可：只限非商业的个人或研究用途、正规教育用途；"Sharing our content. For example, no uploading to social media sites."；商用、文本与数据挖掘、AI 训练都须先取得许可；商用音效须向 Pro Sound Effects 购买。 | [BBC Sound Effects Licensing](https://sound-effects.bbcrewind.co.uk/licensing) | 高（从官方站前端脚本提取的原文） |
| F-CRAFT-27 | SIL OFL 1.1 第 5 条："The requirement for fonts to remain under this license does not apply to any document created using the Font Software."，即用 OFL 字体烧录的字幕和视频不受字体许可约束；字体文件本身不得单独出售。 | [Source Han Sans](https://github.com/adobe-fonts/source-han-sans) | 高 |
| F-CRAFT-28 | 阿里巴巴普惠体 3.0："免费的普通许可，用户可基于合法目的用于商业用途或非商业用途"；禁止仿制、转换、反编译、拆分字库，禁止删改声明，禁止单独定价出售、出租、出借、转让、转授权，禁止暗示与阿里巴巴存在合作、赞助或背书关系。 | [普惠体 3.0 法律声明](https://www.yuque.com/yiguang-wkqc2/hgpff0/nus9wiinq4aeiegy) | 高 |
| F-CRAFT-29 | MiSans：全球免费商用，但许可"可撤销"；须"在软件中特别注明使用了 MiSans 字体"，不得改编或二次开发，不得单独再分发或售卖字体；用它创作的宣传素材、logo、App 可以分发或出售。 | [MiSans 下载与协议](https://hyperos.mi.com/font/zh/download/)、[MiSans FAQ](https://hyperos.mi.com/font/zh/faq/) | 高 |
| F-CRAFT-30 | Incompetech 的 CC BY 4.0 标准署名串是 "Title Kevin MacLeod (incompetech.com) Licensed under Creative Commons: By Attribution 4.0"；用于 YouTube 可以变现，须署名。 | [Incompetech FAQ](https://incompetech.com/music/royalty-free/faq.html) | 高 |
| F-CRAFT-31 | ComfyUI-KJNodes 是 GPL-3.0，依赖的 color-matcher 也是 GPL-3.0；旧版 ColorMatch 节点已标 DEPRECATED，ColorMatchV2 提供 mkl、hm、reinhard、mvgd、hm-mvgd-hm、hm-mkl-hm、reinhard_lab_gpu 方法，strength 取值 0–10。 | [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes) | 高 |
| F-CRAFT-32 | 得意黑推荐用于"视频标题及字幕"、海报等，不推荐用于正文排版、编程代码、手机界面；部分笔画"并未严格遵循中国大陆规范汉字写法"。 | [Smiley Sans](https://github.com/atelier-anchor/smiley-sans) | 高 |

## 空白与未找到

1. **短视频平台响度规格**：抖音、快手、视频号、TikTok、Reels 都没有找到官方响度文档。YouTube 的 -14 LUFS 只来自二手资料（Production Advice 称"多数流媒体当前用 -14 LUFS"）。委托方现行的 -16 LUFS 目标没有平台官方依据可以对照。
2. **Netflix 规格原页**：原页已迁到 studiopartner.netflix.net，是 JS 渲染，抓不到正文；数值来自 Auphonic 2020 年的转述（F-CRAFT-01），2026 年是否仍然有效没有核实。研究员原稿里的"真峰值 ≤ -2 dBTP"在 Auphonic 页上找不到，已删除。
3. **AES TD1008 原文**：26 页的 PDF 本次没有打开，只看了解读文章。研究员原稿里"-17 LUFS 折中"和"移动端增益不足是流媒体响度更高的原因"来自搜索摘要，页面上没有，已删除。
4. **竖屏手机观看的调色、亮度、暗部安全指南**：没有找到权威来源。
5. **中文微短剧行业资料**：中文行业里关于声音设计、调色、表演指导的一手文章本轮没有覆盖。研究员和本轮核实共用的 WebSearch 配额（200 次）已经用完，核实阶段无法补搜。
6. **封面与字体平台**：OPPO Sans、HarmonyOS Sans 的许可原文（协议在下载包内），Canva（403）、稿定设计（405）、创客贴（JS 渲染）的授权都没有核实。站酷字体只核了专题页声明，没有看到完整协议（S-CRAFT-36）。
7. **MiSans 署名在视频上如何履行**：协议要求"在软件中特别注明"，用在视频作品上的具体做法没有官方说明（S-CRAFT-35）。
8. **Pixabay 与 Content ID**：研究员原稿引用竞品 Thematic 的说法，称 Pixabay 曲目可能在下载后被第三方注册 Content ID，但没有给出 URL，本轮无法核实，已从条目中移除。这个风险本身值得在实际上传中留意。
9. **YouTube 音频库的站外使用**：官方页没有说明，只有第三方 LicenseOrg 的解读（F-CRAFT-24）。
10. **ccMixter 可商用曲目**：dig.ccMixter 的"free for commercial use"分类及其实际许可没有抓取核验；Incompetech 付费 Standard License 的价格也没有找到。
11. **H3 声音分层**：H3 官方博客只说明人声、音效、音乐联合建模。"生成阶段不出乐、后期整场铺乐"能否解决剪辑点音乐断裂，以及 overall_soundscape 中写多少层声源合适，都是学院推断，需要实测（见 S-CRAFT-12 的验证方法）。
12. **静音与 room tone 的数字化规则**：没有找到"把静音当作强调"的权威可量化来源。
13. **Lasseter 关于"情绪越强颜色越浓"的引语**：只在研究阶段的搜索摘要中出现过，任何已打开的页面上都没有看到原句，所以没有收录。
14. **AI 视频表演**：关于呼吸、身体语言、多人对手戏表演的提示方法，只有两篇厂商或个人博客（S-CRAFT-20、S-CRAFT-21），而且都不是基于 H3。没有找到中文表演指导面向 AI 视频的资料。
