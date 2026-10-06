---
id: E1
title: 槽位顺序连续性
group: E 流程工程
scope: 工程细节
severity: 一般
provenance: 委托方实证
skills: [video-prompting-h3, production-director]
drills: [DR-14]
---
# E1 · 槽位顺序连续性

> 一句话：**会被删掉的槽位放在末尾。** 编号从 1 起连续是绑定校验的硬约束，所以"临时占位"不能占住 1 号位，否则删掉它的那一刻，整批镜头一起失效。

## 症状（含人类主创原话，逐字引用档案）

- 绑定校验"绑定顺序必须从 1 起唯一连续"失败，踩坑两次：一次 18 镜集体失败，一次 16 镜集体失败〔委托方实证·E1〕。
- 档案没有保留人类主创关于本案的「」逐字原话。本案没有被人类看到，在流程内部就被校验拦下了。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 预制作阶段的模板：起始帧还没生成，于是用占位符"起始帧槽"排在顺序 1，其余参考槽从 2 起〔委托方实证·E1〕。
- 进入生产期后删掉占位槽，剩下的槽从 2 起，不再连续，校验失败〔委托方实证·E1〕。
- 两次都是**批量**失败（18 镜、16 镜）。说明错误在模板层，所有沿用这个模板的镜一起出错。
- 管线约束：起始帧 `REF-SHOTnnn-START` 以顺序 1 送 `first_frame`〔委托方实证·T-3〕；提示词里的 `<Picture N>` 编号必须和引用顺序一致〔委托方实证·T-2〕。

## 根因（分条；区分"直接原因"与"方法论原因"）

1. **直接原因**：把"生命周期最短"的槽放在了"最不能动"的位置。删掉 1 号位，后面所有编号都失去连续性。
2. **直接原因**：删槽时只改了 `references`，没有连带重排 `<Picture N>`。即使补上编号，提示词里的引用也会指向别的图〔学院推断〕。
3. **方法论原因**：模板没在"删掉占位之后"的状态下校验过。校验只覆盖当前状态，没有模拟下一步操作后的状态。
4. **方法论原因**：批量操作之前没有先拿单镜试跑。模板错误被复制到了整集。
5. **外部佐证**：zenstory 的跨文档校验器也要求参考顺序从 1 连续，并且"仍有待补参考图时，禁止出最终视频提示词"〔外部调研·S-ZEN-14〕。它的 prepare 阶段会机械核对参考槽位，任何漂移都 fail closed〔外部调研·S-ZEN-10〕。

## 修正过程（做了什么、第几轮、结果）

- 委托方：把占位帧槽**放到末位**，其余参考占 1..N-1，占位占 N。生产期删掉占位后，编号天然连续。之后升格时，再把起始帧提回顺序 1〔委托方实证·E1〕。
- 学院补充：提回顺序 1 时，所有参考的编号都要 +1，提示词里的每个 `<Picture N>` 也要同步改写。`slot_order_check.py` 报 `SLOT-placeholder-pos` 时会给出重排方案和 `<Picture N>` 改写表，照抄即可。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] 改了 `references`、导出了 ComfyUI 绑定列表之后，prepare 之前跑：
  `slot_order_check.py video-prompts.md --simulate-remove-placeholder --assets-dir <ep>/assets`
  以下规则码必须为 0：`SLOT-contiguous`、`SLOT-unique`、`SLOT-placeholder-pos`、`SLOT-sim`〔E1〕。
- [自动] 有绑定 JSON 时加 `--bindings exports/bindings.json`，`SLOT-bind-mismatch` 必须为 0。顺序不一致时，`<Picture N>` 会指错图〔E1、T-2〕。
- [自动] `slot_order_check.py` 不报 `SLOT-placeholder-ref`：提示词里不得有 `<Picture N>` 指向占位槽〔E1〕。
- [自动] `prompt_lint.py` 不报 `VP-picture`：`<Picture N>` 都已定义，首次引用顺序是升序〔T-2、E1〕。
- [自动] `SLOT-first-frame` 为 0：`first_frame` 是本镜自己的 `REF-SHOT<同号>-START`〔T-3、P4〕。

## → 行为改变（下次……）

- 下次建任何带占位的模板，占位一律放在末位；建好后先跑 `--simulate-remove-placeholder`，再复制到整集。
- 下次做批量操作（改模板、改 references、重导绑定），先拿 1 镜试跑，通过校验后再扩到整集。
- 下次移动任何槽位，同一次提交里改写全部 `<Picture N>`。**禁止**只改 `references`。
- 下次还有参考图没出来时，不出最终视频提示词，也不进 prepare。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ☆ "从 1 起连续"是委托方 ComfyUI 绑定节点的校验规则，换节点或换 API 要重查。托管 API 的上限也不同，例如参考图最多 9 张〔外部调研·F-ZEN-01〕。
- ★ "会删的东西放末尾"和"校验删除之后的状态"适用于一切有序编号：剪辑单 CUT 号、镜号、字幕序号。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（references 与 `<Picture N>`）、[`20-craft/production-director/SKILL.md`](../../20-craft/production-director/SKILL.md)（prepare 前校验、批量前单镜试跑）。
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)。
- 判据清单：[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)。
- 脚本：[`50-rubrics/scripts/slot_order_check.py`](../../50-rubrics/scripts/slot_order_check.py)、[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)。
- 契约：[`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §2 规则 2。
- 找错题：[`60-casebook/drills/DR-14.md`](../../60-casebook/drills/DR-14.md)（槽位 / 路径）。
- 相邻案例：[`60-casebook/cards/E2-stale-paths.md`](E2-stale-paths.md)、[`60-casebook/positive-assets.md`](../positive-assets.md)（P5、P6）。
