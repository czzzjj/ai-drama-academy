# 训练回路（Training Loop）

> 回答 G3〔委托方实证·F4〕：能力 = 知识 × 实践反馈 × 标准内化。装载技能只是第一项。本文件把后两项做成回路：**装载 → 找错题 → 小任务 → 自动判分 → 对照标准答案复盘 → 把每一条新的人类反馈写成新题回流**。
> 读者是 agent。本回路的出口是 [`90-curriculum/entry-prompt.md`](entry-prompt.md) 第 3 步的最低学分；入口是 [`90-curriculum/load-protocol.md`](load-protocol.md) 步骤 6 的重启自检。

```
 装载(§2) ──► 找错题(§3) ──► 小任务(§4) ──► 自动判分+复盘(§5) ──► 装机验证 ──► 生产
    ▲            │ <7 分 → 写 MEM，隔一次生产后重做      │ 不过线 → 回读对应技能再做      │
    └────────────┴──────────────── 新的人类反馈 → 新找错题(§6) ◄───────────────────────┘
```

## 1. 最低学分（开工门槛）

| 项 | 门槛 | 计分口径 |
|---|---|---|
| 找错题 | ≥10 道不同的题，平均 ≥7/10 | 每题**首次作答**成绩入均值（重做另记，不替换首次，防止刷分）；成绩必须来自判分记录 |
| 小任务 | ≥5 个 EX 通过 | 以各 `EX-nn.md` 内写明的通过线为准；通过必须有脚本输出/评审记录路径 |
| 装机验证 | ≥70/100 | [`90-curriculum/install-verification.md`](install-verification.md)，由属主或独立评审会话打分 |

门槛数值为〔学院推断，待生产验证〕；校准法：记录"达到门槛后首集被人类打回的轮数"（目标 ≤1），多集数据积累后回写本表。**未达门槛，agent 唯一允许的动作是继续训练回路。**

## 2. 装载（每次训练会话的开头）

1. 取记忆里的学院根目录；`cat "$ACADEMY_HOME/.academy_home"` 与之核对。
2. 只装载本次要练的内容：做题装 [`60-casebook/drills/README.md`](../60-casebook/drills/README.md) §1、§3 + 题面；做小任务装对应 `EX-nn.md` + 其指向的技能。**一次只装 1–3 个技能**（[`20-craft/README.md`](../20-craft/README.md)）。
3. 不预读答案：`60-casebook/drills/answers/`、`60-casebook/cards/`、`60-casebook/traceability.md` 在答题期间对答题会话关闭（题面不给案例编号，就是要你从症状推根因）。

## 3. 找错题（`60-casebook/drills/`）

**怎么做**（规则全文以 [`60-casebook/drills/README.md`](../60-casebook/drills/README.md) §1 为准）：

1. **隔离**：新会话（或确认上下文无该题答案/案例卡），**只读题面** `60-casebook/drills/DR-nn.md`。
2. **取证**：题面里的分镜表/`## SHOT-nnn` 提示词可直接当脚本输入，例 `python3 50-rubrics/scripts/segment_rhythm.py 60-casebook/drills/DR-01.md`。脚本没报的问题照样要找，每题都埋了脚本查不出的点。
3. **作答**：固定三段——①根因（分条，区分直接原因与方法论原因）②修正方案（可直接执行：改好的行/提示词/命令）③应新增的判据（可判真假，标 `[自动]`/`[目视]`/`[冷观众]`）。缺一段该维度 0 分。
4. **判分**：作答定稿后，由**另一个会话**（首选）装载 `60-casebook/drills/answers/DR-nn.md`，按得分点逐条给分（每点写"得分/依据原句"），写判分记录；自判时只认答案写明的得分点，不得"意思差不多"给分〔C2、F1〕。通过线：总分 ≥7 且根因 ≥3；≥9 记"内化"。
5. **失分回流**：<7 分 → 回读对应案例卡与技能 → 把漏掉的得分点改写成一条"下次……先/改为/禁止……"写入记忆（格式 [`CONVENTIONS.md`](../CONVENTIONS.md) §5.6）→ **间隔至少一次生产任务后重做**该题。

**顺序**（[`drills/README.md`](../60-casebook/drills/README.md) §2）：分镜与提示词设计（DR-11 / 01 / 02 / 03 / 04 / 05）→ 资产与身份（DR-08 / 09 / 06）→ 生成与验收（DR-07 / 10 / 12 / 13 / 14 / 15）→ 方法论（DR-16–DR-19，须先做过 ≥8 道单案例题）→ 综合（DR-20–DR-22）。

→ 行为改变：下次开始一个生产阶段前，先做该阶段对应的 1–2 道题；下次发现自己在题里"答对了方向但没给可执行产物"，按修正维度的 1 分封顶规则重答。

## 4. 小任务（`90-curriculum/exercises/EX-01 … EX-10`）

找错题训练"审"，小任务训练"做"：每个 EX 是一个小而完整的产出（分镜行、提示词、锚点卡、缺陷单、复述记录等），自带输入素材、判分命令与通过线，**以各 EX 文件内容为准**：
[`EX-01`](exercises/EX-01.md) · [`EX-02`](exercises/EX-02.md) · [`EX-03`](exercises/EX-03.md) · [`EX-04`](exercises/EX-04.md) · [`EX-05`](exercises/EX-05.md) · [`EX-06`](exercises/EX-06.md) · [`EX-07`](exercises/EX-07.md) · [`EX-08`](exercises/EX-08.md) · [`EX-09`](exercises/EX-09.md) · [`EX-10`](exercises/EX-10.md)

1. 先读该 EX 指向的技能与模板，再动手；产物按 [`70-playbooks/format-contracts.md`](../70-playbooks/format-contracts.md) 的表头与键名写（脚本按表头名解析，写错 = 脚本读不到 = 白做）。
2. 产物放 `training/exercises/EX-nn/`；脚本报告 `--json` 存同目录。
3. 优先覆盖不同阶段的 EX（设计 / 提示词 / 验收各至少一个），不要连刷同一阶段凑数〔学院推断〕。
4. 一次不过 → 按脚本规则码与判分记录回到对应技能的"步骤"修，**不是**在产物上打补丁；重做算新一次尝试，账本里记录尝试次数。

## 5. 自动判分与复盘

### 5.1 判分用真实脚本，不自写替代品

- 判分者（另一会话，或你本人在提交后）**重新运行**脚本，不采信答题者自报的"0 error"。脚本在 [`50-rubrics/scripts/`](../50-rubrics/scripts/)，命令以其 [`README.md`](../50-rubrics/scripts/README.md) §1、§5 为准；退出码 0 通过 / 1 有 error / 2 用法或环境错误（2 = 没跑成，不是通过）。
- 禁止调脚本参数消 error（`--margin` 降低、`--rate` 提高等，[`R-SB-16`](../50-rubrics/checklists/storyboard.md)）；禁止删掉让脚本报错的内容来换 0 error（脚本找不到任何镜时退出码 2 或 FMT 错误）。
- 脚本只报事实；`visual`（需目视）项由判分者打开证据文件亲自看，结论与证据路径写进判分记录。技术全绿 ≠ 通过 〔F2〕。

| 产物 | 判分命令（示例路径按你的文件改） |
|---|---|
| 分镜表 | `python3 50-rubrics/scripts/segment_rhythm.py ep/storyboard.md`；`python3 50-rubrics/scripts/dialogue_capacity.py --storyboard ep/storyboard.md` |
| 视频提示词 | `python3 50-rubrics/scripts/h3_frame_grid.py --check ep/video-prompts.md`；`python3 50-rubrics/scripts/prompt_lint.py ep/video-prompts.md --anchors ep/anchors.md --storyboard ep/storyboard.md`；`python3 50-rubrics/scripts/direction_audit.py ep/video-prompts.md --storyboard ep/storyboard.md`；`python3 50-rubrics/scripts/slot_order_check.py ep/video-prompts.md --simulate-remove-placeholder` |
| 出片/成片 | `contact_sheet.py` `psnr_scan.py` `burnin_text_scan.py` `transcript_reconcile.py` `asset_exists.py` `loudness_verify.py`（见脚本 README §5 步骤 7–12） |
| 需判断的部分 | 对应 [`50-rubrics/checklists/`](../50-rubrics/checklists/) 中的 `[目视]`/`[冷观众]` 条目 + [`50-rubrics/quality-model.md`](../50-rubrics/quality-model.md)，由**不同于产出者**的会话判 |

### 5.2 对照标准答案复盘（每次判分后必做）

1. 逐个得分点：得分 / 依据原句；失分点写"漏了什么 → 为什么漏"（漏的是知识、是流程、还是又用了自己的标准验自己〔F1〕）。
2. 命中答案列出的"常见错答"必须单独记一行——它们是你的稳定盲区。
3. 对每个失分点回答一句"下次……时，先……"；值得常驻的写进记忆，其余写进账本的"回流动作"。
4. 同一类失分在 ≥2 题重复出现 = 病灶在方法而非运气：回读对应技能全文再继续。

## 6. 把每条新的人类反馈变成新找错题

触发：人类主创/冷观众/独立评审指出了一个**你交付前没先发现**的问题（G4）。流程：

1. **逐字记录**原话进缺陷单（[`70-playbooks/templates/defect-ticket.md`](../70-playbooks/templates/defect-ticket.md)"反馈原话"一节），不转述。
2. 按 [`production-lifecycle.md`](../00-orientation/production-lifecycle.md) §3 定位病灶阶段、Q 维度、随机/结构性；修复并复验。
3. 问："本可拦下它的脚本/判据是什么？"——有就记下命令；没有就在题里把它写成新判据。
4. 构造**坏素材**：用学院构造的合成素材重现该类缺陷（脱敏，不放真实项目的未公开内容）；能被脚本检查的按契约格式写，使题面可直接当脚本输入。
5. 按下面模板写题面与答案；题号接续（`DR-<现有最大号+1>`）。
6. **落点**：在学院仓库内工作的维护者 → 写入 `60-casebook/drills/DR-nn.md` 与 `answers/DR-nn.md`，同步 [`drills/README.md`](../60-casebook/drills/README.md) §2 索引与案例卡 frontmatter 的 `drills` 字段，并跑 `python3 tools/academy_lint.py`；在项目里干活的生产 agent（学院对你只读）→ 写入项目的 `training/new-drills/`，并在交付报告里列出，由属主转交学院维护者。
7. 同一条反馈同时写一条"下次……"记忆（若是 Top-12 级别的常犯错，申请替换 T1，规则见 [`40-memory/README.md`](../40-memory/README.md) §4）。

**题面模板**（`DR-<nn>.md`；格式依据 [`CONVENTIONS.md`](../CONVENTIONS.md) §5.5）：

````markdown
# DR-<nn> · 找错：<中性标题，不暗示结论>

> 难度：★☆☆–★★★ ｜ 素材类型：<分镜行 / 提示词 / 验收记录 …> ｜ 建议用时：<n> 分钟
> 作答规则见 [`60-casebook/drills/README.md`](README.md)：只读本文件作答，作答完成前不得打开答案文件。允许对本文件运行 `50-rubrics/scripts/` 中的任何脚本取证。
> 题面素材是学院按真实生产情境构造的训练素材（不是项目原件）。

## 现场
- <第几集/第几轮；谁做了什么；看到的症状。不写根因，不写案例编号。>
- 人类反馈原话（逐字，来源：缺陷单 DEF-<nn>）：「<原话>」
- 生产 agent 的处理（原文）：```text …```

## 素材 1：<分镜行 / 提示词 / 锚点卡 / 日志>
<按 70-playbooks/format-contracts.md 的表头与键名书写；至少埋 1 个脚本查不出的点>

请输出：①根因（分条）②修正方案（可直接执行）③应新增的判据
````

**答案模板**（`answers/DR-<nn>.md`）：

````markdown
# DR-<nn> 答案 · <结论性标题>

> 题面：[`60-casebook/drills/DR-<nn>.md`](../DR-<nn>.md) ｜ 对应案例：<主案例>；<次要案例>
> 训练技能：[`20-craft/<skill>/SKILL.md`](../../../20-craft/<skill>/SKILL.md)

## 标准答案
### ①根因（分条；标注 直接原因 / 方法论原因）
### ②修正方案（可直接执行：改好的表行/提示词原文/命令）
### ③应新增的判据（表：检查句 | 方式 | 证据 | 溯源 | 工具）

## 打分规则（满分 10）
| 维度 | 满分 | 得分点（每点写分值） | 部分得分 | 常见错答（命中扣分） |
|---|---|---|---|---|
| 根因 | 4 | … | … | … |
| 修正 | 4 | … | … | … |
| 判据 | 2 | … | … | … |

## 本可拦下它的脚本与确切命令
`python3 50-rubrics/scripts/<script>.py <题面路径>` → 实际规则代码：<…>（没有则写"无脚本可查，只能目视/流程判据"）
````

→ 行为改变：下次被人类指出一个你没先发现的问题时，修完它之后，先把它写成题（并加判据），再继续下一项工作。

## 7. 学分账本（模板；放 `training/credit-ledger.md`，每次判分后更新）

````markdown
# 学分账本 · <agent/运行时标识> · 学院版本 <git 短哈希>

## A. 找错题（首次作答成绩入均值）
| 日期 | 题号 | 判分会话 | 根因/4 | 修正/4 | 判据/2 | 总分 | 判分记录路径 | 失分点与回流动作（MEM 编号或"下次…"） | 重做日期与成绩 |
|---|---|---|---|---|---|---|---|---|---|
| | DR-11 | | | | | | training/drills/DR-11.grade.md | | |
- 已完成不同题数：__ / ≥10　　首次作答平均分：__ / ≥7　　内化（≥9）题数：__

## B. 小任务
| 日期 | EX | 尝试次序 | 判分命令与退出码 | 目视/评审项结论 | 通过 | 证据路径 |
|---|---|---|---|---|---|---|
| | EX-01 | 1 | | | 是/否 | training/exercises/EX-01/ |
- 通过数：__ / ≥5

## C. 装机验证
| 日期 | 组别 | 自动分/40 | 评审分/60 | 总分 | 评审会话 | 结果记录路径 |
|---|---|---|---|---|---|---|
| | 实验组（装学院） | | | | | |
- 总分：__ / ≥70

## D. 门槛判定
- 最低学分是否达标：<是 / 否——差 …>　　判定日期：…　　开工许可：<是 / 否>

## E. 新题回流记录
| 日期 | 触发反馈（缺陷单 DEF-nn） | 病灶阶段 | 新题号 | 落点（学院仓库 / 项目 training/new-drills/） | 对应 MEM |
|---|---|---|---|---|---|

## F. 校准数据（回写 §1 的依据）
| 集号 | 达到门槛时的账本摘要 | 首集被人类打回轮数 | 备注 |
|---|---|---|---|
````

→ 行为改变：账本空着或只有自评分，就视为学分为 0；下次要说"我已通过入学"时，贴账本 A–D 四节的数字。

## 关联

- 入学与门槛：[`90-curriculum/entry-prompt.md`](entry-prompt.md)；装机验证：[`90-curriculum/install-verification.md`](install-verification.md)；冷观众：[`90-curriculum/cold-audience-protocol.md`](cold-audience-protocol.md)
- 题库规则：[`60-casebook/drills/README.md`](../60-casebook/drills/README.md)；判据：[`50-rubrics/checklists/`](../50-rubrics/checklists/)；脚本：[`50-rubrics/scripts/README.md`](../50-rubrics/scripts/README.md)
- 回答的困惑：G3、G4（[`00-orientation/eight-questions.md`](../00-orientation/eight-questions.md)）
