# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""整厅批量演示（TASK-56B）：按展厅布局顺序为每台设备产出 demo 帧存证。

用法:
  python scripts/launch_room.py --layout godot/content/exhibit_dawn.json
  python scripts/launch_room.py --layout exhibit_mainframe.json --frames 3 --out demo_out
  python scripts/launch_room.py --layout exhibit_console.json --halt-on-error
产物：demo_out/<厅名>_<YYYYmmdd_HHMMSS>/<device_id>_*.png + room_summary.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from launch_lib import (REPO, decision_chain, run_demo)  # noqa: E402

CONTENT = os.path.join(REPO, "godot", "content")


def resolve_layout(name: str) -> str:
    if os.path.sep in name and os.path.isfile(name):
        return name
    cand = os.path.join(CONTENT, name)
    if os.path.isfile(cand):
        return cand
    return ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="整厅批量演示（demo 帧存证）")
    ap.add_argument("--layout", default="exhibit_dawn.json")
    ap.add_argument("--frames", type=int, default=3)
    ap.add_argument("--out", default=os.path.join(REPO, "demo_out"))
    ap.add_argument("--halt-on-error", action="store_true")
    args = ap.parse_args(argv)

    layout_path = resolve_layout(args.layout)
    if not layout_path:
        print("布局文件不可用: %s" % args.layout)
        return 1
    with open(layout_path, encoding="utf-8-sig") as fh:
        layout = json.load(fh)
    hall = layout.get("hall_name", os.path.basename(layout_path))
    devices = layout.get("devices", [])
    if not devices:
        print("布局无设备: %s" % layout_path)
        return 1
    stamp = time.strftime("%Y%m%d_%H%M%S")
    room_out = os.path.join(args.out, "%s_%s" % (hall, stamp))
    os.makedirs(room_out, exist_ok=True)
    print("整厅演示：%s（%d 台，每台 %d 帧）→ %s"
          % (hall, len(devices), args.frames, room_out))

    rows: list[dict] = []
    fail = 0
    for idx, dev in enumerate(devices, 1):
        did = dev.get("id")
        print("\n-- [%d/%d] %s --" % (idx, len(devices), did))
        mapping, chain = decision_chain(str(did))
        for line in chain:
            print("  " + line)
        if not mapping:
            rows.append({"device": did, "rc": 1, "frames": 0, "note": "未注册"})
            fail += 1
            if args.halt_on_error:
                return 1
            continue
        if not (mapping["demo_mode"]):
            rows.append({"device": did, "rc": 0, "frames": 0,
                         "note": "非 demo（决策链已打印，跳过演示）"})
            continue
        rc = run_demo(mapping, args.frames, room_out, quiet=True)
        rows.append({"device": did, "rc": rc, "frames": args.frames if rc == 0 else 0,
                     "note": "demo 帧存证" if rc == 0 else "启动失败"})
        fail += rc
        if rc and args.halt_on_error:
            break

    summary = ["# 整厅演示汇总：%s（%s）" % (hall, time.strftime("%Y-%m-%d %H:%M:%S")),
               "", "| # | 设备 | 结果 | 帧数 | 备注 |", "|---|---|---|---|---|"]
    ok = 0
    for i, r in enumerate(rows, 1):
        ok += 0 if r["rc"] else 1
        summary.append("| %d | %s | %s | %d | %s |"
                       % (i, r["device"], "✓" if r["rc"] == 0 else "✗",
                          r["frames"], r["note"]))
    summary.append("")
    summary.append("合计：成功 %d / 失败 %d" % (ok, len(rows) - ok))
    with open(os.path.join(room_out, "room_summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(summary) + "\n")
    pngs = sum(1 for f in os.listdir(room_out) if f.endswith(".png"))
    print("\n整厅完成：成功 %d / 失败 %d；PNG %d 张；汇总 %s"
          % (ok, len(rows) - ok, pngs, os.path.join(room_out, "room_summary.md")))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())