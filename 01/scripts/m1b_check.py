# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""M1b 验收：内容包 runtime → 网关 的映射桥（TASK-11B，对应 run_profile.py）。

对三个真实内容包执行：
  1) run_profile --json 映射正确性（sinks 映射 / 键名校验 / demo_mode 判定 / 缺省画面值）：
     - manchester-baby：early-computer → 320x200@25；sinks 含 main+led+speaker；36 键全合法；
     - apple-ii：computer → 320x240@24；sinks 含 main+speaker+led；≥50 键全合法；
     - eniac：emulator=none → demo_mode，不起设备；
  2) 对 baby 与 apple-ii：用映射出的 config 经网关启动 fake 设备 → ack 回显 sinks →
     注入 input_map 首键 → input_ack 回显一致 → stop。
退出码：0=全过；1=失败（贴网关 stderr 尾部）。回归：m0/m1 另行运行（见完成报告）。
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
WORK_ROOT = os.path.dirname(os.path.dirname(REPO_ROOT))  # D:\work（内容包在 03/05 线）

DEFAULT_PORT = 17334

PKGS = {
    "baby": os.path.join(WORK_ROOT, "03", "repo", "content", "manchester-baby"),
    "eniac": os.path.join(WORK_ROOT, "03", "repo", "content", "eniac"),
    "apple-ii": os.path.join(WORK_ROOT, "05", "repo", "content", "apple-ii"),
}

PASSED = 0


def check(condition: bool, desc: str) -> None:
    global PASSED
    if condition:
        PASSED += 1
        print("  [PASS] %s" % desc)
    else:
        raise AssertionError(desc)


class GatewayClient:
    """极简 TCP JSON-lines 客户端（同 m0/m1_check）。"""

    def __init__(self, port: int, timeout: float = 20.0) -> None:
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
                if line:
                    try:
                        self._q.put(json.loads(line))
                    except json.JSONDecodeError:
                        pass

    def send(self, obj: dict) -> None:
        self.sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))

    def recv(self, pred, desc: str, timeout: float | None = None):
        deadline = time.time() + (timeout if timeout is not None else self.timeout)
        while True:
            for idx, msg in enumerate(self._keep):
                if pred(msg):
                    return self._keep.pop(idx)
            try:
                msg = self._q.get(timeout=0.1)
            except queue.Empty:
                if time.time() > deadline:
                    raise AssertionError("超时等待 %s（keep %d 条）" % (desc, len(self._keep)))
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


def run_profile(pkg_dir: str) -> dict:
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO_ROOT, "scripts", "run_profile.py"),
         pkg_dir, "--json"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=REPO_ROOT, timeout=60)
    if proc.returncode != 0:
        raise AssertionError("run_profile 失败: %s\n%s" % (pkg_dir, proc.stderr))
    return json.loads(proc.stdout)


def start_and_check(client: GatewayClient, mapping: dict, tag: str) -> None:
    did = mapping["device_id"] + "-m1b"
    client.send({"type": "start_device", "emulator": "fake", "device_id": did,
                 "config": mapping["config"]})
    ack = client.recv(lambda m: m.get("type") == "start_device_ack"
                      and m.get("device_id") == did, "start_device_ack(%s)" % tag)
    check(ack.get("ok") is True, "%s：fake 设备启动 ok（sinks=%s）"
          % (tag, ack.get("info", {}).get("sinks")))
    check(ack.get("info", {}).get("sinks") == mapping["config"]["sinks"],
          "%s：ack 回显 sinks 与映射一致" % tag)
    first = mapping["first_key"]
    client.send({"type": "input_event", "device_id": did,
                 "map": "keyboard", "key": first["action"], "value": True})
    inp = client.recv(lambda m: m.get("type") == "input_ack"
                      and m.get("device_id") == did, "input_ack(%s)" % tag)
    check(inp.get("key") == first["action"] and inp.get("value") is True,
          "%s：input_map 首键 %s 注入回显一致" % (tag, first["action"]))
    client.send({"type": "stop", "device_id": did})
    stopped = client.recv(lambda m: m.get("type") == "stopped"
                          and m.get("device_id") == did, "stopped(%s)" % tag)
    check(stopped.get("ok") is True, "%s：停止正常" % tag)


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
        check(ready, "网关就绪（端口 %d）" % port)
        client = GatewayClient(port)

        # ---- 1) 映射正确性（三个包）----
        m_baby = run_profile(PKGS["baby"])
        m_apple = run_profile(PKGS["apple-ii"])
        m_eniac = run_profile(PKGS["eniac"])

        check(m_eniac.get("demo_mode") is True, "eniac：demo_mode 判定正确（emulator=none）")
        check(m_eniac.get("config", {}).get("sinks", []) == ["led"],
              "eniac：indicator_lamps → led 映射正确")

        baby_sinks = m_baby["config"]["sinks"]
        check(set(baby_sinks) == {"main", "led", "speaker"},
              "manchester-baby：sink 映射 main+led+speaker（实际 %s）" % baby_sinks)
        check(m_baby["config"]["width"] == 320 and m_baby["config"]["height"] == 200
              and m_baby["config"]["fps"] == 25,
              "manchester-baby：early-computer 缺省画面 320x200@25")
        check(m_baby["keys"]["total"] == 36 and len(m_baby["keys"]["unknown"]) == 0,
              "manchester-baby：36 键全部合法（未知 %d）" % len(m_baby["keys"]["unknown"]))
        check(m_baby["first_key"]["action"] == "power"
              and m_baby["first_key"]["token"] == "panel.power",
              "manchester-baby：首键 power -> panel.power")

        apple_sinks = m_apple["config"]["sinks"]
        check(set(apple_sinks) == {"main", "speaker", "led"},
              "apple-ii：sink 映射 main+speaker+led（实际 %s）" % apple_sinks)
        check(m_apple["config"]["width"] == 320 and m_apple["config"]["height"] == 240
              and m_apple["config"]["fps"] == 24,
              "apple-ii：computer 缺省画面 320x240@24")
        check(m_apple["keys"]["total"] >= 50 and len(m_apple["keys"]["unknown"]) == 0,
              "apple-ii：%d 键全部合法（未知 %d）"
              % (m_apple["keys"]["total"], len(m_apple["keys"]["unknown"])))
        afk = m_apple["first_key"] or {}
        check(afk.get("action") == "key_a" and afk.get("map") == "keyboard"
              and afk.get("key") == "KEY_A",
              "apple-ii：首键 key_a -> {keyboard: KEY_A}（对象形态）")

        # ---- 2) 经网关用映射配置真实起设备 ----
        start_and_check(client, m_baby, "manchester-baby")
        start_and_check(client, m_apple, "apple-ii")

        print("\nM1b 验收全部通过 ✔（断言 %d 条）" % PASSED)
        return 0
    except (AssertionError, OSError, TimeoutError) as exc:
        print("\n网关 stderr 尾部:")
        for line in stderr_tail[-30:]:
            print("  | " + line)
        print("\nM1b 验收失败 ✘  ->  %s" % exc)
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


if __name__ == "__main__":
    sys.exit(main())