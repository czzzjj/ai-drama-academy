---
id: A1
title: 碎镜症
group: A 叙事与节奏
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [storyboard-long-take, script-doctor, edit-and-assemble]
drills: [DR-01, DR-22]
---
# A1 · 碎镜症

> 一句话：**短剪不是罪，碎镜症是罪。** 病不在"剪得快"，而在"一个动作 = 一个镜号"：没有"段"这一层设计，因果链被切断、空间建立不起来，而且 H3 根本生成不了 <5.17s 的可靠镜头。

## 症状（含人类主创原话，逐字引用档案）

- 人类主创原话：「片段式、剧情跳跃、无法理解」「切片太短，切点跳脱感强」〔委托方实证·A1〕。
- 与此同时，agent 自己的验收是全绿的（"无坏帧/无烧录/全采用"）——人类说"片段式、跳跃"〔委托方实证·F2〕。
- 观感层面：观众说不出"谁想要什么 → 做了什么 → 结果如何"，即冷观众复述因果链失败——[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) 中 Q1 的阻断缺陷。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 何时：前三集**首轮**成片全部如此〔委托方实证·A1〕。
- 数字：成片 **29 个镜、均长 2.96s/镜**〔委托方实证·A1〕。
- 换算（学院补注）：29 × 2.96 ≈ 85.8s，量级与委托方单集 90–110s 相当〔委托方实证·T-4〕；2.96s × 24fps ≈ 71 帧，**远低于 H3 训练下限 124 帧（5.17s）**，也不在 17k+5 帧网格上〔委托方实证·T-2〕。即"剪辑单位"与"生成单位"被当成了同一个东西。
- 当时的自我设限：每镜 ≤3s；**不知道、也没测过** H3 单次可连续生成 5.2–15.1s〔委托方实证·A1②〕。

## 根因（分条；区分"直接原因"与"方法论原因"）

**直接原因**
1. **动作清单化**：把"分镜"理解成"一个动作 = 一个镜号"，剧本里的每个动词都变成一个独立镜〔委托方实证·A1①〕。相邻镜之间没有动作匹配，剪点落在动作前后的静止处，所以每一刀都"跳"。
2. **不知道生成器的连续能力**：没测过 H3 帧网格（124–362 帧 = 5.17–15.08s），自我设限 ≤3s〔委托方实证·A1②、T-2〕。低于 124 帧时动作表现异常〔委托方实证·T-2；外部调研·S-H3-03〕，所以短镜同时是"观感问题"和"生成质量问题"。
3. **镜内装不下"完成"**：一个内部镜头通常至少要约 4–6s 才能完成动作、反应和退出；镜数超过时长承载能力时，模型会压缩、跳过或在动作中途乱切〔外部调研·S-PIPE-01〕。2.96s 的镜只能装下"动作的一截"，装不下"动作 + 反应"，因果在镜内就断了。

**方法论原因**
4. **没有"段"（sequence）这一设计层**：只有"镜"的概念，没有"一场戏/一条完整动作链"的单位〔委托方实证·A1③〕。节奏被理解为"切得多 = 快"，而节奏 KPI 应是**有效拍数**（状态改变的次数），不是切镜数〔委托方实证·A1；见 [`00-orientation/glossary.md`](../../00-orientation/glossary.md)〕。
5. **把生成执行当成制作**：病灶在预制作（剧本 → 分镜的单位划分），却在生成和剪辑阶段被发现〔委托方实证·G7〕。
6. **用代理指标验收**："全采用、无坏帧"证明不了"看得懂"〔委托方实证·F2〕。
7. **外部补强——快剪为什么在别处成立**：港片 12 分钟高潮约 490 个镜头、最短约 1/3 秒仍"totally intelligible"，靠的是动作匹配剪辑、遵守 180° 规则、稳定机位〔外部调研·S-STORY-19〕；cutting on action 让"两个可能相隔数小时拍的镜头"看起来时间连续〔外部调研·S-STORY-10〕。委托方的短镜缺的正是这三样，所以短 = 碎。
8. **外部补强——剪点 = 一个想法结束**：Murch：动作戏约 25 刀/分钟，对白戏约 6 刀/分钟（≈10s/刀）仍显正常〔外部调研·S-STORY-14〕。把动作戏的刀速用在文戏上，就是碎片化〔学院推断：验证法=统计成片中含对白 CUT 的均长，若 <5s 且冷观众标记跳跃，成立〕。

## 修正过程（做了什么、第几轮、结果）

1. 委托方提出并固化**长段多拍**：8–15s/段、段内 2–3 拍、一段 = 一条完整动作链；连续动作不得切新镜〔委托方实证·A1、P10、M1〕。P10 标注为"实证自 r1–r5 实验"。
2. 结果：档案**未记录**修正后成片是否被人类主创认可为"不再片段式"；T-4 记录整体仍未达到可发布线 → 本卡的修正是"已换来的正确方法论"，但**观感闭环未验证**。下一次生产必须用冷观众判据补上这一环。
3. 学院补强（〔学院推断〕，验证法见判据）：
   - 区分两级单位（R6）：**生成单位（镜）≥124 帧、承载一条完整动作链；剪辑单位（CUT）可以很短**——快剪从长镜里取，不靠多生成短镜〔外部调研·S-PIPE-01："generation_block 一次请求 + edit_beat 2–8s"两级时间〕。
   - 每镜先写"这一镜改变了什么"（信息/权力/情绪/关系/危险/空间），一项都不改变的镜删掉〔外部调研·S-H3-10〕。
   - 生成时尾部留 1.3–1.5s 余量（H3 常在片尾前 1.2–1.7s 崩解），剪辑时裁掉〔外部调研·S-H3-09〕；所以分镜时长 = 剧情所需 + 尾部余量，再吸附到帧网格（`h3_frame_grid.py --seconds`）。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [自动] 送 H3 的镜时长 ≥5.17s（124 帧）；<5.17s 的镜必须填 `短镜理由` 且不送 H3（改本地生成或从长镜中剪出）——`segment_rhythm.py` 的 A1-short-no-reason（error）；`h3_frame_grid.py --check` 的 T2-frames-below-min。〔A1、T-2〕→ storyboard 清单
2. [自动] 分镜平均镜长 ≥5.0s、<5s 短镜占比 ≤20%——`segment_rhythm.py --min-mean 5.0 --max-short-share 0.2`（A1-mean-short error / A1-short-share warn）。〔A1〕→ storyboard 清单
3. [自动] 每镜都有 `段号`（归属一个 SEQ）——`segment_rhythm.py` 的 P10-seq-missing。〔A1③、P10〕→ storyboard 清单
4. [自动] 节奏报告写**有效拍数**（Σ拍数，`segment_rhythm.py` 的 A1-stats），不得以"切镜数多"作为节奏达标证据。〔A1、F2〕→ storyboard 清单
5. [目视] 成片跑 `psnr_scan.py final.mp4 --mode final --edit-list edit-list.md`；出现 A1-mean-short warn 时，逐个短 CUT 核对三件事：剪点在动作进行中（cutting on action）、相邻 CUT 同轴、机位稳定；任一不满足 → 回分镜合段，不在剪辑里加转场。证据：切点帧序列。〔A1；外部调研·S-STORY-19〕→ final-cut 清单
6. [目视] 每个段能写出一句"谁想要什么 → 做了什么 → 结果"；每镜能写出"这一镜改变了什么"，写不出 → 删镜或并入相邻镜。〔A1③；外部调研·S-H3-10〕→ storyboard 清单
7. [目视] 自我放映：连续看一遍不暂停，记录"第一次困惑的时间点"；困惑点落在切点上 → 视为碎镜，回分镜。〔A1、F1〕→ final-cut 清单
8. [冷观众] ≥3 名冷观众中 ≥2/3 能复述本集主因果链，且无 ≥2 人同时标记的"看不懂/跳跃"断点。〔A1、F1；阈值见 definition-of-done L1〕→ final-cut 清单

## → 行为改变（下次……）

- 下次拆剧本时，**先**划"段"（一条完整动作链/一个戏剧单元，8–15s），**再**在段内标 2–3 个拍，**最后**才决定镜；禁止从动词清单直接生成镜号。
- 下次排镜长时，**先**用 `h3_frame_grid.py --seconds <剧情所需+1.5>` 吸附到合法帧数；任何 <5.17s 的镜**必须**写 `短镜理由`，且该镜不送 H3。
- 下次想要"快节奏"时，**改为**生成长镜、在剪辑里从长镜中取多个短 CUT（剪在动作中途、守同一轴线），**禁止**为了快而生成更多短镜。
- 下次写节奏自评时，**只**报有效拍数与段结构，**禁止**把镜数、切点数当成节奏达标证据。
- 下次人类说"片段式/跳跃/看不懂"时，**先**回到分镜阶段重划段，**禁止**在剪辑里加转场特效或字卡解释。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ "段 → 拍 → 镜 → CUT"四层单位对任何题材成立；文戏比动作戏更怕碎（对白场的自然刀速远低于动作场）。
- ★ 生成单位 ≠ 剪辑单位对所有有最短时长/训练区间的视频模型成立；不同模型下限不同——Sora 时长档 4/8/12s，且"两段 4s 拼接常比一段 8s 稳定"〔外部调研·S-VGEN-01〕，所以 5.17s 这个数字是 ☆H3 专属，"先划段再定镜"是 ★通用。
- ☆ 124/362 帧、17k+5 网格、尾部 1.3–1.5s 余量只适用于 H3；换模型时先测下限与崩解区，再改 `h3_frame_grid.py` 的等价参数。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（段/拍/镜结构）、[`20-craft/script-doctor/SKILL.md`](../../20-craft/script-doctor/SKILL.md)（剧本层的段落划分与信息密度）、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)（从长镜取 CUT、剪在动作中）、[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（病灶回到预制作）。
- 理论：[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)。
- 判据清单：[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/script.md`](../../50-rubrics/checklists/script.md)。
- 脚本：[`50-rubrics/scripts/segment_rhythm.py`](../../50-rubrics/scripts/segment_rhythm.py)、[`50-rubrics/scripts/h3_frame_grid.py`](../../50-rubrics/scripts/h3_frame_grid.py)、[`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)。
- 找错题：[`60-casebook/drills/DR-01.md`](../../60-casebook/drills/DR-01.md)（碎镜）、[`60-casebook/drills/DR-22.md`](../../60-casebook/drills/DR-22.md)（病灶路由）。
- 相邻案例：[`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)（拉长镜后若事件密度不足 → 变慢镜）、[`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)（段内拍太多 → 空间跳变）、[`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)。
