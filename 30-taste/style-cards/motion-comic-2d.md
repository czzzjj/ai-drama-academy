# 风格卡 · 二维动态漫（motion-comic-2d）

> 一句话：默认**有限运动**（limited motion）。静止是主动选择的注意力，不是缺陷；每镜只让承担因果的那一层动起来。〔外部调研·S-ZEN-20〕
> 选用技能：[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md)、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)

## 适用题材 / 不适用
- **适用**：漫画、网文改编的"漫剧"（系统流、逆袭、重生穿越、悬疑规则）。旁白、对白占比高、预算低，每集需要快速产出。
- **不适用**：卖点是连续打斗、需要真实接触的动作戏。有限运动会把打斗退化成"姿势切换 + 特效层"，对应委托方实证 A2。如果题材承诺了打斗，至少要有一段全动作的交手回合（R-SB-20），其余用定帧。
- 外部数据：AI 漫剧已经有单独的行业统计〔外部调研·S-PLAT-13〕；红果一季度下架违规漫剧 1718 部〔外部调研·S-PLAT-08〕。这条赛道已被平台单独治理，同质化就是风险。

## 身份锚点载体
- 认人靠**轮廓剪影 + 线条特征 + 固定色块**：发型剪影、脸型比例、服装色块划分，再加一两个不能省的图形记号（领口形状、发饰、袖口条纹）〔外部调研·S-ZEN-20〕。
- 不要拿眼神、写实五官当锚点，二维每个角度都会重画。本风格必做剪影测试 TJ-02（[`30-taste/judgment-cards.md`](../judgment-cards.md)）：角色填成纯黑，仍要认得出是谁。

## 关键词包（EN）〔学院推断，验证：3 seed 接触表，逐镜核对描边粗细和阴影分区〕
| 层 | 短语 |
|---|---|
| 风格总述 | `2D motion comic panel`, `flat color blocks`, `{uniform | tapered} black outlines on every figure` |
| 色块关系 | `base color / shadow color / highlight color in three flat zones`, `hard-edged shadow falling on the {LEFT/RIGHT} half of the face` |
| 可动层（每镜显式写） | `only her hair tips and coat hem move in the wind; her body holds the pose` |
| 视差 | `foreground leaves drift slowly across the frame while the background stays still` |
| 静止人物 | `standing in place, breathing softly, blinking once`〔外部调研·S-H3-08〕 |

## 负面词改写
| 习惯负面词 | 正向可见状态句 | 追加绝对否定（条件） |
|---|---|---|
| `3d shading, volumetric, subsurface` | `flat color blocks with hard-edged two-tone shadows` | 已证实混入三维质感时才追加 |
| `inconsistent outlines` | `every figure has the same {2px-equivalent} black outline in every frame` | — |
| `speech bubble, text, sfx letters` | 不写任何气泡或文字类名词。对白气泡和拟声字一律后期叠层，属于委托方实证 D2 的原则 | D1 禁令句固定放末行 |
| `everything moving` | 明写可动层清单，其余写 `holds still` | — |
> 禁止使用 negative_prompt 字段〔委托方实证·C1、T-2〕。

## 灯光色调
- 可执行的是**色块关系**，不是物理光：主色、阴影色、高光色三段怎么分，阴影边界硬还是渐变，描边颜色随不随环境变〔外部调研·S-ZEN-20〕。
- **禁止**把三维光影词（次表面散射、体积光、物理材质）写进二维提示词，否则质感撕裂。

## 运动特性（H3 / Qwen）
- 一镜只让承担因果的那一层全动。其余交给 hold pose、局部循环（呼吸、发梢、衣摆）、背景视差或效果层；冲击可以用效果层加顿帧承接〔外部调研·S-ZEN-20〕。
- **FL2VA 动漫风帧率减半**〔外部调研·S-H3-13，#74 单帖报告〕：本风格本来就接受一拍二，但要是**设计选择**，不能是意外。用 [`30-taste/style-cards/guoman-2d.md`](guoman-2d.md) 里的 mpdecimate 命令量一次，结果写进 `qc/<SHOT>.md`。
- `Fixed camera.` 可以可靠地锁住机位〔外部调研·S-ZEN-17〕。本风格大多数镜应锁机位，靠视差制造纵深。
- 委托方实证 A1 的警告在本风格最危险：漫剧"一格一镜"的惯性，会直接复刻 29 镜、均长 2.96s 的碎镜。生成单位仍必须 ≥124 帧〔委托方实证·T-2〕；快节奏在剪辑里从长镜中取 CUT（R6）。
- 纯定帧加推拉的镜可以本地做，对冻结关键帧用 ffmpeg `zoompan` 缓推，不必送 H3〔学院推断。验证：本地版与 H3 版并排，交独立评审盲选〕。

## 失败模式
1. 所有图层同时轻微飘动，观众看不出谁在动〔外部调研·S-ZEN-20〕。
2. 阴影分区逐镜换逻辑，描边时有时无。
3. 效果层盖住身份锚点，剪影认不出人。
4. 背景密度过高抢走注意力，人物退成贴纸，可用 TJ-03 画面密度检查。
5. 一格一镜造成碎镜，属于委托方实证 A1。
6. 同质化：和同平台漫剧撞脸、撞构图，下架风险〔外部调研·S-PLAT-07、S-PLAT-08〕。

## 风格锁句模板
```text
STYLE-LOCK (motion-comic-2d): 2D motion comic panel; flat color blocks in three zones (base / shadow / highlight); {uniform black} outlines of identical weight on every figure; shadows hard-edged on the {LEFT/RIGHT}; only the listed moving layer moves: {layer}; everything else holds still; palette {color 1}, {color 2}, {color 3}.
```

## 参考来源
〔外部调研·S-ZEN-20〕形态卡"二维动态漫"；〔外部调研·S-H3-13〕#74；〔外部调研·S-ZEN-17〕；〔外部调研·S-PLAT-13、S-PLAT-08、S-PLAT-07〕；〔委托方实证·A1、A2、T-2〕。

## → 行为改变
- 下次用本风格写分镜，每镜在 `内容` 列写一行"可动层清单"。清单写不出，说明这一镜没有因果事件，回剧本删掉或合并。
- 下次看到漫画原作"一格一个画面"，禁止照搬成一格一镜；先把一个动作链合成一个 ≥124 帧的段。
