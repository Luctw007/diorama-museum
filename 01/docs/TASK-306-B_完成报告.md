# TASK-306-B 完成报告

> 任务 306-B（01 线）：F-16 R5-b 排期状态登记校验实装（release_check.py，信息级）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\scripts\release_check.py`（修改）：新增 `check_r5b()`；`main()` 在 `check_r5a()` 后调用。判据：读台账最新版 §② 表格，逐行 F-7~F-16 检查「状态/责任线」与验收口径列（待实机条数登记处）非空、F-13/F-14 阻塞点已登记（§④ 两行成文）；`R5_HARD=False` 时打印 `[INFO] R5-b ...` 不计 rc，`True` 时走 `mark()`。
- `D:\work\01\repo\01\docs\TASK-306-B_完成报告.md`（本报告）。

## 实装自证

- 函数：`check_r5b()` 经 `_ledger_section_rows(ledger, "②")` 取 §② 表行，cells 列 = 项/状态责任线/前置/轮次/验收口径/实机依赖，检查 cells[1]（责任线）与 cells[5]（验收口径）非空；`_ledger_section_rows(ledger, "④")` 取 §④ 表核对 F-13/F-14 阻塞点列非空。
- 调用点：`main()` 中 `check_r5a()` 之后调用 `check_r5b()`。

## 与任务书的漂移

1. 「待实机条数」落地为台账 §②「验收口径」列非空：v6/v7 台账 §② 无独立「待实机条数」列，条数登记在验收口径列（如 F-7「待实机 6 条」、F-15「三表 35 格」）——以仓库实际列结构落地，判据语义不变。
2. §④ 阻塞点只核 F-13/F-14 两行（任务书范围），F-16 行阻塞点不参与本断言。
3. 执行备注：验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。
4. 门禁数字较任务书背景更新：verify_all 本轮 61/61（基线 60/60，完工包 52→54 两包入账）；release_check R3 完工包 54 ≥ 30、R2 五槽位全绿（三台 live + 第二批 SIMH dry-run）——与本件无关的数字增量属他线产包进账，如实登记不臆造。
5. R5-b 当前复跑 10/10 行全部成文（F-7~F-16 责任线与验收口径均非空），信息级零异常行。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R5-a/b 两行 + 汇总）==
[INFO] R5-a 台账 全馆功能排期台账_v7.md §① F-1~F-6 销账登记 6/6 行状态+产物成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-b 台账 全馆功能排期台账_v7.md §② F-7~F-16 排期登记 10/10 行成文（信息级，R5_HARD=False 不计 rc）
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
