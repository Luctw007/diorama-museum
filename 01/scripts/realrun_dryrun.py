# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""三台真跑工程预演（干跑）收口（TASK-166-B → TASK-176-A 自适应两态改造）。

断言「三台真跑链路的当前真实状态」：三台槽位已登记且有后端模块，并按
`slot_loader.slots_available()[slot_id]["binary_path"]` 分叉为**两态**——
  · 就位态（binary_path 有值）：决策链命中「二进制就位 → 真实后端」，
    后端自测 --check-binary rc==0 且输出含「二进制」路径；
  · 缺失态（无二进制）：保持原「优雅失败链」断言——决策链命中
    「未就位 → EMULATOR_BINARY_MISSING」、自测 rc==2 且含「缺失」。
**全程零下载；二进制路径只读引用（不硬编码、不回退到下载）。**

三台真跑设备表（槽位 id → 内容包设备 id → 后端模块）：
  mame-apple2 → apple-ii     → gw.emulators.mame_apple2
  simh-pdp8   → pdp8         → gw.emulators.simh_pdp8
  stella      → atari-2600   → gw.emulators.stella

用法：python 01/scripts/realrun_dryrun.py
退出码：三台×三步全 PASS → 0；任一失败 → 1（指明哪台/第几步/实际输出）。
"""

from __future__ import annotations

import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import slot_loader  # noqa: E402

DEVICES = [
    ("mame-apple2", "apple-ii", "gw.emulators.mame_apple2"),
    ("simh-pdp8", "pdp8", "gw.emulators.simh_pdp8"),
    ("stella", "atari-2600", "gw.emulators.stella"),
]

fails = 0
ready_count = 0
missing_count = 0


def step(ok: bool, device: str, n: int, name: str, note: str) -> None:
    global fails
    print("  [%s] %s 第%d步 %-22s %s" % ("PASS" if ok else "FAIL", device, n, name, note))
    if not ok:
        fails += 1


def check_slot(slot_id: str, device: str) -> None:
    table = slot_loader.slots_available()
    entry = table.get(slot_id) or {}
    if not entry:
        step(False, device, 1, "槽位登记", "slots_available 中不存在 %s；实际: %s"
             % (slot_id, ", ".join(sorted(table)) or "空"))
        return
    if not entry.get("module"):
        step(False, device, 1, "槽位登记", "module 为空（仍为预留）")
        return
    if "预留" in str(entry.get("desc", "")):
        step(False, device, 1, "槽位登记", "desc 仍含「预留」字样")
        return
    step(True, device, 1, "槽位登记", "module=%s" % entry.get("module"))


def check_dryrun(device: str, dev_id: str) -> None:
    table = slot_loader.slots_available()
    binary_path = (table.get(device) or {}).get("binary_path")
    cp = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "launch_device.py"),
         "--device", dev_id, "--dry-run"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120)
    out = (cp.stdout or "") + (cp.stderr or "")
    if binary_path:   # 就位态（TASK-176-A）
        global ready_count
        ready_count += 1
        ok = cp.returncode == 0 and "二进制就位" in out and "真实后端" in out
        if ok:
            step(True, device, 2, "决策链干跑（就位态）", "命中「二进制就位 → 真实后端」")
        else:
            step(False, device, 2, "决策链干跑（就位态）",
                 "rc=%d 未命中关键字；末行: %s"
                 % (cp.returncode, out.strip().splitlines()[-1][:100] if out.strip() else "（无输出）"))
    else:              # 缺失态（保持 166-B 优雅失败链口径）
        global missing_count
        missing_count += 1
        ok = (cp.returncode == 0 and "未就位" in out
              and "EMULATOR_BINARY_MISSING" in out)
        if ok:
            step(True, device, 2, "决策链干跑（缺失态）", "命中「未就位 → EMULATOR_BINARY_MISSING」")
        else:
            step(False, device, 2, "决策链干跑（缺失态）",
                 "rc=%d 未命中关键字；末行: %s"
                 % (cp.returncode, out.strip().splitlines()[-1][:100] if out.strip() else "（无输出）"))


def check_binary(device: str, module: str) -> None:
    table = slot_loader.slots_available()
    binary_path = (table.get(device) or {}).get("binary_path")
    cp = subprocess.run(
        [sys.executable, "-m", module, "--check-binary"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120)
    out = (cp.stdout or "") + (cp.stderr or "")
    if binary_path:   # 就位态
        ok = cp.returncode == 0 and "二进制" in out
        if ok:
            step(True, device, 3, "后端自测（就位态）", "%s rc=0（%s）" % (module, out.strip()[:60]))
        else:
            step(False, device, 3, "后端自测（就位态）",
                 "rc=%d（预期 0）；输出: %s" % (cp.returncode, out.strip()[:100]))
    else:              # 缺失态
        ok = cp.returncode == 2 and "缺失" in out
        if ok:
            step(True, device, 3, "后端自测（缺失态）", "%s rc=2（二进制缺失）" % module)
        else:
            step(False, device, 3, "后端自测（缺失态）",
                 "rc=%d（预期 2）；输出: %s" % (cp.returncode, out.strip()[:100]))


def main(argv: list[str] | None = None) -> int:
    del argv
    print("== 三台真跑干跑预演（两态自适应：就位态/缺失态 · 零下载） ==")
    for slot_id, dev_id, module in DEVICES:
        print("== %s（设备 %s · 后端 %s）" % (slot_id, dev_id, module))
        check_slot(slot_id, slot_id)
        check_dryrun(slot_id, dev_id)
        check_binary(slot_id, module)
    state = "就位态" if ready_count > 0 and missing_count == 0 else (
        "缺失态" if ready_count == 0 and missing_count > 0 else "混合态")
    print("汇总：三台×三步，FAIL %d 处；检测态=%s（就位 %d / 缺失 %d）"
          % (fails, state, ready_count, missing_count))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())