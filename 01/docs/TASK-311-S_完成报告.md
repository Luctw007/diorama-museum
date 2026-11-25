# TASK-311-S 完成报告

> 任务 311-S（01 线）：回归测试矩阵 v4（311 轮次新接线点静态用例扩展）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\回归测试矩阵扩展_v4.md`（新增另存，3131 字节 ≥1500；v3 保留原文）：①两处新接线点清单（P10 gateway_client status→set_device_running 接线、P11 AXIS_PRESET + 复位矩阵）；②每处 4 条静态用例表（P10：符号存在/running 通知/静默容错/命名纪律；P11：常量口径/类码优先/复位矩阵全覆盖/无重复写 transform）；③回归复跑记录（gd 自检 + verify_all + release_check）。
- `D:\work\01\repo\01\docs\TASK-311-S_完成报告.md`（本报告）。

## 矩阵自证

- 字节数：3131（>1500 达标）。
- P10 用例四条：R-311-01（gateway_client funcs=16 + has_method set_device_running 存在）、02（running→true/stopped→false）、03（get_node_or_null 判空静默）、04（命名 FAIL 0）。
- P11 用例四条：R-311-05（AXIS_PRESET 七键照 §2，ENC +Y 占位待核实）、06（类码优先 + 零破坏回退）、07（复位矩阵五路径全覆盖）、08（不写 transform）。
- 复跑记录引用干净重跑日志（2026-11-26：gd 184 MISS 0、verify 67/67、release_check rc=0）。

## 与任务书的漂移

1. 用例数每处取 4 条（任务书「每处 2-4 条」上限内），共 8 条——P10 拆出「静默容错」、P11 拆出「无重复写 transform」两条任务书示例未列的断言（均为实装关键语义）。
2. P10 接线点位置记 gateway_client.gd + explode_controller.gd 注释更新（311-G 实装涉及两文件，任务书只列一处）。
3. 执行备注：只写用例+复跑，不改引擎/脚本（边界遵守）；验收命令按仓库实际用 `python`；三条命令串行干净复跑，日志见下。

4. 用例断言数字与干净复跑日志一致（funcs 184 / verify 67/67 / FAIL 0），未臆造；P10/P11 与 v3 的 P8/P9 共同构成当前矩阵全集。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：67/67 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd 自检 ==
汇总：17 文件；符号池 funcs 184 / signals 8；MISS 0；已知缺口 KG 0
扫描 17 个 gd；class_name 7 个；FAIL 0

== release_check.py（汇总）==
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
