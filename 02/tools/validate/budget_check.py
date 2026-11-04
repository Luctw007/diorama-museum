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
资产预算检查器（TASK-07，v0.2 补完）

用法：
    python budget_check.py <gltf 文件> [--level L2]

读取单个 glTF（.gltf JSON 或 .glb）精确统计：
  - 场景数 / 节点数 / 网格数 / primitive 数 / material 数
  - 顶点数（各 primitive POSITION accessor 计数之和）
  - 三角面数（按 primitive.mode，默认 TRIANGLES：indices 计数 / 3）
并解析 glTF images 引用的 PNG/JPEG 纹理尺寸（纯 stdlib 解析文件头，
PNG IHDR / JPEG SOF0），逐纹理报告宽高与超限结果。

对照《内容包规范 v0.2》第五章 L1–L4 预算（v0.2 起始值，可调）输出统计。
预算数字为 v0.2 起始值，标注「可调」，不做硬阻塞。

退出码：0=成功；1=文件不可解析；2=参数错误。
"""
from __future__ import annotations

import argparse
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_gltf  # noqa: E402

# v0.2 预算（每台设备 / 每模型，起始值，可调）
BUDGETS = {
    "L1": {"triangles": 2_000, "nodes": 50, "texture": 512, "anim_sec": 60.0},
    "L2": {"triangles": 20_000, "nodes": 500, "texture": 2048, "anim_sec": 180.0},
    "L3": {"triangles": 200_000, "nodes": 5_000, "texture": 4096, "anim_sec": 300.0},
    "L4": {"triangles": 2_000_000, "nodes": 50_000, "texture": 8192, "anim_sec": 600.0},
}

PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8"


# ---------------------------------------------------------------------------
# glTF 精确统计
# ---------------------------------------------------------------------------
def count_vertices(gltf: dict) -> int:
    """各 primitive 的 POSITION accessor 计数之和（顶点数）。"""
    accessors = gltf.get("accessors", [])
    total = 0
    for mesh in gltf.get("meshes", []):
        for prim in mesh.get("primitives", []):
            pos = prim.get("attributes", {}).get("POSITION")
            if pos is not None and pos < len(accessors):
                total += accessors[pos].get("count", 0)
    return total


def count_triangles_exact(gltf: dict) -> int:
    """按 primitive.mode 精确统计三角面数（默认 4=TRIANGLES）。"""
    accessors = gltf.get("accessors", [])
    total = 0
    for mesh in gltf.get("meshes", []):
        for prim in mesh.get("primitives", []):
            mode = prim.get("mode", 4)
            if mode == 4:  # TRIANGLES
                idx = prim.get("indices")
                if idx is not None and idx < len(accessors):
                    total += accessors[idx].get("count", 0) // 3
                else:
                    pos = prim.get("attributes", {}).get("POSITION")
                    if pos is not None and pos < len(accessors):
                        total += accessors[pos].get("count", 0) // 3
            elif mode in (5, 6):  # TRIANGLE_STRIP / TRIANGLE_FAN
                pos = prim.get("attributes", {}).get("POSITION")
                if pos is not None and pos < len(accessors):
                    n = accessors[pos].get("count", 0)
                    total += max(0, n - 2)
    return total


def count_primitives(gltf: dict) -> int:
    return sum(len(m.get("primitives", [])) for m in gltf.get("meshes", []))


# ---------------------------------------------------------------------------
# 纹理尺寸解析（纯 stdlib）
# ---------------------------------------------------------------------------
def png_size(data: bytes):
    """从 PNG 字节流解析 (width, height)。读取 IHDR 块。"""
    if data[:8] != PNG_SIG:
        raise ValueError("不是 PNG 文件（签名不符）")
    if len(data) < 24:
        raise ValueError("PNG 过短")
    if data[12:16] != b"IHDR":
        raise ValueError("PNG 首个 chunk 不是 IHDR")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def jpeg_size(data: bytes):
    """从 JPEG 字节流解析 (width, height)。读取 SOF0/SOF1/SOF2 帧头。"""
    if data[:2] != JPEG_SIG:
        raise ValueError("不是 JPEG 文件（签名不符）")
    i = 2
    n = len(data)
    SOF_MARKERS = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                   0xC9, 0xCA, 0xCB, 0x0D, 0xCE, 0xCF}
    while i + 4 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0xFF:
            i += 1
            continue
        if marker in SOF_MARKERS:
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = int.from_bytes(data[i + 2:i + 4], "big")
        i += 2 + seg_len
    raise ValueError("JPEG 未找到 SOF 帧头")


def image_size_from_bytes(data: bytes):
    """按魔数分派 PNG/JPEG 解析，返回 (width, height)。"""
    if data[:8] == PNG_SIG:
        return png_size(data)
    if data[:2] == JPEG_SIG:
        return jpeg_size(data)
    raise ValueError("不支持的类型（仅 PNG/JPEG）")


def image_size_from_file(path: str):
    with open(path, "rb") as f:
        data = f.read()
    return image_size_from_bytes(data)


# ---------------------------------------------------------------------------
# glTF 纹理解析
# ---------------------------------------------------------------------------
def gltf_textures(gltf: dict, base_dir: str):
    """解析 glTF images 引用的纹理，返回 [(name, (w,h)|None, note)]。"""
    result = []
    for img in gltf.get("images", []):
        uri = img.get("uri")
        mime = img.get("mimeType", "")
        name = img.get("name", "?")
        data = None
        src = None
        if uri and uri.startswith("data:"):
            try:
                payload = uri.split(",", 1)[1]
                data = base64.b64decode(payload)
                src = f"data:{mime or 'image'}"
            except Exception as e:  # noqa: BLE001
                result.append((name, None, f"data URI 解码失败：{e}"))
                continue
        elif uri:
            path = os.path.join(base_dir, uri)
            if not os.path.isfile(path):
                result.append((name, None, f"纹理文件不存在：{uri}"))
                continue
            src = uri
            try:
                with open(path, "rb") as f:
                    data = f.read()
            except OSError as e:
                result.append((name, None, f"读取失败：{e}"))
                continue
        else:
            result.append((name, None, "bufferView 内嵌纹理（未解析）"))
            continue
        try:
            w, h = image_size_from_bytes(data)
            result.append((name, (w, h), src))
        except Exception as e:  # noqa: BLE001
            result.append((name, None, f"尺寸解析失败：{e}"))
    return result


def render_textures(texture_max: int, textures):
    """打印逐纹理表并返回是否超限。"""
    print(f"{'纹理名':<20} {'宽':>6} {'高':>6} {'超限':>6}   来源")
    print("-" * 64)
    any_over = False
    for name, size, note in textures:
        if size is None:
            print(f"{name:<20} {'-':>6} {'-':>6} {'-':>6}   {note}")
            continue
        w, h = size
        over = w > texture_max or h > texture_max
        any_over = any_over or over
        print(f"{name:<20} {w:>6} {h:>6} {'是' if over else '否':>6}   {note}")
    return any_over


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="glTF 资产预算检查器（v0.2）")
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

    base_dir = os.path.dirname(os.path.abspath(args.gltf_path))
    nodes = len(gltf.get("nodes", []))
    scenes = len(gltf.get("scenes", []))
    meshes = len(gltf.get("meshes", []))
    primitives = count_primitives(gltf)
    materials = len(gltf.get("materials", []))
    vertices = count_vertices(gltf)
    triangles = count_triangles_exact(gltf)
    version = gltf.get("asset", {}).get("version", "?")

    print(f"文件         : {args.gltf_path}")
    print(f"glTF 版本    : {version}")
    print(f"场景数       : {scenes}")
    print(f"节点数       : {nodes}")
    print(f"网格数       : {meshes}")
    print(f"primitive 数 : {primitives}")
    print(f"material 数  : {materials}")
    print(f"顶点数       : {vertices}")
    print(f"三角面数     : {triangles}（精确）")

    textures = gltf_textures(gltf, base_dir)
    print(f"纹理数       : {len(textures)}")

    if args.level:
        b = BUDGETS[args.level]
        over = []
        if triangles > b["triangles"]:
            over.append(f"三角面 {triangles} > {b['triangles']}")
        if nodes > b["nodes"]:
            over.append(f"节点 {nodes} > {b['nodes']}")
        print("-" * 64)
        print(f"精度分级     : {args.level}（v0.2 起始预算，可调）")
        print(f"  面数上限 {b['triangles']}  节点上限 {b['nodes']}  纹理上限 {b['texture']}px  动画时长上限 {b['anim_sec']}s")
        print()
        tex_over = render_textures(b["texture"], textures)
        if over or tex_over:
            if over:
                print("超限提示     : " + "；".join(over))
            print("结论         : 超限（v0.2 不阻塞，供作者优化参考）")
        else:
            print("结论         : 在预算内")
    else:
        print("-" * 64)
        render_textures(10**9, textures)
    return 0


if __name__ == "__main__":
    sys.exit(main())
