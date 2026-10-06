# 好/坏样例对 · 一致性与资产（TP-15 – TP-21）

> 训练用法见 [`30-taste/README.md`](../README.md)。❌/✅ 中的提示词与验收记录是学院构造的训练素材，所依据的现场事实逐条取自 [`00-orientation/client-dossier.md`](../../00-orientation/client-dossier.md)（B1–B4、C1、C2、D4）。
> 判据所在清单：[`50-rubrics/checklists/board.md`](../../50-rubrics/checklists/board.md)、[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/season.md`](../../50-rubrics/checklists/season.md)。
> 立场依据：[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1（禁用项先写正向可见状态句，绝对否定只追加在已被证实会自加的物件上）。

## TP-15 · 多人：克隆三人 vs 差异化三人
- ❌ 坏：`Three guards stand behind the elder in the dark hall.` 产出的三张脸高度雷同。同一镜还多出一道并不存在的斜光柱。
- ✅ 好：`Three clearly distinct men with different faces, hair and builds stand behind the elder: on the LEFT a heavy-set bald man with a broad flat nose; in the CENTER a thin young man with a long black ponytail; on the RIGHT a grey-bearded older man with a scar across his chin. Warm ambient light falls on their faces. No flashlight, no torch beam, no spotlight.`
- 点评（≈200 字）：不给差异，生成器就会复用同一张脸，这是默认行为〔委托方实证·B3〕。外部调研补了一条根因："几张脸 = 几个人"，多视角拼在一张设定图上，最容易生成同框的两个同一角色〔外部调研·S-H3-09、S-VGEN-18〕。平台已经把高频 AI 脸列为治理对象，要求主要角色有清晰的区分度〔外部调研·S-PLAT-07〕。所以克隆脸已经从质量问题升级成下架风险。好样按画面位置逐个写出 ≥3 项可见差异（脸型、发型、体格、年龄）。光只写成被动的环境光，对已被证实会自加的光柱再追加绝对否定。可迁移：凡是 ≥2 人的镜，验收时逐张脸裁剪并排比对，任意两张像同一个人就判不通过。
- 可迁移判据：R-VP-08、R-KF-10、R-VID-04、R-SEA-12；TJ-15 选角对照｜溯源：B3, S-PLAT-07, S-H3-09

## TP-16 · 符号：十字 vs 一根竖线贯穿
- ❌ 坏：`the ф mark: a red circle with a line through it, glowing like neon`。产出被画成了十字，多出一根横线；另一镜的质感变成了霓虹或激光。
- ✅ 好：`the ф mark: exactly one red ring crossed by exactly one vertical bar, top to bottom; no horizontal line, no cross sign, no plus sign, no second bar; the mark is fire-textured, not smooth neon, not a laser line.` 锚点卡 `SYM-PHI` 的 `禁用` 栏维护一张"已见错误变体清单"：横线、十字、加号、第二根竖线、霓虹、激光。
- 点评（≈200 字）："a line through it"没有规定方向，模型就套用了最常见的先验：十字。对抗约束的写法分两步〔委托方实证·D4〕：先用正向描述把数量和方向写死（exactly one、vertical、top to bottom），再把**曾经错成过的每一个变体**逐一穷举否定。质感也一样，要火纹就得否定霓虹和激光。这正是 R1 第 2 条的标准用法：被否定的每一项都是已经被证实出现过的错误，不是凭空想象出来的。可迁移：每个符号资产都维护一张"已见错误变体清单"，每出一次新错就追加一项。验收时逐条计数：数横线有几根，数竖线有几根，不凭"看起来像"放行。
- 可迁移判据：R-VP-12、R-BRD-08｜溯源：D4

## TP-17 · 验收："通过" vs 逐特征证据
- ❌ 坏：`qc/boards/nijiadi-v2.md` 只有一句："尼加狄 v2：方位正确，整体符合锚点卡，通过。"
- ✅ 好：逐项表依次是：① 禁用项：无铠甲 ✔（`crop-torso.png`）② 必现项：黑臂在画面左侧 ✔（`crop-arms.png`）③ 方位：左右臂 4× 最近邻放大 ✔ ④ 程度：缩到 270 宽并去色后，黑臂与白臂的明度差"弱，第一眼读不出" ✘（`view270-gray.png`）。结论：不通过。处置：重写提示词，把黑臂前置并强调对比，3 seed 重抽，交独立会话复验。
- 点评（≈200 字）：委托方实证 C1-7 和 C2 是同一件事：方位对了，"黑臂对比弱"却被早期验收放行，复核时才查出来。一句"通过"无法复核，下一个会话不可能知道你当时看了什么、没看什么。好样把每一条必现、禁用都变成"一张证据图 + 一句结论"，并按固定顺序填写：禁用项排在构图之前（C1：禁用项优先于构图）。最容易放水的是"程度类"属性，比如对比、大小、数量；缩小去色测试能把"看起来还行"变成客观可读或不可读。高风险资产还要交给独立会话再验一遍。可迁移：验收记录里，任何没有附证据文件名的 ✔ 一律视为没验过。
- 可迁移判据：R-BRD-03、R-BRD-04、R-BRD-05、R-BRD-07、R-BRD-10；TJ-01 眯眼去色层级测试｜溯源：C2, C1-7

## TP-18 · 禁用项：只写否定 / 写 negative_prompt vs 正向状态句 + 追加否定
- ❌ 坏：正文写 `a straight sword, no gemstone, no ridge`，同时在工作流的 negative_prompt 字段填 `gemstone, double-edged, ornate`。
- ✅ 好：删掉 negative_prompt 字段。正文写 `a Chinese straight single-edged blade; the flat of the blade is smooth with no central ridge; the guard is plain polished steel, smooth and unadorned; a single tiny gem sits in a small groove at the end of the hilt.` 只对护手追加一句 `no gemstone on the guard`，并按 R1 记录 A/B（3 seed：只写正向句 vs 正向句 + 否定句）。
- 点评（≈200 字）：cfg=1.0 时，ComfyUI 会直接跳过无条件分支，negative_prompt 填了不起作用，还会制造一种"已经处理过了"的错觉〔委托方实证·T-2；外部调研·S-COMFY-05、S-COMFY-06〕。只写否定句，模型拿不到"应该是什么"；而写出来的物件名，又可能被登记成画面内容〔外部调研·S-COMFY-08〕。学院立场 R1：先用正向可见状态句锁定外观，只对已被证实会自加的物件（C1-1 里的护手蓝宝石）追加绝对否定，再用 A/B 证明这句否定没有反过来把宝石招进来。可迁移：锚点卡里每一条禁用项旁边，都必须有一条对应的正向状态句。
- 可迁移判据：R-VP-10、R-VP-11、R-BRD-12、R-BRD-13｜溯源：C1-1, T-2, S-COMFY-05, S-COMFY-08

## TP-19 · 人群："远处人群低语" vs 大虚化暗形块
- ❌ 坏：`In the distance a crowd whispers, some holding lanterns and scrolls, watching anxiously.` 人群被模型扩写成一群"持发光平板者"，而且扩散、变形。
- ✅ 好：`Far behind them, the crowd is a heavily blurred mass of dark shapes with no distinguishable faces.` 声音交给 `overall_soundscape: low indistinct murmuring from a distant crowd`。需要表现人群反应时，改用一个具名角色的反应镜。
- 点评（≈200 字）：给人群任何独立特征（道具、动作、情绪）都会被扩写〔委托方实证·B2〕。连"低语"这种声音信息，也会被翻译成视觉道具。坏样还给人群加了两种道具，正好对应"提到即生长"〔外部调研·S-H3-09〕。好样把人群降成没有脸、没有道具的大虚化暗形块，把"低语"搬到声音段，画面和声音各管各的。剧本阶段就要这样写，不要等到提示词阶段才补救（R-SCR-19）。可迁移：人群默认虚化、无脸、无道具。剧情需要人群反应时，用一个已建锚点卡的角色的反应来代替。人群不建独立的 CHR 卡。
- 可迁移判据：R-VP-15、R-KF-11、R-SCR-19、R-BRD-21｜溯源：B2, S-H3-09

## TP-20 · 身份：只挂单张板图 vs 链式参考 + 正脸对照
- ❌ 坏：SHOT-044 只挂了 `- references: 1=CHR-SUXIAO-BOARD`，验收只看了接触表的中间一格。后来发现苏晓的脸漂成了"粗犷成熟脸"，与板图不符。
- ✅ 好：`- 模式: Ref2VA`、`- first_frame: REF-SHOT044-START`、`- references: 1=CHR-SUXIAO-BOARD; 2=REF-SHOT043-START`（同场已经通过的关键帧）。验收时用 `contact_sheet.py --crop face=…` 导出苏晓的脸部裁剪表，和板图按同尺寸并排。
- 点评（≈200 字）：单张板图锁不住身份，跨镜也没有对照机制，于是身份漂移〔委托方实证·B1〕。链式参考（角色板加同场已过的关键帧）同时补上了光线、妆容和角度的上下文〔委托方实证·P5、M7〕。外部调研有两点要注意：给同一个人挂两张脸参考，在运镜中可能被生成成两个人，需要在提示词里声明是同一人〔外部调研·S-H3-09〕；Ref2VA 加音频后，有一例报告身份相似度骤降，但只有单帖，未经复现〔外部调研·S-H3-13〕。可迁移：每镜参考 = 角色板 + 同场最近一张已过关键帧。验收必须导出正脸裁剪并和板图对照，不能只看一格。
- 可迁移判据：R-VID-05、R-KF-15、R-KF-17、R-SEA-11；TJ-15｜溯源：B1, P5, M7, S-H3-09

## TP-21 · 光：写光柱 / 灯具 vs 被动环境光
- ❌ 坏：`A flashlight beam cuts through the dark cave, lighting up the guards; god rays stream down from a crack above.`
- ✅ 好：`Cool moonlight falls from the upper LEFT onto their faces and shoulders; the cave walls fade into darkness behind them.`
- 点评（≈200 字）：写出灯具或光束，它们就会被生成成实物光柱〔委托方实证·B3：同镜多出一道不存在的具象斜光柱〕。社区实测给出的改写方向是：写"暖光从一侧来"，不写"落地灯的光"〔外部调研·S-H3-09〕。光的来源可以在画外，靠场景推断（窗、月、火），这同样符合动机光原则〔外部调研·S-CRAFT-14〕。好样只写三件事：方向、色温、光落在哪里，画面里没有任何光源实物，也就没有东西可以被扩写。可迁移：冻结提示词和视频提示词里，光一律写成被动描述。flashlight、spotlight、light beam、god rays 这类词，`prompt_lint.py` 的 VP-light 必须零命中。
- 可迁移判据：R-VP-14、R-COL-04、R-COL-05｜溯源：B3, S-H3-09, S-CRAFT-14
