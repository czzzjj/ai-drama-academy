---
name: visual-bible
description: 为一季/一集定视觉设定：从 30-taste/style-cards 选一张风格卡并写风格锁句，按段（SEQ）写色彩脚本（主色相/饱和/明度/光比/色温 + 3–5 个命名色），为每个场景定光态（动机光源、方向、色温、光比档），并锁定关键帧规格 9:16 1536×2752。Use when starting pre-production, choosing a look, planning color per beat, or when shots feel "flat / same everywhere / lighting jumps". 触发词：视觉设定、风格卡、风格选择、色彩剧本、色彩脚本、光态、光比、主光方向、命名色、关键帧尺寸、visual bible, style card, color script, lighting state, motivated light, 9:16 keyframe. 不负责单张关键帧的抽卡验收（→ keyframe-freeze）、角色外观锚点（→ casting-and-canon）、后期调色执行（→ edit-and-assemble）。
---
# 视觉设定（visual-bible）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。规格立场见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第三部分。

## 何时用 / 何时不用
- **必须用**：季开机前（选风格卡、季级色彩弧）；每集分镜前（按段写色彩脚本）；新场景首次出现前（光态）；审片出现"全片一个颜色 / 光向跳 / 看不清脸"时。
- **不用**：单镜关键帧构图细节（→ [`keyframe-freeze`](../keyframe-freeze/SKILL.md)）；成片 LUT 统一（→ `edit-and-assemble`，但它必须读本技能的色彩脚本）。
- 判决：委托方从未做过色彩设计〔委托方实证·GAP-4〕；画面级属性（史诗感、方向、构图、灯光）由起始帧决定，提示词救不了〔委托方实证·M2〕——所以视觉设定必须在关键帧之前写死。

## 输入 → 输出
- 输入：`season-bible.md`（题材、季级情绪弧）、`script.md`（每场开场 → 收场状态）、分镜段号草案、风格库 [`30-taste/style-cards/`](../../30-taste/style-cards/)。
- 输出：`season-01/ep03/visual-bible.md`（模板 [`70-playbooks/templates/visual-bible.md`](../../70-playbooks/templates/visual-bible.md)），四节：
  1. **风格卡与风格锁句**：选定卡名 + 一句英文风格锁句（逐字进每张关键帧冻结提示词）。
  2. **色彩脚本表**（每 SEQ 一行）：

```markdown
| 段号 | 情绪 | 主色相 | 饱和 | 明度 | 光比档 | 色温 | 命名色（3–5） |
|---|---|---|---|---|---|---|---|
| SEQ-01 | 压抑、危险 | 青灰 | 低 | 低 | 低调 8:1 | 冷 5600K 月光 | ash grey, moss green, bone white |
| SEQ-02 | 爆发 | 橙红 | 高 | 中 | 低调 8:1 | 暖 火光 | ember orange, soot black, blood red, ash grey |
| SEQ-03 | 余波 | 青蓝 | 中 | 中 | 中调 4:1 | 冷暖交界 | dusk blue, ember orange, bone white |
```

  3. **光态表**（每 LOC 一行）：动机光源（窗/门/灯/屏/火/月/车灯）、画面内位置、光向（画面坐标 LEFT/RIGHT/TOP/BG）、色温、随剧情的变化点。
  4. **规格表**：板图 2:3 1696×2528 可用；**关键帧（送 first_frame）一律 9:16 1536×2752**，或送入前显式裁成 9:16 并记录裁切；交付 1080×1920。

## 步骤
1. **选风格卡**：读 [`30-taste/style-cards/`](../../30-taste/style-cards/) 七张卡（cinematic-realism、dark-fantasy-epic、guoman-2d、motion-comic-2d、stylized-3d、ink-wash、chibi）的"适用题材 / 不适用""运动特性""失败模式"三节，按题材和本季最高频镜型（打斗 / 对白 / 表情特写）选**一张**主卡；禁止混用两张卡的关键词包。卡内〔学院推断〕词包首次使用前按卡末"验证"跑一次 A/B（同镜 ≥3 seed）。
2. **写风格锁句**：从风格卡"风格锁句模板"填一句英文，只写媒介/笔触/材质/镜头质感，不写主体、动作、光向；登记后全季逐字不变。禁止 `masterpiece, best quality, 8k` 一类质量咒语（无可见内容，只占注意力）〔学院推断：用 3 seed 有/无咒语 A/B 验证差异不可见〕。
3. **季级色彩弧**：在季圣经写一条季级色彩弧（如"冷灰 → 暖橙 → 黑金"），每集色彩脚本必须能在弧上定位（R-COL-01）。
4. **按段写色彩脚本**：每个 SEQ 一格，写主色相、饱和（高/中/低）、明度（高/中/低）、光比档、色温（R-COL-01）。情绪不同的相邻两段至少一项不同；全集各格完全相同（全片一套青橙）判不通过（R-COL-03）。
5. **光比档与情绪对应**：紧张/危险段低调约 8:1，轻松段高调约 1:1（R-COL-06）〔外部调研·S-CRAFT-15〕；低调段必须同时满足"缩到 270 宽脸和表情仍可辨"（R-COL-08，学院推断，冷观众断点验证）。
6. **命名 3–5 个颜色**：每格用英文颜色名（`ash grey, ember orange, bruise purple`），并交给 [`keyframe-freeze`](../keyframe-freeze/SKILL.md) **逐字**写进该段每张冻结提示词（R-COL-02）。验：`grep -F "ash grey" season-01/ep03/keyframe-prompts.md` 命中段内全部关键帧。
7. **定光态（动机光）**：每个场景指定画面内或可推断的主光源、方向、色温；光写成**被动描述**（`warm light falls from the LEFT across her cheek`），**禁止**写灯具名（`lit by a floor lamp`）——提到什么就长什么，灯具会出现在画面甚至变光柱〔外部调研·S-H3-09〕（R-COL-04）。场景板验收记录要标出实景光源位置、光向、色温（R-BRD-18）。
8. **跨镜光向锁**：同场全部关键帧主光方向一致并与场景板标注一致（R-COL-05）；跨集重复出现的场景光向与色温不变，除非剧情登记了变化（R-SEA-16）。
9. **规格锁**：把规格表写进视觉设定并通知下游——ComfyUI `MiniMaxH3ImageToVideo` 对 first_frame 不保比例直接拉伸〔外部调研·S-H3-03〕，2:3 图送 9:16 画布会被横向挤压约 16%〔学院推断·待核：用带正圆的测试图跑一次〕；Qwen-Image-2.1 官方 9:16 尺寸为 1536×2752〔外部调研·S-COMFY-01〕。验：R-KF-02。
10. **许可提示**：Qwen-Image-2.1 为 Qwen Research License（仅研究/评估）〔外部调研·S-COMFY-01、S-COMFY-02〕；若本季要变现，在视觉设定首行写"板图/关键帧生成模型许可：待人类确认（R-PUB-11）"，不得默认可商用。
11. **交接与复核**：色彩脚本交 [`storyboard-long-take`](../storyboard-long-take/SKILL.md)（段号对齐）、[`asset-boards`](../asset-boards/SKILL.md)（场景板光源标注）、[`keyframe-freeze`](../keyframe-freeze/SKILL.md)（命名色 + 光句）、`edit-and-assemble`（同场相邻 CUT 肤色/白平衡不跳，R-COL-07）。

## 判据
- 色彩与光：R-COL-01、R-COL-02、R-COL-03、R-COL-04、R-COL-05、R-COL-06、R-COL-07、R-COL-08。
- 规格与资产：R-KF-02、R-KF-13、R-BRD-18、R-SEA-16、R-PUB-11。
- 审美判据卡：关键帧阶段 TJ-01、TJ-04、TJ-12（见 [`30-taste/judgment-cards.md`](../../30-taste/judgment-cards.md)）。
- Q 维度：Q5 美术与密度（主）、Q7 一致性与连续性、Q1（情绪可读）。

## 失败模式
- **灯具 / 光柱被生成进画面，或同框人物被同一灯光"复制"** → [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)：防线 = 步骤 7 光写成被动描述，不点名灯具。
- **远山、光柱等装饰被自动添加** → [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)：防线 = 场景光态只写方向与色温；场景卡禁用项由 casting-and-canon 写。
- **同场光向跳、人物左右也跟着乱** → [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)：防线 = 步骤 8 光向锁写进场景板与冻结提示词。
- **跨镜脸色/色温跳变被读成换人** → [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md)：防线 = 步骤 8 + R-COL-07 后期统一。
- **只看技术参数（LUT 已套）就认为有色彩设计** → [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)：防线 = 步骤 4 逐段色彩脚本，R-COL-03 禁全片同一套。

## 关联
- 理论：[`10-theory/12-color-and-light.md`](../../10-theory/12-color-and-light.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/01-vertical-drama-physiology.md`](../../10-theory/01-vertical-drama-physiology.md)。
- 风格库：[`30-taste/README.md`](../../30-taste/README.md)、[`30-taste/style-cards/dark-fantasy-epic.md`](../../30-taste/style-cards/dark-fantasy-epic.md)（BOSS/神战类首选核对）。
- 相邻技能：[`casting-and-canon`](../casting-and-canon/SKILL.md)、[`asset-boards`](../asset-boards/SKILL.md)、[`keyframe-freeze`](../keyframe-freeze/SKILL.md)、`edit-and-assemble`、[`production-director`](../production-director/SKILL.md)。
- 找错题：DR-06（漂移）、DR-17（代理指标）、DR-20（综合复盘）。
- → 行为改变：下次写冻结提示词前，先查本段色彩脚本格，把 3–5 个命名色与光句逐字贴进去；查不到格 → 先回本技能补格，不得即兴配色。
