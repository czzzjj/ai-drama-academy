# 10-theory · 理论层索引

> 理论层回答"**为什么会这样**"：观众、平台和生成器的机制。技能层（[`20-craft/`](../20-craft/)）回答"怎么做"，判据层（[`50-rubrics/`](../50-rubrics/)）回答"怎么验"。
> 每篇的格式都相同（[`CONVENTIONS.md`](../CONVENTIONS.md) §5.1）：一句话世界模型 → 核心判决 `Tnn.k`（每条附为什么和来源标注）→ 机制 → 本管线变体 → 常见误用 → **→ 行为改变** → 自测。
> 引用某条理论判决时，写它的编号（如 `T03.1`），不要转述。转述会走样，这正是 G6 的病根。

## 怎么用（给装载了本学院的 agent）

1. **按任务读，不按顺序读完。** 开工前先查下面的"任务 → 必读"表，只读当前环节要用的几篇，每篇先读"核心判决"和"→ 行为改变"。
2. **读完必须落到动作上。** 每篇的"→ 行为改变"是下一次生成或验收时的具体改动。读完却不改流程，就是 F4（学了技能 ≠ 有了能力）。
3. **证据等级不能升级。** 〔外部调研〕不能改写成"经验表明"，〔学院推断〕不能删掉验证方法。委托方没做过的事（发布、冷观众、声音设计等），只有外部调研和推断可依。
4. **冲突以裁决为准。** 理论和 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md)（R1–R7）冲突时，以裁决为准，并回报冲突。
5. **用自测检查是否真读懂。** 每篇末尾有 3–5 道自测题；答不出，就回到对应的判决重读。

## 任务 → 必读

| 将要做的事 | 先读 | 再读 |
|---|---|---|
| 写季大纲、分集剧本 | 01、14 | 05、13 |
| 拆段、拆镜、写分镜表 | 06、02、03 | 04、05 |
| 设计打斗或动作戏 | 04、03 | 05、06 |
| 出板图、关键帧 | 07、12 | 01（9:16 几何）、03（空间在图里定） |
| 写 H3 视频提示词 | 08、02 | 03、13 |
| 镜头验收、成片验收 | 10、08 | 07 |
| 剪辑、混音 | 05、11 | 06 |
| 审片、回应人类反馈 | 10 | 被反馈命中的那一篇 + [`00-orientation/glossary.md`](../00-orientation/glossary.md) |
| 发布 | 09 | 01 |

## 推荐通读顺序（首次装载）

1. **10 质量观**：先改掉"符合我的清单 = 质量"这个判断方式，否则后面每一篇读完都会被拿去当新的清单（F1–F4）。
2. **01 竖屏生理学**：知道观众怎么看、为什么会划走。
3. **06 长段多拍 → 02 镜头语言 → 03 空间调度 → 04 动作设计 → 05 节奏工程**：预制作的核心，委托方 A 组五个案例的病灶都在这里。
4. **07 资产管线 → 08 生成器脾气**：一致性和生成器缺陷（B、C、D 组）。
5. **13 表演 → 12 色彩与光 → 11 声音**：委托方的能力缺口（GAP-3、GAP-4、GAP-5、GAP-6）。
6. **14 季架构 → 09 平台发布**：季级连续性和上线（GAP-7、GAP-1）。

## 14 篇总览

| # | 文件 | 一句话世界模型 | 浓缩案例 | 对应技能 |
|---|---|---|---|---|
| 01 | [`10-theory/01-vertical-drama-physiology.md`](01-vertical-drama-physiology.md) | 观众的手指一直在屏幕上，随时会划走：0–5s 静音可读的钩子、约 20s 内的首个转折、集末用问句卡点是承重墙；9:16 靠脸和纵深讲戏，主体全身入镜约占画高 50–60% | GAP-1, GAP-2, A1, F1 | script-doctor, publish-prep, multi-episode-arc, keyframe-freeze |
| 02 | [`10-theory/02-film-language-for-generators.md`](02-film-language-for-generators.md) | "运镜"指镜头语言设计，不是位移次数；H3 只能执行 12 个原语加幅度和速度，动机、轴线和取景在起始帧和分镜阶段定好；一次生成只放一个主运镜 | A4, A5, F2, F4, M2, M4 | storyboard-long-take, video-prompting-h3, keyframe-freeze, screening-review |
| 03 | [`10-theory/03-spatial-staging.md`](03-spatial-staging.md) | 左右关系和轴线由起始帧钉死，文字改不动；默认单轴定侧，按画面位置称呼角色，定稿前跑方位词审计；空间拍要少，打击拍可以密 | A5, M4, P4, P5, C1-6 | storyboard-long-take, keyframe-freeze, video-prompting-h3, shot-qc, action-choreography |
| 04 | [`10-theory/04-action-design.md`](04-action-design.md) | 打斗是有因果的交手，不是精彩瞬间加反应镜头；写战术链、交手回合和七相动作链，出招和受击同框、同一次生成；用真实事件时长，留出后果 | A2, A3, M3, P10 | action-choreography, storyboard-long-take, video-prompting-h3, performance-direction |
| 05 | [`10-theory/05-rhythm-engineering.md`](05-rhythm-engineering.md) | 节奏是变化的密度和对比，不是切镜数；KPI 是有效拍数；时长被读成事件速度；生成单位要长，剪辑单位可以短；按快—慢—爆—静设计 | A1, A3, P10, M1, GAP-6 | storyboard-long-take, action-choreography, edit-and-assemble, sound-design, screening-review |
| 06 | [`10-theory/06-long-take-multi-beat.md`](06-long-take-multi-beat.md) | 一次 H3 生成就是一段：8–15s，一条完整动作链，段内 2–3 拍；连续动作不切新镜；<124 帧的镜不送生成器 | A1, P10, M1, A5 | storyboard-long-take, edit-and-assemble, production-director |
| 07 | [`10-theory/07-asset-pipeline.md`](07-asset-pipeline.md) | 一致性来自资产链（锚点卡 → 板图 → 关键帧 → 链式参考），不来自提示词措辞；每一级都要逐特征放大验收，通过才放行；关键帧要按海报标准出 | P1–P5, B1, C1, C2, M6, M7 | casting-and-canon, asset-boards, keyframe-freeze, visual-bible |
| 08 | [`10-theory/08-generator-temperament.md`](08-generator-temperament.md) | 生成器的脾气是固定的：cfg=1 时负向提示无效，提到什么就长什么，会自己加字幕，默认偏慢，片尾会崩解，事件时刻控制不了，对白容量有物理上限。对付它要靠结构让错误不可能发生，禁令只是兜底 | C1, D1, D2, D3, D4, B2, B3, B4, E4 | video-prompting-h3, shot-qc, asset-boards |
| 09 | [`10-theory/09-platform-publishing.md`](09-platform-publishing.md) | 能不能发由合规决定（AI 标识、许可地域、节目编号），优先于审美；封面、标题、切片、发布节奏全部是外部调研，委托方没有一手经验 | GAP-1 | publish-prep, cold-audience-test |
| 10 | [`10-theory/10-quality-philosophy.md`](10-quality-philosophy.md) | 质量是目标观众的反应，不是"符合我的清单"；指标只是下限；自我放映、独立评审、冷观众这三件套，加上 8 维全量自查，才能证明达到上限 | F1, F2, F3, F4, C2 | screening-review, cold-audience-test, production-director, shot-qc |
| 11 | [`10-theory/11-sound-design.md`](11-sound-design.md) | 不写声音不等于静音；声音要分层设计（对白、环境、拟音、音乐、静场），对白逐字取自剧本，配乐在后期统一铺设，再和剪辑点对齐 | GAP-3, GAP-6, D5 | sound-design, edit-and-assemble |
| 12 | [`10-theory/12-color-and-light.md`](12-color-and-light.md) | 色彩与光由按情绪节拍编写的色彩剧本决定，写成可见光源、光向和色名，不交给模型自由发挥；光只写打在人身上的效果，不写光源物件 | GAP-4, M2, B3 | visual-bible, keyframe-freeze |
| 13 | [`10-theory/13-performance-direction.md`](13-performance-direction.md) | 表演要写成可拍的身体变化（眉 → 眼 → 嘴、呼吸、视线、重心），不写情绪名词；一镜不超过 2–3 个表情拍；中性的脸配合上下文（库里肖夫效应）比夸张表情更稳 | GAP-5 | performance-direction, video-prompting-h3 |
| 14 | [`10-theory/14-season-architecture.md`](14-season-architecture.md) | 一季是一台引擎：核心欲望、可重复的阻碍、倒计时、悬而未决的问题；每集是一个迷你弧；伏笔、回收、卡点类型、角色外观都记在季级账本里 | GAP-7, B1 | multi-episode-arc, casting-and-canon, script-doctor |

> 06–14 由其他章节作者编写；上表的世界模型是本索引的摘要，与正文不一致时以正文为准，并同步修改本表。

## 跨篇共用的六条底层判决（出现冲突时以这六条为锚）

1. **病灶在哪里产生，就回到哪里修。** 节奏、空间、动作、对白容量的病灶在预制作，不在提示词（[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) 病灶路由表；G7）。
2. **起始帧决定画面层面的一切。** 构图、轴线、景别、光都由起始帧决定，文字只描述变化（P4、M2；T02.5、T03.2）。
3. **一次生成只做一件事。** 一个主运镜，空间拍和表情拍各 ≤2–3 个，承载一条完整动作链（R4、R5；T02.3、T03.5、T05.9）。
4. **写事件，不写形容词。** 特效、史诗感、慢和快，都要写成可见事件和真实时长（M3；T04.11、T05.5）。
5. **生成单位 ≥124 帧，剪辑单位可以短**（R6；T05.2）。
6. **指标是下限，观众反应才是质量。** 任何"全绿"都不能代替自我放映、独立评审和冷观众（F1、F2；01、10）。

## 维护

- 新增或修改判决时，编号只增不改。删除的判决保留编号，标注"已撤销"和原因，避免下游引用悬空。
- 新的外部证据与某条判决冲突时，先改 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md)，再改理论，最后同步技能和判据。
- 改完运行：`python3 tools/academy_lint.py --paths 10-theory/*.md`。
