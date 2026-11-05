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
##                 "inspect_reset_view": "key_r", "select_next": "key_tab",
##                 "interact": "key_e", "exit_explode": "key_esc" }
## }
## TASK-106B 登记：interact=key_e（选中设备后进入拆解视图）；
## exit_explode=key_esc（另备 key_b 快捷键，见 WALK_EXIT_KEYS）。
## 键名约定：keyboard 用 Godot KEY_* 小写蛇形（如 key_w）；mouse 用 button_left/middle/right、
## mouse_wheel_up/down；joystick 预留（joy_button_0 / joy_axis_0）。
##
## 自检清单（类成员）：
## - load_from_json(text) -> InputProfile     解析并校验；非法 JSON 返回空档案（_valid=false）
## - binding(action: String) -> String         查询动作绑定（查 actions，再查 keyboard/mouse 表）
## - validate() -> String                      返回 ""（合法）或错误说明（供 HUD 显示）
## - to_dict() -> Dictionary                   回导出（供设置界面显示/保存）

const KEY_ACTION_KEYS := ["key_w", "key_a", "key_s", "key_d"]

## 交互键登记（TASK-106B）：
## - INTERACT_KEY    E：inspect_controller 监听，选中设备后进入拆解视图
## - WALK_EXIT_KEYS  ESC/B：退出拆解、回到行走（inspect_controller._exit_explode_to_walk）
## 运行时宿主编排见 inspect_controller.gd（原始 keycode 轮询，与 M0 的 KEY_W 同模式）。
const INTERACT_KEY := "key_e"
const WALK_EXIT_KEYS := ["key_esc", "key_b"]

## 引擎默认兜底层（TASK-115 三级回退第 3 级）：
##   玩家自定义（actions）→ 机种表（keyboard/mouse）→ 引擎默认（FALLBACK_DEFAULTS）。
## 键名沿用 Godot KEY_* 小写蛇形（见文档头结构与 keymap_register.md §2 三级回退表）。
const FALLBACK_DEFAULTS := {
	"move_forward": "key_w", "move_back": "key_s",
	"move_left": "key_a", "move_right": "key_d",
	"select_next": "key_tab", "inspect_reset_view": "key_r",
	"interact": "key_e", "exit_explode": "key_esc",
}

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
	var res := binding_with_level(action)
	return str(res[0])


## TASK-115：三级回退查询——actions(玩家自定义) → keyboard/mouse(机种表) → 引擎默认。
## 返回 [绑定字符串, 命中层级]；层级 ∈ actions/keyboard/mouse/default/unbound。
func binding_with_level(action: String) -> Array:
	if actions.has(action) and str(actions[action]).strip_edges() != "":
		return [str(actions[action]), "actions"]
	if keyboard.has(action) and str(keyboard[action]).strip_edges() != "":
		return [str(keyboard[action]), "keyboard"]
	if mouse.has(action) and str(mouse[action]).strip_edges() != "":
		return [str(mouse[action]), "mouse"]
	if FALLBACK_DEFAULTS.has(action):
		return [str(FALLBACK_DEFAULTS[action]), "default"]
	return ["", "unbound"]


## TASK-115 自检卡：把三级回退固化为可查报表——逐动作命中层级 + 未绑定清单。
func fallback_report() -> Dictionary:
	var levels := {}
	var unbound: Array = []
	var all: Array = []
	for k in actions:
		if not all.has(k):
			all.append(k)
	for k in keyboard:
		if not all.has(k):
			all.append(k)
	for k in mouse:
		if not all.has(k):
			all.append(k)
	for k in FALLBACK_DEFAULTS:
		if not all.has(k):
			all.append(k)
	for k in all:
		var res := binding_with_level(str(k))
		levels[str(k)] = str(res[1])
		if str(res[1]) == "unbound":
			unbound.append(str(k))
	return {"levels": levels, "unbound": unbound}


func has_action(action: String) -> bool:
	return binding(action) != ""


func validate() -> String:
	if not valid:
		return "输入映射 JSON 无效"
	var errors := PackedStringArray()
	for action in actions:
		if str(actions[action]).strip_edges() == "":
			errors.append("actions.%s 绑定为空" % action)
	# TASK-115：未绑定清单并入自检输出（无任何层级命中的动作）
	var report := fallback_report()
	var unbound: Array = report.get("unbound", [])
	if not unbound.is_empty():
		errors.append("未绑定清单:%s" % ",".join(unbound))
	return ", ".join(errors)


func to_dict() -> Dictionary:
	return {"actions": actions, "keyboard": keyboard, "mouse": mouse}