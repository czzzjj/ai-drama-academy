# 风格卡 · Q 版（chibi）

> 一句话：靠**比例体系 + 大色块 + 一个放大的记号**认人。一个画面或一个运动段**只承载一个因果单位**。可爱不等于持续弹跳。〔外部调研·S-ZEN-20〕
> 选用技能：[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md)、[`20-craft/script-doctor/SKILL.md`](../../20-craft/script-doctor/SKILL.md)、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)

## 适用题材 / 不适用
- **适用**：轻喜剧、萌宠、职场喜剧、知识科普式短剧、番外/彩蛋、正剧角色的 Q 版小剧场。这类内容通常旁白承担主要信息，画面负责证据和后果〔外部调研·S-ZEN-20〕。
- **不适用**：需要压迫感、尺度感的正剧打斗。Q 版比例会消解威胁。正剧里插 Q 版段是合法的，但必须在 `visual-bible.md` 声明切换点。

## 身份锚点载体
- **头身比一旦选定就是硬约束**：不同角色可以有不同头身比，同一角色跨镜不能变〔外部调研·S-ZEN-20〕。锚点句写成数字：`2.5 heads tall`。
- 认人靠发型剪影、主色块，加一处故意放大的特征（眼镜、呆毛、围裙、工牌）。五官细节不做锚点。
- 角色之间的相对尺度写绝对参照：`standing straight, A's head top reaches B's shoulder`〔外部调研·S-ZEN-05 的识别锚点写法：可见、可生成、可比较〕。

## 关键词包（EN）〔学院推断，验证：3 seed 并排量头身比；用 ffmpeg crop 量头高和身高像素比〕
| 层 | 短语 |
|---|---|
| 风格总述 | `chibi style, {2.5} heads tall, oversized head with a small rounded body`, `flat colors with two-step shading` |
| 记号放大 | `her round glasses are drawn oversized, nearly as wide as her face` |
| 色彩焦点 | `the hazard {object} is the only saturated red in the frame; everything else is softened pastel` |
| 材质三类 | `soft (cloth, skin)`, `hard (metal, plastic)`, `clear (glass, liquid)`，够用即止 |
| 运动 | `only her right hand moves, placing the cup on the table; the rest of her body holds the pose` |

## 负面词改写
| 习惯负面词 | 正向可见状态句 | 追加绝对否定（条件） |
|---|---|---|
| `realistic proportions` | `{2.5} heads tall, head as wide as the shoulders` | A/B 出现比例拉长时追加 |
| `detailed face, nose` | `face drawn with two dot eyes and a small curved mouth` | — |
| `bouncing, wobbling` | 明写"只有某只手或某个物体动，其余保持" | — |
| `cute, kawaii, adorable` | **删掉**，这是评价词（R-VP-16）。改写成比例、色块、记号这些可见规格 | — |
| `emoji, sweat drop, symbols`（不想要的漫符） | 不写任何漫符名词（提到即生长〔外部调研·S-H3-09〕）；需要漫符时在后期叠层 | 已证实会自加时追加 |
> 禁止使用 negative_prompt 字段〔委托方实证·C1、T-2〕。

## 灯光色调
- 平涂、两段明暗、高饱和主色，再加少量指示性高光。「危险物用画面里唯一的高饱和红，其余降饱和」可以执行；「可爱风格」「明快色调」不能执行〔外部调研·S-ZEN-20〕。
- 本风格默认高调光，光比约 1:1〔外部调研·S-CRAFT-15〕。色彩脚本仍要有起伏（R-COL-03），否则全片情绪平。

## 运动特性（H3 / Qwen）
- 一个运动段只放一个因果单位，默认 hold 加局部动〔外部调研·S-ZEN-20〕。一镜塞进多个因果单位，观众只记得最后一个。
- 挤压拉伸、预备动作适合 Q 版夸张〔外部调研·S-STORY-22〕。写成可见事件，不写法则名。
- 头身比在大幅运动中可能漂移〔学院推断。验证：接触表 FIRST / MID / TAIL 三格各量一次头高和身高的像素比，偏差 >10% 判漂移〕。量法：`ffmpeg -i clip.mp4 -vf "select='eq(n,0)+eq(n,120)',scale=270:-2,tile=2x1" -frames:v 1 ratio.png`（第 0 帧与第 120 帧并排），然后目视标注。
- 打斗在 Q 版里会被比例消解成玩闹。若剧本承诺"打斗"，仍要有可见的交手回合（委托方实证 A2）。

## 失败模式
1. 全员持续弹跳，因果读不出来〔外部调研·S-ZEN-20〕。
2. 一镜塞进多个因果单位。
3. 漫符、箭头代替了事实：箭头指向被当成"已经展示"。
4. 后期文字压住脸或放大记号，用 TJ-12 空白安排、R-PUB-18 安全区检查。
5. 为了可爱牺牲事实准确性或安全边界（危险动作被完整演示）。

## 风格锁句模板
```text
STYLE-LOCK (chibi): chibi style; every character keeps the same head-to-body ratio in every shot ({A}: 2.5 heads, {B}: 3 heads); flat colors with two-step shading; one oversized signature item per character ({A}: round glasses, {B}: red scarf); only one thing moves per beat; palette {pastel 1}, {pastel 2}, {accent red}.
```

## 参考来源
〔外部调研·S-ZEN-20〕形态卡"Q 版表达"；〔外部调研·S-ZEN-17〕；〔外部调研·S-STORY-22〕；〔外部调研·S-CRAFT-15〕；〔外部调研·S-H3-09〕；〔委托方实证·A2、C1〕。

## → 行为改变
- 下次用 Q 版，锚点卡的锚点句必须含头身比数字。验收时抽 FIRST 和 TAIL 两帧量比例，不靠"看起来差不多"（委托方实证 C2：验收放水）。
- 下次写 Q 版分镜，每拍只写一个因果单位。超出就拆拍或拆镜，同时守住 ≥124 帧下限。
