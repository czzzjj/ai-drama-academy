# 视频提示词 · S<nn>E<nn>

<!-- 产出路径：season-01/epNN/video-prompts.md。技能：video-prompting-h3（主）、performance-direction（表演段 + 闭嘴句）、sound-design（声音段）。
     契约：70-playbooks/format-contracts.md §2——每镜 `## SHOT-nnn` + 元数据列表 + 一个 h3 代码块。同一镜同名键只认第一条；可选键不用时整行删掉（写"否/无"不是豁免）。
     校验：h3_frame_grid.py --check；prompt_lint.py --anchors anchors.md --storyboard storyboard.md；direction_audit.py --storyboard storyboard.md；slot_order_check.py --simulate-remove-placeholder；dialogue_capacity.py。
     选模式：起始帧 + 角色板 + 同场关键帧 → Ref2VA（六段）；只有首帧/尾帧（0–2 张图）→ FL2VA（三段 + 对齐句，references 写 —）。两种方言禁止混用。
     可选键（需要时加在元数据里）：`- 换边: 设计（理由…；起始帧支持证据…）`（须 轴线策略: 换边）；`- 慢动作: 设计选择（理由…）`。禁止写 negative_prompt。 -->

## SHOT-<nnn>
- 时长: <分镜时长(s) + 尾部余量，两位小数>
- 帧数: <17k+5 网格值，124–362，用 h3_frame_grid.py --seconds 换算>
- 模式: Ref2VA
- 尾部余量: 1.30
- 步数: 20
- first_frame: REF-SHOT<nnn>-START
- references: 1=CHR-<A>-BOARD; 2=CHR-<B>-BOARD; 3=REF-SHOT<前镜>-START
- 起始帧方位: <名A=LEFT; 名B=RIGHT>
- 轴线策略: 单轴定侧
- 锚点: CHR-<A>; CHR-<B>
- 角色映射: S1=<名A>; S2=<名B>

```h3
subject_definitions:
  [S1] the <身份> on the LEFT — <CHR-A 锚点句 EN 逐字> <Picture 1>
  [S2] the <身份> on the RIGHT — <CHR-B 锚点句 EN 逐字> <Picture 2>
  The two figures have clearly different faces, builds and silhouettes.
summary:
  <一句话：本镜动作链的事件与结果>
retention_analysis:
  <观众为什么继续看：本镜抛出或推进的具体问题>
detailed_description:
  Real-time speed throughout, no slow motion. <动作链逐相写成事件；一个主运镜（高度或距离）及其触发事件，如 the frame jolts as the blade hits the stone>
  [S1] shouts: <d>[Chinese] <台词，逐字等于分镜 对白></d>
  [S2] does not speak; his lips remain completely closed.
overall_soundscape:
  <≤3 个声源：环境床 + 画面内可见动作的拟音>
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```

## SHOT-<nnn>
- 时长: <分镜时长(s) + 尾部余量>
- 帧数: <17k+5 网格值>
- 模式: FL2VA
- 尾部余量: 1.30
- 步数: 20
- first_frame: REF-SHOT<nnn>-START
- references: —
- 起始帧方位: <名=CENTER>
- 轴线策略: 单轴定侧
- 锚点: <CHR-<A> 或 —>
- 角色映射: S1=<名>

```h3
How the reference pictures align with the target video — the first frame is the opening image of the shot at 0.00s; there is no last frame.

integrated_multimodal_description:
  [S1] the <身份> in the center: <锚点句 EN 逐字>.
  Real-time speed throughout, no slow motion. <事件链 + 一个主运镜>
  [S1] says quietly: <d>[Chinese] <台词></d>
  <正向状态句；已证实会被加的物件写 no X>
overall_soundscape:
  <≤3 个声源>
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```
