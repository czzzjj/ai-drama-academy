---
id: D3
title: 对白容量物理约束
group: D 生成技术
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [script-doctor, storyboard-long-take, video-prompting-h3, shot-qc]
drills: [DR-11]
---
# D3 · 对白容量物理约束

> 一句话：**台词要占时间，镜头时长装不下，就是物理上装不下。** 换 seed 只是换一种缺句方式。7.5 字/秒是"塞得进去"的上限，≈4.1 字/秒才是"演得出来"的规划速度。容量要在分镜阶段算，不能在出片后靠抽卡去碰。

## 症状（含人类主创原话，逐字引用档案）

- 有三镜的对白密度超出了镜长容量〔委托方实证·D3〕。
- 同一镜换了 3 个 seed，每个 seed 缺的句子都不一样。**换 seed 无解**〔委托方实证·D3〕。
- 其中一镜延长了两次才补齐〔委托方实证·D3〕。
- 档案没有保留人类主创关于本案的「」逐字原话。
- 学院缺陷分级：台词缺句、轧词，或字幕与声音对不上，都属于阻断缺陷（Q8），见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §3。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 二次延长的那一镜，原始时长 7.5s，台词不够放。重算方式是"殇月句 4.34s + 一字一顿句 ~6.5s ≈ 10.3s"，之后按 11s 重新生成，台词才齐〔委托方实证·D3〕。
- 帧网格换算（`h3_frame_grid.py --seconds`）：
  - 7.5s 不在网格上：≥7.5s 的最小合法值是 192 帧（8.00s），最近合法值是 175 帧（7.29s）。
  - 11s 同样不在网格上：可以取 260 帧（10.83s），也可以取 277 帧（11.54s）。档案没记录实际取的是哪一档。
- 档案算式本身不闭合：4.34 + 6.5 = 10.84，不是 10.3。如果 10.3 是实测总长，一字一顿句约为 10.3 − 4.34 ≈ 6.0s。不论哪种，按 11s 生成后余量只有 0.16–0.7s。这是 `dialogue_capacity.py` 记录的已知校准点：默认留白 1.0s 加换句气口 0.3s，比实测略保守。
- 另外两镜缺句的细节（字数、时长、最后怎么处理的）档案没有记录。

## 容量算术（全学院统一口径，`dialogue_capacity.py` 执行）

```
字数       = 汉字计 1、数字逐位计 1、拉丁词计 2；标点、省略号不计；≤12 字的括号舞台提示不计
hard       = 字数 ÷ 7.5  +  停顿记号数 × 0.6s  +  (句数 − 1) × 0.3s      ← 台词本身的物理时长
required   = hard + 表演留白 1.0s                                       ← 判定用的最少时长
可用时长   = 时长 − 尾部余量（声明了 `- 尾部余量:` 时）
planning   = 字数 ÷ 4.1 + 停顿 + 换句 + 留白                            ← 规划语速（R3）
```
留白 1.0s、停顿 0.6s、换句 0.3s 是〔学院推断〕，按上面的校准点回调（`--margin` / `--pause-sec`）。

**算例 A：同一句台词，两种语速，两种结论。** 一句 28 字的单人台词（示例句，不是档案原文）：
| 口径 | 计算 | 5.17s（124 帧）够不够 | 脚本结论 |
|---|---|---|---|
| 上限 7.5 | 28÷7.5 = 3.73s，加留白 1.0s 得 4.73s | 装得下，但利用率 92% | `D3-tight`：建议 5.88s（141 帧） |
| 规划 4.1 | 28÷4.1 = 6.83s，加留白 1.0s 得 7.83s | 会念得很赶 | `D3-rushed`：建议 8.00s（192 帧） |
| 规划 + 开口延迟 | 7.83s 再加 1.5–2.5s〔外部调研·F-ZEN-06〕 | — | 9.42s（226 帧）到 10.83s（260 帧） |

同一句话，"塞得下"只要 5.17s，"演得好"要 9–11s，差了将近一倍。**定镜长按表中后两行，拦截按第一行。**

**算例 B：一字一顿句。** 「我……记……住……了。」按字数模型只有 4 字 + 3 顿 × 0.6s = 2.33s。D3 实测这类句子整句约 6.5s。脚本识别出一字一顿句后会报 `D3-stagger`，建议值按 max(模型估值, 6.5s) 取。**停顿主导的台词，字数算法会严重低估。**

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. H3 语速 ≈7.5 字/秒是物理约束。台本设计阶段没有核算容量〔委托方实证·D3、T-2〕。
2. 镜长先按画面和动作定好，台词是后来塞进去的。台词里的停顿（一字一顿）没有算进时长〔委托方实证·D3〕。

### 方法论原因
3. **把结构性缺陷当成随机缺陷**：缺句之后的第一反应是换 seed，连换 3 个，白白花掉 3 次生成〔委托方实证·D3〕。
4. **在病灶下游修**：对白缺句的病灶在"1 剧本/分镜"，却在"2 制作"里靠延长、重产来补。代价从分钟级涨到小时级（[`00-orientation/production-lifecycle.md`](../../00-orientation/production-lifecycle.md) §3、§4）。
5. 只有一个语速数字。7.5 被同时当成"上限"和"目标"来用，于是每一镜都按最赶的速度去排。

### 外部调研：冲突证据与新增根因
6. **双语速**：一份外部实测对同一镜做了 20 次 H3 中文对白生成，自然语速约 4.1 字/秒，较密的输入会赶词或截断〔外部调研·S-ZEN-17、F-ZEN-05〕。配音员实测 4.30 字/秒（含停顿）〔外部调研·S-H3-09〕。GB 45438 的附注给出汉语正常语速约 120–160 字/分〔外部调研·S-PLAT-02〕。Sora 4 秒镜头通常只放得下 1–2 句短对白〔外部调研·S-VGEN-01〕。学院立场按 R3：**7.5 = 硬上限（error），≈4.1 = 规划语速（warn）**（[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R3）。
7. **对白镜实际比计划长**：开口前有延迟，说完台词还要时间，合计比计划多约 1.5–2.5s〔外部调研·F-ZEN-06〕。另有用户报告片头约 0.5s 出现乱语或截断人声〔外部调研·S-H3-13、F-H3-24〕，片尾前 1.2–1.7s 常崩解〔外部调研·F-H3-18〕。所以一镜两端都不能放台词。
8. **说话节奏绑在 seed 上，不在提示词上**：同一个 seed 换提示词，Whisper 逐字时间到小数点后两位都一致〔外部调研·F-H3-19〕。这解释了"换 seed 各缺不同句"：每个 seed 分配时间的方式不同，但总量都装不下；改写提示词措辞也救不了。
9. **硬塞会伤表演**：不要让人物加快语速去硬塞台词。放不下，就把台词拆到说话者和听者的镜头上；镜长由声音事件推出来〔外部调研·S-ZEN-22〕。

## 随机缺陷 vs 结构性缺陷（判法）

| 观察 | 判定 | 动作 | 例 |
|---|---|---|---|
| 并行 ≥3 seed，至少一版干净 | 随机缺陷 | 选优，换版覆盖 | B4 第二骨架（4 seed 选优） |
| ≥3 seed **都有同类缺陷**，具体实例不同也算 | 结构性缺陷 | 停止抽卡，回设计或参数 | D3 三个 seed 各缺不同句 |
| 同一 seed 改措辞，缺陷位置不变 | 结构性缺陷（节奏绑 seed，F-H3-19） | 改时长或删字 | — |
| 容量算术本身已经 `D3-capacity` | 不必生成就知道是结构性 | 先改分镜 | D3 那一镜 7.5s 对 10.3s |

**铁律**：同类缺陷在第 3 个 seed 上再次出现时，禁止跑第 4 个 seed。先写出结构性原因，再改设计。

## 修正过程（做了什么、第几轮、结果）

- 委托方：在设计阶段核算，镜长 ≥ 台词字数 ÷ 7.5 + 表演留白；先判断是随机缺陷还是结构性缺陷，换 seed 无解的问题改参数或改设计〔委托方实证·D3〕。实例：7.5s → 重算 10.3s → 按 11s 重产，台词齐〔委托方实证·D3〕。
- 已固化为正面资产 P9、M5（对白容量核算），并写成 `dialogue_capacity.py` 的 `D3-*` 规则。
- 学院补充：按 R3 加了规划语速检查（`D3-rushed`）；声明 `尾部余量` 时，容量按"时长 − 余量"核算（[`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §2）。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 分镜定稿前跑 `dialogue_capacity.py --storyboard storyboard.md --prompts video-prompts.md`，以下 error 必须为 0：`D3-capacity`、`D3-margin`、`D3-split`、`D3-duration-missing`〔D3、P9、M5〕。
- [自动] `D3-rushed`（按 4.1 字/秒会很赶）有两种处理：把时长加到建议值；或者在分镜 `内容` 列写明"赶词为设计（理由：抢话 / 争吵…）"。不许不处理〔D3、R3〕。
- [自动] 报 `D3-stagger` 的一字一顿句，按 ~6.5s 上界定时长；或者先单句试生成实测，再用 `--stagger-sec` 回填〔D3〕。
- [自动] 时长建议值经 `h3_frame_grid.py` 吸附到 17k+5 网格；`required` > 15.08s 时拆镜或删句〔T-2、D3〕。
- [自动] 出片后跑 `transcript_reconcile.py --storyboard … --prompts … --transcripts …`，`TR-missing` 为 0。同一镜 ≥2 个 seed 报 `TR-missing`，就回到 `dialogue_capacity.py`，不再抽卡〔D3、P7、M10〕。
- [目视] 有对白的镜用 `transcript_reconcile.py --windows` 打印的口型接触表（`lips.jpg`）核对：台词没有落在片头 0.5s 和尾部余量区间里〔S-H3-13、F-H3-18〕。
- [冷观众] 冷观众的断点记录里没有"说太快听不清""话没说完就切了"〔D3〕。

## → 行为改变（下次……）

- 下次写剧本或分镜，**先数字、跑脚本，再定镜长**：镜长 = max(动作链需要的时长, 规划语速下的对白时长 + 开口延迟)。
- 下次台词放不下，按这个顺序处理：删字 → 把台词拆到听者反应镜 → 延长（≤15.08s）→ 拆镜。**禁止**在提示词里写 `speaks quickly` 之类的话去硬塞。
- 下次缺句，先数有几个 seed 缺了同类东西。第 3 个 seed 仍然缺，就停止抽卡，在 `qc/<SHOT>.md` 写"结构性缺陷：容量"。
- 下次遇到一字一顿、迟疑、哭腔这类停顿主导的台词，先单句试生成，把实测时长回填到参数，再定镜长。
- 下次声明 `尾部余量`，台词必须在余量开始之前说完。片头 0.5s 也不放台词。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ 任何音画同出的生成器都有对白容量上限（H3、Sora、Veo、可灵）。"上限判定 + 规划语速 + 随机/结构二分"与模型无关；换模型后只需要重测两个语速。
- ★ "随机 vs 结构性"的判法适用于所有缺陷：漂移、伪影、字幕、禁用项都可以用"≥3 seed 同类复现"来判。
- ★ 换语言时，字数口径要重定（英文约 2.7 词/秒〔外部调研·F-H3-23〕）。
- ☆ 7.5 字/秒和 6.5s 一字一顿是委托方节点上的实测值。换节点、换步数（turbo 下语音最弱〔外部调研·F-H3-09〕）都要复测。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/script-doctor/SKILL.md`](../../20-craft/script-doctor/SKILL.md)（剧本阶段核算）、[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（镜长推导）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（`<d>` 写法、尾部余量）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（三方对账）、[`20-craft/performance-direction/SKILL.md`](../../20-craft/performance-direction/SKILL.md)（留白即表演）。
- 理论：[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/13-performance-direction.md`](../../10-theory/13-performance-direction.md)、[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)。
- 判据清单：[`50-rubrics/checklists/script.md`](../../50-rubrics/checklists/script.md)、[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)。
- 脚本：[`50-rubrics/scripts/dialogue_capacity.py`](../../50-rubrics/scripts/dialogue_capacity.py)、[`50-rubrics/scripts/h3_frame_grid.py`](../../50-rubrics/scripts/h3_frame_grid.py)、[`50-rubrics/scripts/transcript_reconcile.py`](../../50-rubrics/scripts/transcript_reconcile.py)。
- 找错题：[`60-casebook/drills/DR-11.md`](../../60-casebook/drills/DR-11.md)（对白容量）。
- 相邻案例：[`60-casebook/cards/B4-duplicate-artifacts.md`](B4-duplicate-artifacts.md)（随机缺陷的对照）、[`60-casebook/cards/D5-qc-tools-lie.md`](D5-qc-tools-lie.md)（缺句先证伪转写）、[`60-casebook/cards/A1-fragmented-shots.md`](A1-fragmented-shots.md)（镜长下限 5.17s）、[`60-casebook/positive-assets.md`](../positive-assets.md)（P9、M5、P7）。
