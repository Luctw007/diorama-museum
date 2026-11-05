# TASK-106B 完成报告（拆解入口实机验证准备）

## 一、交付物（只改 01/godot/ 与 01/scripts/）
1. `godot/scripts/input_profile.gd`：登记交互键 `INTERACT_KEY="key_e"`、回退键 `WALK_EXIT_KEYS=["key_esc","key_b"]`（文档 JSON 结构同步：actions.interact / exit_explode）；
2. `godot/scripts/inspect_controller.gd`：KEY_E 触发进入拆解（转发 explode_controller.set_exploded，不重写爆炸算法）；KEY_ESCAPE/KEY_B 回退（set_close）；新增状态布尔开关 `_explode_mode`（注释注明 true=拆解视图 / false=行走，并与 state_changed 信号同步防漂移）；
3. `01/scripts/explode_entry_check.py`（新）：纯文本级接线自检（X-01~X-05）。

## 二、验收日志
- explode_entry_check：X-01~X-05 全 PASS（rc=0，含 2 处调用点对账 set_exploded/set_close 均存在于 explode_controller 函数表）
- gd_symbol_check：12 文件；funcs 108 / signals 7；MISS 0；KG 0（rc=0）

## 三、E 键按下后的链路（5 行时序，供 debug 线对照实机）
1. `_unhandled_input` 收到 KEY_E（inspect_controller）；
2. `_try_enter_explode()`：target 非空且未在拆解 → 置 `_explode_mode=true`；
3. `_explode_ref()` 取兄弟节点 DeviceRoot/ExplodeController，转发 `set_exploded()`；
4. ExplodeController 状态机 CLOSED→EXPLODED，滑杆形变驱动接管（相机 orbit 由 InspectController 照常定位）；
5. 回退：Esc/B → `_exit_explode_to_walk()`：`_explode_mode=false` → `set_close()`（EXPLODED→CLOSED，基准形变复原）→ `set_input_as_handled()` 消费事件，回到行走且不误释放鼠标捕获。

## 四、备注
- 进入条件为「设备已装载（target）」；选中零件（_selected）后按 E 效果一致，_selected 声明与输入事件存在性由 X-01/X-02 把关；
- 运行锁复用 explode_controller 既有守卫（设备运行中拒绝进入 EXPLODED），未新增算法；
- E/Esc 事件未改动 player.gd 的环视捕获逻辑（仅拆解态下 Esc 被消费）。