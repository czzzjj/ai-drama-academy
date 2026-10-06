# MiniMax H3 / Hailuo 提示词与运镜资料

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：17 ｜ 核实方式：逐条 WebFetch 打开核对

## 一句话结论

本专题给学院提供四类材料。一是 H3 官方提示词格式：三字段、首行对齐句、12 类运镜原语加振幅和速度、Ref2VA 六段式。二是本地 ComfyUI 的硬参数：17k+5 帧网格、训练区间约 124–362 帧、首帧直接拉伸、无负向分支、步数与 Turbo LoRA 的取舍。三是几份社区 MIT skill 的小样本实测，涉及运镜、节拍密度、对白与 seed、片尾崩解。四是 H3 许可证的地域与署名条款。仍然缺的有：官方 9:16 竖屏构图和运镜指南；官方中文语速和对白容量数据；"I2V 首帧 + 文字运镜"在 9:16 下的受控实验；Hailuo 02/2.3 时代的官方中文提示词指南原文。社区数据大多是单一项目、n=1–2，只能当待复测的假设。

## 条目

### S-H3-01 · MiniMax-AI/MiniMax-H3 官方仓库 skills 目录与 h3-prompt-writing（base-en.txt / ref-en.txt）
- **URL**：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MiniMax H3 Community License Agreement（仓库级；排除地域为欧盟、英国、韩国、美国）
- **核实**：✅ 已打开核实
- **摘录**：目录共 9 个 skill：1 个提示词 skill（h3-prompt-writing，目前只有英文版）和 8 个风格 skill。h3-prompt-writing 的 frontmatter 写明可移植到任何能读本地文件的 agent。抽查 minimalist-product-ad-generator，其 frontmatter 写明 "Requires the MiniMax Hub agent… not portable"；其余 7 个风格 skill 未逐一核对。base-en.txt 内容：三字段 integrated_multimodal_description / overall_soundscape / non_diegetic_music；I2VA/FL2VA/L2VA 的首行必须是 "How the reference pictures align with the target video — …" 对齐句（S.SS 取两位小数，后空一行），T2VA 不写对齐句；§4.3 定义 12 类运镜（Zoom、Push/Pull、Pan、Truck、Tilt、Pedestal、Arc Shot、Tracking、Static、Shake Slightly/Strongly、POV、Roll）加 with small/large amplitude、at slow/fast speed，要求写成句内自然英文动作，不在句尾堆标签；说话人用 (S1)/(S2)，`<d>[Language] 原文</d>`；画外音用固定短语 "says in an off-screen voiceover"，并注明嘴唇闭合；跨剪点台词用 `<scenetrans>`，被片尾截断用 `<cutoff>`；画面文字放进英文双引号。ref-en.txt 内容：六段顺序、四类标签（Subject/Picture/Video/Audio）、retention 标记，生成任务的 detailed_description 通常 350–500 英文词。
- **对本学院有什么用**：agent 写 H3 提示词时先加载这份官方格式，字段名、顺序、对齐句、运镜语法逐字照抄；社区经验只能叠加在上面，冲突时以上游为准。
- **落点模块**：20-craft、40-memory、50-rubrics、70-playbooks

### S-H3-02 · HuggingFace 模型卡 MiniMaxAI/MiniMax-H3
- **URL**：https://huggingface.co/MiniMaxAI/MiniMax-H3
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：MiniMax H3 Community License Agreement
- **核实**：✅ 已打开核实
- **摘录**：输出参数：4–15 秒，24 FPS，短边默认 768，32 kHz 立体声，画幅 21:9 至 9:16。两套检查点：FL2VA 接受 0–2 张图（文生、首帧、尾帧、首尾帧）；Ref2VA 接受 ≤9 张图、≤3 段视频（每段 2–15 秒，合计 ≤15 秒）、≤3 段音频，文件总数 ≤12。权重为 CFG 蒸馏的 BF16。完整系统是 H3-Context-IR → H3-Base（768p）→ H3-Regenerate-2K，其中 Context-IR 和 Regenerate-2K 未开源。README 原文："H3-Context-IR is critical to the quality of the final output, so we strongly recommend incorporating it into your generation pipeline or following the 'Prompting Guidance' to build your own context-processing system." 稳定支持中文、英文等 11 种语言。提示词指南文件为 VIDEO_PROMPT_WRITING_GUIDE_base_en.md / ref_en.md。
- **对本学院有什么用**：本地开源的 H3-Base 没有官方提示词重写器，agent 要自己承担 Context-IR 那一步的结构化扩写，不能只喂一句短提示。
- **落点模块**：10-theory、20-craft、40-memory

### S-H3-03 · ComfyUI 原生 H3 节点源码 comfy_extras/nodes_minimax_h3.py
- **URL**：https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_minimax_h3.py
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：GPL-3.0（ComfyUI）
- **核实**：✅ 已打开核实
- **摘录**：源码常量 `FPS = 24`、`MAX_PIXELS = 768 * 1344`、`REF_IMAGE_SHORT_EDGE = 2048`。length 的 tooltip 原文："Frame count at 24 fps, snapped up to the model's 17k+5 grid (124 = ~5s; trained range is ~124-362, longer is untested)"。MiniMaxH3ImageToVideo 里 first_frame 的注释是 "geometry anchor: plain stretch to canvas"（crop 为 disabled，不保比例），last_frame 的注释是 "follower: aspect-preserving cover-crop"（居中裁切）。ReferenceToVideo 的 ref_image_size 有两档：match 只缩小、保比例，对齐生成画面面积；max 用 2048 短边，"for best identity fidelity"，代价是可能慢数倍。参考槽位上限为图 9、视频 3、视频音轨 3、独立音频 3。MiniMaxH3AddGuide 可以在任意帧锚定图像或音频，多帧批次会裁到 5、22、39… 帧。
- **对本学院有什么用**：喂首帧前，先把关键帧等比裁成与画布同比例（如 768×1344），否则会被直接拉伸；时长只在 17k+5 网格的 124–362 帧之间选。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-H3-04 · ComfyUI 官方 H3 教程（总览 / 原生工作流 / 提示词指南）
- **URL**：https://docs.comfy.org/tutorials/video/minimax/minimax-h3 （提示词页：https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide ）
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：文档（引用即可）
- **核实**：✅ 已打开核实
- **摘录**：总览页：默认关闭 Lightning LoRA，跑 20 步，res_multistep + simple，shift 12 / audio_shift 3。打开 LoRA 后 T2V/I2V 降到 8 步，参考类模板降到 4 步；原生页注明代价是 "slightly lower audio and motion quality"。4 步时参考可能几乎不生效，姿态或脸的角度会随片子漂离参考；简单内容 12–16 步即可，锁子甲、花纹等高频细节到约 50 步仍在改善，步数不够时会出现随运动游动的三角网格伪影；音频比画面收敛晚，8 步时语音和音色最弱，12 步以上可用。Resolution Selector 用 0.98 MP；1.0 MP 得到 1376×768，超出面积上限。Sage Attention 的 INT8 量化可能导致片尾形变和乱码文字。原文写明本地输出商用需要 MiniMax 商业授权，Comfy 是唯一官方经销商。提示词页：BasicGuider 没有负向分支，负向提示无效；"no subtitles and no on-screen text" 这类写法反而会把文字登记为内容，应改写为 "the sign above the door is blank" 这样的正向状态；默认 124 帧，按 17k+5 吸附。
- **对本学院有什么用**：agent 把"不要什么"一律改写成"画面里是什么"；步数、LoRA、注意力后端作为质量门禁参数，记进每次生成的日志。
- **落点模块**：20-craft、50-rubrics、70-playbooks、40-memory

### S-H3-05 · MiniMax 开放平台 H3 视频生成 API（v2 create / H3-Context-IR / 视频生成指南 / Feature Highlights）
- **URL**：https://platform.minimax.io/docs/api-reference/video-generation-v2-create
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：API 文档（按 MiniMax 服务条款）
- **核实**：✅ 已打开核实
- **摘录**：v2 create 页：MiniMax-H3 支持 768P/2K、4–15 秒；MiniMax-H3-Max 是 "the fast generation variant"，480P/768P、5–15 秒，不支持 2K。content[] 的 type 为 text/image_url/video_url/audio_url，role 为 first_frame/last_frame/reference_image/reference_video/reference_audio，首尾帧模式与参考模式互斥。ratio 可选 adaptive/21:9/16:9/4:3/1:1/3:4/9:16。extra.prompt_expansion_mode（disabled/balanced/quality，默认 balanced）只对 H3-Max 生效。每段文本 ≤7000 字符，请求体 ≤64 MB。"由 fal.ai 基于 H3 后训练"这句话出自视频生成指南页（https://platform.minimax.io/docs/guides/video-generation.md），不在 create 页。Context-IR 接口页（https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir.md）写明 "only returns an enhanced video prompt"，不创建视频任务。Feature Highlights 页（https://platform.minimax.io/docs/guides/video-prompt.md）"AI Narrative Content"一节给了 15 秒 9:16 吸血鬼题材竖屏短剧预告示例，原文含 "ReelShort / DramaBox feel… Medium-close and close shots for eye contact and tension"。
- **对本学院有什么用**：预算允许时，agent 可以调 Context-IR 接口拿到官方风格的结构化提示词，当作对照样本，校准自己写的本地提示词。
- **落点模块**：20-craft、60-casebook、70-playbooks

### S-H3-06 · MiniMax 旧版文生视频 API 的方括号运镜指令（Hailuo-02 / Hailuo-2.3 / *-Director）
- **URL**：https://platform.minimaxi.com/docs/api-reference/video-generation-t2v （302 跳转至 https://platform.minimax.cn/docs/api-reference/video-generation-t2v ；英文版 https://platform.minimax.io/docs/api-reference/video-generation-t2v ）
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：API 文档
- **核实**：✅ 已打开核实
- **摘录**：中文版原文："对于 MiniMax-Hailuo-2.3、MiniMax-Hailuo-02 和 *-Director 系列模型，支持使用 [指令] 语法进行运镜控制。"共 15 种指令：[左移][右移][左摇][右摇][推进][拉远][上升][下降][上摇][下摇][变焦推近][变焦拉远][晃动][跟随][固定]。英文版对应 [Truck left/right] [Pan left/right] [Push in] [Pull out] [Pedestal up/down] [Tilt up/down] [Zoom in/out] [Shake] [Tracking shot] [Static shot]。规则：同一 [] 内的多个指令同时生效，建议不超过 3 个；前后出现的指令依次生效；也可以用自然语言，但标准指令响应更准。model 枚举为 MiniMax-Hailuo-2.3、MiniMax-Hailuo-02、T2V-01-Director、T2V-01；prompt 最长 2000 字符；prompt_optimizer 默认 true；Hailuo 768P 可选 6/10 秒，1080P 只有 6 秒；aigc_watermark 默认 false。
- **对本学院有什么用**：方括号语法属于旧的托管模型；写 H3 时改用官方自然语言的"类型+振幅+速度"句式，不在 H3 提示词里堆方括号标签。
- **落点模块**：10-theory、40-memory、90-curriculum

### S-H3-07 · MiniMax 官方《Run and self-host MiniMax H3》
- **URL**：https://platform.minimax.io/docs/guides/local-deploy-h3.md
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：文档
- **核实**：✅ 已打开核实
- **摘录**：文档基线复核日期为 2026-08-26。美国、欧盟、英国、韩国为排除地域。开源只含 H3-Base FL2VA 与 Ref2VA，不含 Context-IR 和 Regenerate-2K，原文："a self-hosted H3-Base service therefore does not reproduce the complete MiniMax Platform Context-IR and 2K workflow"。ComfyUI 用 Comfy-Org 的剪枝或量化转换权重，SGLang 用官方 BF16/FP32 混合权重，"do not mix benchmark claims between the two paths"。FL2VA 示例默认 20 步，可选的 8 步 Turbo LoRA "can reduce motion and audio quality"；R2V 另有 4 步 Turbo LoRA；比较结果时要记录 LoRA 名、强度、步数、seed 和全部参考。SGLang 基准为 50 步、1344×768、124 帧。miles-diffusion 的 H3 FL2VA LoRA 配方标注为 Experimental，默认 rank 64 / alpha 128、lr 3e-5、flow-shift 12；训练数据要求短边 768、24 fps、17n+5 且至少 107 帧。
- **对本学院有什么用**：每次生成都把完整复现参数落盘：检查点修订、LoRA、步数、seed、参考列表。角色 LoRA 微调可以列为解决脸漂的实验性升级路径。
- **落点模块**：20-craft、40-memory、70-playbooks

### S-H3-08 · loopforge0/minimaxh3-shots-skills（h3-camera-shots + h3-shot-iteration）
- **URL**：https://github.com/loopforge0/minimaxh3-shots-skills
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT（upstream/ 目录沿用 MiniMax 条款，不在 MIT 范围内）
- **核实**：✅ 已打开核实
- **摘录**：仓库公开 17 条实际运行过的提示词。统一设置为 1344×768（16:9）、20 步、res_multistep/simple、turbo 关闭、Ref2VA；作者注明多条结论是 n=1 或 n=2，开发时用的是 int8 剪枝 UNet，量化影响未控制。主要结论：4 步 turbo 几乎压掉运镜；最少 124 帧，三段式动作要 192 帧；加背景参考板后背景变换从 0.47x 变为 0.81x（运镜约减半），场景漂移从 0.08 降到 0.02，人物板不影响运镜；称参考图为 first frame 或用 [keyframe completion] 会钉死起幅、约减半运动；small amplitude 基本无效（1.47x 对 1.53x），large 与 fast 不叠加；写明落点后 whip pan 从 23 提到 218 px/step，直接要求 motion blur 无效；起幅放在主体最大的一端；镜头和机身名几乎无效，写入会入镜的器材会被画出来；无法指定事件时刻（3.0s/4.0s 都落在 2.46s）；"holds one single pose completely rigid" 让运镜从 98–108% 降到 22%。附 14 个命名镜头、build_prompt.py、verify_refs.mjs。原则："never let one [metric] outrank your eyes"。
- **对本学院有什么用**：agent 按"原语→起幅→落点"组装运镜，默认不加修饰词；出问题时先查设置（步数、帧数、参考是否真的接上），再改提示词。
- **落点模块**：20-craft、30-taste、50-rubrics、60-casebook、70-playbooks

### S-H3-09 · phileiny/h3-storyboard-skill（h3-storyboard，竖屏连载短剧分镜与表演）
- **URL**：https://github.com/phileiny/h3-storyboard-skill
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：来自一部 9:16、Ref2VA、本地 ComfyUI 的连载短剧，每集约 60 秒、1,100–1,400 帧；正文为繁体中文，SOURCES.md 标出了哪些已验证、哪些部分验证、哪些是推断。第一定律：一镜超过 2–3 个表情节拍会被平均抹平（一颗 7 秒特写写 9 拍，PSNR 37–42 dB，脸没动；拆成三颗 2–3 秒，降到 22–23 dB，表情到位）。武打测试：107 帧、约 3 秒写 8–9 招，4 份提示词 × 2 seed 全部按顺序真速度打出（标为 partly）。`<d>` 会挤占相邻镜头的帧数；本项目配音员语速 4.30 字/秒；片尾前 1.2–1.7 秒常崩解，要留 1.3–1.5 秒余量；运镜作用于整次生成，要切镜就整颗静止；正反打前加 1.5 秒双人引子；空间靠平面图→Blender 灰模→写实板锁定；多人场同框只交代关系，台词全用单人正反打；提到什么就长什么；一人两张脸可能生成两个人；禁用字对照表；用 Whisper 逐字时间验对白，片尾静音处会幻听 "Thank you."；最后一哩靠剪辑。
- **对本学院有什么用**：agent 拆镜前先数节拍，用场景图而非文字定空间；"剪辑能解决的不再重生成"写进决策流程。依赖 Gemini、Blender、mlx_whisper 的步骤需要按学院工具链改写。
- **落点模块**：10-theory、20-craft、30-taste、50-rubrics、60-casebook、70-playbooks

### S-H3-10 · jtydhr88/ComfyTV 中的 skill h3-cinematic-director
- **URL**：https://github.com/jtydhr88/ComfyTV/tree/main/skills/h3-cinematic-director
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实（目录页只列文件，SKILL.md 与 references 内容按仓库克隆核对）
- **摘录**：四个作业：shot-design、h3-prompt、continuity-audit、single-variable-repair。核心链为 "dramatic purpose → spatial blocking → performance → camera → edit → sound → H3 control"。每镜先锁定信息、权力、情绪、关系、危险、空间中哪一项发生变化，"If the shot changes none of these, remove it"。连续性账本记录身份、服装、手持物、180° 轴的哪一侧、屏幕方向、光向与色温、跨切声音。参考优先级为 "identity/assets > scene layout > prop state > action pose > camera example > style decoration"。运镜必须 "reveal, follow, compress, release, isolate, destabilize, or transfer attention"，每个短镜只有一个主运镜想法。FOV 阶梯从 107° 到 8°，身份关键的反应镜头建议 29°–18°。动作链为 intention → anticipation → exertion → contact/near-miss → reaction → recovery → consequence。它建议在正向描述后加短的失败排除句（no identity drift 等），这与 ComfyUI 的"BasicGuider 无负向、点名即登记"说法有张力，需 A/B 验证。
- **对本学院有什么用**：生成任何镜头前，先写一句"这一镜改变了什么"；再用连续性账本审相邻镜头，不过关就删镜，或只改一个变量。
- **落点模块**：10-theory、20-craft、50-rubrics、70-playbooks

### S-H3-11 · teskor-hub/minimax-h3-skill（minimax-h3 + minimax-h3-reel-maker）
- **URL**：https://github.com/teskor-hub/minimax-h3-skill
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：用 fl2va 还是 ref2va 的判断规则："If the value is in the picture, use fl2va. If it's in who's in it, use ref2va."；用 I2VA 从正面特写硬转出背面 "is the single most common way to melt a face"。身份写在 `<Subject N>`，不另立 `<Picture N>`。原生 BasicGuider 路径没有负向，等效 CFG 1。"Structure beats instruction"：能靠构图让错误不可能发生的，就别用文字去禁止；主体自转代替运镜时，用 Arc Shot 并描述背景视差。"Duration is read literally as event speed"：给摔倒 1.5 秒就像月球重力，真实约 0.4–0.6 秒。事件时长表：眨眼 0.3–0.5 秒，转头 0.5–0.8 秒，一步约 0.5 秒，可读运镜 1.5–2.5 秒，英语约 2.7 词/秒。不写声音字段不等于静音。角色设定拼图因分辨率不足，不适合作身份来源。附 check_prompt_dialogue.py。另指出 ComfyUI 节点源码里没有"总文件 ≤12"的校验。
- **对本学院有什么用**：agent 按真实事件时长分配动作节拍（打斗、摔倒用短时长，余下时间留给后果），提交前用对白 lint 检查 (Sx) 和 `<d>` 格式。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-H3-12 · ComfyUI-MiniMaxH3-Director（时间线编辑节点）
- **URL**：https://github.com/seesee75-commits/ComfyUI-MiniMaxH3-Director
- **类型**：tool
- **分类**：🟡 需适配
- **许可**：GPL-3.0
- **核实**：✅ 已打开核实
- **摘录**：由 WhatDreamsCost 的 LTX Director 移植而来的 ComfyUI 时间线编辑器，首个公开版本 0.1.0 发布于 2026-08-04。支持主轨、参考视频轨、音频轨的拖放；每段写一条提示词，实时编译成 H3 分镜格式。完整参考模式包括：参考类别、从 fully_preserved 到 weak_reference 的 retention 标记、自动生成 summary 的 [task type] 前缀，以及把 `@ref1 says: …` 自动转成说话人 ID 和 `<d>`。音频用法有 reference、fully_copy、partially_copy、lock (exact audio) 四种。Save Last Frame 节点把尾帧交给下一镜当首帧；Retake 模式以区间前后的原帧作 first/last 只重生一段，再由 Retake Stitch 拼回。README 写明 "4–15 s is H3's trained range, not a cap"，45 秒据报可跑但会漂移、循环；长时间线的链式窗口节点（Director Chain）已撤回，长片问题 "Not solved yet"。
- **对本学院有什么用**：借鉴它的 Retake 和尾帧接力做法，做局部重生成和镜头衔接，不必整镜重跑。
- **落点模块**：20-craft、70-playbooks

### S-H3-13 · HuggingFace MiniMax-H3 讨论区（#76、#106、#91 等）
- **URL**：https://huggingface.co/MiniMaxAI/MiniMax-H3/discussions
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：用户帖子（仅引用）
- **核实**：✅ 已打开核实（列表页，以及 #76、#106、#91 三帖）
- **摘录**：#76 "Weird gibberish / clipped voice at the very start of H3 videos"：片头约 0.5 秒出现乱语或截断人声。社区给出的绕法：写 overall_soundscape、台词句末加标点、静默段写 silently、音色参考控制在约 4 秒以内；没有官方回复。#106 "如何解决人物胡言乱语的问题"：用户报告角色胡言乱语、发出电子杂音、念出提示词或无故出字幕，有人建议"说完后要求闭嘴"；没有官方回复。#91：Ref2VA 加音频后疑似换人，ImageToVideo 相似度 0.8855，ReferenceToVideo + audio 为 0.0884；仅一人回帖称未复现，且未给数据。列表页还有：#96 几乎不眨眼、#87 脸崩、#84 同一语言口音不一致、#82 Ref2VA 对白场环境声过小、#65 遵循度随分辨率变化、#12 置顶的许可问答帖。
- **对本学院有什么用**：QC 清单专门检查片头 0.5 秒人声、静默段人声、画面里自己冒出的字幕、口音漂移，并把它们记为已知模型缺陷，而不是提示词错误。
- **落点模块**：50-rubrics、60-casebook、40-memory

### S-H3-14 · MiniMax H3 Community License Agreement（含 Acceptable Use Policy）
- **URL**：https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：MiniMax H3 Community License Agreement
- **核实**：✅ 已打开核实
- **摘录**：许可日期 2026-08-02。排除地域："the European Union, the United Kingdom, the Republic of Korea and the United States of America"。V.4：不得在许可地域外 use/reproduce/modify/distribute/display H3 Works 或其 Outputs。IV.2：使用 H3 的商业产品或服务必须在 UI 上显著展示 "MiniMax H3"。III.3：标注 "Powered by MiniMax H3"、添加 AI 生成标识只是"encouraged"（鼓励），不是强制；分发须附 NOTICE 文件。年收入超过 2000 万美元须事先取得书面授权。V.3：不得用 Outputs 改进其他 AI 模型。VI.4：MiniMax 不主张 Outputs 权利。AUP 第 12 条：在公开环境发布须清楚、显著地披露内容为机器生成。AUP 最后修订于 2026-08-02。附注：编码器使用 Qwen3-VL-32B（Apache 2.0）。
- **对本学院有什么用**：发布 playbook 第一步做地域和授权检查（尤其是美区、欧区平台），强制加 AI 生成披露；商业产品 UI 必须标 "MiniMax H3"。
- **落点模块**：70-playbooks、50-rubrics、90-curriculum

### S-H3-15 · MiniMax Speech T2A HTTP API（speech-2.8）
- **URL**：https://platform.minimax.io/docs/api-reference/speech-t2a-http
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：API 服务条款（本次未找到开源权重）
- **核实**：✅ 已打开核实
- **摘录**：模型有 speech-2.8-hd/turbo、2.6-hd/turbo、02-hd/turbo、01-hd/turbo。文本上限 10,000 字符，超过 3,000 字符建议流式输出。停顿语法 `<#x#>`，x 取 0.01–99.99 秒。2.8 专属语气标签 19 个：(laughs)(chuckle)(coughs)(clear-throat)(groans)(breath)(pant)(inhale)(exhale)(gasps)(sniffs)(sighs)(snorts)(burps)(lip-smacking)(humming)(hissing)(emm)(sneezes)。speed 0.5–2，vol (0,10]，pitch −12..12。emotion 枚举为 happy/sad/angry/fearful/disgusted/surprised/calm/fluent/whisper。采样率 8000–44100。字幕时间戳分 sentence/word/word_streaming 三档，单位毫秒。发音词典支持 IPA、带声调数字的普通话拼音、粤拼。
- **对本学院有什么用**：H3 自带对白不可用时改走 TTS 配音链路，直接用 word 级时间戳生成硬字幕，不依赖容易幻听的 ASR。
- **落点模块**：20-craft、70-playbooks

### S-H3-16 · MiniMax Music Generation API（music-3.0 / 2.6）服务调整公告与开源 Music 3 许可
- **URL**：https://platform.minimax.io/docs/api-reference/music-generation
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：API 服务条款；开源权重为 MiniMax-Music3 Community License（https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE ），不是 CC BY-NC 4.0
- **核实**：✅ 已打开核实
- **摘录**：模型有 music-3.0、music-2.6、music-cover 及对应 -free 版。歌词 1–3500 字符（cover 为 10–1000）。结构标签有 [Intro][Verse][Pre Chorus][Chorus][Interlude][Bridge][Outro][Post Chorus][Transition][Break][Hook][Build Up][Inst][Solo]。支持纯音乐开关和歌词自动生成。公告原文："Starting August 20, 2026, the paid APIs (Music Generation and Lyrics Generation) will no longer be available to new users; existing paying users can continue…"；free 版停用，官方引导用户转向 MiniMax Audio 或 Hugging Face 上的开源 MiniMax Music 3。开源权重的许可是 MiniMax-Music3 Community License（最后修订 2026-08-06）：允许商用；年收入超过 2000 万美元须书面授权；商业产品 UI 须显著展示 "MiniMax-Music3"；AUP 要求披露机器生成；本次核对未见地域排除条款。
- **对本学院有什么用**：用 Music 3 做商用配乐时，按其社区许可做署名和收入门槛检查，并把许可版本记进素材台账。
- **落点模块**：20-craft、70-playbooks

### S-H3-17 · Atlas Cloud《MiniMax H3 Director: Can You Actually Direct the Camera?》
- **URL**：https://www.atlascloud.ai/blog/tips/minimax-h3-director
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：博客（仅引用）
- **核实**：✅ 已打开核实
- **摘录**：Atlas Cloud 发表于 2026-08-29。原文："In most creator usage, MiniMax H3 Director means a camera-led way to use MiniMax H3"，即一种以运镜为主导的提示词工作流，不是独立的模型或模式。运镜应当 "treated as instructions to test, not guaranteed buttons"。建议：每段只有一个运镜想法加一个可见动作；写明方向、速度、需要稳定的元素和结束构图；"Start with 5 seconds at the lowest useful test resolution… Move to 2K or a longer duration only after the camera path, subject lock, and final frame work"。三个案例：雨夜自行车快递员跟拍（T2V）、游戏选车界面（R2V）、芝加哥街头服饰广告（I2V），并建议把案例 3 改成 9:16 用于 TikTok/Reels/Shorts。
- **对本学院有什么用**：向用户澄清"Director"只是社区叫法；"一个运镜想法 + 明确结束构图 + 先低清试拍"作为默认工作纪律。
- **落点模块**：10-theory、40-memory

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-H3-01 | H3 官方运镜词表有 12 类运动（Zoom In/Out、Push In/Pull Out、Pan、Truck、Tilt、Pedestal、Arc Shot、Tracking Shot、Static Shot、Shake Slightly/Strongly、POV、Roll），外加 with small/large amplitude、at slow/fast speed；中等振幅、正常速度通常省略；须写成句内自然动作，不在句尾堆标签。 | [MiniMax-H3 skills](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills) | 高 |
| F-H3-02 | I2VA/FL2VA/L2VA 的最终提示词，首行必须是 "How the reference pictures align with the target video — …" 对齐句（秒数两位小数），后空一行再接三字段；T2VA 不写对齐句。 | [MiniMax-H3 skills](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills) | 高 |
| F-H3-03 | Ref2VA 改写分六段：subject_definitions、summary、retention_analysis、detailed_description、overall_soundscape、non_diegetic_music；生成任务的 detailed_description 通常 350–500 英文词，对白密集时优先放下完整台词时间线。 | [MiniMax-H3 skills](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills) | 高 |
| F-H3-04 | 旧托管模型（MiniMax-Hailuo-2.3、MiniMax-Hailuo-02、*-Director）支持 15 条方括号运镜指令；同一 [] 内的指令同时生效、建议不超过 3 个，前后出现的依次生效；prompt 最长 2000 字符。 | [MiniMax 中文 T2V API](https://platform.minimax.cn/docs/api-reference/video-generation-t2v) | 高 |
| F-H3-05 | H3 输出 4–15 秒、24 FPS、短边 768、32 kHz 立体声；开源只有 H3-Base（FL2VA、Ref2VA），Context-IR 与 Regenerate-2K 未开源；官方称 Context-IR "critical to the quality of the final output"，建议接入其 API，或按 Prompting Guidance 自建同等系统。 | [HF 模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3) | 高 |
| F-H3-06 | ComfyUI 中 H3 帧数按 17k+5 网格向上吸附（如 144→158），源码注明训练范围约 124–362 帧（约 5.2–15.1 秒），更长未经测试。 | [nodes_minimax_h3.py](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_minimax_h3.py) | 高 |
| F-H3-07 | MiniMaxH3ImageToVideo 对 first_frame 不保比例直接拉伸到画布，对 last_frame 做居中 cover-crop。推算：1696×2528（约 2:3）的关键帧直接接 768×1344 画布，纵向会被拉伸约 17%。 | [nodes_minimax_h3.py](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_minimax_h3.py) | 中（行为为源码事实，17% 为推算） |
| F-H3-08 | H3 的 ComfyUI 模板走 BasicGuider，没有负向分支，负向提示无效；写 "no subtitles and no on-screen text" 会把文字登记为内容，应写正向状态（如 "the sign above the door is blank"）。 | [Comfy 提示词指南](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide) | 高 |
| F-H3-09 | 默认 20 步；Lightning LoRA 在 T2V/I2V 降到 8 步、在参考类模板降到 4 步。4 步时参考可能几乎不生效、脸角度漂移；8 步时语音音色最弱，12 步以上可用；高频细节到约 50 步仍在改善，步数不足时出现三角网格伪影。 | [Comfy H3 教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3) | 高 |
| F-H3-10 | 社区实测：4 步 turbo 几乎完全压掉运镜，"regardless of the prompt"；最少 124 帧，三段式动作 192 帧。 | [loopforge0/minimaxh3-shots-skills](https://github.com/loopforge0/minimaxh3-shots-skills) | 中 |
| F-H3-11 | 同 prompt、同 seed 的 A/B：只有人物板时背景变换 0.47x，加背景板后 0.81x（运镜约减半），场景漂移由 0.08 降到 0.02（约 4 倍）；把参考称作 first frame 或用 [keyframe completion] 也会钉死起幅、约减半运动。 | [loopforge0/minimaxh3-shots-skills](https://github.com/loopforge0/minimaxh3-shots-skills) | 中 |
| F-H3-12 | 振幅和速度修饰词的实测：small amplitude 基本无效（1.47x，对照 1.53x）；large amplitude 3.18x，末帧糊；large+fast 2.83x，饱和不叠加。 | [loopforge0/minimaxh3-shots-skills](https://github.com/loopforge0/minimaxh3-shots-skills) | 中（n 小） |
| F-H3-13 | whip pan 写明落在谁身上后，单步位移从 23 提到 218 px/step；直接要求 motion blur 不产生动态模糊。 | [loopforge0/minimaxh3-shots-skills](https://github.com/loopforge0/minimaxh3-shots-skills) | 中 |
| F-H3-14 | H3 不能精确安排事件时刻：两份要求在 3.0s / 4.0s 揭示的提示词都在 2.46s 发生；只能规定顺序，精确时机交给剪辑。 | [loopforge0/minimaxh3-shots-skills](https://github.com/loopforge0/minimaxh3-shots-skills) | 中 |
| F-H3-15 | 不可能完成的指令会拖垮整镜：同运镜句，自然动作下运镜位移为 98–108% 画宽，"holds one single pose completely rigid" 降到 22%。 | [loopforge0/minimaxh3-shots-skills](https://github.com/loopforge0/minimaxh3-shots-skills) | 中 |
| F-H3-16 | 一镜塞太多表情节拍会被抹平：7 秒特写写 9 拍，PSNR 37–42 dB（脸不动）；拆成三颗 2–3 秒，降到 22–23 dB（表情到位）；再加 `<d>` 到 19 dB。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 中 |
| F-H3-17 | 武打不受表情节拍上限约束：双人中远景、107 帧、约 3 秒写 8–9 招，4 份提示词 × 2 seed 全部按顺序、真速度完成；作者标为 partly（单场戏、接触未逐格验）。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 低 |
| F-H3-18 | H3 常在片尾前 1.2–1.7 秒崩解，需要留 1.3–1.5 秒尾部余量；运镜作用于整次生成，分段指定会把剪点内插掉，并让剪点从规格的 1.5 秒漂到 3.5–3.8 秒。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 中 |
| F-H3-19 | 说话节奏绑在 seed 上，不在提示词上：同 seed、不同提示词，Whisper 逐字时间到小数点后两位一致；对白坏了先换 seed；有 `<d>` 的镜头里，描述"说话"的叙述句可能被念出来。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 中 |
| F-H3-20 | Whisper 会在片尾安静处幻听一句短语（通常是 "Thank you."），转写出的人声不代表片中真有台词，须逐格核对嘴型。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 中 |
| F-H3-21 | 文字空间地图压不过场景图（同 seed A/B，左右布局不变）；多人场同框只交代关系，台词一律单人正反打。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 中 |
| F-H3-22 | 提示词里提到的物件（包括共用段里的服装、灯具）容易出现在每一颗镜头里；同一人给两张脸参考可能生成两个人，需声明为同一人；服装参考用无脸的隐形人台图。 | [phileiny/h3-storyboard-skill](https://github.com/phileiny/h3-storyboard-skill) | 中 |
| F-H3-23 | 写长的动作时长会被当成慢动作执行（1.5 秒摔倒像月球重力）。参考时长：眨眼 0.3–0.5 秒、转头 0.5–0.8 秒、摔倒 0.4–0.6 秒、一步约 0.5 秒、可读运镜 1.5–2.5 秒、英语约 2.7 词/秒。 | [teskor-hub/minimax-h3-skill](https://github.com/teskor-hub/minimax-h3-skill) | 中 |
| F-H3-24 | 官方讨论区：#76 报告片头约 0.5 秒乱语或截断人声；#106 报告胡言乱语、念出提示词、无故出字幕；#91 报告 Ref2VA + 音频后身份相似度 0.0884（对照 I2V 0.8855）。三帖均无官方回复。 | [HF 讨论区](https://huggingface.co/MiniMaxAI/MiniMax-H3/discussions) | 中 |
| F-H3-25 | H3 许可把欧盟、英国、韩国、美国列为排除地域，禁止在许可地域外使用或展示 Outputs；商业产品 UI 必须显著展示 "MiniMax H3"；"Powered by MiniMax H3" 只是鼓励；年收入超过 2000 万美元须书面授权；不得用 Outputs 改进其他 AI 模型；AUP 第 12 条要求公开发布时明示机器生成。 | [H3 LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) | 高 |
| F-H3-26 | Comfy 文档称本地生成的输出商用需 MiniMax 商业授权，Comfy 为唯一官方经销商；Comfy Cloud 上的生成已含商用权。 | [Comfy H3 教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3) | 高（陈述存在；与许可原文的关系见空白第 5 条） |
| F-H3-27 | 托管 API：MiniMax-H3 支持 768P/2K、4–15 秒；MiniMax-H3-Max 支持 480P/768P、5–15 秒，官方指南称其由 fal.ai 基于 H3 后训练；首尾帧与参考模式互斥；每段文本 ≤7000 字符；prompt_expansion_mode 只对 H3-Max 生效。 | [v2 create](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)、[视频生成指南](https://platform.minimax.io/docs/guides/video-generation.md) | 高 |
| F-H3-28 | H3-Context-IR 接口只返回增强后的提示词，不创建视频任务。 | [Context-IR API](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir.md) | 高 |
| F-H3-29 | "MiniMax H3 Director" 是创作者对"以运镜为主导使用 H3"的叫法，不是独立模型；MiniMax API 枚举里带 Director 的是旧的 T2V-01-Director。h3-cinematic-director、h3-camera-shots、h3-storyboard 均为社区 MIT skill。 | [Atlas Cloud](https://www.atlascloud.ai/blog/tips/minimax-h3-director)、[中文 T2V API](https://platform.minimax.cn/docs/api-reference/video-generation-t2v) | 中 |
| F-H3-30 | MiniMax Speech 2.8 的 T2A 支持 `<#x#>` 停顿、19 个语气标签、9 种 emotion，以及 word 级毫秒时间戳，可用于外配对白和字幕对齐。 | [Speech T2A HTTP](https://platform.minimax.io/docs/api-reference/speech-t2a-http) | 高 |
| F-H3-31 | 2026-08-20 起，付费音乐与歌词 API 不再对新用户开放，free 版停用；开源 MiniMax Music 3 的许可是 MiniMax-Music3 Community License（允许商用，有 2000 万美元收入门槛和 UI 署名要求），不是 CC BY-NC 4.0。 | [Music API](https://platform.minimax.io/docs/api-reference/music-generation)、[Music3 LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE) | 中（许可条款经摘要读取，未逐行通读） |
| F-H3-32 | 社区时间线节点作者称 4–15 秒是训练区间，不是硬上限；45 秒据报可跑但会漂移、循环；长片的链式窗口方案已撤回，"Not solved yet"。 | [ComfyUI-MiniMaxH3-Director](https://github.com/seesee75-commits/ComfyUI-MiniMaxH3-Director) | 中 |

## 空白与未找到

1. **"Director" 的官方出处**：MiniMax 没有任何页面把 H3 称为 Director 模式，也没有 H3 专属的 Director 文档。官方 API 枚举里只看到旧的 T2V-01-Director；I2V-01-Director 本次没有打开核对。有人说"H3 Director"时，可能指社区的 ComfyUI-MiniMaxH3-Director 节点、h3-cinematic-director skill，或泛指运镜主导的写法，需要和说话的人确认。
2. **中文语速与对白容量**：官方没有给出中文语速或每秒对白容量。社区只有单一项目的配音员数据（4.30 字/秒，含句内停顿）和英语约 2.7 词/秒。
3. **9:16 竖屏与 I2V 首帧 + 文字运镜**：官方没有竖屏构图或运镜指南。loopforge 的实测全是 16:9、1344×768、Ref2VA；phileiny 是 9:16，但也是 Ref2VA。所以"I2V 首帧与文字运镜冲突"在 9:16 下没有受控数据。
4. **采样器差异**：官方模板用 res_multistep + simple，没有文档比较 euler 与 res_multistep 在 H3 上的差别；也没有"cfg=1 时如何防止模型自行添加装饰物"的官方条目，只有"提到什么就长什么"的社区经验和 #106 的用户报告。
5. **许可与商用口径不一致**：许可原文写的是"Outputs 不得在排除地域使用或展示""MiniMax 不主张 Outputs 权利"；Comfy 文档写的是"本地输出商用需经 Comfy 购买 MiniMax 商业授权"。两者关系没有找到官方澄清，HF 讨论 #12（许可问答置顶帖）本次没有打开。
6. **配音与配乐的开源路线**：本次没有找到 MiniMax Speech 的开源权重，自托管配音需要另选模型。MiniMax Music 3 的许可已核对（见 S-H3-16），但参数量和发布日期没有在官方页面核实，研究员记录的"约 11.1B、2026-08-13 发布、ComfyUI 当天支持"未采用。
7. **Hailuo 02/2.3 时代的官方提示词指南**：平台文档已切换到 H3，旧指南页没能定位。"T2V-01-Director 2025-02 / Hailuo-02 2025-06 / 2.3 2025-10"这条时间线只见于研究员看到的搜索摘要，本次核实时 WebSearch 额度已用尽，未能复核，因此不收录。
8. **中文版官方文本**：HF 的 README.zh-CN、Comfy 中文版提示词指南没有打开，中文措辞未核对。
9. **托管端几何相机控制**：研究员提到 H3 Max 在 fal / Picsart 有 camera_trajectory（azimuth/elevation/distance 关键帧），本地开源 H3 没有等价控制，社区节点 Camera H3 只是把路径编译成文字。这几点本次均未打开核实，暂不收录为事实。
10. **参考文件总数上限**：HF 模型卡写 Ref2VA 文件总数 ≤12；ComfyUI 节点源码的槽位上限是图 9、视频 3、视频音轨 3、独立音频 3，没看到总数校验（teskor 也指出了这一点）。托管 API 是否强制 ≤12 未核实。
11. **社区数据的外推边界**：loopforge 的结论来自 4 个人物板、5 个场景、int8 量化，多处 n=1–2；phileiny 来自单一项目，其中一条 seed 结论注明是在 "Ref2VA 8 步加速、1376×768" 下测得；teskor 的事件时长表没有给出测量过程。这些数据只能当假设，学院应在自己的管线上复测后再写进判据。
12. **核实说明**：17 条全部用 WebFetch 打开在线页面。GitHub 仓库和官方 skill 的细节（数字、原文）另外对照研究员下载到本地的克隆和文件，并逐条 grep 原文。ComfyTV 的目录页不渲染 SKILL.md，其内容仅按克隆核对。
