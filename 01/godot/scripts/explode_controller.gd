# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Node3D
## 拆解爆炸图控制器（TASK-11C，桌面版；Godot 待实机验证）。
##
## 设备展示状态机（对齐 04 线《01_交互抽象与状态机》）：
##   CLOSED（完整） → OPENED（开盖） → EXPLODED（拆解中） → OPENED / CLOSED
## 进入/退出动作、可受理输入、拒绝反馈如下表（§explode_spec.md 全量表）：
##
## 状态    进入动作              可受理输入                       拒绝反馈
## CLOSED  姿态基准记录          切换 OPENED                      无
## OPENED  顶层盖板透明度/位移   切换 EXPLODED；滑杆仅预览         提示需先进入 EXPLODED
## EXPLODED 记录每层基准形变     滑杆、点选、切换 OPENED           运行中(running)拒绝进入并提示
##
## 互斥规则（与 InspectController）：
## - EXPLODED 锁定 Inspect 的轨道旋转（只允许整机旋转、禁止点选拖拽）；
## - Inspect 悬停点选在 EXPLODED 下照常（零件清单定位用）。
## 运行锁：网关 status(state=running) 时禁止进入 EXPLODED（占位接入点 §4）。
##
## 自检清单：
## - var explode_value: float       0..1 展开系数
## - signal state_changed(old, new) / slider_changed(value)
## - func set_open() / set_close() / set_exploded()
## - func reset_explode()           一键复原（滑杆归零 + 插值）
## - 位移公式：offset_i = explode_value × depth(i) × STEP（沿各层主轴）

signal state_changed(old_state: int, new_state: int)
signal slider_changed(value: float)

enum State { CLOSED, OPENED, EXPLODED }

const STEP := 0.12          # 每层级每单位系数的位移（米）
const SLIDER_SPEED := 2.5   # 复原/展开插值速率（1/秒）
const MAX_DEPTH := 8        # 层级深度上限（防御）

var _loader: Node = null
var _state: int = State.CLOSED
var _value := 0.0
var _target_value := 0.0
var _depth := {}             # node -> depth
var _axis := {}              # node -> Vector3（推拉主轴，默认 +X）
var _base_transform := {}    # node -> Transform3D（闭合基准）

# 运行锁占位（见 §4）：由网关状态信号驱动；M1 阶段无真实运行态，默认 false
var _device_running := false


func _ready() -> void:
	# 约定：ExplodeController 挂在 DeviceRoot（device_loader）兄弟位置或之下
	_loader = get_parent() if get_parent() != null and get_parent().has_method("get_assembly_nodes") else null
	if _loader == null:
		_loader = get_node_or_null("../DeviceRoot")
	if _loader != null and _loader.has_signal("device_loaded"):
		_loader.device_loaded.connect(_on_device_loaded)


func _on_device_loaded(_device_id: String) -> void:
	_set_state(State.CLOSED)
	_value = 0.0
	_target_value = 0.0
	_build_topology()


# ---------------------------------------------------------------- 拓扑
func _build_topology() -> void:
	_depth = {}
	_axis = {}
	_base_transform = {}
	if _loader == null:
		return
	var nodes: Dictionary = _loader.get_assembly_nodes()
	for aid in nodes:
		var node: Node3D = nodes[aid]
		_depth[node] = _compute_depth(nodes, aid, 0)
		_axis[node] = _guess_axis(nodes, aid)
		_base_transform[node] = node.transform


func _compute_depth(nodes: Dictionary, aid: String, acc: int) -> int:
	if acc > MAX_DEPTH:
		return MAX_DEPTH
	var parent_id := ""
	var entry: Dictionary = nodes[aid].get_meta("asmb_entry", {})
	parent_id = str(entry.get("parent", ""))
	if parent_id == "" or not nodes.has(parent_id):
		return acc
	return _compute_depth(nodes, parent_id, acc + 1)


func _guess_axis(nodes: Dictionary, aid: String) -> Vector3:
	# 推拉主轴：读取该装配体相对父级的平移方向；无父级 → +X
	var entry: Dictionary = nodes[aid].get_meta("asmb_entry", {})
	var tr: Variant = entry.get("transform")
	var t: Array = tr.get("translation", [0, 0, 0]) if tr is Dictionary else []
	if not t.is_empty():
		var v := Vector3(float(t[0]), float(t[1]), float(t[2]))
		if v.length() > 0.001:
			return v.normalized()
	var parent_id: String = str(entry.get("parent", ""))
	if parent_id == "" or not nodes.has(parent_id):
		return _axis.get(nodes[aid], Vector3.RIGHT)
	return _axis.get(nodes[parent_id], Vector3.RIGHT)


# ---------------------------------------------------------------- 状态机
func _set_state(next: int) -> void:
	if next == _state:
		return
	# 进入 EXPLODED 的运行锁
	if next == State.EXPLODED and _device_running:
		_request_denied("设备运行中，禁止拆解")
		return
	var old := _state
	_state = next
	match _state:
		State.CLOSED:
			for node in _base_transform:
				node.transform = _base_transform[node]
			_value = 0.0
			_target_value = 0.0
		State.OPENED:
			pass  # 开盖态：M1 以"允许拆解"为语义，不额外形变（见 explode_spec.md）
		State.EXPLODED:
			_set_locked(true)
	state_changed.emit(old, _state)


func _set_locked(_on: bool) -> void:
	# ExplodeController 与 InspectController 的互斥由 InspectController 读取
	# had_explode_lock() 决定是否禁用自身轨道旋转（见 explode_spec.md 互斥表）。
	pass


func is_explode_locked() -> bool:
	return _state == State.EXPLODED


func set_open() -> void:
	if _state == State.EXPLODED:
		_set_state(State.OPENED)
	else:
		_set_state(State.OPENED)


func set_exploded() -> void:
	_set_state(State.EXPLODED)


func set_close() -> void:
	_set_state(State.CLOSED)


func reset_explode() -> void:
	_target_value = 0.0
	if _state == State.EXPLODED:
		_set_state(State.OPENED)


func _request_denied(reason: String) -> void:
	print("[ExplodeController] 拒绝：%s" % reason)
	# HUD 提示占位：由 ExplodePanel 监听 signal 显示（M1：print + 见下）
	denied_reason.emit(reason)


signal denied_reason(reason: String)


# ---------------------------------------------------------------- 形变驱动
func _process(delta: float) -> void:
	if _state != State.EXPLODED:
		return
	# 滑杆逼近（支持面板滑杆与一键复原共用）
	if absf(_target_value - _value) > 0.001:
		var step := SLIDER_SPEED * delta
		_value = move_toward(_value, _target_value, step)
		_apply_explode(_value)
		slider_changed.emit(_value)


func set_explode_value(v: float) -> void:
	if _state != State.EXPLODED:
		_request_denied("请先进入拆解态")
		return
	_target_value = clampf(v, 0.0, 1.0)


func get_explode_value() -> float:
	return _value


func _apply_explode(v: float) -> void:
	for node in _base_transform:
		var base: Transform3D = _base_transform[node]
		var d: int = _depth.get(node, 1)
		var axis: Vector3 = _axis.get(node, Vector3.RIGHT)
		var offset: float = v * float(d) * STEP
		node.transform = base
		node.translate_object_local(axis * offset)


func get_state() -> int:
	return _state


## §4 运行锁接入点：网关 status(state=running) → 置 true；stopped/degraded → false
func set_device_running(running: bool) -> void:
	if running != _device_running:
		_device_running = running
		if running and _state == State.EXPLODED:
			_set_state(State.OPENED)  # 运行中回车：先退出拆解
			_request_denied("设备已开机，已退出拆解")
