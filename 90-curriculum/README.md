# 90-curriculum · 课程层：装载、入学、训练、验收

> 这一层把前面九层的"知识"接成**能力**：能力 = 知识 × 实践反馈 × 标准内化〔委托方实证·F4、G3〕。委托方的 agent 只有第一项（装了 7 个技能），所以质量没有质变。本层补第二、三项：**装载协议 → 入学 → 训练回路（找错题/小任务/判分/复盘）→ 装机验证 → 冷观众验证**。
> 读者是 agent（以及替 agent 装载的属主）。每个文件都以"→ 行为改变"收尾。

## 1. 文件索引

| 文件 | 谁读 | 何时读 | 作用 |
|---|---|---|---|
| [`90-curriculum/load-protocol.md`](load-protocol.md) | 属主 | 装载时 | 7 步安装指令：固定 ACADEMY_HOME → 链接技能 → Top-12 + 根目录写入记忆 → 验收接线 → 风格卡接 visual-bible → **重启运行时（E3-3）** → 入学；四个人类拍板点；H3 排除地域与 Qwen-Image-2.1 研究许可提醒 |
| [`90-curriculum/install/install.sh`](install/install.sh) | 属主 / 受权 agent | 装载与升级时 | 幂等脚本：`--target-skills-dir DIR`（默认 `~/.claude/skills`）、`--dry-run`；链接 17 个技能、写 `.academy_home`、打印 Top-12 记忆行、提示重启；无网络 |
| [`90-curriculum/entry-prompt.md`](entry-prompt.md) | agent | 重启后的第一条消息 | 入学提示词：7 篇必读的顺序、8 问自测、最低学分、每日规则 R1–R9 |
| [`90-curriculum/training-loop.md`](training-loop.md) | agent | 入学后、开工前，以及每次生产后 | 训练回路：找错题 → 小任务 → 真实脚本判分 → 对照答案复盘 → 新反馈变新题；新题模板；学分账本模板 |
| [`90-curriculum/exercises/`](exercises/)（`EX-01` … `EX-10`） | agent | 训练回路 §4 | 10 个小任务：自带素材、判分命令与通过线 |
| [`90-curriculum/install-verification.md`](install-verification.md) | 运行者 / 评审（受测 agent 只读其 §2） | 装载后、训练后 | 15 秒 BOSS 战验收任务：40 分自动 + 60 分评审，≥70 通过；对照组（无学院）同题同模型；结果记录模板 |
| [`90-curriculum/cold-audience-protocol.md`](cold-audience-protocol.md) | agent（主持人角色） | 每集审片阶段 | 冷观众测试：招募、设置、复述因果链、断点、下一集意愿、阈值、替身降级、断点 → 缺陷单 |

## 2. 学分路径

```
装载 (load-protocol)
  └─► 重启运行时 ─► 入学 (entry-prompt：7 篇必读 + 8 问自测)
        └─► 训练回路 (training-loop)
              ├─ 找错题 ≥10 道，首次作答均分 ≥7/10          ┐
              ├─ 小任务 ≥5 个通过（EX-01…EX-10）            ├─ 最低学分：学分账本 A–D 节有数字
              └─ 装机验证 ≥70/100（install-verification）   ┘
                    └─► 开工许可
                          ├─ 开发/预制作：script-doctor、storyboard-long-take、action-choreography、visual-bible …
                          ├─ 制作：keyframe-freeze、video-prompting-h3、shot-qc
                          ├─ 后期/审片：edit-and-assemble、screening-review、cold-audience-test（冷观众协议）
                          └─ 发布：publish-prep（合规先行，拍板点④）
```

- **未达最低学分，agent 唯一允许的动作是继续训练回路**（entry-prompt §3）。门槛数值是〔学院推断，待生产验证〕；校准数据记在学分账本 F 节。
- 技能总表与阶段顺序：[`20-craft/README.md`](../20-craft/README.md)；阶段闸门与人类拍板点：[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md)。
- 每次生产后，把被人类打回的点写成新找错题回流（训练回路 §6）——学分路径不是一次性的，它是**每集都跑**的回路。

## 3. 本层如何回答 G3、G4、G8

| 困惑 | 本层的回答 |
|---|---|
| G3 学了技能为什么没质变 | 学分路径 + 训练回路：没有"做 → 被判分 → 对照答案 → 改"，技能只是知识注入 |
| G4 为什么总要人类指出问题 | 冷观众协议 + 装机验证里的"评审盲评"：引入不共享你上下文的观察者；新反馈变新题 |
| G8 什么算够好 | 冷观众阈值是 L1/L3 的证据来源（[`50-rubrics/definition-of-done.md`](../50-rubrics/definition-of-done.md)）；装机验证是"设计与提示词层面"的证据，二者都不等于发布后的观众数据 |

## 4. 诚实声明

- 最低学分门槛、装机验证的 70 分线与扣分权重、冷观众的 2/3 阈值与 3 秒同标窗口，全部是〔学院推断，待生产验证〕，各文件都写明了校准方法。
- 冷观众测试方法来自〔外部调研〕（[`80-sources/catalog/ai-film-cases-audience-testing.md`](../80-sources/catalog/ai-film-cases-audience-testing.md)）；委托方从未做过（GAP-2）。
- 装机验证只证明装载后的设计/提示词行为，不证明成片观感；对照组分数必须与实验组一起报告。

## → 行为改变

下次装载学院时：先读本页的学分路径，确认自己处于哪一格；下次想跳过训练回路直接开工时：先检查学分账本里有没有数字——没有，就回到第 2 节的第一格。
