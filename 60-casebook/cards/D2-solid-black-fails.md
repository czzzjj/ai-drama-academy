---
id: D2
title: 纯黑画面无法生成
group: D 生成技术
scope: 通用
severity: 严重
provenance: 委托方实证
skills: [edit-and-assemble, video-prompting-h3, shot-qc]
drills: [DR-10]
---
# D2 · 纯黑画面无法生成

> 一句话：**确定性的画面不要交给随机采样器。** 生成器没有"什么都不画"这个选项。画面越空，它越会按先验往里填东西：水印、logo、文字。纯色卡、精确文字、UI、logo 一律本地生成，再由剪辑叠层。

## 症状（含人类主创原话，逐字引用档案）

- 片尾的纯黑字卡交给 H3 生成，结果中段帧里被模型自行加上了 "LAVCE" 文字水印，纯黑没守住〔委托方实证·D2〕。
- 档案没有保留人类主创关于本案的「」逐字原话。
- 学院缺陷分级：画面里出现生成器自行添加的文字或水印，属于阻断缺陷（Q5），见 [`50-rubrics/definition-of-done.md`](../../50-rubrics/definition-of-done.md) §3。

## 现场（何时、哪一集/哪一轮、具体到镜/字样/数字）

- 位置：片尾纯黑字卡；水印字样 `LAVCE`；出现在**中段帧**，不在首帧〔委托方实证·D2〕。所以只看首帧或尾帧的抽查会漏掉它，必须覆盖全程。
- 档案没有记录这一镜的时长、seed 数，也没有记录卡上原本要显示的文字。
- 小号水印在检测上很隐蔽：`burnin_text_scan.py` 头部说明记录的实测显示，居中 28px 或角落 40px（1080p）的水印，在 270 宽灰度帧里的启发式得分只有 0.02–0.05，远低于通用阈值 0.08，按通用阈值会整段漏报。因此脚本对"近纯色帧上出现文字样笔画"单设了 `D2-heuristic-flat`。
- `LAVCE` 已作为默认水印词写进 `burnin_text_scan.py`（`--watermark-token` 还可以追加）。

## 根因（分条；区分"直接原因"与"方法论原因"）

### 直接原因
1. 把一个没有内容的画面交给了按内容采样的生成器。画面里没有可以锚定的主体，模型就用训练分布里最常见的"空画面伴随物"来填，也就是平台水印和片尾字样〔委托方实证·D2；学院推断〕。
2. 字卡上的文字原本打算让生成器一起出。精确文字本来就是生成器的弱项〔委托方实证·D2 判据〕。

### 方法论原因
3. 默认"所有画面都走生成器"，没有先问一句：这个画面是**确定的**还是**需要采样的**？纯色卡、字卡、标识的每个像素都是事先确定的，用随机采样去做，只会多出风险，得不到任何好处。
4. 没有一份"不要交给生成器的事"清单，每次都要靠踩坑才知道。

### 外部调研补强的根因
5. 生成器会自带水印：Seedance 官方 FAQ 说，即使没有提示，也可能生成其他平台的 logo 或水印〔外部调研·S-VGEN-11〕。同行经验也提到，监控室、屏幕墙一类题材词会召回自带角标水印的套路图，负面提示压不住〔外部调研·S-COMFY-21〕。
6. 写了"无可读文字"，表面上仍然会稳定长出类汉字的伪字形，所以否定式约束不可靠〔外部调研·S-COMFY-21〕。纯黑画面没有别的内容去占住注意力，这个问题被放大〔学院推断〕。
7. 时长和时机也不适合交给 H3。单次生成最短 124 帧（5.17s），一张 2s 的黑卡也得生成 5.17s〔委托方实证·T-2〕。H3 片尾前 1.2–1.7s 常崩成噪声色块，而片尾卡正好落在这个区间〔外部调研·F-H3-18〕。H3 也不能精确安排事件时刻〔外部调研·F-H3-14〕，淡入淡出的时机控制不了。

## 修正过程（做了什么、第几轮、结果）

- 委托方的做法：纯色类画面（纯黑、纯白、纯色卡）一律在本地确定性生成静帧图，剪辑时叠层加字，不送生成器〔委托方实证·D2〕。之后三集成片通过 verify，无烧录字幕〔委托方实证·T-4〕。
- 学院落地为契约：剪辑单的 `来源` 写 `local:black`、`local:white` 或 `local:#RRGGBB`，文字写进 `画面文字` 列（[`70-playbooks/format-contracts.md`](../../70-playbooks/format-contracts.md) §4）。
- 本地生成的参考命令（1080×1920，2.5s）：
  `ffmpeg -f lavfi -i color=c=black:s=1080x1920:d=2.5:r=24 -c:v libx264 -pix_fmt yuv420p black.mp4`
  淡入淡出也在剪辑里做（ffmpeg `fade` 滤镜），不写成提示词里的 `fades to black`。
- 同一原则可以迁移到合规：AIGC 显式标识要求字高 ≥ 画面短边 5%、持续 ≥ 2s〔外部调研·S-PLAT-02〕。这类标识由剪辑程序叠加，不交给生成器（[`00-orientation/evidence-reconciliation.md`](../../00-orientation/evidence-reconciliation.md) 第四部分）。

### "不要交给生成器的事"清单（学院版）
| 画面 | 为什么不给 | 改由谁做 | 溯源 |
|---|---|---|---|
| 纯黑 / 纯白 / 纯色卡 | 空画面会被填进水印、文字 | 剪辑单 `local:` | D2 |
| 精确文字（字卡、字幕、标题、AIGC 标识） | 写不对，还会扩写成乱码或水印 | 剪辑单 `字幕` / `画面文字` | D1、D2 |
| logo / 台标 / 水印 | 生成器会自造 | 剪辑叠层 | D2、S-VGEN-11 |
| UI 面板 / 数值界面 | 守不住结构 | 本地生成 + 叠层 | D2 |
| 需要精确几何的符号 | 会被先验改形（见 D4） | 关键帧阶段锁定 + 放大验收；必要时本地合成 | D4〔学院推断〕 |

## 可固化判据（每条标 [自动]/[目视]/[冷观众]；被 50-rubrics 引用）

- [自动] `prompt_lint.py` 不报 `VP-generator-unsafe`。纯色画面、字卡、精确文字、logo/水印、UI 面板、字幕任何一类出现在提示词里，都是 error〔D2、D1〕。
- [自动] 剪辑单里的纯色卡写成 `local:black|white|#RRGGBB`；`asset_exists.py` 报 `D2-local-syntax` 时必须修正〔D2〕。
- [自动]+[目视] 任何近纯色画面（包括误送生成器的旧素材）跑 `burnin_text_scan.py <clip>`。`D2-watermark` 是 error；`D2-heuristic-flat`、`D2-watermark-lowconf` 要打开 `<clip>.burnin-frames.jpg` 逐格看〔D2、D5〕。
- [自动] 成片跑 `psnr_scan.py final/epNN.mp4 --mode final --edit-list edit-list.md`：`local:` 卡区间内的冻结应报 info `P8-freeze-designed`；剪辑单之外的冻结报 `P8-freeze`，要逐个解释〔D2、P8〕。
- [自动] 成片跑 `loudness_verify.py`：设计内的黑场加 `--allow-black`，否则 `T3-black` 必须逐段对上剪辑单里的 `local:black`〔D2、T-3〕。
- [目视] 片尾卡、字卡的文字逐字核对剪辑单 `画面文字` 列〔D2、P7〕。

## → 行为改变（下次……）

- 下次分镜时，每一镜先判断它是"确定画面"还是"采样画面"。确定画面直接写进剪辑单 `local:` 行，不进 `video-prompts.md`。
- 下次需要淡入淡出、黑场停顿、片尾卡，都在剪辑里做。**禁止**在提示词里写 `fades to black`、`black screen`、`end card`。
- 下次遇到"生成器总是做不对的画面"，先查上面的清单。不在清单里但同样确定的画面，加进清单，写回本卡和 [`40-memory/core-memory.md`](../../40-memory/core-memory.md)。
- 下次验收任何"画面很空"的镜（夜空、雾、大片纯色墙），用 `burnin_text_scan.py` 加整帧目视查水印；不能只看底部条带。

## 适用面与迁移（★通用 / ☆项目特有；换题材/换模型时是否仍成立）

- ★ "确定性画面不交给采样器"对任何生成器都成立，与 cfg、模型版本无关。
- ★ 迁移到合规物料：AIGC 标识、剧名、许可证号、节目编号这类片头必备文字〔外部调研·S-PLAT-01、S-PLAT-02〕，同样由剪辑程序化叠加。
- ☆ `LAVCE` 这个具体字样属于本项目的观察。换模型后要重新收集该模型的高发水印词，追加到 `--watermark-token`。

## 关联（技能、理论、判据清单、找错题）

- 技能：[`20-craft/edit-and-assemble/SKILL.md`](../../20-craft/edit-and-assemble/SKILL.md)（`local:` 卡、叠层、淡入淡出）、[`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)（生成器不该做的事）、[`20-craft/shot-qc/SKILL.md`](../../20-craft/shot-qc/SKILL.md)（水印扫描）、[`20-craft/publish-prep/SKILL.md`](../../20-craft/publish-prep/SKILL.md)（AIGC 标识叠加）。
- 理论：[`10-theory/08-generator-temperament.md`](../../10-theory/08-generator-temperament.md)、[`10-theory/07-asset-pipeline.md`](../../10-theory/07-asset-pipeline.md)、[`10-theory/09-platform-publishing.md`](../../10-theory/09-platform-publishing.md)。
- 判据清单：[`50-rubrics/checklists/video-prompt.md`](../../50-rubrics/checklists/video-prompt.md)、[`50-rubrics/checklists/final-cut.md`](../../50-rubrics/checklists/final-cut.md)、[`50-rubrics/checklists/publish.md`](../../50-rubrics/checklists/publish.md)。
- 脚本：[`50-rubrics/scripts/prompt_lint.py`](../../50-rubrics/scripts/prompt_lint.py)、[`50-rubrics/scripts/burnin_text_scan.py`](../../50-rubrics/scripts/burnin_text_scan.py)、[`50-rubrics/scripts/asset_exists.py`](../../50-rubrics/scripts/asset_exists.py)、[`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)、[`50-rubrics/scripts/loudness_verify.py`](../../50-rubrics/scripts/loudness_verify.py)。
- 找错题：[`60-casebook/drills/DR-10.md`](../../60-casebook/drills/DR-10.md)（烧录字幕 / 纯黑卡）。
- 相邻案例：[`60-casebook/cards/D1-burned-in-captions.md`](D1-burned-in-captions.md)、[`60-casebook/cards/D4-symbol-errors.md`](D4-symbol-errors.md)、[`60-casebook/cards/D5-qc-tools-lie.md`](D5-qc-tools-lie.md)（启发式不单独判决）、[`60-casebook/positive-assets.md`](../positive-assets.md)（M8）。
