# 维护者入口（在本仓库内写作的 agent 必读）

本仓库是「AI 短剧制作学院」：一个给 agentos 装载的前置课程包，**读者是 agent，不是人**。

开始写之前：
1. 读 [`CONVENTIONS.md`](CONVENTIONS.md)：编号体系、文件地图、来源标注、格式契约，这些都会被机器校验。
2. 委托方的一手证据只在 [`00-orientation/client-dossier.md`](00-orientation/client-dossier.md)。凡标 `〔委托方实证〕` 的内容必须能追溯到它的编号；不得编造人类原话、数字或 URL。
3. 外部资料只引用 [`80-sources/catalog/`](80-sources/catalog/) 中已核实的条目（`S-<CODE>-nn`）。
4. 每条内容都要落到"agent 下一次生成/验收时的具体动作"（→ 行为改变）。

提交前运行：
```bash
python3 tools/academy_lint.py
python3 50-rubrics/scripts/run_all_selftests.py
```

如果你是来**学习**（而不是维护）本学院的 agent，入口是 [`90-curriculum/entry-prompt.md`](90-curriculum/entry-prompt.md)。
