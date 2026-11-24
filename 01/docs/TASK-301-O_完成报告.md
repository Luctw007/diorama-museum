# TASK-301-O 完成报告

## 交付物清单
- **F-8/F-13 真跑二进制前置核对卡**（docs/F8F13真跑二进制前置核对_v1.md，≥1200 字节）：①F-13 二进制前置清单 7 行（第二批 SIMH 三槽已转正 dry-run + 第三批四台 hercules/openmsx/mini-vmac/86box 预留，逐项「需核实」状态与隔离口径）；②F-8 四条转正条件（产包+二进制/HUD 观感/直起接真实启动链/04 线标记规格）；③阻塞登记与转正后 R2 判定变化（dry-run→live）。
- 改动清单：只新增 1 份 md + 本报告；不下载/不编译二进制（仅清单级引用，标「需核实」）、不实机、不销账、02/03/04/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>1200）；二进制前置清单 7 行 + 转正条件 4 行命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. release_check：硬断言 FAIL 0 处 → rc=0，R2 第二批槽位 run_status=dry-run 佐证（日志块 2）；3. 核对卡自证见上节。

## 与任务书的漂移
1. 第三批四台二进制来源全部标「需核实」（编译路径/许可版本），不写死结论（红线遵守）。
2. 前置 3「release_check.py R2 第二批槽位 dry-run 判定」——以复跑日志 dry-run 行为佐证（见日志块 2）。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

4. 执行备注：本轮验收基线 60/60；release_check R2 第二批槽位 run_status=dry-run 持续 PASS；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿。
---

## 核对卡字节数自证

```
2370 字节
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
