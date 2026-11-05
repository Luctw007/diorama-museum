# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""拆解入口接线自检（TASK-106B）：不发引擎、纯文本级核对 E 键链路的静态契约。

检查项（X-01~X-05）：
  X-01 inspect_controller.gd 声明 `_selected`（点选系统输出端）；
  X-02 inspect_controller.gd 存在输入事件处理（_unhandled_input 含 KEY_E 分支）；
  X-03 调用点转发的方法名（*:set_exploded/set_close）在 explode_controller.gd 的
       函数表中存在（入口函数名与调用点匹配）；
  X-04 Esc/B 回退分支存在且调用 set_close（回到行走）；
  X-05 状态布尔开关 _explode_mode 声明存在（注释布尔语义）。

用法：python 01/scripts/explode_entry_check.py [--dir <godot_root>]
退出码：0=全 PASS；1=存在 FAIL（FAIL 时逐条列出调用链断点）。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FUNC_RE = re.compile(r"^func\s+(\w+)\s*\(", re.M)
CHAIN_RE = re.compile(r"(\w+)\s*\.\s*(set_exploded|set_close|set_open|reset_explode|set_explode_value)\s*\(")

fails = 0


def check(ok: bool, desc: str) -> None:
    global fails
    print("  [%s] %s" % ("PASS" if ok else "FAIL", desc))
    if not ok:
        fails += 1


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def code_only(text: str) -> str:
    """剔除注释行（#/##），避免把 docstring 里的方法名误判成调用点。"""
    return "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))


def parse_funcs(text: str) -> set[str]:
    return {m.group(1) for m in FUNC_RE.finditer(text)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="拆解入口接线自检")
    ap.add_argument("--dir", default=os.path.join(REPO, "godot"))
    args = ap.parse_args(argv)

    inspect_path = os.path.join(args.dir, "scripts", "inspect_controller.gd")
    explode_path = os.path.join(args.dir, "scripts", "explode_controller.gd")
    for p, tag in ((inspect_path, "inspect"), (explode_path, "explode")):
        if not os.path.isfile(p):
            print("!! 文件缺失：%s" % p)
            return 2

    inspect = read(inspect_path)
    explode = read(explode_path)
    explode_funcs = parse_funcs(explode)
    inspect_code = code_only(inspect)

    print("== 拆解入口接线自检（X-01~X-05）")
    check(re.search(r"^var\s+_selected\s*:", inspect, re.M) is not None,
          "X-01 inspect_controller 输出端 _selected 声明存在")

    check("_unhandled_input" in parse_funcs(inspect) and "KEY_E" in inspect,
          "X-02 输入事件处理存在（_unhandled_input + KEY_E 分支）")

    # X-03 调用点 → explode 函数表对账（含调用链断点清单；只看代码行，注释不计）
    chain = CHAIN_RE.findall(inspect_code)
    check(bool(chain), "X-03 调用点转发存在（%d 处）" % len(chain))
    for var, method in chain:
        if method in explode_funcs:
            check(True, "X-03 %s.%s() → explode_controller 函数表中存在 %s()"
                  % (var, method, method))
        else:
            check(False, "X-03 调用链断点：%s.%s() 调用了 explode_controller 中不存在的 %s()"
                  % (var, method, method))

    check(("KEY_ESCAPE" in inspect) and ("KEY_B" in inspect),
          "X-04 Esc/B 回退分支存在")
    check("set_close" in [m for _, m in chain] and "set_close" in explode_funcs,
          "X-04 回退调用 set_close() 且该函数在 explode_controller 中存在")

    check(re.search(r"^var\s+_explode_mode\s*[:=]", inspect, re.M) is not None,
          "X-05 状态布尔开关 _explode_mode 声明存在")

    print("汇总：%s" % ("全 PASS" if fails == 0 else "%d 项 FAIL" % fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())