# TASK-241-A 完成报告

## 交付物清单
- **HallNavPanel 归类**：hall_nav_panel.gd 分组显示——「枢纽（hall_group=hub）」组（HUB_FILE=exhibit_hub.json 按钮）+「子厅」组（四厅）；当前厅「●」高亮；新增 _add_group_label/_add_hall_button。
- **启动厅定案**：exhibit_host.gd DEFAULT_LAYOUT → exhibit_hub.json（L27）。理由：对齐 04 线 03 号动线「大厅为入口动线枢纽、一眼可见三步可达」（221-A §②）；hub 已正式化（236-A）。定案后启动=1 台镇馆白模+4 门框，消除 dawn 设备与 hub 门框并存悬置；godot_first_boot 步 3 同步（241-B）。
- **三系统衔接收口**：新增 docs/F3三系统衔接收口_v1.md——图鉴/真跑/拆解三节静态收口 + 待实装 3 条。
- 回归：gd MISS 0 / FAIL 0；scene_check PASS；layout --all 5 份全 PASS。

## 三系统衔接自证（核对结论）
- **图鉴**：encyclopedia_panel.gd 数据源=CatalogData（全量目录），无厅映射字段；厅归属仅布局 hall_group 声明；链条 布局 id → 内容包（L-02）→ 目录（catalog_ref）→ 图鉴条目——无第二套映射。
- **真跑**：gateway_client.gd 消息带 device_id（L106/L119）；launch_device.py 仅 --device 无 layout 参数（216-B 已证）；acquire_run/release_run 只做配额——切厅不清进程。
- **拆解**：Inspect/ExplodeController 挂 DeviceRoot；clear_devices 只清 ExhibitHost _placed 子树——切厅不打断拆解会话（221-A §②）。

## 待实装验证剩余清单
①真跑中切厅画面重投连续性；②拆解与展厅并发视觉（双高亮/输入优先级）；③图鉴×大厅定位联动（F-7 未接线）；④传送点全部实机行为（见 F1白模验证口径清单_v1.md 四条+5 项）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 三系统衔接自证：见上节 + F3三系统衔接收口_v1.md；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 启动厅定案选「改默认 hub」（而非 dawn 启动+并存）——理由见交付物；godot_first_boot 步 3 同步（241-B 改）。
2. 「六厅映射」实为五件布局（hub+四翼）；第六件（工作台 F-5）未产出——同源收口以「无第二套映射」为判据。
3. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。
4. 门禁预期 49/49 落后实测（46 完工包+7 步=53 项）。门禁曾两度瞬时红：m0 因 17331 端口被占、catalog_ref 因他线新包（walkman-tpsl2/cd-player）反链未跟上——独立复跑均收敛 FAIL 0，最终干净重跑 53/53（日志块 1）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 46，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（53 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 46，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（46 包）        PASS  全部 FAIL 0
结果：53/53 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（gd 自检 + scene_check + layout）

```
== hall_nav_panel.gd      [hall_nav_panel] funcs=13 signals=0
汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
  [PASS] S-01 load_steps=19（ext 13 + sub 5 + 1 = 19）
  [PASS] 总检：main.tscn 静态校验通过（ext 13 / sub 5）
主场景接线静态合法（待 Godot 实机确认表现层）
SCENE_RC=0
=== exhibit_console.json
  OK（设备 2 台）
=== exhibit_dawn.json
  OK（设备 4 台）
=== exhibit_hub.json
  OK（设备 1 台）
=== exhibit_mainframe.json
  OK（设备 4 台）
=== exhibit_personal.json
  OK（设备 3 台）
--all 完成：5 份布局
LAYOUT_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 53/53 通过（2026-11-20 01:26:06）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 47 ≥ 30
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
