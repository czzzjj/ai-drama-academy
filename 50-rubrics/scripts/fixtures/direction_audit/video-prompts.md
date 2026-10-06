# 视频提示词（fixture · direction_audit 专用）

> SHOT-010：[S1] 声明在 LEFT 但起始帧 苏晓=RIGHT（DIR-side error）；否定句 never trucks/arcs/orbits（info）；
>           circles behind / 绕到身后（DIR-path warn）；right hand（角色自身左右）与台词里的"右"（需目视）。
> SHOT-011：轴线策略=换边且写了 换边 理由 → arcs around 降为需目视，0 error。
> SHOT-012：两人同框却缺 角色映射（DIR-mapping error）；分镜起始帧方位与提示词左右对调（DIR-layout error）。

## SHOT-010
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT010-START
- references: 1=CHR-SUXIAO-BOARD; 2=CHR-STONEGOD-BOARD
- 起始帧方位: 石神=LEFT; 苏晓=RIGHT
- 轴线策略: 单轴定侧
- 锚点: —
- 角色映射: S1=苏晓; S2=石神

```h3
subject_definitions:
  [S1] the swordswoman on the LEFT: a slender swordswoman holding a dao in her right hand <Picture 1>
  [S2] the stone god on the LEFT: a towering stone god of cracked grey granite <Picture 2>
  The two figures are clearly distinct: one small human woman, one giant stone being.
summary:
  The swordswoman on the RIGHT circles behind the stone god.
retention_analysis:
  The reversal of positions sets up the next exchange.
detailed_description:
  Real-time speed throughout, no slow motion.
  The camera never trucks, arcs or orbits; it only pushes in toward the contact point.
  [S1] turns her head and shouts: <d>[Chinese] 我在你右边！</d>
  她绕到身后。
overall_soundscape:
  Wind, gravel under boots.
non_diegetic_music:
  None.
No captions, subtitles, or dialogue text overlays appear at any moment.
```

## SHOT-011
- 时长: 10.83
- 帧数: 260
- first_frame: REF-SHOT011-START
- references: 1=CHR-SUXIAO-BOARD; 2=CHR-STONEGOD-BOARD
- 起始帧方位: 石神=LEFT; 苏晓=RIGHT
- 轴线策略: 换边
- 换边: 设计（理由：主客易位，苏晓第一次压制石神；起始帧支持证据：REF-SHOT011-START 为已验收的越肩反打）
- 锚点: —
- 角色映射: S1=苏晓; S2=石神

```h3
subject_definitions:
  [S1] the swordswoman on the RIGHT: a slender swordswoman <Picture 1>
  [S2] the stone god on the LEFT: a towering stone god of cracked grey granite <Picture 2>
  The two figures are clearly distinct: one small human woman, one giant stone being.
summary:
  The camera arcs around the stone god while the swordswoman presses forward.
retention_analysis:
  The first time she dominates the frame.
detailed_description:
  Real-time speed throughout, no slow motion.
  The camera arcs around the stone god until the swordswoman is framed over its shoulder.
overall_soundscape:
  Stone grinding, her breath.
non_diegetic_music:
  Rising taiko.
No captions, subtitles, or dialogue text overlays appear at any moment.
```

## SHOT-012
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT012-START
- references: 1=CHR-SUXIAO-BOARD; 2=CHR-SHANGYUE-BOARD
- 起始帧方位: 殇月=LEFT; 苏晓=RIGHT
- 轴线策略: 单轴定侧
- 锚点: —

```h3
subject_definitions:
  [S1] the girl on the RIGHT <Picture 1>
  [S2] the woman in white on the LEFT <Picture 2>
  The two women are clearly distinct: different faces, hair and builds.
summary:
  [S2] speaks while [S1] listens without moving.
retention_analysis:
  The vow is the episode's promise.
detailed_description:
  Real-time speed throughout, no slow motion.
  Static framing; slow push-in only.
overall_soundscape:
  Lake water lapping.
non_diegetic_music:
  None.
No captions, subtitles, or dialogue text overlays appear at any moment.
```
