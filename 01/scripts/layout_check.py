# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""展陈布局校验（TASK-21B）：校验展厅布局 JSON（exhibit_host.gd 的配置输入）。

规则（与 docs/exhibit_layout_spec.md 一致）：
  L-01 top：hall_name 非空字符串、devices 为非空数组；
  L-02 devices[]：id 必须存在于 godot/content（同名目录）；
  L-03 position 必填 3 元数值数组，且在大厅边界 [-w/2..w/2, 0.., -d/2..d/2] 内（默认 20×12）；
  L-04 同厅 device id 不得重复；可选项 rotation[4]/scale[3]/slot 类型合法。

用法：python scripts/layout_check.py <布局.json> [--width 20 --depth 12]
退出码：0=合法；1=非法（逐条打印）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_ROOT = os.path.join(REPO, "godot", "content")


def known_device_ids() -> set[str]:
    if not os.path.isdir(CONTENT_ROOT):
        return set()
    return {name for name in os.listdir(CONTENT_ROOT)
            if os.path.isdir(os.path.join(CONTENT_ROOT, name))}


def check_number_list(value, n: int, name: str) -> bool:
    return (isinstance(value, list) and len(value) == n
            and all(isinstance(x, (int, float)) for x in value))


def validate(layout: dict, width: float, depth: float) -> list[str]:
    errors: list[str] = []
    if not isinstance(layout, dict):
        return ["L-01 布局文件必须是 JSON 对象"]
    # 厅边界：布局内 width/depth 优先（schema 可选字段），否则用命令行缺省
    try:
        width = float(layout.get("width", width))
        depth = float(layout.get("depth", depth))
    except (TypeError, ValueError):
        errors.append("L-01 width/depth 必须是数值")
        return errors
    if not isinstance(layout.get("hall_name"), str) or not layout["hall_name"].strip():
        errors.append("L-01 hall_name 必须是非空字符串")
    devices = layout.get("devices")
    if not isinstance(devices, list) or not devices:
        errors.append("L-01 devices 必须是非空数组")
        return errors
    known = known_device_ids()
    seen: set[str] = set()
    for i, d in enumerate(devices):
        tag = "devices[%d]" % i
        if not isinstance(d, dict):
            errors.append("%s 必须是对象" % tag)
            continue
        did = d.get("id")
        if not isinstance(did, str) or not did:
            errors.append("%s.id 缺失" % tag)
            continue
        if did not in known:
            errors.append("L-02 %s.id=%s 不在 godot/content（现有: %s）"
                          % (tag, did, ", ".join(sorted(known)) or "无"))
        if did in seen:
            errors.append("L-04 设备 id 重复: %s" % did)
        seen.add(did)
        if not check_number_list(d.get("position"), 3, "position"):
            errors.append("L-03 %s.position 必须是 3 元数值数组" % tag)
        else:
            x, y, z = d["position"]
            if abs(x) > width / 2 or abs(z) > depth / 2 or y < 0:
                errors.append("L-03 %s.position=(%s,%s,%s) 超出大厅 %s×%s（y≥0）"
                              % (tag, x, y, z, width, depth))
        if "rotation" in d and not check_number_list(d.get("rotation"), 4, "rotation"):
            errors.append("%s.rotation 必须是 4 元数值数组（四元数）" % tag)
        if "scale" in d and not check_number_list(d.get("scale"), 3, "scale"):
            errors.append("%s.scale 必须是 3 元数值数组" % tag)
        if "slot" in d and not isinstance(d.get("slot"), int):
            errors.append("%s.slot 必须是整数" % tag)
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="展陈布局 JSON 校验")
    ap.add_argument("layout", nargs="?", help="布局 JSON 路径（--all 时可省）")
    ap.add_argument("--all", action="store_true",
                    help="校验 godot/content 下全部 exhibit_*.json（排除 exhibit_index）")
    ap.add_argument("--width", type=float, default=20.0)
    ap.add_argument("--depth", type=float, default=12.0)
    args = ap.parse_args(argv)

    if args.all:
        layouts = [os.path.join(CONTENT_ROOT, f)
                   for f in sorted(os.listdir(CONTENT_ROOT))
                   if f.startswith("exhibit_") and f.endswith(".json")
                   and not f.startswith("exhibit_index")]
        seen: dict[str, str] = {}
        rc = 0
        for path in layouts:
            print("=== %s" % os.path.basename(path))
            with open(path, encoding="utf-8-sig") as fh:
                layout = json.load(fh)
            errors = validate(layout, args.width, args.depth)
            for e in errors:
                print("  [FAIL] " + e)
                rc = 1
            for d in layout.get("devices", []):
                did = d.get("id")
                if did in seen:
                    print("  [WARN] 设备 %s 跨厅重复（%s 与 %s）——允许（演示复用），提示知悉"
                          % (did, seen[did], os.path.basename(path)))
                else:
                    seen[did] = os.path.basename(path)
            if not errors:
                print("  OK（设备 %d 台）" % len(layout.get("devices", [])))
        print("--all 完成：%d 份布局" % len(layouts))
        return rc
    if not args.layout:
        ap.error("需要 <布局.json> 或 --all")

    with open(args.layout, encoding="utf-8-sig") as fh:   # utf-8-sig：容忍记事本保存的 BOM
        layout = json.load(fh)
    errors = validate(layout, args.width, args.depth)
    for e in errors:
        print("  [FAIL] " + e)
    if errors:
        print("布局校验失败：%d 条" % len(errors))
        return 1
    n = len(layout.get("devices", []))
    print("布局合法：%s，设备 %d 台（大厅 %s×%s，包清单 %d 个）"
          % (layout.get("hall_name"), n, args.width, args.depth,
             len(known_device_ids())))
    return 0


if __name__ == "__main__":
    sys.exit(main())