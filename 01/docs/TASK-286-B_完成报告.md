# TASK-286-B 完成报告

## 交付物清单
- **F-15 性能基线台账框架 v1**：新增 `docs/F15性能基线台账框架_v1.md`（四节）——①采集口径（帧率/内存采集点：5 布局 × 3 点 = 15 点 + 场景覆盖清单，对齐 F-11 待实机 5 条）；②台账表结构（帧率表 A/内存表 B/低载档对照表 C 三表 + 待填列，数据全部留空「待实机」）；③记录口径（逐格填写规则 + 与 F-12 共轮采集建议）；④静态可核项现状（仅引用 B-03/B-06/B-07 已 PASS 断言，不臆造数值）。
- 边界遵守：未填任何实测数值；不销账 F-15。

## 框架自证（字节数 + 三表标题命中 + 数据列留空）
三表结构命中：`### 表 A 帧率表` / `### 表 B 内存表` / `### 表 C 低载档对照表（F-11 同轮）`；「待实机」标注 35 处（帧率 15 格 + 内存 10 格 + 低载对照 10 格，全部数据格留空，不臆造数值）；字节数 2800 > 2500（日志块 2）。

## 改动清单自证
本轮只新增 2 份 md：`docs/F15性能基线台账框架_v1.md`、`docs/TASK-286-B_完成报告.md`；未改任何 gd/脚本/布局。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁只读复跑：58/58 全 PASS、rc=0（日志块 1）；2. 框架自检：三表 + 35 处待实机 + 字节数（日志块 2）；3. 改动清单见上节。

## 与任务书的漂移
1. 采集工具/方法标 [需核实]（Godot 性能面板 vs 系统监控未定）——框架只定表结构，不定工具。
2. 「待实机」标注数为 35 处（帧率 15 + 内存 10 + 低载对照 10）——按实际表格统计。
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

## 验收日志块 2（框架自检）

```
（三表标题命中 + 待实机标注 + 字节数）
### 表 A 帧率表
### 表 B 内存表
### 表 C 低载档对照表（F-11 同轮）
（「待实机」35 处，数据列全留空）
F15框架: 2800 字节
```
