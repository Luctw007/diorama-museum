# TASK-321-S 完成报告

> 任务 321-S（01 线）：门禁基线复核卡 v1（verify/release 基线核对）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\门禁基线复核卡_v1.md`（新增，>1200 字节）：①两门禁基线复核表（verify_all 通过数/release_check R1~R5，各列：门禁/316 基线/321 复跑/是否漂移）；②结论（77/77 + 硬断言 FAIL 0 无漂移，作为 321 新基线）；③残留/降级口径登记（R4 信息级、R5-a~e 信息级）。
- `D:\work\01\repo\01\docs\TASK-321-S_完成报告.md`（本报告）。

## 复核卡自证

- 字节数：>1200 达标。
- 基线复核两行：verify_all 73/73 → **77/77**（完工包 65→69 他线入账，非 01 线漂移）；release_check 硬断言 FAIL 0 无漂移（R1 77/77、R3 69≥30 wip 2 只打印、R5-a/b 读 v10、R5-c 读 v6）。
- 结论成文：77/77 + FAIL 0 为 321 新基线；本轮修复项登记（_latest_doc 数字排序）。
- 残留/降级口径三条登记（R4 1 处合法骨架/R5-a~e 信息级/R3 wip 只打印）。

## 与任务书的漂移

1. 任务书②预期基线 73/73——实际复跑 77/77（他线完工包 +4 入账，含 apple-ii-joystick/frogger-arcade 在制 wip 2 个只打印），按实况登记。
2. **本轮修复 _latest_doc 版本解析**（v10 误判修复）：修复后 R5-a/b 读台账 v10、R5-c 读汇总 v6——基线复核卡的「无漂移」结论建立在修复后复跑上。
3. 执行备注：验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。

4. 新基线 77/77 的构成说明：他线完工包 65→69（+4 包入账）+ 8 步不变——与 01 线本轮纯文档轮（除 _latest_doc 修复）无代码改动的实况一致。5. 本卡字节数与字数均达标。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：77/77 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R1~R5 + 汇总，修复后复跑）==
[PASS] R1 验收基线 77/77 通过（2026-11-27 23:05:43）
[INFO] R3 wip 清单（不计入 rc）：apple-ii-joystick, frogger-arcade
[PASS] R3 完工包 69 ≥ 30
[INFO] R4 残留扫描完成：命中 1 处（含骨架注记与新发现，只暴露不计 rc）
[INFO] R5-a 台账 全馆功能排期台账_v10.md §① F-1~F-6 销账登记 6/6 行状态+产物成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-b 台账 全馆功能排期台账_v10.md §② F-7~F-16 排期登记 10/10 行成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-c 汇总卡 F系列待实机清单汇总_v6.md 合计 69 vs 母本 9 行加和 69 一致（信息级，R5_HARD=False 不计 rc）
[INFO] R5-d 封版文档齐备性 9/9 文件在案（信息级，R5_HARD=False 不计 rc）
[INFO] R5-e 残留扫描 8 文件：命中 0 处（无臆造残留）（恒不计 rc）
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
