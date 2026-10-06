---
id: E4
title: 提示词与产出不对齐
group: E 流程工程
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [video-prompting-h3, keyframe-freeze, shot-qc, production-director]
drills: [DR-15]
---
# E4 · 提示词与产出不对齐

> 一句话：**提示词不是"意图"，是"记录"。** 一条产出一旦被验收、被拿去当参考，提示词就必须改写成产出里的事实。否则下一次生成时，图说一套、字说一套，模型会两头都执行，结果乱成一团。

## 症状（含人类主创原话，逐字引用档案）

- 某镜提示词写的是"短距离"，实际产出却是竖线一路延伸后渐隐，也就是长距离。这条产出被留作参考图后，后续重出的结果和参考图互相矛盾〔委托方实证·E4〕。
- 档案没有保留人类主创关于本案的「」逐字原话。档案把本案标为 ★通用（E 组里唯一的一张通用卡），所以本卡 scope 取"通用"。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 这里有两次失配：第一次是产出偏离提示词（短 → 长），第二次是偏离的产出进了参考链〔委托方实证·E4、P5〕。
- 后果是在后续重出时出现的：参考图里是长线，提示词里是"短距离"。模型会执行你写下的**所有**指令，指令互相打架，它就自己编〔委托方实证·A5④〕。
- 档案没有记录镜号、是哪一轮修订、后来以哪个版本为准。〔学院推断〕这条"竖线"可能就是 D4 符号的竖线，档案没有说明。

## 根因（分条；区分"直接原因"与"方法论原因"）

1. **直接原因**："短距离"是没有锚点的相对词，生成器不认。单位距离和分数会被忽略，要拿画面里的东西当尺〔外部调研·S-H3-09〕；终点写成"碰到某物后停住"4/4 有效，写厘米数无效〔外部调研·F-ZEN-11〕。
2. **直接原因**：验收时拿产出和"好不好看"比，没有拿产出和提示词逐句比，偏离就这样被接受了。
3. **方法论原因**：每轮修订只改了一边，要么只改提示词，要么只换产出，没有"互相回写"这一步。提示词也就从"对产出的记录"退化成了"当初的愿望"。
4. **方法论原因**：参考图是比文字更强的事实（P4：文字救不了构图）。把一张和文字矛盾的图放进参考链，等于在下游植入了一条冲突指令。
5. **外部佐证**：每次重写或压缩提示词，都要填"改写前后回归表"，核对台词、起止、时长、资产有没有丢；指令优先级是故事事实与对白 > 镜头覆盖与起止时长 > 资产身份与连续性 > 视觉方向 > 模型条件 > 装饰偏好〔外部调研·S-ZEN-23、F-ZEN-25〕。连续性锁面要在每条图片、关键帧、视频提示词里逐字出现〔外部调研·S-ZEN-15、F-ZEN-23〕。〔学院推断〕Qwen 编辑里，身份来自参考图时，再用文字去描述它会让模型重新生成并降低相似度〔外部调研·F-COMFY-09〕；图文不一致时，文字会把结果往自己那边拉。**验证方法**：同一参考图配"一致"和"矛盾"两版文字，各跑 3 seed，比较与参考图的差异。

## 修正过程（做了什么、第几轮、结果）

- 委托方：每轮修订之后，提示词文本和已验收的产出**互相回写对齐**；参考图和提示词必须陈述同一个事实〔委托方实证·E4〕。
- 学院固化为二选一，见 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §7：
  - **接受产出**（人类或验收判定新版更好）→ 把提示词改写成产出的事实，例如 `the vertical line extends upward past <画面中的参照物> and fades out`，然后才允许它进 `references`。
  - **拒绝产出** → 这条产出不得进入任何参考链，按原提示词重出；距离改写成有锚点的终点（`stops where it touches <物体>`）。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [目视] 每条 `qc/<SHOT>.md` 都有一行"提示词 ↔ 产出差异"：逐句列出不一致项，结论只能是"已回写"或"已拒绝"〔E4〕。
- [目视] 任何进入 `references` 或 `first_frame` 的图，它的验收记录里都有"已回写"标记，或者"无差异"标记〔E4、P5〕。
- [自动] 提示词改写之后，`prompt_lint.py --anchors … --storyboard …` 不报 `VP-anchor` 和 `VP-sync`，确认锚点句和时长没在改写中丢掉〔E4、P1、P7〕。
- [自动] 对白类改写之后，`transcript_reconcile.py` 不报 `TR-script-prompt`〔E4、P7〕。
- [目视] 提示词里没有不带锚点的距离、大小、时长形容词（"短距离""稍远""很快"），一律改成画面里的参照物〔E4；S-H3-09〕。

## → 行为改变（下次……）

- 下次验收，先逐句对照提示词和产出，再判断好坏。
- 下次接受一条和提示词不一致的产出，同一步里就改写提示词；改完之前，**禁止**把它挂进参考链。
- 下次写距离、长度、范围，写成"到画面里的哪个东西为止"。**禁止**写"短 / 长 / 约 N 厘米"。
- 下次改写提示词，填改写前后回归表：台词、起止、时长、锚点句、禁令包，逐项打勾。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 只要用产出当下一步的参考（链式参考、尾帧续接、关键帧到视频），"提示词 = 产出的记录"就成立，与模型无关。
- ★ 同样适用于锚点卡：板图定稿后，锚点句要回写成定稿板图的事实（C1、P2）。
- ☆ "竖线"这个具体元素属于本项目。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（改写回归表）、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)（冻结提示词 = 关键帧的记录）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（差异行）、[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（参考链准入）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)。
- 判据清单：[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/transcript_reconcile.py`](../../50-rubrics/scripts/transcript_reconcile.py)。
- 找错题：[`60-casebook/drills/DR-15.md`](../../60-casebook/drills/DR-15.md)（环境 / 提示词≠产出）。
- 相邻案例：[`60-casebook/cards/D4-symbol-errors.md`](D4-symbol-errors.md)、[`60-casebook/cards/A5-spatial-chaos.md`](A5-spatial-chaos.md)（指令打架）、[`60-casebook/cards/B4-duplicate-artifacts.md`](B4-duplicate-artifacts.md)（换版后的回写）、[`60-casebook/positive-assets.md`](../positive-assets.md)（P3、P4、P5、P7）。
