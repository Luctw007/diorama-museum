# DEFECT-RUN-08 面板可点 / 方块点选失效

- **状态**：open（2026-11-09 晚已移交 06 线 debug 专员接棒；现场见 `D:\work\06\RUN-08_现场交接.md`）
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

## 第二轮修复（2026-11-09 用户复测：仍无橙色、无装载）

- **gltf 高亮失效**：原 `_first_mesh` 在 gltf 分支返回的是空容器 mi（真正的网格在子实例里），
  override 设上去无可见效果 → 改为直接对**命中的 MeshInstance3D** 设 override。
- **装配体原点叠加**：原拾取用装配体节点原点投影，多层部件同原点互相遮挡 → 改为按
  **真实网格 AABB 中心**投影拾取。
- **加 HUD 实时诊断行**（绿色，y=150）：`[inspect] target=… meshes=N camera=x,y,z sel=…`
  —— 用户复测时把这一行内容报回即可定位。
- `_selected` 语义保持"装配体"（role 文案载体），高亮作用于实际命中网格。

## 第三轮（2026-11-09 晚，移交前现场）

- 用户确认新代码已在跑：绿色诊断行显示 `[inspect] 初始: target=DeviceRoot:<Node3D#…>`，
  但**始终停留在"初始"文本**，未被 `_process` 每帧刷新为 `meshes=…` 实时行（用户：`没有meshs`）。
- Godot 4.3 headless 验证：脚本无 SCRIPT ERROR/Parse Error（exit=0）。
- 已加探针：`_process` 每 60 帧 `print("[inspect-proc] frame=… target=… label_ok=…")`。
- **未解之谜**：`_process` 是否在跑、为何不刷新诊断行（疑点：`_process` 未执行 / 异常退出 /
  文本被覆盖 / 用户观察窗口与运行实例不一致）。
- 下一步排查方向（供 debug 专员）：先让用户在输出面板确认 `[inspect-proc]` 是否出现——
  无 → 查脚本生命周期（节点是否被移出场景树、pause 状态）；有且 label_ok=True →
  查 Label 覆盖/绘制顺序（gateway_client 音频行位置）；有且 label_ok=False → 查 _ready 分支。
