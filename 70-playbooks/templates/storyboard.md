# 分镜 · S<nn>E<nn>

<!-- 产出路径：season-01/epNN/storyboard.md。技能：storyboard-long-take（主）、action-choreography（回填 内容 动作链）、performance-direction（表演卡）。
     契约：70-playbooks/format-contracts.md §1——表头逐字不改，列顺序可变，多余列忽略，单元格内 | 写成 \|，空值写 —。
     校验：segment_rhythm.py storyboard.md；dialogue_capacity.py --storyboard storyboard.md --prompts video-prompts.md；direction_audit.py video-prompts.md --storyboard storyboard.md。 -->

## 段结构
| 段号 | 动作链/戏剧单元（一句话） | 速度层次 | 段长(s) |
|---|---|---|---|
| SEQ-01 | <谁 → 做什么 → 结果> | <快 → 慢 → 爆 → 静> | <8–15> |

## 分镜表
| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |
|---|---|---|---|---|---|---|---|---|---|
| SEQ-01 | SHOT-001 | <≥5.17，两位小数> | <2–3> | <事件 → 事件 → 事件> | <一个主运动：缓推/上摇/拉回/静止> | 因为<画面内可见事件>，所以镜头<动作> | <名=LEFT; 名=RIGHT> | <说话人：台词 / 说话人：台词> | — |
| SEQ-01 | SHOT-002 | <时长> | <n> | <……> | <……> | 因为<……>，所以不动 | <名=CENTER> | — | — |
<!-- 规则（逐条对应 R-SB）：
- 送 H3 的镜 ≥5.17s（124 帧）、≤15.08s（362 帧）；<5.17s 必填 短镜理由 且该镜本地生成不送 H3（R-SB-01、R-SB-02）。
- 拍数 只计空间拍+表情拍，≤3；打击拍写进 内容 的动作链（R-SB-06、R-SB-07，evidence-reconciliation R4）。
- 运镜 只写高度或距离维度，禁止 truck/arc/orbit/weave 等左右维度（R-SB-10、R-SB-12）。
- 起始帧方位 用大写 LEFT/RIGHT/CENTER/FG/BG；同场相邻镜左右顺序不反转（R-SB-11、R-SB-13）。
- 对白 按规划语速 ≈4.1 字/秒 + 开口延迟 + 留白排时长；7.5 字/秒是硬上限（R-SB-14、R-SB-15）。
- 纯色卡、字卡、精确文字、UI、logo 镜不送生成器（R-SB-21）。 -->

## 表演卡（有表演的镜逐镜一节）
### 表演卡 SHOT-<nnn>
- 任务动词: <逼问 / 试探 / 隐瞒……>（不写裸情绪词 sad/angry，R-PRF-01）
- 表情拍: <从 压住 → 泄露>（眉 → 眼 → 嘴；≤2–3 拍，R-PRF-02–R-PRF-04）
- 视线目标: <看谁/看什么>
- 不准动的部位: <嘴角保持不动>
- 非说话人: <[S2] 闭嘴 / 背身 / 出画>（R-PRF-05）
