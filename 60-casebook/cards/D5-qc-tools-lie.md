---
id: D5
title: QC 工具自身会骗你
group: D 生成技术
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [shot-qc, edit-and-assemble, screening-review]
drills: [DR-13]
---
# D5 · QC 工具自身会骗你

> 一句话：**测量仪器也是一个会出错的模型。** 判定问题之前，先证伪工具。转写、OCR、PSNR、LLM 评审，每一样都有已知的骗人方式。单一通道的证据只能用来定位问题，不能用来下判决。

## 症状（含人类主创原话，逐字引用档案）

- 症状一：一个无对白镜的音轨，被语音转写工具识别成"字幕by索兰娅"，这是幻觉〔委托方实证·D5〕。
- 症状二：某镜尾段的低笑气声，单次转写误听成了"救我"。做了多窗口复核：3 个时间窗的结果互相矛盾，置信度都低，判定为误听，没有重出〔委托方实证·D5〕。
- 档案没有保留人类主创关于本案的「」逐字原话。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 两例都发生在视频验收"转写对白逐字对账"这一步〔委托方实证·P8、M10〕。
- 症状一的特征：这一镜的分镜里**本来就没有台词**，转写却给出了一句完整、通顺、高度套路化的话。"字幕by索兰娅"逐字收录在一个公开的 Whisper 静音幻觉数据集里〔外部调研·S-COMFY-16〕。〔学院推断〕委托方用的很可能是 Whisper 系的 ASR；档案没写工具名。
- 症状二的特征：有声音，但不是台词，位置在尾段。3 个窗口的结果互相矛盾，置信度都低。这个结论**省掉了一次不必要的重出**。如果当时按单次转写去判，一个合格镜就会被打回〔委托方实证·D5〕。
- 档案没有记录镜号、置信度数值和所用工具版本。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. ASR 遇到非语音也会输出文字。Whisper 的跳过条件是 `no_speech_prob > 0.6` **并且** `avg_logprob ≤ -1.0`；只要 logprob 足够高，即使判为无语音也不跳过。所以高置信度的套话式幻觉，默认阈值拦不住〔外部调研·S-COMFY-14、F-COMFY-14〕。
2. 笑声、气声这类非言语人声会被映射成最近似的词。单个窗口的切分边界决定了它被听成什么，换一个窗口，结果就变了〔委托方实证·D5；学院推断〕。

### 方法论原因
3. 把仪器读数当成事实。流程里没有"先证伪工具"这一步，单一通道的读数就直接进了判决。
4. 两种误判的代价都高。假阳性是没必要的重出：几个小时的算力，还可能丢掉一条好镜。假阴性是真缺句被放过，变成阻断缺陷。两种都只能靠第二通道来防。
5. 把"工具全绿"当成"没有问题"。这和 F1 自证循环是同一个病：用自己的仪器给自己作证。

### 外部调研补强的根因
6. 幻觉是已知、可复现的现象，并且有公开黑名单：数据集里收录了"字幕by索兰娅""字幕提供者 李宗盛""请不吝点赞 订阅 转发 打赏支持明镜与点点"等串〔外部调研·S-COMFY-16、F-COMFY-15〕。学界用 bag of hallucinations 做后处理，可以降低 WER〔外部调研·S-COMFY-17〕。
7. 约 1% 的转写含整句幻觉，非语音时长占比越高越容易触发〔外部调研·S-CASE-28、F-COMFY-17〕。短剧镜头里静场、环境声、气声占比高，属于高风险输入〔学院推断〕。
8. Whisper 会在片尾安静处幻听一句短语，常见的是 "Thank you."〔外部调研·F-H3-20〕。
9. faster-whisper 默认的 VAD 只去掉超过 2s 的静音〔外部调研·F-COMFY-16〕。5–15s 的短镜需要把门槛调低，例如 300–500ms〔外部调研·S-COMFY-15；学院推断，待样片校准〕。
10. 同行经验：中文频道幻觉的特征是 6–20 个字挤在 20–40ms 内，并且在不同音频的同一位置重复出现。字幕建轴要用双 ASR 交叉加能量实测，不得用 `initial_prompt` 去补漏〔外部调研·S-COMFY-21〕。
11. 真台词也会被听错："诸君，且听龙吟"被转写成"朱军且听龙银"〔外部调研·F-ZEN-21〕。所以**字幕永远逐字取自剧本，转写只用来定位时间和查缺句**〔外部调研·S-ZEN-11、S-ZEN-26、F-ZEN-20〕。

## 修正过程（做了什么、第几轮、结果）

- 委托方：判定问题前先证伪工具；低置信的词必须多窗复核；转写异常时先抽帧核对画面〔委托方实证·D5〕。症状二按这个流程复核后没有重出〔委托方实证·D5〕。
- 已固化为正面资产 M10（视频双通道验收）。`transcript_reconcile.py` 内置了已知幻觉黑名单、低置信提示和 `--windows` 三窗复核命令，并且**绝不仅凭转写给出"重出"结论**。

### 已知 ASR 幻觉黑名单（命中 = 降为"待核"，不自动删除）
| 串 | 出处 | 是否在脚本内置表 `KNOWN_ASR_HALLUCINATIONS` 里 |
|---|---|---|
| 字幕by索兰娅 | D5 实证；S-COMFY-16 | 是 |
| 请不吝点赞 / 订阅 转发 打赏 / 明镜与点点栏目 | S-COMFY-16（数据集里截断，无"栏目"）、S-COMFY-21 | 是（分三段匹配） |
| 字幕由Amara.org社区提供 | S-COMFY-16 | 是 |
| 谢谢观看（含"谢谢观看 下集再见"） | S-COMFY-16 | 是 |
| 字幕提供者 李宗盛、下集预告、别忘了订阅、大家好 欢迎来到我的频道 | S-COMFY-16 | 否：人工比对，写进 [`40-memory/core-memory.md`](../../40-memory/core-memory.md) |
| Thank you.（片尾静音处） | F-H3-20 | 否：人工比对 |

"下集再见""下集预告"在短剧集尾可能是真台词。所以命中黑名单只降为"待核"，最终要看剧本有没有这句，再看第二通道〔外部调研·S-COMFY-16〕。

### 转写异常的判定表（`transcript_reconcile.py` 规则码 → 动作）
| 规则码 | 先做 | 判定 |
|---|---|---|
| `TR-unscripted`（无对白镜出了转写）或 `TR-hallucination` | 用 ffprobe 查有没有音轨（`TR-no-audio`）；用 ffmpeg `volumedetect` / `silencedetect` 量能量；比对黑名单 | 无音轨、能量在静音阈以下、或命中黑名单 → 工具幻觉，不重出 |
| `TR-lowconf`（置信度 < 0.6） | `--windows` 跑三窗（偏移 0 / +0.4s / 前垫 0.4s），看口型接触表 `lips.jpg` | 三窗互相矛盾且都低置信 → 误听（"救我"属于这一型） |
| `TR-missing` | 三窗加口型 | 三窗一致缺同一段 → 真缺句。换 seed 仍缺 → 结构性缺陷，转 D3 |
| `TR-extra` | 三窗加听感 | 只在单窗出现 → 工具噪声；三窗一致且口型接触表上看得到对应口型 → 生成器加了台词，重出 |

### 其他 QC 工具的已知骗法
| 工具 | 骗法 | 防线 |
|---|---|---|
| `burnin_text_scan.py` 无 OCR 时的启发式 | 小号水印得分 0.02–0.05，低于通用阈值 0.08，会漏报（D2 现场） | 单设 `D2-heuristic-flat`；启发式永远不单独判 error，报告写明降级 |
| OCR | 对 AI 伪汉字的召回率没有公开评测〔外部调研·S-COMFY-19〕 | 整帧目视 |
| `psnr_scan.py` | 高颗粒、快动作镜头上绝对阈值失效，会报出假跳变 | `P8-low-baseline` 停用绝对阈值；跳变回接触表确认 |
| `contact_sheet.py` 的 12 格抽样 | 会漏掉短暂闪现的东西 | 高风险镜加密抽帧 |
| 单遍 loudnorm | 一次实跑落在 -12.33 LUFS，目标是 -16〔外部调研·F-ZEN-21〕 | 测编码后的实际值（`loudness_verify.py`） |
| 同一会话的 LLM 自评 | 模型能认出并偏爱自己的输出〔外部调研·S-CASE-23〕 | 独立评审会话（见 F1） |

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 每条生成镜（含无对白镜）都跑 `transcript_reconcile.py --storyboard … --prompts … --transcripts …`。`TR-unscripted`、`TR-hallucination`、`TR-lowconf` 出现时，先按上面的判定表处理，不得直接下结论〔D5、M10〕。
- [自动]+[目视] 任何"重出"或"缺句"结论，都要有 `--windows` 三窗结果加 `lips.jpg` 口型接触表（或听感记录）两份证据文件，写进 `qc/<SHOT>.md`〔D5〕。
- [自动] 无对白镜出现转写时，先用 ffprobe 查音轨（`TR-no-audio`），再用 ffmpeg `volumedetect` 量能量〔D5〕。
- [目视] 剪辑单 `字幕` 列逐字取自分镜 `对白` 列，**禁止**从转写结果复制〔D5、P7；S-ZEN-26〕。
- [目视] 每份 QC 报告都写明各工具的降级状态，例如 `D1-ocr-degraded`、`P8-low-baseline`、`P8-no-drawtext`。报告没写降级状态，不得声明"通过"〔D5〕。
- [冷观众] 冷观众听到的台词与字幕一致，没有"字幕和声音对不上"的断点〔D5、P7〕。

## → 行为改变（下次……）

- 下次任何工具报出异常，第一步是问"这是不是工具在骗我"，查它的已知骗法表，然后再看内容。
- 下次转写给出低置信词或无台词镜的文字，跑三窗加口型接触表。**禁止**凭单次转写重出，也禁止凭单次转写放行。
- 下次做字幕，从剧本取字；转写只用来找入点、出点和缺句。
- 下次发现新的幻觉串，把原文、所用工具和出现位置写进 [`40-memory/core-memory.md`](../../40-memory/core-memory.md)，并在本卡黑名单表里追加一行。
- 下次写验收结论，每条"不通过"都要引用两个独立通道的证据文件。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ "先证伪工具、单通道不判决"适用于所有自动 QC：ASR、OCR、场景检测、响度、LLM 评审。
- ★ 换 ASR 引擎后，幻觉串会变，方法不变。可以接 SenseVoice 这类带事件标签的第二引擎（它能输出 Laughter、Breath 标签）做交叉核对〔外部调研·S-COMFY-18；学院推断〕。
- ☆ 黑名单里的具体字串来自中文 Whisper 系，换语言要重建。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（双通道、三窗复核）、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)（字幕取自剧本）、[`20-craft/screening-review/SKILL.md`](../../20-craft/screening-review/SKILL.md)（独立评审，不自证）、[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)（非言语人声的设计与核对）。
- 理论：[`10-theory/10-quality-philosophy.md`](../../10-theory/10-quality-philosophy.md)、[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)。
- 判据清单：[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/sound-color-performance.md`](../../50-rubrics/checklists/sound-color-performance.md)。
- 脚本：[`50-rubrics/scripts/transcript_reconcile.py`](../../50-rubrics/scripts/transcript_reconcile.py)、[`50-rubrics/scripts/burnin_text_scan.py`](../../50-rubrics/scripts/burnin_text_scan.py)、[`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)、[`50-rubrics/scripts/loudness_verify.py`](../../50-rubrics/scripts/loudness_verify.py)。
- 找错题：[`60-casebook/drills/DR-13.md`](../../60-casebook/drills/DR-13.md)（QC 工具骗人）。
- 相邻案例：[`60-casebook/cards/D3-dialogue-capacity.md`](D3-dialogue-capacity.md)（真缺句 → 容量）、[`60-casebook/cards/F1-self-verification-loop.md`](F1-self-verification-loop.md)（自证循环）、[`60-casebook/cards/C2-lenient-acceptance.md`](C2-lenient-acceptance.md)（证据文件而非一句"通过"）、[`60-casebook/positive-assets.md`](../positive-assets.md)（P7、P8、M10）。
