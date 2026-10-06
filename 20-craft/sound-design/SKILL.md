---
name: sound-design
description: 为每集设计并落地声音：按场写声音层次表（对白/环境床/拟音/设计音效/音乐），生成镜只点名≤3 个声源、配乐一律 N/A，后期在 H3 原声上叠加拟音与连续配乐，用剪辑单的音频偏移做 J/L cut，设计静场与音乐重拍↔切点，终混 -16 LUFS（GY/T 377）并为每条音乐音效建许可台账、为每个说话角色绑定固定音色。Use when planning sound for an episode, writing overall_soundscape / non_diegetic_music, mixing, or when feedback says audio feels fake/empty/noisy. 触发词：声音设计、音效、拟音、环境声、配乐、静场、J-cut、L-cut、响度、混音、音色、sound design, soundscape, foley, ambience, room tone, music cue, J-cut, L-cut, loudness, LUFS, voice binding。不负责台词文本与容量（script-doctor）、字幕与成片渲染（edit-and-assemble）、发布前的许可拍板（publish-prep）。
---
# 声音设计（sound-design）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。委托方只做过"对白 + 基础拟音 + 配乐"（GAP-3、GAP-6），本技能除响度口径外均为〔外部调研〕或〔学院推断〕，按各条验证方法小样验证。

## 何时用 / 何时不用

- **用**：分镜定稿后写 `sound-plan.md`（与表演卡并行）；写每镜 `overall_soundscape` / `non_diegetic_music` 时；剪辑锁定后做后期声音；人类说"声音假 / 空 / 吵"时（Q8）。
- **不用**：缺句、赶词——先回 script-doctor / storyboard 改时长（T11.9：缺句改时长，赶词才换 seed）。
- **不用**：只想让 H3 "生成好听的配乐"——生成镜禁止承担配乐（R-SND-06）。

## 输入 → 输出

| 输入 | 输出 | 模板 / 位置 |
|---|---|---|
| `storyboard.md`（段、拍、对白、打击点） | `sound-plan.md`：每场一张声音层表 + 静场登记 + 重拍↔切点表 | 本集目录；结构随 [`70-playbooks/templates/storyboard.md`](../../70-playbooks/templates/storyboard.md) 的段号 |
| 角色表（`season-bible.md`） | 音色绑定行（角色 → 参考音频 / 外配音色 ID） | [`70-playbooks/templates/season-bible.md`](../../70-playbooks/templates/season-bible.md)、[`70-playbooks/templates/anchor-card.md`](../../70-playbooks/templates/anchor-card.md) |
| 每镜提示词 | `overall_soundscape:`（≤3 声源）+ `non_diegetic_music: N/A` | [`70-playbooks/templates/video-prompt-h3.md`](../../70-playbooks/templates/video-prompt-h3.md) |
| 锁定的 `edit-list.md` | 音频偏移列 / 声音层工程、终混文件 | [`70-playbooks/templates/edit-list.md`](../../70-playbooks/templates/edit-list.md) |
| 外部素材 | `assets/license-ledger.md`（每条一行） | R-SND-10 字段 |

## 步骤

1. **静音看一遍，列缺失清单**：在 animatic 或粗剪上关声音看一遍，写下"画面里看得见、却该有声音"的每个动作与环境。后期顺序固定：对白 → 环境床 → 拟音 → 设计音效 / 冲击声 → 音乐 → 总线平衡；禁止先铺音乐再塞对白（T11.3）。〔外部调研·S-CRAFT-02、S-CRAFT-03〕
2. **写声音层表**（`sound-plan.md`，每场一张）：列 `时间段 | 对白 | 环境床 | 拟音 | 设计音效 | 音乐 | 焦点`。同一时刻同类声 ≤2 层；可分辨声源总数 ≤5 且分散在对白—音效—音乐光谱上（Murch 密度）。戏剧焦点切换处（高潮台词、揭示）必须撤掉一层。验：R-SND-02、R-SND-04。〔外部调研·S-CRAFT-01〕
3. **生成镜只点名 ≤3 个声源**：`overall_soundscape` = 对白 + 1 个关键动作声 + 1 条环境床；更细的层留给后期——生成声轨不能拆，只能叠（T11.2）。`non_diegetic_music: N/A` 必须显式写，不写 ≠ 静音，模型会自配泛用音乐〔外部调研·S-H3-11、S-ZEN-09〕。验：`python3 50-rubrics/scripts/prompt_lint.py video-prompts.md --anchors anchors.md --storyboard storyboard.md`（`VP-music`）；R-SND-06；出片听感 R-VID-22。
4. **绑定音色**：每个有台词的角色全季绑定一个固定音色来源（参考音频或外配音色 ID），写进角色表"音色"列。同场两个同性别说话人，盲听各 3 句分不出 → 改外配，不再赌生成〔外部调研·S-ZEN-17：H3 两个男声相似度高〕。验：R-SEA-13、R-SEA-14。
5. **环境床连续**：每场一条连续环境床（室内用 room tone），跨切点交叉淡化；成片里出现 < -60 dB、≥0.5s 的数字静音，必须对得上 `sound-plan.md` 登记的设计静场。验：R-SND-01；`python3 50-rubrics/scripts/loudness_verify.py final/epNN.mp4 --min 90 --max 110` 的报告 + 目听。
6. **设计静场**：每个打斗 / 爆发段之后留 ≥1s 余波静场：撤音乐，只留环境床、呼吸或余响。静场在层表里登记起止时间。验：R-SND-07〔学院推断：冷观众断点记录里静场处没人标"拖"即成立〕。
7. **拟音只配看得见的动作**：材质与画面一致（石 / 木 / 湿地）；接触相的击中声落在接触帧上（用接触表帧号对齐）。H3 原声保留作底，后期 SFX 叠在其上，冲突时压低原声而不是删掉对白。验：R-SND-08。
8. **J/L cut 写进剪辑单**：每场对白戏至少 1 处 L-cut（说话声延续到听者反应画面，重叠 ≈0.5s）；每次换场至少 1 处 J-cut（下一场声音提前 0.5–2s 进入）。在 `edit-list.md` 用音频入出点相对画面入出点的偏移表达（同一 CUT 写"音频偏移 -0.50"类备注列；脚本忽略多余列，契约列不动）。验：R-SND-05。〔外部调研·S-CRAFT-04〕
9. **配乐按场铺一条连续音轨**：不逐镜生成音乐；对白出现时用侧链把音乐压下（ffmpeg `sidechaincompress`）；打斗关键切点（接触、爆发一击）落在重拍上，偏差 ≤2 帧——先定音乐重拍时间表，再微调 CUT 出点，或反过来裁音乐。验：R-SND-03、R-SND-06。〔外部调研·S-CRAFT-08；学院推断：对齐 vs 不对齐 A/B 请独立评审盲看〕
10. **终混与响度**：整体 -16 LUFS ±1、真峰 ≤ -1 dBTP（GY/T 377-2023：-15 LKFS ±2 LU 区间内）；另查对白段与整体相差 ≤5 LU——整体达标不等于对白听得清。两遍 loudnorm 后测**编码成品**而不是工程文件。验：`python3 50-rubrics/scripts/loudness_verify.py final/epNN.mp4`（`T4-lufs`、`T4-true-peak`）；R-SND-09、R-CUT-01、R-CUT-02。〔外部调研·S-COMFY-12、S-CRAFT-05、S-CRAFT-07〕
11. **许可台账**：每条非生成的音乐 / 音效在 `assets/license-ledger.md` 登记：来源 URL、许可名、是否需署名、署名文本、下载日期、许可原文存档路径。默认禁用：BBC RemArc 音效（非商用）、任何 NC / ND 曲目、MiniMax Music 3 开源权重（据报道 CC BY-NC 4.0）、在 YouTube 以外使用的 YouTube 音频库曲目。验：R-SND-10、R-PUB-12。〔外部调研·S-CRAFT-23、S-CRAFT-24、S-CRAFT-28、S-CRAFT-30、S-H3-16〕
12. **字幕与声音对账交给下游**：字幕逐字取自剧本，转写只定位时间、查缺句（T11.8）——由 shot-qc 的 `transcript_reconcile.py` 与 edit-and-assemble 执行，本技能不改字幕文本。

## 判据

- 设计：R-SND-02、R-SND-04、R-SND-06（生成镜配乐 N/A）、R-SEA-13、R-SEA-14。
- 后期：R-SND-01、R-SND-03、R-SND-05、R-SND-07、R-SND-08。
- 终混与许可：R-SND-09、R-SND-10、R-CUT-01、R-CUT-02、R-PUB-12、R-PUB-13。
- 出片：R-VID-22（写了 N/A 的镜听不到配乐）。
- 质量维度：主 **Q8 声音与对白**；次 **Q6 节奏与速度**（静场、重拍↔切点）、**Q4 特效与事件**（冲击声是特效的一半）。技术全绿只证明 Q8 没有 0 分的技术原因，不证明 ≥2（F2）。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| 某句台词缺失 / 赶词，在混音里试图补救 | [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md) | 声音不修结构缺陷：缺句回分镜改时长；本技能只在容量合格后工作 |
| 静音段被 ASR 幻觉成台词，"多了一句"被误判 | [`60-casebook/cards/D5-qc-tools-lie.md`](../../60-casebook/cards/D5-qc-tools-lie.md) | 步骤 5 登记设计静场；对白结论必须双通道（转写 + 看嘴 / 亲耳听） |
| 响度全绿就宣布"声音合格" | [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md) | 层表、静场、J/L cut 三项目听判据独立于 `T4-lufs` |
| 慢镜段靠铺满音乐撑情绪 | [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md) | 步骤 6：爆发后撤音乐留静场；音乐不能替代事件密度 |
| 切点生硬、片段感强 | [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md) | 步骤 5 环境床跨切点交叉淡化 + 步骤 8 J/L cut 缝合 |
| 字卡 / 纯色段整段数字静音或交给生成器配声 | [`60-casebook/cards/D2-solid-black-fails.md`](../../60-casebook/cards/D2-solid-black-fails.md) | 纯色卡本地生成，声音床在后期铺；R-SND-01 静音段必须登记 |

## 关联

- 理论：[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)（T11.1–T11.12）、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)。
- 裁决：[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第二部分"声音""音色"行、第三部分响度、第四部分配乐许可。
- 相邻技能：[`20-craft/video-prompting-h3/SKILL.md`](../video-prompting-h3/SKILL.md)（soundscape 字段）、[`20-craft/performance-direction/SKILL.md`](../performance-direction/SKILL.md)（呼吸、静场与表演同拍）、[`20-craft/edit-and-assemble/SKILL.md`](../edit-and-assemble/SKILL.md)（偏移落地与渲染）、[`20-craft/multi-episode-arc/SKILL.md`](../multi-episode-arc/SKILL.md)（音色全季绑定）、[`20-craft/publish-prep/SKILL.md`](../publish-prep/SKILL.md)（许可拍板）。
- 找错题：[`60-casebook/drills/DR-11.md`](../../60-casebook/drills/DR-11.md)、[`60-casebook/drills/DR-13.md`](../../60-casebook/drills/DR-13.md)、[`60-casebook/drills/DR-17.md`](../../60-casebook/drills/DR-17.md)。
- 判据清单：[`50-rubrics/checklists/sound-color-performance.md`](../../50-rubrics/checklists/sound-color-performance.md)（R-SND 段）。

## → 行为改变

- 下次写任何 H3 提示词时，`non_diegetic_music: N/A` 先写上，`overall_soundscape` 数一遍声源，>3 就删。
- 下次进后期，先关声音看一遍写缺失清单，再按 对白→环境→拟音→音效→音乐 顺序搭，禁止从挑配乐开始。
- 下次 `loudness_verify.py` 通过后，再单测对白段响度并目听静场与 J/L cut，三项未查不得写"声音合格"。
- 下次下载任何音乐音效，先在许可台账写行再放进工程。
