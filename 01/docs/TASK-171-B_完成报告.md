# TASK-171-B 完成报告（1.0 首批 · 四厅导航 HUD 实装）

## 交付物清单
1. `godot/scripts/hall_nav_panel.gd`（新）：四厅列表（hall_name/台数取自 exhibit_*.json、当前厅 ● 高亮）；点厅名 → `ExhibitHost.switch_hall()`；上一厅/下一厅按钮；**M** 开关（KEY_M）、**N/P** 快速切厅（面板关闭可用）、**ESC** 仅开着时消费关闭；打开时互斥合上 DevicePicker/EncyclopediaPanel（调用二者 `close_panel()`）；宿主 `get_node_or_null("/root/Main/ExhibitHost") as ExhibitHost` 直接类型引用（class_name 已注册），互调符号 switch_hall/next_hall/prev_hall/current_hall + hall_files 均自 ExhibitHost（114 落地，G-03 可对账）。
2. `godot/scenes/main.tscn`（更新）：load_steps 16→17、ext_resource 12_hallnav、HUD 下新增 HallNavPanel 节点。
3. `godot/README.md`（更新）：脚本登记表补 hall_nav_panel/encyclopedia_panel/narr_player/startup_check 四行、device_picker 行改 F1；运行方式补齐快捷键（Tab/F1/M/N/P/E/Esc）。

## 验收日志（原样）
1. `gd_symbol_check.py` → `== hall_nav_panel.gd [hall_nav_panel] funcs=10 signals=0`；`汇总：15 文件；符号池 funcs 130 / signals 7；MISS 0；已知缺口 KG 0`，rc=0
2. `gd_naming_check.py` → `扫描 15 个 gd；class_name 5 个；FAIL 0`，rc=0
3. `scene_check.py` → `[PASS] S-01 load_steps=17（ext 12 + sub 4 + 1 = 17）`、`[PASS] S-02 12_hallnav (res://scripts/hall_nav_panel.gd) 文件存在`、`[PASS] 总检：main.tscn 静态校验通过（ext 12 / sub 4）`，rc=0
4. 回归：`verify_all.py --daily --cache` → `gd PASS（15 文件 MISS 0）`、`gd_naming PASS（FAIL 0）`、**结果：38/38 通过**（见漂移）
5. 静态对照表（互调符号 → 宿主，无未定义引用）：

| hall_nav_panel 互调 | ExhibitHost 定义 | 说明 |
|---|---|---|
| `_host.switch_hall(layout)` | `func switch_hall(...) -> bool` | 点厅名/换厅（非法回退 DEFAULT_LAYOUT） |
| `_host.next_hall() / prev_hall()` | 114 新增 | N/P 快捷切厅 |
| `_host.current_hall()` | 114 新增 | 当前厅高亮基准 |
| `_host.hall_files` | PackedStringArray 四布局 | 面板列表来源（兜底常量同默认值） |

布局→厅名映射：exhibit_dawn.json→黎明厅（Dawn Hall）· exhibit_mainframe.json→大型机与小型机厅（Mainframe Hall）· exhibit_personal.json→个人计算机厅（Personal Computer Hall）· exhibit_console.json→游戏机厅（Console Hall）。

## 与任务书的漂移
- 任务书预期门禁 37/37：实况 **38/38**（03 线新增 nokia-3310 包，与 171-A 报告同口径；非本任务引入）。
- 面板位置/尺寸为自定（右上 300px，避开中置图鉴与右下拆解面板）；其余契约（键位/互斥/命名纪律）与任务书一致；Godot 不实机，静态交付 + 符号自检存证（待首启对照 godot_first_boot.md）。