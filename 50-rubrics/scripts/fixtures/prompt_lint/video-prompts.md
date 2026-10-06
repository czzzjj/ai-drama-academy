# 视频提示词（fixture · prompt_lint 专用）

> SHOT-020：符号禁用项缺 2 条（VP-symbol）、negative_prompt（VP-negative）、spotlight（VP-light）、人群无虚化（VP-crowd）、
> <Picture> 首次引用顺序 1,3,2（VP-picture）、对白缺 [Chinese] 与未闭合（VP-dialogue）；慢动作已在元数据声明（不报 A3 error）。
> SHOT-021：同一场景的干净写法，期望 0 error 0 warn。
> SHOT-022：声明慢动作却仍写实时速度句（VP-realtime warn）。

## SHOT-020
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT020-START
- references: 1=CHR-SUXIAO-BOARD; 2=REF-SHOT019-START; 3=SYM-FMARK-BOARD
- 起始帧方位: 苏晓=CENTER
- 轴线策略: 单轴定侧
- 锚点: CHR-SUXIAO; SYM-FMARK
- 角色映射: S1=苏晓
- 慢动作: 设计选择（印记显形是全集唯一的慢镜，给观众 2 秒读清符号）
- negative_prompt: blurry, extra fingers

```h3
subject_definitions:
  [S1] the swordswoman in the center: a slender 17-year-old Chinese swordswoman with a high black ponytail tied with a plain red cord, sharp dark eyes, wearing a fitted dark-teal cross-collar tunic with leather bracers, holding a single-edged straight Chinese dao in her right hand <Picture 1>
  The mark on her blade: exactly one red ring crossed by exactly one vertical bar, top to bottom, fire-textured <Picture 3>
summary:
  In the same village square as <Picture 2>, the mark ignites on her blade in slow motion while villagers watch.
retention_analysis:
  The mark is the episode's open question; it is readable within two seconds.
detailed_description:
  [S1] raises the dao; a spotlight falls on the blade.
  The mark burns in: no horizontal line, no cross sign, not smooth neon, not a laser line.
  [S1] whispers: <d>原来是你</d>
  [S1] gasps: <d>[Chinese] 这是……
overall_soundscape:
  Low crackle of fire on metal, murmuring villagers.
non_diegetic_music:
  A single low drone.
No captions, subtitles, or dialogue text overlays appear at any moment.
```

## SHOT-021
- 时长: 10.83
- 帧数: 260
- first_frame: REF-SHOT021-START
- references: 1=CHR-SUXIAO-BOARD; 2=REF-SHOT020-START
- 起始帧方位: 苏晓=CENTER
- 轴线策略: 单轴定侧
- 锚点: CHR-SUXIAO; SYM-FMARK
- 角色映射: S1=苏晓

```h3
subject_definitions:
  [S1] the swordswoman in the center: a slender 17-year-old Chinese swordswoman with a high black ponytail tied with a plain red cord, sharp dark eyes, wearing a fitted dark-teal cross-collar tunic with leather bracers, holding a single-edged straight Chinese dao in her right hand <Picture 1>
  The mark on her blade: exactly one red ring crossed by exactly one vertical bar, top to bottom, fire-textured
summary:
  In the same village square as <Picture 2>, she lowers the glowing blade and walks away.
retention_analysis:
  The fading mark leaves the question open for the next episode.
detailed_description:
  Real-time speed throughout, no slow motion.
  [S1] sheathes the dao in one motion and says: <d>[Chinese] 走吧。</d>
  The mark fades: no horizontal line, no cross sign, no plus sign, no second bar, not smooth neon, not a laser line.
  Far behind her, the villagers are heavily blurred, out-of-focus dark silhouettes with no distinct faces.
  Only warm ambient light falls on her face; no flashlight, no torch beam, no spotlight, no light beams.
  No jewelry at all, no armor, no gemstone on the sword guard, no double-edged blade.
overall_soundscape:
  Wind through the square, a distant murmur.
non_diegetic_music:
  None.
No captions, subtitles, or dialogue text overlays appear at any moment.
```

## SHOT-022
- 时长: 8.00
- 帧数: 192
- first_frame: REF-SHOT022-START
- references: 1=CHR-SUXIAO-BOARD
- 起始帧方位: 苏晓=CENTER
- 轴线策略: 单轴定侧
- 锚点: —
- 慢动作: 设计选择（落刀瞬间 1 秒升格）

```h3
subject_definitions:
  [S1] the swordswoman in the center <Picture 1>
summary:
  She drives her blade into the stone floor once.
retention_analysis:
  The impact ends the sequence on a hard accent.
detailed_description:
  Real-time speed throughout, no slow motion.
  [S1] strikes the stone floor with the dao; sparks scatter outward from the contact point.
overall_soundscape:
  A single metallic clang, falling grit.
non_diegetic_music:
  None.
No captions, subtitles, or dialogue text overlays appear at any moment.
```
