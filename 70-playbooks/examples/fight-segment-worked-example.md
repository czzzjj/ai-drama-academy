# 打斗段全流程示例：少女剑客 vs 石像守卫（12.25s，一镜一段）

> **用途**：给 agent 看"一场 12–15s 的 BOSS 战从分镜行走到 H3 提示词，每一步长什么样、过哪道脚本"。读完应能照抄结构、替换内容，并知道每一处写法对应哪条判据。
> **性质**：角色、数字、素材名全部是**学院虚构的通用示例**（不来自委托方证据）；规则出处写在各节末尾（[`action-choreography`](../../20-craft/action-choreography/SKILL.md)、[`keyframe-freeze`](../../20-craft/keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../../20-craft/video-prompting-h3/SKILL.md)、[`evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1/R4/R5）。格式以 [`format-contracts.md`](../format-contracts.md) 为准。
> **同一份内容的独立文件**（脚本直接吃这三份，本文 ①④⑤ 的内容与之逐字一致）：[`fight-segment/storyboard.md`](fight-segment/storyboard.md)、[`fight-segment/anchors.md`](fight-segment/anchors.md)、[`fight-segment/video-prompts.md`](fight-segment/video-prompts.md)。改例子时先改这三份，再跑 ⑥ 的命令，最后同步本文。

**场景**：森林空地。青岚（17 岁少女剑客，右手持单刃直刀）对石守（四倍人高的石像守卫，无武器）。本段 = `SEQ-04` = 一镜 `SHOT-012` = 一次 H3 生成；上一镜 `SHOT-011` 的起始帧作为第 3 张参考，保证空地一致（链式参考，P5）。

---

## ① 分镜行

| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |
|---|---|---|---|---|---|---|---|---|---|
| SEQ-04 | SHOT-012 | 12.25 | 3 | 青岚喊话并佯攻石守前臂→石守举臂过顶、重拳砸地落空，青岚直线后撤一步→青岚矮身切入横斩石膝，膝裂塌，石守单膝砸地，尘停，琥珀光明灭 | 缓推→接触瞬间顿挫 | 因为刀锋接触石膝，所以推近在接触帧顿住强调力量 | 石守=LEFT; 青岚=RIGHT | 青岚：来吧，大块头！ | — |

要点（每条都是"下次生成时的动作"）：

| 写法 | 为什么 | 判据 |
|---|---|---|
| 一段一镜、12.25s，不拆"出招镜 + 受击镜" | 出招与受击必须同镜同次生成；拆开会把接触帧落在剪点上，也会回到碎镜症（A1、A2） | R-SB-20 |
| `拍数` = 3，只数空间拍与表情拍：①对峙喊话 ②砸地与直线后撤 ③切入与倒地；打击拍（佯攻、砸、斩）写在 `内容` 的 `→` 链里，不计入 `拍数` | 打击拍可以密，空间拍要少（R4） | R-SB-06、R-SB-07 |
| `内容` 写事件不写形容词：谁做了什么、碰到什么、什么东西坏了 | M3；形容词（epic、powerful）没有可见事件可执行 | R-SB-17 |
| `运镜` 一条主运动（缓推，距离维度）；"顿挫"写成接触事件引起的响应 | 运镜是全局的、不能分段指定；一次生成一个主运镜（R5） | R-SB-10、R-VP-24 |
| `运镜因果` 用"因为 X，所以镜头 Y"，X 是接触帧这个可见事件 | A4：运镜必须挂在事件上，验收时才能在接触表里找到 X 与 Y | R-SB-09 |
| `起始帧方位` 用大写英文并写成画面坐标：`石守=LEFT; 青岚=RIGHT` | 全程单轴定侧；攻防只沿同侧直线进退（A5） | R-SB-11、R-SB-12 |
| `对白` 只有一句、5 字，`短镜理由` 写 `—`（12.25s 不是短镜） | 容量远低于上限（D3） | R-SB-14、R-SB-24 |

**帧网格（17k+5，24fps，124–362 帧）**：

| 量 | 秒 | 帧数 | 17k+5 | 用在哪 |
|---|---|---|---|---|
| 分镜 `时长(s)`（成片留用） | 12.25 | 294 | k=17 | `storyboard.md` |
| 提示词 `时长`（生成） | 13.67 | 328 | k=19 | `video-prompts.md` 的 `- 时长` / `- 帧数` |
| `尾部余量` | 1.42 | 34 | — | 提示词 `- 尾部余量`；剪辑时裁掉，保留前 294 帧 |

提示词时长 = 分镜时长 + 尾部余量（13.67 = 12.25 + 1.42，R-VP-22；H3 常在最后 1.2–1.7s 崩解，所以多生成再裁）。临时换算用 `python3 50-rubrics/scripts/h3_frame_grid.py --seconds 12.25`（输出 `294 帧（k=17）`）。

---

## ② 七相动作链 + 战术链

**战术链表**（每场一行，≥3 环，每环是"谁利用了什么"）：

| 场 | 战术链（≥3 环） | 交手回合所在镜 | 结果 |
|---|---|---|---|
| 场 4 | 诱敌（青岚喊话并佯攻石守前臂）→ 落空（石守举臂砸地，青岚已直线后撤一步）→ 抓隙（石守拳陷进裂地，青岚矮身从落下的前臂下切入）→ 击飞（横斩石膝，膝裂塌，石守单膝砸地） | SHOT-012（我攻→你挡/砸空→我变招，同框、同镜、同次生成） | 石守失去机动；青岚夺得主动 |

**七相表**（每次接触一行；"时长分配"按相写真实秒数，**多出来的时间全部给后果与静止**）：

| 镜 | 接触# | 意图 | 预备 | 发力 | 接触 | 反应 | 回收 | 后果 | 时长分配（意图/预备/发力/接触/反应/回收/后果） |
|---|---|---|---|---|---|---|---|---|---|
| SHOT-012 | 1 石守砸地（落空） | 石守要砸扁她 | 举拳过顶 | 拳头下砸 | 拳砸进她刚才站的地面，尘与碎石呈环状炸开 | 她已直线后撤一步；拳陷进裂地 | 石守想抽拳，被裂土卡住 | 尘环扩散后落定，空地中央留下一个坑 | 0.8 / 1.2 / 0.4 / 0.2 / 0.8 / 0.8 / 0.8 = **5.0s**（0.00–5.00） |
| SHOT-012 | 2 青岚斩膝（命中） | 她盯住石守的膝 | 矮身切入、刀后引 | 蹬地横斩 | 刀刃砍进石膝，火星与碎石迸出（镜头在此帧顿一下） | 膝裂开、弯折，上身前栽 | 她借反作用力后滑一步 | 石守单膝砸地、碎石弹起，尘停住，裂缝里的琥珀光闪两下 | 0.5 / 0.9 / 0.4 / 0.2 / 1.3 / 0.9 / 3.05 = **7.25s**（5.00–12.25） |

核对：5.0 + 7.25 = 12.25s，与 ① 的 `时长(s)` 一致。接触相 ≤0.2s（真实挥击），后果相最长（3.05s 的"尘停"）——重量落在"停"上，不落在"落"上（R-SB-19；〔外部调研·S-H3-11〕）。**速度层次** ≥2：爆（0.2s 的两次接触）/ 静（尘停 3s），全程实时，无慢动作（R-SB-18；〔委托方实证·A3〕）。

**与提示词的对应**：七相写进 `detailed_description` 的 `Beat 1/2/3`（⑤），`Beat` 数 = `拍数` = 3（`prompt_lint.py` 的 `VP-sync` 会核对）。起始帧取动作链起点（意图/预备相：石守垂臂、青岚低守），不取接触或后果相（R-KF-14）。

---

## ③ 9:16 关键帧冻结提示词（`REF-SHOT012-START`）

起始画面 = 接触#1 的意图相：石守双臂垂落、眼窝盯住她；青岚低守，刀后引。Qwen-Image 出 **1536×2752**（9:16），不用 2:3 原图（R-KF-02）。固定六行结构，每句一行、顺序固定：

```text
[1 风格锁] Grounded live-action wuxia look with matte textures and natural colour.
[2 构图] Vertical 9:16 frame, low camera at knee height, wide shot; the stone guardian fills the LEFT two-thirds of the frame and towers above the top edge, the swordswoman stands small in the lower RIGHT third.
[3 位置+锚点] On the LEFT, a towering stone guardian four times human height, body of weathered grey granite with faint amber light glowing in the cracks, a carved stern face with a closed stone mouth and two amber eye hollows, both arms hanging, amber eye hollows fixed on her. On the RIGHT, a slender 17-year-old Chinese swordswoman with a high black ponytail tied with a plain white cord, sharp dark eyes, wearing a fitted indigo cross-collar tunic with leather bracers, holding a single-edged straight dao in her right hand, knees bent, blade held low and back, eyes on the guardian's forearm.
[4 场景] A forest clearing of packed earth and flat stones ringed by dark tree trunks, a little mist hanging between them.
[5 光] Cold overcast daylight falls from the upper LEFT, hard contrast, palette of ash grey, moss green and indigo.
[6 差异/禁用] The two figures have clearly different faces, builds and silhouettes. The sword guard is plain polished steel, smooth and unadorned; the guardian's chest is bare weathered granite; no armor; no jewelry at all; no gemstone on the sword guard.
```

| 写法 | 为什么 | 判据 |
|---|---|---|
| 每个人物用**画面位置短语**开头（`On the LEFT` / `On the RIGHT`），写画面坐标，不写角色自己的左右 | 空间只能在图里定；位置词决定后面视频的左右（A5、M4） | R-KF-05、R-VP-07 |
| **一句构图**（[2]）：景别 + 机位高度 + 占画比例 + 分区；BOSS 压迫感由"占画高 ≥50%、顶出画框"这样可看的量保证 | 画面级属性由起始帧决定，不指望视频提示词补（P4、M2） | R-KF-08 |
| **一句光**（[5]）：方向 + 色温/对比 + 命名色，不写 flashlight / spotlight / god rays | 写出光源物件就会长出光源物件 | R-VP-14 |
| 锚点句 EN 逐字嵌入 [3]（与 ④ 一字不差，可用 `grep -F` 核对） | 跨镜一致性；改写 = 失效（P1） | R-KF-01 |
| **没有质量咒语**：不写 masterpiece / 8k / best quality / ultra detailed / epic / cinematic | 不携带信息，且形容词无可见事件可执行（M3） | R-VP-16 |
| 送 `first_frame` 前核尺寸：`ffprobe -v error -show_entries stream=width,height -of csv=p=0 assets/keyframes/REF-SHOT012-START.png` 应输出 `1536,2752` | 节点会把非 9:16 的首帧非等比拉伸 | R-KF-02 |

高风险镜（BOSS、打斗起幅）至少 3 个 seed 并排选优，落选版归档到 `assets/keyframes/_rejected/`（R-KF-03）；放大核验 `必现` / `禁用` 每一条（R-KF-04），再写 `qc/SHOT-012.md` 的关键帧一节，结论"通过"之后 ⑤ 才允许引用 `REF-SHOT012-START`（R-KF-19）。

---

## ④ 锚点卡

锚点卡是提示词里逐字复用的唯一事实来源。`禁用` 的写法 = **正向可见状态句在前，绝对否定句在后**（`negative_prompt` 在本管线 cfg=1.0 下无效；〔学院立场·evidence-reconciliation R1〕）：

````markdown
## ANCHOR: CHR-QINGLAN
- 类型: 角色
- 锚点句 EN: `a slender 17-year-old Chinese swordswoman with a high black ponytail tied with a plain white cord, sharp dark eyes, wearing a fitted indigo cross-collar tunic with leather bracers, holding a single-edged straight dao in her right hand`
- 必现: 高马尾 + 白色细绳；靛蓝交领短衣；皮护腕；右手持单刃直刀
- 禁用: the sword guard is plain polished steel, smooth and unadorned; no gemstone on the sword guard; no jewelry at all; no armor
- 方位属性: 刀在她自己的右手；她在画面右侧、面朝画面左（朝向石守），所以握刀手在远离镜头的一侧（关键帧需单独放大核验刀身仍可见）
- 来源依据: 示例设定（学院虚构）
- 板图: assets/boards/CHR-QINGLAN-BOARD.png（seed 3 定稿；落选 seed 1/2 归档于 assets/boards/_rejected/）

## ANCHOR: CHR-STONEWARDEN
- 类型: 角色
- 锚点句 EN: `a towering stone guardian four times human height, body of weathered grey granite with faint amber light glowing in the cracks, a carved stern face with a closed stone mouth and two amber eye hollows`
- 必现: 灰色风化花岗岩躯体；裂缝内琥珀色微光；刻出的严厉面孔 + 闭合石嘴 + 两个琥珀眼窝
- 禁用: the guardian's chest is bare weathered granite, smooth and unadorned; no armor; no weapon; no carved runes on the body
- 方位属性: —
- 来源依据: 示例设定（学院虚构）
- 板图: assets/boards/CHR-STONEWARDEN-BOARD.png（seed 2 定稿；落选 seed 1/3/4 归档于 assets/boards/_rejected/）
````

| 写法 | 判据 |
|---|---|
| `锚点句 EN` 一行、反引号包裹、不换行；所有提示词与冻结提示词逐字嵌入 | R-VP-09、R-KF-01 |
| `禁用` 第一项是正向句（`the sword guard is plain polished steel, smooth and unadorned`），后面才是 `no X` 绝对否定句；每项以 `;` 分隔，便于脚本逐条核对是否写进提示词 | R-VP-10、R-BRD-04 |
| 绝对否定句只给"生成器已被证实会自己加"的东西（本例假设板图阶段已见宝石、铠甲、刻纹被自动添加）；上线前用同镜 A/B 各 3 seed 验证"否定句本身没把 X 招进来" | R1 学院立场第 2 条 |
| `方位属性` 用画面坐标写持刀手所在侧，并注明关键帧要放大核验 | R-BRD-06、R-KF-04 |

---

## ⑤ H3 Ref2VA 视频提示词（`SHOT-012`）

````markdown
## SHOT-012
- 时长: 13.67
- 帧数: 328
- 模式: Ref2VA
- 尾部余量: 1.42
- 步数: 20
- first_frame: REF-SHOT012-START
- references: 1=CHR-QINGLAN-BOARD; 2=CHR-STONEWARDEN-BOARD; 3=REF-SHOT011-START
- 起始帧方位: 石守=LEFT; 青岚=RIGHT
- 轴线策略: 单轴定侧
- 锚点: CHR-QINGLAN; CHR-STONEWARDEN
- 角色映射: S1=青岚; S2=石守

```h3
subject_definitions:
  [S1] the swordswoman on the RIGHT: a slender 17-year-old Chinese swordswoman with a high black ponytail tied with a plain white cord, sharp dark eyes, wearing a fitted indigo cross-collar tunic with leather bracers, holding a single-edged straight dao in her right hand <Picture 1>
  [S2] the stone guardian on the LEFT: a towering stone guardian four times human height, body of weathered grey granite with faint amber light glowing in the cracks, a carved stern face with a closed stone mouth and two amber eye hollows <Picture 2>
  The two figures have clearly different faces, builds and silhouettes: one small human woman, one giant stone guardian.
summary:
  In the same forest clearing as <Picture 3>, the swordswoman on the RIGHT lures the stone guardian on the LEFT into a slam that misses, slips in under its arm and cuts its knee, and the guardian crashes down onto one knee.
retention_analysis:
  Keep the layout and the clearing of <Picture 3>: [S2] stays on the LEFT and [S1] stays on the RIGHT for the whole shot, and neither crosses to the other's side.
detailed_description:
  Real-time speed throughout, no slow motion. The camera slowly pushes in from a low wide angle; at the moment of contact the frame jolts as the blade hits the stone. The camera never moves sideways.
  Beat 1: [S1] shouts: <d>[Chinese] 来吧，大块头！</d> [S2] does not speak; its lips remain completely closed. [S1] steps in and feints a slash at the guardian's forearm.
  Beat 2: [S2] raises its fist overhead and slams it down onto the ground where she stood; a ring of dust and gravel bursts outward; [S1] has already stepped back one pace in a straight line, and the fist sinks into the cracked earth.
  Beat 3: [S1] drops low under the lowered arm and cuts across the guardian's knee; sparks and stone chips burst from the contact point; the knee cracks and buckles; [S2] slams down onto one knee, then the dust hangs still while amber light flickers in the cracks and [S1] holds her blade low.
  The sword guard is plain polished steel, smooth and unadorned; no gemstone on the sword guard; no jewelry at all; no armor. The guardian's chest is bare weathered granite, smooth and unadorned; no weapon; no carved runes on the body.
overall_soundscape:
  Forest wind, gravel under boots, a deep stone thud on the slam, a sharp crack of stone at contact, falling pebbles, her steady breathing.
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```
````

| 写法 | 为什么 | 判据 |
|---|---|---|
| 元数据：`模式: Ref2VA`（起始帧 + 两张角色板 + 前镜关键帧 = 多参考）；`references` 从 1 起连续，`<Picture 1/2/3>` 按首次出现顺序升序 | 参考槽顺序错 = 参考错位（E1） | R-VP-01、R-VP-20 |
| `轴线策略: 单轴定侧`：正文写"石守始终在左、青岚始终在右、互不越到对方一侧" | 越轴是视频级缺陷，只能在起始帧 + 提示词里预防（A5） | R-VP-04、R-VP-05 |
| `subject_definitions` 里两条锚点句 EN **逐字**粘贴，且以画面位置称呼开头（`the swordswoman on the RIGHT`） | P1；画面 ≥2 人用位置称呼 | R-VP-09、R-VP-07 |
| 紧跟一句**差异化句**：`clearly different faces, builds and silhouettes: one small human woman, one giant stone guardian` | 防克隆脸（B3） | R-VP-08 |
| `Real-time speed throughout, no slow motion.` 放在 `detailed_description` 首句；全文不出现肯定式的 slow motion | 慢动作是生成器默认偏差（A3） | R-VP-03 |
| 一个主运镜写成自然句（`slowly pushes in from a low wide angle`）；接触时的顿挫写成事件响应（`the frame jolts as the blade hits the stone`）；`never moves sideways` | 运镜全局、一镜一个（R5） | R-VP-24、R-SB-10 |
| `Beat 1/2/3` 按七相顺序用分号串联可见事件，不写形容词、不写"在 3.0s 时" | 事件不写形容词（M3）；H3 排得准顺序排不准时刻 | R-VP-16 |
| 台词 `<d>[Chinese] 来吧，大块头！</d>` 同一行闭合、前文有 `[S1]`；对白逐字取自分镜 `对白` | 三方对账（P7） | R-VP-17、R-SB-24 |
| 非说话人写闭嘴句：`[S2] does not speak; its lips remain completely closed.`（锚点里也写了 `closed stone mouth`） | 否则口型会落到错的人身上 | R-VP-18 |
| 外观锁：先正向句再绝对否定句（与 ④ 的 `禁用` 逐条一致）；不写 `negative_prompt`；光不写光源物件 | R1；C1 | R-VP-10、R-VP-11 |
| `non_diegetic_music:` 写 `N/A`（不写 ≠ 静音） | 否则模型自填配乐 | R-VP-19 |
| 最后一行恰为 `No captions, subtitles, or dialogue text overlays appear at any moment.` | 烧录字幕兜底（D1） | R-VP-02 |
| `- 时长: 13.67`（= 分镜 12.25 + 余量 1.42）、`- 帧数: 328`（17×19+5）、`- 步数: 20`（定稿不挂 turbo） | 帧网格与双文档对账 | R-VP-21、R-VP-22、R-VP-23 |

---

## ⑥ 检查命令与结果

全部在仓库根目录运行，对象是上面三份独立文件（先过设计层，再过提示词层；全部 0 error 才进 prepare）：

```bash
D=70-playbooks/examples/fight-segment
python3 50-rubrics/scripts/segment_rhythm.py $D/storyboard.md
python3 50-rubrics/scripts/dialogue_capacity.py --storyboard $D/storyboard.md --prompts $D/video-prompts.md
python3 50-rubrics/scripts/h3_frame_grid.py --check $D/video-prompts.md
python3 50-rubrics/scripts/prompt_lint.py $D/video-prompts.md --anchors $D/anchors.md --storyboard $D/storyboard.md
python3 50-rubrics/scripts/direction_audit.py $D/video-prompts.md --storyboard $D/storyboard.md
```

关键结果行（节选自实际输出；五个脚本退出码均为 0）：

```text
$ python3 50-rubrics/scripts/segment_rhythm.py $D/storyboard.md
ℹ️  A1-stats [全局]: 1 镜 / 1 段；总长 12.25s；均长 12.25s；有效拍数 3（14.7 拍/分钟）；短镜占比 0%
结果：通过（0 错误，0 警告，0 需目视）
(exit=0)

$ python3 50-rubrics/scripts/dialogue_capacity.py --storyboard $D/storyboard.md --prompts $D/video-prompts.md
ℹ️  D3-ok [SHOT-012 · storyboard.md:5 = video-prompts.md:3]: 需 1.67s / 时长 12.25s，利用率 14%（5 字÷7.5=0.67s + 停顿 0×0.6=0.00s + 换句 0×0.3=0.00s + 留白 1.00s = 1.67s）
结果：通过（0 错误，0 警告，0 需目视）
(exit=0)

$ python3 50-rubrics/scripts/h3_frame_grid.py --check $D/video-prompts.md
ℹ️  T2-ok [SHOT-012 · video-prompts.md:3]: 328 帧（k=19，13.67s），与时长 13.67s 一致
结果：通过（0 错误，0 警告，0 需目视）
(exit=0)

$ python3 50-rubrics/scripts/prompt_lint.py $D/video-prompts.md --anchors $D/anchors.md --storyboard $D/storyboard.md
  SHOT-012：通过（0 错误 / 0 警告）
结果：通过（0 错误，0 警告，0 需目视）
(exit=0)

$ python3 50-rubrics/scripts/direction_audit.py $D/video-prompts.md --storyboard $D/storyboard.md
👁  DIR-check [SHOT-012 video-prompts.md:18 subject_definitions]: 「right」角色自身左右 ≠ 画面左右 → 需目视：关键帧放大核验持物手/肢体方位（C1-6），与锚点卡 方位属性 一致
  SHOT-012：相机左右(a) 0 / 主体方位(b) 6 / 主体路径(c) 0 / 需目视(d) 1 / 否定 1 → 0 处矛盾
结果：通过（0 错误，0 警告，1 需目视）
方位词审计：通过（0 处矛盾）
(exit=0)
```

**读数**：0 error、0 warning。唯一需要人处理的是 `direction_audit.py` 的 1 条 `DIR-check`（`visual`）：锚点句里的 "her right hand" 是角色自己的右手，不是画面右——必须在关键帧上放大核验持刀手与 ④ 的 `方位属性` 一致，并在 ⑦ 的 QC 记录里写"已核"。`slot_order_check.py` 需要 `assets/` 目录与真实参考图，本例不跑；真实生产里改了 `references` 后必跑（`--simulate-remove-placeholder`）。

---

## ⑦ QC 记录骨架（`qc/SHOT-012.md`）

视频出片后才填；**骨架里没有任何"通过"**——每一行要有证据文件才能打勾（C2）。证据文件名按脚本实际产出命名（[`format-contracts.md` §6](../format-contracts.md)）：

```bash
mkdir -p qc/SHOT-012
python3 50-rubrics/scripts/contact_sheet.py SHOT-012.mp4 --keyframe assets/keyframes/REF-SHOT012-START.png --out-dir qc/SHOT-012
python3 50-rubrics/scripts/psnr_scan.py SHOT-012.mp4 --json > qc/SHOT-012/SHOT-012.psnr.json
python3 50-rubrics/scripts/burnin_text_scan.py SHOT-012.mp4 --out-dir qc/burnin
python3 50-rubrics/scripts/transcript_reconcile.py --storyboard 70-playbooks/examples/fight-segment/storyboard.md --prompts 70-playbooks/examples/fight-segment/video-prompts.md --transcripts qc/transcripts.tsv
```

```markdown
# QC SHOT-012 · seed <n> · <YYYY-MM-DD>
- 结论: <通过 / 不通过 / 有条件通过（条件…）>   <!-- 待填：下面每行都有证据才允许写结论 -->
- 生成日志: 模式 Ref2VA；seed <n>；steps 20；turbo 否；尾部余量 1.42s（裁到前 294 帧）
- 证据: qc/SHOT-012/SHOT-012.contact.jpg; qc/SHOT-012/SHOT-012.contact.json; qc/SHOT-012/SHOT-012.psnr.json; qc/SHOT-012/seeds.png
| 检查项 | 结果 | 证据 |
|---|---|---|
| R-VID-01 接触表含 FIRST / MID / TAIL（最后 0.5s），逐格结论 | 待填 | qc/SHOT-012/SHOT-012.contact.jpg |
| R-VID-02 背景元素清单（树干×?、碎石×?、雾）FIRST/MID/TAIL 计数无变化 | 待填 | 清单 + contact.jpg |
| R-VID-04 两个主体的脸部裁剪互不雷同（人脸 vs 石像面孔） | 待填 | SHOT-012.crop-face.jpg |
| R-VID-05 青岚脸与板图同尺寸并排是同一个人 | 待填 | kf-face-vs-board.png |
| R-VID-14 全程石守在画面左、青岚在画面右，无换边/绕行 | 待填 | contact.jpg 全格 |
| `DIR-check` 持刀手：青岚的刀在她自己的右手（画面中远离镜头一侧），与锚点卡 `方位属性` 一致 | 待填 | 放大裁剪 |
| R-VID-15 砸地、斩膝按实时速度发生，无漂浮式慢放 | 待填 | 动作区间每 0.25s 抽帧 |
| R-VID-17 接触帧可见刀刃砍进石膝，且推近在那一刻顿住（`运镜因果`） | 待填 | 接触三帧 |
| R-VID-06 无烧录文字/水印；`burnin_text_scan.py` 的每个 visual 已看 | 待填 | qc/burnin/*.burnin-strip.jpg |
| R-VID-22 `non_diegetic_music: N/A`，听感里没有配乐 | 待填 | 听感记录 |
| R-VID-21 画幅偏离 9:16 ≤2% | 待填 | contact_sheet 无 `T2-aspect` |
| R-VID-19 / R-VID-20 日志记模式、seed、steps；≥3 个 seed 并排选优，落选归档 | 待填 | 生成日志 + qc/SHOT-012/seeds.png |
- 复验人: <独立评审会话 / 日期>（BOSS 与打斗起幅属高风险，必填，C2）
```
