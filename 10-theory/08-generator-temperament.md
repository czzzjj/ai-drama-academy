# 08 · 生成器脾性：它会做什么、不会做什么

> 一句话世界模型：生成器不是执行者，而是带着默认偏好的条件采样器：只听正向条件，会照训练分布补东西（文字、装饰、配乐、慢动作），守不住纯色、精确文字和精确时刻；agent 的工作是用结构让错误不可能发生，而不是靠祈使句求它别犯错 ｜ 浓缩案例：C1, D1, D2, D3, D4, D5, A3, B2, B3, M3, M8 ｜ 对应技能：video-prompting-h3, keyframe-freeze, asset-boards, shot-qc

## 核心判决

**T08.1 · cfg=1 时 negative_prompt 在机制上不起作用：禁止填写该字段，也禁止因为填了它就认为"已处理"。**
为什么：ComfyUI 在 cond_scale≈1 时把无条件分支置为 None、不计算；CFG 公式 uncond + (cond − uncond)·scale 在 scale=1 时就等于纯条件预测〔外部调研·S-COMFY-05〕。Qwen 官方模板原文："At cfg 1 ComfyUI skips the negative conditioning pass"〔外部调研·S-COMFY-03〕；diffusers 在 true_cfg_scale ≤1 时同样忽略 negative〔外部调研·S-COMFY-06〕；H3 模板走 BasicGuider，本来就没有负向分支〔外部调研·S-COMFY-08〕。委托方 T-2 的判断在机制层面成立〔委托方实证·T-2、C1〕（R-VP-11）。

**T08.2 · 正向优先（R1）：先写正向可见状态句；只对已证实会被自行添加的物件追加绝对否定句；每条新否定句都要做 A/B（≥3 seed）。禁止只写否定句。**
为什么：官方和社区的结论是一致的："Write bans as positives"，点名不要的东西可能反而把它登记成内容〔外部调研·S-COMFY-08〕；Runway 不支持否定句，可能得到相反结果〔外部调研·S-VGEN-05〕；Veo 建议把排除改写成正向描述〔外部调研·S-VGEN-02、S-VGEN-03〕。反例也存在：`No dialogue` 8/8 未出台词〔外部调研·S-ZEN-17〕，Seedance 2.5 对字幕和 BGM 支持否定〔外部调研·S-VGEN-12〕，委托方的绝对否定句也确实修掉了问题〔委托方实证·C1、B3〕。证据冲突，所以学院不选边，只规定写法顺序和验证方法（R-VP-10、R-BRD-12、R-BRD-13）。

**T08.3 · 生成器会自行添加东西：提到的会长出来，没提到的也会按训练分布补上。** 对策依次是结构、多 seed、放大验收，最后才是措辞。
为什么：护手被加了蓝宝石、阿姆被加了全套铠甲、巴哈被加了金色颈饰、湖后多了远山、石碑多了刻纹、三人镜多了光柱〔委托方实证·C1-1 – C1-5、B3〕；"远处人群低语"被扩写成一群持发光平板的人〔委托方实证·B2〕。社区实测"提到什么就长什么"，共用段里写的服装、灯具会出现在每一颗镜头里〔外部调研·S-H3-09〕；"Structure beats instruction"，能用构图让错误不可能发生，就别用文字去禁止〔外部调研·S-H3-11〕。

**T08.4 · 竖屏更容易自动出字幕。禁令末行必须保留，但它只是兜底，烧录文字永远由抽帧 + OCR 把关。**
为什么：委托方在某段视频里遇到过生成器自行烧录字幕〔委托方实证·D1〕；Seedance 官方称竖屏出字幕的概率"significantly"高于横屏，且无法 100% 避免〔外部调研·S-VGEN-11〕；H3 讨论区有"无故出字幕"的报告〔外部调研·S-H3-13〕；Veo 3 也出现过同类事件〔外部调研·S-VGEN-04〕（R-VP-02、R-VID-06、R-VID-07）。

**T08.5 · 纯色画面、精确文字、UI、logo、屏幕内容一律不交给生成器。**
为什么：片尾纯黑字卡送进 H3 后，中段帧被自行加上了"LAVCE"水印〔委托方实证·D2〕；屏幕"只给亮度，不给内容"，精确文字和停顿定格不交给 H3〔外部调研·S-H3-09〕；输入图里有字，视频里就会有字〔外部调研·S-VGEN-08〕（R-VP-13、R-CUT-09）。

**T08.6 · 写事件，不写形容词。** 评价词（epic、spectacular、cinematic、史诗、华丽）不会被渲染；效果要写成"能量从哪来 → 在哪接触 → 怎么扩散 → 留下什么后果"。
为什么："冲击环从接触点炸开" 好过 "特效华丽"〔委托方实证·M3、G5〕；直接要求 motion blur 不会产生动态模糊，写明落点后 whip pan 的单步位移从 23 升到 218 px/step〔外部调研·S-H3-08〕；`motion blur`、`particle trails` 要改写成因果（袖子被甩直、沙被刀风扫平）〔外部调研·S-H3-09〕；fanatical、extremely shocked 这类强情绪词会让瞳孔发光〔外部调研·S-VGEN-12〕（R-VP-16）。

**T08.7 · 对白容量用两个速率（R3）：7.5 字/秒是硬上限（超过 = error，结构性缺陷）；约 4.1 字/秒是规划语速（超过 = warn，会赶词）。**
为什么：委托方在超容量的镜上换 3 个 seed，每次缺的句子都不一样，换 seed 无解〔委托方实证·D3、P9〕；自然语速约 4.1 字/秒，对白镜比计划长 1.5–2.5s〔外部调研·S-ZEN-17〕。另外，说话节奏绑在 seed 上：同 seed 换提示词，Whisper 逐字时间完全一致〔外部调研·S-H3-09〕。判别法：**容量够、单个 seed 缺句 → 先换 seed；换 2–3 个 seed 仍缺（或每个 seed 缺不同的句）→ 结构性缺陷，改时长或删句**（R-VID-12、R-SB-14）。

**T08.8 · 慢动作是默认偏差，"慢"必须是设计选择。** 动作镜写 `Real-time speed throughout, no slow motion`，并按真实事件时长排动作。
为什么：「几个简单动作的慢镜头」〔委托方实证·A3〕。扩散模型偏好帧间变化小的输出，因为这样更容易保持时序一致；速度描述含糊时，它几乎总选更慢的那个〔外部调研·S-VGEN-19〕。H3 把时长当成事件速度执行，1.5s 的摔倒像在月球上〔外部调研·S-H3-11〕；Seedance 官方甚至建议优先用慢、轻的小动作〔外部调研·S-VGEN-11〕（R-VP-03、R-SB-19、R-VID-15）。

**T08.9 · 片尾会崩解：每镜加 1.3–1.5s 尾部余量，剪辑时裁掉。**
为什么：H3 常在片尾前 1.2–1.7s 崩成噪声色块〔外部调研·S-H3-09〕；委托方的视频验收把"尾部无崩解"列为固定检查项〔委托方实证·P8〕。Sage Attention 的 INT8 量化也可能导致片尾形变和乱码文字〔外部调研·S-H3-04〕（R-VP-22、R-CUT-13、R-VID-03）。

**T08.10 · 不写声音字段不等于静音。** 无配乐的镜必须显式写 `non_diegetic_music: N/A`，整场配乐在后期统一铺。
为什么："Unwritten audio isn't silence"，模型会自配泛用音乐〔外部调研·S-H3-11〕；显式写 N/A 的 14 次都没有配乐，省略的 3 次中有 2 次出了配乐〔外部调研·S-ZEN-17〕。Seedance 1.5 Pro 和万相同样默认自配背景音乐〔外部调研·S-VGEN-21、S-VGEN-13〕（R-VP-19、R-SND-06）。

**T08.11 · QC 工具也会编造：单一通道的结论不算结论。**
为什么：无对白镜被转写成"字幕by索兰娅"，尾段低笑被单次转写误听为"救我"〔委托方实证·D5〕。这类幻觉有公开数据集可查〔外部调研·S-COMFY-16〕；Whisper 只在 no_speech_prob>0.6 **且** avg_logprob ≤ -1.0 时才跳过静音段，置信度高的背诵式幻觉拦不住〔外部调研·S-COMFY-14〕；非语音音频本身就会诱发幻觉〔外部调研·S-COMFY-17〕（R-VID-10、R-VID-11）。

**T08.12 · 精确时刻、精确数量、比例分数、"完全不动"都不要写给生成器：生成器只接收顺序和可见关系，时刻在剪辑里定。**
为什么：要求 3.0s / 4.0s 揭示，两次都在 2.46s 发生；"holds one single pose completely rigid" 让整镜运镜从 98–108% 画宽降到 22%〔外部调研·S-H3-08〕；`two thirds as tall as the frame` 这类分数被忽略，实测只到 45–52%〔外部调研·S-H3-09〕；精确时间提示普遍不稳定〔外部调研·S-VGEN-11、S-VGEN-07〕；视频模型对数字不敏感（F-VGEN-29）。

## 机制解释

1. **只有条件分支。** CFG 蒸馏或 cfg=1 的采样只沿着"正向条件"走，提示词里出现的每个名词都在给那个概念加权，包括 `no` 后面的那个名词（T08.1–T08.3）。所以"不要什么"最可靠的写法，是把那块区域写成另一件确定的事：`the sword guard is plain polished steel`、`the sign above the door is blank`。
2. **训练分布会补全空白。** 训练视频大量自带字幕、水印、配乐和装饰。学者把 Veo 3 的乱码字幕归因于训练数据自带字幕，并指出负向提示通常弱于正向提示〔外部调研·S-VGEN-04〕。提示词没有占住的维度（声音、配饰、背景人物），模型就按分布的众数去填。
3. **时序一致性偏好慢。** 帧间变化越小，时序越容易一致，所以速度描述一含糊就向慢靠拢（T08.8）。把一个事件给得太长，也是在告诉模型"慢一点"。
4. **全局条件、全局响应。** 运镜、风格、说话节奏都作用于整次生成：运镜无法分段指定〔外部调研·S-H3-09〕；说话节奏由 seed 的噪声决定，不由措辞决定。所以这几类问题的修复手段是"拆镜"或"换 seed"，不是"加词"。
5. **没有提示词改写器。** 开源的只有 H3-Base，Context-IR 和 Regenerate-2K 不在其中；官方称 Context-IR "critical to the quality of the final output"〔外部调研·S-H3-02〕。agent 自己要承担结构化扩写这一步，不能只喂一句短提示。

### 跨生成器交叉验证

| 脾性 | 委托方实证 | H3 官方 / 社区 | 其他生成器 | 学院立场 |
|---|---|---|---|---|
| 否定句 / 负向分支 | C1、T-2 | S-COMFY-08、S-H3-04（BasicGuider 无负向） | Runway 不支持〔S-VGEN-05〕；Veo 把排除放进负向字段〔S-VGEN-03〕；Seedance 2.5 支持字幕和 BGM 的否定〔S-VGEN-12〕 | R1：正向优先，否定兜底，A/B 验证 |
| 自行出字幕、水印 | D1、D2 | S-H3-13 | Veo 3〔S-VGEN-04〕；Seedance 竖屏更高〔S-VGEN-11〕；可灵沿用输入图里的字〔S-VGEN-08〕 | 禁令末行 + 输入图无字 + OCR |
| 幻影物件、装饰 | C1-1 – C1-5、B3 光柱 | S-H3-09 | Runway：说了不要，仍"may include it anyway"〔S-VGEN-07〕 | 共用段只写每颗都成立的元素；光写方向，不写灯具 |
| 默认慢动作 | A3 | S-H3-11 | LTX〔S-VGEN-19〕；Seedance 偏好慢、轻〔S-VGEN-11〕；Sora 片段常是 50–75% 速度〔S-CASE-05〕 | Real-time 句 + 真实事件时长 |
| 自配音乐 | —（GAP-3） | S-H3-11、S-ZEN-17 | Seedance 1.5〔S-VGEN-21〕；万相〔S-VGEN-13〕 | `N/A` + 后期铺乐 |
| 对白容量 | D3（7.5 字/秒） | 4.1 字/秒〔S-ZEN-17〕；4.30 字/秒〔S-H3-09〕 | Sora：4s 容 1–2 句〔S-VGEN-01〕；可灵：对白用 10s〔S-VGEN-09〕 | R3 双速率 |
| 一镜一运镜 | A4、A5 | S-H3-10、S-H3-09 | Sora〔S-VGEN-01〕；Seedance〔S-VGEN-11〕 | R5 |
| 多视角参考 → 多个人 | B3 | S-H3-09 | Seedance〔S-VGEN-11〕；Luma〔S-VGEN-18〕 | 一图一人一脸 |
| 提示词偏离首帧 → 意外切镜或运动打架 | A5① | S-H3-08（首帧脚手架钉死起幅） | 可灵：偏离图像会触发切镜〔S-VGEN-10〕；Runway：图中隐含的运动线索会与提示词冲突〔S-VGEN-06〕 | 提示词不得与起始帧矛盾；方位审计 |

### 什么永远不交给生成器

| 不交给生成器 | 改由谁做 | 溯源 |
|---|---|---|
| 纯黑、纯白、纯色卡，片名卡，字卡 | 本地静帧生成，剪辑叠层（剪辑单 `local:`） | D2；R-CUT-09 |
| 字幕、精确文字、AI 标识文字、logo、UI 面板 | 后期叠层；标识按 GB 45438 参数程序化叠加 | D1、D2；S-PLAT-02 |
| 屏幕、招牌上的具体内容 | 生成只给亮度或空白表面，内容后期合成 | S-H3-09、S-COMFY-08 |
| <124 帧的镜 | 从长镜中剪出，或本地生成 | T-2、A1 |
| 精确事件时刻、停顿、定格 | 剪辑 | S-H3-08、S-H3-09 |
| 配乐（整场音乐结构） | 后期铺一条连续音轨，生成镜写 `N/A` | S-H3-11；R-SND-06 |
| 精确数量的人群、有独立脸的路人 | 人群写成大虚化暗形块；需要数量时少人 + 剪辑 | B2；F-VGEN-29 |
| 真人照片作身份参考 | 原创板图 | S-PLAT-09；R-BRD-17 |
| 符号的精确计数和形制 | 对抗约束 + 逐条计数验收；同镜 3 seed 仍错，改为后期合成〔学院推断·验证法：记录每个 seed 的错误变体，3/3 错即判定为结构性缺陷〕 | D4 |

## 本管线下的变体

- **H3 + ComfyUI**：BasicGuider（无负向），20 steps，res_multistep + simple〔外部调研·S-H3-04〕。委托方用 euler〔委托方实证·T-2〕；两者的差异没有官方对比，不要在同一轮测试里同时改采样器和提示词。turbo 只用于预览：4 步几乎压掉运镜，8 步时语音最弱〔外部调研·S-H3-04、S-H3-08〕（R-VP-23）。
- **Qwen-Image-2.1**：cfg 1，negative 无效〔外部调研·S-COMFY-03〕。官方 T2I 模板自带的示例提示词以 "Absolutely no text, ... no captions" 结尾，而同一模板又注明 cfg=1 时负向无效（F-COMFY-10）。**厂商示例不能当写法范本。**
- **H3 已知模型缺陷**：片头约 0.5s 会出现乱语或截断的人声；Ref2VA 对白场的环境声偏小〔外部调研·S-H3-13〕；多人镜里口型会落到画面最显眼的正脸上，要明写不说话者 `lips remain completely closed`，加句后从 1/3 正确提到 3/3〔外部调研·S-ZEN-17〕（R-VP-18、R-VID-13）；两个男声的区分度差〔外部调研·S-ZEN-17〕（R-SEA-14）。这些要记成模型缺陷单独检查，不要误判为提示词写错。
- **`<d>` 内只放台词**：提示词里描述"说话"的句子可能被念出来；台词后的空余时间要写成一件事（在等、在翻页），否则模型会用填充和重复来补时长〔外部调研·S-H3-09〕。`dialogue_capacity.py` 对 `<d>` 内的括号舞台提示报 `D3-d-stage`。
- **脚本对应**：`prompt_lint.py` 拦 `VP-ban`（禁令末行）、`VP-realtime`、`VP-generator-unsafe`、`VP-negative`、`VP-adjective`、`VP-light`、`VP-crowd`、`VP-music`；`burnin_text_scan.py` 拦 `D1-burnin-text`、`D2-watermark`；`transcript_reconcile.py` 报 `TR-hallucination`、`TR-unscripted`，报了先证伪工具。

## 常见误用

| 误用 | 后果 | 案例卡 |
|---|---|---|
| 把"不要宝石"写进 negative_prompt，然后认为已经处理 | 宝石照样出现，还制造"已处理"的错觉 | [`60-casebook/cards/C1-banned-items-violated.md`](../60-casebook/cards/C1-banned-items-violated.md) |
| 以为写了 `No captions...` 就一定没字幕，跳过抽帧 | 烧录文字流入成片 | [`60-casebook/cards/D1-burned-in-captions.md`](../60-casebook/cards/D1-burned-in-captions.md) |
| 片尾黑卡、字卡交给 H3 生成 | 出现水印、文字污染 | [`60-casebook/cards/D2-solid-black-fails.md`](../60-casebook/cards/D2-solid-black-fails.md) |
| 缺句就反复换 seed | 结构性缺陷，换多少 seed 都无解 | [`60-casebook/cards/D3-dialogue-capacity.md`](../60-casebook/cards/D3-dialogue-capacity.md) |
| 符号只重复写"正确描述" | 被画成十字，质感被画成霓虹 | [`60-casebook/cards/D4-symbol-errors.md`](../60-casebook/cards/D4-symbol-errors.md) |
| 相信单次转写的结果 | 幻听当成缺陷，或误判重出 | [`60-casebook/cards/D5-qc-tools-lie.md`](../60-casebook/cards/D5-qc-tools-lie.md) |
| 不写实时速度句 | 全片慢镜 | [`60-casebook/cards/A3-slow-motion-default.md`](../60-casebook/cards/A3-slow-motion-default.md) |
| 给人群写了动作和道具 | 人群被扩写、变形 | [`60-casebook/cards/B2-crowd-leak.md`](../60-casebook/cards/B2-crowd-leak.md) |
| 多人镜不写差异化句，光写成具体灯具 | 克隆脸，凭空多出光柱 | [`60-casebook/cards/B3-clone-faces.md`](../60-casebook/cards/B3-clone-faces.md) |

## → 行为改变

1. 下次想写"不要 X"，**先改写成"那里是什么"**（正向可见状态句）；只有 X 已被证实会被自行添加时，才在后面追加绝对否定句，并登记一次 3 seed 的 A/B。
2. 下次提示词或工作流里出现 `negative_prompt`，**删掉它**；发现了也不要当作已经处理。
3. 下次碰到纯色、字卡、精确文字、logo、UI、屏幕内容、片名或 AI 标识，**先查"不交给生成器"表**，直接在分镜里标为本地生成（R-SB-21）。
4. 下次写动作镜，**先写 `Real-time speed throughout, no slow motion`**，再按真实事件时长分配动作，余下时间给后果；需要慢镜时，在元数据里声明 `- 慢动作: 设计选择（理由）`。
5. 下次每个生成镜都**显式写 `non_diegetic_music: N/A`**，并加 1.3–1.5s 尾部余量；禁止依赖"没写就是没有"。
6. 下次遇到缺句，**先判随机还是结构**：容量核算通过时换 seed；换 2–3 个 seed 仍缺，就回到分镜改时长或删句，禁止继续抽卡。
7. 下次 QC 工具报出异常（转写有字、OCR 有字、PSNR 跳变），**先证伪工具**：用 ffprobe 确认有没有音轨，抽帧，听感，多窗口复核；两个通道一致才下结论。
8. 下次遇到抽象评价词（史诗、震撼、华丽），**改为拆成"起始帧可见属性 + 事件 + 后果 + 声音 + 节奏"**再分别落地，提示词里禁止出现未拆解的评价词。

## 自测

1. 判断：把 cfg 从 1.0 调到 1.05，negative_prompt 就能起作用了，所以 C1 的装饰物问题本质上是参数问题。
<details><summary>答案</summary>错，至少未经验证。cfg=1 时负向分支被跳过是事实（S-COMFY-05）；但 H3 模板走的是 BasicGuider，本来就没有负向分支（S-COMFY-08）；Qwen 文档写明调高 cfg 会带来边缘过锐、曝光偏移（S-COMFY-03）。改参数属于另一项实验，必须固定 seed、一次只改一个变量。在实验得出结论前，按 R1 用正向句 + 绝对否定句 + 多 seed + 放大验收。</details>

2. 简答：一镜 6s，两句台词合计 40 字，换了 3 个 seed，每次缺的句子都不一样。怎么判？
<details><summary>答案</summary>40 字 ÷ 7.5 字/秒 ≈ 5.3s，6s 镜扣掉表演留白和开口延迟后装不下，属于结构性缺陷（D3）；"每个 seed 缺不同的句"是典型症状。禁止继续换 seed：回到分镜延长时长（按 4.1 字/秒的规划语速约需 9.8s，再加余量后吸附网格），或者删句、把台词拆到听者镜（R-VID-12、R-SB-15）。对应找错题 DR-11。</details>

3. 简答：列出四件永远不交给 H3 的事，并各给出替代做法。
<details><summary>答案</summary>示例：① 纯色卡、片名卡 → 本地静帧 + 剪辑叠层（D2）；② 字幕、AI 标识文字 → 后期程序化叠加（D1、GB 45438）；③ 屏幕或招牌的具体内容 → 生成只给亮度或空白表面，内容后期合成（S-H3-09）；④ 精确时刻和定格 → 剪辑（S-H3-08）。另外可答：<124 帧的镜、整场配乐、有独立脸的人群、真人照片参考。</details>

4. 判断：无对白镜的转写出现"谢谢观看 下集再见"，说明模型自己加了台词，必须重出。
<details><summary>答案</summary>错。这句在 Whisper 喂纯噪声得到的公开幻觉数据集里（S-COMFY-16），属于工具幻觉的高发形态。先用 ffprobe 确认有没有音轨，再听感、抽帧看嘴型、多窗口复核；只有双通道都确认有人声，才判为生成缺陷（D5，R-VID-10）。对应找错题 DR-13。</details>

5. 简答：为什么"特效再华丽一点"在提示词里加 `spectacular, epic` 没有用？应该怎么写？
<details><summary>答案</summary>生成器渲染的是事件，不是评价（M3）；评价词不对应任何可见的变化，`prompt_lint` 会报 `VP-adjective`。改写成事件链：能量来源 → 接触点 → 扩散方式 → 环境后果，例如 "a ring of shockwave bursts outward from the point where the blade meets the stone, cracking the ground and lifting a wall of dust"。画面级的"史诗感"（尺度、机位、光）在关键帧这一层解决（M2）。</details>
