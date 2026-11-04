# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""fake：测试用假模拟器后端（v2）。

v1 能力（保留）：渐变+游动条测试帧（RGB8）、正弦波音频（s16le）、快照回滚。
v2 新增：
- frame_codec：`raw`（默认）| `rle`（gw/emulators/rle.py 字节级 RLE）；
- sinks：`main` 恒定输出帧；含 `led` 时每 0.5s 输出 light_state（开/关交替）；
- 受控崩溃注入（测试 FR-E8 用）：
    · 输入 keyboard 键 `crash` → 回显 input_ack 后立即以退出码 1 崩溃；
    · config.auto_crash_frame=N → 第 N 帧产出前崩溃；
- 快照持久化：config.persist_path 指定 JSON 文件，save 时落盘、start 时加载，
  使"崩溃 → 网关自动重启 → load __auto"跨进程恢复成为可能。

启动参数全部经 start 消息 config 传入：
    {"width":320,"height":240,"fps":24.0,"tone_hz":440.0,
     "frame_codec":"raw","sinks":["main","led"],
     "auto_crash_frame":null,"persist_path":"..."}
（真实模拟器接入后，本后端作为协议回归参考实现保留。）

注意：由网关以 `python -m gw.emulators.fake_emulator` 拉起的子进程运行，
不要直接 `python gw/emulators/fake_emulator.py` 手动执行（帮助信息除外）。
"""

from __future__ import annotations

import base64
import json
import math
import os
import struct
import sys
import threading
import time
from typing import Any

from gw.emulators.base import BackendBase
from gw.emulators.rle import encode as rle_encode

DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 240
DEFAULT_FPS = 24.0
DEFAULT_TONE_HZ = 440.0

AUDIO_SAMPLE_RATE = 8000
AUDIO_CHUNK_SAMPLES = 160  # 每块 20ms
LED_PERIOD = 0.5  # 指示灯翻转周期（秒）


class FakeBackend(BackendBase):
    name = "fake"

    def __init__(self) -> None:
        super().__init__()
        self._w = DEFAULT_WIDTH
        self._h = DEFAULT_HEIGHT
        self._fps = DEFAULT_FPS
        self._tone_hz = DEFAULT_TONE_HZ
        self._codec = "raw"
        self._sinks: list[str] = ["main"]
        self._auto_crash_frame: int | None = None
        self._persist_path: str | None = None
        self._frame_id = 0
        self._audio_seq = 0
        self._saves: dict[str, int] = {}
        self._frame_lock = threading.Lock()  # 保护 _frame_id 读改写（04 线 DEFECT-M1-ROLLBACK-01 修复）
        self._stop_evt = threading.Event()

    # ---------------------------------------------------------------- 快照持久化
    def _load_persist(self) -> None:
        if not self._persist_path:
            return
        try:
            with open(self._persist_path, "r", encoding="utf-8") as fh:
                data = json.loads(fh.read())
            self._saves = {str(k): int(v) for k, v in data.get("saves", {}).items()}
            self.log("已加载持久化快照 %d 个: %s" % (len(self._saves), self._persist_path))
        except FileNotFoundError:
            self.log("无历史快照文件（首次启动）: %s" % self._persist_path)
        except (OSError, ValueError) as exc:
            self.log("持久化快照读取失败（忽略）: %s" % exc)

    def _persist(self) -> None:
        if not self._persist_path:
            return
        tmp = self._persist_path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"saves": self._saves}, ensure_ascii=False))
            os.replace(tmp, self._persist_path)
        except OSError as exc:
            self.log("持久化快照写入失败: %s" % exc)

    # ---------------------------------------------------------------- 帧与音频
    def _make_frame(self) -> bytes:
        """渐变底色（上蓝下红）+ 按帧号游动的白色竖条（宽 8 像素）。"""
        w, h = self._w, self._h
        bar_x = (self._frame_id * 4) % (w + 8) - 4
        rows = []
        for y in range(h):
            r = (y * 255) // max(h - 1, 1)
            b = 255 - r
            row = bytearray(bytes((r, 48, b)) * w)
            lo, hi = max(bar_x, 0), min(bar_x + 8, w)
            if lo < hi:
                row[lo * 3:hi * 3] = b"\xff\xff\xff" * (hi - lo)
            rows.append(row)
        return b"".join(rows)

    def _make_audio(self) -> bytes:
        n = AUDIO_CHUNK_SAMPLES
        base = self._audio_seq * n
        out = bytearray()
        for k in range(n):
            t = base + k
            value = int(14000.0 * math.sin(2.0 * math.pi * self._tone_hz * t / AUDIO_SAMPLE_RATE))
            out += struct.pack("<h", value)
        return bytes(out)

    def _crash(self, reason: str) -> None:
        """模拟崩溃：日志 + 强制退出码 1（os._exit 保证任何线程中都立即死亡）。"""
        self.log("CRASH-INJECT: %s" % reason)
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)

    def _produce_loop(self) -> None:
        period = 1.0 / self._fps
        while not self._stop_evt.is_set():
            t0 = time.perf_counter()
            # 帧号分配加锁：与 on_load_state 的回卷写互斥，杜绝"发出帧号==保存点"竞态
            with self._frame_lock:
                self._frame_id += 1
                fid = self._frame_id
            if self._auto_crash_frame is not None and fid == self._auto_crash_frame:
                self._crash("auto_crash_frame=%d" % self._auto_crash_frame)
            raw = self._make_frame()
            if self._codec == "rle":
                payload = rle_encode(raw)
            else:
                payload = raw
            self.emit({
                "type": "frame",
                "frame_id": fid,
                "width": self._w,
                "height": self._h,
                "format": "rgb8",
                "codec": self._codec,
                "sink": "main",
                "data_b64": base64.b64encode(payload).decode("ascii"),
                "ts": time.time(),
            })
            self._audio_seq += 1
            self.emit({
                "type": "audio",
                "seq": self._audio_seq,
                "sample_rate": AUDIO_SAMPLE_RATE,
                "channels": 1,
                "format": "s16le",
                "sink": "speaker",
                "data_b64": base64.b64encode(self._make_audio()).decode("ascii"),
            })
            elapsed = time.perf_counter() - t0
            if elapsed < period:
                time.sleep(period - elapsed)

    def _led_loop(self) -> None:
        on = False
        while not self._stop_evt.wait(LED_PERIOD):
            on = not on
            self.emit({"type": "light_state", "sink": "led", "on": on,
                       "ts": time.time()})

    # ---------------------------------------------------------------- 钩子实现
    def on_start(self, msg: dict[str, Any]) -> None:
        cfg = msg.get("config") or {}
        self._w = int(cfg.get("width", DEFAULT_WIDTH))
        self._h = int(cfg.get("height", DEFAULT_HEIGHT))
        self._fps = float(cfg.get("fps", DEFAULT_FPS))
        self._tone_hz = float(cfg.get("tone_hz", DEFAULT_TONE_HZ))
        self._codec = str(cfg.get("frame_codec", "raw"))
        self._sinks = [str(s) for s in cfg.get("sinks", ["main"])]
        self._auto_crash_frame = cfg.get("auto_crash_frame")
        self._auto_crash_frame = int(self._auto_crash_frame) \
            if self._auto_crash_frame is not None else None
        self._persist_path = cfg.get("persist_path")
        self._load_persist()
        self.log("start config=%s device_id=%s"
                 % (cfg, msg.get("device_id", "?")))
        self.emit_state("starting", emulator=self.name, width=self._w,
                        height=self._h, fps=self._fps,
                        codec=self._codec, sinks=self._sinks)
        threading.Thread(target=self._produce_loop, daemon=True).start()
        if "led" in self._sinks:
            threading.Thread(target=self._led_loop, daemon=True).start()
        # 产出循环起来后即为 running（网关以收到本消息为启动完成依据）
        self.emit_state("running", width=self._w, height=self._h, fps=self._fps,
                        codec=self._codec, sinks=self._sinks)

    def on_input(self, msg: dict[str, Any]) -> None:
        key = msg.get("key")
        self.emit({
            "type": "input_ack",
            "map": msg.get("map", "keyboard"),
            "key": key,
            "value": msg.get("value"),
        })
        if msg.get("map", "keyboard") == "keyboard" and key == "crash":
            self._crash("input key=crash")

    def on_save_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        with self._frame_lock:
            self._saves[sid] = self._frame_id
        self._persist()
        with self._frame_lock:
            self.emit_ack("save_state", id=sid, frame_id=self._frame_id)

    def on_load_state(self, msg: dict[str, Any]) -> None:
        sid = str(msg.get("id", "s"))
        with self._frame_lock:
            if sid not in self._saves:
                entry = None
            else:
                entry = self._saves[sid]
        if entry is None:
            self.emit({"type": "error", "code": "NOT_FOUND", "id": sid,
                       "message": "快照不存在: %s" % sid})
            return
        with self._frame_lock:
            self._frame_id = entry
            self.emit_ack("load_state", id=sid, frame_id=entry)

    def on_stop(self, msg: dict[str, Any]) -> None:
        self._stop_evt.set()
        self.emit_state("stopped")


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print("fake 假模拟器后端 v2（测试用）。由网关 gw/gateway.py 以子进程方式调用；")
        print("协议见 gw/PROTOCOL.md。start 消息 config 字段：")
        print("  width/height/fps/tone_hz/frame_codec(raw|rle)/sinks/auto_crash_frame/persist_path")
        return
    FakeBackend().run()


if __name__ == "__main__":
    main()