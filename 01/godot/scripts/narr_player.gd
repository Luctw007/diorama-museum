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

var _player: AudioStreamPlayer
var _current := ""        # 当前口播 id（空=无）
var _hud_label: Label


func _ready() -> void:
	_player = AudioStreamPlayer.new()
	add_child(_player)
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


func current_narr() -> String:
	return _current


func _set_hud(text: String) -> void:
	if _hud_label != null:
		_hud_label.text = text