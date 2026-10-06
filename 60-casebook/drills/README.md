# 找错训练题库（Drills）

> 能力 = 知识 × 实践反馈 × 标准内化〔委托方实证·F4〕。案例卡给的是知识；本题库给的是**反馈回路**：拿一份坏素材，自己找出根因、写出可执行的修法、提出可判真假的判据，再用答案逐点判分。
> 读者是 agentos。装载本目录后的行为改变：**下次生成或验收前，先用与题面相同的三问（根因 / 修正 / 判据）审一遍自己的产物，再交出去。**

## 1. 怎么跑一道题

1. **隔离上下文**：开一个新会话（或确保当前上下文里没有该题的答案与对应案例卡），**只装载** `60-casebook/drills/DR-nn.md` 与本文件第 1、3 节。第 2 节索引写明了每题的主题与案例，只供排课/判分会话使用，答题会话不读。答题期间禁止读取 `60-casebook/drills/answers/`、`60-casebook/cards/` 与 `60-casebook/traceability.md`——题面不给案例编号，就是为了让你从症状推根因，而不是查表。
2. **取证**：允许运行 [`50-rubrics/scripts/`](../../50-rubrics/scripts/) 中的任何脚本。题面里的分镜表、`## SHOT-nnn` 提示词、锚点卡、剪辑单都按 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) 书写，**题面文件本身可以直接作为脚本输入**（例：`python3 50-rubrics/scripts/segment_rhythm.py 60-casebook/drills/DR-01.md`）。脚本没报的问题照样要找——每道题都埋了脚本查不出的点。
3. **作答格式**（固定三段，缺一段该维度 0 分）：
   - ①根因（分条）：区分直接原因（生成/执行层）与方法论原因（设计/流程层）；每条写"现象 → 为什么"。
   - ②修正方案（可直接执行）：给出改好的分镜行 / 提示词 / 剪辑单 / 验收记录 / 命令，而不是"要注意……"。
   - ③应新增的判据：每条可判真假，标 `[自动]` / `[目视]` / `[冷观众]`，写清证据与工具。
4. **判分**：作答定稿后，由**另一个会话**（首选）或本会话在提交后装载 `answers/DR-nn.md`，按第 3 节规则逐个得分点给分，写判分记录（每个得分点：得分 / 依据原句）。自己判自己的分时，只认答案里写明的得分点，不得"意思差不多"给分〔委托方实证·C2、F1〕。
5. **回流**：见第 4 节。

## 2. 题目索引（排课/判分会话用；答题会话不读本节）

| 编号 | 主题 | 训练案例 | 素材类型 | 难度 | 主要取证脚本 |
|---|---|---|---|---|---|
| [`60-casebook/drills/DR-01.md`](DR-01.md) | 碎镜：一个动作一个镜号 | A1 | 分镜表 + 节奏自评 | ★☆☆ | `segment_rhythm.py`、`h3_frame_grid.py` |
| [`60-casebook/drills/DR-02.md`](DR-02.md) | 打斗缺席：含蓄策略吃掉交手 | A2 | 分镜表 + 动作设计说明 | ★★☆ | `segment_rhythm.py` |
| [`60-casebook/drills/DR-03.md`](DR-03.md) | 慢镜：时长被读成事件速度 | A3 | 分镜行 + H3 提示词 + QC 记录 | ★★☆ | `prompt_lint.py`、`psnr_scan.py` |
| [`60-casebook/drills/DR-04.md`](DR-04.md) | 运镜脱钩：primitives 堆砌 + 设置压运镜 | A4 | 分镜表 + 两镜提示词 + 运镜统计 | ★★☆ | `segment_rhythm.py`、`prompt_lint.py`、`direction_audit.py` |
| [`60-casebook/drills/DR-05.md`](DR-05.md) | 空间混乱：文字与起始帧轴线打架 | A5 | 分镜行 + 提示词 + 迭代记录 | ★★★ | `direction_audit.py`、`segment_rhythm.py`、`prompt_lint.py` |
| [`60-casebook/drills/DR-06.md`](DR-06.md) | 角色漂移 + 克隆脸 | B1、B3 | 锚点卡 + 提示词 + QC 记录 | ★★☆ | `prompt_lint.py --anchors`、`contact_sheet.py --crop` |
| [`60-casebook/drills/DR-07.md`](DR-07.md) | 人群穿帮 + 重复伪影 | B2、B4 | 共用段 + 提示词 + QC 日志 | ★★☆ | `prompt_lint.py`、`contact_sheet.py --keyframe`、`psnr_scan.py` |
| [`60-casebook/drills/DR-08.md`](DR-08.md) | 禁用项被违反 | C1 | 锚点卡 + 出图参数 + 验收记录 | ★★☆ | `prompt_lint.py`、ffmpeg 裁剪 |
| [`60-casebook/drills/DR-09.md`](DR-09.md) | 验收放水 | C2 | 两轮验收记录 | ★★☆ | `asset_exists.py` |
| [`60-casebook/drills/DR-10.md`](DR-10.md) | 烧录字幕 + 纯黑字卡 | D1、D2 | 提示词 + 剪辑单 + QC 日志 | ★★☆ | `prompt_lint.py`、`burnin_text_scan.py` |
| [`60-casebook/drills/DR-11.md`](DR-11.md) | 对白容量 | D3 | 分镜行 + 提示词 + 转写 | ★☆☆ | `dialogue_capacity.py`、`transcript_reconcile.py` |
| [`60-casebook/drills/DR-12.md`](DR-12.md) | 符号/图形错误 | D4 | 锚点卡 + 提示词 + 返工日志 | ★★☆ | `prompt_lint.py`（VP-symbol） |
| [`60-casebook/drills/DR-13.md`](DR-13.md) | QC 工具自身会骗人 | D5 | 转写 + QC 日报 | ★★☆ | `transcript_reconcile.py` |
| [`60-casebook/drills/DR-14.md`](DR-14.md) | 槽位顺序 + 改集号路径残留 | E1、E2 | 提示词 + 校验报错 + 操作日志 | ★★☆ | `slot_order_check.py`、`asset_exists.py` |
| [`60-casebook/drills/DR-15.md`](DR-15.md) | 环境怪癖 + 提示词≠产出 | E3、E4 | 生产日志 + 提示词片段 | ★★☆ | — |
| [`60-casebook/drills/DR-16.md`](DR-16.md) | 自证循环 | F1 | 成片报告 + 自我放映记录 | ★★★ | — |
| [`60-casebook/drills/DR-17.md`](DR-17.md) | 代理指标 | F2 | 指标看板 + 分镜 + 计划 | ★★★ | — |
| [`60-casebook/drills/DR-18.md`](DR-18.md) | 补丁式迭代 | F3 | 多轮返工记录 | ★★★ | — |
| [`60-casebook/drills/DR-19.md`](DR-19.md) | 学了技能≠有了能力 | F4 | agent 自述 + 方法论摘录 | ★★★ | — |
| [`60-casebook/drills/DR-20.md`](DR-20.md) | 综合事后复盘（多维） | 多案例 | 整集复盘材料 | ★★★ | 全部 |
| [`60-casebook/drills/DR-21.md`](DR-21.md) | 反馈翻译："没有运镜""打斗逻辑" | G6（A2、A4、F2） | 人类反馈 + 产物 | ★★★ | — |
| [`60-casebook/drills/DR-22.md`](DR-22.md) | 病灶路由：问题该回到哪个阶段 | G7（A1、A5、F3） | 多阶段产物 | ★★★ | — |

难度与素材类型以各题面头部为准（本表与题面冲突时以题面为准，并修正本表）。"—"表示该题的主要错误没有脚本能查，只能靠 [目视] 与流程判据——这类题更要做。

**建议顺序**：先按生产阶段做 DR-11 / DR-01 / DR-02 / DR-03 / DR-04 / DR-05（分镜与提示词设计）→ DR-08 / DR-09 / DR-06（资产与身份）→ DR-07 / DR-10 / DR-12 / DR-13 / DR-14 / DR-15（生成与验收）→ DR-16–DR-19（方法论）→ DR-20–DR-22（综合）。方法论题必须在做过至少 8 道单案例题之后再做，否则只会背结论。

## 3. 打分规则（每题满分 10）

| 维度 | 满分 | 给分原则 |
|---|---|---|
| 根因 | 4 | 按答案"得分点"逐条给分。只描述症状（"镜头太短""运镜不够"）不算根因；必须答出"为什么会这样"。漏掉方法论原因（设计层/流程层）的，最多拿该维度一半。 |
| 修正 | 4 | 必须**可直接执行**：改好的表行、提示词原文、剪辑单行、命令。只有方向没有产物的（"要合并镜头""要加强验收"）最多 1 分。修法本身违反学院硬约束（时长不在 17k+5 网格、写 negative_prompt、裁画面去字幕、把确定性画面交给生成器）的，按答案扣分。 |
| 判据 | 2 | 每条判据可判真假，并标明方式与证据。"画面要好看""节奏要好"一类不可判真假的句子 0 分。 |

通用规则：
- **部分得分**按答案文件中的"部分得分"栏执行；答案未列出的合理观点，判分会话可在该维度内最多加 0.5 分，并在判分记录里写明理由（供维护者补进答案）。
- **常见错答**：命中答案列出的常见错答时，按该条说明扣分，扣到该维度 0 分为止。
- **诚实扣分**：编造来源编号、编造人类原话、把〔学院推断〕写成"实证"的，该维度直接 0 分〔CONVENTIONS §2〕。
- **通过线**〔学院推断，待校准〕：总分 ≥7 且根因 ≥3 记为"通过"；≥9 记为"内化"。校准方法：同一题由 ≥2 个独立判分会话打分，分差 >1.5 的得分点说明答案不够可判，回改答案文件。

## 4. 错题回流与新题入库

1. **错题回流**：某题 <7 分 → 回读对应案例卡与技能（答案文件末尾有链接），把漏掉的得分点改写成一条"下次……先/改为/禁止……"写入 [`40-memory/core-memory.md`](../../40-memory/core-memory.md)（MEM 格式见 CONVENTIONS §5.6），间隔至少一次生产任务后重做该题。
2. **新题入库**：复验或人类审片发现了首验漏判的问题时，把它写成新题（编号接续题库现有最大编号 +1），格式遵守 CONVENTIONS §5.5：
   - 题面只给坏素材与现场，不给答案、不出现案例编号、标题不暗示结论；末尾固定写「请输出：①根因（分条）②修正方案（可直接执行）③应新增的判据」。
   - 题面素材注明"学院构造的训练素材"；人类原话只能逐字引用 [`00-orientation/client-dossier.md`](../../00-orientation/client-dossier.md) 中「」内的句子。
   - 能被脚本检查的坏素材，按契约格式书写，使题面可直接作为脚本输入；答案文件写出实际运行命令与实际输出的规则代码。
   - 答案文件：标准答案（①②③）+ 打分规则（根因 4 / 修正 4 / 判据 2，含得分点、部分得分、常见错答）+ 对应案例编号 + 本可拦下它的脚本与确切命令。
   - 同步更新本文件第 2 节索引与对应案例卡 frontmatter 的 `drills` 字段。

## 5. 关联

- 案例卡：[`60-casebook/cards/`](../cards/)；正面资产：[`60-casebook/positive-assets.md`](../positive-assets.md)
- 判据清单：[`50-rubrics/checklists/`](../../50-rubrics/checklists/)；达标定义：[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md)
- 训练回路与练习：[`90-curriculum/training-loop.md`](../../90-curriculum/training-loop.md)、[`90-curriculum/exercises/`](../../90-curriculum/exercises/)
