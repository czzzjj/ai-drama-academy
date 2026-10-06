# 50-rubrics · 判据层怎么工作

> 本目录回答两个问题：**"够好了吗？"**（G8）与 **"我怎样才能在人类之前发现问题？"**（G4）。
> 装载后的行为要求：任何阶段产物送往下一阶段之前，先跑该阶段清单；任何成片交付之前，先按质量模型打 8 维分、按 definition-of-done 声明级别。技术全绿只是 L0〔委托方实证·F1、F2〕。

---

## 1. 四层结构（从上往下看判决，从下往上跑检查）

```
quality-model.md        Q1–Q8 全片 8 维，0–3 分，观众视角          ← "这部片子好不好"
      │  每维的检查方法指向 ↓
definition-of-done.md   L0 技术合格 / L1 看得懂 / L2 可发布 / L3 有竞争力 ← "能不能交、能声明什么"
      │  每级的通过条件由 ↓ 的条目组成
checklists/*.md         各阶段 R-<STAGE>-nn 判据（可判真假，带溯源）   ← "这个阶段的产物过没过"
      │  [自动] 条目由 ↓ 执行；[目视] 条目由 ↓ 产出证据
scripts/*.py            只报事实，不下审美判决                        ← "数字、位置、偏差、证据文件"
```

- [`50-rubrics/quality-model.md`](quality-model.md)：8 维量表、锚点、阻断缺陷、评分卡、**全维度自查协议**、反馈词 → 维度映射。
- [`50-rubrics/definition-of-done.md`](definition-of-done.md)：L0–L3 的通过条件与证据文件；交付声明模板。
- [`50-rubrics/checklists/`](checklists/)：12 个阶段前缀、10 个文件（见 §4）。
- [`50-rubrics/scripts/`](scripts/)：12 个检查脚本 + 自测汇总（见 [`50-rubrics/scripts/README.md`](scripts/README.md)）。

**判决**：
1. 下层全过不代表上层过。脚本 0 error ⇒ 只能说"该阶段无已知技术缺陷"；清单全过 ⇒ 只能说"该阶段产物合格"；只有质量模型 + 外部视角能说"片子成立"。〔F2〕
2. 上层的每个判断必须能落到下层的证据。质量模型里的每个分数要有时间码与证据文件；没有就按 0 计。〔C2〕
3. 清单是**病灶阶段**的闸门：缺陷回到它产生的阶段的清单里修，不在下游清单里补（路由表见 [`00-orientation/production-lifecycle.md`](../00-orientation/production-lifecycle.md) §3）。〔G7、F3〕

---

## 2. 方式标签

| 标签 | 谁来判 | 必须留下的证据 | 不能替代什么 |
|---|---|---|---|
| `[自动]` | 脚本（退出码 + 规则代码） | `--json` 报告存入 `qc/<脚本名>.json` 或 `qc/<SHOT>/…` | 不能替代 `[目视]`：脚本只证明"没出某类错" |
| `[目视]` | agent 本人或评审 agent **亲自看/听** | 证据文件路径（接触表、裁剪图、帧序列、标注后的文档）+ 一句结论 | 不能写成"已检查，通过"（C2：早期误判放行） |
| `[冷观众]` | 无项目背景的观看者（人，或标注"替身测试，置信度降级"的未见过制作文档的 agent 会话） | `review/cold-audience/*.md`：复述原文、断点时间码 | 不能由制作会话自己扮演（F1 自证循环） |

组合写法：`[自动]+[目视]` = 脚本先跑，脚本报 `visual` 或启发式降级的地方必须补目视。

---

## 3. 证据规则（所有清单通用）

1. **没有证据文件的通过 = 未检查。** 验收记录写在 `qc/<SHOT-nnn>.md`（格式见 [`70-playbooks/format-contracts.md`](../70-playbooks/format-contracts.md) §6），评审写在 `review/`。
2. **双通道**：任何会导致"重出 / 删句 / 判缺陷"的结论，必须有两个独立通道（转写 + 抽帧口型 / 听感；脚本 + 目视）。单通道不判决。〔D5〕
3. **高风险资产（主角 / BOSS / 核心道具 / 关键符号）二次复验**：由另一个会话复验，验收记录写复验人。〔C2〕
4. **方位类属性单独放大**：左右手、左右臂、谁在画左——必须有裁剪图。〔C1-6、C1-7〕
5. **换 seed 前先判"随机 vs 结构性"**：同一缺陷换 ≥2 个 seed 仍在 → 结构性缺陷，回病灶阶段改设计，禁止继续抽卡。〔D3〕
6. **工具先证伪**：转写/OCR/PSNR 报异常时，先确认工具本身没骗你（已知 ASR 幻觉、无音轨、OCR 降级）。〔D5〕
7. **证据与结论同一事实**：已验收产出与提示词不一致时，回写提示词，不保留矛盾。〔E4〕

---

## 4. 清单总表

| 文件 | 前缀 | 阶段（[`production-lifecycle.md`](../00-orientation/production-lifecycle.md)） | 何时跑 | 主要服务的维度 |
|---|---|---|---|---|
| [`checklists/season.md`](checklists/season.md) | `R-SEA` | 0 开发（并在每集交付时复核） | 季圣经/分集地图定稿前；每集交付前复核跨集项 | Q1、Q7、Q8 |
| [`checklists/script.md`](checklists/script.md) | `R-SCR` | 1 预制作·剧本 | 每集剧本定稿前、分镜开工前 | Q1、Q3、Q8 |
| [`checklists/storyboard.md`](checklists/storyboard.md) | `R-SB` | 1 预制作·分镜 | 分镜定稿前、animatic 前；改分镜后全量重跑 | Q2、Q3、Q6、Q8 |
| [`checklists/board.md`](checklists/board.md) | `R-BRD` | 1 预制作·板图 | 每张板图定稿前 | Q5、Q7 |
| [`checklists/keyframe.md`](checklists/keyframe.md) | `R-KF` | 2 制作·关键帧 | 每镜关键帧放行到视频前 | Q2、Q5、Q7 |
| [`checklists/video-prompt.md`](checklists/video-prompt.md) | `R-VP` | 2 制作·视频提示词 | 每镜 prepare 之前；改提示词后全量重跑 | Q2–Q8 |
| [`checklists/video.md`](checklists/video.md) | `R-VID` | 2 制作·镜头验收 | 每条出片后、采用前 | Q2、Q3、Q5、Q7、Q8 |
| [`checklists/sound-color-performance.md`](checklists/sound-color-performance.md) | `R-SND` / `R-COL` / `R-PRF` | 1 设计 + 3 后期 | 声音蓝图/色彩剧本/表演设计定稿时；混音与调色后 | Q5、Q8 |
| [`checklists/final-cut.md`](checklists/final-cut.md) | `R-CUT` | 3 后期 + 4 审片 | 渲染前后；交付声明前 | 全部 |
| [`checklists/publish.md`](checklists/publish.md) | `R-PUB` | 5 发布 | 人类拍板点④之前 | 合规 + Q1 |

**通过规则（每个清单相同）**：该清单全部 `[自动]` 条目 0 error，且每条 `[目视]` / `[冷观众]` 条目的"证据要求"文件存在并写了结论。warn 不阻断，但必须在验收记录里逐条写处置（改 / 不改及理由）。

**条目格式**：每张清单一张表，列固定为 `编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具`（[`CONVENTIONS.md`](../CONVENTIONS.md) §5.4）。溯源列至少一个合法编号（案例 / P / M / T / GAP / S / F），`tools/academy_lint.py` 校验；判据↔案例矩阵由 `tools/build_traceability.py` 生成到 [`60-casebook/traceability.md`](../60-casebook/traceability.md)。

---

## 5. 各阶段脚本链

所有命令在学院根目录下以 `python3 50-rubrics/scripts/<脚本>` 运行；退出码 0 通过 / 1 有 error / 2 用法或环境错误。规则代码全集见各脚本 `--help`。

| 阶段 | 顺序 | 命令（典型） | 关键规则代码 | 对应清单 |
|---|---|---|---|---|
| 剧本 | 1 | `dialogue_capacity.py --text "说话人：台词 / …" --seconds N` | `D3-capacity` `D3-rushed` `D3-stagger` | R-SCR |
| 分镜 | 2 | `segment_rhythm.py storyboard.md --json` | `A1-short-no-reason` `A1-mean-short` `T2-over-max` `A4-cause` `A5-beats-many` `P10-seq-missing` | R-SB |
| 分镜 | 3 | `dialogue_capacity.py --storyboard storyboard.md` | `D3-capacity` `D3-margin` `D3-split` `D3-rushed` | R-SB |
| 提示词 | 4 | `h3_frame_grid.py --check video-prompts.md` | `T2-frames-offgrid` `T2-frames-below-min` `T2-frames-above-max` `T2-duration-mismatch` | R-VP |
| 提示词 | 5 | `prompt_lint.py video-prompts.md --anchors anchors.md --storyboard storyboard.md` | `VP-mode` `VP-struct` `VP-ban` `VP-realtime` `VP-anchor` `VP-distinct` `VP-lipsync` `VP-music` `VP-generator-unsafe` `VP-sync` … | R-VP |
| 提示词 | 6 | `direction_audit.py video-prompts.md --storyboard storyboard.md` | `DIR-camera` `DIR-side` `DIR-layout` `DIR-mapping` `DIR-path` | R-VP、R-SB |
| 提示词 | 7 | `slot_order_check.py video-prompts.md --simulate-remove-placeholder` | `SLOT-contiguous` `SLOT-placeholder-pos` `SLOT-sim` | R-VP |
| 提示词 | 8 | `dialogue_capacity.py --storyboard storyboard.md --prompts video-prompts.md` | `D3-*` `P7-*` | R-VP、R-SB |
| 镜头验收 | 9 | `contact_sheet.py <clip> --keyframe <REF-SHOTnnn-START> --out-dir qc/<SHOT>` | `P8-contact-sheet` `B4-keyframe` `C2-crop` `T2-aspect` | R-VID、R-KF |
| 镜头验收 | 10 | `psnr_scan.py <clip> --json > qc/<SHOT>/<SHOT>.psnr.json` | `P8-freeze` `P8-jump` | R-VID |
| 镜头验收 | 11 | `burnin_text_scan.py <clip或目录> --out-dir qc/burnin` | `D1-burnin-text` `D1-ocr-degraded` `D2-watermark` | R-VID |
| 镜头验收 | 12 | `transcript_reconcile.py --storyboard … --prompts … --transcripts …`（可疑时加 `--windows`） | `TR-missing` `TR-script-prompt` `TR-speaker` `TR-hallucination` `TR-lowconf` | R-VID |
| 成片 | 13 | `asset_exists.py <剪辑单或本季目录> --stale-token <旧集号>` | `E2-missing-asset` `E2-stale-path` `D2-local-syntax` | R-CUT、R-SEA |
| 成片 | 14 | `psnr_scan.py final/epNN.mp4 --mode final --edit-list edit-list.md` | `P8-cut-*` `A1-mean-short` | R-CUT |
| 成片 | 15 | `loudness_verify.py final/epNN.mp4 --min 90 --max 110` | `T4-lufs` `T4-true-peak` `T3-aspect` `T3-black` `T3-freeze` | R-CUT |
| 审片 | 16 | （无脚本）自我放映 → 8 维评分卡 → 独立评审 → 冷观众 | — | quality-model §10–§11、R-CUT |

**闸门**：步骤 2–8 全部 0 error 才进 prepare（三步闸门 P6）；步骤 9–12 的 `[目视]` 结论写进 `qc/<SHOT>.md` 才算采用；步骤 13–15 全过只给 L0；L1 以上只由步骤 16 给出。

---

## 6. 新增判据的规则（清单会长大）

1. 人类每指出一个自查没先发现的问题 → 在**病灶阶段**的清单末尾追加一条（编号顺延，不重排旧编号——其他文件按编号引用）。〔G4〕
2. 检查句必须可判真假："画面好看"不是检查句；"眯眼去色后主体剪影仍可读"是。
3. 溯源写对应的案例/资产/来源编号；如果是新现象，先在 `60-casebook` 补案例卡或在 `40-memory` 记一条，再写判据。
4. 能自动化的写进脚本（改脚本 = 同一次提交改契约、模板、fixtures）；不能自动化的写清证据文件。
5. 判据只对它的病灶阶段负责；同一缺陷不要在三个清单里各写一遍——下游清单写"复核 + 回路由"，不写修法。

**→ 行为改变**：下次任何阶段产物要往下传时，先打开本表找到该阶段清单，逐条跑完并留证据；下次写交付声明时，先按 quality-model 打 8 维分，再按 definition-of-done 选级别，最后才写"达到 L 几"。
