# 成片报告 · S<nn>E<nn>

<!-- 产出路径：season-01/epNN/final-report.md。技能：production-director（总产物）、screening-review（填交付声明）、edit-and-assemble（技术段）。
     依据：50-rubrics/definition-of-done.md（L0–L3 唯一依据）、50-rubrics/quality-model.md（Q1–Q8）。
     硬规则（R-CUT-16）：第一节必须是交付声明；缺证据的级别写"未验证"，不省略；只有 L0 证据时，全文禁止出现 R-CUT-16 列出的三个结论词，只能写"技术合格（L0），观感未验证"。本模板为此不写各级中文名，填写时也不要补。 -->

## 1. 交付声明 · S<nn>E<nn>
- 达到级别: <L0 / L1 / L2 / L3>；<下一级> 未达成，原因: <维度 = 分数（段号 + 时间码 + 现象）>，修复: <已排期 / 缺陷单编号>
- L0 证据: review/l0-report.json（<n>/<n> 自动条目通过）
- L1 证据: review/self-screening.md（第一次困惑点: <时间码 / 无>）；review/cold-audience/（<n> 人，<k>/<n> 复述正确；<人类 / 替身测试，置信度降级>）
- 8 维评分: Q1=<> Q2=<> Q3=<> Q4=<> Q5=<> Q6=<> Q7=<> Q8=<>（见 review/quality-scorecard.md）
- 阻断缺陷: <0 / 列出缺陷单编号>
- 独立评审: review/independent-review.md（<n> 条阻断：<已修复并复评 / 未修复>）
- 合规（L2 起必填）: publish-kit.md 合规表 <全部已确认 / n 项未确认 → 待人类拍板④>
- 对标对照（L3 才填）: review/benchmark-compare.md <或 未验证>
- 未验证项: <发布后数据（未发布）/ 冷观众（未测）/ ……>

## 2. 技术（L0）
| 项 | 结果 | 证据 |
|---|---|---|
| 时长 | <s，季规格 <90–110>s> | loudness_verify 报告 |
| 分辨率 / 画幅 | <1080×1920> | 同上 |
| 响度 / 真峰 | <-16.0 LUFS / -1.2 dBTP> | 同上 |
| 坏帧 / 黑场 / 冻结 | <无 / 设计静场 n 处（时间码）> | 同上 + psnr_scan |
| 素材存在 / 旧路径残留 | <0 / 0> | asset_exists 报告 |
| 字幕逐字对账 | <0 缺句> | transcript_reconcile 报告 |

## 3. 本轮改动与回流
| 缺陷单 | Q 维度 | 病灶阶段 | 修法 | 复验 |
|---|---|---|---|---|
| DEF-<nn> | Q<n> | <剧本/分镜/板图/关键帧/提示词/剪辑/声音> | <一句话> | <证据路径> |

## 4. 请人类拍板
- 拍板点③（审片包）: <审片包路径；请重点看的时间码>
- 风险与未决: <……>
