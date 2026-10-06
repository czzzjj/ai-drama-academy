# 发布验收清单（R-PUB）

> **阶段**：5 发布（`publish-kit.md` + 每集成片的发布版 + `post-release-notes.md`）
> **来源性质**：本表**全部是外部调研**。委托方从未把作品发布到任何平台〔委托方实证·GAP-1〕，下面没有一条是"经验表明"。法规与许可条款**不构成法律意见**，落地前由属主或法务确认〔[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第四部分〕。
> **何时跑**：成片过了 [`50-rubrics/checklists/final-cut.md`](final-cut.md) 之后、人类拍板点④之前；改了片头、标识、封面、标题，或换了目标平台，整表重跑。发布后 24h 和 72h 各跑一次 R-PUB-25。
> **通过规则**：
> 1. **合规优先**：R-PUB-01 – R-PUB-16 决定"能不能发"，优先级高于任何审美问题。任一行为假或"未确认"，**禁止发布**，上报人类拍板点④；agent 不得自行判定"风险可接受"。
> 2. 钩子与运营（R-PUB-17 – R-PUB-25）决定"发出去有没有人看"。为假的行写进缺陷单，按 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3 的病灶路由回流，不在发布环节打补丁。
>
> **对应技能**：[`20-craft/publish-prep/SKILL.md`](../../20-craft/publish-prep/SKILL.md) ｜ 理论：[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)

## 证据命令

```bash
F=final/ep03.mp4; O=review/publish
# AIGC 显式标识：0 / 1 / 2 / 2.4s 四帧，原尺寸（量字高）
for t in 0 1 2 2.4; do ffmpeg -v error -y -ss $t -i $F -frames:v 1 $O/label-t$t.png; done
# AIGC 隐式标识：容器元数据里应有 AIGC 字段（JSON）
ffprobe -v error -show_entries format_tags -of json $F
# 安全区叠加（1080×1920：上 269px、下 672px、左右各 65px，取自 Meta 的 14% / 35% / 6%）
ffmpeg -v error -y -i $F -vf "fps=1,drawbox=x=0:y=0:w=iw:h=269:color=red@0.35:t=fill,drawbox=x=0:y=ih-672:w=iw:h=672:color=red@0.35:t=fill,drawbox=x=0:y=0:w=65:h=ih:color=red@0.35:t=fill,drawbox=x=iw-65:y=0:w=65:h=ih:color=red@0.35:t=fill,scale=270:-2,tile=6x4" -frames:v 1 $O/safezone.jpg
```

## 判据表

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-PUB-01 | 每集成片的起始画面上有 AI 显式标识文字，同时含"人工智能"或"AI"，以及"生成"或"合成"（例如"本剧由 AI 生成"、"人工智能生成合成"）。只写"AI"或"AI 辅助制作"不满足国标的两要素 | [自动]+[目视] | `label-t0.png` + OCR 文本 | S-PLAT-02, F-PLAT-03, S-PLAT-03, S-PLAT-06〔外部调研〕 | `scripts/burnin_text_scan.py --mode final`（`D1-text-final`） |
| R-PUB-02 | 标识文字高度 ≥ 画面短边的 5%（1080 宽时字形实高 ≥54px），字型清晰可辨；量的是原尺寸截图上的字形像素高度，不是字号参数 | [目视] | `label-t0.png` 原尺寸裁剪 + 像素高度读数 | S-PLAT-02, F-PLAT-03〔外部调研〕 | ffmpeg `crop` |
| R-PUB-03 | 标识从第 0 帧开始显示，正常播放速度下持续 ≥2s（学院取 ≥2.5s 留余量）：0 / 1 / 2 / 2.4s 四帧上都在 | [自动]+[目视] | `label-t0/1/2/2.4.png` | S-PLAT-02, F-PLAT-03〔外部调研〕 | ffmpeg `-ss` 抽帧 |
| R-PUB-04 | 标识位于画面的边或角，并且不落在平台 UI 遮挡区（顶部 14%、底部 35%、左右各 6% 以外）；学院默认放在左侧边、顶部 14% 线以下 | [目视] | `safezone.jpg` 首格 | S-PLAT-02, S-PLAT-20, F-PLAT-13〔外部调研〕 | ffmpeg `drawbox` 叠加 |
| R-PUB-05 | 本季**每一集**（不只是第一集）都带 AI 提示标识 | [自动]+[目视] | 每集的 `label-t0.png` | S-PLAT-01, F-PLAT-01〔外部调研〕 | 对每集循环运行上面的抽帧命令 |
| R-PUB-06 | 文件元数据有隐式标识：字段名含 `AIGC`，值为 JSON，至少含 `Label`、`ContentProducer`、`ProduceID` | [自动] | ffprobe `format_tags` 输出 | S-PLAT-02, F-PLAT-04, S-PLAT-11, F-PLAT-19〔外部调研〕 | `ffprobe -show_entries format_tags` |
| R-PUB-07 | 片头明显位置标了剧名，以及按本剧分类所需的许可证号、批准文件编号或节目编号；编剧、导演署名在首集片头或末集片尾。编号还没拿到时，本行为假 | [目视] | 片头截图 + 编号来源记录 | S-PLAT-01, F-PLAT-01, F-PLAT-02, S-PLAT-05〔外部调研〕 | — |
| R-PUB-08 | 上传时已在平台打开 AI 内容声明（抖音的 AI 内容标识、TikTok 的 AI-generated content、YouTube 的 AI use = Yes），每个平台的声明页截图已存档 | [目视] | `review/publish/declare-<平台>.png` | S-PLAT-03, F-PLAT-06, S-PLAT-11, S-PLAT-23, S-PLAT-25〔外部调研〕 | — |
| R-PUB-09 | 发布地域与 H3 许可相符：目标平台和投放地区不在许可排除地域（美国、欧盟、英国、韩国）内展示，或已取得书面授权；许可要求的 "MiniMax H3" 显著署名已经处理 | [目视] | `publish-kit.md` 的平台/地区清单 + 授权文件或属主确认 | S-H3-14, F-H3-25, GAP-1〔外部调研〕 | — |
| R-PUB-10 | 本地 H3 输出用于商业发布，已取得 MiniMax 商业授权（Comfy 文档称经 Comfy 购买）；属主书面确认 | [目视] | 授权凭证或属主确认记录 | S-COMFY-09, F-COMFY-07, F-H3-26〔外部调研〕 | — |
| R-PUB-11 | Qwen-Image-2.1 是 Qwen Research License（只限非商业），变现发布前已签商业许可；否则板图、关键帧已换用可商用模型（如 Apache-2.0 的 Qwen-Image-Edit-2511），资产台账逐张记下出图模型 | [目视] | 许可凭证或资产台账"模型"列 | S-COMFY-01, S-COMFY-02, F-COMFY-06〔外部调研〕 | — |
| R-PUB-12 | 每条配乐、音效在许可台账里标为可商用；生成器配乐（如 MiniMax Music 3）的许可原文已由人类核实（来源互相矛盾：CC BY-NC 4.0 vs MiniMax-Music3 Community License） | [目视] | `assets/license-ledger.md` + 核实记录 | S-H3-16, F-H3-31, S-CRAFT-21, S-CRAFT-25〔外部调研〕 | — |
| R-PUB-13 | 发往 YouTube 且单集超过 60s 时，所用配乐都不会产生任何 Content ID 声明（否则 Short 会被全球屏蔽） | [目视] | 每首曲目的来源与 Content ID 状态 | S-PLAT-24, F-PLAT-20, F-CRAFT-23〔外部调研〕 | — |
| R-PUB-14 | 角色形象无侵权：没有用真实人物照片（含网络写真）作参考，参考图授权台账齐全；同剧主要角色有清晰区分度，不复用本属主其他剧的角色脸 | [目视] | 授权台账 + 选角对照表 | S-PLAT-09, S-PLAT-07, F-PLAT-15, F-PLAT-16, B3〔外部调研〕 | — |
| R-PUB-15 | 已对照《微短剧发展管理办法》的禁止内容条款逐条自查本集内容，结论记录在案；拿不准的条目上报④ | [目视] | `publish-kit.md` 自查表 | S-PLAT-01〔外部调研〕 | — |
| R-PUB-16 | `publish-kit.md` 合规表 R-PUB-01 – R-PUB-15 每行都填了"已确认 / 未确认"、确认人和日期；只要有一行"未确认"，本集状态为"待人类拍板④"，agent 没有执行发布 | [目视] | `publish-kit.md` 合规表 | GAP-1, S-PLAT-01, S-H3-14〔外部调研〕 | — |
| R-PUB-17 | 开场 3s 内，冲突主张已经可见（谁 + 想要什么或受到什么威胁，能用一句话说出）；剧名、编号和 AI 标识叠在剧情画面上，不单独占用开场秒数〔学院推断：冷观众在第 3s 暂停，回答"这集要讲什么冲突"，≥2/3 答对即成立〕 | [目视]+[冷观众] | 0–3s 帧序列 + 冷观众回答 | S-PLAT-12, F-PLAT-09, S-PLAT-21, F-PLAT-10, S-PLAT-22〔外部调研〕 | ffmpeg `fps=2,tile` |
| R-PUB-18 | 字幕、片名、AI 标识和关键人物脸，在全片抽帧上都没有进入安全区遮挡带（Meta Reels：顶部约 14%、底部约 35%、左右各约 6%。这是调研中唯一有官方百分比的安全区，国内平台没有官方值时按它执行） | [目视] | `safezone.jpg` 逐格结论 | S-PLAT-20, F-PLAT-13, S-PLAT-21, F-PLAT-14〔外部调研〕 | ffmpeg `drawbox` 叠加 |
| R-PUB-19 | 关掉声音也能看懂：全部台词都有硬字幕，且字幕位于安全区内 | [目视] | 静音放映记录 + 字幕抽帧 | S-PLAT-22, F-PLAT-11〔外部调研〕 | `scripts/burnin_text_scan.py --mode final`（`D1-text-final`） |
| R-PUB-20 | 封面取自本集正片的一帧（YouTube Shorts 只能选帧）；封面里的文字落在中心 3:4 区域内〔学院推断：抖音 3:4 裁切只是从业者说法，未核实〕；封面画面与正片内容一致 | [目视] | 封面原帧时间码 + 3:4 裁切预览 | S-PLAT-24, F-PLAT-22, S-PLAT-01〔外部调研〕 | ffmpeg `crop=iw:iw*4/3`（中心 3:4 预览） |
| R-PUB-21 | 标题 ≤100 字符（YouTube 上限）；标题承诺的事件确实发生在本集正片里，并能给出时间码（推广信息须与内容相符） | [目视] | 标题 + 对应时间码 | S-PLAT-24, F-PLAT-22, S-PLAT-01〔外部调研〕 | `wc -m` |
| R-PUB-22 | 本集最后 10s 抛出一个具体的未解问题；≥2/3 冷观众能说出"想知道的具体问题"（而不是"挺好看"） | [冷观众] | 冷观众记录中的问题原句 | S-PLAT-18, F-PLAT-28, GAP-2〔外部调研〕 | — |
| R-PUB-23 | `publish-kit.md` 写明更新节奏（每周几集）、合集/专辑名称和集序；各集按序进入同一合集；单日上传量不超过平台上限（据报道红果单账户每天 30 部，原文未找到） | [目视] | `publish-kit.md` 发布计划 + 平台后台截图 | S-PLAT-10, F-PLAT-18, S-PLAT-17〔外部调研〕 | — |
| R-PUB-24 | 平台支持陌生观众测试时（如 Instagram Trial Reels），同一集准备 2–3 个开场或封面变体，先推给非粉丝，24–72h 后按数据选定 | [目视] | 变体清单 + 24h / 72h 数据截图 | S-PLAT-26, F-PLAT-24〔外部调研〕 | — |
| R-PUB-25 | 发布后 24h 和 72h，`post-release-notes.md` 记下播放与 engaged views、完播率、留存曲线的掉点时间码；每个掉点对应一张缺陷单，并标注病灶阶段 | [目视] | `post-release-notes.md` + 留存曲线截图 | S-CASE-16, S-PLAT-24, F-PLAT-23, GAP-1〔外部调研〕 | — |

## 常见误判

- **先做封面，合规最后看**：顺序反了。标识、编号、许可任何一项不过，封面做得再好也发不出去；红果的 AI 脸、侵权治理还会直接下架（S-PLAT-07、S-PLAT-09）。`publish-prep` 的第一步是 R-PUB-01 – R-PUB-16。
- **标识放在角落就够了**：国标要求放在边或角，但右下、底部 35% 的位置会被平台按钮和标题栏挡住。挡住了就等于没标（R-PUB-04）。
- **只在第一集标**：《管理办法》第三十四条要求"每集明显位置"（R-PUB-05）。
- **写了"AI 辅助制作"就算合规**：这个说法只有一家媒体转述（S-PLAT-06），而且不满足 GB 45438 要求的"生成 / 合成"要素（R-PUB-01）。
- **把"黄金 3 秒""前 15 秒反转"当官方规范**：官方锚点只有广电的"有效播放 >3s"和 TikTok 广告建议的"3 秒主张、6 秒钩子"；其余是行规。行规可以用，但要标成行规（R-PUB-17、R-PUB-22）。
- **为了显眼，把字幕放在画面最底部**：底部 35% 是平台 UI 带，字幕要放在这条带的上沿之上（R-PUB-18）。
- **用发布数据给本集打补丁**：留存掉点要回流到病灶阶段（钩子回剧本，看不懂回分镜），不在已发布的片上修（R-PUB-25）。见 [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)。

## → 行为改变

下次接到"准备发布"任务时，先生成 `publish-kit.md` 合规表（R-PUB-01 – R-PUB-16 每行一格），逐行取证。只要有一格"未确认"，就停在拍板点④，把这一格交给人类。
