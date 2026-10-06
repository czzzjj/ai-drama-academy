---
name: publish-prep
description: 发布前准备（⚠全部依据外部调研，委托方从未发布过）：第一步先跑合规——AIGC 显式/隐式标识、《微短剧发展管理办法》片头剧名与编号和内容条款、H3/Qwen-Image/配乐许可与发布地域——任何未确认项上报人类拍板点④；合规全部确认后再做封面、标题、简介、标签、合集、钩子切片、安全区、更新节奏与发布后留存曲线回流，产出 publish-kit.md。Use when an episode reaches L2 candidacy, before uploading anywhere, when choosing platforms/territories, or when designing covers/titles/clips. 触发词：发布、上架、合规、AI标识、许可、商用授权、地域限制、封面、标题、简介、标签、合集、切片、安全区、留存曲线、publish, upload, compliance, AIGC label, license, territory, thumbnail, title, hook clip, safe zone, retention curve。不负责成片内标识的叠加实现（edit-and-assemble）、法律意见（由属主/法务拍板）、季结构与付费卡点设计（multi-episode-arc）。
---
# 发布准备（publish-prep）

> 路径约定：文中 `60-casebook/...` 等路径相对学院根目录。⚠ 本技能所有事实为〔外部调研〕，**不构成法律意见**；委托方无发布实证（GAP-1）。合规表以 [`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第四部分为准，出现新规先改那里。

## 何时用 / 何时不用

- **用**：screening-review 给出 L2 候选之后、人类拍板点④之前；选目标平台 / 地区时（应在开发阶段就做一次地域预检）；设计封面、标题、切片时；发布后 24h / 72h 回收数据时。
- **不用**：成片还没过 L1——物料救不了看不懂；先回 screening-review / cold-audience-test。
- **不用**：自行判断"许可应该没问题"——任何未确认项只能上报，不得自行发布。

## 输入 → 输出

| 输入 | 输出 | 模板 |
|---|---|---|
| `final/epNN.mp4`、`final-report.md`、`assets/license-ledger.md` | `publish-kit.md`：合规表（R-PUB-01–16 每行 已确认 / 未确认→上报）+ 物料表 + 节奏表 | [`70-playbooks/templates/publish-kit.md`](../../70-playbooks/templates/publish-kit.md) |
| 成片 + 剪辑单时间码 | 封面帧、标题、简介、标签、合集、钩子切片 | 同上 |
| 平台后台数据 | `post-release-notes.md`（24h / 72h，曲线与剪辑单时间码对齐） | 同上 |

## 步骤

**A. 合规（先于一切物料，任一项未确认 → 停，上报人类拍板点④）**

1. **AIGC 显式标识复核**：抽成片第 0–3s 帧（`python3 50-rubrics/scripts/contact_sheet.py final/epNN.mp4 --out-dir review/publish`）确认：含"AI / 人工智能"+"生成 / 合成"；在边或角且不落平台 UI 遮挡区；字高 ≥ 短边 5%（1080 宽 ≥54px）；第 0 帧起 ≥2s；**每一集**都有。验：R-PUB-01、R-PUB-02、R-PUB-03、R-PUB-04、R-PUB-05。缺 → 退回 edit-and-assemble 步骤 6。〔外部调研·S-PLAT-02、S-PLAT-03〕
2. **隐式标识**：`ffprobe -show_format final/epNN.mp4` 截取含 `AIGC` 字段的 JSON 元数据作证据。验：R-PUB-06。
3. **《微短剧发展管理办法》（2026-09-01 施行）**：片头标剧名 + 许可证号 / 节目编号（第 27 条）；每集明显位置 AI 提示标识（第 34 条）；对照禁止内容条款逐条核对剧本与成片。分类分层档位与"AI 辅助制作"字样原文未找到 → 不自判，列为人类拍板项。验：R-PUB-07、R-PUB-15。〔外部调研·S-PLAT-01、S-PLAT-04、S-PLAT-05、S-PLAT-06〕
4. **平台 AI 声明**：上传时打开平台 AI 内容声明（抖音 AI 内容标识、TikTok AIGC 标签、YouTube 生成式 AI 披露）。验：R-PUB-08。〔外部调研·S-PLAT-11、S-PLAT-23、S-PLAT-25〕
5. **模型许可与地域**：
   - H3：社区许可把美国、欧盟、英国、韩国列为排除地域，不得在那里展示 Outputs；商用需显著展示 "MiniMax H3"；本地输出商用需取得 MiniMax 商业授权（经 Comfy）。发往 YouTube / TikTok 等全球平台前必须有授权。验：R-PUB-09、R-PUB-10。〔外部调研·S-H3-14、S-COMFY-09〕
   - Qwen-Image-2.1：Qwen Research License 仅研究 / 评估；变现短剧属商用，无商业许可 → 上报；可商用备选是 Qwen-Image-Edit-2511（Apache-2.0），改用须回 asset-boards 重出资产。验：R-PUB-11。〔外部调研·S-COMFY-01、S-COMFY-02〕
   - 配乐 / 音效：许可台账每行标可商用；MiniMax Music 3 开源权重（据报道 CC BY-NC 4.0）、NC / ND、BBC RemArc 一律不可商用；YouTube 单集 >60s 时配乐不得触发 Content ID 认领。验：R-PUB-12、R-PUB-13、R-SND-10。〔外部调研·S-H3-16、S-PLAT-24、S-CRAFT-23〕
6. **形象权与区分度**：角色未使用真实人物照片（含网络写真）；主要角色区分度足够——克隆脸 / 高频 AI 脸已是下架风险。验：R-PUB-14、R-SEA-12。〔外部调研·S-PLAT-07、S-PLAT-09〕
7. **合规表闭合**：`publish-kit.md` 合规表 R-PUB-01 – R-PUB-15 每行写"已确认 + 证据路径"或"未确认 → 已上报拍板点④（日期）"。验：R-PUB-16、R-CUT-21。**任一行未确认 = 不得发布，不得写"可发布"。**

**B. 物料（合规表闭合后）**

8. **开场与集末**：复核开场 3s 内冲突主张可见（谁 + 想要什么或受到什么威胁）、5s 内出现吸引元素；最后 10s 抛出一个具体未解问题（冷观众记录佐证）。不满足 → 回 script-doctor / 剪辑，物料不补救。验：R-PUB-17、R-PUB-22。
9. **安全区与静音可读**：默认禁区上 14% / 下 35% / 左右各 6%（无国内官方像素规范，按平台可配置）；字幕、片名、AI 标识、关键人脸在全片抽帧上都不落禁区；关声音也能看懂（全部台词硬字幕）。验：R-PUB-18、R-PUB-19。〔外部调研·S-PLAT-20、S-PLAT-21〕
10. **封面**：取本集正片一帧（YouTube Shorts 只能选帧），最多 1–2 张带复杂情绪的脸，不出现正片没有的画面。验：R-PUB-20。〔外部调研·S-CASE-18、S-PLAT-24〕
11. **标题 / 简介 / 标签 / 合集**：标题 ≤100 字符，承诺的事件必须在本集兑现（标题党 = 留存断崖）；简介写主角 + 欲望 + 本集钩子，含模型署名（如许可要求 "MiniMax H3"）；标签含题材 + AI 标签；合集 / 专辑按季建立、集号与成片一致。验：R-PUB-21、R-PUB-23。
12. **钩子切片**：从成片取 15–30s 切片（复用剪辑单 CUT，不重新生成），切片自身也必须带 AI 标识。平台支持陌生观众测试（如 Instagram Trial Reels）时，同一集两版开场各投一次。验：R-PUB-24。〔外部调研·S-PLAT-26〕
13. **更新节奏**：`publish-kit.md` 写每周几集、固定时段、合集结构；节奏与季结构的付费 / 门槛集由人类定（T09.5）。验：R-PUB-23。
14. **发布后回流**：24h、72h 在 `post-release-notes.md` 记录播放、完播、互动，留存曲线的每个掉点对齐剪辑单 CUT 时间码，写成"下一集开发阶段的输入"——数据只校准下一集，不证明这一集；A/B 按观看时长判胜负，不按点击率。验：R-PUB-25。〔外部调研·S-CASE-16、S-CASE-17〕

## 判据

- 合规（阻断级）：R-PUB-01 – R-PUB-16、R-CUT-21、R-SND-10、R-SEA-12。
- 物料：R-PUB-17 – R-PUB-24；回流：R-PUB-25。
- 质量维度：主 **Q1 叙事与钩子**（开场 3s、集末问题、标题兑现）；**Q7**（区分度 = 下架风险）。definition-of-done §3：缺 AIGC 标识是阻断缺陷，不得声明 L2。

## 失败模式

| 症状 | 案例卡 | 本技能的防线 |
|---|---|---|
| 主要角色雷同，被平台按"高频 AI 脸"处理 | [`60-casebook/cards/B3-clone-faces.md`](../../60-casebook/cards/B3-clone-faces.md) | 步骤 6 区分度复核；不过 → 回 casting-and-canon |
| 生成器自带字幕 / 水印进了发布版 | [`60-casebook/cards/D1-burned-in-captions.md`](../../60-casebook/cards/D1-burned-in-captions.md) | 步骤 9 全片抽帧复核文字只来自剪辑单 |
| 技术 verify 全绿就上传 | [`60-casebook/cards/F2-proxy-metrics.md`](../../60-casebook/cards/F2-proxy-metrics.md) | 步骤 7 合规表闭合是硬前置；L2 证据缺一不发 |
| agent 自判"许可没问题"直接发 | [`60-casebook/cards/F1-self-verification-loop.md`](../../60-casebook/cards/F1-self-verification-loop.md) | 未确认项只能上报拍板点④ |
| 改了集号，合集里集号与片头不一致 | [`60-casebook/cards/E2-stale-paths.md`](../../60-casebook/cards/E2-stale-paths.md) | 步骤 11 合集集号对账；改号走 edit-and-assemble 步骤 10 |

## 关联

- 理论：[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)（T09.1–T09.10）、[`10-theory/01-vertical-drama-physiology.md`](../../10-theory/01-vertical-drama-physiology.md)、[`10-theory/14-season-architecture.md`](../../10-theory/14-season-architecture.md)。
- 相邻技能：[`20-craft/edit-and-assemble/SKILL.md`](../edit-and-assemble/SKILL.md)（标识实现）、[`20-craft/screening-review/SKILL.md`](../screening-review/SKILL.md)（L2 前置）、[`20-craft/sound-design/SKILL.md`](../sound-design/SKILL.md)（许可台账）、[`20-craft/production-director/SKILL.md`](../production-director/SKILL.md)（拍板点④）、[`20-craft/multi-episode-arc/SKILL.md`](../multi-episode-arc/SKILL.md)（节奏与卡点）。
- 判据清单：[`50-rubrics/checklists/publish.md`](../../50-rubrics/checklists/publish.md)。
- 找错题：[`60-casebook/drills/DR-17.md`](../../60-casebook/drills/DR-17.md)、[`60-casebook/drills/DR-20.md`](../../60-casebook/drills/DR-20.md)。

## → 行为改变

- 下次进入发布，第一件事是打开合规表逐行填，不是挑封面。
- 下次任何一行许可或地域"不确定"，写进上报清单交人类，禁止上传。
- 下次做切片，从剪辑单取 CUT 并保留 AI 标识，禁止为切片单独生成画面。
- 下次看留存曲线，先把掉点对齐到 CUT 时间码，再写进下一集的开发输入。
