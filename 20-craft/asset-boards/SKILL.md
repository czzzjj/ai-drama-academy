---
name: asset-boards
description: 按锚点卡生产并验收板图：关键资产 ≥3 seed 并排抽卡，按"禁用→必现→方位→程度→美感"顺序逐特征放大裁剪取证，方位属性单独放大，高风险资产由独立会话二次复验，落选 seed 归档，生成日志完整，并在开工前过 Qwen-Image 许可闸门。Use when generating character/prop/location/symbol boards, choosing a seed, or accepting/rejecting a board. 触发词：板图、角色板、道具板、场景板、抽卡、多 seed、逐特征验收、放大裁剪、二次复验、落选归档、许可、board, reference sheet, multi-seed, feature-by-feature zoom, second-pass review, Qwen license. 不负责写锚点句与禁用项（→ casting-and-canon）、不负责逐镜关键帧（→ keyframe-freeze）、不负责视频镜头验收（→ shot-qc）。
---
# 板图生产与验收（asset-boards）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。验收记录格式见 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §6。

## 何时用 / 何时不用
- **必须用**：锚点卡定稿后、任何关键帧之前；锚点卡改版（变体卡、禁用项新增）后；QC 发现身份漂移且根因指向板图时。
- **不用**：背景人群不出独立板（R-BRD-21，最多出一张大虚化无独立脸的人群氛围板）；字卡/纯色/logo 不出板，本地生成。
- 判决：板图多 seed + 逐特征放大验收是委托方已被证实有效的三件套〔委托方实证·P2、M6〕；"看一眼整体觉得可以"就放行是 C2 放水的原型。

## 输入 → 输出
- 输入：`anchors.md`（锚点句 EN、必现、禁用、方位属性）、`visual-bible.md`（风格锁句、场景光态、规格）。
- 输出：
  - `assets/boards/<ASSET-ID>-BOARD.png`（定稿）；`assets/boards/_rejected/<ASSET-ID>-seedN.png`（落选全部归档）；
  - `qc/<ASSET-ID>.md` 验收记录（模板 [`70-playbooks/templates/qc-record.md`](../../70-playbooks/templates/qc-record.md)）；
  - `qc/<ASSET-ID>/seeds.png`（并排）、`crop-<项>.png`（逐项放大）、`compare-<部位>.png`（高风险对照）；
  - `assets/boards/casting-lineup.png`（主要角色正脸对照表）；`assets/license-ledger.md` 参考图与模型许可行；
  - 锚点卡 `板图` 字段回填。

## 步骤
1. **许可闸门（先于一切生成）**：确认本季是否变现。Qwen-Image-2.1 是 Qwen Research License，仅研究/评估，商用需另签〔外部调研·S-COMFY-01、S-COMFY-02〕。若变现且未取得授权 → 停止，在 `license-ledger.md` 写"待人类确认（R-PUB-11）"并上报人类拍板；可商用一致性编辑备选为 Qwen-Image-Edit-2511（Apache-2.0）〔外部调研·见 COMFY 目录笔记〕，换模型须重跑本技能全部验收。参考图禁止真实人物照片（R-BRD-17）。
2. **写板图提示词**：锚点句 EN 逐字 + 风格锁句 + 正向可见状态句；每条否定句前必须有对应正向句（R-BRD-12，R1 立场）；**不写** `negative_prompt`（cfg=1.0 无效〔委托方实证·C1〕）。板上**禁止任何文字**：标签、编号、尺寸标注、inset 说明（R-BRD-15）。
3. **身份板构图**：要送 `references` 的角色板一张图 = 一个人、一张脸、一个角度（正脸大头照、全身照各一张），禁止多视角拼图；服装参考图不带脸（R-BRD-14）。理由：几张脸 = 几个人，多视角拼图最易导致"同框两个同一角色"〔外部调研·S-H3-09、S-VGEN-11、S-VGEN-18〕。尺寸：板图 2:3 1696×2528 可用。
4. **多 seed 抽卡**：关键资产（主角、BOSS、核心道具、主场景）≥3 seed；高频细节（锁子甲、花纹）可提到最多 50 步，常规 12–20 步〔外部调研·S-COMFY-09、S-H3-04〕。并排图：
   `ffmpeg -i s1.png -i s2.png -i s3.png -filter_complex hstack=inputs=3 qc/CHR-SUXIAO/seeds.png`
   定稿不得是第 1 个 seed 的默认产出（R-BRD-02）。
5. **生成日志**：每版记 seed、batch_index、steps、尺寸、模型文件名；缺任一项该版不能定稿（R-BRD-19）。
6. **逐项验收，顺序固定（R-BRD-03）**：① 禁用 → ② 必现 → ③ 方位 → ④ 程度 → ⑤ 构图与美感；①–④ 任一行不通过，⑤ 留空不评。先看美感再找缺陷 = 被整体印象说服（C2）。
   - ① 禁用：每条禁用一张最近邻放大裁剪图，图中不存在该物（R-BRD-04）：
     `ffmpeg -i board.png -vf "crop=400:400:620:900,scale=1200:-1:flags=neighbor" qc/CHR-SUXIAO/crop-neck.png`
   - ② 必现：每条必现一张放大裁剪，与锚点卡描述逐项对照（R-BRD-05）。
   - ③ 方位：左右臂、持刀手、伤疤侧**单独**裁剪放大，结论用**画面坐标**书写（"持剑手在画面右侧 = 角色左手"），R-BRD-06。
   - ④ 程度：缩到 270 宽并去色后仍一眼读出（黑白臂明度差、体量对比），R-BRD-07：`ffmpeg -i board.png -vf "scale=270:-2,format=gray" qc/CHR-GOD/poster270-gray.png`。
   - 符号资产（SYM-）：按对抗约束逐条**计数**（红环 = 1、竖线 = 1、横线 = 0），R-BRD-08〔委托方实证·D4〕。
   - 场景板（LOC-）：标出画面内实景光源位置、光向、色温，供关键帧光向锁（R-BRD-18）。
7. **否定句 A/B**：本轮新加的每条否定句做 A（只写正向句）/ B（正向句 + 否定句）各 ≥3 seed，记目标物出现次数；未做 A/B 的否定句在锚点卡标"未验证"（R-BRD-13）。结果写回 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1 的验证方法栏（经属主同意）。
8. **高风险资产对照与二次复验**：高风险 = 主角、BOSS、符号、曾出过 C1/B1 的资产。① 出"本版 vs 上一定稿/参考"同部位并排图（R-BRD-09）；② 开**独立会话**复验：只给板图、锚点卡、裁剪图，不给生成提示词和作者通过理由；记录写 `复验人`（会话标识 + 日期），R-BRD-10。复验结论与作者冲突时以不通过处理。
9. **结论与证据**：`qc/<ASSET-ID>.md` 写 `结论`（通过 / 不通过 / 有条件通过）、`证据` 文件列表、逐项表；没亲眼核过的项写"未验证"，不打 ✅（R-BRD-11）。验证证据存在：`python3 50-rubrics/scripts/asset_exists.py season-01/ep03/qc/`。
10. **选角对照表**：全部主要角色正脸板裁成同尺寸排成一张，任意两人 ≥3 项可见特征不同（R-BRD-16）；不满足 → 回 [`casting-and-canon`](../casting-and-canon/SKILL.md) 改区分项，再重出。
11. **定稿与归档**：落选 seed 全部移入 `assets/boards/_rejected/`；锚点卡 `板图` 字段写定稿 seed 与落选归档路径；定稿图与锚点句有出入时，把锚点句**回写**成图上事实（R-BRD-20），并通知所有已写提示词的镜同步（R-VP-09 逐字）。

## 判据
- 板图：R-BRD-02 – R-BRD-21 全部（重点 R-BRD-03、R-BRD-04、R-BRD-06、R-BRD-10、R-BRD-14、R-BRD-15、R-BRD-19、R-BRD-20）。
- 许可：R-PUB-11、R-PUB-14、R-BRD-17。
- 下游一致：R-KF-04、R-KF-15、R-KF-17、R-VID-05（脸部与板图同尺寸比对）。
- 审美判据卡：板图阶段 TJ-02、TJ-15（[`30-taste/judgment-cards.md`](../../30-taste/judgment-cards.md)）。
- Q 维度：Q7 一致性与连续性（主）、Q5 美术与密度。

## 失败模式
- **"整体看着可以"就通过，放大后禁用物仍在** → [`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md)：防线 = 步骤 6 固定顺序 + 每条一张裁剪图 + 步骤 8 独立复验。
- **宝石/铠甲/颈饰/远山被加** → [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)：防线 = 正向句优先 + ≥3 seed + 否定句 A/B。
- **跨镜脸漂移** → [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md)：防线 = 单人单脸单角度身份板 + 定稿日志完整可复现。
- **同框克隆脸** → [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)：防线 = 步骤 3 禁多视角拼图 + 步骤 10 选角对照表。
- **符号画成十字** → [`60-casebook/cards/D4-symbol-errors.md`](../../60-casebook/cards/D4-symbol-errors.md)：防线 = 步骤 6 计数核对。
- **验收记录引用的裁剪图不存在** → [`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md)：防线 = 步骤 9 `asset_exists.py qc/`。

## 关联
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)。
- 好/坏样例：[`30-taste/pairs/consistency-assets.md`](../../30-taste/pairs/consistency-assets.md)。
- 相邻技能：上游 [`casting-and-canon`](../casting-and-canon/SKILL.md)、[`visual-bible`](../visual-bible/SKILL.md)；下游 [`keyframe-freeze`](../keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../video-prompting-h3/SKILL.md)（`references` 槽）、`shot-qc`。
- 找错题：DR-06、DR-08、DR-09（验收放水）、DR-12。
- → 行为改变：下次想写"板图通过"之前，先数裁剪图张数是否 = 禁用项数 + 必现项数 + 方位项数；少一张就不得写通过。
