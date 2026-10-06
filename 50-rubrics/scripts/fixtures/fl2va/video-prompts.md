# 视频提示词（fixture · fl2va：首/尾帧模式的三段方言，期望 0 error 0 warn）

> FL2VA = MiniMaxH3ImageToVideo（只有首帧/尾帧，0–2 张图，不写 references）；三段：integrated_multimodal_description /
> overall_soundscape / non_diegetic_music，首行为官方对齐句（F-H3-02）。本镜声明尾部余量 1.30s：提示词时长 8.00 = 分镜 6.70 + 1.30。

## SHOT-030
- 时长: 8.00
- 帧数: 192
- 模式: FL2VA
- 尾部余量: 1.30
- first_frame: REF-SHOT030-START
- references: —
- 起始帧方位: 苏晓=CENTER
- 轴线策略: 单轴定侧
- 锚点: —
- 角色映射: S1=苏晓

```h3
How the reference pictures align with the target video — the first frame is the opening image of the shot at 0.00s; there is no last frame.

integrated_multimodal_description:
  [S1] the swordswoman in the center: a slender 17-year-old Chinese swordswoman with a high black ponytail tied with a plain red cord, wearing a fitted dark-teal cross-collar tunic with leather bracers.
  She stands still at the edge of the forest clearing, lowers her dao and looks toward the dark trees. The camera pushes in with small amplitude at slow speed toward her face.
  [S1] says quietly: <d>[Chinese] 走吧。</d>
  No jewelry at all, no armor.
overall_soundscape:
  Wind in the leaves, a distant bird call, her slow breath.
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```
