# AI 短剧爆款案例拆解 / AI 电影节工作流 / 观众测试方法

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：30 ｜ 核实方式：逐条 WebFetch 打开核对

## 一句话结论

本专题给学院提供三类材料。一是 7 个可核实的 AI 影视案例（《山海奇镜》《三星堆：未来启示录》《中国神话》《Air Head》Neural Viz、ANCESTRA、Critterz），外加一个 AI 影展评审标准（Runway AIF 2026）。这些案例的共同做法有四条：把复杂镜头拆小、对表情和一致性做人工干预、用风格化掩盖瑕疵、先锁定机位再交给生成器。二是观众测试方法：出声思考、5 人迭代、cloze 理解阈值、YouTube 留存与标题封面 A/B、Netflix 封面研究、电影试映、animatic。三是 LLM/MLLM 评审偏差的文献，可作为"独立评审 agent"的设计依据。仍然缺的有：抖音、快手、红果 AI 漫剧爆款的一手逐集拆解（前 3 秒、付费卡点）；AIF 往届获奖片的工作流；试映问卷标准题和拨盘测试（dial testing）的一手方法文档；抖音和巨量引擎封面 A/B 的官方文档。

## 条目

### S-CASE-01 · 新榜对话陈坤（闲人一坤）：《山海奇镜》全网刷屏背后
- **URL**：https://www.newrank.cn/article/detail/26578
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：这是新榜对陈坤的访谈。2024 年 1 月预告片的流程是"ChatGPT+Midjourney/DALL·E 3+PixVerse"。正片由快手可灵和陈坤合作，原文说短剧"仍沿用这套工作流，只是用到的具体AI工具有所不同"。陈坤认为"当下能做成熟商业交付只有'图生视频'工作流"，方法是"将AI难以生成的复杂镜头拆解成更小的单元"。他承认 AI 场景"无法保证每一棵树、每一块石头都固定在原来的位置"。团队情况："10人小团队，10天重制"。文章发布时快手播放量已破 1000 万。观众好评如"共工出山场面宏伟，有看大片的感觉"，差评集中在"面部表情太僵硬""没有灵魂"。
- **对本学院有什么用**：让 agent 把复杂镜头拆成可生成的小单元，并把"表演有没有灵魂"列为高于画质的首要验收项。
- **落点模块**：60-casebook、10-theory、50-rubrics

### S-CASE-02 · 新浪财经：《山海奇镜之劈波斩浪》收官数据
- **URL**：https://finance.sina.com.cn/roll/2024-07-30/doc-incfxvrx6491863.shtml
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：全剧 5 集，在快手上线。原文数据："正片5集播放量超过5200万""全网话题曝光量超4.3亿""登上全平台热搜21个""德塔文短剧景气指数top1、猫眼短剧热度日榜top2"。出品方是快手短剧、自然火和导演陈坤，快手大模型团队提供技术支持。制作过程中，团队"对初版的质量和效果并不满意，进行了反复修改和调整。直到六月，快手可灵AI问世"，之后才加快推进。
- **对本学院有什么用**：给案例卡一个可核实的基准：神话奇观题材做 5 集短篇，能拿到 5000 万级播放；但这证明不了季播几十集的形态可行。
- **落点模块**：60-casebook

### S-CASE-03 · 人民日报海外版：《三星堆·未来启示录》上线
- **URL**：http://paper.people.com.cn/rmrbhwb/html/2024-08/02/content_26072484.htm
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：作者张怡靖。该剧由博纳影业出品，共 13 集，每集 3—4 分钟。2022 年立项，"由于制作周期长、资金投入巨大，一度进展缓慢"；2023 年开始引入 AI 工具。制作中"不断对AI生成的内容进行人工干预和后期优化"，用来保证人物表情细腻、场景一致。传播总量超 1.4 亿，其中抖音 1.35 亿，进入抖音短剧最热榜前五。科幻作家吴岩评价它实现了"高保真""厚叠加""密剪接"。
- **对本学院有什么用**：告诉 agent，接近季播形态的 AI 剧能成，靠的是对表情和一致性的持续人工干预，不是一键成片。
- **落点模块**：60-casebook、10-theory

### S-CASE-04 · CCTV：《中国神话》AI 全流程微短剧（附《千秋诗颂》报道）
- **URL**：https://www.cctv.com/2024/03/22/ARTImxwnEZa0LYYPusv8E57A240322.shtml
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：官方媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实（姊妹篇 https://www.cctv.com/2024/03/10/ARTI3yIlJQqtk0E4TZBcxpJm240310.shtml 亦打开）
- **摘录**：原文："该剧由央视频、总台人工智能工作室联合清华大学新闻与传播学院元宇宙文化实验室合作推出"。共六集，依次是《补天》《逐日》《奔月》《填海》《治水》《尝百草》，"其美术、分镜、视频、配音、配乐全部由AI完成"。本页未给播放数据，也没有说明各集是否独立成篇。姊妹篇《千秋诗颂》基于"央视听媒体大模型"，原文称"六集节目收视率在全国所有上星频道动画片中位居第一"。"文生声、声线克隆"和"增加了中国历史背景介绍和人物身份注释"指的是面向海外的英文版制作，不是原版。
- **对本学院有什么用**：让 agent 看到，公共知识题材按一集一个故事来做，可以避开长期一致性问题（这是据集名推断的结构）；季播追更剧不能照搬。
- **落点模块**：60-casebook、10-theory

### S-CASE-05 · fxguide：Actually Using SORA（shy kids《Air Head》）
- **URL**：https://www.fxguide.com/fxfeatured/actually-using-sora/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：shy kids 生成了"hundreds of generations at 10 to 20 seconds a piece"，剪成 1.5 分钟成片，素材比约 300:1。主角黄色气球镜头之间不一致：有时"wouldn't even be yellow"，有时冒出脸，或带着要在 After Effects 里去掉的绳子。片段以 480p 生成，再用 Topaz Video AI 放大。很多片段生成出来是"50 to 75% speed"，提示词里并没有要求慢动作，只能重新调速。镜头术语大约"six out of 10 times"有效。提示词加"35mm film"有助于画面一致；最后整片统一调色并加颗粒。
- **对本学院有什么用**：让 agent 把抽卡率、调速修正（生成器常默认偏慢）和后期修补当作正常流程记账，不要假定一次生成就能用。
- **落点模块**：60-casebook、20-craft、70-playbooks

### S-CASE-06 · The Daring Creatives：How Neural Viz makes an entire TV universe with AI
- **URL**：https://www.thedaringcreatives.com/creator-stories/the-showrunner-how-neural-viz-makes-an-entire-tv-universe-with-ai/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：文章发布于 2026-07-02，创作者是 Josh Kerrigan。他先写完整剧本，原文是"slug lines, action, dialogue, camera blocking, the whole format"；再用 Midjourney 加其他几款图像工具逐镜出分镜静帧，"holding lighting and sight lines consistent"。他本人对着摄像头表演，由 Runway Act-One 映射到外星角色上；Hedra 做口型，ElevenLabs 配音，Premiere Pro 剪辑。画面统一调成旧 VHS 质感，因为"Clean 4K makes every rendering artifact scream"。角色设计成卡通外星人，是为了绕开恐怖谷。每集 2–3 分钟，约 12 小时完成，工具月费约 100 美元，近乎每周更新，单集播放数十万到数百万。
- **对本学院有什么用**：让 agent 学会用固定资产库、真人表演驱动和风格化美学，来对治脸漂移和表演空洞。
- **落点模块**：60-casebook、20-craft、30-taste

### S-CASE-07 · Google Blog：Behind the scenes of ANCESTRA（Veo）
- **URL**：https://blog.google/technology/google-deepmind/ancestra-behind-the-scenes/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：Google 官方博客，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：这是 Google DeepMind 与 Primordial Soup 合作、Eliza McNitt 导演的短片，在 Tribeca 首映。团队上传了"photos taken by McNitt's father of the day she was born"，让 Gemini 逐项描述其美学细节，作为提示词；Imagen 出概念图。为保持风格，他们"fine-tuned an Imagen model to match the style of reference images"。体内穿行段先建了人体 3D 模型，用虚拟摄像机录一条草稿镜头，再让 Veo 跟随这条运动生成。出生场景把实拍素材、文字描述和指定区域交给 Veo，用"add object"生成婴儿，再做传统 VFX 和调色。参与人员 200 多人。
- **对本学院有什么用**：让 agent 先锁定机位和空间（草稿运动或首帧），再交给生成器，避免文字运镜和首帧冲突造成轴线错乱。
- **落点模块**：60-casebook、20-craft

### S-CASE-08 · The Ankler：OpenAI's $30M animated film（Critterz）
- **URL**：https://theankler.substack.com/p/openai-30m-animated-film-coming-challenge-pixar
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：Critterz 由 OpenAI 与伦敦的 Vertigo Films、洛杉矶的 Native Foreign 合作。原文："The budget is under $30 million, and the timeline for completion is a nine-month sprint"，目标是 2026 年戛纳首映。编剧 James Lamont、Jon Foster 曾参与《Paddington in Peru》。GPT-5 用于剧本开发，DALL·E 用于概念图，团队保留人类配音演员和美术。项目源自 Chad Nelson 2023 年用 DALL·E 做的动画短片。（研究员另提到一款定制 Storyboard 工具，本文未提及，不收录。）
- **对本学院有什么用**：作为参照：头部 AI 长片项目仍保留人类编剧、配音和美术，agent 不应把"全自动"当目标。
- **落点模块**：60-casebook、10-theory

### S-CASE-09 · Runway AIF（AI Film Festival）2026 官网
- **URL**：https://aif.runwayml.com/
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：官网，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：2026 届 Grand Prix 是《A Face Only A Mother Could Love》（Robert Gaudette，7:50），奖金 5 万美元加 100 万积分。Gold 是《THE WELL》（Dorian & Daniel，5:29），1.5 万美元加 50 万积分。Silver 是《Where Knights Fall》（Mathery），1 万美元加 50 万积分。另有 Honoree 2 部、Merit 5 部。影片组要求"3-15 minutes in length"、片中含"generative video"，并且是"a fully contained, linear narrative"。评委 9 人，包括 Roger Avary、Jane Rosenthal、Cristobal Valenzuela 等。
- **对本学院有什么用**：给品味模块一个外部标尺：AI 影展评的是完整的线性叙事，不是技术演示。
- **落点模块**：30-taste、60-casebook

### S-CASE-10 · Curious Refuge：MiniMax H3 | An Honest AI Video Review
- **URL**：https://curiousrefuge.com/blog/minimaxh3-review
- **类型**：article
- **分类**：🟡 需适配
- **许可**：博客文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：H3 单次生成最多接受 9 张参考图、3 段视频、3 段音频。托管版最长 15 秒、2K，开放权重版为 768p。画幅支持 16:9、21:9、9:16，对白最多 11 种语言。与 Seedance 2.5 对比，H3 在大场面动作和"physical interactions"上较弱；多镜头中"characters were less expressive, edits felt less natural"；还存在"texture instability, facial distortions, inconsistent compositing, and visual noise"。开放权重版现行协议"restricts creators in the United States, the EU, the UK, and South Korea from distributing videos generated with the open-weight model"。
- **对本学院有什么用**：让 agent 在写打斗或大动作镜头前预判 H3 的短板，改为拆镜加剪辑；面向全球平台发布前，强制核对 H3 权重许可。
- **落点模块**：20-craft、40-memory、70-playbooks

### S-CASE-11 · Curious Refuge：How to Change Camera Angles With AI Video
- **URL**：https://curiousrefuge.com/blog/how-to-change-camera-angles-with-ai-video
- **类型**：article
- **分类**：🟡 需适配
- **许可**：博客文章，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：做法是上传源视频，"prompt the model to recreate the source footage from a different camera position"。可以写得更具体，也可以附一张参考图或示意图，标出新机位相对主体的位置。结果："Seedance preserved roughly 90–95% of the original performance"。MiniMax H3 的问题是脸更不稳定、皮肤偏软、动作更偏离原表演，"struggled more with skin texture, clothing details, and overall realism"。链式操作（拿 AI 生成的片段再换机位）时，"neither model gave us a usable wide shot that accurately preserved the source performance"。收尾需要几轮迭代、调提示词，再做放大和匹配色彩。（研究员引用的姊妹篇语句未在本页出现，不收录。）
- **对本学院有什么用**：让 agent 补镜头（正反打、换景别）时只从原始锚素材出发，不做链式再生成。
- **落点模块**：20-craft、70-playbooks

### S-CASE-12 · 澎湃号·湃客：AI闯短剧：当10万字剧本一键成片，影视行业迎来"无人生产线"
- **URL**：https://www.thepaper.cn/newsDetail_forward_32829833
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：澎湃号自媒体文章（非澎湃新闻采编稿），版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：发布于 2026-03-26。"传统短剧制作周期为3到6个月"，AI 压缩到几天甚至几小时。"传统短剧制作单集成本多数在万元以上"，"AI短剧单集成本仅500到1000元左右"。创翊传媒用字节跳动的小云雀做 60 集漫剧《万兽独尊》，"5人团队仅用8天便产出上线4天播放量破亿的爆款作品"。工具的不足是"等待时间偏长、穿模、文字乱码等"。原文还提到："2026年春节后，部分短剧平台出现大量剧情框架、冲突设置高度相似的AI短剧，导致用户审美疲劳"。
- **对本学院有什么用**：提醒 agent，量产之后最大的风险是同质化，选题和冲突设计必须过一道差异化检查。
- **落点模块**：60-casebook、10-theory、90-curriculum

### S-CASE-13 · Nielsen Norman Group：Thinking Aloud, the #1 Usability Tool
- **URL**：https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：NN/g 文章，版权所有；方法本身可自由使用
- **核实**：✅ 已打开核实
- **摘录**：本文发表于 2012-01-15。定义："you ask test participants to use the system while continuously thinking out loud"。三步：招有代表性的用户，给有代表性的任务，然后闭嘴让用户说。优点是便宜、结论稳健、适用于各开发阶段、能说服团队，一天就能学会。缺点是不出统计数据，持续说话不自然，用户可能过滤想法，主持人的干预会改变用户行为。原文："The test facilitator typically has to prompt users to keep them talking"，又提醒"from an untrained facilitator, such interruptions can very easily change user behavior"。
- **对本学院有什么用**：把"冷观众边看边说"写进 playbook：主持者（agent 或真人）只催促说话、不引导，并记录观众第一次想划走的时间码。
- **落点模块**：70-playbooks、50-rubrics

### S-CASE-14 · Nielsen Norman Group：Why You Only Need to Test with 5 Users
- **URL**：https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：NN/g 文章，版权所有；方法可自由使用
- **核实**：✅ 已打开核实
- **摘录**：单个用户约能发现 31% 的可用性问题，5 人约 85%，之后边际收益递减。建议把预算拆开迭代："Spend this budget on 3 studies with 5 users each!"，每轮修完再测。用户群差异明显时（如儿童与家长）：2 类人群每类测 3–4 人；3 类及以上，每类至少 3 人。
- **对本学院有什么用**：给冷观众测试定样本量：每轮 5 人，多轮迭代；季播剧按"新观众"和"追更观众"两类，各 3–4 人。
- **落点模块**：70-playbooks、50-rubrics

### S-CASE-15 · Nielsen Norman Group：Cloze Test for Reading Comprehension
- **URL**：https://www.nngroup.com/articles/cloze-test-reading-comprehension/
- **类型**：article
- **分类**：🟡 需适配
- **许可**：NN/g 文章，版权所有；方法可自由使用
- **核实**：✅ 已打开核实
- **摘录**：做法是"Replace every Nth word in the text with blanks. A typical test uses N = 6"。受测者填空，"synonyms and misspellings are allowed"。达标线是"60% or more right on average"；文中示例 15 个空，答对至少 9 个。cloze 测的是特定受众的实际理解程度，而不只是文本难度，结果受背景知识影响，所以要用真实目标受众来测。
- **对本学院有什么用**：借用 60% 阈值设计"看完复述剧情和空间关系"的理解测试，低于 60% 就判定剧情跳跃或空间混乱。这是方法借用，影视场景下的阈值还需复测。
- **落点模块**：50-rubrics、70-playbooks

### S-CASE-16 · YouTube Help：Audience retention key moments
- **URL**：https://support.google.com/youtube/answer/9314415
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Google 帮助文档，版权所有；平台功能可直接使用
- **核实**：✅ 已打开核实
- **摘录**：Intro 指前 30 秒后仍在看的观众比例。Top moments 是"almost no one dropped off"的时刻；Spikes 是"rewatched or shared"的时刻；Dips 是"either skipped or moments where viewers stopped watching"。曲线平坦表示观众从头看到尾；逐渐下降表示兴趣在流失，原文说 YouTube 视频普遍如此。可以和最近 10 个同长度视频的 typical retention 对比。key moments 要求视频"at least 60 seconds long and have at least 100 views"。
- **对本学院有什么用**：让 agent 把上线后的留存曲线和剪辑表时间码对齐：dip 对应的镜头进复盘，spike 对应的镜头记作有效爽点，写入长期记忆。
- **落点模块**：70-playbooks、40-memory、50-rubrics

### S-CASE-17 · YouTube Help：Test & Compare thumbnails and titles
- **URL**：https://support.google.com/youtube/answer/13861714
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：Google 帮助文档，版权所有；平台功能可直接使用
- **核实**：✅ 已打开核实
- **摘录**：可测"Title only, Thumbnail only, or Title and thumbnail"，最多 3 组。测试优化的是"overall watch time over other metrics, like click-through-rate"，观看时长占比最高的一组胜出。测试"should be completed within two weeks"。结果分三种：Winner、Performed Same、Inconclusive。不显著时，"the first title and thumbnail you upload will be the default"，之后可以手动改。
- **对本学院有什么用**：规定封面和标题 A/B 以观看时长或完播为终判指标，不看点击率，防止标题党。
- **落点模块**：70-playbooks、50-rubrics

### S-CASE-18 · Netflix：The Power of a Picture
- **URL**：https://about.netflix.com/en/news/the-power-of-a-picture
- **类型**：report
- **分类**：🟡 需适配
- **许可**：Netflix 官方新闻稿，版权所有，仅引用
- **核实**：✅ 已打开核实
- **摘录**：作者是 Netflix 产品创意负责人 Nick Nelson，发布于 2016-05-03。会员浏览时，封面图占"over 82% of their focus"，每个标题平均只考虑 1.8 秒。研究发现：带复杂情绪的面孔胜过平静或中性的表情；有争议的角色、反派比正面主角更能带来互动，在动作片和儿童内容里尤其明显；封面超过 3 人时表现明显下降，小屏上更明显；不同地区偏好不同。换用更好的图片后，"streaming hours and engagement"明显上升。注意这是 2016 年的数据，界面早已变化。
- **对本学院有什么用**：给封面 rubric 定初始规则：1–2 张脸、复杂情绪、主角或反派可辨认、不超过 3 人，并按地区做 A/B。
- **落点模块**：50-rubrics、30-taste、70-playbooks

### S-CASE-19 · Wikipedia：Test screening
- **URL**：https://en.wikipedia.org/wiki/Test_screening
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：CC BY-SA 4.0
- **核实**：✅ 已打开核实
- **摘录**：约 90% 的大规模上映片会做试映，平均每片测 3 次；Harold Lloyd 被认为是这一做法的发明者，最早在 1928 年使用。实例：《La La Land》试映观众搞不清是不是歌舞片，导演恢复了被剪掉的高速路开场；《Shaun of the Dead》补拍了一个"15 second"结尾，后续媒体场观众喜欢，有影评人因此加了"an extra star"；《Sunset Boulevard》和《Escape from New York》试映后都删掉了开头一本。Roger Ebert 批评制片方拿试映当武器，结果是"stupid happy endings tacked on after such screenings"。
- **对本学院有什么用**：让 agent 在冷测里加一道类型识别题（"3 秒处你觉得这是什么类型"），同时防止测试结论变成迎合式改结局。
- **落点模块**：10-theory、70-playbooks

### S-CASE-20 · Wikipedia：Pixar（Braintrust 段落）/ Animatic
- **URL**：https://en.wikipedia.org/wiki/Pixar
- **类型**：article
- **分类**：🟡 需适配
- **许可**：CC BY-SA 4.0
- **核实**：✅ 已打开核实（配套条目 https://en.wikipedia.org/wiki/Animatic 亦打开）
- **摘录**：Pixar Braintrust 的描述是"all of its directors, writers, and lead storyboard artists regularly examine each other's projects and give very candid 'notes'"。Pixar 自称"filmmaker-driven studio"，和传统"executive-driven studio"相对；后者由开发部高管向导演下达强制性意见。Animatic 条目：story reel 是"a sequence of still images (usually taken from a storyboard) displayed in sync with rough dialogue (i.e., scratch vocals) or rough soundtrack"，反复修改直到分镜定稿。在 animatic 阶段剪辑，可以避免在最终会被剪掉的场景上浪费动画工作量。
- **对本学院有什么用**：让评审 agent 只写"位置、现象、证据"式的笔记，由导演 agent 逐条裁决；在 H3 视频生成前，先用关键帧加 TTS 做 animatic 冷测。
- **落点模块**：70-playbooks、10-theory、50-rubrics

### S-CASE-21 · Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena（NeurIPS 2023 D&B）
- **URL**：https://arxiv.org/abs/2306.05685
- **类型**：paper
- **分类**：🟡 需适配
- **许可**：arXiv non-exclusive distribution license（仅引用）
- **核实**：✅ 已打开核实（另打开 HTML 全文 https://arxiv.org/html/2306.05685 核对数字）
- **摘录**：摘要称，GPT-4 等强模型评审与人类偏好的一致率"over 80%"，与人与人之间的一致率相当。正文数字：交换两个答案位置后结论一致的比例，GPT-4 为 65.0%，GPT-3.5 为 46.2%，Claude-v1 为 23.8%，多数偏向排在前面的答案。重复列表攻击（只拉长不加信息）下，GPT-3.5 和 Claude-v1 失败率都是 91.3%，GPT-4 是 8.7%。对策：交换顺序跑两次，"only declare a win when an answer is preferred in both orders"；加 3 个 few-shot 示例，GPT-4 一致率从 65.0% 升到 77.5%，成本约为 4 倍；数学题用 reference-guided（评审先独立解题，再对照评判），失败从 14/20 降到 3/20。
- **对本学院有什么用**：评审 agent 必须交换顺序跑两次，不一致就交给人；评审前先独立写出"本集应有什么"，再去看成片。
- **落点模块**：50-rubrics、70-playbooks、10-theory

### S-CASE-22 · Large Language Models are not Fair Evaluators
- **URL**：https://arxiv.org/abs/2305.17926
- **类型**：paper
- **分类**：🟡 需适配
- **许可**：arXiv non-exclusive distribution license（仅引用）
- **核实**：✅ 已打开核实（仅摘要页）
- **摘录**：以 ChatGPT 为评审，只调换候选答案的顺序，"Vicuna-13B could beat ChatGPT on 66 over 80 tested queries"。论文提出三种校准：Multiple Evidence Calibration，先生成多条评判依据再打分；Balanced Position Calibration，把不同顺序的结果汇总；Human-in-the-Loop Calibration，用"balanced position diversity entropy"找出难例交给人工。在 Vicuna Benchmark 上，校准后的结果更接近人类判断。代码和人工标注已公开。
- **对本学院有什么用**：让评审 agent 每个结论先给带时间码的证据再打分，低置信度的样本自动升级给人工。
- **落点模块**：50-rubrics、70-playbooks

### S-CASE-23 · LLM Evaluators Recognize and Favor Their Own Generations
- **URL**：https://arxiv.org/abs/2404.13076
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：CC BY 4.0
- **核实**：✅ 已打开核实（仅摘要页）
- **摘录**：同一个 LLM 既当评估者又当被评估者时，会产生 self-preference 偏差，即"an LLM evaluator scores its own outputs higher than others' while human annotators consider them of equal quality"。不经训练时，GPT-4、Llama 2 区分自己与其他 LLM 和人类输出的准确率就"non-trivial"。作者通过微调实验发现，自我识别能力与自我偏好强度线性相关，受控实验表明这一因果解释不受简单混杂因素影响。作者认为自我识别会干扰无偏评估，也关系到更广泛的 AI 安全。
- **对本学院有什么用**：作为"生成者不能评审自己"的理论依据：独立评审要换模型或隔离上下文，并且看不到生成提示词。
- **落点模块**：10-theory、50-rubrics

### S-CASE-24 · Large Language Models Cannot Self-Correct Reasoning Yet（ICLR 2024）
- **URL**：https://arxiv.org/abs/2310.01798
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：CC BY 4.0
- **核实**：✅ 已打开核实（仅摘要页）
- **摘录**：论文研究"内在自我纠错"（intrinsic self-correction），即没有外部反馈、只靠模型自身能力修正答案。结论原文："LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction"。在推理任务上，这种自我纠错不可靠，还可能把对的答案改错。
- **对本学院有什么用**：为客户的"自我验证循环"定规则：同一 agent 改完再自评"已修复"，不计入通过，必须有外部信号复核。
- **落点模块**：10-theory、50-rubrics、30-taste

### S-CASE-25 · Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge（CALM）
- **URL**：https://arxiv.org/abs/2410.02736
- **类型**：paper
- **分类**：🟡 需适配
- **许可**：arXiv non-exclusive distribution license（仅引用）
- **核实**：✅ 已打开核实（另打开 HTML 全文 https://arxiv.org/html/2410.02736 核对数字）
- **摘录**：论文"identify 12 key potential biases"，并提出 CALM 框架，用"automated and principle-guided modification"自动量化各类偏差。12 类是：Position、Verbosity、Compassion-Fade、Bandwagon、Distraction、Fallacy-Oversight、Authority、Sentiment、Diversity、Chain-of-Thought、Self-Enhancement、Refinement-Aware。其中 Refinement-Aware 指评审是否知道答案经过自我修改，会影响给分。位置偏差的鲁棒率：Claude-3.5 0.832，GPT-4-Turbo 0.818，GLM-4 0.781，GPT-4o 0.776，Qwen2 0.760，ChatGPT 0.566。情绪化措辞下，各模型和情绪条件的鲁棒率在约 0.24–0.97 之间。
- **对本学院有什么用**：评审 prompt 里去掉"第 N 版修改""全部指标已绿""多数人认为"之类字样，防止 Refinement-Aware 和 Bandwagon 偏差。
- **落点模块**：50-rubrics、70-playbooks、10-theory

### S-CASE-26 · FilmAgent: A Multi-Agent Framework for End-to-End Film Automation in Virtual 3D Spaces
- **URL**：https://arxiv.org/abs/2501.12909
- **类型**：paper
- **分类**：🟡 需适配
- **许可**：论文 CC BY 4.0；代码许可未核
- **核实**：✅ 已打开核实（另下载 HTML 全文逐项 grep）
- **摘录**：系统设导演、编剧、演员、摄影四个角色。Critique-Correct-Verify 用于编剧阶段：一个 agent 产出，另一个 agent 批评，前者修改，批评方再验证。Debate-Judge 用于运镜阶段：两名摄影 agent 各自给每句台词分配镜头，就分歧辩论，最后由导演裁决。实现细节："The maximum number of iterations in multi-agent collaboration algorithms is set to 3"。人评 5 分制（Table 2）：Group（GPT-4o）均分 3.98，Solo 3.04，CoT（o1）3.30，CoT（GPT-4o）2.63。情节连贯性从 Solo 的 1.87 升到 Group 的 3.53，运镜从 2.07 升到 3.53。案例：台词约在咖啡馆见面，下一场却在家里；摄影 agent 指出"Tracking Shot is not applicable as Alex is not moving"。
- **对本学院有什么用**：借用 Critique-Correct-Verify（上限 3 轮）和 Debate-Judge 来设计分镜和运镜的独立评审，把"静止人物不配跟拍"写进运镜动机检查。
- **落点模块**：70-playbooks、50-rubrics、20-craft

### S-CASE-27 · MLLM-as-a-Judge（ICML 2024）
- **URL**：https://arxiv.org/abs/2402.04788
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：CC BY 4.0
- **核实**：✅ 已打开核实（仅摘要页）
- **摘录**：基准包含三种评审任务：Scoring Evaluation、Pair Comparison、Batch Ranking。原文结论："MLLMs demonstrate remarkable human-like discernment in Pair Comparison"，但在打分和批量排序上存在"significant divergence from human preferences"，并有"diverse biases, hallucinatory responses, and inconsistencies in judgment, even in advanced models such as GPT-4V"。作者认为 MLLM 要成为可靠的评审，还需要明显改进。
- **对本学院有什么用**：规定视频评审优先用两两比较（新版对旧版、镜头对锚卡参考图），少用 1–10 的绝对分。
- **落点模块**：50-rubrics、10-theory

### S-CASE-28 · Careless Whisper: Speech-to-Text Hallucination Harms（ACM FAccT 2024）
- **URL**：https://arxiv.org/abs/2402.08021
- **类型**：paper
- **分类**：⚪ 仅借鉴
- **许可**：CC BY-NC-ND 4.0
- **核实**：✅ 已打开核实（另打开 HTML 全文核对静默相关表述）
- **摘录**：研究发现"roughly 1% of audio transcriptions contained entire hallucinated phrases or sentences"，即转写里出现音频中根本不存在的整句。其中"38% of hallucinations include explicit harms"，包括宣扬暴力、捏造关联、冒充权威。失语症患者的幻觉率明显更高。全文假设："longer pauses in spoken speech (thereby, with longer periods of background noise in the audio file) could result in more hallucinations"。失语症组的非发声时长平均占 41%，对照组为 15%。
- **对本学院有什么用**：解释委托方 QC 在静音音频上转出"字幕by索兰娅"的原因。规定先做 VAD 或能量门限，静音段的 ASR 输出一律丢弃，不能当作台词存在的证据。
- **落点模块**：50-rubrics、60-casebook、70-playbooks

### S-CASE-29 · VideoHallucer: Evaluating Intrinsic and Extrinsic Hallucinations in Large Video-Language Models
- **URL**：https://arxiv.org/abs/2406.16338
- **类型**：paper
- **分类**：🟡 需适配
- **许可**：CC BY-NC-SA 4.0
- **核实**：✅ 已打开核实（仅摘要页）
- **摘录**：作者称这是"the first comprehensive benchmark for hallucination detection in large video-language models"。幻觉分两类：内在幻觉（object-relation、temporal、semantic detail）和外在幻觉（factual、non-factual）。评测用成对的"基础题/幻觉题"做对抗式二元问答，共测 11 个模型。发现：多数模型幻觉问题严重；扩大数据和参数有助于识别视觉线索和矛盾，但对外在事实性幻觉帮助很小；模型认出事实的能力强于识别幻觉。作者提出的 self-PEP 框架平均提升约 5.38%。
- **对本学院有什么用**：VLM 评审每次混入明知答案为"否"的探针题（问一个画面里确实不存在的物体），答错就作废本次评审。
- **落点模块**：50-rubrics、70-playbooks

### S-CASE-30 · VideoScore: Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation
- **URL**：https://arxiv.org/abs/2406.15252
- **类型**：paper
- **分类**：🟡 需适配
- **许可**：论文 CC BY 4.0；模型权重许可未核
- **核实**：✅ 已打开核实（仅摘要页；姊妹基准 VBench-2.0 https://arxiv.org/abs/2503.21755 亦打开摘要页）
- **摘录**：VideoFeedback 是"the first large-scale dataset containing human-provided multi-aspect score over 37.6K synthesized videos from 11 existing video generative models"。在此数据上从 Mantis 初始化训练出 VideoScore。原文："the Spearman correlation between VideoScore and humans can reach 77.1 on VideoFeedback-test, beating the prior best metrics by about 50 points"。在 EvalCrafter、GenAI-Bench、VBench 上也有提升。VBench-2.0 的摘要写明评估五个维度："Human Fidelity, Controllability, Creativity, Physics, and Commonsense"。
- **对本学院有什么用**：可用作技术层的自动初筛（畸变、物理），但要写明它不评叙事，不能替代人类冷观众。
- **落点模块**：50-rubrics、20-craft

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-CASE-01 | 《山海奇镜之劈波斩浪》共 5 集，正片播放超 5200 万，全网话题曝光超 4.3 亿，登上全平台热搜 21 个。 | [新浪财经](https://finance.sina.com.cn/roll/2024-07-30/doc-incfxvrx6491863.shtml) | 高 |
| F-CASE-02 | 陈坤认为当下能做成熟商业交付的只有"图生视频"工作流，方法是把 AI 难以生成的复杂镜头拆成更小的单元；观众差评集中在"面部表情太僵硬""没有灵魂"。 | [新榜](https://www.newrank.cn/article/detail/26578) | 高 |
| F-CASE-03 | 陈坤在大银幕放映后自评，约 70–80% 的镜头"扛住了这块银幕"，20–30% 还要等技术进步；团队从传统流程的 100 多人降到 10 人左右。 | [极客公园](https://www.geekpark.net/news/338075) | 高 |
| F-CASE-04 | 《三星堆·未来启示录》共 13 集，每集 3–4 分钟，制作中需要不断人工干预和后期优化，保证表情细腻和场景一致；传播总量超 1.4 亿，其中抖音 1.35 亿。 | [人民日报海外版](http://paper.people.com.cn/rmrbhwb/html/2024-08/02/content_26072484.htm) | 高 |
| F-CASE-05 | 《中国神话》共六集（补天、逐日、奔月、填海、治水、尝百草），美术、分镜、视频、配音、配乐全部由 AI 完成。来源没有说明各集是否独立成篇，"一集一个神话"是据集名推断。 | [CCTV](https://www.cctv.com/2024/03/22/ARTImxwnEZa0LYYPusv8E57A240322.shtml) | 高（推断部分为低） |
| F-CASE-06 | 《Air Head》素材比约 300:1；片段以 480p 生成，再用 Topaz 放大；很多片段生成出来是 50–75% 速度，需要重新调速；镜头术语约 6/10 次有效。 | [fxguide](https://www.fxguide.com/fxfeatured/actually-using-sora/) | 高 |
| F-CASE-07 | Neural Viz 每集 2–3 分钟约用 12 小时，工具月费约 100 美元；表演由创作者本人经 Act-One 驱动，用 VHS 质感掩盖渲染瑕疵，用卡通外星角色绕开恐怖谷。 | [The Daring Creatives](https://www.thedaringcreatives.com/creator-stories/the-showrunner-how-neural-viz-makes-an-entire-tv-universe-with-ai/) | 中 |
| F-CASE-08 | ANCESTRA 的体内穿行段先在人体 3D 模型中用虚拟摄像机录草稿镜头，再让 Veo 跟随这条运动生成；出生场景用 Veo 的"add object"把婴儿合成进实拍素材，再做传统 VFX 和调色。 | [Google Blog](https://blog.google/technology/google-deepmind/ancestra-behind-the-scenes/) | 高 |
| F-CASE-09 | Critterz 预算低于 3000 万美元，计划 9 个月完成，目标 2026 年戛纳首映；GPT-5 用于剧本开发，DALL·E 用于概念图，保留人类配音演员和美术。 | [The Ankler](https://theankler.substack.com/p/openai-30m-animated-film-coming-challenge-pixar) | 中（计划性报道，实际映出未核） |
| F-CASE-10 | MiniMax H3 开放权重版为 768p，现行协议限制美国、欧盟、英国、韩国的创作者分发其生成视频；实测在大场面动作和物理互动上弱于 Seedance 2.5，多镜头中角色表情较少。 | [Curious Refuge](https://curiousrefuge.com/blog/minimaxh3-review) | 中 |
| F-CASE-11 | 用 AI 换机位时，Seedance 约保留 90–95% 的原表演，MiniMax H3 的脸和动作偏离更多；对 AI 生成片段再换机位（链式），两个模型都没给出保住原表演的可用远景。 | [Curious Refuge](https://curiousrefuge.com/blog/how-to-change-camera-angles-with-ai-video) | 中 |
| F-CASE-12 | Runway AIF 2026 影片组要求 3–15 分钟、片中含生成视频，并且是"a fully contained, linear narrative"；Grand Prix 片长 7:50，奖金 5 万美元加 100 万积分。 | [Runway AIF](https://aif.runwayml.com/) | 高 |
| F-CASE-13 | 约 90% 的大规模上映片做试映，平均测 3 次；《La La Land》因试映观众搞不清类型，恢复了被剪掉的高速路歌舞开场。 | [Wikipedia: Test screening](https://en.wikipedia.org/wiki/Test_screening) | 中 |
| F-CASE-14 | 单个可用性测试用户约发现 31% 的问题，5 人约 85%；建议做 3 轮、每轮 5 人；2 类人群时每类 3–4 人，3 类及以上每类至少 3 人。 | [NN/g](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/) | 高 |
| F-CASE-15 | cloze 理解测试每 6 个词挖一个空，同义词和错别字算对；平均正确率 60% 以上，才算目标受众能理解。 | [NN/g](https://www.nngroup.com/articles/cloze-test-reading-comprehension/) | 高 |
| F-CASE-16 | YouTube 留存图中，dip 表示被跳过或观众离开，spike 表示被重看或分享；Intro 指标是前 30 秒后仍在看的比例；key moments 要求视频至少 60 秒、至少 100 次观看。 | [YouTube Help](https://support.google.com/youtube/answer/9314415) | 高 |
| F-CASE-17 | YouTube Test & Compare 最多测 3 组标题或缩略图，按观看时长占比判定胜者，原文说明优先于点击率等指标；测试应在两周内完成，不显著时默认用第一组。 | [YouTube Help](https://support.google.com/youtube/answer/13861714) | 高 |
| F-CASE-18 | Netflix（2016）：会员浏览时 82% 以上的注意力在封面图上，每个标题平均考虑 1.8 秒；带复杂情绪的脸胜过中性表情；超过 3 人的封面表现明显下降。 | [Netflix](https://about.netflix.com/en/news/the-power-of-a-picture) | 高（数据年份较老） |
| F-CASE-19 | 交换位置后 LLM 评审结论一致率：GPT-4 65.0%，GPT-3.5 46.2%，Claude-v1 23.8%。重复列表攻击失败率：GPT-3.5 和 Claude-v1 均为 91.3%，GPT-4 为 8.7%。few-shot 把 GPT-4 一致率提到 77.5%。 | [MT-Bench 论文 HTML](https://arxiv.org/html/2306.05685) | 高 |
| F-CASE-20 | 以 ChatGPT 为评审，只调换顺序，就能让 Vicuna-13B 在 80 题中的 66 题上胜过 ChatGPT。 | [arXiv 2305.17926](https://arxiv.org/abs/2305.17926) | 高 |
| F-CASE-21 | LLM 自我识别能力与自我偏好强度线性相关（微调实验）；self-preference 指评审给自己输出的分高于别人，而人类标注者认为两者质量相当。 | [arXiv 2404.13076](https://arxiv.org/abs/2404.13076) | 高 |
| F-CASE-22 | 没有外部反馈时，LLM 难以自我纠错，有时纠错后表现反而下降（ICLR 2024）。 | [arXiv 2310.01798](https://arxiv.org/abs/2310.01798) | 高 |
| F-CASE-23 | CALM 列出 12 类评审偏差，其中包括 Refinement-Aware（是否知道答案经过自我修改会影响给分）和 Bandwagon。六个模型的位置鲁棒率在 0.566（ChatGPT）到 0.832（Claude-3.5）之间。 | [CALM 论文 HTML](https://arxiv.org/html/2410.02736) | 高 |
| F-CASE-24 | FilmAgent 多智能体（协作算法最多迭代 3 次）人评均分 3.98/5，高于单 agent GPT-4o 的 3.04 和 o1 CoT 的 3.30；情节连贯性从 1.87 升到 3.53，运镜从 2.07 升到 3.53；案例中纠正了"给静止人物用跟拍"。 | [FilmAgent 论文 HTML](https://arxiv.org/html/2501.12909) | 高 |
| F-CASE-25 | 多模态大模型评审在两两比较上接近人类，但在绝对打分和批量排序上与人类偏好差距明显，GPT-4V 也存在偏差、幻觉和不一致。 | [arXiv 2402.04788](https://arxiv.org/abs/2402.04788) | 高 |
| F-CASE-26 | Whisper 约 1% 的转写含整句幻觉，其中 38% 带有明确危害；作者认为较长的停顿或背景噪声段更容易触发幻觉。 | [arXiv 2402.08021](https://arxiv.org/abs/2402.08021) | 高 |
| F-CASE-27 | VideoScore 在 VideoFeedback-test 上与人类的 Spearman 相关达 77.1，比此前最佳指标高约 50 分；数据集含 11 个生成模型的 37.6K 个视频。 | [arXiv 2406.15252](https://arxiv.org/abs/2406.15252) | 高 |
| F-CASE-28 | 2026 年春节后，部分短剧平台出现大量剧情框架和冲突设置高度相似的 AI 短剧，导致用户审美疲劳；AI 短剧单集成本约 500–1000 元，传统短剧多在万元以上。 | [澎湃号·湃客](https://www.thepaper.cn/newsDetail_forward_32829833) | 中（自媒体稿，无数据出处） |

## 空白与未找到

1. **WebSearch 额度**：研究员开始时，整个工作流共用的 WebSearch 配额（200 次）已经用完；核实阶段同样无法搜索。所有条目都来自直接抓取已知 URL。中英文多轮检索没有完成，如需补齐，需要放开搜索配额后再跑一轮。
2. **国内 AI 漫剧爆款的一手拆解**：抖音、快手、红果上具体作品的前 3 秒、每集结构、付费卡点，都没有找到一手拆解。《万兽独尊》只有二手数字（S-CASE-12）；研究员提到的《气运三角洲》和腾讯云文章没有提交 URL，也未核实，不收录。
3. **创作者扶持计划**：可灵 NextGen、即梦短剧扶持计划等官方页面没找到；研究员提到可灵官网列出的《Paper Phone》1 亿播放，没有制作细节，也未核实，不收录。
4. **Runway AIF 往届**：2025 届获奖片（如 Total Pixel Space）及获奖者公开的工作流没有核到，往届页面路径 404。2026 届只有获奖名单和规则，没有评审细则或评分表。
5. **Critterz 实际映出**：2026 年戛纳是否实际映出、观众反应如何，均未查到。S-CASE-08 只能当计划性报道使用。研究员提到的"StartupHub 报道的定制 Storyboard 工具"在 Ankler 原文中不存在，也没有给出 StartupHub 的 URL，已删除。
6. **Curious Refuge 姊妹篇**：研究员引用的"2D+实拍工作流"一文，以及"Sometimes the best solution isn't another generation. It's an edit."这句话，不在 S-CASE-11 页面上。也没有给出该文 URL，核实阶段无法搜索，已删除。
7. **Neural Viz 原始报道**：Wired 原文抓取被拒，YouTube 订阅数未核。S-CASE-06 只有一篇二手报道，置信度记为中。
8. **Pixar Braintrust 一手资料**：HBR 和 Fast Company 原文在付费墙后或返回 403，只拿到 Wikipedia 的概括。
9. **试映与观众测试的行业方法**：试映问卷标准题（Top-2-box、definite recommend、NRG/MarketCast 方法）、影视拨盘测试（dial testing）的一手方法文档都没找到。"看完复述剧情"作为影视理解测试的方法论文献也没找到，暂借 NN/g cloze 的 60% 阈值（S-CASE-15），用到影视场景前需复测。
10. **平台官方 A/B 文档**：抖音和巨量引擎的封面 A/B 官方文档、YouTube Shorts "viewed vs swiped away"的官方页面都没核到。Netflix 技术博客的 A/B 原文返回 403，只用了 2016 年的官方新闻稿（S-CASE-18）。
11. **《千秋诗颂》集数**："26 集、每集 7 分钟"只是二手说法，CCTV 页面只提到英文版"六集节目"，未采用。
12. **核实阶段的更正**（相对研究员原稿）：
    - CALM 位置鲁棒率"多数低于 0.70"不符，实际 6 个模型中 5 个在 0.76 以上；情绪条件范围是 0.24–0.97，不是 0.24–0.66。
    - FilmAgent"情节连贯性提高 87%、镜头选择提高 71%"在论文中找不到，改用 Table 2 的原始分数。
    - 《Shaun of the Dead》"分数上升"不符，原文是媒体场观众喜欢新结尾、有影评人加了一星。
    - 《千秋诗颂》的文生声、声线克隆和历史注释属于英文版。
    - 澎湃稿件实为澎湃号·湃客自媒体稿，不是澎湃新闻采编稿。
    - arXiv 论文许可已逐篇改为 arXiv 页面标注的实际许可。
