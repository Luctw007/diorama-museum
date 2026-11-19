# TASK-231-A 完成报告

## 交付物清单
- `godot/scripts/portal_hub.gd`（class_name PortalHub，7 个 func）：Hub 白模灰盒门框（BoxMesh 1×2.4×0.2、unshaded 半透明材质、Area3D + BoxShape3D 碰撞）+ portals 解析（target/position/rotation）+ hall_group 归属 + 碰撞触发传送；
- `godot/content/hub_definition.json`：hall_group=hub、四翼 portals（dawn/mainframe/personal/console，position 均在 20×12 厅界内）、devices=[]（F-1 白模阶段空设备）；
- `godot/scenes/main.tscn`：挂 PortalHub 节点（ext_resource 13_portalhub，load_steps 18→19）。
- 复用：switch_hall（TASK-114 清场重建/配额与调试圈保留）、HallNavPanel（171-B）为底座；经 `/root/Main/ExhibitHost` 类型引用，无字符串 has_method。

## 实装关键行（portal_hub.gd）
portals 解析 L61；position 应用 L82、rotation 应用 L89；碰撞接线 L106（`body_entered.connect(_on_portal_entered.bind(target))`）；传送执行复用 switch_hall L118-126；hall_group 归属 L50-58 解析 + L130 `current_group()`。

## 待实装验证（实机行为一律不写「已验证」）
① Area3D 门框与玩家碰撞层是否正确交互；② body_entered 未做玩家过滤，任何碰撞体进入即切厅；③ 点选路径（inspect_controller 中心拾取先例）未接线，仅留 activate_portal 入口；④ 子厅→hub 反向 portal 未落（由 wings 的 portals 声明）；⑤ 226-A 白模验证口径①~④（双向可达/切厅无残留/图鉴面板同显/真跑进程跨厅存活）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：50/50 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. release_check：硬断言 FAIL 0 处、rc=0（日志块 3）；4. F-1 自证：scene_check 全 PASS、存量 4 厅全 PASS、hub 三字段过 P-01~P-03 断言（日志块 4）。

## 与任务书的漂移
1. 门禁预期 49/49 实为 50/50：完工包 43 + 7 步（他线产包增长，任务书预期滞后）。
2. hub 布局命名 hub_definition.json（非 exhibit_ 前缀）：227-A L-01 仍要求 devices 非空数组，F-1 白模阶段 hub 无设备，独立命名避免 layout_check --all 扫描冲突；F-3 升级正式枢纽厅布局时改 exhibit_ 前缀并补 devices。
3. hall_group/lod_scale 口径按 227-A（五值 / >0），非 226-A 旧提案（hub/wing、0.5~2.0）。
4. 点选触发仅提供 activate_portal 入口、未接线——标注待实装验证，不臆造就绪。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
===== 验收汇总（50 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 43，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 139 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（43 包）        PASS  全部 FAIL 0
结果：50/50 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== portal_hub.gd          [portal_hub] funcs=7 signals=0
汇总：16 文件；符号池 funcs 139 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 50/50 通过（2026-11-19 23:48:34）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 43 ≥ 30
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

## 验收日志块 4（F-1 自证）

```
  [PASS] S-01 load_steps=19（ext 13 + sub 5 + 1 = 19）
  [PASS] S-02 13_portalhub (res://scripts/portal_hub.gd) 文件存在
  [PASS] 总检：main.tscn 静态校验通过（ext 13 / sub 5）
主场景接线静态合法（待 Godot 实机确认表现层）
SCENE_RC=0

=== exhibit_console.json
  OK（设备 2 台）
=== exhibit_dawn.json
  OK（设备 4 台）
=== exhibit_mainframe.json
  OK（设备 4 台）
=== exhibit_personal.json
  OK（设备 3 台）
--all 完成：4 份布局
LAYOUT_RC=0

（hub_definition 三字段断言）
hub_definition 三字段过 P-01~P-03: []
HUB_PORTALS_ASSERT_PASS
RC=0
```
