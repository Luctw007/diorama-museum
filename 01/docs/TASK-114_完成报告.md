# TASK-114 完成报告（四厅切换骨架）

## 交付物（exhibit_host.gd）
- `switch_hall()`：切厅清场（clear_devices）→ load_layout → spawn_devices；成功后同步 `_hall_cursor`；**保留运行配额（max_running）与调试圈设置**（`_debug_circles_on` 记忆并在切厅后重放）；
- 新增 `next_hall()/prev_hall()`：按 `hall_files` 顺序（黎明/大型机/个人机/游戏机）循环切厅；目标布局非法时**回退 DEFAULT_LAYOUT**（exhibit_dawn.json），全失败返回空串；
- 新增 `current_hall()` 查询当前布局文件名；
- 四厅布局文件（console/dawn/mainframe/personal）经 schema 校验均合法，**未做任何改动**。

## 验收证据
- `python 01/scripts/layout_check.py --all`
```text
=== exhibit_console.json    OK（设备 2 台）
=== exhibit_dawn.json       OK（设备 4 台）
=== exhibit_mainframe.json  OK（设备 4 台）
=== exhibit_personal.json   OK（设备 3 台）
--all 完成：4 份布局   rc=0
```
- Godot 输出面板日志：静态交付（本机无引擎）。预期时序：_ready load_layout(exhibit_dawn) → spawn 4 台；next_hall() ×3 → 依次 load_layout 四厅、spawn 2/4/3/4 台；每次 switch_hall 后 `_placed` 清空重建（clear_devices 释放旧 loader）；非法路径（如表内无此文件）→ push_warning 后回退 DEFAULT_LAYOUT。待实机按此对照。

## 备注
四厅设备 id 均存在于 godot/content（layout_check L-02 全过）；切换为纯本地布局操作，不涉模拟器运行配额冲突（切厅即 clear，释放旧设备）。