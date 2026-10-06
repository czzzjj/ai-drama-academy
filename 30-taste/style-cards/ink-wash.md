# 风格卡 · 水墨（ink-wash）

> 一句话：水墨用**显与隐**说话。浓淡决定观众先看什么，留白决定什么可以暂时不知道。默认运动预算极低。〔外部调研·S-ZEN-20〕
> 选用技能：[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md)、[`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md)、[`20-craft/sound-design/SKILL.md`](../../20-craft/sound-design/SKILL.md)

## 适用题材 / 不适用
- **适用**：神话、志怪、诗词改编、武侠意境段、回忆段、片头片尾。用作关系压力、动作余势、时间流逝、心理距离。
- **不适用**：需要精确地理、机械结构、可读细节（证据、文书、屏幕）承载因果的戏。这些信息会被形态吃掉，必须换载体保住，比如交给后期叠层或改成写实插段。
- **混用**：在写实或国漫剧里插一段水墨回忆是合法的，但必须在 `visual-bible.md` 声明切换点和切换理由，见 [`30-taste/README.md`](../README.md) 的混用规则。

## 身份锚点载体
- 认人靠**轮廓的笔势 + 不能散的墨记号**：发髻的走向、衣纹的三笔主线、腰间最浓的一块墨〔外部调研·S-ZEN-20〕。
- 锚点卡必须点名：**哪些边缘绝不允许洇化**。少了这一条，下游每一次"加点水墨感"都会合法地把人物吃掉一点。

## 关键词包（EN）〔学院推断，验证：3 seed 并排，按 TJ-01 去色看浓淡层级是否按设计排序〕
| 墨的六项 | 承担什么 | 短语 |
|---|---|---|
| 浓淡 | 注意力顺序 | `the swordsman is the darkest, densest ink in the frame; mountains fade to pale grey washes` |
| 干湿 | 时间与用力程度 | `dry, broken brush texture on the sleeve edge` |
| 飞白 | 速度与撕裂 | `flying-white streaks trailing behind the blade to the LEFT` |
| 洇化 | 情绪扩散或时间流失 | `ink bleeding softly into the wet paper around the fallen petal` |
| 留白 | 未知、距离、被拒绝的信息 | `the upper two-thirds of the frame is empty rice paper` |
| 笔势 | 动作方向与余势 | `three bold strokes define the robe, sweeping to the RIGHT` |
- 风格总述：`traditional Chinese ink-wash painting on rice paper, visible paper grain`。若着彩，只给一个焦点：`a single vermilion accent on {object}, everything else monochrome ink`。〔外部调研·S-ZEN-20：多给一处色就会和浓淡抢注意力〕

## 负面词改写
| 习惯负面词 | 正向可见状态句 | 追加绝对否定（条件） |
|---|---|---|
| `colorful, saturated` | `monochrome ink in five tones from jet black to pale wash` | A/B 中出现彩色时追加 `no color except the single vermilion accent` |
| `blurry face`（脸被洇没） | `the face outline is a crisp unbroken ink line; only the robe edges bleed` | — |
| `text, calligraphy, seal`（不想要的题款） | 不写任何字、印类名词（提到即生长〔外部调研·S-H3-09〕）；需要题款就由后期叠层，属于委托方实证 D2 的原则 | 已证实会自加印章、题字时才追加 `the paper is blank outside the painted figures` |
| `ink-wash feel, Chinese aesthetic` | **删掉**，不能执行。改写成六项中的具体条目 | — |
> 禁止使用 negative_prompt 字段〔委托方实证·C1、T-2〕。

## 灯光色调
- 水墨没有物理光。可执行的是**墨的六项**，每项都要写明它承担的叙事职责〔外部调研·S-ZEN-20〕。
- 色彩脚本照写（R-COL-01），格里的字段换成：浓淡主次、留白方位、着彩焦点。不要写色温。

## 运动特性（H3 / Qwen）
- 默认极低预算：大部分画面 hold，只让少数墨迹动，比如洇开的一小块、飘散的笔触、从留白里进来的一笔。转折靠墨的状态变化承接，不靠角色全动作〔外部调研·S-ZEN-20〕。
- H3 写 `Fixed camera.`，4 次全部没有机位位移；不写机位句的 28 次里，有 4 次推拉或平移〔外部调研·S-ZEN-17〕。所以本风格每镜都要明写 `Fixed camera.`。只有一镜主运镜（如缓慢上摇揭示留白）时例外，并写出因果句。
- **禁止**给所有笔触加持续抖动：画面会退化成噪点，浓淡层级和留白同时被破坏〔外部调研·S-ZEN-20〕。验收用 [`50-rubrics/scripts/psnr_scan.py`](../../50-rubrics/scripts/psnr_scan.py)：本该 hold 的镜，相邻帧 PSNR 应高而稳。若整镜偏低（`P8-low-baseline`），说明全画面都在动，抽帧目视确认。
- 本风格的纯 hold 镜可以考虑不送 H3，改为本地对冻结关键帧做慢速缩放或位移〔学院推断。验证：同一镜本地版和 H3 版并排给独立评审盲选，记录选择〕。注意：这类镜依然受 A1 约束，不得把一个动作切成多个镜号。

## 失败模式
1. 用「水墨感」盖掉地理和手中物，因果读不出来〔外部调研·S-ZEN-20〕，对应委托方实证 A1 的"看不懂"。
2. 不能散的边缘被洇化吃掉，人物认不出，属于 B1 身份漂移在本风格下的变体。
3. 浓淡层级逐镜漂移，注意力顺序失效。
4. 把留白当成"还没想好"，而不是设计过的未知。
5. 给所有笔触加运动，画面变成噪点。
6. 生成器自己加了印章、题款文字，属于委托方实证 D1、D2 的同类：生成器会自己加字。

## 风格锁句模板
```text
STYLE-LOCK (ink-wash): traditional Chinese ink-wash painting on rice paper with visible grain; monochrome ink in five tones; {who} is always the darkest, densest ink; these edges never bleed: {face outline}, {hair knot}, {sword}; empty paper fills the {upper/lower} part of the frame; {single vermilion accent on X | no color}.
```

## 参考来源
〔外部调研·S-ZEN-20〕形态卡"水墨笔触"；〔外部调研·S-ZEN-17〕`Fixed camera.` 实测；〔外部调研·S-H3-09〕；〔委托方实证·D1、D2、C1〕。

## → 行为改变
- 下次选水墨，锚点卡先写"不可散边缘清单"。没有这份清单，禁止在任何提示词里加洇化或飞白。
- 下次验收水墨镜，用 TJ-01 去色图检查最浓那块墨是不是在设计好的主体上；不在，判不通过。
