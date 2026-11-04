# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""槽位一致性检查（TASK-46B）：每完工包若声明 runtime.slot，则其槽位类目必须已知/可解析。

判据（提示级 + 阻断级）：
  SC-01 声明 slot 的包：emulator_class 必须 ∈ slot_loader.BACKEND_TYPE_MODULE 键集；
       media_class 若非空必须在 槽位系统媒体类目白名单（见本文件 MEDIA_CLASSES，与 02 线 v0.5 对齐）；
  SC-02 声明 slot 且对应槽位已就位：二进制就绪（提示 OK），否则 HINT（不阻塞）；
  SC-03 未声明 slot 的包：INFO 列举（基线 v0：全部未声明时为正常状态）。
用法：python scripts/slot_consistency_check.py；退出码：0=通过；1=存在 SC-01 违规。
"""

from __future__ import annotations

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import pkg_registry as pr  # noqa: E402
import slot_loader  # noqa: E402

MEDIA_CLASSES = {"cartridge", "disk", "tape", "cd", "dvd", "card",
                 "firmware", "app_package"}
BACKEND_TYPES = set(slot_loader.BACKEND_TYPE_MODULE)


def check() -> int:
    ready, _wip = pr.discover_packages_full()
    slots = slot_loader.slots_available()
    rc = 0
    declared = 0
    hits: list[str] = []
    for dev_id, pkg in ready:
        rt_path = os.path.join(pkg, "runtime.json")
        if not os.path.isfile(rt_path):
            with open(os.path.join(pkg, "meta.json"), encoding="utf-8") as fh:
                runtime = json.load(fh).get("runtime") or {}
        else:
            with open(rt_path, encoding="utf-8") as fh:
                runtime = json.load(fh)
        slot = runtime.get("slot")
        if not slot:
            print("  [INFO] %s：未声明 slot（基线 v0 常态）" % dev_id)
            continue
        declared += 1
        if not isinstance(slot, dict):
            print("  [FAIL] SC-01 %s.slot 必须是对象" % dev_id)
            rc = 1
            continue
        ec = slot.get("emulator_class")
        if ec not in BACKEND_TYPES:
            print("  [FAIL] SC-01 %s.slot.emulator_class=%r 未知（合法: %s）"
                  % (dev_id, ec, sorted(BACKEND_TYPES)))
            rc = 1
            continue
        mc = slot.get("media_class") or ""
        if mc and mc not in MEDIA_CLASSES:
            print("  [FAIL] SC-01 %s.slot.media_class=%r 未知（合法: %s）"
                  % (dev_id, mc, sorted(MEDIA_CLASSES)))
            rc = 1
        if ec in slots:
            entry = slots[ec]
            print("  [%s] SC-02 %s → 槽位 %s %s"
                  % ("OK" if entry["binary_path"] else "HINT", dev_id, ec,
                     "二进制就位" if entry["binary_path"] else "二进制未就位（提示级）"))
        else:
            hits.append("%s → %s（槽位未建立）" % (dev_id, ec))
    for h in hits:
        print("  [HINT] SC-02 " + h)
    print("汇总：完工包 %d，声明 slot %d，SC-01 违规 %d"
          % (len(ready), declared, rc))
    return rc


if __name__ == "__main__":
    sys.exit(check())