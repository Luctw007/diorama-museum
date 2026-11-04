# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""M0 自动化验收：模拟器网关全链路。

用例（对应 TASK-01 里程碑 M0 完成定义）：
  1) heartbeat 探活；
  2) 启动 fake 后端 → start_device_ack ok；
  3) 收到 ≥5 帧（frame_id 从 1 连续）与 ≥1 音频块；
  4) 注入键盘输入 → input_ack 回显；
  5) 快照保存/回滚 → 回滚后 frame_id 回到保存点附近（证明 rollback 语义成立）；
  6) 主动停止 → stopped(ok, reason=user)；
  7) 未注册模拟器 → error(EMULATOR_NOT_FOUND)。

运行（在 repo 根目录）：
    python scripts/m0_check.py
可用环境变量 GW_TEST_PORT 覆盖测试端口（默认 17331，避免与开发端口 7331 冲突）。
退出码：0 = 全部通过；1 = 失败（打印失败明细与网关 stderr 尾部）。
"""

from __future__ import annotations

import json
import os
import queue
import socket
import subprocess
import sys
import threading
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PORT = 17331


def check(condition: bool, desc: str) -> None:
    if condition:
        print("  [PASS] %s" % desc)
    else:
        raise AssertionError(desc)


class GatewayClient:
    """极简 TCP JSON-lines 客户端：后台线程收包，recv(pred) 按序取消息。"""

    def __init__(self, port: int, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self._q: "queue.Queue[dict]" = queue.Queue()
        self._keep: list[dict] = []
        self._buf = ""
        self._dead = threading.Event()
        self.sock = socket.create_connection(("127.0.0.1", port), timeout=5.0)
        self.sock.settimeout(0.5)
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self) -> None:
        while not self._dead.is_set():
            try:
                data = self.sock.recv(65536)
            except socket.timeout:
                continue
            except OSError:
                break
            if not data:
                break
            self._buf += data.decode("utf-8", errors="replace")
            while "\n" in self._buf:
                line, self._buf = self._buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    self._q.put(json.loads(line))
                except json.JSONDecodeError:
                    pass  # 半行/垃圾行直接丢弃，测试另有超时兜底

    def send(self, obj: dict) -> None:
        payload = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
        self.sock.sendall(payload)

    def recv(self, pred, desc: str, timeout: float | None = None):
        """按序返回第一条满足 pred 的消息；不满足的按序暂存，后续调用可见。"""
        deadline = time.time() + (timeout if timeout is not None else self.timeout)
        while True:
            for idx, msg in enumerate(self._keep):
                if pred(msg):
                    return self._keep.pop(idx)
            try:
                msg = self._q.get(timeout=0.1)
            except queue.Empty:
                if time.time() > deadline:
                    raise AssertionError(
                        "超时等待 %s（已收到 %d 条不匹配消息）" % (desc, len(self._keep)))
                continue
            if pred(msg):
                return msg
            self._keep.append(msg)

    def close(self) -> None:
        self._dead.set()
        try:
            self.sock.close()
        except OSError:
            pass


def main() -> int:
    port = int(os.environ.get("GW_TEST_PORT", str(DEFAULT_PORT)))
    gateway_path = os.path.join(REPO_ROOT, "gw", "gateway.py")
    stderr_tail: list[str] = []

    gw_proc = subprocess.Popen(
        [sys.executable, gateway_path, "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace")

    def _drain_stderr() -> None:
        assert gw_proc.stderr is not None
        for raw in gw_proc.stderr:
            stderr_tail.append(raw.rstrip("\n"))
            if len(stderr_tail) > 200:
                stderr_tail.pop(0)

    threading.Thread(target=_drain_stderr, daemon=True).start()

    client: GatewayClient | None = None
    try:
        # ---- 等待网关就绪 ----
        deadline = time.time() + 10.0
        ready = False
        while time.time() < deadline:
            if gw_proc.poll() is not None:
                raise AssertionError("网关提前退出，退出码 %s" % gw_proc.returncode)
            try:
                probe = socket.create_connection(("127.0.0.1", port), timeout=0.5)
                probe.close()
                ready = True
                break
            except OSError:
                time.sleep(0.2)
        check(ready, "网关在端口 %d 就绪" % port)
        client = GatewayClient(port)

        # ---- 1) heartbeat ----
        client.send({"proto": 1, "type": "heartbeat"})
        ack = client.recv(lambda m: m.get("type") == "heartbeat_ack", "heartbeat_ack")
        check(isinstance(ack.get("running_devices"), dict),
              "heartbeat_ack 返回 running_devices=%r" % ack.get("running_devices"))

        # ---- 2) start_device ----
        client.send({"proto": 1, "type": "start_device", "emulator": "fake",
                     "device_id": "dev1",
                     "config": {"width": 96, "height": 64, "fps": 15}})
        start = client.recv(lambda m: m.get("type") == "start_device_ack",
                            "start_device_ack")
        check(start.get("ok") is True, "start_device_ack ok=true")
        check(start.get("device_id") == "dev1", "start_device_ack device_id=dev1")

        # ---- 3) 帧与音频 ----
        prev = 0
        for idx in range(5):
            frame = client.recv(
                lambda m: m.get("type") == "frame_ready" and m.get("device_id") == "dev1",
                "第 %d 帧" % (idx + 1))
            fid = frame.get("frame_id")
            check(fid == prev + 1, "帧序号连续：frame_id=%s（前一张=%s）" % (fid, prev))
            check(frame.get("format") == "rgb8" and isinstance(frame.get("data_b64"), str),
                  "帧格式 rgb8 且携带 data_b64")
            prev = fid
        check(prev >= 5, "连续收到 5 帧（最大 frame_id=%s）" % prev)
        audio = client.recv(
            lambda m: m.get("type") == "audio_chunk" and m.get("device_id") == "dev1",
            "audio_chunk")
        check(audio.get("format") == "s16le" and audio.get("seq", 0) >= 1,
              "收到音频块：seq=%s, format=s16le" % audio.get("seq"))

        # ---- 4) 输入注入 ----
        client.send({"proto": 1, "type": "input_event", "device_id": "dev1",
                     "map": "keyboard", "key": "a", "value": True})
        inp = client.recv(
            lambda m: m.get("type") == "input_ack" and m.get("device_id") == "dev1",
            "input_ack")
        check(inp.get("key") == "a" and inp.get("value") is True,
              "input_ack 回显 key=a value=true")

        # ---- 5) 快照保存 / 回滚 ----
        client.send({"proto": 1, "type": "save_state", "device_id": "dev1", "id": "s1"})
        save_ack = client.recv(
            lambda m: m.get("type") == "save_state_ack" and m.get("device_id") == "dev1",
            "save_state_ack")
        save_pt = save_ack.get("frame_id")
        check(isinstance(save_pt, int) and save_pt >= 1,
              "save_state_ack.frame_id=%r" % save_pt)
        # 让帧继续走一段
        max_after = save_pt
        while max_after <= save_pt + 5:
            frame = client.recv(
                lambda m: m.get("type") == "frame_ready" and m.get("device_id") == "dev1",
                "快照后的帧（用于证明在继续推进）")
            max_after = max(max_after, frame.get("frame_id"))
        check(max_after >= save_pt + 6, "快照后帧继续推进到 %s" % max_after)
        # 回滚
        client.send({"proto": 1, "type": "load_state", "device_id": "dev1", "id": "s1"})
        load_ack = client.recv(
            lambda m: m.get("type") == "load_state_ack" and m.get("device_id") == "dev1",
            "load_state_ack")
        check(load_ack.get("frame_id") == save_pt,
              "load_state_ack.frame_id=%s == 保存点 %s"
              % (load_ack.get("frame_id"), save_pt))
        frame = client.recv(
            lambda m: m.get("type") == "frame_ready" and m.get("device_id") == "dev1",
            "回滚后的第一帧")
        next_fid = frame.get("frame_id")
        check(next_fid >= save_pt + 1 and next_fid <= save_pt + 3 and next_fid < max_after,
              "回滚生效：回滚后第一帧 frame_id=%s（保存点 %s，回滚前已达 %s）"
              % (next_fid, save_pt, max_after))

        # ---- 6) 停止 ----
        client.send({"proto": 1, "type": "stop", "device_id": "dev1"})
        stopped = client.recv(
            lambda m: m.get("type") == "stopped" and m.get("device_id") == "dev1",
            "stopped")
        check(stopped.get("ok") is True and stopped.get("reason") == "user",
              "stopped ok=true reason=user")

        # ---- 7) 未注册模拟器 ----
        client.send({"proto": 1, "type": "start_device", "emulator": "nonexistent",
                     "device_id": "bad"})
        err = client.recv(lambda m: m.get("type") == "error", "error(EMULATOR_NOT_FOUND)")
        check(err.get("code") == "EMULATOR_NOT_FOUND",
              "未注册模拟器返回 EMULATOR_NOT_FOUND")

        print("\nM0 验收全部通过 ✔")
        return 0
    except AssertionError as exc:
        _dump_gateway_tail(stderr_tail)
        print("\nM0 验收失败 ✘  ->  %s" % exc)
        return 1
    except OSError as exc:
        _dump_gateway_tail(stderr_tail)
        print("\nM0 验收失败（网络/进程错误）✘  ->  %s" % exc)
        return 1
    finally:
        if client is not None:
            client.close()
        if gw_proc.poll() is None:
            gw_proc.terminate()
            try:
                gw_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gw_proc.kill()


def _dump_gateway_tail(lines: list[str]) -> None:
    print("\n网关 stderr 尾部:")
    if not lines:
        print("  (空)")
    for line in lines[-40:]:
        print("  | " + line)


if __name__ == "__main__":
    sys.exit(main())