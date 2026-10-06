# 开源 AI 短剧/漫剧/影片 agent 流水线

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：16 ｜ 核实方式：逐条 WebFetch 打开核对。GitHub 仓库另做浅克隆，对照文件原文核对（xixihhhh/ai-short-drama-skill、A-cat-with-carrots/OnlyShot、HKUDS/ViMax、chatfire-AI/huobao-drama、wanglongxiao/seedance-drama-maker、vangongwanxiaowan/screen-creative-skills）。zenstory-ai/drama-skills 对照本地克隆核对（HEAD `c2426e0`，2026-10-03），并用 WebFetch 打开在线仓库页。论文逐篇打开 arXiv 摘要页，关键数字另开 HTML 全文核对

## 一句话结论

本主题能给学院的有三类东西。第一类是两套可直接装进 agent 的短剧 skill：Dramake 提供「生成段/剪辑节拍」两级时间单位、四道验收门、重试纪律和尾帧链上限；drama-skills 提供「文件即事实」的一致性方法、MiniMax H3 提示词方言，以及一份 H3/Seedance/Wan 的小样本行为观察。第二类是多 agent 影片框架和多镜头评测基准（FilmAgent、MovieAgent、MAViS、ViMax、MSVBench、MSAVBench）给出的分层拆解、迭代上限和评测分层；第三类是自动管线的反例（huobao-drama 未见审查环节，seedance-drama-maker 用 VLM 分数自动放行）。缺口：没有任何开源项目针对委托方的 ComfyUI 本地 H3 Director + Qwen-Image 栈（T-1、T-2），没有处理 124 帧下限和 cfg=1 下负面提示无效的问题；各项目的实测数据都是作者自报的小样本，没有独立复现；平台留存数据只有 OnlyShot 的自述，没有可核对的出处。

## 条目

### S-PIPE-01 · Dramake（xixihhhh/ai-short-drama-skill）AI 短剧 Agent Skill
- **URL**：https://github.com/xixihhhh/ai-short-drama-skill
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：只有一个 `dramake` skill（SKILL.md 元数据 version 0.6.0，最后提交 2026-08-30，GitHub 页 44★），面向 Codex、Claude Code、WorkBuddy。README 列出它内置的十二类能力：故事医生、视觉导演、连续性、空间调度、系列记忆、身份画风锁、声音导演、模型路由、预算、任务编排、QA 修复、剪辑发布。时间分两级。generation_block 是一次模型请求，通常 8–30 秒，含 3–6 个内部节拍；edit_beat 是 2–8 秒、让观众获得一项新内容的单位。验收设四道门：剧情、身份/画风、物理/连续性、声音。任何 P0 失败都会阻止素材进入正式状态。冷观众检查不给梗概，只问四件事：主角想要什么、什么阻止了他、发生了什么变化、结局为什么会发生。处置分五种；换种子最多 2–3 次，每次重试只改一个变量；尾帧链默认深度 2、硬上限 3。参考权威矩阵为每个控制维度只指定一个胜出素材。接触动作按「接近→接触→施力→响应→结果」写。仓库附有作者 2026-08-24/25 的匿名实测记录。
- **对本学院有什么用**：agent 规划 H3 镜头时按「生成段 + 剪辑节拍」两级排时长；每段通过四道门和冷观众问答后，下一段才能引用它的状态。
- **落点模块**：10-theory、20-craft、40-memory、50-rubrics、60-casebook、70-playbooks

### S-PIPE-02 · drama-skills（zenstory-ai）11 个短剧/漫剧 Claude Code·Codex 技能
- **URL**：https://github.com/zenstory-ai/drama-skills
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：VERSION 为 0.8.1，最后提交 2026-10-03，GitHub 页 2.5k★，共 11 个 skill。流程是：原著分析→分集剧本→视觉设定→图片提示词与分镜→视频提示词→确认后生产→剪辑成片→审查。每集只维护五份 Markdown（剧本、视觉设定、分镜、图片提示词、视频提示词）作为创作事实，剪成片时再加一份剪辑单。一致性靠写进文件、能用脚本核对的事实：连续性锁短语、REF-/PLAN- 参考槽位、关键帧写明依据了哪些条目，由 `creator_markdown_check.py` 逐条报错。H3 方言规则：Base、首帧、首尾帧三种模式用三段结构，full-reference 用六段；`<Picture N>` 按挂图顺序编号；首/尾帧模式与 full-reference 模式互斥；`duration` 为 4–15 的整数秒。规则分四级：structural_invariant、reviewed_invariant、craft_default、taste_option。审查优先交给没参与创作的 reviewer；没有授权观察时只能写「文字风险」，不得声称看见了漂移。字幕逐字取自剧本，语音转写只用来定位。
- **对本学院有什么用**：可直接作为学院 H3 方言、规则分级和「文件事实可核对」一致性方法的母本（逐文件评估见同目录 zenstory-drama-skills.md 的 S-ZEN 系列）。agent 写视频提示词前，先登记每张参考图的用途和控制范围，再按用途组合决定 H3 模式。
- **落点模块**：20-craft、30-taste、40-memory、50-rubrics、70-playbooks

### S-PIPE-03 · drama-skills 模型行为观察摘要（MiniMax H3 / Seedance / Wan 3.0 小样本）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md
- **类型**：report
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：2026-09-08 至 09-28 的探索性观察，表格共 52 行，每行写明样本、结果和能支持的判断。文件自己声明：盲评的「判断者为同一个模型，不是独立人评」，本表也不是可重放的回归夹具。H3 部分：自然语速约 4.1 字/秒；对白镜比计划多出约 1.5–2.5 秒。写「Fixed camera.」的 4 次都没有位移，不写机位句的 28 次中有 4 次推拉或平移。动作终点写成接触点时 4/4 停在杯沿，写厘米数不起控制作用。用真实尾帧续接时开场 NCC 为 0.91–0.99（3/3），但另一轮复测是 2/3 在 0.94–0.97、1 次只有 0.27。9 秒三切时每切挂关键帧，切点偏差在约 0.12 秒以内。口型会落到画里最显眼的正脸上。H3 反应镜用「情绪词 + 两处可见泄露 + 1.5 秒内落定」盲评最好，Seedance 2.5 却是逐段可见链最好。掌掴宜一镜写全；推搡拆成接触前后两镜时推得动，但跨切连续性最差。
- **对本学院有什么用**：agent 写 H3 提示词时默认写机位句、接触式终点和说话人绑定，对白镜预留开口延迟；这些结论写进记忆时只能标「待复测假设」，委托方实测后才能升级。
- **落点模块**：20-craft、40-memory、50-rubrics、60-casebook

### S-PIPE-04 · OnlyShot（A-cat-with-carrots）AI 短剧工业流水线 Claude Skill
- **URL**：https://github.com/A-cat-with-carrots/OnlyShot
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：v0.6.1（最后提交 2026-05-16，GitHub 页 305★）。Phase 1 是创作：市场情报扫描、IP 简报、故事架构、设定圣经、节奏地图、逐集脚本和 ref 库。Phase 1.5 出分镜图，每格 1–4 张候选，3 积分/张，README 称修改成本是视频（55 积分/段）的 1/18。Phase 2 用 dreamina CLI 调 Seedance 2.0 Fast 出 9:16 视频，模式分配为 image2video 80%、首尾帧 10%、多帧 5%、多模态 5%，之后在剪映拼接。单集 180–195 秒、36 格，每格 4–10 秒变奏。每集按「红果必爆 7 招」时间轴排：0–3s 对抗开场、25–32s 爆破、55–65s 首爽、85–95s 反转、115–125s 二爽、145–160s 钩子、结尾倒计时。ref 用 6 段身份块，分镜用 8 段 SOP，「视觉指纹」在分镜阶段停用。另有 17 条失败模式（多为 CLI、编码等基础设施问题）、6 维自评、套路黑名单和平台审核扫描。平台数据引自 woshipm 等二手来源。
- **对本学院有什么用**：可借用三条做法：关键帧先行以降低返工成本；每集写爽点时间轴；板图用中性光、关键帧用戏剧光，分开写。时间轴数字须另行核实后才能当判据。
- **落点模块**：20-craft、30-taste、50-rubrics、70-playbooks、90-curriculum

### S-PIPE-05 · ViMax: Agentic Video Generation（HKUDS）
- **URL**：https://github.com/HKUDS/ViMax
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：代码 MIT；论文 arXiv 2606.07649 为 CC BY 4.0
- **核实**：✅ 已打开核实
- **摘录**：港大数据智能实验室的 agentic 视频框架。v1.2.0 发布于 2026-07-20，最后提交 2026-09-30，GitHub 页 12.5k★。支持 Idea2Video、Script2Video、Novel2Video、AutoCameo 四种模式。agent 包括 screenwriter、novel_compressor、storyboard_artist、camera_image_generator、best_image_selector 等。视频后端里 Seedance 2.0 Fast（2026-07-17 加入）和 Veo 已支持；MiniMax H3 只在路线图上，标记与已完成项不同。机位树规则：父机位的内容要包含子机位，优先远→中→近，除非万不得已不许远景直跳特写，只有一个无父机位，首个机位为根。选图提示词按三维择优：角色一致（性别、年龄、五官、体型、发型等）、空间一致（左右站位不得与参考图反转）、描述准确。默认候选数为 2。论文提出层级叙事引擎（用 RAG 保持全局故事连贯）和依赖感知的视觉一致性机制。
- **对本学院有什么用**：agent 先出建立镜关键帧，再从它派生近景关键帧（机位树）；拿 ViMax 的选图提示词给 Qwen 多 seed 结果做预筛，预筛结果不当终审。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-PIPE-06 · FilmAgent: A Multi-Agent Framework for End-to-End Film Automation in Virtual 3D Spaces
- **URL**：https://arxiv.org/abs/2501.12909
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：论文（arXiv）；配套仓库 HITsz-TMG/FilmAgent 现显示为 VideoClaw，MIT
- **核实**：✅ 已打开核实
- **摘录**：哈工大（深圳）为主、清华一位作者参与，2025-01-22 提交。导演、编剧、演员、摄影 agent 在 3D 虚拟片场协作。编剧阶段用 Critique-Correct-Verify：Action agent 出稿，Critique agent 写批评，Action agent 修订，再由 Critique agent 核验。摄影阶段用 Debate-Judge：两名摄影各自提案、互相辩论，导演裁决。多 agent 协作算法最多迭代 3 轮。用 15 个故事做人评，均分 3.98/5，其中剧情连贯 3.53、镜头恰当 3.53、人设一致 4.44。对照组：Solo 3.04、GPT-4o CoT 2.63、o1 CoT 3.30。修订后的剧本 66.7% 被偏好。动作集只有 21 种。论文把引入多模态 LLM 列为改进反馈的方向，也就是说当前没有视觉核验。现仓库 VideoClaw 推荐默认用首帧生视频，理由是「完成过多次测试，最稳定」。
- **对本学院有什么用**：agent 的剧本和镜头选择可采用「批评-修订-核验，最多 3 轮」和「双提案辩论 + 裁判」；同时明确这类纯文本回路不能代替看片验收。
- **落点模块**：10-theory、50-rubrics、70-playbooks

### S-PIPE-07 · MovieAgent: Automated Movie Generation via Multi-Agent CoT Planning（showlab）
- **URL**：https://arxiv.org/abs/2503.07314
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：论文（arXiv）；代码 showlab/MovieAgent 仓库页未见 LICENSE 文件
- **核实**：✅ 已打开核实
- **摘录**：Weijia Wu、Zeyu Zhu、Mike Zheng Shou（NUS Show Lab），2025-03-10 提交。输入是剧本和角色库。分层规划由三个 agent 完成：Director Agent 负责高层叙事结构，Scene Plan Agent 定场景、关键要素和场景边界，Shot Plan Agent 定镜头级情节、摄影参数和视觉动态。内部 CoT 分五步，从叙事结构分析到技术性电影规划（运镜、构图、站位、对白）。论文实验用 StoryDiffusion 出关键帧、CogVideoX 出视频，ROICtrl 做角色一致，Hallo2 做说话头。仓库 model zoo 列的是 ROICtrl 出图、SVD/HunyuanVideo_I2V 出视频。人评五维中角色一致 4.04、剧本忠实 3.92。作者自认的失败：脸部严重畸变；小目标身份不一致；边走边说这类复杂交互失败；场景转场突兀；解剖比例和物理不对。
- **对本学院有什么用**：为 agent 的「剧本→场景→镜头」三级拆解，以及失败模式清单（脸、小目标身份、边走边说、转场、解剖）提供命名参照。
- **落点模块**：10-theory、50-rubrics、90-curriculum

### S-PIPE-08 · MAViS: A Multi-Agent Framework for Long-Sequence Video Storytelling
- **URL**：https://arxiv.org/abs/2508.08487
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：论文（arXiv）；代码许可未核
- **核实**：✅ 已打开核实
- **摘录**：Qian Wang、Ziqi Huang、Ruoxi Jia、Paul Debevec、Ning Yu。v1 发布于 2025-08-11，当前为 v5（2026-01-24）。流程分剧本、镜头设计、角色建模、关键帧、视频动画、音频六个阶段，统一遵循 3E 原则：Explore 生成、Examine 审查、Enhance 修订。剧本规则针对生成工具的局限：每镜只放一个简单动作；相邻镜头避免用同一背景，中间插不同角色的特写、局部或环境细节；不写手机屏幕文字、物体小图案这类细节。规则依据的实测：相邻同背景镜头的背景一致性 78.42，单镜 95.88；100 对空间相连的镜头里只有 26 对背景一致。I2V 评审每个候选均匀抽 8 帧。迭代上限：剧本 4、镜头设计 5、T2I 2、I2V 1。60 人用户研究中平均得票率 69.44%。
- **对本学院有什么用**：agent 写分镜时坚持单镜单动作，细字留到后期叠加，每个阶段设迭代上限；同一地点逐镜独立生成的镜头不硬接，改为共享父机位关键帧。
- **落点模块**：10-theory、20-craft、50-rubrics

### S-PIPE-09 · VideoGen-of-Thought (VGoT): Step-by-step multi-shot video generation
- **URL**：https://arxiv.org/abs/2412.02259
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：论文（arXiv）；代码 github.com/DuNGEOnmassster/VideoGen-of-Thought 为 BSD-3-Clause
- **核实**：✅ 已打开核实
- **摘录**：一句话生成多镜头视频的免训练框架。v1 发布于 2024-12-03，v3 于 2025-10-02；代码仓库 README 标注「NeurIPS 2025 NextVid Workshop Oral」，属于 workshop，不是主会。三个问题各给一个机制。叙事碎片化用动态故事线建模：先写镜头草稿，再展开到五个域（角色动态、背景连续、关系演变、运镜、HDR 光照），并做自校验。视觉不一致用身份保持肖像 token 跨镜传播，允许按剧情改动部分特征。转场伪影用相邻 latent 过渡，在切点做边界感知重置。报告的结果：镜内脸部一致提升 20.4%，风格一致提升 17.4%，人工调整减少 10 倍。
- **对本学院有什么用**：agent 的镜头描述显式写五域连续性字段（角色动态、背景连续、关系演变、运镜、光照）。模型级机制只作理论参考。
- **落点模块**：10-theory、20-craft

### S-PIPE-10 · Anim-Director: A Large Multimodal Model Powered Agent for Controllable Animation Video Generation
- **URL**：https://arxiv.org/abs/2408.09787
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：论文（arXiv）；代码 github.com/HITsz-TMG/Anim-Director 仓库页未见 LICENSE 文件
- **核实**：✅ 已打开核实
- **摘录**：SIGGRAPH Asia 2024，作者 Yunxin Li、Haoyuan Shi、Baotian Hu、Min Zhang 等（哈工大深圳）。以大多模态模型（LMM）为核心的动画 agent，分三阶段。第一阶段从简短叙述生成故事线和导演脚本，内容包括角色档案、内外景描述和逐场景说明。第二阶段由 LMM 调用图像工具生成角色图和场景图，用「场景描述 + 角色/场景图」的视觉-语言提示保持跨场景一致。第三阶段以场景图为基础，由 LMM 写提示词驱动动画生成，并评估视觉质量、从多个候选中选最优。同一仓库还收录后续工作 AniMaker（SIGGRAPH Asia 2025 有条件接收）。
- **对本学院有什么用**：给漫剧形态提供结构范例：导演脚本里每场都写出场人物清单，并绑定对应的参考图。
- **落点模块**：10-theory、20-craft

### S-PIPE-11 · MSAVBench: Towards Comprehensive and Reliable Evaluation of Multi-Shot Audio-Video Generation
- **URL**：https://www.alphaxiv.org/abs/2605.20183
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：arXiv 页标注 non-exclusive distribution license
- **核实**：✅ 已打开核实
- **摘录**：arXiv 原页（https://arxiv.org/abs/2605.20183）v1 为 2026-05-19，v4 为 2026-06-24；作者来自复旦、港大、阿里通义、浙大、北大等。这是多镜头音视频生成基准：286 个 prompt、2,198 个镜头，每条最多 15 镜，覆盖非写实和反事实场景。20 项指标分四层：Global（叙事连贯、音画同步）、Cross-Shot（角色一致、风格延续）、Intra-Shot（文字渲染、运镜遵循）、Reference-Conditioned（参考身份保持）。评测框架是自适应混合式，包括带自纠的 VLM 镜头切分、专家模型、逐实例 rubric 和工具取证，与人评的 Spearman 相关为 0.915。评测了 19 个模型，结论：现有系统像「像素渲染器」而不是讲故事者，导演级控制和细粒度音画同步最弱；后期配音会带来语音失真和口型不同步；模块化或 agentic 流水线是缩小开源与闭源差距的可行方向。
- **对本学院有什么用**：学院 rubric 按全局、跨镜、镜内、参考四层组织，「运镜遵循」和「音画同步」各单列评分项。
- **落点模块**：10-theory、50-rubrics

### S-PIPE-12 · MSVBench: Towards Human-Level Evaluation of Multi-Shot Video Generation
- **URL**：https://arxiv.org/abs/2602.23969
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：CC BY 4.0（arXiv 页标注）
- **核实**：✅ 已打开核实
- **摘录**：2026-02-27 提交。作者包括 Haoyuan Shi、Yunxin Li、Zhenran Xu、Longyue Wang、Baotian Hu、Min Zhang 等，与 Anim-Director、FilmAgent 作者有重叠。基准带层级剧本和参考图，评测为混合式：大多模态模型负责高层语义推理，领域专家模型负责细粒度感知。共评测 20 种视频生成方法，与人评的 Spearman 相关为 0.944。结论：现有方法视觉保真度高，但主要是「视觉插值器，而非真正的世界模型」。论文还报告，用基准的推理轨迹微调轻量模型，表现可接近商用系统。
- **对本学院有什么用**：作为理论依据：单靠 VLM 打分不可靠，agent 的自动 QA 要同时用 LMM 做语义判断、用专家模型做测量，并用人评校准。
- **落点模块**：10-theory、50-rubrics

### S-PIPE-13 · CHIEF: Creator-Driven Recurrent Video Generation with Agentic Feedback Loops
- **URL**：https://arxiv.org/abs/2606.18591
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：CC BY 4.0（arXiv 页标注）
- **核实**：✅ 已打开核实
- **摘录**：全题为 Bridging Creative Intent and Visual Quality: Creator-Driven Recurrent Video Generation with Agentic Feedback Loops，2026-06-17 提交，ICML 2026 Workshop on Human-AI Co-Creativity。框架让 persona 条件化的多模态 LLM 观看生成视频，从不同观众视角写主观批评；每轮修订方向由创作者决定，由专门的 refiner agent 执行。测试对象是没有拍片经验的高中生和大学生，产出从 1 分钟短片到 10 分钟、情节复杂的短片。摘要没有给出量化指标，也没有自动评分与人评的对比。
- **对本学院有什么用**：agent 可以用多个 persona 观众模拟做冷观众预演，但预演不能代替真人冷观众，方向仍由人类创意负责人拍板。
- **落点模块**：10-theory、50-rubrics、70-playbooks

### S-PIPE-14 · huobao-drama（火宝短剧，chatfire-AI）
- **URL**：https://github.com/chatfire-AI/huobao-drama
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：CC BY-NC-SA 4.0（禁止商用）
- **核实**：✅ 已打开核实
- **摘录**：AI 短剧自动化生产平台，GitHub 页 15.8k★、2.9k fork，git 标签最新为 v4.0.8（2026-10-06）。技术栈是 TypeScript 全栈：前端 Nuxt 3 + Vue 3，后端 Hono + Drizzle + Mastra Agents + SQLite，另有 Electron 桌面版。内置 4 个 agent：script_rewriter、extractor、storyboard_breaker、prompt_generator。流程是：粘贴原文→AI 改写分集剧本并标注场景与角色→提取角色/场景/道具并生成参考图→拆分镜、生成视频提示词、批量出片（失败任务可一键重试）→勾选镜头后用 FFmpeg 拼成整集。提示词里写 `@角色名` 会自动映射到参考图。视频后端支持 Seedance 2.0、MiniMax H3、Wan 3.0。拼接前检查镜头文件是否存在。README 描述的流程里没有质量审查环节，只有预览、改提示词和失败重试。
- **对本学院有什么用**：作为「一站式全自动、没有审查」的对照样本，提醒 agent 批量出片不等于成片能看；许可禁止商用，只能借鉴思路，不能复用代码或文本。
- **落点模块**：10-theory、60-casebook

### S-PIPE-15 · Seedance Drama Maker（wanglongxiao）多 agent 短剧管线
- **URL**：https://github.com/wanglongxiao/seedance-drama-maker
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：FastAPI + WebSocket 的多 agent 短剧管线（GitHub 页 16★，最后提交 2026-10-05）。README 列出的模型有 DeepSeek-V4.1-Flash、Seed-2.1-turbo、SeeDream-5.0-flash、SeeDance-2.5、Seed-Speech。agents 目录下有 script、image、video、video_review、merge、main 六个 agent。VideoReviewAgent 用 Seed-2.1-turbo 按三维审核：人物一致性、物理规律、与分镜语义一致；默认 60 分及格，max_retries 为 2。自动模式下审核失败就自动重试，到上限后自动选最高分的结果继续流程。单镜 5–30 秒；description 按秒段写，5–9 秒至少 2 段，10–18 秒至少 3 段，19–30 秒至少 4 段。相邻分镜靠动作、视线、道具、构图匹配，或声桥、自然遮挡、光影呼应来衔接。合成前统一编码参数，并校验分镜编号和内容指纹。
- **对本学院有什么用**：是「VLM 自动评分闸门 + 到上限自动放行」的典型反例；agent 只把自动分数当预筛和排序，不当放行依据。
- **落点模块**：50-rubrics、60-casebook

### S-PIPE-16 · screen-creative-skills（vangongwanxiaowan）影视剧本创作与评估 Claude Code Skills
- **URL**：https://github.com/vangongwanxiaowan/screen-creative-skills
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：宫凡维护的 31 个剧本类 skill（README 版本 2.1.0，2026-01-11；最后提交 2026-05-26；GitHub 页 443★），分故事分析、人物分析、创作、评估、小说筛选等类。drama-planner 讲黄金三秒钩子、「期待-压抑-爆发」三幕式结构、人设容器和付费卡点。drama-creator 用「情绪弹簧」写 1–2 分钟的单集：每集要么压弹簧，要么放弹簧。drama-evaluator 的评估标准分四档：S 级 ≥8.5、A 级 8.0–8.4、B 级 7.5–7.9、C 级 ≤7.4。节奏递进的满分标准是：每 1–2 集一个小爽点，每 3–5 集一个中爽点，大结局前一个大爽点。人物维度看反差感、欲望单一明确、反派功能化。只覆盖剧本层，不涉及画面生成。
- **对本学院有什么用**：为 agent 的季级爽点节奏和剧本立项评分提供可改写的档位和递进规则；这些档位是作者设定，没有数据校准。
- **落点模块**：30-taste、50-rubrics、90-curriculum

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-PIPE-01 | Dramake 作者匿名实测（2026-08-24/25）：36 个约 5 秒的片段做视觉/物理评估，结果是 12 个阻断、8 个严重、3 个轻微、13 个单段可接受，严重或阻断合计 20/36 = 55.6%。即使单段可接受，没有设计进入/退出动作、轴线和有动机的接缝，仍然拼不成连贯影片。 | [tested-observations.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/benchmarks/tested-observations.md) | 中 |
| F-PIPE-02 | Dramake 实测：20 个原生音频短段的综合响度在 −25.83 至 −16.93 LUFS 之间，相差 8.9 LU；部分 0.5 秒边界的 RMS 变化超过 30 dB，曾观察到约 40 dB。作者的处理：保留有用的原生对白和拟音，后期重建连续环境、音乐结构、响度和 J/L 声音桥。 | [tested-observations.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/benchmarks/tested-observations.md) | 中 |
| F-PIPE-03 | Dramake 记录了一版技术上明显改善的粗剪，它仍没通过冷观众测试：因果、主角作用、铺垫和结局都不清楚。因此剧情可懂性被设为独立的 P0 门禁。冷观众检查的问法：不给梗概，问主角想要什么、什么阻止了他、发生了什么变化、结局为什么会发生；任一核心答案错误即为 P0。 | [tested-observations.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/benchmarks/tested-observations.md)；[qa-and-repair.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/skills/dramake/references/qa-and-repair.md) | 中 |
| F-PIPE-04 | Dramake 的切镜预算：每个内部镜头通常至少要约 4–6 秒，才能完成动作、反应和退出。10 秒段优先 2 镜，12–15 秒段 2–3 镜；每镜只放一个主要动作、一个主要运镜、一个声音任务。镜头数超出时长承载能力时，模型会压缩、跳过或在动作中途乱切；解决办法是减镜或加长，不是堆描述。 | [directing-camera-and-pacing.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/skills/dramake/references/directing-camera-and-pacing.md) | 中 |
| F-PIPE-05 | Dramake 的修复纪律：换种子重试最多 2–3 次，之后按系统性问题处理；每次重试只改一个变量；第一条请求前写明最大候选/重试数和「足够好」的标准；花掉一半预算仍无进展，就切换模式、拆镜、降低复杂度或换方案。用上一段输出作下一段参考时，链深默认 2、硬上限 3，到上限、跨场景或出现漂移就从母版重新锚定。 | [qa-and-repair.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/skills/dramake/references/qa-and-repair.md)；[continuity-and-transitions.md](https://github.com/xixihhhh/ai-short-drama-skill/blob/main/skills/dramake/references/continuity-and-transitions.md) | 高 |
| F-PIPE-06 | drama-skills 观察：H3 中文对白用同一镜头测了 20 次（7–108 字、5–13 秒），自然语速约 4.1 字/秒，较密的输入会赶词或截断；50 字塞进 5 秒仍能说完，因此不能据此划截断阈值。分镜 A/B 实跑中，对白镜比计划多出约 1.5–2.5 秒，多出的是开口前的延迟加说完台词的时间。〔学院推断〕它与委托方 T-2 的 7.5 字/秒可能分别是自然语速和容量上限，计数口径未核对，待复测。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-PIPE-07 | drama-skills 观察：H3 提示词写「Fixed camera.」的 4 次和写完整锁定描述的 4 次都没有位移；不写机位句的 28 次中有 4 次推拉或平移。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-PIPE-08 | drama-skills 观察：用上一段真实尾帧作参考续接时，H3 开场与该尾帧的 NCC 为 0.91–0.99（3/3）；只给角色和地点图独立生成时为 0.01–0.41（3/3），景别和站位都会跳。另一轮复测中，H3 尾帧续接 3 次里 2 次为 0.94–0.97、1 次为 0.27，说明尾帧续接也不是每次都成立。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-PIPE-09 | drama-skills 观察：H3 生成 9 秒三切，要求在 3.0/6.0 秒切。每切挂一张关键帧并加对齐句时，切点落在 2.88–3.04 / 6.00–6.04 秒，各切与关键帧的 NCC 为 0.88/0.89/0.95；只挂首张关键帧时，切点为 2.92–3.88 / 5.88–6.21 秒，NCC 为 0.88/0.40/0.33，还多出过一次切。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-PIPE-10 | drama-skills 观察：H3 的声音没选错，但口型会落到画里最显眼的正脸上。不说话者在台词期间仍正对镜头时，按现行写法 3 次中有 2 次口型落错；写明说话人音色与在画位置，并写明不说话者嘴唇闭合后，3/3 正确。不说话者出画或背对镜头时，12/12 正确。首帧模式下画中人自己配旁白时，文字约束不可靠。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-PIPE-11 | drama-skills 观察：H3 双人接触镜头只写一个动词时最差（物理 2.2/5、戏剧 2.2/5）；掌掴一镜写全「接近—接触—施力—结果」最好（5/4/4）。推搡拆成「到接触为止」和「从接触后关键帧起」两镜时，只有这种写法把人推退一步，但跨切连续性最差（2.7/5）。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-PIPE-12 | drama-skills 实跑记录：语音转写把「诸君，且听龙吟」听成「朱军且听龙银」，所以字幕必须逐字取自剧本，转写只用来定位。同一记录里，单遍 loudnorm 只到 −12.33 LUFS（偏离目标 3.7 dB），两遍后才到 −15.79。 | [real-outputs.md](https://github.com/zenstory-ai/drama-skills/blob/main/docs/real-outputs.md) | 高 |
| F-PIPE-13 | drama-skills 的节奏档案起点（创作者接受后才做算术核对）：首钩 ≤5 秒（一组实测中 5 部有 3 部在前 5 秒给出第一个钩子）；情绪触点间隔 ≤30 秒；每集至少 1 次有对手参与的反转；集尾停在峰值；真人短剧目标平均镜长 2.5 秒、近景类占比 ≥0.45（来自一组真人短剧实测）。VO 占比 ≤0.3 和漫剧列的多数数值标为「未实测」。 | [episode-design.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-develop/references/episode-design.md) | 中 |
| F-PIPE-14 | FilmAgent 人评（15 个故事）：多 agent 协作版均分 3.98/5，单 agent 版 3.04，GPT-4o CoT 2.63，o1 CoT 3.30。协作算法最多迭代 3 轮；Critique-Correct-Verify 修订后的剧本 66.7% 被偏好。论文把多模态 LLM 列为改进方向，当前流程没有视觉核验。 | [arXiv 2501.12909](https://arxiv.org/abs/2501.12909) | 高 |
| F-PIPE-15 | MAViS 实测：相邻两镜用同一背景时，背景一致性为 78.42，单镜为 95.88；100 对空间相连的镜头中只有 26 对一致。论文据此规定每镜只放一个简单动作、避开细小文字等元素。I2V 评审每个候选均匀抽 8 帧；迭代上限为剧本 4、镜头 5、T2I 2、I2V 1。 | [arXiv 2508.08487](https://arxiv.org/abs/2508.08487) | 高 |
| F-PIPE-16 | MSVBench：混合评测（LMM 语义推理 + 领域专家模型）与人评的 Spearman 相关为 0.944，评测了 20 种方法；结论是现有多镜头视频方法主要是「视觉插值器，而非真正的世界模型」。 | [arXiv 2602.23969](https://arxiv.org/abs/2602.23969) | 高 |
| F-PIPE-17 | MSAVBench：四层 20 项指标，286 个 prompt、2,198 个镜头，评测 19 个模型，与人评的 Spearman 相关为 0.915。现有系统在导演级控制和细粒度音画同步上最弱；后期配音会带来语音失真和口型不同步；模块化或 agentic 流水线是可行方向。 | [alphaXiv 2605.20183](https://www.alphaxiv.org/abs/2605.20183) | 高 |
| F-PIPE-18 | ViMax 机位树规则：父机位要尽量包含子机位的内容（例如中景双人包含过肩反打）；优先按远→中→近传递，除非万不得已不许远景直跳特写；首个机位必须为根。选图评判要求左右站位不得与参考图反转。 | [HKUDS/ViMax](https://github.com/HKUDS/ViMax) | 高 |
| F-PIPE-19 | OnlyShot README：分镜图 3 积分/张，视频 55 积分/段，作者称修改成本是视频的 1/18，所以先确认构图再出视频。视频模式分配为 image2video 80%、首尾帧 10%、多帧 5%、多模态 5%。积分对应即梦当时的计费。 | [A-cat-with-carrots/OnlyShot](https://github.com/A-cat-with-carrots/OnlyShot) | 中 |
| F-PIPE-20 | OnlyShot 的「红果必爆 7 招」时间轴（0–3s 对抗开场、25–32s 爆破、55–65s 首爽、85–95s 反转、115–125s 二爽、145–160s 钩子、结尾倒计时），作者称依据是「woshipm 业界硬数据 + 红果 TOP100 EP01 拆解」。其内置数据表里有「完播率 -172%」这类不可能的数值，未经独立核实，不能直接当判据。 | [A-cat-with-carrots/OnlyShot](https://github.com/A-cat-with-carrots/OnlyShot) | 低 |
| F-PIPE-21 | seedance-drama-maker 的 VideoReviewAgent 用 VLM 按三维打分，默认 60 分及格，max_retries = 2；自动模式下到上限后自动选最高分结果继续。〔学院推断〕这和委托方 F1「自验证循环」同构：分数闸门最终总会放行。 | [wanglongxiao/seedance-drama-maker](https://github.com/wanglongxiao/seedance-drama-maker) | 高 |
| F-PIPE-22 | MIT Technology Review（2026-05-15，Caiwei Chen）：引 DataEye 数据，2026 年 1 月平均每天上线 470 部 AI 短剧。另引 FlexTV 副总裁 Tang Tang 的说法：AI 可把成本降低 80–90%，周期从 3–4 个月缩到不到 1 个月，团队可缩到约 10 人。 | [MIT Technology Review](https://www.technologyreview.com/2026/05/15/1137326/chinese-short-dramas-ai/) | 中 |
| F-PIPE-23 | huobao-drama（15.8k★，支持 Seedance 2.0 / MiniMax H3 / Wan 3.0）采用 CC BY-NC-SA 4.0，禁止商用；学院只能借鉴思路，不能复用代码或文本。 | [chatfire-AI/huobao-drama](https://github.com/chatfire-AI/huobao-drama) | 高 |
| F-PIPE-24 | MovieAgent 作者自认的失败：脸部严重畸变；小目标身份不一致；边走边说这类复杂交互失败；场景转场突兀；解剖比例和物理不对。 | [arXiv 2503.07314](https://arxiv.org/abs/2503.07314) | 高 |

## 空白与未找到

1. **客户线索「ai-manga-drama / neta make-image·make-video·merge-video」没对上**。talesofai/neta-skills 会跳转到 netaart/neta-skills（MIT），里面有 `make_image`、`make_video` 命令，但仓库页没有 merge-video 或 manga-drama。freestylefly/canghe-skills（MIT）里有 canghe-manga-drama，描述为「基于 Seedance、以角色图为底自动生成分镜脚本的漫剧生成器」，内置开场、动作、情绪、互动、结尾几类场景；研究员说的「单图 → 5 模板 × 5 秒」在仓库页上没有核实到。这条线索可能指私有或已改名的项目，需要向委托方要原链接。
2. **实测都是作者自报**。Dramake 是作者匿名自报的本地实验，没有媒体佐证，也没有独立复现。drama-skills 的观察样本是每格 2–20 次，盲评由同一个模型完成，不是独立人评。两者都只能当待复测假设。
3. **没有项目针对委托方栈**（T-1 Qwen-Image 2.1、T-2 ComfyUI 本地 H3 Director）。huobao-drama 通过 API 调 H3；ViMax 的 H3 支持还在路线图上。没有项目处理「低于 124 帧动作崩坏」这条下限，也没有项目处理 cfg=1 时负面提示无效的问题。
4. **平台留存数据没有可核对的来源**。OnlyShot 的 7 招时间轴和红果节奏数据引自 woshipm 等二手材料，没找到原始留存数据；其表内还有不可能的数值（F-PIPE-20）。
5. **冷观众测试缺真人协议**。只找到问答式协议（Dramake）和 persona LLM 模拟（CHIEF），没有带真人样本量和留存对照的公开协议。
6. **打斗/动作编排**：除 Dramake 的物理事件合同、冲击镜头结构和 drama-skills 的掌掴/推搡观察外，没找到专门的开源 skill。
7. **许可未核**：MAViS 代码仓库地址与许可。MovieAgent 和 Anim-Director 的仓库页未见 LICENSE 文件，按未授权处理。
8. **没深读**：huobao-drama 后端 agent 提示词全文；LocalMiniDrama、MoneyPrinterTurbo、NarratoAI（研究员只看了检索摘要，本次未打开，未列入条目）。
9. **技能市场**：研究员称在 claudemarketplaces 看到 drama-planner 安装 234 次、在 skills-hub.ai 看到 drama-skills 上架，本次未核实，已从条目中删去。没找到名为 skillsllm 的 drama 技能市场。
10. **只读了摘要**：StoryAgent、DreamFactory 没有可用的量化细节，未列为条目。
