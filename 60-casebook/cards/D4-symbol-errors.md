---
id: D4
title: 符号/图形错误
group: D 生成技术
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [casting-and-canon, asset-boards, keyframe-freeze, video-prompting-h3, shot-qc]
drills: [DR-12]
---
# D4 · 符号/图形错误

> 一句话：**生成器会把罕见的符号"纠正"成常见的符号。** 只写"应该是什么"挡不住这种回归。要用几何事实写清它是什么，再把所有见过的错法逐条点名禁掉。这张错法清单只增不减，是符号的"病历"。

## 症状（含人类主创原话，逐字引用档案）

- 某个符号（"ф"印记）被画成了"十字"，多出了一根横线〔委托方实证·D4〕。
- 另一镜的质感出成了霓虹 / 激光，应该是火纹〔委托方实证·D4〕。档案原文是"质感写成霓虹/激光"，没有说明是提示词这么写的，还是产出成了这样。两种情况的修法相同。
- 档案没有保留人类主创关于本案的「」逐字原话。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 错误一，形状：目标是"一个环 + 一根竖线"，产出是"一个环 + 一竖一横"，也就是十字〔委托方实证·D4〕。多出来的正好是**最常见的那种补全**：圆加十字（准星、⊕、凯尔特十字）在图像先验里远比 ф 常见〔学院推断〕。
- 错误二，质感：目标是火纹，产出是平滑发光的线（霓虹 / 激光）〔委托方实证·D4〕。"发光的红线"在先验里更接近科幻光效〔学院推断〕。
- 档案没有记录镜号、seed 数和修正后的轮次。
- 〔学院推断〕E4 里"竖线延伸渐隐"可能和本符号同源，档案没有说明。**验证方法**：查 E4 那一镜的锚点 ID 是否为同一个 `SYM-`。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 只描述了目标，没有排除它附近那些高频的错法。生成器向最常见的形状回归，于是多画了一根横线〔委托方实证·D4〕。
2. 质感只写了"什么颜色、会发光"，没写"怎么发光"。火的不规则边缘、跳动的火舌，没有写成可见事件〔委托方实证·D4；对照 M3 "写事件不写形容词"〕。

### 方法论原因
3. 把符号当成装饰，没把它当成资产：没有单独的锚点卡，也没有逐笔画放大验收。印记这类符号承担剧情识别功能，画错一次就是全季的连续性错误。
4. 错误变体没有累积起来。每见到一种错法，都应该当场追加到禁用清单里，否则下一次重写提示词时又会丢掉〔委托方实证·D4 判据："列出所有曾见过的错误变体"〕。

### 外部调研：冲突证据与新增根因
5. **数量词不可靠**：可灵官方指南说，视频模型对数字不敏感〔外部调研·F-VGEN-29〕。`exactly one` 有帮助，但必须配合几何锚定和验收。终点写成"碰到某物后停住"有效，写厘米数无效〔外部调研·F-ZEN-11〕；单位距离和分数会被忽略，要拿画面里的东西当尺〔外部调研·S-H3-09〕。所以竖线写成 `from the top edge of the ring to the bottom edge`，不要写长度。
6. **点名错法可能把它招进来**：官方原则是 "Write bans as positives"〔外部调研·S-COMFY-08〕；社区实测"提到什么就长什么"〔外部调研·S-H3-09〕。写 `no cross sign`，理论上有把十字登记成内容的风险。委托方的对抗约束写法实测修好了问题〔委托方实证·D4〕。学院立场按 R1：**先写正向几何句，再只为"已见过的错法"追加否定，并做 A/B**（[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1）。
7. **符号近似于文字**：写了"无可读文字"，表面上仍会长出类汉字伪字形，否定式约束对字形类元素不可靠，必须原尺寸裁切目检〔外部调研·S-COMFY-21〕。
8. **锁面必须以正向形式逐字出现**：跨镜不变的事实要上锁，锁面在图片提示词、关键帧提示词、视频提示词里都要逐字出现；写在 no/not/without 之后的匹配不算〔外部调研·S-ZEN-15、F-ZEN-23〕。
9. 〔学院推断〕Qwen 编辑类任务里，身份来自参考图时，指向参考图比用文字描述五官更能保持相似度〔外部调研·F-COMFY-09〕。符号很可能也是这样：把通过验收的符号裁切图挂进 `references`，可能比加长文字描述更稳。**验证方法**：同一镜分别做"仅文字"和"文字 + 符号裁切参考"，各跑 3 seed，数笔画正确率。

## 修正过程（做了什么、第几轮、结果）

- 委托方采用**对抗约束写法**：不只写"应该是什么"，还穷举"不许是什么"〔委托方实证·D4〕。
  - 形状：`exactly one red ring crossed by exactly one vertical bar, top to bottom; no horizontal line, no cross sign, no plus sign, no second bar`
  - 质感：`fire-textured, not smooth neon, not a laser line`
- 档案没有记录修正用了几轮、几个 seed。
- 学院落地为契约：符号作为 `SYM-` 资产写锚点卡，`禁用` 列出所有见过的错法；`prompt_lint.py` 的 `VP-symbol` 检查这些错法是否逐条写进了提示词（[`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §3）。示例写法（〔学院推断〕，正向句待 A/B）：

```markdown
## ANCHOR: SYM-PHI-MARK
- 类型: 符号
- 锚点句 EN: `a mark of exactly one thin red ring crossed by exactly one vertical bar running from the top edge of the ring to its bottom edge; the inside of the ring on both sides of the bar is empty; the strokes are made of flickering flame with ragged, uneven edges`
- 必现: 环×1；竖线×1，从环的上缘贯穿到下缘；环内竖线两侧为空；火纹质感（边缘不规则、火舌）
- 禁用: no horizontal line; no cross sign; no plus sign; no second bar; not smooth neon; not a laser line
- 方位属性: 竖线与画面竖直方向平行（放大核验）
- 来源依据: 原著对印记的描写（按原著章节填写）
```

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 每个剧情关键的符号或图形都有 `## ANCHOR: SYM-…` 锚点卡，`类型: 符号`，`禁用` 非空〔D4〕。
- [自动] `prompt_lint.py --anchors anchors.md` 不报 `VP-symbol`（符号锚点的禁用项要逐条写进提示词），也不报 `VP-anchor`（锚点句逐字出现）〔D4、P1〕。
- [目视] 板图和关键帧阶段：裁切放大符号区域，按笔画计数，环 = 1、竖线 = 1、横线 = 0；禁用清单里的每一项都在验收记录里打勾。静帧用 ffmpeg `crop` 加最近邻放大〔D4、C2〕。
- [目视] 视频阶段：`contact_sheet.py <clip> --crop sym=X:Y:W:H` 在 FIRST、MID、TAIL 三格都重新计数。视频是重新采样，关键帧对了，不代表全程都对〔D4、B4〕。
- [目视] 质感按可见事件判：边缘是不是不规则、有没有火舌跳动、亮度是否均匀。平滑匀亮的线一律按"霓虹 / 激光"判不通过〔D4〕。
- [目视] 出现新的错误变体时，当天追加到锚点卡 `禁用` 和本卡现场，再重出〔D4〕。
- [冷观众] 冷观众能把不同镜里的印记认作"同一个符号"〔D4〕。

## → 行为改变（下次……）

- 下次遇到剧情关键的符号、纹章、图腾、文字样图形，先建 `SYM-` 锚点卡，再写任何提示词。
- 下次描述符号，用几何事实写：几个、什么形状、从哪里到哪里、哪里是空的。**禁止**只写符号的名字或字母（"a ф symbol"）。
- 下次描述发光、能量、火焰这类质感，写成可见事件（火舌、不规则边缘、明暗跳动），并点名最接近的错法（`not smooth neon, not a laser line`）。
- 下次验收符号，裁切放大后数笔画。**禁止**在整帧缩略图上"看着像"就放行。
- 下次某个符号连续 3 个 seed 都错，判为结构性缺陷（判法见 [`60-casebook/cards/D3-dialogue-capacity.md`](D3-dialogue-capacity.md)）。考虑在关键帧阶段本地修正符号，再作为起始帧锁定（D2 原则：要求精确几何的东西，少交给采样）。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 任何罕见符号都会向高频形状回归：自创文字、家徽、阵法图、法印、品牌 logo。对抗约束清单加放大计数，与模型无关。
- ★ 质感对抗写法（"是 X，不是最接近的 Y"）可以迁移到材质、光效、天气等所有容易被默认先验覆盖的属性。
- ☆ ф 印记和火纹属于本项目。错法清单（十字、加号、第二根线、霓虹、激光）只对这个符号有效，换符号要重新累积。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/casting-and-canon/SKILL.md`](../../20-craft/casting-and-canon/SKILL.md)（SYM 锚点卡）、[`20-craft/asset-boards/SKILL.md`](../../20-craft/asset-boards/SKILL.md)（多 seed + 放大）、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)（符号在起始帧锁定）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（对抗约束写法）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（逐格计数）。
- 理论：[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)。
- 判据清单：[`50-rubrics/checklists/board.md`](../../50-rubrics/checklists/board.md)、[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-12.md`](../../60-casebook/drills/DR-12.md)（符号）。
- 相邻案例：[`60-casebook/cards/C1-banned-items-violated.md`](C1-banned-items-violated.md)（R1 两句式）、[`60-casebook/cards/C2-lenient-acceptance.md`](C2-lenient-acceptance.md)（放大证据）、[`60-casebook/cards/E4-prompt-output-mismatch.md`](E4-prompt-output-mismatch.md)、[`60-casebook/cards/D2-solid-black-fails.md`](D2-solid-black-fails.md)、[`60-casebook/positive-assets.md`](../positive-assets.md)（P1、M3、M8）。
