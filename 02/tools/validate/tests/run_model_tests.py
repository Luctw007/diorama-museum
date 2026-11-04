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
建模预算校验器反例测试（TASK-27A）

用法：
    python run_model_tests.py

从 test-device 复制到临时目录、对 mainboard.gltf 施加单一破坏后运行 model_check.py，
断言命中预期规则编号与级别（PASS/WARN/FAIL）。覆盖 MR-01~MR-04 全部规则的违规路径。

反例清单：
    01 节点名不符 → MR-01 FAIL
    02 超预算（≤1.5 倍）→ MR-02 WARN
    03 超预算（>1.5 倍）→ MR-02 FAIL
    04 贴图尺寸超 2048 → MR-03 WARN
    05 贴图尺寸非 2 的幂 → MR-03 WARN
    06 未知扩展 → MR-04 WARN
    07 场景多根 → MR-01 WARN
"""
from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CHECK = os.path.abspath(os.path.join(TESTS_DIR, "..", "model_check.py"))
REPO = os.path.abspath(os.path.join(TESTS_DIR, "..", "..", ".."))
EXAMPLE = os.path.join(REPO, "content", "test-device")

PASSED = 0
FAILED = 0


def run_model_check(pkg: str):
    proc = subprocess.run(
        [sys.executable, MODEL_CHECK, pkg],
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.returncode, proc.stdout + proc.stderr


def report(name: str, ok: bool, detail: str = ""):
    global PASSED, FAILED
    mark = "PASS" if ok else "FAIL"
    if ok:
        PASSED += 1
    else:
        FAILED += 1
    print(f"[{mark}] {name}" + (f"  — {detail}" if detail else ""))


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_png(path: str, w: int, h: int):
    """写一个仅含签名+IHDR 的最小 PNG 头（image_size_from_file 可解析宽高）。"""
    sig = b"\x89PNG\r\n\x1a\n"
    with open(path, "wb") as f:
        f.write(sig + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", w, h))


def expect(name: str, mutator, rule: str, level: str):
    """复制 test-device → 施加 mutator(gltf, pkg) → 跑 model_check → 断言命中 rule+level。"""
    tmp = tempfile.mkdtemp(prefix="hako_model_")
    pkg = os.path.join(tmp, "test-device")
    shutil.copytree(EXAMPLE, pkg)
    gltf_path = os.path.join(pkg, "meshes", "mainboard.gltf")
    gltf = load_json(gltf_path)
    mutator(gltf, pkg)
    save_json(gltf_path, gltf)
    code, out = run_model_check(pkg)
    ok = any((rule in ln) and (level in ln) for ln in out.splitlines())
    report(name, ok, f"exit={code}, 命中 {rule} {level}" if ok else f"exit={code}, 未命中 {rule} {level}")
    if not ok:
        for ln in out.splitlines():
            if ln.strip().startswith(("PASS", "WARN", "FAIL")):
                print("      " + ln.strip())
    shutil.rmtree(tmp, ignore_errors=True)


def _add_texture(gltf: dict, pkg: str, w: int, h: int, uri: str = "board_basecolor.png"):
    """给 glTF 追加 image/texture 引用，并写入 w×h 的 PNG。"""
    gltf.setdefault("images", []).append({"uri": uri})
    gltf.setdefault("textures", []).append({"source": len(gltf["images"]) - 1})
    mat = gltf["materials"][0]
    mat.setdefault("pbrMetallicRoughness", {})["baseColorTexture"] = {
        "index": len(gltf["textures"]) - 1
    }
    write_png(os.path.join(pkg, "meshes", uri), w, h)


def main() -> int:
    print("=" * 70)
    print("TASK-27A 建模预算校验器反例测试（model_check.py）")
    print("=" * 70)

    cases = [
        ("反例01：节点名不符 → MR-01 FAIL",
         lambda g, p: g["nodes"][0].__setitem__("name", "wrong_name"),
         "MR-01", "FAIL"),
        ("反例02：超预算（≤1.5 倍）→ MR-02 WARN",
         lambda g, p: g["accessors"][1].__setitem__("count", 63000),  # 21000 三角面
         "MR-02", "WARN"),
        ("反例03：超预算（>1.5 倍）→ MR-02 FAIL",
         lambda g, p: g["accessors"][1].__setitem__("count", 90003),  # 30001 三角面
         "MR-02", "FAIL"),
        ("反例04：贴图尺寸超 2048 → MR-03 WARN",
         lambda g, p: _add_texture(g, p, 2049, 2049),
         "MR-03", "WARN"),
        ("反例05：贴图尺寸非 2 的幂 → MR-03 WARN",
         lambda g, p: _add_texture(g, p, 1000, 1000),
         "MR-03", "WARN"),
        ("反例06：未知扩展 → MR-04 WARN",
         lambda g, p: g.__setitem__("extensionsUsed", ["KHR_unknown_thing"]),
         "MR-04", "WARN"),
        ("反例07：场景多根 → MR-01 WARN",
         lambda g, p: (g["scenes"][0].__setitem__("nodes", [0, 1]),
                       g["nodes"].append({"mesh": 0, "name": "mainboard_dup"})),
         "MR-01", "WARN"),
    ]

    for name, mutator, rule, level in cases:
        expect(name, mutator, rule, level)

    print("-" * 70)
    print(f"结果：PASS {PASSED}，FAIL {FAILED}")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
