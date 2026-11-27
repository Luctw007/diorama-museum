# TASK-321-C 完成报告

> 任务 321-C（01 线）：第二批 SIMH 三槽转 live 条件复核卡 v1。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\第二批SIMH三槽转live条件复核卡_v1.md`（新增，1718 字节 ≥1200）：①三槽逐槽现状表（slot_id/run_status/二进制是否就位/转 live 条件，各列）；②结论（二进制仍未就位 → 维持 dry-run，不转 live）；③转 live 动作登记（一台一台验，不批量）。
- `D:\work\01\repo\01\docs\TASK-321-C_完成报告.md`（本报告）。

## 复核卡自证

- 字节数：1718（>1200 达标）。
- 三槽现状表：simh-hp2100/simh-nova/simh-altair-8800 均 dry-run（MISSING 无二进制），binary_hint 路径成文（altair 名仍标 [需核实]）。
- 结论成文：二进制未就位 → 维持 dry-run 不转 live；转 live 判定口径不变（311-L：二进制就位即 live，release_check 无需改码）。
- 转 live 动作登记：一台一台验（单槽放置后单独 --list + release_check 确认），01 线不代编译不代放置。

## 与任务书的漂移

1. 三槽现状与 311-L 预检卡一致（无变化）：本轮复核确认无漂移，不重复登记转 live 判定细则（引用 311-L）。
2. 验收命令第 2 条同时贴 release_check R2 第二批三槽 dry-run [PASS]（任务书要求）——复跑佐证「dry-run 判合法」。
3. 执行备注：验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。

4. 转 live 条件复核与 311-L 预检卡逐条一致（binary_hint 路径/判定口径/altair 名待核实三处均未变化），本轮复核确认无漂移后维持登记。5. 用户侧动作不变：编译并放置二进制至各槽位 third_party/simh/<target> 路径，01 线不代做。

6. 本卡字节数与字数均达标（1718 字节）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：77/77 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== slot_loader.py --list（节选：三槽 MISSING 现状）==
simh-altair-8800   MISSING(无二进制)  ...
simh-hp2100        MISSING(无二进制)  ...
simh-nova          MISSING(无二进制)  ...
SLOT_RC=0

== release_check.py（R2 第二批三槽 dry-run 行 + 汇总）==
[PASS] R2 第二批槽位 simh-hp2100 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
