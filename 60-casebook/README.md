# 案例库（Casebook）

> 委托方真实生产中的 24 个负面案例（A1–F4）+ 20 项正面资产（P1–P10、M1–M10），每一条都来自 [`00-orientation/client-dossier.md`](../00-orientation/client-dossier.md)。
> 用途：**生成或验收时遇到一个症状，30 秒内查到"它是哪一类病、病灶在哪、哪个技能管、哪个脚本能拦"。**
> 装载顺序：先读 F 组四张卡（它们决定你怎么对待其余 20 张），再按症状查。

## 1. 怎么用

1. **按症状查**（最常用）：收到人类反馈或自己看到异常 → 查第 2 节的症状表 → 打开案例卡，先读「→ 行为改变」与「可固化判据」，再读「根因」。
2. **按阶段查**：开一个新阶段前，读该阶段相关的卡（第 4 节）；病灶阶段的判定以 [`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) §3 为准。**缺陷在哪里被看见 ≠ 缺陷在哪里产生。**
3. **按训练查**：每张卡的 `drills` 字段指向找错题，题面在 [`60-casebook/drills/`](drills/README.md)，答案与打分规则在 `drills/answers/`。先做题，再看卡。
4. **正面资产**：[`60-casebook/positive-assets.md`](positive-assets.md)——P/M 卡是默认工序，负面卡是它们失守时的样子。
5. **追溯**：判据 ↔ 案例矩阵见 [`60-casebook/traceability.md`](traceability.md)（由 `tools/build_traceability.py` 生成，不手改）。

**规则**：
- 引用案例时必须带来源标注：`〔委托方实证·A5〕` / `〔外部调研·S-xxx-nn〕` / `〔学院推断〕`（后者必须写验证法）。
- 人类原话只引用档案中「」内的句子，逐字，不截断改写。
- 新出现的缺陷先归入 24 类之一，写进该卡的「现场」作为新子案；确属新类时，先改 [`CONVENTIONS.md`](../CONVENTIONS.md) §7 与 `tools/academy_lint.py` 的 `CASE_FILES`，再建卡。
- 每个被人类指出、而自查没先发现的问题，当轮补一道找错题 + 一条判据（[`60-casebook/cards/F1-self-verification-loop.md`](cards/F1-self-verification-loop.md)）。

## 2. 症状 → 案例 → 技能 → 脚本

| 你看到 / 听到的症状 | 案例 | 主责技能 | 能拦的脚本（规则代码）或检查方式 |
|---|---|---|---|
| 「片段式、剧情跳跃、无法理解」；均镜长 <5s；一个动作一个镜号 | [A1](cards/A1-fragmented-shots.md) | storyboard-long-take | `segment_rhythm.py`（`A1-mean-short`、`A1-short-no-reason`）；`psnr_scan.py --mode final` |
| 「几乎没有做 BOSS 打斗」；只有动作瞬间 + 反应镜头 | [A2](cards/A2-missing-fights.md) | action-choreography | [目视] 至少 1 个完整交手回合 |
| 「全是几个简单动作的慢镜头」；全片无速度层次 | [A3](cards/A3-slow-motion-default.md) | action-choreography | `prompt_lint.py`（`VP-realtime`） |
| 「无电影级运镜」；运镜说不出为什么 | [A4](cards/A4-unmotivated-camera.md) | storyboard-long-take | `segment_rhythm.py`（`A4-cause`）+ 接触表核对 |
| 「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」；左右互换 | [A5](cards/A5-spatial-chaos.md) | storyboard-long-take | `direction_audit.py`（`DIR-camera`、`DIR-side`、`DIR-path`） |
| 主角脸与板图不符；"穿帮" | [B1](cards/B1-character-drift.md) | casting-and-canon | `contact_sheet.py --keyframe --crop` |
| 背景人群被扩写成具体人物/物件、扩散变形 | [B2](cards/B2-crowd-leak.md) | video-prompting-h3 | `prompt_lint.py`（`VP-crowd`） |
| 同框几张脸雷同；多出不存在的光柱 | [B3](cards/B3-clone-faces.md) | video-prompting-h3 | `prompt_lint.py`（`VP-distinct`、`VP-light`） |
| 背景里出现关键帧没有的元素（"第二骨架"） | [B4](cards/B4-duplicate-artifacts.md) | shot-qc | `contact_sheet.py --keyframe`（`B4-keyframe`） |
| 生成器自行加了宝石/铠甲/颈饰/远山/刻纹；左右臂方位反 | [C1](cards/C1-banned-items-violated.md) | asset-boards | `prompt_lint.py`（`VP-anchor`、`VP-negative`）；`contact_sheet.py --crop` |
| 验收记录只有"通过"；复验推翻初验 | [C2](cards/C2-lenient-acceptance.md) | shot-qc | `asset_exists.py qc/`（`E2-missing-ref`、`E2-empty-asset`） |
| 画面里出现字幕/文字 | [D1](cards/D1-burned-in-captions.md) | video-prompting-h3 | `burnin_text_scan.py`（`D1-burnin-text`）；`prompt_lint.py`（`VP-ban`） |
| 纯黑/纯色卡被加 "LAVCE" 等水印 | [D2](cards/D2-solid-black-fails.md) | edit-and-assemble | `burnin_text_scan.py`（`D2-watermark`）；`prompt_lint.py`（`VP-generator-unsafe`） |
| 换 seed 各缺不同句；台词赶 | [D3](cards/D3-dialogue-capacity.md) | script-doctor | `dialogue_capacity.py`（`D3-capacity`、`D3-rushed`）；`transcript_reconcile.py`（`TR-missing`） |
| 符号多一根线 / 十字；质感错成霓虹、激光 | [D4](cards/D4-symbol-errors.md) | casting-and-canon | `prompt_lint.py`（`VP-symbol`） |
| 无对白镜转出文字；低置信误听 | [D5](cards/D5-qc-tools-lie.md) | shot-qc | `transcript_reconcile.py`（`TR-unscripted`、`TR-hallucination`、`TR-lowconf`） |
| "绑定顺序必须从 1 起唯一连续"校验失败 | [E1](cards/E1-slot-order.md) | video-prompting-h3 | `slot_order_check.py`（`SLOT-contiguous`、`SLOT-placeholder-pos`） |
| 改集号后渲染报"素材不存在" | [E2](cards/E2-stale-paths.md) | edit-and-assemble | `asset_exists.py --stale-token`（`E2-stale-path`、`E2-missing-asset`） |
| 中文命令输出被吞；长任务被掐断；技能装了不生效 | [E3](cards/E3-environment-quirks.md) | production-director | `run_all_selftests.py`；装改后重启 |
| 提示词写的与已验收产出不一致 | [E4](cards/E4-prompt-output-mismatch.md) | keyframe-freeze | [目视] 回写提示词 + `contact_sheet.py` |
| 自己验收全绿，人类每次说"不达标"；每个问题都要人类先指出 | [F1](cards/F1-self-verification-loop.md) | screening-review | [目视] 自我放映 + 独立评审；[冷观众]；`asset_exists.py review/` |
| 指标全绿（固定镜头=0、无坏帧、全采用）却被说「无电影级运镜」 | [F2](cards/F2-proxy-metrics.md) | screening-review | 指标登记表（每个数字配观感检查）；grep 报告措辞 |
| 每轮只修最新一条反馈；"仍不够"；修好的维度"又"坏了 | [F3](cards/F3-patch-iteration.md) | screening-review | 全集重跑生成前脚本 `--json` 并与上一轮比对新 error |
| 装了技能、读了规范、写了方法论文档，质量没有质变 | [F4](cards/F4-skills-not-ability.md) | production-director | `run_all_selftests.py`；训练回路学分；A/B 能力证明 |

技能文件路径：`20-craft/<技能名>/SKILL.md`；脚本路径：`50-rubrics/scripts/<脚本名>`，规则代码含义见 [`50-rubrics/scripts/README.md`](../50-rubrics/scripts/README.md)。

## 3. 案例卡格式（[`CONVENTIONS.md`](../CONVENTIONS.md) §5.3，lint 校验）

- 文件：`60-casebook/cards/<ID>-<slug>.md`，文件名固定（CONVENTIONS §7）。
- frontmatter 八个键：`id`、`title`、`group`、`scope`（通用 / 工程细节 / 项目特有）、`severity`（致命 / 严重 / 一般）、`provenance`、`skills`、`drills`。
- 八个章节：症状（含人类原话）→ 现场（轮次、镜、数字、字样）→ 根因（分"直接原因"与"方法论原因"，外部调研补强单列）→ 修正过程 → 可固化判据（每条标 `[自动]` / `[目视]` / `[冷观众]`，可自动的写出脚本名）→「→ 行为改变」→ 适用面与迁移 → 关联。
- 严重度含义：**致命** = 单独出现即阻断 L2（[`50-rubrics/definition-of-done.md`](../50-rubrics/definition-of-done.md) §3）或会让全片方法失效；**严重** = 明显出戏、需返工；**一般** = 工程损耗，不直接伤观感。

## 4. 案例索引（24 张）

| ID | 标题 | 组 | 严重度 | 范围 | 找错题 |
|---|---|---|---|---|---|
| [A1](cards/A1-fragmented-shots.md) | 碎镜症 | A 叙事与节奏 | 致命 | 通用 | DR-01, DR-22 |
| [A2](cards/A2-missing-fights.md) | 打斗缺席 | A 叙事与节奏 | 致命 | 通用 | DR-02, DR-21 |
| [A3](cards/A3-slow-motion-default.md) | 慢镜死板 | A 叙事与节奏 | 严重 | 通用 | DR-03 |
| [A4](cards/A4-unmotivated-camera.md) | 运镜与叙事脱钩 | A 叙事与节奏 | 严重 | 通用 | DR-04, DR-21 |
| [A5](cards/A5-spatial-chaos.md) | 空间调度混乱 | A 叙事与节奏 | 致命 | 通用 | DR-05, DR-20, DR-22 |
| [B1](cards/B1-character-drift.md) | 角色漂移 | B 一致性 | 致命 | 通用 | DR-06 |
| [B2](cards/B2-crowd-leak.md) | 人群穿帮 | B 一致性 | 严重 | 通用 | DR-07 |
| [B3](cards/B3-clone-faces.md) | 克隆脸 | B 一致性 | 致命 | 通用 | DR-06 |
| [B4](cards/B4-duplicate-artifacts.md) | 重复伪影 | B 一致性 | 严重 | 通用 | DR-07 |
| [C1](cards/C1-banned-items-violated.md) | 禁用项被生成器违反 | C 资产工程 | 致命 | 通用 | DR-08 |
| [C2](cards/C2-lenient-acceptance.md) | 验收放水（早期误判） | C 资产工程 | 严重 | 通用 | DR-09 |
| [D1](cards/D1-burned-in-captions.md) | 烧录字幕 | D 生成技术 | 严重 | 通用 | DR-10 |
| [D2](cards/D2-solid-black-fails.md) | 纯黑画面无法生成 | D 生成技术 | 严重 | 通用 | DR-10 |
| [D3](cards/D3-dialogue-capacity.md) | 对白容量物理约束 | D 生成技术 | 致命 | 通用 | DR-11 |
| [D4](cards/D4-symbol-errors.md) | 符号/图形错误 | D 生成技术 | 严重 | 通用 | DR-12 |
| [D5](cards/D5-qc-tools-lie.md) | QC 工具自身会骗你 | D 生成技术 | 严重 | 通用 | DR-13 |
| [E1](cards/E1-slot-order.md) | 槽位顺序连续性 | E 流程工程 | 一般 | 工程细节 | DR-14 |
| [E2](cards/E2-stale-paths.md) | 改集号后路径残留 | E 流程工程 | 一般 | 工程细节 | DR-14 |
| [E3](cards/E3-environment-quirks.md) | 环境怪癖三则 | E 流程工程 | 一般 | 工程细节 | DR-15 |
| [E4](cards/E4-prompt-output-mismatch.md) | 提示词与产出不对齐 | E 流程工程 | 严重 | 通用 | DR-15 |
| [F1](cards/F1-self-verification-loop.md) | 自证循环 | F 质量与学习论 | 致命 | 通用 | DR-16, DR-20 |
| [F2](cards/F2-proxy-metrics.md) | 数字达标 ≠ 观感达标 | F 质量与学习论 | 致命 | 通用 | DR-17, DR-21 |
| [F3](cards/F3-patch-iteration.md) | 补丁式迭代 | F 质量与学习论 | 致命 | 通用 | DR-18, DR-20, DR-22 |
| [F4](cards/F4-skills-not-ability.md) | 学了技能 ≠ 有了能力 | F 质量与学习论 | 致命 | 通用 | DR-19, DR-20 |

> 严重度、范围与找错题以各卡 frontmatter 为准；本表与卡片不一致时，改本表。

**按阶段读卡**（阶段定义见 [`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md)）：
- 开发 / 剧本：A1、A2、D3，以及 F1（钩子与因果是否看得懂只能靠外部视角验证）。
- 预制作（锚点卡、板图、分镜、动作设计）：A1–A5、B1、B3、C1、C2、D3、D4。
- 制作（关键帧、视频提示词、生成、镜头 QC）：A3、A5、B1–B4、C1、D1、D2、D4、D5、E1、E4。
- 后期：D2、E2、E3。
- 审片与迭代：F1、F2、F3；开工前与装载后：F4。

## 5. → 行为改变

- 下次收到任何反馈，先在第 2 节找到对应案例，再按该卡「→ 行为改变」行事；找不到对应行 → 按 [`60-casebook/cards/F3-patch-iteration.md`](cards/F3-patch-iteration.md) 的 7 步协议处理，并在本表补一行。
- 下次开一个生产阶段前，读第 4 节该阶段的卡，把其「可固化判据」中的 `[自动]` 条目排进本阶段闸门。
- 下次交付前，F1–F3 三张卡的判据必须全部有证据；没有就按 [`50-rubrics/definition-of-done.md`](../50-rubrics/definition-of-done.md) 只声明 L0。
