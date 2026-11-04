# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""键码映射生成器 v2（TASK-31A）：runtime.input_map → <device>_keymap.json 骨架（多机种驱动）。

驱动（--driver）：
  apple2   默认：字符键 mame_char；特殊键 mame_code（CODE_MAP）；摇杆 paddle0/1 字段（26-A 语义）。
  a2600    Atari 2600：摇杆轴共享（joy_up/joy_down 同轴）→ direction 标注；开关键（F1..F4）→
           mame_code + "系统开关"note；全部 verify=true。
  famicom  FC 手柄：hat_N → dpad 字段（direction 取自动作名后缀）；btn 按下标分 pad0/pad1；
           系统键（ENTER/RSHIFT/INSERT/DELETE）→ mame_code，全部 verify=true。
生成骨架一律不入 the 最终键码表（值仅占位语义），须人工审校后定稿。

用法:
  python scripts/gen_keymap.py --pkg <包目录> --driver a2600|famicom [--out x.json] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import run_profile as rp  # noqa: E402  复用双形态归一（对象/legacy）

CHAR_RE = re.compile(r"^KEY_[A-Z0-9]$")
CODE_MAP = {   # 各机种系统/特殊键 → mame_code 骨架（全部 verify=true）
    "KEY_ENTER": "ENTER", "KEY_LEFT": "LEFT", "KEY_RIGHT": "RIGHT",
    "KEY_UP": "UP", "KEY_DOWN": "DOWN", "KEY_ESCAPE": "ESC",
    "KEY_SHIFT": "LSHIFT", "KEY_RSHIFT": "RSHIFT", "KEY_CTRL": "LCONTROL",
    "KEY_CAPSLOCK": "CAPSLOCK", "KEY_REPEAT": "REPT", "KEY_RESET": "RESET",
    "KEY_INSERT": "INSERT", "KEY_DELETE": "DEL", "KEY_POWER": "POWER",
    "KEY_F1": "F1", "KEY_F2": "F2", "KEY_F3": "F3", "KEY_F4": "F4",
    "KEY_F5": "F5", "KEY_F6": "F6", "KEY_F7": "F7", "KEY_F8": "F8",
}
DIR_SUFFIX_RE = re.compile(r"_(up|down|left|right)$")


def _direction_of(action: str) -> str | None:
    m = DIR_SUFFIX_RE.search(action)
    return m.group(1) if m else None


def entry_apple2(action: str, desc: dict) -> dict | None:
    mp, key = desc.get("map"), str(desc.get("key", ""))
    if mp == "keyboard":
        if CHAR_RE.match(key) and key != "KEY_SPACE":
            return {"mame_char": key[-1:].lower(), "verify": False}
        if key == "KEY_SPACE":
            return {"mame_char": " ", "verify": True}
        if key in CODE_MAP:
            return {"mame_code": CODE_MAP[key], "verify": True}
        return None
    if mp == "joystick":
        if key == "axis_x":
            return {"mame_field": {"tag": "paddle0", "field": "analog_x", "kind": "axis"},
                    "verify": True}
        if key == "axis_y":
            return {"mame_field": {"tag": "paddle0", "field": "analog_y", "kind": "axis"},
                    "verify": True}
        if re.match(r"^btn[0-9]+$", key):
            return {"mame_field": {"tag": "paddle0", "field": key, "kind": "button"},
                    "verify": True}
        return None
    return None


def entry_a2600(action: str, desc: dict) -> dict | None:
    mp, key = desc.get("map"), str(desc.get("key", ""))
    if mp == "joystick":
        if key in ("axis_x", "axis_y"):
            return {"mame_field": {"tag": "joy0", "field": "analog_x" if key == "axis_x"
                                   else "analog_y", "kind": "axis"},
                    "direction": _direction_of(action), "verify": True,
                    "note": "2600 方向键两动作共享同一轴（取值正负区分）"}
        if re.match(r"^btn[0-9]+$", key):
            return {"mame_field": {"tag": "joy0", "field": key, "kind": "button"},
                    "verify": True}
        return None
    if mp == "keyboard" and key in CODE_MAP:
        entry = {"mame_code": CODE_MAP[key], "verify": True}
        if key.startswith("KEY_F"):
            entry["note"] = "系统拨档开关（difficulty/tv_type 等）经 MAME 键位/端口映射，[需核实]"
        return entry
    return None


def entry_famicom(action: str, desc: dict) -> dict | None:
    mp, key = desc.get("map"), str(desc.get("key", ""))
    if mp == "joystick":
        if re.match(r"^hat_[0-9]+$", key):
            pad = "pad1" if action.startswith("p2_") else "pad0"
            return {"mame_field": {"tag": pad, "field": key, "kind": "dpad"},
                    "direction": _direction_of(action), "verify": True}
        if re.match(r"^btn[0-9]+$", key):
            idx = int(key[3:])
            pad = "pad0" if idx < 2 else "pad1"
            return {"mame_field": {"tag": pad, "field": "btn%d" % idx, "kind": "button"},
                    "verify": True}
        return None
    if mp == "keyboard" and key in CODE_MAP:
        return {"mame_code": CODE_MAP[key], "verify": True}
    return None


DRIVERS = {"apple2": entry_apple2, "a2600": entry_a2600, "famicom": entry_famicom}


def build_map(runtime: dict, driver: str) -> dict:
    fn = DRIVERS[driver]
    entries: dict = {}
    unmapped: list = []
    for action, desc in rp._norm_key_map(runtime.get("input_map")).items():
        if not isinstance(desc, dict):
            unmapped.append({"action": action, "desc": str(desc)[:80]})
            continue
        entry = fn(action, desc)
        if entry is None:
            unmapped.append({"action": action, "desc": "%s:%s" % (desc.get("map"),
                                                                  desc.get("key"))})
            continue
        entries[action] = entry
    return {"entries": entries, "unmapped": unmapped}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="生成后端键码映射骨架（多机种）")
    ap.add_argument("--pkg", required=True, help="内容包目录（含 runtime.json）")
    ap.add_argument("--driver", choices=sorted(DRIVERS), default="apple2")
    ap.add_argument("--out", help="输出 JSON 路径")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    rt_path = os.path.join(args.pkg, "runtime.json")
    if not os.path.isfile(rt_path):
        print("缺少 runtime.json: %s" % rt_path)
        return 1
    with open(rt_path, encoding="utf-8") as fh:
        runtime = json.load(fh)
    result = build_map(runtime, args.driver)
    n_entries, n_unmapped = len(result["entries"]), len(result["unmapped"])
    print("[%s] 动作 %d；已覆盖 %d；unmapped %d"
          % (args.driver, n_entries + n_unmapped, n_entries, n_unmapped))
    for u in result["unmapped"]:
        print("  [unmapped] %s -> %s" % (u["action"], u["desc"]))
    if args.dry_run:
        return 0
    out_path = args.out or os.path.join(args.pkg, "keymap.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print("已写 %s" % out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())