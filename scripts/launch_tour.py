# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""五厅轮播演示（TASK-66B）：按厅顺序批量产出 demo 帧存证 + 聚合画廊。

用法:
  python scripts/launch_tour.py --frames 3
  python scripts/launch_tour.py --only 黎明
  python scripts/launch_tour.py --frames 3 && python scripts/gen_tour_gallery.py
产物：demo_out/tour_<stamp>/<厅目目录…>/…、tour_summary.md、tour_gallery.html
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
REPO = os.path.dirname(SCRIPT_DIR)
CONTENT = os.path.join(REPO, "godot", "content")


def hall_layouts() -> list[str]:
    out = []
    for f in sorted(os.listdir(CONTENT)):
        if f.startswith("exhibit_") and f.endswith(".json") \
                and not f.startswith("exhibit_index"):
            out.append(os.path.join(CONTENT, f))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="五厅轮播演示")
    ap.add_argument("--frames", type=int, default=3)
    ap.add_argument("--out", default=os.path.join(REPO, "demo_out"))
    ap.add_argument("--only", help="厅名前缀过滤（如 黎明）")
    args = ap.parse_args(argv)

    layouts = [p for p in hall_layouts()
               if not args.only or args.only in os.path.basename(p)]
    if not layouts:
        print("无匹配厅布局（--only=%s）" % args.only)
        return 1
    stamp = time.strftime("%Y%m%d_%H%M%S")
    tour_dir = os.path.join(args.out, "tour_%s" % stamp)
    os.makedirs(tour_dir, exist_ok=True)

    print("轮播开始：%d 个厅 → %s" % (len(layouts), tour_dir))
    rc_all = 0
    for lp in layouts:
        name = os.path.splitext(os.path.basename(lp))[0]
        print("\n===== %s =====" % name)
        cp = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "launch_room.py"),
             "--layout", lp, "--frames", str(args.frames),
             "--out", tour_dir],
            cwd=REPO, text=True)
        rc_all = max(rc_all, cp.returncode)

    rows = ["# 五厅轮播汇总（%s）" % time.strftime("%Y-%m-%d %H:%M:%S"), ""]
    for d in sorted(os.listdir(tour_dir)):
        if os.path.isdir(os.path.join(tour_dir, d)):
            pngs = sum(1 for f in os.listdir(os.path.join(tour_dir, d))
                       if f.endswith(".png"))
            rows.append("- %s：%d 帧" % (d, pngs))
    with open(os.path.join(tour_dir, "tour_summary.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    print("\n".join(rows))
    print("tour 完成（rc=%d）：%s" % (rc_all, tour_dir))
    return rc_all


if __name__ == "__main__":
    sys.exit(main())