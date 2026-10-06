# 续跑提示词（交给 Codex 继续执行）

> 复制下面"提示词正文"整段给 Codex。它是自包含的：仓库内已有全部上下文，Codex 不需要访问任何外部会话。

---

## 提示词正文

你在仓库 `czzzjj/ai-drama-academy` 的分支 `claude/zealous-wozniak-qawl2l` 上继续建设「AI 短剧制作学院」。草稿 PR：https://github.com/czzzjj/ai-drama-academy/pull/1 。

### 0. 这是什么
一个给 agentos（Claude Code / Codex 一类可装载 SKILL.md 的智能体运行时）装载的**前置课程包**：装载后，agent 能用 ComfyUI + MiniMax H3 + Qwen-Image 全自托管地做季级竖屏短剧。读者是 agent 不是人；每一行都要能落到"agent 下一次生成/验收时的具体动作"。

### 1. 开工前必读（按顺序，读完再写）
1. `CONVENTIONS.md` —— 编号体系、文件地图、来源标注、各类文档格式（§5）、17 个技能名（§6）、案例卡文件名（§7）、脚本公约（§8）。**格式被 `tools/academy_lint.py` 机器校验。**
2. `00-orientation/client-dossier.md` —— 委托方一手证据（唯一来源；不得编造人类原话、数字）。
3. `00-orientation/evidence-reconciliation.md` —— 证据冲突的学院立场 R1–R7、新增根因、画幅规格、合规许可。全库以它为准。
4. `00-orientation/{eight-questions,production-lifecycle,glossary}.md`、`50-rubrics/definition-of-done.md`、`70-playbooks/format-contracts.md`、`50-rubrics/scripts/README.md`。

来源标注：`〔委托方实证·A5〕` / `〔外部调研·S-XXX-nn〕`（只引用 `80-sources/catalog/` 中存在的编号）/ `〔学院推断〕`（必须写验证方法）。

### 2. 已完成（不要重写，只在必要时小改）
- 00-orientation 全部；CONVENTIONS / CLAUDE.md / AGENTS.md / README.md
- 80-sources/catalog：9 个主题、217 条已核实来源（S-）、226 条关键事实（F-）
- 60-casebook：24 张案例卡、正面资产卡、22 道找错题 + 答案、README
- 50-rubrics：quality-model（Q1–Q8）、definition-of-done（L0–L3）、10 份阶段清单共 228 条判据（R-）、12 个检查脚本 + `run_all_selftests.py`（全部 PASS）
- 10-theory：14 篇理论 + README
- 30-taste：风格卡、35 组好/坏样例对（TP-）、18 张审美判据卡（TJ-）
- 20-craft：17 个技能（若 `ls 20-craft | wc -l` 少于 18 项（含 README），补齐缺的，格式见 CONVENTIONS §5.2）
- 40-memory：core-memory（目标 50–60 条 MEM-）；70-playbooks/templates：14 个模板（若缺，补齐）

### 3. 你要完成的剩余工作（按优先级）

**P5-1 课程层 `90-curriculum/`**（最高优先级，学院验收的核心）
- `README.md`：课程层索引。
- `load-protocol.md`：给属主的安装指令——克隆到固定 `ACADEMY_HOME`；把 `20-craft/*` 软链接进运行时技能目录（Claude Code：`~/.claude/skills/` 或项目 `.claude/skills/`；Codex 对应目录）；把 `40-memory/core-memory.md` 的 Top-12 写入长期记忆，并写一条"学院根目录 = <路径>，技能中 `60-casebook/...` 等路径相对此根"；判据挂进验收流程；风格卡挂进 visual-bible；**改技能后必须重启运行时**（E3-3）；四个人类拍板点；许可提醒（evidence-reconciliation 第四部分）。
- `install/install.sh`：bash、幂等，参数 `--target-skills-dir`、`--dry-run`；建软链接、写 `ACADEMY_HOME` 文件、打印待写入的记忆条目；不联网。
- `entry-prompt.md`：可直接粘贴给 agent 的"入学提示词"：必读顺序、八问自检、开工前最低学分、日常规则（病灶路由、交付声明、禁止只自证）。
- `training-loop.md`：加载 → 找错题（DR）→ 小任务（EX）→ 用脚本/判据自动判分 → 对照答案复盘 → 把新的人类反馈写成新找错题。最低学分：找错题 ≥10 道且均分 ≥7/10；小任务 ≥5 个通过；装机验证 ≥70 分。
- `exercises/EX-01.md … EX-10.md`：每个含输入、期望产出、**用真实脚本的自动判分命令**。建议题目：对白容量核算；把均长 2.96s 的分镜改写为长段多拍；15 秒打斗战术链；方位词审计修复；正向优先的禁令改写；AIGC 显式标识叠层规格（GB 45438：字高 ≥ 短边 5%、≥2s、起始画面边角）；反馈翻译 A/B；病灶路由；9:16 关键帧冻结提示词；发布合规清单。脚本命令以 `50-rubrics/scripts/README.md` 与各脚本 `--help` 为准，不得编造参数。
- `cold-audience-protocol.md`：招募、单次观看、复述因果链、断点标记、"想不想看下一集"、记录表（`70-playbooks/templates/cold-audience-sheet.md`）、阈值（definition-of-done L1/L3）、替身 agent 降级规则、缺陷单按病灶回流。
- `install-verification.md`：学院验收任务——一个从未学过短剧的新 agent 会话装载学院后，针对给定的 15 秒 BOSS 打斗拍，产出：分镜行、战术链、H3 Ref2VA 提示词、用脚本的自查报告。写清输入、交付物、100 分评分表（自动部分：脚本退出码/规则代码；评审部分：作者或独立评审会话）、通过线 ≥70、**对照组**（同任务不装载学院）、结果记录方式。

**P5-2 `80-sources/README.md`**：采集评估表总索引——读 `80-sources/catalog/*.md`，给出按主题/分类（🟢/🟡/⚪）计数、总表（ID、名称、分类、许可、核实、落点模块，链接到各条目）、"agent 真正该打开的 Top 20"、汇总各目录的"空白与未找到"，并声明全部为外部调研。

**P5-3 `tools/build_traceability.py` → `60-casebook/traceability.md`**（标准库）：解析 `50-rubrics/checklists/*.md` 的 `编号/溯源` 列、案例卡 frontmatter（skills、drills）、答案文件提到的案例编号、各 SKILL.md 提到的案例编号；对每个档案编号（A1..F4、P1..P10、M1..M10、GAP-1..7）列出引用它的判据、技能、找错题；末尾列出"零判据覆盖"的编号。运行并提交生成文件。

**P5-4 `70-playbooks/examples/fight-segment-worked-example.md`**：一个 12–15s BOSS 打斗段的完整走通样例（分镜行 → 七相动作链 + 战术链 → 9:16 关键帧冻结提示词 → H3 Ref2VA 六段提示词（禁令包、单轴定侧、画面位置称呼、闭嘴句、无配乐写 N/A）→ 检查命令（segment_rhythm / dialogue_capacity / h3_frame_grid / prompt_lint / direction_audit）→ QC 记录骨架）。用通用角色，不用委托方小说人物。分镜表与提示词块必须符合 format-contracts，让脚本能通过。

**P5-5 全库收口**
1. `python3 tools/academy_lint.py`（严格模式，不带 `--links-as-warnings`）→ 修到 0 错误（主要是悬空链接：要么补文件，要么改链接）。
2. `python3 50-rubrics/scripts/run_all_selftests.py` → 全部 PASS。
3. 更新 `README.md` 中与实际不一致的地方（如技能数、条目数）；删除本文件 `HANDOFF-CODEX.md` 或在其顶部注明"已完成"。

### 4. 硬性规则
- 文件/目录名英文 kebab-case（E3-1）；内容中文，提示词英文。
- 技能 frontmatter 只允许 `name`（=目录名）和 `description`（≤1024 字符，含中英文触发词与"不负责…"边界）。
- 判据表列固定：`编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具`；方式只能是 `[自动]/[目视]/[冷观众]`；溯源不得为空。
- 记忆条目格式：`- [MEM-nn][域] 规则（为什么：…）〔溯源：…〕`。
- 不改 `50-rubrics/scripts/*.py` 的行为（除非修 bug，且修后跑 `run_all_selftests.py`）。
- 委托方没做过的（平台发布、流量、冷观众、声音设计）一律标〔外部调研〕或〔学院推断〕。

### 5. 提交
- 每完成一个模块就 commit，message 写"该模块让 agentos 能多做/少错什么"。
- `git push -u origin claude/zealous-wozniak-qawl2l`；全部完成后把 PR #1 从草稿改为可审（Ready for review），并更新 PR 描述中的进度清单。
