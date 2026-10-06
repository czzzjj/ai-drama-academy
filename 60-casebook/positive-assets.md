# 正面资产卡（P1–P10 · M1–M10）

> 委托方用真实生产与返工换来的正确做法〔委托方实证·P1–P10、M1–M10〕。**它们不需要重新发明，只需要被默认执行。**
> P = 具体做法（产线上的一道工序），M = 方法论（换题材、换模型仍成立的原则）。两者有重叠，M 卡只写 P 卡没写的部分，并指回对应 P 卡。
> 每张卡六栏：**是什么 / 为什么有效 / 证据 / 下次怎么用 / 谁来执法（技能·脚本规则代码） / 已知边界（外部调研）**。
> 读法：正面资产也有边界。"已知边界"一栏写的是外部调研发现的反作用或前提条件。装载后 agent 必须执行"怎么用"，同时守住"边界"。

---

## P · 具体做法

### P1 · 锚点卡系统
- **是什么**：每个角色/道具/场景/符号一张卡：`锚点句 EN`（逐字嵌入所有含该资产的提示词）+ 必现 + 禁用 + 方位属性 + 来源依据。格式见 [`70-playbooks/format-contracts.md`](../70-playbooks/format-contracts.md) §3。
- **为什么有效**：生成器跨镜没有记忆，每次只读得到这一条提示词的正文和这一组参考图；一致性只能靠"同一事实、同一措辞、每次都写"〔外部调研·S-ZEN-15〕。
- **证据**〔委托方实证·P1〕；反证是 C1 的 7 个子案：凡是锚点卡没写"禁用"的地方，生成器都自行加了东西（宝石、全套铠甲、金颈饰、远山、刻纹）〔C1-1…C1-5〕。
- **下次怎么用**：新资产先建卡再出图；卡里的必现/禁用就是验收逐项表的行。
- **执法**：[`casting-and-canon`](../20-craft/casting-and-canon/SKILL.md)；`prompt_lint.py` `VP-anchor`（锚点句逐字）、`VP-symbol`（符号禁用清单逐条入提示词）。
- **已知边界**：只给"跨 ≥2 镜出现、观众能看出不一致、不随剧情改变"的事实上锁，一集通常只有个位数〔外部调研·S-ZEN-15〕；锚点句会被生成器照字面渲染，"提到什么就长什么"〔外部调研·S-H3-09〕，所以锚点句只写本资产恒定可见的东西，状态（受伤、湿透）不写进锚点句。

### P2 · 板图多 seed 抽卡
- **是什么**：关键资产 ≥3 seed，逐特征对照锚点卡放大核验，选优定稿，落选归档。
- **为什么有效**：cfg=1.0 下 negative 无效〔T-2〕，生成器自行添加的东西只能靠"多个样本里挑"对抗；单张图无法区分"这次运气差"与"提示词有问题"。
- **证据**：C1-1 斩龙闪 3 seed 重抽；C1-6 尼加狄左右臂方位 3 seed 抽卡选出正确版〔委托方实证·P2、C1〕。
- **下次怎么用**：同一提示词的多个 seed 中，同一缺陷出现 ≥2 次 → 改提示词，不再加 seed（结构性缺陷，见 D3 的同构判断）。
- **执法**：[`asset-boards`](../20-craft/asset-boards/SKILL.md)；静帧放大用 ffmpeg `crop` + `scale=…:flags=neighbor` + `hstack` 留证据（见 [`60-casebook/cards/C2-lenient-acceptance.md`](cards/C2-lenient-acceptance.md)）。
- **已知边界**：1696×2528 是 Qwen-Image-2.1 官方 2:3 推荐尺寸，不是 9:16〔外部调研·S-COMFY-01〕；Qwen-Image-2.1 为研究许可，变现短剧需另签商业许可〔外部调研·S-COMFY-01、S-COMFY-02〕；模型自动选图只能做预筛，不能当终审〔外部调研·S-PIPE-05〕。

### P3 · 关键帧冻结
- **是什么**：每镜先写英文"冻结提示词"（起始画面的完整状态）→ 出关键帧 → 逐特征验收（发色/服装/标志物/禁用项）→ 不过关重出，**不放行到视频**。
- **为什么有效**：起始帧是视频的几何锚（见 P4）；关键帧上的错误会被视频忠实地继承 4–15 秒。在静帧上修，比在视频上修便宜一个数量级（[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) §4，〔学院推断〕）。
- **证据**〔委托方实证·P3〕。
- **下次怎么用**：冻结提示词验收通过后锁定，后续若产出与它不一致，回写提示词使二者为同一事实〔E4〕。
- **执法**：[`keyframe-freeze`](../20-craft/keyframe-freeze/SKILL.md)；`contact_sheet.py <clip> --keyframe REF-SHOTnnn-START.png`（`B4-keyframe` 并排比对）。
- **已知边界**：要送 first_frame 的关键帧用 9:16 官方尺寸 1536×2752，或送入前显式裁切〔外部调研·S-COMFY-01〕；ComfyUI 的 first_frame 是"plain stretch to canvas"，2:3 图送 9:16 画布会被挤压〔外部调研·S-H3-03〕。

### P4 · 起始帧驱动视频
- **是什么**：视频以关键帧为 first_frame（`REF-SHOTxxx-START`，顺序 1），方向/构图/灯光/角色形态全部由起始帧锚定。
- **为什么有效**：委托方实证"文字救不了构图，起始帧决定画面级"〔委托方实证·P4〕；外部同证：同 seed A/B，文字空间描述压不过场景图〔外部调研·S-H3-09〕。
- **证据**：P4、A5（起始帧钉死"神左/苏晓右"，文字换边运镜被模型搅乱）。
- **下次怎么用**：所有"画面级"诉求（史诗、方向、光、轴线）先落到关键帧，再写视频提示词；视频提示词只写运动与声音。
- **执法**：[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)；`slot_order_check.py` `SLOT-first-frame`；`prompt_lint.py` `VP-mode`、`VP-scaffold`；`direction_audit.py` `DIR-side`。
- **已知边界**：首帧脚手架句会把运镜幅度减半〔外部调研·S-H3-08〕；六段（Ref2VA）与三段（FL2VA）是不同模式，API 中首尾帧与 reference 互斥（[`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) R2）；从正面特写硬转到背面是"最常见的融脸方式"〔外部调研·S-H3-11〕。

### P5 · 链式参考
- **是什么**：送视频时同时挂"角色板 + 同场已通过的关键帧"（多图参考）。
- **为什么有效**：逐镜独立生成天然不连续：只给角色与地点图时，与上一镜尾帧的 NCC 仅 0.01–0.41〔外部调研·S-PIPE-03〕；同场已过关的关键帧把"这场戏长什么样"直接递给模型。
- **证据**：B1 角色漂移的修正之一〔委托方实证·P5、B1〕。
- **下次怎么用**：同一场的第 2 镜起，必须挂至少 1 张本场已通过关键帧；参考槽 1..N 连续，占位槽放末位〔E1〕。
- **执法**：[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)；`slot_order_check.py` `SLOT-contiguous`、`SLOT-placeholder-pos`、`SLOT-sim`；`prompt_lint.py` `VP-picture`。
- **已知边界**：几张脸 = 几个人——一人两张脸参考会被生成成两个人〔外部调研·S-H3-09〕；背景参考板使运镜约减半，换来场景漂移从 0.08 降到 0.02〔外部调研·S-H3-08〕；只从原始锚素材出发，不对 AI 生成素材做链式再生成〔外部调研·S-CASE-11〕。

### P6 · 三步闸门
- **是什么**：prepare（校验 + 预览）→ confirm（确认）→ run（真执行），所有生成不裸跑。
- **为什么有效**：把"提交错了"的成本从一次算力消耗降到一次预览；生成前的全部 `[自动]` 检查有了固定位置。
- **证据**〔委托方实证·P6、T-3〕。
- **下次怎么用**：生成前脚本（[`50-rubrics/scripts/README.md`](../50-rubrics/scripts/README.md) §5 第 1–6 步）全部 0 error 才进 prepare。
- **执法**：[`production-director`](../20-craft/production-director/SKILL.md)。
- **已知边界**：确认应绑定 job 指纹，job、提示词、参数、输出路径任一变化即失效〔外部调研·S-ZEN-10〕；闸门只防"误提交"，不证明质量〔F1、F2〕。

### P7 · 双文档对账
- **是什么**：分镜.md（蓝图）与视频提示词.md（指令）逐镜对齐；台词三方对账（剧本 ↔ 提示词 ↔ 转写）。
- **为什么有效**：两份文档各自正确、彼此矛盾，是生成器"乱编"的主要来源之一（A5④ 指令矛盾）；稳定 ID + 固定表头让对账可以机械执行〔外部调研·S-ZEN-13、S-ZEN-14〕。
- **证据**〔委托方实证·P7〕。
- **下次怎么用**：改任何一份，同一次提交里改另一份并重跑对账脚本。
- **执法**：[`edit-and-assemble`](../20-craft/edit-and-assemble/SKILL.md)、[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)；`dialogue_capacity.py` `P7-*`、`prompt_lint.py` `VP-sync`、`direction_audit.py` `DIR-layout`、`transcript_reconcile.py` `TR-script-prompt`、`TR-speaker`。
- **已知边界**：文档与产出也要对账——已验收产出与提示词不一致时回写提示词〔E4〕；文档说的做法与脚本实际行为也会分叉，而测试照样全绿〔外部调研·S-ZEN-18〕。

### P8 · 视频验收固定环节
- **是什么**：逐段抽帧（无烧录文字、无克隆、无穿模、尾部无崩解）+ 转写逐字对账 + PSNR 相邻帧扫描 + 成片切点逐帧目视。
- **为什么有效**：生成器的高频缺陷（加字、克隆、伪影、尾部崩解、缺句）都有可见或可测的痕迹，固定工序保证每镜都被同样地看过。
- **证据**〔委托方实证·P8〕；拦下过 D1 烧录字幕、B4 第二骨架。
- **下次怎么用**：按 [`50-rubrics/scripts/README.md`](../50-rubrics/scripts/README.md) §5 第 7–10 步执行；验收记录按 format-contracts §6 写，附证据文件。
- **执法**：[`shot-qc`](../20-craft/shot-qc/SKILL.md)；`contact_sheet.py`（`P8-contact-sheet`）、`psnr_scan.py`（`P8-freeze`、`P8-jump`）、`burnin_text_scan.py`（`D1-burnin-text`、`D2-watermark`）、`transcript_reconcile.py`（`TR-missing`）。
- **已知边界**：H3 常在片尾前 1.2–1.7s 崩成噪声色块 → 生成时加 1.3–1.5s 尾部余量、剪辑时裁掉〔外部调研·S-H3-09〕；ASR 在静音上会幻觉〔外部调研·S-COMFY-16、S-CASE-28〕；全部通过只证明 L0〔F2〕。

### P9 · 对白容量核算
- **是什么**：镜长 ≥ 台词字数 ÷ 7.5 字/秒 + 表演留白，在设计阶段核算。
- **为什么有效**：语速是物理约束，超容量就缺句，换 seed 无解〔委托方实证·D3〕。
- **证据**：同一镜 3 seed 各缺不同句；按"殇月句 4.34s + 一字一顿句 ~6.5s ≈ 10.3s"重算后，7.5s → 11s 重产才齐〔委托方实证·D3〕。
- **下次怎么用**：剧本定稿前就核算；按规划语速排时长，7.5 字/秒只当硬上限。
- **执法**：[`script-doctor`](../20-craft/script-doctor/SKILL.md)、[`storyboard-long-take`](../20-craft/storyboard-long-take/SKILL.md)；`dialogue_capacity.py` `D3-capacity`（error）、`D3-rushed`（warn）、`D3-margin`。
- **已知边界**：外部实测自然语速 ≈4.1 字/秒、对白镜实际比计划长 1.5–2.5s（开口延迟 + 说完）〔外部调研·S-ZEN-17〕；配音员实测 4.30 字/秒〔外部调研·S-H3-09〕。学院立场：7.5 = 容量上限，≈4.1 = 规划语速（evidence-reconciliation R3）。

### P10 · 长段多拍
- **是什么**：8–15s 段、段内 2–3 拍、一条完整动作链；连续动作不得切新镜。
- **为什么有效**：H3 单次可生成 124–362 帧（5.17–15.08s），<124 帧不可信〔T-2〕；一段承载一条因果链，观众才看得懂"谁做了什么、结果如何"。
- **证据**：实证自 r1–r5 实验〔委托方实证·P10〕；对照 A1 的 29 镜均长 2.96s。
- **下次怎么用**：分镜先按"段"设计，再拆拍；生成单位 ≥124 帧，快剪从长镜里取 CUT。
- **执法**：[`storyboard-long-take`](../20-craft/storyboard-long-take/SKILL.md)；`segment_rhythm.py` `A1-short-no-reason`、`A1-mean-short`、`A5-beats-many`、`T2-over-max`；`h3_frame_grid.py` `T2-frames-below-min`。
- **已知边界**：拍分三种——空间拍、表情拍 ≤2–3/镜，打击拍可以密（约 3 秒 8–9 招按序真速度打出）〔外部调研·S-H3-09；R4〕；短剪不是罪，剪辑单位可以很短〔外部调研·S-STORY-19；R6〕；H3 在大场面动作与肢体接触上较弱〔外部调研·S-CASE-10〕。

---

## M · 方法论

### M1 · 长段多拍（生成单位 ≠ 剪辑单位）
- **是什么**：做法见 P10。方法论要点：在"镜"之上必须有"段"这一设计层；**生成单位**按生成器的可靠区间定，**剪辑单位**按观众节奏定，两者分开设计。
- **为什么是方法**：A1 的病不是剪得快，而是把剪辑单位当成了生成单位〔委托方实证·A1；R6〕。
- **下次怎么用**：分镜表同时有 `段号` 与 `镜号`；剪辑单从同一镜取多个 CUT 是常态。
- **执法**：`segment_rhythm.py`（`P10-seq-missing`、`A1-mean-short`）。
- **已知边界**：外部节奏档案的平均镜长 2.5s 要靠长生成后剪辑实现，不能压成 2.5s 的生成单元〔外部调研·S-ZEN-21〕。

### M2 · 起始帧海报级
- **是什么**：画面级属性（史诗感/方向/构图/灯光）由起始帧决定，提示词救不了构图；起始帧按海报标准抽卡 + 验收〔委托方实证·M2〕。做法见 P3、P4。
- **为什么是方法**：它把 G5 的"史诗感不够"从"加形容词"改成"换起始帧"，即把修改送回正确的层〔G5〕。
- **下次怎么用**：遇到"不够史诗/不够大片"，先改起始帧（尺度参照、低机位、纵深、光），再动视频提示词。
- **执法**：[`keyframe-freeze`](../20-craft/keyframe-freeze/SKILL.md)；`prompt_lint.py` `VP-adjective`。
- **已知边界**："A shot that must end tight has to open wide"——推近镜的起幅要在主体最大的一端〔外部调研·S-H3-08〕；能靠构图让错误不可能发生的，就别用文字去禁止（"Structure beats instruction"）〔外部调研·S-H3-11〕。

### M3 · 写事件不写形容词
- **是什么**："冲击环从接触点炸开" > "特效华丽"〔委托方实证·M3〕。
- **为什么是方法**：生成器渲染的是可见事件，不是评价；评价词没有可渲染的对象。
- **下次怎么用**：提示词里的评价词（epic、spectacular、震撼、华丽）全部拆成"起始帧可见属性 + 事件 + 后果 + 声音 + 节奏"后删除〔G5〕。
- **执法**：[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)；`prompt_lint.py` `VP-adjective`、`VP-light`。
- **已知边界**：重量来自停顿而不是下落——"Weight comes from the stop, not the drop"，给一个摔倒 1.5s 就会变成慢动作〔外部调研·S-H3-11〕；事件里点名的物件会被画出来，光写成"暖光从一侧来"而不是"落地灯的光"〔外部调研·S-H3-09〕；用自带速度的动词（strides、darts、charges）对抗慢动作偏差〔外部调研·S-VGEN-19〕。

### M4 · 空间调度单轴定侧
- **是什么**：相机只动高度与距离；方位词全量审计；用画面位置称呼角色〔委托方实证·M4、A5〕。
- **为什么是方法**：它把空间从"文字描述"移到"起始帧 + 规则 + 审计"，r5 实测达标〔A5〕。
- **下次怎么用**：提示词定稿前必跑方位审计；换边只作为受控例外，写 `- 换边:` 理由 + 起始帧支持证据。
- **执法**：[`storyboard-long-take`](../20-craft/storyboard-long-take/SKILL.md)、[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)；`direction_audit.py`（`DIR-camera`、`DIR-side`、`DIR-path`、`DIR-layout`、`DIR-mapping`）；`prompt_lint.py` `VP-position`。
- **已知边界**：每次生成只有一个主运镜〔外部调研·S-H3-10；R5〕；180° 规则允许用弧形移动或角色走动越轴〔外部调研·S-STORY-08〕，所以"禁止换边"是本管线在起始帧驱动下的立场，不是电影通则。

### M5 · 对白容量核算（随机缺陷 vs 结构性缺陷）
- **是什么**：做法见 P9。方法论要点：**换 seed 无解的问题不是随机问题**，要改参数或改设计〔委托方实证·M5、D3〕。
- **为什么是方法**：这条判别适用于所有缺陷：同一缺陷在多个 seed 上复现 → 结构性。
- **下次怎么用**：任何缺陷第 2 次复现即停止重抽，回到病灶阶段（[`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) §3）。
- **执法**：`dialogue_capacity.py`；`transcript_reconcile.py` `TR-missing`（换 seed 仍缺 → 回分镜核算）。
- **已知边界**：外部同证"重抽只用于看起来随机的失败，且有上限；同一缺陷重复出现必须改结构"〔外部调研·S-ZEN-24〕。

### M6 · 锚点卡 + 多 seed 抽卡 + 逐特征放大验收
- **是什么**：关键资产三件套（P1 + P2 + C2 的放大验收）〔委托方实证·M6〕。
- **为什么是方法**：三件套分别对应"说清楚要什么 / 在随机性里挑 / 证明挑对了"，缺一件就会退化成 C1 或 C2。
- **下次怎么用**：高风险资产（主角/BOSS/核心道具）每条特征一张裁剪特写 + 一张与板图并排的对照图；方位、对比这类属性单独放大〔C1-6、C1-7〕。
- **执法**：[`asset-boards`](../20-craft/asset-boards/SKILL.md)、[`shot-qc`](../20-craft/shot-qc/SKILL.md)；`contact_sheet.py --crop`（`C2-crop`）；`asset_exists.py qc/`（证据文件存在且非空）。
- **已知边界**：cfg≈1 时无条件分支被跳过、negative 被忽略〔外部调研·S-COMFY-05、S-COMFY-06〕；先写正向可见状态句，再对已证实会被添加的物件追加绝对否定句，并用 ≥3 seed 验证否定句没有把它招进来（R1）；无法读取媒体时不得从文字推断脸是否一致〔外部调研·S-ZEN-12〕。

### M7 · 链式参考
- **是什么**：角色板 + 同场已过关键帧同送〔委托方实证·M7〕。做法见 P5。
- **为什么是方法**：一致性不是一次性设定，而是一条"已验收事实"的链：每个新镜都从上一个已验收事实出发。
- **下次怎么用**：先出建立镜（远景）关键帧，再从它派生中近景关键帧。
- **执法**：`slot_order_check.py`；`contact_sheet.py --keyframe`。
- **已知边界**：机位树——父机位内容要包含子机位，优先远→中→近，不从远景直跳特写〔外部调研·S-PIPE-05〕；链上只放已验收的原始锚素材，不对生成视频再换机位〔外部调研·S-CASE-11〕。

### M8 · 生成禁令包
- **是什么**：每镜固定附加约束：`No captions, subtitles, or dialogue text overlays appear at any moment.`、实时速度句、差异化句、绝对否定句；纯色卡交本地；符号写对抗约束〔委托方实证·M8、D1、D2、D4〕。
- **为什么是方法**：把"生成器已知会犯的错"变成每镜默认附带的条款，而不是出错后再补。
- **下次怎么用**：禁令句作为 h3 块最后一行；不该交给生成器的（纯色卡、精确文字、UI、logo、字幕）一律走后期叠层。
- **执法**：[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)；`prompt_lint.py` `VP-ban`、`VP-realtime`、`VP-distinct`、`VP-lipsync`、`VP-music`、`VP-generator-unsafe`、`VP-negative`。
- **已知边界**：禁令句是兜底不是保证，烧录文字永远由抽帧核验把关（R1）；H3 社区报告"无故出字幕"〔外部调研·S-H3-13〕，竖屏生成更易出字幕〔外部调研·S-VGEN-11〕；不写配乐段 ≠ 静音，无配乐写 `non_diegetic_music: N/A`〔外部调研·S-ZEN-09〕；多人对白镜要写非说话人闭嘴句〔外部调研·S-ZEN-17〕。

### M9 · 三步闸门
- **是什么**：prepare → confirm → run〔委托方实证·M9〕。做法见 P6。
- **为什么是方法**：任何有成本、不可撤销的动作（生成、发布、批量改名）都先预览再执行。
- **下次怎么用**：批量改集号同样走"预演 → 确认 → 执行"：`asset_exists.py --rename OLD NEW`（默认 dry-run）→ 确认 → `--apply`〔E2〕；长任务挂后台，避免被终端超时掐断〔E3-2〕。
- **执法**：[`production-director`](../20-craft/production-director/SKILL.md)；`asset_exists.py`。
- **已知边界**：同 P6。

### M10 · 双文档对账 + 三方台词对账 + 视频双通道验收
- **是什么**：P7 + P8 的方法论合并：任何 QC 结论需两个独立通道（转写 + 抽帧/听感），单通道不判决〔委托方实证·M10、D5〕。
- **为什么是方法**：QC 工具自己也会出错（"字幕by索兰娅"、气声误听"救我"）〔D5〕；双通道把"工具错"与"产出错"分开。
- **下次怎么用**：字幕永远逐字取自剧本，转写只用于定位时间与查缺句；低置信词做 3 窗复核 + 口型接触表。
- **执法**：[`shot-qc`](../20-craft/shot-qc/SKILL.md)；`transcript_reconcile.py`（`TR-hallucination`、`TR-lowconf`、`TR-unscripted`、`--windows`）；`contact_sheet.py`。
- **已知边界**：约 1% 的转写含整句幻觉，长停顿更易触发〔外部调研·S-CASE-28〕；Whisper 默认阈值拦不住高置信的背诵式幻觉〔外部调研·S-COMFY-14、S-COMFY-16、S-COMFY-17〕。

---

## → 行为改变

- 下次开一集之前，把本页 20 张卡的"下次怎么用"当默认工序执行；省略任何一项必须在交付说明里写理由。
- 下次想"创新"一个做法之前，先查本页是否已有对应资产；已有的，优先在它的"已知边界"内改进，而不是另起炉灶。
- 下次发现某个正面资产在新题材/新模型下失效时，在对应卡的"已知边界"补一行（含证据与验证法），并同步 [`40-memory/core-memory.md`](../40-memory/core-memory.md)。

关联：负面案例见 [`60-casebook/README.md`](README.md)；判据↔案例追溯见 [`60-casebook/traceability.md`](traceability.md)；证据冲突裁决见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md)。
