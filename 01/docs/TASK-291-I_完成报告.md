# TASK-291-I 完成报告

## 交付物清单
- **player.gd 双档限速常量静态落地（57 号参数卡 v2）**：新增常量组——`WALK_SPEED_NORMAL := 2.5`（常态行走）、`WALK_SPEED_NARR := 1.4`（播报限速档）、`TURN_SPEED_REDLINE := 200.0`（角速度红线 °/s）、`PITCH_CLAMP_DEG := 70.0`（俯仰 ±70°）、`MOVE_DAMP_SEC := 0.15`（起停阻尼）。
- 运行时不切换档位：M0 运行时仍用 MOVE_SPEED=3.0 单档（注释声明切换与 F-10 导览联动，标「待实机」）；与 291-B 常量同源对齐。
- 静态验收：gd 符号 MISS 0 / FAIL 0；无运行时行为变更。

## 实装关键行
player.gd L7-19（M0 常量组 + 双档限速常量组及注释）。

## 待实机声明
档位切换（播报中自动降 1.4 m/s）、0.15s 阻尼、±70° 钳制、200°/s 红线均为**待实机**项（运行时仍 3.0/±85°/无阻尼）——本任务只静态落地常量，不臆造「已生效」；复测口径 = F-10 待实机 7 条。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 实装自证：常量定义关键行见上节+「切换待实机」声明；4. release_check：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 任务书列「播报限速档 1.4/常规 2.5、角速度红线、阻尼 0.15s」——实现另加 PITCH_CLAMP_DEG ±70°（57 号 v2 第 3 行建议值，与红线同源），不超边界（任务书第 2 条前置即 57 号参数卡全文）。
2. 角速度红线以 200°/s 数值落地（57 号 §2 红线表第一行）——任务书只写「角速度红线」未给数值，按参数卡母本实值，不臆造。
3. LOOK_SPEED 0.0018（57 号 v2 转身灵敏度建议值）未落地——任务书未列此项，按「不超边界」原则不加。
4. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

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
