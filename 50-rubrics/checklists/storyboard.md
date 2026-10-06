# 分镜清单（R-SB）

> **阶段**：1 预制作·分镜（`storyboard.md` + `action-design.md` + animatic）。服务维度：Q2 空间与调度、Q3 动作与物理、Q6 节奏与速度、Q8 声音与对白（[`50-rubrics/quality-model.md`](../quality-model.md)）。
> **何时跑**：分镜定稿前、animatic 前（人类拍板点②之前）；分镜任何一行改动后**全量**重跑脚本（不是只跑改动的镜）。执行技能：[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)、[`20-craft/action-choreography/SKILL.md`](../../20-craft/action-choreography/SKILL.md)。
> **通过规则**：`segment_rhythm.py`、`dialogue_capacity.py` 0 error（命令见 [`50-rubrics/README.md`](../README.md) §5 步骤 2–3）；`direction_audit.py`、`prompt_lint.py` 的分镜侧条目在提示词写好后复核；每条 `[目视]` 条目的证据存在。**未通过本清单全部 `[自动]` 条目的镜禁止进入 prepare。**
> 表格格式以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §1 为准。

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-SB-01 | 送 H3 的每镜 `时长(s)` ≥ 5.17（124 帧）；< 5.17 的镜填了实质性 `短镜理由` 且标注不送 H3（本地生成或从长镜剪出） | [自动] | `qc/segment_rhythm.json` 无 A1-short-no-reason | A1, T-2, S-H3-02 | scripts/segment_rhythm.py（A1-short-no-reason）；scripts/h3_frame_grid.py（T2-frames-below-min） |
| R-SB-02 | 每镜 `时长(s)` ≤ 15.08（362 帧单次上限）；超出的已拆成两段 | [自动] | segment_rhythm 报告无 T2-over-max | T-2, A1 | scripts/segment_rhythm.py（T2-over-max） |
| R-SB-03 | 生成镜平均时长 ≥ 5.0s，且 < 5s 的短镜占比 ≤ 20% | [自动] | segment_rhythm 报告的 A1-stats 行 | A1, P10 | scripts/segment_rhythm.py（A1-mean-short, A1-short-share） |
| R-SB-04 | 每镜都填了 `段号`（归属一个 SEQ） | [自动] | segment_rhythm 报告无 P10-seq-missing | A1, P10, M1 | scripts/segment_rhythm.py（P10-seq-missing） |
| R-SB-05 | 每个段承载一条完整动作链或一个完整戏剧单元；同一条连续动作没有被切成两个镜号 | [目视] | `review/storyboard/segments.md`：每段一句"谁想要什么 → 做了什么 → 结果" | P10, M1, A1 | — |
| R-SB-06 | 每镜 `拍数` ≤ 3；> 3 的镜在 `内容` 中写明空间如何不跳变，否则已拆段 | [自动]+[目视] | segment_rhythm 报告的 A5-beats-many 行 + 处置 | A5, P10, F-H3-16 | scripts/segment_rhythm.py（A5-beats-many） |
| R-SB-07 | `拍数` 只计空间拍 + 表情拍；打击拍写在 `内容` 动作链里，没有为消 P10-beats-chain 把打击拍计入 `拍数` | [目视] | 打斗段逐镜的拍分类标注 | A2, A5, F-H3-17 | scripts/segment_rhythm.py（P10-beats-chain 为 info，属预期） |
| R-SB-08 | 每镜 `运镜因果` 是"因为 X，所以镜头 Y"句式；静止镜写"因为……，所以不动" | [自动] | segment_rhythm 报告无 A4-cause | A4 | scripts/segment_rhythm.py（A4-cause） |
| R-SB-09 | 每个因果句的 X 是画面内可见事件或信息/情绪转折（受击、爆发、腾跃、揭示、收束），Y 是叙事功能（跟随、揭示、压迫、释放）；"为了更有电影感 / 更动态"类理由为 0 条 | [目视] | `review/storyboard/camera-cause.md`：逐镜 X / Y 分类 | A4, S-STORY-15, F-ZEN-19 | — |
| R-SB-10 | 每镜 `运镜` 只写一个主运动且属于高度或距离维度；顿挫 / 震动写成"接触引起的相机响应"，不是第二条运镜 | [目视] | 运镜列逐镜标注维度 | A4, A5, S-H3-10, F-H3-18 | — |
| R-SB-11 | 每个有人物的镜都填了 `起始帧方位`，取值为大写 `LEFT/RIGHT/CENTER/FG/BG` | [自动] | direction_audit 报告无 DIR-layout | A5, M4, P4 | scripts/direction_audit.py（DIR-layout） |
| R-SB-12 | `运镜` 列与 `内容` 列不含相机左右维度运动（truck / arc / orbit / weave / pan / 绕到身后）；确需换边的镜在提示词 `- 换边:` 写了理由与起始帧支持证据 | [自动]+[目视] | direction_audit 报告中 where=运镜/内容 的 DIR-camera / DIR-path 行与处置 | A5, M4 | scripts/direction_audit.py（DIR-camera, DIR-path） |
| R-SB-13 | 同场相邻镜左右顺序不反转、屏幕方向连续（画右出 → 画左入）；越轴只用轴上缓冲镜、可见跨轴运镜、角色自己走过轴线三种之一 | [目视] | `review/storyboard/axis-map.md`：每场俯视站位图（文字或草图）+ 逐镜方位 | A5, S-STORY-08, F-STORY-13 | — |
| R-SB-14 | 每镜对白装得下：`dialogue_capacity.py --storyboard storyboard.md` 无 D3-capacity / D3-margin / D3-split error | [自动] | `qc/dialogue_capacity.json` | D3, P9, M5, T-2 | scripts/dialogue_capacity.py（D3-capacity, D3-margin, D3-split） |
| R-SB-15 | 每条 D3-rushed / D3-tight warn 已处置：延长到建议帧数、或把台词拆到听者镜、或删句；不允许"让人物加快语速" | [自动]+[目视] | capacity 报告 + 处置记录 | D3, F-ZEN-05, S-ZEN-22 | scripts/dialogue_capacity.py（D3-rushed, D3-tight） |
| R-SB-16 | 运行 dialogue_capacity 时 `--margin` 不低于默认 1.0、`--rate` 不高于 7.5；没有用调参数的方式消 error | [自动] | capacity 报告 JSON 中记录的参数 | D3, F-ZEN-06 | scripts/dialogue_capacity.py |
| R-SB-17 | `内容` 列写事件不写形容词，动作链用 `→` 串联；无"华丽 / 史诗 / 震撼"类评价词 | [目视] | grep 结果（0 命中或附改写） | M3, A1 | grep（无专用脚本） |
| R-SB-18 | 每个动作段标出速度层次（快 / 慢 / 爆 / 静 中 ≥ 2 种），每个"慢"写明设计理由 | [目视] | `action-design.md` 中逐段速度层次行 | A3, GAP-6, F-STORY-10 | — |
| R-SB-19 | 动作按真实事件时长排布（摔倒约 0.4–0.6s、转头约 0.5–0.8s、一步约 0.5s），剩余时间写给后果 / 反应 / 静场；没有"一个单动作占满整镜"的镜 | [目视] | action-design.md 中逐镜事件时长预算表 | A3, F-H3-23, S-H3-11 | — |
| R-SB-20 | 每场打斗至少一个镜内同框可见完整交手回合；出招与受击在同一次生成里；每次接触写全"接近 → 接触 → 施力 → 结果" | [目视] | action-design.md 中交手回合所在镜号 + 七相表 | A2, F-ZEN-13, F-STORY-12 | — |
| R-SB-21 | 纯色卡、字卡、精确文字、UI、logo 镜在分镜中标为本地生成（剪辑单 `local:`），未安排送 H3 | [目视] | 分镜中本地镜清单 | D2, D1 | — |
| R-SB-22 | 每镜能写出"这一镜改变了什么"（状态从 → 到）；写不出的镜已删或并入相邻镜 | [目视] | segments.md 中逐镜状态变化列 | A1, S-H3-10 | — |
| R-SB-23 | 已按分镜时长把关键帧（或占位图）排成 animatic，配临时对白与节拍标记，连续看一遍并记录"第一次困惑点"；困惑点已修或写明为何是设计 | [目视] | `animatic.mp4` + `review/storyboard/animatic-notes.md` | F1, A1, S-CASE-20 | — |
| R-SB-24 | 分镜与提示词逐镜对齐：时长（含尾部余量口径）、对白、起始帧方位三项一致 | [自动] | prompt_lint / dialogue_capacity / direction_audit 报告中无对账类 error | P7, M10 | scripts/prompt_lint.py（VP-sync）；scripts/dialogue_capacity.py（P7-*）；scripts/direction_audit.py（DIR-layout） |

## 常见误判

- **"均长达标"≠ 不碎。** R-SB-03 过了，但一个连续动作仍被切成两个镜号（R-SB-05 不过）——观众照样看到因果断裂。短剪不是罪，碎镜症是罪：生成单位必须承载完整动作链，快剪从长镜里取（evidence-reconciliation R6）。见 [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)。
- **因果句句式对 ≠ 运镜有动机。** `A4-cause` 只查"因为…所以…"句式；"因为要更有冲击力，所以推近"能过脚本、过不了 R-SB-09。见 [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)。
- **把打击拍算进拍数，然后为了 A5-beats-many 减拍。** 结果是把打斗砍薄——A2 与 A5 的修法互相打架。打击拍要密、空间拍要少（evidence-reconciliation R4）。见 [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)、[`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)。
- **对白容量报 error 就换 seed。** 容量不足是结构性缺陷，换 seed 无解（D3 实录：3 个 seed 各缺不同句）；改时长或改台词，在本清单里改。见 [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md)。
- **调小 `--margin` 让 D3-margin 消失。** 这是把检查改成迎合产出（F2 代理指标）；R-SB-16 专门禁止。
- **跳过 animatic 直接送视频。** 节奏与因果问题在 animatic 阶段修是分钟级，在视频阶段修是小时级 + 算力（production-lifecycle §4）。R-SB-23 是本阶段唯一能提前看到"观感"的检查。
