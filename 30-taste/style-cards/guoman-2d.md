# 风格卡 · 国漫二次元（guoman-2d）

> 一句话：用**高完成度单帧**承担情绪和人物魅力；头号风险是**全剧人物互相趋同**。〔外部调研·S-ZEN-20〕
> 选用技能：[`20-craft/visual-bible/SKILL.md`](../../20-craft/visual-bible/SKILL.md) → [`20-craft/keyframe-freeze/SKILL.md`](../../20-craft/keyframe-freeze/SKILL.md) → [`20-craft/video-prompting-h3/SKILL.md`](../../20-craft/video-prompting-h3/SKILL.md)
> 本卡用法见 [`30-taste/README.md`](../README.md)。卡内英文词包标〔学院推断〕的部分都没有经过本管线抽卡，用之前先按"验证"一栏跑一次 A/B。

## 适用题材 / 不适用
- **适用**：仙侠修真、玄幻、古装权谋、都市异能、恋爱向。这些题材靠人物魅力和情绪特写撑起来，长对白场可以用高质量定帧加少量运动顶住。〔外部调研·S-ZEN-20〕
- **不适用**：大量连续空间调度（追逐、多人混战），以及要靠写实质感取信的题材（刑侦、职场）。如果硬上，打斗戏要按 R4 的写法来：打击拍可以密，空间拍压到 ≤2，不然 A5 的空间乱一定复发。

## 身份锚点载体（本风格靠什么认人）
- 五官是精修的，精度本身认不出人，只能靠**可以逐条列出的结构差异**：脸型轮廓（下颌线/颊线）、眼型与瞳孔结构（瞳色分层、高光形状）、发型分层与发色渐变的位置、至少一件不摘的配件。〔外部调研·S-ZEN-20〕
- 必须写进锚点卡：**这个角色和同剧每个其他角色在哪几项结构上不同**，两两分得开为止。「清冷美人」不算锚点；「下颌比同组更方、瞳孔上缘横条高光、左耳一枚不摘的银环」才算。
- 对接判据：R-SEA-12（两两 ≥2 项不同，并写进锚点句）、R-BRD-16（选角对照表）。

## 关键词包（EN，用于板图 / 冻结提示词）〔学院推断〕
| 层 | 短语（{} 是变量） |
|---|---|
| 风格总述 | `Chinese donghua-style 2D illustration`, `clean even-weight {dark brown} ink outlines`, `cel shading with one hard-edged shadow tone per color` |
| 身份层 | `{jaw shape} jawline`, `{eye shape} eyes with {iris color} irises layered in two tones`, `a single horizontal bar-shaped highlight on the upper edge of each iris`, `hair in layered blocks with a gradient from {color A} at the roots to {color B} at the tips`, `{accessory} worn on the {LEFT/RIGHT} side` |
| 环境层 | `painted background one level less detailed than the characters`, `soft depth haze separating foreground and background` |
| 效果层 | `drifting {color} light particles`, `soft bloom around light sources` |
| 光 | `warm key light from the upper right`, `cool bounce light along the left contour`, `shadow edges hard on skin, soft gradient on cloth` |
- **验证**：同一冻结提示词 × 3 seed，跑 [`50-rubrics/scripts/contact_sheet.py`](../../50-rubrics/scripts/contact_sheet.py)，把 3 张正脸裁剪并排，逐项核对身份层的每个短语有没有画出来。没画出来的短语删掉，或改写成更具体的可见状态。

## 负面词改写（R1：正向可见状态句为主，绝对否定只追加在已被证实会自加的物件上）
> 本管线 `negative_prompt` 恒空 + cfg=1.0，等于不起作用〔委托方实证·T-2、C1；外部调研·S-COMFY-05、S-COMFY-06〕。下表左列那些 SD 时代的习惯负面词，**禁止**放进 negative_prompt 字段，也**禁止**原样搬进正文。
| 习惯负面词 | 改写成正向可见状态句 | 追加绝对否定（条件） |
|---|---|---|
| `realistic, 3d, photo` | `flat cel shading, two tones per color, visible ink outlines on every figure` | 只有在 3 seed 中 ≥1 张出现三维体积光影时，才追加 `no photorealistic skin texture` |
| `same face, clone` | 逐人写结构差异句（见身份层）+ `three clearly distinct people with different faces, hair and builds`〔委托方实证·B3〕 | — |
| `bad eyes, asymmetric eyes` | `both irises the same {color}, highlights in the same position on both eyes` | — |
| `text, watermark, signature` | 板图写 `the background wall is blank`；视频块末行固定 D1 禁令句 | D1 句保留（R1-4）；成片照样逐帧抽查 |
| `glowing aura`（不想要的光效） | **什么都不写**：提到什么就会长出什么〔外部调研·S-H3-09〕；光只写成被动的环境光 | — |

## 灯光色调
- 能执行的光写四样：**光源色 + 反射光色 + 高光形状 + 阴影边界硬度**。「精致」「唯美」「高清」都不是规格。〔外部调研·S-ZEN-20〕
- 硬规则：**氛围色不得吃掉识别色**。冷蓝夜景、红色火光底下，瞳色和发色仍要认得出来。验收用 [`30-taste/judgment-cards.md`](../judgment-cards.md) 的 TJ-13 跨场并排，再把脸部裁剪和板图对照。
- 每段色彩脚本命名 3–5 个色名，逐字写进冻结提示词（R-COL-02）。不准全片同一套青橙（R-COL-03）。

## 运动特性（H3 / Qwen 在本风格下）
- **FL2VA 动漫风帧率减半**：H3 讨论区 #74 报告，FL2VA 生成动漫风格时帧率减半〔外部调研·S-H3-13，单帖报告，未复现〕。**验证命令**：
  `k=$(ffmpeg -i clip.mp4 -vf "mpdecimate,showinfo" -f null - 2>&1 | grep -c "Parsed_showinfo.*pts_time"); n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 clip.mp4); echo "$k/$n"`
  比值约为 0.5，就是一拍二（on twos）。对白镜可以接受；动作镜出现就是顿挫感，处置是同镜改用 Ref2VA 再跑 3 seed 做对比，结果写回 `qc/<SHOT>.md`。
- 运动预算：情绪转折镜（眼神变化、转身、伸手）给全动作；对白镜只给口型、眨眼、发梢和衣饰的循环，再加极轻的呼吸位移〔外部调研·S-ZEN-20〕。缓推必须写出因果句（R-SB-08），不然每镜都会默认变成缓推。
- H3 本身大场面动作偏弱，多镜头里表情偏少〔外部调研·S-CASE-10〕，所以本风格不要把一场戏押在大动作上，情绪押在特写与定帧。
- 一镜里表情拍 ≤2–3 个，写多了会被抹平〔外部调研·S-H3-09〕。

## 失败模式（审片时逐条查）
1. **全剧人物趋同**：最常见，也最晚被发现。查法：R-BRD-16 选角对照表、R-VID-04 脸部裁剪表。〔外部调研·S-ZEN-20〕平台把高频 AI 脸当治理对象〔外部调研·S-PLAT-07〕，趋同已经从质量问题升级成下架风险。
2. 氛围光把瞳色、发色吃掉，跨镜认不出人。对应委托方实证 B1 身份漂移。
3. 高光形状逐镜变化，看上去不是同一个人。
4. 背景与角色的写实度差档没有声明，人物像贴纸。
5. 把「精致」「唯美」当规格写进提示词，整段没有一个能执行的字段（R-VP-16）。

## 风格锁句模板（登记进 `visual-bible.md`，逐字嵌入所有板图与冻结提示词）
```text
STYLE-LOCK (guoman-2d): Chinese donghua-style 2D illustration; clean {dark brown} ink outlines of even weight; cel shading with one hard-edged shadow tone per color; painted background one level less detailed than the characters; palette {color 1}, {color 2}, {color 3}; irises keep their {iris colors} and hair keeps its {hair gradient} under every lighting.
```
- H3 提示词里只放短版（≤25 词），写在 `summary:` 的首句〔学院推断。验证：同一镜做"带短版锁句 / 不带"的 A/B，各 3 seed，对比接触表的线稿和平涂有没有漂移〕。

## 参考来源
〔外部调研·S-ZEN-20〕形态卡"国漫二次元"；〔外部调研·S-H3-13〕#74；〔外部调研·S-H3-09〕提到即生长、表情拍上限；〔外部调研·S-CASE-10〕H3 的强项与弱项；〔外部调研·S-PLAT-07〕AI 脸治理；〔委托方实证·B3、C1、T-2〕。

## → 行为改变
- 下次选定本风格时，先产出"角色两两差异矩阵"（R-SEA-12），再写锚点句。矩阵没写完，禁止开板图。
- 下次用 FL2VA 出本风格的动作镜，跑上面的 mpdecimate 命令，比值 ≈0.5 时改用 Ref2VA 对比，不得直接放行。
