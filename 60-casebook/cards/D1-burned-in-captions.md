---
id: D1
title: 烧录字幕
group: D 生成技术
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [video-prompting-h3, shot-qc, edit-and-assemble]
drills: [DR-10]
---
# D1 · 烧录字幕

> 一句话：**生成器会把"有人在说话"补成"画面上有字"。** 禁令句只能压低概率，保证不了结果。真正能保证"成片里没有生成器写的字"的只有两件事：所有画面文字由剪辑程序叠加；每条视频都逐帧抽检。

## 症状（含人类主创原话，逐字引用档案）

- 某段视频里，生成器自己烧进了字幕〔委托方实证·D1〕。
- 档案没有保留人类主创关于本案的「」逐字原话。
- 学院缺陷分级：画面里出现生成器自行添加的文字、水印或字幕，属于阻断缺陷（Q5），见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §3。
- 同类公开报告：H3 讨论区 #106 有用户报告"无故出字幕"〔外部调研·S-H3-13〕；Veo 3 含对白的片段经常出现乱码烧录字幕，一位广告从业者称可多达 40% 不可用〔外部调研·S-VGEN-04〕。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 档案**没有记录**镜号、字幕内容、seed，也没有记录字幕出现在哪个时段。这里只写档案里有的：修正动作，以及之后固化下来的两条规则〔委托方实证·D1〕。
- 规则一（提示词侧）：每镜提示词末尾固定写 `No captions, subtitles, or dialogue text overlays appear at any moment.`，这句后来进了禁令包〔委托方实证·M8〕。
- 规则二（验收侧）：视频验收固定一项"抽帧核验无烧录文字"〔委托方实证·P8〕。
- 结果：三集成片在工程层面"无烧录字幕"〔委托方实证·T-4〕。**注意**：这是"禁令句 + 抽帧拦截 + 重出"三者合起来的结果。档案里没有统计"加了禁令句以后，生成阶段还出不出字幕"，所以不能把这个结果算成禁令句单独的功劳。
- 管线背景：H3 的音频和画面在同一次生成里出来，对白写在 `<d>` 里〔委托方实证·T-2〕。所以"有对白"和"出字幕"就在同一次采样里发生。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 提示词里没有任何约束画面文字的句子。生成器的默认分布里本来就包含"加字幕"〔委托方实证·D1〕。
2. 画面文字归谁负责没有约定。字幕、字卡、标识该由生成器出还是由剪辑出，没有分工；修正后才约定为"画面文字全部由后期叠层负责"〔委托方实证·D1〕。

### 方法论原因
3. 把生成器当成"按描述渲染"的工具，没把它当成"按训练分布补全"的采样器。训练数据里有大量自带字幕的视频，模型学到了"加字幕更像人类视频"〔外部调研·S-VGEN-04，学者解释〕。所以字幕是默认会出现的东西，不是偶发故障。
4. 验收只看"该有的对不对"，没把"多出来的东西"列成固定检查项。这和 B4 背景多出元素是同一种结构。

### 外部调研补强的根因
5. **竖屏是高发区**：Seedance 官方 FAQ 说字幕无法 100% 避免，横屏出字幕的概率显著低于竖屏〔外部调研·S-VGEN-11、F-VGEN-04〕。9:16 短剧天然处在高风险一侧。
6. **参考图带字，视频就带字**：可灵 3.0 会识别上传图里的招牌、字幕、logo，并在视频中保持〔外部调研·S-VGEN-08、F-VGEN-10〕；Seedance 要求先去掉参考图里不必要的文字〔外部调研·S-VGEN-11〕。〔学院推断〕板图上的标注字（三视图标签、inset 说明字、编号）送进 `references` 后，可能被带进视频。**验证方法**：同一镜分别挂"带标注字"和"已去字"的板图，各跑 3 seed，统计 `burnin_text_scan.py` 的命中次数。
7. **台词写法会触发字幕**：Seedance 2.5 FAQ 说，在台词后面重复台词里的词，或者给台词中的个别词附加语气、动作说明，都会触发字幕〔外部调研·S-VGEN-12、F-VGEN-05〕。〔学院推断〕H3 的 `<d>` 里混进舞台提示同样有风险，`dialogue_capacity.py` 遇到这种情况会报 `D3-d-stage`。**验证方法**：同一镜分别写"`<d>` 只放台词"和"`<d>` 内带括号提示"，各跑 3 seed 对比。
8. **写法冲突**：ComfyUI 官方 H3 指南主张 "Write bans as positives"，认为写 "no subtitles and no on-screen text" 可能把文字登记成内容〔外部调研·S-COMFY-08、F-H3-08〕。反方证据是委托方实证有效，另有一份小样本实测中 `No dialogue` 8/8 有效〔外部调研·S-ZEN-17〕。学院按 R1 第 4 条裁决：**保留禁令句作兜底**，再追加正向状态句，并且永远以抽帧核验为准（[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1）。

## 修正过程（做了什么、第几轮、结果）

- 委托方的做法：每镜末尾加禁令句，重出并替换；画面文字全部交给后期叠层〔委托方实证·D1〕。档案没有记录重出用了几个 seed。
- 学院补充（〔学院推断〕，按 R1 做 A/B 后再升格为规则）：
  - 在禁令句之前加一句正向状态句，写清画面下部实际是什么，例如 `The lower third of the frame shows only the cracked stone floor and the hem of her robe.`。**验证**：A 版只写禁令句，B 版写禁令句加正向句，各 3 seed，比较 `burnin_text_scan.py` 的 error 与 visual 计数。
  - 送进 `first_frame` 或 `references` 的图，先去掉所有文字。
  - `<d>` 里只放要念出来的台词；语气写在说话人引导句里，例如 `[S1] says through clenched teeth: <d>[Chinese] …</d>`。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] `prompt_lint.py` 不报 `VP-ban`：h3 块的最后一个非空行，逐字等于 `No captions, subtitles, or dialogue text overlays appear at any moment.`〔D1、M8〕。
- [自动] `prompt_lint.py` 不报 `VP-generator-unsafe` 的"字幕/叠字"类：提示词里不得要求生成器出 subtitles、captions、on-screen text、lower thirds〔D1〕。
- [自动]+[目视] 每条生成镜都跑 `burnin_text_scan.py <clip> --out-dir qc/<SHOT>`。
  - 报 `D1-burnin-text`（error）：该镜不通过。
  - 报任何 visual（`D1-heuristic-bottom`、`D1-heuristic-persistent`、`D1-ocr-lowconf`）：打开 `<clip>.burnin-strip.jpg` 逐格看，结论写进 `qc/<SHOT>.md`。
  - 报 `D1-ocr-degraded`：验收记录必须写明"OCR 未启用，启发式 + 目视"〔D1、D5〕。
- [目视] `contact_sheet.py` 接触表全部格子都没有文字，包括 TAIL 格〔P8〕。
- [自动]+[目视] 成片跑 `burnin_text_scan.py final/epNN.mp4 --mode final`。OCR 识别出的文字逐条对照剪辑单的 `字幕` 和 `画面文字` 两列；剪辑单里没有的文字，就是生成器烧录的〔D1、P7〕。
- [目视] 送入 `first_frame` 和 `references` 的板图、关键帧上没有任何文字，包括标签、编号和 inset 说明字〔S-VGEN-08、S-VGEN-11；学院推断〕。
- [冷观众] 冷观众的断点记录里没有"两层字幕""字幕重影""乱码字"〔D1〕。

## → 行为改变（下次……）

- 下次写 h3 块，先写最后一行禁令句，再写正文。`prompt_lint.py` 报 `VP-ban` 的镜，不得进入 prepare。
- 下次需要画面上出现文字（字幕、字卡、可读招牌、AIGC 标识），一律写进剪辑单的 `字幕` 或 `画面文字` 列。**禁止**写进提示词。
- 下次挂参考图之前，先看图上有没有字。有字就先在本地裁掉或涂掉，再送进去。
- 下次验收"含对白 + 竖屏"的镜，按高风险处理：先跑 `burnin_text_scan.py`，再看内容。
- 下次发现烧录字幕，先换 seed 重出，这是随机缺陷的处理。如果 3 个 seed 都出字幕，就当结构性缺陷处理：依次查参考图上的文字、`<d>` 里的舞台提示、对白后面的重复词，然后改设计（判法见 [`60-casebook/cards/D3-dialogue-capacity.md`](D3-dialogue-capacity.md)）。
- **禁止**通过裁切画面去掉底部字幕。裁切会破坏 9:16，`loudness_verify.py` 的 `T3-aspect` 也会拦下；还会破坏起始帧钉死的构图。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ H3、Veo 3、Seedance 都有这个问题〔外部调研·S-H3-13、S-VGEN-04、S-VGEN-11〕。"文字归剪辑、视频必抽检"与模型无关。
- ★ 换到 cfg>1 且负向生效的管线时，可以**额外**写负向"字幕"（Wan2.2 官方默认负向词里就有"字幕"〔外部调研·S-VGEN-14〕），但不能替代抽检。
- ★ 同一套方法也拦"伪文字"：招牌、书页、屏幕上的类汉字乱码，同样走 OCR 加目视〔外部调研·S-COMFY-21〕。
- ☆ 档案没有记录具体字样，无法给出本项目特有的高发字样清单。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（禁令包、`<d>` 写法）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（烧录扫描、接触表）、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)（字幕与画面文字叠层）。
- 理论：[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)。
- 判据清单：[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/burnin_text_scan.py`](../../50-rubrics/scripts/burnin_text_scan.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-10.md`](../../60-casebook/drills/DR-10.md)（烧录字幕 / 纯黑卡）。
- 相邻案例：[`60-casebook/cards/D2-solid-black-fails.md`](D2-solid-black-fails.md)（不交给生成器的事）、[`60-casebook/cards/C1-banned-items-violated.md`](C1-banned-items-violated.md)（R1 两句式）、[`60-casebook/cards/D5-qc-tools-lie.md`](D5-qc-tools-lie.md)（OCR 降级与双通道）、[`60-casebook/cards/B4-duplicate-artifacts.md`](B4-duplicate-artifacts.md)（"多出来的东西"验收）、[`60-casebook/positive-assets.md`](../positive-assets.md)（P8、M8）。
