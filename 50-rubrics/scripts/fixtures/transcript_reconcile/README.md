# fixture · transcript_reconcile 专用

- `transcripts-good.json`：与 `fixtures/good/` 同内容的 JSON 写法（对象与纯文本两种值），期望 0 error 0 warn。
- `w2.tsv`、`w3.tsv`：与 `fixtures/bad/transcripts.tsv` 配套的两个错位时间窗（起点后移 0.4s / 前垫 0.4s 静音）转写结果：
  - SHOT-001：三窗互斥（字幕by索兰娅 / 谢谢观看 / 空）→ 典型 ASR 幻觉（D5 症状一）；
  - SHOT-002：三窗一致缺"一个字都不许忘…湖边再见" → 更可能真实缺句（D3）；
  - SHOT-003："救我"只在主窗出现（另两窗为"就我"/无）→ 误听特征（D5 症状二）。
