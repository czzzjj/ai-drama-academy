---
name: keyframe-freeze
description: 为每镜写英文冻结提示词并出海报级起始帧：固定结构（风格锁句 → 构图句 → 人物位置句含逐字锚点句 → 场景 → 一句光 + 命名色 → 差异化/人群/禁用句），不写质量咒语，9:16 1536×2752 或显式裁切，多 seed 并排选优，逐特征放大核验，把空间布局钉死在图里，定稿后回写提示词并放行给视频。Use when producing the start frame (first_frame) for any shot, when a shot's composition/epic feel/screen direction is wrong, or before writing the video prompt. 触发词：关键帧、起始帧、冻结提示词、首帧、海报级、构图、画面级、史诗感、压迫感、9:16、多 seed、keyframe, start frame, first frame, freeze prompt, poster test, composition. 不负责板图（→ asset-boards）、视频提示词六段（→ video-prompting-h3）、视频镜头验收（→ shot-qc）。
---
# 关键帧冻结（keyframe-freeze）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。规格见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第三部分；禁用项写法见 R1。

## 何时用 / 何时不用
- **必须用**：分镜过 animatic 闸门后、每镜写视频提示词之前；视频出现越轴、构图弱、"没有压迫感"时——画面级问题回到这里重出起始帧，不在视频提示词里补。
- **不用**：本地生成的字卡/纯色镜（不出关键帧）；板图（→ [`asset-boards`](../asset-boards/SKILL.md)）。
- 判决：画面级属性（史诗感、方向、构图、灯光）由起始帧决定，提示词救不了构图〔委托方实证·M2、P3、P4〕；"空间只能在图里定"——文字空间地图同 seed A/B 压不过场景图〔外部调研·S-H3-09〕。

## 输入 → 输出
- 输入：`storyboard.md`（`内容` 首相、`运镜`、`起始帧方位`）、`anchors.md`、`visual-bible.md`（风格锁句、本段命名色、场景光态）、已过的定稿板图、同场前一已过关键帧。
- 输出：`season-01/ep03/keyframe-prompts.md`（模板 [`70-playbooks/templates/keyframe-prompt.md`](../../70-playbooks/templates/keyframe-prompt.md)）；`keyframes/REF-SHOT004-START.png`（定稿）+ `keyframes/_rejected/`；`qc/SHOT-004.md` 关键帧验收节（模板 `qc-record.md`）。

冻结提示词固定结构（每句一行，顺序固定）：
```text
[1 风格锁] <visual-bible 风格锁句，逐字>
[2 构图] Vertical 9:16 frame, low camera at knee height, wide shot; the stone god fills the LEFT two-thirds and towers above the top edge, the swordswoman small in the lower RIGHT third.
[3 位置+锚点] On the LEFT, <CHR-GOD 锚点句逐字>, right arm raised mid-swing. On the RIGHT, <CHR-SUXIAO 锚点句逐字>, knees bent, sword drawn back low, eyes on the god's knee.
[4 场景] <LOC 锚点句逐字>; cracked flagstones, dust hanging in the air.
[5 光] Cold moonlight falls from the upper LEFT, hard 8:1 contrast, palette of ash grey, moss green and bone white.
[6 差异/人群/禁用] The two figures have clearly different faces, builds and silhouettes. The god's chest is bare weathered stone, smooth and unadorned; no armor.
```

## 步骤
1. **写画面级目标一句**：如"BOSS 压迫感：BOSS 占画高 ≥50%，苏晓在下三分之一"，并预先指定将在图上看哪里取证（R-KF-08）。看不到的"感"不准指望视频提示词补。
2. **取动作链起点**：起始帧必须是本镜动作链的意图或预备相，不是接触或后果相（R-KF-14）；推近/收紧镜取宽的一端，以紧景收束的镜关键帧不得已是紧景（R-KF-09）〔外部调研·S-H3-08〕。
3. **按固定结构写冻结提示词**：
   - [2 构图句] 一句写清景别、机位高度、主体占画比例与画面分区——构图决定画面级属性；
   - [3 位置句] 每个人用画面位置开头（`On the LEFT`），位置与分镜 `起始帧方位` 一致；画面内每个资产的锚点句 EN **逐字**嵌入（R-KF-01；验：`grep -F "<锚点句>" season-01/ep03/keyframe-prompts.md`）；
   - [5 光句] **只一句**：主光源（画面内或可推断）、方向、色温、光比档 + 本段 3–5 个命名色逐字（R-KF-13、R-COL-02、R-COL-04）；光写成被动描述，禁止点名灯具（提到即生长〔外部调研·S-H3-09〕）；
   - [6] ≥2 人时写差异化句（R-KF-10）；背景人群写成大虚化暗色块、无独立脸和手持物（R-KF-11）；禁用项先正向句后绝对否定句（R1）。
4. **禁止项**：不写质量咒语（`masterpiece, best quality, 8k, ultra detailed`）——无可见内容、稀释锚点句权重〔学院推断：同镜 3 seed 有/无咒语 A/B，若无差异即证实无用〕；不写 `negative_prompt`（cfg=1.0 无效，R-KF-20）〔委托方实证·C1〕；不要求画面里出现文字、招牌内容、屏幕内容（只给亮度，R-KF-12）。
5. **规格**：Qwen-Image 出图 **1536×2752（9:16）**；若用 2:3 1696×2528 出图，必须在送 first_frame 前显式裁到 9:16 并在记录里写裁切框——`MiniMaxH3ImageToVideo` 对 first_frame 直接拉伸不保比例〔外部调研·S-H3-03、S-COMFY-01〕（R-KF-02）：
   `ffmpeg -i kf-2x3.png -vf "crop=1422:2528:137:0,scale=1536:2752" keyframes/REF-SHOT004-START.png`
6. **多 seed 海报级选优**：高风险镜（多人、BOSS、打斗、复杂背景）≥3 seed 并排；其余镜也至少 2 版并排，不得第一版直接定稿（R-KF-03）。并排：`ffmpeg -i a.png -i b.png -i c.png -filter_complex hstack=inputs=3 qc/SHOT-004/kf-seeds.png`。生成日志记 seed、batch_index、steps、尺寸、模型文件名（R-KF-20）。
7. **海报测试**：缩到 270 宽并去色后，主体剪影、视线方向、冲突双方相对关系一眼可读（R-KF-07）：`ffmpeg -i REF-SHOT004-START.png -vf "scale=270:-2,format=gray" qc/SHOT-004/kf-poster270-gray.png`。低调段同时看脸是否可辨（R-COL-08）。
8. **逐特征放大核验**（顺序同板图：禁用 → 必现 → 方位 → 程度 → 美感）：每个资产的必现与禁用逐条放大裁剪（R-KF-04）；持刀手、黑臂侧、伤疤侧单独裁剪，用画面坐标写结论（R-KF-06）；人物左右与 `起始帧方位` 一致（R-KF-05）；≥2 人逐张脸裁剪并排，任意两张不像同一人（R-KF-10）；主角本集 ≥1 个正脸关键帧，与板图逐特征比对（R-KF-17）。
9. **链式一致**：与同场前一已过关键帧并排，脸、服装、手持物、场景元素、主光方向一致（R-KF-15、R-COL-05）——这是视频链式参考（P5、M7）的前提。
10. **高风险二次复验**：独立会话只看关键帧、板图、锚点卡、分镜方位，不看提示词与作者理由，记 `复验人`（R-KF-16）。
11. **回写与放行**：定稿画面与冻结提示词有出入 → 把提示词**回写成画面事实**（R-KF-18，E4）；在 `qc/SHOT-004.md` 写结论"通过"后，才允许 [`video-prompting-h3`](../video-prompting-h3/SKILL.md) 在 `first_frame` 引用 `REF-SHOT004-START`（R-KF-19）。视频生成后 `python3 50-rubrics/scripts/contact_sheet.py SHOT-004.mp4 --keyframe keyframes/REF-SHOT004-START.png --out-dir qc/SHOT-004` 把起始帧放在接触表第 1 格做对照。

## 判据
- 关键帧：R-KF-01 – R-KF-20 全部（重点 R-KF-02、R-KF-03、R-KF-05、R-KF-07、R-KF-08、R-KF-14、R-KF-18、R-KF-19）。
- 色彩光：R-COL-02、R-COL-04、R-COL-05、R-COL-08。
- 审美判据卡：关键帧阶段 TJ-01、TJ-04、TJ-11（史诗/压迫镜）、TJ-12（[`30-taste/judgment-cards.md`](../../30-taste/judgment-cards.md)）。
- Q 维度：Q5 美术与密度、Q2 空间与调度（主）、Q7 一致性与连续性。

## 失败模式
- **视频里人物乱跑、越轴** → [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)：防线 = 步骤 3 位置句与方位列一致 + 步骤 8 左右核验，空间钉死在图里。
- **起始帧已是接触相，视频没有动作可演** → [`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)：防线 = 步骤 2 取意图/预备相。
- **推近镜从紧景起、运镜无处可去** → [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)：防线 = 步骤 2 宽端起幅。
- **同框克隆脸** → [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)：防线 = 差异化句 + 逐脸并排。
- **人群长出独立脸和发光平板** → [`60-casebook/cards/B2-crowd-leak.md`](../../60-casebook/cards/B2-crowd-leak.md)：防线 = 大虚化暗色块句（R-KF-11）。
- **禁用物在关键帧复现、放水通过** → [`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md)：防线 = 步骤 8 逐条裁剪 + 步骤 10 独立复验。
- **关键帧与提示词各说各话** → [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)：防线 = 步骤 11 回写。

## 关联
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/12-color-and-light.md`](../../10-theory/12-color-and-light.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)。
- 好/坏样例：[`30-taste/pairs/generation-prompting.md`](../../30-taste/pairs/generation-prompting.md)、[`30-taste/pairs/consistency-assets.md`](../../30-taste/pairs/consistency-assets.md)；风格卡 [`30-taste/style-cards/dark-fantasy-epic.md`](../../30-taste/style-cards/dark-fantasy-epic.md)。
- 相邻技能：[`storyboard-long-take`](../storyboard-long-take/SKILL.md)、[`visual-bible`](../visual-bible/SKILL.md)、[`asset-boards`](../asset-boards/SKILL.md)、[`action-choreography`](../action-choreography/SKILL.md)、[`video-prompting-h3`](../video-prompting-h3/SKILL.md)、`shot-qc`。
- 找错题：DR-05（空间混乱）、DR-06（漂移 + 克隆脸）、DR-07（人群穿帮）、DR-08（禁用项）。
- → 行为改变：下次人类说"没有史诗感/压迫感"，先回关键帧改构图句与机位并重出 ≥3 seed，禁止往视频提示词里加 epic 一类形容词。
