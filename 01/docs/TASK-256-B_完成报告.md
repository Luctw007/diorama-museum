# TASK-256-B 完成报告

## 交付物清单
- **排期台账 v3**：新增 `docs/全馆功能排期台账_v3.md`（3687 字节）——①销账行扩至 F-1~F-6（F-5 方案销账 251-A、F-6 实装销账 256-A；F-4 仅口径已出未销账）；②F-4/F-5 实装与 F-7~F-16 剩余排期刷新表（责任线/前置/建议轮次/验收口径/实机依赖，F-12/F-13/F-14 标「待用户实机」，F-8 前置补 251-B 槽位预留）；③与 221-A 映射核对 v3 增量（F-5/F-6 口径、F-8 前置、总数不变）。

## 台账自证（F-5/F-6 销账行 + 剩余排期行数 + 字节数）
F-5 销账行（方案销账、实装未销账——exhibit_workbench.json 未建，待 04 线子区布局同轮落地）；F-6 销账行（256-A 提示式续接：记录最近拆解台 + HUD 常驻提示 + 查询入口，待实机 3 条）；剩余排期 12 行（F-4/F-5 实装 + F-7~F-16，其中 F-12/F-13/F-14 标「待用户实机」，F-13 另挂第二批 SIMH 二进制待用户编译 + 251-B 四台预留仅登记方案）；字节数 3687 > 1500。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：54/54 全 PASS、rc=0（日志块 1）；2. 台账自检：销账行 + 排期行 + 字节数（日志块 2）；3. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. v3 另存新文件（`全馆功能排期台账_v3.md`），v2 保留历史——任务书写「v2 更新为 v3」，新文件避免历史轮次引用漂移。
2. F-5 销账为**方案销账**（实装未销账）：251-A 只出方案，exhibit_workbench.json 未建——按红线「未完成项不销账」，销账行标注实装待 04 线同轮。
3. F-6 销账依据 256-A 同批实装（提示式口径），待实机项 3 条入表。
4. 门禁预期 49/49 落后实测（46 完工包+7 步=53 项起，以实测为准）。

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

## 验收日志块 2（台账自检）

```
（销账行命中 + 字节数）
| F-5 | **方案销账** | F5工作台布局方案_v1.md（251-A） | **实装未销账**（待 04 线子区布局同轮） |
| F-6 | **实装销账** | inspect_controller 最近拆解台记录 + HUD 常驻提示（256-A，提示式口径） | HUD 提示观感、L2/L3 层级精确回放 |
## ② F-4~F-16 剩余排期刷新
台账v3: 3687 字节
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
