---
id: E3
title: 环境怪癖三则
group: E 流程工程
scope: 工程细节
severity: 一般
provenance: 委托方实证
skills: [production-director]
drills: [DR-15]
---
# E3 · 环境怪癖三则

> 一句话：**"没有输出"不等于"成功"，"装上了"不等于"生效了"，"命令发出去了"不等于"任务跑完了"。** 判断成败看退出码和产物文件，不看终端里显示了什么。

## 症状（含人类主创原话，逐字引用档案）

| 编号 | 症状 | 委托方修正 |
|---|---|---|
| E3-1 | 中文路径 + 在 cmd 里裸跑多行中文命令，输出被吞掉 | 一律改成写 `.py` 脚本文件再执行 |
| E3-2 | 终端工具 10 分钟超时，长任务被掐断 | 长任务挂后台或用独立进程 |
| E3-3 | 技能或插件装好、改好之后，不重启就不生效（只在装配期扫描一次） | 改完必须重启运行时；技能正文文件可以直接读取使用 |

〔委托方实证·E3-1、E3-2、E3-3〕。档案没有保留人类主创关于本案的「」逐字原话。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 三则都发生在委托方的运行环境里：Windows cmd、终端工具有 10 分钟超时、运行时在装配期扫描技能〔委托方实证·E3〕。档案没有记录具体是哪次任务、损失了多少。
- 学院已经把 E3-1 落进公约：文件名和目录名一律用英文 kebab-case（[`CONVENTIONS.md`](../../CONVENTIONS.md) §1.6）；`academy_lint.py` 检查路径里有没有中文；所有检查脚本在非 UTF-8 控制台（GBK）下会把无法编码的字符替换成 `?`，不会崩溃（[`50-rubrics/scripts/README.md`](../../50-rubrics/scripts/README.md) §3）。

## 根因（分条；区分"直接原因"与"方法论原因"）

1. **直接原因（E3-1）**：控制台编码与 UTF-8 中文不一致，输出被吞或乱码，而命令本身可能已经执行，也可能没执行。
2. **直接原因（E3-2）**：用同步阻塞的方式跑生成或渲染这类长任务，时长超过了工具的硬超时。
3. **直接原因（E3-3）**：运行时只在启动时装载技能清单。
4. **方法论原因**：用终端回显判断成败。回显被吞、被截断、被超时打断时，agent 会做出错误推断：要么误以为成功，要么重复提交。
5. **外部佐证**：ComfyUI 本身支持异步提交：`POST /prompt` 拿到 `prompt_id`，再轮询 `GET /history/{prompt_id}`，或者监听 WebSocket，收到 `executing` 且 `node` 为空时判定完成〔外部调研·S-COMFY-10〕。生产闸门的做法是：中断后先用 audit 找出 `orphaned_provider_job`，用 collect 取回已计费的结果，不重投〔外部调研·S-ZEN-10、F-ZEN-24〕。

## 修正过程（做了什么、第几轮、结果）

- 委托方：脚本文件模式、后台或独立进程、改完重启〔委托方实证·E3〕。
- 学院补充（〔学院推断〕，用一次真实长任务验证：提交 → 主动断开终端 → 重新轮询，能取回同一个 `prompt_id` 的产物即为通过）：
  - 长任务改成"提交 → 记下 `prompt_id`、seed、prompt JSON → 每次轮询远低于超时 → 从 history 取产物"的模式。
  - 中断之后先查队列和 history，再决定要不要重投。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 所有生产文件和目录名不含中文。`academy_lint.py` 的路径检查通过〔E3-1；format-contracts §0.1〕。
- [自动] 每一步的成败以"退出码 + 预期产物文件存在且非空"判定，不以终端回显判定。检查脚本统一用退出码 0/1/2〔E3〕。
- [自动] 预计超过 5 分钟的任务（H3 生成、整集渲染；阈值取 10 分钟超时的一半，〔学院推断〕）一律后台运行或走 API 异步提交。提交记录里写下 `prompt_id`，产物从 history 获取〔E3-2；S-COMFY-10〕。
- [自动] 中断后重投之前，先查 `GET /queue` 和 `GET /history/{prompt_id}`，确认没有已经完成或正在跑的同一任务〔E3-2；S-ZEN-10〕。
- [目视] 安装或修改技能后，重启运行时，并确认技能清单里出现了新技能；没出现时，直接读取 `SKILL.md` 正文继续工作〔E3-3〕。

## → 行为改变（下次……）

- 下次要跑多行或带中文的命令，先写成 `.py` 文件，再用 `python3 文件.py` 执行。输出写进文件，再读文件。
- 下次跑生成或渲染，先估时长，超过 5 分钟就异步提交、轮询取回。**禁止**在一个同步调用里等它跑完。
- 下次看到"命令没输出"，先查退出码和产物文件，再决定下一步。**禁止**直接重跑。
- 下次装载或更新学院技能，按 [`90-curriculum/load-protocol.md`](../../90-curriculum/load-protocol.md) 重启运行时，再按 [`90-curriculum/install-verification.md`](../../90-curriculum/install-verification.md) 验证生效。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ☆ cmd 编码、10 分钟超时、装配期扫描都是委托方环境的具体参数，换运行时要重查。
- ★ "成败看退出码和产物""长任务异步提交加轮询""中断先查再投"适用于任何 agent 运行时。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（三步闸门、异步提交、中断恢复）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)。
- 判据清单：本案没有专属清单，装机验证见 [`90-curriculum/install-verification.md`](../../90-curriculum/install-verification.md)。
- 脚本：[`50-rubrics/scripts/run_all_selftests.py`](../../50-rubrics/scripts/run_all_selftests.py)（装载后自检）、[`tools/academy_lint.py`](../../tools/academy_lint.py)（路径无中文）。
- 找错题：[`60-casebook/drills/DR-15.md`](../../60-casebook/drills/DR-15.md)（环境 / 提示词≠产出）。
- 相邻案例：[`60-casebook/cards/E2-stale-paths.md`](E2-stale-paths.md)（行尾零扰动）、[`60-casebook/positive-assets.md`](../positive-assets.md)（P6、M9）。
