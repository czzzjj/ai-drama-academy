---
name: performance-direction
description: 把剧本里的情绪翻译成 H3 能生成、观众能读懂的可拍表演——任务动词、表情变化链（眉→眼→嘴）、每镜≤2–3 个表情拍、呼吸眨眼式静止、非说话人闭嘴句、反应镜公式与库里肖夫兜底，并在出片后用 PSNR 与裁剪证据验收表演是否落地。Use when writing performance notes for a shot, a close-up or reaction shot looks stiff/frozen, lip-sync lands on the wrong person, or feedback says faces are dead. 触发词：表演、表情、微表情、反应镜、眼神、视线、口型串人、脸僵、面无表情、没有灵魂、performance, acting, facial expression, reaction shot, eyeline, lip sync, stiff face, blank stare。不负责镜头运镜与空间调度（storyboard-long-take）、打击拍动作链（action-choreography）、角色外观锚点（casting-and-canon）、台词容量（script-doctor）。
---
# 表演指导（performance-direction）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。本技能的大部分依据是〔外部调研〕——委托方从未系统做过表演设计（GAP-5），落地前每条都按"如何验证"一栏小样验证。

## 何时用 / 何时不用

- **用**：分镜定稿后、冻结关键帧与写视频提示词之前，为每个"有表演"的镜写表演卡；出片后表情镜验收；人类说"脸僵 / 没表情 / 假"时。
- **用**：多人对白镜（≥2 主体 + 对白）——必须用，口型串人是高频缺陷〔外部调研·S-ZEN-17〕。
- **不用**：纯空镜、纯动作打击段（打击拍密度由 action-choreography 决定，R4：打击拍不受表情拍上限约束）。
- **不用**：要改的是"角色站哪、镜头怎么动"——那是 storyboard-long-take；表演不能修空间问题。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| `episode-script.md`（场景目标、台词） | 表演卡：每镜一节，写在 `storyboard.md` 该镜下方 | [`70-playbooks/templates/storyboard.md`](../../70-playbooks/templates/storyboard.md) |
| `storyboard.md`（起始帧方位、拍数） | 冻结提示词中的"表情起点"句 | [`70-playbooks/templates/keyframe-prompt.md`](../../70-playbooks/templates/keyframe-prompt.md) |
| `anchors.md`（角色外观、音色） | `video-prompts.md` 中 `detailed_description` 的表演段 + 闭嘴句 | [`70-playbooks/templates/video-prompt-h3.md`](../../70-playbooks/templates/video-prompt-h3.md) |
| 出片 `SHOT-nnn.mp4` | `qc/SHOT-nnn.md` 的表演行（PSNR 中位、口型裁剪） | [`70-playbooks/templates/qc-record.md`](../../70-playbooks/templates/qc-record.md) |

表演卡最少字段：`任务动词 | 视线目标 | 表情链(从A到B…镜末收束) | 不准动的部位 | 形体动作 | 非说话人处理 | 兜底方案`。

## 步骤

1. **定任务动词**：每个有表演的镜先写一个及物动词（说服、逼问、试探、隐瞒、求饶、挑衅），禁止只写 sad / angry / 悲伤 当表演。由动词推身体动作。验：R-PRF-01；`grep -nE 'sad|angry|happy|悲伤|愤怒' video-prompts.md` 命中且无对应动作句 → 改。〔外部调研·S-CRAFT-18、S-CRAFT-19〕
2. **情绪 → 可拍动作翻译**：内心状态（"心中一震""神色一凛"）一律改成当前景别看得见的部位变化。速查：
   - 震惊 → 眉上抬、眼睁大、呼吸停一拍、下颌微落；
   - 压抑愤怒 → 下颌咬紧、鼻翼张、眼不眨、手指收拢；
   - 恐惧 → 视线快速扫视出口、肩上提、后撤半步、吞咽；
   - 隐瞒 → 视线下移再回来、嘴角压平、手藏到身后或摸物件；
   - 释然 → 长呼气、肩落、眼先软、嘴角最后动。
   景别不支持的部位不写（全景不写睫毛）。验：R-PRF-07（每个情绪转折至少一个形体动作）。
3. **写成变化，不写成状态**：每个表情拍写"从 A 到 B"，按生理顺序 **眉 → 眼 → 嘴**（真笑先到眼睛），并写镜末收束状态 `settling into a held stillness by the end`。同时写"不准动的部位"（例：`her mouth stays flat, no smile`）防模型自动补笑。验：R-PRF-02、R-PRF-03。〔外部调研·S-H3-09〕
4. **数表情拍**：每镜表情拍 ≤2–3 个（R4），打击拍另计。超了 → 拆成同次生成里的多个 `[Shot]` 或拆成多次生成，或在剪辑里用插入镜。表情拍计入 `storyboard.md` 的 `拍数` 列。验：R-PRF-04；`python3 50-rubrics/scripts/segment_rhythm.py storyboard.md`（`A5-beats-many`）。
5. **写视线**：每个表演镜写视线目标（看谁、看哪；直视 / 回避 / 扫视）。多人镜视线方向必须与 `起始帧方位` 一致（LEFT 的人看向画面右）；要看的东西不在画面里时写明它在画外哪一侧，否则人物会看镜头〔外部调研·S-H3-09〕。验：R-PRF-06；`python3 50-rubrics/scripts/direction_audit.py video-prompts.md --storyboard storyboard.md`。
6. **静止 ≠ 冻结**：静着的人写 `standing in place, breathing softly, blinking and shifting weight a little as people naturally do`；禁止 `completely still`、`holds one pose completely rigid`〔外部调研·S-H3-08〕。
7. **非说话人闭嘴**：画面 ≥2 主体且有对白 → 非说话人写 `[S2] does not speak; his lips remain completely closed.`，或安排背身 / 出画；说话人用稳定说话人 ID 引出 `<d>[Chinese] …</d>`。验：R-PRF-05；`python3 50-rubrics/scripts/prompt_lint.py video-prompts.md --anchors anchors.md --storyboard storyboard.md`（`VP-lipsync`）。〔外部调研·S-ZEN-17：不写 3 次 2 次落错人，加句后 3/3〕
8. **反应镜公式**：先点名情绪 → 写两处当前景别可见的泄露 → "在约 1.5 秒内落下，然后定住"。例：`A flicker of fear: her eyes widen and her breath catches; within about 1.5 seconds it settles, and she holds still.` 〔外部调研·S-ZEN-17 同源 zenstory 小样，学院推断：样本小，用 3 seed A/B 验证〕
9. **微表情特写只用固定机位**：`static, on a tripod, with no camera movement whatsoever`；不叠运镜，不在表情特写里同时写身体大位移。验：R-PRF-09。
10. **兜底（库里肖夫）**：表情写不出来、两次重出仍僵 → 改为中性脸 + 上下文镜（他看见了什么），让剪辑承担情绪；反应慢半拍用插入镜盖住。在表演卡 `兜底方案` 栏预先写好用哪颗上下文镜。〔外部调研·S-STORY-12〕
11. **出片验收**：表情镜跑 `python3 50-rubrics/scripts/psnr_scan.py SHOT-nnn.mp4 --json > qc/SHOT-nnn/SHOT-nnn.psnr.json`，中位 PSNR ≥37 dB = 脸基本没动 → 拆镜或减拍重出（R-PRF-08）；多人镜跑 `python3 50-rubrics/scripts/contact_sheet.py SHOT-nnn.mp4 --keyframe REF-SHOTnnn-START.png --out-dir qc/SHOT-nnn --crop face=x:y:w:h`，逐格看非说话人嘴部（R-VID-13）。结论写进 `qc/SHOT-nnn.md`。
12. **外部读表演**：关键表演镜交给 screening-review / cold-audience-test，问"这个角色此刻想要什么"，答案与任务动词一致才算落地（R-PRF-10）。

## 判据

- 设计阶段：R-PRF-01、R-PRF-02、R-PRF-03、R-PRF-04、R-PRF-05、R-PRF-06、R-PRF-07、R-PRF-09。
- 出片阶段：R-PRF-08（PSNR 中位 <37 dB）、R-VID-13（非说话人闭嘴）、R-VID-04（≥2 人无克隆脸——表演再好，两张同脸也作废）。
- 外部视角：R-PRF-10（冷观众 / 独立评审能说出角色想要什么）。
- 质量维度：主 **Q1 叙事与钩子**（观众读不出动机 = 因果链断）、**Q8 声音与对白**（口型错人、赶词）、**Q7 一致性与连续性**（表情把脸拉变形 = 身份漂移）。
- 优先级：表演是观众最先骂 AI 剧的地方〔外部调研·S-CASE-02〕，验收地位高于画质；但 Q2/Q7 是独立闸门，不能"表演好"放过越轴或漂移（R7）。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| 一镜塞满表情和动作，结果脸不动、动作也糊 | [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md) 的反面：拍太密 | 步骤 4 数拍；R-PRF-04 + R-PRF-08 PSNR 证据 |
| 情绪靠"慢下来"表达，整段变慢镜 | [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md) | 步骤 8：反应 ≈1.5s 落下即定住，剩余时间给后果；禁止把情绪写成慢动作 |
| 夸张表情把脸拉成另一个人 | [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md) | 步骤 3"不准动的部位"；出片用 R-VID-05 同尺寸裁脸比板图 |
| 两人同框，口型落在不说话的人脸上；或两人一张脸 | [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md) | 步骤 7 闭嘴句 / 背身出画；R-VID-04、R-VID-13 |
| 写满台词又要演，嘴赶词、表演没呼吸 | [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md) | 表情拍与台词共享时长：`dialogue_capacity.py` 的 `D3-rushed`（4.1 字/秒规划语速）出现 → 先减台词或减表情拍 |
| 提示词写"眼含泪光"，产出平脸却被记为通过 | [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md) | 步骤 11：PSNR + 裁剪双证据；不符则重出或把提示词回写为事实（R-VID-18） |
| 表演镜"技术全绿"即交付 | [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md) | PSNR 只证明"脸动了"，不证明"演对了"；必须过步骤 12 外部读表演 |

## 关联

- 理论：[`10-theory/13-performance-direction.md`](../../10-theory/13-performance-direction.md)（T13.1–T13.12）、[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)（拍的分类）、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)。
- 裁决：[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R4（表情拍 ≤2–3）、第二部分"口型"行。
- 上游：[`20-craft/script-doctor/SKILL.md`](../script-doctor/SKILL.md)（场景目标与台词容量）、[`20-craft/storyboard-long-take/SKILL.md`](../storyboard-long-take/SKILL.md)（拍数、起始帧方位）、[`20-craft/casting-and-canon/SKILL.md`](../casting-and-canon/SKILL.md)（锚点句、音色）。
- 下游：[`20-craft/keyframe-freeze/SKILL.md`](../keyframe-freeze/SKILL.md)（表情起点写进冻结提示词）、[`20-craft/video-prompting-h3/SKILL.md`](../video-prompting-h3/SKILL.md)、[`20-craft/shot-qc/SKILL.md`](../shot-qc/SKILL.md)、[`20-craft/edit-and-assemble/SKILL.md`](../edit-and-assemble/SKILL.md)（插入镜兜底）。
- 找错题：[`60-casebook/drills/DR-06.md`](../../60-casebook/drills/DR-06.md)（克隆脸）、[`60-casebook/drills/DR-11.md`](../../60-casebook/drills/DR-11.md)（容量挤压表演）、[`60-casebook/drills/DR-15.md`](../../60-casebook/drills/DR-15.md)（提示词≠产出）。
- 判据清单：[`50-rubrics/checklists/sound-color-performance.md`](../../50-rubrics/checklists/sound-color-performance.md)（R-PRF 段）。

## → 行为改变

- 下次写任何有人脸的镜时，先填表演卡的"任务动词 + 视线目标"两栏，再写提示词；填不出就不进入冻结。
- 下次多人对白镜送 H3 前，先确认每个非说话人有闭嘴句或已背身出画，`prompt_lint.py` 无 `VP-lipsync`。
- 下次表情特写出片后，先看 PSNR 中位：≥37 dB 直接判"表情未落地"，禁止凭接触表一格好看就通过。
- 下次同一表情两次重出仍僵，停止换 seed，改走库里肖夫兜底（中性脸 + 上下文镜）。
