# QC SHOT-<nnn> · seed <n> · <YYYY-MM-DD>

<!-- 产出路径：season-01/epNN/qc/SHOT-nnn.md（板图/关键帧验收用 qc/<ASSET-ID>.md，同结构）。技能：shot-qc（主）、asset-boards、keyframe-freeze、performance-direction。
     契约：70-playbooks/format-contracts.md §6——验收记录不是一句"通过"（C2）；证据文件名按脚本实际产出写，统一 --out-dir qc/SHOT-nnn。 -->
- 结论: <通过 / 不通过 / 有条件通过（条件…）>
- 证据: qc/SHOT-<nnn>/SHOT-<nnn>.contact.jpg; qc/SHOT-<nnn>/SHOT-<nnn>.crop-face.jpg; qc/SHOT-<nnn>/SHOT-<nnn>.psnr.json
- 生成日志: 模式 <Ref2VA/FL2VA>；seed <n>（候选 <…>）；steps <20>；turbo <否>（R-VID-19）
- 背景元素清单（看视频前写，R-VID-02）: <关键帧中每个显著元素及位置>

| 检查项 | 结果 | 证据 |
|---|---|---|
| R-VID-01 接触表含起始关键帧 + FIRST/MID/TAIL | <✅/❌> | SHOT-<nnn>.contact.jpg |
| R-VID-03 TAIL 无崩解 | <> | 同上 TAIL 格 |
| R-VID-04 多人时脸不雷同 | <> | SHOT-<nnn>.crop-face.jpg |
| R-VID-05 主角脸与板图同一人 | <> | 裁脸 vs CHR-<NAME>-BOARD 并排 |
| R-VID-07 全格无文字/字幕/水印 | <> | 接触表全 <n> 格 + burnin 报告 |
| R-VID-08 PSNR 死段已解释或剪掉 | <> | SHOT-<nnn>.psnr.json |
| R-VID-09 台词三方对账无 error | <> | transcript_reconcile 报告 |
| R-VID-13 不说话的人嘴部闭合 | <> | 口型裁剪 |
| R-VID-14 左右位置与起始帧方位一致 | <> | 首/中/末格 |
| R-VID-15 实时速度 | <> | 接触表时间码 |
| R-VID-16 禁用项在 MID/TAIL 放大裁剪中不存在 | <> | SHOT-<nnn>.crops/<区域>/ |
| R-VID-17 运镜因果的事件 X 可见且 Y 发生在 X 时 | <> | 接触表 |
| R-VID-22 N/A 镜无配乐 | <> | 听感记录 |

## 提示词 ↔ 产出差异（R-VID-18）
| 差异 | 结论（回写提示词 / 重出 / 设计接受） |
|---|---|
| <提示词写短距离，产出为长竖线> | <回写提示词（E4）> |

<!-- 判"重出/缺句/误听"必须同时引用转写证据和抽帧或听感证据（R-VID-11、D5）；换 seed 仍缺同句 → 不再抽卡，开缺陷单回流分镜时长（R-VID-12、D3）。 -->
- 复验人: <独立评审会话 ID / 日期>（高风险资产与镜头必填，C2）
