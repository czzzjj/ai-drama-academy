---
name: casting-and-canon
description: 从原著与季圣经为每个角色/道具/场景/符号建立锚点卡：一句逐字嵌入所有提示词的英文锚点句、正向优先 + 绝对否定的必现/禁用项、方位属性、原著出处、音色绑定，并保证主要角色两两可区分。Use when creating or revising characters, props, locations or symbols before any board/keyframe/video generation, or when a face/outfit drifts across shots. 触发词：锚点卡、锚点句、选角、角色设定、禁用项、必现项、原著出处、角色区分度、音色绑定、anchor card, anchor sentence, casting, canon, banned items, character distinctness, voice reference. 不负责生成板图与抽卡验收（→ asset-boards）、不负责风格与色彩（→ visual-bible）、不负责季级角色弧线（→ multi-episode-arc）。
---
# 选角与原著锚定（casting-and-canon）
> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。锚点卡格式以 [`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §3 为准，`prompt_lint.py --anchors` 按它解析。

## 何时用 / 何时不用
- **必须用**：任何资产第一次在剧本/分镜中出现之前；原著有新的外观描述被采用时；QC 发现身份漂移、装饰物被加、符号画错时（回到锚点卡修，不在提示词里修）。
- **不用**：背景人群——人群不建独立 `CHR-` 卡（R-BRD-21），只在场景卡写"大虚化暗形块"。纯色卡/字卡——它们是本地叠层，不是资产。
- 判决：跨镜一致性不是生成器给的，是锚点卡→板图→关键帧→链式参考一层层锁出来的；锚点卡是第一层文字锁〔委托方实证·P1、M6〕。

## 输入 → 输出
- 输入：原著相关章节、`season-bible.md` 角色表、`visual-bible.md`（风格卡与色名）、剧本中的出场清单。
- 输出：`season-01/ep03/anchors.md`（季级共用则放 `season-01/anchors.md`，各集引用），模板 [`70-playbooks/templates/anchor-card.md`](../../70-playbooks/templates/anchor-card.md)；选角对照表 `assets/boards/casting-lineup.png`（与 asset-boards 交接）；原著取舍登记进 `season-bible.md`。
- 每张卡固定字段（契约 §3）：

```markdown
## ANCHOR: CHR-SUXIAO
- 类型: 角色
- 锚点句 EN: `a slender 17-year-old girl with a sharp jaw, straight black hair tied high with a plain dark-red cord, a faded indigo cotton jacket with frayed cuffs, holding a single-edged straight sword in her LEFT hand`
- 必现: 黑直发高马尾 + 暗红素绳；靛蓝旧棉衣、袖口磨损；单刃直剑、无中脊
- 禁用: the hair cord is a plain dark-red cord, smooth and unadorned; no jewelry at all; no armor; no neck ornament
- 方位属性: 左手持剑（画面方位需单独放大核验）
- 来源依据: 原著第 x 章 "……"（逐字摘句）
- 区分项: 脸型尖；高马尾；瘦长体型；主色靛蓝
- 音色: voices/CHR-SUXIAO-ref.wav（全季固定）
- 板图: （asset-boards 定稿后回填）
```

## 步骤
1. **列出场清单**：从剧本动作行与分镜 `内容` 列抽出全部在 ≥1 镜出现的资产，分配 ID：`CHR-` 角色 / `PRP-` 道具 / `LOC-` 场景 / `SYM-` 符号（契约 §0.4）。验：R-BRD-01 每个资产有卡。
2. **原著取证**：每个外观项（发、衣、装备、标志物、伤痕）先在原著找出处，逐字摘到 `来源依据`。原著没写的装备**不得发明**（BOSS 无铠甲就写 `no armor`）。验：R-SCR-18。被砍的原著设定登记进取舍表（R-SEA-19）。
3. **写锚点句 EN**：一句英文、一行、反引号包裹、不可换行；只写**每一镜都成立**的可见特征（脸型、发、衣、标志物、持物手）；不写情绪、动作、光、镜头。顺序：年龄体型 → 脸 → 发 → 衣 → 标志物 → 持物。禁止写"提到会长出来"的物件（S-H3-09：提到什么就长什么）。登记进季圣经后**全季逐字不变**（R-SEA-10），剧情变体（受伤、换装）另开 `CHR-SUXIAO-V2` 卡。
4. **写必现**：每条必现必须能在 270 宽放大裁剪上判真假（"发色黑"可判，"气质清冷"不可判）。程度类属性写成可量的对比（"黑臂与白臂明度差一眼可读"）。
5. **写禁用（R1 立场）**：每条禁用**先写正向可见状态句**，再在其后追加绝对否定句：`the sword guard is plain polished steel, smooth and unadorned; no gemstone`。只有生成器**已被证实会自行添加**的物件（宝石、铠甲、颈饰、远山、刻纹、光柱）才追加否定句；新加的否定句须由 asset-boards 做 A/B（各 ≥3 seed）验证没把物件招进来（R-BRD-12、R-BRD-13）。禁止写 `negative_prompt` 字段——cfg=1.0 下无条件分支被跳过，无效〔委托方实证·C1；外部调研·S-COMFY-05、S-COMFY-06〕。
6. **写方位属性**：持物手、黑臂/白臂、伤疤侧、刘海分向，一律写"角色自身左右"并注明"画面方位需单独放大核验"。验：R-BRD-06、R-KF-06（下游执行）。
7. **符号资产（SYM-）写对抗约束**：不止写正确形态，还要把每个已见过的错误变体逐条写成计数句：`exactly one red ring; exactly one vertical line through the center; zero horizontal lines; not a cross`。验：R-BRD-08，下游 R-VP-12〔委托方实证·D4〕。
8. **角色区分度**：全部主要角色两两比较脸型 / 发型 / 体型 / 服装主色，至少 2 项不同，且区分项**写进各自锚点句**（R-SEA-12）；板图阶段再做选角对照表，任意两人 ≥3 项可见特征不同（R-BRD-16）。同框多人的镜由 video-prompting-h3 写差异化句（R-VP-08）。平台治理"高频 AI 脸"，红果要求主要角色形象有清晰区分〔外部调研·S-PLAT-07〕。
9. **音色绑定**：每个有台词角色绑定固定音色来源（参考音频或外配音色 ID），写进 `音色` 字段与角色表（R-SEA-13）；同场两个同性别说话人须盲听可分（R-SEA-14）。H3 两个男声音色相似度高〔外部调研·S-ZEN-17〕。
10. **参考来源合规**：禁止用真实人物照片（含网络写真）当角色参考；参考图来源记入授权台账（R-BRD-17、R-PUB-14）。
11. **交接**：把卡交给 [`asset-boards`](../asset-boards/SKILL.md) 出板；板图定稿后回填 `板图` 字段（定稿 seed + 落选归档路径，R-BRD-20）。若定稿图与锚点句有出入，**改锚点句为画面事实**或重出，不允许两者不一致地流入下游（E4）。
12. **自检命令**：`python3 50-rubrics/scripts/prompt_lint.py season-01/ep03/video-prompts.md --anchors season-01/ep03/anchors.md` —— `VP-anchor` 0 error 证明锚点句逐字进了每镜 `subject_definitions`（R-VP-09）。

## 判据
- 锚点卡本身：R-BRD-01、R-BRD-06、R-BRD-08、R-BRD-12、R-BRD-16、R-BRD-17、R-BRD-20、R-BRD-21。
- 剧本与季级：R-SCR-18、R-SEA-10、R-SEA-12、R-SEA-13、R-SEA-14、R-SEA-19。
- 下游消费：R-VP-09（逐字）、R-VP-10（正向优先）、R-VP-11（无 negative_prompt）、R-VP-12（符号对抗约束）、R-KF-04、R-VID-16（中后段禁用物复现）。
- Q 维度：Q7 一致性与连续性（主）、Q5 美术与密度、Q8 声音与对白（音色）。

## 失败模式
- **脸在第 N 镜变成另一个人** → [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md)：防线 = 锚点句全季逐字（步骤 3）+ 变体另开卡。
- **同框两人长同一张脸** → [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)：防线 = 步骤 8 区分项写进锚点句；一人只给一张脸参考（R-BRD-14，"几张脸 = 几个人"〔外部调研·S-H3-09〕）。
- **宝石、铠甲、颈饰被加回来** → [`60-casebook/cards/C1-banned-items-violated.md`](../../60-casebook/cards/C1-banned-items-violated.md)：防线 = 步骤 5 正向句 + 已证实物件的绝对否定句 + 原著无出处不发明。
- **符号十字/竖线画错** → [`60-casebook/cards/D4-symbol-errors.md`](../../60-casebook/cards/D4-symbol-errors.md)：防线 = 步骤 7 计数式对抗约束。
- **人群被生成出独立脸和道具** → [`60-casebook/cards/B2-crowd-leak.md`](../../60-casebook/cards/B2-crowd-leak.md)：防线 = 不给人群建卡。
- **锚点句与定稿图不一致仍流入下游** → [`60-casebook/cards/E4-prompt-output-mismatch.md`](../../60-casebook/cards/E4-prompt-output-mismatch.md)：防线 = 步骤 11 回写纪律。

## 关联
- 理论：[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)。
- 证据立场：[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) R1（禁用项写法）、第四部分（参考图授权）。
- 相邻技能：上游 `multi-episode-arc`（角色表）、[`visual-bible`](../visual-bible/SKILL.md)（色名）；下游 [`asset-boards`](../asset-boards/SKILL.md)、[`keyframe-freeze`](../keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../video-prompting-h3/SKILL.md)。
- 找错题：DR-06（漂移 + 克隆脸）、DR-08（禁用项被违反）、DR-12（符号错误）。
- → 行为改变：下次在提示词里想"补一句外观描述"时，改为先改锚点卡并登记版本，再让所有镜逐字同步。
