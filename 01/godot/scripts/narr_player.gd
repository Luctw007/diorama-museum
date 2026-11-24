# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
extends Node
## 占位口播轨播放器（TASK-116，引擎侧 · 对应 04 线 44 号 G-9）：
## 把两条占位口播轨（narr 系，04 线 20 号规格）接起来播放，验证"单口播互斥"。
##
## 语义（20 号规格 narr 系 · 单口播互斥）：
## - play_narr(id)：播新停旧——同一时刻只有一个口播在播；
## - stop_narr()：停止当前口播；
## - HUD 显示当前口播 id 与状态（playing/stopped/fallback）。
## 正式解说轨由 04 线配音/TTS 流程产出后替换（本任务只用占位轨，不下载真实素材）。

const NARR_PATHS := {
	"narr_hall_intro": "res://content/audio/demo/narr_hall_intro_placeholder.wav",
	"narr_eniac": "res://content/audio/demo/narr_eniac_placeholder.wav",
}
const FALLBACK_NARR := "narr_hall_intro"

## F-9（TASK-271-A）：四厅导览台本挂接表——layout 文件 → 口播 id 序列（占位轨，116 口径）。
## F-9 深化（TASK-291-C）：由单条扩为**每厅序列**——按四厅台本条目顺序静态挂接
## （16 号 8 站 / 22 号 7 站 / 27 号 8 站 / 41 号 9 站）；条目 id 未定案处标
## [待定案:xxx] 不臆造，播放推进时跳过并 HUD 提示。
## 数据源（只读引用，不落地 01）：04 线 16_黎明厅导览台本_v2 / 22_大型机厅 / 27_个人机厅 /
## 41_游戏机厅（D:/work/04/repo/docs/design/）；正式解说轨由 04 线配音/TTS 产出后替换占位轨。
const HALL_NARR_IDS := {
	"exhibit_dawn.json": [
		"narr_hall_intro", "narr_eniac",
		"[待定案:edvac]", "[待定案:edsac]", "[待定案:baby]",
		"[待定案:crt_room]", "[待定案:exit]",
	],
	"exhibit_mainframe.json": [
		"narr_hall_intro", "[待定案:s360]", "[待定案:pdp8]",
		"[待定案:pdp11]", "[待定案:vax]", "[待定案:exit]",
	],
	"exhibit_personal.json": [
		"narr_hall_intro", "[待定案:year_wall]", "[待定案:c64]",
		"[待定案:apple2]", "[待定案:5150]", "[待定案:bbc]",
		"[待定案:compare]", "[待定案:exit]",
	],
	"exhibit_console.json": [
		"narr_hall_intro", "[待定案:odyssey]", "[待定案:2600]",
		"[待定案:fc]", "[待定案:md]", "[待定案:sfc]",
		"[待定案:mvs]", "[待定案:gb]", "[待定案:gw]",
		"[待定案:exit]",
	],
	"exhibit_hub.json": ["narr_hall_intro"],
}

var _player: AudioStreamPlayer
var _current := ""        # 当前口播 id（空=无）
var _hud_label: Label
## F-9 深化（TASK-291-C）：当前厅序列与游标（切厅重置；逐条推进状态）。
var _hall_seq: Array = []
var _seq_index := 0


func _ready() -> void:
	_player = AudioStreamPlayer.new()
	add_child(_player)
	# F-9 深化：当前条真实播完 → 推进下一条（.finished 为引擎内置信号，点号连接不经字符串池）
	_player.finished.connect(_on_finished)
	var hud := get_node_or_null("/root/Main/HUD") as CanvasLayer
	if hud != null:
		_hud_label = Label.new()
		_hud_label.position = Vector2(16, 240)
		_hud_label.add_theme_font_size_override("font_size", 13)
		hud.add_child(_hud_label)
	_set_hud("口播：空闲")


## 播放口播 id；切换时停旧播新（单口播互斥）。未知 id 降级到 FALLBACK_NARR。
func play_narr(narr_id: String) -> void:
	if not NARR_PATHS.has(narr_id):
		narr_id = FALLBACK_NARR
		_set_hud("口播：未知 id → 降级 %s" % narr_id)
	if _current == narr_id and _player.playing:
		return   # 同一口播已在播：不重启（互斥语义下的幂等）
	stop_narr()
	var stream: AudioStream = load(NARR_PATHS[narr_id]) as AudioStream
	if stream == null:
		_current = ""
		_set_hud("口播：FAIL 无法加载 %s" % narr_id)
		return
	_current = narr_id
	_player.stream = stream
	_player.play()
	_set_hud("口播：%s（playing）" % narr_id)


func stop_narr() -> void:
	if _player != null and _player.playing:
		_player.stop()
	if _current != "":
		_set_hud("口播：%s（stopped）" % _current)
		_current = ""


## F-9（TASK-271-A）：切厅后播本厅导览口播——单口播互斥（停旧播新，同一时刻仅一条；
## 切换厅打断旧口播由 play_narr 的 stop_narr 语义保证）。未知厅降级 FALLBACK_NARR。
## F-9 深化（TASK-291-C）：切厅重置序列游标并从首条起逐条推进（占位轨沿用 116）。
func play_hall_narr(layout_file: String) -> void:
	var ids: Array = HALL_NARR_IDS.get(layout_file, [])
	if ids.is_empty():
		play_narr(FALLBACK_NARR)
		return
	_hall_seq = ids
	_seq_index = 0
	_play_seq_current()


## F-9 深化（TASK-291-C）：播当前游标条目——[待定案] 条目跳过不播（不臆造 id），
## 播到序列末尾提示收束。play_narr 的互斥/降级语义不变。
func _play_seq_current() -> void:
	while _seq_index < _hall_seq.size():
		var narr_id: String = str(_hall_seq[_seq_index])
		if narr_id.begins_with("[待定案"):
			_set_hud("口播：%s 条目未定案，跳过" % narr_id)
			_seq_index += 1
			continue
		play_narr(narr_id)
		return
	_set_hud("口播：本厅序列播完")


## F-9 深化（TASK-291-C）：推进序列下一条（导览同步/调试手动调用）；
## 自动推进由 _player.finished → _on_finished 驱动。
func advance_narr() -> void:
	if _seq_index + 1 >= _hall_seq.size():
		_set_hud("口播：序列末尾")
		return
	_seq_index += 1
	_play_seq_current()


## F-9 深化：占位轨真实播完 → 推进下一条（若序列未到末尾）。
func _on_finished() -> void:
	if _seq_index + 1 < _hall_seq.size():
		advance_narr()


func current_narr() -> String:
	return _current


func _set_hud(text: String) -> void:
	if _hud_label != null:
		_hud_label.text = text