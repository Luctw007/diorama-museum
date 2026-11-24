# TASK-271-B 完成报告

## 交付物清单
- **排期台账 v4**：新增 `docs/全馆功能排期台账_v4.md`（3701 字节，v3 保留）——①销账行刷新（F-4 增补「预算表 v1+断言脚本已出，未销账——挂载待统筹」；F-6 增补 261-A 层级分档深化）；②剩余排期刷新（F-7「实装已出不销账（待实机 6 条）」、F-9「接入已出（271-A），销账待 04 线同轮」、F-8/F-10~F-16 逐行核对）；③映射核对 v4 增量（F-4/F-6/F-7/F-9 四行变更，总数不变）；④v3→v4 变更说明 5 条。

## 台账自证（字节数 + F-4/F-6/F-7/F-9 四行更新 + 变更说明）
字节数 3701 > 1500；四行更新：F-4（未销账 + 预算表 v1/断言脚本 266-B，PASS 9/SKIP 2/FAIL 0，挂载待统筹）、F-6（销账 + 深化 261-A：get_depth_level 层级分档，L2/L3 受引擎限制）、F-7（实装已出不销账 / 待实机 6 条，266-A）、F-9（接入已出 271-A / 销账待 04 线同轮）；变更说明 5 条（见日志块 2）。

## 改动清单自证
本轮只新增 2 份 md：`docs/全馆功能排期台账_v4.md`、`docs/TASK-271-B_完成报告.md`；未改 v3 原文、未改任何 gd/脚本/布局。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁只读复跑：56/56 全 PASS、rc=0（日志块 1）；2. 台账自证：3701 字节 + 四行更新原文（日志块 2）；3. 改动清单见上节。

## 与任务书的漂移
1. v4 另存新文件（v3 保留）——与 v3 同款处理，避免历史轮次引用漂移。
2. F-7 实装已出仍「不销账」（266-A 边界）——待实机 6 条未核对，红线遵守。
3. F-9 接入已出但「销账待 04 线同轮」——任务书边界明确，不提前销账。
4. 门禁日志与 271-A 共用同一次干净重跑（同批状态）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 49，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 156 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（56 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 49，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 156 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（49 包）        PASS  全部 FAIL 0
结果：56/56 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（台账自证）

```
（F-4/F-6/F-7/F-9 四行更新原文节选 + 变更说明）
| F-4 | **未销账** | 口径（246-A）+ 预算表 v1 + device_budget_check.py（266-B，PASS 9/SKIP 2/FAIL 0） | 断言挂载 verify_all 待统筹收口 |
| F-6 | 销账 + 深化 | 提示式续接（256-A）+ 层级分档 get_depth_level/HUD Lx 显示（261-A） | L2/L3 级联爆炸未实装 |
| F-7 | **实装已出，不销账**（01） | 266-A（回厅高亮+图鉴双向联动） | 待实机 6 条 |
| F-9 | **接入已出（271-A），销账待 04 线同轮**（01+04） | narr_player HALL_NARR_IDS + play_hall_narr + 切厅触发 | 口播单互斥 + 实机核对 |
## ④ v3→v4 变更说明（5 条）
台账v4: 3701 字节
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 56/56 通过（2026-11-21 23:46:21）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 49 ≥ 30
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
