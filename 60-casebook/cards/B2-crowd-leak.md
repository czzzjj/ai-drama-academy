---
id: B2
title: 人群穿帮
group: B 一致性
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [video-prompting-h3, storyboard-long-take, shot-qc, sound-design]
drills: [DR-07]
---
# B2 · 人群穿帮

> 一句话：**你写进提示词却没设计清楚的东西，生成器都会替你设计。** 人群是画面里最大的一块空白画布：每个人的脸、衣服、手里拿的东西，模型都要现编，而且不受任何锚点卡约束。

## 症状（含人类主创原话，逐字引用档案）

- 某镜提示词只写了"远处人群低语"，产出里被模型扩写成一群"持发光平板者"，人群还在镜内扩散、变形〔委托方实证·B2〕。
- 这是两层错误叠在一起：
  - **内容错**：奇幻/古装世界里冒出了发光平板，属于时代穿帮；
  - **形态错**：人群的数量和形体在镜内不稳定。
- 档案没有保留人类主创关于本案的「」逐字原话。学院术语表把本案归入"穿帮"族（B1–B4），见 [`00-orientation/glossary.md`](../../00-orientation/glossary.md) B 表。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 原写法："远处人群低语"。这是一个**以声音为主**的描述。除了"远处"，没有任何视觉约束：没写虚化、没写数量、没写轮廓，也没说明手里拿什么。
- 产出：人群拿着提示词里不存在的具体道具（发光平板），并在镜内扩散变形。
- 档案**没有记录**镜号、seed，也没记录这句写在哪一段（`summary` / `detailed_description` / `overall_soundscape`）。复盘时先查这一点，因为写在哪一段决定了下面根因 8 是否成立。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. **人群是"存在但没定义"的主体**。模型只能为每个人现编脸、衣服和手持物，现编的结果不受锚点卡约束〔委托方实证·B2〕。
2. **人群被给了可以扩写的特征**（"低语"这个动作）。档案判据原文就是：给了就会被扩写〔委托方实证·B2〕。

### 方法论原因
3. 把人群当成"氛围布景"，没当成"高风险资产"：没有锚点卡、没有禁用项、没有验收条目。风险最高的元素，管得反而最少。
4. 分镜阶段没问过"这一镜**必须**看见人群吗"。能用声音或画外交代的，就不该让人群入画。病灶在预制作阶段，不在提示词（见 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3）。

### 外部调研补强的根因
5. **提到什么就长什么**：写进共用段的物件会在每一颗镜头里长出来，所以共用段只放每颗都成立的元素〔外部调研·S-H3-09〕。连写出"不要的元素"都可能被当成内容登记进去〔外部调研·S-COMFY-08〕。
6. **人一多就不稳**：参考人数超过 4 人稳定性下降，实测 8 人参考出了 9 人〔外部调研·S-VGEN-11〕。Wan2.2 官方默认负向词里就有"背景人很多""杂乱的背景"〔外部调研·S-VGEN-14〕。可见人群失控是跨模型的通病，不是 H3 特有的。
7. 多人场的成熟写法：同框只拍一两颗中景交代关系，台词全部用单人正反打，单人镜的前景不放路人〔外部调研·S-H3-09〕。
8. 〔学院推断〕**声音描述可能被画成画面**。H3 的音频和画面在同一个 pass 里生成〔委托方实证·T-2〕。"人群低语"这类声音，如果画面段没写"在画外"或"虚化"，模型可能给声源补一个画面。**验证方法**：同一镜做两版，各跑 3 seed，数可辨人形出现了几次。A 版声音段写 `distant crowd murmur`，同时画面段写明人群在画外；B 版只在声音段写。

## 修正过程（做了什么、第几轮、结果）

- 委托方的修正：人群镜尽量少；人群写成"大虚化、无独立可辨脸的暗形块"〔委托方实证·B2〕。
- 学院固定的英文写法与 `prompt_lint.py` VP-crowd 给出的修法一致：`heavily blurred, out-of-focus dark silhouettes with no distinct faces`，不给人群任何独立特征。
- 按 R1 立场写成完整两句：第一句写正向可见状态，第二句写绝对否定，否定只针对已被证实会加出来的东西（本案是发光平板）：

```
Far behind them, the crowd is only heavily blurred, out-of-focus dark silhouettes with no distinct faces, standing still at the edge of the light.
The silhouettes hold nothing in their hands; no screens, no glowing devices.
```

- 第二句属于"否定句是否会招来被否定物"的待验证范围。按 R1 做 A/B：A 版只写第一句，B 版两句都写，各跑 3 seed，用 `contact_sheet.py` 并排数手持物和发光物。
- 档案没有记录修正后重出了几轮、用了哪些 seed。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] `prompt_lint.py` VP-crowd：出现人群词（crowd / onlookers / spectators / villagers / bystanders …）但全镜没有虚化描述。脚本报 warn，学院口径是**不修不得 run**〔B2〕。
- [目视] 分镜阶段，每个让人群入画的镜，都要在 `内容` 里写出"为什么必须看见人群"。写不出来，就改成画外声音或单人反应镜，让人群出画。
- [目视] 群声只出现在 `overall_soundscape` 时，画面段必须写明人群在画外或是虚化暗形。**禁止**只写声音、让模型自己决定画不画（根因 8，待 A/B）。
- [目视] 场景锚点卡的 `禁用` 列入本世界观的时代穿帮物（屏幕、平板、手机、电灯等，按设定定），并写进所有含人群的镜的提示词〔B2；format-contracts §3〕。
- [目视] `contact_sheet.py <clip>` 接触表的 FIRST / MID / TAIL 三格中，人群剪影数量不增加、没有可辨认的脸、没有手持物、没有自发光物体。任何一项不满足就不通过〔B2、P8〕。
- [自动] `psnr_scan.py <clip> --mode clip` 没有 P8-jump；如果有，就抽帧确认是不是人群"扩散变形"的那一段（双通道，D5）。
- [冷观众] 冷观众的断点记录里，没有"后面那些人是谁 / 他们拿的是什么"这类注意力被背景吸走的条目。

## → 行为改变（下次……）

- 下次写分镜写到人群时，先问"删掉人群，这场戏还成立吗"。成立就删：要氛围交给声音，要反应用单人反应镜。
- 下次人群必须入画时，提示词里人群只允许三个属性：**距离**（far / in the background）、**虚化**（heavily blurred, out-of-focus）、**无脸**（no distinct faces）。**禁止**给人群写动作、服装、道具、表情。
- 下次在声音段写群声时，同时在画面段写清人群在画外或虚化。
- 下次验收含人群的镜，单独数一遍背景人形和手持物，写进 `qc/<SHOT>.md`，不要和主体验收混在一起。
- 下次换世界观时，先重写场景锚点卡的时代穿帮禁用清单，再写提示词。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 跨模型成立：Seedance 的参考人数上限、Wan 的默认负向词都指向同一个问题。"不设计的东西由模型设计"对一切生成器成立。
- ★ 换成现代都市题材后，"发光平板"不再算穿帮，但人群被凭空加上不受控的特征这一点照样成立，禁用清单要按世界观重写。
- ★ 同一机制还覆盖路人、士兵方阵、观众席、宴会宾客：只要是"多个没有锚点卡的人"，都按本卡处理。
- ☆ "发光平板"这个具体的扩写物属于本项目。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（人群写法、R1 两句式）、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（人群入画须给理由）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（接触表数人形）、[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)（群声改走声音层）。
- 理论：[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)。
- 判据清单：[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)、[`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)。
- 找错题：[`60-casebook/drills/DR-07.md`](../../60-casebook/drills/DR-07.md)（人群 / 伪影）。
- 相邻案例：[`60-casebook/cards/B4-duplicate-artifacts.md`](../../60-casebook/cards/B4-duplicate-artifacts.md)（背景元素凭空增殖）、[`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)（R1：正向可见状态 + 绝对否定）、[`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)（多人同框）。
