# 制作工业流程：从"生成执行"到"制作"

> 回答 G7〔委托方实证〕："我把'生成执行'当成了'制作'。"
> 本文件定义学院认可的**六阶段流程**、每阶段的**产物**与**闸门**，以及最重要的——**缺陷回到病灶阶段修**的路由表。
> 可执行版本：[`20-craft/production-director/SKILL.md`](../20-craft/production-director/SKILL.md)。

---

## 1. 六阶段总览

```
 ┌─────────┐   ┌──────────┐   ┌─────────┐   ┌───────┐   ┌───────┐   ┌───────┐
 │0 开发   │ → │1 预制作  │ → │2 制作   │ → │3 后期 │ → │4 审片 │ → │5 发布 │
 │选题/季  │   │剧本/设定 │   │关键帧/  │   │剪辑/  │   │放映/  │   │物料/  │
 │圣经/对标│   │锚点/分镜 │   │视频/QC  │   │声音/  │   │评审/  │   │合规/  │
 │         │   │预演      │   │         │   │verify │   │冷观众 │   │数据   │
 └─────────┘   └──────────┘   └─────────┘   └───────┘   └───────┘   └───────┘
       ▲             ▲              ▲            ▲           │           │
       └─────────────┴──────────────┴────────────┴── 缺陷单按病灶回流 ◄──┘
```

**判决**：委托方的历史产线 ≈ 只有"2 制作"一个阶段在认真运转（关键帧、视频、QC 都很严），而 0/1/4/5 几乎缺席或只是形式。所以缺陷全部在"2"被发现、又在"2"被打补丁——这就是 F3 补丁式迭代的结构性原因。〔委托方实证·F3、G7；学院推断〕

---

## 2. 各阶段：做什么 / 产物 / 闸门

### 阶段 0 · 开发（Development）
- **做什么**：确定题材与目标观众；原著分析（取哪些情节、砍哪些）；季结构（集数、每集时长、付费/追更节点）；对标作品拆解（至少 3 部同类爆款，记录它们的开场钩子、首反转时间、集末悬念）；平台定位。
- **产物**：`season-bible.md`（季圣经：世界观、角色弧线、主线/支线、伏笔表）、`episode-map.md`（每集一句话 + 集末钩子）、`benchmarks.md`（对标拆解）。
- **闸门**：R-SEA 季级清单 + R-SCR 中的"钩子设计"条目；**人类拍板点①：题材与季结构**。
- **技能**：[`multi-episode-arc`](../20-craft/multi-episode-arc/SKILL.md)、[`script-doctor`](../20-craft/script-doctor/SKILL.md)、[`publish-prep`](../20-craft/publish-prep/SKILL.md)（对标拆解部分）。

### 阶段 1 · 预制作（Pre-production）——**大多数"观感缺陷"的病灶在这里**
- **做什么**：逐集剧本 → 剧本诊断（钩子/节奏/信息密度/对白容量）→ 视觉设定（风格卡、色彩剧本、光态）→ 锚点卡 → 板图（多 seed）→ 分镜（段/拍/镜，运镜因果，方位）→ 动作设计（七相、交手回合、战术链）→ 声音蓝图 → **动态预演（animatic）**。
- **动态预演**：用已冻结的关键帧按分镜时长排成幻灯式粗剪，配临时对白（TTS 或按 7.5 字/秒占位）与节拍标记，在送视频生成**之前**检查：节奏、因果是否看得懂、对白是否装得下。这是成本最低的观感测试点。〔学院推断；动画工业通行做法，见 80-sources〕
- **产物**：`script.md`、`visual-bible.md`、`anchors.md`、`assets/boards/`、`storyboard.md`、`action-design.md`、`sound-plan.md`、`animatic.mp4`。
- **闸门**：R-SCR、R-SB、R-BRD、R-COL、R-PRF（设计部分）；`dialogue_capacity.py`、`segment_rhythm.py` 必须通过；**人类拍板点②：看 animatic，确认节奏与因果**。
- **技能**：[`script-doctor`](../20-craft/script-doctor/SKILL.md)、[`visual-bible`](../20-craft/visual-bible/SKILL.md)、[`casting-and-canon`](../20-craft/casting-and-canon/SKILL.md)、[`asset-boards`](../20-craft/asset-boards/SKILL.md)、[`storyboard-long-take`](../20-craft/storyboard-long-take/SKILL.md)、[`action-choreography`](../20-craft/action-choreography/SKILL.md)、[`sound-design`](../20-craft/sound-design/SKILL.md)、[`performance-direction`](../20-craft/performance-direction/SKILL.md)。

### 阶段 2 · 制作（Production）
- **做什么**：每镜冻结提示词 → 关键帧（海报级抽卡 + 逐特征验收）→ 视频提示词（六段 + 禁令包 + 方位审计）→ prepare → confirm → run → 镜头级 QC（抽帧/PSNR/双通道）。
- **产物**：`keyframes/`、`video-prompts.md`、`clips/`、`qc/`。
- **闸门**：R-KF、R-VP、R-VID；`prompt_lint.py`、`direction_audit.py`、`slot_order_check.py`、`contact_sheet.py`、`psnr_scan.py`、`burnin_text_scan.py`、`transcript_reconcile.py`。
- **技能**：[`keyframe-freeze`](../20-craft/keyframe-freeze/SKILL.md)、[`video-prompting-h3`](../20-craft/video-prompting-h3/SKILL.md)、[`shot-qc`](../20-craft/shot-qc/SKILL.md)。

### 阶段 3 · 后期（Post）
- **做什么**：剪辑单 → 装配 → 声音（环境层/拟音层/音效层/音乐层与剪辑点对齐，混音）→ 色彩统一 → 字幕与叠层字卡（本地生成纯色卡）→ verify（时长/响度/真峰/坏帧/素材存在性）。
- **产物**：`edit-list.md`、`final.mp4`、`final-report.md`。
- **闸门**：R-CUT（技术部分）、R-SND；`asset_exists.py`、`loudness_verify.py`。
- **技能**：[`edit-and-assemble`](../20-craft/edit-and-assemble/SKILL.md)、[`sound-design`](../20-craft/sound-design/SKILL.md)。

### 阶段 4 · 审片（Review）——**委托方历史上缺席的阶段**
- **做什么**：① 自我放映（连续看一遍，写观后感与第一次困惑时间点）；② 8 维全片自查（Q1–Q8 打分）；③ 独立评审（另一会话，只给成片与判据）；④ 冷观众测试（复述因果、记录断点）；⑤ 把所有问题写成缺陷单，**按病灶路由回流**。
- **产物**：`review/self-screening.md`、`review/quality-scorecard.md`、`review/independent-review.md`、`review/cold-audience/*.md`、`review/defects.md`。
- **闸门**：[`definition-of-done.md`](../50-rubrics/definition-of-done.md) 的 L1/L2；**人类拍板点③：看成片 + 审片包**（人类此时看到的应是"已经过三轮外部视角"的片子）。
- **技能**：[`screening-review`](../20-craft/screening-review/SKILL.md)、[`cold-audience-test`](../20-craft/cold-audience-test/SKILL.md)。

### 阶段 5 · 发布（Publish）——**委托方完全空白（GAP-1），以外部调研为据**
- **做什么**：封面、标题、简介、标签、合集；AIGC 标识与平台合规；发布节奏；发布后读留存曲线/完播/追更数据，回流到下一集的开发与剧本。
- **产物**：`publish-kit.md`、`post-release-notes.md`。
- **闸门**：R-PUB；**人类拍板点④：是否发布**。
- **技能**：[`publish-prep`](../20-craft/publish-prep/SKILL.md)。

---

## 3. 缺陷病灶路由表（最重要的一张表）

> 判决：**缺陷在哪里被看见 ≠ 缺陷在哪里产生。** 修复必须回到产生它的阶段；在下游打补丁只会把成本翻倍，并制造新的不一致（E4）。

| 看见的症状 | 病灶阶段 | 回到哪里修 | 不要做的事 | 溯源 |
|---|---|---|---|---|
| 片段式、剧情跳跃、切点跳脱 | 1 分镜 | 重做段/拍结构（长段多拍） | 在剪辑里调转场 | A1 |
| 打斗缺席 / 只有慢镜动作 | 1 动作设计 | 写战术链与交手回合 | 在提示词里加 "epic fight" | A2, A3 |
| 运镜不电影 / 耿直 | 1 分镜 | 重写运镜因果 | 往提示词堆 primitives 词 | A4 |
| 人物乱跑、位置混乱 | 1 分镜 + 2 起始帧 | 单轴定侧、重出起始帧 | 在视频提示词里写更多方位词 | A5 |
| 角色脸漂移 | 1 锚点卡/板图 + 2 参考链 | 链式参考、正脸库比对 | 只换 seed 碰运气 | B1 |
| 生成器添加装饰物/文字 | 2 提示词 + 验收 | 绝对否定句 + 多 seed + 放大验收 | 写 negative_prompt | C1, D1 |
| 对白缺句 | 1 剧本/分镜 | 核算容量、延长镜或删句 | 换 seed | D3 |
| 符号画错 | 1 锚点卡 | 对抗约束清单 | 只重复"正确描述" | D4 |
| 纯色/文字卡被污染 | 3 后期 | 本地生成 + 叠层 | 继续让生成器出纯色 | D2 |
| 素材路径失效 | 3 后期 | 全量替换 + 存在性复查 | 逐条手改 | E2 |
| 技术全绿但人类说"不行" | 4 审片缺席 | 补审片阶段 | 再加一个技术指标 | F1, F2 |
| 每轮修一点永远修不完 | 4 审片 | 8 维全量自查 | 只修最新一条 | F3 |
| 看不懂 / 没人追 | 0 开发 + 1 剧本 | 钩子、首反转、集末悬念 | 在剪辑里加字卡解释 | GAP-1, F1 |

## 4. 成本梯度（为什么要前移）

〔学院推断〕在本管线中，同一个问题在不同阶段修的代价大致是：剧本/分镜（改文字，分钟级）＜ 板图/关键帧（抽卡，十分钟级）＜ 视频（每镜多 seed，小时级 + 算力）＜ 成片后（重生成 + 重剪 + 重混 + 重验）。
**→ 行为改变**：每个能在预制作发现的问题（节奏、因果、对白容量、空间方位、动作逻辑）都必须在 animatic 闸门前发现；送视频生成前未通过 R-SB 全部 `[自动]` 条目的镜，禁止进入 prepare。

## 5. 人类拍板点（只在这四处打扰人类）

| # | 时机 | 人类看什么 | agent 必须先准备好 |
|---|---|---|---|
| ① | 开发结束 | 季结构、题材、对标 | season-bible、episode-map、benchmarks |
| ② | 预制作结束 | animatic | 分镜表、对白容量报告、动作设计 |
| ③ | 审片结束 | 成片 + 审片包 | 自我放映、8 维评分、独立评审、冷观众记录 |
| ④ | 发布前 | 发布物料 | publish-kit、合规清单 |

其余全部由 agent 自主完成（"完全自托管"，见 [`README.md`](../README.md)）。
