# 视频镜头验收清单（R-VID）

> **阶段**：2 制作 · 镜头级 QC（每条 H3 生成镜，验收通过才进剪辑单）
> **何时跑**：每条出片之后、写进 `edit-list.md` 之前；换 seed、换提示词后，新版本从头重跑。
> **通过规则**：本表全部行为真。`[自动]` 行以脚本 0 error 为下限，脚本报出的每条 `visual` 都必须有目视结论写进 `qc/<SHOT-nnn>.md`。**单通道不判决**：转写说缺句、PSNR 说跳变、OCR 说有字，这些都要有第二通道证据（抽帧或听感）才能下"重出"结论〔委托方实证·D5、M10〕。脚本全绿只说明没出错，不说明好看〔委托方实证·F2〕。
> **证据放哪**：统一用 `--out-dir qc/SHOT-nnn`，文件名按脚本实际产出写，见 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §6。
> **对应技能**：[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md) ｜ 理论：[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)

## 一镜一遍的命令串（按顺序）

```bash
S=SHOT-004; C=assets/clips/$S.mp4; O=qc/$S
python3 50-rubrics/scripts/contact_sheet.py $C --keyframe assets/keyframes/REF-SHOT004-START.png --out-dir $O \
        --crop face=180:220:160:160          # 有人物就裁脸；多人每人一组 --crop
python3 50-rubrics/scripts/psnr_scan.py $C --json > $O/$S.psnr.json
python3 50-rubrics/scripts/burnin_text_scan.py $C --out-dir $O --json > $O/$S.burnin.json
python3 50-rubrics/scripts/transcript_reconcile.py --storyboard storyboard.md --prompts video-prompts.md \
        --transcripts qc/transcripts.tsv --json > $O/$S.tr.json      # 有可疑项再加 --windows
python3 50-rubrics/scripts/asset_exists.py qc/                         # 证据文件都在、非空
```

## 判据表

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-VID-01 | 本镜有接触表：起始关键帧在第 1 格，包含 FIRST、MID、TAIL（最后 0.5s）格；每一格的目视结论已写进 `qc/<SHOT>.md` | [自动]+[目视] | `qc/<SHOT>/<SHOT>.contact.jpg`、`.contact.json` + 逐格结论 | P8, B4 | `scripts/contact_sheet.py --keyframe`（`P8-contact-sheet` `B4-keyframe`） |
| R-VID-02 | 看视频之前，记录里已经写好"背景元素清单"（关键帧里每个显著元素及数量，如"骨架×1、石柱×2、火把×0"）；FIRST、MID、TAIL 各格按清单计数，每项都没有变化 | [目视] | 清单 + 每格计数表 | B4, P8 | `scripts/contact_sheet.py --keyframe`（`B4-keyframe`） |
| R-VID-03 | TAIL 格没有崩解（噪声色块、形体融化）；如果尾部有崩解，生成时长里已含 1.3–1.5s 尾部余量，并且剪辑出点早于崩解起点 | [目视] | TAIL 格 + 崩解起点时间码 + 计划出点 | P8, S-H3-09, F-H3-18 | `scripts/contact_sheet.py`（尾部格橙框） |
| R-VID-04 | 画面有 ≥2 人时，按人逐张导出脸部裁剪表，任意两张脸都不雷同（没有克隆脸） | [目视] | 每人一组 `<SHOT>.crop-<名>.jpg` | B3, S-PLAT-07 | `scripts/contact_sheet.py --crop`（`C2-crop`） |
| R-VID-05 | 主角脸部裁剪表的每一格，与板图同尺寸裁脸并排后都是同一个人（没有身份漂移，比如变成"粗犷成熟脸"） | [目视] | `<SHOT>.crop-face.jpg` + 与板图并排图 | B1, P5, M7 | `scripts/contact_sheet.py --crop`（`C2-crop`） |
| R-VID-06 | `burnin_text_scan.py` 没报 `D1-burnin-text`、`D2-watermark`；报出的每个 `visual` 都已打开条带图看过并写结论；报 `D1-ocr-degraded` 时，记录里写明"OCR 未启用，启发式 + 目视" | [自动]+[目视] | `<SHOT>.burnin.json` + `.burnin-strip.jpg` + 结论 | D1, D2, D5 | `scripts/burnin_text_scan.py`（`D1-burnin-text` `D2-watermark` `D1-heuristic-*` `D1-ocr-degraded`） |
| R-VID-07 | 接触表全部格子（含 TAIL）都没有任何文字、字幕或水印。这是 R-VID-06 的第二通道，两行都为真才算无烧录 | [目视] | 接触表逐格结论 | D1, D5, P8 | `scripts/contact_sheet.py` |
| R-VID-08 | `psnr_scan.py` 报出的每个 `P8-freeze`（死段）已经解释为设计静场，或者剪掉、重出；每个 `P8-jump`（镜内跳变）已在接触表或补抽帧中定位，并判定为崩解、换景或合法的快动作之一 | [自动]+[目视] | `<SHOT>.psnr.json` + 每个时间码的判定 | P8, D5 | `scripts/psnr_scan.py --mode clip`（`P8-freeze` `P8-jump` `P8-low-baseline`） |
| R-VID-09 | 台词三方对账没有 `TR-script-prompt`、`TR-speaker` error；报 `TR-missing` 的句子，只有在 `--windows` 三窗结果和口型接触表 `lips.jpg` 都齐了之后才判"真缺句" | [自动]+[目视] | `<SHOT>.tr.json` + `qc/<SHOT>/w1–w3` 转写 + `lips.jpg` | P7, M10, D3, D5 | `scripts/transcript_reconcile.py`（`TR-script-prompt` `TR-speaker` `TR-missing`；`--windows`） |
| R-VID-10 | 无对白镜出现转写（`TR-unscripted`、`TR-hallucination`）时，先用 ffprobe 确认有没有音轨、用 `volumedetect` 量能量，**不**据此重出；字幕永远逐字取自剧本 | [自动]+[目视] | ffprobe / volumedetect 输出 + 结论 | D5, S-COMFY-16, F-COMFY-15 | `scripts/transcript_reconcile.py`（`TR-unscripted` `TR-hallucination` `TR-no-audio`） |
| R-VID-11 | 记录里每个"重出""缺句""误听"结论，都同时引用转写证据和抽帧或听感证据两份文件 | [目视] | 两份证据文件路径 | D5, M10 | — |
| R-VID-12 | 换过 seed 后，同一句台词仍然缺失（或每个 seed 缺不同的句），这一镜已经判为结构性缺陷，退回分镜按容量重算时长或删句，不再继续换 seed | [目视] | 各 seed 的缺句对照 + 回分镜的缺陷单号 | D3, P9, M5 | `scripts/dialogue_capacity.py`（回分镜重算，`D3-capacity`） |
| R-VID-13 | 多人对白镜里，不说话的人在对方台词时段嘴部闭合（口型没有落到错的人身上） | [目视] | 非说话人的 `--crop mouth` 裁剪表 + 台词时段 | S-ZEN-17, F-ZEN-08 | `scripts/contact_sheet.py --crop`（`C2-crop`） |
| R-VID-14 | 全程每个人物的画面左右位置与起始帧方位一致，段内没有无理由的换边、绕行或"乱跑" | [目视] | 接触表逐格标出左右 + 结论 | A5, M4 | `scripts/contact_sheet.py` |
| R-VID-15 | 动作镜按实时速度发生：没有 `慢动作: 设计选择` 声明的镜，摔倒、挥击、扑跃等事件里没有漂浮式慢放 | [目视] | 动作区间的补抽帧（每 0.25s）+ 结论 | A3, S-H3-11, F-H3-23 | ffmpeg `fps=4,tile`（无专用脚本） |
| R-VID-16 | 锚点卡的禁用项在 MID、TAIL 格的放大裁剪里也都不存在（视频生成会在中后段把装饰物加回来） | [目视] | 每条禁用项一组裁剪 | C1, C2 | `scripts/contact_sheet.py --crop`（`C2-crop`） |
| R-VID-17 | 分镜 `运镜因果` 句里的事件 X 在接触表中可见，镜头动作 Y 恰好发生在 X 那一刻；没有运镜或方向不符，就判这一行不通过 | [目视] | 因果句 + X 与 Y 的时间码 | A4, F2 | `scripts/contact_sheet.py` |
| R-VID-18 | 记录里有一行"提示词 ↔ 产出差异"，逐条列出不一致处，每条结论只能是"已回写"或"已拒绝"；这条产出如果要当后续镜的参考图，必须已回写 | [目视] | 差异行 + 提示词 diff | E4, P5 | `git diff video-prompts.md` |
| R-VID-19 | 生成日志记下模式（Ref2VA / FL2VA）、seed、steps、是否 turbo；定稿版不是 4-step turbo 或 ≤8 步的预览产出 | [目视] | 生成日志参数行 | S-H3-04, F-H3-09, B4 | `scripts/prompt_lint.py`（`VP-steps`，查提示词元数据） |
| R-VID-20 | 高风险镜（多人、复杂背景、打斗、BOSS）至少有 3 个 seed 的接触表并排选优，落选版归档 | [目视] | 各 seed 接触表 + 选中理由 | B4, P2, M6 | `scripts/contact_sheet.py`（逐 seed 运行） |
| R-VID-21 | 单镜画幅偏离 9:16 不超过 2% | [自动] | contact_sheet 报告 | T-2, S-H3-02 | `scripts/contact_sheet.py`（`T2-aspect`） |
| R-VID-22 | 提示词写了 `non_diegetic_music: N/A` 的镜，听感里没有配乐；有配乐就记为生成偏差，后期剥不掉时重出 | [目视] | 听感记录（时间码） | F-ZEN-07, S-ZEN-09, GAP-6 | — |
| R-VID-23 | `qc/<SHOT>.md` 引用的每个证据文件都存在且非空 | [自动] | asset_exists 报告 | C2, E2 | `scripts/asset_exists.py qc/`（`E2-missing-ref` `E2-empty-asset`） |

## 常见误判

- **"转写说缺了'救我'，重出"**：单次转写会误听，也会在静音上编造句子。委托方实际遇到过"字幕by索兰娅"和把低笑听成"救我"。先做三窗复核加口型接触表再下结论（R-VID-09、R-VID-11）。见 [`60-casebook/cards/D5-qc-tools-lie.md`](../../60-casebook/cards/D5-qc-tools-lie.md)。
- **OCR 没报字就当无烧录**：没有 OCR 后端时，脚本只能做启发式；小水印在启发式下会漏报。R-VID-06 和 R-VID-07 两条都要为真。见 [`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md)。
- **只看 FIRST 和 MID**：H3 常在片尾前 1.2–1.7s 崩解（F-H3-18），"第二骨架"这类伪影也可能只在中后段出现。TAIL 格和背景元素清单必须逐格核（R-VID-02、R-VID-03）。见 [`60-casebook/cards/B4-duplicate-artifacts.md`](../../60-casebook/cards/B4-duplicate-artifacts.md)。
- **缺句就换 seed 碰运气**：换 seed 每次缺不同的句，说明这是容量问题，不是随机问题（R-VID-12）。见 [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md)。
- **产出比提示词好，就直接收**：收下之前先把提示词回写成产出的事实，否则下一次重出、下一镜参考都会自相矛盾（R-VID-18）。见 [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)。
- **把 `P8-jump` 当切点放过**：单个生成镜里本不该有切点；镜内跳变要么是崩解，要么是生成器自己换了景。两种都要定位到具体时间码（R-VID-08）。

## → 行为改变

下次验收一条视频，先写背景元素清单、填好本镜的方位与运镜因果，**再**打开接触表。先看再写清单，眼睛会替生成器圆场。
