# 学院写作与格式公约（CONVENTIONS）

> 任何在本仓库内新增/修改内容的作者（人或 agent）必须遵守本公约。`tools/academy_lint.py` 会机器校验其中标 🔒 的条款。
> 一句话原则：**每一行内容都要回答"一个 agentos 装载了这条之后，它下一次生成/验收时的行为会有什么不同？"** 回答不了的，不写。

---

## 1. 读者与文风

1. 读者是 **agentos**（Claude Code / Codex 一类可装载技能、有记忆、有工具的智能体运行时），不是人类学员，也不是讲师。
2. 文风是**判决式**：优先写"必须 / 禁止 / 若…则…"，少写"可以考虑 / 一般来说"。少铺垫，多给数字、判据、动作。
3. 主语言中文；提示词、模型参数、英文句式原样保留英文。
4. 每篇理论、每张案例卡、每个技能都要有 **「→ 行为改变」**：用"下次……时，先/改为/禁止……"的句式，落到 agent 的下一步具体动作。
5. ⛔ 禁止产出"讲师手册""教学大纲""学习目标"这类只给人类讲师看的东西。
6. 文件名、目录名一律**英文 kebab-case**（委托方实证 E3-1：中文路径会在 cmd 裸跑时吞输出）。文件内容可以是中文。

## 2. 来源标注（诚实铁律）🔒

所有事实性陈述必须能被归类为以下三种之一，并在关键处显式标注：

| 标签 | 含义 | 必须能追溯到 |
|---|---|---|
| `〔委托方实证·A5〕` | 来自委托方真实生产与返工 | [`00-orientation/client-dossier.md`](00-orientation/client-dossier.md) 中的编号 |
| `〔外部调研·S-PLAT-03〕` | 来自外部公开资料 | [`80-sources/catalog/`](80-sources/catalog/) 中的条目编号（带 URL） |
| `〔学院推断〕` | 学院基于上两者的推理，**尚未被生产实证** | 必须同时写出"如何验证它" |

- 委托方没做过的事（平台发布、流量运营、冷观众、声音设计等）**不得**写成"经验表明"，只能是〔外部调研〕或〔学院推断〕。
- 不允许编造数字、URL、人类原话。人类原话只能逐字引用档案中「」内的句子。

## 3. 编号体系 🔒

| 前缀 | 对象 | 定义位置 |
|---|---|---|
| `T-1`…`T-4` | 工作流底座技术事实 | client-dossier.md |
| `P1`…`P10` | 委托方正面资产 | client-dossier.md / 60-casebook/positive-assets.md |
| `M1`…`M10` | 已换来的正确方法论 | client-dossier.md / 60-casebook/positive-assets.md |
| `A1`…`F4`（含 `C1-1`…`C1-7`、`E3-1`…`E3-3`） | 负面案例 | client-dossier.md / 60-casebook/cards/ |
| `G1`…`G8` | 委托方困惑 | client-dossier.md / 00-orientation/eight-questions.md |
| `GAP-1`…`GAP-7` | 能力缺口 | client-dossier.md |
| `S-<CODE>-nn` | 外部来源条目 | 80-sources/catalog/*.md |
| `F-<CODE>-nn` | 外部来源中的关键事实 | 80-sources/catalog/*.md |
| `Q1`…`Q8` | 全片质量模型的 8 个维度 | 50-rubrics/quality-model.md |
| `R-<STAGE>-nn` | 验收条目（判据） | 50-rubrics/checklists/*.md |
| `DR-nn` | 找错训练题 | 60-casebook/drills/DR-nn.md |
| `EX-nn` | 小任务练习 | 90-curriculum/exercises/EX-nn.md |
| `TP-nn` | 好/坏样例对（taste pair） | 30-taste/pairs/*.md |
| `TJ-nn` | 审美判据卡（taste judgment） | 30-taste/judgment-cards.md |
| `MEM-nn` | 长期记忆条目 | 40-memory/core-memory.md |

`R-<STAGE>` 的 STAGE 取值：`SCR` 剧本 / `SB` 分镜设计 / `VP` 视频提示词 / `BRD` 板图 / `KF` 关键帧 / `VID` 视频镜头 / `CUT` 成片 / `SND` 声音 / `COL` 色彩灯光 / `PRF` 表演 / `PUB` 发布 / `SEA` 季级连续性。

## 4. 全仓文件地图（预分配，链接请按此写）

```
README.md                      学院总览
CONVENTIONS.md                 本公约
CLAUDE.md / AGENTS.md          维护者入口（指向本公约）
00-orientation/
  README.md                    入学总述：问题、负面资产总述、学院结构如何回答
  client-dossier.md            委托方证据档案（一手源）
  eight-questions.md           G1–G8 逐条回答 + 回答模块映射
  production-lifecycle.md      开发→预制作→制作→后期→审片 的工业流程与各阶段闸门（回答 G7）
  glossary.md                  术语表（段/拍/镜/起始帧/锚点句…；澄清 G6 的"运镜""打斗逻辑"歧义）
  evidence-reconciliation.md   证据冲突裁决（委托方实证 vs 官方文档 vs 社区实测）、新增根因、画幅规格、合规许可
10-theory/
  README.md
  01-vertical-drama-physiology.md   02-film-language-for-generators.md
  03-spatial-staging.md             04-action-design.md
  05-rhythm-engineering.md          06-long-take-multi-beat.md
  07-asset-pipeline.md              08-generator-temperament.md
  09-platform-publishing.md         10-quality-philosophy.md
  11-sound-design.md                12-color-and-light.md
  13-performance-direction.md       14-season-architecture.md
20-craft/<skill-name>/SKILL.md （17 个技能，见第 6 节）
30-taste/
  README.md
  style-cards/<style>.md       风格库卡片
  pairs/<group>.md             好/坏样例对（TP-nn）
  judgment-cards.md            审美判据卡（TJ-nn）
40-memory/
  README.md                    写入方法与分级
  core-memory.md               MEM-nn 条目
50-rubrics/
  README.md
  quality-model.md             Q1–Q8
  definition-of-done.md        "够好了"的可操作定义（回答 G8）
  checklists/{script,storyboard,video-prompt,board,keyframe,video,final-cut,sound-color-performance,publish,season}.md
  scripts/*.py                 可执行检查脚本（见第 8 节）
  scripts/fixtures/            脚本自测样例
60-casebook/
  README.md
  cards/<ID>-<slug>.md         24 张负面案例卡（见第 7 节）
  positive-assets.md           P1–P10、M1–M10 正面资产卡
  drills/README.md
  drills/DR-nn.md              找错题（只含题面）
  drills/answers/DR-nn.md      标准答案 + 打分规则
  traceability.md              判据↔案例 追溯矩阵（由 tools/build_traceability.py 生成）
70-playbooks/
  README.md
  format-contracts.md          文档格式契约（脚本解析依据）
  templates/*.md               剧本/锚点卡/分镜/提示词/剪辑单/报告等模板
  examples/*.md                走通的完整样例
80-sources/
  README.md                    采集评估表（总索引）
  catalog/*.md                 分主题来源条目（S-<CODE>-nn）
90-curriculum/
  README.md
  load-protocol.md             装载协议（给属主的安装指令）
  entry-prompt.md              入学提示词（开工前必读清单）
  training-loop.md             训练回路
  exercises/EX-nn.md           小任务 + 判分方法
  cold-audience-protocol.md    冷观众测试协议
  install-verification.md      装机验证方案（学院验收任务 + 打分规则）
  install/install.sh           一键装载脚本
tools/
  academy_lint.py              全库自检（frontmatter / 链接 / 编号 / 追溯）
  build_traceability.py        生成 60-casebook/traceability.md
```

链接一律用**相对路径**的 Markdown 链接（GitHub 可点），显示文本写**仓库根相对路径**，例如：
`[`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)`。
装载后，agent 以记忆中的"学院根目录"解析这些根相对路径（见 90-curriculum/load-protocol.md）。

## 5. 文档类型格式

### 5.1 理论（10-theory/NN-*.md）
```
# NN · 标题
> 一句话世界模型 ｜ 浓缩案例：A5, M4 ｜ 对应技能：storyboard-long-take, video-prompting-h3
## 核心判决（5–12 条，编号 T03.1 …，每条一句话 + 为什么 + 来源标注）
## 机制解释（为什么会这样：生成器/观众/平台的机制）
## 本管线下的变体（H3 / Qwen / ComfyUI 语境）
## 常见误用（链接案例卡）
## → 行为改变（下次……时，先/改为/禁止……）
## 自测（3–5 个是非/简答题，答案折叠在 <details> 中）
```

### 5.2 技能（20-craft/<name>/SKILL.md）🔒
```
---
name: <与目录同名，小写 kebab-case，≤64 字符>
description: <≤1024 字符。第一句说做什么；随后写"Use when / 触发词：…"，中英文触发词都要有>
---
# <技能中文名>（<name>）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。
## 何时用 / 何时不用
## 输入 → 输出（产物文件与模板链接）
## 步骤（编号；每步写清"做什么 + 用什么脚本/清单验"）
## 判据（引用 R-xxx 条目与 Q 维度）
## 失败模式（每条链接案例卡：症状 → 本技能中的防线）
## 关联（理论、相邻技能、找错题、练习）
```
- frontmatter 只写 `name` 与 `description` 两个键。
- 正文 ≤ 400 行；长内容放 `20-craft/<name>/references/*.md`。

### 5.3 案例卡（60-casebook/cards/<ID>-<slug>.md）🔒
```
---
id: A5
title: 空间调度混乱
group: A 叙事与节奏
scope: 通用          # 通用 | 工程细节 | 项目特有
severity: 致命       # 致命 | 严重 | 一般
provenance: 委托方实证
skills: [storyboard-long-take, video-prompting-h3]
drills: [DR-05]
---
# A5 · 空间调度混乱
## 症状（含人类主创原话，逐字引用档案）
## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）
## 根因（分条；区分"直接原因"与"方法论原因"）
## 修正过程（做了什么、第几轮、结果）
## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）
## → 行为改变（下次……）
## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）
## 关联（技能、理论、判据清单、找错题）
```

### 5.4 验收条目（50-rubrics/checklists/*.md）🔒
每个清单用一张表，**每行一条判据**，列固定为：

```
| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-VP-04 | 提示词中不存在与起始帧方位矛盾的换边运镜词 | [自动]+[目视] | direction_audit 报告 + 起始帧方位声明 | A5, M4 | scripts/direction_audit.py |
```
- **方式**只能是 `[自动]`、`[目视]`、`[冷观众]` 及其组合（`[目视]` = agent 本人或评审 agent 亲自看/听，必须留下证据文件）。
- **溯源**列不得为空，必须含至少一个合法编号（案例 / P / M / T / S / F / GAP）。判据不允许凭空写。
- 检查句必须可判真假；"画面好看"不是检查句，"眯眼去色后主体剪影仍可读"是。

### 5.5 找错题（60-casebook/drills/DR-nn.md + answers/DR-nn.md）
- 题面只给"症状现场描述 / 坏素材描述（坏提示词、坏分镜表、坏验收记录等）"，不给答案、不暗示案例编号。
- 题面末尾固定写：「请输出：①根因（分条）②修正方案（可直接执行）③应新增的判据」。
- 答案文件：标准答案 + 打分规则（满分 10：根因 4 / 修正 4 / 判据 2，列出得分点与常见错答）+ 对应案例编号。

### 5.6 记忆条目（40-memory/core-memory.md）🔒
一行一条，格式：
```
- [MEM-07][空间] 相机的左右移动会把轴线搅乱；轴线由起始帧钉死，只做高度与距离运动。（为什么：r4 复审"苏晓乱跑"，r5 单轴定侧后达标）〔溯源：A5, M4〕
```

### 5.7 好/坏样例对（30-taste/pairs/*.md）
```
## TP-03 · 符号：十字 vs 竖线贯穿
- ❌ 坏：……（具体到提示词原文/画面描述）
- ✅ 好：……
- 点评（≈200 字）：为什么，指出可迁移判据。
- 可迁移判据：……（链接 R-xxx 或 TJ-xx）｜溯源：D4
```

## 6. 技能清单（17 个，名称固定）

| 名称 | 环节 | 主要浓缩案例 |
|---|---|---|
| `production-director` | 总流程：开发→预制作→制作→后期→审片，阶段闸门与产物 | F1–F4, G7 |
| `casting-and-canon` | 从原著建立角色锚点卡与禁用项 | P1, C1, B1 |
| `script-doctor` | 剧本诊断：钩子/节奏/信息密度/对白容量 | D3, A1, GAP-1 |
| `visual-bible` | 视觉设定：色彩剧本/光态/风格库选择 | GAP-4, M2 |
| `asset-boards` | 板图生产：多 seed 抽卡 + 逐特征验收 | P2, C1, C2 |
| `storyboard-long-take` | 长段多拍分镜：段/拍结构、运镜因果、方位审计 | A1, A4, A5, P10 |
| `action-choreography` | 打斗/动作设计：七相动作链、交手回合、战术链 | A2, A3 |
| `keyframe-freeze` | 关键帧冻结：冻结提示词 + 海报级验收 | P3, P4, M2 |
| `video-prompting-h3` | H3 六段提示词：禁令包、对抗约束、对白标记 | D1–D4, A3, A5, B2, B3, E1 |
| `performance-direction` | 表演/表情：微表情、呼吸、视线、身体语言 | GAP-5 |
| `sound-design` | 声音设计：层次/环境声/静场/音乐↔剪辑点 | GAP-3, GAP-6 |
| `shot-qc` | 镜头级验收：抽帧/PSNR/双通道/逐特征放大 | P8, D5, B4, C2 |
| `edit-and-assemble` | 剪辑装配：剪辑单/字幕/叠层/verify | E2, D2, P7 |
| `screening-review` | 自我放映 + 8 维全片自查 + 独立对抗评审 | F1, F2, F3 |
| `cold-audience-test` | 冷观众测试：复述因果、断点记录、回流缺陷单 | F1, GAP-2 |
| `publish-prep` | 发布物料：封面/标题/简介/切片/合规标识（外部调研源） | GAP-1 |
| `multi-episode-arc` | 季级连续性：角色弧线/伏笔/回收/集末钩子 | GAP-7, B1 |

## 7. 案例卡文件名（固定）

```
A1-fragmented-shots      A2-missing-fights        A3-slow-motion-default
A4-unmotivated-camera    A5-spatial-chaos
B1-character-drift       B2-crowd-leak            B3-clone-faces           B4-duplicate-artifacts
C1-banned-items-violated C2-lenient-acceptance
D1-burned-in-captions    D2-solid-black-fails     D3-dialogue-capacity     D4-symbol-errors   D5-qc-tools-lie
E1-slot-order            E2-stale-paths           E3-environment-quirks    E4-prompt-output-mismatch
F1-self-verification-loop F2-proxy-metrics        F3-patch-iteration       F4-skills-not-ability
```

## 8. 脚本公约（50-rubrics/scripts/）🔒

1. **只依赖 Python 3.9+ 标准库 + 系统 `ffmpeg`/`ffprobe`**（媒体类脚本）。可选依赖（OCR、ASR）必须"有则用、无则降级并明确报告降级"，不得因缺依赖崩溃。
2. 每个脚本必须支持 `--selftest`：用 `scripts/fixtures/` 中的样例或 ffmpeg `lavfi` 合成素材自测，退出码 0 = 通过。
3. 输出：默认人类可读报告；`--json` 输出机器可读结果。退出码：0 通过 / 1 发现问题 / 2 用法或环境错误。
4. 脚本头部 docstring 写：用途、溯源编号（如 `溯源：D3, P9, M5`）、输入格式（指向 70-playbooks/format-contracts.md）、用法示例。
5. 脚本**只报告事实，不替人下审美判决**；需要目视的地方，脚本负责产出证据（接触表、裁剪图、帧序列），并在报告里写"需目视：……"。
6. `run_all_selftests.py` 汇总运行全部自测；CI 会跑它。

## 9. 文档格式契约（摘要，全文见 70-playbooks/format-contracts.md）

脚本按以下**表头名**解析 Markdown 表格（列顺序不限，表头必须一致）：

- **分镜表**（分镜.md）：`段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由`
  - `对白` 多句用 ` / ` 分隔，每句 `说话人：台词`；无对白写 `—`。
  - `起始帧方位` 写法：`神=LEFT; 苏晓=RIGHT`（画面位置大写 LEFT / RIGHT / CENTER / FG / BG）。
  - `短镜理由`：时长 < 5s 的镜必填，否则写 `—`。
- **视频提示词**（视频提示词.md）：每镜一个二级标题 `## SHOT-012`，其下：
  - 元数据列表：`- 时长: 10.83`、`- 帧数: 260`（帧数必须落在 17k+5 网格上，124–362）、`- first_frame: REF-SHOT012-START`、`- references: 1=CHR-SUXIAO-BOARD; 2=REF-SHOT011-START`、`- 起始帧方位: 神=LEFT; 苏晓=RIGHT`、`- 轴线策略: 单轴定侧`
  - 一个 ```` ```h3 ```` 代码块，六段各以 `段名:` 顶格起行：`subject_definitions:` / `summary:` / `retention_analysis:` / `detailed_description:` / `overall_soundscape:` / `non_diegetic_music:`；对白写作 `<d>[Chinese] 台词</d>`，由稳定说话人 ID 引出；参考图写作 `<Picture N>`。
- **锚点卡**（锚点卡.md）：每资产一个二级标题 `## ANCHOR: CHR-SUXIAO`，其下必须有一行 `- 锚点句 EN: \`...\``、`- 必现: …`、`- 禁用: …`、`- 来源依据: …`。
- **剪辑单**（剪辑单.md）：`CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字`，`来源`为相对路径。
- **转写对账输入**：`SHOT-012<TAB>文本` 每行一条，或 JSON `{"SHOT-012": "文本"}`。

## 10. 提交与自检

- 每个模块完成即 commit；commit message 写"该模块让 agentos 能多做/少错什么"。
- 提交前运行 `python3 tools/academy_lint.py` 与 `python3 50-rubrics/scripts/run_all_selftests.py`。
