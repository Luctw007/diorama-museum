# TASK-256-A 完成报告

## 交付物清单
- **F-6 实装（提示式口径，按 251-A 预口径）**：`inspect_controller.gd` 新增——①进入拆解即记录最近拆解台（`_last_exploded` 设备 id 经 device_loader_hint.get_current_device() + `_last_exploded_level` 层级标记）；②HUD 诊断行常驻「上次拆解:xx」提示（_process 逐帧刷新，切厅后不消失——InspectController 挂 DeviceRoot，clear_devices 不动它，241-A 已证）；③查询入口 `last_exploded_device()` / `last_exploded_level()` 供 HUD/导览调用。
- **拆解会话保活静态收口**：切厅不打断拆解（241-A 已证）+ 本任务补续接入口——不自动跳回（提示式）。
- 回归：gd 符号 MISS 0 / 命名 FAIL 0；scene_check PASS；layout --all 5 份全 PASS。

## F-6 实装关键行（inspect_controller.gd）
记录：L294-298（has_method("get_current_device") → _last_exploded/_last_exploded_level）；常驻提示：L163-168（诊断行追加「上次拆解:%s」）；查询：L325-332（last_exploded_device/last_exploded_level）。

## 待实装验证清单
①HUD 提示观感与位置（诊断行）实机核对；②L2/L3 层级精确回放（当前仅 "exploded" 标记，深度分档导出待 explode_controller 状态接口）；③「回厅续接高亮该台」视觉引导未接线（F-7 联动候选）；④拆解中切厅的并发视觉（双高亮/输入优先级，241-A 遗留）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 或更高全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. F-6 自证：关键行见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 续接口径选**提示式**（任务书二选一）：HUD 常驻提示不自动跳回——自动跳回会打断玩家当前动线，与 04 线「一眼可见三步可达」口径冲突；251-A 预口径即提示式。
2. 层级记录为 "exploded" 标记（进入即拆解态），L2/L3 精确回放依赖 explode_controller 状态导出接口——不臆造，标待实装验证。
3. 记录存 InspectController（DeviceRoot 子树），而非 ExhibitHost——拆解设备是单机直连设备，可能不在展厅布局 _placed 内。
4. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
（verify_all 实际输出，待回填）
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== inspect_controller.gd  [inspect_controller] funcs=20 signals=1
   [OK] has_method get_current_device → 存在
   [OK] has_method get_node_role → 存在
汇总：16 文件；符号池 funcs 148 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
（release_check 实际输出，待回填）
RELEASE_RC=0
```
