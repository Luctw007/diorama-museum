# DEFECT-RUN-08 面板可点 / 方块点选失效

- **状态**：closed（修复已落盘，待用户实机确认）
- **日期**：2026-11-09
- **报告来源**：用户实机报告——「看到的都是黑色或白色方块；按 F1 出计算机选项但不能选择；方块不能点击」
- **影响范围**：F1 设备面板 / Tab 图鉴面板 / M 四厅导航面板不可点选；设备白模点选无反馈；背光面全黑

## 根因

1. **鼠标捕获与 UI 未统一（主因）**：`player.gd` 启动即 `MOUSE_MODE_CAPTURED`。捕获模式下
   Control 收不到鼠标事件 → F1/Tab/M 面板的按钮点了没反应。
2. **点选坐标与捕获状态脱钩**：`inspect_controller.gd` 把点击一律当「屏幕中心准星拾取」
   （RUN-05/06 时代的设计）。用户按 ESC 释放鼠标去点面板/方块后，真实点击位置被丢弃，
   仍按屏幕中心拾取 → 方块点不中、无高亮。
3. **场景无环境光**：只有一盏 DirectionalLight3D，无材质白模的背光面全黑（"黑色方块"观感）。

## 修复

- `player.gd`：`_set_captured` 公开为 `set_captured(on)`，供 UI 调用。
- `device_picker.gd` / `encyclopedia_panel.gd` / `hall_nav_panel.gd`：toggle/close_panel 后统一调
  `_sync_panel_mouse()`——任一面板可见即释放捕获，全关后恢复捕获。
- `inspect_controller.gd`：点选坐标自适应——`MOUSE_MODE_VISIBLE` 用 `event.position`，
  捕获中用屏幕中心。
- `main.tscn`：新增 WorldEnvironment（颜色环境光 0.5），背光面不再纯黑。

## 验证

- `gd_symbol_check.py`：MISS 0；`gd_naming_check.py`：FAIL 0。

## 用户重测（务必）

1. **完全退出 Godot 再重开**（防旧缓冲回写），弹窗选 Reload；
2. 按 F1 → 面板应弹出且**可用鼠标点击**设备条目（会装载对应设备包）；
3. 关闭面板 → 用鼠标直接点方块（或捕获态下把准星对准方块点左键）→ 方块应**变橙色高亮**，
   左上 HUD 显示「[选中] 组件名 + role」；
4. 观察方块背光面不再是纯黑（有淡淡环境光）。
