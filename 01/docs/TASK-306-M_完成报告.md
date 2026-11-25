# TASK-306-M 完成报告

> 任务 306-M（01 线）：实机卡滚动 · B-4 实测值回写执行卡 v1。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\B4实测值回写执行卡_v1.md`（新增，2347 字节 ≥1200）：①回写步骤清单 4 步（改 L34 占位常量为实测权威值 → B-04 SKIP→PASS 断言（`co_active_max == 实测值` 或 `1 <= co_active_max <= 实测值`）→ F4 预算表 B-04 行更新 → 复跑验证）；②梯度实测回填表单（N=1~5 实测值采集栏，数据格式按 301-A 对齐口径）；③声明「本卡待实测权威值，不执行回写」。
- `D:\work\01\repo\01\docs\TASK-306-M_完成报告.md`（本报告）。

## 执行卡自证

- 字节数：2347（>1200 达标）。
- 回写四步与 301-B 预案逐条对应（改常量/转断言/更新预算表/复跑），未增删。
- 梯度表单 N=1~5 六列（FPS_avg/FPS_min/frame_ms_p99/mem_MB/是否卡顿/激活形态）+ 采集人日期列，与 301-A 三方对齐口径一致。
- 「不执行」声明成文：不执行回写、不改 device_budget_check.py、不转 PASS、不销账 B-4。

## 与任务书的漂移

1. 验收命令 `device_budget_check.py` 复跑确认 B-04 仍 SKIP（默认 3 占位未动），与「不转 PASS」边界一致——日志见下。
2. 回写步骤口径补充「B-05 仍 SKIP」观察项未动（本卡只涉 B-04）。
3. 执行备注：验收命令按仓库实际用 `python`；verify_all 门禁在无他线 python 进程窗口干净复跑，日志见下。
4. device_budget_check 复跑确认回写前基线：B-04 仍 SKIP（默认 3 占位）、PASS 9 行 / SKIP 2 项 / FAIL 0 处 rc=0——与本卡「不执行回写」边界互证。
5. 梯度表单判据补充「N=3 达标则默认 3 成立」（272-B 口径），为回填人提供权威值判读锚点。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== device_budget_check.py（B-04 仍 SKIP 佐证）==
  [SKIP] B-04 co_active_max 同屏激活上限（默认 3，02 线 B-4 待实测——占位）
汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
BUDGET_RC=0
```
