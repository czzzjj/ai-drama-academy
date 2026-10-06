---
name: action-choreography
description: 设计打斗与动作戏：每场 ≥3 环战术链 + ≥1 个镜内可见的交手回合，每次接触写全七相（意图→预备→发力→接触→反应→回收→后果），出招与受击同镜同次生成，按真实事件时长排时、打击拍密而空间拍少，相机顿挫写成事件引起的响应，全程实时速度、重量落在"停"上。Use when a script contains a fight, chase, strike, fall or any physical action, or when feedback says "打斗缺席 / 打斗逻辑不对 / 像慢动作 / 没有力量感". 触发词：打斗、武打、动作设计、招式、交手回合、战术链、七相、接触、受击、反应、后果、慢动作、力量感、fight choreography, action design, exchange, hit reaction, real-time speed, impact. 不负责镜头切分与轴线（→ storyboard-long-take）、提示词最终措辞（→ video-prompting-h3）、拟音与配乐卡点（→ sound-design）。
---
# 动作与打斗设计（action-choreography）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。拍数与运镜立场见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R4、R5；A3 新增根因见同文件第二部分。

## 何时用 / 何时不用
- **必须用**：剧本出现任何打斗、追逐、击打、摔倒、扑跃之后，分镜定稿之前；人类反馈"打斗缺席 / 打斗逻辑 / 慢 / 没劲"时（G6 中"打斗逻辑"= 战术链与交手回合缺失，见 [`00-orientation/glossary.md`](../../00-orientation/glossary.md)）。
- **不用**：纯表情戏（→ `performance-direction`）；特效事件链若不涉及身体接触，只用本技能步骤 6–7 的"来源 → 接触 → 扩散 → 后果"写法。
- 判决：委托方"含蓄策略"吃掉了交手，A2 打斗缺席；慢镜是默认偏差不是风格〔委托方实证·A2、A3〕。打斗的修正是**打击拍要密，空间拍要少**（R4）。

## 输入 → 输出
- 输入：`script.md` 打斗场（战术链初稿）、`anchors.md`（持物手、体量）、`storyboard.md` 段草案与 `起始帧方位`。
- 输出：`season-01/ep03/action-design.md`（无独立模板，按下列三张表写），并把动作链回填 [`70-playbooks/templates/storyboard.md`](../../70-playbooks/templates/storyboard.md) 的 `内容` 列。

战术链表（每场一行）：
```markdown
| 场 | 战术链（≥3 环） | 交手回合所在镜 | 结果 |
|---|---|---|---|
| 场 4 | 诱敌（苏晓佯攻右肩）→ 落空（神抬臂格挡空）→ 抓隙（矮身切入）→ 击飞（斩腿，神跪地） | SHOT-004 | 神失去机动，苏晓获得接近封印的时间 |
```
七相表（每次接触一行）：
```markdown
| 镜 | 接触# | 意图 | 预备 | 发力 | 接触 | 反应 | 回收 | 后果 | 时长分配 |
|---|---|---|---|---|---|---|---|---|---|
| SHOT-004 | 3 | 苏晓盯住神的膝 | 重心下沉、刀后引 | 蹬地横斩 | 刀刃砍进石膝、火星 | 神膝弯折、上身前栽 | 苏晓借反作用力后滑一步 | 神单膝砸地、碎石溅起、尘雾停住 | 0.3/0.3/0.2/0.1/0.5/0.4/2.0s |
```
事件时长表（真实时长，排时依据）：摔倒 0.4–0.6s；转头 0.5–0.8s；一步约 0.5s；挥击接触 ≤0.2s；其余时间给后果与静止（R-SB-19）。

## 步骤
1. **战术链先于招式**：每场打斗写 ≥3 环战术链（诱敌 → 落空 → 抓隙 → 击飞），每环是"谁利用了什么"；"二人激战""大战数回合"类概括句不算打斗描写（R-SCR-10）。战术链必须能接回本集主因果链的"做了什么 → 结果"。
2. **交手回合**：每场至少 1 个**我攻 → 你挡/闪 → 我变招**的完整回合，且在**同一镜内同框可见**；出招与受击在同一次生成里，禁止拆成"出招镜 + 受击镜"（R-SB-20）〔委托方实证·A2；外部调研·F-ZEN-13；学院推断：拆开后接触帧落在剪点、力量感丢失——验证：同一回合"同镜 vs 拆两镜"各 2 seed，冷观众盲评哪版"打中了"〕。
3. **七相写全**：每次接触填七相表；只写一个动词的接触（"掌掴""斩"）不算数——H3 双人接触实测只写一个动词效果最差，写全"接近—接触—施力—结果"显著改善〔外部调研·S-H3-10〕。接触相必须写可见的材质反馈（火星、碎石、布料撕裂），反应相必须写受力方向（"膝弯折、上身前栽"）。
4. **起始帧取意图/预备相**：每镜起始帧必须是动作链起点（意图或预备相），不是接触或后果相，否则视频没有完整动作可演（R-KF-14）。把这一点写进交给 [`keyframe-freeze`](../keyframe-freeze/SKILL.md) 的说明。
5. **拍的三分法（R4）**：
   - 打击拍（原地攻防）可以密：约 3 秒写 8–9 招，H3 4 份提示词 × 2 seed 全部按顺序真速度打出〔外部调研·S-H3-09〕；
   - 空间拍（位置/朝向/站位改变）每镜 ≤2–3，打斗中翻滚、绕身、换向是空间拍，最容易引起乱跑〔委托方实证·A5〕；
   - 港式节奏可参考：一镜约 3 招，第 4 招做剪点桥；停 → 爆 → 停〔外部调研·S-STORY-17、S-STORY-19〕。
   拆打斗镜的理由应是"换角度"，不是"节拍太多"。
6. **按真实时长排时**：按事件时长表分配七相时长，**剩余时间写给后果与静止**；时长会被读成事件速度——给摔倒 1.5s 就是月球重力慢动作；"Weight comes from the stop, not the drop"〔外部调研·S-H3-11〕（R-SB-19）。镜内事件密度不足 = 慢。
7. **后果必写**：每次有效接触后写后果相（倒地、碎裂、尘停、对手失去机动），并说明后果如何改变下一环战术链；无后果的打击 = 无重量。特效写成 来源 → 接触 → 扩散 → 后果（R-VP-16）。
8. **速度层次**：每个动作段标 ≥2 种速度层次（快 / 慢 / 爆 / 静），每个"慢"写设计理由（R-SB-18）；默认全部实时：提示词必含 `Real-time speed throughout, no slow motion`（R-VP-03），只有元数据声明 `- 慢动作: 设计选择（理由…）` 才豁免。慢动作是生成器的默认偏差（更易保持时序一致）〔外部调研·S-VGEN-19、S-VGEN-11〕，不是风格。
9. **相机顿挫 = 事件引起的响应（R5）**：一镜一个主运镜（高度或距离维度）；接触时的"顿/震"写成 `the frame jolts as the blade hits the stone`，挂在接触事件上，禁止写成第二条独立运镜指令（R-SB-10、R-VP-24）。需要两种运镜状态 → 拆两次生成，剪辑里接。
10. **空间锁**：打斗全程沿用 `起始帧方位`，攻防只沿"同侧直线进退"；需要绕到身后 → 交 [`storyboard-long-take`](../storyboard-long-take/SKILL.md) 走换边设计流程，不在本镜里写 arc/orbit（R-SB-12）。
11. **回填与验**：把战术链与七相压缩成 `→` 动作链写进分镜 `内容` 列（打击拍不计入 `拍数`，R-SB-07），然后跑 `python3 50-rubrics/scripts/segment_rhythm.py season-01/ep03/storyboard.md`（0 个 `A5-beats-many` / `P10-*` error）。提示词阶段跑 `python3 50-rubrics/scripts/prompt_lint.py season-01/ep03/video-prompts.md`（`VP-realtime` 0 error）。
12. **镜头验收要求**：交给 `shot-qc` 的验收指令写明：动作区间每 0.25s 补抽帧（`ffmpeg -i SHOT-004.mp4 -vf "fps=4,tile=4x4" qc/SHOT-004/action-grid.png`），看接触三帧（TJ-16）与速度曲线（TJ-17）；无漂浮式慢放（R-VID-15）；运镜响应发生在接触那一刻（R-VID-17）。拟音击中声落在接触帧，交 `sound-design`（R-SND-08、R-SND-03）。

## 判据
- 剧本与分镜：R-SCR-10、R-SB-06、R-SB-07、R-SB-10、R-SB-17、R-SB-18、R-SB-19、R-SB-20。
- 关键帧与提示词：R-KF-14、R-VP-03、R-VP-16、R-VP-24。
- 视频与声音：R-VID-15、R-VID-17、R-SND-03、R-SND-07、R-SND-08。
- 审美判据卡：TJ-16 接触三帧测试、TJ-17 速度曲线测试（[`30-taste/judgment-cards.md`](../../30-taste/judgment-cards.md)）。
- Q 维度：Q3 动作与物理（主）、Q4 特效与事件、Q6 节奏与速度、Q2 空间与调度。

## 失败模式
- **打斗被"含蓄处理"掉，只剩对峙和结果** → [`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)：防线 = 步骤 1–2 战术链 + 同框交手回合。
- **动作漂浮、像慢动作** → [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)：防线 = 步骤 6 真实时长 + 后果占时 + 步骤 8 实时速度句。
- **为了"有力量"加运镜，人物开始乱跑** → [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)：防线 = 步骤 9 顿挫挂事件 + 步骤 10 同侧直线进退。
- **运镜和事件脱钩（推近不停在接触上）** → [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)：防线 = 步骤 9 因果绑定。
- **出招镜和受击镜拆开、碎成几颗短镜** → [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)：防线 = 步骤 2 同镜同次生成。
- **提示词写 "epic fight" 当修复** → [`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)：防线 = 病灶在动作设计，回本技能重写战术链，不在提示词加形容词。

## 关联
- 理论：[`10-theory/04-action-design.md`](../../10-theory/04-action-design.md)、[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)。
- 好/坏样例：[`30-taste/pairs/space-action.md`](../../30-taste/pairs/space-action.md)；风格卡 [`30-taste/style-cards/dark-fantasy-epic.md`](../../30-taste/style-cards/dark-fantasy-epic.md)、[`30-taste/style-cards/stylized-3d.md`](../../30-taste/style-cards/stylized-3d.md)。
- 相邻技能：[`script-doctor`](../script-doctor/SKILL.md)、[`storyboard-long-take`](../storyboard-long-take/SKILL.md)、[`keyframe-freeze`](../keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../video-prompting-h3/SKILL.md)、`sound-design`、`shot-qc`。
- 找错题：DR-02（打斗缺席）、DR-03（慢镜）、DR-21（"打斗逻辑"反馈翻译）。
- → 行为改变：下次写任何接触动作，先填七相表并按事件时长表分时间；填不满七格的接触不得进入分镜。
