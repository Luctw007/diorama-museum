# TASK-256-A 完成报告

## 交付物清单
- **F-6 实装（提示式口径，按 251-A 预口径）**：`inspect_controller.gd` 新增——①进入拆解即记录最近拆解台（`_last_exploded` 设备 id 经 device_loader_hint.get_current_device() + `_last_exploded_level` 层级标记）；②HUD 诊断行常驻「上次拆解:xx」提示（_process 逐帧刷新，切厅后不消失——InspectController 挂 DeviceRoot，clear_devices 不动它，241-A 已证）；③查询入口 `last_exploded_device()` / `last_exploded_level()` 供 HUD/导览调用。
- **拆解会话保活静态收口**：切厅不打断拆解（241-A 已证）+ 本任务补续接入口——不自动跳回（提示式）。
- 回归：gd 符号 MISS 0 / 命名 FAIL 0；scene_check PASS；layout --all 5 份全 PASS。

## F-6 实装关键行（inspect_controller.gd）
记录：L294-298（has_method("get_current_device") → _last_exploded/_last_exploded_level）；常驻提示：L163-168（诊断行追加「上次拆解:%s」）；查询：L325-332（last_exploded_device/last_exploded_level）。

## 待实装验证清单
①HUD 提示观感与位置（诊断行）实机核对；②L2/L3 层级精确回放（当前仅 "exploded" 标记，深度分档导出待 explode_controller 状态接口）；③「回厅续接高亮该台」视觉引导未接线（F-7 联动候选）；④拆解中切厅的并发视觉（双高亮/输入优先级，241-A 遗留）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：54/54 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. F-6 自证：关键行见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 续接口径选**提示式**（任务书二选一）：HUD 常驻提示不自动跳回——自动跳回会打断玩家当前动线，与 04 线「一眼可见三步可达」口径冲突；251-A 预口径即提示式。
2. 层级记录为 "exploded" 标记（进入即拆解态），L2/L3 精确回放依赖 explode_controller 状态导出接口——不臆造，标待实装验证。
3. 记录存 InspectController（DeviceRoot 子树），而非 ExhibitHost——拆解设备是单机直连设备，可能不在展厅布局 _placed 内。
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
== inspect_controller.gd  [inspect_controller] funcs=20 signals=1
   [OK] has_method get_current_device → 存在
   [OK] has_method get_node_role → 存在
汇总：16 文件；符号池 funcs 148 / signals 7；MISS 0；已知缺口 KG 0
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
