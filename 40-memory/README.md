# 长期记忆：写入方法与分级（40-memory）

> 读者：要把学院装进自己长期记忆（CLAUDE.md / AGENTS.md / 运行时 memory）的 agent。条目在 [`40-memory/core-memory.md`](core-memory.md)，共 MEM-01–MEM-60。
> 一句话：**记忆只装"会改变下一步动作"的判决**；细节、证据、例子留在学院文件里按需查。

## 1. 分级装载

| 级别 | 内容 | 何时装 | 怎么用 |
|---|---|---|---|
| T1 · Top-12 | MEM-01–MEM-12 | 每个会话开工时，逐字写入常驻记忆 | 任何阶段都先遵守；与项目习惯冲突时以 T1 为准 |
| T2 · 分域 | MEM-13–MEM-60（按 `##` 域分组） | 进入对应阶段/技能时装该域 | 剧本域 → `script-doctor`、`multi-episode-arc`；分镜/空间/节奏 → `storyboard-long-take`、`action-choreography`；资产/关键帧 → `casting-and-canon`、`asset-boards`、`keyframe-freeze`；H3 → `video-prompting-h3`；声音 → `sound-design`；验收 → `shot-qc`；交付/回流 → `screening-review`、`cold-audience-test`；合规 → `publish-prep` |
| T3 · 不进记忆 | 案例卡、判据、脚本参数、对标数据 | 用时查 | 记忆里只写路径或编号（如 `R-CUT-16`），禁止把整张清单抄进记忆 |

## 2. 写入格式（🔒 lint 校验）

一行一条，必须匹配：`^- \[MEM-(\d{2,3})\]\[[^\]]+\] .+（为什么：.+）〔溯源：[^〕]+〕$`

- `[域]` 用 2–4 字中文（空间、对白、合规…）；规则句用"必须/禁止/若…则…"，写到能直接执行的粒度（数字、脚本名、英文原句）。
- `（为什么：…）` 写**事件**（哪一轮、什么症状、人类原话逐字），不写道理。
- `〔溯源：…〕` 至少一个合法编号（案例 / P / M / T / GAP / S- / F-）；只写学院立场 R1–R7 不算溯源，必须同时带其证据编号。

## 3. 诚实纪律（最常犯的错）

1. **禁止把外部调研存成委托方经验。** 来自 `80-sources` 的事实在"为什么"里写〔外部调研·S-…〕，规则里不得出现"实测/经验表明/我们发现"。
2. 〔学院推断〕必须同时写"如何验证"（例：MEM-39 的正圆测试图、MEM-41 的同 seed A/B）。验证完成后把结论回写 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md)，再改记忆条目的标注。
3. 人类原话只能逐字引用 [`00-orientation/client-dossier.md`](../00-orientation/client-dossier.md) 中「」内的句子，不改一个字。

## 4. 更新政策

| 情况 | 动作 |
|---|---|
| 生产中被人类打回、且病灶已定位并修复验证 | 新增一条（新编号，不复用旧号）：规则 + 本次事件 + 案例/缺陷单编号 |
| evidence-reconciliation 立场变化 | 同一次提交里改受影响条目；记忆与立场冲突时以 evidence-reconciliation 为准 |
| 条目被证伪 | 不删除：改写规则并在"为什么"里写"已于 <日期> 被 <证据> 推翻"，避免旧版本在别处复活 |
| 一次性项目事实（seed、具体镜号、某集角色名） | 不进 core-memory，写入该项目自己的 memory 文件或锚点卡 |
| T1 要换条目 | 必须说明新条目比被替换者更常改变动作；T1 恒为 12 条 |

改完运行 `python3 tools/academy_lint.py --paths 40-memory/core-memory.md`：格式、重复编号、溯源编号合法性必须 0 error。

## 5. → 行为改变

下次开工时，先把 Top-12 逐字装入常驻记忆，再按当前阶段装对应域；下次想写"经验表明"时，先查来源是不是委托方档案编号——不是就改写成〔外部调研〕或〔学院推断〕并附验证方法。
