---
id: B1
title: 角色漂移
group: B 一致性
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [casting-and-canon, asset-boards, keyframe-freeze, video-prompting-h3, shot-qc, multi-episode-arc]
drills: [DR-06]
---
# B1 · 角色漂移

> 一句话：**身份不会因为提示词里写了名字就成立。** 它只在"参考链（角色板 + 同场已过关键帧）+ 逐字锚点句 + 逐镜裁脸比对"三者同时存在时成立；缺任何一环，生成器就按自己的先验重画一张脸。

## 症状（含人类主创原话，逐字引用档案）

- 某镜中主角苏晓的脸漂移成"粗犷成熟脸"，与板图不符〔委托方实证·B1〕。
- 人类主创把"穿帮"列为重点整改项〔委托方实证·B1〕。⚠ 档案没有保留本案的「」逐字原话。"穿帮"是档案转述的整改项名称，**禁止**把它扩写成人类引语。
- 发现者是人类，不是 agent：档案记录的修正是"把跨镜一致性对照**升为**固定验收环节"，说明此前的验收里没有这一环〔委托方实证·B1〕。
- 在学院缺陷分级里，"角色身份漂移（正脸与板图不符）且无剧情理由"属于阻断缺陷（Q7），见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §3。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 时间：前三集生产期。先导集与前三集均为竖屏 9:16，单集约 90–110s〔委托方实证·T-4〕。
- 管线：Qwen-Image-2.1 板图 1696×2528 → 关键帧（同规格，剪辑时缩放到 480×864）→ H3 以关键帧为 first_frame 驱动视频〔委托方实证·T-1、T-2、P4〕。
- 出事时的参考配置：单张板图。根因原文是"单张板图参考不足以锁住身份"〔委托方实证·B1〕。
- 漂移方向：从板图面貌漂成"粗犷成熟"。年龄感和骨相一起偏了，属于身份级偏移，不是细节噪声。
- 档案**没有记录**具体镜号、seed、景别、该镜是否有运镜或转身。复盘时不得补造这些数字；需要复现时，从本集 `qc/` 与生成日志里取。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. **没有跨镜一致性对照**：每镜只对自己验收，没有"本镜脸 vs 板图 vs 同场上一镜脸"的并排比对〔委托方实证·B1〕。
2. **单张板图不足以锁住身份**〔委托方实证·B1〕。只给一张正面肖像、却要求别的角度或景别时，模型 "has to invent what it cannot see"〔外部调研·S-VGEN-18〕。

### 方法论原因
3. 把身份当成"板图阶段一次就解决的事"，而不是**每一次生成都要重新证明的事**。板图过关不等于关键帧过关，关键帧过关也不等于视频过关，因为每次生成都会重新采样这张脸。
4. 没有区分"长期母版"和"最新变体"。拿上一镜的产出当参照，漂移会一镜一镜累积。原文："The latest variant is not your source of truth, your Master Reference Assets are"〔外部调研·S-VGEN-18〕。
5. 质量判断里没有"一致性"这一维的独立闸门。R7 立场是：身份漂移属于 AI 生成的高频缺陷，**不能以"情绪对了"为由放过**〔[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R7〕。

### 外部调研补强的根因（需在委托方节点上复测）
6. **改写锚点句会重新抽一张脸**：每一颗都要逐字重写 6–8 个具体特征，paraphrase 会重骰脸〔外部调研·S-H3-09〕。这是 P1"锚点句逐字嵌入"之所以有效的机制解释。
7. **参考图里脸太小，或用了多视角拼图**：混合参考图中脸占比太小，会导致中途"换脸"，需要另备无表情大头照；多视角图会被识别成多个主体〔外部调研·S-VGEN-11〕。不要把多个角度拼在一张 sheet 上〔外部调研·S-VGEN-18〕。角色设定拼图分辨率不够，不适合作为身份来源〔外部调研·S-H3-11〕。
8. **参考尺寸与步数**：`MiniMaxH3ReferenceToVideo` 的 `ref_image_size=max`（2048 短边）"for best identity fidelity"，`match` 档会把参考缩小〔外部调研·S-H3-03〕。4 步 turbo 下参考可能几乎不生效，脸的角度会随片子漂离参考〔外部调研·S-H3-04〕。
9. **用首帧硬转角度会融脸**：用 I2VA 从正面特写硬转出背面，"is the single most common way to melt a face"〔外部调研·S-H3-11〕。
10. 〔学院推断〕**首帧被拉伸后变形**：`MiniMaxH3ImageToVideo` 的 first_frame 是 "plain stretch to canvas"〔外部调研·S-H3-03〕。1696×2528（2:3）的关键帧送进 9:16 画布，会被横向挤压约 16%（evidence-reconciliation 第三部分）。脸型比例被改写后，模型可能沿着变形方向"补完"出另一张脸。**验证方法**：同一镜分别送"原 2:3 图"和"先等比裁成 9:16 的图"，各跑 3 seed，用 `contact_sheet.py --crop face=X:Y:W:H` 并排比较脸的宽高比和身份。

## 修正过程（做了什么、第几轮、结果）

- 委托方的修正（档案原文）：跨镜一致性对照升为固定验收环节；改用链式参考，把角色板和同场已过关键帧一起送入〔委托方实证·B1、P5、M7〕。
- 档案**没有记录**修正后的复测数字（重出了几镜、用了几个 seed、漂移率）。所以"链式参考能解决漂移"在本学院的证据等级是：委托方已采用并写入正面资产 P5/M7，但**没有量化对照**。下一次生产时，按下面的判据留存证据，把这个缺口补上。
- 学院在修正之上补了三条结构性防线：一是身份参考用单角度单图（正脸大头照与全身板分开）；二是关键帧先裁成 9:16 再送 first_frame；三是终版生成禁用 turbo。这三条都来自外部调研，委托方未实证，见根因 7–10。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 每个含角色的镜，元数据 `锚点` 都列出该角色，而且其锚点句 EN 逐字出现在 `subject_definitions` 里（`prompt_lint.py` VP-anchor；即使只是空白不同也要修）〔P1；S-H3-09〕。
- [自动] `references` 编号从 1 起连续，`<Picture N>` 与首次引用顺序一致（`prompt_lint.py` VP-picture、`slot_order_check.py`）。参考指错了图，身份就错了〔E1、T-2〕。
- [目视] 每个含主角的镜，`references` 同时挂了 `CHR-<角色>-BOARD` 和同场已通过的关键帧（P5 链式参考）。学院暂时没有脚本校验"挂的是哪张"，所以要在 `qc/<SHOT>.md` 里逐镜写明。
- [目视] 身份参考图是**单角度单图**（正脸大头照、全身各一张），不是多视角拼图；大头照里脸占画面主体〔S-VGEN-11、S-VGEN-18〕。
- [自动]+[目视] 关键帧宽高比与视频画布一致。`contact_sheet.py <clip> --keyframe <REF-SHOTnnn-START>` 报出 `B4-keyframe-aspect`，就说明关键帧不是 9:16，要先裁成 9:16 再送 first_frame〔S-H3-03〕。
- [目视] 正脸库：主角每集至少 1 个正脸镜头，裁出脸后与板图逐特征比对（发际线、眉形、眼型、鼻梁、下颌、年龄感），裁剪图存入 `qc/`〔委托方实证·B1〕。
- [目视] 跨镜对照：同场所有含主角的镜，用 `contact_sheet.py <clip> --crop face=X:Y:W:H` 导出脸部裁剪表，与板图裁脸并排。任何一格"看起来像另一个人"，该镜就不通过〔B1〕。
- [目视] 终版视频没有用 4-step turbo（查生成日志的 steps 字段）〔S-H3-04〕。
- [冷观众] 冷观众看完一集，没有出现"这是另一个人吗"这类断点；只要出现 1 次，就回流本卡。

## → 行为改变（下次……）

- 下次写任何含角色的视频或关键帧提示词时，**先从锚点卡复制**锚点句 EN 原文。禁止改写、缩写、换同义词，改一个词就等于重抽一次脸。
- 下次送 H3 之前，先看 `references`：角色板和同场已过关键帧是不是都在？只挂了一张板图就**不得 run**。
- 下次验收视频，第一个动作是裁脸并排（本镜、板图、同场上一镜），而不是先看整体好不好看。
- 下次发现漂移，先换 2–3 个 seed，判断是随机缺陷还是结构性缺陷（判法同 D3）。如果仍然漂移，就是结构性的，按下面顺序排查：参考链缺板图 → 参考图是拼图或脸太小 → `ref_image_size` 不是 max → 用了 turbo → 首帧被拉伸 → 本镜要求从正面硬转到侧面或背面。**禁止**继续加 seed 碰运气。
- 下次做板图时，为每个主角额外生成并定稿一张"无表情正脸大头照"作为身份参考，与全身板分开存放。
- **禁止**用最新一版视频帧顶替板图作为身份参照，否则漂移会累积。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 任何参考驱动的图像或视频生成器，在参考没覆盖到的角度和景别上都会自行发明面貌。换模型后，"链式参考 + 逐字锚点 + 逐镜裁脸比对"依然成立。
- ★ 季级迁移：跨集时漂移会累积。正脸库要按集存档，供 `multi-episode-arc` 做季级比对。平台对 AI 仿真人剧在"人物形象""画面衔接"上提出了更高要求〔外部调研·S-PLAT-07〕，所以漂移在发布侧也是风险。
- ☆ 漂成"粗犷成熟脸"这一方向，以及苏晓这个角色，属于本项目。1696×2528 → 9:16 的拉伸问题，只在用 `MiniMaxH3ImageToVideo` first_frame 且没有先裁切时存在。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/casting-and-canon/SKILL.md`](../../20-craft/casting-and-canon/SKILL.md)（锚点句与身份参考）、[`20-craft/asset-boards/SKILL.md`](../../20-craft/asset-boards/SKILL.md)（大头照与全身板分开、多 seed）、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)（关键帧 9:16、逐特征验收）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（逐字锚点、链式参考）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（裁脸并排）、[`20-craft/multi-episode-arc/SKILL.md`](../../20-craft/multi-episode-arc/SKILL.md)（季级正脸库）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)。
- 判据清单：[`50-rubrics/checklists/board.md`](../../50-rubrics/checklists/board.md)、[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/season.md`](../../50-rubrics/checklists/season.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/slot_order_check.py`](../../50-rubrics/scripts/slot_order_check.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-06.md`](../../60-casebook/drills/DR-06.md)（漂移 / 克隆）。
- 相邻案例与正面资产：[`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)（同框串脸）、[`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md)（验收不放大）、[`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)（参考与提示词同一事实）、[`60-casebook/positive-assets.md`](../../60-casebook/positive-assets.md)（P1、P5、M6、M7）。
