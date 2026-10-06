# 装载协议（给属主的安装指令）

> 读者：agentos 的属主（人类），或被属主授权执行安装的 agent。一句话：**克隆到固定路径 → 链接技能 → 写入记忆 → 接进验收流 → 重启运行时 → 验证。** 少一步，学院就只是一堆没人读的文件〔F4：技能不等于能力〕。
> 工具：[`90-curriculum/install/install.sh`](install/install.sh)（幂等、无网络、不改仓库内容）。装完后的入学与验证：[`90-curriculum/entry-prompt.md`](entry-prompt.md) → [`90-curriculum/training-loop.md`](training-loop.md) → [`90-curriculum/install-verification.md`](install-verification.md)。

---

## 1. 前置条件

| 项 | 要求 | 为什么 |
|---|---|---|
| 学院根目录 `ACADEMY_HOME` | 固定、**纯英文、无空格**路径（例 `~/ai-drama-academy`），装完不要再搬 | 中文路径会在 cmd 裸跑时吞输出〔委托方实证·E3-1〕；技能里的 `60-casebook/...` 等路径全部相对这个根解析，搬走 = 全部失效 |
| Python | 3.9+，仅标准库 | 检查脚本只依赖标准库〔[`CONVENTIONS.md`](../CONVENTIONS.md) §8〕 |
| ffmpeg / ffprobe | 在 PATH 中 | 媒体类脚本（`contact_sheet.py` `psnr_scan.py` `loudness_verify.py` 等）需要；缺失时它们明确 SKIP/退出码 2，不会静默通过 |
| bash | install.sh 需要 | Windows：用 Git Bash 或 WSL 跑 install.sh；若运行时在原生 Windows，改用目录联接 `mklink /J <技能目录>\<name> <ACADEMY_HOME>\20-craft\<name>` 或直接复制（复制后学院更新需重复复制）〔学院推断，未在 Windows 实机验证〕 |

---

## 2. 安装步骤

### 步骤 1 · 克隆到固定 ACADEMY_HOME

```bash
git clone <this-repo> ~/ai-drama-academy
export ACADEMY_HOME=~/ai-drama-academy
```

### 步骤 2 · 技能：把 `20-craft/*` 链接进运行时技能目录

```bash
bash "$ACADEMY_HOME/90-curriculum/install/install.sh" --dry-run    # 先看它会做什么
bash "$ACADEMY_HOME/90-curriculum/install/install.sh"              # 默认装到 ~/.claude/skills
bash "$ACADEMY_HOME/90-curriculum/install/install.sh" --target-skills-dir DIR   # 其他运行时/项目级
```

| 运行时 | 技能目录（`--target-skills-dir`） | 说明 |
|---|---|---|
| Claude Code，全局 | `~/.claude/skills/`（默认值） | 对本机所有项目生效 |
| Claude Code，项目级 | `<项目根>/.claude/skills/` | 只对该项目生效；短剧项目推荐用这个，避免污染其他项目 |
| Codex | 所用版本的技能目录（以其官方文档为准，常见为 `~/.codex/skills/`） | 路径以运行时文档为准，不要照抄本表〔学院推断〕 |

脚本行为：对每个含 `SKILL.md` 的 `20-craft/<name>/` 建符号链接 `DIR/<name> → $ACADEMY_HOME/20-craft/<name>`（17 个）；已是正确链接则跳过，指向别处则更新；目标处已有同名**真实目录/文件**则跳过并以退出码 1 报告（先手动移走旧拷贝再重跑）；写入 `$ACADEMY_HOME/.academy_home`（一行：根目录绝对路径）；打印可粘贴的记忆行；打印"请重启运行时"。

### 步骤 3 · 记忆：Top-12 + 根目录条目逐字写入长期记忆

install.sh 的第 3 段输出（`BEGIN MEMORY` … `END MEMORY` 之间）就是要写入的全部内容。**逐字**粘贴，不改写、不合并、不摘要：

1. [`40-memory/core-memory.md`](../40-memory/core-memory.md) 第一个 `##` 标题（Top-12）下的 12 条 `MEM-01`–`MEM-12`；
2. 一条根目录条目：`学院根目录 = <ACADEMY_HOME>；技能里 60-casebook/... 等路径相对此根`（脚本会把 `<ACADEMY_HOME>` 替换成真实路径）。没有这一条，agent 读到 SKILL.md 里的 `60-casebook/cards/A5-spatial-chaos.md` 会按当前工作目录去找，找不到后开始凭印象答。

落点：Claude Code → `~/.claude/CLAUDE.md`（全局）或项目 `CLAUDE.md` / 记忆库；Codex → `AGENTS.md` 或其记忆机制。装完数一遍：必须恰好 12 条 MEM + 1 条根目录条目。

T2 分域条目（MEM-13–MEM-60）**不进常驻记忆**，进入对应阶段/技能时再装（分级见 [`40-memory/README.md`](../40-memory/README.md) §1）；案例卡、判据、脚本参数不进记忆，只在记忆里写路径或编号（T3）。

### 步骤 4 · 验收流：把 `50-rubrics` 的清单与脚本接进项目的"验收"

在项目的 `CLAUDE.md` / `AGENTS.md`（或运行时等价物）写入一节"验收"，内容固定为下表的接线（命令前缀统一 `python3 $ACADEMY_HOME/50-rubrics/scripts/`，参数见 [`50-rubrics/scripts/README.md`](../50-rubrics/scripts/README.md) §1、§5）：

| 阶段闸门 | 必过清单（[`50-rubrics/checklists/`](../50-rubrics/checklists/)） | 必跑脚本（0 error 才放行） |
|---|---|---|
| 分镜定稿 → animatic（人类拍板点②前） | `script.md` `storyboard.md` `board.md` | `segment_rhythm.py` `dialogue_capacity.py` |
| 送 H3 之前（prepare 前） | `video-prompt.md` `keyframe.md` | `h3_frame_grid.py` `prompt_lint.py` `direction_audit.py` `slot_order_check.py` |
| 每条出片后（进剪辑前） | `video.md` | `contact_sheet.py` `psnr_scan.py` `burnin_text_scan.py` `transcript_reconcile.py` + 目视证据 |
| 成片（渲染前后） | `final-cut.md` `sound-color-performance.md` | `asset_exists.py` `loudness_verify.py` |
| 审片（人类拍板点③前） | `season.md`（季内集）+ [`definition-of-done.md`](../50-rubrics/definition-of-done.md) | 自我放映、独立评审、冷观众（[`90-curriculum/cold-audience-protocol.md`](cold-audience-protocol.md)） |
| 发布前（人类拍板点④前） | `publish.md` | 合规表（见 §4） |

写进验收节的三条硬规则：
1. 任何一条验收记录必须附证据文件路径；"通过"二字不是证据〔C2、F1〕；
2. 脚本参数（`--margin` `--rate` 等）不得为消 error 而调〔R-SB-16〕；
3. 交付声明按 [`definition-of-done.md`](../50-rubrics/definition-of-done.md) §4 写，缺证据的级别写"未验证"。

若运行时支持 hooks，可在 prepare/confirm/run 前自动触发 `prompt_lint.py` 与 `direction_audit.py`，失败则阻断〔学院推断；未在任何运行时验证，验证法：故意送一条 `VP-ban` 缺失的提示词，看是否被拦下〕。

### 步骤 5 · 风格卡：接进 visual-bible

[`30-taste/style-cards/`](../30-taste/style-cards/) 有 7 张风格卡：`cinematic-realism` `dark-fantasy-epic` `guoman-2d` `ink-wash` `motion-comic-2d` `stylized-3d` `chibi`。在项目的视觉设定入口（模板 [`70-playbooks/templates/visual-bible.md`](../70-playbooks/templates/visual-bible.md)）写明"风格卡取自 `$ACADEMY_HOME/30-taste/style-cards/`，由 `visual-bible` 技能选定并在 `visual-bible.md` 里逐字落地"。属主在拍板点①确认题材时一并确认所选风格卡；开工后更换风格卡 = 重做板图，必须重新过拍板点②〔学院推断〕。

### 步骤 6 · 重启运行时

**改完技能目录必须重启运行时**：技能在装配期一次性扫描，装/改后不重启不生效〔委托方实证·E3-3〕。重启前如要立即使用，可直接读 `20-craft/<name>/SKILL.md` 正文（同样 E3-3：正文文件可直接读取使用），但不要把"能读"当成"已装载"。

重启后自检（全部为真才算装好）：
- 运行时的技能列表里能看到 17 个学院技能（名称见 [`20-craft/README.md`](../20-craft/README.md) §2）；
- 记忆里能复述 MEM-01 与根目录条目；`cat "$ACADEMY_HOME/.academy_home"` 输出的路径与记忆里的一致；
- `python3 "$ACADEMY_HOME/50-rubrics/scripts/run_all_selftests.py" --quick` 退出码 0（媒体类 SKIP 需注明原因，有 ffmpeg 时去掉 `--quick` 全跑）。

### 步骤 7 · 入学、训练、验证

让 agent 读 [`90-curriculum/entry-prompt.md`](entry-prompt.md)；完成 [`90-curriculum/training-loop.md`](training-loop.md) 的最低学分；跑 [`90-curriculum/install-verification.md`](install-verification.md)，≥70 分才算"装机验证通过"。**未通过最低学分与装机验证前，agent 不得开始任何一集的正式制作**（G3：只装技能 = 只做了乘法的第一项）。

---

## 3. 四个人类拍板点

学院只在这四处打扰人类，其余由 agent 自主完成（[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) §5）。属主在装载时就要知道自己会被问哪四件事：

| # | 时机 | 人类看什么 | agent 必须先准备好 |
|---|---|---|---|
| ① | 开发结束 | 季结构、题材、对标（含风格卡选择） | `season-bible.md`、`episode-map.md`、`benchmarks.md` |
| ② | 预制作结束 | animatic | 分镜表、对白容量报告、动作设计 |
| ③ | 审片结束 | 成片 + 审片包 | 自我放映、8 维评分、独立评审、冷观众记录（L1 + 8 维自评 + 独立评审意见是最低交付要求，[`definition-of-done.md`](../50-rubrics/definition-of-done.md) §1） |
| ④ | 发布前 | 发布物料 | `publish-kit.md`、合规清单（§4 全部项已确认或已上报） |

agent 越过任何一个拍板点（尤其④：自行发布）= 违规；人类在拍板点之间没有被问到的事，agent 不得回头来问，按学院判据自决并留证据。

---

## 4. 合规与许可提醒（发布前由人类拍板）

委托方从未发布过作品（GAP-1），以下全部是外部调研，**不构成法律意见**；完整表格与来源见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) 第四部分，属主必须在拍板点④前亲自读一遍：

- **MiniMax H3 排除地域**：社区许可把美国、欧盟、英国、韩国列为 Excluded Territories，并禁止在许可地域外使用/展示输出；发往含这些地区的平台（如 YouTube、TikTok）前必须取得授权〔外部调研·S-H3-14〕。商用与 ComfyUI 本地输出的授权表述尚需属主与 Comfy/MiniMax 确认〔S-COMFY-09〕。
- **Qwen-Image-2.1 研究许可**：Qwen Research License 仅限研究/评估，商用需另签商业许可；变现短剧属商用〔外部调研·S-COMFY-01、S-COMFY-02〕。
- 配乐模型、AIGC 显式/隐式标识、微短剧备案编号等项见同一表格；任一"未确认"，agent 必须上报拍板点④，不得自行发布〔MEM-12〕。

---

## 5. 升级与卸载

- 升级：`git -C "$ACADEMY_HOME" pull` → 重跑 install.sh（幂等：新增技能被链接，已有链接不变）→ 对照新的 `core-memory.md` Top-12 更新记忆 → **重启运行时**。
- 卸载：`find DIR -maxdepth 1 -type l -lname "$ACADEMY_HOME/20-craft/*" -delete`（只删指向学院的链接），再手动删记忆里的 MEM 条目与根目录条目。

---

## → 行为改变

- 属主下次装载时：不再"把仓库放进去就算装好"，按步骤 1–7 逐项勾；缺记忆写入（步骤 3）或缺重启（步骤 6）就视为未装载。
- agent 下次读到 SKILL.md 里的 `60-casebook/...` 路径时：先取记忆里的学院根目录再拼路径，禁止按当前工作目录猜。
- agent 下次改了技能目录而技能"没反应"时：先判断是不是没重启（E3-3），再怀疑别的。
