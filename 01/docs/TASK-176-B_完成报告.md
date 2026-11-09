# TASK-176-B 完成报告（第二批设备包接纳的引擎侧支持）

## 交付物清单
1. `scripts/gen_exhibit_index.py`（改）：`HALL_OF` 新增 `phone/pda → 手机与手持（Mobile & Handheld）`、补 `personal-computer → 个人计算机厅`（历史缺失键，12 台曾静默沉入示例厅）、`workstation → 个人计算机厅`（173-A「个人机/工作站」同组口径）；`HALL_ORDER` 追加「手机与手持」（游戏机厅之后、示例之前）；未知 category 不再静默沉入示例厅——stderr 打印 `[需核实] 未归类 category=…（设备 …）` 并归入置末「未归类（Unclassified）」厅。
2. `godot/content/exhibit_index.json`（重生成）：34 台 6 厅（黎明 4 / 大型机小型机 4 / 个人计算机 14 / 游戏机 6 / 手机与手持 4 / 示例 2）；Nokia 3310 与 dynatac-8000x、iphone、palm-pilot 同入「手机与手持」，无未归类告警；generated 刷新 2026-11-10T01:14:48。
3. `godot/scripts/exhibit_index.gd`（改）：新增 `get_paged_devices(page, page_size)`（全馆平铺按 name 不区分大小写稳定排序后切片，返回 page/page_size/total/items；命名避开原生方法；既有契约方法只增不改）。
4. `godot/content/README.md`（自动重写）：nokia-3310 入包清单（validate FAIL 0 通过）与字段齐备表（gltf=6——`sync_content.measure()` 兼容 meshes/ 与 assemblies/ 双目录计数，仅改计数口径、校验语义与退出码未动）。

## 验收日志（原样）
1. `pkg_registry.py --json` → ready 32 / wip 0，含 `nokia-3310`
2. `sync_content.py` → nokia-3310 复制完成 validate 通过；`README 已重写（目录包 1582 行）`；`同步汇总：32 包，失败 0` rc=0；`--dry-run` → `同步汇总：0 包，失败 0` rc=0
3. `gen_exhibit_index.py` → 各厅台数：黎明 4 / 大型机与小型机 4 / 个人计算机 14 / 游戏机 6 / 手机与手持 4 / 示例 2；`合计 34 台`；**无未归类告警** rc=0
4. `gen_exhibit_index.py --verify` → `verify 结果：通过（0 条差异）` rc=0
5. `gd_naming_check.py` → `扫描 15 个 gd；class_name 5 个；FAIL 0` rc=0；`gd_symbol_check.py` → `汇总：15 文件；符号池 funcs 133 / signals 7；MISS 0` rc=0
6. 回归：`verify_all.py --daily --cache` → **结果：39/39 通过**（catalog 步 `verify：24 片 / 1582 行，通过`）rc=0；`release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. `workstation`（next 包）任务书未指定厅：按 173-A「个人机/工作站」同组口径归入个人计算机厅（无未归类告警）。
2. 任务书列出的 handheld / appliance 类目**实际未出现**（32 包 category 扫描：phone×3/pda×1/workstation×1 等），按「未实际出现的值不硬造」未建立映射。
3. **门禁曾两度受他线并发写干扰**：catalog 步先报「28 片/1720 行不一致」（catalog_ref 亦曾 FAIL 1）——根因之一是工作源中分类名含 `/`（如 05 线「键鼠/输入」）使 `gen_catalog_bundle` 落盘炸掉、bundle 未再生；已按红线只改 01 侧工具（文件名安全化 `／`），源数据未动；重跑后 catalog 步 `24 片 / 1582 行，通过`、门禁 39/39 收敛。
4. README 中 nokia-3310 名称显示 `?`（03 线 meta.name 形态非本任务口径，未改他线文件，仅记录）。未下载任何介质；未做 git。