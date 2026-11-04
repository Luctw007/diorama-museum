# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
class_name DeviceLoader
extends Node3D
## 设备内容包多设备加载器 v2（TASK-11A）：内容包 → Godot 节点树。
##
## 约定：
## - 内容根目录：res://content/<device-id>/（当前装载 4 包：test-device / manchester-baby /
##   eniac / apple-ii，来源与自检表见 content/README.md）；
## - 包结构（内容线 v0.1 实际格式，已与 02 线规范对照）：
##   meta.json = { meta, assemblies[], components[], runtime? }；
##   assemblies[].transform 为对象 {translation:[x,y,z], rotation:[x,y,z,w], scale:[x,y,z]}
##   （兼容旧扁平数组 [x,y,z,qx,qy,qz,qw]），role 文案内联在 assembly.role；
##   components[] 经 .assembly 挂在对应装配体下；runtime.json 可独立存在。
##
## 降级表（degradation）：
##   meta 缺失/非法    → 设备不可加载（index 中 loadable=false）
##   mesh_ref 缺失或    → 占位盒 MeshInstance3D + push_warning（M1 阶段正式资产未到）
##   glTF 未导入
##   annotations 缺失  → 软跳过（role 以内联 assembly.role 为主）
##
## 自检清单（信号/方法）：
## - signal device_index_ready(index: Array)    index 条目:{id,name,name_en,category,
##                                              precision_level,loadable,warnings[]}
## - signal device_loaded(device_id: String)
## - func scan_index() -> Array                 枚举 res://content
## - func load_device(device_id: String) -> bool
## - func get_node_role(node: Node3D) -> String 内联 role（备用 annotations）
## - func get_device_meta() / get_runtime() / get_assembly_nodes()
## - 不硬编码任何具体设备 id / 字段名（字段按规范读取）。

signal device_index_ready(index: Array)
signal device_loaded(device_id: String)

const CONTENT_ROOT := "res://content"
const PLACEHOLDER_COLOR := Color(0.55, 0.5, 0.42)

var _index: Array = []
var _meta := {}
var _runtime := {}
var _annotations := {}
var _assembly_nodes := {}      # assembly_id -> Node3D
var _role_by_node := {}        # Node3D -> role 文案
var _current_device := ""


func _ready() -> void:
	scan_index()
	# 默认装载第一台可加载设备（空厅时留空，由 DevicePicker 选择）
	var first := ""
	for entry in _index:
		if entry.get("loadable", false):
			first = str(entry.get("id", ""))
			break
	if first != "":
		load_device(first)


# ---------------------------------------------------------------- 索引
func scan_index() -> Array:
	_index = []
	var dir := DirAccess.open(CONTENT_ROOT)
	if dir == null:
		push_warning("[DeviceLoader] 无法打开 %s" % CONTENT_ROOT)
		device_index_ready.emit(_index)
		return _index
	dir.list_dir_begin()
	var entry_name := dir.get_next()
	while entry_name != "":
		if not dir.current_is_dir() or entry_name.begins_with("."):
			entry_name = dir.get_next()
			continue
		var pkg_dir := CONTENT_ROOT + "/" + entry_name
		var meta_path := pkg_dir + "/meta.json"
		var warnings: Array = []
		var meta: Dictionary = {}
		if not FileAccess.file_exists(meta_path):
			warnings.append("缺 meta.json")
		else:
			var parsed = _parse_json_file(meta_path)
			if typeof(parsed) == TYPE_DICTIONARY and typeof(parsed.get("meta", {})) == TYPE_DICTIONARY:
				meta = parsed
			else:
				warnings.append("meta.json 非法")
		if meta.is_empty():
			_index.append({"id": entry_name, "name": entry_name, "loadable": false,
						   "warnings": warnings})
		else:
			var top: Dictionary = meta.get("meta", {})
			_index.append({
				"id": str(top.get("id", entry_name)),
				"name": str(top.get("name", entry_name)),
				"name_en": str(top.get("name_en", "")),
				"category": str(top.get("category", "")),
				"precision_level": str(top.get("precision_level", "L2")),
				"loadable": warnings.is_empty(),
				"warnings": warnings,
			})
		entry_name = dir.get_next()
	dir.list_dir_end()
	_index.sort_custom(func(a, b): return str(a.get("id", "")) < str(b.get("id", "")))
	device_index_ready.emit(_index)
	return _index


# ---------------------------------------------------------------- 装载
func load_device(device_id: String) -> bool:
	_clear_tree()
	_current_device = device_id
	var pkg_root := CONTENT_ROOT + "/" + device_id
	var meta: Variant = _parse_json_file(pkg_root + "/meta.json")
	if typeof(meta) != TYPE_DICTIONARY or typeof(meta.get("assemblies", [])) != TYPE_ARRAY:
		push_warning("[DeviceLoader] 设备 %s 无法装载（meta 缺失/非法）" % device_id)
		device_loaded.emit(device_id)
		return false
	_meta = meta
	_runtime = _parse_json_file(pkg_root + "/runtime.json")
	if typeof(_runtime) != TYPE_DICTIONARY and typeof(meta.get("runtime")) == TYPE_DICTIONARY:
		_runtime = meta.get("runtime")
	_annotations = _parse_json_file(pkg_root + "/annotations/annotations.json")
	if typeof(_annotations) != TYPE_DICTIONARY:
		_annotations = {}

	# 第一遍：建装配体节点（先全部挂到自身树下，再按 parent 重排）
	var kindom: Dictionary = {}  # assembly id -> {node, entry}
	for assembly in meta.get("assemblies", []):
		if typeof(assembly) != TYPE_DICTIONARY:
			continue
		var aid := str(assembly.get("id", ""))
		if aid == "":
			continue
		var node := Node3D.new()
		node.name = aid
		node.set_meta("asmb_id", aid)
		node.set_meta("asmb_entry", assembly)
		kindom[aid] = {"node": node, "entry": assembly}
	# 第二遍：按 parent/children 建立层级
	for aid in kindom:
		var entry: Dictionary = kindom[aid]["entry"]
		var node: Node3D = kindom[aid]["node"]
		_apply_transform(node, entry.get("transform"))
		var children: Array = entry.get("children", [])
		var parent_id := str(entry.get("parent", ""))
		if parent_id == "" or not kindom.has(parent_id):
			add_child(node)  # 根装配体
		else:
			kindom[parent_id]["node"].add_child(node)
		var role := str(entry.get("role", ""))
		if role != "":
			_role_by_node[node] = role
		# 网格
		var mesh_ref := str(entry.get("mesh_ref", ""))
		if mesh_ref != "":
			_attach_mesh(node, pkg_root, mesh_ref)
	# 第三遍：components 挂到所属装配体
	for component in meta.get("components", []):
		if typeof(component) != TYPE_DICTIONARY:
			continue
		var asmb := str(component.get("assembly", ""))
		if not kindom.has(asmb):
			continue
		var cnode := Node3D.new()
		cnode.name = str(component.get("id", "component"))
		cnode.set_meta("component_entry", component)
		var role := str(component.get("role", ""))
		if role != "":
			_role_by_node[cnode] = role
		kindom[asmb]["node"].add_child(cnode)
	_assembly_nodes = {}
	for aid in kindom:
		_assembly_nodes[aid] = kindom[aid]["node"]
	device_loaded.emit(device_id)
	return true


func _clear_tree() -> void:
	for child in get_children():
		child.queue_free()
	_meta = {}
	_runtime = {}
	_annotations = {}
	_assembly_nodes = {}
	_role_by_node = {}


func _apply_transform(node: Node3D, t) -> void:
	# v0.1 实际格式：{translation:[x,y,z], rotation:[x,y,z,w], scale:[x,y,z]}
	# 兼容：扁平数组 [x,y,z,qx,qy,qz,qw]
	if typeof(t) == TYPE_DICTIONARY:
		var tl: Array = t.get("translation", [0.0, 0.0, 0.0])
		var rt: Array = t.get("rotation", [0.0, 0.0, 0.0, 1.0])
		var sc: Array = t.get("scale", [1.0, 1.0, 1.0])
		node.transform = Transform3D(
			Quaternion(float(rt[3]), float(rt[0]), float(rt[1]), float(rt[2])),
			Vector3(float(tl[0]), float(tl[1]), float(tl[2])))
		var s := Vector3(float(sc[0]), float(sc[1]), float(sc[2]))
		if s != Vector3.ONE:
			node.scale = s
	elif typeof(t) == TYPE_ARRAY and t.size() >= 7:
		node.transform = Transform3D(
			Quaternion(float(t[3]), float(t[4]), float(t[5]), float(t[6])),
			Vector3(float(t[0]), float(t[1]), float(t[2])))


func _attach_mesh(owner_node: Node3D, pkg_root: String, mesh_ref: String) -> void:
	var mi := MeshInstance3D.new()
	mi.name = "mesh"
	var scene_path := pkg_root + "/" + mesh_ref
	if ResourceLoader.exists(scene_path):
		var scene := ResourceLoader.load(scene_path) as PackedScene
		if scene != null:
			var inst := scene.instantiate()
			if inst is Node3D:
				mi.add_child(inst)
				owner_node.add_child(mi)
				return
	push_warning("[DeviceLoader] 网格降级为占位盒: %s" % scene_path)
	_attach_placeholder_box(owner_node)


func _attach_placeholder_box(owner_node: Node3D) -> void:
	var mi := MeshInstance3D.new()
	mi.name = "mesh"
	var box := BoxMesh.new()
	box.size = Vector3(0.3, 0.2, 0.2)
	mi.mesh = box
	var mat := StandardMaterial3D.new()
	mat.albedo_color = PLACEHOLDER_COLOR
	mi.material_override = mat
	owner_node.add_child(mi)


# ---------------------------------------------------------------- 查询
func _parse_json_file(path: String) -> Variant:
	if not FileAccess.file_exists(path):
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return {}
	return JSON.parse_string(f.get_as_text())


func get_device_index() -> Array:
	return _index


func get_current_device() -> String:
	return _current_device


func get_node_role(node: Node3D) -> String:
	return _role_by_node.get(node, "")


func get_device_meta() -> Dictionary:
	return _meta


func get_runtime() -> Dictionary:
	return _runtime


func get_assembly_nodes() -> Dictionary:
	return _assembly_nodes
