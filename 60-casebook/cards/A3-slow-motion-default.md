---
id: A3
title: 慢镜死板
group: A 叙事与节奏
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [action-choreography, video-prompting-h3, edit-and-assemble, sound-design]
drills: [DR-03]
---
# A3 · 慢镜死板

> 一句话：**慢 = 段内事件密度不足。** 生成器把"时长"读成"事件速度"：给一个动作 5 秒，它就用 5 秒做完这个动作。写 `Real-time speed` 是必要条件，不是充分条件——还要把时间填满事件与后果。"慢"只能是设计选择，不能是默认。

## 症状（含人类主创原话，逐字引用档案）

- 人类主创原话：「全是几个简单动作的慢镜头」〔委托方实证·A2、A3〕。
- 观感：全片没有速度层次——冲刺、对峙、爆发、余波都是同一种匀速偏慢的流动〔委托方实证·A3〕；动作没有重量。
- 对应质量维度：Q6 节奏与速度（[`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) 交付声明样例："Q6 = 1（全段无速度层次）"）。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 与 A2 同一批反馈，指向前三集的打斗段〔委托方实证·A2、A3〕。
- 当时提示词**没有写**实时速度约束〔委托方实证·A3〕；也没有任何节拍设计（快-慢-爆-静）〔委托方实证·A3〕。
- 结构背景：H3 单次生成下限 124 帧（5.17s），A1 的修正方向是 8–15s 长段〔委托方实证·T-2、A1〕；A2 的"动作瞬间 + 反应镜头"策略让每镜只装"几个简单动作"〔委托方实证·A2〕。档案未记录 A3 反馈与 A1 修正的先后顺序。
- 生成参数：cfg=1.0〔委托方实证·T-2〕——没有引导强度可调，速度只能靠提示词与设计控制。

## 根因（分条；区分"直接原因"与"方法论原因"）

**直接原因**
1. **未写实时速度约束**〔委托方实证·A3〕。
2. **时长被读成事件速度**："Duration is read literally as event speed"——给摔倒 1.5s 就是月球重力；真实摔倒 ≈0.4–0.6s，其余时间给后果；"Weight comes from the stop, not the drop"〔外部调研·S-H3-11〕。一镜 ≥5.17s 却只装一两个简单动作，模型就把动作拉满全镜 → 慢镜。
3. **生成器的默认偏差是慢**：慢动作帧间变化小、更容易保持时序一致；提示对速度含糊时"It will almost always choose slower, because slower is safer"〔外部调研·S-VGEN-19〕；Seedance 官方甚至建议"优先慢、轻、连续的小动作"〔外部调研·S-VGEN-11〕。开源用户可降 cfg 对抗，本管线 cfg 已是 1.0〔委托方实证·T-2〕，只剩提示词这条路。
4. **动词不带速度、背景不动**：`walks`/`moves` 这类中性动词 + 无环境运动，会出现"慢速奔跑者配静止背景"〔外部调研·S-VGEN-19〕。
5. **想用"秒数"控节奏**：H3 不能精确安排事件时刻（要求 3.0s/4.0s 揭示，两次都落在 2.46s），"State the sequence, never the timing"〔外部调研·S-H3-08〕。在提示词里写"在 3 秒内慢慢倒下"既控不住时刻，又把"慢慢"登记成内容。

**方法论原因**
6. **没有节拍设计**：速度层次（冲刺快 → 对峙慢 → 爆发 → 余波静）是剧本/分镜阶段的设计，不是生成参数〔委托方实证·A3；GAP-6 节奏工程薄弱〕。
7. **修 A1 时只改了时长，没改事件密度**〔学院推断〕：把 3s 碎镜拉成 ≥5.17s 长镜，但镜内仍是"一个动作"，碎镜症就变成了慢镜症——典型的补丁式迭代（F3）。验证法：对同一起始帧、158 帧，A 写单个出招，B 写"三招 + 一桥 + 后果"，各 3 seed，用 `contact_sheet.py` 数"预备 → 接触"占用的帧数，A 显著更长则成立。
8. **"慢"被当成安全选项**：为规避崩坏而偏好小动作（同 A2 的防御性策略），慢成了默认而不是设计〔委托方实证·A2、A3〕。

## 修正过程（做了什么、第几轮、结果）

1. 委托方提出的修正：提示词明写 `Real-time speed throughout, no slow motion`；节拍设计（冲刺快切 → 对峙慢推 → 爆发一击 → 余波静场）；音乐节拍对齐切点〔委托方实证·A3〕。前者已写入禁令包 M8。
2. 结果：档案**未记录**修正后是否被人类主创认可；音乐节拍 ↔ 剪辑点仍是缺口（GAP-6）。A3 **未闭环**。
3. 学院补强（〔学院推断〕，验证法见判据）：
   - **按真实事件时长分配节拍**（外部参考表〔外部调研·S-H3-11〕）：眨眼/小笑 0.3–0.5s；摔倒/撞击 0.4–0.6s；转头 0.5–0.8s；抬手 0.8–1.2s；一步 ≈0.5s；可读运镜 1.5–2.5s。一镜的事件预算 = Σ事件时长 + 后果/反应/静场；预算填不满就加事件或缩镜长，**不许**让一个动作独占全镜。
   - **只写顺序，不写秒数**：用"三招 → 桥 → 后果 → 静止对视"排序，精确时机在剪辑里定〔外部调研·S-H3-08〕。
   - **用自带速度的动词 + 环境运动**：`strides / darts / lunges / charges / snaps`、`in rapid succession`，同时写尘土被刀风扫起、碎石弹开等环境响应〔外部调研·S-VGEN-19〕。
   - **停-爆-停**：静止对峙 → 一串爆发 → 定格反应〔外部调研·S-STORY-18〕；"静"是让"快"被看见的对比，不是拖。
   - **后期变速有上限**：超过约 106% 观众就看得出人工变速，且要缓入缓出；打斗剪辑节奏逐步提速，而不是一刀突然变快〔外部调研·S-STORY-21〕。
   - **真要慢镜**：只能在元数据写 `- 慢动作: 设计选择（理由…）`，且该段必须有快段作对比；同时**删掉**实时速度句，避免指令打架（A5④）。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [自动] 动作镜（拍数 ≥2 或含 strike/slash/punch/kick/leap/charge/dodge/attack/block/swing/fight/lunge/stab）含 `Real-time speed throughout, no slow motion`；非否定的 slow motion / slowmo / bullet time / time slows / half speed 不得出现——`prompt_lint.py` 的 VP-realtime 0 error；唯一豁免是元数据 `- 慢动作: 设计选择（理由…）`。〔A3、M8〕→ video-prompt 清单
2. [自动] 声明了 `慢动作` 却仍写实时速度句 → `prompt_lint.py` VP-realtime warn，必须二选一。〔A3、A5④〕→ video-prompt 清单
3. [自动]+[目视] 动作镜跑 `psnr_scan.py <clip>`：P8-psnr-stats 的相邻帧 PSNR 中位若落在 30–40 dB（"呼吸级"运动），疑似慢镜/没动起来 → 用 `contact_sheet.py` 出接触表目视确认。〔A3；外部调研·S-H3-09 的 PSNR 分档；学院推断：阈值需在委托方素材上用已知"好/慢"各 3 镜校准〕→ video 清单
4. [目视] 视频提示词与动作设计中，每镜的动作链按真实事件时长排布，剩余时间写给后果/反应/静场；不存在"一个单动作占满整次生成"的镜。证据：动作设计里的事件预算表。〔A3；外部调研·S-H3-11〕→ storyboard 清单
5. [目视] 每个动作段在分镜中标出速度层次（快 / 慢 / 爆 / 静 中至少两种），且"慢"处写明设计理由。〔A3〕→ storyboard 清单
6. [目视] 动作镜提示词用自带速度的动词并写环境运动；提示词中无"slowly / gracefully / over N seconds"之类给动作降速或定秒数的写法（设计慢镜除外）。〔A3；外部调研·S-VGEN-19、S-H3-08〕→ video-prompt 清单
7. [目视] 剪辑单中任何变速 ≤106% 且缓入缓出；打斗段刀速逐步提升。〔A3；外部调研·S-STORY-21〕→ final-cut 清单
8. [冷观众] 冷观众标记"拖 / 慢 / 走神"的时间点；≥2 人标在同一段 → 回分镜补事件密度，不在剪辑里硬加速。〔A3、F1〕→ final-cut 清单

## → 行为改变（下次……）

- 下次写任何动作镜，**先**做事件预算：列出动作链每一节的真实时长，加上后果与静场，再对照镜长；预算 < 镜长的 60%〔学院推断，待校准〕就加事件或缩镜，**禁止**指望模型"自然填满"。
- 下次写动作提示词，**必须**同时写三样：实时速度句、带速度的动词、环境运动；**禁止**写"在 N 秒内"之类的秒数控速。
- 下次想要"有分量"，**改为**写"停"（撞击后定住、碎石落地、喘息对视），**禁止**把撞击本身拉慢。
- 下次想用慢镜，**先**在元数据写 `- 慢动作: 设计选择（理由…）` 并删实时速度句，**再**在同段安排一个快段作对比；没有对比的慢镜一律视为默认慢。
- 下次修 A1（拉长镜）时，**同步**提高事件密度；拉长镜长而不加事件 = 制造 A3。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ "时长读成事件速度""默认偏慢"是扩散视频模型的共性〔外部调研·S-VGEN-19〕，换模型仍成立；文戏同理：台词远短于镜长时，模型会用填充与重复补时间〔外部调研·S-H3-09〕。
- ★ 速度层次、停-爆-停适用于一切动作与追逐题材；文戏的"速度"体现为对白节奏与反应停顿。
- ☆ 可调 cfg/STG 的开源模型还能靠降引导强度提速〔外部调研·S-VGEN-19〕；本管线 cfg=1.0，此路不通。
- ☆ PSNR 30–40 dB 分档来自外部单项目（S-H3-09），换分辨率/画风须重新校准。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/action-choreography/SKILL.md`](../../20-craft/action-choreography/SKILL.md)（事件预算、停-爆-停）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（实时速度句、速度动词、慢动作元数据）、[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)（变速上限、刀速递进）、[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)（音乐/冲击声与剪辑点对齐，GAP-6）。
- 理论：[`10-theory/04-action-design.md`](../../10-theory/04-action-design.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)。
- 判据清单：[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/sound-color-performance.md`](../../50-rubrics/checklists/sound-color-performance.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-03.md`](../../60-casebook/drills/DR-03.md)（慢镜）。
- 相邻案例：[`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)（同一反馈的另一半）、[`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)（拉长镜的副作用）、[`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)。
