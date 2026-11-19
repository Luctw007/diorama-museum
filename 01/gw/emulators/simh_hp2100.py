# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""simh-hp2100 后端骨架（TASK-196-A）：第二批 SIMH 真跑矩阵第 4 台（HP 2100）。

结构对齐 `simh_pdp8.py`（母本）：终端文本流、不产帧；无二进制时
EMULATOR_BINARY_MISSING 并退出；命令文件 + 启动脚本骨架；全部未核实项标
[需核实]，不臆造 SIMH 语法。二进制由用户侧自行编译放入 third_party/ 或设
SIMH_HP2100_BIN（不下载、不编译）。

启动方式：python -m gw.emulators.simh_hp2100（由网关拉起；不要直接运行）。
自测：python -m gw.emulators.simh_hp2100 --check-binary（缺失退出码 2，找到退出码 0）
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

# 就绪横幅 [需核实]：Open SIMH HP2100 模拟器横幅字符串以真实发行版输出为准
# （对齐 pdp8 的 "PDP-8 simulator" 模式，此处按同构推断，未实测）
BANNER_RE = "HP2100 simulator"


def _find_binary() -> Optional[str]:
    """SIMH HP2100 二进制：环境变量 SIMH_HP2100_BIN 优先，其次 third_party/simh/hp2100。"""
    env_path = os.environ.get("SIMH_HP2100_BIN")
    if env_path and os.path.isfile(env_path):
        return env_path
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for name in ("hp2100", "hp2100.exe"):
        candidate = os.path.join(root, "third_party", "simh", name)
        if os.path.isfile(candidate):
            return candidate
    return None


class SimhHp2100Backend(BackendBase):
    name = "simh-hp2100"

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
        machine = cfg.get("machine", "hp2100")   # 本后端只服务 hp2100；machine 仅记录
        media = cfg.get("media") or []            # 用户自备介质；红线：不自动下载
        binary = _find_binary()
        if binary is None:
            self.emit_error(
                "EMULATOR_BINARY_MISSING",
                "SIMH HP2100 二进制未找到：请放入 third_party/simh/hp2100 或设置环境变量 "
                "SIMH_HP2100_BIN（见 licenses/SIMH.md）")
            self.emit_state("stopped", reason="binary_missing")
            self.log("start 拒绝：binary_missing（machine=%s）" % machine)
            raise SystemExit(1)

        self._cmd_path = os.path.join(tempfile.gettempdir(), "diorama_hp2100_cmds.txt")
        self._script_path = os.path.join(tempfile.gettempdir(), "diorama_hp2100_start.ini")
        self._write_script(machine, media)
        # 拉起方式 [需核实]：与 pdp8 同构（SIMH 惯例支持命令行给启动脚本文件）
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
            "; diorama hp2100 启动脚本（TASK-196-A 骨架，命令逐条 [需核实]）",
            "; machine=%s" % machine,
        ]
        for m in media:
            lines.append("; media（用户自备，红线仅引用）: %s" % m)
        lines.append("; [需核实] HP2100 交互命令（BOOT/CONT/EXIT 等）以发行版手册为准")
        with open(self._script_path or "", "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def _pump(self, stream_name: str, stream: Any) -> None:
        for raw in stream:
            self._parse_simh_line(stream_name, raw.rstrip("\n"))

    def _parse_simh_line(self, stream_name: str, line: str) -> None:
        """终端文本流转接：只记录文本、判定就绪；**不产帧**。"""
        if not line.strip():
            return
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
        self.emit({"type": "input_ack", "map": mp, "key": key, "value": value})
        # HP2100 走 TTY 文本注入（无 keymap 三级回退）；注入通道 [需核实]
        self._write_cmd({"cmd": "input", "as": "tty_text",
                         "map": mp, "key": key, "value": bool(value)})

    # ---------------------------------------------------------------- 快照（骨架）
    def on_save_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
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
    parser = argparse.ArgumentParser(description="simh-hp2100 后端（TASK-196-A 骨架）")
    parser.add_argument("--check-binary", action="store_true",
                        help="检查 SIMH HP2100 二进制；缺失退出码 2，找到退出码 0")
    args = parser.parse_args(argv)
    if args.check_binary:
        path = _find_binary()
        if path:
            print("SIMH HP2100 二进制: %s" % path)
            return 0
        print("SIMH HP2100 二进制缺失（third_party/simh/hp2100 或环境变量 SIMH_HP2100_BIN）")
        return 2
    SimhHp2100Backend().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())