---
id: C1
title: 禁用项被生成器违反
group: C 资产工程
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [casting-and-canon, asset-boards, keyframe-freeze, video-prompting-h3, shot-qc]
drills: [DR-08]
---
# C1 · 禁用项被生成器违反

> 一句话：**在 cfg=1.0 的管线里，"禁止"没有通道。** 能对抗生成器自作主张的只有三样：写在正向提示词里的**可见状态**、多个 seed 的**统计**、放大到像素级的**验收**。

## 症状（含人类主创原话，逐字引用档案）

- 武器、角色、灵兽、场景、BOSS 共 7 个资产，在板图阶段被生成器加上了锚点卡明确不要的东西，或者方位、对比做错了〔委托方实证·C1-1…C1-7〕。
- 其中 C1-7 被 agent 自己的早期验收误判放行，后来复核才查出来〔委托方实证·C1-7、C2〕。
- 档案没有保留人类主创关于本案的「」逐字原话。人类介入点的记录是：C1-7 的新版由人类主创选定。
- 学院缺陷分级：禁用项出现在主角、BOSS、核心道具上属于阻断缺陷（Q7），见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §3。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

### 7 个子案（全部取自档案，未补造）
| 子案 | 资产 | 锚点卡要求 | 生成器实际产出 | 修正 | seed / 轮次 |
|---|---|---|---|---|---|
| C1-1 | 斩龙闪（刀）r1 | 护手"简朴无宝石"；单刃；柄末凹槽 | 护手加了醒目蓝宝石；刀身出中脊，像双刃剑；柄末凹槽没画出来；刀身过宽 | 改写为"中式直刀形制 + 单刃 + 无中脊 + 护手无宝石 + 柄末小槽嵌单颗微宝石" | 3 seed 重抽 |
| C1-2 | 阿姆（角色） | 原著没有装备描写 | 被加了全套肩甲、臂甲、腰裙、腿甲 | 提示词明写无装备，重出 | 档案未记录 |
| C1-3 | 巴哈（猛禽） | 小型猛禽，可以停在肩上 | 被加了金色颈饰；体量偏大 | 明写 `no jewelry at all`，重出 | 档案未记录 |
| C1-4 | 湖泊（场景） | 正圆湖；密林深处，没有远山 | 不是圆形；背景有远山 | 强化 "perfect round"，并否定远山 | 档案未记录 |
| C1-5 | 乱石区（场景） | `no carved stone, no runes`；树线围合 | 石碑上有刻纹；背景是山崖 | 重出（档案没说首版是否已写否定句） | 档案未记录 |
| C1-6 | 尼加狄 r1（BOSS） | 画面左侧应是黑臂 | 左右臂方位反了 | 3 seed 抽卡，选出方位正确的一版 | 3 seed |
| C1-7 | 尼加狄 v2 前（BOSS） | 黑臂对比一眼能读出来 | 方位对了，但黑臂对比弱，**早期验收误判放行** | 复核查出 → 重写提示词（黑臂前置 + 双臂特写 inset + "对比必须一眼读出"）→ 人类主创选定新版 | 档案未记录 |

### 子案归类（决定该用哪种防线）
| 失败类型 | 子案 | 生成器在做什么 | 主防线 |
|---|---|---|---|
| 加装饰物 | C1-1 宝石、C1-2 铠甲、C1-3 颈饰 | 按题材先验"补全"：奇幻武器镶宝石，战士穿甲，猛禽戴饰物〔学院推断〕 | 正向写出"素面 / 裸露"的可见状态 + 绝对否定 + 多 seed |
| 形制、尺度偏移 | C1-1 中脊和过宽、C1-3 体量偏大 | 向常见形制回归（往剑的方向画、把猛禽画大） | 形制写成几何事实；用画面里的物体当尺（停在肩上） |
| 环境先验 | C1-4 远山、C1-5 山崖和刻纹 | 奇幻外景默认加远山，石头默认带符文 | 正向写出背景里"是什么"（树干和树冠填满背景） |
| 几何精度 | C1-4 不是正圆 | 精确几何本来就是弱项 | "perfect round" + 选利于判读的机位 + 放大验收 |
| 方位属性 | C1-6 | 左右能互换；正面构图下会镜像 | 用**画面坐标**写方位 + 单独放大核验 |
| 程度、可读性 | C1-7 | "有"做到了，"一眼读出"没做到 | 把程度写成可判读的条件 + 缩略图、去色验收 |

〔学院推断〕"题材先验补全"的**验证方法**：同一锚点句做两版，一版去掉题材词（fantasy / warrior），一版保留，各跑 3 seed，统计装饰物出现率。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 背景根因（档案原文立场 + 机制证实）
- 本管线 `negative_prompt` 恒为空，cfg=1.0，negative 无效。生成器会自行添加装饰物，只能靠"提示词绝对否定式 + 多 seed 抽卡 + 逐特征放大验收"三件套对抗〔委托方实证·C1、T-2〕。
- 机制上已证实：ComfyUI 在 cfg≈1 时直接跳过无条件分支，也就是负向分支〔外部调研·S-COMFY-05〕；diffusers 中 `true_cfg_scale` ≤1 时会忽略 negative_prompt〔外部调研·S-COMFY-06〕；Qwen-Image-2.1 官方模板注释写着 "negative_prompt: unused while cfg is 1"〔外部调研·S-COMFY-04〕。板图（Qwen）和视频（H3）两侧都适用，前提是工作流 cfg=1，所以先查工作流 JSON 里的 cfg 值。

### 直接原因
1. 锚点卡的"禁用"只写在锚点卡上，或者只以否定词形式出现在提示词里。正向提示词没写这个表面**实际是什么样**，空白表面就由生成器按先验去填。
2. 方位、程度这两类属性（C1-6、C1-7）没有作为独立验收项，整体看着"像"就放行了。
3. 首版单 seed 就当候选。C1-1 和 C1-6 都是抽了 3 个 seed 才选出正确版。

### 方法论原因
4. 没有立下「禁用项优先于构图」：验收先看构图好不好看，禁用项就被好看的构图盖过去了〔委托方实证·C1 判据〕。
5. 把"写了"当成"做到了"。提示词里有否定句，不等于产出里没有那个东西；每一条禁用都要有对应的放大证据（见 C2）。
6. 〔学院推断〕C1-6 的方位反转，可能来自坐标系混用：角色自己的左右和画面的左右，在正面构图下互为镜像。锚点卡、提示词、验收三方里只要有一方用错坐标系，结果就会反。**验证方法**：查当时锚点卡和提示词里的方位措辞；同一镜做两版，A 用画面坐标（`the arm on the LEFT side of the frame`），B 用解剖坐标（`his left arm`），各跑 3 seed，统计正确率。

### 外部调研：冲突证据与新增根因
7. **否定词可能把东西招进来**：官方原则是 "Write bans as positives"，写出不要的元素，可能反而把它登记成内容〔外部调研·S-COMFY-08〕。社区实测"提到什么就长什么"，光要写成"暖光从一侧来"，不写"落地灯的光"〔外部调研·S-H3-09〕。Runway 说否定句不受支持，可能产生相反结果〔外部调研·S-VGEN-05〕；Veo 建议把排除项改写成正向的场景描述〔外部调研·S-VGEN-02、S-VGEN-03〕。
8. **反方证据**：一份小样本实测里，含 `No dialogue` 的 8/8 次都没出台词，没观察到"否定反而招来被排除内容"〔外部调研·S-ZEN-17〕。委托方在 C1、B3、D1 里用的绝对否定句，也确实修掉了问题。
9. **补充做法**：共用段只放每一颗都成立的元素〔外部调研·S-H3-09〕；角色视觉锁要写明配饰数量，并禁止改变服装拓扑〔外部调研·S-PIPE-01〕；尺度次序要带一个绝对参照〔外部调研·S-ZEN-05〕。单位距离和分数会被忽略，要拿画面里的物体当尺〔外部调研·S-H3-09〕。

## 修正过程（做了什么、第几轮、结果）

- 每个子案的修正方式和 seed 数见上表。可以数出来的结果是：C1-1、C1-6 各抽 3 个 seed 得到合格版；C1-7 复核后重写提示词，人类主创选定了新版〔委托方实证〕。
- 档案没有记录各子案修正后的出现率统计。R1 的 A/B 还没有在委托方节点上执行过。

### 学院立场 R1：禁用项怎么写（全学院以此为准）
1. **第一句写正向可见状态**，即这个表面实际是什么样：`the sword guard is plain polished steel, smooth and unadorned`。
2. **第二句写绝对否定**，只针对**已被证实会加出来**的物件。本卡 7 个子案里的宝石、铠甲、颈饰、远山、刻纹，以及 B3 的光柱，都属于这一类：`no gemstone, no jewel, no inlay on the guard`。
3. **做 A/B 验证**：A 版只写正向句，B 版写正向句 + 否定句，各 ≥3 seed，统计目标物出现率。视频镜用 `contact_sheet.py` 并排，静帧板图用 ffmpeg 并排（见判据）。结果写回 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1 的验证方法。
4. **禁止**只靠否定句；**禁止**写 `negative_prompt` 字段，它在这里无效，还会制造"已经处理过了"的错觉。
5. 锚点卡的 `禁用` 按契约写成绝对否定句 `no X`，`必现` 写成可见状态，两者都要写进提示词（[`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §3）。

### 7 个子案按 R1 重写（学院示例写法，〔学院推断〕待 A/B）
| 子案 | 第一句：正向可见状态 | 第二句：绝对否定 |
|---|---|---|
| C1-1 | `a Chinese straight dao with a single cutting edge and a flat blade with no ridge line; the guard is a plain polished steel disc, smooth and unadorned; exactly one tiny gem sits in a small notch at the very end of the hilt` | `no gemstone on the guard, no central ridge, not a double-edged sword` |
| C1-2 | `<原著给定的衣着可见描述>; his shoulders, arms and legs are covered only by cloth` | `no armor, no pauldrons, no bracers, no greaves, no armored skirt` |
| C1-3 | `a small raptor perched on <角色>'s shoulder, its body no wider than the shoulder; its neck shows only natural feathers` | `no jewelry at all, no collar, no neck ornament` |
| C1-4 | `a perfectly round lake with a clean circular shoreline, enclosed on all sides by dense forest; only tree trunks and canopy fill the background` | `no mountains, no distant peaks, no hills on the horizon` |
| C1-5 | `smooth, weathered, unmarked boulders; a ring of tree line encloses the area` | `no carved stone, no runes, no inscriptions, no cliff` |
| C1-6 | `the arm on the LEFT side of the frame is black; the arm on the RIGHT side of the frame is <另一臂外观>` | 方位不写否定句，靠画面坐标 + ≥3 seed + 单独放大核验 |
| C1-7 | `the arm on the LEFT side of the frame is pitch black and matte, in stark contrast to <躯干肤色>; the contrast reads at a glance`，板图版式加双臂特写 inset | 程度属性靠版式和验收，不靠否定句 |

- C1-1 的要点：护手不许有宝石，柄末却要一颗微宝石。**允许出现的同类物件，必须给出唯一的位置和精确的数量**（`exactly one … only at …`），否则一提"宝石"，宝石就会撒到别处去（S-H3-09 的机制 +〔学院推断〕）。
- C1-3 的要点：尺度用画面里的物体来量（停在肩上、不比肩宽），不要用"小型"这种相对词。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [目视] 「禁用项优先于构图」：板图和关键帧的验收顺序固定为 ① 禁用项逐条 → ② 必现项逐条 → ③ 方位属性 → ④ 程度属性 → ⑤ 构图与美感。①–④ 任一项不过，⑤ 不评〔C1〕。
- [目视] 每张板图按锚点卡的 `必现` / `禁用` 逐条**放大核验**，每条一张裁剪图。静帧用 ffmpeg：`ffmpeg -i board.png -vf "crop=W:H:X:Y,scale=iw*4:ih*4:flags=neighbor" crop-<项>.png`。视频用 `contact_sheet.py <clip> --crop 名=X:Y:W:H`。`contact_sheet.py` 只接受视频输入〔C1、C2〕。
- [目视] 方位、朝向类属性（左右臂、持刀手、伤疤在哪一侧）单独裁剪放大确认，结论用**画面坐标**记录〔C1-6、C1-7〕。视频提示词里出现"角色自身左右"（left hand / right arm）时，`direction_audit.py` 会把它记为 DIR-check 需目视，见到就核。
- [目视] 程度类属性（对比、大小、数量）按观看尺寸判：缩到 270 宽（`contact_sheet.py` 默认格宽）并去色（ffmpeg `format=gray`）后，仍然"一眼读出"才算过〔C1-7〕。
- [自动] 锚点卡的 `禁用` 全部写成 `no X` 绝对否定句。`prompt_lint.py` 的 VP-anchor info（非符号锚点的禁用项没写进提示词）按学院口径视为必修〔C1；format-contracts §3〕。
- [自动] `prompt_lint.py` VP-negative 报出 `negative_prompt` 时，把它删掉〔C1、T-2〕。
- [目视] 每一句禁用句前面，都有一句对应的正向可见状态句（R1）。只有否定句、没有正向句的，不得 run。
- [目视] 关键资产 ≥3 seed（P2、M6），首版不得直接定稿；落选版归档到 `assets/boards/_rejected/`〔format-contracts §3〕。
- [目视] 新增禁用句时，同时记下 A/B 结果（A 正向、B 正向+否定，各 ≥3 seed 的出现次数）。没做 A/B 的否定句，在锚点卡上标"未验证"。

## → 行为改变（下次……）

- 下次写锚点卡时，每一条 `禁用` 旁边都配一句"这个表面实际是什么样"的正向可见状态，两句一起写进所有含该资产的提示词。
- 下次生成关键资产，直接排 ≥3 个 seed。第一版看着"差不多"也不停。
- 下次验收板图，先按锚点卡逐条裁剪放大，最后才看构图。**禁止**用"整体很好看"抵消任何一条禁用项。
- 下次写方位，一律用画面坐标（`LEFT / RIGHT side of the frame`），不用角色自身的左右；方位单独放大验收。
- 下次遇到"对比、大小、数量"类要求，把它写成可以判读的条件，并在缩略图 + 去色下验收。
- 下次想写 negative_prompt 时，改成"正向可见状态 + 绝对否定"，写进正向提示词。
- 下次进入视频阶段，把板图阶段被违反过的禁用项原样带进视频提示词，并在抽帧时逐条复核。视频是重新采样，同一个装饰物可能被再加一次。〔学院推断；验证：对含该资产的镜，在接触表上逐条复核禁用项，统计复发率。〕

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ cfg=1 的管线和 CFG 蒸馏模型普遍没有可用的负向通道（H3 权重本身就是 CFG 蒸馏的〔外部调研·S-H3-02〕）。"正向可见状态 + 否定 + 多 seed + 放大验收"对任何生成器都适用。
- ★ 换模型时：如果新管线 cfg>1 且 negative 生效〔外部调研·S-COMFY-06〕，negative 字段可以**额外**使用，但不能替代正向句和验收。
- ★ 同题材迁移：题材先验补全的方向（奇幻 → 宝石、铠甲、符文、远山）可以直接搬到同类项目，作为禁用清单的初稿。
- ☆ 7 个具体资产，以及它们各自的错误变体，属于本项目。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/casting-and-canon/SKILL.md`](../../20-craft/casting-and-canon/SKILL.md)（锚点卡：必现 / 禁用 / 方位属性）、[`20-craft/asset-boards/SKILL.md`](../../20-craft/asset-boards/SKILL.md)（多 seed + 逐特征放大）、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)（禁用项优先于构图）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（R1 两句式）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（视频阶段禁用项复核）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)。
- 判据清单：[`50-rubrics/checklists/board.md`](../../50-rubrics/checklists/board.md)、[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/direction_audit.py`](../../50-rubrics/scripts/direction_audit.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-08.md`](../../60-casebook/drills/DR-08.md)（禁用项）。
- 相邻案例与正面资产：[`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md)（C1-7 的验收侧）、[`60-casebook/cards/D4-symbol-errors.md`](../../60-casebook/cards/D4-symbol-errors.md)（对抗约束）、[`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)（光柱否定句）、[`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md)（禁令包兜底）、[`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)（画面坐标）、[`60-casebook/positive-assets.md`](../../60-casebook/positive-assets.md)（P1、P2、P3、M6、M8）。
