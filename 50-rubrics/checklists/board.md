# 板图验收清单（R-BRD）

> **阶段**：1 预制作 · 板图（角色 `CHR-` / 场景 `LOC-` / 道具 `PRP-` / 符号 `SYM-` 的资产母版，Qwen-Image，1696×2528，40 steps〔委托方实证·T-1〕）
> **何时跑**：每张板图定稿前；锚点卡的 `必现` / `禁用` / `方位属性` 改动后，受影响资产全部重跑；板图被选作视频 `references` 之前必须已过本表。
> **通过规则**：本表全部行为真才算定稿。任一 `[目视]` 行没有证据文件，该行按"未验证"处理，资产不通过。高风险资产（主角、BOSS、核心道具、主场景）还必须过 R-BRD-10 的独立复验。"看一眼差不多"不是证据〔委托方实证·C2〕。
> **证据放哪**：`qc/<ASSET-ID>.md` 写验收记录，裁剪与对照图放 `qc/<ASSET-ID>/`。证据路径一律写成**带目录的反引号路径**（如 `qc/CHR-NIJIADI/crop-arm-left.png`），`asset_exists.py qc/` 才查得到。
> **对应技能**：[`20-craft/asset-boards/SKILL.md`](../../20-craft/asset-boards/SKILL.md)、[`20-craft/casting-and-canon/SKILL.md`](../../20-craft/casting-and-canon/SKILL.md) ｜ 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)

## 证据制作命令（静帧）

`contact_sheet.py` 只收视频，板图的放大裁剪和并排对照直接用 ffmpeg：

```bash
# 逐特征放大裁剪：最近邻放大，不"脑补"细节（C1、C2）
ffmpeg -v error -y -i assets/boards/CHR-NIJIADI-BOARD.png -vf "crop=420:600:180:900,scale=iw*4:ih*4:flags=neighbor" qc/CHR-NIJIADI/crop-arm-left.png
# 观看尺寸 + 去色测试：程度类属性（对比/大小/数量）用（C1-7）
ffmpeg -v error -y -i assets/boards/CHR-NIJIADI-BOARD.png -vf "scale=270:-2,format=gray" qc/CHR-NIJIADI/view270-gray.png
# 多 seed 并排（先统一高度再 hstack）
ffmpeg -v error -y -i s1.png -i s2.png -i s3.png -filter_complex "[0]scale=-2:1200[a];[1]scale=-2:1200[b];[2]scale=-2:1200[c];[a][b][c]hstack=inputs=3" qc/CHR-NIJIADI/seeds.png
```

## 判据表

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-BRD-01 | 每个在 ≥1 镜出现的资产，在 `anchors.md` 有一张锚点卡，`锚点句 EN`、`必现`、`禁用`、`来源依据` 四行齐全，有方位要求的另有 `方位属性`；`板图` 字段指向的文件存在且非空 | [自动] | `asset_exists.py` 报告无 error | P1, T-3, E2 | `scripts/asset_exists.py anchors.md`（`E2-missing-ref` `E2-empty-asset`） |
| R-BRD-02 | 关键资产（主角、BOSS、核心道具、主场景）至少生成 3 个 seed，并排比较后选定；定稿版不是第 1 个 seed 的默认产出；落选版归档在 `assets/boards/_rejected/` | [目视] | `qc/<ASSET-ID>/seeds.png` 并排图 + 记录里写明选中 seed 与淘汰理由 | P2, M6, C1-1, C1-6 | ffmpeg `hstack`（无专用脚本） |
| R-BRD-03 | 验收记录的逐项表按固定顺序填写：① 禁用项 → ② 必现项 → ③ 方位属性 → ④ 程度属性 → ⑤ 构图与美感；①–④ 有任一行不通过时，⑤ 留空不评 | [目视] | `qc/<ASSET-ID>.md` 逐项表的行序与结论 | C1, C2 | — |
| R-BRD-04 | 锚点卡 `禁用` 的每一条都对应一张最近邻放大裁剪图，图中不存在该物（宝石、铠甲、颈饰、远山、刻纹、光柱等） | [目视] | 每条禁用项一张 `crop-<项>.png`，逐项表里每行指向自己的图 | C1, C1-1, C1-2, C1-3, C1-4, C1-5 | ffmpeg `crop` + `scale=…:flags=neighbor` |
| R-BRD-05 | 锚点卡 `必现` 的每一条（发色、服装、标志物、形制如"单刃无中脊"）都有一张放大裁剪图，与锚点卡文字逐字段对照后一致 | [目视] | 每条必现项一张裁剪图 + 对照结论 | P2, P3, C1-1 | ffmpeg `crop` + `scale=…:flags=neighbor` |
| R-BRD-06 | 方位/朝向类属性（左右臂、持刀手、伤疤在哪侧）单独裁剪放大确认，结论用**画面坐标**书写（"画面左 = 黑臂"），不写角色自身的左右 | [目视] | `crop-<方位项>.png` + 一行画面坐标结论 | C1-6, C1-7, A5 | ffmpeg `crop` |
| R-BRD-07 | 程度类属性（对比、大小、数量）缩到 270 宽并去色后，仍能一眼读出（如"黑臂与白臂的明度差"） | [目视] | `view270-gray.png` + 一句可读性结论 | C1-7, M2 | ffmpeg `scale=270:-2,format=gray` |
| R-BRD-08 | 符号/图形资产（`SYM-`）按对抗约束清单逐条计数核对（例：红环数 = 1、竖线数 = 1、横线数 = 0），质感与锚点卡一致（火纹而非霓虹/激光） | [目视] | 符号放大裁剪 + 逐条计数表 | D4 | ffmpeg `crop` |
| R-BRD-09 | 高风险资产另有一张"本版 vs 锚点卡参考/上一定稿版"的同部位并排对照图 | [目视] | `qc/<ASSET-ID>/compare-<部位>.png` | C2, B1 | ffmpeg `hstack` |
| R-BRD-10 | 高风险资产有第二遍复验，由**独立会话**完成：复验会话只拿到板图、锚点卡和裁剪图，没看过生成提示词和作者的通过理由；记录里有 `复验人`（会话标识 + 日期） | [目视] | `qc/<ASSET-ID>.md` 的 `复验人` 行 + 复验会话的逐项表 | C2, C1-7, S-ZEN-12 | — |
| R-BRD-11 | 验收记录含 `结论`（通过 / 不通过 / 有条件通过）、`证据` 文件列表和逐项表；没亲眼核过的项写"未验证"，不打 ✅；记录里引用的每个证据文件都存在且非空 | [自动]+[目视] | `qc/<ASSET-ID>.md` + `asset_exists.py qc/` 报告 | C2, E2, S-PIPE-01 | `scripts/asset_exists.py qc/`（`E2-missing-ref` `E2-empty-asset`） |
| R-BRD-12 | 板图提示词里每一条否定句（`no X`）前面都有一条对应的正向可见状态句（如 `the guard is plain polished steel, smooth and unadorned`）；工作流里不存在被填写的 `negative_prompt` | [自动]+[目视] | 板图提示词原文 + grep 结果 | C1, T-2, S-COMFY-05, S-COMFY-08 | `grep -n "negative_prompt"`（无专用脚本） |
| R-BRD-13 | 本轮新加的每条否定句都有 A/B 记录（A = 只写正向句，B = 正向句 + 否定句，各 ≥3 seed，记下目标物出现次数）；没做 A/B 的否定句在锚点卡上标"未验证" | [目视] | A/B 并排图 + 出现次数表 | C1, S-H3-09, S-COMFY-08, S-ZEN-17 | ffmpeg `hstack` |
| R-BRD-14 | 要送 `references` 当身份参考的角色板，一张图只有一个人、一张脸、一个角度（正脸大头照、全身照各一张），不是多视角拼图；服装参考图不带脸 | [目视] | 板图缩略图 + 一行结论 | B3, S-H3-09, S-VGEN-11, S-VGEN-18 | — |
| R-BRD-15 | 板图上没有任何文字：标签、编号、尺寸标注、inset 说明字都不允许 | [目视] | 全图 + 四角放大裁剪 | D1, D2, S-VGEN-11 | ffmpeg `crop` |
| R-BRD-16 | 全部主要角色的正脸板裁成同尺寸，排成一张选角对照表；任意两个角色至少在 3 项可见特征上不同（发型轮廓、脸型、体格、年龄感、服色中选） | [目视] | `qc/casting-lineup.png` + 两两差异表 | B3, S-PLAT-07 | ffmpeg `hstack` |
| R-BRD-17 | 每张角色/服装参考图的来源可追溯；没有用真实人物照片（包括网络写真）当参考；授权台账逐图有一行（来源、许可、日期） | [目视] | `assets/license-ledger.md` 对应行 | S-PLAT-09, S-PLAT-07 | — |
| R-BRD-18 | 场景板（`LOC-`）在验收记录里标出画面内的实景光源（窗、火、灯、月）位置、光向和色温；后续同场关键帧以它为准 | [目视] | 场景板标注图或一行"光源 / 方向 / 色温"记录 | GAP-4, S-CRAFT-14, F-CRAFT-13 | — |
| R-BRD-19 | 板图生成日志记下 seed、batch_index、steps、尺寸、模型文件名；缺任一项，该版不能定稿 | [目视] | 生成日志或 `qc/<ASSET-ID>.md` 的参数行 | T-1, P2, S-COMFY-18 | — |
| R-BRD-20 | 定稿后锚点卡 `板图` 字段写明定稿 seed 和落选 seed 的归档路径；如果定稿图与 `锚点句 EN` 有出入（例如发饰形状），已把锚点句**回写**成图上的事实 | [目视] | 锚点卡 diff + 一行"已回写 / 无差异" | E4, P1, P2 | `git diff anchors.md` |
| R-BRD-21 | 背景人群不建独立的 `CHR-` 卡与特征板；需要人群板时，画成大虚化、没有可辨认独立脸和手持物的暗色块 | [目视] | 人群板缩略图 + 一行结论 | B2 | — |

## 常见误判

- **"方位对了就过"**：C1-6 修好左右臂之后，C1-7 的首验只核了方位，把"黑臂对比弱"放了过去。方位和程度是两个独立属性，各自要一张证据（R-BRD-06、R-BRD-07）。见 [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)。
- **全图看着很美就跳过禁用项**：构图好看不能抵消禁用项。顺序固定为禁用 → 必现 → 方位 → 程度 → 美感（R-BRD-03）。生成器会自己加东西，因为本管线的 `negative_prompt` 无效（T-2）。
- **以为写了 `no gemstone` 就处理了**：只写否定句可能反而把宝石招进来（S-COMFY-08）。要先写正向状态句，再追加否定句，并用 A/B 证明否定句没有起反作用（R-BRD-12、R-BRD-13）。
- **验收记录写"通过"两个字**：在本学院等于"未验证"。没有裁剪图的通过一律重验，见 [`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md)。
- **自己复验自己**：作者会话第二遍看图，会被自己的通过理由带着走。复验必须换独立会话，并且不给它提示词（R-BRD-10）。
- **多视角设定图当身份参考**：一张图上有几张脸，视频里就可能出几个人（S-H3-09）。设定图可以存档，但不能送 `references`（R-BRD-14）。见 [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)。

## → 行为改变

下次验收板图时，先按锚点卡生成逐项表骨架（每条禁用、必现、方位、程度各占一行），再逐行出裁剪图填结论。最后一行填满之前，**禁止**写"结论：通过"。
