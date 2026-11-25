# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Camera3D
## 展厅漫游相机（M0 原型）：WASD 平移、鼠标环视、滚轮缩放 FOV、ESC 释放鼠标。
## 说明：M0 采用无碰撞自由移动（对应设计文档 FR-B1"无碰撞约束"的观察需求）。

const MOVE_SPEED := 3.0
const LOOK_SPEED := 0.0025
const FOV_DEFAULT := 70.0
const FOV_MAX := 85.0

## 57 号行走相机手感参数卡 v2（TASK-148，只读引用）双档限速常量静态落地（TASK-291-I）：
## 运行时不切换档位——M0 运行时仍用上方 MOVE_SPEED=3.0 单档；档位切换与 F-10
## 导览镜头联动（291-B narr_tour_controller.gd 同款常量），标「待实机」。
const WALK_SPEED_NORMAL := 2.5        # 常态行走（57 号 v2 建议值）
const WALK_SPEED_NARR := 1.4          # 播报中限速档（16 号全程规则加档）
const TURN_SPEED_REDLINE := 200.0     # 转身角速度红线（°/s，12 号晕动红线）
const PITCH_CLAMP_DEG := 70.0         # 环视俯仰上限 ±70°（57 号 v2 建议值；M0 现值 ±85 待切换）
const MOVE_DAMP_SEC := 0.15           # 起停线性阻尼（s，防急停晕动）

var _captured := false
## F-14⑥（TASK-301-J）：玩家碰撞体——Camera3D 下挂 CharacterBody3D 子节点 + CapsuleShape3D，
## 并 add_to_group("player") 与 portal_hub PLAYER_GROUP 契约对齐（portal 碰撞传送前置）。
## 位置每帧同步相机；本文件运行时移动仍沿用现有 WASD 直改 global_position（M0 无碰撞
## 自由移动口径不变，不臆造新增手感参数）。待实机：碰撞传送（F-14⑥）与墙体碰撞走查。
var _body = null


func _ready() -> void:
	fov = FOV_DEFAULT
	set_captured(true)
	_body = CharacterBody3D.new()
	_body.name = "PlayerBody"
	add_child(_body)
	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.height = 1.7    # 站姿高度（57 号 v2 眼高 1.55 m 口径加余量）
	capsule.radius = 0.35
	shape.shape = capsule
	_body.add_child(shape)
	_body.add_to_group("player")   # portal_hub PLAYER_GROUP := "player" 契约
	# TASK-316-M：相机聚焦插值本体（gap #3）——连接 ExplodeController.focus_requested 信号
	# （306-H 已 emit {center, duration}），tween 运镜到目标框中心；节点/信号缺失时静默不崩。
	var explode := get_node_or_null("/root/Main/DeviceRoot/ExplodeController")
	if explode != null and explode.has_signal("focus_requested"):
		explode.focus_requested.connect(_on_focus_requested)


## 鼠标捕获开关（RUN-08 公开化）：面板打开时由 UI 调 set_captured(false) 释放鼠标，
## 面板关闭后恢复捕获。ESC 切换逻辑不变。
func set_captured(on: bool) -> void:
	_captured = on
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED if on else Input.MOUSE_MODE_VISIBLE


## TASK-316-M：聚焦运镜插值（depth_model §4 gap #3 本体）——tween 把相机位置插值到
## 目标框中心并朝向目标（look_at），时长取 signal 传入 duration（0.9~1.2s 区间，
## 防御钳制 0.2~3.0s）。不改 WASD/FOV 移动语义、不新增手感参数；运镜观感待实机验证。
func _on_focus_requested(target: Vector3, duration: float) -> void:
	var tw := create_tween()
	var dur := clampf(duration, 0.2, 3.0)
	tw.tween_property(self, "global_position", target, dur)
	tw.tween_callback(look_at.bind(target))


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
	if _body != null:
		_body.global_position = global_position   # 碰撞体跟随相机（portal 触发检测体）