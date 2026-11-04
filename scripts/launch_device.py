# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""一键启动设备（TASK-46B → 56B 重构）：核心逻辑抽至 launch_lib.py。

用法:
  python scripts/launch_device.py --device apple-ii
  python scripts/launch_device.py --device apple-ii --frames 10 --out demo_out
  python scripts/launch_device.py --device pdp8 --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from launch_lib import (REPO, decision_chain, print_doctor_guide,  # noqa: E402
                        run_demo)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="一键启动设备（槽位绑定）")
    ap.add_argument("--device", required=True, help="设备 id（完工包注册表）")
    ap.add_argument("--dry-run", action="store_true", help="只打印决策链")
    ap.add_argument("--force-demo", action="store_true",
                    help="忽略 demo_mode 判定，强制 fake 演示预览")
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--out", default=os.path.join(REPO, "demo_out"))
    args = ap.parse_args(argv)

    mapping, chain = decision_chain(args.device)
    for line in chain:
        print("  " + line)
    if not mapping:
        return 1
    if args.dry_run:
        return 0
    if mapping["demo_mode"] or args.force_demo:
        if not mapping["demo_mode"]:
            print("（--force-demo：预览通道，非真实运行）")
        return run_demo(mapping, args.frames, args.out)
    print_doctor_guide()
    return 0


if __name__ == "__main__":
    sys.exit(main())