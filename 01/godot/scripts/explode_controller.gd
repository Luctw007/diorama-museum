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
## TASK-306-H：聚焦运镜请求（target=目标框中心，duration=时长秒）。
## 相机插值本体（tween）由 player.gd 消费本信号实现（标待实机）。
signal focus_requested(target: Vector3, duration: float)

enum State { CLOSED, OPENED, EXPLODED }

const STEP := 0.12          # 每层级每单位系数的位移（米）
const STEP_L2 := 0.06       # L2 子树二次爆炸步距（米，depth_model §4）
const SLIDER_SPEED := 2.5   # 复原/展开插值速率（1/秒）
const MAX_DEPTH := 8        # 层级深度上限（防御）
const FOCUS_DURATION_MIN := 0.9  # 聚焦运镜时长下限（秒，depth_model §4 目标框缩放）
const FOCUS_DURATION_MAX := 1.2  # 聚焦运镜时长上限（秒）

var _loader: Node = null
var _state: int = State.CLOSED
var _value := 0.0
var _target_value := 0.0
var _depth := {}             # node -> depth
var _axis := {}              # node -> Vector3（推拉主轴，默认 +X）
var _base_transform := {}    # node -> Transform3D（闭合基准）
## F-6 深化（TASK-301-I）：子树聚焦 asmb_id（空=整机 L1 视图）与 L3 代表件 role 焦点。
var _subtree_focus := ""
var _rep_focus := ""
## TASK-306-G：子树局部基准形变记录（node -> Transform3D，enter_subtree 时记录）。
var _subtree_base := {}
## TASK-306-I：L3 代表件高亮集合（role 节点，只记录不位移）。
var _rep_highlight: Array = []
## TASK-306-J：面包屑状态数组（数据即可，UI 归 04 线；depth_model §4 逐级返回）。
var _breadcrumb: Array[String] = []

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
	_subtree_focus = ""
	_rep_focus = ""
	_subtree_base = {}
	_rep_highlight = []
	_breadcrumb = []
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
	var tf: Variant = entry.get("transform")
	var t: Array = []
	if tf is Dictionary:
		t = tf.get("translation", [0, 0, 0])
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
	# RUN-08 复测：进入拆解即演示展开，给可见反馈；滑杆可继续调（0..1）
	if _state == State.EXPLODED and not _base_transform.is_empty():
		_target_value = 0.35


func set_close() -> void:
	_set_state(State.CLOSED)  # 全树已按 _base_transform 复原（TASK-306-G：基准清空即可）
	_set_subtree_visibility(false)
	_subtree_base = {}
	_subtree_focus = ""
	_rep_focus = ""
	_rep_highlight = []
	_breadcrumb = []


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


## F-6 深化（TASK-301-I）：L2/L3 级联爆炸分档导出（depth_model.md L0-L3）。
## L2 = 子树级视图（EXPLODED 中点选某件 → 子树聚焦，depth_model §4「子树视图」）；
## L3 = 零件级视图（子树内点选带 role 节点 → 代表件高亮，不位移，depth_model §1 L3）。
## 续实装（TASK-306-G~K）：子树局部位移（explode_subtree/STEP_L2）、聚焦运镜
## （focus_node/focus_requested）、L3 代表件高亮（_rep_highlight）、面包屑
## （_breadcrumb）、子树 hide/show 批处理（_set_subtree_visibility）已静态落地；
## 相机插值本体与高亮材质表现仍标待实机。
func get_depth_level() -> int:
	match _state:
		State.EXPLODED:
			if _rep_focus != "":
				return 3   # L3 零件级视图（代表件高亮）
			if _subtree_focus != "":
				return 2   # L2 子树级视图（某件聚焦）
			return 1       # L1 大部件级（全树按深度爆炸）
		_:
			return 0       # L0 整机（CLOSED/OPENED 无展开形变）


## F-6 深化（TASK-301-I）：进入子树视图（L2）——EXPLODED 中点选 asmb_id 聚焦该件；
## 需该件在拓扑中（_depth 有记录）。返回是否成功。
## 续实装：TASK-306-G 记录子树局部基准形变；306-H 调 focus_node 发运镜信号；
## 306-J 面包屑 push 件名；306-K 隐藏非子树节点（深层性能回收）。
func enter_subtree(asmb_id: String) -> bool:
	if _state != State.EXPLODED or asmb_id.is_empty():
		return false
	var focus_target = null
	for node in _depth:
		if node.has_meta("asmb_id") and str(node.get_meta("asmb_id")) == asmb_id:
			focus_target = node
			break
	if focus_target == null:
		return false
	_subtree_focus = asmb_id
	_rep_focus = ""
	_subtree_base = {}
	for node in _subtree_nodes_of(asmb_id):
		_subtree_base[node] = node.transform
	_breadcrumb.append(asmb_id)
	_set_subtree_visibility(true)
	focus_node(focus_target)
	return true


## F-6 深化（TASK-301-I）：退出子树视图，回 L1（EXPLODED 全树爆炸）。
## 续实装：306-G 复原子树局部形变并清空基准；306-J 面包屑 pop 回 L1；
## 306-K 全部节点恢复 show。
func exit_subtree() -> void:
	for node in _subtree_base:
		node.transform = _subtree_base[node]
	_subtree_base = {}
	_subtree_focus = ""
	_rep_focus = ""
	_rep_highlight = []
	while not _breadcrumb.is_empty():
		_breadcrumb.pop_back()
	_set_subtree_visibility(false)


## F-6 深化（TASK-301-I）：子树内点选带 role 标注节点 → L3 代表件高亮（不位移）。
## role 标注来源 = annotations（03 线），缺失时按无 role 处理（待核实：L3 代表件
## 选择标准见 depth_model §7-3）。返回是否成功。
## 续实装：306-I 内联调 _apply_rep_highlight；306-J 面包屑 push 代表件 role。
func focus_rep(node: Node3D) -> bool:
	if _state != State.EXPLODED or _subtree_focus == "":
		return false
	if node == null or not node.has_meta("role"):
		return false
	_rep_focus = str(node.get_meta("role"))
	_breadcrumb.append(_rep_focus)
	_apply_rep_highlight()
	return true


## TASK-306-G：收集以 root_id 为根的子树节点（含根），复用 _depth 拓扑的 asmb parent 链。
func _subtree_nodes_of(root_id: String) -> Array:
	var id_to_node := {}
	for node in _depth:
		if node.has_meta("asmb_id"):
			id_to_node[str(node.get_meta("asmb_id"))] = node
	var out: Array = []
	for aid in id_to_node:
		var cur: String = aid
		var hops := 0
		while cur != "" and hops <= MAX_DEPTH:
			if cur == root_id:
				out.append(id_to_node[aid])
				break
			var parent_node: Node3D = id_to_node.get(cur)
			if parent_node == null:
				break
			var entry: Dictionary = parent_node.get_meta("asmb_entry", {})
			cur = str(entry.get("parent", ""))
			hops += 1
	return out


## TASK-306-G：L2 子树局部位移（depth_model §4/§6 #2）——对 _subtree_focus 子树沿局部
## 轴二次爆炸 offset = v × 相对深度 × STEP_L2；基准取 _subtree_base（enter_subtree 记录）。
func explode_subtree(v: float) -> void:
	if _state != State.EXPLODED or _subtree_focus == "" or _subtree_base.is_empty():
		return
	var root_depth := -1
	for node in _depth:
		if node.has_meta("asmb_id") and str(node.get_meta("asmb_id")) == _subtree_focus:
			root_depth = int(_depth[node])
			break
	if root_depth < 0:
		return
	for node in _subtree_base:
		var base: Transform3D = _subtree_base[node]
		var rel := int(_depth.get(node, 0)) - root_depth
		if rel < 0:
			rel = 0
		var axis: Vector3 = _axis.get(node, Vector3.RIGHT)
		var offset: float = v * float(rel) * STEP_L2
		node.transform = base
		node.translate_object_local(axis * offset)


## TASK-306-H：相机聚焦运镜（depth_model §4/§6 #3）——求 node 下 MeshInstance3D 全局
## AABB 的 {center, radius}，时长按半径在 0.9~1.2s 线性映射，emit focus_requested 并返回。
func focus_node(node: Node3D) -> Dictionary:
	if node == null:
		return {}
	var meshes: Array = []
	_collect_meshes(node, meshes)
	var aabb := AABB()
	var found := false
	for mesh_node in meshes:
		var mesh = mesh_node.mesh
		if mesh == null:
			continue
		var local: AABB = mesh.get_aabb()
		if local.size.length_squared() < 0.0001:
			continue
		var global_aabb: AABB = mesh_node.global_transform * local
		if not found:
			aabb = global_aabb
			found = true
		else:
			aabb = aabb.merge(global_aabb)
	if not found:
		return {}
	var center: Vector3 = aabb.get_center()
	var radius := aabb.get_longest_axis_size() * 0.5
	var duration := clampf(lerpf(FOCUS_DURATION_MIN, FOCUS_DURATION_MAX, radius / 2.0),
			FOCUS_DURATION_MIN, FOCUS_DURATION_MAX)
	var result := {"center": center, "radius": radius, "duration": duration}
	focus_requested.emit(center, duration)
	return result


## TASK-306-H：递归收集 root 下的 MeshInstance3D 节点（focus_node 用）。
func _collect_meshes(root: Node3D, out: Array) -> Array:
	if root is MeshInstance3D:
		out.append(root)
	for child in root.get_children():
		if child is Node3D:
			_collect_meshes(child, out)
	return out


## TASK-306-I：L3 代表件高亮集合渲染（depth_model §1/§6 #6）——收集 role == _rep_focus 的
## 节点入 _rep_highlight；只记录集合不位移，材质/自发光高亮表现标待实机。
func _apply_rep_highlight() -> void:
	_rep_highlight = []
	if _rep_focus == "":
		return
	for node in _depth:
		if node.has_meta("role") and str(node.get_meta("role")) == _rep_focus:
			_rep_highlight.append(node)


## TASK-306-J：面包屑数组（depth_model §4「整机 / 主板 / 扩展卡」逐级返回，数据即可）。
func get_breadcrumb() -> Array:
	return _breadcrumb.duplicate()


## TASK-306-K：深层性能回收（depth_model §5/§6 #8）——子树视图切换的 hide/show 批处理。
## visible=true 时仅保留 _subtree_focus 子树可见（非子树批量 hide）；false 时全部 show。
## 只做可见性批处理，不删节点、不改资产。
func _set_subtree_visibility(visible: bool) -> void:
	if visible and _subtree_focus == "":
		return
	var subtree_set := {}
	for node in _subtree_nodes_of(_subtree_focus):
		subtree_set[node] = true
	for node in _depth:
		if visible:
			if subtree_set.has(node):
				node.show()
			else:
				node.hide()
		else:
			node.show()


## 当前视图分档查询（L0-L3 语义同 get_depth_level；供 HUD/复盘显示）。
func current_view_level() -> int:
	return get_depth_level()


## §4 运行锁接入点：网关 status(state=running) → 置 true；stopped/degraded → false
func set_device_running(running: bool) -> void:
	if running != _device_running:
		_device_running = running
		if running and _state == State.EXPLODED:
			_set_state(State.OPENED)  # 运行中回车：先退出拆解
			_request_denied("设备已开机，已退出拆解")
