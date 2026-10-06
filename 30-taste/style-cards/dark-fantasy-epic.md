# 风格卡 · 暗黑奇幻史诗（dark-fantasy-epic）

> 一句话："史诗感"是**画面级**属性，由起始帧决定：尺度对比、低机位、纵深、有来源的低调光。再加上**事件 + 后果**，以及蓄力和释放的节奏与声音。形容词渲染不出来。〔委托方实证·M2、M3、G5〕
> 选用技能：[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)、[`20-craft/action-choreography/SKILL.md`](../../20-craft/action-choreography/SKILL.md)、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)、[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)
> 本卡不在 S-ZEN-20 的六张形态卡里，是学院依据委托方实证和外部调研组合出来的。委托方被打回最多的就是这类戏：BOSS 战、神、斩龙闪、ф 印记、尼加狄黑臂。

## 适用题材 / 不适用
- **适用**：玄幻、魔幻、神话战争、BOSS 战、末日、克苏鲁。底色可以是写实，也可以是国漫；本卡叠在底色卡上，只管光、尺度和事件。
- **不适用**：日常、轻喜剧。低调光会让手机小屏看不清脸（R-COL-08）。

## 身份锚点载体
- 继承底色卡的锚点规则。本风格另外要锁三类**会被生成器自己加装饰的东西**：武器形制、铠甲有无、首饰〔委托方实证·C1-1、C1-2、C1-3〕，以及关键符号〔委托方实证·D4〕。
- 方位类属性（黑臂在哪一侧、持刀手）必须单独放大确认〔委托方实证·C1-6、C1-7〕（R-BRD-06）。

## 关键词包（EN）〔委托方实证短语照抄；其余为学院推断，验证：3 seed + TJ-11 尺度参照〕
| 层 | 短语 |
|---|---|
| 尺度（起始帧） | `low camera at knee height looking up`, `{the god} on the LEFT fills two-thirds of the frame height while {Su Xiao} on the RIGHT stands no taller than its knee`, `ruined pillars receding into deep haze` |
| 有来源的光 | `the only light is {lava glow | moonlight | burning braziers} from {direction}`, `warm firelight falls across the left side of her face`（被动描述，不写灯具） |
| 事件（不写评价词） | `a shockwave ring bursts outward from the point of contact, flattening the dust in a circle`〔委托方实证·M3〕 |
| 后果 | `cracks race across the stone floor`, `debris rains down for a second afterwards` |
| 武器（对抗约束写法） | `a Chinese straight single-edged blade with no central ridge; the guard is plain polished steel, smooth and unadorned; one small gem set in the pommel groove`〔委托方实证·C1-1；R1〕 |
| 符号 | `exactly one red ring crossed by exactly one vertical bar, top to bottom; no horizontal line, no cross sign, no plus sign, no second bar`〔委托方实证·D4〕 |
| 速度 | `Real-time speed throughout, no slow motion`〔委托方实证·A3〕 |

## 负面词改写
| 习惯负面词 / 反馈词 | 正向可见状态句 | 追加绝对否定（条件：已证实会自加） |
|---|---|---|
| `epic, grand, spectacular, cinematic` | **删掉**（R-VP-16）。拆成尺度 + 事件 + 后果 + 光 + 声音五栏（G5） | — |
| `no armor`（原著无装备） | `wearing only a sleeveless linen tunic and cloth trousers, bare arms` | `no armor, no pauldrons, no gauntlets`〔委托方实证·C1-2〕 |
| `no jewelry`（猛禽） | `a small raptor small enough to perch on a shoulder, plain brown feathers` | `no jewelry at all`〔委托方实证·C1-3〕 |
| `god rays, magic beam`（不想要光柱） | `warm ambient light falls on their faces` | `no flashlight, no torch beam, no spotlight`〔委托方实证·B3〕 |
| `mountains in background`（不该有远山） | `a perfectly round lake enclosed by dense forest on every side` | `no distant mountains`〔委托方实证·C1-4〕 |
| `runes, carvings` | `smooth weathered boulders, bare stone surfaces` | `no carved stone, no runes`〔委托方实证·C1-5〕 |
> 每条追加的否定句都要按 R1 做 A/B（只写正向句 / 正向句 + 否定句），各 3 seed，记录目标物出现率（R-BRD-13）。禁止使用 negative_prompt 字段。

## 灯光色调
- 低调光，主辅光比约 8:1，用于惊悚、恐怖、暗黑剧〔外部调研·S-CRAFT-15〕。光源必须能在画面里指认，或能从场景推断（岩浆、月、火盆、法阵），补光色温要和光源一致〔外部调研·S-CRAFT-14〕。
- 光写成被动描述（`warm light falls from the left`），不写会被生成成实物的灯具或光柱〔外部调研·S-H3-09；委托方实证·B3〕（R-COL-04、R-VP-14）。
- 手机小屏上暗部会丢细节：低调段的关键帧缩到 270 宽后，脸和表情仍要认得出〔学院推断，见 R-COL-08〕。
- 色彩脚本里暗黑不等于全片一个色。蓄力段冷、压，爆发段给一个暖色焦点，余波段降饱和（R-COL-03）。

## 运动特性（H3 / Qwen）
- H3 大场面动作和物理互动偏弱〔外部调研·S-CASE-10〕。所以史诗感要押在**起始帧尺度**和**单一主运镜**上（上摇揭示巨物、拉远交代规模），不押在复杂群战上。
- 每次生成只有一个主运镜。顿挫、震动写成事件引起的相机响应：`the frame jolts as the blade hits the stone`（R5，R-VP-24）。起幅要放在主体最大的一端：要以紧景收束的镜，必须从宽景开始〔外部调研·S-H3-08〕（R-KF-09）。
- 打斗：打击拍可以密，空间拍 ≤2–3（R4）。单轴定侧，删掉一切 truck、arc、orbit〔委托方实证·A5、M4〕。
- 锁子甲、花纹这类高频细节在低步数下容易出"三角网格伪影"，官方建议高频细节最多可到 50 步〔外部调研·S-COMFY-09〕。turbo 只用于预览（R-VP-23）。出现伪影时，同镜跑 20 步和更高步数的 A/B，结果记进生成日志。
- H3 片尾前 1.2–1.7 秒常崩解，生成时加 1.3–1.5 秒尾部余量（R-VP-22）〔外部调研·S-H3-09〕。

## 失败模式（委托方真实踩过的，全部在本风格高风险区）
1. 「全是几个简单动作的慢镜头」：委托方实证 A2、A3，打斗缺席，没有速度层次。
2. 「苏晓乱跑」：委托方实证 A5，换边运镜词和起始帧打架。
3. 「特效不够」：委托方实证 M3、G5，写了评价词，没写事件。
4. 装饰物被自动加上（宝石、铠甲、颈饰、刻纹）：委托方实证 C1。
5. 符号画错，十字代替竖线：委托方实证 D4。
6. 暗到看不清，冷观众标"看不懂"〔学院推断〕。

## 风格锁句模板
```text
STYLE-LOCK (dark-fantasy-epic, layered on {base style}): low-key dark fantasy; contrast about 8:1; the only light comes from {source} on the {LEFT/RIGHT}, {color temperature}; deep haze gives three depth layers; the human figure is always small against {the giant/the ruins} for scale; palette {ash grey}, {ember orange}, {bruise purple}.
```

## 参考来源
〔委托方实证·M2、M3、A2、A3、A5、B3、C1、D4、G5〕；〔外部调研·S-CRAFT-14、S-CRAFT-15〕；〔外部调研·S-H3-08、S-H3-09、S-CASE-10、S-COMFY-09〕。

## → 行为改变
- 下次被要求"更史诗"，禁止在视频提示词里加形容词。先回到起始帧，按 TJ-11 检查尺度参照、低机位、纵深、光源四项，缺哪项补哪项，重出关键帧。
- 下次写本风格任何角色或道具，先查锚点卡的禁用清单里有没有 C1 子案中出现过的装饰类别。没有就补上，并按 R1 写正向句。
