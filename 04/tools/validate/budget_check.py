#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2026 箱庭电子博物馆项目组 (Hako Electronic Museum Project)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
资产预算检查器（TASK-02，v0.1）

用法：
    python budget_check.py <gltf 文件> [--level L2]

读取单个 glTF（.gltf JSON 或 .glb）统计节点数与三角面数，并对照
《内容包规范 v0.1》第五章 L1–L4 预算（v0.1 起始值，可调）输出统计与超限提示。

退出码：0=统计成功；1=文件不可解析；2=参数错误。
预算数字为 v0.1 起始值，标注为「可调」，不做硬阻塞。
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_gltf, count_gltf_triangles  # noqa: E402

# v0.1 预算（每台设备 / 每模型，起始值，可调）
BUDGETS = {
    "L1": {"triangles": 2_000, "nodes": 50, "texture": 512},
    "L2": {"triangles": 20_000, "nodes": 500, "texture": 2048},
    "L3": {"triangles": 200_000, "nodes": 5_000, "texture": 4096},
    "L4": {"triangles": 2_000_000, "nodes": 50_000, "texture": 8192},
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="glTF 资产预算检查器（v0.1）")
    parser.add_argument("gltf_path", help="glTF 文件（.gltf 或 .glb）")
    parser.add_argument("--level", default=None, choices=["L1", "L2", "L3", "L4"],
                        help="对照的精度分级（可选）")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.gltf_path):
        sys.stderr.write(f"错误：文件不存在：{args.gltf_path}\n")
        return 2

    try:
        gltf = load_gltf(args.gltf_path)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"错误：glTF 解析失败：{e}\n")
        return 1

    nodes = len(gltf.get("nodes", []))
    scenes = len(gltf.get("scenes", []))
    meshes = len(gltf.get("meshes", []))
    triangles = count_gltf_triangles(gltf)
    version = gltf.get("asset", {}).get("version", "?")

    print(f"文件       : {args.gltf_path}")
    print(f"glTF 版本 : {version}")
    print(f"场景数    : {scenes}")
    print(f"节点数    : {nodes}")
    print(f"网格数    : {meshes}")
    print(f"三角面数  : {triangles}（估算）")

    if args.level:
        b = BUDGETS[args.level]
        over = []
        if triangles > b["triangles"]:
            over.append(f"三角面 {triangles} > {b['triangles']}")
        if nodes > b["nodes"]:
            over.append(f"节点 {nodes} > {b['nodes']}")
        print("-" * 50)
        print(f"精度分级  : {args.level}（v0.1 起始预算，可调）")
        print(f"  面数上限: {b['triangles']}  节点上限: {b['nodes']}  纹理上限: {b['texture']}px")
        if over:
            print("超限提示  : " + "；".join(over))
            print("结论      : 超限（v0.1 不阻塞，供作者优化参考）")
            return 0
        print("结论      : 在预算内")
    return 0


if __name__ == "__main__":
    sys.exit(main())
