---
id: A5
title: 空间调度混乱
group: A 叙事与节奏
scope: 通用
severity: 致命
provenance: 委托方实证
skills: [storyboard-long-take, keyframe-freeze, video-prompting-h3, shot-qc, action-choreography]
drills: [DR-05, DR-20, DR-22]
---
# A5 · 空间调度混乱（最难的一课）

> 一句话：**左右与轴线由起始帧图钉死，文字改不动；文字里每一个与起始帧打架的方位词，都会被模型"执行"成乱跑。** 空间在图里定，文字只负责高度与距离。

## 症状（含人类主创原话，逐字引用档案）

- r4 复审，人类主创原话：「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」〔委托方实证·A5〕。
- 关键字是「又」：空间混乱不是 r4 才出现的新病，而是此前修过、在后续轮次被别的修改带回来的老病〔委托方实证·A5、F3〕。
- 观感层面：观众无法回答"谁在画左、谁在画右、谁在追谁、BOSS 在场地哪里"，打斗因果随之不可读——这是 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) 的阻断缺陷（Q2：角色左右位置在段内无理由互换 / "乱跑"）。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 场合：r1→r5 五轮打斗实验中的 r4 复审〔委托方实证·T-4、F3〕。五轮依次被修的反馈主题是 运镜 → 特效 → 史诗 → 空间〔委托方实证·F3〕。
- 起始帧（关键帧，送 `first_frame`）钉的布局：**神在左 / 苏晓在右**〔委托方实证·A5①〕。
- 同一镜的视频提示词里写了换边运镜词：`trucks left`、`arcs around`、`weaves`〔委托方实证·A5①〕。
- 段内节拍：重复接近、翻滚、换向〔委托方实证·A5③〕。
- r4 vs r5 对照（本卡核心证据）：

| 维度 | r4（被打回） | r5（实测达标） |
|---|---|---|
| 相机运动维度 | 左右维度：`trucks left` / `arcs around` / `weaves` | 只动高度与距离：缓推 / 顿挫 / 上摇 / 拉回；删掉一切 truck/arc/orbit/weave |
| 文字 vs 起始帧 | 起始帧"神左/苏晓右"，文字要求相机换边 → 互相矛盾 | 文字服从起始帧，不碰左右维度 |
| 节拍 | 重复接近、翻滚、换向 → 空间连续跳变 | 减拍到"一条线打完" |
| 宽景身份称呼 | 靠名字（由根因②反推） | 画面位置称呼：`the god on the LEFT` |
| 定稿前检查 | 无方位审计（由 r5 新增反推） | grep left/right/turn/toward/behind/front/arc/truck/orbit 逐一排查矛盾 |
| 结论 | 「又变成苏晓乱跑……」 | 空间维度实测达标〔委托方实证·A5〕；全片仍未到可发布线〔委托方实证·T-4、F3〕 |

## 根因（分条；区分"直接原因"与"方法论原因"）

**直接原因（生成层）**
1. **起始帧钉死轴线，文字改不动**：H3 首帧驱动时，画面左右位置与轴线由起始帧决定；提示词再写 `trucks left`/`arcs around`，模型同时满足"图里神在左"与"相机绕到另一侧"两条互斥指令，只能编出空间跳变〔委托方实证·A5①、P4〕。外部同证：同 seed A/B，文字空间地图压不过场景图，"空间只能在图里定"〔外部调研·S-H3-09〕。
2. **宽景只用名字称呼**：多人宽景中模型不知道"苏晓"对应画里哪个人形，名字与位置脱钩〔委托方实证·A5②〕。
3. **空间拍太多**：重复接近、翻滚、换向 = 一镜内多次改变相对站位，每次改变都是一次让模型重新排布空间的机会〔委托方实证·A5③〕。注意区分：这里超标的是**空间拍**，不是打击拍（见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R4）。
4. **指令矛盾未全量排查**：模型会执行你写的**所有**指令，指令打架它就乱编〔委托方实证·A5④〕。同类矛盾还有：声明慢动作又写实时速度句；"holds one single pose completely rigid" 与运镜同写，运镜位移从 98–108% 画宽掉到 22%〔外部调研·S-H3-08〕。

**方法论原因（设计层）**
5. **空间没有在预制作阶段被设计**：没有场地平面/站位图、没有"本场轴线在哪一侧"的声明，空间被推迟到视频提示词里"用文字描述"——病灶在分镜 + 起始帧阶段，却在生成阶段打补丁〔委托方实证·G7；学院推断：验证法=查该轮是否存在 storyboard 的 `起始帧方位` 列与场地图，缺则成立〕。外部做法：平面图坐标 → 灰模每机位一张 → 转写实板，第三轮起各机位空间一致〔外部调研·S-H3-09〕。
6. **补丁式修复把老病带回来**：修 A4"无运镜"时，机械套用运镜 primitives 词汇（含 truck/arc/orbit 等左右维度原语），正好与起始帧轴线冲突〔委托方实证·A4②、F3、F4〕。〔学院推断〕r4 的换边词来自为修 A4 引入的 primitives；验证法：对 r1–r4 各轮 `video-prompts.md` 跑 `direction_audit.py`，比较 DIR-camera 命中数是否在修运镜那轮后上升。
7. **没有"轴线"这个独立闸门**：委托方 QC 很严（抽帧/PSNR/转写），但全是"出没出错"的检查，没有"左右是否守住"的检查。外部：180° 规则在战斗叙事中尤其重要〔外部调研·S-STORY-08〕；剪辑取舍中 3D 空间排最后，但 AI 生成里越轴/乱跑会直接摧毁"故事看得懂"，必须作为独立闸门〔外部调研·S-STORY-13；学院立场见 evidence-reconciliation R7〕。
8. **逐镜独立生成天然不连续**：100 对空间相连的镜头只有 26 对背景一致〔外部调研·S-PIPE-08〕；只给角色与地点图独立生成时，与上一镜尾帧的 NCC 仅 0.01–0.41，景别和站位都会跳〔外部调研·S-PIPE-03〕。所以相邻镜必须共享已过关关键帧（链式参考 P5/M7），而不是各自从文字重建空间。

## 修正过程（做了什么、第几轮、结果）

1. r4 被打回后，委托方回头深挖已安装的专业分镜技能，定位到根因①–④〔委托方实证·A5〕。
2. r5 方案 = **单轴定侧**：相机只做"高度与距离"维度运动（缓推/顿挫/上摇/拉回），删除一切 truck/arc/orbit/weave；减拍到"一条线打完"；宽景用画面位置称呼；提示词落地前跑方位词全量审计〔委托方实证·A5、M4〕。
3. 结果：r5 空间维度**实测达标**〔委托方实证·A5〕。但人类主创对整体仍判"不够"——单轴定侧修好的是 Q2 空间，不是全片〔委托方实证·F3、T-4〕。
4. 学院补强（r5 之后，〔学院推断〕，验证法见各条判据）：把 r5 的人工 grep 固化成 [`50-rubrics/scripts/direction_audit.py`](../../50-rubrics/scripts/direction_audit.py)，把"换边"从禁止改为"需声明 + 起始帧证据"的受控例外（`- 换边: 设计（理由…；起始帧支持证据…）`，见 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §2）。

### 方位词全量审计清单（`direction_audit.py` 实际词表 → 处置）

| 类别 | 命中词（EN / 中文） | 指挥谁 | 判定 | 处置 |
|---|---|---|---|---|
| 相机左右运动 DIR-camera | truck / orbit / pan / crab / arc / circle / weave / 360° / sideways / lateral；环绕、横移、侧移、平移、环拍、绕拍、向左/右摇·移·甩、横摇、甩镜、弧线/弧形运镜、360度；相机作主语时的 around / behind / left / right / turn | 相机 | 单轴定侧（或未声明）且无 `换边` 元数据 → **error** | 改 push-in / pull-back / tilt up / crane up |
| 主体侧位 DIR-side | `[S1] … on the RIGHT`、`the god on the LEFT` | 主体 | 经 `角色映射` 对 `起始帧方位`：矛盾 → **error**，一致 → info | 让文字服从起始帧 |
| 主体路径 DIR-path | behind / around / weave / flank / circle / sidestep / switch·swap·change sides / cross over·cross the axis/line；绕到、绕行、绕过、绕、换边、换位、闪到身后 | 主体 | **warn**：空间连续跳变风险（A5③） | 改同侧直线进退，或拆新镜 |
| 需目视 DIR-check | turn / toward(s) / front / in front of；转身、转向、左转/右转；角色自身左右（左手、right hand）；台词里的方位词；代词无法解析 | 不确定 | visual | 打开起始帧逐处看并留证据 |
| 否定 DIR-negated | never trucks / no orbit / 不绕 | — | info，不计矛盾 | — |
| 文档对账 | DIR-layout（分镜 ≠ 提示词 `起始帧方位`）/ DIR-mapping（≥2 人缺 `角色映射`）/ DIR-axis（未声明 `轴线策略`） | — | error / error / warn | 补齐元数据 |

报告末行固定为「方位词审计：通过（0 处矛盾）」或「方位词审计：不通过（N 处矛盾）」——只有前者才允许提示词定稿。

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

1. [自动] `direction_audit.py video-prompts.md --storyboard storyboard.md` 末行为「方位词审计：通过（0 处矛盾）」；DIR-camera / DIR-side / DIR-layout / DIR-mapping 任一 error → 提示词不得定稿、不得进 prepare。〔A5、M4、P7〕→ video-prompt 清单
2. [自动] 每个 DIR-path warn 必须有处置记录：改为同侧直线进退 / 拆新镜 / 在 `- 换边:` 元数据写理由 + 起始帧支持证据；`换边: 否/无/no` 视同未声明。〔A5③〕→ video-prompt 清单
3. [自动] `prompt_lint.py` 无 VP-position warn：`起始帧方位` ≥2 人时，每个 `[S#]` 定义含 "on the LEFT/RIGHT" 画面位置称呼。〔A5②〕→ video-prompt 清单
4. [自动] `segment_rhythm.py` 的 A5-beats-many（拍数 > 3）必须在 `内容` 列写明空间如何不跳变，否则拆段；`拍数` 只计空间拍 + 表情拍，打击拍写在动作链里（R4）。〔A5③〕→ storyboard 清单
5. [目视] 起始帧方位声明逐人对图核验：谁在画左/画右、朝向、与场地地标的相对位置；关键帧为 9:16（1536×2752）或送入前已裁到 9:16——`first_frame` 是"plain stretch to canvas"，比例不对会挤压几何锚〔外部调研·S-H3-03〕。证据：关键帧裁剪图 + 方位声明截图。→ keyframe 清单
6. [目视] 视频产出用 `contact_sheet.py <clip> --keyframe <REF-…-START>` 出接触表：首/中/末格每个角色仍在声明一侧；任何换边必须能对应到分镜的 `换边` 设计。单张静帧不判动作，看连续格。→ video 清单
7. [目视] 同场相邻镜守 180° 规则：左右顺序不反转、屏幕方向连续（画右出 → 画左入）；合法越轴只有三种——轴上缓冲镜、可见的跨轴运镜、角色自己走过轴线〔外部调研·S-STORY-08〕；相邻镜挂同场已过关键帧（P5/M7）。→ final-cut 清单
8. [冷观众] 看完打斗段后，冷观众能说出"谁在哪一侧、谁在追谁、BOSS 在场地哪里"；≥2 人答错同一段 → 回分镜阶段。〔学院推断：阈值沿用 definition-of-done L1 的 2/3 规则，待首次冷观众测试校准〕→ final-cut 清单

## → 行为改变（下次……）

- 下次写分镜时，**先**画本场站位图（谁左谁右、轴线、出入口方向），把 `起始帧方位` 与 `轴线策略: 单轴定侧` 写进分镜表，**再**写运镜；空间在关键帧里定，不在视频提示词里定。
- 下次写运镜时，**只**在高度与距离两个维度选一个主运镜（push-in / pull-back / tilt up / crane up）；需要动感时改用**事件引起的相机响应**（`the frame jolts as the blade hits the stone`），禁止为"更有电影感"写 truck/arc/orbit/weave。
- 下次宽景 ≥2 人时，在 `subject_definitions` 里用 `the god on the LEFT` / `the young swordswoman on the RIGHT` 定义主体，**禁止**只靠名字。
- 下次提示词定稿前，**必须**跑 `direction_audit.py`，逐条处置 error / warn / visual；审计不通过就不 prepare——不是"再加几个方位词"。
- 下次确实需要换边（角色绕后偷袭等），**先**出一张支持换边的新起始帧或拆成两次生成在剪辑里接，并写 `- 换边: 设计（理由…；起始帧支持证据…）`；禁止在一次生成里用文字让相机绕过去。
- 下次收到任何"运镜/特效/史诗"类反馈并修改提示词后，**必须**重跑方位审计——修别的维度最容易把 A5 带回来（「又变成」）。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ "图定空间、字定运动"对一切首帧驱动的 I2V 成立（H3 FL2VA/Ref2VA 挂起始帧、其他 I2V 模型同理）；首帧脚手架会钉死起幅（R2），需要钉轴线时保留它正是为此〔外部调研·S-H3-08〕。
- ★ 180° 规则、画面位置称呼、方位词审计对文戏同样成立：对话正反打的视线方向与左右顺序也会被换边词搅乱。
- ★ 拍数纪律对任何题材成立，但要按 R4 区分：空间拍少、打击拍可以密；不要因 A5 把打斗本身砍掉（那会变回 A2）。
- ☆ 词表与脚本针对英文提示词 + 委托方元数据格式；换节点（JSON 字段）时按同名键转换，规则不变。
- ☆ 纯文生视频（无起始帧）时轴线由文字建立，审计改为"全段方位词与第一句站位描述一致"〔学院推断：验证法=同提示词 3 seed 出片，接触表看左右是否稳定〕。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/storyboard-long-take/SKILL.md`](../../20-craft/storyboard-long-take/SKILL.md)（站位图、方位声明、拍数）、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)（起始帧钉轴线）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（单轴定侧、画面位置称呼、方位审计）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（接触表核左右）、[`20-craft/action-choreography/SKILL.md`](../../20-craft/action-choreography/SKILL.md)（打击拍 vs 空间拍）。
- 理论：[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/06-long-take-multi-beat.md`](../../10-theory/06-long-take-multi-beat.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)。
- 判据清单：[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)。
- 脚本：[`50-rubrics/scripts/direction_audit.py`](../../50-rubrics/scripts/direction_audit.py)、[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/segment_rhythm.py`](../../50-rubrics/scripts/segment_rhythm.py)、[`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)。
- 找错题：[`60-casebook/drills/DR-05.md`](../../60-casebook/drills/DR-05.md)（空间混乱）、[`60-casebook/drills/DR-20.md`](../../60-casebook/drills/DR-20.md)（综合复盘）、[`60-casebook/drills/DR-22.md`](../../60-casebook/drills/DR-22.md)（病灶路由）。
- 相邻案例：[`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)（修运镜引入换边词）、[`60-casebook/cards/A2-missing-fights.md`](../../60-casebook/cards/A2-missing-fights.md)（减拍≠砍打斗）、[`60-casebook/cards/F3-patch-iteration.md`](../../60-casebook/cards/F3-patch-iteration.md)、[`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)（C1-6 方位类属性需放大核验）。
