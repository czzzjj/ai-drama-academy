# 风格卡 · 写实电影（cinematic-realism）

> 一句话：写实风格靠**造型状态**和**有来源的光**认人、取信。生成器最容易在这里露馅：脸僵、恐怖谷，还有被平台认定为"AI 脸"。〔外部调研·S-ZEN-20、S-CASE-01、S-PLAT-07〕
> 选用技能：[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md)、[`20-craft/performance-direction/SKILL.md`](../../20-craft/performance-direction/SKILL.md)、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)

## 适用题材 / 不适用
- **适用**：都市、职场、悬疑、刑侦、家庭伦理、复仇打脸、豪门婚恋。这类竖屏真人短剧的主流审美要靠"像真的"取信。
- **慎用**：重度奇幻打斗、大型生物、群像战争。H3 在大场面动作和物理互动上偏弱〔外部调研·S-CASE-10〕，写实风格会把这些缺陷全部暴露出来。真要做，先读 [`30-taste/style-cards/dark-fantasy-epic.md`](dark-fantasy-epic.md)。
- **合规前提**：禁止用真实人物照片、明星脸做参考，"AI 偷脸"已有下架案〔外部调研·S-PLAT-09〕，见 R-BRD-17、R-PUB-14。在海外平台发布逼真的 AI 人物，必须打开 AI 披露〔外部调研·S-PLAT-25、S-PLAT-23〕。

## 身份锚点载体
- 写实风格认人靠的是**可比较的造型状态**，不是长相评价：发型走向和凌乱度、袖子挽到哪、扣子扣到第几颗、随身物的固定位置、伤妆的位置和进展。〔外部调研·S-ZEN-20〕
- 「英俊坚毅」写了等于没写，要写成「左眉一道旧疤，右手食指缠创可贴」这种可执行的状态。
- 最常断的地方：袖口衣褶、烟酒食物的消耗量、伤妆的进展方向。这些都要登记进状态账本（R-SEA-15）。

## 关键词包（EN）〔学院推断，验证方法见本节末〕
| 层 | 短语 |
|---|---|
| 风格总述 | `photorealistic live-action drama still`, `natural skin texture with visible pores`, `shot on a 9:16 vertical frame` |
| 光（来源 + 方向 + 遮挡 + 反射 + 用途） | `daylight from a window behind her on the LEFT`, `venetian blinds cut the light into stripes across his chest`, `the metal badge is the only bright highlight in frame` |
| 材质（要能被光验证） | `pilled wool sweater`, `cotton shirt washed pale`, `dried blood darkened to brown`, `rain-soaked fabric clinging to the shoulders` |
| 色彩关系 | `{who} is the brightest element`, `{object} is the only saturated red in frame` |
| 表演（交给 performance-direction） | 写成变化：`her expression shifts from polite neutrality to a tight, suppressed anger, jaw setting, eyes narrowing, settling into stillness`〔外部调研·S-H3-08〕 |
- 镜头名和机身名（`Cooke S4 50mm`）基本不起作用；写画面里会出现的器材，器材会被画出来〔外部调研·S-H3-08〕。**禁止**用器材名代替构图描述。
- **验证**：3 seed 对比接触表。重点看脸部裁剪：质感是"蜡像皮肤"还是"有毛孔"；手部是否完整。结论写进 `qc/<SHOT>.md`。

## 负面词改写
| 习惯负面词 | 正向可见状态句 | 追加绝对否定（条件） |
|---|---|---|
| `plastic skin, airbrushed` | `natural skin texture with faint pores and slight unevenness under soft side light` | — |
| `cartoon, anime, illustration` | `photorealistic live-action still, natural lens depth of field` | 只有在 A/B 中出现插画化时才追加 |
| `ugly, deformed hands` | `both hands relaxed, fingers naturally curved, holding {object} by the {part}`（手部动作写全，减少自由发挥） | — |
| `cinematic lighting, masterpiece` | **删掉**。这是评价词，不是规格（R-VP-16）。改写成光源 + 方向 + 色温 + 光比档 | — |
| `no smoke`（场景不该有烟） | **什么都不写**，免得招进来〔外部调研·S-COMFY-08、S-H3-09〕 | 已证实会自加时才追加 |
> 禁止使用 negative_prompt 字段〔委托方实证·C1；外部调研·S-COMFY-05〕。视频块末行固定写 D1 禁令句〔委托方实证·D1〕。

## 灯光色调
- 光必须有来源，能指认或能推断：窗、门、台灯、屏幕、火、月、车灯〔外部调研·S-CRAFT-14〕。补光色温要和光源一致：月光偏冷，烛光偏暖。
- 光比档跟着情绪走：紧张、悬疑段用低调光，约 8:1；轻松段用高调光，约 1:1〔外部调研·S-CRAFT-15〕（R-COL-06）。
- 青橙只是"人物和环境分离"的一种手段，不是默认 LUT〔外部调研·S-CRAFT-16〕。全片同一套青橙判不通过（R-COL-03）。
- 「电影感」「高级灰」「大师光」「氛围感」都不能执行，禁写〔外部调研·S-ZEN-20〕。

## 运动特性（H3 / Qwen）
- 写实风格默认全动作。预算问题反过来，是**哪些必须限制**：同一镜里并行的动作数、道具交接的手数、台词和动作谁先谁后〔外部调研·S-ZEN-20〕。
- **观众差评集中在脸**：「面部表情太僵硬」「没有灵魂」是公开的 AI 剧差评点〔外部调研·S-CASE-01〕。H3 讨论区也有人报告几乎不眨眼〔外部调研·S-H3-13〕。处置：静止人物写 `breathing softly, blinking and shifting weight a little as people naturally do`〔外部调研·S-H3-08〕；表情拍 ≤2–3 个（R-PRF-04）；微表情特写只用固定机位（R-PRF-09）。
- 多人对白镜要给非说话人写闭嘴句，不然口型会落到错的人身上（R-VP-18）〔外部调研·S-ZEN-17〕。
- 两个男声音色相近，季级要给每个有台词的角色绑定音色来源（R-SEA-13）。

## 失败模式
1. 蜡像脸、塑料皮，不眨眼。冷观众最先出戏的地方〔学院推断，验证：冷观众断点记录里"假""不像人"的标注集中在哪些镜〕。
2. 造型跨镜"自动整齐"，伤妆自己消退〔外部调研·S-ZEN-20〕，对应委托方实证 B1 一致性体系缺陷。
3. 用形容词代替光源，审片时没法比较。
4. 把情绪写成症状（发抖、冷汗、瞳孔放大），用一套通用微表情顶替人物正在处理的对象和选择〔外部调研·S-ZEN-20〕。
5. 主角脸被平台判为"高频 AI 脸"或与真人撞脸〔外部调研·S-PLAT-07、S-PLAT-09〕。

## 风格锁句模板
```text
STYLE-LOCK (cinematic-realism): photorealistic live-action vertical drama still; natural skin texture; light comes only from {practical source} on the {LEFT/RIGHT}, {color temperature}, {low-key ~8:1 | soft ~2:1 | high-key ~1:1} contrast; palette {color 1}, {color 2}, {color 3}; {who} is the brightest element in frame.
```
- 每场换一次光源从句，并登记进色彩脚本（R-COL-01、R-COL-04）。"每场加一句光与色温，再挂一张定调图"这个做法，实测让同场 13 张关键帧的平均亮度离散度从 18.3 降到 6.6〔外部调研·S-ZEN-17、F-ZEN-15〕。

## 参考来源
〔外部调研·S-ZEN-20〕形态卡"实拍"；〔外部调研·S-CRAFT-14、S-CRAFT-15、S-CRAFT-16〕；〔外部调研·S-CASE-01、S-CASE-10〕；〔外部调研·S-H3-08、S-H3-13、S-ZEN-17〕；〔外部调研·S-PLAT-07、S-PLAT-09、S-PLAT-25〕。

## → 行为改变
- 下次选写实风格，先跑合规三问：参考图有没有真人照片？发往哪个平台？逼真 AI 披露开了没有？三问没答完，禁止开板图。
- 下次写写实关键帧，冻结提示词里必须有"光源从句"。写不出光从哪来，就退回场景板标注实景光源（R-BRD-18）。
