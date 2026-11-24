# TASK-291-A 完成报告

## 交付物清单
- **co_active_max 引擎实装（B-4 链条第①步）**：exhibit_host.gd 新增 `@export_range(1, 6) var co_active_max: int = 3`（同屏激活上限，注释写明与 max_running「同厅运行配额」显式区分）；新增 `_active_ids` 计数与 `acquire_activation`（达上限拒绝并提示）/`release_activation`/`active_count`/`is_active`；clear_devices 清空；get_layout_summary 增补两字段。
- 计数口径对齐 282-A 需求卡：激活态 = 进入拆解/运行且未退出的设备；与 acquire_run（max_running 配额）判据独立、互不覆盖。
- 静态验收：gd 符号 MISS 0 / 命名 FAIL 0；B-04 断言保持 SKIP；实测标「待实测」（272-B 梯度实测口径，本任务不做）。

## 实装关键行
exhibit_host.gd L42-47（co_active_max 字段）、L75（_active_ids）、L185-196（acquire_activation 判读点）、L200-210（release/查询三件）、L242-243（摘要扩展）、L340（清场清名额）。

## 待实测声明
本任务只做字段与判读点静态实装；「同屏 N 台不卡」权威值与 B-04 SKIP→PASS 待按实测口径卡梯度实测后回写（②③④步未做，不臆造「已实测」）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 实装自证：关键行见上节；4. release_check：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 任务书验收写「55/55 或更高」，仓库实际基线 59/59（51 完工包+8 步含 budget 行）——按仓库实际回写。
2. 任务书命令 `py -3.7` 环境无此启动器，用 PATH 指向的 python 3.12.10 执行（结果一致）。
3. 判读点采用「≥ 上限」口径（计数达 co_active_max 即拒绝新增），等价于任务书「> co_active_max 抑制」的边界语义。
4. 激活计数以独立接口落地，未塞进 acquire_run——282-A 需求卡要求两字段判据独立、不互相覆盖；实装前 grep 无命中现状已确认。

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
