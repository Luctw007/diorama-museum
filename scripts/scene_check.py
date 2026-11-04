# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""主场景静态校验（TASK-26B）：在不安装 Godot 的前提下，对 scenes/main.tscn 做文本级检查。

检查项（S-01~S-06）：
  S-01 load_steps 计数 == 资源总数+1；
  S-02 所有 ext_resource Script 路径在仓库内存在；
  S-03 节点 script= 引用的 ext id 均已在文件头声明；
  S-04 所有 SubResource 引用已声明；
  S-05 ExhibitHost 节点的 layout_file 指定的布局 JSON 存在（godot/content/）；
  S-06 场景内脚本的重复挂载提示（DeviceRoot/DeviceLoader 与 ExhibitHost 并存属
      设计有意为之：直接单机模式 + 展厅模式；本检查只提示不报错）。

用法：python scripts/scene_check.py [--tscn godot/scenes/main.tscn]
退出码：0=通过；1=存在违规。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TSCN = os.path.join(REPO, "godot", "scenes", "main.tscn")

EXT_RE = re.compile(r'\[ext_resource[^\]]*type="Script"[^\]]*path="([^"]+)"[^\]]*id="([^"]+)"')
SUB_DECL_RE = re.compile(r'\[sub_resource[^\]]*id="([^"]+)"')
SUB_USE_RE = re.compile(r'SubResource\("([^"]+)"\)')
NODE_SCRIPT_RE = re.compile(r'^script = ExtResource\("([^"]+)"\)')
LAYOUT_RE = re.compile(r'^layout_file = "([^"]+)"')


def check(condition: bool, desc: str) -> bool:
    print("  [%s] %s" % ("PASS" if condition else "FAIL", desc))
    return condition


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="main.tscn 静态校验")
    ap.add_argument("--tscn", default=DEFAULT_TSCN)
    args = ap.parse_args(argv)

    with open(args.tscn, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    fails = 0

    # S-01 load_steps
    m = re.match(r"\[gd_scene load_steps=(\d+)[^\]]*\]", lines[0] or "")
    declared = int(m.group(1)) if m else -1
    n_ext = text.count("[ext_resource")
    n_sub = text.count("[sub_resource")
    expected = n_ext + n_sub + 1
    if not check(declared == expected,
                 "S-01 load_steps=%d（ext %d + sub %d + 1 = %d）"
                 % (declared, n_ext, n_sub, expected)):
        fails += 1

    # S-02 ext 路径存在
    ext_paths: dict[str, str] = {}
    for pm, pid in EXT_RE.findall(text):
        ext_paths[pid] = pm
        rel = pm.replace("res://", "")
        ok = os.path.isfile(os.path.join(REPO, "godot", rel))
        if not check(ok, "S-02 %s (%s) 文件存在" % (pid, pm)):
            fails += 1

    # S-03 节点 script 引用的 id 已声明
    for ln in lines:
        am = NODE_SCRIPT_RE.match(ln)
        if am and am.group(1) not in ext_paths:
            check(False, "S-03 节点引用了未声明的脚本 id %s（行: %s）"
                  % (am.group(1), ln.strip()))
            fails += 1

    # S-04 SubResource 引用已声明
    declared_subs = set(SUB_DECL_RE.findall(text))
    for used in SUB_USE_RE.findall(text):
        if used not in declared_subs:
            check(False, "S-04 SubResource(%s) 未声明" % used)
            fails += 1

    # S-05 ExhibitHost 布局文件存在
    for lm in LAYOUT_RE.findall(text):
        layout_path = os.path.join(REPO, "godot", "content", lm)
        if not check(os.path.isfile(layout_path),
                     "S-05 布局文件 godot/content/%s 存在" % lm):
            fails += 1

    # S-06 并存提示（只提示）
    if "3_device" in ext_paths and "8_host" in ext_paths:
        print("  [INFO] S-06 DeviceLoader 与 ExhibitHost 并存（设计有意：单机直连 + 展厅模式）")

    if check(not fails and n_ext >= 8, "总检：main.tscn 静态校验通过（ext %d / sub %d）"
             % (n_ext, n_sub)):
        print("主场景接线静态合法（待 Godot 实机确认表现层）")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())