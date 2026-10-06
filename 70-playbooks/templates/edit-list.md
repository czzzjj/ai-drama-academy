# 剪辑单 · S<nn>E<nn>

<!-- 产出路径：season-01/epNN/edit-list.md。技能：edit-and-assemble（主）、sound-design（音频偏移/声音层）。
     契约：70-playbooks/format-contracts.md §4——必需列 CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字；可加 所属段、音频偏移、备注 等多余列（脚本忽略）。
     校验：asset_exists.py edit-list.md --stale-token <旧集号>；psnr_scan.py --mode final --edit-list edit-list.md；loudness_verify.py final/epNN.mp4。 -->

| CUT | 来源 | 入点 | 出点 | 字幕 | 画面文字 | 所属段 | 音频偏移 |
|---|---|---|---|---|---|---|---|
| CUT-001 | local:black | 0.00 | 2.50 | — | <剧名> / <AI 生成标识文字> | SEQ-00 | — |
| CUT-002 | assets/clips/SHOT-001.mp4 | <入点> | <出点 ≤ 生成时长 − 尾部余量> | <逐字取自分镜 对白> | — | SEQ-01 | <+0.00> |
| CUT-003 | assets/clips/SHOT-002.mp4 | <…> | <…> | — | — | SEQ-01 | <L-cut：-0.40> |

<!-- 规则：
- 来源 写相对本集目录的路径；纯色卡写 local:black / local:white / local:#RRGGBB，本地生成，不送生成器（D2、R-CUT-09）。
- 来自生成镜的 CUT，出点必须早于该镜尾部余量起点（R-CUT-13）。
- 字幕 逐字等于分镜 对白（R-CUT-11）；转写只用于定位时间，禁止拿转写当字幕（D5）。
- 画面文字 由剪辑程序化叠加：AI 标识从第 0 帧起 ≥2.5s、字高 ≥ 短边 5%（1080 宽 ≥54px）、位于边或角且避开平台 UI 区（R-PUB-01–R-PUB-04）。
- 快剪从长镜里取：一个生成镜可拆多个 CUT；成片均长不报 A1-mean-short（R-CUT-12）。
- 改集号/镜号后跑 asset_exists.py 全量复查（E2）。 -->
