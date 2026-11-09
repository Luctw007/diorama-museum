# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Node
## 引擎启动自检屏（TASK-120）：_ready 内跑三项 quickcheck，HUD 逐项打 PASS/FAIL，
## 便于实机首验排障（失败可降级，只打标不崩溃）。
##
## 三项：
##   1. 目录可读   DirAccess.open("res://content") 成功且枚举非空；
##   2. meta 可读   任一内容包 meta.json 解析为 Dictionary；
##   3. 槽位表可读 res://slots/emulators 有 manifest 可读 → OK(清单)；
##                否则走内置登记口径（网关 EMULATORS 内置登记）→ OK(内置)。
## 自检三行挂在 HUD（CanvasLayer）顶部下方，与 gateway_client 同模式。

const CONTENT_ROOT := "res://content"
const SLOTS_ROOT := "res://slots/emulators"

var _hud_lines: Array = []


func _ready() -> void:
	var hud := get_node_or_null("/root/Main/HUD") as CanvasLayer
	if hud == null:
		push_warning("[StartupCheck] HUD 不存在，自检结果仅输出面板")
	_run_checks()
	if hud != null:
		_build_hud(hud)


## 三项 quickcheck（可降级：任何异常 → 该项 FAIL，不中断）
func _run_checks() -> void:
	_hud_lines = [_check_content_dir(), _check_meta(), _check_slots()]


func _check_content_dir() -> String:
	var dir := DirAccess.open(CONTENT_ROOT)
	if dir == null:
		return "目录 FAIL：res://content 不可打开"
	dir.list_dir_begin()
	var count := 0
	var entry_name := dir.get_next()
	while entry_name != "":
		if dir.current_is_dir() and not entry_name.begins_with("."):
			count += 1
		entry_name = dir.get_next()
	dir.list_dir_end()
	return "目录 OK：%d 个子目录" % count if count > 0 else "目录 FAIL：枚举为空"


func _check_meta() -> String:
	var dir := DirAccess.open(CONTENT_ROOT)
	if dir == null:
		return "meta FAIL：res://content 不可打开"
	dir.list_dir_begin()
	var entry_name := dir.get_next()
	while entry_name != "":
		if dir.current_is_dir() and not entry_name.begins_with("."):
			var pkg_meta := CONTENT_ROOT + "/" + entry_name + "/meta.json"
			if FileAccess.file_exists(pkg_meta):
				var f := FileAccess.open(pkg_meta, FileAccess.READ)
				if f != null:
					var parsed: Variant = JSON.parse_string(f.get_as_text())
					f.close()
					if typeof(parsed) == TYPE_DICTIONARY:
						return "meta OK：%s/meta.json 解析为 Dictionary" % entry_name
		entry_name = dir.get_next()
	dir.list_dir_end()
	return "meta FAIL：未发现可解析的包 meta.json"


## 槽位表：优先读 res://slots/emulators 清单；缺失时按"内置登记"口径降级为 OK。
func _check_slots() -> String:
	var dir := DirAccess.open(SLOTS_ROOT)
	if dir == null:
		return "槽位表 OK：走内置登记口径（res://slots 未导出）"
	var manifests := 0
	dir.list_dir_begin()
	var entry_name := dir.get_next()
	while entry_name != "":
		if dir.current_is_dir():
			var mpath := SLOTS_ROOT + "/" + entry_name + "/manifest.json"
			if FileAccess.file_exists(mpath):
				manifests += 1
		entry_name = dir.get_next()
	dir.list_dir_end()
	return "槽位表 OK：%d 个 manifest" % manifests if manifests > 0 else "槽位表 FAIL：slots 目录无 manifest"


func _build_hud(hud: CanvasLayer) -> void:
	var title := Label.new()
	title.text = "[启动自检 quickcheck]"
	title.position = Vector2(16, 64)
	title.add_theme_font_size_override("font_size", 14)
	hud.add_child(title)
	var y := 84.0
	for line in _hud_lines:
		var lab := Label.new()
		lab.text = "  " + str(line)
		lab.position = Vector2(16, y)
		lab.add_theme_font_size_override("font_size", 13)
		hud.add_child(lab)
		y += 18.0