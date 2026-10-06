---
id: B3
title: 克隆脸
group: B 一致性
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [casting-and-canon, asset-boards, video-prompting-h3, shot-qc, publish-prep]
drills: [DR-06]
---
# B3 · 克隆脸

> 一句话：**生成器默认"同一类人长同一张脸"。** 要打破这一点，选角时板图上就得长得不一样，提示词里要把差别写出来，验收时要并排看出差别。现在这已经不只是质量问题，平台也在治理"高频 AI 脸"。

## 症状（含人类主创原话，逐字引用档案）

- 三人同框的镜里，三张脸高度雷同，有克隆复制感〔委托方实证·B3〕。
- 同一镜还被加了一道具象的斜光柱，提示词没要求，场景里也没有这个光源〔委托方实证·B3〕。
- 档案没有保留人类主创关于本案的「」逐字原话。学院缺陷分级把"克隆脸（≥2 人同框且脸雷同）"列为阻断缺陷，属于 Q7 维度，见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §3。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 镜型：三人同框，三人都是男性。依据是修正句原文 `three clearly distinct men`。
- 同一镜里有两个缺陷：脸被克隆，外加光柱。两者同源，都是模型在**没被约束的维度上按先验补完**。
- 档案**没有记录**镜号、seed、三人是否各有板图、`references` 挂了几张图。复盘第一步就是查 `references`：三个人是不是各有一张身份图？有没有人挂了两张脸？

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 提示词只写了人数和角色，没写**彼此之间看得见的差异**。模型给没有区分开的同类主体套上同一张"平均脸"。依据：委托方的修正就是明写差异化〔委托方实证·B3〕。
2. 光效写成了可以被具象化的光源或光束，模型就画出了光柱。依据：委托方的判据是"光效只允许写打在脸上的环境光"〔委托方实证·B3〕。

### 方法论原因
3. 把差异化当成提示词层的事，而不是**选角层**的事。如果三个人的板图本身就长得像，提示词怎么写也救不回来，这和 M2"画面级属性由图决定"同理。〔学院推断；**验证方法**：把全部主要角色板图的脸裁成同尺寸并排，交给独立评审会话，看它能不能 1 秒内把脸和名字配上。〕
4. 验收只数"人数对不对"，不比"脸是不是同一张"。多人镜的每张脸都没有裁出来并排比，这和 C2 是同一个结构。

### 外部调研补强的根因
5. **几张脸 = 几个人**：同一个人挂两张脸参考（正面 + 3/4），在运镜镜头里会被生成两个人。对策是写明 `<Picture 3>` 与 `<Picture 4>` 是同一个人。服装参考图用不带脸的"隐形人台"，21 次生成始终只有一个人〔外部调研·S-H3-09〕。
6. 三视图或多视角设定图最容易导致"同框两个同一角色"，也就是双胞胎效果〔外部调研·S-VGEN-11〕。不要把多个角度拼在一张 sheet 上〔外部调研·S-VGEN-18〕。反过来也成立〔学院推断〕：几个角色的身份图如果出自同一张多人拼图，或出自同一个 seed 族，也会互相串脸。**验证方法**：独立板图对比拼图板，各跑 3 seed 做 A/B。
7. 参考人数超过 4 人稳定性下降，实测 8 人参考出了 9 人〔外部调研·S-VGEN-11〕。
8. **提到什么就长什么**：光要写成"暖光从一侧来"，不要写成"落地灯的光"〔外部调研·S-H3-09〕。官方也要求把禁令写成正向状态〔外部调研·S-COMFY-08〕。
9. **平台在治理"高频 AI 脸"**：红果《关于规范AI剧角色创作的公告》要求"一部剧的主要角色应具备清晰的形象区分度"，"避免不同剧集、不同角色使用高度相似的形象"，治理重点包括"高频AI脸复用"〔外部调研·S-PLAT-07〕。所以克隆脸从"质量问题"升级成了"下架风险"（[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第四部分）。这对同剧角色之间、跨剧角色之间**都**适用。

## 修正过程（做了什么、第几轮、结果）

- 委托方的修正（英文为原文）：差异化写 `three clearly distinct men with different faces, hair and builds`，绝对否定写 `no flashlight, no torch beam, no spotlight`〔委托方实证·B3〕。
- 档案没有记录重出用了几个 seed，也没有记录成功比例。
- 按 R1 立场升级后的完整写法：先写正向可见状态，再写绝对否定，并做 A/B 验证。下面的人物外貌只是示例，不是委托方角色：

```
[S1] the tall lean man on the LEFT — <CHR-xxx 锚点句逐字> <Picture 1>
[S2] the short stocky man in the CENTER — <CHR-yyy 锚点句逐字> <Picture 2>
[S3] the grey-bearded older man on the RIGHT — <CHR-zzz 锚点句逐字> <Picture 3>
The three men are clearly distinct, with different faces, hair and builds; no two of them look alike.
Soft ambient light falls on their faces from the left; the background stays evenly dim.
No flashlight, no torch beam, no spotlight.
```

- A/B 验证：A 版只写差异化句和正向光句，B 版在 A 版基础上加否定句，各跑 3 seed。用 `contact_sheet.py --crop` 比较两版的光柱出现率和脸部区分度，结果写回 R1。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] `prompt_lint.py` VP-distinct（error）：画面有 ≥2 个主体却没有差异化句，不得送 H3〔B3〕。
- [自动] `prompt_lint.py` VP-light（warn）：出现 flashlight / spotlight / light beam / god rays 等具象光柱物件，改写为被动环境光句〔B3〕。
- [自动] `prompt_lint.py` VP-position（warn）：≥2 人时没有用 on the LEFT / RIGHT 画面位置称呼〔A5②〕。位置称呼也能帮模型把几个人分开。
- [目视] 每人只挂一张身份图。同一个人不得挂两张脸；确实要挂两张（正脸 + 全身）时，在 `subject_definitions` 写明 `<Picture N> and <Picture M> show the same person`。服装参考用不带脸的图。**禁止**用多视角拼图作身份参考〔S-H3-09、S-VGEN-11、S-VGEN-18〕。
- [目视] 同一镜参考人数 ≤4。超过时先分组出图，再用图生视频〔S-VGEN-11〕。
- [目视] 选角闸门：把全部主要角色的正脸板图裁成同尺寸，并排成一张对照表。任意两个角色至少在 3 项可见特征上不同，可从发型轮廓、脸型、体格、年龄、服色中选。〔学院推断，依据是 S-VGEN-11 的"取 2–3 个稳定静态特征"和 S-PLAT-07 的"清晰区分度"。**验证方法**：独立评审会话只看对照表，能否把每张脸和名字配对。〕
- [目视] 多人镜验收：用 `contact_sheet.py <clip> --crop` 给每张脸各导出一组裁剪并排。任意两张"像同一个人"就不通过〔B3〕。
- [目视] 跨剧去重（平台要求）：与本属主已有剧集的角色比对。学院**暂时没有**人脸相似度脚本。外部调研建议在角色板阶段做人脸相似度去重〔S-PLAT-07〕；脚本到位之前，用并排目视代替，并在发布报告里写明"未做自动去重"。
- [冷观众] 冷观众看完多人镜后，能说出谁是谁。有 ≥2 名冷观众混淆同两个角色，就回流到选角阶段。

## → 行为改变（下次……）

- 下次写任何 ≥2 人的镜，先写差异化句再写动作。差异化句必须点名看得见的差别（脸型、发型、体格、年龄），只写 "different people" 不算。
- 下次写光，只写"光从哪个方向、以什么颜色落在谁身上"。**禁止**写光源物件（手电、聚光灯、光柱、灯），除非这个物件是剧情道具并且有锚点卡。
- 下次选角做板图时，主要角色定稿前必须过"并排对照表"闸门。在板图阶段就雷同的，**禁止**进入关键帧。
- 下次挂参考图前，数一遍每个人挂了几张脸。一人多脸要么声明是同一人，要么拆掉。
- 下次做发布准备时，把"主要角色区分度"列入合规项（`publish-prep`），而不是审美项。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 跨模型成立：Seedance、Luma、H3 社区实测都指向"多视角参考产生双胞胎、同类主体趋同"。
- ★ 跨题材成立，而且在都市、家庭这类"AI 仿真人剧"品类中风险更高。红果对这些品类在"人物形象""表情变化"上提出了更高要求〔外部调研·S-PLAT-07〕。
- ★ 光柱问题也覆盖其他具象光：落地灯、火把光束、丁达尔光。凡是写成"物件 + 光"的，都按本卡处理。
- ☆ "三个男人"的镜型、斜光柱这一具体形态属于本项目。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/casting-and-canon/SKILL.md`](../../20-craft/casting-and-canon/SKILL.md)（选角对照表、区分特征）、[`20-craft/asset-boards/SKILL.md`](../../20-craft/asset-boards/SKILL.md)（单角度单图）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（差异化句、被动光句）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（逐脸裁剪）、[`20-craft/publish-prep/SKILL.md`](../../20-craft/publish-prep/SKILL.md)（角色区分度合规）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/12-color-and-light.md`](../../10-theory/12-color-and-light.md)、[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)。
- 判据清单：[`50-rubrics/checklists/board.md`](../../50-rubrics/checklists/board.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/sound-color-performance.md`](../../50-rubrics/checklists/sound-color-performance.md)、[`50-rubrics/checklists/publish.md`](../../50-rubrics/checklists/publish.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-06.md`](../../60-casebook/drills/DR-06.md)（漂移 / 克隆）。
- 相邻案例：[`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md)、[`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)（R1 立场）、[`60-casebook/cards/B2-crowd-leak.md`](../../60-casebook/cards/B2-crowd-leak.md)、[`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)（画面位置称呼）。
