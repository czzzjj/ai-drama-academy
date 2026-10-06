# 关键帧冻结提示词 · S<nn>E<nn>

<!-- 产出路径：season-01/epNN/keyframe-prompts.md；定稿图 keyframes/REF-SHOTnnn-START.png，落选归档 keyframes/_rejected/。
     技能：keyframe-freeze（主）、performance-direction（表情起点句）。闸门：R-KF-01–R-KF-20；验收记录用 qc-record.md 的关键帧节。
     每镜一节；六行顺序固定，每行一句类型，不得合并。 -->

## SHOT-<nnn>
- 关键帧: REF-SHOT<nnn>-START
- 尺寸: 1536×2752（9:16；若用其他尺寸，写明送入前的裁切方式）
- 画面级目标: <一句话：这一帧要让观众一眼读出什么>（R-KF-08）
- 起始帧方位: <名=LEFT; 名=RIGHT>（与分镜一致，R-KF-05）
- 动作链起点: <本镜 内容 的第一相：预备姿态>（R-KF-14）
- 锚点: <CHR-xxx; LOC-xxx; PRP-xxx>
- seed 记录: <seed 1 / 2 / 3 / 4；batch_index；steps>（高风险镜 ≥3 seed 并排，R-KF-03、R-KF-20）

```text
[1 风格锁] <visual-bible 风格锁句，逐字>
[2 构图] Vertical 9:16 frame, <机位高度>, <景别>; <主体 A 在画面哪一区域、占多大>, <主体 B ……>.
[3 位置+锚点] On the LEFT, <CHR-xxx 锚点句 EN 逐字>, <姿态：动作链起点>. On the RIGHT, <CHR-yyy 锚点句 EN 逐字>, <姿态>, <表情起点：眉/眼/嘴>.
[4 场景] <LOC-xxx 锚点句 EN 逐字>; <本镜特有的可见场景细节>.
[5 光] <被动光描述：cold light falls from the upper LEFT>, <光比档>, palette of <本段命名色 3–5 个，逐字>.
[6 差异/人群/禁用] <The two figures have clearly different faces, builds and silhouettes.> <人群：a heavily blurred dark mass with no distinguishable faces.> <正向状态句 + 已证实会被加的物件的 no X>.
```

<!-- 推近/收紧镜：起幅取主体最大的一端（R-KF-09）。关键帧上不得有文字/水印/标签/inset（R-KF-12）。
     定稿后画面与冻结提示词不符 → 回写提示词为画面事实（R-KF-18、E4）。 -->
