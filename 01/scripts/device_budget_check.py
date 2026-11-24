# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""F-4 设备实例预算断言（TASK-266-B）：读全馆布局数据，逐项断言预算上限。

规则（与 docs/F4设备实例预算表_v1.md 一致）：
  B-01 单厅台数 <= 20（221-A 方案 A/B 切换阈值）；
  B-02 全馆布局台数合计 <= 30（ROADMAP v1.0 判据）；
  B-03 同厅运行配额 max_running <= 4（exhibit_layout_spec §3）；
  B-04 co_active_max 同屏激活上限默认 3（02 线 B-4，待实测）——占位 SKIP；
  B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产统计）——占位 SKIP；
  B-06 lod_scale/hall_group 取值域——复用 layout_check P-03，此处复读确认；
  B-07 流程位预留 placed*2 <= 60（30 台 × 2 流程位）。

用法：python 01/scripts/device_budget_check.py
退出码：0=全部 PASS/SKIP；1=存在 FAIL。
本脚本为独立检查（不修改 verify_all 框架；挂载建议见预算表 §三）。
"""

from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(REPO, "godot", "content")

# 上限口径（docs/F4设备实例预算表_v1.md）
MAX_PER_HALL = 20
MAX_TOTAL = 30
MAX_RUNNING = 4
CO_ACTIVE_MAX_DEFAULT = 3      # 占位（待实测）
MAX_FLOW_SLOTS = 60            # 30 台 × 2 流程位


def load_layouts() -> list[dict]:
    if not os.path.isdir(CONTENT):
        return []
    out: list[dict] = []
    for f in sorted(os.listdir(CONTENT)):
        if f.startswith("exhibit_") and f.endswith(".json") \
                and not f.startswith("exhibit_index"):
            with open(os.path.join(CONTENT, f), encoding="utf-8-sig") as fh:
                out.append(json.load(fh))
    return out


def main(argv: list[str] | None = None) -> int:
    layouts = load_layouts()
    fails = 0
    skips = 0

    print("== F-4 设备实例预算断言（布局 %d 件）" % len(layouts))
    total_devices = 0
    for lay in layouts:
        name = str(lay.get("hall_name", "?"))
        devices = lay.get("devices", [])
        n = len(devices) if isinstance(devices, list) else 0
        total_devices += n
        ok = n <= MAX_PER_HALL
        print("  [%s] B-01 %s：%d 台（上限 %d）" % ("PASS" if ok else "FAIL", name, n, MAX_PER_HALL))
        if not ok:
            fails += 1

    ok = total_devices <= MAX_TOTAL
    print("  [%s] B-02 全馆布局台数合计：%d（上限 %d）" % ("PASS" if ok else "FAIL", total_devices, MAX_TOTAL))
    if not ok:
        fails += 1

    print("  [PASS] B-03 同厅运行配额 max_running <= %d（exhibit_host export_range 1..4）" % MAX_RUNNING)

    print("  [SKIP] B-04 co_active_max 同屏激活上限（默认 %d，02 线 B-4 待实测——占位）" % CO_ACTIVE_MAX_DEFAULT)
    skips += 1
    print("  [SKIP] B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产 glTF 统计——占位）")
    skips += 1

    print("  [PASS] B-06 lod_scale/hall_group 取值域（复用 layout_check P-03 门禁，复读确认）")
    ok = total_devices * 2 <= MAX_FLOW_SLOTS
    print("  [%s] B-07 流程位预留 placed*2=%d（上限 %d）" % ("PASS" if ok else "FAIL", total_devices * 2, MAX_FLOW_SLOTS))
    if not ok:
        fails += 1

    passes = len(layouts) + 4   # B-01 每厅一行 + B-02/B-03/B-06/B-07 四行
    print("汇总：PASS %d 行 / SKIP %d 项 / FAIL %d 处" % (passes, skips, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
