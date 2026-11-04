# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""无引擎演示打包（TASK-31B）：不起 Godot，直接抓网关 fake 设备画面生成 PNG 帧序列 +
单文件 HTML 画廊。纯 stdlib（PNG 经 zlib 手写）。

用法:
  python scripts/demo_frames.py                    # 默认 30 帧 → demo_out/
  python scripts/demo_frames.py --frames 60 --html --txt
  python scripts/demo_frames.py --port 17337       # 专用端口（勿与其他 suite 冲突）
退出码：0=成功；1=失败。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import queue
import socket
import struct
import subprocess
import sys
import threading
import time
import zlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PORT = 17337
W, H, FPS = 280, 192, 25   # Apple II 6 色高分辨率 / fake 配置


class Client:
    """网关客户端（自包含副本，见 m2a_check.py 同款）。"""

    def __init__(self, port: int, timeout: float = 30.0) -> None:
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
        while time.time() < deadline:
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
        raise AssertionError("超时等待 %s" % desc)

    def close(self) -> None:
        self._dead.set()
        try:
            self.sock.close()
        except OSError:
            pass


def png_chunk(tag: bytes, data: bytes) -> bytes:
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def write_png(path: str, w: int, h: int, rgb: bytes) -> int:
    """写 8-bit RGB PNG（无第三方库）。返回文件字节数。"""
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)   # 8bit, color type 2 (RGB)
    rows = b"".join(b"\x00" + rgb[y * w * 3:(y + 1) * w * 3] for y in range(h))
    payload = (b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", ihdr)
               + png_chunk(b"IDAT", zlib.compress(rows, 6)) + png_chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(payload)
    return len(payload)


def gallery_html(frame_names: list[str], fps: int, out_dir: str) -> str:
    names_json = json.dumps(frame_names)
    html = """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>Diorama 帧序列画廊</title>
<style>
body{margin:0;background:#14161a;color:#cfd3da;font-family:system-ui,sans-serif;
display:flex;flex-direction:column;align-items:center;padding:24px;}
#stage{border:1px solid #3a3f47;background:#000;image-rendering:pixelated;}
#bar{margin-top:12px;display:flex;gap:12px;align-items:center;}
button{background:#2a2e36;color:#dfe3ea;border:1px solid #4a505b;border-radius:6px;
padding:6px 14px;cursor:pointer;}
#info{font-variant-numeric:tabular-nums;}
</style></head><body>
<img id="stage" width="640" height="439" alt="frame">
<div id="bar"><button id="play">暂停/播放</button><span id="info"></span></div>
<script>
const FRAMES = __FRAMES__;
const FPS = __FPS__;
let i = 0, playing = true;
const img = document.getElementById("stage");
const info = document.getElementById("info");
function show(){ img.src = FRAMES[i]; info.textContent = (i+1) + " / " + FRAMES.length; }
img.onload = () => { if (playing) setTimeout(() => { i = (i+1) % FRAMES.length; show(); }, 1000/FPS); };
document.getElementById("play").onclick = () => { playing = !playing; if (playing) show(); };
show();
</script></body></html>"""
    return (html.replace("__FRAMES__", names_json)
                .replace("__FPS__", str(fps)))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="无引擎演示打包（PNG 帧序列 + 画廊）")
    ap.add_argument("--frames", type=int, default=30)
    ap.add_argument("--out", default=os.path.join(REPO, "demo_out"))
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--html", action="store_true", help="生成 gallery.html")
    ap.add_argument("--txt", action="store_true", help="打印每帧校验摘要")
    args = ap.parse_args(argv)

    frames_dir = os.path.join(args.out, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    gw_proc = subprocess.Popen(
        [sys.executable, os.path.join(REPO, "gw", "gateway.py"),
         "--host", "127.0.0.1", "--port", str(args.port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace")
    ready = False
    deadline = time.time() + 10.0
    while time.time() < deadline and gw_proc.poll() is None:
        try:
            probe = socket.create_connection(("127.0.0.1", args.port), timeout=0.5)
            probe.close()
            ready = True
            break
        except OSError:
            time.sleep(0.2)
    if not ready:
        print("失败：网关未就绪（退出码 %s）" % gw_proc.returncode)
        return 1

    client = Client(args.port)
    saved: list[str] = []
    summary: list[str] = []
    try:
        did = "demo-apple2"
        client.send({"type": "start_device", "emulator": "fake", "device_id": did,
                     "config": {"width": W, "height": H, "fps": FPS,
                                "frame_codec": "raw", "sinks": ["main", "speaker"]}})
        ack = client.recv(lambda m: m.get("type") == "start_device_ack"
                          and m.get("device_id") == did, "start_device_ack")
        if ack.get("ok") is not True:
            print("失败：设备启动未 ok")
            return 1
        for i in range(args.frames):
            fr = client.recv(lambda m: m.get("type") == "frame_ready"
                             and m.get("device_id") == did, "frame_ready#%d" % i)
            rgb = base64.b64decode(fr.get("data_b64", ""))
            fid = fr.get("frame_id")
            name = "frame_%04d.png" % (i + 1)
            path = os.path.join(frames_dir, name)
            size = write_png(path, W, H, rgb)
            saved.append(os.path.join("frames", name))
            line = "frame %d | frame_id=%s | %dx%d | png %d B" % (
                i + 1, fid, W, H, size)
            summary.append(line)
            if args.txt:
                print("  " + line)
        client.send({"type": "stop", "device_id": did})
        client.recv(lambda m: m.get("type") == "stopped"
                    and m.get("device_id") == did, "stopped")
    except (AssertionError, OSError) as exc:
        print("失败：%s" % exc)
        return 1
    finally:
        client.close()
        if gw_proc.poll() is None:
            gw_proc.terminate()
            try:
                gw_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gw_proc.kill()

    if args.html:
        gpath = os.path.join(args.out, "gallery.html")
        with open(gpath, "w", encoding="utf-8") as fh:
            fh.write(gallery_html(saved, FPS, args.out))
        print("画廊已生成: %s" % gpath)
    print("完成：%d 帧 PNG → %s" % (len(saved), frames_dir))
    print("摘要示例（首帧）：%s" % summary[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())