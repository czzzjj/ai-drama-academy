# 生产手册：模板索引（70-playbooks）

> 读者：正在生产某一集的 agent。每份制作文档都从这里的模板起稿；脚本按 [`70-playbooks/format-contracts.md`](format-contracts.md) 解析，模板是契约的可填写版本。
> 用法：把模板复制到本集目录并改成"产出文件名"，替换全部 `<…>` 占位，删掉 `<!-- -->` 指引注释（可保留）。占位未替换就跑脚本，会报 `FMT-*` 或内容 error——这是预期，不要绕过。

## 1. 模板 → 产出 → 技能 → 校验

| 模板 | 产出文件（`season-01/epNN/` 下） | 使用技能 | 契约节 | 校验 / 判据 |
|---|---|---|---|---|
| [`season-bible.md`](templates/season-bible.md) | `../season-bible.md`、`../episode-map.md`（季级） | multi-episode-arc、production-director、sound-design（音色绑定） | — | R-SEA-01–R-SEA-04 |
| [`episode-script.md`](templates/episode-script.md) | `script.md` | script-doctor、multi-episode-arc | — | R-SCR-01–R-SCR-20 |
| [`anchor-card.md`](templates/anchor-card.md) | `anchors.md`（季级共用放 `season-01/anchors.md`） | casting-and-canon、asset-boards、multi-episode-arc、sound-design | §3 | `prompt_lint.py --anchors`；R-BRD-01–R-BRD-21 |
| [`visual-bible.md`](templates/visual-bible.md) | `visual-bible.md` | visual-bible（下游 keyframe-freeze） | — | R-COL-01–R-COL-08 |
| [`storyboard.md`](templates/storyboard.md) | `storyboard.md`（含表演卡） | storyboard-long-take、action-choreography、performance-direction、sound-design | §1 | `segment_rhythm.py`、`dialogue_capacity.py`、`direction_audit.py`；R-SB-01–R-SB-24 |
| [`keyframe-prompt.md`](templates/keyframe-prompt.md) | `keyframe-prompts.md` + `keyframes/REF-SHOTnnn-START.png` | keyframe-freeze、performance-direction | §0.4 ID 规则 | R-KF-01–R-KF-20 |
| [`video-prompt-h3.md`](templates/video-prompt-h3.md) | `video-prompts.md`（Ref2VA 六段 / FL2VA 三段） | video-prompting-h3、performance-direction、sound-design | §2、§2.1 | `h3_frame_grid.py`、`prompt_lint.py`、`direction_audit.py`、`slot_order_check.py`；R-VP-01–R-VP-25 |
| [`edit-list.md`](templates/edit-list.md) | `edit-list.md` | edit-and-assemble、sound-design | §4 | `asset_exists.py`、`psnr_scan.py --mode final`、`loudness_verify.py`；R-CUT-08–R-CUT-13 |
| [`qc-record.md`](templates/qc-record.md) | `qc/SHOT-nnn.md`、`qc/<ASSET-ID>.md` | shot-qc、asset-boards、keyframe-freeze、performance-direction | §6 | `contact_sheet.py`、`psnr_scan.py`、`burnin_text_scan.py`、`transcript_reconcile.py`；R-VID-01–R-VID-23 |
| [`defect-ticket.md`](templates/defect-ticket.md) | `review/defects.md` | screening-review、cold-audience-test、shot-qc | — | 每单必有 Q 维度 + 病灶阶段 + 证据 |
| [`review-memo.md`](templates/review-memo.md) | `review/self-screening.md`、`review/independent-review.md` | screening-review | — | R-CUT-17、R-CUT-18 |
| [`cold-audience-sheet.md`](templates/cold-audience-sheet.md) | `review/cold-audience/viewer-nn.md`、`summary.md` | cold-audience-test | — | R-CUT-19；L1 阈值 |
| [`final-report.md`](templates/final-report.md) | `final-report.md`（第一节 = L0–L3 交付声明） | production-director、screening-review、edit-and-assemble | — | R-CUT-15、R-CUT-16、R-CUT-20 |
| [`publish-kit.md`](templates/publish-kit.md) | `publish-kit.md`（合规表在最前） | publish-prep | — | R-PUB-01–R-PUB-25 |

转写对账输入（`qc/transcripts.tsv` / `.json`）无模板，格式见契约 §5。

## 2. 契约合规（违反即脚本失效）

1. **表头与元数据键逐字照抄**：`段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由`；`CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字`；提示词键 `时长 / 帧数 / 模式 / first_frame / references / 起始帧方位 / 轴线策略 / 锚点 / 角色映射`（+ 可选 `尾部余量 / 步数 / 换边 / 慢动作`）。列顺序可变，多余列忽略，空值写 `—`，单元格内 `|` 写 `\|`。
2. **模式与方言一致**：`模式: Ref2VA` → 六段；`模式: FL2VA` → 三段 + 对齐句 + `references: —`。禁止混用、禁止写 `negative_prompt`。
3. **可选键不用就整行删掉**：`慢动作: 否` 不是豁免；同一镜同名键只认第一条。
4. **方位值用大写英文**：`LEFT / RIGHT / CENTER / FG / BG`；中文会被归一但报 warn。
5. **文件名用英文**（E3-1），一集一个目录，素材放 `assets/`。
6. **改契约 = 同一次提交里改** `format-contracts.md`、`50-rubrics/scripts/`、本目录模板与 fixtures；只改其一视为破坏。

## 3. → 行为改变

下次起任何制作文档时，先从本表找到模板与契约节，复制后再写内容；写完先跑表中脚本到 0 error，再进入下一阶段——禁止先自由写作再"对齐格式"。
