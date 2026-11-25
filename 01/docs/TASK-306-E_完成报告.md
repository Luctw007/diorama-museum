# TASK-306-E 完成报告

> 任务 306-E（01 线）：F-16 R5-e 残留扫描 + R5-f 扩展自守实装（release_check.py）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\scripts\release_check.py`（修改）：新增 `check_r5e()` 与 `check_r5f()`；`main()` 在 `check_r5d()` 后依次调用。R5-e 判据：扫描汇总卡与七张执行卡文本，命中「已通过/已验证」未实机项即打印 `[INFO] R5-e ...`（占位文案白名单除外），恒不计 rc。R5-f 判据：`mark(fails == 0, "R5-f", ...)` 判硬，与既有汇总行语义一致。
- `D:\work\01\repo\01\docs\TASK-306-E_完成报告.md`（本报告）。

## 实装自证

- R5-e：扫描对象 = 汇总卡最新版 + 七张执行卡（301-M/N/O/P/A/B + F1F2 验收单），白名单 `R5_E_WHITELIST = ("静态",)`（放行「实装已通过静态验收」类表述，静态 ≠ 实机）；命中行打印 `文件: 行内容`，恒不调 mark。
- R5-f：`mark(fails == 0, "R5-f", "扩展自守：R1~R5 全硬断言 FAIL %d 处" % fails)`，在 check_r5e 后、smoke/snapshot 前调用（只判 R1~R5 域，不含 SMOKE/SNAP）。

## 与任务书的漂移

1. 白名单落地为「含『静态』的行放行」：F1F2 验收单第 3 行「实装已通过静态验收」命中「已通过」但属静态验收表述，非未实机项臆造——按母本「占位文案白名单」语义放行，复跑命中 0 处。
2. R5-f 调用位置置于 check_r5e 后、run_smoke/run_snapshot 前：保证「R1~R5 全硬断言」语义不含 SMOKE/SNAP 域。
3. 执行备注：验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。
4. R5-e 恒不计 rc 的落地方式：check_r5e 直接 print、不调 mark（连信息级分流都不走），与母本「R5-e 仍信息（扫描只暴露）」且「转硬后仍信息」一致——本件无转硬路径，防臆造扫描始终只暴露不阻断。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R5-a~e + R5-f + 汇总）==
[INFO] R5-a 台账 全馆功能排期台账_v7.md §① F-1~F-6 销账登记 6/6 行状态+产物成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-b 台账 全馆功能排期台账_v7.md §② F-7~F-16 排期登记 10/10 行成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-c 汇总卡 F系列待实机清单汇总_v3.md 合计 69 vs 母本 9 行加和 69 一致（信息级，R5_HARD=False 不计 rc）
[INFO] R5-d 封版文档齐备性 9/9 文件在案（信息级，R5_HARD=False 不计 rc）
[INFO] R5-e 残留扫描 8 文件：命中 0 处（无臆造残留）（恒不计 rc）
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
