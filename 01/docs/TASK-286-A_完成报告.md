# TASK-286-A 完成报告

## 交付物清单
- **F-12 预研口径卡**：新增 `docs/F12四厅白模灰盒实测预研_v1.md`（四节）——①校准清单七条逐条梳理（246-A 原文 + 静态可核/实机必测拆分表）；②逐条实测执行口径（记录表格式「校准项#N/观察步骤/观察项/结果记录」+ ①~⑦各视角截图与计时口径，结果栏留空）；③待实机清单 4 条；④与 04 线同轮执行口径（01 出白模现状、04 按 03 号动线/94 号总检卡核对，偏差以 04 线定案回写）。
- 边界遵守：未实测；04 线文档只读引用未改。

## 预研卡自证（字节数 + 三节标题 + 七条命中 + 待实机条数）
三节标题命中：`## ① 校准清单七条逐条梳理（246-A 原文 + 拆分）` / `## ② 逐条实测执行口径（供实机轮次直接填）` / `## ③ 待实机清单（逐条，不臆造「已通过」）`（④为同轮口径节）；七条全部命中（①门框尺寸②颜色③间距④反向门⑤朝向⑥调试圈⑦穿厅耗时）；待实机 4 条；字节数见日志块 2（>2500）。

## 改动清单自证
本轮只新增 2 份 md：`docs/F12四厅白模灰盒实测预研_v1.md`、`docs/TASK-286-A_完成报告.md`；未改任何 gd/脚本/布局/04 线文档。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁只读复跑：58/58 全 PASS、rc=0（日志块 1）；2. 预研卡自检：三节 + 七条 + 4 条 + 字节数（日志块 2）；3. 改动清单见上节。

## 与任务书的漂移
1. 校准七条全部标「实机必测」（观感类无静态替代）——静态可核列只记常量/坐标已定值的事实，不写成「已核对」。
2. 记录表格式与 04 线 94 号总检卡的具体表头未逐格对齐（94 号只读参照，未逐字核对 [需核实]）——实机轮次以 04 线表头为准。
3. 门禁日志与 276/281/286 同批共用同一次干净重跑（同批状态）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 50，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
== [budget] scripts/device_budget_check.py
     [SKIP] B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产 glTF 统计——占位）
     [PASS] B-06 lod_scale/hall_group 取值域（复用 layout_check P-03 门禁，复读确认）
     [PASS] B-07 流程位预留 placed*2=28（上限 60）
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（58 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 50，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（50 包）        PASS  全部 FAIL 0
结果：58/58 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（预研卡自检）

```
（三节标题命中 + 七条命中 + 字节数）
## ① 校准清单七条逐条梳理（246-A 原文 + 拆分）
## ② 逐条实测执行口径（供实机轮次直接填）
## ③ 待实机清单（逐条，不臆造「已通过」）
（七条：①~⑦ 全命中；待实机 4 条）
F12预研卡: 2780 字节
```
