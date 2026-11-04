# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""输入映射生成器（TASK-16B）：runtime.input_map → 玩家层 input_profile.json 骨架。

与 godot/scripts/input_profile.gd 的 JSON 结构对齐（actions/keyboard/mouse），
两层键名模型见 docs/runtime_mapping.md §5：input_map 的 action 名是设备逻辑动作，
本工具为其生成"默认宿主绑定"骨架（键盘 KEY_* → Godot 小写键名；摇杆 → joy_*）。

用法:
  python scripts/gen_input_profile.py <包目录>              # 单包
  python scripts/gen_input_profile.py --all                 # 五包
  python scripts/gen_input_profile.py --all --dry-run       # 只预览不写文件
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
# run_profile 为同目录脚本；复用其双形态条目归一（对象/legacy 字符串）
import run_profile as rp  # noqa: E402

# 默认目标：godot/content 下的包副本（避免写入 03/05 线源仓；先跑 sync_content.py）
PKGS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "godot", "content", pid)
    for pid in ("manchester-baby", "eniac", "edsac", "edvac", "apple-ii")
]

JOY_AXIS = {"axis_x": "joy_axis_x", "axis_y": "joy_axis_y"}
MOUSE_KEYS = {
    "motion": "mouse_motion", "btn_left": "mouse_button_left",
    "btn_right": "mouse_button_right", "btn_middle": "mouse_button_middle",
    "wheel_up": "mouse_wheel_up", "wheel_down": "mouse_wheel_down",
}


def default_binding(action: str, desc) -> tuple[str, str]:
    """返回 (区段, 绑定)；无法推导的返回 ("actions", "")。所属区段 ∈ actions/keyboard/mouse。"""
    if isinstance(desc, dict):
        mp = desc.get("map")
        key = str(desc.get("key", ""))
        if mp == "keyboard":
            binding = "key_" + key.removeprefix("KEY_").lower()
            if binding != "key_" and binding.isascii():
                return "keyboard", binding
        elif mp == "joystick":
            if key in JOY_AXIS:
                return "actions", JOY_AXIS[key]
            if key.startswith("btn"):
                digits = key.removeprefix("btn")
                if digits.isdigit():
                    return "actions", "joy_button_%s" % digits
            if key.startswith("hat_") and key[4:].isdigit():
                return "actions", "joy_hat_%s" % key[4:]
        elif mp == "mouse" and key in MOUSE_KEYS:
            return "mouse", MOUSE_KEYS[key]
        return "actions", ""
    if isinstance(desc, str):  # legacy 设备逻辑令牌（两层键名模型）
        parts = desc.split(".")
        leaf = parts[-1]
        prefix = parts[0] if len(parts) > 1 else ""
        if prefix == "keyboard" and leaf and leaf.isascii():
            binding = leaf if leaf.startswith("key_") else "key_" + leaf.lower()
            return "keyboard", binding
        return "actions", ""
    return "actions", ""


def build_profile(runtime: dict) -> dict:
    profile: dict = {"actions": {}, "keyboard": {}, "mouse": {}}
    unbound: list[str] = []
    for action, desc in rp._norm_key_map(runtime.get("input_map")).items():
        section, binding = default_binding(action, desc)
        if binding:
            profile[section][action] = binding
        else:
            profile["actions"][action] = ""
            unbound.append(action)
    profile["unbound"] = unbound
    profile["note"] = (
        "由 gen_input_profile.py 生成：默认宿主绑定骨架，待玩家自定义；"
        "unbound 为无法自动推导的设备逻辑动作")
    return profile


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="生成玩家层 input_profile.json 骨架")
    ap.add_argument("pkg_dir", nargs="?", help="内容包目录（含 runtime.json）")
    ap.add_argument("--all", action="store_true", help="处理五包")
    ap.add_argument("--dry-run", action="store_true", help="只预览不写文件")
    args = ap.parse_args(argv)

    targets = PKGS if args.all else ([os.path.abspath(args.pkg_dir)] if args.pkg_dir else [])
    if not targets:
        ap.error("需要 <包目录> 或 --all")

    rc = 0
    for pkg in targets:
        rt_path = os.path.join(pkg, "runtime.json")
        print("== %s" % os.path.basename(pkg))
        if not os.path.isfile(rt_path):
            print("   !! 缺少 runtime.json，跳过")
            rc = 1
            continue
        with open(rt_path, encoding="utf-8") as fh:
            runtime = json.load(fh)
        profile = build_profile(runtime)
        n_bound = (len(profile["keyboard"]) + len(profile["mouse"])
                   + sum(1 for v in profile["actions"].values() if v))
        print("   动作总数 %d；可自动绑定 %d；unbound %d"
              % (len(profile["actions"]) + len(profile["keyboard"])
                 + len(profile["mouse"]), n_bound, len(profile["unbound"])))
        for u in profile["unbound"]:
            print("     [unbound] %s" % u)
        if args.dry_run:
            continue
        out_path = os.path.join(pkg, "input_profile.json")
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(profile, fh, ensure_ascii=False, indent=2)
        print("   已写 %s" % out_path)
    return rc


if __name__ == "__main__":
    sys.exit(main())