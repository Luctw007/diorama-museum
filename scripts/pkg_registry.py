# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""内容包注册表（TASK-41A）：门禁数据驱动化——包清单自动发现。

替代 verify_all.py / sync_content.py 中手工维护的 PKGS/SOURCES 硬编码。
扫描范围：D:\\work\\03\\repo\\content 与 D:\\work\\05\\repo\\content（内容线两仓）。
判定：子目录内存在 meta.json 即视为规范包；EXCLUDES 内的 fixture/示例默认剔除。

用法:
  python scripts/pkg_registry.py --list     # 人类可读清单
  python scripts/pkg_registry.py --json     # 机器可读
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCRIPTS)                 # D:\work\01\repo
WORK = os.path.dirname(REPO)                    # D:\work\01
WORK_ROOT = os.path.dirname(WORK)               # D:\work

SCAN_ROOTS = [
    os.path.join(WORK_ROOT, "03", "repo", "content"),
    os.path.join(WORK_ROOT, "05", "repo", "content"),
]

# fixture/示例：不参与量产门禁与同步
EXCLUDES = {"test-device", "manchester-baby-scaffold"}

# 完工判定（TASK-41A 轮 4）：
#   WIP 判据 = 结构性半成品：缺 THIRD_PARTY.md / annotations.json / 两网格目录合计 0 gltf；
#   或包内存在 `.wip` 标记文件（内容线生产中的显式声明，交付时删除）。
#   encyclopedia.md 缺失不算 WIP（内容缺口，进 NOTE 清单转内容线补齐）。
WIP_STRUCTURAL = ["THIRD_PARTY.md", "annotations/annotations.json"]
GLTF_DIRS = ("meshes", "assemblies")   # 老包 meshes/，v0.4 新包 assemblies/
ENCYCLOPEDIA = "encyclopedia.md"


def _gltf_total(pkg: str) -> int:
    total = 0
    for d in GLTF_DIRS:
        path = os.path.join(pkg, d)
        if os.path.isdir(path):
            total += len([f for f in os.listdir(path) if f.endswith(".gltf")])
    return total


def _is_wip(pkg: str) -> bool:
    if os.path.isfile(os.path.join(pkg, ".wip")):
        return True
    if any(not os.path.isfile(os.path.join(pkg, rel)) for rel in WIP_STRUCTURAL):
        return True
    return _gltf_total(pkg) < 1


def _missing_encyclopedia(pkg: str) -> bool:
    return not os.path.isfile(os.path.join(pkg, ENCYCLOPEDIA))


def discover_packages_full() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """返回 (ready_packages, wip_packages)，均按 device_id 排序。"""
    found: dict[str, str] = {}
    for root in SCAN_ROOTS:
        if not os.path.isdir(root):
            print("[pkg_registry] 扫描根缺失: %s" % root, file=sys.stderr)
            continue
        for name in sorted(os.listdir(root)):
            pkg = os.path.join(root, name)
            if (not os.path.isdir(pkg)
                    or not os.path.isfile(os.path.join(pkg, "meta.json"))):
                continue
            if name in EXCLUDES:
                continue
            found[name] = pkg
    ready, wip = [], []
    for name, path in sorted(found.items()):
        (wip if _is_wip(path) else ready).append((name, path))
    return ready, wip


def discover_packages() -> list[tuple[str, str]]:
    """返回 [(device_id, 包目录绝对路径)]，按 device_id 排序（仅完工包）。"""
    return discover_packages_full()[0]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="内容包注册表（自动发现）")
    ap.add_argument("--list", action="store_true", help="打印清单")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)
    ready, wip = discover_packages_full()
    if args.json:
        print(json.dumps({"ready": [{"id": i, "path": p} for i, p in ready],
                          "wip": [{"id": i, "path": p} for i, p in wip]},
                         ensure_ascii=False, indent=2))
    if args.list or not args.json:
        for i, p in ready:
            note = "   [NOTE 缺 encyclopedia.md]" if _missing_encyclopedia(p) else ""
            print("%-18s %s%s" % (i, p, note))
        for i, p in wip:
            print("%-18s %s   [WIP 生产中，不进失败判定]" % (i, p))
        print("共 %d 包（ready %d / wip %d / EXCLUDES=%s）"
              % (len(ready) + len(wip), len(ready), len(wip), sorted(EXCLUDES)))
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())