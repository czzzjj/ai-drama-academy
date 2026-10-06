---
name: storyboard-long-take
description: 把剧本拆成"段（SEQ）/ 拍 / 镜（SHOT）/ 剪辑点（CUT）"四层的长段多拍分镜表：8–15 秒一段承载一条完整动作链，空间拍与表情拍每镜 ≤2–3、打击拍可密，每镜写"因为 X，所以镜头 Y"的运镜因果句，单轴定侧并填起始帧方位列，短镜写理由，送生成前过 animatic 闸门；用 segment_rhythm / dialogue_capacity / h3_frame_grid 验。Use when converting a script into a storyboard, fixing "片段式 / 剧情跳跃 / 人物乱跑 / 运镜耿直", or before any keyframe/video generation. 触发词：分镜、分镜表、长镜头、长段多拍、段拍镜、运镜因果、起始帧方位、单轴定侧、轴线、短镜理由、预演、animatic、storyboard, long take, multi-beat, camera motivation, axis, screen direction. 不负责招式与交手细节（→ action-choreography）、提示词措辞（→ video-prompting-h3）、剪辑节奏执行（→ edit-and-assemble）。
---
# 长段多拍分镜（storyboard-long-take）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。表头与写法以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §1 为准；拍数与短镜立场见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R4、R5、R6。

## 何时用 / 何时不用
- **必须用**：剧本定稿后、关键帧之前；审片缺陷路由到"1 分镜"（A1 碎镜、A4 运镜耿直、A5 乱跑）时——回这里重做，不在剪辑或提示词里补。
- **不用**：打斗招式本身（→ [`action-choreography`](../action-choreography/SKILL.md)，但它的产出必须回填本表 `内容` 列）；台词删改（→ [`script-doctor`](../script-doctor/SKILL.md)）。
- 判决：**短剪不是罪，碎镜症是罪**（R6）。生成单位（镜）≥124 帧且承载一条完整动作链；剪辑单位（CUT）可以很短，快剪从长镜里取〔委托方实证·A1、P10、M1〕。

## 输入 → 输出
- 输入：`script.md`、`action-design.md`、`visual-bible.md`（段色彩脚本）、`anchors.md`（角色 ID）。
- 输出：`season-01/ep03/storyboard.md`（模板 [`70-playbooks/templates/storyboard.md`](../../70-playbooks/templates/storyboard.md)）与 `animatic.mp4`。四层术语：

| 层 | 是什么 | 约束 |
|---|---|---|
| 段 SEQ-nn | 一条完整动作链 / 一个戏剧单元 | 常态 8–15s（P10） |
| 拍 | 空间拍（位置/朝向/站位变）、表情拍（情绪状态变）、打击拍（原地攻防） | 空间拍 + 表情拍 ≤2–3/镜；打击拍可密（R4） |
| 镜 SHOT-nnn | 一次 H3 生成 | 5.17–15.08s（124–362 帧） |
| CUT | 剪辑单位，从镜里取 | 可 <5s，但必须指向一条 ≥124 帧的镜（R-CUT-12） |

```markdown
| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |
|---|---|---|---|---|---|---|---|---|---|
| SEQ-02 | SHOT-004 | 10.83 | 3 | 苏晓佯攻右肩→神抬臂格挡落空→苏晓矮身抓隙斩腿→神膝盖砸地、碎石溅起 | 缓推，接触瞬间画面一震 | 因为斩击接触，所以推近在接触帧被撞停 | 神=LEFT; 苏晓=RIGHT | 苏晓：就是现在！ | — |
| SEQ-02 | SHOT-005 | 5.88 | 2 | 神单膝跪地→地面裂纹从膝下扩散到苏晓脚边 | 上升 | 因为裂纹扩散到全场，所以镜头升高交代后果 | 神=LEFT; 苏晓=RIGHT | — | — |
```

## 步骤
1. **先切段**：按剧本每场"开场 → 收场状态"把每条完整动作链或戏剧单元划成一个 SEQ，常态 8–15s；同一条连续动作禁止切成两个镜号（R-SB-05）。每镜填 `段号`（R-SB-04）。
2. **再定镜**：每个送 H3 的镜 5.17–15.08s（R-SB-01、R-SB-02）；>15.08s 拆两镜，拆点放在拍与拍之间，不放在动作中间。整集生成镜均长 ≥5.0s 且 <5s 短镜占比 ≤20%（R-SB-03）。
3. **短镜理由**：<5.17s 的镜必须填实质性 `短镜理由`（如"本地生成字卡""剪辑从 SHOT-004 取 1.2s 插入"），并标注不送 H3；`—`/`TBD` 视同未填（契约 §1）。快剪需求写进剪辑意图，不写成新镜号。
4. **数拍（R4）**：`拍数` 只计空间拍 + 表情拍，每镜 ≤3（R-SB-06、R-SB-07）；>3 必须在 `内容` 写明空间如何不跳变，否则拆段。打击拍写进 `内容` 的 `→` 动作链，不计入 `拍数`——禁止为了消 `P10-beats-chain` 把打击拍计入。表情镜表情拍 ≤2–3（R-PRF-04）〔外部调研·S-H3-09〕。
5. **内容写事件**：`内容` 用 `→` 串联可见事件，禁止"华丽 / 史诗 / 震撼"类评价词（R-SB-17）〔委托方实证·M3〕；每镜写得出"这一镜改变了什么"（状态从 → 到），写不出删或并（R-SB-22）。
6. **速度与真实时长**：每个动作段标 ≥2 种速度层次（快 / 慢 / 爆 / 静），每个"慢"写设计理由（R-SB-18）；按真实事件时长排布（摔倒 0.4–0.6s、转头 0.5–0.8s、一步约 0.5s），剩余时间写给后果（R-SB-19）——时长会被读成事件速度〔外部调研·S-H3-11〕。
7. **运镜因果句**：`运镜因果` 必须是"因为 X，所以镜头 Y"；静止镜写"因为……，所以不动"（R-SB-08）。X 是画面内可见事件或信息/情绪转折（受击、爆发、腾跃、揭示、收束），Y 是叙事功能（reveal / follow / compress / release / isolate），R-SB-09。写不出 X 的运镜删掉。
8. **一个主运镜（R5）**：`运镜` 只写一个主运动，且属于高度（上升/下降/上摇/下摇）或距离（推/拉/变焦）维度；顿挫/震动写成"接触引起的相机响应"，不写成第二条运镜（R-SB-10）。需要两种运镜状态 → 拆两次生成，剪辑里接。推近/收紧镜的起幅必须是宽的一端（R-KF-09；"A shot that must end tight has to open wide"〔外部调研·S-H3-08〕）。
9. **单轴定侧 + 方位列**：每个有人物的镜填 `起始帧方位`，大写 `LEFT/RIGHT/CENTER/FG/BG`（R-SB-11）。`运镜` 与 `内容` 禁止左右维度运动（truck / arc / orbit / weave / pan / 绕到身后），R-SB-12；同场相邻镜左右顺序不反转、屏幕方向连续（画右出 → 画左入），越轴只用轴上缓冲镜或可见跨越动作（R-SB-13）。确需换边：单独新出一张支持换边的关键帧，提示词元数据写 `- 换边: 设计（理由…；起始帧支持证据…）`〔委托方实证·A5、M4〕。
10. **对白装得下**：`对白` 逐字取自剧本；跑 `python3 50-rubrics/scripts/dialogue_capacity.py --storyboard season-01/ep03/storyboard.md`，0 个 `D3-capacity / D3-margin / D3-split` error（R-SB-14）；每条 `D3-rushed / D3-tight` warn 已处置（延长到建议帧数、拆到听者镜、或删句，R-SB-15）；禁止调参消 error（R-SB-16）。
11. **本地生成镜**：纯色卡、字卡、精确文字、UI、logo 镜标为本地生成（剪辑单 `local:`），不安排送 H3（R-SB-21）〔委托方实证·D2〕。
12. **结构自检**：`python3 50-rubrics/scripts/segment_rhythm.py season-01/ep03/storyboard.md` → 0 error（`A1-short-no-reason`、`T2-over-max`、`A4-cause`、`A5-beats-many`、`P10-*`）；`python3 50-rubrics/scripts/h3_frame_grid.py --seconds 10.83` 换算每镜帧数并记入交接表（17k+5 网格）。
13. **animatic 闸门（人类拍板点②）**：用关键帧或占位图按分镜时长排幻灯式粗剪，配临时对白（≈4.1 字/秒占位）与节拍标记，自己 1× 连续看一遍，记录"第一次困惑时间点"与因果是否连得上（R-SB-23）；通过后才交 [`keyframe-freeze`](../keyframe-freeze/SKILL.md)。未过 R-SB 全部 `[自动]` 条目的镜禁止进入 prepare。
14. **双文档对齐**：提示词写完后，逐镜核对分镜与 `video-prompts.md` 的时长（含尾部余量口径）、对白、起始帧方位三项一致（R-SB-24）〔委托方实证·P7〕：`python3 50-rubrics/scripts/direction_audit.py season-01/ep03/video-prompts.md --storyboard season-01/ep03/storyboard.md`。

## 判据
- 分镜：R-SB-01 – R-SB-24 全部（结构 R-SB-01 – R-SB-07；运镜 R-SB-08 – R-SB-10；空间 R-SB-11 – R-SB-13；对白 R-SB-14 – R-SB-16；事件与速度 R-SB-17 – R-SB-20；本地与对齐 R-SB-21 – R-SB-24）。
- 下游验证：R-VID-14（全程左右不变）、R-VID-17（因果事件 X 与镜头动作 Y 同刻）、R-CUT-12（短 CUT 指向长镜）、R-KF-09。
- Q 维度：Q2 空间与调度、Q6 节奏与速度（主）、Q1 叙事与钩子。

## 失败模式
- **29 镜均长 2.96s，"片段式、剧情跳跃"** → [`60-casebook/cards/A1-fragmented-shots.md`](../../60-casebook/cards/A1-fragmented-shots.md)：防线 = 步骤 1–3 段先于镜、≥124 帧、短镜要理由。
- **运镜不电影 / 耿直、primitives 堆砌** → [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)：防线 = 步骤 7 因果句 + 步骤 8 一个主运镜。
- **"又变成苏晓乱跑"** → [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)：防线 = 步骤 9 单轴定侧 + 方位列 + 禁左右维度。
- **拍太多、空间连续跳变** → [`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)：防线 = 步骤 4 打击拍密、空间拍少。
- **动作像月球重力** → [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)：防线 = 步骤 6 真实事件时长 + 后果占时。
- **台词装不下** → [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md)：防线 = 步骤 10。
- **为消指标调参数** → [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md)：防线 = R-SB-07、R-SB-16 禁止"为过脚本改口径"。

## 关联
- 理论：[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)、[`10-theory/05-rhythm-engineering.md`](../../10-theory/05-rhythm-engineering.md)。
- 好/坏样例：[`30-taste/pairs/space-action.md`](../../30-taste/pairs/space-action.md)、[`30-taste/pairs/narrative-rhythm.md`](../../30-taste/pairs/narrative-rhythm.md)。
- 相邻技能：[`script-doctor`](../script-doctor/SKILL.md)、[`action-choreography`](../action-choreography/SKILL.md)、[`keyframe-freeze`](../keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../video-prompting-h3/SKILL.md)、`edit-and-assemble`、[`production-director`](../production-director/SKILL.md)。
- 找错题：DR-01、DR-04、DR-05、DR-11、DR-21、DR-22。
- → 行为改变：下次想给一个动作开新镜号时，先问"它和上一镜是不是同一条动作链"；是 → 并入同一镜，快剪留给剪辑。
