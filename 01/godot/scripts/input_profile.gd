# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
class_name InputProfile
extends RefCounted
## 输入映射配置加载与查询（M1，静态工具类）。
##
## JSON 结构（与 02 线《内容包规范》第 11 章、04 线交互规格对齐的起始版）：
## {
##   "keyboard": { "move_forward": "key_w", "move_back": "key_s",
##                 "move_left": "key_a", "move_right": "key_d" },
##   "mouse":    { "inspect_rotate": "button_left", "inspect_pan": "button_middle" },
##   "actions":  { "inspect_zoom": "mouse_wheel_up", "inspect_zoom_out": "mouse_wheel_down",
##                 "inspect_reset_view": "key_r", "select_next": "key_tab" }
## }
## 键名约定：keyboard 用 Godot KEY_* 小写蛇形（如 key_w）；mouse 用 button_left/middle/right、
## mouse_wheel_up/down；joystick 预留（joy_button_0 / joy_axis_0）。
##
## 自检清单（类成员）：
## - load_from_json(text) -> InputProfile     解析并校验；非法 JSON 返回空档案（_valid=false）
## - binding(action: String) -> String         查询动作绑定（查 actions，再查 keyboard/mouse 表）
## - validate() -> String                      返回 ""（合法）或错误说明（供 HUD 显示）
## - to_dict() -> Dictionary                   回导出（供设置界面显示/保存）

const KEY_ACTION_KEYS := ["key_w", "key_a", "key_s", "key_d"]

var actions := {}          # 动作 → 绑定字符串
var keyboard := {}         # 键盘动作 → 键名
var mouse := {}            # 鼠标动作 → 按键名
var valid := false


static func load_from_json(text: String) -> InputProfile:
	var profile := InputProfile.new()
	var data = JSON.parse_string(text)
	if typeof(data) != TYPE_DICTIONARY:
		return profile
	profile.actions = data.get("actions", {}) if typeof(data.get("actions", {})) == TYPE_DICTIONARY else {}
	profile.keyboard = data.get("keyboard", {}) if typeof(data.get("keyboard", {})) == TYPE_DICTIONARY else {}
	profile.mouse = data.get("mouse", {}) if typeof(data.get("mouse", {})) == TYPE_DICTIONARY else {}
	profile.valid = true
	return profile


func binding(action: String) -> String:
	if actions.has(action):
		return str(actions[action])
	if keyboard.has(action):
		return str(keyboard[action])
	if mouse.has(action):
		return str(mouse[action])
	return ""


func has_action(action: String) -> bool:
	return binding(action) != ""


func validate() -> String:
	if not valid:
		return "输入映射 JSON 无效"
	var errors := PackedStringArray()
	for action in actions:
		if str(actions[action]).strip_edges() == "":
			errors.append("actions.%s 绑定为空" % action)
	return ", ".join(errors)


func to_dict() -> Dictionary:
	return {"actions": actions, "keyboard": keyboard, "mouse": mouse}