# TASK-291-L 完成报告

## 交付物清单
- **四厅白模自检卡**（docs/四厅白模自检_v1.md，≥2000 字节）：
  - §①layout_check --all 复跑日志（5 份全 PASS、rc=0，逐件贴出）；
  - §②白模自检表：五厅每厅台数/占位盒状态/与预算表 B-01 对账（hub 1/dawn 4/mainframe 4/personal 3/console 2，合计 14 台，B-01/B-02/B-07 全 PASS）；
  - §③第三批 10 台布局占位预案注记：逐台目标厅（02 线 287-B v3 名单）+「未产包不上布局」口径（不预填坐标）。
- 改动清单：只新增 1 份 md + 本报告；不改布局文件（纯复跑）、02/03/04/05 线零改动。

## 自检卡自证
字节数（UTF-8）见报告末自证块（>2000）；白模自检表 5 行 + B-01 对账命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. layout_check --all 复跑：5 份全 PASS、rc=0（日志块 2）；3. 自检卡自证见上节。

## 与任务书的漂移
1. 任务书前置 2「F4设备实例预算表_v1——布局台数口径（14 台）」与实际一致（hub 1+四厅 13=14 台）。
2. 第三批 10 台名单取自 02 线《第三批产包验收清单_v3》（287-B）——任务书未给名单，按仓库实际引用（不臆造名单）。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. 复跑时间 2026-11-24、命令 layout_check.py --all：本轮 291-A/B/C/I 四处置改动不触及布局 JSON，复跑结果与历史全绿基线一致；与 291-S 归档卡共用同一份复跑日志（本卡侧重四厅白模、S 卡侧重五件对账）。

---

## 自检卡字节数自证

```
3491 字节
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
