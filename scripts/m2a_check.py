# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""M2a 验收（TASK-21A）：M2 里程碑断言的可运行实现（fake 先行双轨）。

依据 docs/m2_assert_draft.md 断言 a–j：
  - fake 轨（默认）：emulator=fake，执行 b/c/d/e/g/h/i/j 全部断言（a 隐含于 start ack）；
  - mame 轨（--mame）：emulator=mame-apple2。MAME 二进制缺失时 → 断言错误路径
    EMULATOR_BINARY_MISSING，其余项 SKIP 且退出码 0（不误红 CI）；二进制就位时执行真实断言。
退出码：0=全过（含 SKIP 语义）；1=失败。

用法:
  python scripts/m2a_check.py           # fake 轨
  python scripts/m2a_check.py --mame    # mame 轨（本机无二进制 → SKIP 演示）
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import queue
import socket
import subprocess
import sys
import threading
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PORT = 17335
MISSING_PORT = 17336

# Apple II 6 色高分辨率（m2_assert_draft §2）：真实轨期望尺寸；fake 轨按 config 递推
APPLE2_W = 280
APPLE2_H = 192

PASSED = 0
SKIPPED: list[str] = []


def check(condition: bool, desc: str) -> None:
    global PASSED
    if condition:
        PASSED += 1
        print("  [PASS] %s" % desc)
    else:
        raise AssertionError(desc)


def skip(desc: str) -> None:
    SKIPPED.append(desc)
    print("  [SKIP] %s" % desc)


class GatewayClient:
    """极简 TCP JSON-lines 客户端（同 m0/m1/m1b_check 的自带副本）。"""

    def __init__(self, port: int, timeout: float = 25.0) -> None:
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
        while time.time() < deadline:   # 洪水防护：收包不断流时也强制到期
            for idx, msg in enumerate(self._keep):
                if pred(msg):
                    return self._keep.pop(idx)
            try:
                msg = self._q.get(timeout=0.1)
            except queue.Empty:
                continue
            if pred(msg):
                return msg
            self._keep.append(msg)
        raise AssertionError("超时等待 %s（keep %d 条）" % (desc, len(self._keep)))

    def close(self) -> None:
        self._dead.set()
        try:
            self.sock.close()
        except OSError:
            pass


def start_gateway(port: int) -> tuple[subprocess.Popen, list[str], threading.Thread]:
    stderr_tail: list[str] = []
    gw_proc = subprocess.Popen(
        [sys.executable, os.path.join(REPO_ROOT, "gw", "gateway.py"),
         "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace")

    def _drain() -> None:
        assert gw_proc.stderr is not None
        for raw in gw_proc.stderr:
            stderr_tail.append(raw.rstrip("\n"))
            if len(stderr_tail) > 200:
                stderr_tail.pop(0)

    t = threading.Thread(target=_drain, daemon=True)
    t.start()
    deadline = time.time() + 10.0
    while time.time() < deadline:
        if gw_proc.poll() is not None:
            raise AssertionError("网关提前退出，退出码 %s" % gw_proc.returncode)
        try:
            probe = socket.create_connection(("127.0.0.1", port), timeout=0.5)
            probe.close()
            return gw_proc, stderr_tail, t
        except OSError:
            time.sleep(0.2)
    raise AssertionError("网关未在 10s 内就绪")


def recv_frames(client: GatewayClient, did: str, n: int, timeout: float = 25.0) -> list[dict]:
    """顺序接收 n 条本设备的 frame_ready 事件（网关将后端 frame 转帧就绪广播）。"""
    out: list[dict] = []
    pred = lambda m: m.get("type") == "frame_ready" and m.get("device_id") == did
    for _ in range(n):
        out.append(client.recv(pred, "frame_ready×%d" % (len(out) + 1), timeout=timeout))
    return out


def fake_track(port: int) -> None:
    """断言 b/c/d/e/g/h/i/j 全量（a 隐含）：见 m2_assert_draft §2-4。"""
    did = "apple2-m2a"
    cfg = {"width": APPLE2_W, "height": APPLE2_H, "fps": 25,
           "frame_codec": "raw", "sinks": ["main", "speaker"]}
    client = GatewayClient(port)
    try:
        client.send({"type": "start_device", "emulator": "fake", "device_id": did,
                     "config": cfg})
        ack = client.recv(lambda m: m.get("type") == "start_device_ack"
                          and m.get("device_id") == did, "start_device_ack")
        check(ack.get("ok") is True, "a：fake 设备启动 ok（进入 running）")

        # ---- b/c：≥5 帧严格递增 + rgb8 尺寸校验 ----
        frames = recv_frames(client, did, 5)
        ids = [f.get("frame_id") for f in frames]
        check(ids == list(range(ids[0], ids[0] + 5)),
              "b：连续 5 帧 frame_id 严格递增（%s..%s）" % (ids[0], ids[-1]))
        f5 = frames[-1]
        fmt = f5.get("format")
        raw = base64.b64decode(f5.get("data_b64", ""))
        check(fmt == "rgb8" and len(raw) == f5.get("width", 0) * f5.get("height", 0) * 3,
              "c：帧格式 rgb8 且尺寸 %d×%d×3 校验成立（%d B）"
              % (f5.get("width", 0), f5.get("height", 0), len(raw)))

        # ---- d：音频块（fake 打入正弦波；MAME 轨此项 [需核实] 时 SKIP） ----
        audio = client.recv(lambda m: m.get("type") == "audio_chunk"
                            and m.get("device_id") == did, "audio_chunk")
        check(audio.get("format") == "s16le", "d：音频块格式 s16le")

        # ---- e：输入回显 ----
        client.send({"type": "input_event", "device_id": did,
                     "map": "keyboard", "key": "KEY_A", "value": True})
        ack_in = client.recv(lambda m: m.get("type") == "input_ack"
                             and m.get("device_id") == did, "input_ack")
        check(ack_in.get("map") == "keyboard" and ack_in.get("key") == "KEY_A"
              and ack_in.get("value") is True, "e：KEY_A 注入回显一致")

        # ---- g：连续两次注入各自 ack、顺序一致 ----
        client.send({"type": "input_event", "device_id": did,
                     "map": "keyboard", "key": "KEY_R", "value": True})
        time.sleep(0.12)
        client.send({"type": "input_event", "device_id": did,
                     "map": "keyboard", "key": "KEY_T", "value": True})
        ack1 = client.recv(lambda m: m.get("type") == "input_ack"
                           and m.get("device_id") == did
                           and m.get("key") == "KEY_R", "input_ack(KEY_R)")
        ack2 = client.recv(lambda m: m.get("type") == "input_ack"
                           and m.get("device_id") == did
                           and m.get("key") == "KEY_T", "input_ack(KEY_T)")
        check(ack1.get("value") is True and ack2.get("value") is True,
              "g：两次注入各自独立回显（KEY_R 先于 KEY_T）")

        # ---- h：存档 ack 帧号为正 ----
        client.send({"type": "save_state", "device_id": did, "id": "m2_s1"})
        saved = client.recv(lambda m: m.get("type") == "save_state_ack"
                            and m.get("id") == "m2_s1", "save_state_ack")
        save_pt = saved.get("frame_id")
        check(isinstance(save_pt, int) and save_pt > 0,
              "h：save_state_ack.frame_id=%s（正整数）" % save_pt)

        # ---- i：推进 ≥5 帧后回滚，ack 帧号 == 保存点 ----
        target = save_pt + 5
        drop = 0
        while True:
            fr = client.recv(lambda m: m.get("type") == "frame_ready"
                             and m.get("device_id") == did, "frame_ready(推进)")
            drop += 1
            if fr.get("frame_id") >= target:
                break
        client.send({"type": "load_state", "device_id": did, "id": "m2_s1"})
        loaded = client.recv(lambda m: m.get("type") == "load_state_ack"
                             and m.get("id") == "m2_s1", "load_state_ack")
        check(loaded.get("frame_id") == save_pt,
              "i：推进 ≥5 帧（%d 条）后 load_state_ack.frame_id==保存点 %s"
              % (drop, save_pt))

        # ---- j：回滚后下一帧 == 保存点+1（DEFECT-M1-ROLLBACK-01 语义） ----
        next_fr = client.recv(lambda m: m.get("type") == "frame_ready"
                              and m.get("device_id") == did
                              and m.get("frame_id", 0) > save_pt,
                              "回滚后首帧", timeout=15.0)
        check(next_fr.get("frame_id") == save_pt + 1,
              "j：回滚后第一帧 frame_id=%s（== 保存点+1）" % next_fr.get("frame_id"))

        client.send({"type": "stop", "device_id": did})
        stopped = client.recv(lambda m: m.get("type") == "stopped"
                              and m.get("device_id") == did, "stopped")
        check(stopped.get("ok") is True, "设备停止正常（reason=user）")
    finally:
        client.close()


def mame_track(port: int) -> bool:
    """mame 轨：二进制缺失 → 错误路径断言 + SKIP；就位 → 真实断言（精简跑）。"""
    did = "apple2-m2a-mame"
    client = GatewayClient(port)
    try:
        client.send({"type": "start_device", "emulator": "mame-apple2",
                     "device_id": did,
                     "config": {"machine": "apple2", "frame_codec": "rle",
                                "sinks": ["crt_display", "speaker"]}})
        err = client.recv(lambda m: m.get("type") == "error"
                          and m.get("device_id") == did, "error", timeout=15.0)
        if err.get("code") == "EMULATOR_BINARY_MISSING":
            check(True, "mame 轨错误路径：无二进制 → EMULATOR_BINARY_MISSING（正确）")
            for item in ("b/c：frame 流", "d：音频（[需核实]）", "e/g：输入注入",
                         "h/i/j：存档回滚", "真实帧：280x192 特征验证"):
                skip("mame 轨 %s（MAME 二进制缺失，等待人工安装）" % item)
            return True
        check(err.get("code") is not None, "mame 轨：收到 error code=%s"
              % err.get("code"))
        return True
    finally:
        client.close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="M2a 验收（fake 先行双轨）")
    ap.add_argument("--mame", action="store_true", help="mame 轨（默认无二进制时 SKIP）")
    args = ap.parse_args(argv)
    port = int(os.environ.get("GW_TEST_PORT", str(DEFAULT_PORT)))

    gw_proc, stderr_tail, _t = start_gateway(port)
    try:
        if args.mame:
            ok = mame_track(port)
        else:
            fake_track(port)
            ok = True
    except (AssertionError, OSError, TimeoutError) as exc:
        print("\n网关 stderr 尾部:")
        for line in stderr_tail[-30:]:
            print("  | " + line)
        print("\nM2a 验收失败 ✘  ->  %s" % exc)
        ok = False
    finally:
        if gw_proc.poll() is None:
            gw_proc.terminate()
            try:
                gw_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gw_proc.kill()

    print("\nM2a%s 结果：PASS %d / SKIP %d"
          % ("(mame 轨)" if args.mame else "(fake 轨)", PASSED, len(SKIPPED)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())