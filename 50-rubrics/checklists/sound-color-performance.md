# 声音 / 色彩灯光 / 表演 验收清单（R-SND · R-COL · R-PRF）

> **定位**：委托方在这三门手艺上是薄弱或空白（GAP-3 声音薄弱、GAP-4 色彩灯光薄弱、GAP-5 表演空白、GAP-6 节奏工程薄弱）。下面是**最低可用判据**：全部来自外部调研或学院推断，**没有一条是委托方实证**。凡标〔学院推断〕的阈值，都写了验证方法；验证结果出来后回写本表。
> **阶段与时机**：
> - 设计部分（预制作）：写 `sound-plan.md`、色彩脚本、表演卡时自查，animatic 闸门前过完（人类拍板点②）。
> - 生成部分（制作）：每镜关键帧与视频验收时，和 [`50-rubrics/checklists/keyframe.md`](keyframe.md)、[`50-rubrics/checklists/video.md`](video.md) 一起跑。
> - 混音与调色（后期）：成片渲染前后，和 [`50-rubrics/checklists/final-cut.md`](final-cut.md) 一起跑。
>
> **通过规则**：三张表各自全部行为真。`[目视]` 行没有证据文件按"未验证"处理。声明 L2 的成片，三张表都必须全过。
> **对应技能**：[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)、[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md)、[`20-craft/performance-direction/SKILL.md`](../../20-craft/performance-direction/SKILL.md) ｜ 理论：[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)、[`10-theory/12-color-and-light.md`](../../10-theory/12-color-and-light.md)、[`10-theory/13-performance-direction.md`](../../10-theory/13-performance-direction.md)

## 一、声音（R-SND）

前提：H3 的对白、音效、配乐在同一个 pass 里联合生成，**不能分轨**（S-CRAFT-12）。后期对生成音频只能叠加，不能拆除；所以生成阶段要少点名声源，精细的层次留给后期。

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-SND-01 | 每场戏有一条连续的环境床（室内的 room tone 也算），跨切点做了交叉淡化；成片中的数字静音段（低于 -60 dB、≥0.5s）都能对上已登记的设计静场 | [自动]+[目视] | silencedetect 输出 + `sound-plan.md` 的静场登记表 | GAP-3, S-CRAFT-02, S-CRAFT-03, F-CRAFT-07 | ffmpeg `silencedetect=n=-60dB:d=0.5`（无专用脚本） |
| R-SND-02 | `sound-plan.md` 的声音层表里，任一时刻同类声音 ≤2 层，同时"被点名"的声源 ≤3（对白 + 1 个关键动作声 + 1 条环境床）；每条 H3 提示词的 `overall_soundscape` 点名的声源也 ≤3 | [目视] | 声音层表 + 各镜 `overall_soundscape` 声源计数 | S-CRAFT-01, F-CRAFT-05, GAP-3 | — |
| R-SND-03 | 打斗、爆发段的关键切点（接触、爆发一击）落在配乐重拍上，偏差 ≤2 帧〔学院推断：用 3 段 A/B（对齐 vs 不对齐）请独立评审盲看，记录哪组被判"更有力"〕 | [目视] | 切点时间码 vs 节拍时间码对照表 | A3, GAP-6 | — |
| R-SND-04 | 戏剧焦点切换处（高潮台词、关键揭示）撤掉一层：音乐撤出，或用对白作侧链把音乐压下去 | [目视] | 混音参数（sidechaincompress 设置）+ 时间码 | S-CRAFT-01, F-CRAFT-04, S-CRAFT-08 | ffmpeg `sidechaincompress` |
| R-SND-05 | 每场对白戏至少 1 处 L-cut（说话声延续到听者反应画面，重叠约 0.5s）；每次换场至少 1 处 J-cut（下一场的声音提前 0.5–2s 进入）；剪辑单里音频入出点与画面入出点分开记录 | [目视] | 剪辑单的音频偏移列或备注 + 时间码 | S-CRAFT-04, F-CRAFT-06, S-CRAFT-02, GAP-6 | — |
| R-SND-06 | 生成镜一律写 `non_diegetic_music: N/A`；整场配乐在后期作为一条连续音轨铺设，跨切点没有调性或速度跳变〔学院推断：同一场分别用"逐镜生成配乐"和"后期一条轨"各出一版，独立评审盲听，记录切点断裂次数〕 | [自动]+[目视] | `grep -c "non_diegetic_music:"` 与 `N/A` 计数 + 盲听记录 | F-ZEN-07, S-ZEN-09, F-CRAFT-11, GAP-6 | `scripts/prompt_lint.py`（`VP-music`） |
| R-SND-07 | 每个打斗或爆发段之后有余波静场：音乐撤出，只留环境床、呼吸或余响，时长 ≥1s〔学院推断：用冷观众断点记录验证，静场处没人标"拖"〕 | [目视] | 静场时间码 + `sound-plan.md` 登记 | A3, S-CRAFT-01 | — |
| R-SND-08 | 拟音只配画面里看得见的动作，材质与画面一致（石、木、湿地）；每个接触相的击中声落在接触帧上 | [目视] | 拟音清单（动作、时间码、材质）+ 接触帧时间码 | S-CRAFT-03, F-CRAFT-07, A2 | — |
| R-SND-09 | 终混整体 -16 LUFS ±1、真峰 ≤ -1 dBTP（GY/T 377：-15 LKFS ±2 LU，真峰 ≤ -1 dBTP）；另外对白段响度与整体响度相差 ≤5 LU。整体 -16 达标不等于对白清晰 | [自动] | `review/verify.json` + 对白段 ebur128 输出 | T-4, S-COMFY-12, F-COMFY-11, F-CRAFT-01 | `scripts/loudness_verify.py`（`T4-lufs` `T4-true-peak`）；对白段用 ffmpeg `ebur128` |
| R-SND-10 | 每条非生成的音乐、音效在 `assets/license-ledger.md` 有一行：来源 URL、许可名、是否需署名、署名文本、下载日期、许可原文存档路径；BBC RemArc、CC BY-NC、CC BY-ND 来源的素材数为 0 | [目视] | 许可台账 + 存档文件 | S-CRAFT-21, S-CRAFT-30, F-CRAFT-20, F-CRAFT-26, S-CRAFT-25 | `grep -c` 台账行数 vs 素材文件数 |

## 二、色彩与灯光（R-COL）

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-COL-01 | 每集有色彩脚本：每个段（`SEQ-nn`）一格，写明主色相、饱和度（高/中/低）、明度（高/中/低）、光比档、色温；季圣经里另有一条季级色彩弧 | [目视] | `visual-bible.md` 的色彩脚本表 | S-CRAFT-13, F-CRAFT-14, GAP-4 | — |
| R-COL-02 | 色彩脚本每格命名 3–5 个颜色（如 `ash grey, ember orange, bruise purple`），并逐字写进该段每一个关键帧的冻结提示词 | [自动]+[目视] | 每格色名 + 各关键帧提示词的 grep 命中 | F-CRAFT-08, S-CRAFT-10 | `grep -F`（无专用脚本） |
| R-COL-03 | 情绪不同的相邻两段，色彩脚本格至少有一项（色相、饱和、明度、光比）不同；全集各格完全相同（例如全片同一套青橙）判不通过 | [目视] | 色彩脚本表的逐格对照 | F-CRAFT-14, S-CRAFT-16 | — |
| R-COL-04 | 每个关键帧的冻结提示词都写了主光源（画面内或可推断：窗、门、灯、屏、火、月、车灯）、方向、色温和光比档；光写成被动描述（`warm light falls from the left`），不写会被生成成实物的灯具或光柱 | [自动]+[目视] | 冻结提示词原文 | S-CRAFT-14, F-CRAFT-13, B3, S-H3-09 | `scripts/prompt_lint.py`（`VP-light`，视频提示词侧） |
| R-COL-05 | 同一场景的全部关键帧并排后，主光方向一致，并与场景板标注一致；不一致的镜回关键帧重出 | [目视] | 同场关键帧拼图 + 光向标注 | S-CRAFT-14, S-H3-10, A5 | ffmpeg `tile` / `hstack` |
| R-COL-06 | 色彩脚本格声明的光比档与该段情绪一致（紧张、危险段为低调，约 8:1；轻松段为高调，约 1:1）；关键帧去色后的明暗分布与声明档位相符 | [目视] | 去色缩略图 + 档位声明 | S-CRAFT-15, F-CRAFT-12 | ffmpeg `format=gray` |
| R-COL-07 | 同场相邻 CUT 的抽帧并排后，肤色和白平衡没有跳变；需要统一时，用场景参考帧做颜色匹配，或全集统一一份 `.cube`（ffmpeg `lut3d`），参数记进剪辑单备注 | [目视] | 成片接触表 + 处理参数 | S-CRAFT-17, S-CRAFT-08, F-CRAFT-31, B1 | `scripts/contact_sheet.py final/epNN.mp4`；ffmpeg `lut3d` |
| R-COL-08 | 低调段的关键帧缩到 270 宽后，主体的脸和表情仍可辨〔学院推断：外部调研没找到竖屏手机调色指南；用冷观众断点记录验证，暗场处没人标"看不清"〕 | [目视]+[冷观众] | `kf-poster270-gray.png` + 冷观众断点记录 | GAP-4, M2 | ffmpeg `scale=270:-2` |

## 三、表演（R-PRF）

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-PRF-01 | 每个有表演的镜，在表演卡里写了一个任务动词（说服、逼问、试探、隐瞒、求饶……）；冻结提示词和视频提示词里，没有把裸情绪词（sad、angry、happy、scared）当表情指令 | [自动]+[目视] | 表演卡 + grep 结果为空 | S-CRAFT-18, F-CRAFT-15, F-CRAFT-17, GAP-5 | `grep -n -i -w -e sad -e angry -e happy -e scared video-prompts.md` |
| R-PRF-02 | 表情写成变化，不写成状态：每个表情拍写"从 A 到 B"的过渡（例如压住 → 泄露 → 释放 → 恢复），并写明镜末的收束状态 | [目视] | 提示词中的过渡句 + 收束句 | F-CRAFT-18, S-CRAFT-20, F-CRAFT-16 | — |
| R-PRF-03 | 表情变化按生理顺序写：眉 → 眼 → 嘴（真笑先到眼）；同时写出"不准动的部位"，防止模型自动补齐笑容 | [目视] | 提示词原文 | S-H3-09, GAP-5 | — |
| R-PRF-04 | 每镜表情拍 ≤2–3 个；超过的拆成多镜，或在剪辑里用插入镜处理 | [自动]+[目视] | 分镜 `拍数` 列 + segment_rhythm 报告 | S-H3-09, F-H3-16, A5 | `scripts/segment_rhythm.py`（`A5-beats-many`） |
| R-PRF-05 | 画面 ≥2 个主体且有对白时，非说话人有闭嘴句（`[S2] does not speak; his lips remain completely closed.`），或背身、出画；出片后非说话人在对方台词时段嘴部闭合 | [自动]+[目视] | prompt_lint 报告 + 嘴部裁剪表 | S-ZEN-17, F-ZEN-08 | `scripts/prompt_lint.py`（`VP-lipsync`）；`scripts/contact_sheet.py --crop` |
| R-PRF-06 | 每个有表演的镜写明视线目标（看谁、看哪；直视、回避、扫视）；多人镜的视线方向与起始帧方位一致（画面左的人看向画面右） | [目视] | 提示词视线句 + 关键帧标注 | F-CRAFT-17, S-CRAFT-21, A5 | — |
| R-PRF-07 | 每个情绪转折至少落一个可见的形体动作（吞咽、攥拳、肩落、长呼气），不只靠脸 | [目视] | 提示词形体句 + 接触表中对应格 | S-CRAFT-19, S-CRAFT-18, GAP-5 | `scripts/contact_sheet.py` |
| R-PRF-08 | 标为表情镜的特写，`psnr_scan` 的中位 PSNR <37 dB，且没有覆盖全镜的 `P8-freeze`；中位 ≥37 dB 视为脸基本没动、表情没落地，拆镜或减拍重出〔阈值取自 F-H3-16 的单项目实测（塞满 9 拍时 37–42 dB），待本管线复测〕 | [自动]+[目视] | `<SHOT>.psnr.json` 的中位值 + 接触表 | F-H3-16, S-H3-09, P8, GAP-5 | `scripts/psnr_scan.py`（`P8-psnr-stats` `P8-freeze`） |
| R-PRF-09 | 微表情特写只用固定机位（`static, on a tripod, with no camera movement whatsoever`），不叠加运镜 | [目视] | 提示词原文 | F-CRAFT-18, S-H3-09, S-H3-10 | — |
| R-PRF-10 | 冷观众或独立评审看完关键表演镜，能说出这个角色此刻"想要什么"，并且与表演卡上的任务动词一致 | [冷观众] | 冷观众记录中的复述句 | GAP-5, F1 | — |

## 常见误判

**声音**
- **"响度 -16 达标了，声音就没问题"**：-16 LUFS 只证明整体音量合规。对白会不会被音乐盖住、层次是不是糊成一团，它都证明不了（R-SND-02、R-SND-09）。见 [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)。
- **不写配乐字段 = 静音**：省略 `non_diegetic_music` 时，模型会自配通用音乐（F-ZEN-07）。每镜各带一段配乐，切点上就是一次调性跳变，"片段感"会被放大（R-SND-06）。
- **静场用数字静音实现**：真正的安静里有 room tone；数字零在切点上听起来像掉了个洞（R-SND-01）。

**色彩**
- **全片套一个 LUT 就算有了色彩设计**：统一 LUT 只解决一致性，不表达情绪变化。色彩脚本是逐段的（R-COL-01、R-COL-03）。
- **写 `lit by a floor lamp`**：提到什么就长什么，灯具会出现在画面里，还可能变成光柱（S-H3-09）。只写光的方向和色温（R-COL-04）。见 [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)。

**表演**
- **写 `she looks sad`**：结果是夸张的卡通表情（F-CRAFT-17）。要写任务动词和可见的变化过程（R-PRF-01、R-PRF-02）。
- **一个特写塞满情绪层次**：超过 2–3 个表情拍会被平均抹平，结果是脸不动（F-H3-16）。拆镜，并用 PSNR 验证表情真的落地了（R-PRF-04、R-PRF-08）。
- **多人镜不写闭嘴句**：口型会落到不说话的人身上（R-PRF-05）。

## → 行为改变

下次进入预制作，在写分镜的同时出三张表：`sound-plan.md` 的声音层表、色彩脚本、表演卡。animatic 闸门前用本文件三张清单自查。三张表缺任何一张，不进 prepare。
