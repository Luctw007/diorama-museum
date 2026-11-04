# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""引擎脚本符号级自检（TASK-66A）：无法实机运行时，静态核对 12 个 gd 脚本的互调 API。

检查项：
  G-01 每文件 func/signal/const/class_name 声明收集（符号表）；
  G-02 preload path 存在（与磁盘对账）；
  G-03 字符串式跨脚本引用：has_method("x")/connect("sig")/emit_signal 的符号必须在
      全脚本符号池中存在；不在者列入 KNOWN_GAPS（注明原因）或报 MISS；
  G-04 main.tscn 的脚本挂点已由 scene_check 负责（本步只引用其结果口径）。
用法：python scripts/gd_symbol_check.py [--json]；退出码 0=MISS 为空；1=存在未登记 MISS。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GD_DIR = os.path.join(REPO, "godot", "scripts")

FUNC_RE = re.compile(r"^func\s+(\w+)\s*\(")
SIGNAL_RE = re.compile(r"^signal\s+(\w+)")
CONST_RE = re.compile(r"^const\s+(\w+)")
CLASSNAME_RE = re.compile(r"^class_name\s+(\w+)")
PRELOAD_RE = re.compile(r'preload\("([^"]+)"\)')
HAS_METHOD_RE = re.compile(r'has_method\("(\w+)"\)')
CONNECT_RE = re.compile(r'connect\("(\w+)"')
STRING_CALL_RE = re.compile(r'get_node_or_null\("([A-Za-z0-9_/]+)"\)')

# 已知缺口登记（每条：符号, 原因）。不阻断、打印 KG 行。
KNOWN_GAPS = {
    # 例：输入视觉尚未实装的函数可以登记于此；当前猜测项需实机确认的暂不预登记
}


def parse_gd(path: str) -> dict:
    info = {"file": os.path.basename(path), "funcs": set(), "signals": set(),
            "consts": set(), "class_names": set(), "preloads": [],
            "has_method": set(), "connect": set(), "nodes": set()}
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for line in text.splitlines():
        m = FUNC_RE.match(line.strip())
        if m:
            info["funcs"].add(m.group(1))
        m = SIGNAL_RE.match(line.strip())
        if m:
            info["signals"].add(m.group(1))
        m = CONST_RE.match(line.strip())
        if m:
            info["consts"].add(m.group(1))
        m = CLASSNAME_RE.match(line.strip())
        if m:
            info["class_names"].add(m.group(1))
    info["preloads"] = sorted(set(PRELOAD_RE.findall(text)))
    info["has_method"] = set(HAS_METHOD_RE.findall(text))
    info["connect"] = set(CONNECT_RE.findall(text))
    info["nodes"] = set(STRING_CALL_RE.findall(text))
    return info


def symname(entry: dict) -> str:
    return (entry["class_names"] or {os.path.splitext(entry["file"])[0]}).pop()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="引擎脚本符号级自检")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    files = sorted(f for f in os.listdir(GD_DIR) if f.endswith(".gd"))
    infos = [parse_gd(os.path.join(GD_DIR, f)) for f in files]

    pool_funcs: set = set()
    pool_signals: set = set()
    class_index: dict[str, str] = {}
    base_of: dict[str, str] = {}
    for e in infos:
        pool_funcs |= e["funcs"]
        pool_signals |= e["signals"]
        base_of[e["file"]] = symname(e)
        for cn in e["class_names"]:
            class_index[cn] = e["file"]

    rows: list[dict] = []
    miss = 0
    kg = 0
    for e in infos:
        rows.append({"file": e["file"], "name": symname(e),
                     "funcs": len(e["funcs"]), "signals": len(e["signals"]),
                     "checks": []})
        # G-02 preload 存在性
        for p in e["preloads"]:
            rel = p.replace("res://", "")
            ok = os.path.isfile(os.path.join(REPO, "godot", rel))
            rows[-1]["checks"].append([("OK" if ok else "MISS"), "preload " + rel])
            if not ok:
                miss += 1
        # G-03 has_method 全池核对
        for mth in sorted(e["has_method"]):
            if mth in pool_funcs:
                rows[-1]["checks"].append(["OK", "has_method %s → 存在" % mth])
            elif mth in KNOWN_GAPS:
                rows[-1]["checks"].append(["KG", "has_method %s → %s" % (mth, KNOWN_GAPS[mth])])
                kg += 1
            else:
                rows[-1]["checks"].append(["MISS", "has_method %s → 全池不存在" % mth])
                miss += 1
        # G-03 connect 信号核对
        for sig in sorted(e["connect"]):
            if sig in pool_signals:
                rows[-1]["checks"].append(["OK", "connect %s → 存在" % sig])
            elif sig in KNOWN_GAPS:
                rows[-1]["checks"].append(["KG", "connect %s → %s" % (sig, KNOWN_GAPS[sig])])
                kg += 1
            else:
                rows[-1]["checks"].append(["MISS", "connect %s → 全池不存在" % sig])
                miss += 1

    if args.json:
        print(json.dumps({"pool_funcs": sorted(pool_funcs),
                          "pool_signals": sorted(pool_signals),
                          "rows": rows}, ensure_ascii=False, indent=2))
    for r in rows:
        print("== %-22s [%s] funcs=%d signals=%d" % (
            r["file"], r["name"], r["funcs"], r["signals"]))
        for tag, desc in r["checks"]:
            print("   [%s] %s" % (tag, desc))
    print("汇总：%d 文件；符号池 funcs %d / signals %d；MISS %d；已知缺口 KG %d"
          % (len(infos), len(pool_funcs), len(pool_signals), miss, kg))
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())