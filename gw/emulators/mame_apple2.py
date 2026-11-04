# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""mame-apple2 后端骨架（TASK-16A；M2 里程碑对应的真实运行通道）。

设计依据：05 线 docs/research/apple-ii/13_MAME接入预研.md（协议映射表 §三、
启动参数 §九、boot.lua 骨架 §十、后端骨架 §十一）。

状态：**骨架**。真实接通路径已按 14-A 编写，但本仓库不随附 MAME 二进制与 ROM——
无二进制时 on_start 回 EMULATOR_BINARY_MISSING 并退出（网关注册表已登记 mame-apple2）。

三层切分（M2 里程碑）：
  M2.1 画面+音频 —— _start_mame() 拉起 MAME + Lua 抓帧；_forward_frame/_forward_audio
  M2.2 输入      —— on_input() 本地回显 + _write_cmd() 下发（Lua 侧 natkeyboard:post / field:set_value）
  M2.3 存档      —— on_save_state/on_load_state → _write_cmd() → save_ack/load_ack 事件 → emit_ack

运行时命令下发通道（14-A §八）：本骨架采用「命令文件轮询」（跨平台最简），boot.lua
以 emu.register_periodic 周期读同一文件；若改为命名管道只需替换 _write_cmd 的落点。

启动方式：python -m gw.emulators.mame_apple2（由网关拉起；不要直接运行本脚本）。
自测：python -m gw.emulators.mame_apple2 --check-binary  （缺失退出码 2，找到退出码 0）
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any, Optional

from .base import BackendBase

try:  # 与 fake 后端一致：包内相对导入；直接运行本文件时降级为 raw 直传
    from .rle import rle_encode
except ImportError:  # pragma: no cover
    def rle_encode(data: bytes) -> bytes:
        return bytes(data)

# M2.1 断言约定的画面要素（见 docs/m2_assert_draft.md）：Apple II 6 色高分辨率 280x192
FRAME_FORMAT = "rgb8"
DEFAULT_WIDTH = 280
DEFAULT_HEIGHT = 192


def _find_mame_binary() -> Optional[str]:
    """查找 MAME 二进制：环境变量 MAME_BIN 优先，其次 third_party/mame/。"""
    env_path = os.environ.get("MAME_BIN")
    if env_path and os.path.isfile(env_path):
        return env_path
    for name in ("mame", "mame.exe"):
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        candidate = os.path.join(root, "third_party", "mame", name)
        if os.path.isfile(candidate):
            return candidate
    return None


class MameApple2Backend(BackendBase):
    name = "mame-apple2"

    def __init__(self) -> None:
        super().__init__()
        self._proc: Optional[subprocess.Popen] = None
        self._running = False
        self._frame_id = 0
        self._frame_lock = threading.Lock()
        self._cfg: dict[str, Any] = {}
        self._cmd_path: Optional[str] = None
        self._lua_path: Optional[str] = None
        self._warned_audio = False
        self._warned_keymap = False
        self._keymap: dict[str, dict] = {}
        self._pending_saves: dict[str, float] = {}

    # ---------------------------------------------------------------- start
    def on_start(self, msg: dict[str, Any]) -> None:
        cfg = msg.get("config") or {}
        self._cfg = cfg
        machine = cfg.get("machine", "apple2")
        codec = cfg.get("frame_codec", "rle")
        sinks = cfg.get("sinks") or ["crt_display", "speaker"]
        media = cfg.get("media") or []          # 用户自备路径列表；红线：本仓库不自动下载 ROM
        binary = _find_mame_binary()
        if binary is None:
            self.emit_error(
                "EMULATOR_BINARY_MISSING",
                "MAME 二进制未找到：请放入 third_party/mame/ 或设置环境变量 MAME_BIN"
                "（见 licenses/MAME.md）")
            self.emit_state("stopped", reason="binary_missing")
            self.log("start 拒绝：binary_missing（machine=%s）" % machine)
            raise SystemExit(1)

        self._cmd_path = os.path.join(tempfile.gettempdir(), "mame_cmds.jsonl")
        self._lua_path = os.path.join(tempfile.gettempdir(), "diorama_boot_apple2.lua")
        self._load_keymap(machine)
        with open(self._lua_path, "w", encoding="utf-8") as fh:
            fh.write(self._build_boot_lua(machine, codec, sinks))
        # 启动参数（草案，与 14-A §九 对齐；正式清单随 MAME 版本核对后固化）
        cmd = [binary, machine, "-video", "none", "-console",
               "-autoboot_script", self._lua_path]
        if media:
            for item in media:
                cmd += ["-flop1", item]
        self.log("Popen: %s" % " ".join(cmd))
        self._proc = subprocess.Popen(
            cmd, cwd=os.path.dirname(binary),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, encoding="utf-8", errors="replace")
        self.emit_state("starting")
        for stream_name, stream, parser in (
                ("stderr", self._proc.stderr, self._parse_mame_line),
                ("stdout", self._proc.stdout, self._parse_mame_line)):
            t = threading.Thread(target=self._pump, args=(stream_name, stream, parser),
                                 daemon=True)
            t.start()

    def _pump(self, stream_name: str, stream: Any, parser: Any) -> None:
        for raw in stream:
            parser(raw.rstrip("\n"))

    def _parse_mame_line(self, line: str) -> None:
        """Lua 侧以 emu.print_info 打印结构化事件 `j{...}`；其余行仅记录。"""
        if line.startswith("j{"):
            try:
                self._handle_mame_event(json.loads(line[1:]))
            except json.JSONDecodeError:
                self.log("无法解析事件行: %s" % line[:120])
            return
        if line.strip():
            self.log(line[:200])

    def _handle_mame_event(self, evt: dict[str, Any]) -> None:
        kind = evt.get("evt")
        if kind == "frame":
            self._forward_frame(evt)
        elif kind == "audio":
            self._forward_audio(evt)
        elif kind == "state":
            self.emit_state(str(evt.get("state", "running")))
        elif kind == "save_ack":
            self._pending_saves.pop(str(evt.get("id", "s")), None)
            self.emit_ack("save_state", id=evt.get("id"),
                          frame_id=evt.get("frame_id"))
        elif kind == "load_ack":
            self._pending_saves.pop(str(evt.get("id", "s")), None)
            self.emit_ack("load_state", id=evt.get("id"),
                          frame_id=evt.get("frame_id"))
        elif kind == "error":
            self.emit_error(str(evt.get("code", "BACKEND")),
                            str(evt.get("message", "")))
        else:
            self.log("忽略未知事件: %s" % kind)

    # ---------------------------------------------------------------- M2.1
    def _forward_frame(self, evt: dict[str, Any]) -> None:
        with self._frame_lock:
            self._frame_id += 1
            fid = self._frame_id
        first = not self._running
        if first:
            self._running = True
            self.emit_state("running")   # 判定依据：首个 frame_done 回调（14-A §3.2）
        data_b64 = evt.get("data_b64", "")
        payload = data_b64
        if self._cfg.get("frame_codec", "rle") == "rle" and data_b64:
            raw = base64.b64decode(data_b64)
            payload = base64.b64encode(rle_encode(raw)).decode("ascii")
        self.emit({
            "type": "frame",
            "frame_id": fid,
            "w": int(evt.get("w", DEFAULT_WIDTH)),
            "h": int(evt.get("h", DEFAULT_HEIGHT)),
            "format": FRAME_FORMAT,
            "data_b64": payload,
            "ts": time.time(),
        })

    def _forward_audio(self, evt: dict[str, Any]) -> None:
        """MAME 原生扬声器采样流输出通道 [需核实]（14-A 开放问题）：
        骨架按事件直传；若长期无该通道，M2.1 音频断言以"退化不丢帧"降级。"""
        if not self._warned_audio:
            self._warned_audio = True
            self.log("警告：MAME 扬声器采样流通道需核实；收到第一块音频事件，先按直传处理")
        self.emit({
            "type": "audio",
            "format": evt.get("format", "s16le"),
            "sample_rate": int(evt.get("sample_rate", 0)),
            "samples_b64": evt.get("samples_b64", ""),
        })

    # ---------------------------------------------------------------- M2.2
    def on_input(self, msg: dict[str, Any]) -> None:
        key = msg.get("key")
        mp = msg.get("map", "keyboard")
        value = msg.get("value")
        # 本地回显（客户端等待的 input_ack，与 fake 后端行为一致）
        self.emit({"type": "input_ack", "map": mp, "key": key, "value": value})
        # 翻译层：动作名 → MAME 注入指令（TASK-26A）；查不到回退字面下发并警告
        entry = self._keymap.get(str(key))
        if entry is None:
            if not self._warned_keymap:
                self._warned_keymap = True
                self.log("警告：键 %r 不在 keymap 中，按字面下发（map=%s）" % (key, mp))
            self._write_cmd({"cmd": "input", "map": mp, "key": key,
                             "value": bool(value)})
            return
        cmd: dict[str, Any] = {"cmd": "input", "action": str(key),
                               "value": bool(value)}
        if "mame_char" in entry:
            cmd["mame_char"] = entry["mame_char"]
        elif "mame_code" in entry:
            cmd["mame_code"] = entry["mame_code"]
        elif "mame_field" in entry:
            cmd["mame_field"] = entry["mame_field"]
        cmd["verify"] = bool(entry.get("verify"))
        self._write_cmd(cmd)

    def _load_keymap(self, machine: str) -> None:
        """三级回退加载后端键码映射（TASK-31A，见 docs/keymap_register.md）：
        1. config.keymap（客户端显式指定；相对路径按仓库根解析，绝对路径直用）；
        2. keys/keymap_<machine>.json（机种默认，同目录）；
        3. 旧路径 gw/emulators/keymap_<machine>.json（v1 兼容）；
        均失败 → 空表 + 警告（输入按字面下发）。"""
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        candidates: list[str] = []
        explicit = self._cfg.get("keymap")
        if explicit:
            candidates.append(explicit if os.path.isabs(explicit)
                              else os.path.join(root, explicit))
        candidates.append(os.path.join(root, "gw", "emulators", "keys",
                                       "keymap_%s.json" % machine))
        candidates.append(os.path.join(root, "gw", "emulators",
                                       "keymap_%s.json" % machine))
        for path in candidates:
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
                self._keymap = data.get("entries") or {}
                self.log("已加载键码映射 %s（%d 条目）" % (path, len(self._keymap)))
                return
            except (OSError, json.JSONDecodeError) as exc:
                self.log("键码映射候选未命中（%s）: %s" % (path, exc))
        self._keymap = {}
        self.log("警告：三级回退全部未命中，输入按字面下发")

    # ---------------------------------------------------------------- M2.3
    def on_save_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        self._pending_saves[sid] = time.time()   # 超时兜底留待 watchdog（骨架不启用）
        self._write_cmd({"cmd": "save", "id": sid})
        # 真正的 ack 在 _handle_mame_event("save_ack") 回（帧号由 Lua 侧帧计数回填）

    def on_load_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        self._pending_saves[sid] = time.time()
        self._write_cmd({"cmd": "load", "id": sid})

    # ---------------------------------------------------------------- stop
    def on_stop(self, msg: dict[str, Any]) -> None:
        self._write_cmd({"cmd": "stop"})
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
        """:return: 写入成功与否；无命令文件（未启动）仅记录。"""
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

    # ---------------------------------------------------------------- boot.lua
    def _build_boot_lua(self, machine: str, codec: str, sinks: list[str]) -> str:
        """boot.lua 模板（与 14-A §十 骨架对齐）。占位符 @@xxx@@ 在此替换；
        画面直读 API 与快照兜底路径标注 [需核实]（14-A §3.2）。"""
        tpl = r"""
-- diorama boot.lua（mame-apple2 后端生成，TASK-16A 骨架）
local EMI = manager.machine
local cmd_path = "@@CMD_PATH@@"
local sink_table = @@SINKS@@
local codec = "@@CODEC@@"
local w, h = @@W@@, @@H@@
local frame_n = 0
local function j(t) emu.print_info("j" .. t) end   -- 剩空格避免 MAME 日志前缀干扰

-- M2.1：逐帧抓取（> 边兜底位图路径）
emu.register_frame_done(function()
  frame_n = frame_n + 1
  -- 位图直读 API [需核实]；快照兜底 video:snapshot() + 后端读 PNG 亦可
  j("{\"evt\":\"frame\",\"frame_id\":" .. frame_n .. ",\"w\":" .. w .. ",\"h\":" .. h .. ",\"data_b64\":\"\"}")
end)
if frame_n == 1 then
  -- [需核实] 位图直读替换此处后，首帧即真数据；当前骨架帧事件仅作状态信号
end
-- 首帧后报告 running
emu.register_start(function() j("{\"evt\":\"state\",\"state\":\"starting\"}") end)

-- M2.2/2.3：命令文件轮询（14-A §八 候选1；命名管道替换点）
local last_pos = 0
emu.register_periodic(function()
  local f = io.open(cmd_path, "r")
  if f then
    f:seek("set", last_pos)
    for line in f:lines() do
      last_pos = f:seek("cur")  -- [需核实] 行读取后位置行为跨平台差异，必要时按字节累计
      local ok, c = pcall(function() return json_decode(line) end)  -- [需核实] 内建 JSON 库名
      if ok and c then
        if c.cmd == "input" then
          if c.map == "keyboard" then
            -- natkeyboard:post / post_coded 映射表见 14-A §3.1；键名转换 [需核实]
            EMI.natkeyboard:post(tostring(c.key or ""))
            j("{\"evt\":\"input_ack\",\"map\":\"keyboard\",\"key\":\"" .. tostring(c.key) .. "\"}")
          elseif c.map == "joystick" then
            -- ioport.field:set_value 摇杆轴/按钮写入 [需核实 port tag 与 field 掩码]
            j("{\"evt\":\"input_ack\",\"map\":\"joystick\",\"key\":\"" .. tostring(c.key) .. "\"}")
          end
        elseif c.cmd == "save" then
          -- machine:save / state 集保存点（14-A §3.1）；完成后续报 save_ack
          j("{\"evt\":\"save_ack\",\"id\":\"" .. tostring(c.id) .. "\",\"frame_id\":" .. frame_n .. "}")
        elseif c.cmd == "load" then
          j("{\"evt\":\"load_ack\",\"id\":\"" .. tostring(c.id) .. "\",\"frame_id\":" .. frame_n .. "}")
        elseif c.cmd == "stop" then
          EMI:exit()
        end
      end
    end
    f:close()
  end
end)
-- @@GUIDE@@：本模板随 MAME 版本核对（14-A §十二 [需核实] 清单），不作为可运行成品。
"""
        return (tpl
                .replace("@@CMD_PATH@@", (self._cmd_path or "").replace("\\", "\\\\"))
                .replace("@@SINKS@@", json.dumps(sinks))
                .replace("@@CODEC@@", codec)
                .replace("@@W@@", str(int(self._cfg.get("frame_w", DEFAULT_WIDTH))))
                .replace("@@H@@", str(int(self._cfg.get("frame_h", DEFAULT_HEIGHT))))
                .replace("@@GUIDE@@", ""))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="mame-apple2 后端（TASK-16A 骨架）")
    parser.add_argument("--check-binary", action="store_true",
                        help="检查 MAME 二进制；缺失退出码 2，找到退出码 0")
    args = parser.parse_args(argv)
    if args.check_binary:
        path = _find_mame_binary()
        if path:
            print("MAME 二进制: %s" % path)
            return 0
        print("MAME 二进制缺失（third_party/mame/ 或环境变量 MAME_BIN）")
        return 2
    MameApple2Backend().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())