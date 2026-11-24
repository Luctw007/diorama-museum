# TASK-261-B 完成报告

## 交付物清单
- **F-7 预研口径卡**：新增 `docs/F7图鉴大厅联动预研_v1.md`（4097 字节）——①回厅续接高亮方案（数据源 last_exploded_device/level、触发时机 ExhibitHost._notify_portal_hub 同点扩展、高亮复用 set_device_highlight、与导览/点选高亮互斥口径、未接线原因）；②图鉴入口联动方案（图鉴→大厅「定位到厅」、大厅→图鉴「本厅图鉴」双向接线口径，基于 F-3 已证无第二套映射）；③与 256-A 遗留④并发视觉的关系（不同时发生 + is_explode_locked 跳过口径）；④待实机核对清单 6 条（逐条，不臆造）。
- 边界遵守：未做 F-7 实装；台账 v3 F-7 行未动（保持「待排/待用户实机」）。

## 预研卡自证（字节数 + 四节标题 + 待实机条数）
字节数 4097 > 2500；四节命中：`## ① 回厅续接高亮方案（静态口径）` / `## ② 图鉴入口联动方案（静态口径）` / `## ③ 与 256-A 遗留④「拆解中切厅并发视觉」的关系` / `## ④ 待实机核对清单（逐条，不臆造「已通过」）`；待实机清单 6 条。

## 静态自查（改动文件清单）
新增 2 份：`docs/F7图鉴大厅联动预研_v1.md`、`docs/TASK-261-B_完成报告.md`；未触碰任何门禁断言项、未改 gd/布局。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁只读复跑：54/54 全 PASS、rc=0（日志块 1）；2. 预研卡自检：4097 字节 + 四节 + 6 条（日志块 2）；3. 改动文件清单见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 高亮触发点建议改在 `ExhibitHost._notify_portal_hub`（241-A 已有回调点）扩展——比 PortalHub 侧接线更贴近展厅宿主语义，实装轮次按此落。
2. 大厅→图鉴依赖 02 线目录字段反查（device_id 过滤），标 [需核实] 不落定论。
3. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

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

## 验收日志块 2（预研卡自检）

```
F7预研卡: 4097 字节
## ① 回厅续接高亮方案（静态口径）
## ② 图鉴入口联动方案（静态口径）
## ③ 与 256-A 遗留④「拆解中切厅并发视觉」的关系
## ④ 待实机核对清单（逐条，不臆造「已通过」）
（待实机清单 6 条）
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
