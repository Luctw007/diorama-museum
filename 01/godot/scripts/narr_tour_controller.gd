# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Node
class_name NarrTourController
## F-10（TASK-291-B）：馆长路线导览调度器——导览启动 → 镜头接管 → 站间迁移 → 导览结束回行走。
## 按 276-B 预研口径做静态接线（39 号馆长路线 8 站卡 + 57 号行走相机参数卡 v2）；不上 Godot
## 实机，实机行为标「待实机」。调度器数据源 = 39 号 §5 映射 {station, ref, stay_sec, radius}。
##
## 静态接线点：
##   1. 导览启动（HUD「馆长路线」徽标）→ 镜头接管（玩家行走/环视输入挂起，待实机）；
##   2. 站内巡航/站间迁移按 39 号路线静态序列（三选一：进触发区 / 手动 next / 超时 +15s 提示）；
##   3. 导览结束回行走（自由漫游，状态复位）。
## 57 号参数衔接：播报限速 1.4 m/s 档与导览镜头同源常量（player.gd 双档常量对齐 TASK-291-I）。
## 与 F-9 口播联动（TASK-271-A）：站内讲解复用 narr_player 单口播互斥通道（同刻仅一条）。

## 39 号馆长路线全馆导览 v1（TASK-74A，只读引用）§1/§5 动线总图 8 站卡静态序列。
## radius = -1.0 表示主站（子站触发半径沿用各台本总谱，39 号 §3.1 口径）。
const TOUR_STATIONS := [
	{"station": "door", "name": "馆门入口", "ref": "03", "stay_sec": 8, "radius": 1.5},
	{"station": "dawn", "name": "黎明厅", "ref": "16", "stay_sec": 458, "radius": -1.0},
	{"station": "wall", "name": "时间轴墙", "ref": "34", "stay_sec": 90, "radius": 2.0},
	{"station": "main", "name": "大型机厅", "ref": "22", "stay_sec": 388, "radius": -1.0},
	{"station": "pc", "name": "个人机厅", "ref": "27", "stay_sec": 473, "radius": -1.0},
	{"station": "game", "name": "游戏机厅", "ref": "41", "stay_sec": 530, "radius": -1.0},
	{"station": "pedia", "name": "图鉴与拆解", "ref": "35/32", "stay_sec": 60, "radius": -1.0},
	{"station": "exit_", "name": "出口", "ref": "16", "stay_sec": 35, "radius": 2.0},
]
## 厅站 → 布局文件映射（与 ExhibitHost.hall_files 一致；站内讲解经 play_hall_narr 触发）。
const STATION_LAYOUT := {
	"dawn": "exhibit_dawn.json",
	"main": "exhibit_mainframe.json",
	"pc": "exhibit_personal.json",
	"game": "exhibit_console.json",
}
## 57 号行走相机手感参数卡 v2（TASK-148，只读引用）导览镜头口径常量。
const WALK_SPEED_NORMAL := 2.5        # 常态行走（m/s）
const WALK_SPEED_NARR := 1.4          # 播报中限速档（m/s，16 号全程规则加档）
const TURN_SPEED_REDLINE := 200.0     # 转身角速度红线（°/s，12 号晕动红线）
const FOV_REDLINE_MIN := 50.0         # FOV 红线下限（57 号 §2）
const FOV_REDLINE_MAX := 100.0        # FOV 红线上限
const MOVE_DAMP_SEC := 0.15           # 起停线性阻尼（s，导览镜头起步/急停同款适用）
const TIMEOUT_GRACE_SEC := 15.0       # 39 号 §3.1 超时自动推进宽限（本站停留 +15s 提示「我们继续」）

var _tour_active := false     # 导览模式开关（39 号 §3.3 馆长路线 ↔ 自由漫游一键切换）
var _station_index := 0       # 当前站游标
var _station_timer := 0.0     # 本站停留计时（超时推进判定，待实机）
var _timeout_pending := false # 超时宽限已到、待句末推进（待实机核对句末判定）
var _hud_label: Label


func _ready() -> void:
	var hud := get_node_or_null("/root/Main/HUD") as CanvasLayer
	if hud != null:
		_hud_label = Label.new()
		_hud_label.position = Vector2(16, 258)
		_hud_label.add_theme_font_size_override("font_size", 13)
		hud.add_child(_hud_label)
	_set_hud("馆长路线：未启动（自由漫游）")


## 导览启动：置模式开关 + 站游标归零 + 镜头接管（HUD「馆长路线」徽标）。
## 镜头接管口径（待实机）：玩家行走/环视输入挂起，行走限速切 1.4 m/s 播报档
## （player.gd 双档常量 TASK-291-I 已静态落地，运行时切换待实机）；首站触发
## 若为厅站则经 play_hall_narr 播厅内首条口播（复用 F-9 单口播互斥通道）。
func start_tour() -> void:
	_tour_active = true
	_station_index = 0
	_station_timer = 0.0
	_timeout_pending = false
	_set_hud("馆长路线：%s（1/%d）" % [station_name(), TOUR_STATIONS.size()])
	_notify_station_narr()


## 导览结束回行走（39 号 §3.3 退出）：状态复位、站标清空、计时停止；镜头回自由漫游
## 与行走档位恢复待实机（输入挂起解除）。
func stop_tour() -> void:
	_tour_active = false
	_station_timer = 0.0
	_timeout_pending = false
	_set_hud("馆长路线：已结束（回自由漫游）")


## 手动下一步（39 号 §3.1 第 2 项）：推进到下一站并触发该站讲解；到末尾则结束导览。
func next_station() -> bool:
	if not _tour_active:
		return false
	if _station_index + 1 >= TOUR_STATIONS.size():
		stop_tour()
		return true
	_station_index += 1
	_station_timer = 0.0
	_timeout_pending = false
	_set_hud("馆长路线：%s（%d/%d）" % [station_name(), _station_index + 1, TOUR_STATIONS.size()])
	_notify_station_narr()
	return true


## 当前站卡（无则空字典）。
func current_station() -> Dictionary:
	if _station_index >= 0 and _station_index < TOUR_STATIONS.size():
		return TOUR_STATIONS[_station_index]
	return {}


func station_name() -> String:
	return str(current_station().get("name", "?"))


func is_tour_active() -> bool:
	return _tour_active


## 超时宽限计时（39 号 §3.1 第 3 项）：本站停留 +15s 无交互置 _timeout_pending，
## 提示「我们继续」；实际推进等句末再推（不打断口播，句末判定待实机）。
func _process(delta: float) -> void:
	if not _tour_active or _timeout_pending:
		return
	_station_timer += delta
	var stay: float = float(current_station().get("stay_sec", 0.0))
	if stay > 0.0 and _station_timer > stay + TIMEOUT_GRACE_SEC:
		_timeout_pending = true
		_set_hud("馆长路线：我们继续（等句末推进）")


## 站内讲解（F-9 联动）：厅站经 NarrPlayer.play_hall_narr 复用单口播互斥通道；
## 非厅站（door/wall/pedia/exit_）讲解轨 id 待 40 号总表定案，此处只留接线注释不臆造。
func _notify_station_narr() -> void:
	var station: String = str(current_station().get("station", ""))
	if not STATION_LAYOUT.has(station):
		return
	var narr := get_node_or_null("/root/Main/NarrPlayer")
	if narr != null and narr.has_method("play_hall_narr"):
		@warning_ignore("unsafe_method_access")
		narr.play_hall_narr(str(STATION_LAYOUT[station]))


func _set_hud(text: String) -> void:
	if _hud_label != null:
		_hud_label.text = text
