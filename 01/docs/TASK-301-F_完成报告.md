# TASK-301-F 完成报告

## 交付物清单
- **F-16 封版 F-7~F-16 排期项核对卡**（docs/F16封版F7-F16排期核对_v1.md）：①F-7~F-16 逐项核对表 10 行（状态/责任线/待实机条数/阻塞点）；②F-13/F-14/F-16 现状与阻塞三行（用户二进制编译、实机执行、release_check 扩展）；③封版排期结论（静态产物可进封版、销账各自挂起；F-13/F-14/F-16 挂用户/统筹）。
- 改动清单：只新增 1 份 md + 本报告；不销账、不改台账原文、不实机、02/03/04/05 线零改动。

## 核对表自证
字节数（UTF-8）见报告末自证块；F-7~F-16 逐项核对表 10 行 + 阻塞点结论命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. release_check：硬断言 FAIL 0 处 → rc=0（F-16 现状佐证，日志块 2）；3. 核对表自证见上节。

## 与任务书的漂移
1. 任务书前置 3「F16封版扩展口径设计_v1.md（301-D 产物，若已出）」——301-D 同轮已出，核对表 R5 口径对齐无冲突。
2. F-10/F-14 行按本轮 301-K/J/L 实装后现状登记（导览挂载、碰撞体/墙体碰撞静态落地），与任务书背景（台账 v5 状态）有增量——以仓库实际为准回写。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

5. 执行备注：本轮验收基线 60/60；release_check 硬断言 FAIL 0 处 rc=0（F-16 现状佐证）；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿。
6. 合计口径：F-7~F-15 待实机条数与汇总卡 v2 一致（69 项/格）。
---

## 核对卡字节数自证

```
2611 字节
```

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 52，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：17 文件；符号池 funcs 175 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 17 个 gd；class_name 7 个；FAIL 0
== [budget] scripts/device_budget_check.py
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（60 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 52，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：17 文件；符号池 funcs 175 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 17 个 gd；class_name 7 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（52 包）        PASS  全部 FAIL 0
结果：60/60 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 60/60 通过（2026-11-25 00:49:57）
[INFO] R3 wip 清单（不计入 rc）：xbox
[PASS] R3 完工包 52 ≥ 30
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
