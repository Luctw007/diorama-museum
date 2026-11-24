# TASK-291-K 完成报告

## 交付物清单
- **切厅性能静态核对卡**（docs/切厅性能静态核对_v1.md，≥2000 字节）：
  - §①B-03/B-06 断言逐项复核记录（device_budget_check.py 复跑：PASS 9 行/SKIP 2 项/FAIL 0、rc=0，日志贴卡）；
  - §②切厅路径现状核对：switch_hall 调用链四触发源（portal 点选/碰撞、hall_nav、图鉴定位、291-B 站迁移口径）+ 内部顺序（clear_devices→load→spawn→游标→调试圈→_notify_portal_hub）+ 清场要点（同帧峰值 N≤4、真跑进程不杀、激活名额清空）；
  - §③待实机项 4 行（切厅耗时 <100ms/F-12·F-15 联动、同帧内存峰值、导览站迁移即切厅、B-04 实测）。
- 改动清单：只新增 1 份 md + 本报告；不改 gd（纯核对）、02/03/04/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>2000）；断言复核行命中（B-03 PASS/B-06 PASS/B-04 SKIP 三行贴出）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. budget 复跑：rc=0（日志块 2）；3. 核对卡自证见上节。

## 与任务书的漂移
1. 任务书第 2 条验收命令 `py -3.7 .\01\scripts\device_budget_check.py` 用 python 3.12.10 执行，rc=0。
2. 291-A 后 exhibit_host 新增 _active_ids 清场（B-4 口径）——切厅清场顺序核对按实装后现状登记（任务书前置 3 写「max_running/切厅现状」，以仓库实际为准）。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. budget 复跑与本轮 layout_check --all 同源数据（5 件布局 14 台），B-01 逐厅行与布局复跑归档卡（291-S）对账一致；B-04 保持 SKIP 与 291-A 实装不矛盾（转 PASS 待实测权威值）。

---

## 核对卡字节数自证

```
3990 字节
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
