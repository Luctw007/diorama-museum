# TASK-266-B 完成报告

## 交付物清单
- **预算表 v1**：新增 `docs/F4设备实例预算表_v1.md`（2516 字节）——七项预算（B-01 单厅 ≤20 / B-02 全馆 ≤30 / B-03 max_running ≤4 / B-04 co_active_max 占位 / B-05 顶点材质占位 / B-06 lod_scale 复用门禁 / B-07 流程位 placed×2）+ 占位项清单 3 条 + 断言挂载建议（不自行改 verify_all）。
- **预算断言脚本**：新增 `scripts/device_budget_check.py`（独立脚本）——读全馆 5 件布局逐项断言；B-04/B-05 如实 SKIP；自跑 rc=0。
- 边界遵守：不销账 F-4（台账口径保持）；不改 verify_all 框架；不改 02/03/04/05 线。

## 预算断言自证（逐项输出 + rc）
B-01 五厅各 PASS（2/4/1/4/3 台，上限 20）；B-02 合计 14 ≤ 30 PASS；B-03 PASS；B-04 SKIP（co_active_max 默认 3 待实测）；B-05 SKIP（依赖正式资产）；B-06 PASS；B-07 28 ≤ 60 PASS。汇总 PASS 9 行 / SKIP 2 项 / FAIL 0 处，rc=0（日志块 2）。

## 预算表自证（字节数 + 预算项数 + 占位项清单）
字节数 2516 > 2500；预算项 7 项；占位项 2 项（B-04 待实测、B-05 待正式资产）+ 补充项 1 条（材质上限口径需 02 线补，[需核实]）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：55/55 全 PASS、rc=0（日志块 1）；2. 预算断言自证：rc=0（日志块 2）；3. 预算表自证：2516 字节 + 7 项 + 占位 2 项；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. **不自行挂载 verify_all**：任务书「挂门禁」——按预算表 §三建议交统筹收口（挂载权归门禁收口方），脚本独立自跑 rc=0 为证。
2. 内容包基线为 48 包（任务书写 47，他线滚动产包，实测为准）；预算表只统计布局台数（14 台），不逐包统计包内资产。
3. B-04/B-05 按红线标「占位」不写死上限；co_active_max 默认 3 引 02 线 B-4 待办。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 48，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 154 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（55 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 48，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 154 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（48 包）        PASS  全部 FAIL 0
结果：55/55 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（device_budget_check.py 自跑）

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

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 55/55 通过（2026-11-21 23:08:42）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 48 ≥ 30
[PASS] R2 槽位 mame-apple2 已登记后端 gw.emulators.mame_apple2
[PASS] R2 槽位 mame-apple2 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 simh-pdp8 已登记后端 gw.emulators.simh_pdp8
[PASS] R2 槽位 simh-pdp8 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 stella 已登记后端 gw.emulators.stella
[PASS] R2 槽位 stella run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 第二批槽位 simh-hp2100 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 许可记录存在 licenses/MAME.md
[PASS] R2 许可记录存在 licenses/SIMH.md
[PASS] R2 许可记录存在 licenses/Stella.md
[INFO] R4 gw\emulators\mame_apple2.py: 「占位」×1
[INFO] R4 残留扫描完成：命中 1 处（含骨架注记与新发现，只暴露不计 rc）
汇总：硬断言 FAIL 0 处 → rc=0
RELEASE_RC=0
```
