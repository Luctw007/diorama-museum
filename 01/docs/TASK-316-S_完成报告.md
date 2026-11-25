# TASK-316-S 完成报告

> 任务 316-S（01 线）：回归测试矩阵 v5（316 轮次新接线点静态用例扩展）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\回归测试矩阵扩展_v5.md`（新增另存，2644 字节 ≥1500；v4 保留原文）：①两处新接线点清单（P12 player.gd focus_requested→tween 接线、P13 release_check 第三批 R2 分组）；②每处用例表（P12 四条：符号存在/连接存在/tween 时长/命名纪律；P13 三条：常量存在（暂停态）/分组放行（设计态）/阈值留白）；③回归复跑记录（gd 自检 + verify_all + release_check）。
- `D:\work\01\repo\01\docs\TASK-316-S_完成报告.md`（本报告）。

## 矩阵自证

- 字节数：2644（>1500 达标）。
- P12 用例四条：R-316-01（player funcs=5 + focus_requested 入池）、02（点号连接不进符号池）、03（tween 时长取 duration + clampf 防御）、04（命名 FAIL 0）。
- P13 用例三条：R-316-05（THIRD_BATCH_SLOTS 当前不存在——记「暂停待落地」）、06（预留 missing 合法/转正 dry-run/二进制 live，311-K 第③步口径）、07（阈值 ≥3 维持留白）。
- 复跑记录引用干净重跑日志（2026-11-26：gd 185 MISS 0、verify 73/73、release_check rc=0）。

## 与任务书的漂移

1. P13 用例记「暂停待落地」（316-K 触发条件未满足未落地）——任务书 §2 已预留此口径（「P13 若 316-K 未落地则记暂停待落地」），用例改按设计态断言（311-K 预案口径）成文，落地后复跑即验。
2. P13 用例数 3 条（任务书「每处 2-4 条」上限内），含「阈值留白」设计态断言。
3. 执行备注：只写用例+复跑，不改引擎/脚本（边界遵守）；验收命令按仓库实际用 `python`；三条命令串行干净复跑，日志见下。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：73/73 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd 自检 ==
汇总：17 文件；符号池 funcs 185 / signals 8；MISS 0；已知缺口 KG 0
扫描 17 个 gd；class_name 7 个；FAIL 0

== release_check.py（汇总）==
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
