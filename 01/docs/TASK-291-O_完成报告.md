# TASK-291-O 完成报告

## 交付物清单
- **拆解体验深化规格落地核对卡**（docs/拆解深化落地核对_v1.md，≥2000 字节）：
  - §①73 号规格逐条核对表 14 行：L0 整机态已落地；L1 全树爆炸部分落地（七类主轴未接）；L2 级联爆炸/子树视图、L3 代表元件**未实装**（get_depth_level 上限 L1 如实标注）；开盖 ≥60% 判定口径差异；爆炸步距 0.12vs0.16 数值差异登记待裁决；滑杆步进 0.01vs0.05 差异；零件勾选脱离/Esc 层叠返回未落地；状态保持部分；
  - §②未落地项清单 8 项（依赖引擎后续实现/03 线盖件标记/待裁决）；
  - §③与 F-6 深化（261-A）口径一致性核对：无漂移（261-A 上限 L1 与 73 号 L2/L3 未实装一致；depth_model §6 差距审阅同源）。
- 改动清单：只新增 1 份 md + 本报告；不实装、不实机、不改 04 线 73 号文档、02/03/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>2000）；核对表 14 行 + L2/L3 未落地标注命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 核对卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 爆炸步距差异（73 号建议 0.16 vs 现状 0.12）登记为「待裁决」——depth_model §4 已定 0.12（54-B 定稿），本卡不改任一方。
2. 前置 4「depth_model.md（L0-L3）」与实际一致；explode_panel.gd（零件清单/滑杆现状）为核对所需补读文件，与任务书前置 2 同目录。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

---

## 核对卡字节数自证

```
4934 字节
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
