# TASK-301-T 完成报告

## 交付物清单
- **301 轮次收口总览卡（本报告即交付物）**：①20 份产出总登记表；②台账 v6 ↔ 待实机 v2 一致性核对；③遗留交接清单。

## ① 本轮 20 份产出总登记表

| 任务 | 交付物 |
|---|---|
| 301-A | B4实测口径01线对齐核对_v1.md |
| 301-B | B04回写预案_v1.md |
| 301-C | release_check现状盘点_v1.md |
| 301-D | F16封版扩展口径设计_v1.md |
| 301-E | F16封版F1-F6销账核对_v1.md |
| 301-F | F16封版F7-F16排期核对_v1.md |
| 301-G | F16封版文档完整性核对_v1.md |
| 301-H | F16封版预检总卡_v1.md |
| 301-I | explode_controller.gd（L2/L3 视图分档） |
| 301-J | player.gd（PlayerBody + player 分组） |
| 301-K | main.tscn（NarrTourController 挂载） |
| 301-L | main.tscn（四面墙碰撞化） |
| 301-M | F11F12F15共轮实测执行卡_v1.md |
| 301-N | F14六项实机执行卡_v1.md |
| 301-O | F8F13真跑二进制前置核对_v1.md |
| 301-P | F9F10口播导览实机核对卡_v1.md |
| 301-Q | 全馆功能排期台账_v6.md |
| 301-R | F系列待实机清单汇总_v2.md |
| 301-S | 回归测试矩阵扩展_v2.md |
| 301-T | 本报告（收口总览卡） |

## ② 台账 v6 ↔ 待实机 v2 一致性核对

条数一致（合计 69 项/格）；前置一致（v6 登记 301-I/J/K/L 静态落地，v2 对应行同步更新）；阻塞一致（v6 F-13/F-14/F-16 与 v2 四批次建议对应）——**三者均无冲突**。

## ③ 本轮遗留交接清单

- B-4 待实测（301-A/B 已铺）→ 用户实机；
- F-13 二进制 → 用户编译（301-O 在案）；
- F-14 六项 + 69 项/格 → 用户实机（301-M/N/P 执行卡）；
- F-16 R5 实装 → 后续任务（301-D/H 已铺）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁 60/60 PASS rc=0（日志块 1）；2. release_check FAIL 0 处 rc=0（日志块 2）；3. 总览表自证见 §①。

## 与任务书的漂移
1. 总登记表按各完成报告实际产物登记；I/J/K/L 为代码实装（「引擎小功能四件」口径）。
2. 条数合计 69（v2 口径）与 v1 的 68 差异已在 301-R 登记。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 60/60（本轮干净重跑）。

---

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
