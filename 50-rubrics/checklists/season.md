# 季级连续性清单（R-SEA）

> **阶段**：0 开发（`season-bible.md`、`episode-map.md`、`benchmarks.md`）+ 每集交付时的跨集复核。服务维度：Q1 叙事与钩子、Q7 一致性与连续性、Q8 声音与对白（[`50-rubrics/quality-model.md`](../quality-model.md)）。
> **何时跑**：① 季圣经与分集地图定稿前（人类拍板点①之前）跑 R-SEA-01 … R-SEA-09；② 每集交付前跑 R-SEA-10 … R-SEA-20（跨集复核）；③ 改集号 / 改镜号后跑 R-SEA-18。执行技能：[`20-craft/multi-episode-arc/SKILL.md`](../../20-craft/multi-episode-arc/SKILL.md)、[`20-craft/casting-and-canon/SKILL.md`](../../20-craft/casting-and-canon/SKILL.md)。
> **通过规则**：全部 `[自动]` 条目 0 error；每条 `[目视]` / `[冷观众]` 条目的证据存在并写了结论。委托方只有锚点卡、没有季级弧线/伏笔调度（GAP-7）——本清单的方法多为外部调研与学院推断，首季生产中逐条校准。

| 编号 | 检查句（可判真假） | 方式 | 证据要求 | 溯源 | 工具 |
|---|---|---|---|---|---|
| R-SEA-01 | `season-bible.md` 存在且含五节：世界规则（能力/代价/禁忌）、角色表、主线与支线、伏笔账本、原著取舍表 | [目视] | season-bible.md 目录 | GAP-7, S-ZEN-03 | — |
| R-SEA-02 | `episode-map.md` 每集一行：一句话梗概 + 集末问句 + 卡点类型（揭示 / 反转 / 期限 / 闯入）+ 推进的角色弧线步 | [目视] | episode-map.md | GAP-7, GAP-1, F-STORY-22 | — |
| R-SEA-03 | 每个主要角色有弧线表（季初状态 → 每集变化 → 季末状态），每集至少推进一个主要角色弧线的一步，且没有连续 3 集不动的主角 | [目视] | season-bible.md 弧线表 + episode-map 推进列 | GAP-7, F-STORY-04 | — |
| R-SEA-04 | 伏笔账本每条一行：埋设（集 / 镜）→ 计划回收集 → 实际回收（集 / 镜）→ 状态；季末不存在"已埋、未收、未登记转下季"的条目 | [目视] | `foreshadow-ledger.md`（或 season-bible 伏笔节） | GAP-7 | — |
| R-SEA-05 | 每次主角脱困都能指向一条更早埋设的伏笔或已建立的规则；不存在靠巧合脱困的情节 | [目视] | episode-map 中每个脱困点 → 伏笔账本行号 | GAP-7, F-STORY-05 | — |
| R-SEA-06 | 相邻两集的卡点类型不同；同一种反转机制（如"身份揭秘"）不连续出现 3 次及以上 | [目视] | episode-map 卡点类型列 + 反转机制列 | GAP-1, F-STORY-22, S-STORY-26 | — |
| R-SEA-07 | 若属主声明了付费 / 门槛集：门槛集停在揭晓前一秒、悬念只依赖观众已建立的人物与规则，且不紧跟在一次大回报兑现之后；未声明则不擅自设门槛 | [目视] | episode-map 门槛集标注与理由 | GAP-1, F-ZEN-17, S-PLAT-17 | — |
| R-SEA-08 | 第 1 集内兑现第一个大回报（主角的核心能力或核心冲突被观众看到一次） | [目视] | episode-map 第 1 集行的"首个大回报"字段 | GAP-1, S-ZEN-21 | — |
| R-SEA-09 | 每集开头复现上一集最后一拍（让只看本集的观众接得上），复现时长与内容写进 episode-map | [目视] | episode-map 中每集"开头复现"字段 | GAP-7, S-ZEN-21 | — |
| R-SEA-10 | 本集用到的每个锚点句 EN 与季圣经登记版本逐字相同；有变化的必须是登记过的剧情变体（变体卡写明生效集范围） | [自动] | 锚点句跨集 diff 输出（0 差异，或差异全部对应变体卡） | P1, B1, F-ZEN-23, S-ZEN-15 | diff（无专用脚本；单集内由 prompt_lint VP-anchor 复核） |
| R-SEA-11 | 本集主角至少 1 个正脸镜，已与板图逐特征比对（脸型、发色、标志物）并与前一集正脸库并排 | [目视] | `review/face-library/<角色>/epNN.png` 裁剪图 + 并排对照图 | B1, P5, M7 | scripts/contact_sheet.py（--crop 产出证据） |
| R-SEA-12 | 主要角色两两在脸型 / 发型 / 体型 / 服装主色中至少 2 项不同，且这些区分项写进了各自锚点句 | [目视] | 角色区分矩阵（角色 × 区分项） | B3, S-PLAT-07, GAP-7 | — |
| R-SEA-13 | 每个有台词角色绑定固定音色来源（参考音频或外配音色 ID），全季不变；绑定写在角色表中 | [目视] | season-bible 角色表"音色"列 | GAP-7, S-ZEN-17, F-H3-30 | — |
| R-SEA-14 | 同场出现的两个同性别说话人，盲听各 3 句能被区分；区分不了的已改用音色参考或后期配音 | [冷观众] | `review/cold-audience/voice-*.md`：盲听辨认记录 | S-ZEN-17, GAP-3 | — |
| R-SEA-15 | 状态账本登记伤痕、服装破损、道具持有与位置；本集开头状态与上一集结尾状态逐项一致（或有剧情交代） | [目视] | `continuity-ledger.md` 本集开头/结尾两列 + 对应镜接触表 | GAP-7, B1, S-ZEN-15 | — |
| R-SEA-16 | 本集每个场景的主色与光态与色彩剧本登记一致；跨集重复出现的场景光向与色温不变（或剧情交代了时间变化） | [目视] | 跨集同场景关键帧并排图 | GAP-4, F-ZEN-15 | — |
| R-SEA-17 | 本集成片时长在季规格内（委托方现规格 90–110s） | [自动] | `qc/loudness_verify.json` | T-4 | scripts/loudness_verify.py（--min 90 --max 110） |
| R-SEA-18 | 改集号 / 镜号后全仓无旧集号路径残留，剪辑单素材全部存在 | [自动] | `qc/asset_exists.json` 无 E2-stale-path / E2-stale-token / E2-missing-asset | E2 | scripts/asset_exists.py（E2-stale-path, E2-stale-token, E2-missing-asset） |
| R-SEA-19 | 原著取舍表登记每个被砍情节；被砍情节中没有任何一条是已埋伏笔的回收依据 | [目视] | 原著取舍表 × 伏笔账本交叉核对记录 | T-4, S-ZEN-02, GAP-7 | — |
| R-SEA-20 | 只看本集（未看过前集）的冷观众能复述本集主因果链，并说出"上集发生了什么"中理解本集所必需的那一件事 | [冷观众] | `review/cold-audience/epNN-fresh.md` | F1, GAP-2, GAP-7 | — |

## 常见误判

- **有锚点卡 = 有连续性管理。** 锚点卡只管"外观长什么样"；伏笔、弧线、状态（伤、破损、持有物）、音色都不在锚点卡里（GAP-7）。R-SEA-04、R-SEA-13、R-SEA-15 补的是这一层。
- **每集单独过 L2 = 季成立。** 单集都"看得懂"，但卡点连续三集同一类型、主角连续三集原地不动，追更照样掉（R-SEA-03、R-SEA-06）。季级问题的病灶在开发阶段，不在任何一集的剪辑里。
- **只比当集板图，不比上一集正脸。** 板图 → 第 1 集 → 第 2 集逐步漂移，每一集与板图的差都"差不多"，累积起来就是另一个人。R-SEA-11 要求与前一集正脸库并排。见 [`60-casebook/cards/B1-character-drift.md`](../../60-casebook/cards/B1-character-drift.md)。
- **克隆脸只当成画面瑕疵。** 平台已把"高频 AI 脸 / 主要角色缺乏区分度"列入治理（R-SEA-12），它是下架风险。见 [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md)。
- **音色靠 H3 每镜自由发挥。** 同性别角色音色相似度高，季内会串（R-SEA-13、R-SEA-14）；季开工前就决定音色参考或外配方案。
- **改集号后逐条手改路径。** 委托方实录：整季重编号后 4 份文档残留 143 处旧路径，渲染校验报 30 条"素材不存在"（R-SEA-18）。见 [`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md)。
