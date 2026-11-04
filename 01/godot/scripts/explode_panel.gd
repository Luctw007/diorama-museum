# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Control
## 拆解 HUD 面板（TASK-11C 配套，桌面版）。
##
## 与 explode_controller.gd 联动：
## - 展开滑杆（0..1）→ set_explode_value()
## - 开盖/拆解/复原 按钮 → set_open() / set_exploded() / reset_explode()
## - 零件清单：按 loader 装配节点生成（勾选 = 该层是否脱离基准形变）
## - 状态与拒绝提示显示（denied_reason 信号）
##
## 自检清单：
## - func bind(explode, loader)     绑定控制器与装载器
## - _refresh_parts()               重建零件清单
## - 布局锚点：屏幕右下，宽 280px，不抢主视区)

var _explode: Node = null
var _loader: Node = null
var _state_label: Label
var _hint_label: Label
var _slider: HSlider
var _parts_box: VBoxContainer
var _locked_down := false

const STATE_NAMES := {0: "完整", 1: "开盖", 2: "拆解中"}


func _ready() -> void:
	custom_minimum_size = Vector2(280, 0)
	set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	position = Vector2(-292, -8)
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
	margin.add_child(vbox)  # 注意：子控件挂在 margin 之下（margin 本身在面板之上）

	_state_label = Label.new()
	_state_label.text = "拆解面板（未绑定）"
	vbox.add_child(_state_label)

	var row := HBoxContainer.new()
	vbox.add_child(row)
	var btn_open := Button.new()
	btn_open.text = "开盖"
	btn_open.pressed.connect(func(): if _explode: _explode.set_open())
	row.add_child(btn_open)
	var btn_explode := Button.new()
	btn_explode.text = "拆解"
	btn_explode.pressed.connect(func(): if _explode: _explode.set_exploded())
	row.add_child(btn_explode)
	var btn_reset := Button.new()
	btn_reset.text = "复原"
	btn_reset.pressed.connect(func():
		if _explode:
			_explode.reset_explode())
	row.add_child(btn_reset)

	_slider = HSlider.new()
	_slider.min_value = 0.0
	_slider.max_value = 1.0
	_slider.step = 0.01
	_slider.value_changed.connect(_on_slider)
	_slider.editable = false
	vbox.add_child(_slider)

	_parts_box = VBoxContainer.new()
	_parts_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	vbox.add_child(_parts_box)

	_hint_label = Label.new()
	_hint_label.add_theme_color_override("font_color", Color(0.85, 0.6, 0.2))
	vbox.add_child(_hint_label)

	# 自动绑定场景节点
	bind(get_node_or_null("/root/Main/DeviceRoot/ExplodeController"),
		 get_node_or_null("/root/Main/DeviceRoot"))


func bind(explode: Node, loader: Node) -> void:
	_explode = explode
	_loader = loader
	if _explode != null and _explode.has_signal("state_changed"):
		_explode.state_changed.connect(_on_state_changed)
	if _explode != null and _explode.has_signal("denied_reason"):
		_explode.denied_reason.connect(_on_denied)
	if _loader != null and _loader.has_signal("device_loaded"):
		_loader.device_loaded.connect(func(_id: String) -> void: _refresh_parts())


func _on_state_changed(_old: int, new: int) -> void:
	_state_label.text = "设备状态：" + str(STATE_NAMES.get(new, "?"))
	_slider.editable = new == 2
	if new != 2:
		_slider.value = 0.0


func _on_slider(value: float) -> void:
	if _locked_down:
		return
	if _explode != null:
		_explode.set_explode_value(value)


func _on_denied(reason: String) -> void:
	_hint_label.text = reason
	var timer := get_tree().create_timer(3.0)
	timer.timeout.connect(func(): _hint_label.text = "")


func _refresh_parts() -> void:
	if _parts_box == null:
		return
	for child in _parts_box.get_children():
		child.queue_free()
	if _loader == null or not _loader.has_method("get_assembly_nodes"):
		return
	var nodes: Dictionary = _loader.get_assembly_nodes()
	for aid in nodes:
		var label := Label.new()
		var node: Node3D = nodes[aid]
		var entry: Dictionary = node.get_meta("asmb_entry", {})
		var name_txt := str(entry.get("name", aid))
		label.text = "· %s（%s）" % [name_txt, aid]
		_parts_box.add_child(label)