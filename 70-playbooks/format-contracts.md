# 文档格式契约（Format Contracts）

> 这是**脚本与文档之间的接口**。[`50-rubrics/scripts/`](../50-rubrics/scripts/) 中的检查脚本按本文件解析制作文档；[`70-playbooks/templates/`](templates/) 中的模板按本文件生成。改契约 = 同时改脚本、模板、fixtures，三者必须同一次提交。
> 溯源：P7（双文档对账）、E1（槽位顺序）、E2（路径残留）、D3（对白容量）、A5（方位审计）〔委托方实证〕。

## 0. 通用规则

1. 文件编码 UTF-8，换行 LF。文件名用英文（`storyboard.md`、`video-prompts.md`…），中文名可作为标题（E3-1：中文路径在 cmd 下会吞输出）。
2. 一集一个目录：`season-01/ep03/`，其下放该集全部文档；素材放 `season-01/ep03/assets/`。
3. **Markdown 表格解析规则**：脚本寻找"表头行包含契约列名"的管道表；列顺序不限；多余列忽略；单元格内 `|` 必须写成 `\|`；空值统一写 `—`。
4. ID 规则：镜号 `SHOT-012`（三位数字，集内唯一）；段号 `SEQ-03`；资产 ID `CHR-` 角色 / `PRP-` 道具 / `LOC-` 场景 / `SYM-` 符号；参考图 ID `REF-SHOT012-START`（起始帧）、`CHR-SUXIAO-BOARD`（板图）。
5. 时长单位：秒，保留两位小数；帧数必须落在 H3 帧网格 `17k+5`（k=7…21，即 124…362 帧，24 fps）上，由 `h3_frame_grid.py` 校验/吸附。

---

## 1. 分镜表（`storyboard.md`）

必需列：

| 列名 | 类型 | 规则 |
|---|---|---|
| `段号` | `SEQ-nn` | 一个段 = 一条完整动作链/一场戏的一个单元（A1、P10） |
| `镜号` | `SHOT-nnn` | 集内唯一 |
| `时长(s)` | 数字 | 送 H3 的镜 ≥ 5.17（124 帧下限，T-2）；< 5 必须填 `短镜理由` |
| `拍数` | 整数 | 段内 2–3 拍为常态（P10）；>3 拍需在 `内容` 中说明空间如何不跳变（A5③） |
| `内容` | 文本 | 写**事件**不写形容词（M3）；动作链用 `→` 串联 |
| `运镜` | 文本 | 只写一种主运动 + 方向维度（高度/距离/左右） |
| `运镜因果` | 文本 | 必须是"因为 X，所以镜头 Y"句式（A4）；静止镜写"因为……，所以不动" |
| `起始帧方位` | `名=LEFT; 名=RIGHT` | 取值 `LEFT` / `RIGHT` / `CENTER` / `FG` / `BG`；无人物写 `—` |
| `对白` | 文本 | 多句以 ` / ` 分隔，每句 `说话人：台词`；无对白写 `—` |
| `短镜理由` | 文本 | 时长 < 5s 时必填，否则 `—` |

示例：

```markdown
| 段号 | 镜号 | 时长(s) | 拍数 | 内容 | 运镜 | 运镜因果 | 起始帧方位 | 对白 | 短镜理由 |
|---|---|---|---|---|---|---|---|---|---|
| SEQ-02 | SHOT-004 | 10.83 | 3 | 苏晓佯攻右肩→神抬臂格挡落空→苏晓矮身抓隙斩腿 | 缓推→接触瞬间顿挫 | 因为接触发生，所以推近在接触帧顿住强调力量 | 神=LEFT; 苏晓=RIGHT | 苏晓：就是现在！ | — |
| SEQ-02 | SHOT-005 | 5.88 | 2 | 神踉跄后退→跪地，地面裂纹扩散 | 上摇→拉回 | 因为神倒下，所以拉回交代全局后果 | 神=LEFT; 苏晓=RIGHT | — | — |
```

脚本：`segment_rhythm.py`（段长/短镜/拍数）、`dialogue_capacity.py`（对白容量）、`direction_audit.py`（与提示词交叉核对方位）。

---

## 2. 视频提示词（`video-prompts.md`）

每镜一个二级标题 `## SHOT-nnn`，下接**元数据列表**与**一个 `h3` 代码块**：

````markdown
## SHOT-004
- 时长: 10.83
- 帧数: 260
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
  ...
No captions, subtitles, or dialogue text overlays appear at any moment.
```
````

规则：
1. 元数据键固定：`时长`、`帧数`、`first_frame`、`references`、`起始帧方位`、`轴线策略`、`锚点`（锚点资产 ID，分号分隔）、`角色映射`（说话人/主体 ID → 分镜表中的角色名，如 `S1=苏晓; S2=神`；画面 ≥2 人时必填，方位审计靠它把提示词与起始帧方位对上）。
   可选键：`慢动作: 设计选择（理由…）`（豁免实时速度句，A3）；`换边: 设计（理由…；起始帧支持证据…）`（豁免单轴定侧，A5）；`negative_prompt` 不要写（cfg=1.0 下无效，C1）。
2. `references` 编号必须从 1 起**唯一且连续**（E1）；提示词中出现的 `<Picture N>` 必须都在 `references` 中定义，且编号顺序与首次引用顺序一致（T-2）。占位槽放末位（E1 修正）。
3. 六段名顶格起行、以冒号结尾，顺序固定：`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`。
4. 对白：`<d>[Chinese] 台词</d>`，同一行前文必须出现说话人 ID（如 `[S1]`）。
5. 禁令包（M8）：代码块最后一行固定为 `No captions, subtitles, or dialogue text overlays appear at any moment.`（D1）；含动作的镜必须含 `Real-time speed throughout, no slow motion`（A3），除非元数据加 `- 慢动作: 设计选择（理由…）`。
6. `锚点` 中列出的每个资产，其锚点句 EN 必须**逐字**出现在 `subject_definitions` 中（P1）。
7. 画面中 ≥2 个人物时，`subject_definitions` 或 `detailed_description` 必须有差异化描述句（B3），宽景中人物用画面位置称呼（A5②）。

> 说明：六段结构是委托方在 ComfyUI 中使用的 H3 提示词方言（T-2）。若你的节点要求 JSON，按同名键一一转换，**内容规则不变**。

脚本：`prompt_lint.py`（结构/禁令包/锚点/对白标记/参考编号）、`direction_audit.py`（方位词审计）、`slot_order_check.py`（参考槽连续性）、`dialogue_capacity.py`（从 `<d>` 中取台词核算容量）。

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

验收记录不是一句"通过"（C2）。最少包含：

```markdown
# QC SHOT-004 · seed 3 · 2026-10-06
- 结论: 通过 / 不通过 / 有条件通过（条件…）
- 证据: qc/SHOT-004/contact.jpg; qc/SHOT-004/crop-face.png; qc/SHOT-004/psnr.json
| 检查项 | 结果 | 证据 |
|---|---|---|
| R-VID-xx 无烧录文字 | ✅ | contact.jpg 全 12 帧 |
| ... | | |
- 复验人: 独立评审会话 / 日期（高风险资产必填，C2）
```

---

## 7. 版本与改名

- 改集号、改镜号必须走**全仓替换 + `asset_exists.py` 全量复查 + 重渲**（E2）；替换要保持行尾零扰动（二进制级替换，不得把 LF 变 CRLF）。
- 已验收产出若与提示词不一致，必须把提示词**回写**成产出的事实（E4），参考图与提示词必须是同一事实。
