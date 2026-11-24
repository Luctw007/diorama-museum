# TASK-291-N 完成报告

## 交付物清单
- **F-7 图鉴检索联动接线复查卡**（docs/F7联动复查_v1.md，≥2000 字节）：
  - §①接线复查表 5 行：回厅续接高亮/图鉴→大厅定位/大厅→图鉴/高亮互斥/gd 符号命中（17 文件 MISS 0）逐处现状核对，全部与 261-B/266-A 口径一致；
  - §②待实机 6 条复核：①③④⑤⑥维持，②维持，③更新（F-10 调度器 291-B 已出，过渡镜头裁决有承接点，与 F-10 待实机共轮）；
  - §③多厅同 id「列全部厅供选」未实装项确认：维持未实装（当前 14 台 id 互不重复），登记为待排项非回归缺陷。
- 改动清单：只新增 1 份 md + 本报告；不新增实装（任务书边界，复查发现缺陷只登记待排）、02/03/04/05 线零改动。

## 复查卡自证
字节数（UTF-8）见报告末自证块（>2000）；接线复查表 5 行命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 复查卡自证见上节。

## 与任务书的漂移
1. 任务书前置 1「TASK-266-A 完成报告——待实机 6 条」与实际一致；③的「更新」为复查新增结论（F-10 承接点），非任务书外实装。
2. 复查结论「无回归缺陷」——五处接线点与预研口径一致，未触发任务书「复查发现缺陷只登记待排」分支。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. 复查范围限 F-7 五处接线点；③的「更新」登记不改变 266-A 实装（未新增任何代码改动），只把 F-10 承接关系写进待实机清单。

---

## 复查卡字节数自证

```
3437 字节
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
