# TASK-236-A 完成报告

## 交付物清单
- **hub 布局正式化**：`hub_definition.json` → `godot/content/exhibit_hub.json`（exhibit_ 前缀，进 layout_check --all）+ devices 补全（altair-8800 白模占位 1 台，过 L-01/L-02）；旧文件已删除。
- **反向 portal**：四厅布局各补 `portals: [{target:"hub", position:[0.0,0.0,5.5]}]`（各厅边界内）；portal_hub.gd 新增 `refresh_portals`（切厅后按当前厅 portals 重建门框）+ `GROUP_TO_LAYOUT`（"hub"→exhibit_hub.json）；exhibit_host.gd 切厅成功后回调 `PortalHub.refresh_portals`。
- **点选接线**：portal_hub.gd 新增左键拾取（鼠标可见用真实点击位置、捕获用屏幕中心）+ `_pick_portal` 屏幕空间最近门框（unproject_position + 18px，inspect_controller 同款口径）→ activate_portal。碰撞/点选双路径。
- **静态验收**：gd MISS 0 / FAIL 0；layout_check --all 5 份全 PASS（含 exhibit_hub）；scene_check 全 PASS。

## 实装关键行
portal_hub.gd：GROUP_TO_LAYOUT L32、refresh_portals L57、_unhandled_input L150 / _pick_portal L165、activate_portal L191、_resolve_layout_file L203；exhibit_host.gd：回调 L216、L221-224；玩家过滤（236-B 同源）L141-145。

## 待实装验证（实机行为不写「已验证」）
详见 F1白模验证口径清单_v1.md：①四厅双向可达；②清场无残留、配额与调试圈保留；③图鉴面板同显；④真跑跨厅存活。纯实机项：玩家碰撞体缺失、点选与设备拾取互斥、碰撞层交互、启动厅默认 dawn 与 hub 门框并存（F-3 定案）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：51/51 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. layout 自证：--all 5 份全 PASS（日志块 2）；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）；5. 剩余待实装清单见上节。

## 与任务书的漂移
1. hub 占位设备选 **altair-8800**：仓库无「镇馆之宝」标记字段，altair-8800 为 SIMH 真跑机种槽位，兼顾 F-8；最终以 04 线动线定案为准。
2. 点选采用 inspect_controller 屏幕投影拾取口径（非物理 raycast）。
3. 反向 portal 位置统一 [0.0, 0.0, 5.5]；子厅布局为 01 线文件，本轮按需修改。
4. 启动厅仍为 exhibit_dawn（任务书未要求改默认厅）。
5. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

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

## 验收日志块 2（gd 自检 + layout 自证 + scene_check）

```
== portal_hub.gd          [portal_hub] funcs=12 signals=0
== exhibit_host.gd        [exhibit_host] funcs=24 signals=0
汇总：16 文件；符号池 funcs 144 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
  [PASS] S-01 load_steps=19（ext 13 + sub 5 + 1 = 19）
  [PASS] 总检：main.tscn 静态校验通过（ext 13 / sub 5）
主场景接线静态合法（待 Godot 实机确认表现层）
SCENE_RC=0
=== exhibit_console.json
  OK（设备 2 台）
=== exhibit_dawn.json
  OK（设备 4 台）
=== exhibit_hub.json
  OK（设备 1 台）
=== exhibit_mainframe.json
  OK（设备 4 台）
=== exhibit_personal.json
  OK（设备 3 台）
--all 完成：5 份布局
LAYOUT_RC=0
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
