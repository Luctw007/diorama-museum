# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Node3D
## Inspect 观察交互控制器（M1）：旋转 / 缩放 / 平移 / 点选查看，对齐 04 线
## 《01_交互抽象与状态机》Inspect 原语。桌面键鼠版本；VR 由输入适配层复用同一抽象。
##
## 交互定义：
## - 左键拖拽     轨道旋转（绕设备枢轴，水平 yaw / 垂直 pitch，速率 0.3°/像素）
## - 滚轮         缩放（围绕枢轴半径钳制 [0.5m, 5m]，每格 0.1m）
## - 中键拖拽     屏幕平面平移（pan，移动目标节点）
## - 鼠标悬停点选 屏幕空间最近节点拾取（将节点全局位置投影到屏幕，取 18px 内最近者）
## - R 键         复位视角（恢复初始 orbit 参数）
## - F 键         聚焦当前选中节点（相机对准它）
##
## 自检清单（信号/方法）：
## - var target: Node3D              被观察目标（DeviceRoot 装载的根装配体）
## - func set_target(node)           设置观察目标并记录初始位姿
## - func picked_node() -> Node3D    当前选中节点（无则 null）
## - signal node_picked(node)        点选变化（供 HUD 显示 role 文案）
## - func reset_view() / focus_selected()   视角复位 / 聚焦
## - 与 device_loader.get_node_role() 联用：把 role 文案交给 HUD

signal node_picked(node: Node3D)

const ORBIT_SPEED := 0.3 / 100.0   # 弧度/像素
const PAN_SPEED := 0.9             # 比例系数
const PICK_RADIUS_PX := 18.0

var target: Node3D
var _pivot := Vector3.ZERO
var _yaw := 0.45
var _pitch := 0.15
var _radius := 2.2
var _pan := Vector2.ZERO
var _dragging := false
var _panning := false
var _hovered: Node3D
var _selected: Node3D
var _hud_label: Label

## 状态布尔开关（TASK-106B，拆解入口）：
##   _explode_mode == false → 行走/观察（默认，玩家自由环视、界面点选）
##   _explode_mode == true  → 拆解视图（E 进入；Esc/B 退出回到行走）
## 本布尔与 ExplodeController 的 State 同步（_ready 里监听 state_changed 信号），
## 避免两处状态漂移；拆解算法本体在 explode_controller.gd，此处只做入口转发。
var _explode_mode := false


func set_target(node: Node3D) -> void:
	target = node
	if target != null:
		_pivot = _estimate_pivot(target)
	reset_view()


func _estimate_pivot(node: Node3D) -> Vector3:
	# M1 简化：目标节点世界原点附近（占位阶段设备未铺开）
	if node == null:
		return Vector3.ZERO
	var aabb := AABB()
	for child in node.find_children("*", "MeshInstance3D", true, false):
		var mi := child as MeshInstance3D
		if mi != null and mi.mesh != null:
			aabb = aabb.merge(mi.global_transform * mi.mesh.get_aabb())
	if aabb.size.length() > 0.001:
		return aabb.get_center()
	return node.global_position


func set_hud_label(label: Label) -> void:
	_hud_label = label


func _unhandled_input(event: InputEvent) -> void:
	if target == null:
		return
	if event is InputEventMouseButton:
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				_dragging = event.pressed
				if event.pressed:
					# RUN-08：鼠标捕获中坐标恒为屏幕中心（准星拾取）；
					# 鼠标可见（面板打开/ESC 释放）时用真实点击位置拾取。
					var pick_pos: Vector2 = event.position \
							if Input.mouse_mode == Input.MOUSE_MODE_VISIBLE \
							else get_viewport().get_visible_rect().size * 0.5
					_update_hover(pick_pos)
			MOUSE_BUTTON_MIDDLE:
				_panning = event.pressed
			MOUSE_BUTTON_WHEEL_UP:
				if event.pressed:
					_radius = clampf(_radius - 0.1, 0.5, 5.0)
			MOUSE_BUTTON_WHEEL_DOWN:
				if event.pressed:
					_radius = clampf(_radius + 0.1, 0.5, 5.0)
	elif event is InputEventMouseMotion:
		if _dragging:
			_yaw -= event.relative.x * ORBIT_SPEED
			_pitch = clampf(_pitch - event.relative.y * ORBIT_SPEED, -1.2, 1.2)
		elif _panning:
			_pan += Vector2(event.relative.x, event.relative.y) * PAN_SPEED * 0.002
		else:
			_update_hover(event.position)
	elif event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_R:
				reset_view()
			KEY_F:
				focus_selected()
			KEY_E:
				_try_enter_explode()
			KEY_ESCAPE, KEY_B:
				_exit_explode_to_walk()


func _process(_delta: float) -> void:
	if target == null:
		return
	_apply_view()


func _apply_view() -> void:
	# 相机绕枢轴（沿目标所在平面）：目标节点自身的朝向保持为"展示台架"（不动），
	# 旋转/平移作用到相机（由本控制器持有 camera）。
	var camera := get_viewport().get_camera_3d()
	if camera == null:
		return
	var dir := Vector3(cos(_pitch) * sin(_yaw), sin(_pitch), cos(_pitch) * cos(_yaw))
	camera.global_position = _pivot + dir * _radius + Vector3(_pan.x, 0.0, _pan.y)
	camera.look_at(_pivot + Vector3(_pan.x, 0.0, _pan.y), Vector3.UP)


func _update_hover(screen_pos: Vector2) -> void:
	var camera := get_viewport().get_camera_3d()
	if camera == null or target == null:
		return
	var best: Node3D = null
	var best_dist := PICK_RADIUS_PX
	var best_cam_z := INF
	for child in target.find_children("*", "Node3D", true, false):
		if not child.name.to_lower().begins_with("mesh") and child.get_child_count() == 0:
			continue  # 只有叶子装配体参与点选（M1 简化）
		var projected := camera.unproject_position(child.global_position)
		if camera.is_position_behind(child.global_position):
			continue
		var d := screen_pos.distance_to(projected)
		var camz := camera.global_position.distance_to(child.global_position)
		if d <= best_dist and camz < best_cam_z:
			best_dist = d
			best_cam_z = camz
			best = child
	_set_selected(best)


func _set_selected(node: Node3D) -> void:
	if _selected == node:
		return
	_clear_highlight(_selected)
	_selected = node
	if _selected != null:
		var mi := _first_mesh(_selected)
		if mi != null:
			var mat := mi.material_override as StandardMaterial3D
			if mat == null:   # 白模无材质 → 现建 override，保证高亮可见
				mat = StandardMaterial3D.new()
				mi.material_override = mat
			mat.emission_enabled = true
			mat.emission = Color(1.0, 0.6, 0.1)
			mat.emission_energy_multiplier = 0.6
		if _hud_label != null:
			var role: String = device_loader_hint.get_node_role(_selected) if device_loader_hint != null else ""
			_hud_label.text = "[选中] %s\n%s" % [_selected.name, role if role != "" else "（无 role 标注）"]
	node_picked.emit(_selected)


func _clear_highlight(node: Node3D) -> void:
	if node == null:
		return
	var mi := _first_mesh(node)
	if mi != null and mi.material_override is StandardMaterial3D:
		(mi.material_override as StandardMaterial3D).emission_enabled = false


func _first_mesh(node: Node3D) -> MeshInstance3D:
	for child in node.find_children("*", "MeshInstance3D", true, false):
		return child as MeshInstance3D
	return null


func picked_node() -> Node3D:
	return _selected


func reset_view() -> void:
	_yaw = 0.45
	_pitch = 0.15
	_radius = 2.2
	_pan = Vector2.ZERO
	if target != null:
		_pivot = _estimate_pivot(target)


func focus_selected() -> void:
	if _selected == null:
		if target != null:
			_pivot = _estimate_pivot(target)
		return
	_pivot = _selected.global_position
	_radius = clampf(_radius, 0.5, 5.0)


## 取兄弟节点 ExplodeController（本节点挂在 DeviceRoot 下，爆炸算法本体在那里）。
func _explode_ref() -> Node:
	return get_node_or_null("../ExplodeController")


## 交互键 E（input_profile.gd INTERACT_KEY）：选中设备后进入拆解视图。
## 转发链：InspectController._try_enter_explode → ExplodeController.set_exploded()（状态机入口）。
func _try_enter_explode() -> void:
	if target == null or _explode_mode:
		return
	var explode := _explode_ref()
	if explode == null:
		_explode_mode = false
		return
	_explode_mode = true
	@warning_ignore("unsafe_method_access")
	explode.set_exploded()


## Esc/B（input_profile.gd WALK_EXIT_KEYS）：退出拆解、回到行走。
## 布尔开关回拨并消费事件（不再传给 player.gd 的 ui_cancel，避免误释放鼠标捕获）。
## 预检说明（TASK-112）：退出后相机仍处于 Inspect 观察轨道（M0 设计：设备装载即观察态，
## _apply_view 持续接管相机）；"行走视角"此刻 = 观察轨道 + 鼠标捕获环视。若要字面
## "回到装载前视角"，需引入行走/观察状态切换（属状态机语义变更，不在此做最小修复边界内）。
func _exit_explode_to_walk() -> void:
	if not _explode_mode:
		return
	_explode_mode = false
	var explode := _explode_ref()
	if explode != null:
		@warning_ignore("unsafe_method_access")
		explode.set_close()
	get_viewport().set_input_as_handled()


# 由 Main 装配注入（避免 device_loader 与 inspect_controller 的循环引用）
var device_loader_hint: Node = null


func _ready() -> void:
	# 约定：InspectController 挂在 DeviceRoot（device_loader）下
	var parent_node := get_parent()
	if parent_node != null and parent_node.has_method("get_node_role"):
		device_loader_hint = parent_node
		set_target(parent_node as Node3D)
	# 选中 HUD：历史上 set_hud_label 无人调用——这里自建标签挂 HUD（与 gateway_client 同模式）
	var hud := get_node_or_null("/root/Main/HUD") as CanvasLayer
	if hud != null and _hud_label == null:
		_hud_label = Label.new()
		_hud_label.position = Vector2(16, 40)
		_hud_label.add_theme_font_size_override("font_size", 16)
		hud.add_child(_hud_label)
	# 拆解入口布尔开关与 ExplodeController 状态同步（TASK-106B）
	var explode := _explode_ref()
	if explode != null and explode.has_signal("state_changed"):
		explode.state_changed.connect(func(_old: int, new_state: int) -> void:
			_explode_mode = new_state == 2)   # 2 = ExplodeController.State.EXPLODED
