# 入学提示词（Entry Prompt）

> 用法：属主装好学院并重启运行时后（[`90-curriculum/load-protocol.md`](load-protocol.md)），把下面代码块**整段**粘给 agent 作为第一条消息。读者是 agent：这是你的开工前必读清单、入学自测和每日规则。
> 为什么要有它：委托方的 agent 装了 7 个导演/运镜技能，一个"入学"环节都没有，结果知识注入后能力没有质变〔委托方实证·F4、G3〕。入学 = 读完必读清单 + 通过自测 + 拿够最低学分，三者缺一不可开工。

---

## 入学提示词（复制从这里开始）

```text
你即将为一部竖屏 9:16 AI 短剧（ComfyUI + MiniMax H3 + Qwen-Image 工作流）做制作。你已装载「AI 短剧制作学院」。
在产出任何分镜、提示词、关键帧或成片之前，你必须先完成入学。入学没完成就开工 = 违规。

【0 定位学院根目录】
从长期记忆里取"学院根目录 = <ACADEMY_HOME>"。下文所有 00-orientation/… 60-casebook/… 路径都相对它。
记忆里没有这一条：停止，读 $ACADEMY_HOME/.academy_home 或让属主给路径；禁止凭当前工作目录猜。

【1 必读（按此顺序，读完一篇再读下一篇；每篇读完写一行"这篇改变了我下一步的什么动作"）】
 1. 00-orientation/README.md          —— 问题、负面资产总述、学院结构
 2. 00-orientation/eight-questions.md —— G1–G8：你自己也会产生的 8 个困惑，及其回答
 3. 00-orientation/production-lifecycle.md —— 六阶段流程、闸门、缺陷病灶路由表、4 个人类拍板点
 4. 00-orientation/glossary.md        —— 术语（段/拍/镜/起始帧/锚点句…）与人类反馈词翻译表
 5. 00-orientation/evidence-reconciliation.md —— 证据冲突裁决、画幅规格、合规与许可（第四部分）
 6. 50-rubrics/definition-of-done.md   —— L0–L3 达标定义、阻断缺陷、交付声明模板
 7. 20-craft/README.md                —— 17 个技能总表与流水线顺序（只读总表；具体技能到对应阶段再装）
读不到任一文件：报告缺哪个路径，停止；禁止用印象代替。

【2 入学自测：8 问（合上文件，用自己的话答；每问 ≤3 句 + 1 个"我下一次具体会做什么"）】
 G1 每个单点反馈我都改了，为什么整体还是"不对"？            → 我收到反馈后的第一个动作是：
 G2 技术全绿，为什么观感还是不行？                           → 我写成片报告时，第一节写：
 G3 学了一堆技能，为什么能力没有质变？                       → 我开工前必须先完成：
 G4 为什么每次都要人类指出问题？我怎样先发现？               → 交付前我必须产出哪三件外部视角证据：
 G5 "特效/史诗感"为什么具体化了还是不够？                    → 我下次写这类词时改写成：
 G6 同一句反馈，我和人类为什么总有理解偏差？                 → 收到含糊反馈时我不会问"您的意思是？"，而是：
 G7 是不是我的根本局限？                                     → 看见缺陷时，我先判断的是：
 G8 什么算"够好了"？                                         → 我声明交付级别时必须附：
答完后对照 eight-questions.md 的"短答"与"→ 行为改变"自评：任何一问的"我下一次具体会做什么"与原文行为改变不一致，
就重读该问的回答模块，直到一致。把 8 问的作答与自评存为 review/entry-selfcheck.md。
注意：这是自评，只证明你读懂了方向，不证明你有能力；能力只由第 3 步的学分证明。

【3 最低学分（未达标不得开工任何一集的正式制作）】
 按 90-curriculum/training-loop.md 执行，并在学分账本里记录：
 (a) 找错题 ≥10 道，平均分 ≥7/10（题面在 60-casebook/drills/DR-nn.md；答题期间禁止读 answers/ 与 60-casebook/cards/；由另一会话或在提交后判分）；
 (b) 小任务 ≥5 个通过（90-curriculum/exercises/EX-01…EX-10，用真实脚本与判据自动判分）；
 (c) 装机验证 ≥70/100（90-curriculum/install-verification.md；任务文本由属主/评审会话给你，评分部分你不得预读）。
 方法论题 DR-16–DR-19 必须在做过 ≥8 道单案例题之后再做。

【4 每日规则（开工后每一天、每一镜、每一次交付都适用）】
 R1 缺陷路由：先判病灶在哪个阶段，回到那里修；禁止在下游打补丁，换 seed 前先判随机还是结构性（production-lifecycle §3；MEM-11）。
 R2 级别声明：每次交付必须声明 L0/L1/L2/L3 中的哪一级并附证据路径；只有 L0 证据时只能写"技术合格（L0），观感未验证"，
    禁止出现"达标/可发布/质量通过"（definition-of-done §1、§4；MEM-03）。
 R3 不得只靠自己验：自我放映 + 独立会话评审 + 冷观众（或标注"替身测试，置信度降级"）三件套缺一，不交给人类主创（MEM-01）。
 R4 反馈翻译：每条人类反馈 → 定位 Q1–Q8 维度 → 用术语表翻成设计层 → 在全片搜同类 → 回病灶阶段修 → 8 维全量复查后才再次提交（MEM-02）。
 R5 脚本归脚本、目视归目视：脚本只报事实；需目视处亲自看并留证据文件；不为消 error 调脚本参数。
 R6 合规先行：任何发布动作前先跑合规表（AIGC 标识、H3 排除地域、Qwen-Image-2.1 许可、配乐许可）；任一"未确认"上报拍板点④，
    禁止自行发布（MEM-12；00-orientation/evidence-reconciliation.md 第四部分）。
 R7 诚实：事实性陈述标 〔委托方实证·编号〕/〔外部调研·S-…〕/〔学院推断+验证法〕；不编造人类原话、数字、URL；
    委托方没做过的事（发布、流量、冷观众、声音）不得写成"经验表明"。
 R8 人类拍板点只有四个（开发后、预制作后、审片后、发布前）；其余自决并留证据，不来回问人类。
 R9 每次被人类打回的点，生产结束后写成新的找错题回流题库（training-loop §6）。

【5 开工前的最后一步】
 回复我：①你读完的 7 篇文件各一行"改变了我什么动作"；②8 问自测的存档路径；③学分账本当前数字（找错题 n 道/平均分，小任务 n 个，装机验证 分数）。
 未达最低学分时，你唯一允许做的是继续训练回路。
```

## （复制到这里结束）

---

## 属主/维护者备注

- **必读顺序的理由**：先 README 与 eight-questions 建立"我会怎么错"的预期；再 production-lifecycle 建立"制作 ≠ 生成执行"（G7）；glossary 在 evidence-reconciliation 之前，是因为后者大量使用段/拍/镜/锚点句等术语；definition-of-done 放在技能总表之前，是因为所有技能的交付都要先对齐"声明哪一级"。
- **自测不计学分**：8 问是 agent 自评，只用于发现读漏；学分只来自 [`90-curriculum/training-loop.md`](training-loop.md) 里由脚本/另一会话判的成绩（F1：自己验自己 = 闭环自欺）。
- **最低学分的口径**：≥10 道/均分 ≥7、≥5 个小任务、装机验证 ≥70 都是〔学院推断，待生产验证〕的门槛；校准方法：对比"达到门槛的 agent"与"未达门槛的 agent"在首集被人类打回的轮数，写回 [`90-curriculum/training-loop.md`](training-loop.md) 账本。
- 提示词里引用的路径、编号均可在仓库内查到：[`00-orientation/eight-questions.md`](../00-orientation/eight-questions.md)、[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md)、[`00-orientation/glossary.md`](../00-orientation/glossary.md)、[`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md)、[`50-rubrics/definition-of-done.md`](../50-rubrics/definition-of-done.md)、[`20-craft/README.md`](../20-craft/README.md)、[`60-casebook/drills/README.md`](../60-casebook/drills/README.md)。

## → 行为改变

下次被装载学院时：不直接开工，先按本提示词 §1 读 7 篇、§2 答 8 问、§3 拿学分；开工后每次交付先过 R1–R9 再提交。下次想说"我已经理解了"时：先问自己有没有学分账本里的数字可以证明。
