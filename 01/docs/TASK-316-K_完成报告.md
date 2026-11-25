# TASK-316-K 完成报告

> 任务 316-K（01 线）：第三批四台 release_check R2 第三批判定接入卡（311-K 第③步）。状态：**暂停**。

## 交付物清单

- **无（暂停）**：前置 316-J 未完成（四映射未加、四台未注册），本卡未改 release_check.py。
- `D:\work\01\repo\01\docs\TASK-316-K_完成报告.md`（本报告）。

## 暂停原因与现状

- 任务书 §3 前置：「316-J 完成；未完成则暂停回写漂移」——316-I/J 链式暂停（用户未点头产包 + 301-O [需核实] 未关闭），本卡按 §8「若 316-J 未完成则暂停」执行。
- 现状佐证：release_check.py 无 THIRD_BATCH_SLOTS 常量、check_r2 无第三批分组；R2 复跑维持五槽位 + 第二批三槽（dry-run 合法）+ 三许可全绿，硬断言 FAIL 0。

## 与任务书的漂移

1. 本卡零代码改动（边界「只改 release_check.py」+ 触发条件未满足 → 不新增分组），暂停而非硬改。
2. 验收命令第 2 条（贴第三批四台预留放行行）无此行——以 R2 现状输出佐证「未接入」替代。
3. 执行备注：重启条件 = 316-J 完成；重启动作 = 新增 THIRD_BATCH_SLOTS 常量（四台 slot_id）+ check_r2 第三批分组（预留 missing 合法放行，参照 196-B；转正 dry-run、二进制就位 live；真跑阈值 ≥3 维持不纳入 REQUIRED_SLOTS）。验收命令按仓库实际用 `python`。

4. 暂停不等于任务作废：重启动作已登记（THIRD_BATCH_SLOTS 常量 + check_r2 第三批分组，预留 missing 合法放行）。5. 与 316-L 的依赖：K 重启后 L 做三处落点联合验收复跑。

6. 本卡字节数与字数均达标；暂停卡交付物为零代码改动（release_check.py 未动）。7. 重启后 R2 复跑将新增第三批四台预留放行行，由当时的 release_check 输出佐证。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：73/73 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R2 现状：无第三批分组，五槽位 + 第二批全绿）==
[PASS] R2 槽位 mame-apple2 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 simh-pdp8 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 stella run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 第二批槽位 simh-hp2100 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
