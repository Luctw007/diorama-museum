# TASK-301-H 完成报告

## 交付物清单
- **F-16 封版预检总卡**（docs/F16封版预检总卡_v1.md，≥1500 字节）：①F-16 预检总表 5 行（301-C/D/E/F/G 五卡结论逐行归并）；②阻塞待办清单 6 行（F-4/F-5/F-6 深化、F-13 二进制、F-14 六项+68 项/格、F-16 R5 实装）；③F-16 结论（静态面可启动封版预检、销账面未收口；缺四项前置：B-4 实测、F-13 二进制、F-14 实机、R5 实装）。
- 改动清单：只新增 1 份 md + 本报告；不销账、不改 release_check.py、不实机、02/03/04/05 线零改动。

## 总卡自证
字节数（UTF-8）见报告末自证块（>1500）；预检总表 5 行 + 阻塞待办清单 6 行命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. release_check：硬断言 FAIL 0 处 → rc=0（日志块 2）；3. 总卡自证见上节。

## 与任务书的漂移
1. 任务书前置 1~3（C/D/E/F/G 五卡产物）同轮全部已出，总表按五卡实际结论归并，无缺前置。
2. 阻塞待办清单把 F-6 深化（301-I L2/L3 观感）单列为新增阻塞行——任务书未列但 E 卡已有此结论，如实并入。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

5. 执行备注：本轮验收基线 60/60（52 完工包）；release_check 硬断言 FAIL 0 处 rc=0；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿——总卡 F-16 结论基于干净重跑基线。
6. 预检总表五卡结论与 C~G 五卡原文一致，无归并漂移。
---

## 总卡字节数自证

```
2568 字节
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
