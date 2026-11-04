# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Node3D
## 展厅宿主（TASK-21B）：按展陈布局 JSON 放置多台设备，管理运行配额与围观圈。
## 制式：Godot 4.x GDScript（静态交付，实机核对见 godot/content/README.md 待验证清单 #5）。
##
## 职责：
##   1. 读取布局文件（res://content/<layout>.json，schema 见 docs/exhibit_layout_spec.md L1）；
##   2. 为每台设备实例化一个 DeviceLoader（scripts/device_loader.gd），惰性加载设备包；
##   3. 运行配额：全厅同时只允许 max_running=1 台设备接模拟器运行（资源预算，见 exhibit_layout_spec §3）；
##   4. 围观圈：每台设备维护 audience_radius，导览触发（04 线 16 号导览台本）据此判定玩家进入互动作业区。
##
## 静态说明：本文件按 Godot 4.x GDScript 编写，未实机运行；实机核对清单见
##   godot/content/README.md "待验证清单（引擎侧）" 节，或 docs/TASK-21B_完成报告.md §4。
## 依赖 API（device_loader.gd v2）：
##   - DeviceLoader.load_device(device_id: String) -> bool
##   - DeviceLoader.get_index() -> Array          # {id, name, category...}
##   - DeviceLoader.get_meta() / get_runtime() / get_assembly_nodes()

class_name ExhibitHost

const CONTENT_ROOT := "res://content"
const DEVICE_LOADER := preload("res://scripts/device_loader.gd")
const DEFAULT_LAYOUT := "exhibit_dawn.json"

## 布局 JSON 顶层字段（与 docs/exhibit_layout_spec.md L1 一致）
const LAYOUT_HALL_NAME := "hall_name"
const LAYOUT_DEVICES := "devices"

## 设备条目字段
const DEV_FIELDS_POSITION := "position"   # Vector3（米；=Vector3(0,0,yaw) 含义见 spec §4）
const DEV_FIELDS_ROTATION := "rotation"   # 四元数 [x,y,z,w]，可选
const DEV_FIELDS_SCALE := "scale"         # 米制缩放，可选
const DEV_FIELDS_SLOT := "slot"           # 导览参观序号，可选

## 运行配额：全厅同时运行设备上限（模拟器进程数预算）
@export_range(1, 4) var max_running: int = 1

## 布局文件名（相对 res://content）
@export var layout_file: String = DEFAULT_LAYOUT

## 本宿主可切换的厅布局清单（TASK-41B；与 godot/content/exhibit_*.json 对应）
@export var hall_files: PackedStringArray = PackedStringArray([
	"exhibit_dawn.json",
	"exhibit_mainframe.json",
	"exhibit_personal.json",
	"exhibit_console.json",
])

## 观众围观半径（米）——玩家进入该半径才触发 Inspect/导览特效
@export var audience_radius: float = 2.2

## 是否在 _ready 自动载入布局
@export var auto_spawn: bool = true

## 布局解析结果缓存
var _layout: Dictionary = {}
var _load_error: String = ""
## 已放置设备：device_id -> {loader: DeviceLoader, entry: Dictionary}
var _placed: Dictionary = {}
## 当前运行设备（配额内）
var _running_id: String = ""


func _ready() -> void:
	if auto_spawn:
		var ok := load_layout(layout_file)
		if not ok:
			push_warning("ExhibitHost: 布局加载失败 -> %s" % _load_error)
			return
		spawn_devices()
		if OS.is_debug_build():
			# 调试构建自动显示观众围观圈，便于验证 find_audience 半径与导览站位
			toggle_debug_circles(true)


## 载入并校验布局文件；成功返回 true。
func load_layout(path: String) -> bool:
	_layout = {}
	_load_error = ""
	var res := FileAccess.open("%s/%s" % [CONTENT_ROOT, path], FileAccess.READ)
	if res == null:
		_load_error = "布局文件无法打开: %s/%s" % [CONTENT_ROOT, path]
		return false
	var parsed: Variant = JSON.parse_string(res.get_as_text())
	res.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		_load_error = "布局 JSON 不是对象"
		return false
	_layout = parsed
	if not _layout.has(LAYOUT_HALL_NAME) or not _layout.has(LAYOUT_DEVICES):
		_load_error = "缺少 hall_name 或 devices 字段"
		return false
	return true


## 按布局放置全部设备（未加载成功则不动作）。返回成功数量。
func spawn_devices() -> int:
	var entries: Array = _layout.get(LAYOUT_DEVICES, [])
	var placed := 0
	for entry in entries:
		if not (entry is Dictionary):
			continue
		var did: String = str(entry.get("id", ""))
		if did.is_empty():
			push_warning("ExhibitHost: 设备条目缺 id，跳过")
			continue
		if _placed.has(did):
			push_warning("ExhibitHost: 设备重复放置 %s，跳过" % did)
			continue
		var loader: DeviceLoader = DEVICE_LOADER.new()
		loader.name = "Device_%s" % did
		add_child(loader)
		if not loader.load_device(did):
			push_warning("ExhibitHost: 设备包加载失败 %s（占位盒降级）" % did)
		_apply_entry_transform(loader, entry)
		_placed[did] = {"loader": loader, "entry": entry}
		placed += 1
	return placed


## 解释条目 transform 字段并应用（position/rotation/scale 三选一可有）。
func _apply_entry_transform(loader: Node3D, entry: Dictionary) -> void:
	if entry.has(DEV_FIELDS_POSITION):
		var pos: Array = entry[DEV_FIELDS_POSITION]
		if pos is Array and pos.size() >= 3:
			loader.position = Vector3(float(pos[0]), float(pos[1]), float(pos[2]))
	if entry.has(DEV_FIELDS_ROTATION):
		var rot: Array = entry[DEV_FIELDS_ROTATION]
		if rot is Array and rot.size() >= 4:
			# [x,y,z,w] 四元数 → 引擎增广；布局通常只给绕 Y 的朝向时由 position[3] 兜底
			loader.quaternion = Quaternion(float(rot[0]), float(rot[1]),
					float(rot[2]), float(rot[3]))
	elif entry.has(DEV_FIELDS_POSITION) and entry[DEV_FIELDS_POSITION].size() >= 4:
		# 兼容：position 第 4 元为绕 Y 朝向角（度）——04 线 03 号文档俯视网格的 yaw 约定
		var yaw: float = float(entry[DEV_FIELDS_POSITION][3])
		loader.rotation.y = deg_to_rad(yaw)
	if entry.has(DEV_FIELDS_SCALE):
		var scl: Array = entry[DEV_FIELDS_SCALE]
		if scl is Array and scl.size() >= 3:
			loader.scale = Vector3(float(scl[0]), float(scl[1]), float(scl[2]))


## 领取"运行许可证"：配额内把 device_id 设为运行中；超配额返回 false。
## 运行中设备由 01 线网关客户端（gateway_client.gd）负责"上电→画面投放→关机"三阶段调用。
func acquire_run(device_id: String) -> bool:
	if not _placed.has(device_id):
		push_warning("ExhibitHost: 未放置的设备申请运行 %s" % device_id)
		return false
	if _running_id != "" and _running_id != device_id:
		push_warning("ExhibitHost: 运行配额已满（当前 %s），拒绝 %s"
				% [_running_id, device_id])
		return false
	_running_id = device_id
	return true


func release_run(device_id: String) -> void:
	if _running_id == device_id:
		_running_id = ""


## 玩家位置是否进入某台设备的围观圈。
func find_audience(player_pos: Vector3) -> String:
	var best := ""
	var best_d := audience_radius
	for did in _placed:
		var loader: Node3D = _placed[did]["loader"]
		var d: float = player_pos.distance_to(loader.global_position)
		if d <= best_d:
			best_d = d
			best = str(did)
	return best


## 查询：按参观序号返回设备清单（供导览 HUD/图鉴）。
func get_tour_order() -> Array:
	var order: Array = []
	for did in _placed:
		order.append({"id": did, "slot": int(_placed[did]["entry"].get(DEV_FIELDS_SLOT, 0))})
	order.sort_custom(func(a, b): return int(a["slot"]) < int(b["slot"]))
	return order


## 查询：布局摘要（HUD 顶栏用）。
func get_layout_summary() -> Dictionary:
	return {
		"hall_name": _layout.get(LAYOUT_HALL_NAME, ""),
		"placed": _placed.size(),
		"running": _running_id,
		"max_running": max_running,
	}


## 切换展厅（TASK-41B）：拆除当前全部设备 → 载入并放置新厅布局。
## 保留运行配额与调试圈设置；成功返回 true；布局路径非法返回 false。
func switch_hall(new_layout_file: String) -> bool:
	clear_devices()
	layout_file = new_layout_file
	var ok := load_layout(layout_file)
	if not ok:
		push_warning("ExhibitHost: 切厅失败 -> %s" % _load_error)
		return false
	return spawn_devices() > 0


## 拆除全部设备（清空场景；换厅时调用）。
func clear_devices() -> void:
	for did in _placed:
		var loader: Node3D = _placed[did]["loader"]
		if is_instance_valid(loader) and loader.get_parent() == self:
			remove_child(loader)
			loader.queue_free()
	_placed.clear()
	_running_id = ""
	_layout = {}


# ============================================================ 导览衔接（04 线 16 号）
## 导览推进：跳到第 step 站（slot 序号），高亮该设备、清空运行配额。
## 返回本步设备 id（无此站返回空串）。导览 HUD 据此挂接讲解/音效触发。
func sync_to_tour_step(step: int) -> String:
	for did in _placed:
		var slot: int = int(_placed[did]["entry"].get(DEV_FIELDS_SLOT, -1))
		if slot == step:
			clear_highlights()
			set_device_highlight(did, true)
			return str(did)
	return ""


## 本厅参观总站数（= 设备台数）。
func tour_step_count() -> int:
	return _placed.size()


# ============================================================ 高亮与调试
## 指定设备的高亮标记：廉价做法是给加载器挂一个半透明线框盒；
## 正式资产到达后替换为"导览光柱"粒子。返回是否成功。
func set_device_highlight(device_id: String, on: bool) -> bool:
	if not _placed.has(device_id):
		return false
	var loader: Node3D = _placed[device_id]["loader"]
	var marker: Node3D = loader.get_node_or_null("TourHighlight")
	if on:
		if marker == null:
			marker = _make_highlight_box()
			marker.name = "TourHighlight"
			loader.add_child(marker)
		marker.visible = true
	elif marker != null:
		marker.visible = false
	return true


## 清除所有高亮。
func clear_highlights() -> void:
	for did in _placed:
		set_device_highlight(str(did), false)


## 调试观围圈：每台设备脚下画一个 audience_radius 的圆环（半透明），
## 视角调试用；release 默认关闭（_ready 检查 OS.is_debug_build）。
func toggle_debug_circles(on: bool) -> void:
	for did in _placed:
		var loader: Node3D = _placed[did]["loader"]
		var ring: Node3D = loader.get_node_or_null("AudienceRing")
		if on and ring == null:
			ring = _make_ring_mesh(audience_radius)
			ring.name = "AudienceRing"
			loader.add_child(ring)
		if ring != null:
			ring.visible = on


## 生成高亮线框盒（几何 2×2×1.5 米，与占位盒比例近似的通用尺寸）。
func _make_highlight_box() -> Node3D:
	var box := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = Vector3(2.0, 2.0, 1.5)
	var mat := StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color = Color(1.0, 0.85, 0.3, 0.25)
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mesh.material = mat
	box.mesh = mesh
	return box


## 生成调试圆环（细分 64 段；比 BoxMesh 更直观读距离）。
func _make_ring_mesh(radius: float) -> Node3D:
	var ring := MeshInstance3D.new()
	var points := PackedVector3Array()
	var count := 64
	for i in count:
		var a := TAU * float(i) / float(count)
		points.append(Vector3(cos(a) * radius, 0.02, sin(a) * radius))
	var im := ImmediateMesh.new()
	im.surface_begin(Mesh.PRIMITIVE_LINE_STRIP)
	for p in points:
		im.surface_add_vertex(p)
	im.surface_add_vertex(points[0])
	im.surface_end()
	ring.mesh = im
	return ring


## 设备查询：did -> loader。供网关画面投放（gateway_client.gd）取内屏节点。
func get_device(device_id: String) -> Node3D:
	if _placed.has(device_id):
		return _placed[device_id]["loader"]
	return null


## 帧率保护：同厅设备全部占位盒，场景开销可忽略；正式建模后按
## get_layout_summary().placed 数量在 _process 节流高亮计算（预留接口）。
func refresh_budget_hint() -> int:
	return maxi(1, _placed.size() * 2)   # 每台预留 2 个流程位（讲解+演示），供 HUD 显示