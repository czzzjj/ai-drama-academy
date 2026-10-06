# 平台发布与流量学（外部调研）

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：28 ｜ 核实方式：逐条 WebFetch 打开核对。GB 45438-2025 PDF 超出 WebFetch 体积上限，改用 curl 下载后以 pdftotext 抽取原文核对；TikTok Creator Academy 两页由 JS 渲染，WebFetch 只拿到导航，改用 curl 取原始 HTML 核对原文句子

## 一句话结论

本专题给学院的主要是发布前的硬门槛和几条有出处的数字锚点。在中国，《微短剧发展管理办法》第三十四条要求 AI 微短剧"在每集明显位置添加提示标识"，GB 45438-2025 把视频显式标识写成可检查的参数：起始画面、画面边或角、字高不低于最短边 5%、持续不少于 2s；抖音、红果、TikTok、YouTube 也各自要求 AI 声明或规定了 AI 剧的准入门槛。"3 秒"能找到的官方锚点是广电总局的有效播放口径（收视时长大于 3s），TikTok 广告建议是 3 秒内给出主张、6 秒内放钩子；集长、集数、付费卡点和节拍公式只有媒体转述的行规，市场数据多是二手转载。仍然缺的有：抖音、红果、快手的官方安全区和上传规格，完播率的官方定义与基准，"AI辅助制作"标注的原文，以及国内平台对 AI 剧分发权重的官方表态。

## 条目

### S-PLAT-01 · 《微短剧发展管理办法》（国家广播电视总局令第16号）
- **URL**：https://www.news.cn/legal/20260731/4b8eea40226644d0a347c72ea1b21b75/c.html
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：政府公开法规文本（新华网刊载），可引用
- **核实**：✅ 已打开核实
- **摘录**：2026-07-27 总局局务会审议通过，2026-09-01 起施行。第二条：微短剧是"单集时长少于二十分钟，主题主线明确、故事情节连续完整、人物角色突出的剧集"。第五条：按投资额度、题材分为一类、二类、三类。第十七条：一类、二类播出前须向省级以上部门申请内容审核和发行许可；三类"由符合条件的播出单位履行内容管理职责，进行播前审核并标注节目编号"。第二十七条：片头"应当在明显位置标注剧名、许可证号、批准文件编号、节目编号"，编剧、导演署名放在首集片头或末集片尾字幕的醒目位置。第二十八条：推广信息"应当与微短剧内容相适配"。第三十四条：使用人工智能技术生成、制作的微短剧，制作机构和播出单位应当"在每集明显位置添加提示标识"。第四十六条：未按备案的内容制作、未按许可通过的内容播出或转移送审的，"可以并处十万元以下罚款"。
- **对本学院有什么用**：agent 在 render 阶段给每一集加 AI 提示标识，片头加剧名和节目编号；verify 阶段把这两项设为发布硬门槛。
- **落点模块**：10-theory、50-rubrics、70-playbooks、40-memory

### S-PLAT-02 · GB 45438-2025《网络安全技术 人工智能生成合成内容标识方法》（原文 PDF）
- **URL**：https://www.sidley.com/en/-/media/resource-pages/ai-monitor/20250314-china-standard-gb-454382025-labeling-method-for-content-generated-by-ai.pdf
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：强制性国家标准文本（编号为 GB，不是 GB/T），可引用；本 URL 是 Sidley 律所网站转存的中文原文 PDF，19 页
- **核实**：✅ 已打开核实
- **摘录**：2025-02-28 发布，2025-09-01 实施。5.4 视频内容显式标识：采用文字提示；同时包含人工智能要素（"人工智能"或"AI"）和生成合成要素（"生成"和/或"合成"）；应位于视频起始画面，可另加在末尾和中间适当位置；位于画面的边或角；字型清晰可辨；"文字高度不应低于画面最短边长度的 5%"；"在视频正常播放速度下，视频内容显式标识持续时间不应少于 2s"。附录 C.4 的示例是在起始画面右下角写"人工智能生成合成"。5.3 音频：用语音标识或"短长 短短"节奏标识（注 1：这是"AI"的摩斯码）；语音标识用正常语速，注 4："汉语正常语速约在 120 字/min～160 字/min"。附录 E（规范性）：文件元数据中加隐式标识扩展字段，字段名或关键词含"AIGC"，值为 JSON 字符串，要素为 Label（1 属于、2 可能、3 疑似）、ContentProducer、ProduceID、ReservedCode1、ContentPropagator、PropagateID、ReservedCode2。
- **对本学院有什么用**：agent 把"起始画面、边或角、字高不低于最短边 5%（1080 宽竖屏即不低于 54px）、持续不少于 2s、文字含 AI 和生成/合成"写成自动检查脚本，并在成片元数据中写入 AIGC 字段。
- **落点模块**：50-rubrics、70-playbooks、20-craft、40-memory

### S-PLAT-03 · 《人工智能生成合成内容标识办法》（网信办等四部门）
- **URL**：https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：政府公开法规文本，可引用
- **核实**：✅ 已打开核实
- **摘录**：国家网信办、工业和信息化部、公安部、国家广播电视总局联合发布，2025-09-01 起施行。第四条：视频"在视频起始画面和视频播放周边的适当位置添加显著的提示标识"，也可加在中间或末尾；音频在起始、末尾或中间适当位置加语音提示或节奏提示；提供下载、导出功能的，"应当确保文件中含有满足要求的显式标识"。第六条：内容传播平台要核验文件元数据中的隐式标识，核验到的在发布内容周边加显著提示；没有核验到、但检测到生成合成痕迹的，标为"疑似生成合成内容"。第十条：用户发布生成合成内容，应当"主动声明并使用服务提供者提供的标识功能进行标识"；"任何组织和个人不得恶意删除、篡改、伪造、隐匿"标识。
- **对本学院有什么用**：agent 上传任何平台都勾选 AI 声明，剪辑和二次封装时不裁掉、不遮挡片头标识，也不擦除文件元数据。
- **落点模块**：10-theory、50-rubrics、70-playbooks

### S-PLAT-04 · 广电总局微短剧"分类分层审核"制度（新华社，2025-02-05）
- **URL**：https://www.news.cn/politics/20250205/3fbf8abbfa344641b01f799ae42a6318/c.html
- **类型**：regulation
- **分类**：🟡 需适配
- **许可**：政府文件的新闻转载，可引用
- **核实**：✅ 已打开核实
- **摘录**：新华社《广电总局：落实微短剧"分类分层审核"制度》。重点微短剧指"符合特殊题材、总投资额度达到100万元及以上、长短视频平台招商主推或在各终端首页首屏推荐播出、自愿按重点微短剧申报等几种条件之一"的，须报省级以上部门规划备案和成片审查，并由总局统一备案公示。普通微短剧：总投资 30 万元（含）至 100 万元且非重点推荐，报省级以上部门备案和审查。其他微短剧：不足 30 万元且非重点推荐，"由播出或为其引流、推送的网络视听平台履行内容管理的职责"，定期报属地省级广电主管部门备案。节目上线前须在片头按格式标注《网络剧片发行许可证》号或节目登记备案号；平台不得上线、引流、推送未标注的微短剧。本条是沿革材料：AI 微短剧的阈值已由 2026-06 的专用标准改为 80 万/30 万（S-PLAT-05），2026-09-01 起另有《管理办法》的一、二、三类体系（S-PLAT-01）。
- **对本学院有什么用**：agent 学习层级判断的逻辑，即先按投资额和题材定层级，再准备对应的片头编号和报备材料；具体阈值以最新文件为准。
- **落点模块**：10-theory、70-playbooks

### S-PLAT-05 · 财联社：广电总局发布 AI 微短剧分类分层标准（2026-06-25）
- **URL**：https://www.cls.cn/detail/2409479
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：新闻报道转述政府文件
- **核实**：✅ 已打开核实
- **摘录**：财联社 2026-06-25《广电总局发布AI微短剧分类分层标准》，原文写"本标准自2026年7月1日起施行"。重点微短剧："投资额度达到80万元及以上，或者主要剧情涉及政治、军事、外交、国家安全、统战、民族、宗教、司法、公安等内容的特殊题材"。普通微短剧："投资额度为30万元（含）至80万元之间、且为一般题材"。其他微短剧："投资额度不足30万元、且为一般题材"。本文没有提到"AI辅助制作"标注，也没有提到 AI 占比红线。本轮没有找到总局发布的原文，也没有找到这套重点/普通/其他分层与《管理办法》一、二、三类之间的官方对应说明。
- **对本学院有什么用**：agent 在立项卡中记录 AI 剧专用的 80 万/30 万阈值和特殊题材清单，用来判断审核层级。
- **落点模块**：10-theory、40-memory、70-playbooks

### S-PLAT-06 · 澎湃：AI 微短剧须标注"AI辅助制作"的说法（2026-07-23，单一来源）
- **URL**：https://www.thepaper.cn/newsDetail_forward_33643733
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章
- **核实**：✅ 已打开核实
- **摘录**：标题为"7月起执行！所有AI微短剧必须标注，无证作品将全面清退"。文中写："按照监管要求，微短剧剧本撰写、画面渲染、配音合成三个环节里，只要任意一项 AI 技术使用占比达到新规划定的红线，剧集就必须在片头位置标注'AI 辅助制作'字样"，并把它归于网络视听司 2026-06-25 发布的《管理提示（AI 微短剧分类分层标准）》。核对结果：同一标准的财联社报道（S-PLAT-05）没有提到这一项；本文没有给出红线的具体数值；本轮没有找到原文。
- **对本学院有什么用**：只作为待核实线索存入记忆，置信度低，不进 rubric 硬门槛；当前的标识硬门槛以《管理办法》第三十四条和 GB 45438-2025 为准。
- **落点模块**：40-memory、10-theory

### S-PLAT-07 · 新京报：红果短剧《关于规范AI剧角色创作的公告》（2026-07-23）
- **URL**：https://www.bjnews.com.cn/detail/1784799185129120.html
- **类型**：article
- **分类**：🟡 需适配
- **许可**：新闻报道（引用平台公告）
- **核实**：✅ 已打开核实
- **摘录**：红果从"角色差异化、版权合规两个维度明确创作标准"。角色差异化方面，"一部剧的主要角色应具备清晰的形象区分度"，鼓励打造有记忆点、高辨识度的角色，"避免不同剧集、不同角色使用高度相似的形象"。版权合规方面，未经授权不得使用他人作品中具有独创性的角色、服装、造型、道具等设计，不得盗用他人享有著作权的写真、美术等作品，使用受版权保护的内容须提前取得合法授权。治理重点是"高频AI脸复用、内容同质化及素材违规三类问题"。7 月 21 日起，对"都市情感、破局成长、家庭温情、都市逆袭等品类AI仿真人剧"，"从画面衔接、人物形象、表情变化、音画同步等方面提出更高要求"。
- **对本学院有什么用**：agent 在角色板阶段做人脸相似度去重（同剧角色之间、跨剧之间），并把画面衔接、人物形象稳定、表情变化、音画同步列为准入级的 rubric 项。
- **落点模块**：50-rubrics、30-taste、60-casebook、20-craft

### S-PLAT-08 · 中新网：红果短剧发布治理公告，一季度下架违规漫剧 1718 部（2026-04）
- **URL**：https://www.chinanews.com.cn/cul/2026/04-07/10599613.shtml
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：新闻报道
- **核实**：✅ 已打开核实
- **摘录**：标题为"红果短剧发布治理公告 一季度下架违规漫剧1718部"。原文："今年一季度，平台已累计下架违反平台治理规范的漫剧1718部"；"目前已完成1.5万部作品的全面核查"，"依规处置违规作品670部"。四类典型违规：擅自使用大众熟知的卡通形象，因无法提供合法授权证明被下架；违规使用 AI 品牌形象与商标标识，涉事剧集两季内容均下架；盗用游戏原创角色形象，人物设定等方面高度相似的作品被下架；AI 生成内容冒用演员形象，因未取得合规授权被处置。平台表示对严重违规采取下架、封号、终止合作和法律追责等措施。
- **对本学院有什么用**：agent 为每张角色板、服装板记录参考来源和授权状态，不以已有 IP 角色、品牌形象或真实演员为参考生成角色。
- **落点模块**：60-casebook、50-rubrics、70-playbooks

### S-PLAT-09 · 凤凰科技：《桃花簪》"AI 偷脸"下架案（2026-04-03）
- **URL**：https://tech.ifeng.com/c/8s1WjF9N52D
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：新闻报道
- **核实**：✅ 已打开核实
- **摘录**：标题为"红果短剧回应'AI偷脸'：下架《桃花簪》 涉事出品方被暂停上传15天"。网友称自己拍摄的照片被"未经授权擅自使用，并通过AI技术进行了内容生成"，剧中"人物角色所穿衣物、配饰以及整体妆容，均与自己的照片高度一致"。红果经 72 小时全面审核，"全面下架短剧《桃花簪》，并暂停该出品方上传所有剧集15天"。文中写："《桃花簪》相关平台播放量曾突破4000万，超2.8万收藏。"
- **对本学院有什么用**：作为案例卡：agent 不用真实人物照片（包括网上的写真）作角色或服装参考图，每张参考图的来源都要可追溯。
- **落点模块**：60-casebook、50-rubrics

### S-PLAT-10 · 科技日报：红果单账户单日上传上限（2026-03-19）
- **URL**：https://www.stdaily.com/web/gdxw/2026-03/19/content_488121.html
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章
- **核实**：✅ 已打开核实
- **摘录**：科技日报 2026-03-19《AI漫剧：告别"草台班子"，走向"掘金赛道"》。文中写："红果短剧规定，单个账户真人剧、漫剧单日上传总量上限为30部"。文章没有给出这条规定的发布时间和原文出处，本轮也没有找到红果的官方文本。这是本轮找到的唯一一条关于红果上传数量限制的说法，属于媒体转述。
- **对本学院有什么用**：agent 规划批量发布时把单账户每日 30 部作为参考上限，正式使用前到红果后台核实。
- **落点模块**：70-playbooks、40-memory

### S-PLAT-11 · 澎湃：抖音升级 AI 内容标识功能（2025-09-01）
- **URL**：https://m.thepaper.cn/newsDetail_forward_31523045
- **类型**：article
- **分类**：🟢 可直接用
- **许可**：新闻报道（平台规则）
- **核实**：✅ 已打开核实
- **摘录**：抖音依据《人工智能生成合成内容标识办法》和配套国标升级 AI 内容标识。创作者可以主动添加 AI 声明。元数据中检测到隐式 AI 标识的内容，展示"作品含AI生成内容"；创作者没有主动标注、平台技术检测认为使用了 AI 的，打上"疑似使用了AI生成技术，请谨慎甄别"。平台提供 AI 内容元数据的读写能力，用于溯源和技术核验。禁止删除、篡改、伪造、隐匿 AI 标识，违者按社区规则处理。
- **对本学院有什么用**：agent 发布到抖音系平台时主动打开 AI 声明，导出时保留隐式元数据，避免被动挂上"疑似"标签。
- **落点模块**：70-playbooks、50-rubrics

### S-PLAT-12 · IT之家：广电总局《网络视听收视指标及计算方法》（2024-01）
- **URL**：https://www.ithome.com/0/746/248.htm
- **类型**：regulation
- **分类**：🟢 可直接用
- **许可**：行业标准（新闻转述）
- **核实**：✅ 已打开核实
- **摘录**：国家广播电视总局 2024-01-18 发布。有效播放须同时满足"播放速率小于 3 倍速"和"收视时长大于 3s"。有效内容触达的收视时长不小于 2s，有效广告触达不小于 1s。"1 分钟内产生多于 60 条收视行为"或"在 1 日内产生多于 10000 条收视行为"的用户视为无效用户，不计入指标。适用于电视、电脑、手机、投屏等终端。
- **对本学院有什么用**：agent 写理论时把"3 秒"锚定在这条官方有效播放口径上，同时注明"90% 死在前 3 秒"一类说法没有一手来源，只是行规。
- **落点模块**：10-theory、50-rubrics

### S-PLAT-13 · 澎湃转载 DataEye 研究院 WAIC 发布：AI 漫剧上半年数据（2026-07-22）
- **URL**：https://m.thepaper.cn/newsDetail_forward_33627271
- **类型**：report
- **分类**：⚪ 仅借鉴
- **许可**：行业报告（媒体转载，仅引用数据）
- **核实**：✅ 已打开核实
- **摘录**：出处是 DataEye 研究院在 WAIC 2026 论坛发布的《2026上半年AI漫剧以及互动影游数据洞察》。2026 年全年市场规模预测 400 亿元，比 2025 年增长 138%，前 5 个月超 220 亿元。上半年抖音端新上作品 22.19 万部，6 月单月上新 3.77 万部（日均超 1200 部）；累计播放增量 5157.38 亿。原文："上半年22.19万部作品中，播放量破亿的仅1055部"，按此计算约 0.48%；文中的"破亿率0.73%"只指 6 月当月上新（破亿 277 部）。AI 仿真人剧播放增量超 4800 亿，占 67.0%，其后是 3D 漫 16%、2D 漫 8%、沙雕漫 6%。番茄以 2297.43 亿播放增量占 TOP15 平台总增量的 67.9%。文中称"每140部作品里，只有1部能跑出来"。
- **对本学院有什么用**：agent 在立项评估中以"上半年破亿约千分之五"为基率设定预期，用冷启动测试决定是否追加投入，不盲目铺量。
- **落点模块**：10-theory、90-curriculum、40-memory

### S-PLAT-14 · 新华网（转载解放日报）：《中国微短剧行业发展白皮书(2025)》数据（2026-01-15）
- **URL**：https://www.news.cn/ent/20260115/6c93a5532af346a38166083dba3df00e/c.html
- **类型**：report
- **分类**：⚪ 仅借鉴
- **许可**：协会报告（媒体转载）
- **核实**：✅ 已打开核实
- **摘录**：标题为《微短剧从"爽感狂飙"到迈向精品化》，白皮书由中国网络视听协会发布。用户规模 6.96 亿；相关企业 10.02 万家；2025 年竖屏剧预计上线 4 万部；2025 年 1-8 月 AI 漫剧累计上线 2902 部。海外微短剧市场 2025 年 1-8 月收入 15.25 亿美元，同比增长 194.9%；海外应用下载约 7.3 亿次，同比增长 370.4%。本文没有"2025年产值892亿元"这一数字。
- **对本学院有什么用**：agent 在课程导论中用协会口径的规模数据说明赛道，不使用来源不明的数字。
- **落点模块**：10-theory、90-curriculum

### S-PLAT-15 · 中国作家网（转载文汇报）：《中国网络视听发展研究报告(2026)》数据（2026-04-16）
- **URL**：https://www.chinawriter.com.cn/n1/2026/0416/c404003-40702348.html
- **类型**：report
- **分类**：⚪ 仅借鉴
- **许可**：协会报告（媒体转载）
- **核实**：✅ 已打开核实
- **摘录**：标题为《网络视听铸就新大众文艺主阵地》，引用《中国网络视听发展研究报告（2026）》的三组数据。一是"微短剧人均单日使用时长129分钟，同比增长28.4%，使用时长已超过长视频"；二是"重点网络微短剧上线625部，同比增长30.21%"；三是"2025年全行业AI生成视音频累计超20亿条，较2024年增长14倍以上"。报告原文本轮没有打开，以上数字都来自这篇转载。
- **对本学院有什么用**：agent 在课程导论中说明用户时长和 AI 内容供给的规模，作为"观众注意力竞争激烈"的背景数据。
- **落点模块**：10-theory、90-curriculum

### S-PLAT-16 · 虎嗅：漫剧经营数据（2026-10-01）
- **URL**：https://m.huxiu.com/article/4895036.html
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：媒体文章（仅引用事实）
- **核实**：✅ 已打开核实
- **摘录**：标题为《没看过姜月初，朋友说我"有点土"》。引 QuestMobile：红果 DAU 2026 年 7 月达 1.68 亿，同比增长 107%。漫剧"人均单日使用时长达90.7分钟，比真人短剧板块的72分钟高出26%"；"AI漫剧的平均完播率和转发分享数据比真人短剧高出约30%"。"万播收益，从2025年下半年的30—100元，跌至2026年的5—10元，跌幅近90%"。"精品AI短剧制作成本在800—1500元/分钟，单部约10万元"；流量投放"约占全链路总成本的70%"，"成熟投流团队的ROI也只稳定在1.03—1.07的微利区间"；"90%以上的漫剧公司不赚钱"；"2026年一季度，全行业上线微短剧约12.8万部，其中AI微短剧占比超过95%"。除 DAU 外，其余数字的原始出处本轮没有逐一核对。
- **对本学院有什么用**：agent 由此理解在免费广告变现模式下，单集完播和追更时长直接决定收益，所以把留存指标放在 rubric 首位；成本数字只作量级参考。
- **落点模块**：10-theory、40-memory、90-curriculum

### S-PLAT-17 · CBNData：《千亿短剧市场，上演付费"局中局"》（2024-03-25）
- **URL**：https://www.cbndata.com/information/292345
- **类型**：article
- **分类**：🟡 需适配
- **许可**：媒体文章（仅引用行规）
- **核实**：✅ 已打开核实
- **摘录**：CBNData 转载定焦的文章（作者王璐）。小程序付费短剧"指单集时长在一到两分钟的微短剧"，"一部短剧大概有100集"。前几集免费，"一般第10集左右是第一个付费点"，"后续还有20集、30集等付费卡点"；编剧"会非常重视前10集的内容，然后在9-10集卡点留足钩子"。单集约 1 元，全集购买从 9.9 元到 100 元以上不等。"一部收入1000万的短剧，在投流上大概要花出去800万"。这些是 2024 年付费模式下的行规描述，不是官方标准。
- **对本学院有什么用**：agent 做付费版季规划时把第一个大卡点放在第 9-10 集附近；做免费广告版时不直接套用，并注明这是 2024 年付费模式的行规。
- **落点模块**：20-craft、90-curriculum、50-rubrics

### S-PLAT-18 · 人人都是产品经理：《微短剧，风再起》（2024-01-03）
- **URL**：https://www.woshipm.com/it/5969019.html
- **类型**：article
- **分类**：🟡 需适配
- **许可**：媒体文章（仅引用行规）
- **核实**：✅ 已打开核实
- **摘录**：文中给出行业节拍公式："15秒有冲突或反转，30秒要推进剧情，最后10秒给出悬念"。"爽剧"单集 1-2 分钟，80-100 集或更多，用户通过小程序付费观看；精品短剧单集 3-4 分钟、约 20 集，以抖音为主，采用部分集数付费解锁。市场规模：2021 年 36.8 亿元，2022 年 101.7 亿元，2023 年 373.9 亿元。付费逻辑转向小程序和应用内付费后，按投流回收数据"以销定产"，ROI 目标 1.2 以上。
- **对本学院有什么用**：agent 给每集套用"15s 冲突/30s 推进/末 10s 悬念"节拍模板作为起点，同时注明这是行规，不是官方规定。
- **落点模块**：20-craft、90-curriculum、50-rubrics

### S-PLAT-19 · 东方财富（转载证券日报）：多平台 10 月起实施短剧激励新则（2026-09-30）
- **URL**：https://wap.eastmoney.com/a/202609303887585279.html
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：财经媒体报道
- **核实**：✅ 已打开核实
- **摘录**：标题为《多平台10月起实施短剧激励新则 真人短剧热度再起？》。抖音 10 月 1 日起"首发真人短剧默认参与"激励，要求"竖屏、总时长不少于70分钟"，按上线后 30 天的自然免费模式数据考核，单部"激励上限60万元"。微信 10 月 16 日至 12 月 31 日按用户播放时长结算，"最高可享受100%收入激励"，"不区分真人短剧、AI仿真人短剧"。优酷（至 2027 年 3 月 31 日）按热力值综合评分发阶梯奖金，"单合作方月度最高可获10万元奖励"，属于分账之外的额外激励。
- **对本学院有什么用**：agent 选择发布平台时核对激励是否覆盖 AI 剧（抖音这项只覆盖真人剧，微信不区分），并可把"总时长不少于 70 分钟"作为季长度的参考。
- **落点模块**：70-playbooks、40-memory

### S-PLAT-20 · Meta Ads Guide：Instagram Reels 广告规格与安全区
- **URL**：https://www.facebook.com/business/ads-guide/update/image/instagram-reels
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：Meta 官方文档（引用参数）
- **核实**：✅ 已打开核实
- **摘录**：该页是 Reels 图片广告（Image）规格：9:16，推荐 1440×2560。原文："Consider leaving roughly 14% of the top, 35% of the bottom, and 6% on each side of your asset free from text, logos, or other key creative elements to avoid cropping key elements or covering them with the profile icon or call-to-action." 这是本轮找到的唯一给出明确百分比的官方安全区。本目录据此换算（不是原文）：1080×1920 约为上 269px、下 672px、左右各 65px。注意这是广告投放规格，自然发布的 Reels 界面遮挡未必相同。
- **对本学院有什么用**：agent 在 render 阶段以 14/35/6% 作为可配置的默认禁区，自动检查硬字幕和标题卡是否落入；AI 标识按国标须放在边或角，要在禁区之外的边角位置找落点，避免被界面遮挡。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-PLAT-21 · TikTok Ads 帮助中心：广告创意最佳实践（附竞价信息流广告规格）
- **URL**：https://ads.tiktok.com/help/article/creative-best-practices?lang=en
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：TikTok 官方文档
- **核实**：✅ 已打开核实
- **摘录**：原文："Prioritize your hook in the first 6 seconds to boost engagement and increase watch time."；"Introduce your content proposition in the first 3 seconds for better recall and awareness."；"We recommend displaying 5-10 words per second when using text."。竖屏 9:16，至少 720P；内容要留在安全区内；每个广告组放 3-5 条不同创意。规格页 https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads?lang=en 写明安全区大小"is determined by the dimension (vertical, horizontal, or square), ad caption length, and any additional formats used"，只提供可下载模板，不给百分比；9:16 最低 540×960；非 Spark Ads 最长 10 分钟。两页都是广告投放语境，不是自然内容规范。
- **对本学院有什么用**：agent 把"3 秒主张/6 秒钩子"作为开场节拍的参考上限；字幕密度按每秒 5-10 个英文词估算，中文的等效值需要自测。
- **落点模块**：20-craft、50-rubrics、10-theory

### S-PLAT-22 · TikTok Creator Academy：Elements of a TikTok video
- **URL**：https://www.tiktok.com/creator-academy/en/article/elements-of-tiktok-video?lang=en
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：TikTok 官方创作者教程
- **核实**：✅ 已打开核实
- **摘录**：原文建议画面"centered and not having it covered by any buttons on the screen"；"Consider having an attractive element early on in your video that sparks interest, ideally within the first 5 seconds, to hook viewers and get them to stop scrolling."；"Over 30% of TikTok survey respondents shared that they actually watch videos on mute, and rely on captions for context."；"videos with background music added have an average of +98.31% more views per video compared to those without background music"。竖屏或全屏模式下的横屏都可以发布。98.31% 是平台自报的对比数据，没有说明统计方法，只能看作相关关系。
- **对本学院有什么用**：agent 做出海版本时坚持烧录字幕（放在安全区内）以照顾静音观看的用户，并在开场 5 秒内给出吸引元素。
- **落点模块**：20-craft、70-playbooks、10-theory

### S-PLAT-23 · TikTok Creator Academy：AI-generated content label
- **URL**：https://www.tiktok.com/creator-academy/en/article/ai-generated-content-label
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：TikTok 官方创作者教程
- **核实**：✅ 已打开核实
- **摘录**：页面把 AI 生成内容定义为由 AI 制作或改动的任何图像、视频或音频，包括逼真场景，也包括动漫、卡通、绘画等艺术风格。原文："Our Community Guidelines require that content that uses AI or includes significant edits to show realistic-looking people or scenes be clearly disclosed." 需要披露的情形包括把一张脸换成另一个人的脸、让人看起来说了没说过的话等。操作方法：发布视频时点 More options，打开"AI-generated content"设置。原文注明："Turning on the AI-generated content setting won't affect the distribution of your video as long as it doesn't violate our Community Guidelines."
- **对本学院有什么用**：agent 在 TikTok 发布 AI 仿真人剧时默认打开 AI 标签；平台称打标不影响分发。
- **落点模块**：70-playbooks、50-rubrics

### S-PLAT-24 · YouTube Help：Shorts 时长与 Content ID、缩略图、浏览量计数
- **URL**：https://support.google.com/youtube/answer/15424877?hl=en
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：YouTube 官方帮助中心
- **核实**：✅ 已打开核实
- **摘录**：answer/15424877：2024-10-15 及之后上传、方形或竖屏、不超过 3 分钟的视频归为 Shorts；"Any Short that is over one minute in duration with an active Content ID claim of any type, including manual claims, will be blocked globally on YouTube."，声明解除后恢复。answer/10343433（https://support.google.com/youtube/answer/10343433）：Shorts 不能上传自定义缩略图，只能"choose a frame from your Short"；标题"max 100 characters"。answer/2991785（https://support.google.com/youtube/answer/2991785）："Beginning August 24, 2026"，所有格式（含 Shorts、长视频、直播）在开始播放时即计一次 view；YPP 收益仍按"engaged views"和"engaged watch hours"计算。
- **对本学院有什么用**：agent 发布超过 1 分钟的单集时避开任何受 Content ID 保护的配乐，每集预先设计一个可选作封面的帧，复盘时把 views 和 engaged views 分开看。
- **落点模块**：70-playbooks、50-rubrics、20-craft

### S-PLAT-25 · YouTube Help：生成式 AI 内容披露
- **URL**：https://support.google.com/youtube/answer/14328491?hl=en&co=GENIE.Platform%3DDesktop
- **类型**：official-doc
- **分类**：🟢 可直接用
- **许可**：YouTube 官方帮助中心
- **核实**：✅ 已打开核实
- **摘录**：上传时在 YouTube Studio 的"AI use"设置中选 Yes 或 No。可以不披露的有三类：一是不逼真的 AI 内容，如动画、奇幻场景、绿幕特效；二是小幅编辑，如美颜滤镜、调色、特效、字幕、音频修复，以及用自己克隆的声音做配音；三是脚本、缩略图生成等制作辅助。原文："Creators who consistently choose not to disclose this information may be subject to manual application of a label, or penalties from YouTube, including removal of content or suspension from the YouTube Partner Program." YouTube 也可能通过内部系统、C2PA 元数据等方式自动加标。
- **对本学院有什么用**：agent 发布 AI 仿真人剧到 YouTube 时把"AI use"设为 Yes；纯动画风格的漫剧是否算"不逼真"，先人工判断再决定。
- **落点模块**：70-playbooks、50-rubrics

### S-PLAT-26 · Instagram 官方博客：Trial Reels
- **URL**：https://creators.instagram.com/blog/instagram-trial-reels
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：Instagram 官方博客
- **核实**：✅ 已打开核实
- **摘录**：2024-12-10 开始推出。"Trial reels will be shown to non-followers first"；试播期间不出现在粉丝的 Feed、Reels 标签页和主页网格。"Approximately 24 hours after you share a trial reel, you can view key engagement metrics in the reels viewer – including views, likes, comments and shares"。可以设置为在"within the first 72 hours"内达到表现阈值时自动分享给粉丝，设置可随时调整。资格要求见帮助中心，本页没有写明账号类型。
- **对本学院有什么用**：agent 把"同一集准备 2-3 个开场或封面变体，先推给非粉丝，24-72 小时后按数据选择"写进冷启动测试 playbook，用陌生观众的数据代替自评。
- **落点模块**：70-playbooks、50-rubrics、90-curriculum

### S-PLAT-27 · Filmustage：Short Drama Apps Compared: ReelShort vs DramaBox in 2026
- **URL**：https://filmustage.com/blog/short-drama-apps-compared-reelshort-vs-dramabox-in-2026/
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：第三方博客（仅引用数据）
- **核实**：✅ 已打开核实
- **摘录**：2026-05-06 发布。每部 60-90 集，前 5-10 集免费；主体拍摄 7-10 天；单部预算 15-25 万美元，平台全球买断版权；制片费约为预算的 10-15%（引 Vitrina 2025 数据）。ReelShort 的编剧室不用 AI，AI 只用于 VFX 和后期。DramaBox 母公司称 AI 把单集成本从约 8000 美元降到 2000 美元，但文章注明这指动态漫画产出，不是美国真人原创剧。ReelShort 美国用户日均使用 35.7 分钟（Omdia 2025Q4 数据）。文中引 Sensor Tower 的 2025Q1 全球内购收入：ReelShort 1.3 亿美元，DramaBox 1.2 亿美元。
- **对本学院有什么用**：agent 做出海版本时参考"60-90 集、前 5-10 集免费"的格式；成本数字只作量级参考。
- **落点模块**：10-theory、90-curriculum、70-playbooks

### S-PLAT-28 · Sensor Tower：State of Short Drama Apps 2026
- **URL**：https://sensortower.com/blog/state-of-short-drama-apps-2026-report
- **类型**：report
- **分类**：⚪ 仅借鉴
- **许可**：第三方数据报告（仅引用数据）
- **核实**：✅ 已打开核实
- **摘录**：2026 年 6 月发布。2026Q1 短剧应用下载超 8.5 亿次，同比增长 140%；内购收入约 7.5 亿美元，同比增长 20%；DramaBox 和 ReelShort 当季内购收入各约 1.4 亿美元。下载的地区分布为东南亚 32%、拉美 23%、印度 22%，三地都是三位数同比增长，合计占全球下载的 75% 以上。下载同比增速（140%）远高于收入同比增速（20%）。
- **对本学院有什么用**：agent 安排出海本地化时优先考虑东南亚和拉美；下载与收入增速之间的差距说明新增市场的付费能力弱，免费广告模式的完播和留存更重要。
- **落点模块**：10-theory、90-curriculum、70-playbooks

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-PLAT-01 | 《微短剧发展管理办法》（总局令第16号）2026-09-01 施行。第三十四条：使用人工智能技术生成、制作的微短剧，须"在每集明显位置添加提示标识"；第二十七条：片头须在明显位置标注剧名、许可证号、批准文件编号、节目编号。 | [新华网·微短剧发展管理办法](https://www.news.cn/legal/20260731/4b8eea40226644d0a347c72ea1b21b75/c.html) | 高 |
| F-PLAT-02 | 《管理办法》第十七条：三类微短剧由符合条件的播出单位播前审核并标注节目编号；一、二类须向省级以上部门申请内容审核和发行许可。 | [新华网·微短剧发展管理办法](https://www.news.cn/legal/20260731/4b8eea40226644d0a347c72ea1b21b75/c.html) | 高 |
| F-PLAT-03 | GB 45438-2025 视频显式标识：文字提示须同时含"人工智能/AI"和"生成/合成"，位于起始画面的边或角，字高不低于画面最短边的 5%，正常播放速度下持续不少于 2s。 | [GB 45438-2025 PDF](https://www.sidley.com/en/-/media/resource-pages/ai-monitor/20250314-china-standard-gb-454382025-labeling-method-for-content-generated-by-ai.pdf) | 高 |
| F-PLAT-04 | GB 45438-2025 附录 E：文件元数据隐式标识字段名含"AIGC"，值为 JSON，要素为 Label（1 属于/2 可能/3 疑似）、ContentProducer、ProduceID、ReservedCode1、ContentPropagator、PropagateID、ReservedCode2。 | [GB 45438-2025 PDF](https://www.sidley.com/en/-/media/resource-pages/ai-monitor/20250314-china-standard-gb-454382025-labeling-method-for-content-generated-by-ai.pdf) | 高 |
| F-PLAT-05 | GB 45438-2025 注 4：汉语正常语速约为 120～160 字/min（约 2～2.7 字/s），这是国标中关于语音标识语速的注释，可作为官方"常速"参考。 | [GB 45438-2025 PDF](https://www.sidley.com/en/-/media/resource-pages/ai-monitor/20250314-china-standard-gb-454382025-labeling-method-for-content-generated-by-ai.pdf) | 高 |
| F-PLAT-06 | 《人工智能生成合成内容标识办法》第十条：用户发布 AI 生成内容须主动声明并使用平台的标识功能；任何组织和个人不得恶意删除、篡改、伪造、隐匿标识。第六条：平台对检测到生成痕迹的内容标"疑似生成合成内容"。 | [网信办·标识办法](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm) | 高 |
| F-PLAT-07 | AI 微短剧分类阈值（2026-07-01 起）：投资 80 万元及以上或特殊题材为重点；30 万（含）至 80 万的一般题材为普通；不足 30 万的一般题材为其他。目前只有媒体转述，未找到原文。 | [财联社](https://www.cls.cn/detail/2409479) | 中 |
| F-PLAT-08 | 有媒体称 AI 占比达到红线的微短剧须在片头标注"AI 辅助制作"；只有澎湃一家这样写，同一标准的财联社报道没有提到，原文未找到，红线数值也未给出。 | [澎湃](https://www.thepaper.cn/newsDetail_forward_33643733) | 低 |
| F-PLAT-09 | 广电总局收视口径：有效播放＝收视时长大于 3s 且播放速率小于 3 倍速；有效内容触达不小于 2s，有效广告触达不小于 1s。这是"3 秒"的官方锚点。 | [IT之家](https://www.ithome.com/0/746/248.htm) | 高 |
| F-PLAT-10 | TikTok 广告创意建议：前 3 秒引出内容主张，前 6 秒优先放钩子；使用文字时每秒 5-10 个词。属于广告投放语境。 | [TikTok Ads 创意最佳实践](https://ads.tiktok.com/help/article/creative-best-practices?lang=en) | 高 |
| F-PLAT-11 | TikTok Creator Academy：吸引元素最好在前 5 秒内出现；超过 30% 的受访者静音观看、依赖字幕；加背景音乐的视频平均多 98.31% 播放（平台自报，未说明方法）。 | [TikTok Creator Academy](https://www.tiktok.com/creator-academy/en/article/elements-of-tiktok-video?lang=en) | 高 |
| F-PLAT-12 | TikTok 要求逼真的 AI 人物或场景内容必须披露，并称打开"AI-generated content"设置不影响分发（前提是不违反社区准则）。 | [TikTok AI 标签](https://www.tiktok.com/creator-academy/en/article/ai-generated-content-label) | 高 |
| F-PLAT-13 | Meta Reels 广告安全区：顶部约 14%、底部约 35%、左右各约 6% 不放文字、logo 和关键元素（9:16，1440×2560，图片广告规格页）。 | [Meta Ads Guide](https://www.facebook.com/business/ads-guide/update/image/instagram-reels) | 高 |
| F-PLAT-14 | TikTok 竞价信息流广告的安全区随画幅、caption 长度和附加组件变化，官方只给模板不给百分比；9:16 最低 540×960。 | [TikTok In-Feed Ads 规格](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads?lang=en) | 高 |
| F-PLAT-15 | 红果 2026-07 公告：主要角色须有清晰的形象区分度，避免不同剧集、不同角色使用高度相似的形象；治理"高频AI脸复用"；7 月 21 日起，都市情感等品类 AI 仿真人剧在画面衔接、人物形象、表情变化、音画同步上门槛更高。 | [新京报](https://www.bjnews.com.cn/detail/1784799185129120.html) | 高 |
| F-PLAT-16 | 红果 2026 一季度下架违规漫剧 1718 部，核查 1.5 万部，处置 670 部；典型违规之一是"AI生成内容冒用演员形象"。 | [中新网](https://www.chinanews.com.cn/cul/2026/04-07/10599613.shtml) | 高 |
| F-PLAT-17 | 《桃花簪》案：网友照片被 AI 生成为剧中角色，红果经 72 小时审核后全剧下架，出品方暂停上传 15 天；该剧下架前播放量曾突破 4000 万。 | [凤凰科技](https://tech.ifeng.com/c/8s1WjF9N52D) | 高 |
| F-PLAT-18 | 有媒体称红果规定单个账户真人剧、漫剧单日上传总量上限为 30 部；未找到平台原文。 | [科技日报](https://www.stdaily.com/web/gdxw/2026-03/19/content_488121.html) | 中 |
| F-PLAT-19 | 抖音对元数据含隐式 AI 标识的内容展示"作品含AI生成内容"，对未标注但检测为 AI 的内容打"疑似使用了AI生成技术，请谨慎甄别"。 | [澎湃·抖音 AI 标识](https://m.thepaper.cn/newsDetail_forward_31523045) | 高 |
| F-PLAT-20 | YouTube：2024-10-15 后上传的竖屏或方形、不超过 3 分钟的视频算 Shorts；超过 1 分钟且有任何有效 Content ID 声明的 Short 会被全球屏蔽。 | [YouTube Help 15424877](https://support.google.com/youtube/answer/15424877?hl=en) | 高 |
| F-PLAT-21 | YouTube：逼真的 AI 内容须在 Studio 把"AI use"设为 Yes；动画、奇幻等不逼真的内容可以不披露；持续不披露可能被强制加标、删除内容或暂停 YPP。 | [YouTube Help 14328491](https://support.google.com/youtube/answer/14328491?hl=en&co=GENIE.Platform%3DDesktop) | 高 |
| F-PLAT-22 | YouTube Shorts 不能上传自定义缩略图，只能从视频中选帧；标题最多 100 字符。 | [YouTube Help 10343433](https://support.google.com/youtube/answer/10343433) | 高 |
| F-PLAT-23 | YouTube 自 2026-08-24 起，所有格式在开始播放时即计一次 view；YPP 收益仍按 engaged views 和 engaged watch hours 计算。 | [YouTube Help 2991785](https://support.google.com/youtube/answer/2991785) | 高 |
| F-PLAT-24 | Instagram Trial Reels 先推给非粉丝，约 24 小时后可看 views、likes、comments、shares，可设置在 72 小时内达到阈值后自动推给粉丝。 | [Instagram 官方博客](https://creators.instagram.com/blog/instagram-trial-reels) | 高 |
| F-PLAT-25 | 2026 上半年抖音端新上 AI 剧漫剧 22.19 万部，破亿 1055 部（约 0.48%）；文中"破亿率 0.73%"只指 6 月当月上新。 | [澎湃·DataEye](https://m.thepaper.cn/newsDetail_forward_33627271) | 中 |
| F-PLAT-26 | 红果 DAU 1.68 亿（2026-07，QuestMobile）；漫剧人均单日时长 90.7 分钟，真人剧 72 分钟；万播收益从 2025 下半年的 30-100 元跌到 2026 年的 5-10 元；投流约占全链路成本 70%。 | [虎嗅](https://m.huxiu.com/article/4895036.html) | 中 |
| F-PLAT-27 | 行规（非官方，2024 年付费模式）：小程序付费短剧单集 1-2 分钟、约 100 集，约第 10 集开始收费，后续在第 20、30 集等设卡点。 | [CBNData](https://www.cbndata.com/information/292345) | 中 |
| F-PLAT-28 | 行规节拍公式（非官方）："15秒有冲突或反转，30秒要推进剧情，最后10秒给出悬念"。 | [人人都是产品经理](https://www.woshipm.com/it/5969019.html) | 中 |
| F-PLAT-29 | 海外竖屏剧（ReelShort/DramaBox）：60-90 集，前 5-10 集免费，单部预算 15-25 万美元，平台买断全球版权。 | [Filmustage](https://filmustage.com/blog/short-drama-apps-compared-reelshort-vs-dramabox-in-2026/) | 中 |
| F-PLAT-30 | 2026Q1 全球短剧应用下载超 8.5 亿次（+140%），内购收入约 7.5 亿美元（+20%）；DramaBox 和 ReelShort 各约 1.4 亿美元；东南亚、拉美、印度分别占下载 32%、23%、22%。 | [Sensor Tower](https://sensortower.com/blog/state-of-short-drama-apps-2026-report) | 中 |
| F-PLAT-31 | 抖音 2026-10-01 起的真人优质短剧激励要求竖屏、总时长不少于 70 分钟，按上线 30 天自然免费数据考核，单部上限 60 万元，只面向真人剧；微信同期激励不区分真人剧和 AI 仿真人剧。 | [东方财富](https://wap.eastmoney.com/a/202609303887585279.html) | 中 |
| F-PLAT-32 | 中国网络视听协会白皮书：微短剧用户 6.96 亿；海外微短剧 2025 年 1-8 月收入 15.25 亿美元（+194.9%）。 | [新华网·白皮书](https://www.news.cn/ent/20260115/6c93a5532af346a38166083dba3df00e/c.html) | 中 |

## 空白与未找到

1. **国内平台的安全区与上传规格**：抖音、红果、快手都没有找到官方的 9:16 安全区像素规范。唯一给出百分比的是 Meta（S-PLAT-20），而且是广告规格；TikTok 只提供模板。抖音的 3:4 封面裁切只是从业者说法。红果版权方后台的上传规范（封面尺寸、单集时长、集数下限）没有公开文档；单账户日上传 30 部的说法只有媒体转述（S-PLAT-10）。
2. **"AI辅助制作"标注与 AI 占比红线**：只有澎湃一家转述（S-PLAT-06），财联社对同一标准的报道没有提到，总局原文没有找到。2026-06 的 AI 微短剧分类分层标准原文、它与《管理办法》一/二/三类的对应关系，本轮也都没有找到。
3. **抖音 2026-05《动画微短剧(漫剧)内容创作建议》**：没有公开原文，只有媒体转述，本目录没有收录。研究笔记中提到的"穿模""音画不同步""服化道不一致"、封面不得写"热播/强推"等条目，未经核实。
4. **完播率的官方定义与基准**：抖音创作者学院、巨量引擎对"完播率""3 秒/5 秒完播率"的官方定义和基准值没有抓到（页面需要登录或由 JS 渲染）。"黄金 3 秒""90% 死在前 3 秒""50% 第 2 秒划走"都没有一手数据，只能按行规处理；官方锚点只有 S-PLAT-12 的有效播放口径。
5. **YouTube Shorts 分析指标**：研究笔记称"Shown in feed"和"viewed vs swiped away"的定义在 support.google.com/youtube/answer/12942217，但本次打开该页没有找到这两个指标的定义，所以没有收录。研究笔记还称 YouTube Test & Compare 只支持长视频、不支持 Shorts，本次没有核实。
6. **快手、B 站、视频号**：只拿到 2024-2025 年的分账或扶持数字，没有 2026 年的集长规范；视频号只有激励比例（S-PLAT-19），没有官方的原生短剧格式要求。抖音合集、追剧提醒、自动连播只找到旧报道，没有 2026 年的官方说明。
7. **AI 剧的分发权重**：没有找到国内主流平台对"AI 剧是否单独限流或降权"的官方表态；唯一的官方说法是 TikTok 称 AI 标签不影响分发（S-PLAT-23）。
8. **数字口径**：白皮书的"2025年产值892亿元"在新华网原文中不存在（S-PLAT-14），不要引用。破亿率有两种口径：上半年约 0.48%（1055/22.19 万），6 月当月 0.73%，引用时须注明分母。研究笔记中的"破千万约 5.8%"在 DataEye 转载文中没有出现，已删除。《中国网络视听发展研究报告(2026)》原文没有打开，只核对了转载。
9. **本次核实的限制**：核实过程中 WebSearch 配额已用尽，以上空白没能再通过搜索补充，下一轮可以继续查。
