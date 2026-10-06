---
name: shot-qc
description: 对每条 H3 出片做镜头级验收并留下可复核证据：先写背景元素清单，再跑接触表（首/中/尾 0.5s 与起始关键帧并排）、PSNR 扫描、烧录文字扫描、台词三方对账，按人导出放大裁剪与板图并排查漂移、克隆脸、禁用项，判定缺陷是随机（换 seed）还是结构性（回上游改设计），最后写 qc/SHOT-nnn.md。Use when a generated clip comes back, before a shot enters the edit list, or when a QC script reports findings. 触发词：镜头验收、抽帧、接触表、尾部崩解、烧录字幕、PSNR、转写对账、克隆脸、穿帮、换seed还是改设计、QC记录、shot QC, contact sheet, tail collapse, burned-in text, transcript check, clone face, reroll or redesign。不负责提示词写作（video-prompting-h3）、成片级 verify（edit-and-assemble）、全片观感评分（screening-review）。
---
# 镜头级验收（shot-qc）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。证据命名以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §6 为准。铁律：**脚本只报事实，结论由你看完证据文件后写；"通过"两个字不是验收记录**〔委托方实证·C2、D5〕。

## 何时用 / 何时不用

- **用**：每条出片（含每个 seed）进入剪辑单之前；改提示词重出之后；独立评审或冷观众指向某镜时复查。
- **用**：高风险镜（多人、复杂背景、打斗、BOSS）——至少 3 个 seed 并排比较后再选（R-VID-20）。
- **不用**：判断"这一镜在全片里好不好看、节奏对不对"——那是 screening-review；本技能只判"这颗镜是否忠实、无缺陷"。
- **不用**：成片响度、画幅、素材存在性——那是 edit-and-assemble 的 verify。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| `SHOT-nnn.mp4`（每个 seed）、`REF-SHOTnnn-START.png` | `qc/SHOT-nnn/SHOT-nnn.contact.jpg` + `.contact.json`、`.crop-<区域>.jpg`、`.psnr.json` | 命名见 format-contracts §6 |
| `video-prompts.md`、`storyboard.md`、`anchors.md`、板图 | `qc/SHOT-nnn.md` 验收记录（结论 / 证据 / 逐条 R-VID / 提示词↔产出差异 / 生成日志） | [`70-playbooks/templates/qc-record.md`](../../70-playbooks/templates/qc-record.md) |
| 转写 `qc/transcripts.tsv` | 对账结论（双通道） | format-contracts §5 |
| 结构性缺陷 | 缺陷单（回流到病灶阶段） | [`70-playbooks/templates/defect-ticket.md`](../../70-playbooks/templates/defect-ticket.md) |

## 步骤

1. **先写背景元素清单，再看视频**：打开起始关键帧，在 `qc/SHOT-nnn.md` 写下每个显著元素及数量（"骨架×1、石柱×2、火把×0"）和锚点卡禁用项。先写后看，防止"看到什么就认什么"。验：R-VID-02。〔委托方实证·B4、C2〕
2. **接触表（含尾部）**：`python3 50-rubrics/scripts/contact_sheet.py SHOT-nnn.mp4 --keyframe REF-SHOTnnn-START.png --out-dir qc/SHOT-nnn`。起始关键帧在第 1 格，必须含 FIRST / MID / 最后 0.5s（TAIL）。逐格对照背景清单：元素增减（`B4-keyframe`）、文字、穿模、形体融化。TAIL 崩解（噪声色块）→ 查生成时长是否含 1.3–1.5s 尾部余量，并把崩解起点写进记录供剪辑出点使用。验：R-VID-01、R-VID-03、R-VID-07、R-VID-21（`T2-aspect`）。〔委托方实证·P8；外部调研·S-H3-09〕
3. **放大裁剪 vs 板图**：`--crop face=x:y:w:h`（每个人一个区域，另加禁用项所在区域，如 `--crop guard=…`）。主角脸裁剪与板图同尺寸并排逐特征比（脸型、眉、发际、疤）；禁用项在 MID、TAIL 的裁剪里也必须不存在。验：R-VID-05、R-VID-16；`C2-crop` 报 visual = 必须打开 `.crop-*.jpg` 看。〔委托方实证·C1、C2、B1〕
4. **克隆脸检查**：画面 ≥2 人 → 按人导出脸部裁剪表，两两比较；任意两张雷同 = 阻断（平台已把高频 AI 脸列为治理对象）。验：R-VID-04。〔委托方实证·B3；外部调研·S-PLAT-07〕
5. **PSNR 扫描**：`python3 50-rubrics/scripts/psnr_scan.py SHOT-nnn.mp4 --json > qc/SHOT-nnn/SHOT-nnn.psnr.json`。每个 `P8-freeze` 解释为设计静止或判缺陷；每个 `P8-jump` 回接触表找对应帧目视——PSNR 跳变可能是合法闪光，也可能是镜内瞬移（双通道，D5）。验：R-VID-08。
6. **烧录文字**：`python3 50-rubrics/scripts/burnin_text_scan.py SHOT-nnn.mp4 --out-dir qc/burnin --json`。报 `D1-ocr-degraded` = 无 OCR，必须逐格目视底部条带接触图。任何字幕、水印、乱码字 = 不通过（禁令包只是兜底，竖屏更易出字〔外部调研·S-VGEN-11、S-H3-13〕）。验：R-VID-06、R-VID-07。
7. **台词三方对账（双通道）**：`python3 50-rubrics/scripts/transcript_reconcile.py --storyboard storyboard.md --prompts video-prompts.md --transcripts qc/transcripts.tsv --windows`。任何"缺句 / 多字 / 误听 / 串台"结论必须同时引用 ①转写 ②口型接触表 `lips.jpg` 或亲耳复听；无对白镜出现转写（`TR-hallucination`）先按 ASR 幻觉处理，静音段幻觉是已知现象〔外部调研·S-COMFY-14、S-COMFY-16、S-CASE-28〕。多人镜目视非说话人嘴部闭合。验：R-VID-09、R-VID-10、R-VID-11、R-VID-13。
8. **方位、速度、运镜兑现**：首 / 中 / 末格人物左右与 `起始帧方位` 一致（R-VID-14）；动作按实时速度（R-VID-15）；`运镜因果` 句里的事件 X 在接触表可见且镜头随之响应（R-VID-17）；写了 `non_diegetic_music: N/A` 的镜听不到配乐（R-VID-22）。
9. **提示词 ↔ 产出差异行**：逐条列出产出与提示词不一致处；选用这一条 → 把提示词回写为产出的事实，参考图与提示词必须是同一事实（format-contracts §7）。验：R-VID-18。〔委托方实证·E4〕
10. **随机 vs 结构判定**（决定下一步动作，写进记录）：
    - 同一缺陷只在部分 seed 出现、位置不固定 → **随机缺陷**：换 seed 重出（高风险镜 ≥3 seed 并排选）。
    - 换 ≥2 个 seed 后同一缺陷仍在，或每个 seed 缺的东西不同但总量不变（如台词总缺）→ **结构性缺陷**：禁止继续抽卡，开缺陷单回病灶阶段（缺句 → 分镜时长；方位乱 → 起始帧 / 分镜；禁用项 → 锚点句 / 板图；尾部崩解 → 时长余量）。验：R-VID-12；路由依据 [`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3。〔委托方实证·D3、F3〕
11. **写 QC 记录**：`qc/SHOT-nnn.md` 首行 `# QC SHOT-nnn · seed N · 日期`；结论只能是 通过 / 不通过 / 有条件通过（写明条件，如"出点 ≤ 8.40s"）；每行 R-VID 写结果 + 证据文件名；记录生成日志：模式（Ref2VA / FL2VA）、seed、steps、是否 turbo（R-VID-19）。高风险资产写"复验人：独立评审会话"。验：R-VID-23（引用的证据文件都存在且非空）——`ls -s qc/SHOT-nnn/` 核对。
12. **同类搜索**：本镜发现的缺陷类型，在本集其他镜的接触表里搜一遍（例：一镜出字幕 → 全集跑 `burnin_text_scan.py ep03/assets/clips/`），结果写"已搜，无"或镜号列表。

## 判据

- 证据完整：R-VID-01、R-VID-02、R-VID-23、R-VID-19、R-VID-20。
- 画面：R-VID-03（尾部）、R-VID-04（克隆）、R-VID-05（漂移）、R-VID-06/07（文字）、R-VID-14（方位）、R-VID-15（实时速度）、R-VID-16（禁用项）、R-VID-17（运镜兑现）、R-VID-21（画幅）。
- 声音：R-VID-09、R-VID-10、R-VID-11、R-VID-12、R-VID-13、R-VID-22。
- 诚实：R-VID-18（提示词回写为事实）、R-VID-08（PSNR 发现逐条解释）。
- 质量维度：本技能直接守 **Q7 一致性与连续性**、**Q5 美术与密度**（文字 / 伪影）、**Q2 空间与调度**（方位）、**Q8 声音与对白**（缺句）；阻断缺陷表（definition-of-done §3）中的漂移、克隆、自加文字、缺句、禁用项都在这里第一次被拦。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| "看过了没问题"，事后被人类指出禁用项 | [`60-casebook/cards/C2-lenient-acceptance.md`](../../60-casebook/cards/C2-lenient-acceptance.md) | 步骤 1 先写清单；步骤 3 放大裁剪；结论必须挂证据文件 |
| 宝石 / 铠甲 / 颈饰仍出现 | [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md) | 禁用项区域单独 `--crop`，MID/TAIL 都看（R-VID-16） |
| 背景骨架变两具、石柱复制 | [`60-casebook/cards/B4-duplicate-artifacts.md`](../../60-casebook/cards/B4-duplicate-artifacts.md) | 背景元素清单 + `--keyframe` 并排逐格数 |
| 同框两张一样的脸 | [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md) | 步骤 4 按人裁脸两两比 |
| 主角变成"粗犷成熟脸" | [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md) | 步骤 3 同尺寸裁脸比板图 |
| 画面自带字幕 | [`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md) | 步骤 6 扫描 + 降级时逐格目视 |
| 转写说"多了一句"，其实是静音幻觉；按转写重出浪费一轮 | [`60-casebook/cards/D5-qc-tools-lie.md`](../../60-casebook/cards/D5-qc-tools-lie.md) | 步骤 7 双通道；单凭转写不得下重出结论 |
| 换 seed 五次仍缺同一句 | [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md) | 步骤 10 结构判定 → 回分镜改时长 |
| 选中的产出与提示词不符，下次复用提示词翻车 | [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md) | 步骤 9 差异行 + 回写 |
| 自己验自己，全部通过 | [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md) | 高风险资产由独立会话复验并署名 |

## 关联

- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)。
- 脚本与链路：[`50-rubrics/scripts/README.md`](../../50-rubrics/scripts/README.md) §5 步骤 7–10。
- 上游：[`20-craft/video-prompting-h3/SKILL.md`](../video-prompting-h3/SKILL.md)、[`20-craft/keyframe-freeze/SKILL.md`](../keyframe-freeze/SKILL.md)、[`20-craft/asset-boards/SKILL.md`](../asset-boards/SKILL.md)（板图是比对基准）。下游：[`20-craft/edit-and-assemble/SKILL.md`](../edit-and-assemble/SKILL.md)（用崩解起点定出点）。
- 找错题：[`60-casebook/drills/DR-06.md`](../../60-casebook/drills/DR-06.md)、[`60-casebook/drills/DR-07.md`](../../60-casebook/drills/DR-07.md)、[`60-casebook/drills/DR-08.md`](../../60-casebook/drills/DR-08.md)、[`60-casebook/drills/DR-09.md`](../../60-casebook/drills/DR-09.md)、[`60-casebook/drills/DR-10.md`](../../60-casebook/drills/DR-10.md)、[`60-casebook/drills/DR-13.md`](../../60-casebook/drills/DR-13.md)。
- 判据清单：[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)。

## → 行为改变

- 下次出片回来，先写背景元素清单再打开视频；没有清单的记录作废。
- 下次转写报缺句 / 多句，先导口型接触表或复听，双通道一致才下结论。
- 下次同一缺陷换第 2 个 seed 仍在，停止抽卡，开缺陷单回上游。
- 下次写"通过"前，`ls` 一遍记录里引用的每个证据文件。
