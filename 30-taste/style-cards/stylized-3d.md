# 风格卡 · 风格化三维（stylized-3d）

> 一句话：靠**比例 + 剪影 + 材质分区**认人。"接触即有声、接触即有重量"，摄影机是最贵的一层。〔外部调研·S-ZEN-20〕
> 选用技能：[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md)、[`20-craft/action-choreography/SKILL.md`](../../20-craft/action-choreography/SKILL.md)、[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)

## 适用题材 / 不适用
- **适用**：奇幻冒险、合家欢、萌宠或非人主角、系统流、科幻轻喜剧。卡通化角色能绕开恐怖谷，有创作者正是这样用卡通外星角色规避恐怖谷的〔外部调研·S-CASE-06〕。
- **不适用**：要靠细腻真人微表情承重的情感剧。三维卡通脸的表情幅度偏大，用基础情绪词生成会得到夸张的卡通表情〔外部调研·S-CRAFT-21〕。

## 身份锚点载体
- 写比例和剪影，不写妆造：头身比、肩宽、手长、材质分区（哪块是布、哪块是皮革、哪块是金属）〔外部调研·S-ZEN-20〕。
- 必须多写一项别的风格不写的：**哪些比例和剪影不能被广角畸变或姿势掩盖**。
- 剪影测试见 TJ-02（[`30-taste/judgment-cards.md`](../judgment-cards.md)）：主要角色填成纯黑，仍要认得出是谁。

## 关键词包（EN）〔学院推断，验证：3 seed 接触表 + TJ-02 剪影〕
| 层 | 短语 |
|---|---|
| 风格总述 | `stylized 3D animated feature look`, `soft subsurface skin`, `slightly exaggerated proportions: {head-to-body ratio} heads tall` |
| 材质（表面怎样响应光） | `rough matte wool`, `glossy elongated highlight streaks on wet asphalt`, `semi-translucent ears glowing at the edges in backlight` |
| 体积介质 | `light dust hanging in the air catching the window light`（有介质才有体积光；只写 god rays 会招来实物光柱，见 B3） |
| 接触与重量 | `her boots sink slightly into the mud as she lands`, `the crate dents under his weight` |
| 摄影机空间 | `camera height at the character's chest`, `the axis stays on one side` |

## 负面词改写
| 习惯负面词 | 正向可见状态句 | 追加绝对否定（条件） |
|---|---|---|
| `floating feet` | `both feet planted on the stone floor, soles touching the ground, a soft contact shadow under each foot` | — |
| `clipping, intersecting` | 写清接触点：`his right hand grips the sword at the lower half of the hilt` | — |
| `realistic human skin` | `stylized smooth skin with simplified pores, painted cheek color` | A/B 出现真人化时追加 |
| `smooth, fluid motion`（这是好词，但没法验证） | 换成可验证的重量描写：下沉、形变、余势〔外部调研·S-ZEN-20〕 | — |
> 禁止使用 negative_prompt 字段，原因同 R1〔委托方实证·C1、T-2〕。

## 灯光色调
- 写表面怎么响应光：粗糙还是光滑，高光是圆点还是拉长的条，透光还是不透光，边缘有没有轮廓光，体积光里有没有介质〔外部调研·S-ZEN-20〕。
- 同场两镜光向相反，是本风格最常见的穿帮之一。R-COL-05 要求同场全部关键帧并排，光向一致。
- 皮克斯式色彩脚本：情绪强就加浓，危险段转灰浊〔外部调研·S-CRAFT-13〕。每段写一格（R-COL-01）。

## 运动特性（H3 / Qwen）
- 默认可以全动作，但承担因果的接触事件（递交、抓握、推倒、落地）**必须在镜内完成**；长距离位移、转身交给剪辑〔外部调研·S-ZEN-20〕。
- H3 双人接触：动词只写一个最差（掌掴三次都只是"碰一下"）；写全"接近—接触—施力—结果"最好〔外部调研·S-ZEN-17〕（R-SB-20）。
- 摄影机运动必须有动机：跟随、揭示、施压。不为炫技拍连续长镜。H3 每次生成只给一个主运镜〔外部调研·S-H3-10〕（R-VP-24）。
- 动画十二法则中的挤压拉伸、预备、跟随动作适合本风格夸张化〔外部调研·S-STORY-22〕。写进提示词时要写成可见事件（`his body squashes as he lands, then springs upright`），不写法则名。

## 失败模式
1. 脚离地、穿模、持物无来源换手〔外部调研·S-ZEN-20〕。接触表逐格查脚底和握持点（R-VID-01）。
2. 同场光向翻转或轴线翻转，属于委托方实证 A5 的空间混乱，三维风格里同样成立。
3. 摄影机运动没有动机，只为显示"空间存在"，属于委托方实证 A4 的运镜脱钩。
4. 用「流畅」「自然」代替能验证的接触和重量。
5. 混进二维层时，身份边缘被两层同时决定，边缘抖动，改也改不动〔外部调研·S-ZEN-20〕。

## 风格锁句模板
```text
STYLE-LOCK (stylized-3d): stylized 3D animated feature still; {N}-heads-tall proportions kept identical in every shot; material zones: {zone 1}, {zone 2}, {zone 3}; key light from the {LEFT/RIGHT} at {height}, {color temperature}; air holds faint {dust|mist} so light has visible volume; palette {color 1}, {color 2}, {color 3}.
```

## 参考来源
〔外部调研·S-ZEN-20〕形态卡"风格化三维"；〔外部调研·S-ZEN-17〕双人接触实测；〔外部调研·S-CASE-06〕卡通角色规避恐怖谷；〔外部调研·S-CRAFT-13、S-CRAFT-21〕；〔外部调研·S-STORY-22〕；〔外部调研·S-H3-10〕。

## → 行为改变
- 下次用本风格写接触动作，先列"接触点表"（谁的哪只手 → 物体哪一段），再写提示词；接触点没写清的镜不得送 H3。
- 下次验收本风格镜头，接触表必须逐格标出脚底是否着地。只看"动作流畅"不算验收。
