# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""黎明厅站位静态自检（TASK-91B / 44 号 G-2）。

断言（对 01/godot/content/exhibit_dawn.json）：
  S-1 每台机器位置在厅界内（留 0.5 m 边距，含体积余量）；
  S-2 站位两两水平距离 ≥ 16 号台本表的最小步距 3.4 m（防触发区重叠/串音）；
  S-3 动线顺序 = v2（ENIAC→EDVAC→EDSAC→Baby）且 scale 合法。
退出码：0=全过；1=有违规（逐条打印）。
"""

from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUT = os.path.join(REPO, "godot", "content", "exhibit_dawn.json")
EXPECT_ORDER = ["eniac", "edvac", "edsac", "manchester-baby"]
MIN_STEP = 3.4


def main() -> int:
    with open(LAYOUT, encoding="utf-8") as fh:
        data = json.load(fh)
    w = float(data.get("width", 20.0))
    d = float(data.get("depth", 12.0))
    devs = data.get("devices", [])
    fails: list[str] = []

    order = [x.get("id") for x in devs]
    if order != EXPECT_ORDER:
        fails.append("S-3 动线顺序不符: %s（期望 %s）" % (order, EXPECT_ORDER))
    for x in devs:
        px, _, pz = x.get("position", [0, 0, 0])
        if abs(px) > w / 2 - 0.5 or abs(pz) > d / 2 - 0.5:
            fails.append("S-1 越界: %s @ (%s, %s)" % (x.get("id"), px, pz))
        sc = x.get("scale", [1, 1, 1])
        if any(not (0.1 <= s <= 4.0) for s in sc):
            fails.append("S-3 非法 scale: %s %s" % (x.get("id"), sc))
    for i in range(len(devs)):
        for j in range(i + 1, len(devs)):
            a, b = devs[i]["position"], devs[j]["position"]
            dist = ((a[0] - b[0]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
            if dist < MIN_STEP:
                fails.append("S-2 间距不足 %.2fm: %s<->%s"
                             % (dist, devs[i]["id"], devs[j]["id"]))
    print("站位自检：%d 台 / 厅 %.0fm×%.0fm / 最小步距 %.1fm"
          % (len(devs), w, d, MIN_STEP))
    if fails:
        for f in fails:
            print("  FAIL " + f)
        print("结果：%d 项违规" % len(fails))
        return 1
    print("  全部通过（S-1 厅界/S-2 间距/S-3 动线顺序）")
    return 0


if __name__ == "__main__":
    sys.exit(main())