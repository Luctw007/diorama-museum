# TASK-281-B 完成报告

## 交付物清单
- **F-11 预研口径卡**：新增 `docs/F11低载档验证预研_v1.md`（2728 字节）——①RC-A-06 判据梳理（66 号原文「低载与 HUD｜黄｜HUD 正常已证；低载档未测」+ 静态可核/实机必测拆分，数值判据缺位标 [需核实]）；②低载档规格静态核对（占位盒降级/白模灰盒/lod_scale 未实装/max_running=1/B-04·B-05 占位 六行表）；③待实机清单 5 条；④实装轮次建议（待用户实机轮次，与 F-15 同轮）。
- 边界遵守：未实装、未做低载档验证本体；66 号只读引用未改。

## 预研卡自证（字节数 + 四节标题 + 待实机条数）
四节命中：`## ① RC-A-06 判据梳理` / `## ② 低载档规格静态核对` / `## ③ 待实机清单（逐条，不臆造「已通过」）` / `## ④ 实装轮次建议`；待实机 5 条（低配流畅性/切厅加载时长/内存台账/lod_scale 运行时/HUD 低载复测）；字节数 2728 > 2500（日志块 2）。

## 改动清单自证
本轮只新增 2 份 md：`docs/F11低载档验证预研_v1.md`、`docs/TASK-281-B_完成报告.md`；未改任何 gd/脚本/布局/04 线文档。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁只读复跑：58/58 全 PASS、rc=0（日志块 1）；2. 预研卡自检：四节 + 5 条 + 2728 字节（日志块 2）；3. 改动清单见上节。

## 与任务书的漂移
1. RC-A-06 无低载档数值判据（66 号只记「低载档未测」）——判据数值需 04 线补或实机轮次自定基线，本卡标 [需核实] 不落定论。
2. 前置「30 台齐备」已满足（48+ 包 ready；布局 14 台白模）——任务书「47 内容包」滞后，实测为准。
3. 门禁日志与 281-A 共用同一次干净重跑（同批状态）。

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
（四节标题命中 + 待实机条数 + 字节数）
## ① RC-A-06 判据梳理
## ② 低载档规格静态核对
## ③ 待实机清单（逐条，不臆造「已通过」）
## ④ 实装轮次建议
（待实机 5 条）
F11预研卡: 2728 字节
```
