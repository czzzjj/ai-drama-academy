# 采集评估表（外部来源总索引）

> 本目录是学院的**外部资料总索引**：9 个分主题目录共 234 条来源（`S-<CODE>-nn`），每条都有 URL、分类、许可、核实状态与落点模块。采集日期 2026-10-06，逐条打开核对过。
> **性质声明**：本目录与 `catalog/` 中的一切内容都是〔外部调研〕，**不是委托方经验**。委托方的一手证据只在 [`00-orientation/client-dossier.md`](../00-orientation/client-dossier.md)（`〔委托方实证〕`）。外部资料与委托方实证冲突时，以 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) 的裁决为准；外部资料只能让一条判断更可信或指出需要 A/B 验证，不能替代委托方的生产事实。
> 引用格式见 [`CONVENTIONS.md`](../CONVENTIONS.md) §2：`〔外部调研·S-PLAT-02〕`；条目 ID 必须存在于下表。目录中的 `F-<CODE>-nn`（关键事实）在各目录的「关键事实」一节。

## 1. 使用规则（agent 读这一节就够开工）

1. **先看分类再决定怎么用**：🟢 可直接用 = 原文/规格/许可明确，可直接落成判据或检查（仍须带 S- 编号）；🟡 需适配 = 方向对但口径、模型、画幅或样本与本管线不同，写成判据前必须标〔学院推断〕并给出 A/B 验证法；⚪ 仅借鉴 = 只取思路或背景，**不得**把其数字写成「经验表明」或判据阈值。
2. **看许可**：「媒体文章，版权所有，仅引用」的条目只能引用关键句并注明出处，不得整段搬运；GitHub 仓库按其许可证；没有许可证声明的仓库按未授权处理，只借鉴思路（见各目录「空白与未找到」）。
3. **看核实列**：`✅` = 已打开页面核对原文；`✅*` = 已打开核对，但抓取方式有变（curl、API、补录等），详见条目的「核实」行；`✅†` = 只核对了摘要页 / 书目页 / 专题页，**未读正文**，引用其数字前回条目确认摘录范围。本目录没有「未核实」条目——未核实的内容已由核实员删除，并写在各目录末节。
4. **社区实测多为小样本**：H3 / Seedance / Wan 的行为数据多数 n=1–20、作者自报（见 S-ZEN-17、S-H3-09 的限定说明）。写进判据时一律按〔外部调研〕标注，并在 40-memory 里留「待本管线复测」。
5. **合规类（S-PLAT-01/02/03、S-H3-14、S-COMFY-01/02/09）优先级高于一切审美类来源**，且**不构成法律意见**，落地前由属主或法务确认（[`50-rubrics/checklists/publish.md`](../50-rubrics/checklists/publish.md)）。

## 2. 统计

### 2.1 按分类

| 分类 | 条数 | 占比 | 含义 |
|---|---|---|---|
| 🟢 可直接用 | 56 | 24% | 可直接落成判据 / 检查 / 参数 |
| 🟡 需适配 | 99 | 42% | 需换口径、验证后再用 |
| ⚪ 仅借鉴 | 79 | 34% | 只借鉴思路，不引数字为据 |
| 合计 | 234 | 100% | 9 个主题目录 |

核实状态：`✅` 173 条，`✅*`（方式说明）51 条，`✅†`（仅摘要/书目/专题页）10 条；未核实 0 条。

### 2.2 按主题与分类

| 主题目录 | 代号 | 🟢 可直接用 | 🟡 需适配 | ⚪ 仅借鉴 | 合计 |
|---|---|---|---|---|---|
| [MiniMax H3 / Hailuo 提示词与运镜](catalog/minimax-h3-hailuo.md) | `S-H3-nn` | 2 | 11 | 4 | 17 |
| [ComfyUI / Qwen-Image / QC 工具链](catalog/comfyui-qwen-qc-tooling.md) | `S-COMFY-nn` | 14 | 3 | 4 | 21 |
| [主流视频模型官方提示词指南（交叉验证模型脾气）](catalog/video-model-prompt-guides.md) | `S-VGEN-nn` | 2 | 12 | 8 | 22 |
| [zenstory-ai/drama-skills 深度评估](catalog/zenstory-drama-skills.md) | `S-ZEN-nn` | 10 | 16 | 6 | 32 |
| [开源 AI 短剧 / 漫剧 / 影片 agent 流水线](catalog/open-source-ai-drama-pipelines.md) | `S-PIPE-nn` | 3 | 2 | 11 | 16 |
| [编剧理论 / 电影语言 / 动作设计 / 竖屏短剧编剧法](catalog/screenwriting-film-language-action.md) | `S-STORY-nn` | 5 | 17 | 10 | 32 |
| [声音 / 色彩灯光 / 表演指导 / 免版权素材库](catalog/sound-color-performance-assets.md) | `S-CRAFT-nn` | 9 | 15 | 12 | 36 |
| [平台发布与流量学（合规、标识、安全区）](catalog/platform-publishing-traffic.md) | `S-PLAT-nn` | 9 | 8 | 11 | 28 |
| [AI 短剧爆款案例 / AI 电影节工作流 / 观众测试方法](catalog/ai-film-cases-audience-testing.md) | `S-CASE-nn` | 2 | 15 | 13 | 30 |
| **合计** | | **56** | **99** | **79** | **234** |

读法：🟢 最集中在 COMFY（工具链原文）、ZEN（可抄的 skill 规则）、PLAT（法规原文）；论文类来源（PIPE 的 agent 框架论文、CASE 中的 LLM-judge 论文）绝大多数是 ⚪，只能给「为什么自评不可信、为什么要独立评审」这类机制背书，不给数字。

## 3. agent 真正该打开的 Top 20

> 选法：全仓引用频次 × 对本管线（ComfyUI 本地 H3 + Qwen-Image，9:16 竖屏）的直接可操作性 × 合规硬度。其余条目按需在下方主表里查。

| # | ID | 名称 | 分类 | 为什么要打开 | 目录 |
|---|---|---|---|---|---|
| 1 | `S-H3-09` | phileiny/h3-storyboard-skill（h3-storyboard，竖屏… | 🟡 需适配 | 条目里引用最多（全仓 160+ 次）：9:16 连载短剧的分镜、拍数、尾部崩解、几张脸几个人、空间只能在图里定；单一项目实测，当假设用，写判据前回条目读限定语。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 2 | `S-ZEN-17` | 模型行为观察摘要（model-behavior-probes.md） | ⚪ 仅借鉴 | 唯一有对白实测数字的来源：自然语速 ≈4.1 字/秒、不写闭嘴句口型落错人、`non_diegetic_music: N/A` 的作用；校准 `dialogue_capacity.py` 的 D3-rushed 与 prompt_lint 的 VP-lipsync / VP-music。 | [zenstory-drama-skills](catalog/zenstory-drama-skills.md) |
| 3 | `S-H3-08` | loopforge0/minimaxh3-shots-skills（h3-camera-s… | 🟡 需适配 | 运镜被什么压掉：4 步 turbo、首帧脚手架、背景参考板；起幅必须在主体最大的一端。写 A4 / R5 相关判据前先读。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 4 | `S-H3-11` | teskor-hub/minimax-h3-skill（minimax-h3 + mini… | 🟡 需适配 | 时长被读成事件速度、「重量落在停上」、事件时长表；A3 慢镜与七相排时的外部依据。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 5 | `S-H3-10` | jtydhr88/ComfyTV 中的 skill h3-cinematic-direct… | 🟡 需适配 | 双人接触只写一个动词最差、写全接近-接触-施力-结果最好；一个短镜只留一个主运镜。action-choreography 的外部依据。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 6 | `S-H3-03` | ComfyUI 原生 H3 节点源码 comfy_extras/nodes_minimax… | 🟡 需适配 | ComfyUI 节点源码：17k+5 帧网格、first_frame 是 plain stretch（2:3 图会被挤）、MAX_PIXELS；一切画幅与帧数判据的出处。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 7 | `S-H3-01` | MiniMax-AI/MiniMax-H3 官方仓库 skills 目录与 h3-prom… | 🟢 可直接用 | 官方 h3-prompt-writing（Ref2VA 六段 / FL2VA 三段 + 对齐句）；社区经验与它冲突时以它为准，写提示词方言前先对一遍字段名与顺序。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 8 | `S-H3-14` | MiniMax H3 Community License Agreement（含 Acce… | 🟢 可直接用 | H3 社区许可：排除地域（美国、欧盟、英国、韩国）、署名、AUP；发布前必须交给人类拍板（R-PUB-09）。 | [minimax-h3-hailuo](catalog/minimax-h3-hailuo.md) |
| 9 | `S-COMFY-08` | ComfyUI 官方：MiniMax H3 Prompt Guide（"Write ban… | 🟢 可直接用 | ComfyUI 官方 H3 提示词指南：「Write bans as positives」；R1「正向优先 + 对已知会长出的物件追加绝对否定」的官方依据。 | [comfyui-qwen-qc-tooling](catalog/comfyui-qwen-qc-tooling.md) |
| 10 | `S-COMFY-05` | ComfyUI 源码 comfy/samplers.py（cfg=1 跳过无条件分支） | 🟢 可直接用 | ComfyUI 源码证实 cfg≈1 时跳过无条件分支：negative_prompt 无效不是错觉，是机制；禁写 negative_prompt 的依据（与 S-COMFY-06 成对读）。 | [comfyui-qwen-qc-tooling](catalog/comfyui-qwen-qc-tooling.md) |
| 11 | `S-COMFY-01` | Qwen-Image-2.1 官方模型卡（Hugging Face） | 🟢 可直接用 | Qwen-Image-2.1 官方模型卡：9:16 官方尺寸 1536×2752 与 2:3 的 1696×2528、Research License（非商用）；关键帧规格与 R-PUB-11 的依据。 | [comfyui-qwen-qc-tooling](catalog/comfyui-qwen-qc-tooling.md) |
| 12 | `S-COMFY-09` | ComfyUI 官方：MiniMax H3 Video Generation Guide（… | 🟡 需适配 | ComfyUI 官方 H3 视频生成指南：本地输出商用授权口径、画布、步数、采样器；与 S-H3-14 许可表述不一致处要上报属主。 | [comfyui-qwen-qc-tooling](catalog/comfyui-qwen-qc-tooling.md) |
| 13 | `S-COMFY-16` | Whisper 静音幻觉数据集 sachaarbonel/whisper-hallucin… | 🟢 可直接用 | Whisper 静音幻觉公开数据集：转写不能当事实，只能定位与查缺句（D5）；`transcript_reconcile.py` 的 TR-hallucination 黑名单出处。 | [comfyui-qwen-qc-tooling](catalog/comfyui-qwen-qc-tooling.md) |
| 14 | `S-PLAT-02` | GB 45438-2025《网络安全技术 人工智能生成合成内容标识方法》（原文 PDF） | 🟢 可直接用 | GB 45438-2025：显式标识要素、起始画面边或角、字高 ≥ 画面短边 5%、≥2s、AIGC 元数据字段；R-PUB-01 – R-PUB-06 的原文来源（EX-06 用它）。 | [platform-publishing-traffic](catalog/platform-publishing-traffic.md) |
| 15 | `S-PLAT-01` | 《微短剧发展管理办法》（国家广播电视总局令第16号） | 🟢 可直接用 | 《微短剧发展管理办法》：第 34 条每集明显位置 AI 提示标识、第 27 条片头剧名与编号；发布合规的第一道门。 | [platform-publishing-traffic](catalog/platform-publishing-traffic.md) |
| 16 | `S-PLAT-07` | 新京报：红果短剧《关于规范AI剧角色创作的公告》（2026-07-23） | 🟡 需适配 | 红果 AI 剧角色规范：主要角色清晰区分度、治理高频 AI 脸；把 B3 克隆脸从质量问题升级为下架风险。 | [platform-publishing-traffic](catalog/platform-publishing-traffic.md) |
| 17 | `S-PLAT-20` | Meta Ads Guide：Instagram Reels 广告规格与安全区 | 🟡 需适配 | Meta Reels 广告安全区（顶 14% / 底 35% / 左右 6%）：调研中唯一有官方百分比的安全区，R-PUB-04 / R-PUB-18 照它执行；只是广告规格，须标〔学院推断〕。 | [platform-publishing-traffic](catalog/platform-publishing-traffic.md) |
| 18 | `S-VGEN-11` | BytePlus ModelArk: Dreamina Seedance 2.0 seri… | 🟡 需适配 | Seedance 2.0 官方指南：竖屏更易出字幕、多视角设定图的同框重复风险；与 H3 同类脾气的交叉验证，D1 / B3 的旁证。 | [video-model-prompt-guides](catalog/video-model-prompt-guides.md) |
| 19 | `S-VGEN-19` | LTX Blog: How To Fix Slow Motion In AI-Genera… | 🟡 需适配 | LTX：慢动作是生成器默认偏差的成因与修法；A3 不是风格问题的旁证，改写实时速度句前先读。 | [video-model-prompt-guides](catalog/video-model-prompt-guides.md) |
| 20 | `S-CASE-23` | LLM Evaluators Recognize and Favor Their Own … | ⚪ 仅借鉴 | LLM 评审偏好自己的生成：agent 自验证不可信、审片要换会话的机制依据（F1、screening-review；与 S-CASE-21、S-CASE-24 成组）。 | [ai-film-cases-audience-testing](catalog/ai-film-cases-audience-testing.md) |

## 4. 分主题主表

> 列：ID ｜ 名称 ｜ 分类 ｜ 许可（取首句，全文见目录条目）｜ 核实（`✅` / `✅*` / `✅†`，见 §1.3）。URL、摘录、落点模块在对应目录文件。

### 4.1 [MiniMax H3 / Hailuo 提示词与运镜](catalog/minimax-h3-hailuo.md)（17 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-H3-01` | MiniMax-AI/MiniMax-H3 官方仓库 skills 目录与 h3-prompt-writing… | 🟢 可直接用 | MiniMax H3 Community License Agre… | ✅ |
| `S-H3-02` | HuggingFace 模型卡 MiniMaxAI/MiniMax-H3 | 🟡 需适配 | MiniMax H3 Community License Agre… | ✅ |
| `S-H3-03` | ComfyUI 原生 H3 节点源码 comfy_extras/nodes_minimax_h3.py | 🟡 需适配 | GPL-3.0（ComfyUI） | ✅ |
| `S-H3-04` | ComfyUI 官方 H3 教程（总览 / 原生工作流 / 提示词指南） | 🟡 需适配 | 文档（引用即可） | ✅ |
| `S-H3-05` | MiniMax 开放平台 H3 视频生成 API（v2 create / H3-Context-IR / 视频… | 🟡 需适配 | API 文档（按 MiniMax 服务条款） | ✅ |
| `S-H3-06` | MiniMax 旧版文生视频 API 的方括号运镜指令（Hailuo-02 / Hailuo-2.3 / *-… | ⚪ 仅借鉴 | API 文档 | ✅ |
| `S-H3-07` | MiniMax 官方《Run and self-host MiniMax H3》 | 🟡 需适配 | 文档 | ✅ |
| `S-H3-08` | loopforge0/minimaxh3-shots-skills（h3-camera-shots + h3-… | 🟡 需适配 | MIT（upstream/ 目录沿用 MiniMax 条款，不在 … | ✅ |
| `S-H3-09` | phileiny/h3-storyboard-skill（h3-storyboard，竖屏连载短剧分镜与表演） | 🟡 需适配 | MIT | ✅ |
| `S-H3-10` | jtydhr88/ComfyTV 中的 skill h3-cinematic-director | 🟡 需适配 | MIT | ✅* |
| `S-H3-11` | teskor-hub/minimax-h3-skill（minimax-h3 + minimax-h3-ree… | 🟡 需适配 | MIT | ✅ |
| `S-H3-12` | ComfyUI-MiniMaxH3-Director（时间线编辑节点） | 🟡 需适配 | GPL-3.0 | ✅ |
| `S-H3-13` | HuggingFace MiniMax-H3 讨论区（#76、#106、#91 等） | ⚪ 仅借鉴 | 用户帖子（仅引用） | ✅* |
| `S-H3-14` | MiniMax H3 Community License Agreement（含 Acceptable Use… | 🟢 可直接用 | MiniMax H3 Community License Agre… | ✅ |
| `S-H3-15` | MiniMax Speech T2A HTTP API（speech-2.8） | 🟡 需适配 | API 服务条款（本次未找到开源权重） | ✅ |
| `S-H3-16` | MiniMax Music Generation API（music-3.0 / 2.6）服务调整公告与开源 … | ⚪ 仅借鉴 | API 服务条款 | ✅ |
| `S-H3-17` | Atlas Cloud《MiniMax H3 Director: Can You Actually Direc… | ⚪ 仅借鉴 | 博客（仅引用） | ✅ |

### 4.2 [ComfyUI / Qwen-Image / QC 工具链](catalog/comfyui-qwen-qc-tooling.md)（21 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-COMFY-01` | Qwen-Image-2.1 官方模型卡（Hugging Face） | 🟢 可直接用 | Qwen Research License Agreement | ✅ |
| `S-COMFY-02` | QwenLM/Qwen-Image-2.1 GitHub README（官方提示词改写与架构说明） | 🟡 需适配 | Qwen Research License Agreement（非… | ✅ |
| `S-COMFY-03` | ComfyUI 官方教程：Qwen-Image-2.1 Native Workflow Example | 🟢 可直接用 | Comfy Org 官方文档（引用事实） | ✅ |
| `S-COMFY-04` | Comfy-Org workflow_templates：Qwen-Image-2.1 T2I/Edit 模板… | 🟢 可直接用 | MIT（仓库 LICENSE 已核对，Copyright Comf… | ✅* |
| `S-COMFY-05` | ComfyUI 源码 comfy/samplers.py（cfg=1 跳过无条件分支） | 🟢 可直接用 | GPL-3.0 | ✅* |
| `S-COMFY-06` | Diffusers 文档：QwenImage pipelines（true_cfg_scale / negat… | 🟢 可直接用 | Apache-2.0（diffusers 项目文档） | ✅ |
| `S-COMFY-07` | Ho & Salimans《Classifier-Free Diffusion Guidance》arXiv:… | ⚪ 仅借鉴 | arXiv 论文（引用） | ✅† |
| `S-COMFY-08` | ComfyUI 官方：MiniMax H3 Prompt Guide（"Write bans as posit… | 🟢 可直接用 | Comfy Org 官方文档（引用事实） | ✅ |
| `S-COMFY-09` | ComfyUI 官方：MiniMax H3 Video Generation Guide（许可、画布、步数、采… | 🟡 需适配 | 文档引用 | ✅ |
| `S-COMFY-10` | ComfyUI 官方：Server Routes & WebSocket | 🟢 可直接用 | 文档引用 | ✅* |
| `S-COMFY-11` | FFmpeg Filters Documentation | 🟢 可直接用 | FFmpeg 文档（软件为 LGPL/GPL） | ✅* |
| `S-COMFY-12` | GY/T 377—2023《网络视听节目音频响度技术要求和测量方法》全文 PDF | 🟢 可直接用 | 国家广播电视总局发布的推荐性行业标准（公开引用） | ✅* |
| `S-COMFY-13` | AES TD1008 流媒体响度建议（Production Advice 解读） | ⚪ 仅借鉴 | 第三方文章（引用） | ✅ |
| `S-COMFY-14` | openai/whisper transcribe.py（幻觉相关阈值的真实语义） | 🟢 可直接用 | MIT | ✅* |
| `S-COMFY-15` | SYSTRAN/faster-whisper（Silero VAD 过滤） | 🟢 可直接用 | MIT | ✅* |
| `S-COMFY-16` | Whisper 静音幻觉数据集 sachaarbonel/whisper-hallucinations | 🟢 可直接用 | MIT | ✅* |
| `S-COMFY-17` | Barański 等《Investigation of Whisper ASR Hallucinations … | ⚪ 仅借鉴 | arXiv 论文（引用） | ✅† |
| `S-COMFY-18` | FunAudioLLM/SenseVoice（中文 ASR + 情感/事件标签） | 🟡 需适配 | 代码为 MIT | ✅ |
| `S-COMFY-19` | PaddleOCR 3.7 / PP-OCRv6（含 RapidOCR ONNX 部署） | 🟢 可直接用 | Apache-2.0 | ✅* |
| `S-COMFY-20` | PySceneDetect v0.7.1 CLI 文档 | 🟢 可直接用 | BSD-3-Clause（另取 GitHub 仓库 LICENSE… | ✅ |
| `S-COMFY-21` | 同行 AI 片管线经验：infometa/workbuddyskills workrally-brand-fi… | ⚪ 仅借鉴 | 未声明（页面未显示许可，仓库根目录 LICENSE 返回 404）… | ✅* |

### 4.3 [主流视频模型官方提示词指南（交叉验证模型脾气）](catalog/video-model-prompt-guides.md)（22 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-VGEN-01` | OpenAI Sora 2 Prompting Guide（Cookbook） | 🟡 需适配 | MIT（同文 notebook 位于 openai/openai-… | ✅* |
| `S-VGEN-02` | Google Cloud Blog: The ultimate prompting guide for Veo… | 🟡 需适配 | Google 博客，版权所有，仅引用 | ✅ |
| `S-VGEN-03` | Vertex AI: Veo video generation prompt guide | 🟡 需适配 | 页脚注明内容 CC BY 4.0、代码示例 Apache-2.0（… | ✅* |
| `S-VGEN-04` | MIT Technology Review: Google's generative video model … | ⚪ 仅借鉴 | 版权所有，仅引用 | ✅ |
| `S-VGEN-05` | Runway: Gen-4 Video Prompting Guide | 🟡 需适配 | Runway 帮助中心，版权所有，仅引用 | ✅* |
| `S-VGEN-06` | Runway: Image to Video Prompting Guide（Gen-4.5） | 🟡 需适配 | Runway 帮助中心，版权所有，仅引用 | ✅* |
| `S-VGEN-07` | Runway: Introduction to Prompting（Gen-4.5，含同系列 Text to … | ⚪ 仅借鉴 | Runway 帮助中心，版权所有，仅引用 | ✅* |
| `S-VGEN-08` | Kling VIDEO 3.0 Model User Guide（可灵 3.0 官方指南） | 🟡 需适配 | 快手可灵官方文档，版权所有，仅引用 | ✅* |
| `S-VGEN-09` | KLING VIDEO 2.6 Audio User Guide（可灵 2.6 音画同出指南） | 🟡 需适配 | 快手可灵官方文档，版权所有，仅引用 | ✅* |
| `S-VGEN-10` | Kling Image-to-Video Guide（可灵图生视频指南） | ⚪ 仅借鉴 | 快手可灵官方文档，版权所有，仅引用 | ✅ |
| `S-VGEN-11` | BytePlus ModelArk: Dreamina Seedance 2.0 series prompt … | 🟡 需适配 | BytePlus（字节跳动）官方文档，版权所有，仅引用 | ✅* |
| `S-VGEN-12` | BytePlus ModelArk: Dreamina Seedance 2.5 prompt guide | 🟡 需适配 | BytePlus（字节跳动）官方文档，版权所有，仅引用 | ✅* |
| `S-VGEN-13` | 阿里云百炼：文生视频/图生视频 Prompt 使用指南（万相 3.0/2.7/2.6/2.5） | 🟡 需适配 | 阿里云文档，版权所有，仅引用 | ✅* |
| `S-VGEN-14` | Wan2.2 开源仓库默认负向提示词（wan/configs/shared_config.py） | 🟢 可直接用 | Apache-2.0（仓库 LICENSE.txt 已核对） | ✅* |
| `S-VGEN-15` | MiniMax H3 官方 Video Prompt Writing Guide（base / ref，Hug… | 🟢 可直接用 | MiniMax H3 Community License（Docu… | ✅* |
| `S-VGEN-16` | MiniMax-H3 GitHub skills：h3-prompt-writing | 🟡 需适配 | 仓库根目录没有 LICENSE 文件（raw 404） | ✅* |
| `S-VGEN-17` | Luma Learning Center: MiniMax H3 Complete Guide | ⚪ 仅借鉴 | Luma AI，版权所有，仅引用 | ✅ |
| `S-VGEN-18` | Luma Learning Center: Character Consistency Techniques | ⚪ 仅借鉴 | Luma AI，版权所有，仅引用 | ✅* |
| `S-VGEN-19` | LTX Blog: How To Fix Slow Motion In AI-Generated Videos | 🟡 需适配 | Lightricks/LTX 博客，版权所有，仅引用 | ✅* |
| `S-VGEN-20` | Gemini API: Generate videos with Veo | ⚪ 仅借鉴 | Google 开发者文档（页脚许可本次未核对），仅引用 | ✅* |
| `S-VGEN-21` | BytePlus ModelArk: Seedance 1.5 Pro prompt guide | ⚪ 仅借鉴 | BytePlus（字节跳动）官方文档，版权所有，仅引用 | ✅* |
| `S-VGEN-22` | Vidu 开放平台 API：图生视频 | ⚪ 仅借鉴 | Vidu 开放平台文档，版权所有，仅引用 | ✅* |

### 4.4 [zenstory-ai/drama-skills 深度评估](catalog/zenstory-drama-skills.md)（32 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-ZEN-01` | drama-skills 总路由 skill：short-drama/SKILL.md | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-02` | short-drama-novel-analyze：长篇原著 S0–S5 分析管道 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-03` | short-drama-develop：故事引擎、分集地图与节奏档案 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-04` | short-drama-write：可拍中文剧本格式与写作规则 | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-05` | short-drama-assets：身份/变体/镜头瞬态拆分与视觉设定 | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-06` | short-drama-image-prompts：角色/场景/道具板提示词 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-07` | short-drama-storyboard：有职责的分镜与冻结关键帧 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-08` | short-drama-video-prompts：视频提示词与模型方言路由 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-09` | MiniMax H3 提示词方言（minimax-h3.md） | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-10` | short-drama-produce：预览→确认→执行的生产闸门 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-11` | short-drama-edit：剪辑单 + check/render/verify | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-12` | short-drama-review：独立证据审查 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-13` | 五份创作文档模型（creator-documents.md） | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-14` | creator_markdown_check.py：五文档跨文档机械校验器 | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-15` | 跨镜一致性锁（continuity-lock.md） | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-16` | duration_estimate.py：按项目声明语速的剧本时长估算 | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-17` | 模型行为观察摘要（model-behavior-probes.md） | ⚪ 仅借鉴 | MIT | ✅ |
| `S-ZEN-18` | 评估体系 README（回归闸门 + 跨题材盲评门禁 + 实跑） | ⚪ 仅借鉴 | MIT（仓库） | ✅ |
| `S-ZEN-19` | 剧本盲评量表 v5（content-quality-rubric.md） | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-20` | 制作形态卡（production-form-profiles.md + form-cards/ 六张） | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-21` | 分集设计与项目节奏档案（episode-design.md） | 🟡 需适配 | MIT | ✅ |
| `S-ZEN-22` | 镜头手艺（shot-craft.md）：运镜逐镜选、对白估时、镜长推导 | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-23` | 制作质量检查与改写回归（production-quality-gates.md） | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-24` | 项目级校准与结果处置（project-calibration.md） | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-25` | 动作的可生成性（generability.md，VID-21） | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-26` | 字幕与声音规范（sound-and-subtitles.md） | 🟢 可直接用 | MIT | ✅ |
| `S-ZEN-27` | DESIGN.md：单页创作台设计 | ⚪ 仅借鉴 | MIT | ✅ |
| `S-ZEN-28` | 维护者 know-how 晋升流程（short-drama-knowhow） | ⚪ 仅借鉴 | MIT | ✅ |
| `S-ZEN-29` | MiniMax 官方 H3 full-reference 提示词指南（ref-en.txt） | 🟡 需适配 | MiniMax H3 Community License Agre… | ✅ |
| `S-ZEN-30` | MiniMax 官方 H3 base 提示词指南（base-en.txt） | 🟡 需适配 | MiniMax H3 Community License Agre… | ✅ |
| `S-ZEN-31` | MiniMax 视频生成 API（video-generation-v2-create） | ⚪ 仅借鉴 | 官方文档（非开源） | ✅ |
| `S-ZEN-32` | MiniMax H3 官方 skills 发布报道（ComfyUI Wiki） | ⚪ 仅借鉴 | 未标明 | ✅ |

### 4.5 [开源 AI 短剧 / 漫剧 / 影片 agent 流水线](catalog/open-source-ai-drama-pipelines.md)（16 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-PIPE-01` | Dramake（xixihhhh/ai-short-drama-skill）AI 短剧 Agent Skill | 🟢 可直接用 | MIT | ✅ |
| `S-PIPE-02` | drama-skills（zenstory-ai）11 个短剧/漫剧 Claude Code·Codex 技能 | 🟢 可直接用 | MIT | ✅ |
| `S-PIPE-03` | drama-skills 模型行为观察摘要（MiniMax H3 / Seedance / Wan 3.0 小… | 🟢 可直接用 | MIT | ✅ |
| `S-PIPE-04` | OnlyShot（A-cat-with-carrots）AI 短剧工业流水线 Claude Skill | 🟡 需适配 | MIT | ✅ |
| `S-PIPE-05` | ViMax: Agentic Video Generation（HKUDS） | 🟡 需适配 | 代码 MIT | ✅ |
| `S-PIPE-06` | FilmAgent: A Multi-Agent Framework for End-to-End Film … | ⚪ 仅借鉴 | 论文（arXiv） | ✅ |
| `S-PIPE-07` | MovieAgent: Automated Movie Generation via Multi-Agent … | ⚪ 仅借鉴 | 论文（arXiv） | ✅ |
| `S-PIPE-08` | MAViS: A Multi-Agent Framework for Long-Sequence Video … | ⚪ 仅借鉴 | 论文（arXiv） | ✅ |
| `S-PIPE-09` | VideoGen-of-Thought (VGoT): Step-by-step multi-shot vid… | ⚪ 仅借鉴 | 论文（arXiv） | ✅ |
| `S-PIPE-10` | Anim-Director: A Large Multimodal Model Powered Agent f… | ⚪ 仅借鉴 | 论文（arXiv） | ✅ |
| `S-PIPE-11` | MSAVBench: Towards Comprehensive and Reliable Evaluatio… | ⚪ 仅借鉴 | arXiv 页标注 non-exclusive distribut… | ✅ |
| `S-PIPE-12` | MSVBench: Towards Human-Level Evaluation of Multi-Shot … | ⚪ 仅借鉴 | CC BY 4.0（arXiv 页标注） | ✅ |
| `S-PIPE-13` | CHIEF: Creator-Driven Recurrent Video Generation with A… | ⚪ 仅借鉴 | CC BY 4.0（arXiv 页标注） | ✅ |
| `S-PIPE-14` | huobao-drama（火宝短剧，chatfire-AI） | ⚪ 仅借鉴 | CC BY-NC-SA 4.0（禁止商用） | ✅ |
| `S-PIPE-15` | Seedance Drama Maker（wanglongxiao）多 agent 短剧管线 | ⚪ 仅借鉴 | MIT | ✅ |
| `S-PIPE-16` | screen-creative-skills（vangongwanxiaowan）影视剧本创作与评估 Clau… | ⚪ 仅借鉴 | MIT | ✅ |

### 4.6 [编剧理论 / 电影语言 / 动作设计 / 竖屏短剧编剧法](catalog/screenwriting-film-language-action.md)（32 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-STORY-01` | StudioBinder：Save the Cat Beat Sheet（Blake Snyder 15 拍） | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-02` | McKee 官方站：Do Your Scenes Turn? | 🟡 需适配 | 版权 | ✅ |
| `S-STORY-03` | The Story Department：Inciting Incident Definitions（Kare… | ⚪ 仅借鉴 | 版权文章 | ✅ |
| `S-STORY-04` | Jane Friedman 站：What Does It Mean to Write a Scene That… | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-05` | Den of Geek：Rick and Morty Season 4 & Dan Harmon's Stor… | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-06` | Tubefilter：Pixar's 22 Rules of Storytelling（Emma Coats） | ⚪ 仅借鉴 | 版权文章 | ✅ |
| `S-STORY-07` | David Bordwell：Hitchcock, Lessing, and the bomb under t… | 🟡 需适配 | 版权博客 | ✅ |
| `S-STORY-08` | Wikipedia：180-degree rule | 🟢 可直接用 | CC BY-SA 4.0 | ✅ |
| `S-STORY-09` | Wikipedia：Continuity editing | 🟢 可直接用 | CC BY-SA 4.0 | ✅ |
| `S-STORY-10` | Wikipedia：Cutting on action | 🟢 可直接用 | CC BY-SA 4.0 | ✅ |
| `S-STORY-11` | learnaboutfilm：The 180 Degree Rule, Looking Space and E… | 🟡 需适配 | 版权教育网站 | ✅ |
| `S-STORY-12` | Wikipedia：Kuleshov effect | 🟢 可直接用 | CC BY-SA 4.0 | ✅ |
| `S-STORY-13` | No Film School：6 "Rules" for Good Cutting According to … | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-14` | Musicbed：Editing Secrets from Legendary Editor Walter M… | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-15` | How To Film School：Motivated Camera Movement | 🟡 需适配 | 版权教育网站 | ✅ |
| `S-STORY-16` | No Film School：Jackie Chan's 9 Principles of Action Com… | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-17` | No Film School：Tarantino Breaks Down Hong Kong vs. Amer… | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-18` | David Bordwell：A glance at blows（2008-12-28） | 🟡 需适配 | 版权博客 | ✅ |
| `S-STORY-19` | David Bordwell：PLANET HONG KONG: The dragon dances（2011… | 🟡 需适配 | 版权博客 | ✅ |
| `S-STORY-20` | David Bordwell：Unsteadicam Chronicles（2007-08-17） | ⚪ 仅借鉴 | 版权博客 | ✅ |
| `S-STORY-21` | PremiumBeat：How to Edit a Fight Scene（John Francis McCu… | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-22` | Wikipedia：Twelve basic principles of animation | 🟢 可直接用 | CC BY-SA 4.0 | ✅ |
| `S-STORY-23` | 人民日报客户端（来源：央视新闻）：起底野蛮生长的微短剧（2024-12-21） | ⚪ 仅借鉴 | 新闻报道，版权归媒体 | ✅ |
| `S-STORY-24` | 中国作家网（原载光明日报）陈艳：微短剧流行与竖屏风格构建（2026-08-29） | ⚪ 仅借鉴 | 媒体评论文章，版权归作者/媒体 | ✅ |
| `S-STORY-25` | 人民论坛 范志忠：网络微短剧何以成为风口（2024-03-01） | ⚪ 仅借鉴 | 期刊文章，版权归作者/媒体 | ✅ |
| `S-STORY-26` | 界面新闻 潘文捷：微短剧注定肤浅吗？（2023-12-01） | ⚪ 仅借鉴 | 新闻报道，版权归媒体（页面注明未经授权禁止转载） | ✅* |
| `S-STORY-27` | 澎湃号·湃客：纯小白现在入局也不晚？爆款短剧编剧分享第一期（2025-11-02） | 🟡 需适配 | 自媒体文章，版权归作者 | ✅ |
| `S-STORY-28` | Filmustage：How to Write a Vertical Drama Script | 🟡 需适配 | 版权文章（商业工具博客） | ✅ |
| `S-STORY-29` | InkTip：Writing for Verticals（Thomas Blakeley） | 🟡 需适配 | 版权文章 | ✅ |
| `S-STORY-30` | LA Film School：Every Second Is Drama: Behind the Scenes… | ⚪ 仅借鉴 | 版权文章 | ✅ |
| `S-STORY-31` | The Vertical Reach Podcast Ep.11：The Writer Is King: Ad… | ⚪ 仅借鉴 | 播客节目页，版权归节目方 | ✅ |
| `S-STORY-32` | 豆瓣读书：张力《功夫片的秘密：动作导演艺术》（世界图书出版公司，2012） | ⚪ 仅借鉴 | 图书，版权所有 | ✅† |

### 4.7 [声音 / 色彩灯光 / 表演指导 / 免版权素材库](catalog/sound-color-performance-assets.md)（36 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-CRAFT-01` | Walter Murch — Dense Clarity / Clear Density（Transom） | ⚪ 仅借鉴 | 版权归作者/Transom，仅可引用观点与短句 | ✅ |
| `S-CRAFT-02` | Krotos — Film sound design: a how-to guide | ⚪ 仅借鉴 | 版权归 Krotos，仅借鉴 | ✅ |
| `S-CRAFT-03` | HackerNoon — AI video comes out silent: the sound desig… | 🟡 需适配 | 版权归作者，仅借鉴流程 | ✅ |
| `S-CRAFT-04` | FilmDaft — The L-Cut and J-Cut: How Film Editors Use Au… | ⚪ 仅借鉴 | 版权归 FilmDaft，仅借鉴 | ✅ |
| `S-CRAFT-05` | Auphonic — Dialog Loudness Normalization（Netflix 对白门限 -… | 🟡 需适配 | 版权归 Auphonic | ✅ |
| `S-CRAFT-06` | Production Advice — AES TD1008 streaming loudness recom… | 🟡 需适配 | 文章版权归作者 | ✅ |
| `S-CRAFT-07` | EBU R 128（v5.0）与 R128 s4（电影化内容） | ⚪ 仅借鉴 | EBU 公开技术文档，PDF 免费下载 | ✅* |
| `S-CRAFT-08` | FFmpeg Filters Documentation — loudnorm / sidechaincomp… | 🟢 可直接用 | FFmpeg 为 LGPL-2.1 或更高版本 | ✅* |
| `S-CRAFT-09` | Google Cloud — The ultimate prompting guide for Veo 3.1 | 🟡 需适配 | Google 官方博客，版权所有，仅借鉴写法 | ✅* |
| `S-CRAFT-10` | OpenAI Cookbook — Sora 2 Prompting Guide | 🟡 需适配 | OpenAI 官方文档，仅借鉴写法（许可细节见 S-VGEN-01） | ✅ |
| `S-CRAFT-11` | Kling AI — VIDEO 2.6 Native Audio User Guide | 🟡 需适配 | 快手可灵官方文档，仅借鉴写法（同一 URL 另见 S-VGEN-0… | ✅ |
| `S-CRAFT-12` | MiniMax — MiniMax H3 官方博客 | 🟡 需适配 | MiniMax 官方博客 | ✅* |
| `S-CRAFT-13` | Hyperallergic — 25 Years of Pixar's Vibrant, Emotional … | ⚪ 仅借鉴 | 版权归 Hyperallergic/Pixar，仅借鉴方法 | ✅* |
| `S-CRAFT-14` | StudioBinder — What is Motivated Lighting in Film | ⚪ 仅借鉴 | 版权归 StudioBinder，仅借鉴 | ✅ |
| `S-CRAFT-15` | StudioBinder — What is Key Light（光比与类型） | ⚪ 仅借鉴 | 版权归 StudioBinder，仅借鉴 | ✅ |
| `S-CRAFT-16` | PetaPixel — What is the Orange & Teal Look and Why is i… | ⚪ 仅借鉴 | 版权归 PetaPixel，仅借鉴 | ✅ |
| `S-CRAFT-17` | ComfyUI-KJNodes — ColorMatch / ColorMatchV2 节点（kijai） | 🟡 需适配 | GPL-3.0（已核对仓库 LICENSE） | ✅* |
| `S-CRAFT-18` | USC Scalar — Directing with Action Verbs!（基于 Judith Wes… | ⚪ 仅借鉴 | 学术教学页，版权归作者，仅借鉴 | ✅ |
| `S-CRAFT-19` | Wikipedia — Stanislavski's system | ⚪ 仅借鉴 | CC BY-SA 4.0（Wikipedia 文本） | ✅ |
| `S-CRAFT-20` | WeShop — Seedance 2.5 micro-expressions: can an AI face… | 🟡 需适配 | 版权归 WeShop，仅借鉴写法 | ✅ |
| `S-CRAFT-21` | BudgetPixel — Beyond the Blank Stare: prompting cinemat… | 🟡 需适配 | 版权归作者，仅借鉴 | ✅ |
| `S-CRAFT-22` | AtlasCloud — 氛围感创作技巧指南（Vibe Creating） | ⚪ 仅借鉴 | 版权归 AtlasCloud，仅借鉴 | ✅ |
| `S-CRAFT-23` | YouTube Help — Use music and sound effects from the Aud… | 🟡 需适配 | YouTube 音频库：标准许可曲目和 CC 曲目 | ✅ |
| `S-CRAFT-24` | Pixabay Content License Summary | 🟢 可直接用 | Pixabay Content License（不是 CC0） | ✅* |
| `S-CRAFT-25` | Free Music Archive — License Guide | 🟡 需适配 | 每首曲目单独标 CC 许可（BY / BY-SA / BY-ND … | ✅ |
| `S-CRAFT-26` | Incompetech（Kevin MacLeod）— FAQ / licensing | 🟢 可直接用 | CC BY 4.0（免费，须署名） | ✅ |
| `S-CRAFT-27` | ccMixter | 🟡 需适配 | 首页的 CC BY-NC 4.0 声明只针对站点文字和图片 | ✅* |
| `S-CRAFT-28` | Freesound — Help / FAQ（licenses） | 🟢 可直接用 | 每条音效单独标许可：CC0 / CC BY / CC BY-NC | ✅ |
| `S-CRAFT-29` | Sonniss — GDC Game Audio Bundle | 🟢 可直接用 | Sonniss 免版税许可：可商用、免署名、禁止单独转售、禁止 A… | ✅ |
| `S-CRAFT-30` | BBC Sound Effects（RemArc 许可） | ⚪ 仅借鉴 | BBC RemArc 许可：只限非商业的个人或研究用途、正规教育用途 | ✅* |
| `S-CRAFT-31` | Adobe Source Han Sans / Source Han Serif（思源黑体 / 思源宋体） | 🟢 可直接用 | SIL OFL 1.1，保留字体名 "Source" | ✅* |
| `S-CRAFT-32` | LXGW WenKai 霞鹜文楷 | 🟢 可直接用 | SIL OFL 1.1，保留名：霞鹜、霞鶩、落霞孤鹜、落霞孤鶩、L… | ✅* |
| `S-CRAFT-33` | Smiley Sans 得意黑 | 🟢 可直接用 | SIL OFL 1.1，保留名 Smiley / 得意黑 | ✅* |
| `S-CRAFT-34` | 阿里巴巴普惠体 3.0 法律声明 | 🟢 可直接用 | 阿里巴巴专有免费许可（不是 OFL），可商用 | ✅* |
| `S-CRAFT-35` | MiSans 字体知识产权许可协议（小米） | 🟡 需适配 | 小米专有免费许可：可商用，但须"在软件中特别注明"，且不得改编 | ✅* |
| `S-CRAFT-36` | 站酷字体专题页（站酷快乐体 / 高端黑 / 酷黑等） | 🟡 需适配 | 站酷专题页声明"免费授权全社会使用（包括商用）" | ✅† |

### 4.8 [平台发布与流量学（合规、标识、安全区）](catalog/platform-publishing-traffic.md)（28 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-PLAT-01` | 《微短剧发展管理办法》（国家广播电视总局令第16号） | 🟢 可直接用 | 政府公开法规文本（新华网刊载），可引用 | ✅ |
| `S-PLAT-02` | GB 45438-2025《网络安全技术 人工智能生成合成内容标识方法》（原文 PDF） | 🟢 可直接用 | 强制性国家标准文本（编号为 GB，不是 GB/T），可引用 | ✅ |
| `S-PLAT-03` | 《人工智能生成合成内容标识办法》（网信办等四部门） | 🟢 可直接用 | 政府公开法规文本，可引用 | ✅ |
| `S-PLAT-04` | 广电总局微短剧"分类分层审核"制度（新华社，2025-02-05） | 🟡 需适配 | 政府文件的新闻转载，可引用 | ✅ |
| `S-PLAT-05` | 财联社：广电总局发布 AI 微短剧分类分层标准（2026-06-25） | 🟢 可直接用 | 新闻报道转述政府文件 | ✅ |
| `S-PLAT-06` | 澎湃：AI 微短剧须标注"AI辅助制作"的说法（2026-07-23，单一来源） | ⚪ 仅借鉴 | 媒体文章 | ✅ |
| `S-PLAT-07` | 新京报：红果短剧《关于规范AI剧角色创作的公告》（2026-07-23） | 🟡 需适配 | 新闻报道（引用平台公告） | ✅ |
| `S-PLAT-08` | 中新网：红果短剧发布治理公告，一季度下架违规漫剧 1718 部（2026-04） | ⚪ 仅借鉴 | 新闻报道 | ✅ |
| `S-PLAT-09` | 凤凰科技：《桃花簪》"AI 偷脸"下架案（2026-04-03） | ⚪ 仅借鉴 | 新闻报道 | ✅ |
| `S-PLAT-10` | 科技日报：红果单账户单日上传上限（2026-03-19） | ⚪ 仅借鉴 | 媒体文章 | ✅ |
| `S-PLAT-11` | 澎湃：抖音升级 AI 内容标识功能（2025-09-01） | 🟢 可直接用 | 新闻报道（平台规则） | ✅ |
| `S-PLAT-12` | IT之家：广电总局《网络视听收视指标及计算方法》（2024-01） | 🟢 可直接用 | 行业标准（新闻转述） | ✅ |
| `S-PLAT-13` | 澎湃转载 DataEye 研究院 WAIC 发布：AI 漫剧上半年数据（2026-07-22） | ⚪ 仅借鉴 | 行业报告（媒体转载，仅引用数据） | ✅ |
| `S-PLAT-14` | 新华网（转载解放日报）：《中国微短剧行业发展白皮书(2025)》数据（2026-01-15） | ⚪ 仅借鉴 | 协会报告（媒体转载） | ✅ |
| `S-PLAT-15` | 中国作家网（转载文汇报）：《中国网络视听发展研究报告(2026)》数据（2026-04-16） | ⚪ 仅借鉴 | 协会报告（媒体转载） | ✅ |
| `S-PLAT-16` | 虎嗅：漫剧经营数据（2026-10-01） | ⚪ 仅借鉴 | 媒体文章（仅引用事实） | ✅ |
| `S-PLAT-17` | CBNData：《千亿短剧市场，上演付费"局中局"》（2024-03-25） | 🟡 需适配 | 媒体文章（仅引用行规） | ✅ |
| `S-PLAT-18` | 人人都是产品经理：《微短剧，风再起》（2024-01-03） | 🟡 需适配 | 媒体文章（仅引用行规） | ✅ |
| `S-PLAT-19` | 东方财富（转载证券日报）：多平台 10 月起实施短剧激励新则（2026-09-30） | ⚪ 仅借鉴 | 财经媒体报道 | ✅ |
| `S-PLAT-20` | Meta Ads Guide：Instagram Reels 广告规格与安全区 | 🟡 需适配 | Meta 官方文档（引用参数） | ✅ |
| `S-PLAT-21` | TikTok Ads 帮助中心：广告创意最佳实践（附竞价信息流广告规格） | 🟡 需适配 | TikTok 官方文档 | ✅ |
| `S-PLAT-22` | TikTok Creator Academy：Elements of a TikTok video | 🟡 需适配 | TikTok 官方创作者教程 | ✅ |
| `S-PLAT-23` | TikTok Creator Academy：AI-generated content label | 🟢 可直接用 | TikTok 官方创作者教程 | ✅ |
| `S-PLAT-24` | YouTube Help：Shorts 时长与 Content ID、缩略图、浏览量计数 | 🟢 可直接用 | YouTube 官方帮助中心 | ✅ |
| `S-PLAT-25` | YouTube Help：生成式 AI 内容披露 | 🟢 可直接用 | YouTube 官方帮助中心 | ✅ |
| `S-PLAT-26` | Instagram 官方博客：Trial Reels | 🟡 需适配 | Instagram 官方博客 | ✅ |
| `S-PLAT-27` | Filmustage：Short Drama Apps Compared: ReelShort vs Dram… | ⚪ 仅借鉴 | 第三方博客（仅引用数据） | ✅ |
| `S-PLAT-28` | Sensor Tower：State of Short Drama Apps 2026 | ⚪ 仅借鉴 | 第三方数据报告（仅引用数据） | ✅ |

### 4.9 [AI 短剧爆款案例 / AI 电影节工作流 / 观众测试方法](catalog/ai-film-cases-audience-testing.md)（30 条）

| ID | 名称 | 分类 | 许可 | 核实 |
|---|---|---|---|---|
| `S-CASE-01` | 新榜对话陈坤（闲人一坤）：《山海奇镜》全网刷屏背后 | ⚪ 仅借鉴 | 媒体文章，版权所有，仅引用 | ✅ |
| `S-CASE-02` | 新浪财经：《山海奇镜之劈波斩浪》收官数据 | ⚪ 仅借鉴 | 媒体文章，版权所有，仅引用 | ✅ |
| `S-CASE-03` | 人民日报海外版：《三星堆·未来启示录》上线 | ⚪ 仅借鉴 | 媒体文章，版权所有，仅引用 | ✅ |
| `S-CASE-04` | CCTV：《中国神话》AI 全流程微短剧（附《千秋诗颂》报道） | ⚪ 仅借鉴 | 官方媒体文章，版权所有，仅引用 | ✅* |
| `S-CASE-05` | fxguide：Actually Using SORA（shy kids《Air Head》） | 🟡 需适配 | 媒体文章，版权所有，仅引用 | ✅ |
| `S-CASE-06` | The Daring Creatives：How Neural Viz makes an entire TV … | 🟡 需适配 | 媒体文章，版权所有，仅引用 | ✅ |
| `S-CASE-07` | Google Blog：Behind the scenes of ANCESTRA（Veo） | ⚪ 仅借鉴 | Google 官方博客，版权所有，仅引用 | ✅ |
| `S-CASE-08` | The Ankler：OpenAI's $30M animated film（Critterz） | ⚪ 仅借鉴 | 媒体文章，版权所有，仅引用 | ✅ |
| `S-CASE-09` | Runway AIF（AI Film Festival）2026 官网 | ⚪ 仅借鉴 | 官网，版权所有，仅引用 | ✅ |
| `S-CASE-10` | Curious Refuge：MiniMax H3 \| An Honest AI Video Review | 🟡 需适配 | 博客文章，版权所有，仅引用 | ✅ |
| `S-CASE-11` | Curious Refuge：How to Change Camera Angles With AI Video | 🟡 需适配 | 博客文章，版权所有，仅引用 | ✅ |
| `S-CASE-12` | 澎湃号·湃客：AI闯短剧：当10万字剧本一键成片，影视行业迎来"无人生产线" | ⚪ 仅借鉴 | 澎湃号自媒体文章（非澎湃新闻采编稿），版权所有，仅引用 | ✅ |
| `S-CASE-13` | Nielsen Norman Group：Thinking Aloud, the #1 Usability T… | 🟡 需适配 | NN/g 文章，版权所有 | ✅ |
| `S-CASE-14` | Nielsen Norman Group：Why You Only Need to Test with 5 U… | 🟡 需适配 | NN/g 文章，版权所有 | ✅ |
| `S-CASE-15` | Nielsen Norman Group：Cloze Test for Reading Comprehensi… | 🟡 需适配 | NN/g 文章，版权所有 | ✅ |
| `S-CASE-16` | YouTube Help：Audience retention key moments | 🟢 可直接用 | Google 帮助文档，版权所有 | ✅ |
| `S-CASE-17` | YouTube Help：Test & Compare thumbnails and titles | 🟢 可直接用 | Google 帮助文档，版权所有 | ✅ |
| `S-CASE-18` | Netflix：The Power of a Picture | 🟡 需适配 | Netflix 官方新闻稿，版权所有，仅引用 | ✅ |
| `S-CASE-19` | Wikipedia：Test screening | ⚪ 仅借鉴 | CC BY-SA 4.0 | ✅ |
| `S-CASE-20` | Wikipedia：Pixar（Braintrust 段落）/ Animatic | 🟡 需适配 | CC BY-SA 4.0 | ✅* |
| `S-CASE-21` | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena（… | 🟡 需适配 | arXiv non-exclusive distribution … | ✅* |
| `S-CASE-22` | Large Language Models are not Fair Evaluators | 🟡 需适配 | arXiv non-exclusive distribution … | ✅† |
| `S-CASE-23` | LLM Evaluators Recognize and Favor Their Own Generations | ⚪ 仅借鉴 | CC BY 4.0 | ✅† |
| `S-CASE-24` | Large Language Models Cannot Self-Correct Reasoning Yet… | ⚪ 仅借鉴 | CC BY 4.0 | ✅† |
| `S-CASE-25` | Justice or Prejudice? Quantifying Biases in LLM-as-a-Ju… | 🟡 需适配 | arXiv non-exclusive distribution … | ✅* |
| `S-CASE-26` | FilmAgent: A Multi-Agent Framework for End-to-End Film … | 🟡 需适配 | 论文 CC BY 4.0 | ✅* |
| `S-CASE-27` | MLLM-as-a-Judge（ICML 2024） | ⚪ 仅借鉴 | CC BY 4.0 | ✅† |
| `S-CASE-28` | Careless Whisper: Speech-to-Text Hallucination Harms（AC… | ⚪ 仅借鉴 | CC BY-NC-ND 4.0 | ✅* |
| `S-CASE-29` | VideoHallucer: Evaluating Intrinsic and Extrinsic Hallu… | 🟡 需适配 | CC BY-NC-SA 4.0 | ✅† |
| `S-CASE-30` | VideoScore: Building Automatic Metrics to Simulate Fine… | 🟡 需适配 | 论文 CC BY 4.0 | ✅† |

## 5. 空白与未找到（9 个目录末节的归并）

> 这些是**调研没有找到、没有核实或已被删除**的东西。agent 遇到相关问题时：不得凭印象补齐，不得把它写成「据调研」；按右列动作处理。完整原文见各目录末节「空白与未找到」。

### 5.1 最影响本管线决策的空白（跨目录归并）

| 空白 | 出处 | 在此之前 agent 怎么做 |
|---|---|---|
| ComfyUI 本地 H3 的实际行为没有任何外部数据：first_frame + 六段 + 多图参考加载哪个检查点、euler vs res_multistep、cfg=1 防装饰物的官方条目、9:16 下首帧与文字运镜的冲突都没有受控数据 | [H3 §空白 3–4](catalog/minimax-h3-hailuo.md)、[ZEN §空白 1](catalog/zenstory-drama-skills.md)、[PIPE §空白 3](catalog/open-source-ai-drama-pipelines.md) | 一律走 `evidence-reconciliation.md` R2 的同 seed A/B；结论写回 R2，不引外部数字当结论 |
| 中文对白容量没有官方数字：7.5（委托方 T-2）、4.1（S-ZEN-17，可发声字口径）、4.30（S-H3-09，含停顿）计数口径互不相同 | [H3 §空白 2](catalog/minimax-h3-hailuo.md)、[VGEN §空白 4](catalog/video-model-prompt-guides.md)、[ZEN §空白 3](catalog/zenstory-drama-skills.md) | 7.5 当硬上限、4.1 当规划语速（R3）；每次出片后用 `transcript_reconcile.py` 回填校准 |
| Qwen-Image-2.1 非商用限制是否及于生成物，LICENSE 没写明；Comfy 文档的商用授权口径与 H3 许可原文关系未澄清 | [COMFY §空白 3](catalog/comfyui-qwen-qc-tooling.md)、[H3 §空白 5](catalog/minimax-h3-hailuo.md) | R-PUB-10 / R-PUB-11 一律上报人类拍板④，不自行判断 |
| 国内平台（抖音、红果、快手、视频号）的官方安全区、上传规格、响度目标、完播率定义都没找到；AI 剧是否降权没有官方表态 | [PLAT §空白 1/4/6/7](catalog/platform-publishing-traffic.md)、[CRAFT §空白 1](catalog/sound-color-performance-assets.md)、[COMFY §空白 1](catalog/comfyui-qwen-qc-tooling.md) | 安全区按 Meta 百分比执行并标〔学院推断〕；响度保留 -16 LUFS（合规依据只有 GY/T 377）；「黄金 3 秒」标成行规 |
| AI 微短剧分类分层标准原文与「AI 辅助制作」标注说法只有转述（单一来源），总局原文没找到 | [PLAT §空白 2](catalog/platform-publishing-traffic.md) | 标识按 GB 45438 的两要素（人工智能 / AI + 生成 / 合成）写，不采用「AI 辅助制作」；分类档位上报属主 |
| 冷观众测试没有带真人样本量的公开协议；「看完复述剧情」没有影视理解测试文献，暂借 NN/g cloze 的 60% 阈值 | [CASE §空白 9](catalog/ai-film-cases-audience-testing.md)、[PIPE §空白 5](catalog/open-source-ai-drama-pipelines.md) | 冷观众阈值全部标〔学院推断〕，首次真实测试后回写；不把 60% 当行业标准 |
| AI 视频表演、竖屏调色/暗部安全、静音与 room tone 的可量化规则、H3 声音分层写多少层——没有权威来源 | [CRAFT §空白 4/11/12/14](catalog/sound-color-performance-assets.md) | 相关判据只能是〔学院推断〕，附实测验证法；不写「经验表明」 |
| 坏帧、烧录文字、AI 伪汉字的公开评测与阈值没有；PaddleOCR 对 AI 伪汉字的召回率未评测 | [COMFY §空白 4/5](catalog/comfyui-qwen-qc-tooling.md) | `burnin_text_scan.py` 无 OCR 时降级为启发式 + 目视；阈值用委托方样片校准 |
| 打斗 / 动作编排的开源 skill 几乎空白；Jackie Chan / 港式动作的原片与逐镜分析多数没取到正文 | [PIPE §空白 6](catalog/open-source-ai-drama-pipelines.md)、[STORY §空白 1/5/9](catalog/screenwriting-film-language-action.md) | 「打与受击同框」「两次好击打」等落到 H3 的做法都是〔学院推断〕，按 `action-choreography` 的验证法 A/B |
| 厂商建议冲突待 A/B：是否复述首帧（F-VGEN-16）、多张单角度参考 vs 大头照加全身照（F-VGEN-24）、`No subtitles` 类否定是否会招字幕（F-H3-08 vs Seedance 2.5） | [VGEN §空白 9](catalog/video-model-prompt-guides.md) | D1 禁令包保留（委托方实证有效）；其余在本管线同 seed 对比后再写判据 |

### 5.2 分目录清单（原文摘要，逐条回原文核对）

**[MiniMax H3 / Hailuo 提示词与运镜](catalog/minimax-h3-hailuo.md)**

- H3「Director」没有官方出处（只有旧 T2V-01-Director；社区节点 / skill 同名）；
- 中文语速与对白容量无官方数字；9:16 与 I2V 首帧 + 文字运镜无受控数据（社区实测多为 16:9）；
- euler 与 res_multistep 差异、cfg=1 防装饰物官方条目缺；
- 许可原文与 Comfy 文档的商用口径不一致，HF 许可问答置顶帖未读；
- 开源配音路线、Music 3 参数量与发布日期未核；Hailuo 02/2.3 旧指南、中文版官方文本未读；
- 托管端 camera_trajectory、Ref2VA 文件总数上限（≤12）是否强制未核；
- 社区数据外推边界：loopforge n=1–2、int8 量化；phileiny 单一项目、部分结论在 8 步加速下测得。

**[ComfyUI / Qwen-Image / QC 工具链](catalog/comfyui-qwen-qc-tooling.md)**

- 平台官方响度目标（抖音、快手、视频号、TikTok、Shorts）未找到，GY/T 377 的 PDF 为第三方托管；
- Whisper 中文幻觉缺官方 issue，证据只有 MIT 数据集与同行经验；
- Qwen-Image-2.1：官方博客未打开、多视图设定板无写法说明、2:3 人像无额外参数建议、LICENSE 对生成物的非商用范围未写明；
- OCR：tesseract chi_sim 文档未核，对 AI 伪汉字的召回率无公开评测；坏帧无公开阈值；
- euler 与 res_multistep 无对比评测；infometa/workbuddyskills 无许可证，只借鉴思路。

**[主流视频模型官方提示词指南（交叉验证模型脾气）](catalog/video-model-prompt-guides.md)**

- 火山引擎中文版 Seedance 指南未读；Luma Ray3.2、Vidu 无可用官方提示词指南；
- 台词容量硬数字：没有任何一家官方给出；
- 官方文档没有「擅自加服饰」条目，只能靠委托方 C1；没有官方讨论 180° 轴线 / 空间连续；
- Kling 3.0 Omni / Camera Control、Vertex 视频最佳实践、Runway Aleph 未读；
- 厂商冲突待 A/B（F-VGEN-16、F-VGEN-24、字幕否定）；H3 4–15 秒（模型卡）与 124–362 帧（节点源码）口径不同，引用须注明出处。

**[zenstory-ai/drama-skills 深度评估](catalog/zenstory-drama-skills.md)**

- ComfyUI 侧完全空白（无帧网格、cfg=1.0、20 步 / 4 步 turbo 信息）；Qwen-Image 出图配方空白；
- 观察样本小（每格 2–20 次）、评审非独立（单一模型）；4.1 与 7.5 字/秒差异原因未定；
- 审查 skill 明写「不查看媒体」——没有自动看片方法，这正是委托方「指标全绿、人仍说不行」的缺口；
- 平台发布与流量、冷观众测试、系统化声音设计、调色、打斗编排体系都不在其覆盖内；
- DESIGN.md 与现行 Dashboard 描述不一致（以现行 SKILL 为准）；无第三方评测；CHANGELOG 与形态卡未逐条核。

**[开源 AI 短剧 / 漫剧 / 影片 agent 流水线](catalog/open-source-ai-drama-pipelines.md)**

- 客户线索「ai-manga-drama / neta make-image·make-video·merge-video」没对上（neta-skills 无 merge-video；canghe-manga-drama 另见）；
- 实测都是作者自报，盲评同一模型完成；没有项目针对 Qwen-Image 2.1 + ComfyUI 本地 H3，也没有处理 <124 帧与 cfg=1；
- 平台留存数据无原始来源（OnlyShot 表内有不可能数值，F-PIPE-20）；冷观众测试缺真人协议；打斗 / 动作编排几乎无开源 skill；
- MAViS 仓库与许可未核，MovieAgent / Anim-Director 无 LICENSE（按未授权）；huobao-drama 后端提示词全文、LocalMiniDrama、MoneyPrinterTurbo、NarratoAI 未深读；技能市场安装量未核。

**[编剧理论 / 电影语言 / 动作设计 / 竖屏短剧编剧法](catalog/screenwriting-film-language-action.md)**

- Every Frame a Painting 原片、成龙 9 原则逐条解释、McKee「gap」原书引文未取得；
- Jim Emerson《In the Cut》（空间混乱逐镜分析）403，建议补抓；Murch 六原则完整权重只核实了情绪 51%；
- 剪到音乐节拍无权威来源；中文竖屏编剧规范无平台官方或教材级手册；
- 动作理论文献（Gravestock、SCMP、《功夫片的秘密》正文）未读；竖屏剧数字（60 秒集、付费墙、季长）单一来源；
- 核实阶段更正了 15 处研究员表述（详见原文，凡引用 STORY 条目以条目现文为准）。

**[声音 / 色彩灯光 / 表演指导 / 免版权素材库](catalog/sound-color-performance-assets.md)**

- 短视频平台响度规格无官方文档，-14 LUFS 仅二手；Netflix 规格原页抓不到；AES TD1008 原文未开；
- 竖屏手机调色 / 亮度 / 暗部安全指南、中文微短剧声音 / 调色 / 表演一手资料、AI 视频表演（呼吸、身体语言、多人对手戏）基于 H3 的资料均无；
- 字体与封面平台授权（OPPO Sans、HarmonyOS Sans、Canva、稿定、创客贴）未核；MiSans 署名在视频中如何履行无官方说明；
- Pixabay 与 Content ID 风险未核实；YouTube 音频库站外使用无官方说明；ccMixter 可商用曲目与 Incompetech 价格未核；
- H3 声音分层、静音 / room tone 数字化规则、Lasseter 引语：均无可核来源。

**[平台发布与流量学（合规、标识、安全区）](catalog/platform-publishing-traffic.md)**

- 国内平台官方安全区与上传规格、红果版权方后台规范、单账户日上传 30 部原文均未找到；
- 「AI 辅助制作」标注与 AI 占比红线只有单一转述；分类分层标准原文未找到；抖音 2026-05 动画微短剧建议无公开原文；
- 完播率官方定义与基准、YouTube Shorts 分析指标、快手 / B 站 / 视频号 2026 集长规范、AI 剧分发权重官方表态均无；
- 数字口径：白皮书「2025 年产值 892 亿元」在原文不存在（不得引用）；破亿率须注明分母。

**[AI 短剧爆款案例 / AI 电影节工作流 / 观众测试方法](catalog/ai-film-cases-audience-testing.md)**

- 整轮检索额度用尽，全部条目来自直接抓取已知 URL（中英文多轮检索未完成）；
- 国内 AI 漫剧爆款一手拆解、创作者扶持计划页、Runway AIF 往届获奖工作流、Critterz 实际映出情况均未找到；
- Neural Viz 只有二手报道（置信度中）；Pixar Braintrust 一手资料被付费墙挡住；
- 试映问卷标准题、拨盘测试方法、「复述剧情」理解测试文献、平台官方 A/B 文档均无；
- 《千秋诗颂》集数只有二手说法；核实阶段更正了 CALM 数值、FilmAgent 百分比等 6 处研究员表述。

## → 行为改变

1. 下次写任何带〔外部调研〕标签的句子，先在 §4 主表里查到该 `S-<CODE>-nn`；查不到就不写（禁止编 ID、URL）。
2. 下次要把一条外部发现写成判据，先看它的分类：🟢 直接写；🟡 写成〔学院推断〕并附 A/B；⚪ 只写成背景，不进判据阈值。
3. 下次遇到 §5.1 列出的空白，不凭印象补，按右列动作处理；做完 A/B 或拿到属主确认后，把结论写回 `evidence-reconciliation.md` 或 40-memory，并把对应空白从本表移走。
4. 下次发布准备、画幅、帧网格、ComfyUI 节点行为相关的任务，先打开 §3 里对应的 Top 20 条目，而不是在 234 条里全文检索。
