# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""stella 后端骨架（TASK-161-B）：v0.1「三台真跑」第三台（Stella / Atari 2600）。

状态：**骨架**。Stella 为图形系统（2600 有帧缓冲）：帧通道格式对齐内容包
`rgba8`、音频 `pcm16`（05 线 atari-2600 runtime.json）——但抓帧与音频直读 API
一律标 [需核实]，骨架阶段不落真实帧数据（与 mame_apple2 骨架同等诚实，不做
"貌似能跑"的假数据）。无二进制时 on_start 回 EMULATOR_BINARY_MISSING 并退出。

输入语义：以 runtime.json `input_map` 的 `map/key`（joystick axis_x/axis_y/btn*、
keyboard KEY_*）为参照直传；**不得**把 keys/keymap_atari-2600.json 的
`mame_field/mame_code`（MAME 语义遗留）当 Stella 键码翻译层。注入通道 [需核实]。

启动方式：python -m gw.emulators.stella（由网关拉起；不要直接运行本脚本）。
自测：python -m gw.emulators.stella --check-binary（缺失退出码 2，找到退出码 0）
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any, Optional

from .base import BackendBase

# 内容包侧声明的输出格式（05 线 runtime.json）：video rgba8 / audio pcm16
FRAME_FORMAT = "rgba8"
AUDIO_FORMAT = "pcm16"


def _find_binary() -> Optional[str]:
    """Stella 二进制：环境变量 STELLA_BIN 优先，其次 third_party/stella/。"""
    env_path = os.environ.get("STELLA_BIN")
    if env_path and os.path.isfile(env_path):
        return env_path
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for name in ("stella", "stella.exe"):
        candidate = os.path.join(root, "third_party", "stella", name)
        if os.path.isfile(candidate):
            return candidate
    return None


class StellaBackend(BackendBase):
    name = "stella"

    def __init__(self) -> None:
        super().__init__()
        self._proc: Optional[subprocess.Popen] = None
        self._cfg: dict[str, Any] = {}
        self._cmd_path: Optional[str] = None
        self._warned_input = False
        self._warned_frame_api = False

    # ---------------------------------------------------------------- start
    def on_start(self, msg: dict[str, Any]) -> None:
        cfg = msg.get("config") or {}
        self._cfg = cfg
        media = cfg.get("media") or []      # 卡带路径（用户自备；红线：不自动下载）
        binary = _find_binary()
        if binary is None:
            self.emit_error(
                "EMULATOR_BINARY_MISSING",
                "Stella 二进制未找到：请放入 third_party/stella/ 或设置环境变量 "
                "STELLA_BIN（见 licenses/Stella.md）")
            self.emit_state("stopped", reason="binary_missing")
            self.log("start 拒绝：binary_missing")
            raise SystemExit(1)

        self._cmd_path = os.path.join(tempfile.gettempdir(), "diorama_stella_cmds.txt")
        # 启动参数 [需核实]：Stella CLI 当前骨架仅传卡带路径；
        # 窗口/无头/抓帧相关开关（如 -video/截图通道）以 stella --help 与版本为准
        cmd = [binary]
        for item in media:
            cmd.append(item)
        self.log("Popen: %s" % " ".join(cmd))
        self._proc = subprocess.Popen(
            cmd, cwd=os.path.dirname(binary),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, encoding="utf-8", errors="replace")
        self.emit_state("starting")
        for stream_name, stream in (("stderr", self._proc.stderr),
                                    ("stdout", self._proc.stdout)):
            t = threading.Thread(target=self._pump, args=(stream_name, stream),
                                 daemon=True)
            t.start()

    def _pump(self, stream_name: str, stream: Any) -> None:
        for raw in stream:
            if raw.strip():
                self.log("TTY[%s] %s" % (stream_name, raw.rstrip("\n")[:200]))

    # ---------------------------------------------------------------- 帧/音频骨架（不落假数据）
    def _note_frame_api(self) -> None:
        """帧/音频直读 API [需核实]：骨架阶段只发一次性说明日志，不产帧。"""
        if not self._warned_frame_api:
            self._warned_frame_api = True
            self.log("提示：Stella 帧（%s）/音频（%s）直读 API 需核实；"
                     "骨架阶段不落真实帧数据（无假数据），待核实后接入" %
                     (FRAME_FORMAT, AUDIO_FORMAT))

    # ---------------------------------------------------------------- 输入
    def on_input(self, msg: dict[str, Any]) -> None:
        key = msg.get("key")
        mp = msg.get("map", "keyboard")
        value = msg.get("value")
        # 本地回显（客户端等待的 input_ack，与 fake/mame 后端行为一致）
        self.emit({"type": "input_ack", "map": mp, "key": key, "value": value})
        # 语义参照 runtime.json input_map（joystick axis/btn、keyboard KEY_*），
        # 注入通道 [需核实]；不用 keymap_atari-2600.json（MAME 语义遗留）作翻译层
        if not self._warned_input:
            self._warned_input = True
            self.log("提示：Stella 注入通道（joystick axis/btn、键盘）需核实；"
                     "当前按 input_map 语义字面下发并记账")
        self._write_cmd({"cmd": "input", "map": mp, "key": key,
                         "value": bool(value), "ts": time.time()})

    # ---------------------------------------------------------------- 快照（骨架）
    def on_save_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        # Stella 快照命令/机制 [需核实]；骨架仅落命令写入 + 时间戳记账，不伪造 ack
        self._write_cmd({"cmd": "save", "id": sid, "ts": time.time()})
        self.log("save 命令已写入命令文件（id=%s；机制 [需核实]）" % sid)

    def on_load_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        self._write_cmd({"cmd": "load", "id": sid, "ts": time.time()})
        self.log("load 命令已写入命令文件（id=%s；机制 [需核实]）" % sid)

    # ---------------------------------------------------------------- stop
    def on_stop(self, msg: dict[str, Any]) -> None:
        self._write_cmd({"cmd": "stop", "ts": time.time()})
        if self._proc and self._proc.poll() is None:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=3)
            except (OSError, subprocess.TimeoutExpired):
                self._proc.kill()
        self.emit_state("stopped", reason="user")
        # 基类 dispatch 在 on_stop 后 SystemExit(0)

    # ---------------------------------------------------------------- 下发通道
    def _write_cmd(self, obj: dict[str, Any]) -> bool:
        if not self._cmd_path:
            self.log("命令下发跳过：未初始化通道")
            return False
        try:
            with open(self._cmd_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
            return True
        except OSError as exc:
            self.log("命令写入失败: %s" % exc)
            return False


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="stella 后端（TASK-161-B 骨架）")
    parser.add_argument("--check-binary", action="store_true",
                        help="检查 Stella 二进制；缺失退出码 2，找到退出码 0")
    args = parser.parse_args(argv)
    if args.check_binary:
        path = _find_binary()
        if path:
            print("Stella 二进制: %s" % path)
            return 0
        print("Stella 二进制缺失（third_party/stella/ 或环境变量 STELLA_BIN）")
        return 2
    StellaBackend().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())