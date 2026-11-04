# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
extends Node
## 模拟器网关 TCP 客户端（M0 原型）。
##
## 连接 127.0.0.1:7331 的网关（先运行 `python gw/gateway.py`），自动启动 fake
## 后端，把帧投放到 Main/Room/Screen 墙壁屏幕上；空格键注入一次键盘输入事件。
## 协议见 repo/gw/PROTOCOL.md。

const HOST := "127.0.0.1"
const PORT := 7331
const DEVICE_ID := "demo"

var _tcp := StreamPeerTCP.new()
var _recv_buf := ""
var _screen_tex := ImageTexture.new()
var _screen_mat := StandardMaterial3D.new()
var _start_sent := false
var _started := false
var _space_held := false
var _msg_count := 0
var _frame_parts := {}  # frame_id -> {total, seqs:{seq:data_b64}, meta}（frame_chunk 重组缓冲）

var _status_label: Label
var _info_label: Label


func _ready() -> void:
	_build_hud()
	var screen := get_node_or_null("/root/Main/Room/Screen") as MeshInstance3D
	if screen != null:
		_screen_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		screen.material_override = _screen_mat
		# 初始黑屏占位（与 fake 后端默认 320x240 一致）
		var img := Image.create(320, 240, false, Image.FORMAT_RGB8)
		img.fill(Color(0.02, 0.02, 0.03))
		_screen_tex = ImageTexture.create_from_image(img)
		_screen_mat.albedo_texture = _screen_tex
	_set_status("未连接")
	_tcp.connect_to_host(HOST, PORT)


func _build_hud() -> void:
	var hud := get_node_or_null("/root/Main/HUD") as CanvasLayer
	if hud == null:
		return
	_status_label = Label.new()
	_status_label.position = Vector2(16, 16)
	hud.add_child(_status_label)
	_info_label = Label.new()
	_info_label.anchor_top = 1.0
	_info_label.anchor_bottom = 1.0
	_info_label.offset_top = -40.0
	_info_label.offset_bottom = -16.0
	hud.add_child(_info_label)


func _set_status(text: String) -> void:
	if _status_label != null:
		_status_label.text = "[网关] " + text


func _set_info(text: String) -> void:
	if _info_label != null:
		_info_label.text = text


func _reconnect() -> void:
	_tcp = StreamPeerTCP.new()
	_tcp.connect_to_host(HOST, PORT)
	_start_sent = false
	_started = false
	_recv_buf = ""
	_set_status("重连中…")


func _send(obj: Dictionary) -> void:
	if _tcp.get_status() != StreamPeerTCP.STATUS_CONNECTED:
		return
	_tcp.put_data((JSON.stringify(obj) + "\n").to_utf8_buffer())


func _process(_delta: float) -> void:
	var status := _tcp.get_status()
	match status:
		StreamPeerTCP.STATUS_CONNECTED:
			if not _start_sent:
				_start_sent = true
				_send({
					"type": "start_device",
					"emulator": "fake",
					"device_id": DEVICE_ID,
					"config": {"width": 320, "height": 240, "fps": 24},
				})
				_set_status("已连接，正在启动 fake…")
			_poll()
		StreamPeerTCP.STATUS_ERROR:
			_set_status("连接失败：请先运行 python gw/gateway.py（端口 %d），按 R 重连" % PORT)
		StreamPeerTCP.STATUS_NONE:
			_set_status("连接中…（网关未启动？按 R 重连）")
	# 演示输入注入：空格发送一次键盘事件
	var space_now := Input.is_physical_key_pressed(KEY_SPACE)
	if space_now and not _space_held and _started \
			and status == StreamPeerTCP.STATUS_CONNECTED:
		_send({"type": "input_event", "device_id": DEVICE_ID,
			   "map": "keyboard", "key": "space", "value": true})
	_space_held = space_now
	if Input.is_physical_key_pressed(KEY_R) \
			and status != StreamPeerTCP.STATUS_CONNECTED:
		_reconnect()


func _poll() -> void:
	var avail := _tcp.get_available_bytes()
	while avail > 0:
		var res := _tcp.get_data(avail)
		if res[0] != OK:
			break
		_recv_buf += res[1].get_string_from_utf8()
		avail = _tcp.get_available_bytes()
	_parse_lines()


func _parse_lines() -> void:
	while true:
		var idx := _recv_buf.find("\n")
		if idx < 0:
			break
		var line := _recv_buf.substr(0, idx)
		_recv_buf = _recv_buf.substr(idx + 1)
		if line.strip_edges() != "":
			_handle_line(line)


func _handle_line(line: String) -> void:
	var data = JSON.parse_string(line)
	if typeof(data) != TYPE_DICTIONARY:
		return
	_msg_count += 1
	match str(data.get("type")):
		"start_device_ack":
			_started = true
			_set_status("fake 已启动：%s" % str(data.get("info")))
		"frame_ready":
			_apply_frame(int(data.get("frame_id", 0)), int(data.get("width", 0)),
						int(data.get("height", 0)), str(data.get("data_b64", "")))
		"frame_chunk":
			_apply_chunk(data)
		"light_state":
			_set_info("[light_state] %s=%s（消息计数 %d，R=重连）"
					% [str(data.get("sink", "?")), str(data.get("on", false)), _msg_count])
		"audio_chunk":
			pass  # M0 暂不接放音，音频通道验证由 scripts/m0_check.py 承担
		"status", "stopped", "error", "input_ack":
			_set_info("[%s] %s（消息计数 %d，R=重连）"
					% [str(data.get("type")), str(data.get("message", data.get("state", data.get("code", "")))), _msg_count])
		_:
			_set_info("消息计数 %d（R=重连）" % _msg_count)


func _apply_frame(fid: int, w: int, h: int, b64: String) -> void:
	if w <= 0 or h <= 0 or fid < 1:
		return
	var raw := Marshalls.base64_to_raw(b64)
	# RGB8 每像素 3 字节，长度不匹配说明协议帧损坏，直接丢弃（有超时与日志兜底）
	if raw.size() != w * h * 3:
		_set_info("帧长度不符：%dx%d 但收到 %d 字节" % [w, h, raw.size()])
		return
	var img := Image.create_from_data(w, h, false, Image.FORMAT_RGB8, raw)
	_screen_tex.update(img)
	_set_info("frame_id=%d  %dx%d（消息计数 %d，R=重连）" % [fid, w, h, _msg_count])


func _apply_chunk(data: Dictionary) -> void:
	# 协议 v2 frame_chunk 重组（见 gw/PROTOCOL.md §10.2）；codec=rle 暂未在
	# Godot 侧实现（当前客户端默认请求 raw，rle 解码留给后续迭代）。
	var fid := int(data.get("frame_id", 0))
	var total := int(data.get("total", 1))
	var seq := int(data.get("seq", 0))
	if not _frame_parts.has(fid):
		_frame_parts[fid] = {"total": total, "seqs": {}, "meta": data}
	var bucket: Dictionary = _frame_parts[fid]
	if bucket["seqs"].has(seq):
		return  # 重复分片丢弃
	bucket["seqs"][seq] = str(data.get("data_b64", ""))
	bucket["meta"] = data
	if bucket["seqs"].size() >= int(bucket["total"]):
		_frame_parts.erase(fid)
		var joined := ""
		for i in range(int(bucket["total"])):
			joined += str(bucket["seqs"][i])
		_apply_frame(fid, int(bucket["meta"].get("width", 0)),
					int(bucket["meta"].get("height", 0)), joined)