# 文档格式契约（Format Contracts）

> 这是**脚本与文档之间的接口**。[`50-rubrics/scripts/`](../50-rubrics/scripts/) 中的检查脚本按本文件解析制作文档；[`70-playbooks/templates/`](templates/) 中的模板按本文件生成。改契约 = 同时改脚本、模板、fixtures，三者必须同一次提交。
> 溯源：P7（双文档对账）、E1（槽位顺序）、E2（路径残留）、D3（对白容量）、A5（方位审计）〔委托方实证〕。

## 0. 通用规则

1. 文件编码 UTF-8，换行 LF。文件名用英文（`storyboard.md`、`video-prompts.md`…），中文名可作为标题（E3-1：中文路径在 cmd 下会吞输出）。
2. 一集一个目录：`season-01/ep03/`，其下放该集全部文档；素材放 `season-01/ep03/assets/`。
3. **Markdown 表格解析规则**：脚本寻找"表头行包含契约列名"的管道表；列顺序不限；多余列忽略；单元格内 `|` 必须写成 `\|`；空值统一写 `—`。
4. ID 规则：镜号 `SHOT-012`（三位数字，集内唯一）；段号 `SEQ-03`；资产 ID `CHR-` 角色 / `PRP-` 道具 / `LOC-` 场景 / `SYM-` 符号；参考图 ID `REF-SHOT012-START`（起始帧）、`CHR-SUXIAO-BOARD`（板图）。
5. 时长单位：秒，保留两位小数；帧数必须落在 H3 帧网格 `17k+5`（k=7…21，即 124…362 帧，24 fps）上，由 `h3_frame_grid.py` 校验/吸附。两位小数是显示舍入：所有脚本吸附时容忍 0.005s（`5.17` = 124 帧 = 5.1667s，不会被吸到 141 帧）。
6. **交付规格**：成片交付 **1080×1920，严格 9:16**。H3 768P 的 9:16 输出 768×1344 是 32 对齐的近似 9:16 中间稿（偏 ≈1.6%）；委托方剪辑稿 480×864 实为 5:9（偏 ≈1.2%，T-1）——两者都只能做草稿/中间稿，不能直接交付〔外部调研·S-H3-02、S-H3-03〕。脚本容差口径（两处一致）：
   - 成片级 `loudness_verify.py`：偏离 9:16 **> 1% → error `T3-aspect`**（`--aspect-tol` 默认 0.01；480×864 会被拦下并注明"实为 5:9"）；
   - 单镜级 `contact_sheet.py`：偏离 9:16 **> 2% → warn `T2-aspect`**（`--aspect-tol` 默认 0.02；768×1344、480×864 不告警，16:9 告警）。

---

## 1. 分镜表（`storyboard.md`）

必需列：

| 列名 | 类型 | 规则 |
|---|---|---|
| `段号` | `SEQ-nn` | 一个段 = 一条完整动作链/一场戏的一个单元（A1、P10） |
| `镜号` | `SHOT-nnn` | 集内唯一 |
| `时长(s)` | 数字 | 送 H3 的镜 ≥ 5.17（124 帧下限，T-2）；**< 5.17s（不足 124 帧）必须填 `短镜理由`**，且该镜不送 H3（本地生成，D2） |
| `拍数` | 整数 | 段内 2–3 拍为常态（P10）；>3 拍需在 `内容` 中说明空间如何不跳变（A5③） |
| `内容` | 文本 | 写**事件**不写形容词（M3）；动作链用 `→` 串联 |
| `运镜` | 文本 | 只写一种主运动 + 方向维度（高度/距离/左右） |
| `运镜因果` | 文本 | 必须是"因为 X，所以镜头 Y"句式（A4）；静止镜写"因为……，所以不动" |
| `起始帧方位` | `名=LEFT; 名=RIGHT` | 取值 `LEFT` / `RIGHT` / `CENTER` / `FG` / `BG`；无人物写 `—` |
| `对白` | 文本 | 多句以 ` / ` 分隔，每句 `说话人：台词`；无对白写 `—` |
| `短镜理由` | 文本 | 时长 < 5.17s（124 帧，H3 下限）时必填，否则 `—`；只写 `—`/`——`/`TBD` 等占位视同未填 |

示例：

```markdown
| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |
|---|---|---|---|---|---|---|---|---|---|
| SEQ-02 | SHOT-004 | 10.83 | 3 | 苏晓佯攻右肩→神抬臂格挡落空→苏晓矮身抓隙斩腿 | 缓推→接触瞬间顿挫 | 因为接触发生，所以推近在接触帧顿住强调力量 | 神=LEFT; 苏晓=RIGHT | 苏晓：就是现在！ | — |
| SEQ-02 | SHOT-005 | 5.88 | 2 | 神踉跄后退→跪地，地面裂纹扩散 | 上摇→拉回 | 因为神倒下，所以拉回交代全局后果 | 神=LEFT; 苏晓=RIGHT | — | — |
```

`起始帧方位` 的值用大写英文 `LEFT/RIGHT/CENTER/FG/BG`；写成中文 `左/右/中/前景/背景` 时脚本会归一后照常核对，但报 warn（`DIR-layout`）要求改回契约写法。

脚本：`segment_rhythm.py`（段长/短镜/拍数，短镜阈值 5.17s）、`dialogue_capacity.py`（对白容量）、`direction_audit.py`（与提示词交叉核对方位）。

---

## 2. 视频提示词（`video-prompts.md`）

每镜一个二级标题 `## SHOT-nnn`，下接**元数据列表**与**一个 `h3` 代码块**：

````markdown
## SHOT-004
- 时长: 10.83
- 帧数: 260
- 模式: Ref2VA
- first_frame: REF-SHOT004-START
- references: 1=CHR-SUXIAO-BOARD; 2=CHR-GOD-BOARD; 3=REF-SHOT003-START
- 起始帧方位: 神=LEFT; 苏晓=RIGHT
- 轴线策略: 单轴定侧
- 锚点: CHR-SUXIAO; CHR-GOD
- 角色映射: S1=苏晓; S2=神

```h3
subject_definitions:
  [S1] the young swordswoman on the RIGHT — <CHR-SUXIAO 锚点句逐字> <Picture 1>
  [S2] the stone god on the LEFT — <CHR-GOD 锚点句逐字> <Picture 2>
summary:
  ...
retention_analysis:
  ...
detailed_description:
  Real-time speed throughout, no slow motion. ...
  [S1] shouts: <d>[Chinese] 就是现在！</d>
  ...
overall_soundscape:
  ...
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```
````

FL2VA（只有首帧/尾帧）的写法——三段，首行是官方对齐句（见 [`50-rubrics/scripts/fixtures/fl2va/video-prompts.md`](../50-rubrics/scripts/fixtures/fl2va/video-prompts.md)）：

````markdown
## SHOT-030
- 时长: 8.00
- 帧数: 192
- 模式: FL2VA
- 尾部余量: 1.30
- first_frame: REF-SHOT030-START
- references: —
...

```h3
How the reference pictures align with the target video — the first frame is the opening image of the shot at 0.00s; there is no last frame.

integrated_multimodal_description:
  [S1] the swordswoman in the center: <锚点句逐字> ...
  [S1] says quietly: <d>[Chinese] 走吧。</d>
overall_soundscape:
  ...
non_diegetic_music:
  N/A
No captions, subtitles, or dialogue text overlays appear at any moment.
```
````

### 2.1 模式（必填）：Ref2VA 还是 FL2VA

| `- 模式:` | 何时用 | ComfyUI 节点 | 提示词方言 |
|---|---|---|---|
| `Ref2VA` | 多张参考图：起始帧 + 角色板 + 前镜关键帧（委托方链式参考做法 P5 就是这一类） | `MiniMaxH3ReferenceToVideo` | 六段：`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music` |
| `FL2VA` | 只有首帧和/或尾帧（0–2 张图），不挂角色板 | `MiniMaxH3ImageToVideo` | 三段：`integrated_multimodal_description:` / `overall_soundscape:` / `non_diegetic_music:`（首行官方对齐句 "How the reference pictures align with the target video — …"） |

〔外部调研〕见 [`80-sources/catalog/minimax-h3-hailuo.md`](../80-sources/catalog/minimax-h3-hailuo.md)：两种模式是**两个不同的检查点文件**（S-H3-02）；托管 API 中 first/last frame 与 `reference_*` **互斥**（F-H3-27）；Ref2VA 六段、FL2VA 三段 + 对齐句（F-H3-02、F-H3-03）。所以"起始帧 + 角色板 + 前镜关键帧"按官方口径属于 Ref2VA，写六段。
〔学院推断·待核〕委托方节点里"first_frame + 六段 + 多图参考"究竟加载的是哪个检查点、起始帧是作为 reference 还是经 AddGuide 钉在第 0 帧（S-H3-03），未经核实 → **用一次同 seed A/B 确认**（同一镜分别按 Ref2VA 六段 / FL2VA 三段各出一条，比对起幅贴合度与运镜量），结论回写本节。
缺 `模式` 时 `prompt_lint.py` 报 warn `VP-mode` 并按 Ref2VA 检查；`模式: FL2VA` 却写了 `references` 也报 `VP-mode`（互斥）。

规则：
1. 元数据键固定：`时长`、`帧数`、**`模式`（`Ref2VA` / `FL2VA`，见 §2.1）**、`first_frame`、`references`、`起始帧方位`、`轴线策略`、`锚点`（锚点资产 ID，分号分隔）、`角色映射`（说话人/主体 ID → 分镜表中的角色名，如 `S1=苏晓; S2=神`；画面 ≥2 人时必填，方位审计靠它把提示词与起始帧方位对上）。同一镜内同名键只认第一条。
   - `轴线策略` 合法值只有 `单轴定侧` 与 `换边`；写 `换边` 必须同时有 `- 换边:` 理由。其余写法（单侧、拼错、英文）一律按单轴定侧审计并报 warn（`DIR-axis`）。
   - `起始帧方位` 值用大写英文 `LEFT/RIGHT/CENTER/FG/BG`；中文 `左/右` 会被归一后核对，但报 warn。
   可选键：
   - `慢动作: 设计选择（理由…）`（豁免实时速度句，A3）；`换边: 设计（理由…；起始帧支持证据…）`（豁免单轴定侧，A5）。**值为 `否/无/no/none` 不是豁免**，按未声明处理。
   - `步数: 20`：≤ 8 时 `prompt_lint.py` 报 warn `VP-steps`——turbo/低步数会压掉运镜、削弱参考与语音（〔外部调研·F-H3-09、F-H3-10〕），只用于预览抽卡，定稿镜用默认 20 步重出。
   - `尾部余量: 1.3`（秒）：H3 常在最后 ~1.2–1.7s 崩解（〔外部调研·F-H3-18〕），生成时多留 1.3–1.5s、剪辑时裁掉。**声明后：提示词 `时长` = 分镜 `时长(s)` + 尾部余量**（帧数仍按提示词时长取网格）；凡比较两份文档时长的脚本（`prompt_lint.py` VP-sync、`dialogue_capacity.py`）都按此口径，台词容量按"时长 − 余量"核算。
   - `negative_prompt` 不要写（cfg=1.0 下无效，C1）。
2. `references` 编号必须从 1 起**唯一且连续**（E1）；提示词中出现的 `<Picture N>` 必须都在 `references` 中定义，且编号顺序与首次引用顺序一致（T-2）。占位槽放末位（E1 修正）。
3. 段名顶格起行、以冒号结尾，顺序固定。Ref2VA：`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`；FL2VA：`integrated_multimodal_description` → `overall_soundscape` → `non_diegetic_music`。两种方言不得混用。
   `non_diegetic_music:` **不得为空**：没有配乐就显式写 `N/A`——没写不等于静音，模型会自填通用配乐（〔外部调研·F-ZEN-07〕：写 N/A 的 14 次无配乐，省略的 3 次中 2 次有配乐）。
4. 对白：`<d>[Chinese] 台词</d>`，同一行前文必须出现说话人 ID（如 `[S1]`）。画面 ≥2 个主体且有对白时，必须为不说话的人写一句闭嘴句（如 `[S2] does not speak; his lips remain completely closed.`），否则口型会落到错的人身上（〔外部调研·F-ZEN-08〕：不写 3 次中 2 次落错，写后 3/3 正确）；非说话人背身/出画/无脸时可免。
   Ref2VA 中慎用首帧脚手架句（`[keyframe completion]`、`<Picture N> is the first frame`、`begins in the position and framing established by`）：社区实测运镜约减半（〔外部调研·F-H3-11〕）。如本镜需要明显运镜，改用 reference generation 表述；如本镜需要钉死构图/轴线（A5），可保留。
5. 禁令包（M8）：代码块最后一行固定为 `No captions, subtitles, or dialogue text overlays appear at any moment.`（D1）；含动作的镜必须含 `Real-time speed throughout, no slow motion`（A3），除非元数据加 `- 慢动作: 设计选择（理由…）`。
6. `锚点` 中列出的每个资产，其锚点句 EN 必须**逐字**出现在 `subject_definitions` 中（P1）。
7. 画面中 ≥2 个人物时，`subject_definitions` 或 `detailed_description` 必须有差异化描述句（B3），宽景中人物用画面位置称呼（A5②）。

> 说明：六段结构是委托方在 ComfyUI 中使用的 H3 提示词方言（T-2），即官方 Ref2VA 方言；FL2VA 用三段。若你的节点要求 JSON，按同名键一一转换，**内容规则不变**。

脚本：`prompt_lint.py`（模式与方言/结构/禁令包/锚点/对白标记/参考编号/闭嘴句/配乐 N/A/步数）、`direction_audit.py`（方位词审计）、`slot_order_check.py`（参考槽连续性）、`dialogue_capacity.py`（从 `<d>` 中取台词核算容量）。

---

## 3. 锚点卡（`anchors.md`）

```markdown
## ANCHOR: CHR-SUXIAO
- 类型: 角色
- 锚点句 EN: `a slender 17-year-old girl with ... (一段英文，所有提示词逐字嵌入)`
- 必现: 发色…；服装…；标志物…
- 禁用: no jewelry at all; no armor; ...
- 方位属性: 左手持刀（画面方位需单独放大核验）
- 来源依据: 原著第 x 章 "……"
- 板图: assets/boards/CHR-SUXIAO-BOARD.png（seed 4 定稿；落选 seed 1/2/3 归档于 assets/boards/_rejected/）
```

规则：`锚点句 EN` 一行、用反引号包裹、不可换行；`禁用` 必须写成**绝对否定句**（`no X`），因为本管线 negative_prompt 无效（C1、T-2）；`方位属性` 有则必填（C1-6、C1-7）。

---

## 4. 剪辑单（`edit-list.md`）

| 列名 | 规则 |
|---|---|
| `CUT` | `CUT-nnn` |
| `来源` | 相对本集目录的路径；纯色卡写 `local:black` / `local:white` / `local:#RRGGBB`（D2：纯色画面本地生成，不送生成器） |
| `入点` / `出点` | 秒，两位小数 |
| `字幕` | 逐字取自剧本（P7）；无则 `—` |
| `画面文字` | 叠层字卡文字（由剪辑程序化叠加，绝不交给生成器，D1/D2）；无则 `—` |

脚本：`asset_exists.py`（全部 `来源` 存在；旧集号路径残留扫描，E2）。

---

## 5. 转写对账输入（`transcripts.tsv` 或 `.json`）

- TSV：每行 `SHOT-012<TAB>转写文本<TAB>置信度(可选 0–1)`。
- JSON：`{"SHOT-012": {"text": "…", "confidence": 0.62}}` 或 `{"SHOT-012": "…"}`。
- 剧本侧台词取自 `storyboard.md` 的 `对白` 列，提示词侧取自 `video-prompts.md` 的 `<d>` 标记 → 三方对账（P7）。

脚本：`transcript_reconcile.py`（三方逐字对账、低置信词多窗复核提示、已知 ASR 幻觉黑名单，D5）。

---

## 6. 验收记录（`qc/<SHOT-nnn>.md`）

验收记录不是一句"通过"（C2）。证据文件名**按脚本实际产出的命名**写（统一用 `--out-dir qc/SHOT-004`）：

| 证据 | 产出命令 | 实际文件 |
|---|---|---|
| 接触表 + 旁车 | `contact_sheet.py SHOT-004.mp4 --out-dir qc/SHOT-004` | `qc/SHOT-004/SHOT-004.contact.jpg`、`qc/SHOT-004/SHOT-004.contact.json`（每格帧号/时间/角色、尾部格） |
| 放大裁剪 | 同上加 `--crop face=x:y:w:h` | 拼图 `qc/SHOT-004/SHOT-004.crop-face.jpg`；逐帧 `qc/SHOT-004/SHOT-004.crops/face/f00129_t5.38.png`（`f<帧号5位>_t<秒>.png`） |
| PSNR 扫描 | `psnr_scan.py SHOT-004.mp4 --json > qc/SHOT-004/SHOT-004.psnr.json` | psnr_scan **不自己写文件**，证据就是重定向的 `--json` 输出；按此约定命名 |

不给 `--out-dir` 时 contact_sheet 把文件写在视频旁（`<视频名>.contact.jpg`）。最少包含：

```markdown
# QC SHOT-004 · seed 3 · 2026-10-06
- 结论: 通过 / 不通过 / 有条件通过（条件…）
- 证据: qc/SHOT-004/SHOT-004.contact.jpg; qc/SHOT-004/SHOT-004.crop-face.jpg; qc/SHOT-004/SHOT-004.psnr.json
| 检查项 | 结果 | 证据 |
|---|---|---|
| R-VID-xx 无烧录文字 | ✅ | SHOT-004.contact.jpg 全 12 格 |
| ... | | |
- 复验人: 独立评审会话 / 日期（高风险资产必填，C2）
```

---

## 7. 版本与改名

- 改集号、改镜号必须走**全仓替换 + `asset_exists.py` 全量复查 + 重渲**（E2）；替换要保持行尾零扰动（二进制级替换，不得把 LF 变 CRLF）。
- 已验收产出若与提示词不一致，必须把提示词**回写**成产出的事实（E4），参考图与提示词必须是同一事实。
