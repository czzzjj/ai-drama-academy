# 02 · 给生成器用的电影语言

> 人类说的"运镜"，指的是镜头语言设计：这一刻为什么用这个景别、从哪个位置看、镜头怎么动、在哪里切。它不是相机位移次数。H3 能执行的只有 12 个运镜原语，加上幅度和速度修饰；动机、轴线和取景必须在起始帧和分镜阶段先定下来，然后一次生成只放一个主运镜 ｜ 浓缩案例：A4, A5, F2, F4, M2, M4 ｜ 对应技能：storyboard-long-take, video-prompting-h3, keyframe-freeze, screening-review

## 核心判决

**T02.1 每个运镜都必须写得出因果句："因为发生了 X，所以镜头做 Y"。写不出，就改成 Static，并写明为什么不动。**
为什么：委托方"固定镜头 = 0"全绿，人类主创仍说「无电影级运镜」「苏晓冲击镜头过于耿直，没有运镜和合理的打斗逻辑」〔委托方实证·A4、F2〕。有动机的运镜只分三类——角色动作、信息揭示、情绪变化，"Choosing not to move can also be a motivated decision"〔外部调研·F-STORY-15〕。判据：R-SB-08、R-SB-09；脚本：`segment_rhythm.py` 的 `A4-cause`。

**T02.2 运镜动词从叙事功能里选，不从原语词表里挑。**
为什么：装了 7 个运镜技能、每镜都嵌入 primitives 句式，质量也没有质变〔委托方实证·A4②、F4〕。社区的质量底线是："A camera move must reveal, follow, compress, release, isolate, destabilize, or transfer attention"〔外部调研·S-H3-10〕。委托方 r5 的动作驱动映射是：受击 → 顿挫，爆发 → 震动，腾跃 → 上摇，收束 → 拉回〔委托方实证·A4〕。

**T02.3 一次生成只放一个主运镜，而且只在高度或距离维度上；顿挫、震动写成事件引起的相机反应。**
为什么：H3 的运镜作用于整次生成，分段指定会把剪点插值抹掉〔外部调研·F-H3-18〕。社区和多家模型的指南都要求"一镜一个主运镜"〔外部调研·S-H3-10、F-VGEN-17、F-VGEN-18〕。学院立场见 [`00-orientation/evidence-reconciliation.md`](../00-orientation/evidence-reconciliation.md) R5。判据：R-SB-10、R-VP-24。

**T02.4 左右维度的原语（Truck、Arc、Pan、横向 Tracking）默认禁用；只有分镜声明了换边、并且起始帧能支持时才放行。**
为什么：起始帧钉死了"神在左 / 苏晓在右"，提示词却写 `trucks left`、`arcs around`，结果是「又变成苏晓乱跑……」；r5 只动高度与距离，空间维度达标〔委托方实证·A5、M4〕。细节见 [`10-theory/03-spatial-staging.md`](03-spatial-staging.md)。

**T02.5 轴线、构图和景别的起点由起始帧决定，文字只描述从这个起点开始发生的变化。**
为什么：画面层面的东西（构图、方向、灯光、史诗感）由起始帧决定，提示词救不了构图〔委托方实证·P4、M2〕。同 seed A/B 测试中，文字写的空间地图压不过场景图〔外部调研·F-H3-21〕。所以景别和机位要在关键帧阶段设计好，不能指望视频提示词去"改机位"。

**T02.6 推近镜必须从宽景起幅，拉远镜必须从紧景起幅。起始帧的取景要给运镜留出行程。**
为什么："A shot that must end tight has to open wide"。super dolly in 从极远景起幅时，主体缩放从 3.08x 提到 7.42x〔外部调研·S-H3-08〕。委托方的 framing 规则（推近镜开场取景在主体最大端）说的是同一件事〔委托方实证·A4〕。

**T02.7 默认不加幅度和速度修饰词；只有镜头的性质本身就是"大"或"快"时（crash zoom、whip pan、360 orbit）才写。**
为什么：`with small amplitude` 基本无效（1.47x，对照 1.53x），不是刹车；large 和 fast 叠在一起会饱和、不叠加〔外部调研·F-H3-12〕。官方写法是把"类型 + 幅度 + 速度"写成句子里的自然动作，不在句尾堆标签〔外部调研·F-H3-01〕。

**T02.8 首帧脚手架和背景参考板会让运镜幅度减半，这是取舍：要钉死轴线时保留，要看得出运镜时改用 reference generation 的写法。**
为什么：`[keyframe completion]`、"<Picture 1> is the first frame" 会钉死起幅、运动约减半；加背景参考板后运镜也约减半，换来约 4 倍的场景稳定〔外部调研·F-H3-11〕。学院立场见 evidence-reconciliation R2。`prompt_lint.py` 对脚手架句报 `VP-scaffold` info。

**T02.9 定稿生成禁止用 4-step turbo，也禁止用 ≤8 步。**
为什么：4 步 turbo 几乎完全压掉运镜，"regardless of the prompt"〔外部调研·F-H3-10〕；8 步时语音和音色最弱〔外部调研·F-H3-09〕。turbo 只能用于预览抽卡。判据：R-VP-23、R-VID-19。

**T02.10 守住 180° 规则、视线匹配和 30° 规则。只换距离或小角度时，用运镜，不切镜。**
为什么：180° 规则在战斗叙事中尤其重要〔外部调研·F-STORY-13〕；机位夹角小于 30° 的两个镜头相接就是跳切〔外部调研·F-STORY-14〕。H3 官方的原话是："If only the distance or a slight angle needs to change, prefer camera motion"〔外部调研·F-VGEN-14〕。

**T02.11 不写机身和镜头型号；画面里会出现的器材名也不写。**
为什么：Cooke、Petzval 这类镜头名基本无效（8mm 和 50mm 出来的构图像素级一致）；写了 "Snorricam body rig" 这种会入镜的器材，模型就把它画出来〔外部调研·S-H3-08〕。景别用取景关系表达（T01.6）。

## 机制解释

**为什么"动了"不等于"有运镜"。** 观众感受到的运镜是"镜头在这一刻替我做了一个选择"：凑近去看、退开去看、跟上去、被震了一下。没有动机的运动会引起注意，有动机的运动观众几乎察觉不到〔外部调研·S-STORY-15〕。所以"固定镜头 = 0"这种代理指标，只会把没有动机的运动堆得更多（F2）。

**为什么原语词表救不了。** 12 个原语只规定了相机**能怎么动**，没有说**为什么动**。动机在分镜层，原语在提示词层。只在提示词层补词，就是把分镜层的病放到下游打补丁（G7）。

### H3 官方 12 原语 × 维度 × 本管线默认（〔外部调研·S-H3-01〕）

| 原语 | 维度 | 典型叙事功能（S-H3-10 动词） | 本管线默认 |
|---|---|---|---|
| Push In / Pull Out | 距离 | compress（压到某人身上）/ release（收束拉回） | ✅ 主力 |
| Zoom In / Zoom Out | 距离（焦距） | crash zoom 只用于峰值 isolate | ✅ 只用于峰值，起幅要宽 |
| Pedestal Up / Down | 高度 | 腾跃上升、俯瞰揭示 reveal | ✅ 主力 |
| Tilt Up / Down | 高度（俯仰） | 由低到高揭示 BOSS 体量 reveal | ✅ 主力 |
| Static Shot | — | 让表演或动作自己说话；对峙、静场 | ✅ 写 `Fixed camera.` 并写明理由 |
| Shake Slightly / Strongly | 事件反应 | destabilize（受击、爆发） | ✅ 只写成事件引起的反应（R5） |
| Pan Left / Right | 左右（转向） | 揭示画外的新信息 | ⚠ 需声明换边 + 起始帧支持 |
| Truck Left / Right | 左右（平移） | 横向跟随 | ⛔ 默认禁用（A5） |
| Arc Shot | 左右（绕行） | 原地重新审视一段关系 | ⛔ 默认禁用（A5） |
| Tracking Shot | 随主体 | follow | ⚠ 只做纵深方向的跟随（朝镜头或离镜头） |
| POV | 视点 | transfer attention | ⚠ 必须先建立"谁在看" |
| Roll CW / CCW | 轴转 | 失衡、眩晕 | ⚠ 只用于主观失衡时刻 |

### 景别与角度：每个都要有职责

| 景别 | 职责 | 竖屏注意 |
|---|---|---|
| 全景 / 远景 | 地理：谁在哪、谁对谁、BOSS 在场地哪里 | 人只占画高 ≤50–60%（T01.6）；每场开头和每次空间变化之后各给一次〔外部调研·S-STORY-20〕 |
| 中景 / 中全景 | 交手回合、关系、动作因果 | 打斗的"出招—命中—反应"要同框（[`10-theory/04-action-design.md`](04-action-design.md)） |
| 近景 / 特写 | 只用于信息、脆弱、思考、权力〔外部调研·S-H3-10〕 | 竖屏主力景别；表情拍每镜 ≤2–3 个〔外部调研·F-H3-16〕 |

- 景别要有序列（远 → 中 → 近，或者反过来但有理由）。一整段都是同一景别，就是 Q2 的 1 分锚点（见 [`50-rubrics/quality-model.md`](../50-rubrics/quality-model.md) Q2）。
- 〔学院推断〕角度（仰、俯、平、Dutch）只在权力关系发生变化时才换：仰拍压迫者，俯拍受压者，Dutch 只用 `Roll Counterclockwise` 表达失衡。验证方法：冷观众看完问"这一段谁占上风"，答案要和角度设计一致。
- 每镜先写一句"这一镜改变了什么"：信息、权力、情绪、关系、危险、空间，六选一以上；一项都不变，就删镜〔外部调研·S-H3-10〕。判据：R-SB-22。

## 本管线下的变体

1. **起始帧钉住轴线。** Ref2VA 起始帧以顺序 1 送入，左右关系从此锁定〔委托方实证·T-2、P4〕。视频提示词里任何与起始帧方位矛盾的左右词都会被"执行"成乱跑（A5①）。
2. **一个主运镜。** 需要两个运镜状态（先推近，再拉回）时，拆成两次生成，在剪辑里接起来（R5）。"顿挫"写成 `the frame jolts as the blade hits the stone`，不写成第二条运镜指令。
3. **脚手架的取舍。** 委托方"起始帧 + 角色板 + 同场关键帧"的组合 = Ref2VA 六段。轴线优先的打斗镜保留首帧锚定；运镜是主角的揭示镜，减少背景板、不称参考图为首帧，然后用接触表首末格的主体尺寸来确认运镜真的发生了（R-VID-17）。
4. **不写运镜句 ≠ 固定。** 不写机位句，28 次里有 4 次出现推拉或平移；写 `Fixed camera.` 的 4 次全部无位移〔外部调研·F-ZEN-11〕。所以静止镜必须显式写出来。
5. **whip pan 要写落点。** 写明落在谁身上后，单步位移从 23 px/step 提到 218 px/step；直接要求 motion blur 无效〔外部调研·F-H3-13〕。
6. **不可能完成的指令会拖垮整镜。** 自然动作下运镜位移是 98–108% 画宽，写了 "holds one single pose completely rigid" 降到 22%〔外部调研·F-H3-15〕。运镜镜里，人物要写成正常呼吸和微动。
7. **手持抖动要有由头。** 主体静止、镜头却在抖，看起来就是瑕疵〔外部调研·S-H3-08〕。Shake 只跟在冲击、奔跑、爆发后面。
8. **换机位只能靠新关键帧，不能事后补。** 让 H3 对已生成的片段换机位，脸和动作偏离更大；链式换机位时，两个模型都没给出可用的远景〔外部调研·F-CASE-11〕。所以覆盖镜头（正反打、远景插入）必须在分镜阶段规划好，各自出关键帧、各自生成。

## 常见误用

| 误用 | 症状 | 案例 |
|---|---|---|
| 把"固定镜头 = 0"当成有运镜 | 统计全绿，观感「无电影级运镜」 | [`60-casebook/cards/A4-unmotivated-camera.md`](../60-casebook/cards/A4-unmotivated-camera.md)、[`60-casebook/cards/F2-proxy-metrics.md`](../60-casebook/cards/F2-proxy-metrics.md) |
| 为修 A4 往提示词里堆 truck、arc、orbit | 和起始帧轴线打架，人物乱跑 | [`60-casebook/cards/A5-spatial-chaos.md`](../60-casebook/cards/A5-spatial-chaos.md) |
| 装更多运镜技能、背更多 primitives | 知识注入，没有能力变化 | [`60-casebook/cards/F4-skills-not-ability.md`](../60-casebook/cards/F4-skills-not-ability.md) |
| 用 turbo 跑定稿，再抱怨"写了运镜不动" | 设置问题被误判成提示词问题 | T02.9 |
| 一次生成里写"先推近、再环绕、最后拉回" | 运镜被平均成一团，剪点漂移 | T02.3 |
| 推近镜从近景起幅 | 推不动，末格和首格几乎一样 | T02.6 |

对应找错题：DR-04（运镜脱钩）、DR-05（空间混乱）、DR-21（把"没有运镜"翻译成镜头语言设计）。

## → 行为改变

- 下次填分镜 `运镜` 列之前，**先**写 `运镜因果`："因为 X（画面内可见事件），所以 Y（叙事功能）"；写不出就填 Static，并写"因为……，所以不动"（R-SB-08、R-SB-09）。
- 下次写 H3 提示词时，**只**写一个高度或距离维度的主运镜，句式用官方的自然句；顿挫、震动写成事件引起的反应；**禁止**在同一镜写第二条运镜指令（R-VP-24）。
- 下次出关键帧时，**先**按运镜终点倒推起幅：推近用宽起幅，拉远用紧起幅，上摇从低处起幅。
- 下次看到"写了运镜但没动"，**先**查设置（步数是否 20、是否挂了 turbo、是否有脚手架句、是否挂了背景板、帧数是否 ≥124），**再**考虑改提示词〔外部调研·S-H3-08〕。
- 下次收到"没有运镜""运镜耿直"这类反馈，**改为**按 [`00-orientation/glossary.md`](../00-orientation/glossary.md) 把它翻译成"镜头语言设计缺席"，去重做分镜里的景别序列和因果句；**禁止**直接往提示词里加运镜词。
- 下次验收运镜镜时，**先**看接触表首末格：推近镜末格主体必须明显更大，上摇镜末格机位必须明显更高；没兑现就记为生成偏差（R-VID-17）。

相关：[`20-craft/storyboard-long-take/SKILL.md`](../20-craft/storyboard-long-take/SKILL.md)、[`20-craft/video-prompting-h3/SKILL.md`](../20-craft/video-prompting-h3/SKILL.md)、[`20-craft/keyframe-freeze/SKILL.md`](../20-craft/keyframe-freeze/SKILL.md)、[`50-rubrics/checklists/storyboard.md`](../50-rubrics/checklists/storyboard.md)、[`50-rubrics/checklists/video-prompt.md`](../50-rubrics/checklists/video-prompt.md)、[`10-theory/08-generator-temperament.md`](08-generator-temperament.md)。

## 自测

1. 是非：一集里固定镜头数为 0，说明运镜设计合格。
<details><summary>答案</summary>错。这是代理指标（F2）。合格的标准是：每个运镜都写得出因果句，并且在产出中兑现；静止也可以是有动机的选择（F-STORY-15）。</details>

2. 简答：起始帧里神在 LEFT、苏晓在 RIGHT，导演想要"镜头绕到苏晓身后看 BOSS"。怎么做？
<details><summary>答案</summary>不在这一镜里写 arc 或 orbit。可选做法：① 新出一张"苏晓背身前景、BOSS 在后景"的关键帧，单独生成，在分镜里声明 `换边: 设计（理由…；起始帧支持证据…）`，并用轴上缓冲镜或可见的跨轴运镜过渡（F-STORY-13）；② 保持单轴，用 Pedestal Up / Tilt 从苏晓肩后的高度揭示 BOSS。</details>

3. 简答：提示词写了 `The camera pushes in with small amplitude at slow speed`，产出几乎看不出推近，列出排查顺序。
<details><summary>答案</summary>先查设置：步数是否 20、有没有挂 4-step turbo（F-H3-10）、有没有首帧脚手架句或背景板（F-H3-11）、帧数是否 ≥124。再查写法：small amplitude 本来就基本无效（F-H3-12），应该去掉；起幅是否已经是近景（T02.6）；有没有 "rigid pose" 这类不可能完成的指令（F-H3-15）。</details>

4. 是非：想让一次生成先推近、在接触瞬间顿一下、再拉回，可以在提示词里写三条运镜。
<details><summary>答案</summary>错。运镜作用于整次生成（F-H3-18、R5）。只写一个主运镜（推近）；"顿"写成接触引起的相机反应；"拉回"拆成下一次生成，在剪辑里接。</details>

5. 简答：为什么不写 `shot on Cooke S4 50mm`？那景别怎么控制？
<details><summary>答案</summary>镜头名基本无效，写会入镜的器材名还会被画出来（S-H3-08）。景别靠起始帧的取景，再加取景字段描述（到腰、头在上三分之一、机位高度与距离，F-ZEN-10）。</details>
