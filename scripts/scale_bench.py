# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""万级规模基准（TASK-51A）：合成 1k/5k/10k 条目录，实测摄取/查询/内存。

用法：python scripts/scale_bench.py [--max 10000] [--sizes 1000,5000,10000]
输出：三档基准表（摄取秒、按分类路径查询、关键词查询、tracemalloc 峰值增量）。
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import tracemalloc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from catalog_ingest import Catalog  # noqa: E402

BIGS = ["计算机", "游戏机", "通讯与移动", "家电影音", "办公与计算外设",
        "嵌入式与工业", "其他"]
PATH_SAMPLES = [
    ["计算机", "个人机", "8位家用"],
    ["计算机", "小型机", "DEC系"],
    ["计算机", "工作站", "RISC"],
    ["游戏机", "家用机", "世嘉系"],
    ["游戏机", "掌机", "任天堂系"],
    ["通讯与移动", "手机", "功能机"],
    ["通讯与移动", "PDA", "笔式"],
    ["家电影音", "影碟机", "VCD"],
    ["家电影音", "影碟机", "DVD"],
    ["办公与计算外设", "打印机", "针式"],
    ["办公与计算外设", "存储", "磁盘驱动器"],
    ["嵌入式与工业", "单板机", "Arduino系"],
]


def synth_rows(n: int) -> list[dict]:
    rows = []
    for i in range(n):
        p = PATH_SAMPLES[i % len(PATH_SAMPLES)]
        rows.append({
            "id": "C-%06d" % i,
            "name": "合成设备%05d号" % (i + 1),
            "aliases": ["synth%05d" % (i + 1)],
            "maker": "合成厂%d" % (i % 40),
            "origin": "合成地",
            "year": 1900 + (i % 126),
            "path": p,
            "reason": "合成基准条目",
            "status": "planned",
            "device_id": None,
            "sources": [],
        })
    return rows


def bench(n: int) -> dict:
    tracemalloc.start()
    t0 = time.perf_counter()
    cat = Catalog(synth_rows(n))
    t_ingest = time.perf_counter() - t0

    t0 = time.perf_counter()
    hit = cat.list_path("/".join(PATH_SAMPLES[0]))
    t_path = time.perf_counter() - t0

    t0 = time.perf_counter()
    found = cat.find("合成设备%05d号" % n)
    t_find = time.perf_counter() - t0

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"n": n, "ingest_s": round(t_ingest, 3),
            "path_query_ms": round(t_path * 1000, 2),
            "find_query_ms": round(t_find * 1000, 2),
            "path_hits": len(hit), "found": len(found),
            "peak_mb": round(peak / 1024 / 1024, 1)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="万级目录规模基准")
    ap.add_argument("--sizes", default="1000,5000,10000")
    ap.add_argument("--max", type=int, default=10000)
    args = ap.parse_args(argv)
    sizes = [int(x) for x in args.sizes.split(",") if int(x) <= args.max]
    print("%-8s %-10s %-12s %-12s %-10s %-8s %-8s"
          % ("规模", "摄取(s)", "路径查询(ms)", "关键词(ms)", "路径命中", "关键词命中", "峰值(MB)"))
    results = []
    for n in sizes:
        r = bench(n)
        results.append(r)
        print("%-8d %-10s %-12s %-12s %-10d %-8d %-8s"
              % (r["n"], r["ingest_s"], r["path_query_ms"], r["find_query_ms"],
                 r["path_hits"], r["found"], r["peak_mb"]))
    if results:
        last = results[-1]
        print("\n结论（%d 条）：摄取 %.3fs / 路径查询 %s ms / 关键词 %s ms / 峰值 %s MB"
              % (last["n"], last["ingest_s"], last["path_query_ms"],
                 last["find_query_ms"], last["peak_mb"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())