# 视频提示词清单（R-VP）

> **阶段**：2 制作·视频提示词（`video-prompts.md`，送 MiniMax H3 之前）。服务维度：Q2–Q8（[`50-rubrics/quality-model.md`](../quality-model.md)）。
> **何时跑**：每镜进入 prepare 之前；改任何一镜的提示词、references 或导出绑定后，对**全集**重跑（防止新补丁句在别的镜引入矛盾，A5④）。执行技能：[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)。
> **通过规则**：`h3_frame_grid.py --check`、`prompt_lint.py`、`direction_audit.py`、`slot_order_check.py --simulate-remove-placeholder`、`dialogue_capacity.py --storyboard --prompts` 全部 0 error（命令见 [`50-rubrics/README.md`](../README.md) §5 步骤 4–8），`direction_audit` 末行为「方位词审计：通过（0 处矛盾）」；每条 warn 有处置记录；每条 `[目视]` 条目证据存在。任何一项不过 → 不得进 prepare（三步闸门 P6）。
> 格式以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §2 为准；冲突立场以 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1–R5 为准。

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-VP-01 | 每镜声明 `- 模式: Ref2VA` 或 `FL2VA`，方言与模式一致（Ref2VA 六段、FL2VA 三段 + 首行对齐句），段名顶格、顺序固定、不混用；FL2VA 镜不写 `references` | [自动] | `qc/prompt_lint.json` 无 VP-mode / VP-struct | T-2, S-H3-01, F-H3-02, F-H3-03, F-ZEN-02 | scripts/prompt_lint.py（VP-mode, VP-struct） |
| R-VP-02 | h3 代码块最后一个非空行恰为 `No captions, subtitles, or dialogue text overlays appear at any moment.` | [自动] | prompt_lint 报告无 VP-ban | D1, M8, S-H3-13 | scripts/prompt_lint.py（VP-ban） |
| R-VP-03 | 动作镜含 `Real-time speed throughout, no slow motion`，且全文无非否定的 slow motion / slowmo；唯一豁免是元数据 `- 慢动作: 设计选择（理由…）`，豁免镜不再同时写实时速度句 | [自动] | prompt_lint 报告无 VP-realtime | A3, F-H3-23, S-VGEN-19 | scripts/prompt_lint.py（VP-realtime） |
| R-VP-04 | 提示词中不存在与起始帧方位矛盾的换边运镜词 | [自动]+[目视] | direction_audit 报告 + 起始帧方位声明 | A5, M4 | scripts/direction_audit.py（DIR-camera） |
| R-VP-05 | 附着在主体上的 LEFT/RIGHT 经 `角色映射` 与 `起始帧方位` 全部一致；≥2 人的镜写了 `角色映射`；提示词与分镜的 `起始帧方位` 相同 | [自动] | direction_audit 报告无 DIR-side / DIR-mapping / DIR-layout error | A5, P7, C1-6 | scripts/direction_audit.py（DIR-side, DIR-mapping, DIR-layout） |
| R-VP-06 | 每条 DIR-path warn 有处置（改同侧直线进退 / 拆镜 / `- 换边:` 理由 + 起始帧支持证据）；每条 DIR-check visual 已对照起始帧看过 | [自动]+[目视] | `qc/direction_audit.json` + 逐条处置记录 | A5, M4 | scripts/direction_audit.py（DIR-path, DIR-check） |
| R-VP-07 | 起始帧方位 ≥2 人时，每个 `[S#]` 定义含画面位置称呼（`the god on the LEFT`） | [自动] | prompt_lint 报告无 VP-position | A5, M4 | scripts/prompt_lint.py（VP-position） |
| R-VP-08 | 画面 ≥2 个人物的镜含差异化描述句（脸 / 发型 / 体型逐项不同，如 `three clearly distinct men with different faces, hair and builds`） | [自动] | prompt_lint 报告无 VP-distinct | B3, S-PLAT-07, F-H3-22 | scripts/prompt_lint.py（VP-distinct） |
| R-VP-09 | `- 锚点:` 中每个资产的锚点句 EN 逐字出现在 `subject_definitions`（FL2VA 为 `integrated_multimodal_description`） | [自动] | prompt_lint（带 `--anchors`）无 VP-anchor error | P1, B1, F-ZEN-23 | scripts/prompt_lint.py（VP-anchor） |
| R-VP-10 | 每个要锁定的外观先写成正向可见状态句（`the sword guard is plain polished steel, smooth and unadorned`）；绝对否定句只追加在生成器已被证实会自加的物件之后；不存在"只有否定句、没有正向状态句"的锁定项 | [目视]+[自动] | 每镜锁定项对照表（正向句 / 否定句）；prompt_lint 的 VP-anchor info 行（禁用项未写进提示词）已逐条处置 | C1, S-COMFY-08, F-H3-08, S-H3-09 | scripts/prompt_lint.py（VP-anchor info） |
| R-VP-11 | 提示词与工作流中不出现 `negative_prompt` | [自动] | prompt_lint 报告无 VP-negative | C1, T-2, S-COMFY-05 | scripts/prompt_lint.py（VP-negative） |
| R-VP-12 | 含符号锚点（SYM-*）的镜，把锚点卡 `禁用` 中列出的每个错误变体逐条写进提示词（`exactly one vertical bar … no horizontal line, no cross sign`），质感同理（`fire-textured, not smooth neon, not a laser line`） | [自动] | prompt_lint 报告无 VP-symbol | D4 | scripts/prompt_lint.py（VP-symbol） |
| R-VP-13 | 不要求生成器出纯色画面、字卡、精确文字、logo、UI 面板或字幕 | [自动] | prompt_lint 报告无 VP-generator-unsafe | D2, D1, M8 | scripts/prompt_lint.py（VP-generator-unsafe） |
| R-VP-14 | 镜内不应出现的物件名一个都没写（"提到即生长"）；光写成"打在脸上的环境光 / 从一侧来的暖光"，不写 flashlight / spotlight / light beam / god rays 等具象光源；共用段只放每一镜都成立的元素 | [自动]+[目视] | prompt_lint 无 VP-light；共用段逐句核对记录 | B3, S-H3-09, F-H3-22 | scripts/prompt_lint.py（VP-light） |
| R-VP-15 | 含人群词的镜写了虚化（大虚化、无独立可辨脸的暗形块），且没给人群独立特征或道具 | [自动] | prompt_lint 报告无 VP-crowd | B2 | scripts/prompt_lint.py（VP-crowd） |
| R-VP-16 | 不含未拆解的评价形容词（epic / spectacular / cinematic / stunning 等）；特效写成 来源 → 接触 → 扩散 → 后果 | [自动]+[目视] | prompt_lint 报告无 VP-adjective；特效句逐条对照 | M3, G5 | scripts/prompt_lint.py（VP-adjective） |
| R-VP-17 | 每句对白写作 `<d>[Chinese] 台词</d>`、同一行闭合、同一行前文有稳定说话人 ID（`[S1]`），说话人在 subject_definitions 或 `角色映射` 中定义 | [自动] | prompt_lint 报告无 VP-dialogue | T-2, P7 | scripts/prompt_lint.py（VP-dialogue） |
| R-VP-18 | ≥2 个主体且有对白的镜，为每个不说话且脸可见的人写了 `[S2] does not speak; his lips remain completely closed.`（或其出画 / 背身） | [自动] | prompt_lint 报告无 VP-lipsync | F-ZEN-08, S-ZEN-17 | scripts/prompt_lint.py（VP-lipsync） |
| R-VP-19 | `non_diegetic_music:` 非空；无配乐的镜显式写 `N/A` | [自动] | prompt_lint 报告无 VP-music | F-ZEN-07, S-H3-11 | scripts/prompt_lint.py（VP-music） |
| R-VP-20 | `references` 编号从 1 起唯一连续，`<Picture N>` 首次引用顺序升序且都已定义；占位槽在末位，删除占位后仍连续；`first_frame` 是本镜 `REF-SHOTnnn-START` | [自动] | prompt_lint 无 VP-picture；slot_order_check 无 SLOT-* error | E1, T-2, T-3 | scripts/prompt_lint.py（VP-picture）；scripts/slot_order_check.py（SLOT-contiguous, SLOT-placeholder-pos, SLOT-sim） |
| R-VP-21 | `帧数` 落在 17k+5 网格（124–362），且与 `时长` 一致 | [自动] | h3_frame_grid --check 无 T2-* error | T-2, F-H3-06 | scripts/h3_frame_grid.py（T2-frames-offgrid, T2-frames-below-min, T2-frames-above-max, T2-duration-mismatch） |
| R-VP-22 | 每镜声明 `- 尾部余量: 1.3`–`1.5`，提示词 `时长` = 分镜 `时长(s)` + 尾部余量；台词在"时长 − 余量"内装得下 | [自动] | prompt_lint 无 VP-sync；dialogue_capacity（带 `--prompts`）无 D3-* error | P8, F-H3-18, P7 | scripts/prompt_lint.py（VP-sync）；scripts/dialogue_capacity.py（D3-capacity） |
| R-VP-23 | 定稿镜 `- 步数:` 为 20（未写按工作流默认 20），未挂 4-step turbo LoRA；≤ 8 步的镜只用于预览抽卡且已标注"预览" | [自动]+[目视] | prompt_lint 无 VP-steps；工作流 JSON 快照中 steps 与 LoRA 列表 | T-2, F-H3-09, F-H3-10, A4 | scripts/prompt_lint.py（VP-steps） |
| R-VP-24 | 每镜只有一个主运镜指令（高度或距离维度）；顿挫 / 震动写成事件引起的相机响应（`the frame jolts as the blade hits the stone`）；不靠 `with small amplitude` 控制幅度；需要明显运镜的镜不含首帧脚手架句 | [目视]+[自动] | 逐镜运镜句标注；prompt_lint 的 VP-scaffold info 已逐条判断"保留（钉轴线）/ 删除（要运镜）" | A4, A5, S-H3-10, F-H3-11, F-H3-12 | scripts/prompt_lint.py（VP-scaffold） |
| R-VP-25 | 已验收产出与提示词描述同一事实：任何与提示词不一致但被采用的产出，提示词已回写为产出的事实，再作为后续参考图 | [目视] | 回写 diff + 对应 `qc/<SHOT>.md` 结论 | E4 | — |

## 常见误判

- **prompt_lint 0 error = 提示词好。** 它只证明"没犯已知的格式与禁令错误"。运镜有没有动机、事件写没写全，都在 `[目视]` 条目里（R-VP-10、R-VP-16、R-VP-24）。见 [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)。
- **用方位词"说服"模型换边。** 起始帧钉死轴线，文字改不动；多写方位词只会制造更多矛盾。要换边就换起始帧或拆镜（R-VP-04/05/06）。见 [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)。
- **只写否定句、或者反过来全删否定句。** 学院立场（R1）：先正向状态句锁外观，只对已被证实会自加的物件追加绝对否定句，并用 ≥3 seed 比对否定句有没有把东西招进来。`No captions…` 末行保留（D1 实证有效），但它是兜底不是保证——烧录文字永远由抽帧核验把关。见 [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)、[`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md)。
- **写了 negative_prompt 就算处理过禁用项。** cfg=1.0 时无条件分支被跳过，negative 无效，还制造"已处理"的错觉（R-VP-11）。
- **"不说话的人"不用管。** 多人对白镜不写闭嘴句，口型会落到错的人身上（R-VP-18）；这类错误到转写对账才暴露，成本已翻倍。
- **用 turbo 出定稿。** 4-step 几乎压掉运镜、削弱参考与语音；"没有运镜"的反馈可能根本不是提示词问题（R-VP-23）。见 [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)。
- **补丁句越加越多。** 每轮返工往提示词里加一句，旧句不删，指令开始打架（A5④：模型执行你写的**所有**指令）。改写提示词时附改写前后对照，删除被新设计取代的旧句；全集重跑本清单。见 [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)。
