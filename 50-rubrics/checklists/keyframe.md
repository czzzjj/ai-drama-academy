# 关键帧验收清单（R-KF）

> **阶段**：2 制作 · 关键帧（每镜的起始帧 `REF-SHOTnnn-START`，送 H3 `first_frame`）。画面级要素（方向、构图、灯光、尺度、史诗感）由起始帧决定，提示词救不了构图〔委托方实证·P4、M2〕。
> **何时跑**：每镜关键帧定稿前。本表没全过的镜**禁止**进入视频 prepare〔委托方实证·P3、M9〕。分镜 `起始帧方位` 改了、锚点卡改了、同场前一镜的关键帧换了，受影响的镜都要重跑。
> **通过规则**：本表全部行为真；任一 `[目视]` 行缺证据文件，视为未验证，按不通过处理。主角正脸、BOSS、核心道具特写、打斗起幅这几类镜属于高风险，另须过 R-KF-16 的独立复验。
> **证据放哪**：`qc/<SHOT-nnn>.md` 的"关键帧"一节；图放 `qc/<SHOT-nnn>/kf-*.png`，路径写成带目录的反引号路径。
> **对应技能**：[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md) ｜ 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/12-color-and-light.md`](../../10-theory/12-color-and-light.md)

## 证据制作命令（静帧）

```bash
# 尺寸（必须 9:16）
ffprobe -v error -show_entries stream=width,height -of csv=p=0 assets/keyframes/REF-SHOT004-START.png
# 显式裁到 9:16（2:3 母图 1696×2528 → 中心裁 1422×2528，再缩放到 1536×2752 或直接送入），命令写进记录
ffmpeg -v error -y -i src-1696x2528.png -vf "crop=1422:2528:(iw-1422)/2:0,scale=1536:2752:flags=lanczos" assets/keyframes/REF-SHOT004-START.png
# 海报测试：观看尺寸 + 去色
ffmpeg -v error -y -i assets/keyframes/REF-SHOT004-START.png -vf "scale=270:-2,format=gray" qc/SHOT-004/kf-poster270-gray.png
# 与板图同部位并排（脸、手、标志物）
ffmpeg -v error -y -i kf-face.png -i board-face.png -filter_complex "[0]scale=-2:600[a];[1]scale=-2:600[b];[a][b]hstack" qc/SHOT-004/kf-face-vs-board.png
```

## 判据表

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-KF-01 | 本镜有一条英文冻结提示词，描述起始画面的完整状态（人物、位置、姿态、光、背景），并逐字嵌入画面内每个资产的 `锚点句 EN` | [自动]+[目视] | 冻结提示词原文 + 每条锚点句的 grep 命中 | P3, P1 | `grep -F "<锚点句>"`（无专用脚本） |
| R-KF-02 | 要送 `first_frame` 的关键帧是 9:16：尺寸为 1536×2752，或在送入前显式裁成 9:16 并在记录里留下裁切命令；1696×2528 的 2:3 原图不得直接送入（节点会把它非等比拉伸到画布） | [自动] | ffprobe 输出的宽高 + 裁切命令 | T-1, S-COMFY-01, S-H3-03, F-H3-07 | `ffprobe`；出视频后 `scripts/contact_sheet.py --keyframe` 不得报 `B4-keyframe-aspect` |
| R-KF-03 | 高风险镜的关键帧至少 3 个 seed 并排选优；其余镜也不得把第一版直接定稿，至少要有 2 版并排〔学院推断：普通镜的 2 版下限待生产数据校准〕 | [目视] | `qc/<SHOT>/kf-seeds.png` + 选中理由 | P2, P3, M2, M6 | ffmpeg `hstack` |
| R-KF-04 | 画面内每个资产的 `必现` 和 `禁用` 都已逐条放大核验（发色、服装、标志物、禁用物），每条一张裁剪图，与板图同部位并排 | [目视] | 每条一张 `kf-crop-<项>.png` + 并排图 | P3, C1, C2 | ffmpeg `crop` + `scale=…:flags=neighbor` |
| R-KF-05 | 人物在画面中的左右位置与分镜 `起始帧方位` 一致（`神=LEFT` 即神的身体主体在画面左半），结论用画面坐标书写 | [目视] | 关键帧缩略图上标出左右分界 + 一行结论 | A5, P4, M4 | — |
| R-KF-06 | 方位/朝向类属性（持刀手、黑臂在哪一侧、伤疤侧）单独裁剪放大确认 | [目视] | `kf-crop-<方位项>.png` + 画面坐标结论 | C1-6, C1-7 | ffmpeg `crop` |
| R-KF-07 | 海报测试：缩到 270 宽并去色后，主体剪影、视线方向和冲突双方的相对关系一眼可读 | [目视] | `kf-poster270-gray.png` + 三句结论（主体 / 视线 / 关系） | M2, C1-7 | ffmpeg `scale=270:-2,format=gray` |
| R-KF-08 | 记录里写出本镜的画面级目标（一句，如"BOSS 压迫感：BOSS 占画高 ≥50%，苏晓在下三分之一"），并指出关键帧上对应的可见证据；关键帧上看不到的"感"，不准指望视频提示词补 | [目视] | 一句目标 + 证据位置（裁剪或标注） | M2, P4, A5 | — |
| R-KF-09 | 运镜为推近/收紧的镜，关键帧取的是宽的一端；需要以紧景收束的镜，关键帧不得已经是紧景（"A shot that must end tight has to open wide"） | [目视] | 关键帧景别 + 分镜 `运镜` 列对照 | A4, S-H3-08 | — |
| R-KF-10 | 画面有 ≥2 人时，逐张脸裁剪后并排，任意两张都不像同一个人；冻结提示词含差异化描述句 | [目视] | `kf-faces.png` + 差异化句原文 | B3 | ffmpeg `crop` + `hstack` |
| R-KF-11 | 背景人群是大虚化的暗色块，没有可辨认的独立脸，也没有具象手持物（发光平板之类） | [目视] | 人群区域放大裁剪 | B2 | ffmpeg `crop` |
| R-KF-12 | 关键帧上没有文字、水印、标签或 inset 说明字；画面里的屏幕、招牌只给亮度、不给内容 | [目视] | 全图 + 四角与屏幕区域放大裁剪 | D1, D2, S-H3-09 | ffmpeg `crop` |
| R-KF-13 | 主光源能在画面内指认，或能由场景推断（窗、火、月、屏）；光向与同场景板标注、同场前一已过关键帧一致；主色符合本段色彩脚本格（细则见 [`50-rubrics/checklists/sound-color-performance.md`](sound-color-performance.md) 的 R-COL-02、R-COL-04、R-COL-05） | [目视] | 与前一关键帧并排图 + 一行"光源 / 方向 / 色温" | GAP-4, S-CRAFT-14, A5 | ffmpeg `hstack` |
| R-KF-14 | 起始帧呈现的是本镜动作链的起点（意图或预备相），不是接触或后果相；视频还有完整的动作可生成〔学院推断：用 A/B 验证——同镜分别以起点帧、高潮帧起生成，比较动作完整度〕 | [目视] | 关键帧 + 分镜 `内容` 列的动作链，标出起始帧落在第几相 | A2, P10, M1 | — |
| R-KF-15 | 与同场前一已过关键帧并排后，角色脸、服装、手持物、场景元素一致（链式参考的前提） | [目视] | `kf-vs-prev.png` | P5, M7, B1 | ffmpeg `hstack` |
| R-KF-16 | 高风险镜有独立会话完成的第二遍复验：复验方只看关键帧、板图、锚点卡和分镜方位，没看过冻结提示词和作者理由；记录里有 `复验人` | [目视] | `qc/<SHOT>.md` 的 `复验人` 行 + 复验逐项表 | C2, S-ZEN-12 | — |
| R-KF-17 | 主角在本集至少有 1 个正脸关键帧，脸部裁剪已与板图逐特征比对（发际线、眉形、眼型、鼻梁、下颌、年龄感），裁剪图已入正脸库 | [目视] | `qc/face-library/<EP>-<CHR>.png` + 逐特征表 | B1 | ffmpeg `crop` + `hstack` |
| R-KF-18 | 关键帧定稿后，如果画面与冻结提示词有出入，提示词已回写成画面的事实；参考图与提示词描述同一事实 | [目视] | 记录里一行"提示词 ↔ 关键帧差异：已回写 / 无差异" | E4, P3 | `git diff` |
| R-KF-19 | 视频提示词 `first_frame` 指向的 `REF-SHOTnnn-START` 文件存在，且它的 `qc/<SHOT>.md` 结论为"通过"；验收记录引用的证据文件都存在且非空 | [自动] | `asset_exists.py` 报告 + `grep -l "结论: 通过" qc/` | P3, T-3, M9, C2 | `scripts/asset_exists.py qc/`（`E2-missing-ref` `E2-empty-asset`） |
| R-KF-20 | 关键帧生成日志记下 seed、batch_index、steps、尺寸和模型文件名；冻结提示词里没有填 `negative_prompt` | [目视] | 生成日志或记录参数行 | T-1, C1, S-COMFY-18 | `grep -n "negative_prompt"` |

## 常见误判

- **"方向不对，在视频提示词里写 `turns to face left` 修一下"**：画面的左右位置和轴线由起始帧钉死，文字改不动；硬改只会把空间搅乱。应当回关键帧重出（R-KF-05）。见 [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)。
- **把 2:3 板图尺寸直接当关键帧**：1696×2528 是 Qwen 的 2:3 推荐尺寸，9:16 是 1536×2752。2:3 图送进 9:16 画布会被非等比拉伸（S-H3-03），脸和圆形物件都会变形（R-KF-02）。
- **全图看着有史诗感就放行**：海报测试要在手机观看尺寸、去色后做（R-KF-07）。全分辨率下好看、270 宽时读不出关系的画面，视频里同样读不出。
- **起始帧选了"最好看的那一刻"**：如果选的是接触或爆发瞬间，视频只剩后果可演，结果就是慢镜和定格感（R-KF-14）。见 [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)。
- **关键帧和板图分别验收，没有并排**：分开看都"像"，并排才看得出漂移（R-KF-04、R-KF-15、R-KF-17）。见 [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md)。
- **关键帧过了，但冻结提示词还是旧版**：后续重出会按旧描述走，与参考图互相矛盾（R-KF-18）。见 [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)。

## → 行为改变

下次出关键帧前，先从分镜表抄出本镜的 `起始帧方位`、`运镜` 和动作链第一相，写在 `qc/<SHOT>.md` 顶部当验收靶子。关键帧必须逐条命中这三项，才开始核特征。
