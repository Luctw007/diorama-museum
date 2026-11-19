# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Node3D
## 传送点枢纽（TASK-231-A · F-1 骨架；TASK-236-A/B · F-2 正式化 + 玩家过滤 + 点选接线）。
##
## 职责：
##   1. 读取枢纽布局 res://content/exhibit_hub.json（hall_group + portals，
##      三字段 schema 见 02 线 layout扩展规格_v1 L-11~L-13）；
##   2. 为每个 portal 生成白模灰盒门框（BoxMesh 1×2.4×0.2，unshaded 半透明）
##      + Area3D 碰撞体（BoxShape3D 同尺寸，226-A Hub 骨架口径）；
##   3. 碰撞触发（236-B 玩家过滤：仅 is_in_group("player") 的碰撞体触发）+ 准星点选
##      （236-A：屏幕空间最近门框拾取，inspect_controller 中心拾取同款口径）双路径
##      → ExhibitHost.switch_hall(目标布局)（复用 114 切厅清场重建）；
##   4. 反向 portal（236-A）：切厅后 refresh_portals 按当前厅布局 portals 重建门框，
##      子厅 → hub（target="hub" → exhibit_hub.json）双向可达；
##   5. hall_group 归属记录（L-12）：解析并暴露 current_group()，供 HallNavPanel
##      大厅总览按组归类（F-3 枢纽厅布局接入）。
##
## 静态说明：本文件按 Godot 4.x GDScript 编写，未实机运行；待实装验证清单见
##   docs/F1白模验证口径清单_v1.md 与 docs/TASK-236-A_完成报告.md §5。
## 依赖 API（exhibit_host.gd）：
##   - ExhibitHost.switch_hall(new_layout_file: String) -> bool（TASK-114 落地）
##   - ExhibitHost 切厅成功后回调本节点 refresh_portals(layout_file)

class_name PortalHub

const CONTENT_ROOT := "res://content"
## 枢纽布局文件名（236-A 正式化：exhibit_ 前缀 + devices 非空，进 layout_check --all）
const HUB_DEFINITION := "exhibit_hub.json"
## hall_group 标识 → 布局文件映射（227-A L-11：target 可为 hall_group 标识）
const GROUP_TO_LAYOUT := {"hub": HUB_DEFINITION}
## 门框白模尺寸（米）：宽 1 × 高 2.4 × 厚 0.2（226-A 提案口径）
const PORTAL_BOX_SIZE := Vector3(1.0, 2.4, 0.2)
## 准星点选半径（像素）：inspect_controller PICK_RADIUS_PX 同款口径
const PICK_RADIUS_PX := 18.0
## 玩家分组（236-B 过滤契约）：玩家碰撞体挂 is_in_group("player") 后生效
const PLAYER_GROUP := "player"

## 枢纽宿主：/root/Main/ExhibitHost（class_name 直接类型引用）
var _host: ExhibitHost
## 枢纽 hall_group 归属（L-12）：当前装载布局声明的值
var hall_group: String = ""
## 已生成传送点：target -> Area3D
var _portal_nodes: Dictionary = {}


func _ready() -> void:
	_host = get_node_or_null("/root/Main/ExhibitHost") as ExhibitHost
	if _host == null:
		push_warning("PortalHub: ExhibitHost 未找到，传送点不可用")
		return
	_load_portals_from(HUB_DEFINITION)


## 切厅后由 ExhibitHost.switch_hall 回调：清旧门框、按当前厅 portals 重建（反向 portal）。
func refresh_portals(layout_file: String) -> void:
	_clear_portals()
	_load_portals_from(layout_file)


## 清空已生成传送点（换厅时旧门框全部拆除；立即 remove_child 防同帧重建同名冲突）。
func _clear_portals() -> void:
	for target in _portal_nodes:
		var node: Node = _portal_nodes[target]
		if is_instance_valid(node) and node.get_parent() == self:
			remove_child(node)
			node.queue_free()
	_portal_nodes.clear()


## 读取布局文件的 hall_group（若有）+ portals，并生成门框。
func _load_portals_from(layout_file: String) -> void:
	var f := FileAccess.open(CONTENT_ROOT + "/" + layout_file, FileAccess.READ)
	if f == null:
		push_warning("PortalHub: 布局缺失 %s/%s" % [CONTENT_ROOT, layout_file])
		return
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("PortalHub: 布局 JSON 不是对象: %s" % layout_file)
		return
	var definition: Dictionary = parsed
	if definition.has("hall_group"):
		hall_group = str(definition.get("hall_group", ""))
		if hall_group != "hub":
			push_warning("PortalHub: hall_group=%s 非 hub（L-12 取值域外）" % hall_group)
	var raw: Array = definition.get("portals", []) if typeof(definition.get("portals", [])) == TYPE_ARRAY else []
	for i in raw.size():
		var entry: Variant = raw[i]
		if not (entry is Dictionary):
			push_warning("PortalHub: portals[%d] 不是对象，跳过" % i)
			continue
		var portal_def: Dictionary = entry
		var target: String = str(portal_def.get("target", ""))
		if target.is_empty():
			push_warning("PortalHub: portals[%d] 缺 target，跳过" % i)
			continue
		_spawn_portal(target, portal_def)


## 生成单个传送点：Area3D 碰撞触发 + 白模灰盒门框。
func _spawn_portal(target: String, portal_def: Dictionary) -> void:
	var portal := Area3D.new()
	portal.name = "Portal_%s" % target
	portal.set_meta("portal_target", target)
	add_child(portal)
	var pos: Array = portal_def.get("position", []) if typeof(portal_def.get("position", [])) == TYPE_ARRAY else []
	if pos.size() >= 3:
		portal.position = Vector3(float(pos[0]), float(pos[1]), float(pos[2]))
	else:
		push_warning("PortalHub: portal %s 缺合法 position，落原点" % target)
	if portal_def.has("rotation"):
		var rot: Array = portal_def["rotation"]
		if rot is Array and rot.size() >= 4:
			# [x,y,z,w] 四元数（227-A L-11 口径；朝向角写法待实装验证）
			portal.quaternion = Quaternion(float(rot[0]), float(rot[1]),
					float(rot[2]), float(rot[3]))
	var shape := CollisionShape3D.new()
	var box_shape := BoxShape3D.new()
	box_shape.size = PORTAL_BOX_SIZE
	shape.shape = box_shape
	portal.add_child(shape)
	var gate := MeshInstance3D.new()
	var gate_mesh := BoxMesh.new()
	gate_mesh.size = PORTAL_BOX_SIZE
	var mat := StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color = Color(0.85, 0.9, 1.0, 0.35)
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	gate_mesh.material = mat
	gate.mesh = gate_mesh
	portal.add_child(gate)
	portal.body_entered.connect(_on_portal_entered.bind(target))
	_portal_nodes[target] = portal


## 碰撞触发（236-B 玩家过滤）：仅玩家碰撞体触发切厅，非玩家碰撞体忽略。
## 前置（待用户实机）：player.gd 当前为无碰撞自由相机（M0 设计），需挂碰撞体并
## add_to_group("player") 后本路径才可达；未实机前点选路径为主（236-A）。
func _on_portal_entered(body: Node3D, target: String) -> void:
	if not body.is_in_group(PLAYER_GROUP):
		push_warning("PortalHub: 非玩家碰撞体 %s 进入 portal，忽略" % body.name)
		return
	activate_portal(target)


## 准星点选（236-A）：鼠标可见时按真实点击位置、捕获时按屏幕中心（inspect_controller
## RUN-08 同款口径），拾取 18px 内最近门框并传送。
func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton):
		return
	if event.button_index != MOUSE_BUTTON_LEFT or not event.pressed:
		return
	var pick_pos: Vector2 = event.position \
			if Input.mouse_mode == Input.MOUSE_MODE_VISIBLE \
			else get_viewport().get_visible_rect().size * 0.5
	var target: String = _pick_portal(pick_pos)
	if target != "":
		get_viewport().set_input_as_handled()
		activate_portal(target)


## 屏幕空间最近门框拾取（inspect_controller._update_hover 同款：投影 + 半径 + 近者优先）。
func _pick_portal(screen_pos: Vector2) -> String:
	var camera := get_viewport().get_camera_3d()
	if camera == null or _portal_nodes.is_empty():
		return ""
	var best := ""
	var best_dist := PICK_RADIUS_PX
	var best_cam_z := INF
	for target in _portal_nodes:
		var portal: Node3D = _portal_nodes[target]
		if not is_instance_valid(portal):
			continue
		var center: Vector3 = portal.global_position
		if camera.is_position_behind(center):
			continue
		var projected := camera.unproject_position(center)
		var d := screen_pos.distance_to(projected)
		var camz := camera.global_position.distance_to(center)
		if d <= best_dist and camz < best_cam_z:
			best_dist = d
			best_cam_z = camz
			best = str(target)
	return best


## 传送执行：target 可为布局文件名（不含 .json）或 hall_group 标识（"hub"，227-A L-11）。
## 复用 ExhibitHost.switch_hall（清场重建/配额与调试圈保留，114 落地）。
func activate_portal(target: String) -> bool:
	if _host == null:
		push_warning("PortalHub: ExhibitHost 未找到，传送失败 %s" % target)
		return false
	var layout_file: String = _resolve_layout_file(target)
	var ok: bool = _host.switch_hall(layout_file)
	if not ok:
		push_warning("PortalHub: 传送失败 %s（目标布局不可装载）" % layout_file)
	return ok


## hall_group 标识 → 布局文件；其余按「文件名不含 .json」拼接。
func _resolve_layout_file(target: String) -> String:
	if GROUP_TO_LAYOUT.has(target):
		return str(GROUP_TO_LAYOUT[target])
	return target + ".json"


## hall_group 归属查询（L-12）：供 HallNavPanel 大厅总览按组归类。
func current_group() -> String:
	return hall_group


## 已生成传送点目标清单（供 HUD/调试）。
func portal_targets() -> Array:
	return _portal_nodes.keys()
