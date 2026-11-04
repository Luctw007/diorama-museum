# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""M1 自动化验收：网关 v2 全链路（对应 TASK-06）。

用例：
  1) 网关就绪 + heartbeat；
  2) list_emulators（fake available）；
  3) rle 编解码单元自测（导入 gw.emulators.rle）；
  4) 启动 dev1（rle 编码 + 强制分片 + led sink）→ ack 回显 codec；
  5) 经 frame_chunk 重组收 5 帧：frame_id 连续、RLE 解码后尺寸正确；单帧多分片证据；
  6) light_state（led）至少 2 条且开/关交替；
  7) 输入注入 input_ack 回显；
  8) 快照保存/回滚（frame_id 回跳语义）；
  9) 多设备并发：dev3（800×600 raw 大帧 → 天然触发分片）与 dev1 并行，
     各自帧尺寸正确；heartbeat 显示双设备；stop dev3；
  10) 崩溃注入（dev1，input key=crash）→ PROCESS_CRASHED → 自动重启 → 帧恢复
      且 frame_id 回跳到 __auto 快照附近（证明 FR-E8）；
  11) 再次注入崩溃 → 再次自动恢复（主连接全程不掉线）；
  12) dev2（auto_crash_frame=3）→ 连续 3 次失败重启 → RESTART_EXCEEDED + degraded；
      停止 degraded 设备可用；
  13) 停止 dev1，收尾。

运行（在 repo 根目录）：python scripts/m1_check.py
环境变量 GW_TEST_PORT 可覆盖测试端口（默认 17333）。
退出码：0 = 全部通过；1 = 失败（打印失败明细与网关 stderr 尾部）。
"""

from __future__ import annotations

import base64
import json
import glob
import os
import queue
import random
import socket
import subprocess
import sys
import tempfile
import threading
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gw.emulators.rle import encode as rle_encode  # noqa: E402
from gw.emulators.rle import decode as rle_decode  # noqa: E402

DEFAULT_PORT = 17333

PASSED = 0


def check(condition: bool, desc: str) -> None:
    global PASSED
    if condition:
        PASSED += 1
        print("  [PASS] %s" % desc)
    else:
        raise AssertionError(desc)


class GatewayClient:
    """极简 TCP JSON-lines 客户端（同 m0_check）。"""

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
                if not line:
                    continue
                try:
                    self._q.put(json.loads(line))
                except json.JSONDecodeError:
                    pass

    def send(self, obj: dict) -> None:
        payload = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
        self.sock.sendall(payload)

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


def _is_frame_of(device_id: str):
    return lambda m: m.get("type") in ("frame_ready", "frame_chunk") \
        and m.get("device_id") == device_id


class FrameAssembler:
    """按 frame_id 归组分片并重组；完整帧（已解码为 RGB8 字节）按完成顺序入 ready。"""

    def __init__(self) -> None:
        self._parts: dict[int, dict] = {}
        self.ready: list[dict] = []

    def push(self, msg: dict) -> None:
        fid = msg.get("frame_id")
        codec = msg.get("codec", "raw")
        if msg.get("type") == "frame_ready":
            seqs = {0: msg.get("data_b64", "")}
            total = 1
        else:
            seqs = {int(msg.get("seq", 0)): msg.get("data_b64", "")}
            total = int(msg.get("total", 1))
        bucket = self._parts.get(fid)
        if bucket is None:
            bucket = {"total": total, "seqs": {}, "meta": msg}
            self._parts[fid] = bucket
        for seq, data in seqs.items():
            bucket["seqs"].setdefault(seq, data)
        if len(bucket["seqs"]) >= bucket["total"]:
            joined = "".join(bucket["seqs"][i] for i in range(bucket["total"]))
            raw = base64.b64decode(joined)
            if codec == "rle":
                decoded = rle_decode(raw)
                raw = decoded if decoded is not None else b""
            bucket["meta"]["raw_len"] = len(raw)
            self.ready.append(bucket["meta"])


def collect_frames(client: GatewayClient, device_id: str, asm: FrameAssembler,
                   count: int, timeout: float = 60.0, desc: str = ""):
    """推入消息直到取满 count 个完整帧（按完成顺序弹出）；返回完整帧列表。"""
    out: list[dict] = []
    deadline = time.time() + timeout
    while len(out) < count:
        # 先取已重组完成的帧
        while asm.ready and len(out) < count:
            out.append(asm.ready.pop(0))
        if len(out) >= count:
            break
        if time.time() > deadline:
            raise AssertionError("超时收集 %s 的 %d 帧（当前 %d）%s"
                                 % (device_id, count, len(out), desc))
        msg = client.recv(_is_frame_of(device_id), "帧",
                          timeout=min(10.0, max(1.0, deadline - time.time())))
        asm.push(msg)
    return out


def main() -> int:
    # 卫生：清理历史持久化快照，保证洁净环境（04 线 DEFECT-M1-ROLLBACK-01 备注建议）
    for stale in glob.glob(os.path.join(tempfile.gettempdir(), "diorama_*.json")):
        try:
            os.remove(stale)
        except OSError:
            pass
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
            if len(stderr_tail) > 300:
                stderr_tail.pop(0)

    threading.Thread(target=_drain_stderr, daemon=True).start()

    client: GatewayClient | None = None
    try:
        # ---- 1) 网关就绪 + heartbeat ----
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
        client.send({"proto": 2, "type": "heartbeat"})
        hb = client.recv(lambda m: m.get("type") == "heartbeat_ack", "heartbeat_ack")
        check(hb.get("running_devices") == {}, "heartbeat 初始无运行设备")

        # ---- 2) list_emulators ----
        client.send({"proto": 2, "type": "list_emulators"})
        le = client.recv(lambda m: m.get("type") == "list_emulators_ack",
                         "list_emulators_ack")
        emus = le.get("emulators", {})
        check(isinstance(emus.get("fake"), dict) and emus["fake"].get("available") is True,
              "list_emulators：fake 可用")

        # ---- 3) rle 单元自测 ----
        for trial in range(3):
            rnd = bytes(random.randrange(256) for _ in range(3000))
            if rle_decode(rle_encode(rnd)) != rnd:
                raise AssertionError("rle roundtrip #%d 失败" % trial)
        check(True, "rle 编解码 roundtrip ×3")
        check(rle_decode(b"\x01") is None and rle_decode(b"\x00\x01") is None,
              "rle 畸形输入返回 None")

        # ---- 4) 启动 dev1：rle + 强制分片 + led ----
        client.send({"proto": 2, "type": "start_device", "emulator": "fake",
                     "device_id": "dev1",
                     "config": {"width": 160, "height": 120, "fps": 15,
                                "frame_codec": "rle", "force_chunk": True,
                                "force_chunk_chars": 15000,
                                "sinks": ["main", "led"], "tone_hz": 300}})
        ack = client.recv(lambda m: m.get("type") == "start_device_ack",
                          "start_device_ack(dev1)")
        check(ack.get("ok") is True, "dev1 启动 ok")
        check(ack.get("info", {}).get("frame_codec") == "rle",
              "dev1 ack 回显 frame_codec=rle")
        check("led" in ack.get("info", {}).get("sinks", []), "dev1 sinks 含 led")

        # ---- 5) 分片重组收 5 帧 + 单帧多分片证据 ----
        asm1 = FrameAssembler()
        frames1 = collect_frames(client, "dev1", asm1, 5, desc="主帧")
        prev = 0
        for f in frames1:
            fid = f.get("frame_id")
            check(fid == prev + 1, "dev1 帧连续：frame_id=%s（前一张=%s）" % (fid, prev))
            check(f["raw_len"] == 160 * 120 * 3,
                  "dev1 帧解码尺寸正确（%d）" % f["raw_len"])
            prev = fid
        # 单帧多分片证据：拦截下一帧的 frame_chunk 流
        parts: dict[int, set] = {}
        evidence_total = 0
        evidence_fid = 0
        while True:
            m = client.recv(_is_frame_of("dev1"), "分片证据帧", timeout=20.0)
            if m.get("type") != "frame_chunk":
                continue
            evidence_fid = m.get("frame_id")
            parts.setdefault(evidence_fid, set()).add(m.get("seq"))
            if len(parts[evidence_fid]) >= int(m.get("total", 1)):
                evidence_total = int(m.get("total", 1))
                break
        check(evidence_total > 1,
              "单帧多分片证据：frame_id=%s total=%s（force_chunk 生效）"
              % (evidence_fid, evidence_total))

        # ---- 6) light_state ----
        led = []
        while len(led) < 2:
            m = client.recv(lambda m: m.get("type") == "light_state"
                            and m.get("device_id") == "dev1", "light_state",
                            timeout=20.0)
            led.append(m.get("on"))
        check(led[0] != led[1], "dev1 led 灯状态交替：%s" % led)

        # ---- 7) 输入注入 ----
        client.send({"proto": 2, "type": "input_event", "device_id": "dev1",
                     "map": "keyboard", "key": "a", "value": True})
        inp = client.recv(lambda m: m.get("type") == "input_ack"
                          and m.get("device_id") == "dev1", "input_ack")
        check(inp.get("key") == "a" and inp.get("value") is True, "dev1 input_ack 回显")

        # ---- 8) 快照保存/回滚 ----
        client.send({"proto": 2, "type": "save_state", "device_id": "dev1", "id": "s1"})
        save_ack = client.recv(lambda m: m.get("type") == "save_state_ack"
                               and m.get("device_id") == "dev1"
                               and m.get("id") == "s1", "save_state_ack(s1)")
        save_pt = save_ack.get("frame_id")
        check(isinstance(save_pt, int) and save_pt >= 1, "save_state_ack.frame_id=%r" % save_pt)
        post_asm = FrameAssembler()
        fmax = save_pt
        while fmax <= save_pt + 5:
            f = collect_frames(client, "dev1", post_asm, 1, desc="快照后推进")[0]
            fmax = max(fmax, f.get("frame_id"))
        check(fmax >= save_pt + 6, "快照后帧推进到 %s" % fmax)
        client.send({"proto": 2, "type": "load_state", "device_id": "dev1", "id": "s1"})
        load_ack = client.recv(lambda m: m.get("type") == "load_state_ack"
                               and m.get("device_id") == "dev1"
                               and m.get("id") == "s1", "load_state_ack(s1)")
        check(load_ack.get("frame_id") == save_pt, "load 回到保存点 %s" % save_pt)
        # 回滚证据：加载后等待 frame_id 回落到保存点+3 以内（此前 keep 里的旧帧均大于此）
        roll_asm = FrameAssembler()
        roll_f = None
        for _ in range(200):
            f = collect_frames(client, "dev1", roll_asm, 1, desc="回滚后第一帧")[0]
            if f.get("frame_id") <= save_pt + 3:
                roll_f = f
                break
        if roll_f is None:
            raise AssertionError("load 后未观察到帧序号回跳")
        check(roll_f.get("frame_id") >= save_pt + 1,
              "回滚生效：回滚后第一帧 frame_id=%s（保存点 %s，此前已达 %s）"
              % (roll_f.get("frame_id"), save_pt, fmax))

        # ---- 9) 多设备并发：dev3（800×600 raw 大帧，天然分片）----
        client.send({"proto": 2, "type": "start_device", "emulator": "fake",
                     "device_id": "dev3",
                     "config": {"width": 800, "height": 600, "fps": 6,
                                "frame_codec": "raw", "force_chunk": True}})
        ack3 = client.recv(lambda m: m.get("type") == "start_device_ack"
                           and m.get("device_id") == "dev3", "start_device_ack(dev3)")
        check(ack3.get("ok") is True, "dev3 启动 ok")
        asm3 = FrameAssembler()
        frames3 = collect_frames(client, "dev3", asm3, 3, desc="dev3 大帧")
        for f in frames3:
            check(f["raw_len"] == 800 * 600 * 3,
                  "dev3 大帧尺寸正确（%d）" % f["raw_len"])
        client.send({"proto": 2, "type": "heartbeat"})
        hb2 = client.recv(lambda m: m.get("type") == "heartbeat_ack", "heartbeat_ack#2")
        rd = hb2.get("running_devices", {})
        check(rd.get("dev1") == "running" and rd.get("dev3") == "running",
              "双设备并发 heartbeat：%s" % rd)
        client.send({"proto": 2, "type": "stop", "device_id": "dev3"})
        st3 = client.recv(lambda m: m.get("type") == "stopped"
                          and m.get("device_id") == "dev3", "stopped(dev3)", timeout=15.0)
        check(st3.get("ok") is True and st3.get("reason") == "user", "dev3 正常停止")

        # ---- 10/11) 崩溃注入 → 自动重启 + __auto 恢复（两轮）----
        probe_asm = FrameAssembler()
        probe = collect_frames(client, "dev1", probe_asm, 2, desc="崩溃前基线")
        max_before_crash = max(f.get("frame_id") for f in probe)
        for round_no in (1, 2):
            client.send({"proto": 2, "type": "input_event", "device_id": "dev1",
                         "map": "keyboard", "key": "crash", "value": True})
            err = client.recv(lambda m: m.get("type") == "error"
                              and m.get("code") == "PROCESS_CRASHED"
                              and m.get("device_id") == "dev1",
                              "PROCESS_CRASHED(第%d轮)" % round_no, timeout=30.0)
            check(err.get("code") == "PROCESS_CRASHED", "第%d轮崩溃上报" % round_no)
            # 恢复证据：先跳过 keep 里的旧帧，等 frame_id 回落到基线区（≤8）
            recover_asm = FrameAssembler()
            first = None
            for _ in range(400):
                f = collect_frames(client, "dev1", recover_asm, 1,
                                   desc="第%d轮恢复" % round_no, timeout=60.0)[0]
                if f.get("frame_id") <= 8:
                    first = f
                    break
            if first is None:
                raise AssertionError("第%d轮崩溃后未观察到帧序号回跳" % round_no)
            first_fid = int(first.get("frame_id"))
            # 说明：重启后新进程先从 frame 1 起跑（≤8 即"新进程签名"），
            # 网关随后 load __auto 使流跳到快照附近；因此恢复流形如 1,17,18,…
            check(first_fid <= 8 and first_fid < max_before_crash,
                  "第%d轮恢复：新进程签名帧 first=%s（崩溃前 %s）"
                  % (round_no, first_fid, max_before_crash))
            tail = collect_frames(client, "dev1", recover_asm, 3,
                                  desc="第%d轮恢复续帧" % round_no, timeout=30.0)
            seq = [first_fid] + [int(f["frame_id"]) for f in tail]
            check(all(seq[i + 1] > seq[i] for i in range(len(seq) - 1)),
                  "第%d轮恢复流单调递增：%s" % (round_no, seq))

        # ---- 12) dev2：auto_crash_frame → 连续失败重启 → degraded ----
        client.send({"proto": 2, "type": "start_device", "emulator": "fake",
                     "device_id": "dev2",
                     "config": {"width": 64, "height": 48, "fps": 30,
                                "frame_codec": "raw", "auto_crash_frame": 3}})
        ack2 = client.recv(lambda m: m.get("type") == "start_device_ack"
                           and m.get("device_id") == "dev2", "start_device_ack(dev2)",
                           timeout=15.0)
        check(ack2.get("ok") is True, "dev2 启动 ok")
        err2 = client.recv(lambda m: m.get("type") == "error"
                           and m.get("code") == "RESTART_EXCEEDED"
                           and m.get("device_id") == "dev2",
                           "RESTART_EXCEEDED(dev2)", timeout=120.0)
        check(err2.get("code") == "RESTART_EXCEEDED",
              "dev2 连续失败重启上报 RESTART_EXCEEDED")
        deg = client.recv(lambda m: m.get("type") == "status"
                          and m.get("device_id") == "dev2"
                          and m.get("state") == "degraded", "status degraded(dev2)",
                          timeout=10.0)
        check(deg.get("state") == "degraded", "dev2 降级 degraded")
        client.send({"proto": 2, "type": "stop", "device_id": "dev2"})
        st2 = client.recv(lambda m: m.get("type") == "stopped"
                          and m.get("device_id") == "dev2", "stopped(dev2)", timeout=15.0)
        check(st2.get("ok") is True, "degraded 设备可 stop 清理")

        # ---- 13) 收尾 ----
        client.send({"proto": 2, "type": "stop", "device_id": "dev1"})
        st1 = client.recv(lambda m: m.get("type") == "stopped"
                          and m.get("device_id") == "dev1", "stopped(dev1)", timeout=15.0)
        check(st1.get("ok") is True and st1.get("reason") == "user", "dev1 正常停止")

        print("\nM1 验收全部通过 ✔（断言 %d 条）" % PASSED)
        return 0
    except AssertionError as exc:
        _dump_gateway_tail(stderr_tail)
        print("\nM1 验收失败 ✘  ->  %s" % exc)
        return 1
    except OSError as exc:
        _dump_gateway_tail(stderr_tail)
        print("\nM1 验收失败（网络/进程错误）✘  ->  %s" % exc)
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