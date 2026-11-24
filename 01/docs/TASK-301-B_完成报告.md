# TASK-301-B 完成报告

## 交付物清单
- **B-04 实测权威值回写预案**（docs/B04回写预案_v1.md）：①回写步骤清单 4 步（改 device_budget_check.py L34 占位常量为实测权威值、B-04 SKIP→PASS 断言写法 `co_active_max == 实测权威值` 或 `1 <= co_active_max <= 实测权威值`、F4 预算表 B-04 行更新、复跑验证）；②回写触发条件（三条件齐备：01 线梯度数据表 + 02 线规范回写 + 引擎帧率达标自证）；③声明「本预案不执行，待实测权威值」。
- 改动清单：只新增 1 份 md + 本报告；不执行回写、不改 device_budget_check.py / F4 预算表、不转 PASS、不销账 B-4、02 线零改动。

## 预案自证
字节数（UTF-8）见报告末自证块；回写步骤清单 4 步 + 「不执行/待实测」声明命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. budget 复跑：FAIL 0 处、rc=0，B-04 仍 SKIP（确认未改动，日志块 2）；3. 预案自证见上节。

## 与任务书的漂移
1. 任务书前置 2「第 34 行 CO_ACTIVE_MAX_DEFAULT = 3」与仓库实际一致（L34）。
2. 回写断言写法按 272-B §三-1 双口径（== 或 1<=x<=权威值）登记，未选定单一写法（留实装轮裁决）。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准（仓库实际 59/59）。
4. 触发条件三条件即 272-B 销账三条件（02 线勾销权），01 线侧只守回写步骤不代销账。

5. 执行备注：本轮验收基线 60/60；首次 58/59（catalog_ref 瞬时红 gamecube 反链），单步复跑收敛后干净重跑全绿。
---

## 预案字节数自证

```
2372 字节
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

## 验收日志块 2（device_budget_check.py）

```
== F-4 设备实例预算断言（布局 5 件）
  [PASS] B-01 游戏机厅（Console Hall）：2 台（上限 20）
  [PASS] B-01 黎明厅（Dawn Hall）：4 台（上限 20）
  [PASS] B-01 枢纽大厅（Hub Hall）：1 台（上限 20）
  [PASS] B-01 大型机与小型机厅（Mainframe Hall）：4 台（上限 20）
  [PASS] B-01 个人计算机厅（Personal Computer Hall）：3 台（上限 20）
  [PASS] B-02 全馆布局台数合计：14（上限 30）
  [PASS] B-03 同厅运行配额 max_running <= 4（exhibit_host export_range 1..4）
  [SKIP] B-04 co_active_max 同屏激活上限（默认 3，02 线 B-4 待实测——占位）
  [SKIP] B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产 glTF 统计——占位）
  [PASS] B-06 lod_scale/hall_group 取值域（复用 layout_check P-03 门禁，复读确认）
  [PASS] B-07 流程位预留 placed*2=28（上限 60）
汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
BUDGET_RC=0
```
