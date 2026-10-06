# 成片验收清单（R-CUT）

> **阶段**：3 后期 → 4 审片 → 交付（`final/epNN.mp4` + `final-report.md` + `review/`）
> **何时跑**：每次渲染出成片之后、交给人类拍板点③之前；重剪、重混、重编号之后整表重跑。
> **通过规则**：本表分两层。
> - **L0 技术层**（R-CUT-01 – R-CUT-15）：全部 `[自动]` 条目 0 error，结果写进 `review/l0-report.json`。只过 L0 的片，交付声明只能写"技术合格（L0），观感未验证"〔委托方实证·F1、F2〕。
> - **交付声明层**（R-CUT-16 – R-CUT-22）：声明到哪一级，就必须有那一级的全部证据文件；缺证据的级别写"未验证"，不能省略〔[`50-rubrics/definition-of-done.md`](../definition-of-done.md)〕。
>
> 交给人类主创审片的最低要求是 L1 + 8 维自评 + 独立评审意见。
> **对应技能**：[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)、[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)、[`20-craft/cold-audience-test/SKILL.md`](../../20-craft/cold-audience-test/SKILL.md)

## 命令串（L0）

```bash
E=season-01/ep03; F=final/ep03.mp4
python3 50-rubrics/scripts/asset_exists.py $E/edit-list.md --stale-token ep02 --json > review/asset_exists.json   # 渲染前
python3 50-rubrics/scripts/loudness_verify.py $F --min 90 --max 110 --json > review/verify.json  # 时长按季圣经；有设计黑场加 --allow-black
python3 50-rubrics/scripts/psnr_scan.py $F --mode final --edit-list $E/edit-list.md --json > review/psnr-final.json
python3 50-rubrics/scripts/burnin_text_scan.py $F --mode final --out-dir review/burnin --json > review/burnin-final.json
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 $F         # 必须 1080,1920
```

## 判据表

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-CUT-01 | 成片整体响度为 -16 LUFS ±1（落在 GY/T 377 的 -15 LKFS ±2 LU 范围内） | [自动] | `review/verify.json` | T-4, S-COMFY-12, F-COMFY-11 | `scripts/loudness_verify.py`（`T4-lufs`） |
| R-CUT-02 | 真峰 ≤ -1 dBTP | [自动] | `review/verify.json` | T-3, S-COMFY-12, F-COMFY-11 | `scripts/loudness_verify.py`（`T4-true-peak`） |
| R-CUT-03 | 交付文件分辨率恰为 1080×1920（严格 9:16）；768×1344 或 480×864 这类中间稿不得作为交付文件 | [自动] | ffprobe 输出 + verify 表 | T-1, T-2, S-H3-02 | `ffprobe`；`scripts/loudness_verify.py`（`T3-aspect`） |
| R-CUT-04 | 有视频流和音频流，两者时长相差 ≤0.2s | [自动] | `review/verify.json` | T-3 | `scripts/loudness_verify.py`（`T3-no-video` `T3-no-audio` `T3-av-duration`） |
| R-CUT-05 | 解码全程没有报错（无坏帧、坏包） | [自动] | `review/verify.json` | T-4, T-3 | `scripts/loudness_verify.py`（`T3-decode-error`） |
| R-CUT-06 | 时长落在季圣经声明的单集区间内（`--min/--max` 来自 `season-bible.md`，不用脚本默认值） | [自动] | verify 表 + 季圣经里的区间 | T-4 | `scripts/loudness_verify.py --min --max`（`T4-duration`） |
| R-CUT-07 | 每段黑场（`T3-black`）、冻结（`T3-freeze`、`P8-freeze`）都能对上剪辑单里的 `local:` 卡或已登记的设计静场；`P8-cut-unexpected`（不在剪辑单切点上的跳变）为 0 或已逐个解释 | [自动]+[目视] | verify 表 + `review/psnr-final.json` + 解释清单 | D2, P8, T-3 | `scripts/loudness_verify.py`（`T3-black` `T3-freeze`）；`scripts/psnr_scan.py --mode final --edit-list`（`P8-cut-unexpected` `P8-freeze-designed`） |
| R-CUT-08 | 剪辑单每个 `来源` 都存在且非空；没有旧集号路径残留；`local:` 写法合法 | [自动] | `review/asset_exists.json` | E2, D2, T-3 | `scripts/asset_exists.py --stale-token`（`E2-missing-asset` `E2-stale-path` `D2-local-syntax`） |
| R-CUT-09 | 纯色卡、片名卡、字卡、AI 标识全部在本地生成、由剪辑叠层；剪辑单里没有任何一条来源是生成器产出的纯色或文字画面 | [自动]+[目视] | 剪辑单逐行核对 | D2, M8 | `scripts/asset_exists.py`（`local:` 语法） |
| R-CUT-10 | 成片 OCR 识别出的每段文字，都能在剪辑单 `字幕` 或 `画面文字` 列逐字找到；没有水印词 | [自动]+[目视] | `review/burnin-final.json` + 逐条对照表 | D1, D2, P7 | `scripts/burnin_text_scan.py --mode final`（`D1-text-final` `D2-watermark`） |
| R-CUT-11 | 剪辑单 `字幕` 列逐字等于分镜 `对白` 列（字幕取自剧本，不取自转写） | [自动] | 两列导出后的 diff 结果为空 | P7, D5, S-ZEN-26 | `diff`（无专用脚本：两列各导出为逐行文本后比对） |
| R-CUT-12 | `psnr_scan` 成片模式没报 `A1-mean-short`；如果报了，每个 <5s 的 CUT 都能在剪辑单里指向一条 ≥124 帧生成镜的取段（快剪取自长镜，而不是碎镜生成） | [自动]+[目视] | `review/psnr-final.json` + 剪辑单来源对照 | A1, P10, S-STORY-19 | `scripts/psnr_scan.py --mode final`（`A1-mean-short` `A1-shot-stats`） |
| R-CUT-13 | 每个来自生成镜的 CUT，出点都早于该镜的尾部崩解窗（出点 ≤ 镜长 − 声明的 `尾部余量`） | [自动]+[目视] | 剪辑单出点 vs 提示词 `时长`、`尾部余量` 对照表 | P8, F-H3-18 | 无专用脚本：对照 `video-prompts.md` 元数据 |
| R-CUT-14 | 每个切点前后各 2 帧已导出目视，没有闪帧、跳帧、误剪 | [目视] | `review/cuts/` 切点帧拼图 | P8 | ffmpeg `select` + `tile`（时间码取自 `review/psnr-final.json`） |
| R-CUT-15 | `review/l0-report.json` 存在，逐条列出 R-CUT-01 – R-CUT-13 中 `[自动]` 部分的结果和证据文件 | [自动] | `review/l0-report.json` | T-3, F2 | `test -s review/l0-report.json` |
| R-CUT-16 | `final-report.md` 第一节是交付声明，写明达到的级别、各级证据路径、未验证项；只有 L0 证据时，全文不出现"达标""可发布""质量通过" | [自动]+[目视] | `final-report.md` + grep 结果 | F1, F2 | `grep -n -e 达标 -e 可发布 -e 质量通过 final-report.md`（无专用脚本） |
| R-CUT-17 | `review/self-screening.md` 存在，写于打开任何制作文档之前，字段齐全：观看方式（1×、不暂停、只开成片）、第一次困惑的时间码、第一次想划走的时间码、主因果链复述（谁想要什么 → 阻碍 → 做了什么 → 结果） | [目视] | `review/self-screening.md` | F1, G4 | — |
| R-CUT-18 | `review/independent-review.md` 由隔离会话产出：首行列出输入清单，并声明"未见生成提示词、修改轮次、指标面板、作者通过理由"；每条意见含时间码、证据、严重度；至少含 1 道幻觉探针（问一个确定不存在的物体），评审答"有"则整份作废重做 | [目视] | `review/independent-review.md` | F1, S-ZEN-12, S-CASE-29 | — |
| R-CUT-19 | 交付声明 ≥ L1 时，`review/cold-audience/` 有 ≥3 份记录，≥2/3 正确复述主因果链，没有断点被 ≥2 人同时标记；用 agent 替身测试的，声明里写明"替身测试，置信度降级" | [冷观众] | `review/cold-audience/*.md` | GAP-2, F1 | — |
| R-CUT-20 | 交付声明 = L2 时，`review/quality-scorecard.md` 的 Q1–Q8 每维 ≥2，每个分数都附证据时间码；阻断缺陷表每一行都填了"无"或"已修复 + 复评证据" | [目视] | `review/quality-scorecard.md` | F3, F2, B1, A5 | — |
| R-CUT-21 | 交付声明 = L2 时，[`50-rubrics/checklists/publish.md`](publish.md) 的合规行 R-PUB-01 – R-PUB-16 全部为真，或未确认项已上报人类拍板点④ | [目视] | `publish-kit.md` 合规表 | GAP-1, S-PLAT-01, S-PLAT-02 | — |
| R-CUT-22 | 审片包里引用的接触表、截图、帧拼图都存在且非空 | [自动] | asset_exists 报告 | F1, C2 | `scripts/asset_exists.py review/`（`E2-missing-ref` `E2-empty-asset`） |

## 常见误判

- **"verify 全绿 = 可以交付"**：委托方的 check、render、verify 一直是全绿，人类主创照样连续打回〔T-4〕。L0 是下限，不是结论。R-CUT-16 专门拦这句话。见 [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)。
- **480×864 剪辑稿直接交付**：480×864 实为 5:9，`loudness_verify.py` 会按 `T3-aspect` 拦下（R-CUT-03）。中间稿只能用于预览。
- **自我放映前先读了分镜**：读过分镜再看片，脑子会自动补全因果，困惑点就消失了。自我放映必须先写，再打开文档（R-CUT-17）。见 [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md)。
- **独立评审拿到了提示词**：评审看过提示词，就会"看到"提示词里写了、画面里没有的东西。输入清单必须声明隔离，并加一道幻觉探针（R-CUT-18）。
- **字幕从转写复制**：转写会误听、幻听；字幕必须逐字取自剧本（R-CUT-11）。见 [`60-casebook/cards/D5-qc-tools-lie.md`](../../60-casebook/cards/D5-qc-tools-lie.md)。
- **平均镜长报警就合并 CUT**：病不在"剪得快"，在"一个动作一个镜号"。只要每个短 CUT 都取自长镜，快剪是合法的（R-CUT-12）。见 [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)。

## → 行为改变

下次写 `final-report.md`，先填交付声明，再按声明的级别逐行勾本表。勾不满的行，把声明降一级，不改措辞绕过去。
