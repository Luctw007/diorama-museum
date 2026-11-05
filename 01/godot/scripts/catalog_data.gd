# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
class_name CatalogData
extends RefCounted
## 图鉴目录数据层（TASK-56A，静态交付；与 04 线 31 号 API 提案对齐）。
##
## 数据源：res://content/catalog/meta.json（分类树+分片清单）
##         res://content/catalog/data/<大分类>__<中分类>.json（分片数组，按需加载）
##
## 契约（31 号 AP-01~AP-04）：
## - get_taxonomy() -> Dictionary            大→中→[子分类] 树
## - load_shard(big: String, mid: String) -> Array   分片条目数组（内部键 name/year/…+
##   _taxonomy）；已加载分片缓存，重复调用零 IO
## - search(keyword: String) -> Array        名称/别名内存索引命中（需先 build_index）
## - build_index() / get_summary() -> Dictionary


const META_PATH := "res://content/catalog/meta.json"
const DATA_TEMPLATE := "res://content/catalog/data/%s__%s.json"

var _meta: Dictionary = {}
var _valid := false
var _shard_cache: Dictionary = {}      # "big__mid" -> Array
var _name_index: Dictionary = {}       # 小写关键词 -> Array(entries)
var _summary := {"total_rows": 0, "loaded_shards": 0}
# TASK-117：缓存命中统计与查询计时（累积微秒；命名避开 get_meta/get_index 等原生冲突）
var _cache_hits := 0
var _cache_misses := 0
var _query_us := 0


func load_meta() -> bool:
	var f := FileAccess.open(META_PATH, FileAccess.READ)
	if f == null:
		_valid = false
		return false
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	_valid = typeof(parsed) == TYPE_DICTIONARY
	if _valid:
		_meta = parsed
		_summary["total_rows"] = int(_meta.get("total_rows", 0))
	return _valid


func is_valid() -> bool:
	return _valid


func get_taxonomy() -> Dictionary:
	if not _valid:
		return {}
	return _meta.get("taxonomy", {})


func get_shards() -> Array:
	if not _valid:
		return []
	return _meta.get("shards", [])


## 加载某中分类分片（缓存命中零 IO）。返回条目数组。
## TASK-117：命中/未命中计数与耗时（Time.get_ticks_usec 计量，暴露在 get_summary）。
func load_shard(big: String, mid: String) -> Array:
	if not _valid:
		return []
	var key := "%s__%s" % [big, mid]
	var t0 := Time.get_ticks_usec()
	if _shard_cache.has(key):
		_cache_hits += 1
		_query_us += Time.get_ticks_usec() - t0
		return _shard_cache[key]
	_cache_misses += 1
	var f := FileAccess.open(DATA_TEMPLATE % [big, mid], FileAccess.READ)
	if f == null:
		_query_us += Time.get_ticks_usec() - t0
		return []
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	var rows: Array = parsed if typeof(parsed) == TYPE_ARRAY else []
	_shard_cache[key] = rows
	_summary["loaded_shards"] = _shard_cache.size()
	_query_us += Time.get_ticks_usec() - t0
	return rows


## 构建全库名称/别名内存索引（图鉴搜索框用；800 行量级即刻，万级后接引擎侧并发索引）。
func build_index() -> int:
	_name_index.clear()
	for shard in get_shards():
		for row in load_shard(str(shard.get("big", "")), str(shard.get("mid", ""))):
			for key in [row.get("name", "")] + (row.get("aliases", []) as Array):
				if key:
					var norm := str(key).strip_edges().to_lower()
					if not _name_index.has(norm):
						_name_index[norm] = []
					_name_index[norm].append(row)
	return _name_index.size()


## 关键词搜索（先 build_index；精确小写匹配名/别名，简版——模糊匹配待引擎实装）。
func search(keyword: String) -> Array:
	var t0 := Time.get_ticks_usec()
	var norm := keyword.strip_edges().to_lower()
	var hits: Array = [] if not _name_index.has(norm) else _name_index[norm]
	_query_us += Time.get_ticks_usec() - t0
	return hits


func get_summary() -> Dictionary:
	var s := _summary.duplicate()
	# TASK-117：缓存命中/未命中/查询耗时（微秒）随摘要暴露
	s["cache_hits"] = _cache_hits
	s["cache_misses"] = _cache_misses
	s["query_us"] = _query_us
	return s


## 排序辅助（TASK-111）：条目按 name 字典序（不区分大小写），同名按 era 升序；
## 非法行（非字典或缺 name）沉底不崩溃。不动既有契约方法名（load_shard 等）。
static func sort_shard_rows(rows: Array) -> Array:
	var valid: Array = []
	var invalid: Array = []
	for row in rows:
		if typeof(row) == TYPE_DICTIONARY:
			valid.append(row)
		else:
			invalid.append(row)
	valid.sort_custom(func(a, b) -> bool:
		var an: String = str(a.get("name", "")).to_lower()
		var bn: String = str(b.get("name", "")).to_lower()
		if an != bn:
			return an < bn
		return int(a.get("era", a.get("year", 0))) < int(b.get("era", b.get("year", 0))))
	return valid + invalid