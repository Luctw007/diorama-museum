# TASK-306-D 完成报告

> 任务 306-D（01 线）：F-16 R5-d 封版文档齐备性实装（release_check.py，信息级）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\scripts\release_check.py`（修改）：新增 `check_r5d()`；`main()` 在 `check_r5c()` 后调用。判据：逐文件检查存在性——docs/README.md、docs/RELEASE-v0.1.md、docs/全馆功能排期台账（最新版）、docs/F系列待实机清单汇总（最新版）、docs/F1F2实机验收单_v1.md、docs/godot_first_boot.md、licenses/{MAME,SIMH,Stella}.md；`R5_HARD=False` 时打印 `[INFO] R5-d ...` 不计 rc，`True` 时走 `mark()`。
- `D:\work\01\repo\01\docs\TASK-306-D_完成报告.md`（本报告）。

## 实装自证

- 函数：`check_r5d()` 组七类必查文件清单（六项固定名 + 台账/汇总两项经 `_latest_doc` 取最新版）+ `LICENSES` 三份许可（复用 R2 常量），逐项 `os.path.isfile` 判定，缺失项列 `os.path.relpath` 相对路径；出口走 `_r5_report("R5-d", ...)`。
- 复跑：9/9 文件在案（301-G 核对卡七类 + 三许可无缺口，机器断言落地替代人工核对）。

## 与任务书的漂移

1. 台账/汇总按「最新版」解析（当前 v7/v3），任务书母本所列固定文件名是 301-G 时期的 v5/v1——实装为动态取最新版，符合「封版时以最新版为对照」口径。
2. 三份许可复用 R2 的 `LICENSES` 常量（licenses/{MAME,SIMH,Stella}.md），未重复造清单。
3. 执行备注：只检查存在性、不新建/不补文档（边界遵守）；验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。
4. 机器断言落地后 301-G 人工核对卡由 R5-d 替代：同一清单（七类必查文件 + 三份许可）从人工核对转为机器断言，转硬后即封版文档齐备性判定；当前信息级只暴露缺失。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R5-a/b/c/d 四行 + 汇总）==
[INFO] R5-a 台账 全馆功能排期台账_v7.md §① F-1~F-6 销账登记 6/6 行状态+产物成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-b 台账 全馆功能排期台账_v7.md §② F-7~F-16 排期登记 10/10 行成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-c 汇总卡 F系列待实机清单汇总_v3.md 合计 69 vs 母本 9 行加和 69 一致（信息级，R5_HARD=False 不计 rc）
[INFO] R5-d 封版文档齐备性 9/9 文件在案（信息级，R5_HARD=False 不计 rc）
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
