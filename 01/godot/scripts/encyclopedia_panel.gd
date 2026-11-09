# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Control
## 图鉴面板（TASK-106A）：把 1484 条目录变成可浏览的图鉴骨架——v0.1 三件套③第一步。
##
## 数据层零重写：直接复用 CatalogData（catalog_data.gd）——
##   get_shards() → 28 个中分类（大分类/中分类）；load_shard(big, mid) → 条目数组
##   （缓存命中零 IO）。meta.json 由 01 线 catalog 工具链生成，本面板只读。
##
## 交互（复用 input_profile 习惯键位）：
##   Tab（ui_focus_next）  打开/关闭面板；ESC（ui_cancel）关闭。
##   与 DevicePicker 互斥：本面板打开时合上 DevicePicker（Tab 归属本面板，
##   DevicePicker 改由 F1 开关，见 device_picker.gd）。
##
## 布局：左 = 中分类列表；右 = 条目三列（名称 · 年代 · 厂商）；
##       底 = 详情行（taxonomy_path 全称 · status · device_id · influence 前 80 字）。

const PANEL_SIZE := Vector2(680, 380)
const MID_LIST_WIDTH := 200.0
const INFLUENCE_LEN := 80   # 影响力截断长度（详情行）

var _catalog: CatalogData = null   # 数据层实例（load_meta 后可用）
var _open := false
var _mid_list: ItemList
var _shards: Array = []            # 与 _mid_list 平行的分片字典数组
var _row_list: ItemList
var _detail: Label
var _title: Label
var _rows: Array = []              # 当前分片行缓存（原始顺序）
var _shown_rows: Array = []        # 与右侧列表顺序一致的行（排序后同序）
var _sort_button: Button
var _sort_enabled := true          # 排序开关（TASK-111，默认开，可关闭）
var _invalid_rows := 0             # 当前分片非法行数（降级提示用）


func _ready() -> void:
	# 居中放置（锚点中心；position 为相对锚点的偏移）
	set_anchors_preset(Control.PRESET_CENTER)
	position = Vector2(-PANEL_SIZE.x * 0.5, -PANEL_SIZE.y * 0.5)
	custom_minimum_size = PANEL_SIZE

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
	_title.text = "设备图鉴（Tab 开关 · ESC 关闭 · 目录加载中…）"
	vbox.add_child(_title)

	var row := HBoxContainer.new()
	row.size_flags_vertical = Control.SIZE_EXPAND_FILL
	vbox.add_child(row)

	var left := VBoxContainer.new()
	left.custom_minimum_size = Vector2(MID_LIST_WIDTH, 0)
	row.add_child(left)
	var mid_label := Label.new()
	mid_label.text = "中分类"
	left.add_child(mid_label)
	_mid_list = ItemList.new()
	_mid_list.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_mid_list.item_selected.connect(_on_mid_selected)
	left.add_child(_mid_list)

	var right := VBoxContainer.new()
	right.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(right)
	var entry_row := HBoxContainer.new()
	right.add_child(entry_row)
	var entry_label := Label.new()
	entry_label.text = "条目（名称 · 年代 · 厂商）"
	entry_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	entry_row.add_child(entry_label)
	_sort_button = Button.new()
	_sort_button.text = "排序:开"
	_sort_button.tooltip_text = "条目按名称排序（同名按年代升序）；点击关闭，回退为分片源码顺序"
	_sort_button.pressed.connect(_on_sort_toggled)
	entry_row.add_child(_sort_button)
	_row_list = ItemList.new()
	_row_list.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_row_list.item_selected.connect(_on_row_selected)
	right.add_child(_row_list)

	_detail = Label.new()
	_detail.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_detail.custom_minimum_size = Vector2(0, 56)
	_detail.add_theme_font_size_override("font_size", 13)
	_detail.add_theme_color_override("font_color", Color(0.85, 0.75, 0.4))
	vbox.add_child(_detail)

	visible = false
	# 数据层：CatalogData（catalog_data.gd），失败时标题显示原因
	_catalog = CatalogData.new()
	if _catalog.load_meta():
		_title.text = "设备图鉴（Tab 开关 · ESC 关闭 · 共 %d 条）" % int(_catalog.get_summary().get("total_rows", 0))
		_rebuild_mid_list()
	else:
		_title.text = "设备图鉴：catalog/meta.json 加载失败"


func toggle() -> void:
	_open = not _open
	visible = _open
	if _open:
		# 与 DevicePicker 互斥：打开本面板时合上设备选择面板
		var picker := get_node_or_null("/root/Main/HUD/DevicePicker")
		if picker != null and picker.visible:
			@warning_ignore("unsafe_method_access")
			picker.close_panel()
	_sync_panel_mouse()


func close_panel() -> void:
	_open = false
	visible = false
	_sync_panel_mouse()


## RUN-08：任何面板可见即释放鼠标捕获；全关后恢复捕获（与 device_picker 同模式）。
func _sync_panel_mouse() -> void:
	var hud := get_node_or_null("/root/Main/HUD")
	if hud == null:
		return
	var any_open := false
	for panel_name in ["DevicePicker", "EncyclopediaPanel", "HallNavPanel"]:
		var panel := hud.get_node_or_null(panel_name)
		if panel != null and panel.visible:
			any_open = true
	var cam := get_node_or_null("/root/Main/Room/Camera")
	if cam != null and cam.has_method("set_captured"):
		@warning_ignore("unsafe_method_access")
		cam.set_captured(not any_open)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_focus_next") and event.pressed \
			and not (event is InputEventKey and event.echo):
		get_viewport().set_input_as_handled()   # Tab 归本面板（DevicePicker 改走 F1）
		toggle()
	elif event.is_action_pressed("ui_cancel") and _open:
		get_viewport().set_input_as_handled()   # 已消费：不打扰 player 的 ESC（鼠标捕获）
		close_panel()


func _rebuild_mid_list() -> void:
	_mid_list.clear()
	var shards: Array = _catalog.get_shards()
	_shards = []
	for shard in shards:
		_mid_list.add_item("%s · %s（%s）" % [
			str((shard as Dictionary).get("big", "")),
			str((shard as Dictionary).get("mid", "")),
			str((shard as Dictionary).get("rows", 0))])
		_shards.append(shard)
	if _shards.is_empty():
		_detail.text = "目录无分片数据"


func _on_mid_selected(index: int) -> void:
	if index < 0 or index >= _shards.size():
		return
	var shard: Dictionary = _shards[index]
	var loaded: Array = _catalog.load_shard(str(shard.get("big", "")), str(shard.get("mid", "")))
	# TASK-111 降级：非法行计数并置底（缺 name/era/manufacturer 的字典行按缺省显示，不崩溃）
	_invalid_rows = 0
	for row in loaded:
		if typeof(row) != TYPE_DICTIONARY:
			_invalid_rows += 1
	_rows = loaded
	_populate_rows()
	var note := "已选中「%s」%d 条" % [str(shard.get("mid", "")), _rows.size()]
	if _invalid_rows > 0:
		note += "（含 %d 条非法行已置底）" % _invalid_rows
	_detail.text = note


## 条目排序开关（TASK-111）：开=name 升序（同名按 era），关=分片源码顺序。
func _on_sort_toggled() -> void:
	_sort_enabled = not _sort_enabled
	_sort_button.text = "排序:%s" % ("开" if _sort_enabled else "关")
	_populate_rows()


func _populate_rows() -> void:
	_row_list.clear()
	if _rows.is_empty():
		_detail.text = "该分片无条目"
		return
	# TASK-111：中分类按 meta.json shards 顺序稳定展示（_shards 即该顺序，
	# 不另排序）；条目按 name 排序且可关闭。
	var shown: Array = _rows
	if _sort_enabled:
		shown = CatalogData.sort_shard_rows(_rows)
	_shown_rows = shown
	for row in shown:
		if typeof(row) != TYPE_DICTIONARY:
			_row_list.add_item("（非法行）")
			continue
		var r: Dictionary = row
		_row_list.add_item("%s ｜ %s ｜ %s" % [
			str(r.get("name", "-")), str(r.get("era", "-")), str(r.get("manufacturer", "-"))])


func _on_row_selected(index: int) -> void:
	if index < 0 or index >= _shown_rows.size():
		return
	var row: Variant = _shown_rows[index]
	if typeof(row) != TYPE_DICTIONARY:
		_detail.text = "（非法行，无详情）"
		return
	var r: Dictionary = row
	var tx: Array = r.get("_taxonomy", r.get("taxonomy_path", []))
	var influence := str(r.get("influence", r.get("reason", "")))
	_detail.text = "%s\n状态 %s · 包 %s · %s" % [
		" › ".join(tx) if not tx.is_empty() else "（无分类路径）",
		str(r.get("status", "-")), str(r.get("device_id", "-")),
		influence.left(INFLUENCE_LEN)]