# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
class_name ExhibitIndex
extends RefCounted
## 图鉴静态索引工具类（TASK-36B，静态交付）。
##
## 数据源：res://content/exhibit_index.json（由 scripts/gen_exhibit_index.py 生成）。
## JSON 结构：{"generated": str, "halls":[{"hall": str,
##   "devices":[{"id","name","era","category","emulator","demo_mode",
##               "annotation_count","meshes"}]}]}
##
## 给 HUD/DevicePicker 的接口契约（与 04 线 02 号 UI 信息架构对齐）：
## - get_halls() -> Array[Dictionary]          厅列表（含 devices 冗余，便于一次渲染）
## - get_hall_names() -> PackedStringArray     厅名平铺
## - get_devices(hall: String) -> Array        某厅设备数组
## - get_device(device_id: String) -> Dictionary 单机条目（含厅名回填 hall）
## - hall_of(device_id: String) -> String      反查所在厅


const INDEX_PATH := "res://content/exhibit_index.json"

var _data: Dictionary = {}
var _valid := false


## 加载索引（可重复调用；失败置 _valid=false）。
func load_index() -> bool:
	var f := FileAccess.open(INDEX_PATH, FileAccess.READ)
	if f == null:
		_valid = false
		return false
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	_valid = typeof(parsed) == TYPE_DICTIONARY
	if _valid:
		_data = parsed
	return _valid


func is_valid() -> bool:
	return _valid


func get_halls() -> Array:
	if not _valid:
		return []
	return _data.get("halls", [])


func get_hall_names() -> PackedStringArray:
	var names := PackedStringArray()
	for hall in get_halls():
		names.append(str(hall.get("hall", "")))
	return names


func get_devices(hall_name: String) -> Array:
	for hall in get_halls():
		if str(hall.get("hall", "")) == hall_name:
			return hall.get("devices", [])
	return []


func get_device(device_id: String) -> Dictionary:
	for hall in get_halls():
		for dev in hall.get("devices", []):
			if str(dev.get("id", "")) == device_id:
				var out: Dictionary = dev.duplicate()
				out["hall"] = hall.get("hall", "")
				return out
	return {}


func hall_of(device_id: String) -> String:
	return str(get_device(device_id).get("hall", ""))


## 图鉴 HUD 常用汇总（顶部条）：设备总数/可运行数（非 demo_mode）。
func get_summary() -> Dictionary:
	var total := 0
	var runnable := 0
	for hall in get_halls():
		for dev in hall.get("devices", []):
			total += 1
			if not bool(dev.get("demo_mode", true)):
				runnable += 1
	return {"total": total, "runnable": runnable,
			"generated": _data.get("generated", "")}


## 分页访问器（TASK-176-B）：全馆设备平铺后按 name 稳定排序（不区分大小写，
## 同 catalog_data.sort_shard_rows 语义）切片，供 60+ 台图鉴画廊分批渲染。
## 返回 {"page":…, "page_size":…, "total":…, "items":[…]}
## （命名避开 get_index/get_meta/get_name 等 Object/Node 原生方法名）。
func get_paged_devices(page: int, page_size: int) -> Dictionary:
	var flat: Array = []
	for hall in get_halls():
		for dev in hall.get("devices", []):
			flat.append(dev)
	flat.sort_custom(func(a, b) -> bool:
		var an: String = str(a.get("name", "")).to_lower()
		var bn: String = str(b.get("name", "")).to_lower()
		return an < bn)
	var total: int = flat.size()
	var size: int = maxi(page_size, 1)
	var start: int = page * size
	var items: Array = []
	if start < total:
		items = flat.slice(start, mini(start + size, total))
	return {"page": page, "page_size": size, "total": total, "items": items}