# ComfyUI / Qwen-Image / QC 工具链事实

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：21 ｜ 核实方式：逐条 WebFetch 打开核对

## 一句话结论

本专题给学院提供三类可引用的硬事实。一是 Qwen-Image-2.1 在 ComfyUI 中的官方参数路径：2:3 对应 1696×2528，官方管线约 40 步；"cfg=1 时负向提示不参与计算"有 ComfyUI 文档、ComfyUI 源码、diffusers 文档三处独立出处。官方提示词改写规范（方位短语、光照句、禁质量咒语、肯定式约束、身份指向参考图）也已逐字核对。二是 QC 工具链的默认阈值和命令，涵盖 FFmpeg 响度/黑场/冻帧/切点、PySceneDetect、Whisper/faster-whisper/SenseVoice、PaddleOCR，另有 Whisper 中文静音幻觉串的 MIT 数据集证据，以及中国网络视听响度标准 GY/T 377-2023。三是许可边界：Qwen-Image-2.1 用研究许可（非商用），MiniMax H3 本地生成内容商用需另购授权。

仍然缺的有：各短视频平台的官方响度目标；OCR 对 AI 伪汉字的召回评测；AI 视频坏帧的公认阈值；H3 上 euler 与 res_multistep 的对比。Qwen 许可是否约束生成物本身，需要法务确认。

## 条目

### S-COMFY-01 · Qwen-Image-2.1 官方模型卡（Hugging Face）
- **URL**：https://huggingface.co/Qwen/Qwen-Image-2.1
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Qwen Research License Agreement。LICENSE 原文授权范围是 "FOR NON-COMMERCIAL PURPOSES ONLY"，"Non-Commercial" 定义为 "for research or evaluation purposes only"。商用须另获商业许可，申请邮箱为 model-business@notice.qwencloud.com。
- **核实**：✅ 已打开核实
- **摘录**：生成部分为 32 层 Single-Stream DiT，7B 参数，采用混合粒度注意力和前缀 KV 缓存复用。原生支持 RGBA 透明。最多接受 10 张参考图，局部编辑可以用圈选、涂画标注或单独的 mask 指定，并保持人物与产品的身份。推荐尺寸如下：
  - 1:1：2048×2048
  - 4:3：2400×1792；3:4：1792×2400
  - 3:2：2528×1696；2:3：1696×2528
  - 16:9：2752×1536；9:16：1536×2752

  示例代码一律写 `num_inference_steps=40`，不传 cfg/guidance 参数。透明图的示例提示词以 "This is an RGBA image with transparency." 开头，以 "The image has alpha channel and the background is transparent." 结尾。Comfy 模板里的同类包裹句写作 "This is an RGBA format image with transparency"，与模型卡差一个词。发布日期 2026-09-20，见 GitHub 仓库 News 和 LICENSE 的 Release Date。
- **对本学院有什么用**：agent 可以确认 1696×2528 加 40 步就是官方 2:3 路径，不是自创参数；任何商用发布前，必须先过一道"模型许可证核查"。
- **落点模块**：20-craft、40-memory、50-rubrics、70-playbooks

### S-COMFY-02 · QwenLM/Qwen-Image-2.1 GitHub README（官方提示词改写与架构说明）
- **URL**：https://github.com/QwenLM/Qwen-Image-2.1
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：Qwen Research License Agreement（非商用，与 S-COMFY-01 相同）
- **核实**：✅ 已打开核实
- **摘录**：
  - **架构**：文本编码器为 Qwen3-VL 8B，同时编码文本指令和条件图。VAE 为 64 通道 RGBA 自编码器，空间压缩 16 倍。调度器为 Flow Matching + Euler discrete + dynamic shifting。默认参数表：num_inference_steps 40，分辨率 2048×2048。
  - **提示词改写**：官方推荐两款提示词改写模型 Qwen/Qwen-Image-2.1-PE-T2I 和 PE-I2I，均由 Qwen3.5-VL 9B 微调而来，输出 `rewritten_prompt` 和 `wh_ratio`；编辑任务可输出 `"ratio_follow": "<image1>"`。
  - **多参考图示例**：提示词为 "These three characters are sitting around a campfire in a forest"。README 另有一张图注为 "Storyboard generated from a three-view character reference"。
  - **SGLang 示例**：`--num-inference-steps 40 --guidance-scale 1`。
  - **首日支持**：2026-09-20 当天，Diffusers（`QwenImage21Pipeline`）、ComfyUI、vLLM-Omni、SGLang、LightX2V 均宣布支持。
- **对本学院有什么用**：agent 可以用官方 PE 改写模型（或按其写法）规范板图提示词。需要知道：官方采样路径的 guidance 就是 1。
- **落点模块**：20-craft、40-memory、70-playbooks

### S-COMFY-03 · ComfyUI 官方教程：Qwen-Image-2.1 Native Workflow Example
- **URL**：https://docs.comfy.org/tutorials/image/qwen/qwen-image-2-1
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Comfy Org 官方文档（引用事实）
- **核实**：✅ 已打开核实
- **摘录**：
  - **采样设置**：三个模板都用 steps 25、cfg 1、euler、simple。
  - **cfg**：原文 "At `cfg` 1 ComfyUI skips the negative conditioning pass, so a negative prompt has no effect on these workflows"。cfg 2 更贴合密集提示（含小字和数字），代价是边缘过锐；cfg 再高会让曝光偏亮或偏暗；cfg 5 严重劣化；cfg 0.5 画面崩坏。文档要求一次只改一个值，并在固定 seed 下比较。
  - **steps**：官方管线约 40–50 步，用 euler。局部小编辑 4–8 步即可，整帧重写需要完整 25 步。手和手指约 30 步才稳定；从 25 步升到 40 步，细节区的 fizzle 会减少。目标尺寸远超 2K（如 4K）时提示遵从下降。
  - **编辑**：Text Encode 节点最多 16 个槽；模板接了前 10 个，提示词里用 `<image1>`…`<image10>` 指代，其中 image_1 是被编辑图，其余为素材。`resolution` 是总像素预算，不是宽或高。可以用 Mask Editor 的 Paint Pen 涂色，再在提示词里点名该颜色，把编辑限定在该区域。
  - **缓存**：Qwen Image 2.1 Cache 节点的 int4 选项把缓存降到四分之一，但每步误差约翻倍。
- **对本学院有什么用**："cfg=1 负向提示无效"引用这里作为首要官方出处。agent 编辑时用 `<imageN>` 指向身份参考，调参时固定 seed、一次只改一个变量。
- **落点模块**：10-theory、20-craft、40-memory、50-rubrics

### S-COMFY-04 · Comfy-Org workflow_templates：Qwen-Image-2.1 T2I/Edit 模板 JSON（含官方 PE 系统提示词）
- **URL**：https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT（仓库 LICENSE 已核对，Copyright Comfy Org）
- **核实**：✅ 已打开核实（另下载原始 JSON 逐字 grep；编辑模板见同目录 `image_qwen_image_2_1_image_edit.json`）
- **摘录**：
  - **模板注释原文**："negative_prompt: unused while cfg is 1."、"cfg: keep 1 for the Qwen Image 2.1 official path. Raise it only if you use a negative prompt."、"Prefer multiples of 32."
  - **T2I 系统提示词**：
    - 篇幅约二十句、四到五百词，写成一段。
    - 开头句模板为 "The image is a ⟨vertical / wide / square / tall⟩ ⟨style⟩ ⟨medium⟩ of ⟨subject⟩, ⟨background and palette⟩."。未指定画幅时，横构图默认 3:2，竖构图默认 2:3。
    - 需要 8–14 个方位短语，约三分之一的句子以方位短语开头。
    - 单主体按以下顺序描写：背景 → 姿态与位置 → 头脸 → 身体与服装 → 手持或接触物 → 边缘。
    - 光照单独写一句 "The lighting is …"，最后以 "The overall composition …" 收尾。
    - 禁止 "masterpiece" 一类质量增强词。颜色要带修饰语，要写材质，逐项列举而不概括；画面没有可读文字时，不得凭空发明招牌。
  - **Edit 系统提示词**：
    - 以"属性解耦"为总原则。
    - 保留项优先用一句整体保留句带过，原文 "the more concretely you describe something you meant to keep, the more likely it drifts"。
    - 身份来自参考图时，指向该图，不用文字描述五官，原文 "verbal descriptions make the model regenerate and degrade the likeness"。
    - 多图必须用 `<image1>` 等标签。
    - 要求用肯定式表达（例："保持背景与输入图完全一致"），不用禁止式。
  - **反例**：T2I 模板自带的默认示例提示词以 "Absolutely no text, no typography, no letters, no words, no numbers, no logos, no watermark, no captions, pure imagery only." 结尾。这与同一模板的 cfg=1 注释和 PE 规范相矛盾，说明官方示例本身也会写否定式。
- **对本学院有什么用**：可以直接改编成学院的"板图/关键帧提示词写法"技能和 lint 规则：方位短语、光照句、禁质量咒语、肯定式约束、身份指向参考图。另外，不得把厂商示例提示词当范本照抄。
- **落点模块**：20-craft、30-taste、50-rubrics、70-playbooks

### S-COMFY-05 · ComfyUI 源码 comfy/samplers.py（cfg=1 跳过无条件分支）
- **URL**：https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/samplers.py
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：GPL-3.0
- **核实**：✅ 已打开核实（另取原始文件逐行核对 samplers.py、sample.py、cli_args.py）
- **摘录**：
  - **cfg≈1 跳过无条件分支**：`sampling_function` 中，`if math.isclose(cond_scale, 1.0) and model_options.get("disable_cfg1_optimization", False) == False: uncond_ = None`，即 cfg≈1 时不计算无条件/负向分支。
  - **CFG 公式**：`cfg_function` 中为 `cfg_result = uncond_pred + (cond_pred - uncond_pred) * cond_scale`，scale=1 时等于条件预测。
  - **噪声生成**：同仓库 comfy/sample.py 的 `prepare_noise` 用 `torch.manual_seed(seed)` 建一个生成器，在 CPU 上为整批 latent 一次性生成噪声；带 batch_index 时按序号依次抽取。所以批内第 k 张的噪声不等于单独用 seed+k 生成的噪声。
  - **命令行参数**：comfy/cli_args.py 提供 `--listen`（默认 127.0.0.1）、`--port`（默认 8188）、`--disable-metadata`、`--deterministic`。`--deterministic` 的帮助文字写明 "might not make images deterministic in all cases"。
- **对本学院有什么用**：为"cfg=1 负向提示无效"提供代码级证据。agent 每次抽卡都要记录 seed 和 batch_index，才能复现。
- **落点模块**：10-theory、40-memory、50-rubrics

### S-COMFY-06 · Diffusers 文档：QwenImage pipelines（true_cfg_scale / negative_prompt 语义）
- **URL**：https://huggingface.co/docs/diffusers/main/en/api/pipelines/qwenimage
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Apache-2.0（diffusers 项目文档）
- **核实**：✅ 已打开核实
- **摘录**：
  - **true_cfg_scale**：定义为 Imagen 论文式 2 中的 w；原文 "Classifier-free guidance is enabled by setting `true_cfg_scale > 1` and a provided `negative_prompt`"。
  - **negative_prompt**：原文 "Ignored when not using guidance (i.e., ignored if `true_cfg_scale` is not greater than `1`)"。
  - **guidance_scale**：只供 guidance-distilled 模型使用，非蒸馏模型会忽略。文档还说明，传入 true_cfg_scale>1 时，哪怕负向提示只是一个空格 " "，也会启用 CFG 计算。
  - **管线**：页面列出 QwenImagePipeline、Img2Img、Inpaint、Edit、EditInpaint、ControlNet、EditPlus、Layered。另给出加载 `lightx2v/Qwen-Image-Lightning` 8 步 LoRA 减步的示例。
- **对本学院有什么用**：在理论章节里作为第二个独立出处：负向提示只在 cfg>1 时参与计算，agent 不得把负向字段当成禁止某内容出现的机制。
- **落点模块**：10-theory、50-rubrics

### S-COMFY-07 · Ho & Salimans《Classifier-Free Diffusion Guidance》arXiv:2207.12598
- **URL**：https://arxiv.org/abs/2207.12598
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：arXiv 论文（引用）
- **核实**：✅ 已打开核实（仅摘要页）
- **摘录**：论文提出不需要外部分类器的引导方法：联合训练条件扩散模型和无条件扩散模型，采样时组合两者的 score 估计，在样本质量和多样性之间取舍，效果与 classifier guidance 相当。本次只核实了摘要，没有核对正文公式的记法。"scale=1 时退化为纯条件预测"这一点来自 ComfyUI 源码（S-COMFY-05）和 diffusers 文档（S-COMFY-06），不是本论文摘要里的原话。
- **对本学院有什么用**：在理论章节里作为 CFG 原理的原典引用，解释为什么 cfg=1 路径只能靠正向描述控制内容。
- **落点模块**：10-theory

### S-COMFY-08 · ComfyUI 官方：MiniMax H3 Prompt Guide（"Write bans as positives"）
- **URL**：https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Comfy Org 官方文档（引用事实）
- **核实**：✅ 已打开核实
- **摘录**：
  - **第 8 条 "Write bans as positives"**：H3 模板经 `BasicGuider` 采样，只有一个条件输入，原文 "there is no negative branch and a negative prompt has no effect (the guider runs at `cfg` 1, where ComfyUI skips the unconditional pass; a `CFGGuider` only uses negative conditioning above `cfg` 1)"。写 "no subtitles and no on-screen text" 反而会把文字登记为内容，应改写成 "the sign above the door is blank"。
  - **语言与文字**：提示词用英文。台词放在 `<d>` 里，原文照录。画内文字用英文双引号括起，保留原语言原文。
  - **时长**：length 是 24fps 下的帧数，默认 124（约 5 秒），向上对齐 17k+5。
  - **音频字段**：overall_soundscape 写 1–4 句，non_diegetic_music 写 1–3 句。安静镜头冒出没要求的台词时，要把两个音频字段都显式写出再重生成。
  - **说话人**：说话人 ID 用 (S1)、(S2) 并在每个发声镜头中重复。画外音须写 "says in an off-screen voiceover"，紧接着声明画面人物嘴唇闭合。
  - **参考图**：本地 R2V 节点最多 9 张参考图。多视图设定板单独占一个 `<Picture N>`，按面板逐镜指向。
- **对本学院有什么用**：agent 要把所有"不要字幕/不要首饰/不要盔甲/不要水印"改写成对该表面实际内容的正向描述。相关 lint 规则以这里的官方原文为依据。
- **落点模块**：10-theory、20-craft、50-rubrics、60-casebook、70-playbooks

### S-COMFY-09 · ComfyUI 官方：MiniMax H3 Video Generation Guide（许可、画布、步数、采样器）
- **URL**：https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：文档引用。文档写明 H3 本地生成内容商用需要 MiniMax 商业许可，经 Comfy 购买；Comfy Cloud 上的生成已含商用权。
- **核实**：✅ 已打开核实
- **摘录**：
  - **许可原文**："Commercial use of locally generated outputs requires a MiniMax commercial license, available through Comfy, the only official reseller. Generations on Comfy Cloud already include commercial rights."
  - **画布**：开放权重短边 768（约 1MP），24fps，约 15 秒；16:9 时为 1344×768。尺寸取 32 的倍数。2K 需在原生画布生成后另做放大。
  - **采样器**：所有本地模板都用 res_multistep + simple；H3 模型定义内置 shift 12 / audio_shift 3。
  - **步数**：
    - 基础权重默认 20 步。
    - 简单内容 12–16 步即可。
    - 锁子甲、花纹一类高频细节直到约 50 步仍在改善，步数不够时出现随运动游动的三角网格伪影。
    - 音频收敛最晚：8 步时语音和音色最弱，12 步以上可用。
  - **Turbo/Lightning LoRA**：参考驱动模板开启后降到 4 步。原文称这时参考 "can end up barely applied"，姿态或脸部角度可能随片段推进漂离参考。
  - **Sage Attention**：配 INT8 时可能出现片尾形变和画内文字乱码；bf16 检查点配 Comfy Kitchen attention 可以消除。
- **对本学院有什么用**：agent 在视频环节要核对采样器、步数、Turbo 开关与参考一致性之间的关系，并把 H3 商用许可列进发布前检查清单。
- **落点模块**：20-craft、40-memory、50-rubrics、70-playbooks

### S-COMFY-10 · ComfyUI 官方：Server Routes & WebSocket
- **URL**：https://docs.comfy.org/development/comfyui-server/comms_routes
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：文档引用；配套示例脚本属 ComfyUI 仓库（GPL-3.0）
- **核实**：✅ 已打开核实（示例脚本与 KSampler 文档另行打开）
- **摘录**：
  - **路由**：POST /prompt 提交工作流；GET/POST /queue 查询或管理队列；GET /history/{prompt_id} 取结果；GET /view 取图；POST /upload/image 和 /upload/mask 上传；POST /interrupt 中断；POST /free 卸载模型；GET /object_info 取节点定义；GET /system_stats 取系统信息。
  - **WebSocket**：/ws 推送 status、execution_start、execution_cached、executing、progress、executed 等消息。
  - **示例脚本**（script_examples/websockets_api_example.py）：以 `{"prompt":..., "client_id":..., "prompt_id":...}` 提交；收到 executing 且 `data['node'] is None` 时判定完成；再从 /history 读 outputs，经 /view 下载。
  - **KSampler 文档**（https://docs.comfy.org/built-in-nodes/sampling/ksampler）：seed 带 `control_after_generate` 属性，cfg 默认 8.0。
- **对本学院有什么用**：agent 可以用无头 API 批量提交冻结的提示词，自己管理 seed 并把 prompt JSON 落盘，不依赖 UI 自动改种子。
- **落点模块**：40-memory、70-playbooks、90-curriculum

### S-COMFY-11 · FFmpeg Filters Documentation
- **URL**：https://ffmpeg.org/ffmpeg-filters.html
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：FFmpeg 文档（软件为 LGPL/GPL）
- **核实**：✅ 已打开核实（另下载全文逐项 grep）
- **摘录**：
  - **ebur128**：target 默认 -23LUFS，原文 "material published online may prefer a level of -16LUFS (e.g. for use with podcasts or video platforms)"。该 target 只是可视化的相对零点，ebur128 本身不做归一。`peak=true` 时在过采样信号上测真峰值。M 为 400ms，S 为 3s。
  - **loudnorm**：I 默认 -24、LRA 7、TP -2。动态模式会上采样到 192kHz 测真峰值。linear 模式需要提供 measured_I/LRA/TP/thresh 四项，且满足条件，否则退回 dynamic。
  - **检测类滤镜**：blackdetect 默认 d=2.0、pic_th 0.98、pix_th 0.10；freezedetect 默认 -60dB、2 秒；silencedetect 默认 -60dB、2 秒；scdet 默认阈值 10，原文 "Good values are in the [8.0, 14.0] range"。
  - **tile**：默认 6x5，可设 padding 和 margin。
  - **psnr/ssim**：两路输入须同分辨率、同像素格式，逐帧比较。
- **对本学院有什么用**：为学院的 verify 脚本提供可以直接运行的命令和默认阈值，包括响度、黑场、冻帧、静音、切点、联络表，以及"输出首帧 vs 输入关键帧"的 SSIM 首帧遵从检查。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-COMFY-12 · GY/T 377—2023《网络视听节目音频响度技术要求和测量方法》全文 PDF
- **URL**：https://file.smejs.cn/group1/M00/05/0B/rBIAAWTsVOuAR79xAARAFqo4M3s952.pdf
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：国家广播电视总局发布的推荐性行业标准（公开引用）。该 PDF 托管在第三方站点，不是总局官网。
- **核实**：✅ 已打开核实（下载 PDF 并抽取文本核对）
- **摘录**：
  - **发布**：国家广播电视总局 2023-08-18 发布并实施。适用于非直播类网络视听节目的制作、分发和接收，直播类参考执行。
  - **响度（5.1 a）**：原文"网络视听节目的平均响度应保持一致，应为-15LKFS 或-24LKFS，容差范围应不超过±2LU"。平台可同时分发两个版本：-15LKFS 面向嘈杂环境（车载接收、户外运动、公交地铁等），-24LKFS 面向安静环境。
  - **真峰值（5.1 c）**："最大真峰值音频电平应不超过-1dB TP"。
  - **测量**：用 GY/T 262—2012 算法，平均模式（对应 EBU-TECH 3341 的 integrated mode），测完整时长内所有声道。对白占比少的节目，宜测含对白部分的平均响度。
- **对本学院有什么用**：把客户的 -16 LUFS 目标锚定到中国官方标准（-15±2 LKFS、TP≤-1 dBTP），让响度量规有合规出处。
- **落点模块**：10-theory、50-rubrics、70-playbooks

### S-COMFY-13 · AES TD1008 流媒体响度建议（Production Advice 解读）
- **URL**：https://productionadvice.co.uk/td1008/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：第三方文章（引用）
- **核实**：✅ 已打开核实
- **摘录**：这是一篇 2021-10-01 的文章，解读 AES TD1008（TD1004 的后继，全名 "Recommendations for Loudness of Internet Audio Streaming and On-Demand Distribution"）。
  - **定义**：Distribution Loudness 指设备实际播放的整体响度。
  - **建议值**：纯语音和 "Assorted"（语音、音乐、音效混合，如播客）推荐 -18 LUFS，与 TD1004 相同；音乐有两种归一方式，结果都是 -16 LUFS。
  - **用户偏好**：文中称研究显示 80% 用户更偏好专辑归一。
  - **适用范围**：作者强调这些建议面向在线电台和流媒体服务，不约束录音、混音和母带。
- **对本学院有什么用**：为"对白类内容与音乐类内容的响度目标不同"提供国际参照，辅助判断短剧对白与配乐的混音平衡。
- **落点模块**：10-theory、50-rubrics

### S-COMFY-14 · openai/whisper transcribe.py（幻觉相关阈值的真实语义）
- **URL**：https://github.com/openai/whisper/blob/main/whisper/transcribe.py
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实（另取原始文件核对代码行）
- **摘录**：
  - **默认值**：compression_ratio_threshold=2.4、logprob_threshold=-1.0、no_speech_threshold=0.6、condition_on_previous_text=True、hallucination_silence_threshold=None（需 word_timestamps=True 才生效）。
  - **静音跳过逻辑**：先判 `should_skip = no_speech_prob > no_speech_threshold`；若 `avg_logprob > logprob_threshold`，则置回 False，源码注释为 "don't skip if the logprob is high enough, despite the no_speech_prob"。
  - **相关文档说明**：关闭 condition_on_previous_text 后，模型 "less prone to getting stuck in a failure loop, such as repetition looping"；hallucination_silence_threshold 会在检测到可能的幻觉时跳过长静音。
  - **〔学院推断〕**：高置信度的套话式幻觉（如片尾字幕串）不会被默认阈值拦下。
- **对本学院有什么用**：让 agent 明白，Whisper 默认阈值不足以拦住"字幕by索兰娅"一类幻觉，必须先做 VAD 门控和字速检查，再采信 ASR 结果。
- **落点模块**：10-theory、50-rubrics、60-casebook

### S-COMFY-15 · SYSTRAN/faster-whisper（Silero VAD 过滤）
- **URL**：https://github.com/SYSTRAN/faster-whisper
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实（另取 faster_whisper/vad.py 核对默认值）
- **摘录**：
  - **用法**：`transcribe(..., vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))` 会用 Silero VAD 去掉无语音部分。
  - **README 原文**："The default behavior is conservative and only removes silence longer than 2 seconds"、"Vad filter is enabled by default for batched transcription"。
  - **VadOptions 默认值**（vad.py）：threshold 0.5、neg_threshold None、min_speech_duration_ms 0、max_speech_duration_s inf、min_silence_duration_ms 2000、speech_pad_ms 400。
- **对本学院有什么用**：对 5–15 秒的短片段，agent 要把 VAD 静音阈值调低（如 300–500ms，〔学院推断〕，待样片校准），无语音段不送 ASR。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-COMFY-16 · Whisper 静音幻觉数据集 sachaarbonel/whisper-hallucinations
- **URL**：https://huggingface.co/datasets/sachaarbonel/whisper-hallucinations
- **类型**：asset-library
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实（另下载 phrases.csv 逐条 grep）
- **摘录**：
  - **构建方法**：把纯噪声片段用默认参数喂给 Whisper，收集非空输出，做空格与 Unicode 归一，再按语种和短语计频后导出。
  - **规模**：phrases.csv 有 lang、phrase、count 三列，实际 7,889 行数据。
  - **中文条目**（逐字核对存在）："字幕by索兰娅""字幕提供者 李宗盛""请不吝点赞 订阅 转发 打赏支持明镜与点点"（数据集中截断，无"栏目"二字）"字幕由amara org社区提供""谢谢观看 下集再见""下集预告""别忘了订阅""大家好 欢迎来到我的频道"。
  - 研究员提到的 amical 衍生列表（7,422 条）和 Speech-Translate 黑名单不在本页面，本次未核实，不采用。
- **对本学院有什么用**：直接作为学院 Bag-of-Hallucinations 黑名单的种子。规定命中只降级为"待核"，避免误删短剧集尾的真台词（如"下集再见"）。
- **落点模块**：40-memory、50-rubrics、60-casebook

### S-COMFY-17 · Barański 等《Investigation of Whisper ASR Hallucinations Induced by Non-Speech Audio》arXiv:2501.11378（ICASSP 2025）
- **URL**：https://arxiv.org/abs/2501.11378
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：arXiv 论文（引用）
- **核实**：✅ 已打开核实（仅摘要页；配套论文 arXiv:2402.08021 亦打开摘要页）
- **摘录**：
  - **本文**：研究非语音音频在推理时诱发的 Whisper 幻觉。用多种声音诱发后，发现存在一组高频出现的幻觉；又研究了语音与这些声音混合时的情况。论文构建 "bag of hallucinations (BoH)" 做转写后处理，摘要称其 "is capable of reducing word error rate (WER) and acts as a good safeguard against problematic hallucinations"。
  - **配套论文**：Koenecke 等《Careless Whisper: Speech-to-Text Hallucination Harms》（https://arxiv.org/abs/2402.08021）摘要：约 1% 的转写含整句幻觉，其中 38% 含明确伤害；幻觉在 non-vocal durations 占比更长的说话人（失语症组）中更多发生。
- **对本学院有什么用**：为"QC 工具自己也会幻觉，需要黑名单加门控"提供学术依据，写进自我验证闭环的反例案例卡。
- **落点模块**：10-theory、60-casebook

### S-COMFY-18 · FunAudioLLM/SenseVoice（中文 ASR + 情感/事件标签）
- **URL**：https://github.com/FunAudioLLM/SenseVoice
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：代码为 MIT。SenseVoiceSmall 权重按 FunASR Model Open Source License；README 引用维护者澄清，官方权重在遵守许可前提下允许商用，但第 2.2 条的署名与模型名要求仍然适用。
- **核实**：✅ 已打开核实
- **摘录**：
  - **能力**：SenseVoiceSmall 支持普通话、粤语、英、日、韩的 ASR 和语种识别。
  - **标签**：情感标签 7 类（HAPPY/SAD/ANGRY/NEUTRAL/FEARFUL/DISGUSTED/SURPRISED），事件标签 8 类（BGM/Speech/Applause/Laughter/Cry/Sneeze/Breath/Cough）。
  - **速度**：非自回归，参数量相近时比 Whisper-Small 快 5 倍以上，比 Whisper-Large 快 15 倍。
  - **示例用法**：`AutoModel(model="iic/SenseVoiceSmall", vad_model="fsmn-vad", vad_kwargs={"max_single_segment_time": 30000})`，`generate(language="auto", use_itn=True, batch_size_s=60, merge_vad=True, merge_length_s=15)`。language 可选值含 "nospeech"。
  - **README 自述**：事件分类与专用 AED 模型仍有差距。
- **对本学院有什么用**：agent 可以把它作为第二个 ASR 引擎，与 Whisper 交叉核对台词，并用情感和事件标签粗查表演情绪与音效是否生成。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-COMFY-19 · PaddleOCR 3.7 / PP-OCRv6（含 RapidOCR ONNX 部署）
- **URL**：https://github.com/PaddlePaddle/PaddleOCR
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：Apache-2.0。RapidOCR（https://github.com/RapidAI/RapidOCR）的 LICENSE 也是 Apache-2.0。
- **核实**：✅ 已打开核实（RapidOCR 另取 README 与 LICENSE 核对）
- **摘录**：
  - **发布**：2026-06-11 发布 PaddleOCR 3.7.0 与 PP-OCRv6。
  - **档位**：tiny 1.5M、small 7.7M、medium 34.5M 三档。
  - **语种**：单模型覆盖中文、英文、日文及 46 种拉丁语系语言。
  - **精度**：medium 相对 PP-OCRv5_server 检测 +4.6%、识别 +5.1%。
  - **速度**：OpenVINO 下 CPU 提速 5.2 倍，A100 上 0.13s。
  - **场景改进**：数字显示屏、点阵字、轮胎印字、工业文字。
  - **RapidOCR**：把 PaddleOCR 模型转为 ONNX，`pip install rapidocr onnxruntime` 即可在 CPU 上运行。
- **对本学院有什么用**：agent 可以按"抽帧 → 字幕带/四角/全画面分区裁切 → OCR → 与允许文字清单比对"的流程，自动拦截硬字幕、水印和伪文字。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-COMFY-20 · PySceneDetect v0.7.1 CLI 文档
- **URL**：https://www.scenedetect.com/docs/latest/cli.html
- **类型**：tool
- **分类**：🟢 可直接用
- **许可**：BSD-3-Clause（另取 GitHub 仓库 LICENSE 核对）
- **核实**：✅ 已打开核实
- **摘录**：
  - **检测器与默认阈值**：
    - detect-content：27.0
    - detect-adaptive：3.0（min-content-val 15.0，frame-window 2）
    - detect-threshold：12.0（用于淡入淡出，fade-bias 0）
    - detect-hash：0.395（size 16，lowpass 2）
    - detect-hist：0.05（bins 256）
  - **最短镜头**：min-scene-len 默认 0.6s。
  - **常用命令**：list-scenes 输出 CSV，save-images 每镜抽图，split-video 按切点分割，time 设定处理区间。
- **对本学院有什么用**：agent 可以量化成片的平均镜头时长和分布，把"片段式 3 秒碎镜"变成可测指标，并检测单条生成片段里模型自己插入的硬切。
- **落点模块**：30-taste、50-rubrics、70-playbooks

### S-COMFY-21 · 同行 AI 片管线经验：infometa/workbuddyskills workrally-brand-film-pipeline SKILL.md
- **URL**：https://github.com/infometa/workbuddyskills/blob/main/connectors/workrally1/skills/workrally-brand-film-pipeline/SKILL.md
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：未声明（页面未显示许可，仓库根目录 LICENSE 返回 404），只借鉴思路
- **核实**：✅ 已打开核实（另取原始文件 grep 原文；版本 2026.09.22.1）
- **摘录**：
  - **Pitfall 69**："否定式约束在生成模型上不可靠"。写了"无可读文字"，招牌、水幕、书页上仍稳定生成"类汉字伪字形"。应改成肯定式描述该表面的实际内容，并做原尺寸裁切目检。
  - **Pitfall 58 / §2f**：图库原型召回。监控室、屏幕墙、安防一类题材词会召回自带标识和角标水印的套路图，负面提示压不住，需要换语义场。
  - **Pitfall 70**：字幕建轴要做双 ASR 交叉、定点复核和 volumedetect 能量实测；不得用 initial_prompt 补漏。中文频道幻觉的特征是 6–20 字挤在 20–40ms 内，并在不同音频的同一位置重复，文中举例"请不吝点赞 订阅 转发 打赏支持明镜与点点栏目""字幕by索兰娅"。
  - **音频**：文档要求对最终编码的 MP4/AAC 用 `ebur128=peak=true` 实测真峰值，并明确写道：某次 0.5–1.0dB 的 AAC 过冲、+1.1dB 的抬升"不当定律"。
- **对本学院有什么用**：为学院案例库提供与客户问题同构的真实失败案例（伪文字、水印、ASR 幻觉、响度过冲）及其修复顺序。这些都是单一项目经验，需要复测。
- **落点模块**：60-casebook、40-memory、70-playbooks

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-COMFY-01 | 客户板图尺寸 1696×2528 正是 Qwen-Image-2.1 官方推荐的 2:3 尺寸。官方示例统一 num_inference_steps=40，默认分辨率 2048×2048（原生 2K）。 | [HF 模型卡](https://huggingface.co/Qwen/Qwen-Image-2.1)、[GitHub README](https://github.com/QwenLM/Qwen-Image-2.1) | 高 |
| F-COMFY-02 | ComfyUI 官方 Qwen-Image-2.1 模板用 cfg 1，原文 "At cfg 1 ComfyUI skips the negative conditioning pass, so a negative prompt has no effect"。cfg 2 更贴合小字但边缘过锐，cfg 5 严重劣化，cfg 0.5 崩坏。 | [ComfyUI Qwen-Image-2.1 教程](https://docs.comfy.org/tutorials/image/qwen/qwen-image-2-1) | 高 |
| F-COMFY-03 | ComfyUI 源码在 cond_scale≈1 时把 uncond 置为 None，不计算负向分支（可用 disable_cfg1_optimization 关闭此优化）。CFG 公式 uncond+(cond−uncond)·scale 在 scale=1 时等于纯条件预测。 | [comfy/samplers.py](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/samplers.py) | 高 |
| F-COMFY-04 | MiniMax H3 官方模板经 BasicGuider 以 cfg 1 采样，没有负向分支。在正向提示里写 "no subtitles and no on-screen text" 反而会把文字登记为内容，应改写为 "the sign above the door is blank" 这类正向描述。 | [H3 Prompt Guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide) | 高 |
| F-COMFY-05 | diffusers：negative_prompt 在 true_cfg_scale 不大于 1 时被忽略；启用 CFG 需要 true_cfg_scale>1 并提供 negative_prompt（空格 " " 也算）。 | [diffusers QwenImage](https://huggingface.co/docs/diffusers/main/en/api/pipelines/qwenimage) | 高 |
| F-COMFY-06 | Qwen-Image-2.1 用 Qwen Research License，授权限于 "NON-COMMERCIAL PURPOSES ONLY"（研究/评估），商用须另签商业许可。对照：Qwen-Image-Edit-2511 的 HF 许可标签为 apache-2.0。 | [Qwen-Image-2.1 README/LICENSE](https://github.com/QwenLM/Qwen-Image-2.1)、[Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | 高（Edit-2511 只核对了 HF API 的许可标签） |
| F-COMFY-07 | MiniMax H3 开放权重在本地生成的内容，商用需要 MiniMax 商业许可，Comfy 是唯一官方经销商；Comfy Cloud 上的生成已含商用权。 | [H3 Guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3) | 高（与 H3 许可原文的关系见 minimax-h3-hailuo.md 空白第 5 条） |
| F-COMFY-08 | H3 本地模板一律用 res_multistep + simple，基础 20 步。音频收敛晚于画面：8 步时语音最弱，12 步以上可用。参考驱动模板开 Turbo 后为 4 步，参考可能几乎未被施加，脸和姿态会漂移。高频细节要接近 50 步。 | [H3 Guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3) | 高 |
| F-COMFY-09 | Qwen-Image-2.1 官方编辑 PE 规范：身份来自参考图时，要指向该图（用 `<imageN>`）；用文字描述五官会让模型重新生成并降低相似度。保留项描述得越具体越容易漂移。约束要用肯定式表达。 | [Edit 模板 JSON](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_image_edit.json) | 高 |
| F-COMFY-10 | 官方 Qwen-Image-2.1 T2I 模板自带的默认示例提示词以 "Absolutely no text, no typography, ... no watermark, no captions" 结尾，而同一模板注明 cfg=1 时负向提示不起作用。厂商示例不能当写法范本。 | [T2I 模板 JSON](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json) | 高 |
| F-COMFY-11 | GY/T 377—2023：网络视听节目平均响度应为 -15 LKFS 或 -24 LKFS（容差 ±2 LU），-15 LKFS 适用于车载、户外、公交地铁等嘈杂环境；最大真峰值不超过 -1 dBTP。客户 -16 LUFS 落在 -15±2 范围内（〔学院推断〕：LUFS 与 LKFS 同义）。 | [GY/T 377—2023 PDF](https://file.smejs.cn/group1/M00/05/0B/rBIAAWTsVOuAR79xAARAFqo4M3s952.pdf) | 高 |
| F-COMFY-12 | FFmpeg ebur128 文档：target 默认 -23 LUFS（EBU R128），并写明 "material published online may prefer a level of -16LUFS (e.g. for use with podcasts or video platforms)"。该参数只是可视化的相对零点，不做归一；归一要用 loudnorm（默认 I=-24、TP=-2）。 | [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html) | 高 |
| F-COMFY-13 | AES TD1008（经 Production Advice 解读）：语音和混合内容的分发响度建议为 -18 LUFS，音乐为 -16 LUFS；这些建议面向流媒体服务，不约束母带。 | [Production Advice TD1008](https://productionadvice.co.uk/td1008/) | 中（二手解读，未读 AES 原文） |
| F-COMFY-14 | Whisper 判静音跳过的条件是 no_speech_prob>0.6 且 avg_logprob 不高于 -1.0；avg_logprob 高于阈值时即使 no_speech_prob 高也不跳过。〔学院推断〕高置信度的套话式幻觉因此不会被默认阈值过滤。 | [whisper transcribe.py](https://github.com/openai/whisper/blob/main/whisper/transcribe.py) | 高（代码）／中（推断） |
| F-COMFY-15 | "字幕by索兰娅""请不吝点赞 订阅 转发 打赏支持明镜与点点""字幕由amara org社区提供""谢谢观看 下集再见""字幕提供者 李宗盛"都出现在 Whisper 喂纯噪声得到的 MIT 幻觉数据集中。 | [whisper-hallucinations 数据集](https://huggingface.co/datasets/sachaarbonel/whisper-hallucinations) | 高 |
| F-COMFY-16 | faster-whisper 的默认 VAD 只去除超过 2 秒的静音（min_silence_duration_ms=2000，threshold 0.5，speech_pad_ms 400）；批量转写默认开启 VAD。 | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 高 |
| F-COMFY-17 | Careless Whisper：约 1% 的转写含整句幻觉，其中 38% 含明确伤害；non-vocal 时长占比更长的说话人更易触发。BoH 后处理可降低 WER（ICASSP 2025）。 | [arXiv:2402.08021](https://arxiv.org/abs/2402.08021)、[arXiv:2501.11378](https://arxiv.org/abs/2501.11378) | 中（英文语料与失语症研究，能否外推到中文短剧未验证） |
| F-COMFY-18 | ComfyUI 的噪声由 `torch.manual_seed(seed)` 在 CPU 上为整批 latent 一次生成，初始噪声与 GPU 型号无关；但批内第 k 张不等于单独用 seed+k 生成，因此需要记录 seed 和 batch_index。整图能否逐位复现没有保证（`--deterministic` 帮助文字自述不保证）。 | [comfy/sample.py](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/sample.py)、[cli_args.py](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/cli_args.py) | 高 |
| F-COMFY-19 | FFmpeg 默认值：scdet 阈值 10，推荐 8–14；blackdetect d=2.0s、pic_th 0.98、pix_th 0.10；freezedetect 和 silencedetect 均为 -60dB、2s。PySceneDetect 默认值：detect-content 27、detect-adaptive 3.0、min-scene-len 0.6s。 | [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html)、[PySceneDetect CLI](https://www.scenedetect.com/docs/latest/cli.html) | 高 |
| F-COMFY-20 | PP-OCRv6（PaddleOCR 3.7.0，2026-06-11）单模型覆盖中、英、日及 46 种拉丁语系语言；medium 34.5M 相对 PP-OCRv5_server 检测 +4.6%、识别 +5.1%；许可 Apache-2.0。 | [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 高 |
| F-COMFY-21 | SenseVoiceSmall 输出 7 类情感标签和 8 类事件标签（含 BGM、Laughter、Cry），比 Whisper-Large 快 15 倍。官方权重在遵守 FunASR 模型许可的前提下可以商用，须署名。 | [SenseVoice](https://github.com/FunAudioLLM/SenseVoice) | 高 |
| F-COMFY-22 | Qwen-Image-2.1 的透明图要用固定包裹句：模型卡写 "This is an RGBA image with transparency. … The image has alpha channel and the background is transparent."，Comfy 模板写 "This is an RGBA format image with transparency"。两处官方措辞差一个词。 | [HF 模型卡](https://huggingface.co/Qwen/Qwen-Image-2.1)、[T2I 模板 JSON](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json) | 高 |

## 空白与未找到

1. **平台官方响度目标**：抖音、快手、视频号、TikTok、YouTube Shorts 的官方响度目标值（LUFS）都没找到官方文档。搜索结果只有第三方文章（多称约 -14，TikTok 另有 -13 或 -12~-10 的说法），因此没有收录。中国官方依据目前只有 GY/T 377—2023，而且本次拿到的 PDF 托管在第三方站点，没找到总局官网的原始下载链接。
2. **Whisper 中文幻觉的来源**：openai/whisper 官方仓库里没找到讨论"字幕by索兰娅"一类中文幻觉的 issue。这类串的证据只有 MIT 数据集（S-COMFY-16）和同行经验（S-COMFY-21）。研究员提到的 amical 列表、Speech-Translate 黑名单本次未打开，不采用。"明镜与点点"等频道片尾串的成因属于推断，没有官方说明。
3. **Qwen-Image-2.1 未查清的部分**：
   - 官方博客（qwen.ai/blog?id=qwen-image-2.1）没有打开。
   - 关于多视图设定板，README 只有一张"由三视图角色参考生成分镜"的示例图，没有写法说明。
   - 2:3 竖版人像，官方没有给出 cfg/steps 以外的参数建议。
   - LICENSE 中 "Materials" 定义为 Qwen 模型和文档，生成物（outputs）只在第 3b 条（用输出训练模型须署名）和诉讼条款中出现。非商用限制是否及于生成物，条款没有写明，需要法务确认。
4. **OCR**：tesseract chi_sim 的最新文档没有核实。PaddleOCR/RapidOCR 对 AI"伪汉字"纹理的召回率没有公开评测。研究员提到的 EasyOCR 用法未核实，不采用。
5. **坏帧阈值**：没找到公开的、用 ffmpeg/VMAF 判断 AI 生成视频"坏帧"的标准阈值。学院里的 SSIM/YDIF 用法属于工程建议，需要用客户样片校准。研究员自述曾用 ffmpeg 6.1.1 和合成片段实测过命令，本次未复核。
6. **采样器对比**：客户的 H3 管线用 euler 采样器，官方模板用 res_multistep，两者的差异没有找到对比评测。
7. **许可证缺口**：infometa/workbuddyskills 没有声明许可证（根目录 LICENSE 返回 404），只能借鉴思路。其数据为单一项目经验，学院需要复测后才能写进判据。
8. **核实说明**：21 条全部用 WebFetch 打开在线页面。GitHub、HF、docs.comfy.org 的关键原文另外下载原始文件逐字 grep，包括模板 JSON、LICENSE、源码、数据集 CSV、Comfy 文档的 .md 版本和 GY/T 377 PDF。研究员原稿中有以下改动：
   - **删除了无法在所给 URL 核实的内容**：GY/T 282/379 对比、TD1008 "-20 至 -16" 早期范围、"Export (API)" 说法、EasyOCR、amical 列表。
   - **纠正了过度表述**：faster-whisper 短片段阈值改标为推断；"同 seed 跨 GPU 可复现"改为只说初始噪声与 GPU 无关；infometa 的响度数字原文明确"不当定律"。
