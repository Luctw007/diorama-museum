# TASK-301-R 完成报告

## 交付物清单
- **F 系列待实机清单汇总 v2**（docs/F系列待实机清单汇总_v2.md，另存新文件，v1 保留，≥2500 字节）：①逐 F 项待实机清单更新 9 行（F-14⑥ 前置由「待挂玩家碰撞体」改「已静态落地 301-J/L，待用户实机」；F-10 增「导览挂载已静态落地 301-K」；新增 F-6 深化 L2/L3 观感 1 项）；②用户实机执行建议 5 批次（引用 301-M/N/O/P 四张执行卡）；③条数合计更新（68→69 项/格）+ v1→v2 变更说明 5 条。
- 改动清单：只新增 1 份 md + 本报告；v1 原文件未改；不实机、不代用户执行、02/03/04/05 线零改动。

## 汇总卡自证
字节数（UTF-8）见报告末自证块（>2500）；逐 F 项更新行 9 行 + 条数合计 69 + v1→v2 变更说明命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. 汇总卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 2「台账 v6（301-Q 产物，若已出）」——同轮已出，按 v6 全行状态登记。
2. 条数合计 68→69（新增 F-6 深化 1 项）：任务书交付物未列 F-6 新增行，但「F-6 增 L2/L3 观感待实机」为其明确要求——以新增行落地并计入合计，如实登记。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

4. 执行备注：本轮验收基线 60/60；首次 58/59（catalog_ref 瞬时红 gamecube 反链），单步复跑收敛后干净重跑全绿。
---

## 汇总卡字节数自证

```
3043 字节
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
