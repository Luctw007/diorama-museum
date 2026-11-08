# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Control
## 四厅导航 HUD（TASK-171-B · 1.0 首批工程）：把 114 的切厅骨架接到玩家面前。
##
## 面板列出四厅（hall_name 一律取自 exhibit_*.json）+ 每厅设备台数 + 当前厅高亮；
## 点击某厅 → ExhibitHost.switch_hall(<布局文件>)；「上一厅/下一厅」按钮快捷切厅。
##
## 交互：M 开/关面板；N 下一厅、P 上一厅（面板关闭时亦可直接切厅）；ESC 关面板
## （仅面板开着时消费，不抢 player 的鼠标捕获）。
## 与 DevicePicker（F1）/ EncyclopediaPanel（Tab）互斥：本面板打开时调用二者 close_panel()。
## 宿主：/root/Main/ExhibitHost（class_name ExhibitHost，直接类型引用，无字符串 has_method）。

const CONTENT_ROOT := "res://content"
## 兜底清单：与 ExhibitHost.hall_files 默认值一致（宿主可用时以宿主为准，单一真相源）
const HALL_FILES_FALLBACK: Array = [
	"exhibit_dawn.json",
	"exhibit_mainframe.json",
	"exhibit_personal.json",
	"exhibit_console.json",
]

var _host: ExhibitHost
var _open := false
var _title: Label
var _hint: Label
var _hall_box: VBoxContainer


func _ready() -> void:
	set_anchors_preset(Control.PRESET_TOP_RIGHT)
	position = Vector2(-320, 120)
	custom_minimum_size = Vector2(300, 0)
	_host = get_node_or_null("/root/Main/ExhibitHost") as ExhibitHost
	_build_ui()
	visible = false


func _build_ui() -> void:
	var bg := Panel.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)
	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 10)
	margin.add_theme_constant_override("margin_top", 10)
	margin.add_theme_constant_override("margin_right", 10)
	margin.add_theme_constant_override("margin_bottom", 10)
	add_child(margin)
	var vbox := VBoxContainer.new()
	margin.add_child(vbox)
	_title = Label.new()
	_title.text = "展厅导航（M 开关 · N/P 快速切厅 · ESC 关闭）"
	vbox.add_child(_title)
	_hall_box = VBoxContainer.new()
	_hall_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	vbox.add_child(_hall_box)
	var row := HBoxContainer.new()
	vbox.add_child(row)
	var btn_prev := Button.new()
	btn_prev.text = "上一厅"
	btn_prev.pressed.connect(func() -> void: _nav(-1))
	row.add_child(btn_prev)
	var btn_next := Button.new()
	btn_next.text = "下一厅"
	btn_next.pressed.connect(func() -> void: _nav(1))
	row.add_child(btn_next)
	_hint = Label.new()
	_hint.add_theme_color_override("font_color", Color(0.7, 0.85, 1.0))
	vbox.add_child(_hint)


func toggle() -> void:
	_open = not _open
	visible = _open
	if _open:
		_close_siblings()
		_refresh()
	else:
		_hint.text = ""


## 供互斥方调用的合上入口（与 DevicePicker/EncyclopediaPanel 同模式）。
func close_panel() -> void:
	_open = false
	visible = false


func _close_siblings() -> void:
	var picker := get_node_or_null("/root/Main/HUD/DevicePicker")
	if picker != null and picker.visible:
		@warning_ignore("unsafe_method_access")
		picker.close_panel()
	var enc := get_node_or_null("/root/Main/HUD/EncyclopediaPanel")
	if enc != null and enc.visible:
		@warning_ignore("unsafe_method_access")
		enc.close_panel()


## 重绘四厅列表：hall_name/台数取布局 JSON；当前厅「●」高亮。
func _refresh() -> void:
	for child in _hall_box.get_children():
		child.queue_free()
	var files: Array = _host.hall_files if (_host != null
			and not _host.hall_files.is_empty()) else HALL_FILES_FALLBACK
	var current: String = _host.current_hall() if _host != null else ""
	_hint.text = "当前厅布局：%s" % (current if current != "" else "（未装载）")
	for f in files:
		var fname: String = str(f)
		var info: Dictionary = _read_hall(fname)
		var prefix: String = "● " if current == fname else "○ "
		var btn := Button.new()
		btn.text = "%s%s（%d 台）" % [prefix, str(info.get("hall_name", fname)),
								int(info.get("count", 0))]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.pressed.connect(func() -> void: _switch_to(fname))
		_hall_box.add_child(btn)


func _read_hall(layout_file: String) -> Dictionary:
	var f := FileAccess.open(CONTENT_ROOT + "/" + layout_file, FileAccess.READ)
	if f == null:
		return {"hall_name": layout_file, "count": 0}
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		return {"hall_name": layout_file, "count": 0}
	var d: Dictionary = parsed
	var devices: Array = d.get("devices", []) if typeof(d.get("devices", [])) == TYPE_ARRAY else []
	return {"hall_name": str(d.get("hall_name", layout_file)), "count": devices.size()}


## 点击某厅 → 切厅（走 ExhibitHost.switch_hall 既有语义，切厅成功与否只看返回值）。
func _switch_to(layout_file: String) -> void:
	if _host == null:
		_hint.text = "ExhibitHost 未找到，无法切厅"
		return
	var ok: bool = _host.switch_hall(layout_file)
	_hint.text = "已切换：%s" % layout_file if ok else "切换失败：%s" % layout_file
	_refresh()


## 快捷切厅：dir>0 下一厅 / dir<0 上一厅（ExhibitHost.next_hall/prev_hall，114 落地）。
func _nav(dir: int) -> void:
	if _host == null:
		_hint.text = "ExhibitHost 未找到，无法切厅"
		return
	var next_hall: String = _host.next_hall() if dir > 0 else _host.prev_hall()
	_hint.text = "当前厅布局：%s" % (next_hall if next_hall != "" else "（切换失败）")
	_refresh()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_M:
				get_viewport().set_input_as_handled()
				toggle()
			KEY_N:
				get_viewport().set_input_as_handled()
				_nav(1)
			KEY_P:
				get_viewport().set_input_as_handled()
				_nav(-1)
			KEY_ESCAPE:
				if _open:
					get_viewport().set_input_as_handled()   # 只开着时消费，不抢 player
					close_panel()