# 溯源总表（档案编号 → 判据 → 技能 → 找错题）

> **本文件由脚本生成，请勿手改。** 改源（判据溯源列 / 案例卡 frontmatter / 技能正文 / 找错题答案）后，用下面的命令重新生成；`--check` 用于确认没有过期。
>
> ```bash
> python3 tools/build_traceability.py            # 重新生成本文件
> python3 tools/build_traceability.py --check    # 过期则退出码 1
> ```
>
> 数据源：`50-rubrics/checklists/*.md`（228 条判据，读「溯源」列）、`60-casebook/cards/*.md`（frontmatter 的 skills/drills）、`60-casebook/drills/answers/*.md`（「对应案例」行）、`20-craft/*/SKILL.md`（正文提及的编号）。
> 规则：C1-1..C1-7 计入 C1，E3-1..E3-3 计入 E3；P1 不含 P10。技能列 = 卡片 frontmatter 声明 ∪ 技能正文提及；找错题列 = 卡片声明 ∪ 答案「对应案例」行提及。

| 编号 | 判据（R-） | 技能 | 找错题 |
|---|---|---|---|
| A1 | 12 条：R-CUT-12, R-SB-01, R-SB-02, R-SB-03, R-SB-04, R-SB-05, R-SB-17, R-SB-22, R-SB-23, R-SCR-07, R-SCR-08, R-SCR-09 | `action-choreography`, `cold-audience-test`, `edit-and-assemble`, `multi-episode-arc`, `performance-direction`, `production-director`, `screening-review`, `script-doctor`, `sound-design`, `storyboard-long-take` | DR-01, DR-03, DR-20, DR-21, DR-22 |
| A2 | 5 条：R-KF-14, R-SB-07, R-SB-20, R-SCR-10, R-SND-08 | `action-choreography`, `keyframe-freeze`, `production-director`, `screening-review`, `script-doctor`, `storyboard-long-take`, `video-prompting-h3` | DR-02, DR-03, DR-04, DR-18, DR-20, DR-21, DR-22 |
| A3 | 6 条：R-SB-18, R-SB-19, R-SND-03, R-SND-07, R-VID-15, R-VP-03 | `action-choreography`, `edit-and-assemble`, `performance-direction`, `production-director`, `sound-design`, `storyboard-long-take`, `video-prompting-h3` | DR-01, DR-02, DR-03, DR-18, DR-20, DR-21 |
| A4 | 7 条：R-KF-09, R-SB-08, R-SB-09, R-SB-10, R-VID-17, R-VP-23, R-VP-24 | `action-choreography`, `keyframe-freeze`, `production-director`, `screening-review`, `storyboard-long-take`, `video-prompting-h3` | DR-04, DR-05, DR-17, DR-18, DR-19, DR-21 |
| A5 | 20 条：R-BRD-06, R-COL-05, R-CUT-20, R-KF-05, R-KF-08, R-KF-13, R-PRF-04, R-PRF-06, R-SB-06, R-SB-07, R-SB-10, R-SB-11, R-SB-12, R-SB-13, R-VID-14, R-VP-04, R-VP-05, R-VP-06, R-VP-07, R-VP-24 | `action-choreography`, `cold-audience-test`, `keyframe-freeze`, `performance-direction`, `production-director`, `screening-review`, `shot-qc`, `storyboard-long-take`, `video-prompting-h3`, `visual-bible` | DR-04, DR-05, DR-15, DR-17, DR-18, DR-19, DR-20, DR-21, DR-22 |
| B1 | 10 条：R-BRD-09, R-COL-07, R-CUT-20, R-KF-15, R-KF-17, R-SEA-10, R-SEA-11, R-SEA-15, R-VID-05, R-VP-09 | `asset-boards`, `casting-and-canon`, `keyframe-freeze`, `multi-episode-arc`, `performance-direction`, `production-director`, `shot-qc`, `video-prompting-h3`, `visual-bible` | DR-06, DR-13, DR-14, DR-20 |
| B2 | 4 条：R-BRD-21, R-KF-11, R-SCR-19, R-VP-15 | `casting-and-canon`, `keyframe-freeze`, `shot-qc`, `sound-design`, `storyboard-long-take`, `video-prompting-h3` | DR-07 |
| B3 | 9 条：R-BRD-14, R-BRD-16, R-COL-04, R-KF-10, R-PUB-14, R-SEA-12, R-VID-04, R-VP-08, R-VP-14 | `asset-boards`, `casting-and-canon`, `cold-audience-test`, `keyframe-freeze`, `multi-episode-arc`, `performance-direction`, `publish-prep`, `shot-qc`, `video-prompting-h3`, `visual-bible` | DR-06, DR-20 |
| B4 | 4 条：R-VID-01, R-VID-02, R-VID-19, R-VID-20 | `keyframe-freeze`, `shot-qc`, `video-prompting-h3` | DR-07 |
| C1 | 18 条：R-BRD-02, R-BRD-03, R-BRD-04, R-BRD-05, R-BRD-06, R-BRD-07, R-BRD-10, R-BRD-12, R-BRD-13, R-KF-04, R-KF-06, R-KF-07, R-KF-20, R-SCR-18, R-VID-16, R-VP-05, R-VP-10, R-VP-11 | `asset-boards`, `casting-and-canon`, `keyframe-freeze`, `multi-episode-arc`, `production-director`, `shot-qc`, `video-prompting-h3`, `visual-bible` | DR-08, DR-09, DR-22 |
| C2 | 10 条：R-BRD-03, R-BRD-09, R-BRD-10, R-BRD-11, R-CUT-22, R-KF-04, R-KF-16, R-KF-19, R-VID-16, R-VID-23 | `asset-boards`, `edit-and-assemble`, `keyframe-freeze`, `screening-review`, `shot-qc` | DR-06, DR-07, DR-08, DR-09, DR-12 |
| D1 | 9 条：R-BRD-15, R-CUT-10, R-KF-12, R-SB-21, R-SCR-13, R-VID-06, R-VID-07, R-VP-02, R-VP-13 | `edit-and-assemble`, `production-director`, `publish-prep`, `shot-qc`, `video-prompting-h3` | DR-10 |
| D2 | 10 条：R-BRD-15, R-CUT-07, R-CUT-08, R-CUT-09, R-CUT-10, R-KF-12, R-SB-21, R-SCR-13, R-VID-06, R-VP-13 | `edit-and-assemble`, `production-director`, `script-doctor`, `shot-qc`, `sound-design`, `storyboard-long-take`, `video-prompting-h3` | DR-10, DR-20, DR-22 |
| D3 | 7 条：R-SB-14, R-SB-15, R-SB-16, R-SCR-14, R-SCR-15, R-VID-09, R-VID-12 | `performance-direction`, `production-director`, `script-doctor`, `shot-qc`, `sound-design`, `storyboard-long-take`, `video-prompting-h3` | DR-06, DR-11, DR-12, DR-15, DR-18, DR-20, DR-22 |
| D4 | 2 条：R-BRD-08, R-VP-12 | `asset-boards`, `casting-and-canon`, `keyframe-freeze`, `production-director`, `shot-qc`, `video-prompting-h3` | DR-12, DR-22 |
| D5 | 7 条：R-CUT-11, R-VID-06, R-VID-07, R-VID-08, R-VID-09, R-VID-10, R-VID-11 | `edit-and-assemble`, `screening-review`, `script-doctor`, `shot-qc`, `sound-design` | DR-07, DR-10, DR-13, DR-20 |
| E1 | 1 条：R-VP-20 | `production-director`, `video-prompting-h3` | DR-14 |
| E2 | 5 条：R-BRD-01, R-BRD-11, R-CUT-08, R-SEA-18, R-VID-23 | `asset-boards`, `edit-and-assemble`, `multi-episode-arc`, `production-director`, `publish-prep` | DR-14, DR-22 |
| E3 | — | `edit-and-assemble`, `production-director` | DR-15 |
| E4 | 4 条：R-BRD-20, R-KF-18, R-VID-18, R-VP-25 | `casting-and-canon`, `keyframe-freeze`, `performance-direction`, `production-director`, `shot-qc`, `video-prompting-h3` | DR-09, DR-12, DR-13, DR-15 |
| F1 | 9 条：R-CUT-16, R-CUT-17, R-CUT-18, R-CUT-19, R-CUT-22, R-PRF-10, R-SB-23, R-SCR-07, R-SEA-20 | `cold-audience-test`, `edit-and-assemble`, `production-director`, `publish-prep`, `screening-review`, `script-doctor`, `shot-qc` | DR-09, DR-16, DR-20, DR-22 |
| F2 | 5 条：R-CUT-15, R-CUT-16, R-CUT-20, R-SCR-08, R-VID-17 | `cold-audience-test`, `edit-and-assemble`, `performance-direction`, `production-director`, `publish-prep`, `screening-review`, `shot-qc`, `sound-design`, `storyboard-long-take`, `visual-bible` | DR-01, DR-02, DR-04, DR-13, DR-14, DR-16, DR-17, DR-19, DR-21, DR-22 |
| F3 | 1 条：R-CUT-20 | `action-choreography`, `cold-audience-test`, `keyframe-freeze`, `multi-episode-arc`, `production-director`, `screening-review`, `shot-qc`, `storyboard-long-take`, `video-prompting-h3` | DR-03, DR-05, DR-16, DR-17, DR-18, DR-20, DR-21, DR-22 |
| F4 | — | `production-director`, `screening-review`, `storyboard-long-take`, `video-prompting-h3` | DR-04, DR-19, DR-20 |
| P1 | 6 条：R-BRD-01, R-BRD-20, R-KF-01, R-SCR-18, R-SEA-10, R-VP-09 | `casting-and-canon`, `multi-episode-arc`, `video-prompting-h3` | DR-06, DR-08 |
| P2 | 6 条：R-BRD-02, R-BRD-05, R-BRD-19, R-BRD-20, R-KF-03, R-VID-20 | `asset-boards` | DR-08 |
| P3 | 6 条：R-BRD-05, R-KF-01, R-KF-03, R-KF-04, R-KF-18, R-KF-19 | `keyframe-freeze` | — |
| P4 | 3 条：R-KF-05, R-KF-08, R-SB-11 | `keyframe-freeze`, `video-prompting-h3` | DR-14 |
| P5 | 4 条：R-KF-15, R-SEA-11, R-VID-05, R-VID-18 | `keyframe-freeze`, `video-prompting-h3` | DR-06, DR-15 |
| P6 | — | `production-director` | — |
| P7 | 7 条：R-CUT-10, R-CUT-11, R-SB-24, R-VID-09, R-VP-05, R-VP-17, R-VP-22 | `edit-and-assemble`, `script-doctor`, `storyboard-long-take`, `video-prompting-h3` | DR-11, DR-13 |
| P8 | 10 条：R-CUT-07, R-CUT-13, R-CUT-14, R-PRF-08, R-VID-01, R-VID-02, R-VID-03, R-VID-07, R-VID-08, R-VP-22 | `edit-and-assemble`, `shot-qc` | DR-07, DR-10 |
| P9 | 3 条：R-SB-14, R-SCR-14, R-VID-12 | — | DR-11 |
| P10 | 6 条：R-CUT-12, R-KF-14, R-SB-03, R-SB-04, R-SB-05, R-SB-06 | `action-choreography`, `storyboard-long-take` | — |
| M1 | 3 条：R-KF-14, R-SB-04, R-SB-05 | `storyboard-long-take` | — |
| M2 | 5 条：R-BRD-07, R-COL-08, R-KF-03, R-KF-07, R-KF-08 | `keyframe-freeze`, `video-prompting-h3`, `visual-bible` | DR-18, DR-19 |
| M3 | 5 条：R-SB-17, R-SCR-02, R-SCR-11, R-SCR-12, R-VP-16 | `script-doctor`, `storyboard-long-take`, `video-prompting-h3` | DR-02, DR-03, DR-12, DR-18, DR-19, DR-20 |
| M4 | 7 条：R-KF-05, R-SB-11, R-SB-12, R-VID-14, R-VP-04, R-VP-06, R-VP-07 | `storyboard-long-take` | DR-05 |
| M5 | 3 条：R-SB-14, R-SCR-14, R-VID-12 | — | DR-11 |
| M6 | 3 条：R-BRD-02, R-KF-03, R-VID-20 | `asset-boards`, `casting-and-canon` | DR-08 |
| M7 | 3 条：R-KF-15, R-SEA-11, R-VID-05 | `keyframe-freeze` | DR-06 |
| M8 | 4 条：R-CUT-09, R-SCR-13, R-VP-02, R-VP-13 | `video-prompting-h3` | DR-10 |
| M9 | 1 条：R-KF-19 | `production-director` | — |
| M10 | 3 条：R-SB-24, R-VID-09, R-VID-11 | — | DR-11, DR-13 |
| GAP-1 | 14 条：R-CUT-21, R-PUB-09, R-PUB-16, R-PUB-25, R-SCR-01, R-SCR-02, R-SCR-03, R-SCR-04, R-SCR-06, R-SCR-20, R-SEA-02, R-SEA-06, R-SEA-07, R-SEA-08 | `production-director`, `publish-prep` | DR-20, DR-22 |
| GAP-2 | 3 条：R-CUT-19, R-PUB-22, R-SEA-20 | `cold-audience-test`, `script-doctor` | — |
| GAP-3 | 3 条：R-SEA-14, R-SND-01, R-SND-02 | `sound-design` | DR-20 |
| GAP-4 | 5 条：R-BRD-18, R-COL-01, R-COL-08, R-KF-13, R-SEA-16 | `visual-bible` | DR-20 |
| GAP-5 | 7 条：R-PRF-01, R-PRF-03, R-PRF-07, R-PRF-08, R-PRF-10, R-SCR-16, R-SCR-17 | `performance-direction` | — |
| GAP-6 | 6 条：R-SB-18, R-SCR-05, R-SND-03, R-SND-05, R-SND-06, R-VID-22 | `sound-design` | — |
| GAP-7 | 11 条：R-SEA-01, R-SEA-02, R-SEA-03, R-SEA-04, R-SEA-05, R-SEA-09, R-SEA-12, R-SEA-13, R-SEA-15, R-SEA-19, R-SEA-20 | `multi-episode-arc` | DR-20 |

## 覆盖缺口

- **零判据的编号（3）**：E3, F4, P6
- **零技能的编号（3）**：P9, M5, M10
- **零找错题的编号（8）**：P3, P6, P10, M1, M9, GAP-2, GAP-5, GAP-6

处理：零判据 = 档案里的这条经验还没被固化成可判真假的检查句；零技能 = 没有任何技能把它变成生成/验收动作；零找错题 = 没有训练题让 agent 练习识别它。补缺口时改源文件，不要改本表。

## 一致性提示（卡片声明了、但技能正文/答案没有回指的）

卡片是单向声明；下列是卡片写了、对端却没有回指的项。答案「对应案例」行里多出来的次要案例（卡片没列）是设计如此，不在此报。

- A2：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 A2
- A3：卡片 skills 列了 `edit-and-assemble`，但 `20-craft/edit-and-assemble/SKILL.md` 正文没有出现 A3
- A5：卡片 skills 列了 `shot-qc`，但 `20-craft/shot-qc/SKILL.md` 正文没有出现 A5
- B1：卡片 skills 列了 `keyframe-freeze`，但 `20-craft/keyframe-freeze/SKILL.md` 正文没有出现 B1
- B1：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 B1
- B2：卡片 skills 列了 `storyboard-long-take`，但 `20-craft/storyboard-long-take/SKILL.md` 正文没有出现 B2
- B2：卡片 skills 列了 `shot-qc`，但 `20-craft/shot-qc/SKILL.md` 正文没有出现 B2
- B2：卡片 skills 列了 `sound-design`，但 `20-craft/sound-design/SKILL.md` 正文没有出现 B2
- B4：卡片 skills 列了 `keyframe-freeze`，但 `20-craft/keyframe-freeze/SKILL.md` 正文没有出现 B4
- B4：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 B4
- C1：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 C1
- C2：卡片 skills 列了 `screening-review`，但 `20-craft/screening-review/SKILL.md` 正文没有出现 C2
- D2：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 D2
- D2：卡片 skills 列了 `shot-qc`，但 `20-craft/shot-qc/SKILL.md` 正文没有出现 D2
- D4：卡片 skills 列了 `keyframe-freeze`，但 `20-craft/keyframe-freeze/SKILL.md` 正文没有出现 D4
- D4：卡片 skills 列了 `shot-qc`，但 `20-craft/shot-qc/SKILL.md` 正文没有出现 D4
- D5：卡片 skills 列了 `screening-review`，但 `20-craft/screening-review/SKILL.md` 正文没有出现 D5
- E1：卡片 skills 列了 `production-director`，但 `20-craft/production-director/SKILL.md` 正文没有出现 E1
- F2：卡片 skills 列了 `shot-qc`，但 `20-craft/shot-qc/SKILL.md` 正文没有出现 F2
- F3：卡片 skills 列了 `storyboard-long-take`，但 `20-craft/storyboard-long-take/SKILL.md` 正文没有出现 F3
- F3：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 F3
- F3：卡片 skills 列了 `keyframe-freeze`，但 `20-craft/keyframe-freeze/SKILL.md` 正文没有出现 F3
- F4：卡片 skills 列了 `storyboard-long-take`，但 `20-craft/storyboard-long-take/SKILL.md` 正文没有出现 F4
- F4：卡片 skills 列了 `video-prompting-h3`，但 `20-craft/video-prompting-h3/SKILL.md` 正文没有出现 F4
