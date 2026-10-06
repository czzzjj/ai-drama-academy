# 03 · 空间调度

> 左右关系和轴线由起始帧那张图决定，文字改不了。文字里每一个和起始帧打架的方位词，都会被模型当成指令执行，结果就是人物乱跑。所以空间在图里定，相机只动高度和距离，角色按画面位置称呼，提示词定稿前要先通过方位词审计 ｜ 浓缩案例：A5, M4, P4, P5, C1-6 ｜ 对应技能：storyboard-long-take, keyframe-freeze, video-prompting-h3, shot-qc, action-choreography

## 核心判决

**T03.1 全片默认单轴定侧：同一场戏只有一条轴线，相机永远在它的同一侧，只做高度和距离两个维度的运动（缓推、顿挫、上摇、拉回）。**
为什么：r4 起始帧钉了"神在左 / 苏晓在右"，提示词写了 `trucks left`、`arcs around`、`weaves`，结果被人类主创打回：「又变成苏晓乱跑、分镜和场地和 BOSS 位置混乱的效果了」。r5 删掉所有左右维度的运动后，空间维度实测达标〔委托方实证·A5、M4〕。判据：R-SB-12、R-VP-04。

**T03.2 空间只能在图里定：场地布局、站位、轴线侧由场景板和起始帧锁定；提示词里的文字空间地图视为无效。**
为什么：同 seed 做 A/B，文字写的空间地图压不过场景图，"空間只能在圖裡定"〔外部调研·F-H3-21〕；起始帧决定画面层面的一切〔委托方实证·P4、M2〕。外部的做法是：平面图坐标 → 每个机位一张灰模 → 转成写实板，到第三轮各机位的空间就一致了〔外部调研·S-H3-09〕。

**T03.3 两人及以上同框的镜头，用画面位置称呼角色（`the god on the LEFT`），不能只写名字。**
为什么：宽景里模型不知道"苏晓"对应画面里的哪个人形，名字和位置会脱钩〔委托方实证·A5②〕。判据：R-VP-05、R-VP-07；`prompt_lint.py` 的 `VP-position`。

**T03.4 提示词定稿前必须跑方位词全量审计；`direction_audit.py` 不通过，提示词就不能定稿。**
为什么：模型会执行你写下的**所有**指令，指令之间打架，它就自己乱编〔委托方实证·A5④〕。r5 的做法是人工 grep left/right/turn/toward/behind/front/arc/truck/orbit，逐个排查矛盾〔委托方实证·A5〕；现在这一步固化成了 [`50-rubrics/scripts/direction_audit.py`](../50-rubrics/scripts/direction_audit.py)。判据：R-VP-04、R-VP-06。

**T03.5 一镜里的空间拍（位置、朝向、相对站位的改变）不超过 2–3 个；打击拍（原地攻防）可以很密。两者分开计数。**
为什么：重复接近、翻滚、换向会让空间连续跳变〔委托方实证·A5③〕；但武打例外：约 3 秒写 8–9 招，能按顺序以真实速度打出来〔外部调研·F-H3-17，置信度低〕。学院立场见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) R4：分镜 `拍数` 列只计空间拍和表情拍。判据：R-SB-06、R-SB-07。

**T03.6 换边是受控的例外，不是禁区：分镜要声明 `轴线策略: 换边` 和 `- 换边: 设计（理由…；起始帧支持证据…）`，并且只能用三种合法越轴方式之一。**
为什么：180° 规则给出的越轴办法有：在轴线上插缓冲镜、用看得见的跨轴运镜、让角色自己走过轴线〔外部调研·F-STORY-13〕。`direction_audit.py` 对已声明换边的镜报 `visual`，要求附上起始帧证据。

**T03.7 屏幕方向要连续：从画右出画，下一镜就从画左入画；相邻镜头之间人物的左右顺序不能反转。**
为什么：越过轴线后，两个人"看起来朝同一个方向"，不再面对面〔外部调研·S-STORY-11〕；对运动中的主体来说，轴线就是运动方向〔外部调研·S-STORY-11〕。判据：R-SB-13。

**T03.8 每场戏的开头、每次空间发生变化之后，都要给一个能看清地理关系的镜头；动作段每 3–5 个短切之后插一个重新定位的全景。**
为什么：Greengrass 式的手持碎切让身体处在 "architectural vacuum" 里，观众没法重建空间〔外部调研·F-STORY-26〕；港片靠 "judicious long shots keep us oriented"〔外部调研·S-STORY-18〕。

**T03.9 "方向 / 方位"类属性（左臂右臂、站在哪一侧、谁朝哪看）必须单独放大核验，不能看一眼整体就放行。**
为什么：尼加狄左右臂方位反了，靠 3 seed 抽卡才选出方位正确的版本〔委托方实证·C1-6〕；黑臂对比弱的问题在早期验收中被误判放行〔委托方实证·C1-7、C2〕。判据：R-VID-14。

**T03.10 在 AI 生成里，空间错误是独立闸门；不能拿"情绪对了"当理由放过。**
为什么：Murch 的六原则把三维空间排在最后〔外部调研·F-STORY-07〕，但在 AI 生成中，越轴、乱跑、漂移是最高频的缺陷，而且会直接摧毁"故事看得懂"这一层（学院立场见 evidence-reconciliation R7）。Q2 的阻断缺陷就是"角色左右位置在段内无理由互换"（见 [`50-rubrics/definition-of-done.md`](../50-rubrics/definition-of-done.md)）。

## 机制解释

1. **首帧驱动 = 几何锚点。** H3 的 first_frame 是 "geometry anchor"〔外部调研·S-H3-03〕。生成从这张图开始"往后演"，图里的左右关系是既成事实。文字要求相机换边时，模型要同时满足两件互斥的事：第一帧神在左，同时镜头绕到对面。它只能在中间某处编出一个跳变——观众看到的就是人物突然换了位置。
2. **名字不是坐标。** 模型通过参考图认人，名字到画面中人形的映射不稳定，多人宽景时尤其如此。画面位置是唯一不会歧义的坐标。
3. **每个空间拍都是一次"重新排布空间"的机会。** 拍越多，模型重新摆放人物和背景的次数越多，累积漂移越大。打击拍发生在原地，不改变相对站位，所以可以密（R4）。
4. **逐镜独立生成天生不连续。** 空间相连的 100 对镜头里，只有 26 对背景一致〔外部调研·S-PIPE-08〕；只给角色图和地点图独立生成时，和上一镜尾帧的相似度只有 0.01–0.41〔外部调研·S-PIPE-03〕。用上一段真实尾帧作参考时，开场 NCC 是 0.91–0.99〔外部调研·F-ZEN-14〕。相邻镜的空间连续靠**共享已过关的图**，不靠文字。
5. **竖屏放大了这个问题。** 9:16 的横向很窄，左右调度本来就没有空间（[`10-theory/01-vertical-drama-physiology.md`](01-vertical-drama-physiology.md) T01.7）；纵深分层（前景、主体、背景）是竖屏组织空间的主轴〔外部调研·S-ZEN-22〕。
6. **矛盾不只出现在方位词上。** 其他同类矛盾包括：声明了慢动作又写实时速度句；运镜镜里写 "holds one single pose completely rigid"，运镜位移从 98–108% 画宽掉到 22%〔外部调研·F-H3-15〕。所以审计的对象是全部指令之间的一致性〔委托方实证·A5④〕，方位词只是其中最高发的一类。

## 本管线下的变体

### 设计顺序（病灶在预制作，不在提示词）

1. **场地图**：每场戏先画俯视站位（文字表格就够：谁在哪、门和障碍物在哪、轴线画在哪），声明本场的轴线侧。
2. **场景板**：Qwen 出一张锁定布局的场景板（建议是能看清全场地理的中远景），多 seed 抽卡后逐元素核对场地图〔委托方实证·P2〕。
3. **关键帧**：每镜的起始帧都从同一场景板和角色板派生，分镜 `起始帧方位` 写成 `神=LEFT; 苏晓=RIGHT`，冻结后不改〔委托方实证·P3〕。
4. **链式参考**：送视频时同时挂角色板和同场已通过的关键帧〔委托方实证·P5、M7〕。动作连续的相邻镜，用上一镜尾段的姿态作下一镜起始帧的依据（[`10-theory/04-action-design.md`](04-action-design.md)）。
5. **提示词**：元数据写 `起始帧方位`、`轴线策略: 单轴定侧`、`角色映射: S1=苏晓; S2=神`，主体定义里用画面位置称呼。
6. **审计**：`direction_audit.py video-prompts.md --storyboard storyboard.md`，最后一行必须是「方位词审计：通过（0 处矛盾）」。

### `direction_audit.py` 规则码 → 处置

| 规则码 | 指的是什么 | 处置 |
|---|---|---|
| `DIR-camera` | 相机的左右维度运动（truck / arc / orbit / weave / pan / circle…） | 单轴定侧下是 error：删掉，改成 push-in / pull-back / tilt up / crane up |
| `DIR-side` | 附着在主体上的 LEFT/RIGHT 与起始帧方位矛盾 | 让文字服从起始帧 |
| `DIR-path` | 主体路径词（behind / around / flank / sidestep / 绕到身后 / 换边） | 改成同侧直线进退，或者拆新镜 |
| `DIR-check` | turn / toward / front / 角色自身的左右手 / 台词里的方位词 | 打开起始帧逐处目视核对 |
| `DIR-layout` | 分镜和提示词的 `起始帧方位` 不一致 | 双文档对账，改到一致〔委托方实证·P7〕 |
| `DIR-mapping` | ≥2 人却缺 `角色映射` | 补上映射，否则审计无法对齐 |
| `DIR-axis` | 有人物却没有声明 `轴线策略`，或者取值不认识 | 补上 `单轴定侧` 或 `换边`（附理由） |
| `DIR-negated` | 方位词出现在否定句里（never trucks / 不绕） | 记为 info，不算矛盾；但这类否定句本身不能代替删词 |

### 多人与对白场的空间写法

- 多人同框只做一两个中景交代关系；台词一律用单人正反打，单人机位放在"听的人"的视线上〔外部调研·S-H3-09〕。
- 反打前补约 1.5 秒双人引子，后期丢掉〔外部调研·S-H3-09〕。
- 视线：高个子往下看、矮个子往上看，视线方向留出看的空间〔外部调研·S-STORY-11〕。
- 说话对象的视线偏离镜头轴 25–40° 显得自然，小于 15° 就像在看观众〔外部调研·S-H3-09〕。单人镜的机位按这个角度放，不要让人物直视镜头。
- 每场维护一本连续性账本，逐镜记录：身份、服装、手持物、轴线在哪一侧、屏幕方向、光的方向与色温、起止姿态〔外部调研·S-H3-10〕。相邻镜逐项对账，有一项不一致，就删镜或只改这一个变量。
- 2:3 板图直接送 first_frame 会被拉伸，几何关系随之失真〔外部调研·S-H3-03〕，所以关键帧必须是 9:16。

## 常见误用

| 误用 | 症状 | 案例 |
|---|---|---|
| 起始帧钉了左右，提示词又写换边运镜 | 人物乱跑，「又变成苏晓乱跑……」 | [`60-casebook/cards/A5-spatial-chaos.md`](../60-casebook/cards/A5-spatial-chaos.md) |
| 为了"有运镜"套用 truck、arc 原语 | 修好 A4，又把 A5 带回来 | [`60-casebook/cards/A4-unmotivated-camera.md`](../60-casebook/cards/A4-unmotivated-camera.md)、[`60-casebook/cards/F3-patch-iteration.md`](../60-casebook/cards/F3-patch-iteration.md) |
| 用更多方位词去"描述清楚"空间 | 方位词越多，矛盾越多 | [`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) 病灶路由表 |
| 打斗里塞进重复接近、翻滚、换向 | 空间连续跳变 | A5③ |
| 左右臂、朝向这类属性看一眼整体就放行 | 方位反了却通过验收 | [`60-casebook/cards/C1-banned-items-violated.md`](../60-casebook/cards/C1-banned-items-violated.md)、[`60-casebook/cards/C2-lenient-acceptance.md`](../60-casebook/cards/C2-lenient-acceptance.md) |
| 把 2:3 板图直接当起始帧送 H3 | 画面被拉伸，几何关系失真 | [`10-theory/01-vertical-drama-physiology.md`](01-vertical-drama-physiology.md) T01.9 |
| 相邻镜各自从文字重建场地 | 背景和站位每切一次都变 | [`60-casebook/cards/B1-character-drift.md`](../60-casebook/cards/B1-character-drift.md)（链式参考） |

对应找错题：DR-05（空间混乱）、DR-04（运镜脱钩）、DR-20（综合复盘）。

## → 行为改变

- 下次拆一场戏的分镜之前，**先**写场地站位表和轴线侧，**再**出场景板；**禁止**把空间留到视频提示词里用文字去描述。
- 下次填分镜时，每个有人物的镜都**必须**填 `起始帧方位`（大写 LEFT / RIGHT / CENTER / FG / BG），`拍数` 只计空间拍和表情拍；空间拍超过 3 个，就拆段（R-SB-06、R-SB-11）。
- 下次写多人镜的提示词，**改为**用画面位置称呼加 `角色映射`，**禁止**只写名字。
- 下次提示词定稿之前，**先**跑 `direction_audit.py`（带 `--storyboard`）；有一处矛盾就不进 prepare。
- 下次确实需要换边时，**先**出支持换边的新起始帧，用三种合法越轴方式之一，写清 `换边` 元数据；**禁止**在单次生成里靠 arc 或 orbit "转过去"。
- 下次收到"乱跑""位置混乱"一类反馈时，**改为**回到分镜和起始帧去修（[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) 病灶路由表），**禁止**在视频提示词里加更多方位词。
- 下次验收视频时，**先**看接触表首、中、末三格，逐人核对左右位置，再看别的（R-VID-14）；冷观众测试时问"谁在哪一侧、谁在追谁"。

相关：[`20-craft/storyboard-long-take/SKILL.md`](../20-craft/storyboard-long-take/SKILL.md)、[`20-craft/keyframe-freeze/SKILL.md`](../20-craft/keyframe-freeze/SKILL.md)、[`20-craft/video-prompting-h3/SKILL.md`](../20-craft/video-prompting-h3/SKILL.md)、[`20-craft/shot-qc/SKILL.md`](../20-craft/shot-qc/SKILL.md)、[`50-rubrics/checklists/storyboard.md`](../50-rubrics/checklists/storyboard.md)、[`10-theory/02-film-language-for-generators.md`](02-film-language-for-generators.md)、[`10-theory/07-asset-pipeline.md`](07-asset-pipeline.md)。

## 自测

1. 是非：只要提示词把每个人的位置都写得足够详细（"苏晓在神的右侧两米处"），就能纠正起始帧的布局。
<details><summary>答案</summary>错。文字写的空间地图压不过场景图（F-H3-21），左右关系由起始帧钉死（A5①、P4）。要改布局，就重出起始帧。写得越多，矛盾越多。</details>

2. 简答：`direction_audit.py` 对 `the camera arcs around the god` 报了 `DIR-camera` error，应该怎么处置？
<details><summary>答案</summary>单轴定侧下，删掉 arc，改成高度或距离维度的运动（push-in、tilt up、crane up）。如果设计上确实需要换边：出支持换边的新起始帧，元数据写 `轴线策略: 换边` 和 `- 换边: 设计（理由…；起始帧支持证据…）`，再用合法的越轴方式。</details>

3. 简答：一镜写了"苏晓连出 6 拳 → 神格挡 → 苏晓后撤翻滚 → 绕到神身后 → 再冲上来"，问题在哪？
<details><summary>答案</summary>6 拳加格挡是原地的打击拍，可以密（R4）；问题在"后撤翻滚、绕到身后、再冲上来"，这是 3 个空间拍，其中"绕到身后"还是换边路径（`DIR-path`）。改法：一镜只打"原地交手 + 一次直线退开"，绕后拆成新段，配新起始帧。</details>

4. 是非：Murch 把三维空间排在最后，所以只要情绪到位，越轴可以放过。
<details><summary>答案</summary>错。在 AI 生成里，空间错误是独立闸门（R7）：越轴和乱跑会直接摧毁"故事看得懂"，也是 Q2 的阻断缺陷。</details>

5. 简答：为什么建议相邻的动作镜把上一镜尾段的姿态作为下一镜起始帧的依据？
<details><summary>答案</summary>独立生成的镜头和上一镜尾帧几乎不连续（NCC 0.01–0.41，S-PIPE-03）；用真实尾帧作参考时，开场 NCC 是 0.91–0.99（F-ZEN-14）。共享图像比文字更能保住站位和背景的连续。</details>
