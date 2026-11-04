# AI 短剧制作学院（AI-Drama-Academy）

> **一个给 agentos 装载的前置课程包。** 装载后，一个基于「ComfyUI + MiniMax H3 + Qwen-Image」工作流的智能体，能以**完全自托管**的方式，产出**可直接发布**、并能争取**可观浏览量**的**季级竖屏短剧**。
>
> 读者是 agent，不是人。这里没有讲师手册：每一页都是技能（SKILL.md）、记忆条目、判据、脚本、案例或训练题。每一条都要回答：*"装载了这条之后，agent 下一次生成/验收时的行为会有什么不同？"*

---

## 为什么有这个学院

前一个 agentos 已经用这套工具链做出了一部季级短剧的前三集：**工程上全绿**（-16 LUFS、无坏帧、无烧录字幕、字幕逐字对账），**艺术上被人类主创连续打回**——"片段式、剧情跳跃""几乎没有做 BOSS 打斗""无电影级运镜""又变成乱跑了"。它装过 7 个导演/运镜技能、做过 r1→r5 五轮实验，质量没有质变，而且**连"为什么一直达不到要求"都回答不了**。

本学院的三个使命：
1. **把负面资产变成教材与判据**：24 个真实失败案例 → 案例卡 + 找错题 + 可执行判据（[`60-casebook/`](60-casebook/)、[`50-rubrics/`](50-rubrics/)）。
2. **补齐空白环节**：平台发布与流量、冷观众测试、声音、色彩、表演、季级连续性（以外部调研为据，明确标注）。
3. **建立"从判断到执行"的翻译链**：知识 × 实践反馈 × 标准内化 = 能力（[`90-curriculum/`](90-curriculum/)）。

一手证据：[`00-orientation/client-dossier.md`](00-orientation/client-dossier.md)。它的 8 个困惑的回答：[`00-orientation/eight-questions.md`](00-orientation/eight-questions.md)。

## 谁该装载

| 你是 | 你会得到 |
|---|---|
| 即将开始做 AI 短剧/漫剧的 agentos（Claude Code、Codex 等可装载 SKILL.md 的运行时） | 全套技能、判据、记忆、训练回路 |
| 已经在做、但被人类反复打回的 agentos | 先读 [`eight-questions.md`](00-orientation/eight-questions.md) 与 [`production-lifecycle.md`](00-orientation/production-lifecycle.md) 的病灶路由表 |
| agentos 的属主（人类） | [`90-curriculum/load-protocol.md`](90-curriculum/load-protocol.md)：一段安装指令 + 四个人类拍板点 |

**工具链前提**（全篇对齐，见 [`client-dossier.md` § T](00-orientation/client-dossier.md)）：Qwen-Image（板图/关键帧，1696×2528，多 seed）、MiniMax H3（9:16，帧网格 17k+5 = 124–362 帧 ≈ 5.17–15.08s，cfg=1.0，音画同轨，中文 ≈7.5 字/秒容量上限）、ComfyUI、prepare→confirm→run 闸门、ffmpeg 后期链。

## 学什么：十层结构

| 层 | 目录 | 内容 | 形态 |
|---|---|---|---|
| 入学 | [`00-orientation/`](00-orientation/) | 问题、证据档案、8 个困惑的回答、六阶段流程、术语与反馈翻译表 | 必读文档 |
| 理论 | [`10-theory/`](10-theory/) | 14 篇"给 agent 的世界模型"：竖屏生理学、生成语境下的电影语言、空间调度、动作设计、节奏、长段多拍、资产管线、生成器脾气、平台学、质量哲学、声音、色彩、表演、季级架构 | 判决式短文 |
| 手艺 | [`20-craft/`](20-craft/) | 17 个可装载技能，覆盖从开发到发布的每个环节 | `SKILL.md` |
| 美学 | [`30-taste/`](30-taste/) | 风格库、好/坏样例对、审美判据卡 | 对照样例 |
| 记忆 | [`40-memory/`](40-memory/) | 最致命教训的长期记忆条目 | 一行一条 |
| 判据 | [`50-rubrics/`](50-rubrics/) | 8 维质量模型、L0–L3 达标定义、逐环节验收清单、可执行检查脚本 | 清单 + Python |
| 案例 | [`60-casebook/`](60-casebook/) | 24 张负面案例卡、正面资产卡、找错训练题（题面/答案分离） | 案例 + 训练题 |
| 文档包 | [`70-playbooks/`](70-playbooks/) | 剧本/锚点卡/分镜/提示词/剪辑单等模板与格式契约 | 模板 |
| 采集 | [`80-sources/`](80-sources/) | 外部资料评估表（带 URL、分类、核实状态） | 目录 |
| 课程 | [`90-curriculum/`](90-curriculum/) | 装载协议、入学提示词、训练回路、冷观众协议、装机验证 | 协议 + 练习 |

## 怎么装载（摘要；完整版见 [`90-curriculum/load-protocol.md`](90-curriculum/load-protocol.md)）

```bash
git clone <this-repo> ~/ai-drama-academy
bash ~/ai-drama-academy/90-curriculum/install/install.sh   # 技能→技能目录；记忆→记忆库；记录学院根目录
# 改完技能后必须重启运行时（委托方实证 E3-3：技能在装配期一次性扫描）
```

然后让 agent 读 [`90-curriculum/entry-prompt.md`](90-curriculum/entry-prompt.md)，并完成训练回路的最低学分。

## 学分路径

```
入学(00) ──► 训练回路最低学分 ──► 开发/预制作技能 ──► 制作技能 ──► 后期/审片 ──► 发布
  │            找错题 ≥ 10 道          script-doctor        keyframe-freeze   edit-and-assemble   publish-prep
  │            小任务 ≥ 5 个           storyboard-long-take video-prompting-h3 screening-review
  │            装机验证任务 ≥ 70 分     action-choreography  shot-qc           cold-audience-test
  └─ 读 eight-questions / production-lifecycle / glossary / definition-of-done
```

## KPI：学院怎样算"有效"

| KPI | 定义 | 测法 |
|---|---|---|
| 困惑消除 | 装载后 agent 不再产生 G1–G8 中任何一个困惑 | 入学自测 + 训练回路复盘 |
| 装机验证得分 | 未学过短剧的 agent 装载后完成"15 秒打斗段"任务的得分 | [`90-curriculum/install-verification.md`](90-curriculum/install-verification.md)，≥ 70/100 |
| 达标等级 | 产出成片声明的级别（L0–L3）及其证据完整度 | [`50-rubrics/definition-of-done.md`](50-rubrics/definition-of-done.md) |
| 人类打回轮数 | 同一集被人类主创打回的轮数（目标：≤ 1） | 生产记录 |
| 观众指标 | 完播率、追更率（发布后） | 平台数据〔外部调研口径〕 |

## 诚实声明

- 标 `〔委托方实证〕` 的内容来自真实生产与返工；标 `〔外部调研〕` 的来自 [`80-sources/`](80-sources/) 中带 URL 的公开资料；标 `〔学院推断〕` 的尚未被生产验证，并附验证方法。
- 委托方从未发布过作品、从未做过冷观众测试——平台发布、流量运营、冷观众相关内容全部是外部调研，**不是**经验。
- 外部来源之间、以及外部来源与委托方实证之间存在冲突，裁决见 [`00-orientation/evidence-reconciliation.md`](00-orientation/evidence-reconciliation.md)。

## 维护

写作公约：[`CONVENTIONS.md`](CONVENTIONS.md)。提交前：

```bash
python3 tools/academy_lint.py                       # 格式、编号、追溯、链接
python3 50-rubrics/scripts/run_all_selftests.py     # 全部检查脚本自测
```

## 许可

| 范围 | 许可 | 全文 |
|---|---|---|
| 文档（`*.md`：课程、理论、案例、判据、记忆、playbook） | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE`](LICENSE) |
| 脚本与工具（`*.py`、`*.sh`） | [MIT](https://opensource.org/license/mit) | [`LICENSE-MIT`](LICENSE-MIT) |

转载或再分发请保留署名：`AI-Drama-Academy — github.com/czzzjj/ai-drama-academy`。

## 第三方内容与引用声明

- 本仓库**不包含**任何原著的正文、插图或音视频素材。案例卡里出现的角色名（如「苏晓」「尼加狄」）仅用于指认具体的生产缺陷与验收判据，属评论与教学性质的引用，相关权利归原作者及权利人所有。
- [`80-sources/`](80-sources/) 下是外部公开资料的摘要与出处索引，每条附 URL 供回源核对；引用范围以说明观点为限。
- 文中提到的 Qwen-Image、MiniMax H3、ComfyUI、Runway、Seedance 等产品与模型，名称与许可归各自权利人所有；本仓库不分发任何模型权重、素材或生成产物。
