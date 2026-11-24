# TASK-291-B 完成报告

## 交付物清单
- **F-10 导览调度器静态接线（新建文件）**：narr_tour_controller.gd（class_name NarrTourController，10 funcs）——导览启动→镜头接管→站间迁移→回行走的静态接线：
  - `TOUR_STATIONS` 39 号 8 站卡静态序列（含 stay_sec/radius）；`start_tour`/`next_station`/`stop_tour` 调度接口 + HUD「馆长路线」徽标行；
  - `STATION_LAYOUT` + `_notify_station_narr`——与 F-9 口播联动（复用 play_hall_narr 单口播互斥通道）；
  - 57 号参数常量组：1.4/2.5 m/s 双档、200°/s 红线、FOV 50~100、阻尼 0.15s、超时宽限 15s。
- 静态验收：gd 符号 MISS 0 / FAIL 0（17 文件、funcs 171）；待实机 7 条（276-B §③）逐条续挂。

## 实装关键行
narr_tour_controller.gd L13-24（8 站卡）、L26-43（厅站映射+常量组）、L61-100（start/stop/next_tour）、L118-148（超时宽限+口播联动）。

## 待实机清单（276-B §③ 7 条逐条续挂）
①镜头接管/回行走手感；②双档限速复测；③57 号红线复测；④口播与镜头同步（句末推进）；⑤馆长路线↔自由漫游切换；⑥8 站卡时长误差；⑦晕动复测（俯仰 ±70°）。均已挂载说明。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 实装自证：关键行见上节+待实机 7 条；4. release_check：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 任务书「新建调度器 gd 或并入既有结构」两可——选新建独立文件；未挂 main.tscn（scene_check load_steps=19 不变），挂载点待实机轮。
2. 镜头接管按静态口径落地（_tour_active + HUD + 注释声明输入挂起待实机），未调 player.gd 未实现函数——避免 gd_symbol_check 字符串引用 MISS。
3. 站间迁移即切厅的接线点（next_station → switch_hall）留待实机与 39 号 §3.1 三条件一并核对。
4. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际，任务书写 55/55 或更高）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 51，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 17 个 gd；class_name 7 个；FAIL 0
== [budget] scripts/device_budget_check.py
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（59 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 51，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 17 个 gd；class_name 7 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（51 包）        PASS  全部 FAIL 0
结果：59/59 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== exhibit_host.gd        [exhibit_host] funcs=30 signals=0
   [OK] has_method is_explode_locked → 存在
   [OK] has_method last_exploded_device → 存在
   [OK] has_method play_hall_narr → 存在
== narr_player.gd         [narr_player] funcs=9 signals=0
== narr_tour_controller.gd [narr_tour_controller] funcs=10 signals=0
   [OK] has_method play_hall_narr → 存在
汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 17 个 gd；class_name 7 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 59/59 通过（2026-11-24 23:01:11）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 51 ≥ 30
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
