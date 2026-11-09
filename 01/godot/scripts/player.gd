# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Camera3D
## 展厅漫游相机（M0 原型）：WASD 平移、鼠标环视、滚轮缩放 FOV、ESC 释放鼠标。
## 说明：M0 采用无碰撞自由移动（对应设计文档 FR-B1"无碰撞约束"的观察需求）。

const MOVE_SPEED := 3.0
const LOOK_SPEED := 0.0025
const FOV_DEFAULT := 70.0
const FOV_MAX := 85.0

var _captured := false


func _ready() -> void:
	fov = FOV_DEFAULT
	set_captured(true)


## 鼠标捕获开关（RUN-08 公开化）：面板打开时由 UI 调 set_captured(false) 释放鼠标，
## 面板关闭后恢复捕获。ESC 切换逻辑不变。
func set_captured(on: bool) -> void:
	_captured = on
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED if on else Input.MOUSE_MODE_VISIBLE


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and _captured:
		rotation_degrees.y -= event.relative.x * LOOK_SPEED * 100.0
		var pitch: float = rotation_degrees.x - event.relative.y * LOOK_SPEED * 100.0
		rotation_degrees.x = clampf(pitch, -85.0, 85.0)
	elif event is InputEventMouseButton and event.pressed:
		match event.button_index:
			MOUSE_BUTTON_WHEEL_UP:
				fov = clampf(fov - 3.0, 20.0, FOV_MAX)
			MOUSE_BUTTON_WHEEL_DOWN:
				fov = clampf(fov + 3.0, 20.0, FOV_MAX)
	elif event.is_action_pressed("ui_cancel"):
		set_captured(not _captured)


func _process(delta: float) -> void:
	if not _captured:
		return
	var dir := Vector3.ZERO
	if Input.is_key_pressed(KEY_W):
		dir += -global_transform.basis.z
	if Input.is_key_pressed(KEY_S):
		dir -= -global_transform.basis.z
	if Input.is_key_pressed(KEY_A):
		dir += -global_transform.basis.x
	if Input.is_key_pressed(KEY_D):
		dir -= -global_transform.basis.x
	dir.y = 0.0  # 水平移动不受俯仰影响
	if dir != Vector3.ZERO:
		global_position += dir.normalized() * MOVE_SPEED * delta