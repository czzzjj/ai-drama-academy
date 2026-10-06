# 视觉设定 · S<nn>E<nn>

<!-- 产出路径：season-01/epNN/visual-bible.md。技能：visual-bible；下游 keyframe-freeze 逐字取用风格锁句与命名色。闸门：R-COL-01–R-COL-08。 -->

## 1. 风格卡与风格锁句
- 风格卡: 30-taste/style-cards/<style>.md
- 风格锁句 EN（逐字进每张关键帧冻结提示词第 1 行）: `<one English sentence: medium, palette logic, lens feel, texture>`

## 2. 色彩脚本（每 SEQ 一行）
| 段号 | 情绪 | 主色相 | 饱和 | 明度 | 光比档 | 色温 | 命名色（3–5） |
|---|---|---|---|---|---|---|---|
| SEQ-01 | <压抑、危险> | <青灰> | 高/中/低 | 高/中/低 | <低调 8:1> | <冷 5600K 月光> | <ash grey, moss green, bone white> |
| SEQ-02 | <……> | <……> | <…> | <…> | <…> | <…> | <……> |
<!-- 情绪不同的相邻两段至少在一项上明显不同（R-COL-03）；命名色逐字写进该段每个关键帧（R-COL-02）。 -->

## 3. 光态表（每 LOC 一行）
| 场景 ID | 动机光源 | 画面内位置 | 光向 | 色温 | 随剧情的变化点 |
|---|---|---|---|---|---|
| LOC-<NAME> | <窗/门/灯/屏/火/月/车灯> | <画面上方左侧> | LEFT / RIGHT / TOP / BG | <K 值/冷暖> | <SHOT-nnn 起火光熄灭> |
<!-- 光只写被动描述（cold light falls from the upper LEFT），不写光柱或具体光源物件进视频提示词（B3、C1）。 -->

## 4. 规格表
| 用途 | 尺寸 | 比例 | 规则 |
|---|---|---|---|
| 板图 | 1696×2528 | 2:3 | 只做资产母版，不直接送 first_frame |
| 关键帧（送 first_frame） | 1536×2752 | 9:16 | 或送入前显式裁成 9:16 并记录裁切（R-KF-02） |
| H3 中间稿 | 768×1344 | ≈9:16 | 只做中间稿 |
| 交付 | 1080×1920 | 9:16 | loudness_verify.py 偏离 >1% 即 error |
