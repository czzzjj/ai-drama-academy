# zenstory-ai/drama-skills 深度评估

> 采集日期：2026-10-06 ｜ 来源性质：外部调研（非委托方实证）｜ 条目数：32 ｜ 核实方式：逐条打开核对。github.com/zenstory-ai/drama-skills 下的条目对照本地克隆核对（HEAD `c2426e0`，经 `git ls-remote` 确认与 origin/main 为同一提交），并抽样用 WebFetch 打开在线页面；其余外部条目逐条 WebFetch

## 一句话结论

zenstory-ai/drama-skills（MIT，GitHub releases 页标注 v0.8.1 为 Latest，2026-09-28）能给学院的有：一套「五份 Markdown + 稳定 ID」的创作文档格式、一个跨文档机械校验脚本、prepare→confirm→run 生产闸门的强化版、审查 finding 格式与四档结论、MiniMax H3 提示词方言，以及一份 H3 / Seedance / Wan 的小样本行为观察。它缺的是：ComfyUI 节点、帧网格（17k+5）、cfg=1 条件下的任何数据；Qwen-Image 出图配方；能看片的媒体审查方法（审查 skill 明写「本套件不查看媒体」）；平台发布与运营、系统化声音设计、调色、打斗编排。它的模型观察样本很小，盲判由单一模型完成，只能当待复测的假设。

## 条目

### S-ZEN-01 · drama-skills 总路由 skill：short-drama/SKILL.md
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：总入口 skill，负责项目初始化（`project_tool.py init`，已确认时带上 `--language/--prompt-language/--aspect-ratio/--episode-count/--target-seconds`）、跨阶段路由表（每类请求对应一个 owner skill 和它的文档）、制作形态与 Look Development 决策，以及本地 Dashboard（`--detach` 独立进程）。执行规则：只有真实创作分叉才询问，不拿 schema、目录或检查器问创作者；不自动开始用户没点名的审查、归档或生产。用户在会话里点名目标视频模型而 `production_profile` 仍是 `unset` 时，先按「决策记录 → publish → accept → set-authority」写进 `short-drama.json`，否则下一轮会退回通用路径。`rhythm_profile` 只有 `accepted` 才做算术核对。`export` 附 manifest 与 checksums，`asserts_approval` 恒为 `false`。
- **对本学院有什么用**：学院总入口 skill 按「路由表 + 不做什么 + 模型档案落盘」来写：agent 听到「按 H3 写」时，先把 H3 的时长区间、参考方式、提示词语言（委托方为 T-2 的帧网格档案）写进项目配置，再进入下游阶段。
- **落点模块**：70-playbooks、90-curriculum、40-memory

### S-ZEN-02 · short-drama-novel-analyze：长篇原著 S0–S5 分析管道
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-novel-analyze/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：管道分六段。S0 用 `novel_index.py` 建章节索引，它是唯一切片真源：识别阿拉伯与中文数字章号，只认一种编号单位，剔除开头目录块，`problems` 非空就停。S1 抽样快评（`sample --count 12`，结果确定、首尾必取，第一行写覆盖率），然后停下问创作者是否继续。S2 逐章功能提取（可并发子代理，每批 5–8 章），覆盖率不足不进 S3。S3 聚合剧情单元与节奏，附按观众收益排名的爽点表。S4 人物归并，描述性称谓与头衔永远不触发合并。S5 给出改编价值和分集候选，按爽点分布切，不按章号或字数平均切，并回填 S1 哪些判断被推翻。不成段复制原文；分析只是候选，交 develop 定案。
- **对本学院有什么用**：改编类季播项目照此执行：agent 先抽样快评再全量拆，以脚本索引为唯一切片真源，按观众收益切分集，不按章节平均切。
- **落点模块**：20-craft、70-playbooks、10-theory

### S-ZEN-03 · short-drama-develop：故事引擎、分集地图与节奏档案
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-develop/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：产出 creative-brief、story-engine、director-brief（仅作候选）、adaptation-map.jsonl、series-arc.json、episode-map.jsonl。episode-map 每集记录进入状态、开场、当集追求、阻力、方向性转折、当集结果、信息释放、出去的压力和下一集必须继承的事实。候选方向必须机制不同（主角策略、对抗来源、代价或持续冲突方式），不能只换标题。题材卡共 15 张，一次只读一张，不进交付物；重生、系统这类「前提装置」要先给边界与代价。制作形态定下后，按默认值提出节奏档案交创作者接受。它引用的 episode-design.md 另规定：首集入口至少比较时序、收益、冷开三个候选（STY-25）；门槛集停在揭晓前一秒（STY-27）。
- **对本学院有什么用**：学院季级弧线与追更模块采用它的分集契约字段（进入状态 / 当集结果 / 出去的压力 / 继承事实），agent 规划几十集时逐集写清交接。
- **落点模块**：10-theory、20-craft、30-taste、70-playbooks

### S-ZEN-04 · short-drama-write：可拍中文剧本格式与写作规则
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-write/SKILL.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：每集只维护一份 `剧本.md`。一级标题 `# EP001 集名`，场景 `## EP001-SC001 内 · 地点 · 时间/天气`，对白 `角色（可选表演提示）：台词`，生产标签 `[VO]` `[OS]` `[SFX]` `[画面文字]` `[连续性]` `[转场]`。规则：每场改变信息、权力、关系、情绪、物理状态或风险；自己写的对白初稿回读一遍，转不成演员动作或表情的句子删掉或改成动作；全集第一拍自身是钩子（SCR-22）；用 `[VO]` 交代信息时读「能演的不说」；已接受档案 `end_on_peak` 为 `true` 时停在峰值。没有语速或动作段速率时只报可数事实，不猜秒数；交稿前静默做经济性检查，删掉输入没要求的精确数字和机关。
- **对本学院有什么用**：学院剧本层可直接采用这套 Markdown 格式和标签，agent 写剧本时让每场有可见状态变化、第一拍自成钩子、能演的不说。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-ZEN-05 · short-drama-assets：身份/变体/镜头瞬态拆分与视觉设定
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-assets/SKILL.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：把剧本拆进 `视觉设定.md`，区分四类：身份（换了就不是同一人、地、物）、变体（服装、伤势、时段、天气、开合、持有状态）、镜头瞬态（姿势、视线、左右手、站位、机位，归分镜）、故事语义（归写作 / 开发）。每项先写不变的识别锚点，再写本集状态；含混指代不猜；识别锚点必须可见、可生成、可比较。提示词语言不是中文时，人物条目必须写「画面代称」（正文拼写或「无」）。跨镜出现、观众看得出不一致的可见事实才写连续性锁。references/character-and-look.md 补充：锚点里至少一条侧面成立、一条背面成立；全组尺度次序带一个绝对参照；临时淤青、制服、雨水、当天妆容不能当持久锚点（AST-04）。
- **对本学院有什么用**：针对脸漂移、克隆脸、生成器乱加饰物：agent 拆资产时按身份 / 变体 / 瞬态三层写可比较的锚点和尺度次序，不写空泛质量词。
- **落点模块**：20-craft、50-rubrics、40-memory

### S-ZEN-06 · short-drama-image-prompts：角色/场景/道具板提示词
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-image-prompts/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：每项写成 `## IMG-... · 中文名`，正文放在 `### 可复制提示词` 引用块里；`IMG-...` 只是提示词条目 ID，不代表图片已经存在。写作顺序：主体与身份锚点 → 当前变体 → 构图/视角 → 光色/材质 → 背景边界 → 禁止项。被连续性锁点名的条目，锁面原样写进正文。可见文字、logo、水印、界面、字幕要明确允许或禁止。references 里文字政策分两层：资产来源政策（`exact_readable / graphic_only / no_readable_text / pending_creator_text`）和呈现方法（`readable / symbolic / blank / postproduction`）；多视图板要写明画面内无视图标签、引线箭头、尺寸标注和图注。正文不放占位符、路径或 QA 结论。
- **对本学院有什么用**：学院板图课程借用这套配方顺序（common-recipe 为八项）和两层文字政策，再补上委托方 T-1 的 1696×2528、40 步、多 seed 规格和 Qwen-Image 专用的反文字、反水印写法。
- **落点模块**：20-craft、70-playbooks、50-rubrics

### S-ZEN-07 · short-drama-storyboard：有职责的分镜与冻结关键帧
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-storyboard/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：每镜写来源（剧本场景 ID 加短引文）、时长、目的、景别/机位、运镜（行为、起止、理由，固定也写理由）、起点 → 唯一动作 → 终点（人物、双手、持物怎样完成状态转换）、声音（对白估时依据）。冻结关键帧只投影起点；收尾关键帧可选，只投影终点。关键帧成稿后再回填三条依据：视觉依据（必写）、图片提示词项、输入参考图（REF / PLAN / 待补 / 明确文生）。`用途` 封闭词表 9 个。镜长先按叙事定，短于模型下限的镜头向创作者提议装进多镜容器。同一集用同一句画风词，每场一句光与色温，并先出一张中远景定调图只约束色调。
- **对本学院有什么用**：对治「片段式剧情跳跃」和「运镜无动机」：agent 每镜写唯一动作链和运镜理由，上镜终点就是下镜起点；镜长下限换成委托方 T-2 的约 5.2 秒。
- **落点模块**：20-craft、50-rubrics、70-playbooks、30-taste

### S-ZEN-08 · short-drama-video-prompts：视频提示词与模型方言路由
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：生成路径由分镜的「输入参考图」决定：有 REF 或 PLAN 是图生；只有创作者明确选择才是文生；待补则停下，并同时给出三条路（把已有图放进项目绑成 REF、写 PLAN 挂图计划、明确改走文生）。方言按 `target_video_model` 路由，只读命中的一份：Seedance 2.0 / 2.5、MiniMax H3、Wan 3.0。字段依次为分镜、时长、生成方式、输入参考图、静态视觉锚点、起始帧、状态链、终点。正文直接声明全镜任何时刻都不生成非画内字幕和 caption；同轨声音写成完整时间线，逐字对白只出现一次；连续段同时绑定上一段实际视频和实际尾帧。镜头时长不在原生区间内就回分镜修订，不在正文里暗改。
- **对本学院有什么用**：针对字幕烧录、对白溢出：agent 写 H3 提示词时逐镜声明不生成字幕、写全声音时间线，不在提示词阶段改分镜的起止和时长。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-ZEN-09 · MiniMax H3 提示词方言（minimax-h3.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/references/minimax-h3.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：推荐档案：`native_duration_seconds` 4–15，模式 text / first_frame / first_last_frame / reference，声音 same_pass。模式由各参考图的 `用途` 组合决定：无图、只有起始帧、起始帧 + 结束帧用三段（integrated_multimodal_description / overall_soundscape / non_diegetic_music）；起始帧再加角色板或场景板，必须整组走 full-reference 六段，因为首尾帧与 `reference_*` 互斥。`<Picture N>` 按「顺序」编号。对白写 `<d>[Chinese]…</d>`，说话人用稳定 `(S1)`；口型绑定靠两句（交代谁在画内、音色，并明写其他正脸 lips remain completely closed）。无配乐写 `N/A`。多镜容器要求逐切挂关键帧加对齐句。素材上限 9 图、3 视频、3 音频。中文约 4.1 可发声字/秒。文件写 H3-Max「不支持 full-reference」，与 2026-10-06 官方 API 页不符（见 F-ZEN-28）。
- **对本学院有什么用**：学院 H3 方言课的底稿：agent 按参考图用途选三段还是六段、按「顺序」编 `<Picture N>`、用两句写法锁口型；委托方「first_frame + 六段」的写法要在 ComfyUI 节点上核实。
- **落点模块**：20-craft、70-playbooks、40-memory、50-rubrics

### S-ZEN-10 · short-drama-produce：预览→确认→执行的生产闸门
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-produce/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：硬闸门四步不可合并：建一个有边界的 job（一种 modality、明确数量、prompt、参考、参数、输出路径、adapter profile）；跑 `prepare` 展示完整预览，不调用供应商，并机械核对可复制正文与参考槽位，任一漂移 fail closed；创作者看完预览后明确确认，才跑 `confirm`（`CONFIRM <id> <code>`，绑定 job 指纹，job、prompt、参数、输出路径任一变化即失效）；`run` 消费这次确认。「继续」「预算没问题」都不算确认。中断后 `audit` 报 `orphaned_provider_job`，用 `collect` 取回已计费的结果，不重投、不需新确认。失败三路：技术失败有上限重试；被拒点名哪项输入就改哪项；重复内容缺陷回到 owner。adapter 以 argv + JSON stdin 调用，不走 shell，凭据只从环境读取。
- **对本学院有什么用**：把委托方 P6 的 prepare→confirm→run 升级为「确认绑定 job 指纹 + 中断后先 collect 不重投 + 失败按被拒输入路由」，并按它的 adapter 契约写一个 ComfyUI adapter。
- **落点模块**：70-playbooks、50-rubrics、20-craft

### S-ZEN-11 · short-drama-edit：剪辑单 + check/render/verify
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-edit/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：进入条件是素材文件当前可读，job 成功或 adapter 返回成功都不算。流程：逐段看完整素材，先标可用带（起势静止、结尾漂移、发白、动作回弹、多余重复表演）；有台词的镜先定位发声区间；每段写「取舍：入点=理由；出点=理由」，理由写画面上发生了什么，不写「节奏需要」。字幕逐字取自剧本，转写只用来定位时间。未采用镜头写理由，区分「文件缺失」和「质量不可用」。剪辑能取舍上游，不能改写上游。`check` 只核对；`render` 切段、同场景自动接镜、烧字幕与画面文字、统一响度（edit_tool.py 用两遍 loudnorm，TP=-1.5、LRA=11）；`verify` 只报数字（含切点前后亮度差超过 20 的切点、疑似坏帧），不给质量结论。
- **对本学院有什么用**：针对「指标全绿但成片不行」：agent 交付时把实测数字和看过、听过的判断分开写，技术成功不写成质量结论；字幕不取自 ASR。
- **落点模块**：20-craft、50-rubrics、70-playbooks、60-casebook

### S-ZEN-12 · short-drama-review：独立证据审查
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-review/SKILL.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：优先由未参与当前版本创作的 reviewer 审查，自检要如实声明（stage-contract 的 REV-04）。审查与修改是两个工作单元。审查范围 10 个：source_analysis、story_script、assets_continuity、image_prompts、storyboard_keyframes、video_prompts、production_outputs、full_episode、delivery_privacy、project_calibration。先查可证明的事实（ID、时长、引用、连续性、同轨声音、泄漏），再带证据审内容。每条 finding 写位置、短引文或冲突事实、观众或制作影响、修订结果、owner、严重度（blocker / major / minor / note）和规则等级。结论分 APPROVE、APPROVE_WITH_NOTES、REVISE、PROVISIONAL。不能只说「AI 味」「不够电影感」；无法读取媒体时，不从文字推断脸部一致、表演、口型或混音。
- **对本学院有什么用**：学院 rubric 的 finding 格式和四档结论照搬，并要求审查 agent 与创作 agent 隔离上下文，打破委托方 F1 的自我验证闭环。
- **落点模块**：50-rubrics、70-playbooks、10-theory

### S-ZEN-13 · 五份创作文档模型（creator-documents.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama/references/creator-documents.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：文件自述是「建议格式，不是 schema」。每集维护五份 Markdown：剧本、视觉设定、分镜、图片提示词、视频提示词（剪辑单在素材生产后另记，见总路由 SKILL）。规定了标题语法：`## <人物|造型|地点|道具> · 名称`、`## SHOT-…`、`## MOTION-…`、`## IMG-…`。三类依据不得混用：图片提示词项（IMG）、输入参考图（REF / PLAN）、视觉依据（文字事实）。REF 槽位唯一语法为 `REF-<slot>（顺序：<n>）· 路径《中文名》（用途；控制；不得控制）`。输入参考图有四种准备结果；视频文档的输入参考图必须与分镜逐字一致；正文里引号或 `<d>` 中的中文必须能在剧本或视觉设定里找到。可复制提示词整段是一条，一次提交。
- **对本学院有什么用**：学院 skill 格式借鉴这一点：每层决定只住一份人可读的文档，用稳定 ID 跨文档引用，检查脚本才能机械对账。
- **落点模块**：70-playbooks、90-curriculum、40-memory

### S-ZEN-14 · creator_markdown_check.py：五文档跨文档机械校验器
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama/scripts/creator_markdown_check.py
- **类型**：tool
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：1740 行脚本，只用标准库（argparse、json、re、pathlib 等）。核对一集五文档的可执行契约：标题 ID 唯一且带中文名；SHOT 与 MOTION 对应、时长一致；来源场景存在，未拍场次带理由；REF / PLAN / 参考音频语法正确，顺序从 1 连续，用途属于封闭词表；关键帧正文点名的条目必须进视觉依据；连续性锁面在关键帧、视频、IMG 正文逐字出现，写在否定词之后或粘在别的词上的匹配不算；`<d>` 或引号内连续 4 个以上汉字要能在剧本找到（VID-25）；仍有待补参考图时禁止出最终视频提示词。报错写明原因和改法。
- **对本学院有什么用**：学院 check 脚本照这个套路写：每条结构规则有脚本兜底，报错给改法，并核对提示词里的台词逐字来自剧本。
- **落点模块**：50-rubrics、70-playbooks

### S-ZEN-15 · 跨镜一致性锁（continuity-lock.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-assets/references/continuity-lock.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：识别锚点写给人读，执行端只读得到每条提示词自己的正文，所以要给跨镜不变的事实上锁。三条同时成立才上锁：在本集两个以上镜头出现（或一镜加一张资产板）；观众能看出不一致；不随剧情改变，状态不上锁。一集里的锁通常是个位数。锁面是提示词语言写的最小名词短语（「颜色 + 材质/形制 + 物体」，例 `pale blue chunky knit wool sweater`），不含动作和剧情；在生效范围内必须逐字出现在图片提示词、冻结关键帧、视频提示词正文里，不能以「参考帧已交代」为由删掉（CON-07，structural_invariant）。语法为 `LOCK-…《中文名》（镜头：全集或 SHOT 列表；图片提示词项：IMG…）· 锁面：…`。
- **对本学院有什么用**：解决服装、道具跨镜漂移：agent 只给少量不变事实上锁，并把锁面逐字带进每条 Qwen 关键帧和 H3 提示词，可与委托方 P1 锚点卡的「锚点句 EN」对齐。
- **落点模块**：20-craft、50-rubrics、40-memory

### S-ZEN-16 · duration_estimate.py：按项目声明语速的剧本时长估算
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-write/scripts/duration_estimate.py
- **类型**：tool
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：脚本自述「只报数字，不判断」。套件不内置跨项目语速，只用 `short-drama.json` 里声明的 `spoken_characters_per_second` 和 `seconds_per_action_paragraph`；没声明时只报对白字数和动作段数，并说明秒数无法推出。`[VO]` / `[OS]` 计入发声时长。不自己解析剧本，依赖 `screenplay_index.py` 的块索引。write SKILL 提醒：`dialogue_characters` 含标点，不能直接按「可发声字/秒」换算。项目接受了节奏档案时额外报 `vo_share` 与上限。仓库实跑日志（evaluations/让你管账号/reference-run/RUN-LOG.md）记载旧版把 `[VO]` 计为 0 秒，一集漏计 30.8 秒（报 64.0 秒，实为 94.8 秒），已修复。
- **对本学院有什么用**：学院时长核算可直接用它：项目档案登记委托方 T-2 实测的 7.5 字/秒（容量上限），并另记 4.1 字/秒（zenstory 观察到的自然语速），让 agent 在剧本阶段就发现对白溢出。
- **落点模块**：50-rubrics、70-playbooks、40-memory

### S-ZEN-17 · 模型行为观察摘要（model-behavior-probes.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md
- **类型**：report
- **分类**：⚪ 仅借鉴
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：2026-09-08 至 09-28 的探索性观察，经中转服务或 WorkRally 平台调用，不是 ComfyUI。人工判断先去掉臂身份、打乱顺序，判断者为同一个模型，不是独立人评；文件声明不构成能力、成功率或质量保证。H3 部分：写 `non_diegetic_music: N/A` 的 14 次无配乐；同镜头 20 次中文对白，自然语速约 4.1 字/秒，较密输入赶词或截断；对白镜比计划多约 1.5–2.5 秒；「Fixed camera.」4 次无位移，不写机位句 28 次中 4 次推拉或平移；写接触点的终点 4/4 有效，写厘米数无效；无起始帧时加取景字段后 8 次中 7 次中景；真实尾帧续接一组 NCC 0.91–0.99，另一组 3 次中 1 次仅 0.27；两个男声区分度差。另含 Seedance 与 Wan 对照。
- **对本学院有什么用**：作为学院 40-memory 的初始假设库：agent 在委托方 ComfyUI H3（cfg=1、帧网格）上逐条复测后再晋升为规则，不直接当定律。
- **落点模块**：40-memory、60-casebook、10-theory、20-craft

### S-ZEN-18 · 评估体系 README（回归闸门 + 跨题材盲评门禁 + 实跑）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/README.md
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：MIT（仓库）；其中原著文本按 README 说明版权归仓库所有者，限作评估基准与工作流示例
- **核实**：✅ 已打开核实
- **摘录**：评估分两层。回归闸门（unittest）重放《让你管账号》实跑录下的产物：20 章原著 → 437 个情节点 → 24 个分集候选 → EP001 20 镜，94.8 秒对目标 90 秒，只判断有没有退步，不看戏写得好不好。主工作流实跑要在固定提交的 worktree 上从原著跑到视频提示词，记录哪一步需要人替系统解决问题。内容门禁：16 个合成案例（12 个 development、4 个只跑一次的 holdout，另有负对照），每 arm 3 个 replicate，Codex 与 Kimi 各自交换 A/B 盲评，一轮 192 份报告；生成器与 judge 都在净化的临时工作区运行；holdout 一旦促成修改即退役。教训：上一轮最重的缺陷是 SKILL.md 写的做法与脚本实际行为不一致，而测试全绿。
- **对本学院有什么用**：学院打破自我验证闭环照此做：创作与评审隔离、跨模型盲评、一次性 holdout，并把「文档说的和脚本做的是否一致」单列为发布前检查项。
- **落点模块**：50-rubrics、90-curriculum、10-theory

### S-ZEN-19 · 剧本盲评量表 v5（content-quality-rubric.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/content-quality-rubric.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：只评单集剧本文本，总分 100：hook_payoff 15、causality 15、character 15、dialogue_action 15、visual_drama 10、pacing_retention 10、prompt_fidelity 10、genre_fit 10。统一五档锚点：0–20% 缺失或反效果，25–40% 可辨但薄弱，45–60% 成立，65–80% 强，85–100% 卓越；文本更长、格式正确、用了更多物件或数字都不自动加分。每维给整数分，并引用 A/B 各自的证据。过拟合诊断标签：forced_choice、forced_evidence_procedure、forced_deadline、case_echo、mechanical_rule_display；负对照案例的候选作品不得出现这些标签。门禁要求两个 split 与全语料不退步，单案例跌幅不超过 2 分。
- **对本学院有什么用**：直接作为学院 50-rubrics 的剧本层量表：agent 审剧本时逐维引证打分，并检查是否把局部技巧套成了模板。
- **落点模块**：50-rubrics、30-taste

### S-ZEN-20 · 制作形态卡（production-form-profiles.md + form-cards/ 六张）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama/references/production-form-profiles.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：视觉风格不是贴在提示词前的标签，要先写一张 production-form card，记九项：叙事职责、身份锚点载体、连续性载体、层级拆分、形与识别、材质与光色、运动预算、声音与文字、变与不变。判据：删掉一条描述后提示词一字不变，它就只是标签。六张形态卡：实拍、二维动态漫、风格化三维、水墨笔触、Q 版表达、国漫二次元，各卡小节含叙事职责、身份锚点载体、连续性载体、层级拆分、光与材质词汇、运动预算、声音与文字职责、跨阶段传递、常见失效。实拍卡把可执行的光定义为来源 + 方向 + 遮挡 + 反射 + 叙事用途，列「电影感、高级灰、大师光、氛围感」为不可执行写法。形态卡默认是 craft_default，审查不得单凭形态卡阻断。
- **对本学院有什么用**：学院色彩与光线、表演设计模块按「形态卡九项」组织，agent 定风格时写成能改变提示词字段的条目，不用风格标签。
- **落点模块**：30-taste、20-craft、10-theory

### S-ZEN-21 · 分集设计与项目节奏档案（episode-design.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-develop/references/episode-design.md
- **类型**：repo
- **分类**：🟡 需适配
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：节奏档案起点值（AI 真人 / 漫剧）：first_hook_seconds 5（一组实测 5 部里 3 部在前 5 秒给出第一个钩子）；beat_interval_seconds_max 30（取「每 20–30 秒一个情绪触点」的上沿）；opposed_reversals_per_episode_min 1；end_on_peak true；reprise_previous_last_beat true；vo_share_max 0.3（未实测）；target_avg_shot_seconds 2.5（真人实测；漫剧 3.0 未实测）；close_shot_share_min 0.45（漫剧未实测）；first_major_payoff_by_episode 1。文件明写这些是起点，不是质量线。门槛集位置由创作者定，套件无默认；创作者已声明门槛并请求建议时，才可举经验区间作例：第一道约第 8–16 集，第二道约第 25–30 集。门槛处停在揭晓前一秒，钩子分台词钩和画面钩。
- **对本学院有什么用**：学院平台与留存模块的数值起点：agent 用 5 秒首钩、30 秒触点、集尾停峰值核剧本；2.5 秒平均镜长要靠 H3 多镜容器或长生成后剪辑实现，不能压成 2.5 秒的生成单元（委托方 T-2 下限约 5.2 秒）。
- **落点模块**：10-theory、50-rubrics、30-taste

### S-ZEN-22 · 镜头手艺（shot-craft.md）：运镜逐镜选、对白估时、镜长推导
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-storyboard/references/shot-craft.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：运镜对照表（SHT-04）：人物移动本身是这一镜的事就跟拍或横移；新信息从画外进来就摇、俯仰或后拉；台词或认识压到某人身上就缓推或前移，停在承受者脸上；关系在原地被重新评估就环绕；高度本身有意义才升降；情绪爆发、重大反转用短促推近；以上都不成立才固定，固定也写理由。强调手段只有短促推近、定格、闪白三种，只留给峰值。对白估时：先排完整声音事件再定镜长，不让人物加快语速硬塞台词，放不下就拆到说话者和听者的镜头上。镜长由声音事件与目标平均镜长推出，不按字数折算（SHT-28）。对白场默认一句一镜、给听者反应、交锋用正反打（SHT-29）。竖屏空间靠纵深分层交代。
- **对本学院有什么用**：对治「运镜无动机」和「对白溢出」：agent 写每一镜的运镜都要能对上表里一行并写出理由，对白先估时再定镜长。
- **落点模块**：20-craft、50-rubrics、30-taste

### S-ZEN-23 · 制作质量检查与改写回归（production-quality-gates.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-review/references/production-quality-gates.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：列出跨环节常见返工原因六类：覆盖丢失、表演只有标签、空间与状态漂移、文本与声音边界混乱（exact-readable 与全局 no-text 冲突、参考图带水印或字幕却只加负面词、VO/OS 写成对口型等）、负面补丁淹没动作、版本和执行状态冒充内容权威。REV-09 指令优先级：已确认的故事事实与对白/文字 > 镜头覆盖、目的、起止与时长 > 资产身份与连续性 > 创作者确认的视觉方向与制作配置 > 目标模型条件 > 装饰性偏好。附「改写前后回归表」：每次重写或压缩提示词，都比对原文覆盖、镜头目的、起止时长、资产、对白与项目配置有没有丢。给出合格 finding 范例；不合格写法举例为「镜头太少、不够电影感、没有按参考比例、AI 味重」。
- **对本学院有什么用**：学院 50-rubrics 的生产层采用六类返工原因和优先级，agent 每次压缩或改写提示词后填回归表，证明没丢台词和起止边界。
- **落点模块**：50-rubrics、60-casebook、70-playbooks

### S-ZEN-24 · 项目级校准与结果处置（project-calibration.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-review/references/project-calibration.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：观察分两种：`input_reference`（参考图本身的可见事实）与 `generated_result`（某个准确提示词、参考和配置下的结果）；后者只支持项目内校准，不自动升格为跨项目定律。拿到诊断后先在五种处置里选一种：保留、后期处理、局部编辑、重新提交（有上限，只用于看起来随机的失败）、改写（同一缺陷重复出现时改结构：拆镜、减并发、换实现路径）。两条判据：缺陷是否落在文字能控制的范围内；同一缺陷是否已复现。不要用叠加「高质量、避免变形、保持一致」这类词回应重复缺陷。修订单变量，写 change_set 与 preserve_set。试跑按项目风险挑有代表性的镜头，不随机抽样。
- **对本学院有什么用**：学院 QC playbook 照此规定：agent 发现缺陷先选处置再动手，同一缺陷第二次出现就改结构而不是重抽，防止把抽卡当方法。
- **落点模块**：70-playbooks、50-rubrics、40-memory

### S-ZEN-25 · 动作的可生成性（generability.md，VID-21）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/references/generability.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：只在项目声明由生成模型承担画面时适用。判据一句：这个动作在普通生活影像里是否大量出现。放心写：走进来、坐下、回头、递东西、接过、抱住、推开门、放下、翻页。四类高风险写法：精确拦截、不可见的内部状态（「神色一凛」）、否定式动作（「没有接话」）、三步以上的手部编排链；另外厘米级位移、单指精确操作、把微表情当承重信息也要改。戏剧信息来自常见动作的组合与时机。改写顺序：换承担者 → 拆到相邻镜 → 换成停留 → 交给声音 → 标为高风险并给降级实现。改写不得改变镜头边界、起止状态和剧本事实。
- **对本学院有什么用**：学院动作与打斗课的底层约束：agent 把打斗写成「接近—接触—施力—结果」这类高频整体动作和接触点，不写模型做不出的精细编排。
- **落点模块**：20-craft、50-rubrics

### S-ZEN-26 · 字幕与声音规范（sound-and-subtitles.md）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-edit/references/sound-and-subtitles.md
- **类型**：repo
- **分类**：🟢 可直接用
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：竖屏短剧默认硬字幕，文字逐字取自剧本，转写只辅助定位。烧录时按 GY/T 288 与短剧惯例改写显示形式：去掉句末标点，保留问号和感叹号，句中逗号、句号、顿号、分号、冒号换成全角空格。字幕一行显示，超过 12 字在句中停顿处拆成先后几条。字高为画面高度 4.3%，深色描边 0.42%，基线距底边约 24%，避开平台底部界面。字色按来源区分（edit SKILL：对白白色，系统 VO 青色，重点词黄色）。内置 render 不执行 ducking、交叉淡入或配乐进入，写了声音方案不等于已经混音。两遍响度测量也不保证恰好达标，要测编码后的实际 LUFS 与真峰。
- **对本学院有什么用**：学院成片渲染采用这套字幕参数和「字幕不取自 ASR」规则，从根上避免委托方 D5 中转写工具在静音上幻听出「字幕by索兰娅」这类错误进入字幕。
- **落点模块**：20-craft、50-rubrics、70-playbooks

### S-ZEN-27 · DESIGN.md：单页创作台设计
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/DESIGN.md
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：Dashboard 设计文档（Status: Active，Last refreshed 2026-08-06）。单页布局为「内容目录 + 始终可见的正文 + 待办与导出提示」，不提供 tab、弹窗文档查看器、高级模式、工程模式或原始文件视图。进度从五份可见文档与媒体推断（未开始、创作中、提示词就绪、已有媒体），不另建生命周期文件。保存不触发外部生产，生产确认与导出交回对话。问题卡写场景/镜头、观众或制作影响、预期结果、直接动作，不显示内部严重度名、审查者身份和存储路径。实现只用 Python 标准库与原生 HTML/CSS/JS，要求只监听回环、Host/Origin 校验、原子保存和并发编辑保护。注意：当前总路由 SKILL 描述的 Dashboard 已有每集六个视图和 ⌘K 搜索，与本文的单页设计不完全一致。
- **对本学院有什么用**：学院若给人类主创做审片面板，借鉴「问题卡写观众影响而不写内部状态」和「界面不冒充它做不到的动作」两条。
- **落点模块**：90-curriculum、70-playbooks

### S-ZEN-28 · 维护者 know-how 晋升流程（short-drama-knowhow）
- **URL**：https://github.com/zenstory-ai/drama-skills/blob/main/maintainers/skills/short-drama-knowhow/SKILL.md
- **类型**：repo
- **分类**：⚪ 仅借鉴
- **许可**：MIT
- **核实**：✅ 已打开核实
- **摘录**：维护者专用：从授权的只读文本源学习完整项目链，把私有观察转成公共规则候选，不碰媒体。原则：语义判断交给 agent，脚本只做格式校验、比对、查重与隐私扫描；统计只用来安排下一次读什么，不能从频次、排名或相关性推出创作规则；每条候选都要带证据、反例或失败情形、冲突解释、适用边界和置信度。流程：observation 卡 → decision 卡 → 题材 × 机制 coverage matrix（不填出现次数或成功率）→ 去标识与 de-copy → fresh-agent 盲测 → 独立 reviewer → promotion 或 retire。promotion-ledger 的决定有 promotion、narrow-and-retest、hold、retire 四种，hold 与 retire 同样记录。
- **对本学院有什么用**：学院 40-memory 的经验晋升照此设计：agent 从每次生产失败写观察卡，经过反例和盲测才晋升为长期记忆规则，不让单次成功变成定律。
- **落点模块**：40-memory、90-curriculum、10-theory

### S-ZEN-29 · MiniMax 官方 H3 full-reference 提示词指南（ref-en.txt）
- **URL**：https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：MiniMax H3 Community License Agreement（仓库首页所示的仓库级许可；本文件页面未单独标注）
- **核实**：✅ 已打开核实
- **摘录**：官方六段结构：subject_definitions、summary、retention_analysis、detailed_description、overall_soundscape、non_diegetic_music。标签：`<Subject N>`（可复用的可见内容）、`<Picture N>`、`<Video N>`、`<Audio N>`。视觉保留度用 fully_preserved、partially_preserved、attribute_transfer、weak_reference；音频用 fully_copy、partially_copy、reference、weak_reference。对白写 `<d>[Language] …</d>`，保留原语言；说话人 `(Sx)` 按实际发声顺序分配一次后复用，不写进 retention_analysis；听不清的写 `[unclear]`，不猜。第一镜写 `[Shot 1]` 不带时间戳，后续写 `[Shot N] At MM:SS.mmm`；跨切发声用 `<scenetrans>`，被视频结尾截断用 `<cutoff>`。生成任务的 detailed_description 一般为 350–500 个英文词（指这一段，不是整条提示词）。
- **对本学院有什么用**：学院 H3 方言课的一手依据：agent 写 full-reference 提示词时把 detailed_description 控制在 350–500 英文词，并核对段名和词表与官方一致。
- **落点模块**：20-craft、70-playbooks

### S-ZEN-30 · MiniMax 官方 H3 base 提示词指南（base-en.txt）
- **URL**：https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt
- **类型**：official-doc
- **分类**：🟡 需适配
- **许可**：MiniMax H3 Community License Agreement（仓库级许可；本文件页面未单独标注）
- **核实**：✅ 已打开核实
- **摘录**：（核实时补入：研究员在关键事实中引用了本文件，但未列为条目。）覆盖 T2VA、I2VA、FL2VA、L2VA 四种模式，三段结构为 integrated_multimodal_description、overall_soundscape、non_diegetic_music。规定每个画外音 `<d>` 块之后紧跟一句，说明对应画面人物的嘴唇完全闭合（示例 `while his lips remain completely closed`）。运镜写成运动类型、幅度、速度三项，示例「The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.」overall_soundscape 用 1–4 句英文写成一段，non_diegetic_music 用 1–3 句英文；integrated_multimodal_description 未给字数要求。
- **对本学院有什么用**：学院 H3 方言课的首帧 / 首尾帧部分以它为准：agent 写画外音时紧跟闭嘴句，运镜按「类型 + 幅度 + 速度」写。
- **落点模块**：20-craft、70-playbooks

### S-ZEN-31 · MiniMax 视频生成 API（video-generation-v2-create）
- **URL**：https://platform.minimax.io/docs/api-reference/video-generation-v2-create
- **类型**：official-doc
- **分类**：⚪ 仅借鉴
- **许可**：官方文档（非开源）
- **核实**：✅ 已打开核实
- **摘录**：模型有 MiniMax-H3 和 MiniMax-H3-Max。`duration` 必填且为整数：H3 为 4–15 秒，H3-Max 为 5–15 秒。分辨率：H3 为 768P / 2K，H3-Max 为 480P / 768P。画幅含 adaptive、21:9、16:9、4:3、1:1、3:4、9:16；文生视频不能用 adaptive，图生视频由输入图决定、ratio 固定为 adaptive。content role：first_frame ≤1、last_frame ≤1、reference_image ≤9、reference_video ≤3、reference_audio ≤3（视频、音频每段 2–15 秒，各自合计 ≤15 秒）。图片 ≤30MB，视频 ≤50MB，音频 ≤15MB；每个 text ≤7000 字符。图生与参考生互斥：出现任何 `reference_*` 就不能再用 first_frame / last_frame。model 参数说明写明 H3 与 H3-Max 都支持 text-to-video、首尾帧和 reference-to-video。页面未描述输出是否含声音。
- **对本学院有什么用**：学院用它核对委托方 ComfyUI 节点与官方 API 的差异（帧网格对整数秒、first_frame 与参考图同用），agent 遇到模式选择时以官方互斥规则为准，再在 ComfyUI 上实测。
- **落点模块**：20-craft、40-memory

### S-ZEN-32 · MiniMax H3 官方 skills 发布报道（ComfyUI Wiki）
- **URL**：https://comfyui-wiki.com/en/news/2026-08-10-minimax-h3-official-skills
- **类型**：article
- **分类**：⚪ 仅借鉴
- **许可**：未标明
- **核实**：✅ 已打开核实
- **摘录**：报道日期 2026-08-09/10：MiniMax 在 GitHub 发布 H3 官方 skills 包。核心是 h3-prompt-writing，把多模态请求改写成 H3 结构化提示词，覆盖 T2VA、I2VA、FL2VA、L2VA、Ref2VA 五种模式，含 base-en.txt（base / 关键帧模式）与 ref-en.txt（full-reference 模式）两份指南。另有八个风格生成器：3d-animation-short-generator、brand-promo-video-generator、co-op-game-intro-generator、handdrawn-live-video-generator、minimalist-product-ad-generator、music-video-subtitle-generator、paper-collage-explainer-generator、papercraft-stop-motion-explainer。仓库同时把它镜像在 `.agents/skills/` 和 `.claude/skills/` 下。
- **对本学院有什么用**：学院 H3 方言以官方 skill 为上游、zenstory 方言为实践补充，agent 遇到模式问题时先查官方五种模式的定义。
- **落点模块**：20-craft、90-curriculum

## 关键事实（可被理论/判据引用）

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| F-ZEN-01 | MiniMax 官方 API：MiniMax-H3 的 `duration` 为 4–15 整数秒（H3-Max 为 5–15 秒）；first_frame/last_frame 与 reference_image/video/audio 在同一请求中互斥；最多 9 张参考图、3 段参考视频、3 段参考音频，每段 2–15 秒且各自合计不超过 15 秒；每个 text 最多 7000 字符。 | [MiniMax API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) | 高 |
| F-ZEN-02 | zenstory 的 H3 方言规定：无图、只有起始帧、起始帧加结束帧用三段结构；起始帧与角色板或场景板同时存在时整组走 full-reference 六段，起始帧也以 reference_image 送入。〔学院推断〕委托方 T-2/T-3 的「起始帧送 first_frame + 六段提示词 + 多图参考」与官方 API 互斥规则不一致，需在 ComfyUI 节点上做 A/B 核实。 | [minimax-h3.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/references/minimax-h3.md) | 中 |
| F-ZEN-03 | 官方 full-reference 指南：生成任务的 detailed_description 一般为 350–500 个英文词；第一镜 `[Shot 1]` 不带时间戳，后续写 `[Shot N] At MM:SS.mmm`；跨切发声用 `<scenetrans>`，被视频结尾截断用 `<cutoff>`；`(Sx)` 不写进 retention_analysis。 | [ref-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt) | 高 |
| F-ZEN-04 | 官方 base 指南：每个画外音 `<d>` 块后紧跟一句，说明画面人物的嘴唇完全闭合；运镜写成「运动类型 + 幅度 + 速度」，例 The camera pushes in with small amplitude at slow speed。 | [base-en.txt](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt) | 高 |
| F-ZEN-05 | zenstory 对同一镜头做了 20 次 H3 中文对白生成（7–108 字、5–13 秒），自然语速约 4.1 字/秒，较密输入会赶词或截断；50 字/5 秒仍说完整，不能据此划定截断阈值。〔学院推断〕它与委托方 T-2 的 7.5 字/秒可能分别对应自然语速与容量上限，计数口径未核对，待复测。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-06 | H3 对白镜实际比计划多约 1.5–2.5 秒（开口前延迟加说完台词）：两版分镜计划平均镜长 5.3 / 3.3 秒，剪到台词说完后为 6.0 / 4.3 秒。每镜各生成 1 次。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-07 | H3 显式写 `non_diegetic_music: N/A` 的 14 次都没有配乐，省略的 3 次中 2 次有配乐；含 No dialogue 的 8 次未出现台词，未支持「否定句会招来被排除内容」。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-08 | H3 口型落错人：远处小孩说话、近处骑手正对镜头不说话时，现行写法 3 次中 2 次口型落在骑手；加「说话人带音色与画内标注 + 明写骑手 does not speak; his lips remain completely closed」后 3/3 正确；骑手出画或背身时 12/12 正确。发声基频都在儿童区间，声音没选错。 | [minimax-h3.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/references/minimax-h3.md) | 低 |
| F-ZEN-09 | H3 多镜容器（9 秒三切，要求 3.0/6.0 秒切）：每切挂关键帧加对齐句时切点落在 2.88–3.04 / 6.00–6.04 秒，各切与关键帧 NCC 0.88/0.89/0.95；只挂首张关键帧时为 0.88/0.40/0.33，另有 1 次多出一个切；对白 12/12 逐字完整。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-10 | H3 无起始帧、挂地点图时，只写「Medium shot」的 8 次出了远景 3、中远 3、中景 2；加取景字段（到腰、头在上三分之一、机位高度与距离）后 8 次中 7 次中景。「不继承构图」一句挡不住景别漂移。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-11 | H3 写「Fixed camera.」的 4 次无机位位移，不写机位句的 28 次中 4 次推拉或平移；终点写「指尖碰到杯沿后停住」4/4 停在杯沿，写「约二十厘米后停住」4 次中 3 次仍伸到杯子并接触。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 低 |
| F-ZEN-12 | H3 反应镜写法「先点名情绪 + 两处当前景别读得到的泄露 + 1.5 秒内落下再定住」：单模型盲评清晰 3.9/5、自然 4.0/5，四拍全部第一或并列第一；只写情绪词自然度 2.8，逐段写可见反应链强度 1.9。文件注明不外推到其他模型。 | [performance-action-timing.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/references/performance-action-timing.md) | 低 |
| F-ZEN-13 | H3 双人接触（每格 3 次）：只写一个动词最差（掌掴三次都是碰一下没反应）；掌掴一镜写全「接近—接触—施力—结果」最好（5/4/4）；推搡拆成「到接触为止」与「从接触后关键帧起」两镜才把人推退一步，但跨切连续性最差（2.7/5）。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 低 |
| F-ZEN-14 | H3 续接：一组用上一段真实尾帧作参考 3/3 开场 NCC 0.91–0.99，只用角色图和地点图独立生成为 0.01–0.41；另一组 3 次中 2 次为 0.94–0.97、1 次为 0.27。方言文件规定尾帧在 full-reference 中作 reference_image，不标成 first_frame；真实视频续接在该平台上未验证。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-15 | 关键帧统一画风：示例 EP001 关键帧把 motion-comic 换成写实、每场加一句光与色温、以一张中远景定调图挂在最后后，第一场 13 张的平均亮度离散度 18.3→6.6，冷暖离散度 9.3→4.2。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 中 |
| F-ZEN-16 | zenstory 的 AI 真人短剧节奏起点值：首钩 ≤5 秒（一组实测 5 部里 3 部在前 5 秒给出第一个钩子），情绪触点间隔 ≤30 秒，每集至少 1 次有对手的反转，集尾停在峰值，平均镜长 2.5 秒与近景类占比 ≥0.45（一组真人短剧实测），VO 占比 ≤0.3（未实测）。文件明写是起点，不是质量线。 | [episode-design.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-develop/references/episode-design.md) | 中 |
| F-ZEN-17 | 付费门槛集：套件不提供默认位置；创作者已声明门槛并请求建议时，可举经验区间作例（第一道约第 8–16 集，第二道约第 25–30 集）。门槛处停在揭晓前一秒，悬念只依赖观众已建立的人物、规则和赌注；刚兑现完大回报就设门槛不成立。 | [episode-design.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-develop/references/episode-design.md) | 低 |
| F-ZEN-18 | zenstory 规定：生成单元固定在更长一档时，切镜密度由镜内调度承担（景别或视点的实际变化，或一次完整的动作与反应交接），否则「观众读到的都是幻灯片」；超过约五到八秒后，一张冻结关键帧只描述了镜头开头。 | [production-shot-grammar.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-storyboard/references/production-shot-grammar.md) | 中 |
| F-ZEN-19 | 运镜逐镜选（SHT-04）：人物移动是重点就跟拍或横移，新信息进画就摇、俯仰或后拉，压力落到某人身上就缓推，以上都不成立才固定，固定也写理由；短促推近、定格、闪白只留给情绪爆发和重大反转。 | [shot-craft.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-storyboard/references/shot-craft.md) | 高 |
| F-ZEN-20 | 竖屏字幕规范：一行显示，超过 12 字在停顿处拆分；去掉句末标点，保留问号和感叹号（GY/T 288 与短剧惯例）；字高为画高 4.3%，描边 0.42%，基线距底边约 24%；字幕逐字取自剧本，转写只定位时间。 | [sound-and-subtitles.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-edit/references/sound-and-subtitles.md) | 高 |
| F-ZEN-21 | 一次实跑记录：语音转写把「诸君，且听龙吟」听成「朱军且听龙银」；单遍 loudnorm 落在 -12.33 LUFS（偏离 -16 目标 3.7 dB），两遍后到 -15.79。edit_tool.py 的两遍 loudnorm 参数为 I=目标、TP=-1.5、LRA=11，输出 48 kHz。 | [real-outputs.md](https://github.com/zenstory-ai/drama-skills/blob/main/docs/real-outputs.md) | 中 |
| F-ZEN-22 | 剪辑对白镜：入点落在开口前约 0.25 秒，出点在台词结束后留约 0.4 秒反应，整段不短于约 1.2 秒；生成的对白镜常晚开口、句后拖尾。verify 把切点前后两帧平均亮度差超过 20（0–255）的切点列出供人工查看，不给质量结论。 | [cut-craft.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-edit/references/cut-craft.md) | 中 |
| F-ZEN-23 | 连续性锁三条件：两个以上镜头（或一镜 + 一张资产板）出现；观众看得出不一致；不随剧情变化，状态不上锁。锁面在生效范围内必须逐字出现在图片、关键帧、视频提示词中；写在 no/not/without/avoid/不要/没有/避免 之后的匹配不算，粘在别的 ASCII 词上的匹配也不算（CON-07，脚本可阻断）。 | [continuity-lock.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-assets/references/continuity-lock.md) | 高 |
| F-ZEN-24 | 生产闸门：prepare（只预览，不调用供应商）→ 创作者看完预览后明确确认 → confirm（绑定 job 指纹，job、prompt、参数、输出路径任一变化即失效）→ run（消费确认，重试必须重新确认）。「继续」「预算没问题」不算确认。中断后 audit 报 orphaned_provider_job，用 collect 取回已计费结果，不重投。 | [produce SKILL.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-produce/SKILL.md) | 高 |
| F-ZEN-25 | REV-09 指令优先级：已确认的故事事实与对白/文字 > 镜头覆盖、目的、起止、时长 > 资产身份与连续性 > 创作者确认的视觉方向与制作配置 > 目标模型条件 > 装饰性偏好。每次重写或重编组提示词都要填改写前后回归表。 | [production-quality-gates.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-review/references/production-quality-gates.md) | 高 |
| F-ZEN-26 | 剧本盲评量表 v5 共 100 分（hook_payoff 15、causality 15、character 15、dialogue_action 15、visual_drama 10、pacing_retention 10、prompt_fidelity 10、genre_fit 10）；门禁每 arm 3 个 replicate，Codex 与 Kimi 两家各自交换 A/B 盲评，另设 4 个一次性 holdout，单案例跌幅不超过 2 分。 | [content-quality-rubric.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/content-quality-rubric.md) | 高 |
| F-ZEN-27 | 可生成性（VID-21，仅在生成模型承担画面时生效）的四类高风险写法：精确拦截、不可见内部状态（「神色一凛」）、否定式动作（「没有接话」）、三步以上手部编排链；改写为日常高频的整体动作组合，戏剧信息由组合和时机承担。 | [generability.md](https://github.com/zenstory-ai/drama-skills/blob/main/skills/short-drama-video-prompts/references/generability.md) | 高 |
| F-ZEN-28 | 文档冲突：zenstory 的 minimax-h3.md 写 H3-Max「仅支持文生和首/尾帧，不支持 full-reference」，而 2026-10-06 打开的官方 API 页 model 参数说明写 H3-Max 支持 text-to-video、首尾帧和 reference-to-video（reference image / video / audio）。以官方页为准，并实测。 | [MiniMax API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) | 中 |
| F-ZEN-29 | zenstory 的模型观察经中转服务或 WorkRally 平台调用，不是 ComfyUI；盲判先去掉臂身份、打乱顺序，判断者为同一个模型，不是独立人评；每格样本多为 2–20 次，文件声明不构成能力、成功率或质量保证。 | [model-behavior-probes.md](https://github.com/zenstory-ai/drama-skills/blob/main/evaluations/model-behavior-probes.md) | 高 |

## 空白与未找到

1. **ComfyUI 侧完全空白**：zenstory 的方言与观察走官方 API、中转服务或 WorkRally 平台，没有 ComfyUI 节点、帧网格（17k+5）、cfg=1.0、20 步或 4 步 turbo LoRA 的任何信息。委托方「起始帧送 first_frame + 六段 + 多图参考」在 ComfyUI 节点上如何被解析，仍需自测（见 F-ZEN-02、F-ZEN-28）。
2. **Qwen-Image 出图配方空白**：没有 1696×2528 板图、多 seed 抽卡、Qwen 专用反文字反水印写法；图片侧只有模型无关的配方，内置图片 adapter 是 GPT Image 2，观察里的参考图由 Seedream-5 Pro 或 gpt-image-2 生成。
3. **观察样本小、评审不独立**：每格 2–20 次，盲判由单一模型完成，不是人评；只能作 40-memory 的待复测假设。4.1 字/秒（zenstory，按可发声字计）与 7.5 字/秒（委托方 T-2，计数口径未写明）的差异原因未定。
4. **媒体审查方法空白**：审查 skill 的 rubric-visual-motion.md 明写「本套件不查看媒体」，成片质量交给创作者判断，没有提供自动看片的方法。这正是委托方「指标全绿、人仍说不行」要补的缺口。
5. **覆盖之外的领域**：平台发布与流量运营（3 秒钩子以外的完播率、封面标题、更新节奏、追更运营、合规）、冷启动观众测试、系统化音效与配乐设计、调色与 LUT（只有同场景自动接镜和亮度/饱和/色温小幅校正）、打斗编排体系（只有掌掴、推搡、拉手腕、拥抱的小样本）。
6. **版本与主页（更正研究员记录）**：GitHub releases 页标注 v0.8.1（2026-09-28）为 Latest，与本地 VERSION 0.8.1 一致，研究员记录的「latest release 为 v0.7.1」不成立。主页 https://zenstory.ai/zh/drama-skills 在本次核实时可以打开（研究员当时遇到 503），页面未见成本数字；「68 秒样片、视频生成成本约 40 元」只见于仓库 README 自述，未独立核实。星数 GitHub 页显示约 2.5k，第三方站点的 1,080 未核实。
7. **DESIGN.md 与现行 Dashboard 不一致**：DESIGN.md（2026-08-06）写单页、无 tab；总路由 SKILL 描述每集六个视图和 ⌘K 搜索。借鉴设计原则时以现行 SKILL 为准。
8. **第三方评测未找到**：研究员未检索到第三方深度评测或使用反馈；核实阶段因本轮检索额度用尽，未再补搜。
9. **未逐条核对**：CHANGELOG 与各 release notes 未逐条读；六张形态卡只核对了实拍卡的小节与光的定义。
