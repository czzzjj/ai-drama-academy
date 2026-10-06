# 锚点卡 · <剧名>

<!-- 产出路径：season-01/anchors.md（季级共用）或 season-01/epNN/anchors.md。技能：casting-and-canon（建卡）、asset-boards（板图）、multi-episode-arc（版本/变体）。
     契约：70-playbooks/format-contracts.md §3——prompt_lint.py --anchors 按此解析。每资产一个 `## ANCHOR: <ID>`；锚点句 EN 一行、反引号包裹、不换行。
     ID 前缀：CHR- 角色 / PRP- 道具 / LOC- 场景 / SYM- 符号。 -->

## ANCHOR: CHR-<NAME>
- 类型: 角色
- 锚点句 EN: `<一段英文：年龄、体型、发型发色、服装、标志物——所有提示词逐字嵌入>`
- 必现: <发色…；服装…；标志物…>
- 禁用: <no jewelry at all; no armor; ……>
- 方位属性: <左手持刀 / 左臂黑色——有则必填，画面方位需单独放大核验；无写 —>
- 来源依据: <原著第 x 章 "……">
- 板图: assets/boards/CHR-<NAME>-BOARD.png（seed <n> 定稿；落选 seed <…> 归档于 assets/boards/_rejected/）
- 音色: <参考音频路径 / 外配音色 ID>
- 版本: v1（<日期>）；变体: <CHR-<NAME>-V2 伤势/换装，起于 EPnn/SHOT-nnn，或 —>

## ANCHOR: SYM-<NAME>
- 类型: 符号
- 锚点句 EN: `<exactly one red ring crossed by exactly one vertical bar, top to bottom; fire-textured>`
- 必现: <形状、数量、方向、质感>
- 禁用: <no horizontal line, no cross sign, no plus sign, no second bar; not smooth neon, not a laser line>
- 方位属性: —
- 来源依据: <……>
- 板图: assets/boards/SYM-<NAME>-BOARD.png（seed <n> 定稿）

<!-- 规则：
1. 禁用先写正向可见状态（plain polished steel, smooth and unadorned），只对生成器已证实会加的物件追加 `no X` 并做 ≥3 seed A/B（evidence-reconciliation R1；R-BRD-12、R-BRD-13）。
2. 符号资产的禁用项穷举所有见过的错误变体（D4）。
3. 背景人群不建 CHR 卡（R-BRD-21）。
4. 主要角色两两在脸型/发型/体型上写出可区分特征（B3、R-SEA-12）。 -->
