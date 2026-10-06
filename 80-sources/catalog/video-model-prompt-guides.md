# 主流视频模型官方提示词指南（交叉验证"模型脾气"）

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：22 ｜ 核实方式：逐条 WebFetch 打开核对

## 一句话结论

本专题收了 Sora、Veo、Runway、可灵、Seedance、万相、Wan2.2、LTX、Vidu 的官方提示词或参数文档，加上 Luma 对 H3 的第三方解读和 H3 官方指南作对照基准。几家文档能互相印证的规则有七条：文本里的否定句不可靠；首帧决定构图，文本偏离首帧会引发切镜；一镜只写一个运镜、一个主动作；时段内事件太密会碎切或漏情节；情绪要写成可见动作；模型默认偏慢；模型会自行加字幕、水印或配乐。仍然缺的有：任何一家给出的台词字/秒硬数字；"擅自加首饰、盔甲"的官方条目；轴线与跨镜空间连续规则。另有两处厂商建议互相矛盾（多角度参考图要不要给、要不要复述首帧），在 H3 上还没有受控对比。

## 条目

### S-VGEN-01 · OpenAI Sora 2 Prompting Guide（Cookbook）
- **URL**：https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：MIT（同文 notebook 位于 openai/openai-cookbook 仓库 examples/sora/，仓库 LICENSE 为 MIT，已核对）；developers.openai.com 页面本身未标许可
- **核实**：✅ 已打开核实（另对照 openai-cookbook 仓库 notebook 原文）
- **摘录**：把写提示比作给"没看过分镜的摄影师"做简报。model、size、seconds 只能用 API 参数设定，"You cannot request them in prose"；sora-2 时长可选 4/8/12/16/20 秒，默认 4。模板是散文场景描述加 Cinematography、Actions、Dialogue 三块。原文："Each shot should have one clear camera move and one clear subject action"；多镜头时每个镜头块只放一个机位、一个动作、一套光照。动作写成可数节拍，如走四步到窗边、停顿、最后一秒拉窗帘。台词："a 4-second shot will usually accommodate one or two short exchanges"，8 秒可多几句，长台词难对口型。图像是首帧锚点，文本决定之后发生什么。点名三到五种颜色可稳定调色板。修改要 "nudging, not gambling"，一次改一处。一次最多引用 2 个已上传角色；扩展最多 6 次、共 120 秒。
- **对本学院有什么用**：agent 写每个 shot 时强制"一镜一运镜一主动作 + 可数节拍"，并按时长预算台词句数。
- **落点模块**：10-theory、20-craft、50-rubrics、70-playbooks

### S-VGEN-02 · Google Cloud Blog: The ultimate prompting guide for Veo 3.1
- **URL**：https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- **类型**：article
- **分类**：🟡 需适配
- **许可**：Google 博客，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：2025-10-16 发布。公式为 [Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]。音频分三类：台词放引号里（A woman says, "We have to leave now."），音效用 "SFX:" 前缀，环境声用 "Ambient noise:"。否定要改写成具体场景："a desolate landscape with no buildings or roads" 优于 "no man-made structures"。时间戳多镜头示例在 8 秒内写了 [00:00-00:02] 到 [00:06-00:08] 四个镜头。Ingredients to Video 用人物、场景参考图让多个镜头保持一致；首尾帧模式只需 "describe the transition and the audio you want"，示例是 180° arc shot。时长 4/6/8 秒，16:9 或 9:16，720p/1080p，全部带 SynthID 水印。
- **对本学院有什么用**：作为"时间戳分镜 + 音频分类"写法的对照样本。示例里每镜 2 秒，这种密度在短剧里就是碎镜（对照〔委托方实证·A1〕），不得当作 H3 模板照搬〔学院推断〕。
- **落点模块**：10-theory、20-craft、60-casebook

### S-VGEN-03 · Vertex AI: Veo video generation prompt guide
- **URL**：https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：页脚注明内容 CC BY 4.0、代码示例 Apache-2.0（已核实）
- **核实**：✅ 已打开核实（页面最后更新 2026-10-05）
- **摘录**：提示要素列为 Subject、Action、Scene or context、Camera angles、Camera movements、Lens and optical effects、Visual style & aesthetics、Temporal elements、Audio 等。运镜词有 Static、Pan、Tilt、Dolly、Truck、Pedestal、Zoom、Crane、Aerial/drone、Handheld、Whip pan、Arc；rack focus、vertigo effect（dolly zoom）归在镜头与光学效果里。负向提示：不推荐 "no"、"don't" 这类指令式写法（例如避免 "no walls"），推荐只写不想看到的东西的名词（"wall, frame"）。音频："We recommend that you use separate sentences in your prompt to describe the audio"，分音效、环境声、对白三类，对白示例是 "the man in the red hat says: Where is the rabbit?"。另注明部分高级机位和镜头 "not officially supported"，效果因提示而异。
- **对本学院有什么用**：为"否定分层"提供官方依据：文本内否定句不可靠，负向内容只能以名词清单进入有负向通道的模型。H3 本地管线 cfg=1.0，负向通道无效〔委托方实证·T-2〕。
- **落点模块**：10-theory、20-craft、40-memory

### S-VGEN-04 · MIT Technology Review: Google's generative video model Veo 3 has a subtitles problem
- **URL**：https://www.technologyreview.com/2025/07/15/1120156/googles-generative-video-model-veo-3-has-a-subtitles-problem
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：Rhiannon Williams，2025-07-15。Veo 3 在含对白的片段里频繁生成乱码烧录字幕，图注示例为 "Appreclarry, I was buwn't cav're tryying not die!"。广告创意总监 Mona Weiss 称有对白的场景 "up to 40% of its output has gibberish subtitles that make it unusable"。Clark University 的 Shuo Niu 解释：训练数据可能含大量自带字幕的 YouTube 视频、vlog、游戏频道和 TikTok 剪辑，模型学到加字幕能提高与人类视频的相似度。Stony Brook University 的 Tuhin Chakrabarty 指出负向提示通常不如正向有效。Google 的 Josh Woodward 6 月 9 日称已开发修复，一个多月后用户仍在报告。用户的办法只有重抽、外部去字幕工具或裁切。
- **对本学院有什么用**：作为"有人说话就出字幕"的公开案例进入 casebook（对照〔委托方实证·D1〕），支撑对每条含对白片段做画面文字 OCR 检测。
- **落点模块**：60-casebook、10-theory、50-rubrics

### S-VGEN-05 · Runway: Gen-4 Video Prompting Guide
- **URL**：https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：Runway 帮助中心，版权所有，仅引用
- **核实**：✅ 已打开核实（网页对 WebFetch 返回 403；经同站 Zendesk 公开 API 取同一篇文章正文核对，更新于 2026-07-30）
- **摘录**：Gen-4 生成 5 或 10 秒。先写只含核心运动的简单句，再一次加一个元素：Subject motion、Camera motion、Scene motion、Style descriptors。原文："Negative phrasing is not supported and may produce unpredictable or even opposite results"，例如用 "Locked camera. The camera remains still." 代替 "No camera movement."。抽象概念要换成具体动作（"The woman smiles and waves."）。"Reiterating elements that exist within the image in high detail can lead to reduced motion or unexpected results"。主体用 "the subject" 或代词指代；多主体用位置语言（"The subject on the left walks forward. The subject on the right remains still."）。避免对话式、命令式提示，避免在一条里塞多次场景切换和变形。
- **对本学院有什么用**：I2V 提示里删掉对首帧外观的复述，改用位置语言指代角色，否定句一律改写为正向描述。
- **落点模块**：10-theory、20-craft、50-rubrics

### S-VGEN-06 · Runway: Image to Video Prompting Guide（Gen-4.5）
- **URL**：https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：Runway 帮助中心，版权所有，仅引用
- **核实**：✅ 已打开核实（网页 403，经 Zendesk 公开 API 取正文，更新于 2026-04-20）
- **摘录**：原文："your image defines composition, subject matter, lighting, and style"，提示词写运动、运镜和时间推进；只有引入新元素、大幅变化、变形或多元素交互时才需要写视觉描述。推荐结构 "The camera [motion description] as the subject [action]."。FAQ：输入图带运动模糊、动作中的姿态、方向线等隐含运动线索时，与之矛盾的运动提示 "may require more iteration"。示例中带尘土和运动模糊的车图配 "The car is parked and completely motionless" 未达预期，去掉线索后同一提示成功。出现不想要的切镜，先加长时长，仍切就加 "Continuous, seamless shot"。模型天生要产生运动，可写 "The locked-off camera remains perfectly still."，再后期稳定。长序列可取上一段末帧作下一段输入。输入图里的糊手糊脸会在视频中被放大。
- **对本学院有什么用**：关键帧要预置下一动作的起势和朝向；文本运镜不得与首帧的隐含运动矛盾。
- **落点模块**：10-theory、20-craft、50-rubrics、60-casebook

### S-VGEN-07 · Runway: Introduction to Prompting（Gen-4.5，含同系列 Text to Video Prompting Guide）
- **URL**：https://help.runwayml.com/hc/en-us/articles/47313698911891-Introduction-to-Prompting
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：Runway 帮助中心，版权所有，仅引用
- **核实**：✅ 已打开核实（网页 403，经 Zendesk 公开 API 取正文，更新于 2026-06-27；T2V 指南同法核对）
- **摘录**：迭代是常态；简单提示适合探索，详细提示适合定稿。正向表达："When you say what not to include, the model still has to interpret that concept and may include it anyway"（❌ not blurry ✅ sharp focus）。避免 beautiful、professional 这类主观词，避免矛盾指令（戏剧阴影配柔和均匀光）。多段落超长提示 "can paradoxically lead to unexpected or unnatural results"。排错：剥离到核心概念，再一次加回一个细节。FAQ："JSON formatting is ignored by generative models– what matters is the detail provided within the prompt"。同系列 T2V 指南（https://help.runwayml.com/hc/en-us/articles/47313737321107-Text-to-Video-Prompting-Guide）：提示开头没有优先权；时间戳要符合动作真实耗时（走过房间给 00:00–00:03，不是 0.5 秒）；T2V 不受起始画面约束，复杂运动比 I2V 好处理。
- **对本学院有什么用**：支撑"结构只在模型训练过该格式时才起作用"的判断〔学院推断〕，并提供"剥离、逐项加回"的排错流程。
- **落点模块**：10-theory、30-taste、70-playbooks

### S-VGEN-08 · Kling VIDEO 3.0 Model User Guide（可灵 3.0 官方指南）
- **URL**：https://kling.ai/quickstart/klingai-video-3-model-user-guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：快手可灵官方文档，版权所有，仅引用
- **核实**：✅ 已打开核实（WebFetch 加 curl 原文逐句 grep）
- **摘录**：时长 3–15 秒，1080p/720p。Multi-Shot 开启后模型自动规划切镜，"if the described scene is better suited to a single shot, the model will flexibly adjust"；自定义分镜示例写到 Shot 6，页面没写上限。对白示例 "Mom (softly, in a surprised tone): …"；支持中、英、日、韩、西五种语言，中文方言有东北、北京、台湾、粤语、四川等，并标注 Multi-Character Coreference (3+)。主体元素可由 2–4 张参考图或一段视频创建并绑定音色，官方称推拉摇时主体 "stays clear and stable"。模型会识别上传图中的文字（招牌、字幕、logo）并在视频里保持一致。计费：原生音频 1080p 12 积分/秒，720p 9 积分/秒。
- **对本学院有什么用**：参考图和首帧里的文字会被视频继承，关键帧必须先去字；对白统一写成"角色名（语气）：台词"。
- **落点模块**：20-craft、40-memory

### S-VGEN-09 · KLING VIDEO 2.6 Audio User Guide（可灵 2.6 音画同出指南）
- **URL**：https://kling.ai/quickstart/klingai-video-26-audio-user-guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：快手可灵官方文档，版权所有，仅引用
- **核实**：✅ 已打开核实（WebFetch 加 curl 原文 grep，发布于 2025-12-16）
- **摘录**：支持 5/10 秒，一次生成画面、人声、音效和环境声。原文："For singing or dialogue scenes, using the 10s parameter is recommended for more complete and stable results."。对白公式为 "Sentence" + Emotion + Speech Speed + Tone + Character Label；多人示例 [Character A, angrily] says, "…" [Character B, calmly] replies, "…"，换人时用 Immediately 等连接词。正误对照要求角色标签唯一、全程一致，不用代词或同义称呼。音效示例 [Object: Wooden Door] suddenly [Action: Slams] + [Sound Effect: Bang]。音色控制推荐用于双人对话，"performance may degrade in scenes with three or more characters"。语音只支持中英文，其他语言自动译成英语。
- **对本学院有什么用**：对白镜头优先给长时长，同镜说话人控制在 2 人以内〔学院推断，原文针对音色控制功能〕，每句台词按"情绪 + 语速 + 语调"写表演。
- **落点模块**：20-craft、50-rubrics、40-memory

### S-VGEN-10 · Kling Image-to-Video Guide（可灵图生视频指南）
- **URL**：https://kling.ai/quickstart/image-to-video-guide
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：快手可灵官方文档，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：图生视频公式 "Subject + Movement, Background + Movement"。图像已经给定场景，只需写图中主体和它的预期运动。示例："Put on sunglasses" 可能失败，"Mona Lisa puts on sunglasses with her hand" 成功，再加背景光效更好。要点：用简单词句；"Movement should comply with the laws of physics, and it's best to describe movements that are likely to occur in the image"；"A description that significantly deviates from the image may cause a camera cut or transition"；弹跳的球、高空抛物这类复杂物理运动目前难生成。同站 T2V 指南（https://kling.ai/quickstart/text-to-video-prompt-guide）补充：模型对数字不敏感（"10 puppies on the beach" 难保证数量），画面内容尽量简单，力求在 5–10 秒内完成。
- **对本学院有什么用**："首帧主导、文本偏离会切镜"的第二份官方证据，写进关键帧与运动一致性的 rubric。
- **落点模块**：10-theory、50-rubrics

### S-VGEN-11 · BytePlus ModelArk: Dreamina Seedance 2.0 series prompt guide
- **URL**：https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：BytePlus（字节跳动）官方文档，版权所有，仅引用
- **核实**：✅ 已打开核实（页面 JS 渲染，WebFetch 只拿到导航；经 curl 取页面内嵌正文逐句核对，更新于 2026-09-28）
- **摘录**：进阶公式：precise subject + action details + scene/environment + lighting & color tone + camera movement + visual style + image quality + constraints。主体用 "Define [Core_Subject_Features] in <Image/Video_N> as <Subject_N>" 定义，取 2–3 个稳定静态特征，之后同名指代。分镜用 Shot 1/2/3，"precise timing (such as 0–3 seconds) is unstable"。动作："Prioritize slow, gentle, coherent subtle movements, and try to avoid high-burst, large-dynamic actions such as sprinting, big jumps, and violent rolls"；单镜只写一种运镜。附悲伤、喜悦、紧张、愤怒、释然的情绪外化表。对话长镜头用视频扩展，追逐、打斗、蒙太奇分段生成再剪。FAQ：字幕无法 100% 避免，横屏出字幕概率显著低于竖屏；未提示也会出其他平台 logo/水印；三视图易出双胞胎；参考人数超过 4 人稳定性下降；混合参考图里脸太小会导致中途"换脸"，需另备无表情大头照；多音字读错可换同音常用字。
- **对本学院有什么用**：用于参考图准备（大头照加全身照，不用多视角拼图）、动作写法（情绪外化表）和竖屏字幕风险 QC（对照〔委托方实证·B3〕〔委托方实证·D1〕）。
- **落点模块**：10-theory、20-craft、40-memory、50-rubrics、60-casebook

### S-VGEN-12 · BytePlus ModelArk: Dreamina Seedance 2.5 prompt guide
- **URL**：https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：BytePlus（字节跳动）官方文档，版权所有，仅引用
- **核实**：✅ 已打开核实（经 curl 取页面内嵌 Markdown 正文逐句核对，更新于 2026-09-28）
- **摘录**：单条最长 30 秒，单次最多 50 个参考素材（图 ≤30；视频 ≤10，总长 ≤30 秒；音频 ≤10，总长 ≤30 秒）；2.0 只认镜头号，2.5 支持整数秒时间戳。写法：一句话概要，再写时间线或 Shot N，最后写全局一致性备注。"Use positive descriptions whenever possible. Negative constraints are supported for subtitles and audio control"。"If too much content is packed into a given time range, the result may contain excessive cuts or omit parts of the plot"。动作优先概括（"both sides engaging in close combat"），只细写少数记忆点。FAQ：fanatical、extremely shocked 这类强情绪词会让瞳孔发光；在台词后重复台词词语，或给个别词附加语气、表情、动作说明，会触发字幕；参考视频里的字幕会压过无字幕指令；写了 no BGM 仍可能出音乐，要枚举同义词并在开头结尾各写一遍；映射关系要写在文本里，只写在图上容易导致角色混淆或重复。页面提供提示词优化 skill sd25-pe。
- **对本学院有什么用**：给 agent 一份"字幕、BGM、发光眼"的触发源清单和规避写法，并确立"时段内事件过密会碎切或漏情节"的规则。
- **落点模块**：10-theory、20-craft、40-memory、50-rubrics、60-casebook

### S-VGEN-13 · 阿里云百炼：文生视频/图生视频 Prompt 使用指南（万相 3.0/2.7/2.6/2.5）
- **URL**：https://help.aliyun.com/zh/model-studio/text-to-video-prompt
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：阿里云文档，版权所有，仅引用
- **核实**：✅ 已打开核实（WebFetch 加 curl 中文原文 grep）
- **摘录**：基础公式：提示词 = 主体 + 场景 + 运动。进阶公式在其上加主体描述、场景描述、运动描述、美学控制（光源、光线环境、景别、视角、镜头、运镜）和风格化。声音公式：人声 = 角色说话的内容 + 情绪 + 语调 + 语速 + 音色 + 口音；音效 = 音源材质 + 行为 + 环境音；背景音乐 = 背景音乐/配乐 + 风格。多镜头公式：总体描述 + 镜头序号 + 时间戳 + 分镜内容。图生视频公式：运动 + 运镜，镜头不动时写"固定镜头"。参考生视频用"图 n""视频 n"指代。附景别、焦段、光线等中文词典。同站万相 2.7 文生视频 API（https://help.aliyun.com/zh/model-studio/text-to-video-api-reference）：反向提示词不超过 500 字符，prompt 不超过 5000 字符，duration 取 2–15 的整数、默认 5；不传 audio_url 时"根据视频内容自动生成匹配的背景音乐或音效"；2.7 弃用 shot_type，单/多镜头靠 prompt 自然语言控制。
- **对本学院有什么用**：给风格库一套中文镜头、光线、声音词表；"默认自动配乐"作为又一个官方实例写入 memory。
- **落点模块**：20-craft、30-taste、40-memory

### S-VGEN-14 · Wan2.2 开源仓库默认负向提示词（wan/configs/shared_config.py）
- **URL**：https://raw.githubusercontent.com/Wan-Video/Wan2.2/main/wan/configs/shared_config.py
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：Apache-2.0（仓库 LICENSE.txt 已核对）
- **核实**：✅ 已打开核实（全文逐字核对）
- **摘录**：sample_neg_prompt 原文：色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走。同文件：sample_fps=16，frame_num=81，文本编码器 umt5_xxl，text_len=512。也就是说，官方默认负向词把字幕、静止画面、杂乱背景、背景人多、倒着走、多指都列为要压制的对象。
- **对本学院有什么用**：H3 本地管线 cfg=1.0，用不上负向词〔委托方实证·T-2〕；但这份清单可以原样转成 QC 检测项：字幕、静止、杂乱背景、倒走、多指等。
- **落点模块**：50-rubrics、40-memory、10-theory

### S-VGEN-15 · MiniMax H3 官方 Video Prompt Writing Guide（base / ref，Hugging Face）
- **URL**：https://huggingface.co/MiniMaxAI/MiniMax-H3
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：MiniMax H3 Community License（Documentation 属 Materials，许可地域内可复制、修改、分发；排除地域为欧盟、英国、韩国、美国；再分发需附 NOTICE、标注修改）
- **核实**：✅ 已打开核实（模型卡、LICENSE 与 docs/ 下两份指南原文逐句 grep）
- **摘录**：输出 4–15 秒、24 FPS、32 kHz 立体声，稳定支持 11 种对白语言；Ref2VA 最多 9 图、3 段视频、3 段音频，文件总数 ≤12；发布权重为 CFG 蒸馏版。base 模式三字段：integrated_multimodal_description、overall_soundscape、non_diegetic_music。I2VA 首行固定为 "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced."；描述先建立图中风格、主体、构图和场景锚点再写动作，结构为"首帧锚、动作起始、连续发展、结果或反应"。"A cut should introduce new information about the subject, space, state, viewpoint, or time. If only the distance or a slight angle needs to change, prefer camera motion." 运镜 = 类型 + 幅度 + 速度。说话人写 (S1)，台词 <d>[Language] …</d>；画外音写 "says in an off-screen voiceover" 并注明嘴唇闭合；跨切台词用 <scenetrans>，片尾截断用 <cutoff>。画面上真实可见的文字放英文双引号。配乐段不用抽象情绪词。ref 模式六段，生成任务 detailed_description 通常 350–500 英文词。
- **对本学院有什么用**：学院所有 H3 提示词模板和 lint 规则以此为准，其余厂商指南只作交叉验证。H3 专题另见 S-H3-01、S-H3-02。
- **落点模块**：20-craft、40-memory、50-rubrics、70-playbooks、90-curriculum

### S-VGEN-16 · MiniMax-H3 GitHub skills：h3-prompt-writing
- **URL**：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：仓库根目录没有 LICENSE 文件（raw 404）；仓库 README 声明 MiniMax H3 以 MiniMax H3 Community License 发布，并链接到 HF 上的 LICENSE
- **核实**：✅ 已打开核实（目录页、skills/README.md、SKILL.md 原文）
- **摘录**：skills 目录有 1 个提示词 skill（h3-prompt-writing，目前只有英文版）和 8 个风格 skill：极简产品广告、3D 动画短片、纸艺定格讲解、品牌宣传、音乐视频字幕、双人合作游戏开场、纸拼贴讲解、手绘与实拍混合。8 个风格 skill 都附中英双语 SKILL.md / SKILL.cn.md。h3-prompt-writing 的 frontmatter 写明可移植到任何能读本地文件的 agent。工作流：识别模式（T2VA/I2VA/FL2VA/L2VA/Ref2VA），读 references/base-en.txt 或 ref-en.txt，严格保留字段名、顺序、标签和计时写法。输出规则：改写段用英文，台词、歌词和画面文字保留原语言；每镜写构图、主体、环境、动作、运镜、声音和参考生效点。提示：描述总时长匹配 4–15 秒，用具体视听细节替代 "cinematic""beautiful" 这类抽象词。
- **对本学院有什么用**：学院的 H3 提示词 skill 以它为骨架扩展（加入短剧时长预算、台词容量、首帧一致性校验），不另起炉灶。另见 S-H3-01。
- **落点模块**：70-playbooks、20-craft、90-curriculum

### S-VGEN-17 · Luma Learning Center: MiniMax H3 Complete Guide
- **URL**：https://lumalabs.ai/learning-center/articles/minimax-h3-complete-guide
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：Luma AI，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：Luma 学习中心文章，作者 Davicho Barona，2026-07-30，属第三方解读。原文："think through three layers: What happens on screen → what happens in the soundscape → what music accompanies it"，并称官方指南把它们分成视觉/动作时间线、总体声景、非叙事配乐。写可观察的物理变化："'She tightens her grip on the letter and looks away' gives the model something more visible to generate than 'she becomes emotional.'"。"Introduce a cut when the next shot reveals genuinely new information."；台词要 "concise enough to fit comfortably within the clip"。"Every instruction competes for time inside a short clip"：四个运镜、三个动作、两句台词、一次变形加几次切镜，都得压进同一段时长。I2V：开场图、第一动作、持续动作、最终反应。参考素材各给一个职责："Use Image 1 for the character's appearance. Use Video 1 only for movement."，先用最少的参考。
- **对本学院有什么用**：作为"时长预算、指令竞争"的通俗说明，让 agent 写提示前先删到最重要的节拍。
- **落点模块**：10-theory、20-craft、30-taste

### S-VGEN-18 · Luma Learning Center: Character Consistency Techniques
- **URL**：https://lumalabs.ai/learning-center/articles/character-consistency-techniques
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：Luma AI，版权所有，仅引用
- **核实**：✅ 已打开核实（含同站《Don't Make These Mistakes》）
- **摘录**：2026-03-09。漂移的根源："Luma doesn't know what must stay the same"；只给一张正面肖像却要侧面或全身，模型 "has to invent what it cannot see"。做法：建立主参考素材包（正、背、顶、左右 3/4、左右侧、全身、T-pose），干净或白底，每张一个角度；"Do not combine multiple angles into one sheet, this has the potential to cause hallucinations and artifacts that then leak over into new generations"。把图转成文字蓝图（形状比例、颜色、材质、关键特征），列出锁定特征；变体只改机位和姿势；"The latest variant is not your source of truth, your Master Reference Assets are"。同站《Don't Make These Mistakes》（https://lumalabs.ai/learning-center/articles/dont-make-these-mistakes）：每个 moment 先做一张关键帧；不要一次生成 60–90 秒；重抽 20 次是 "gambling, not iteration"，先把问题归到 motion、camera、style drift、character drift、pacing。
- **对本学院有什么用**：复查委托方 1696×2528 板图〔委托方实证·T-1〕是不是多视角拼图；若是，改为单角度单图加锁定特征文本，用来预防克隆脸和漂移（对照〔委托方实证·B3〕）。
- **落点模块**：20-craft、40-memory、70-playbooks

### S-VGEN-19 · LTX Blog: How To Fix Slow Motion In AI-Generated Videos
- **URL**：https://ltx.io/blog/how-to-fix-slow-motion-in-ai-generated-video
- **类型**：article
- **分类**：🟡 需适配
- **许可**：Lightricks/LTX 博客，版权所有，仅引用
- **核实**：✅ 已打开核实（WebFetch 报 Header overflow，改用 curl 取原文逐句 grep）
- **摘录**：LTX Team，2026-04-26。扩散模型偏好慢而平滑的运动，因为帧间变化小更容易保持时序一致，快动作会增加伪影，"So the model defaults to the safest option: make everything slow."；提示对速度含糊时，"It will almost always choose slower, because slower is safer"。修法：用自带速度的动词（walks 换成 strides、hurries、rushes；moves 换成 darts、sweeps、charges），加 "quickly""at full speed""in rapid succession"；同时写环境运动（树影掠过、湿路面反光拉丝、人群让开），否则可能出现慢速奔跑者配静止背景；写明运镜类型、方向和速度。开源用户可把 cfg_scale 降到 2.0–2.5、stg_scale 降到 0.5–0.8；托管 API 用户只能靠提示词。
- **对本学院有什么用**：本地 H3 管线 cfg 已是 1.0〔委托方实证·T-2〕，没有引导参数可调，快节奏和打斗镜头必须写"速度动词 + 环境运动 + 运镜速度"（对照〔委托方实证·A3〕）。
- **落点模块**：10-theory、20-craft、50-rubrics

### S-VGEN-20 · Gemini API: Generate videos with Veo
- **URL**：https://ai.google.dev/gemini-api/docs/veo
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：Google 开发者文档（页脚许可本次未核对），仅引用
- **核实**：✅ 已打开核实（核实员补录：研究员只在关键事实中引用此页）
- **摘录**：Veo 3.1 有 veo-3.1-generate-preview、veo-3.1-fast-generate-preview、veo-3.1-lite-generate-preview 三个变体。durationSeconds 可选 "4""6""8"，原文："Must be '8' when using extension, reference images or with 1080p and 4k resolutions"。参考图最多 3 张。扩展每次加 7 秒，最多 20 次，与原片合计约 148 秒；扩展只支持 720p。画幅 16:9（默认）或 9:16；分辨率 720p 默认，1080p 和 4k 只能配 8 秒，Lite 不支持 4k。页面的音频写法建议是对白放引号里（示例 "This must be the key," he murmured），音效和环境声分别显式描述。生成的视频在服务器上保留 2 天后删除，全部带 SynthID 水印。
- **对本学院有什么用**：说明时长、参考图数量这类约束是厂商锁死的参数，提示词改不了；agent 设计镜头前先查参数边界。
- **落点模块**：10-theory、40-memory

### S-VGEN-21 · BytePlus ModelArk: Seedance 1.5 Pro prompt guide
- **URL**：https://docs.byteplus.com/en/docs/ModelArk/2168087
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：BytePlus（字节跳动）官方文档，版权所有，仅引用
- **核实**：✅ 已打开核实（该地址跳转到 https://docs.byteplus.com/en/docs/modelark/seedance-1-5-pro ；核实员补录：研究员只在关键事实中引用此页）
- **摘录**：公式为 Subject + Movement + Environment (optional) + Camera movement (optional) + Aesthetic description (optional) + Sound (optional)。可用 resolution、ratio、duration、seed、camera_fixed、watermark 等参数控制输出。台词的情绪和语速写在句前，如 "In a calm emotional state, with an even tone and a normal speaking pace, say: …"。原文："By default, Seedance 1.5 Pro automatically generates background music that matches the prompt."。示例支持对白正反打（"The shot cuts to a close-up of the suspect…"）。运镜描述公式：起幅构图 + 运镜 + 运镜幅度 + 落幅构图。
- **对本学院有什么用**："模型默认自行配乐"的又一官方实例；"起幅 + 运镜 + 幅度 + 落幅"的写法可作为 H3 运镜句的交叉参照。
- **落点模块**：20-craft、40-memory

### S-VGEN-22 · Vidu 开放平台 API：图生视频
- **URL**：https://docs.platform.vidu.cn/331819348e0
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：Vidu 开放平台文档，版权所有，仅引用
- **核实**：✅ 已打开核实（核实员补录：研究员只在关键事实中引用此页）
- **摘录**：页面标题"图生视频"。viduq2-pro-fast、viduq2-pro、viduq2-turbo 时长 1–10 秒，默认 5；viduq1、viduq1-classic 只能 5 秒；vidu2.0 为 4 或 8 秒。prompt "字符长度不能超过 1500 个字符"。movement_amplitude（运动幅度）"默认 auto，可选值：auto、small、medium、large"，页面没写哪些模型支持。audio 设为 true 时"输出带台词以及背景音的视频"，默认 false 输出静音。参数表里没有负向提示词字段。
- **对本学院有什么用**：Vidu 把运动幅度做成显式参数；H3 没有这个参数，只能在文本里用 "with small/large amplitude" 控制，agent 不能假设幅度可调。
- **落点模块**：10-theory、20-craft

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-VGEN-01 | Runway Gen-4 只解读"应该发生什么"，"Negative phrasing is not supported and may produce unpredictable or even opposite results"，应写 "Locked camera. The camera remains still." 而不是 "No camera movement."；Gen-4.5 入门指南补充：说了不要什么，模型仍要理解这个概念，"may include it anyway"。 | [Runway Gen-4 指南](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)、[Runway 入门](https://help.runwayml.com/hc/en-us/articles/47313698911891-Introduction-to-Prompting) | 高 |
| F-VGEN-02 | Vertex AI Veo 指南不推荐在提示中用 "no""don't" 这类指令式否定（如 "no walls"），推荐把不想要的内容写成名词（"wall, frame"）放进负向提示。 | [Vertex AI 提示指南](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide) | 高 |
| F-VGEN-03 | Seedance 2.5 原文："Negative constraints are supported for subtitles and audio control, such as 'no subtitles' and 'no BGM.'"。写了 no BGM 仍可能把音效渲染成配乐，官方对策是枚举 music、background music、BGM、score、instrumental、melody、synth effects、ambient pad 等同义词，并在提示开头和结尾各写一遍；官方示例提示还写到 drone、swelling tone、crescendo、stinger；或后期去掉非人声音轨。 | [Seedance 2.5 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide) | 高 |
| F-VGEN-04 | Seedance 2.0 FAQ："it is not possible to directly avoid generating subtitles 100%"；参考图或参考视频中非必要的文字应先去掉；"the probability of generating subtitles in landscape is significantly lower than in portrait"。对 9:16 短剧，这意味着字幕风险更高，生成后必须做 OCR 检测〔学院推断〕。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide) | 高 |
| F-VGEN-05 | Seedance 2.5 FAQ：在台词后重复台词词语，或给台词中个别词附加语气、表情、动作说明，会触发字幕；不同台词要不同表演时，写成 "Character's line (emotion): content"；参考视频里的字幕可能压过无字幕指令。 | [Seedance 2.5 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide) | 高 |
| F-VGEN-06 | Seedance 2.0 FAQ：提示没提水印，生成视频里仍可能出现其他视频平台的 logo 或水印。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide) | 高 |
| F-VGEN-07 | Veo 3 公开事件：含对白片段频繁出现乱码烧录字幕。"up to 40%" 不可用是一位广告从业者的说法；学者把原因归于训练数据自带字幕，并指出负向提示通常弱于正向提示；Google 称已开发修复，一个多月后用户仍在报告。 | [MIT Technology Review](https://www.technologyreview.com/2025/07/15/1120156/googles-generative-video-model-veo-3-has-a-subtitles-problem) | 中（40% 为单一用户说法） |
| F-VGEN-08 | Wan2.2 官方默认负向提示词包含"字幕""静态""静止不动的画面""杂乱的背景""背景人很多""倒着走""多余的手指""手指融合"等。 | [Wan2.2 shared_config.py](https://raw.githubusercontent.com/Wan-Video/Wan2.2/main/wan/configs/shared_config.py) | 高 |
| F-VGEN-09 | 默认自行配乐是多家行为："By default, Seedance 1.5 Pro automatically generates background music that matches the prompt."；万相 2.7 API 不传 audio_url 时"根据视频内容自动生成匹配的背景音乐或音效"。 | [Seedance 1.5 Pro 指南](https://docs.byteplus.com/en/docs/ModelArk/2168087)、[万相 2.7 API](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference) | 高 |
| F-VGEN-10 | 可灵 3.0 会识别上传图中的文字（招牌、字幕、logo）并在视频中保持一致，即输入图里有字，视频里就会有字。 | [可灵 3.0 指南](https://kling.ai/quickstart/klingai-video-3-model-user-guide) | 高 |
| F-VGEN-11 | Runway I2V："your image defines composition, subject matter, lighting, and style"，提示词写运动；输入图中的运动模糊、动作中姿态、方向线等隐含运动线索与提示矛盾时 "may require more iteration"，官方示例去掉线索后同一提示成功。 | [Runway I2V 指南](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide) | 高 |
| F-VGEN-12 | 可灵 I2V："A description that significantly deviates from the image may cause a camera cut or transition"；运动应符合物理，最好写图中"likely to occur"的动作。 | [可灵 I2V 指南](https://kling.ai/quickstart/image-to-video-guide) | 高 |
| F-VGEN-13 | 不想要的切镜：Runway 称通常说明时长不够，先加长时长，仍切就加 "Continuous, seamless shot"；Seedance 2.5 称时段内塞太多内容会 "contain excessive cuts or omit parts of the plot"。 | [Runway I2V 指南](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide)、[Seedance 2.5 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide) | 高 |
| F-VGEN-14 | H3 官方："A cut should introduce new information about the subject, space, state, viewpoint, or time. If only the distance or a slight angle needs to change, prefer camera motion." | [H3 模型卡与指南](https://huggingface.co/MiniMaxAI/MiniMax-H3) | 高 |
| F-VGEN-15 | H3 官方规格：输出 4–15 秒、24 FPS、32 kHz 立体声，稳定支持 11 种对白语言；发布权重为 CFG 蒸馏版；Ref2VA 的 detailed_description 通常 350–500 英文词。官方下限 4 秒与〔委托方实证·T-2〕"低于 124 帧（约 5.2 秒）动作异常"不一致，学院以委托方实测为准。 | [H3 模型卡与指南](https://huggingface.co/MiniMaxAI/MiniMax-H3) | 高 |
| F-VGEN-16 | 是否复述首帧，两家相反：H3 官方要求 I2VA 描述先建立图中风格、主体、构图与场景锚点再写动作；Runway 称在提示中高细节复述图中已有元素 "can lead to reduced motion or unexpected results"。写 H3 时按 H3 官方。 | [H3 模型卡与指南](https://huggingface.co/MiniMaxAI/MiniMax-H3)、[Runway Gen-4 指南](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide) | 高（两条原文均已核对；H3 上孰优未测） |
| F-VGEN-17 | Sora 2："Each shot should have one clear camera move and one clear subject action"；多镜头时每个镜头块只放一个机位、一个动作、一套光照。 | [Sora 2 指南](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | 高 |
| F-VGEN-18 | Seedance 2.0："Try to specify only 1 type of camera movement in a single shot"，同时要求推、拉、摇、移会增加画面不稳定。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide) | 高 |
| F-VGEN-19 | Sora 2 台词容量："a 4-second shot will usually accommodate one or two short exchanges"，8 秒可多几句；长而复杂的台词难对口型，会打乱节奏。没有给出字/秒数字。 | [Sora 2 指南](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | 高 |
| F-VGEN-20 | 可灵 2.6：唱歌或对白场景建议用 10 秒；音色控制推荐双人对话，"performance may degrade in scenes with three or more characters"。 | [可灵 2.6 指南](https://kling.ai/quickstart/klingai-video-26-audio-user-guide) | 高 |
| F-VGEN-21 | Seedance 2.0 建议优先慢、轻、连贯的小动作，避免冲刺、大跳、剧烈翻滚；单场景对话用视频扩展做一镜到底，追逐、打斗、蒙太奇分段生成再剪辑。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide) | 高 |
| F-VGEN-22 | LTX 官方的解释：扩散模型偏好慢动作，因为帧间变化小更易保持时序一致；提示对速度含糊时几乎总选更慢。对策是速度动词、环境运动和显式运镜速度；开源可把 cfg_scale 降到 2.0–2.5、stg_scale 降到 0.5–0.8，托管 API 只能靠提示词。 | [LTX 博客](https://ltx.io/blog/how-to-fix-slow-motion-in-ai-generated-video) | 中（厂商解释，未附测量数据） |
| F-VGEN-23 | Seedance 2.0 要求用具体身体细节表达情绪，给出悲伤、喜悦、紧张、愤怒、释然的对照表（如悲伤：低头、肩膀轻颤、眼眶发红、无意识攥衣角、泪在眼眶不落）；Seedance 2.5 补充：fanatical、extremely shocked 等强情绪词会让瞳孔发光，应换成 amazed 等中性词并约束 "normal human eyes; no glowing eyes"。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide)、[Seedance 2.5 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide) | 高 |
| F-VGEN-24 | 角色参考，两家说法不同：Seedance 2.0 称多视角、三视图资产易被识别为多个主体，加剧 ID 漂移和双胞胎，推荐无表情大头照加全身照，参考人数超过 4 人稳定性下降；Luma 推荐正、背、侧、3/4 等多张单角度图，但 "Do not combine multiple angles into one sheet"。两家一致的只有"不要把多角度拼在一张图上"。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide)、[Luma 角色一致性](https://lumalabs.ai/learning-center/articles/character-consistency-techniques) | 高（原文均已核对；H3 上孰优未测） |
| F-VGEN-25 | Runway FAQ：JSON 提示只有安慰剂效果，"JSON formatting is ignored by generative models– what matters is the detail provided within the prompt"。这与 H3 的字段格式不矛盾：结构只在模型训练过该格式时才起作用〔学院推断〕。 | [Runway 入门](https://help.runwayml.com/hc/en-us/articles/47313698911891-Introduction-to-Prompting) | 高 |
| F-VGEN-26 | Veo 3.1（Gemini API）：时长 4/6/8 秒，用扩展、参考图或 1080p/4k 时必须 8 秒；参考图最多 3 张；扩展每次加 7 秒、最多 20 次、合计约 148 秒，扩展只支持 720p。 | [Gemini API Veo](https://ai.google.dev/gemini-api/docs/veo) | 高 |
| F-VGEN-27 | Vidu 把运动幅度做成显式参数 movement_amplitude（auto/small/medium/large）；viduq2 系列时长 1–10 秒，prompt ≤1500 字符；该页参数表没有负向提示词字段。 | [Vidu 图生视频 API](https://docs.platform.vidu.cn/331819348e0) | 中（只核对了图生视频一页） |
| F-VGEN-28 | Sora 2：一次生成最多引用 2 个已上传角色；扩展用整段原片作上下文，单次最多 20 秒，最多 6 次，合计 120 秒。 | [Sora 2 指南](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | 高 |
| F-VGEN-29 | 可灵：当前视频模型对数字不敏感，"10 puppies on the beach" 这类数量难以保证；画面内容尽量简单，力求在 5–10 秒内完成。 | [可灵 T2V 指南](https://kling.ai/quickstart/text-to-video-prompt-guide) | 高 |
| F-VGEN-30 | 精确时间控制普遍不可靠：Seedance 2.0 称 "precise timing (such as 0–3 seconds) is unstable"，只认镜头号；Seedance 2.5 才支持整数秒时间戳；Runway 称时间戳提示 "may not be perfectly precise"，只能引导大致顺序。 | [Seedance 2.0 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide)、[Seedance 2.5 指南](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide)、[Runway T2V 指南](https://help.runwayml.com/hc/en-us/articles/47313737321107-Text-to-Video-Prompting-Guide) | 高 |

## 空白与未找到

1. **火山引擎中文版 Seedance 指南**：https://www.volcengine.com/docs/82379/1956278 是 JS 渲染且跳转异常，未读，改用同源的 BytePlus 英文版（2026-09-28 更新）。Seedance 2.5 页面给出了提示词优化 skill sd25-pe 的 npx 安装命令，本次没有安装，内容未读。
2. **Luma Ray3.2**：官方提示词文章返回 404。"positive only、约 100 词、进行时动词"等说法只见于搜索摘要，未核实，不收录。
3. **Vidu**：没找到官方提示词指南，只有 API 参数页。Q3 的 16 秒、多人对话等信息只来自第三方，不收录。
4. **台词容量硬数字**：没有任何一家官方给出字/秒或词/秒。Veo"8 秒约 20–30 词"是社区经验，不收录。委托方实测 7.5 字/秒〔委托方实证·T-2〕〔委托方实证·D3〕仍是唯一的定量依据。
5. **擅自加服饰**：官方文档里没有"自行加首饰、盔甲、装饰"的条目。只找到字幕、水印/logo、BGM、发光眼、继承参考图文字这几类自动添加。服饰被加料的问题只能靠委托方案例〔委托方实证·C1〕和其他研究补证。
6. **空间连续**：没有官方指南讨论 180° 轴线、视线匹配或跨镜空间连续规则。可灵 3.0 称主体在运镜中保持稳定，属于厂商自述，没有受控数据。
7. **未读页面**：Kling 3.0 Omni、Kling Camera Control、Vertex AI 的 Video best practices、Runway Aleph 与角色对白相关文档。研究员称 Gemini API 视频总览页把 "Gemini Omni Flash" 列为默认视频模型；本次打开的 /veo 页没有这个说法，总览页没有打开，不收录。
8. **研究员遗留项已解决**：Sora 2"最多 2 个角色、扩展 6 次共 120 秒"已在 openai-cookbook 仓库 notebook 原文核实，见 F-VGEN-28。
9. **厂商冲突待 A/B**：两处建议相反，见 F-VGEN-16（是否复述首帧）和 F-VGEN-24（多张单角度参考还是只给大头照加全身照）。H3 上哪种更好没有数据，需要在委托方管线上同 seed 对比。还有一处冲突相关：H3 专题称 "no subtitles…" 这类否定会把文字登记为内容（见 F-H3-08），Seedance 2.5 却称支持字幕否定，委托方 D1 也用了否定句重出替换〔委托方实证·D1〕。H3 上这句的实际效果需要 A/B。
10. **规格口径差异**：H3 模型卡写 4–15 秒；124–362 帧的训练区间来自 ComfyUI 节点源码注释（见 S-H3-03），与委托方实测一致。两者口径不同，引用时要注明出处。
11. **核实说明**：22 条全部打开核对。Runway 帮助中心网页对抓取返回 403，正文经同站 Zendesk 公开 API 取得。BytePlus 页面为 JS 渲染，正文经 curl 取页面内嵌数据。可灵、阿里云、LTX、H3 指南另用 curl 原文逐句 grep。S-VGEN-20、21、22 是核实员根据研究员关键事实里的 URL 补录的条目。
