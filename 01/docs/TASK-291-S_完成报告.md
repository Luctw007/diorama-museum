# TASK-291-S 完成报告

## 交付物清单
- **全馆布局五件 layout_check 复跑归档卡**（docs/布局复跑归档_v1.md，≥2000 字节）：
  - §①五件布局逐件复跑日志（console 2 台/dawn 4/hub 1/mainframe 4/personal 3 全 PASS、rc=0，2026-11-24 复跑，规则覆盖 L-01~L-04+P-01~P-03）；
  - §②与 B-01 预算断言对账表：五厅台数 vs 上限 20 逐行 PASS（合计 14 ≤ B-02 30、流程位 28 ≤60），与 F4预算表基线「hub 1/dawn 4/mainframe 4/personal 3/console 2」逐项吻合；
  - §③异常/漂移登记：无异常无漂移（布局 JSON 零改动；第三批 10 台与家电五台未上布局不影响复跑口径）。
- 改动清单：只新增 1 份 md + 本报告；不改布局文件、02/03/04/05 线零改动。

## 归档卡自证
字节数（UTF-8）见报告末自证块（>2000）；对账表 6 行命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. layout_check --all 复跑：5 份全 PASS、rc=0（日志块 2）；3. 归档卡自证见上节。

## 与任务书的漂移
1. 任务书第 1 条前置「layout_check.py（若路径有出入以仓库实际为准）」——实际路径 01/scripts/layout_check.py 无出入。
2. 本卡与 291-L（四厅白模自检）同源复跑：291-L 侧重四厅白模状态与第三批预案，本卡侧重五件（含枢纽）归档与 B-01 对账——两卡互补不重复。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. 复跑与 291-L 同批执行（同一份 layout_check --all 输出）；本轮门禁 59/59 含 budget 步，五件布局在门禁链中持续全绿，归档卡记录与 verify_last.json 时间戳一致。

---

## 归档卡字节数自证

```
2588 字节
```

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

## 验收日志块 2（layout_check --all）

```
=== exhibit_console.json
  OK（设备 2 台）
=== exhibit_dawn.json
  OK（设备 4 台）
=== exhibit_hub.json
  OK（设备 1 台）
=== exhibit_mainframe.json
  OK（设备 4 台）
=== exhibit_personal.json
  OK（设备 3 台）
--all 完成：5 份布局
LAYOUT_RC=0
```
