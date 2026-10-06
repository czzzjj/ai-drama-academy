# 好/坏样例对 · 空间与动作（TP-08 – TP-14）

> 训练用法见 [`30-taste/README.md`](../README.md)。❌/✅ 中的镜号与提示词是学院构造的训练素材；「」内人类原话逐字取自 [`00-orientation/client-dossier.md`](../../00-orientation/client-dossier.md)。
> 判据所在清单：[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/storyboard.md`](../../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/keyframe.md`](../../50-rubrics/checklists/keyframe.md)、[`50-rubrics/checklists/video.md`](../../50-rubrics/checklists/video.md)。
> 相关案例卡：[`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)、[`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)。

## TP-08 · 轴线：trucks left 换边运镜 vs 单轴定侧
- ❌ 坏：起始帧方位是 `神=LEFT; 苏晓=RIGHT`，提示词却写 `The camera trucks left and arcs around Su Xiao as she weaves past the god, circling behind him before striking.` 人类 r4 复审：「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」。
- ✅ 好：元数据写 `- 轴线策略: 单轴定侧`。提示词：`The god on the LEFT raises its stone arm. Su Xiao on the RIGHT charges straight toward it. The camera slowly pushes in from a low angle; the frame jolts as her blade hits its chest. Su Xiao stays on the RIGHT side of the frame throughout.`
- 点评（≈200 字）：画面的左右位置已经被起始帧钉死，文字改不动它〔委托方实证·A5①〕。外部同 seed A/B 也证实，文字写的空间地图压不过场景图〔外部调研·S-H3-09〕。坏样一句话里塞了 truck、arc、weave、circling behind 四个换边信号，全部和起始帧冲突。模型会执行你写的**所有**指令，指令互相打架时它只能乱编，于是苏晓"乱跑"。好样的相机只在高度和距离上动（低机位缓推，接触瞬间顿一下），角色用画面位置来称呼，还写明全程保持在哪一侧。可迁移：提示词定稿前必须跑 `direction_audit.py`，DIR-camera 的 error 为 0 才算定稿。确实需要换边时，用剪辑接两个各自单轴的镜，不要在一次生成里换边。
- 可迁移判据：R-VP-04、R-SB-12、R-VID-14；TJ-10 视线引导｜溯源：A5, M4, S-H3-09

## TP-09 · 称呼：宽景只用名字 vs 画面位置称呼
- ❌ 坏：三人宽景写成 `Su Xiao attacks Nijiadi while Amu watches from behind.` 产出里，苏晓和尼加狄的左右对调了，阿姆跑到了两人中间。
- ✅ 好：`[S1] Su Xiao, the slim young woman on the RIGHT in a grey tunic` ／ `[S2] Nijiadi, the tall figure on the LEFT, his black arm on the LEFT side of the frame` ／ `[S3] Amu, the broad man small in the BACKGROUND, CENTER`。事件写成 `The woman on the RIGHT lunges at the tall figure on the LEFT.`，`- 起始帧方位: 尼加狄=LEFT; 苏晓=RIGHT; 阿姆=BG`。
- 点评（≈200 字）：宽景里脸很小，身份特征分辨不出来，模型把名字绑到哪个形体上几乎是随机的〔委托方实证·A5②〕。画面位置是模型唯一能稳定对齐的坐标，起始帧上谁在左、谁在右已经定了，用位置称呼就是在复用这个事实。好样还把"黑臂在画面左侧"这种方位属性写进了定义，这正是 C1-6 里左右臂画反的那一类属性。可迁移：只要起始帧里有 ≥2 个人，每个 `[S#]` 定义都必须带画面位置；事件句里优先用位置称呼，不用名字。审计时用 `direction_audit.py` 的 DIR-side 去核对附着在主体上的 LEFT/RIGHT 是否和起始帧方位一致。
- 可迁移判据：R-VP-05、R-VP-07、R-KF-05｜溯源：A5, C1-6

## TP-10 · 拍数：一镜五次换向 vs 一条线打完
- ❌ 坏：一个 9.42s 的镜，内容写"苏晓冲刺→翻滚→绕到神身后→跃起→转身→落地→再次冲向神→斩击"，`拍数` 一列却填 2。
- ✅ 好：拆成两个镜，并删掉"绕后"和"翻滚"。SHOT-051 写"苏晓冲刺→斩击神的胸口→被反震后退一步"，计空间拍 1、打击拍 2。SHOT-052 写"神反扑→苏晓横刀格挡→刀被压低，火星溅地"，计空间拍 1、打击拍 2。
- 点评（≈200 字）：每一次翻滚、换向、绕后都是一个**空间拍**，空间拍一多，画面空间就连续跳变〔委托方实证·A5③〕。`拍数` 填 2 是自欺：`segment_rhythm.py` 只能检查你写下来的数字，所以拍数必须按 R4 口径如实计（空间拍 + 表情拍）。打击拍可以很密，社区实测约 3 秒写 8–9 招，真速度按顺序打出来〔外部调研·S-H3-09〕；要少的是空间拍。好样把"一条线打完"落到了实处：每个镜只有一次位置改变，其余都是原地攻防。可迁移：分镜写完后，给每个 `→` 节点标上 [空间]、[打击] 或 [表情]，空间拍超过 3 的镜要么拆，要么删。
- 可迁移判据：R-SB-06、R-SB-07｜溯源：A5, P10, S-H3-09

## TP-11 · 特效："特效华丽" vs 冲击环从接触点炸开
- ❌ 坏：`An epic, spectacular magical explosion with stunning visual effects, very cinematic and powerful.` 人类反馈"特效不够"，下一轮又加了 `breathtaking`、`awe-inspiring`。
- ✅ 好：`Her blade meets the god's stone palm. A ring-shaped shockwave bursts outward from the point of contact, flattening the dust in a widening circle; cracks race across the floor toward the LEFT; small stones lift and fall for a second afterwards. The frame jolts once at the moment of contact.`
- 点评（≈200 字）：生成器渲染的是能被画出来的**事件**，不是评价〔委托方实证·M3〕。评价词等于让模型自己挑一个通用"特效"，结果要么平庸，要么冒出一个发光的实物。坏样的第二轮在同一层继续加形容词，是 G5 的典型表现：具体化的努力用在了错误的层。好样把特效拆成五个部分：来源（刀和掌接触）、接触点、扩散形态（一个环）、后果（尘土被压平、裂纹、碎石的余波）、相机响应（顿一下）。每一项都能在接触表上逐格核对。可迁移：遇到任何评价形容词，先拆成五栏：起始帧可见属性、事件、后果、声音、节奏。`prompt_lint.py` 的 VP-adjective 必须零命中。
- 可迁移判据：R-VP-16、R-SB-17、R-SCR-11｜溯源：M3, G5

## TP-12 · 史诗感：加形容词 vs 起始帧尺度参照
- ❌ 坏：冻结提示词写 `epic grand shot of Su Xiao facing the god, majestic, awe-inspiring`，产出是两人同高、平视的中景，背景一堵空墙。之后三轮都在视频提示词里加 `epic`。
- ✅ 好：冻结提示词写 `low camera at knee height looking up; the stone god on the LEFT fills two-thirds of the frame height, its head lost in the haze above; Su Xiao on the RIGHT reaches only its knee; broken pillars recede into three layers of haze; the only light is lava glow from below.`
- 点评（≈200 字）：史诗感是**画面级**属性，由起始帧决定，提示词救不了构图〔委托方实证·M2、P4〕。坏样在错误的层用力：起始帧已经是平视、两人同高，视频提示词写再多 `epic` 也改不了尺度关系，三轮投入全部白费，这就是 F3 补丁式迭代的样子。好样把"史诗"拆成能验收的画面属性：尺度参照（人只到膝盖）、低机位、三层纵深、单一来源的光。这四项缩到 270 宽、去色后依然读得出来。可迁移：被说"不够史诗"时，先回关键帧跑 TJ-04 第一帧海报测试和 TJ-11 尺度参照测试。不过关就重出关键帧，视频提示词一个字也不动。
- 可迁移判据：R-KF-07、R-KF-08；TJ-04、TJ-11｜溯源：M2, P4, G5, F3

## TP-13 · 重量：3 秒缓缓落地 vs 半秒砸地 + 后果
- ❌ 坏：分镜写"神一掌把苏晓击飞，她在空中翻转、缓缓落地（3s）"，提示词写 `she flies through the air, turning, and falls to the ground over three seconds.`
- ✅ 好：`The palm strike hits her shoulder; she is thrown back and hits the ground hard within half a second, skids a short distance across the stone, and lies still for a beat; dust settles around her; she presses one hand to the floor and pushes herself up. Real-time speed throughout, no slow motion.`
- 点评（≈200 字）：时长会被逐字读成事件速度：给摔倒 3 秒，就是月球重力下的慢镜头〔外部调研·S-H3-11〕。真实的摔倒和撞击大约 0.4–0.6 秒，重量感来自"停住"，不来自"下落"（"Weight comes from the stop, not the drop"）。好样镜长没变，剩下的时间分给了后果：滑行、静止一拍、尘土落下、撑地起身。观感因此有了重量。这也是 A3"慢镜死板"的一条新根因：慢不是因为动作少，而是动作被拉长了。可迁移：分镜写动作时，对照事件时长表（眨眼 0.3–0.5s、转头 0.5–0.8s、摔倒 0.4–0.6s、一步约 0.5s），时长有多余就加后果拍，不拉长动作。
- 可迁移判据：R-SB-19、R-VP-03、R-VID-15｜溯源：A3, S-H3-11

## TP-14 · 起幅：推近镜起幅已经是近景 vs 起幅取宽的一端
- ❌ 坏：分镜的运镜写"推近到苏晓眼睛的特写"，关键帧却已经是苏晓的半身近景，脸约占画面高度的 1/3。产出几乎推不动，要么推成一片糊掉的局部。
- ✅ 好：关键帧取宽的一端：苏晓全身位于画右下 1/3，神的手臂横在画左上。运镜写"缓推，停在她的眼睛上"，因果句是"因为神叫出她的真名，所以推近"。提示词里不写首帧脚手架句。
- 点评（≈200 字）：起始帧会钉死起幅构图。起幅已经很紧，模型就没有空间可推。外部实测的原话是 "A shot that must end tight has to open wide"〔外部调研·S-H3-08〕。另外，`[keyframe completion]`、"<Picture 1> is the first frame" 这类首帧脚手架句也会把运镜幅度砍掉一半，背景参考板同样如此〔外部调研·S-H3-08〕。这是 A4"无运镜"的设置层根因，和提示词措辞无关。好样把起幅放在景别最宽的一端，推近的终点用"停在谁身上"来写。可迁移：推近、收紧类的镜，关键帧景别至少要比终点宽两档。需要明显运镜的镜，必须处理 `prompt_lint.py` 报出的 VP-scaffold 提示。
- 可迁移判据：R-KF-09、R-VP-24｜溯源：A4, S-H3-08
