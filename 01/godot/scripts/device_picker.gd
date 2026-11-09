# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Control
## 设备选择面板（TASK-11A）：图鉴入口的桌面版实现。
##
## 对齐 04 线《02_UI信息架构》图鉴条目态：可玩（runtime 非 none）加"PLAY 候选"角标、
## 可看可拆（正常）普通条目、未安装/不可加载置灰。
## 交互：F1 开/关面板；点击条目加载设备；ESC 关闭。加载结果由 DeviceLoader 信号驱动。
## 注（TASK-106A）：Tab 已让位给目录图鉴 EncyclopediaPanel（encyclopedia_panel.gd），
## 本面板改由 F1 开关；两面板互斥（本面板提供 close_panel() 供对方合上自己）。
##
## 自检清单：
## - func bind(loader: Node)         绑定 DeviceLoader（读取 index / 信号）
## - func toggle()                   开/关面板
## - _refresh()                      按 index 重建条目（列表 + 状态 + 角标）
## - 信号：device_selected(device_id)

signal device_selected(device_id: String)

const PANEL_SIZE := Vector2(360, 220)
const ITEM_HEIGHT := 34.0

var _loader: Node = null
var _open := false
var _title: Label
var _list: VBoxContainer
var _hint: Label


func _ready() -> void:
	custom_minimum_size = PANEL_SIZE
	# 面板底板与布局
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
	_title.text = "设备图鉴（F1 开关 · ESC 关闭）"
	vbox.add_child(_title)
	_list = VBoxContainer.new()
	_list.size_flags_vertical = Control.SIZE_EXPAND_FILL
	vbox.add_child(_list)
	_hint = Label.new()
	_hint.text = "暂无设备索引"
	_hint.add_theme_color_override("font_color", Color(0.6, 0.6, 0.6))
	vbox.add_child(_hint)
	visible = false
	position = Vector2(16, 48)
	# 自动绑定场景中的 DeviceRoot（device_loader）
	var loader := get_node_or_null("/root/Main/DeviceRoot")
	if loader != null:
		bind(loader)


func bind(loader: Node) -> void:
	_loader = loader
	if _loader != null and _loader.has_signal("device_index_ready"):
		_loader.device_index_ready.connect(_on_index_ready)
	if _loader != null and _loader.has_signal("device_loaded"):
		_loader.device_loaded.connect(_on_device_loaded)
	if _loader != null and _loader.has_method("get_device_index"):
		_on_index_ready(_loader.get_device_index())


func toggle() -> void:
	_open = not _open
	visible = _open
	if _open:
		_refresh()
	_sync_panel_mouse()


## 供 EncyclopediaPanel 调用：目录图鉴打开时合上本面板（两图鉴互斥）。
func close_panel() -> void:
	_open = false
	visible = false
	_sync_panel_mouse()


## RUN-08：任何面板可见即释放鼠标捕获（GUI 才能点按钮）；全关后恢复捕获。
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
	if event is InputEventKey and event.pressed and not event.echo \
			and event.keycode == KEY_F1:
		get_viewport().set_input_as_handled()
		toggle()
	elif event.is_action_pressed("ui_cancel") and _open:
		get_viewport().set_input_as_handled()
		_open = false
		visible = false


func _on_index_ready(index: Array) -> void:
	# 存最近一次索引，等面板打开时刷新
	set_meta("last_index", index)
	if _open:
		_refresh()


func _on_device_loaded(device_id: String) -> void:
	_refresh()
	_hint.text = "已装载：%s" % device_id


func _refresh() -> void:
	if _loader == null or _list == null:
		return
	for child in _list.get_children():
		child.queue_free()
	var index: Array = _loader.get_device_index()
	if index.is_empty():
		_hint.text = "content/ 下没有可加载的设备包"
		return
	var loadable_count := 0
	for entry in index:
		if entry.get("loadable", false):
			loadable_count += 1
		_add_item(entry)
	_hint.text = "共 %d 台，可加载 %d 台" % [index.size(), loadable_count]


func _add_item(entry: Dictionary) -> void:
	var item := Button.new()
	var device_id := str(entry.get("id", ""))
	var loadable: bool = entry.get("loadable", false)
	var title := "%s · %s" % [device_id, str(entry.get("name", ""))]
	item.text = title
	item.disabled = not loadable
	item.alignment = HORIZONTAL_ALIGNMENT_LEFT
	item.custom_minimum_size = Vector2(0, ITEM_HEIGHT)
	item.tooltip_text = "类别 %s · 精度 %s" % [entry.get("category", "-"),
											entry.get("precision_level", "L2")]
	item.pressed.connect(func() -> void:
		select_device(device_id))
	_list.add_child(item)


func select_device(device_id: String) -> void:
	if _loader != null and _loader.has_method("load_device"):
		@warning_ignore("unsafe_method_access")
		_loader.load_device(device_id)
	device_selected.emit(device_id)
	_open = false
	visible = false