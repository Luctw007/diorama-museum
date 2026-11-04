# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""启动共享库（TASK-56B）：launch_device.py 与 launch_room.py 的公共核心。

导出：find_pkg / decision_chain / run_demo / print_doctor_guide / ensure_gateway。
抽取自 TASK-46B 的 launch_device.py（行为不变，供单机与整厅双通道复用）。
"""

from __future__ import annotations

import base64
import json
import os
import socket
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import pkg_registry as pr  # noqa: E402
import run_profile as rp   # noqa: E402
import slot_loader         # noqa: E402
import emulator_doctor     # noqa: E402
from demo_frames import Client, write_png, W, H  # noqa: E402

REPO = os.path.dirname(SCRIPT_DIR)
LAUNCH_PORT = 17341


def find_pkg(device_id: str) -> str | None:
    for pid, path in pr.discover_packages_full()[0]:
        if pid == device_id:
            return path
    return None


def decision_chain(device_id: str) -> tuple[dict, list[str]]:
    """返回 (mapping, 决策链文本)。空 mapping = 找不到包。"""
    chain: list[str] = []
    pkg = find_pkg(device_id)
    if pkg is None:
        return {}, ["设备 %s 不在完工包注册表（可用: %s）"
                    % (device_id,
                       ", ".join(p for p, _ in pr.discover_packages_full()[0]))]
    mapping = rp.build_mapping(pkg)
    chain.append("包位置: %s" % pkg)
    chain.append("emulator=%s  demo_mode=%s  category=%s"
                 % (mapping["emulator"], mapping["demo_mode"], mapping["category"]))
    slot = mapping.get("slot") or {}
    if mapping["demo_mode"]:
        chain.append("决策: demo_mode → fake 演示直起（无需槽位）")
        return mapping, chain
    ec = slot.get("emulator_class") or mapping["emulator"]
    canon = slot_loader.canonical(ec)
    slots = slot_loader.slots_available()
    chain.append("slot 提示: %s%s（media_class=%s bios_hint=%s）"
                 % (ec, (" → " + canon) if canon != ec else "",
                    slot.get("media_class") or "?", slot.get("bios_hint") or "?"))
    entry = slots.get(canon)
    if entry is None:
        chain.append("决策: 槽位未建立 → MISSING（先按 slots/README.md 建 manifest）")
        return mapping, chain
    if not entry.get("module"):
        chain.append("决策: 后端模块未实现（预留槽位）→ 暂不可真跑；"
                     "可选 demo 预览（--force-demo）或等待后端")
        return mapping, chain
    if entry["binary_path"]:
        chain.append("决策: 槽位 %s 二进制就位（%s）→ 真实后端（管线待后端实现）"
                     % (canon, entry["binary_path"]))
    else:
        chain.append("决策: 二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引: "
                     "把二进制放入 %s 或设环境变量 %s"
                     % (entry.get("binary_hint") or "slots/emulators/%s/" % canon,
                        entry.get("binary_env") or "?"))
    return mapping, chain


def ensure_gateway(port: int = LAUNCH_PORT) -> subprocess.Popen:
    """起网关子进程并等待就绪；失败 raise RuntimeError。"""
    gw = subprocess.Popen(
        [sys.executable, os.path.join(REPO, "gw", "gateway.py"),
         "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 10.0
    while time.time() < deadline and gw.poll() is None:
        try:
            p = socket.create_connection(("127.0.0.1", port), timeout=0.5)
            p.close()
            return gw
        except OSError:
            time.sleep(0.2)
    raise RuntimeError("网关未就绪（exit=%s）" % gw.returncode)


def run_demo(mapping: dict, frames: int, out_dir: str,
             port: int = LAUNCH_PORT, quiet: bool = False) -> int:
    """fake 演示直起 + 抓帧存证；返回 0/1。quiet=True 时不打详细日志（整厅批量用）。"""
    os.makedirs(out_dir, exist_ok=True)
    gw = ensure_gateway(port)
    try:
        client = Client(port)
        did = "launch-%s" % mapping["device_id"]
        cfg = dict(mapping["config"])
        client.send({"type": "start_device", "emulator": "fake",
                     "device_id": did, "config": cfg})
        ack = client.recv(lambda m: m.get("type") == "start_device_ack"
                          and m.get("device_id") == did, "ack", timeout=20.0)
        if not quiet:
            print("演示启动 ok（sinks=%s 画面 %dx%d@%s）"
                  % (ack.get("info", {}).get("sinks"), cfg.get("width"),
                     cfg.get("height"), cfg.get("fps")))
        saved = 0
        for i in range(frames):
            fr = client.recv(lambda m: m.get("type") == "frame_ready"
                             and m.get("device_id") == did, "frame#%d" % i,
                             timeout=25.0)
            rgb = base64.b64decode(fr.get("data_b64", ""))
            path = os.path.join(out_dir, "%s_%04d.png"
                                % (mapping["device_id"], i + 1))
            write_png(path, fr.get("width", W), fr.get("height", H), rgb)
            saved += 1
        client.send({"type": "stop", "device_id": did})
        client.recv(lambda m: m.get("type") == "stopped"
                    and m.get("device_id") == did, "stopped", timeout=15.0)
        client.close()
        if not quiet:
            print("帧存证：%d 张 PNG → %s" % (saved, out_dir))
        return 0
    finally:
        if gw.poll() is None:
            gw.terminate()
            try:
                gw.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gw.kill()


def print_doctor_guide() -> None:
    print("真实运行前置：")
    for c in emulator_doctor.run_checks():
        if c["status"] in ("MISSING", "FAIL"):
            print("  [%s] %-18s %s" % (c["status"], c["item"], c["guide"]))
    print("（装好二进制/介质后重跑本命令即自动切换真实通道；当前保留在指引层）")