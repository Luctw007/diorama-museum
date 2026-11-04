# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""模拟器网关主进程（v2）。

职责（设计文档 ADR D1、§5.4，TASK-06）：
1. 以独立子进程启动模拟器后端（进程隔离，stdio 上走 JSON lines 协议）；
2. TCP（默认 127.0.0.1:7331）控制通道，多客户端并发，事件广播；
3. 生命周期管理：启动超时、崩溃上报、停止兜底（terminate → kill）；
4. v2 新增：
   - 帧压缩与分片：frame_codec raw|rle 透传；大帧/强制分片走 frame_chunk；
   - 崩溃自动重启 + 快照恢复（FR-E8）：config.auto_restart（默认开），
     崩溃后重启后端并 load "__auto" 快照（快照由后端持久化到 persist_path）；
     "连续 3 次失败重启" → degraded + error(RESTART_EXCEEDED)；
   - 多设备并发（每设备独立子进程与状态机）；
   - Sink 多输出路：frame_ready 带 sink，light_state 透传。

协议：gw/PROTOCOL.md（v2，向下兼容 v1）。日志全部写入 stderr。
运行：python gw/gateway.py [--host 127.0.0.1] [--port 7331]
"""

from __future__ import annotations

import argparse
import json
import math
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:  # 允许以 `python gw/gateway.py` 直接运行
    sys.path.insert(0, REPO_ROOT)

# 常量
START_TIMEOUT = 8.0        # 等待后端进入 running 的超时（秒）
STOP_TIMEOUT = 5.0         # 等待后端自行退出的超时（秒）
KILL_GRACE = 2.0           # terminate 后到 kill 的宽限（秒）
MAX_LINE_CHARS = 512_000   # 单条 JSON 行超过该长度才触发分片
DEFAULT_CHUNK_CHARS = 300_000  # 每片 data_b64 的最大字符数（默认）
FAIL_WINDOW = 5.0          # 重启"快速再崩"判定窗口（秒）
MAX_RESTART_FAILURES = 3   # 连续失败重启上限 → degraded

# 已注册模拟器。真实模拟器接入时只需在此登记并新增一个后端模块。
EMULATORS: dict[str, dict[str, Any]] = {
    "fake": {
        "desc": "测试用假模拟器：彩条帧 + 正弦波音频 + rle/分片/崩溃注入（协议回归参考实现）",
        "module": "gw.emulators.fake_emulator",
        "license": "MIT（本仓库自带）",
    },
    "simh-pdp8": {
        "desc": "SIMH PDP-8（需用户提供 SIMH 二进制，见 licenses/SIMH.md）",
        "license": "SIMH 许可（需核实，见 licenses/SIMH.md）",
        "binary_env": "SIMH_PDP8_BIN",
        "binary_hint": os.path.join("third_party", "simh", "pdp8"),
        # 无 module：后端模块未实现（预留槽位）——start 时网关注销报 EMULATOR_BACKEND_MISSING
    },
    "mame-apple2": {
        "desc": "MAME apple2 驱动骨架（需用户提供 MAME 二进制，见 licenses/MAME.md 与 05 线 13_MAME接入预研.md）",
        "license": "MAME 上游 GPLv2+/BSD-3-Clause 双许可（版本需核实，见 licenses/MAME.md）",
        "module": "gw.emulators.mame_apple2",
        "binary_env": "MAME_BIN",
        "binary_hint": os.path.join("third_party", "mame", "mame"),
        "keymap": "keys/keymap_apple2.json",
    },
}


def _find_binary(entry: dict[str, Any]) -> Optional[str]:
    """通用二进制定位（TASK-46A）：环境变量优先，其次 binary_hint 相对 REPO_ROOT（含 .exe 变体）。"""
    env_name = entry.get("binary_env")
    if env_name:
        env_path = os.environ.get(env_name)
        if env_path and os.path.isfile(env_path):
            return env_path
    hint = entry.get("binary_hint")
    if not hint:
        return None
    base = hint if os.path.isabs(hint) else os.path.join(REPO_ROOT, hint)
    for cand in (base, base + ".exe"):
        if os.path.isfile(cand):
            return cand
    return None


def _binary_ok(emulator: str) -> bool:
    """该模拟器是否需要外部二进制；需要时校验存在。无 binary_hint 的条目（fake/native）恒可。"""
    entry = EMULATORS.get(emulator) or {}
    if not entry.get("binary_hint"):
        return True
    return _find_binary(entry) is not None


class Device:
    """一个设备实例（一次模拟器运行，可因崩溃重启而更换子进程）的句柄。"""

    def __init__(self, device_id: str, emulator: str, config: dict[str, Any]) -> None:
        self.device_id = device_id
        self.emulator = emulator
        # 注入快照持久化路径（后端据此跨进程保存 saves；网关注入前用户 config 不变）
        config.setdefault("persist_path",
                          os.path.join(tempfile.gettempdir(),
                                       "diorama_%s.json" % device_id))
        self.config = config
        self.proc: Optional[subprocess.Popen] = None
        self.state = "starting"
        self.stopped_intentionally = False
        self.stop_reported = False
        self.returncode: Optional[int] = None
        # v2 自动重启记账
        self.generation = 0          # 子进程代际（防御旧读线程的过期消息）
        self.restart_time = 0.0      # 最近一次重启后进入 running 的时刻
        self.restart_failures = 0    # 连续失败重启计数
        self.last_cmd_time = 0.0     # 最近一次客户端命令时间（判定"窗口内无命令"）

    @property
    def is_active(self) -> bool:
        return self.state in ("starting", "running", "stopping")


class Gateway:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.devices: dict[str, Device] = {}
        self.clients: set[object] = set()
        self._lock = threading.RLock()
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._srv.bind((host, port))
        self._srv.listen(8)
        self._srv.settimeout(1.0)
        self._shutdown = False
        self.log("网关 v2 已监听 %s:%d（repo: %s）" % (host, port, REPO_ROOT))

    # ---------------------------------------------------------------- 工具
    def log(self, message: str) -> None:
        print("[gw] %s" % message, file=sys.stderr, flush=True)

    def send(self, client: Any, msg: dict[str, Any]) -> None:
        msg.setdefault("proto", 2)
        self._send_line(client, json.dumps(msg, ensure_ascii=False) + "\n")

    def _send_line(self, client: Any, line: str) -> None:
        try:
            client.sendall(line.encode("utf-8"))
        except OSError:
            self._drop_client(client)

    def _broadcast_line(self, line: str) -> None:
        with self._lock:
            clients = list(self.clients)
        for client in clients:
            self._send_line(client, line)

    def broadcast(self, msg: dict[str, Any]) -> None:
        """广播一条事件；frame_ready 超长或设备配置强制分片时改为 frame_chunk 序列。"""
        msg.setdefault("proto", 2)
        if msg.get("type") == "frame_ready":
            line = json.dumps(msg, ensure_ascii=False) + "\n"
            with self._lock:
                dev = self.devices.get(msg.get("device_id"))
            force = bool(dev.config.get("force_chunk")) if dev else False
            chars = int(dev.config.get("force_chunk_chars") or DEFAULT_CHUNK_CHARS) \
                if dev else DEFAULT_CHUNK_CHARS
            if force or len(line) > MAX_LINE_CHARS:
                self._broadcast_frame_chunks(msg, chars)
                return
            self._broadcast_line(line)
            return
        self._broadcast_line(json.dumps(msg, ensure_ascii=False) + "\n")

    def _broadcast_frame_chunks(self, msg: dict[str, Any], chars: int) -> None:
        """把 frame_ready 拆为 frame_chunk 序列（data_b64 按序切分，拼接还原）。"""
        data = msg.get("data_b64", "")
        total = math.ceil(len(data) / max(chars, 1)) if data else 1
        for seq in range(total):
            piece = data[seq * chars:(seq + 1) * chars]
            chunk = {k: v for k, v in msg.items() if k != "data_b64"}
            chunk["type"] = "frame_chunk"
            chunk["seq"] = seq
            chunk["total"] = total
            chunk["data_b64"] = piece
            self._broadcast_line(json.dumps(chunk, ensure_ascii=False) + "\n")

    def _drop_client(self, client: Any) -> None:
        with self._lock:
            self.clients.discard(client)
        try:
            client.close()
        except OSError:
            pass

    def reply_error(self, client: Any, code: str, message: str,
                    device_id: Optional[str] = None) -> None:
        self.send(client, {"type": "error", "code": code, "message": message,
                           "device_id": device_id})

    # ---------------------------------------------------------------- 进程管理
    def _spawn(self, device: Device) -> None:
        entry = EMULATORS[device.emulator]
        if not entry.get("module"):
            raise RuntimeError("EMULATOR_BACKEND_MISSING")
        if not _binary_ok(device.emulator):
            raise RuntimeError("EMULATOR_BINARY_MISSING")
        env = dict(os.environ)
        env["PYTHONPATH"] = REPO_ROOT + os.pathsep + env.get("PYTHONPATH", "")
        kwargs: dict[str, Any] = dict(
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, encoding="utf-8", errors="replace",
            cwd=REPO_ROOT, env=env,
        )
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        device.proc = subprocess.Popen(
            [sys.executable, "-m", entry["module"]], **kwargs)

    def _attach(self, device: Device) -> None:
        """为新子进程挂读/监视线程（线程内以 proc 快照工作，防止过期消息串代）。"""
        proc = device.proc
        assert proc is not None
        threading.Thread(target=self._backend_reader, args=(device, proc),
                         daemon=True).start()
        threading.Thread(target=self._monitor, args=(device, proc),
                         daemon=True).start()
        if proc.stderr is not None:
            threading.Thread(target=self._pump_stderr, args=(device, proc),
                             daemon=True).start()

    def _backend_reader(self, device: Device, proc: Any) -> None:
        for raw in proc.stdout:  # type: ignore[union-attr]
            line = raw.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                self.log("[%s] 后端发来无法解析的行: %.80s" % (device.device_id, line))
                continue
            self._route_backend(device, msg)

    def _route_backend(self, device: Device, msg: dict[str, Any]) -> None:
        mt = msg.get("type")
        did = device.device_id
        if mt == "state":
            state = msg.get("state")
            with self._lock:
                if state == "running" and device.state == "starting":
                    device.state = "running"
                elif state == "stopped":
                    device.stopped_intentionally = True
            self.broadcast({"type": "status", "device_id": did, "state": state,
                            "message": msg.get("message")})
            if state == "stopped":
                self._report_stopped(device, "user", ok=True)
        elif mt == "frame":
            self.broadcast({"type": "frame_ready", "device_id": did,
                            "frame_id": msg.get("frame_id"),
                            "width": msg.get("width"), "height": msg.get("height"),
                            "format": msg.get("format", "rgb8"),
                            "codec": msg.get("codec", "raw"),
                            "sink": msg.get("sink", "main"),
                            "data_b64": msg.get("data_b64"), "ts": msg.get("ts")})
        elif mt == "audio":
            self.broadcast({"type": "audio_chunk", "device_id": did,
                            "seq": msg.get("seq"),
                            "sample_rate": msg.get("sample_rate"),
                            "channels": msg.get("channels", 1),
                            "format": msg.get("format", "s16le"),
                            "sink": msg.get("sink", "speaker"),
                            "data_b64": msg.get("data_b64")})
        elif mt == "light_state":
            self.broadcast({"type": "light_state", "device_id": did,
                            "sink": msg.get("sink"), "on": msg.get("on"),
                            "ts": msg.get("ts")})
        elif mt == "input_ack":
            self.broadcast({"type": "input_ack", "device_id": did,
                            "map": msg.get("map"), "key": msg.get("key"),
                            "value": msg.get("value")})
        elif mt == "ack":
            op = msg.get("op")
            if op in ("save_state", "load_state"):
                # __auto 是网关内部快照（用户保存时同步写），其 ack 不回传客户端
                if op == "save_state" and msg.get("id") == "__auto":
                    self.log("[%s] 内部快照 __auto 已更新（frame %s）"
                             % (did, msg.get("frame_id")))
                    return
                self.broadcast({"type": op + "_ack", "device_id": did,
                                "id": msg.get("id"),
                                "frame_id": msg.get("frame_id"),
                                "ok": msg.get("ok", True)})
        elif mt == "error":
            # __auto 恢复时快照不存在属正常（首启崩溃），只记日志不透传
            if msg.get("code") == "NOT_FOUND" and msg.get("id") == "__auto":
                self.log("[%s] 无 __auto 快照可恢复（跳过）" % did)
                return
            self.broadcast({"type": "error", "code": msg.get("code"),
                            "message": msg.get("message"), "device_id": did})
        else:
            self.log("[%s] 忽略后端未知消息类型: %r" % (did, mt))

    def _monitor(self, device: Device, proc: Any) -> None:
        """等待后端退出；非主动停止且退出码非 0 → 走崩溃处理。"""
        code = proc.wait()
        if device.proc is not proc:
            return  # 已被新一代子进程替换，旧代事件作废
        device.returncode = code
        if (not device.stopped_intentionally) and code != 0:
            self._handle_crash(device, code)
        else:
            with self._lock:
                if device.state != "stopped" and device.state != "degraded":
                    device.state = "stopped"
            self.log("[%s] 后端退出，退出码 %d" % (device.device_id, code))

    def _handle_crash(self, device: Device, code: int) -> None:
        """崩溃处理：上报；按 auto_restart 策略自动重启 + 快照恢复，或降级。"""
        now = time.time()
        with self._lock:
            # "失败重启"：重启成功进入 running 后 FAIL_WINDOW 秒内再次崩溃，
            # 且期间无任何客户端命令（命令时间戳不晚于重启时刻）。
            is_failure = (device.restart_time > 0.0
                          and (now - device.restart_time) <= FAIL_WINDOW
                          and device.last_cmd_time <= device.restart_time)
            if is_failure:
                device.restart_failures += 1
            else:
                device.restart_failures = 0
            device.state = "crashed"
            failures = device.restart_failures
        self.broadcast({"type": "error", "code": "PROCESS_CRASHED",
                        "message": "后端进程异常退出，退出码 %d（失败重启 %d/%d）"
                        % (code, failures, MAX_RESTART_FAILURES),
                        "device_id": device.device_id})
        self.broadcast({"type": "status", "device_id": device.device_id,
                        "state": "crashed"})
        self.log("[%s] 后端崩溃，退出码 %d" % (device.device_id, code))

        if is_failure and failures >= MAX_RESTART_FAILURES:
            with self._lock:
                device.state = "degraded"
            self.broadcast({"type": "error", "code": "RESTART_EXCEEDED",
                            "message": "连续 %d 次失败重启，设备降级为 degraded"
                            % MAX_RESTART_FAILURES,
                            "device_id": device.device_id})
            self.broadcast({"type": "status", "device_id": device.device_id,
                            "state": "degraded"})
            self.log("[%s] 重启失败次数达上限，降级 degraded" % device.device_id)
            return
        if device.config.get("auto_restart") is False:
            self.log("[%s] auto_restart=false，保持 crashed 态" % device.device_id)
            return
        threading.Thread(target=self._do_restart, args=(device,),
                         daemon=True).start()

    def _do_restart(self, device: Device) -> None:
        """自动重启：换新子进程 → start → running → load __auto 恢复。"""
        with self._lock:
            device.generation += 1
            device.proc = None
            device.state = "starting"
        self.log("[%s] 自动重启（第 %d 代）" % (device.device_id, device.generation))
        self.broadcast({"type": "status", "device_id": device.device_id,
                        "state": "restarting"})
        try:
            self._spawn(device)
        except OSError as exc:
            self.log("[%s] 重启 spawn 失败: %s" % (device.device_id, exc))
            self._report_stopped(device, "error", ok=False)
            return
        except RuntimeError:
            self._report_stopped(device, "error", ok=False)
            return
        self._attach(device)
        try:
            self._write_to_backend(device, {"type": "start",
                                            "device_id": device.device_id,
                                            "config": device.config})
        except OSError as exc:
            self.log("[%s] 重启下发 start 失败: %s" % (device.device_id, exc))
            self._report_stopped(device, "error", ok=False)
            return
        deadline = time.time() + START_TIMEOUT
        while True:
            state = device.state
            if state == "running":
                break
            if state in ("crashed", "degraded", "stopped"):
                return  # 崩溃处理线程接管（启动阶段即崩 → 再次走崩溃流程）
            if time.time() > deadline:
                self._kill_process(device)
                self._report_stopped(device, "timeout", ok=False)
                self.log("[%s] 重启等待 running 超时" % device.device_id)
                return
            time.sleep(0.02)
        with self._lock:
            device.restart_time = time.time()
            device.last_cmd_time = device.restart_time  # 基线：此后无命令才计失败
        self.log("[%s] 自动重启成功，恢复 __auto 快照" % device.device_id)
        try:
            self._write_to_backend(device, {"type": "load_state", "id": "__auto"})
        except OSError:
            self.log("[%s] 下发 load __auto 失败（忽略）" % device.device_id)

    def _report_stopped(self, device: Device, reason: str, ok: bool) -> None:
        if device.stop_reported:
            return
        device.stop_reported = True
        with self._lock:
            if device.state not in ("crashed",):
                device.state = "stopped"
        self.broadcast({"type": "stopped", "device_id": device.device_id,
                        "ok": ok, "reason": reason})

    # ---------------------------------------------------------------- 命令处理
    def handle_msg(self, client: Any, msg: dict[str, Any]) -> None:
        mt = msg.get("type")
        if mt == "heartbeat":
            with self._lock:
                running = {d: dev.state for d, dev in self.devices.items()
                           if dev.state != "stopped"}
            self.send(client, {"type": "heartbeat_ack", "running_devices": running})
        elif mt == "list_emulators":
            listing = {}
            for name, entry in EMULATORS.items():
                listing[name] = {"desc": entry["desc"],
                                 "license": entry["license"],
                                 "available": _binary_ok(name)}
            self.send(client, {"type": "list_emulators_ack", "emulators": listing})
        elif mt == "start_device":
            self.cmd_start_device(client, msg)
        elif mt == "input_event":
            self.cmd_to_device(client, msg, "input_event")
        elif mt == "save_state":
            self.cmd_to_device(client, msg, "save_state")
        elif mt == "load_state":
            self.cmd_to_device(client, msg, "load_state")
        elif mt == "stop":
            self.cmd_to_device(client, msg, "stop")
        else:
            self.reply_error(client, "UNSUPPORTED", "不支持的消息类型: %r" % mt)

    def cmd_start_device(self, client: Any, msg: dict[str, Any]) -> None:
        emulator = msg.get("emulator")
        device_id = msg.get("device_id")
        config = dict(msg.get("config") or {})
        if emulator and emulator in EMULATORS:
            # 机种键码表三级回退的第 1 级默认值：网关注册表注入（客户端可覆盖）
            default_keymap = EMULATORS[emulator].get("keymap")
            if default_keymap and "keymap" not in config:
                config["keymap"] = default_keymap
        if not emulator or not device_id:
            self.reply_error(client, "INVALID_MESSAGE",
                             "start_device 缺少 emulator 或 device_id")
            return
        with self._lock:
            existing = self.devices.get(device_id)
            if existing and (existing.is_active or existing.state == "degraded"):
                self.reply_error(client, "ALREADY_RUNNING",
                                 "设备已存在实例: %s（状态 %s）"
                                 % (device_id, existing.state), device_id)
                return
        if emulator not in EMULATORS:
            self.reply_error(client, "EMULATOR_NOT_FOUND",
                             "未注册的模拟器: %s（已注册: %s）"
                             % (emulator, ", ".join(EMULATORS)), device_id)
            return
        if not _binary_ok(emulator):
            self.reply_error(
                client, "EMULATOR_BINARY_MISSING",
                "模拟器二进制未找到：请安装到 %s 或设置环境变量 %s"
                % (EMULATORS[emulator].get("binary_hint", "?"),
                   EMULATORS[emulator].get("binary_env", "?")), device_id)
            return

        device = Device(device_id, emulator, config)
        cfg = device.config
        with self._lock:
            self.devices[device_id] = device
        try:
            self._spawn(device)
        except OSError as exc:
            self._report_stopped(device, "error", ok=False)
            self.reply_error(client, "INTERNAL", "启动后端进程失败: %s" % exc, device_id)
            return
        except RuntimeError as exc:
            self._report_stopped(device, "error", ok=False)
            if str(exc) == "EMULATOR_BACKEND_MISSING":
                self.reply_error(client, "EMULATOR_BACKEND_MISSING",
                                 "模拟器已登记但后端模块未实现（预留槽位）: %s"
                                 % emulator, device_id)
            else:
                self.reply_error(client, "EMULATOR_BINARY_MISSING",
                                 "模拟器二进制缺失", device_id)
            return
        self._attach(device)
        start_msg = {"type": "start", "device_id": device_id, "config": cfg}
        try:
            self._write_to_backend(device, start_msg)
        except OSError as exc:
            self._report_stopped(device, "error", ok=False)
            self.reply_error(client, "INTERNAL", "下发 start 失败: %s" % exc, device_id)
            return
        deadline = time.time() + START_TIMEOUT
        while device.state != "running":
            if device.state in ("crashed", "stopped", "degraded"):
                self.reply_error(client, "INTERNAL",
                                 "后端在启动阶段退出（退出码 %s）" % device.returncode,
                                 device_id)
                return
            if time.time() > deadline:
                self._kill_process(device)
                self._report_stopped(device, "timeout", ok=False)
                self.reply_error(client, "TIMEOUT",
                                 "后端 %ds 内未进入 running" % int(START_TIMEOUT),
                                 device_id)
                return
            time.sleep(0.02)
        with self._lock:
            device.last_cmd_time = time.time()
        self.send(client, {"type": "start_device_ack", "device_id": device_id,
                           "ok": True, "emulator": emulator,
                           "info": {
                               "width": cfg.get("width"),
                               "height": cfg.get("height"),
                               "fps": cfg.get("fps"),
                               "frame_codec": cfg.get("frame_codec", "raw"),
                               "sinks": cfg.get("sinks", ["main"]),
                               "auto_restart": cfg.get("auto_restart", True),
                           }})
        self.broadcast({"type": "status", "device_id": device_id, "state": "running"})
        # 建立基线快照 __auto（供崩溃自动恢复）
        try:
            self._write_to_backend(device, {"type": "save_state", "id": "__auto"})
        except OSError:
            self.log("[%s] 写入 __auto 基线失败（忽略）" % device_id)

    def cmd_to_device(self, client: Any, msg: dict[str, Any], cmd: str) -> None:
        device_id = msg.get("device_id")
        with self._lock:
            device = self.devices.get(device_id)
        if device is None:
            self.reply_error(client, "NOT_RUNNING", "设备不存在: %s" % device_id,
                             device_id)
            return
        with self._lock:
            device.last_cmd_time = time.time()  # 任何命令都刷新"失败重启"窗口基线
        # degraded/crashed 终态允许 stop 清理（后端进程已死）
        if cmd == "stop" and device.state in ("degraded", "crashed"):
            self._report_stopped(device, "user", ok=True)
            return
        if device.state != "running":
            self.reply_error(client, "NOT_RUNNING",
                             "设备 %s 当前状态: %s" % (device_id, device.state),
                             device_id)
            return
        if cmd == "input_event":
            outgoing = {"type": "input", "map": msg.get("map", "keyboard"),
                        "key": msg.get("key"), "value": msg.get("value")}
        elif cmd in ("save_state", "load_state"):
            outgoing = {"type": cmd, "id": str(msg.get("id", "s"))}
        else:  # stop
            outgoing = {"type": "stop"}
        try:
            if cmd == "stop":
                device.stopped_intentionally = True
            self._write_to_backend(device, outgoing)
            # 用户快照同步写 __auto（崩溃恢复用）
            if cmd == "save_state":
                self._write_to_backend(device, {"type": "save_state", "id": "__auto"})
        except (OSError, ValueError) as exc:
            self.reply_error(client, "INTERNAL", "下发 %s 失败: %s" % (cmd, exc),
                             device_id)
            return
        if cmd == "stop":
            threading.Thread(target=self._stop_watchdog, args=(device,),
                             daemon=True).start()

    # ---------------------------------------------------------------- 进程 IO
    def _write_to_backend(self, device: Device, msg: dict[str, Any]) -> None:
        proc = device.proc
        if proc is None or proc.stdin is None or proc.poll() is not None:
            raise OSError("后端进程不可写")
        proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        proc.stdin.flush()

    def _pump_stderr(self, device: Device, proc: Any) -> None:
        for raw in proc.stderr or ():  # type: ignore[union-attr]
            self.log("[%s] %s" % (device.device_id, raw.rstrip("\n")))

    def _kill_process(self, device: Device) -> None:
        proc = device.proc
        device.stopped_intentionally = True
        if proc is not None and proc.poll() is None:
            proc.terminate()
        try:
            if proc is not None:
                proc.wait(timeout=KILL_GRACE)
        except subprocess.TimeoutExpired:
            if proc is not None and proc.poll() is None:
                proc.kill()

    def _stop_watchdog(self, device: Device) -> None:
        proc = device.proc
        if proc is None:
            self._report_stopped(device, "user", ok=True)
            return
        try:
            proc.wait(timeout=STOP_TIMEOUT)
            self._report_stopped(device, "user", ok=True)
        except subprocess.TimeoutExpired:
            self._kill_process(device)
            self._report_stopped(device, "user", ok=True)
            self.log("[%s] 停止超时，已强制终止" % device.device_id)

    # ---------------------------------------------------------------- 服务循环
    def run(self) -> None:
        while not self._shutdown:
            try:
                conn, _addr = self._srv.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with self._lock:
                self.clients.add(conn)
            threading.Thread(target=self._client_loop, args=(conn,),
                             daemon=True).start()
        self.shutdown()

    def _client_loop(self, conn: Any) -> None:
        buffer = ""
        try:
            while True:
                data = conn.recv(65536)
                if not data:
                    break
                buffer += data.decode("utf-8", errors="replace")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        self.reply_error(conn, "INVALID_MESSAGE",
                                         "消息必须是合法 JSON")
                        continue
                    if isinstance(msg, dict):
                        self.handle_msg(conn, msg)
        except OSError:
            pass
        finally:
            self._drop_client(conn)

    def shutdown(self) -> None:
        self._shutdown = True
        with self._lock:
            devices = list(self.devices.values())
        for device in devices:
            if device.is_active:
                device.stopped_intentionally = True
                try:
                    if device.proc and device.proc.poll() is None:
                        self._write_to_backend(device, {"type": "stop"})
                        device.proc.wait(timeout=STOP_TIMEOUT)
                except (OSError, subprocess.TimeoutExpired, ValueError):
                    self._kill_process(device)
        try:
            self._srv.close()
        except OSError:
            pass
        self.log("网关已退出")


def main() -> None:
    parser = argparse.ArgumentParser(description="模拟器网关（v2）")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址（默认 127.0.0.1）")
    parser.add_argument("--port", type=int, default=7331, help="监听端口（默认 7331）")
    args = parser.parse_args()
    # TASK-46A：启动时把可用槽位自动注册进 EMULATORS（零槽位=行为不变）
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
    try:
        import slot_loader  # noqa: F401  延迟导入：网关可为独立进程运行
        applied = slot_loader.apply_slots(EMULATORS)
        if applied:
            print("[gw] 槽位系统：注册 %d 个槽位（EMULATORS 共 %d 项）"
                  % (applied, len(EMULATORS)), file=sys.stderr, flush=True)
    except ImportError as exc:
        print("[gw] 槽位装载器不可用（忽略）: %s" % exc, file=sys.stderr, flush=True)
    try:
        gateway = Gateway(args.host, args.port)
    except OSError as exc:
        print("[gw] 启动失败（端口被占用？）: %s" % exc, file=sys.stderr)
        sys.exit(1)
    try:
        gateway.run()
    except KeyboardInterrupt:
        gateway.shutdown()


if __name__ == "__main__":
    main()