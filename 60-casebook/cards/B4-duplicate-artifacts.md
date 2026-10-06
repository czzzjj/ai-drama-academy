---
id: B4
title: 重复伪影
group: B 一致性
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [shot-qc, keyframe-freeze, video-prompting-h3]
drills: [DR-07]
---
# B4 · 重复伪影

> 一句话：**视频不是"让关键帧动起来"，而是从关键帧出发重新采样。** 起点里有一个东西，过程中可能就长出第二个。验收必须把关键帧当账本，逐段核对背景元素。

## 症状（含人类主创原话，逐字引用档案）

- 某段视频的背景里持续出现"第二骨架"，关键帧里没有这个元素〔委托方实证·B4〕。
- "持续出现"意味着它不是一两帧的闪烁，而是贯穿整段。只看几帧的抽查不一定会漏，但如果不拿关键帧来对，就不会意识到"多了一个"。
- 档案没有保留人类主创关于本案的「」逐字原话。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 起点是干净的：关键帧（`REF-SHOTnnn-START`）里没有第二骨架〔委托方实证·B4〕。所以伪影是视频生成阶段新增的，不是关键帧带进来的，病灶在制作阶段。
- 修正用了 4 个 seed，产出 4 版，抽帧对比后选出最好的一版，换版覆盖〔委托方实证·B4〕。这说明本案是**随机缺陷**，换 seed 就能解决；D3 则相反，是换 seed 也没用的结构性缺陷。
- 档案**没有记录**镜号、具体 seed 值，以及"第一具骨架"是否本来就在关键帧里。"第二"暗示画面里原本有一具骨架，复盘时以关键帧为准核实。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 生成器在背景里复制或新增了显著元素，关键帧没法保证全程不变〔委托方实证·B4〕。
2. 验收没有"以关键帧为基准核对背景元素"这一步，只看了主体，没数背景。B4 的判据就是从这里来的〔委托方实证·B4〕。

### 方法论原因
3. 把关键帧当成"画面已经定了"的保证，可它只定了起点。视频的中段和尾段都要单独验收，对应 P8 的"逐段抽帧、尾部无崩解"〔委托方实证·P8〕。
4. 复杂背景或多人物的镜头只抽了一个 seed 就直接用，没有提前规划多 seed，出了问题才去补抽。
5. 没有在看视频**之前**写下"应该有什么"。不先列清单，就只能凭印象判断"有没有多出东西"，而人的注意力会被主体吸走。

### 外部调研补强的根因
6. 显著元素被复制是跨模型的通病。Wan2.2 官方默认负向词里就有"三条腿""多余的手指""背景人很多""杂乱的背景"〔外部调研·S-VGEN-14〕。在 cfg=1 的管线里负向词用不上，但这份清单可以原样转成 QC 检测项。
7. 步数不够时，会出现随运动游动的三角网格伪影；锁子甲、花纹这类高频细节，步数加到约 50 步仍在改善〔外部调研·S-COMFY-09、S-H3-04〕。Sage Attention 的 INT8 量化可能导致片尾形变和乱码文字〔外部调研·S-H3-04〕。
8. H3 常在片尾前 1.2–1.7s 崩成噪声色块。生成时要留 1.3–1.5s 尾部余量，剪辑时裁掉〔外部调研·S-H3-09〕。
9. **提到什么就长什么**：写在共用段里的物件，会在每一颗镜头里长出来〔外部调研·S-H3-09〕。〔学院推断〕如果"骨架"写在共用段或多处描述里，被复制的概率会上升。**验证方法**：同一镜做两版，各跑 3 seed，数骨架的数量。A 版只在本镜 `detailed_description` 里提一次，并写明 `exactly one skeleton lies by the far wall`；B 版用原写法。
10. 要复现结果，必须同时记下 seed 和 batch_index：批内第 k 张的噪声，不等于单独用 seed+k 生成的噪声〔外部调研·S-COMFY-05〕。不记 batch_index，选中的"好版"就无法复现。

## 修正过程（做了什么、第几轮、结果）

- 委托方：多 seed 抽卡，4 个 seed 产出 4 版，抽帧对比选优，换版覆盖〔委托方实证·B4〕。
- 换版之后，学院补充的连带动作：
  - 被换掉的版本如果已经被下游引用（作为下一镜的参考帧，或作为剪辑单来源），要同步替换所有引用，并跑一遍 `asset_exists.py`〔E2〕；
  - 选中的版本如果和提示词描述不一致，把提示词回写成产出的事实〔E4〕。
- 重试上限：换 seed 最多 2–3 次，仍然复现就视为系统性问题，改提示词、步数或关键帧〔外部调研·S-PIPE-01〕。委托方"一次并行 4 seed"属于预先规划的抽卡，不算串行重试。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [目视] 看视频之前，先在 `qc/<SHOT>.md` 写"背景元素清单"：关键帧里每个显著元素及其数量，例如"骨架×1、石柱×2、火把×0"〔B4〕。
- [自动]+[目视] 运行 `contact_sheet.py <clip> --keyframe <REF-SHOTnnn-START.png>`，第 1 格是关键帧，脚本会报 visual `B4-keyframe`。然后逐格（FIRST / MID / TAIL）按清单计数，任何元素数量有变化就不通过〔B4、P8〕。
- [自动] `psnr_scan.py <clip> --mode clip` 报出 `P8-jump`（镜内跳变）时，要抽帧确认是不是伪影出现或崩解的位置。单通道不下结论〔P8、D5〕。
- [目视] 尾部窗口：接触表的 TAIL 格（最后 0.5s）没有崩解；生成时长里已经包含 1.3–1.5s 尾部余量〔S-H3-09〕。
- [目视] 多人物或复杂背景的镜，提前规划 ≥3 个 seed（委托方实例是 4 个），并在生产清单里标注"高风险背景"〔B4〕。
- [目视] 生成日志记下 seed、batch_index、steps、是否用了 turbo、注意力后端。缺任何一项，这一版都不能当定稿〔S-COMFY-05、S-H3-04〕。
- [冷观众] 冷观众的断点记录里，没有"背景里多出来的东西"这一类。

## → 行为改变（下次……）

- 下次验收任何视频镜，先打开关键帧写背景元素清单，再看视频。**禁止**"看了一遍觉得没问题"就放行。
- 下次遇到伪影，先判断随机还是结构：并行 3–4 个 seed 里至少有一版干净，就是随机缺陷，选优即可；全部复现，就是结构性缺陷，回去查提示词共用段、步数、turbo、关键帧里有没有诱发元素。
- 下次换版覆盖后，立刻在全仓搜索旧版文件名，把引用一并替换。
- **禁止**用 4-step turbo 生成终版，turbo 只用于预览抽卡（见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第二部分"步数"）。
- 下次写共用段（多镜复用的场景描述），只放每一颗都成立的元素：年代、质感、光的方向和色温。可数的具体物件放进各镜自己的描述里，并写明数量。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 任何视频生成器都会在背景里复制显著元素。"关键帧就是背景账本"的验收方法与模型无关。
- ★ 换题材后清单内容会变（路人、车辆、窗户、招牌），方法不变。
- ★ 同一套方法也能查"消失"：关键帧里有、视频中段没了，同样算不一致。
- ☆ 骨架这一具体元素（暗黑奇幻场景）属于本项目。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（背景元素清单、接触表、PSNR）、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)（关键帧即账本）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（共用段纪律、尾部余量）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)。
- 判据清单：[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)。
- 脚本：[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)、[`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)、[`50-rubrics/scripts/asset_exists.py`](../../50-rubrics/scripts/asset_exists.py)。
- 找错题：[`60-casebook/drills/DR-07.md`](../../60-casebook/drills/DR-07.md)（人群 / 伪影）。
- 相邻案例：[`60-casebook/cards/B2-crowd-leak.md`](../../60-casebook/cards/B2-crowd-leak.md)、[`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md)（随机缺陷 vs 结构性缺陷）、[`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md)（换版后的引用替换）、[`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)。
