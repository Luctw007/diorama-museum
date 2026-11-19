# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""三台真跑「启动器前置参数核对」脚本（TASK-181-B）：免 ROM、零介质、零下载、零联网，
**不 Popen 任何真实模拟器进程**。只跑三类只读探针：
  · launch_device.py --device <id> --dry-run：断言 rc=0 且决策链命中
    「二进制就位 → 真实后端」与「slot 提示」（启动参数侧不启动后端）；
  · python -m gw.emulators.<mod> --check-binary：断言 rc=0 且打印二进制路径；
  · emulator_doctor.py：断言 rc=0、部署就绪判定行、third_party 与 roms 提示路径
    （ROM/介质缺失提示路径证据，只打印核对）。
汇总三台×N 步 [PASS/FAIL]，全过 rc=0、任一 FAIL rc=1。

用法：python 01/scripts/realrun_launch_check.py
"""

from __future__ import annotations

import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

DEVICES = [
    ("apple-ii", "gw.emulators.mame_apple2"),
    ("pdp8", "gw.emulators.simh_pdp8"),
    ("atari-2600", "gw.emulators.stella"),
]

fails = 0


def step(ok: bool, device: str, n: int, name: str, note: str) -> None:
    global fails
    print("  [%s] %s 第%d步 %-18s %s" % ("PASS" if ok else "FAIL", device, n, name, note))
    if not ok:
        fails += 1


def run(cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    cp = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=timeout)
    return cp.returncode, (cp.stdout or "") + (cp.stderr or "")


def check_dryrun(device: str, dev_id: str) -> None:
    rc, out = run([sys.executable,
                   os.path.join(REPO, "scripts", "launch_device.py"),
                   "--device", dev_id, "--dry-run"])
    for line in out.strip().splitlines():
        if "决策:" in line or "slot 提示" in line or "emulator=" in line:
            print("      " + line[:110])
    ok = (rc == 0 and "二进制就位" in out and "真实后端" in out
          and "slot 提示" in out)
    step(ok, device, 1, "决策链干跑", "rc=%d" % rc)


def check_binary(device: str, module: str) -> None:
    rc, out = run([sys.executable, "-m", module, "--check-binary"])
    path_line = out.strip().splitlines()[0] if out.strip() else "（无输出）"
    print("      " + path_line[:110])
    ok = rc == 0 and "二进制" in out
    step(ok, device, 2, "后端自测", "rc=%d" % rc)


def check_missing_guide() -> None:
    """ROM/介质缺失提示路径（三台共用一次）：doctor 就绪判定行 + rom 提示行。"""
    rc, out = run([sys.executable, os.path.join(REPO, "scripts", "emulator_doctor.py")],
                  timeout=300)
    for line in out.strip().splitlines():
        if "部署就绪判定" in line or "rom_location_hint" in line or "部署签字" in line:
            print("      " + line[:120])
    ok = (rc == 0 and "部署就绪判定" in out and "齐" in out
          and "third_party" in out and "roms" in out)
    step(ok, "三台共用", 3, "缺失提示路径", "rc=%d" % rc)


def main(argv: list[str] | None = None) -> int:
    del argv
    print("== 三台真跑启动器前置参数核对（免 ROM · 零介质 · 不启动模拟器） ==")
    for dev_id, module in DEVICES:
        print("== %s（后端 %s）" % (dev_id, module))
        check_dryrun(dev_id, dev_id)
        check_binary(dev_id, module)
    check_missing_guide()
    print("汇总：三台×N 步，FAIL %d 处（全 PASS 则 rc=0）" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())