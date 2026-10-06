# 检查脚本（50-rubrics/scripts/）

> 这些脚本把委托方真实踩过的坑变成可执行检查。**脚本只报事实、不下审美判决**：数字、位置、与契约的偏差、下一步动作；凡需要"看"的地方，脚本产出证据文件并报 `visual`（需目视），结论由 agent 亲自看完写进 `qc/<SHOT-nnn>.md`。技术全绿 ≠ 可发布（F1/F2）。
> 输入格式一律以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) 为准；脚本公约见 [`CONVENTIONS.md`](../../CONVENTIONS.md) §8。共享解析在 `academy_common.py`。

## 1. 脚本一览

| 脚本 | 阶段 | 用途 | 溯源 | 典型命令 | 主要规则代码 |
|---|---|---|---|---|---|
| `segment_rhythm.py` | 设计 | 分镜 段/拍/镜 节奏结构：短镜无理由、超 362 帧、拍数过多、运镜因果句、碎镜均长 | A1, A4, A5, P10, M1, T-2 | `python3 segment_rhythm.py ep03/storyboard.md` | `A1-short-no-reason` `A1-mean-short` `T2-over-max` `A4-cause` `A5-beats-many` `P10-*` |
| `dialogue_capacity.py` | 设计 | 对白容量：7.5 字/秒容量上限（error）+ 自然语速 4.1 字/秒规划检查（warn）；两文档台词/时长对账；认 `尾部余量` | D3, P9, M5, T-2, P7, F-ZEN-05 | `python3 dialogue_capacity.py --storyboard ep03/storyboard.md --prompts ep03/video-prompts.md` | `D3-capacity` `D3-margin` `D3-split` `D3-tight` `D3-rushed` `D3-stagger` `P7-*` |
| `h3_frame_grid.py` | 提示词 | H3 帧网格 17k+5（124–362 帧）换算与校验；超上限给拆段方案 | T-2, A1 | `python3 h3_frame_grid.py --check ep03/video-prompts.md`；`--seconds 10.3` | `T2-frames-offgrid` `T2-frames-below-min` `T2-frames-above-max` `T2-duration-mismatch` `FMT-shot-heading` |
| `prompt_lint.py` | 提示词 | 送 H3 前硬约束：模式与方言（Ref2VA 六段 / FL2VA 三段）、禁令包末行、实时速度句、`<Picture N>`、锚点句逐字、对白标记、差异化句、闭嘴句、配乐 N/A、步数、生成器不该做的事 | D1, D2, D4, A3, A5, B2, B3, C1, P1, M3, M8, T-2, F-H3-09/11, F-ZEN-07/08 | `python3 prompt_lint.py ep03/video-prompts.md --anchors ep03/anchors.md --storyboard ep03/storyboard.md` | `VP-mode` `VP-struct` `VP-ban` `VP-realtime` `VP-picture` `VP-anchor` `VP-dialogue` `VP-distinct` `VP-lipsync` `VP-music` `VP-steps` `VP-scaffold` `VP-sync` `VP-frames` |
| `direction_audit.py` | 提示词 | 方位词全量审计：相机左右运动 vs 轴线策略、主体左右 vs 起始帧方位、绕行路径 | A5, M4, P4, P7, C1-6 | `python3 direction_audit.py ep03/video-prompts.md --storyboard ep03/storyboard.md` | `DIR-camera` `DIR-side` `DIR-path` `DIR-check` `DIR-layout` `DIR-mapping` `DIR-axis` |
| `slot_order_check.py` | 提示词 | 参考槽编号 1 起连续、占位槽在末位、删占位模拟、绑定列表与 references 一致 | E1, T-3, P4, T-2 | `python3 slot_order_check.py ep03/video-prompts.md --simulate-remove-placeholder --assets-dir ep03/assets` | `SLOT-contiguous` `SLOT-placeholder-pos` `SLOT-sim` `SLOT-first-frame` `SLOT-bind-mismatch` |
| `contact_sheet.py` | 媒体 | 抽帧接触表（必含首/中/最后 0.5s）、关键帧并排、区域放大裁剪；单镜画幅 >2% 偏离 9:16 → warn | P8, B4, D1, C2, C1-7 | `python3 contact_sheet.py SHOT-004.mp4 --keyframe REF-SHOT004-START.png --out-dir qc/SHOT-004` | `P8-contact-sheet` `B4-keyframe` `C2-crop` `T2-aspect` `P8-unreadable` |
| `psnr_scan.py` | 媒体 | 相邻帧 PSNR：死段/冻结、镜内跳变、成片切点（可与剪辑单对齐） | P8, A1, D5 | `python3 psnr_scan.py SHOT-004.mp4 --json > qc/SHOT-004/SHOT-004.psnr.json`；`--mode final --edit-list ep03/edit-list.md` | `P8-freeze` `P8-jump` `P8-cut-*` `A1-mean-short` |
| `burnin_text_scan.py` | 媒体 | 烧录字幕/文字水印扫描：有 OCR 用 OCR，无 OCR 明确降级为启发式 + 目视 | D1, D2, P8, D5 | `python3 burnin_text_scan.py ep03/assets/clips/ --out-dir qc/burnin --json` | `D1-burnin-text` `D1-heuristic-*` `D1-ocr-degraded` `D2-watermark` |
| `transcript_reconcile.py` | 媒体 | 台词三方对账（分镜 ↔ `<d>` ↔ 转写），多窗复核、已知 ASR 幻觉；绝不仅凭转写下重出结论 | P7, M10, D3, D5, P8 | `python3 transcript_reconcile.py --storyboard sb.md --prompts vp.md --transcripts qc/transcripts.tsv --windows` | `TR-missing` `TR-script-prompt` `TR-speaker` `TR-hallucination` `TR-lowconf` `TR-no-audio` |
| `asset_exists.py` | 成片 | 剪辑单素材存在性、旧集号路径残留、行尾审计、字节级改名预演/执行 | E2, D2, T-3 | `python3 asset_exists.py season-01/ --stale-token ep03`；`--rename ep03 ep04 [--apply]` | `E2-missing-asset` `E2-stale-path` `E2-stale-token` `E2-crlf` `D2-local-syntax` |
| `loudness_verify.py` | 成片 | 成片 verify：响度 -16 LUFS±1、真峰、画幅 9:16（>1% → error）、音视频流、黑场、冻结、坏帧 | T-3, T-4, T-2, F2 | `python3 loudness_verify.py final/ep03.mp4 --min 90 --max 110` | `T4-lufs` `T4-true-peak` `T3-aspect` `T3-decode-error` `T3-black` `T3-freeze` |
| `run_all_selftests.py` | 全部 | 汇总运行以上全部 `--selftest`；`--quick` 跳过媒体类并明确列为 SKIP；缺 ffmpeg 时媒体类记 SKIP 并写原因 | CONVENTIONS §8 | `python3 run_all_selftests.py [--quick] [--json]` | PASS / FAIL / SKIP |

每个脚本的完整规则表、参数与容错口径见其 `--help`（即文件头 docstring）。

## 2. 规则代码族

| 前缀 | 含义 | 出处 |
|---|---|---|
| `FMT-*` | 文档格式偏离契约（BOM、表头笔误、镜头标题不合 `## SHOT-nnn`、值写法、镜号重复…）；脚本已尽量按值继续检查，但偏差照报 | 各脚本 |
| `T2-*` | H3 技术约束：帧网格、时长、单次上限、单镜画幅 | T-2 |
| `T3-*` / `T4-*` | 成片 verify：流、画幅、坏帧、黑场、冻结 / 响度、真峰、时长 | T-3、T-4 |
| `A1-*` | 碎镜症：短镜、均长 | A1 |
| `A4-*` `A5-*` | 运镜因果 / 空间调度（拍数过多） | A4、A5 |
| `P7-*` `P8-*` `P10-*` | 双文档对账 / 视频验收证据 / 长段多拍 | P7、P8、P10 |
| `D1-*` `D2-*` `D3-*` | 烧录文字 / 纯色卡与水印 / 对白容量（含 `D3-rushed` 自然语速规划） | D1、D2、D3 |
| `E2-*` | 路径残留、改名、行尾 | E2 |
| `B4-*` `C2-*` | 关键帧比对 / 放大裁剪证据 | B4、C2 |
| `VP-*` | 视频提示词（prompt_lint） | 见 prompt_lint 头部 |
| `DIR-*` | 方位词审计（direction_audit） | A5、M4 |
| `SLOT-*` | 参考槽顺序（slot_order_check） | E1 |
| `TR-*` | 台词三方对账（transcript_reconcile） | P7、M10、D5 |

级别：`error`（必须修，退出码 1）/ `warn`（偏差或风险，不改退出码）/ `info`（事实）/ `visual`（需目视：打开证据文件逐项看，结论写进验收记录）。

## 3. 退出码与输出

- `0` 通过（没有 error）/ `1` 发现 error / `2` 用法或环境错误（文件不存在、缺 ffmpeg 或必需滤镜、参数非法、输出写不出）。
- 默认输出人类可读报告；`--json` 输出机器可读结果（`ok`、`counts`、`findings`，外加各脚本的附加字段）。
- 输出在非 UTF-8 控制台（Windows cmd/GBK，E3-1）下不会因图标崩溃：无法编码的字符替换为 `?`。
- 全部输入一律按 UTF-8（容忍 BOM）读；带 BOM 会报 `FMT-bom` 让你去掉。

## 4. 证据文件放哪里

统一放在本集 `qc/<SHOT-nnn>/` 下（命名见 [`format-contracts.md` §6](../../70-playbooks/format-contracts.md)）：

- `contact_sheet.py ... --out-dir qc/SHOT-004` → `SHOT-004.contact.jpg`、`SHOT-004.contact.json`；加 `--crop face=…` → `SHOT-004.crop-face.jpg` 与 `SHOT-004.crops/face/f<帧号>_t<秒>.png`。不给 `--out-dir` 时写在视频旁。
- `psnr_scan.py` 不写文件：`--json > qc/SHOT-004/SHOT-004.psnr.json`。
- `burnin_text_scan.py --out-dir qc/burnin` 写底部条带接触图 `<视频名>.burnin-strip.jpg`；`transcript_reconcile.py --windows` 打印的复核命令把 `w1/w2/w3.wav`、`lips.jpg` 写到 `qc/<SHOT>/`。
- 其他脚本的报告用 `--json > qc/<脚本名>.json` 留档。

## 5. 按生产阶段串联

**生成前（每镜送 H3 之前，全部 0 error 才进 prepare）**

1. `segment_rhythm.py storyboard.md` —— 段/拍/镜结构先站住（短镜、超长、拍数、运镜因果）。
2. `dialogue_capacity.py --storyboard storyboard.md --prompts video-prompts.md` —— 时长装得下台词；`D3-rushed` 提示按自然语速会很赶。
3. `h3_frame_grid.py --check video-prompts.md` —— 帧数落网格、与时长一致。
4. `prompt_lint.py video-prompts.md --anchors anchors.md --storyboard storyboard.md` —— 模式/方言、禁令包、锚点、对白、闭嘴句等。
5. `direction_audit.py video-prompts.md --storyboard storyboard.md` —— 方位词审计通过才算定稿。
6. `slot_order_check.py video-prompts.md --simulate-remove-placeholder` —— 参考槽顺序（改 references / 导出绑定后必跑）。

**生成后（每条出片，验收前）**

7. `contact_sheet.py <clip> --keyframe <REF-SHOTnnn-START> --out-dir qc/<SHOT>` —— 逐格目视（文字、克隆、穿模、尾部崩解、背景元素）。
8. `psnr_scan.py <clip> --json > qc/<SHOT>/<SHOT>.psnr.json` —— 死段/镜内跳变；跳变回接触表复核（D5 双通道）。
9. `burnin_text_scan.py <clip>` —— 烧录文字/水印。
10. `transcript_reconcile.py --storyboard … --prompts … --transcripts …` —— 缺句/多字/串台；可疑处 `--windows` 多窗复核 + 口型接触表。

**成片（渲染前后）**

11. `asset_exists.py <剪辑单或本季目录>` —— 渲染前素材全在、无旧集号残留。
12. `loudness_verify.py final/epNN.mp4` —— verify 表（响度、真峰、画幅 1080×1920 / 9:16、坏帧、黑场、冻结）。

维护者：改契约 = 同一次提交里改 `format-contracts.md`、脚本、模板与 fixtures；提交前跑 `python3 50-rubrics/scripts/run_all_selftests.py` 与 `python3 tools/academy_lint.py`。
