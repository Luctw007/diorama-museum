# TASK-306-A 完成报告

> 任务 306-A（01 线）：F-16 R5-a 销账状态登记校验实装（release_check.py，信息级）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\scripts\release_check.py`（修改）：新增模块常量 `R5_HARD = False`（注释「F-1~F-15 收口后置 True，见 F16封版扩展口径设计 §②」）；新增 `check_r5a()`；`main()` 在 `check_r4()` 后调用。判据：读台账最新版 §① 表格，逐行 F-1~F-6 检查「状态」∈ {销账, 未销账, 方案销账, 销账+深化} 且「产物（轮次）」非空；`R5_HARD=False` 时打印 `[INFO] R5-a ...` 不计 rc，`True` 时走 `mark()`。
- `D:\work\01\repo\01\docs\TASK-306-A_完成报告.md`（本报告）。

## 实装自证

- 常量：`R5_HARD = False  # F-1~F-15 收口后置 True（设计卡 §② 四项转硬前提）`。
- 函数：`check_r5a()` 经 `_latest_doc("全馆功能排期台账")` 取最新版台账，`_ledger_section_rows(ledger, "①")` 取 §① 表行，状态去空白后与 `R5_STATUS_OK` 比对、产物非空；出口统一走 `_r5_report("R5-a", ...)` 按 R5_HARD 分流 [INFO]/mark。
- 调用点：`main()` 中 `check_r4()` 之后调用 `check_r5a()`。

## 与任务书的漂移

1. 状态字段比对做了去空白归一：台账 F-6 实际写「销账 + 深化」（带空格），301-D 母本集合写「销账+深化」（无空格）——归一后一致，避免误判异常行。
2. 台账路径按「自动取 v 号最大文件」解析（_latest_doc），当前命中 v7（306-Q 产物），比任务书前置所列 v6 新——符合「以最新版路径为准」边界，不臆造。
3. 执行备注：本机无 `py -3.7` 启动器，验收命令按仓库实际改用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。
4. R5-a 复跑口径：check_r5a 单独复跑与门禁内复跑输出一致（6/6 行成文），信息级不触发 rc；转硬后同一函数走 mark 判硬，无需再改代码。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R5-a 新行 + 汇总）==
[INFO] R5-a 台账 全馆功能排期台账_v7.md §① F-1~F-6 销账登记 6/6 行状态+产物成文（信息级，R5_HARD=False 不计 rc）
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
