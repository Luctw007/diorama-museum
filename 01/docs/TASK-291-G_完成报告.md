# TASK-291-G 完成报告

## 交付物清单
- **图鉴面板视觉规格落地核对卡**（docs/图鉴面板落地核对_v1.md，≥2000 字节）：
  - §①49 号规格逐条核对表 13 行（已落地/未落地/差异）：字段序与接口约定「已落地」；面板尺寸/锚点/栏比/行高/字号色板/选中样式/键位子集/空态为部分或未落地；选中联动与三列取数键两处「口径差异」；
  - §②未落地项清单 6 项（含处置：待排轮次/待 02 线目录字段定案 [需核实]）；
  - §③与 F-7 联动口径一致性核对：261-B 预研 vs 266-A 实装 vs 49 号三方对照，结论无漂移（以按钮式为实装事实）。
- 改动清单：只新增 1 份 md + 本报告；不实装、不改 04 线 49 号文档、02/03/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>2000）；核对表 13 行 + 未落地项 6 项清单贴出（不臆造「已落地」——未落地项如实标注）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 核对卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 1 路径 `04\repo\docs\design\49_...` 与实际一致（只读引用）；前置 3「F7图鉴大厅联动预研_v1.md」实为 261-B 产物——已按仓库实际引用。
2. 49 号 §6 自声明「与 106-A 交付无冲突；106-A 完成后按实产复核再升 v1.1 [需核实]」——本卡即该复核的 01 线侧登记，不代 04 线升版。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

---

## 核对卡字节数自证

```
4903 字节
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
