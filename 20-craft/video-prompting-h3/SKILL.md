---
name: video-prompting-h3
description: 为每镜写 MiniMax H3 视频提示词：先定模式再选方言（Ref2VA 六段 / FL2VA 三段），官方 12 类运镜写成自然句且一镜一个主运镜，写事件不写形容词，<d> 对白配稳定说话人 ID、非说话人写闭嘴句，禁令包末行 + 正向优先 + 符号对抗约束，用画面位置称呼人物、写差异化句、人群大虚化，定稿 20 步、留 1.3–1.5s 尾部余量、无配乐写 N/A、参考槽从 1 连续（起始帧在前、占位在末）；用 prompt_lint / direction_audit / slot_order_check / h3_frame_grid 验。Use when writing or fixing any H3 video prompt (video-prompts.md), or when a generated shot has captions, wrong mouth, clone faces, drift, slow motion or missing camera. 触发词：视频提示词、H3、六段、三段、Ref2VA、FL2VA、运镜词、对白标记、<d>、禁令包、闭嘴句、参考槽、尾部余量、步数、配乐 N/A、video prompt, MiniMax H3, camera primitives, ban pack, lip sync, reference order. 不负责起始帧构图（→ keyframe-freeze）、分镜运镜设计（→ storyboard-long-take）、生成后的镜头验收（→ shot-qc）。
---
# H3 视频提示词（video-prompting-h3）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。格式以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §2 为准；方言、禁用项、运镜立场见 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1、R2、R5。

## 何时用 / 何时不用
- **必须用**：关键帧 `qc/<SHOT>.md` 结论"通过"之后（R-KF-19）、prepare 之前；镜头 QC 判定"提示词层病灶"（字幕、口型、克隆脸、慢镜、方位词）时。
- **不用**：构图/越轴/压迫感问题（病灶在起始帧 → [`keyframe-freeze`](../keyframe-freeze/SKILL.md)）；台词装不下（病灶在剧本/分镜 → [`script-doctor`](../script-doctor/SKILL.md)）；纯色卡、字卡、logo、UI、字幕（永不送 H3，R-VP-13）。
- 判决："Structure beats instruction"——能用构图让错误不可能发生，就不靠提示词禁止〔外部调研·S-H3-11〕；提示词救不了起始帧〔委托方实证·M2〕。

## 输入 → 输出
- 输入：`storyboard.md`（时长、运镜、运镜因果、起始帧方位、对白）、`anchors.md`、定稿关键帧与板图、`action-design.md`。
- 输出：`season-01/ep03/video-prompts.md`（模板 [`70-playbooks/templates/video-prompt-h3.md`](../../70-playbooks/templates/video-prompt-h3.md)），每镜一节：

````markdown
## SHOT-004
- 时长: 12.33
- 帧数: 299
- 模式: Ref2VA
- 尾部余量: 1.50
- 步数: 20
- first_frame: REF-SHOT004-START
- references: 1=CHR-SUXIAO-BOARD; 2=CHR-GOD-BOARD; 3=REF-SHOT003-START
- 起始帧方位: 神=LEFT; 苏晓=RIGHT
- 轴线策略: 单轴定侧
- 锚点: CHR-SUXIAO; CHR-GOD
- 角色映射: S1=苏晓; S2=神

```h3
subject_definitions:
  [S1] the young swordswoman on the RIGHT — <CHR-SUXIAO 锚点句逐字> <Picture 1>
  [S2] the stone god on the LEFT — <CHR-GOD 锚点句逐字> <Picture 2>
  The two figures have clearly different faces, builds and silhouettes.
summary:
  On a moonlit ruined terrace, [S1] feints at [S2]'s shoulder, ducks his block and cuts his knee; he crashes down onto one knee.
retention_analysis:
  Keep the opening layout and the terrace of <Picture 3>: [S2] stays on the LEFT, [S1] stays on the RIGHT for the whole shot.
detailed_description:
  Real-time speed throughout, no slow motion. The camera slowly pushes in toward the two fighters.
  [S1] shouts: <d>[Chinese] 就是现在！</d> [S2] does not speak; his lips remain completely closed.
  [S1] lunges at [S2]'s right shoulder; [S2] swings his arm up to block and hits only air; [S1] drops low and slashes across his knee; sparks burst from the stone; the frame jolts as the blade hits the stone; [S2]'s knee buckles and slams into the flagstones, chips of rock scatter, then the dust hangs still.
  The distant crowd is a heavily blurred dark mass with no distinct faces.
overall_soundscape:
  Wind over stone, a sharp metallic crack on impact, rock chips clattering, heavy breathing.
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```
````

## 步骤
1. **定模式 → 定方言（R2）**：挂多张参考（起始帧 + 角色板 + 同场前镜关键帧，委托方链式参考 P5）= `模式: Ref2VA`，六段 `subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music`；只有首帧/首尾帧、不挂角色板 = `模式: FL2VA`，三段 `integrated_multimodal_description / overall_soundscape / non_diegetic_music`，首行写官方对齐句，且不写 `references`（互斥）〔外部调研·S-H3-01、S-H3-03、S-H3-05〕。段名顶格、顺序固定（R-VP-01）。
2. **参考顺序（E1）**：起始帧走 `first_frame`，必须是本镜自己的已验收 `REF-SHOTnnn-START`（`SLOT-first-frame`，T-3、P4）；`references` 编号从 1 起唯一连续（角色板在前、同场前镜关键帧在后）；`<Picture N>` 首次引用顺序升序且都已定义；预制作期占位槽**放末位**，删除后编号仍连续（R-VP-20）〔委托方实证·E1、T-3〕。一个角色只挂一张脸参考（几张脸 = 几个人〔外部调研·S-H3-09〕）。
3. **锚点句逐字**：`- 锚点:` 中每个资产的锚点句 EN 逐字进 `subject_definitions`（FL2VA 进 `integrated_multimodal_description`），R-VP-09〔委托方实证·P1〕。每个 `[S#]` 定义以**画面位置称呼**开头（`the god on the LEFT`，R-VP-07），并与 `角色映射`、`起始帧方位` 一致（R-VP-05）。
4. **差异化句与人群**：≥2 人写差异化句（`clearly different faces, builds and silhouettes`，R-VP-08）；人群写成大虚化、无独立可辨脸的暗形块，不给人群特征或道具（R-VP-15）〔委托方实证·B2、B3〕。
5. **一个主运镜，自然句（R5）**：官方运镜词表 12 类——Zoom In/Out、Push In/Pull Out、Pan、Truck、Tilt、Pedestal、Arc Shot、Tracking Shot、Static Shot、Shake Slightly/Strongly、POV、Roll〔外部调研·F-H3-01〕——一律写成自然英文句（`The camera slowly pushes in toward …`），不用方括号指令（那是旧 Hailuo 语法〔外部调研·F-H3-04〕）。每镜只写**一个**主运镜，属于高度或距离维度（R-VP-24）〔外部调研·S-H3-10〕；Truck/Arc 默认禁用，Pan 需声明换边（R-VP-04、R-VP-06）。顿挫写成事件引起的响应：`the frame jolts as the blade hits the stone`。不加 `with small amplitude`（实测基本无效〔外部调研·F-H3-12〕）。静止镜写 `static, on a tripod, with no camera movement whatsoever` 并有理由。
6. **首帧脚手架取舍**：`<Picture 1> is the first frame` / `[keyframe completion]` 会把运镜幅度约减半〔外部调研·S-H3-08〕。需要钉死轴线（A5）时用 `retention_analysis` 保留布局；需要明显运镜（A4）时删脚手架句，改用参考生成表述。
7. **写事件不写形容词**：`detailed_description` 用分号串联可见事件，按七相顺序（来自 action-design）；禁止 epic / spectacular / cinematic / stunning（R-VP-16）〔委托方实证·M3〕；特效写 来源 → 接触 → 扩散 → 后果。H3 只能排顺序、排不准时刻〔外部调研·F-H3-14〕——不写"在 3.0s 时"。不可能完成的指令（"完全僵住不动"）会拖垮整镜〔外部调研·F-H3-15〕，删掉。
8. **实时速度**：动作镜必含 `Real-time speed throughout, no slow motion`；豁免只有元数据 `- 慢动作: 设计选择（理由…）`（R-VP-03）〔委托方实证·A3〕。
9. **对白**：每句 `<d>[Chinese] 台词</d>` 同一行闭合，前文有稳定说话人 ID `[S1]`（R-VP-17）；台词逐字取自分镜 `对白`（P7）。≥2 个主体且有对白：每个不说话且脸可见的人写 `[S2] does not speak; his lips remain completely closed.`（R-VP-18）——实测不写时 3 次 2 次口型落错人，加句后 3/3〔外部调研·S-ZEN-17〕；或让其出画/背身。说话节奏绑在 seed 上而不是提示词上〔外部调研·F-H3-19〕：对白坏了换 seed 前先确认容量（D3）。
10. **禁令包（M8）+ 正向优先（R1）**：要锁的外观先写正向可见状态句（`the sword guard is plain polished steel, smooth and unadorned`），只对生成器已被证实会自加的物件追加绝对否定句（R-VP-10）；镜内不该出现的物件名一个都不写，光写成方向与色温，不写 flashlight / spotlight / god rays（R-VP-14）〔外部调研·S-COMFY-08、S-H3-09〕；不出现 `negative_prompt`（R-VP-11）。代码块最后一个非空行恰为 `No captions, subtitles, or dialogue text overlays appear at any moment.`（R-VP-02）〔委托方实证·D1〕——它是兜底不是保证，烧录文字由抽帧核验把关。
11. **符号对抗约束**：含 `SYM-*` 的镜把锚点卡禁用中的每个错误变体逐条写成计数/质感句（`exactly one vertical bar … no horizontal line, no cross sign`；`fire-textured, not smooth neon`），R-VP-12〔委托方实证·D4〕。
12. **声音字段**：`overall_soundscape` 只写画面内可见动作的声音；`non_diegetic_music:` 不得为空，无配乐写 `N/A`——不写 ≠ 静音，模型会自配泛用音乐（R-VP-19）〔外部调研·S-ZEN-09、S-H3-11〕；整场配乐后期铺（R-SND-06）。
13. **时长、帧数、尾部余量、步数**：`- 尾部余量: 1.3`–`1.5`，提示词 `时长` = 分镜 `时长(s)` + 余量（R-VP-22）〔外部调研·F-H3-18〕；帧数用 `python3 50-rubrics/scripts/h3_frame_grid.py --seconds 12.33` 吸附到 17k+5 网格（124–362，R-VP-21）。定稿 20 步、不挂 4-step turbo；≤8 步只用于预览抽卡并标"预览"（R-VP-23）——turbo 几乎完全压制运镜〔外部调研·F-H3-10、S-COMFY-09〕。
14. **送生成前四道脚本（全部 0 error）**：
    - `python3 50-rubrics/scripts/prompt_lint.py season-01/ep03/video-prompts.md --anchors season-01/ep03/anchors.md --storyboard season-01/ep03/storyboard.md`
    - `python3 50-rubrics/scripts/direction_audit.py season-01/ep03/video-prompts.md --storyboard season-01/ep03/storyboard.md`（每条 DIR-path warn 有处置，R-VP-06）
    - `python3 50-rubrics/scripts/slot_order_check.py season-01/ep03/video-prompts.md --simulate-remove-placeholder --assets-dir season-01/ep03/assets`
    - `python3 50-rubrics/scripts/h3_frame_grid.py --check season-01/ep03/video-prompts.md`；另跑 `dialogue_capacity.py --storyboard … --prompts …`（R-SB-24 双文档对齐）。
15. **回写**：产出与提示词不一致但被采用 → 把提示词回写成产出事实（R-VP-25、R-VID-18），否则下一轮会在错误的"事实"上迭代〔委托方实证·E4〕。

## 判据
- 视频提示词：R-VP-01 – R-VP-25 全部。
- 上下游：R-KF-19（放行前提）、R-SB-24（双文档对齐）、R-SND-06、R-VID-06、R-VID-13、R-VID-19、R-VID-22。
- Q 维度：Q2 空间与调度、Q3 动作与物理、Q7 一致性与连续性、Q8 声音与对白。

## 失败模式
- **成片出现烧录字幕** → [`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md)：防线 = 步骤 10 禁令包末行 + 不要求生成任何文字。
- **参考槽删占位后集体失败** → [`60-casebook/cards/E1-slot-order.md`](../../60-casebook/cards/E1-slot-order.md)：防线 = 步骤 2 占位在末 + `slot_order_check.py --simulate-remove-placeholder`。
- **人物乱跑、换边** → [`60-casebook/cards/A5-spatial-chaos.md`](../../60-casebook/cards/A5-spatial-chaos.md)：防线 = 步骤 3 画面位置称呼 + 步骤 5 禁左右运镜 + `direction_audit.py`。
- **慢动作** → [`60-casebook/cards/A3-slow-motion-default.md`](../../60-casebook/cards/A3-slow-motion-default.md)：防线 = 步骤 8 实时速度句 + 步骤 13 不用 turbo 定稿。
- **人群穿帮 / 克隆脸** → [`60-casebook/cards/B2-crowd-leak.md`](../../60-casebook/cards/B2-crowd-leak.md)、[`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)：防线 = 步骤 4。
- **台词缺句、口型落错人** → [`60-casebook/cards/D3-dialogue-capacity.md`](../../60-casebook/cards/D3-dialogue-capacity.md)：防线 = 步骤 9 闭嘴句 + 容量回剧本。
- **符号画错** → [`60-casebook/cards/D4-symbol-errors.md`](../../60-casebook/cards/D4-symbol-errors.md)：防线 = 步骤 11。
- **提示词与产出不一致** → [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)：防线 = 步骤 15 回写。
- **运镜被压没** → [`60-casebook/cards/A4-unmotivated-camera.md`](../../60-casebook/cards/A4-unmotivated-camera.md)：防线 = 步骤 6 脚手架取舍 + 步骤 13 20 步。

## 关联
- 理论：[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/02-film-language-for-generators.md`](../../10-theory/02-film-language-for-generators.md)、[`10-theory/03-spatial-staging.md`](../../10-theory/03-spatial-staging.md)、[`10-theory/11-sound-design.md`](../../10-theory/11-sound-design.md)。
- 好/坏样例：[`30-taste/pairs/generation-prompting.md`](../../30-taste/pairs/generation-prompting.md)；脚本说明 [`50-rubrics/scripts/README.md`](../../50-rubrics/scripts/README.md)。
- 相邻技能：[`keyframe-freeze`](../keyframe-freeze/SKILL.md)、[`storyboard-long-take`](../storyboard-long-take/SKILL.md)、[`action-choreography`](../action-choreography/SKILL.md)、[`casting-and-canon`](../casting-and-canon/SKILL.md)、`shot-qc`、`performance-direction`。
- 找错题：DR-03、DR-04、DR-05、DR-07、DR-10、DR-12、DR-14、DR-15。
- → 行为改变：下次 QC 发现问题想"再加一句提示词"前，先判断病灶是否在起始帧或分镜；是 → 回上游，不在本文件追加词。
