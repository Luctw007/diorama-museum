# TASK-261-A 完成报告

## 交付物清单
- **层级精确回放实装**：`explode_controller.gd` 新增 `get_depth_level() -> int`（L213-218）——实际拆解深度分档导出：EXPLODED=1（L1 大部件级，全树按深度爆炸，depth_model §4 口径）、CLOSED/OPENED=0（L0 整机）；L2/L3 需级联爆炸（子树视图）未实装，导出上限 L1 如实回退。
- **inspect_controller 深化**：`_last_exploded_level` 由「进入即 exploded」升级为**退出时按 explode 实际深度分档记录**（L316-320，get_depth_level → _level_label）；新增 `_level_label()`（L336-342，L0-L3 标签）；HUD 诊断行显示「上次拆解:xx(Lx)」（L163-169）。
- 回归：gd 符号 MISS 0（get_depth_level 符号命中）/ 命名 FAIL 0；scene_check/layout 前轮全绿不变。

## 层级分档自证（关键行）
explode_controller.gd L213-218（get_depth_level 导出）；inspect_controller.gd L316-320（退出时记录）、L336-342（_level_label）、L163-169（HUD 显示）。

## 待实装验证清单（如实续挂）
①HUD 观感与位置实机核对（256-A 遗留①）；②拆解中切厅并发视觉（256-A 遗留④，261-B 已出关系说明）；③L2/L3 级联爆炸子树视图未实装——get_depth_level 恒 ≤1，待 54-B 级联实现后自然升级；④回厅续接高亮（256-A 遗留③）归 261-B F-7 预研，不实装。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：54/54 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 层级分档自证：关键行见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 任务书预期 54/54：实测以运行结果为准（完工包数随他线持续增长）。
2. **L2/L3 分档无法实装**：depth_model §4 明确级联爆炸（子树视图）待引擎后续实现，现行状态机仅全树一次爆炸——导出接口上限 L1，不臆造 L2/L3 可达性（红线遵守）。
3. 层级记录点从「进入时」改为「退出时」：进入瞬间状态尚未 EXPLODED，退出时才是实际深度（运行锁回退时得 L0 亦如实记录）。
4. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 47，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 150 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（54 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 47，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 150 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（47 包）        PASS  全部 FAIL 0
结果：54/54 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== explode_controller.gd  [explode_controller] funcs=20 signals=3
== inspect_controller.gd  [inspect_controller] funcs=21 signals=1
   [OK] has_method get_depth_level → 存在
   [OK] has_method get_current_device → 存在
汇总：16 文件；符号池 funcs 150 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 54/54 通过（2026-11-21 22:33:42）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 48 ≥ 30
[PASS] R2 槽位 mame-apple2 已登记后端 gw.emulators.mame_apple2
[PASS] R2 槽位 mame-apple2 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 simh-pdp8 已登记后端 gw.emulators.simh_pdp8
[PASS] R2 槽位 simh-pdp8 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 stella 已登记后端 gw.emulators.stella
[PASS] R2 槽位 stella run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 第二批槽位 simh-hp2100 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 许可记录存在 licenses/MAME.md
[PASS] R2 许可记录存在 licenses/SIMH.md
[PASS] R2 许可记录存在 licenses/Stella.md
[INFO] R4 gw\emulators\mame_apple2.py: 「占位」×1
[INFO] R4 残留扫描完成：命中 1 处（含骨架注记与新发现，只暴露不计 rc）
汇总：硬断言 FAIL 0 处 → rc=0
RELEASE_RC=0
```
