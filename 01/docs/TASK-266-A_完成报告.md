# TASK-266-A 完成报告

## 交付物清单
- **回厅续接高亮实装**：exhibit_host.gd `_notify_portal_hub` 扩展调 `_resume_highlight_check()`（L228）——最近拆解设备（InspectController.last_exploded_device）在本厅时 set_device_highlight 高亮；拆解锁定中跳过（is_explode_locked，261-B §③口径）；与导览/点选高亮互斥沿用既有（sync_to_tour_step 清场、切厅清场自然清除）。
- **图鉴入口联动实装**：①图鉴→大厅——encyclopedia_panel.gd 新增「定位到厅」按钮（选中行带 device_id 时可用）+ `_find_hall_for()` 布局扫描 → switch_hall + 高亮该台；多厅同 id 取首个命中（列全部厅供选待实机）；②大厅→图鉴——hall_nav_panel.gd 新增「本厅图鉴」按钮 → 打开图鉴并提示本厅清单（device_id 反查目录 [需核实]，不落定论）。
- 回归：gd 符号 MISS 0（is_explode_locked/last_exploded_device 符号命中）/ 命名 FAIL 0。

## F-7 实装关键行
exhibit_host.gd L224-248（_notify_portal_hub 扩展 + _resume_highlight_check）；encyclopedia_panel.gd L92-97（按钮）、L242-281（_on_locate_pressed/_find_hall_for）；hall_nav_panel.gd L63-67（按钮）、L195-207（_open_encyclopedia_for_hall）。

## 待实机清单（261-B 预研卡 6 条逐条续挂）
①回厅续接高亮视觉观感；②续接高亮与导览/点选高亮切换互斥手感；③图鉴→大厅切厅耗时与相机衔接（关联 F-10）；④大厅→图鉴目录反查字段 [需核实]；⑤多厅同 id「列全部厅供选」未实装（现取首个命中）；⑥is_explode_locked 跳过边界行为。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：55/55 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. F-7 自证：关键行见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 多厅同 id 取首个命中（261-B §④-5 的「列全部厅供选」未实装，待实机后按需补）。
2. 大厅→图鉴仅打开面板+提示本厅清单，不做目录内过滤（02 线目录字段反查 [需核实]，红线遵守不落定论）。
3. F-7 不销账（边界遵守：台账 v3 F-7 行保持「待排/待用户实机」）。
4. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 48，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 154 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（55 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 48，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 154 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（48 包）        PASS  全部 FAIL 0
结果：55/55 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== exhibit_host.gd        [exhibit_host] funcs=25 signals=0
   [OK] has_method is_explode_locked → 存在
   [OK] has_method last_exploded_device → 存在
== encyclopedia_panel.gd  [encyclopedia_panel] funcs=12 signals=0
== hall_nav_panel.gd      [hall_nav_panel] funcs=14 signals=0
汇总：16 文件；符号池 funcs 154 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 55/55 通过（2026-11-21 23:08:42）
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
