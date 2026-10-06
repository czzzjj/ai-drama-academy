# 续跑提示词（任何节点都可交给 Codex）

> 把下面"提示词正文"整段交给 Codex。它不依赖任何会话记忆：Codex 先**探测**仓库当前做到哪一步，再从第一个未完成项继续。

---

## 提示词正文

你在 GitHub 仓库 `czzzjj/ai-drama-academy` 上继续建设「AI 短剧制作学院」。主分支 `main` 已包含前期全部成果。工作分支用 `claude/zealous-wozniak-qawl2l`（若它已被合并或不存在，就从最新 `main` 新建同名分支）；完成后向 `main` 提 PR 并合并（若属主允许直接推 main，也可以直接推）。

### 0. 这是什么
一个给 agentos（Claude Code / Codex 一类可装载 SKILL.md 的智能体运行时）装载的**前置课程包**：装载后，agent 能用 ComfyUI + MiniMax H3 + Qwen-Image 全自托管地做季级竖屏短剧。读者是 agent；每一行都要能落到"agent 下一次生成/验收时的具体动作"。

### 1. 必读（先读再写）
1. `CONVENTIONS.md`：编号体系、文件地图（§4）、来源标注、文档格式（§5）、技能名（§6）、脚本公约（§8）。格式被 `tools/academy_lint.py` 机器校验。
2. `00-orientation/client-dossier.md`：委托方一手证据（唯一来源；不得编造人类原话或数字）。
3. `00-orientation/evidence-reconciliation.md`：证据冲突的学院立场 R1–R7、画幅规格、合规许可。全库以它为准。
4. 按需：`00-orientation/{eight-questions,production-lifecycle,glossary}.md`、`50-rubrics/definition-of-done.md`、`70-playbooks/format-contracts.md`、`50-rubrics/scripts/README.md`。

来源标注：`〔委托方实证·A5〕` / `〔外部调研·S-XXX-nn〕`（只引用 `80-sources/catalog/` 中存在的编号）/ `〔学院推断〕`（须写验证方法）。

### 2. 进度探测（每次开工先跑）
```bash
git log --oneline -5
ls 90-curriculum 90-curriculum/exercises 90-curriculum/install 2>/dev/null
ls 80-sources/README.md 60-casebook/traceability.md tools/build_traceability.py 70-playbooks/examples 2>/dev/null
ls 20-craft | wc -l                        # 应为 18（17 技能 + README）
grep -c '^- \[MEM-' 40-memory/core-memory.md   # 应 ≥ 50
python3 tools/academy_lint.py --links-as-warnings | tail -2
```
对照下表，**从第一个"未完成"的行开始做**；已存在且非空的文件不要重写，只补缺口。

| # | 模块 | 完成标准（文件存在且内容完整） |
|---|---|---|
| 1 | 课程层 `90-curriculum/` | `README.md`、`load-protocol.md`、`install/install.sh`（可执行）、`entry-prompt.md`、`training-loop.md`、`cold-audience-protocol.md`、`install-verification.md` |
| 2 | 小任务 | `90-curriculum/exercises/EX-01.md … EX-10.md`（每题含输入、期望产出、用真实脚本的自动判分命令） |
| 3 | 采集总索引 | `80-sources/README.md`（按主题/分类计数、总表、Top 20、空白汇总） |
| 4 | 追溯矩阵 | `tools/build_traceability.py` + 生成的 `60-casebook/traceability.md` |
| 5 | 走通样例 | `70-playbooks/examples/fight-segment-worked-example.md` + `70-playbooks/examples/fight-segment/{storyboard,anchors,video-prompts}.md`（脚本可通过） |
| 6 | 收口 | `python3 tools/academy_lint.py`（严格模式，不带 `--links-as-warnings`）0 错误；`python3 50-rubrics/scripts/run_all_selftests.py` 全 PASS；`README.md` 中的数字与实际一致；本文件顶部标注"已完成"或删除 |
| 7 | 可选增强 | `.github/workflows/academy-check.yml` 跑上述两条命令；SKILL.md 重排为短行；`70-playbooks/examples/` 增加对白戏样例 |

### 3. 各模块要点
- **load-protocol / install.sh**：克隆到固定 `ACADEMY_HOME`；把 `20-craft/*` 软链接进运行时技能目录（Claude Code：`~/.claude/skills/`；Codex：其技能目录）；把 `40-memory/core-memory.md` 的 Top-12 写入长期记忆，并加一条"学院根目录 = <路径>"；改技能后**必须重启运行时**（委托方实证 E3-3）；四个人类拍板点；许可提醒（evidence-reconciliation 第四部分：H3 排除地域、Qwen-Image-2.1 研究许可）。install.sh：幂等、`--target-skills-dir`、`--dry-run`、不联网。
- **entry-prompt**：可直接粘贴给学习者 agent：必读顺序、八问自检、开工前最低学分（找错题 ≥10 道均分 ≥7/10、小任务 ≥5 个通过、装机验证 ≥70 分）、日常规则（病灶路由、L0–L3 交付声明、禁止只自证、发布前合规闸门）。
- **training-loop**：加载 → 找错题（只给题面，再用 answers/ 判分）→ 小任务 → 脚本/判据自动判分 → 复盘 → 把每条新的人类反馈写成新找错题。
- **cold-audience-protocol**：≥3 名冷观众、手机竖屏单次连续观看、复述因果链、断点时间码、"想不想看下一集"、记录表 `70-playbooks/templates/cold-audience-sheet.md`、阈值取自 definition-of-done、替身 agent 降级规则、断点转缺陷单并按病灶回流。注明委托方从未做过（GAP-2），方法为〔外部调研〕。
- **install-verification**：一个从未学过短剧的新 agent 会话装载学院后，针对给定的 15 秒 BOSS 打斗拍（通用角色），交付分镜行、七相动作链 + 战术链、H3 Ref2VA 六段提示词、用脚本的自查报告；100 分（40 自动：脚本退出码/规则代码；60 评审）；通过线 ≥70；**对照组**（同任务不装载学院）。
- **exercises**：脚本命令以 `50-rubrics/scripts/README.md` 与各脚本 `--help` 为准，不得编造参数；内嵌材料须符合 format-contracts（含 `- 模式: Ref2VA`、`角色映射` 等）。

### 4. 硬性规则
- 文件/目录名英文 kebab-case（E3-1）；内容中文，提示词英文。
- 技能 frontmatter 只允许 `name`（=目录名）与 `description`（≤1024 字符，含中英触发词与"不负责…"边界）。
- 判据表列固定：`编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具`；方式只能是 `[自动]/[目视]/[冷观众]`；溯源不得为空。
- 记忆条目格式：`- [MEM-nn][域] 规则（为什么：…）〔溯源：…〕`。
- 不改 `50-rubrics/scripts/*.py` 的行为（修 bug 后须跑 `run_all_selftests.py`）。
- 委托方没做过的（平台发布、流量、冷观众、声音设计）一律标〔外部调研〕或〔学院推断〕。

### 5. 提交
每完成一个模块就 commit（message 写"该模块让 agentos 能多做/少错什么"）并 push；全部完成后合并进 `main`。
