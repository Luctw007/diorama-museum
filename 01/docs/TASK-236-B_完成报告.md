# TASK-236-B 完成报告

## 交付物清单
- **玩家过滤**：portal_hub.gd `_on_portal_entered` 加 `body.is_in_group(PLAYER_GROUP)` 过滤（L141-145），非玩家碰撞体忽略并 push_warning；`PLAYER_GROUP := "player"` 契约常量（L37-38）。判定依据：player.gd 为 M0 无碰撞自由相机（无 PhysicsBody、无分组注册）——过滤契约以「玩家碰撞体挂 is_in_group("player")」为准。
- **白模验证口径清单**：新增 `01/docs/F1白模验证口径清单_v1.md`——226-A 四条口径（双向可达/清场无残留/图鉴面板同显/真跑跨厅存活）逐条「验证步骤 + 预期 + 状态（待用户实机）」+ 纯实机项 5 条 + 完成判据。
- 回归：gd 符号 MISS 0 / 命名 FAIL 0。

## 玩家过滤关键行（portal_hub.gd）
- L37-38：`const PLAYER_GROUP := "player"`（过滤契约）；
- L141-145：`_on_portal_entered` 中 `if not body.is_in_group(PLAYER_GROUP): push_warning("PortalHub: 非玩家碰撞体 %s 进入 portal，忽略" % body.name); return` → 仅玩家碰撞体触发切厅。

## 待实装验证剩余清单（纯实机项）
1. **玩家碰撞体缺失（前置）**：player.gd 无 PhysicsBody，碰撞路径当前不可达——需挂碰撞体并 `add_to_group("player")`，或定案「点选为主」（236-A 点选已接线）；→ 待用户实机。
2. 点选与设备拾取互斥手感；3. 碰撞层 mask/layer 配对；4. 启动厅默认值（hub 门框与 dawn 设备并存，F-3 定案）；5. HallNavPanel hall_group 归类（F-3）。详见 F1白模验证口径清单_v1.md。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：51/51 全 PASS、rc=0（日志块 1）；
2. gd 自检：MISS 0 / FAIL 0（日志块 2）；
3. 玩家过滤自证：关键行见上节（diff 型证据，日志块 2 附 gd 全绿佐证）；
4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）；
5. 剩余待实装清单见上节 + F1 清单文档。

## 与任务书的漂移
1. player.gd 无分组注册、无碰撞体（M0 无碰撞设计）——过滤契约落 is_in_group("player")；本任务**不改 player.gd**（挂碰撞体属实机项，已列清单第 1 条）。
2. 清单落点选独立文档 F1白模验证口径清单_v1.md（任务书两选一）；不改 godot_first_boot.md（26B 首验口径维持不变）。
3. 任务书前置路径写 `D:\work\01\repo\godot\`，实际引擎在 `01\repo\01\godot\`（既有事实）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 44，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 144 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（51 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 44，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 144 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（44 包）        PASS  全部 FAIL 0
结果：51/51 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== portal_hub.gd          [portal_hub] funcs=12 signals=0
== exhibit_host.gd        [exhibit_host] funcs=24 signals=0
汇总：16 文件；符号池 funcs 144 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 51/51 通过（2026-11-20 00:21:42）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 44 ≥ 30
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
