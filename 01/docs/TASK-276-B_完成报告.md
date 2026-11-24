# TASK-276-B 完成报告

## 交付物清单
- **F-10 预研口径卡**：新增 `docs/F10大厅导览镜头预研_v1.md`（四节）——①镜头规格梳理（39 号馆长路线 8 站卡 ≈34 分钟路径 + 运镜节奏 + 静态接线点「导览启动→镜头接管→站间迁移→回行走」+ 57 号参数衔接「1.4 m/s 播报限速档/角速度红线/0.15s 阻尼」+ 现状差距）；②与 F-9 口播联动口径（复用单口播互斥通道、播报中限速同步、超时推进等句末）；③待实机核对清单 7 条；④实装轮次建议（待排/待用户实机，不销账）。
- 边界遵守：未实装；04 线 57/39 号文档只读引用未改。

## 预研卡自证（字节数 + 四节标题 + 待实机条数）
四节命中：`## ① 镜头规格梳理` / `## ② 与 F-9 口播接入的联动口径` / `## ③ 待实机核对清单（逐条，不臆造「已通过」）` / `## ④ 实装轮次建议`；待实机 7 条（接管手感/双档限速/红线复测/口播同步/一键切换/时长误差/晕动复测）；字节数 3118 > 2500（日志块 2）。

## 改动清单自证
本轮只新增 2 份 md：`docs/F10大厅导览镜头预研_v1.md`、`docs/TASK-276-B_完成报告.md`；未改任何 gd/脚本/布局/04 线文档。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁只读复跑：58/58 全 PASS、rc=0（日志块 1）；2. 预研卡自检：四节 + 7 条 + 字节数（日志块 2）；3. 改动清单见上节。

## 与任务书的漂移
1. 57 号参数引用为 v2 口径（双档限速 2.5/1.4、±70°、阻尼 0.15s）——player.gd 仍为 M0 单档常量，差距如实列「现状差距」行，不写「已对齐」。
2. 导览调度器接线点建议新建（01 线），不入 39 号 §5 伪代码（04 线明确「不入引擎」）。
3. 门禁日志与 276-A 共用同一次干净重跑（同批状态，276-A 挂载后门禁含 budget 行）。

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
## ① 镜头规格梳理
## ② 与 F-9 口播接入的联动口径
## ③ 待实机核对清单（逐条，不臆造「已通过」）
## ④ 实装轮次建议
（待实机 7 条）
F10预研卡: 3118 字节
```
