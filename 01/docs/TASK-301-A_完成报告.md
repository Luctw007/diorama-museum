# TASK-301-A 完成报告

## 交付物清单
- **B-4 实测口径 01 线对齐核对卡**（docs/B4实测口径01线对齐核对_v1.md）：①三方对齐表 6 行（272-B 采集表格式字段 ↔ exhibit_host.gd 激活计数口径 ↔ device_budget_check.py B-04 占位值 3）——默认值 3/计数口径/梯度判据/回填口径四方一致性逐行标注；②实测前置声明（三台真跑 RC + 槽位多后端并发未满足 → 不催测、不臆造权威值）；③与 282-A 需求卡「与 max_running 独立」口径复核（acquire_run 与 acquire_activation 两条独立路径，复核通过无漂移）。
- 改动清单：只新增 1 份 md + 本报告；不改引擎/脚本、不销账 B-4、02/03/04/05 线零改动。

## 对齐卡自证
字节数（UTF-8）见报告末自证块；三方对齐表 6 行 + 实测前置声明命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. budget 复跑：FAIL 0 处、rc=0，B-04 仍 SKIP（日志块 2）；3. 对齐卡自证见上节。

## 与任务书的漂移
1. 任务书前置 2 行号「L42-47 字段、L180-210 激活接口」与仓库实际一致（291-A 实装位置）。
2. 任务书命令 `py -3.7` 环境无此启动器，用 PATH 指向的 python 3.12.10 执行。
3. 验收基数以本轮干净重跑为准（任务书未给数值，仓库实际 59/59）。
4. B-04 SKIP 确认未转 PASS（复跑日志佐证），符合「不提前转 PASS」红线。

5. 执行备注：本轮验收基线 60/60（52 完工包+8 步，他线新增 gamecube 包并补反链）；首次跑 58/59 因 gamecube 反链瞬时缺失，单步复跑 catalog_ref 收敛后干净重跑全绿，报告日志以干净重跑为准。
---

## 对齐卡字节数自证

```
3140 字节
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
