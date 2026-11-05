# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""simh-pdp8 后端骨架（TASK-161-A）：v0.1「三台真跑」第二台（SIMH PDP-8）。

关键事实（licenses/SIMH.md、TASK-01 §四 第 5 步结论）：
SIMH PDP-8 的输出是**终端文本流**（TTY）而非帧缓冲——本后端**不产帧**（不发 frame
事件），只如实转接终端文本；画面验证由 fake 后端承担。不得自行"发明"帧格式。

状态：**骨架**。无二进制时 on_start 回 EMULATOR_BINARY_MISSING 并退出（对应
gw/gateway.py EMULATORS["simh-pdp8"]，其 module 字段由本任务补齐）。
未核实项一律标 [需核实]，不伪装成可运行成品（红线）。

命令下发与 mame_apple2 同风格：命令文件（临时目录）轮询骨架；区别——本后端**没有
keymap 三级回退**（PDP-8 走 TTY 文本注入，非键码表；与 mame_apple2 不同，见 on_input）。

启动方式：python -m gw.emulators.simh_pdp8（由网关拉起；不要直接运行本脚本）。
自测：python -m gw.emulators.simh_pdp8 --check-binary（缺失退出码 2，找到退出码 0）
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

# SIMH 启动横幅（就绪判定 [需核实]：以所采用发行版真实输出为准；
# 预演假二进制输出的版本行形如 "PDP-8 simulator V4.0-0 Beta …"）
BANNER_RE = "PDP-8 simulator"
PROMPT_MARKS = (".", "sim>")


def _find_binary() -> Optional[str]:
    """SIMH PDP-8 二进制：环境变量 SIMH_PDP8_BIN 优先，其次 third_party/simh/。"""
    env_path = os.environ.get("SIMH_PDP8_BIN")
    if env_path and os.path.isfile(env_path):
        return env_path
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for name in ("pdp8", "pdp8.exe"):
        candidate = os.path.join(root, "third_party", "simh", name)
        if os.path.isfile(candidate):
            return candidate
    return None


class SimhPdp8Backend(BackendBase):
    name = "simh-pdp8"

    def __init__(self) -> None:
        super().__init__()
        self._proc: Optional[subprocess.Popen] = None
        self._cfg: dict[str, Any] = {}
        self._cmd_path: Optional[str] = None
        self._script_path: Optional[str] = None
        self._banner_seen = False

    # ---------------------------------------------------------------- start
    def on_start(self, msg: dict[str, Any]) -> None:
        cfg = msg.get("config") or {}
        self._cfg = cfg
        machine = cfg.get("machine", "pdp8")   # 本后端只服务 pdp8；machine 仅记录
        media = cfg.get("media") or []          # 用户自备介质路径；红线：不自动下载
        binary = _find_binary()
        if binary is None:
            self.emit_error(
                "EMULATOR_BINARY_MISSING",
                "SIMH 二进制未找到：请放入 third_party/simh/ 或设置环境变量 "
                "SIMH_PDP8_BIN（见 licenses/SIMH.md）")
            self.emit_state("stopped", reason="binary_missing")
            self.log("start 拒绝：binary_missing（machine=%s）" % machine)
            raise SystemExit(1)

        self._cmd_path = os.path.join(tempfile.gettempdir(), "diorama_simh_cmds.txt")
        self._script_path = os.path.join(tempfile.gettempdir(), "diorama_pdp8_start.ini")
        self._write_script(machine, media)
        # 拉起方式 [需核实]：SIMH 惯例支持命令行给启动脚本文件（`pdp8 <file>`），
        # 亦可用 stdin 重定向；以所采用发行版手册为准。
        cmd = [binary, self._script_path]
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

    def _write_script(self, machine: str, media: list[str]) -> None:
        """启动脚本骨架（[需核实] 命令名与语法；不伪装成可运行成品）。"""
        lines = [
            "; diorama pdp8 启动脚本（TASK-161-A 骨架，命令逐条 [需核实]）",
            "; machine=%s" % machine,
        ]
        for m in media:
            lines.append("; media（用户自备，红线仅引用）: %s" % m)
        lines.append("; [需核实] 就绪后建议由后端经命令文件驱动；"
                     "SIMH 交互命令（BOOT/CONT/EXIT 等）以发行版手册为准")
        with open(self._script_path or "", "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def _pump(self, stream_name: str, stream: Any) -> None:
        for raw in stream:
            self._parse_simh_line(stream_name, raw.rstrip("\n"))

    def _parse_simh_line(self, stream_name: str, line: str) -> None:
        """终端文本流转接：只记录文本、判定就绪；**不产帧**。"""
        if not line.strip():
            return
        # 就绪判定 [需核实]：以真实发行版启动横幅为准（假二进制曾输出
        # "PDP-8 simulator V4.0-0 Beta DRILL-FAKE-BINARY"）
        if not self._banner_seen and BANNER_RE in line:
            self._banner_seen = True
            self.emit_state("running")
            self.log("识别启动横幅→running（流=%s，[需核实]横幅格式）" % stream_name)
        self.log("TTY[%s] %s" % (stream_name, line[:200]))

    # ---------------------------------------------------------------- 输入（TTY 文本注入）
    def on_input(self, msg: dict[str, Any]) -> None:
        key = msg.get("key")
        mp = msg.get("map", "keyboard")
        value = msg.get("value")
        # 本地回显（客户端等待的 input_ack，与 fake/mame 后端行为一致）
        self.emit({"type": "input_ack", "map": mp, "key": key, "value": value})
        # PDP-8 走 TTY 文本注入（非键码表三级回退——本后端不含 keymap，
        # 与 mame_apple2 的差异点；具体注入通道 [需核实]：命令文件轮询 / stdin 直写）
        self._write_cmd({"cmd": "input", "as": "tty_text",
                         "map": mp, "key": key, "value": bool(value)})

    # ---------------------------------------------------------------- 快照（骨架）
    def on_save_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        # SIMH SAVE 命令名与确认回执 [需核实]（SIMH 快照命令以发行版手册为准，
        # 常见 SAVE/RESTORE）；骨架仅落命令写入 + 时间戳记账，不伪造 ack
        self._write_cmd({"cmd": "save", "id": sid, "ts": time.time()})
        self.log("save 命令已写入命令文件（id=%s；SIMH 命令名 [需核实]）" % sid)

    def on_load_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        self._write_cmd({"cmd": "load", "id": sid, "ts": time.time()})
        self.log("load 命令已写入命令文件（id=%s；SIMH 命令名 [需核实]）" % sid)

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
    parser = argparse.ArgumentParser(description="simh-pdp8 后端（TASK-161-A 骨架）")
    parser.add_argument("--check-binary", action="store_true",
                        help="检查 SIMH 二进制；缺失退出码 2，找到退出码 0")
    args = parser.parse_args(argv)
    if args.check_binary:
        path = _find_binary()
        if path:
            print("SIMH 二进制: %s" % path)
            return 0
        print("SIMH 二进制缺失（third_party/simh/ 或环境变量 SIMH_PDP8_BIN）")
        return 2
    SimhPdp8Backend().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())