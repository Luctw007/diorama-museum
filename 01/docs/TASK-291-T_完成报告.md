# TASK-291-T 完成报告

## 交付物清单
- **F 系列待实机清单汇总卡**（docs/F系列待实机清单汇总_v1.md，≥2500 字节）：
  - §①逐 F 项待实机清单总表：F-7×6（266-A）、F-8×4（281-A）、F-10×7（276-B §③ + 291-B）、F-11×5（281-B）、F-12×4（286-A）、F-13×1 项（用户二进制编译）、F-14×6（241-B 验收单）、F-15×35 格（286-B 三表）——合计 68 项/格，逐条来源轮次贴出；
  - §②用户实机执行建议：四批（第 1 批 F-14 验收单优先/第 2 批 F-12+F-15+F-11 性能共轮/第 3 批 F-10+F-7③+F-9 口播听感/第 4 批 F-8+F-13+B-4 真跑）+「随时」项（F-7④ 目录反查）；
  - §③F1F2 实机验收单状态登记：未执行（结果栏由用户填写；碰撞体前置缺失→⑤可验⑥不可验）。
- 改动清单：只新增 1 份 md + 本报告；不实机、不代用户执行、02/03/04/05 线零改动。

## 汇总卡自证
字节数（UTF-8）见报告末自证块（>2500）；总表逐 F 项命中（F-7/F-8/F-10/F-11/F-12/F-13/F-14/F-15 八行）+ 条数合计 68 项/格。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 汇总卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 1「台账 v4（或 v5 若已出）」——同批 291-D 已出 v5，按 v5 引用。
2. F-13 以「1 项用户动作」计（二进制编译/提供）；F-14 六项与 F1F2 验收单同一清单（任务书前置 3 即该单）——条数合计 68 以各母本为准。
3. 任务书第 2 条验收「条数合计」：F-7~F-15 = 6+4+7+5+4+1+6+35 = 68 项/格（已贴卡）。
4. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

---

## 汇总卡字节数自证

```
4331 字节
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
