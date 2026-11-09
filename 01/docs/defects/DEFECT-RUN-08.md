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

## 第四轮（2026-11-09 深夜，06 线 debug 专员接棒）

### 根因（已定位，证据链闭合）

**InspectController / ExplodeController 挂在 DeviceRoot（device_loader）之下，
而 `load_device()` 第一步的 `_clear_tree()` 会 `queue_free` DeviceRoot 的**所有**子节点——
首次启动 `_ready` 自动装载第一台设备时，两个控制节点即被移出场景树。**

时序（Godot `_ready` 子先父后）：
1. InspectController._ready 先跑：自建 HUD 标签（add_child 到 HUD，父级与 DeviceRoot 无关，
   故标签幸存）、写入诊断行初始文本、set_target(DeviceRoot)；
2. DeviceRoot(DeviceLoader)._ready → scan_index → load_device(first) → _clear_tree()
   → InspectController/ExplodeController 被 queue_free；
3. 帧末两节点移出场景树 → 此后 `_process` / `_unhandled_input` 永不调用。

与全部实测现象逐条吻合：
- 诊断行**停"初始"不刷新**、无 `[inspect-proc]` 探针 → `_process` 未执行；
- 方块**点选无反应、无橙色、无 [选中] 标签** → `_unhandled_input` 未执行；
- 诊断行初始文本显示 `target=DeviceRoot` 非 null → set_target 发生在被清之前；
- "鼠标部分场景可用" → player（Room/Camera 下）与 HUD 面板均不受 DeviceRoot 影响。

### 修复（01/godot/scripts，未推送，待统筹收口）

1. **device_loader.gd**（根因修复）：新增内容专用容器 `ContentRoot`（Node3D，`_ready`
   创建；`load_device` 入口兜底创建）；根装配体一律挂 `_content_root` 下；
   `_clear_tree` 只清 `_content_root` 的子节点——控制节点与设备内容隔离，不再被误杀。
2. **警告清零（防"警告即错误"回归 + 实机输出面板清洁）**：
   - device_loader.gd：删未用局部变量 `children`；
   - inspect_controller.gd：删未用类变量 `_hovered`；局部变量 `owner` → `asmb`
     （避 Node.owner 遮蔽）；role 三元改 if 分支（消"三元值不兼容"）；
   - explode_controller.gd：局部变量 `tr` → `tf`（避 Object.tr 遮蔽）；三元改 if；
   - startup_check.gd：三处 `var name` → `entry_name`（避 Node.name 遮蔽）。

### 验证

- gd_symbol_check.py：15 文件 MISS 0 / KG 0；
- gd_naming_check.py：FAIL 0。

### 用户重测（务必）

1. **完全退出 Godot → 重开工程 → 有提示选 Reload → 按 F5**；
2. 输出面板约 1 秒后应出现 `[inspect-proc] frame=61 …` 探针（此后每 60 帧一条）；
3. HUD 绿色诊断行应从"初始"变为 `[inspect] target=DeviceRoot meshes=N camera=… sel=…`
   并持续刷新；
4. 准星对准白模点左键 → 应出现**橙色高亮** + 左上 `[选中]` 标签（含 role 文案）；
5. F1 面板点条目装载设备 → 方块树随包切换；E 键拆解三态可用（ExplodeController 幸存）。
   把结果（截图或文字）发回，确认后本档案置 closed。

## 第五轮（2026-11-10 凌晨，用户复测：橙色已出，新报两点）

用户复测反馈（截图 2026-11-10 001114.jpg）：
- **橙色高亮已生效**：`[选中] panel` 标签 + 诊断行实时刷新
  `[inspect] target=DeviceRoot meshes=4 camera=1.0,3.7,-2.9 sel=panel`——第四轮根因修复确认有效。
- **新问题 1（"位置在地下"）**：轨道相机 `_apply_view` 无地面钳制，`_pitch` 下压（下限 -1.2 弧度）
  时相机可绕到枢轴下方 y≈-1，视角钻入地板。
- **新问题 2（"无法进入"）**：E 键链路本身通（ExplodeController 已随 ContentRoot 修复幸存），
  但进入 EXPLODED 后展开系数 `_value=0` 且无演示展开——白模纹丝不动、无可见反馈，
  观感等于"没进去"。

### 修复（第五轮）

1. inspect_controller.gd `_apply_view`：相机位置 y 钳制 `maxf(pos.y, 0.15)`，永不钻地板；
2. inspect_controller.gd 诊断行加 `mode=拆解/观察` 字段（HUD 一眼确认拆解态）；
3. explode_controller.gd `set_exploded()`：进入 EXPLODED 且基准拓扑已建时
   `_target_value = 0.35` 自动演示展开，滑杆仍可调（0..1）。

### 验证

- gd_symbol_check.py：MISS 0 / KG 0；gd_naming_check.py：FAIL 0。

### 用户重测（务必）

1. **完全退出 Godot → 重开工程 → 有提示选 Reload → 按 F5**；
2. 环视/滚轮缩放任意角度 → 相机永不低于地板（不再有"在地下"视角）；
3. 点选白模变橙后按 **E** → 白模应立即沿轴**展开散开**（演示展开），HUD 诊断行
   `mode=拆解`；右下角拆解面板显示"设备状态：拆解中"，滑杆可继续拖；Esc/B 退出复原；
4. 把结果（截图或文字）发回，确认后本档案置 closed。

## 第六轮（2026-11-10，用户复测：无法移动）

用户反馈"无法移动了"。根因：第五轮修复使 InspectController 复活后，`_apply_view` 每帧
无条件接管相机——player.gd 的 WASD 移动与自由环视（rotation_degrees）全部被覆盖
（第四轮前控制器已死，WASD 反而可用；复活后行走能力丢失，体验回退）。

### 修复（第六轮，inspect_controller.gd）

1. 观察轨道上补行走：`_process` 在鼠标捕获（captured）时读 W/A/S/D，
   沿相机水平朝向平移 `_pivot`（速度 WALK_SPEED=3.0，与 player.MOVE_SPEED 一致），
   相机随 `_apply_view` 跟随——WASD 恢复移动且永不钻地（第五轮 y 钳制仍生效）；
2. 补自由环视：captured 下非拖拽鼠标移动也旋转 `_yaw/_pitch`（原只有左键拖拽可环视），
   环视同时按准星中心更新悬停拾取；面板打开（鼠标可见）时行走/环视自动停用。

### 验证

- gd_symbol_check.py：MISS 0 / KG 0；gd_naming_check.py：FAIL 0。

### 用户重测（务必）

1. **完全退出 Godot → 重开工程 → 有提示选 Reload → 按 F5**；
2. WASD 可自由走动、鼠标移动自由环视（无需按住左键）、滚轮缩放；
3. 走远/走近设备后点选仍可橙色高亮；按 E 白模展开、Esc/B 复原；
4. 打开 F1 面板（鼠标可见态）时行走/环视自动停用，关闭恢复。
   把结果（截图或文字）发回，确认后本档案置 closed。

## 第七轮（2026-11-10，用户复测：环视上下方向相反）

用户反馈"上下方向相反，有点像操作mac"。根因：pitch 更新用 `_pitch - relative.y * ORBIT_SPEED`，
鼠标上移（relative.y 为负）反而增大俯角 = 低头，与直觉（上移=抬头）相反。
修复：自由环视与左键拖拽环视两处 pitch 一律改 `+relative.y`（上移=抬头），yaw 不变。

### 验证

- gd_symbol_check.py：MISS 0 / KG 0；gd_naming_check.py：FAIL 0。

### 用户重测（务必）

1. **完全退出 Godot → 重开工程 → 有提示选 Reload → 按 F5**；
2. 鼠标上移=抬头看天、下移=低头看地（无论自由环视还是按住左键拖拽）；
3. 其余：WASD 走动、滚轮缩放、点选橙色、E 展开、Esc 复原。
   把结果（截图或文字）发回，确认后本档案置 closed。
