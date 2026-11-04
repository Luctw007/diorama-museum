# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""模拟器后端公共骨架。

后端进程与网关之间的"设备通道"协议见 gw/PROTOCOL.md 第 2.2 / 5 章：
- 后端从 stdin 读命令（一行一条 JSON），向 stdout 发事件（同样一行一条 JSON）；
- stderr 仅用于后端自身的日志；
- 收到 stop 命令后必须发 state:stopped 并以退出码 0 退出。

使用方式：子类实现 on_start / on_input / on_save_state / on_load_state / on_stop，
然后以 `python -m gw.emulators.<模块名>` 启动（不要直接运行脚本自身）。
"""

from __future__ import annotations

import abc
import json
import sys
from typing import Any, TextIO


class BackendBase(abc.ABC):
    """模拟器后端基类：负责 stdio 行式 JSON 的收发与消息分发。"""

    #: 后端名称（必须与网关注册表中的键一致）
    name: str = "base"

    def __init__(self) -> None:
        self._stdin: TextIO = sys.stdin
        self._stdout: TextIO = sys.stdout

    # ------------------------------------------------------------------ 发送
    def emit(self, obj: dict[str, Any]) -> None:
        """向网关发送一条事件（含 proto 版本字段）。"""
        obj.setdefault("proto", 1)
        self._stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
        self._stdout.flush()

    def emit_state(self, state: str, **kw: Any) -> None:
        self.emit({"type": "state", "state": state, **kw})

    def emit_error(self, code: str, message: str) -> None:
        self.emit({"type": "error", "code": code, "message": message})

    def emit_ack(self, op: str, **kw: Any) -> None:
        self.emit({"type": "ack", "op": op, "ok": True, **kw})

    def log(self, message: str) -> None:
        """后端自身的诊断日志（stderr，网关原样透传记录）。"""
        print("[%s] %s" % (self.name, message), file=sys.stderr, flush=True)

    # ------------------------------------------------------------------ 入口
    def run(self) -> None:
        """后端主循环：阻塞读 stdin，逐行分发。"""
        for raw in self._stdin:
            line = raw.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                self.emit_error("INVALID_MESSAGE", "无法解析的消息: %s" % line[:80])
                continue
            if not isinstance(msg, dict):
                self.emit_error("INVALID_MESSAGE", "消息必须是 JSON 对象")
                continue
            self.dispatch(msg)

    def dispatch(self, msg: dict[str, Any]) -> None:
        msg_type = msg.get("type")
        if msg_type == "start":
            self.on_start(msg)
        elif msg_type == "input":
            self.on_input(msg)
        elif msg_type == "save_state":
            self.on_save_state(msg)
        elif msg_type == "load_state":
            self.on_load_state(msg)
        elif msg_type == "stop":
            self.on_stop(msg)
            raise SystemExit(0)
        else:
            self.emit_error("UNSUPPORTED", "不支持的消息类型: %r" % msg_type)

    # ------------------------------------------------------------------ 钩子
    @abc.abstractmethod
    def on_start(self, msg: dict[str, Any]) -> None: ...

    @abc.abstractmethod
    def on_input(self, msg: dict[str, Any]) -> None: ...

    @abc.abstractmethod
    def on_save_state(self, msg: dict[str, Any]) -> None: ...

    @abc.abstractmethod
    def on_load_state(self, msg: dict[str, Any]) -> None: ...

    @abc.abstractmethod
    def on_stop(self, msg: dict[str, Any]) -> None: ...