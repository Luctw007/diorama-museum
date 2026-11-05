# TASK-119 完成报告（defects 索引自动生成脚本）

## 交付物
- `gen_defects_index.py`（新增）：扫描 `01/docs/defects/DEFECT-RUN-*.md`，提取编号/标题/状态/修复提交/关联任务，生成索引表；纯文本解析，对缺字段可降级（缺状态按 open、缺提交/任务留"-"，不崩溃）；`--dry-run` 只打印不写。
- `01/docs/defects/index.md`：脚本生成产物（含"自动生成，勿手工编辑"抬头），未手工编辑；缺陷原始文档内容未改。

## 验收证据
- `python 01/scripts/gen_defects_index.py`
```text
DEFECT-RUN-01 [closed] 实机首验缺陷 · closed（提交 - · 任务 -）
DEFECT-RUN-02 [closed] …（提交 ba72577）  … 03 dd67bfb / 04 92b1b0d / 05·06 02dd2d7
DEFECT-RUN-07 [open] 实机首验缺陷 · 修复待用户确认（提交 d85e0f9）
已生成 D:\work\01\repo\01\docs\defects\index.md
计 7 条：closed 6 / open 1（缺状态按 open 计）   rc=0
```
- 生成的 index.md 首表片段
```text
| 编号 | 标题 | 状态 | 修复提交 | 关联任务 |
|---|---|---|---|---|
| DEFECT-RUN-01 | 实机首验缺陷 · closed | closed | - | - |
| DEFECT-RUN-02 | 实机首验缺陷 · closed | closed | ba72577 | - |
```

## 与任务书预期的漂移（如实记录）
任务书前置称"7 条状态行均含 closed"、验收预期"closed 7 / open 0"；实际 DEFECT-RUN-07 状态为"修复完成 · 待用户重测确认（用户确认后置 closed）"→ 脚本如实计 closed 6 / open 1（待确认），并在待确认标记（"待用户/待重测"）优先于"置 closed"字样判定。建议统筹在 RUN-07 实机确认后更新其状态行，重跑本脚本即自动翻为 7/0。