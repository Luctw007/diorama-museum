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
校验器测试套件（TASK-02）

用法：
    python run_tests.py

正例：直接对 content/test-device 运行 validate.py，断言退出码 0 且全 PASS。
反例：从示例包复制到临时目录、施加单一破坏后运行 validate.py，断言退出码非 0
     且命中对应规则编号。反例覆盖 ≥5 类：缺引用 / 循环父子 / 命名违规 /
     缺 THIRD_PARTY / 含未定标记文案 / transform 越界。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
VALIDATE = os.path.abspath(os.path.join(TESTS_DIR, "..", "validate.py"))
REPO = os.path.abspath(os.path.join(TESTS_DIR, "..", "..", ".."))
EXAMPLE = os.path.join(REPO, "content", "test-device")

PASSED = 0
FAILED = 0


def run_validate(pkg: str):
    proc = subprocess.run(
        [sys.executable, VALIDATE, pkg],
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


def load_meta(pkg: str):
    with open(os.path.join(pkg, "meta.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def save_meta(pkg: str, meta: dict):
    with open(os.path.join(pkg, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def make_fixture(mutator) -> str:
    """复制示例包到临时目录并施加 mutator(meta, pkg)，返回临时目录路径。"""
    tmp = tempfile.mkdtemp(prefix="hako_test_")
    pkg = os.path.join(tmp, "test-device")
    shutil.copytree(EXAMPLE, pkg)
    meta = load_meta(pkg)
    mutator(meta, pkg)
    save_meta(pkg, meta)
    return pkg


def expect_fail(name: str, mutator, rule: str):
    pkg = make_fixture(mutator)
    code, out = run_validate(pkg)
    ok = code != 0 and rule in out
    report(name, ok, f"exit={code}, 命中 {rule}" if ok else f"exit={code}, 未命中 {rule}")
    shutil.rmtree(pkg, ignore_errors=True)


def main() -> int:
    print("=" * 70)
    print("TASK-02 校验器测试")
    print("=" * 70)

    # --- 正例 ---
    code, out = run_validate(EXAMPLE)
    # 校验器退出码 0 即表示无任何 FAIL；再确认报告汇总行存在
    ok = code == 0 and "总计" in out and "FAIL 0" in out
    report("正例：content/test-device 全绿", ok, f"exit={code}, 汇总「FAIL 0」")
    if not ok:
        print(out)

    # --- 反例 1：缺引用（component.assembly 指向不存在的装配体 → R-014）---
    def m_missing_ref(meta, pkg):
        meta["components"][0]["assembly"] = "no_such_board"
    expect_fail("反例1：缺引用（component.assembly 悬空）", m_missing_ref, "R-014")

    # --- 反例 2：循环父子（装配树成环 → R-012）---
    def m_cycle(meta, pkg):
        for a in meta["assemblies"]:
            if a["id"] == "mainboard":
                a["children"] = ["whole"]
    expect_fail("反例2：循环父子（装配树成环）", m_cycle, "R-012")

    # --- 反例 3：命名违规（节点 id 含连字符 → R-021）---
    def m_bad_name(meta, pkg):
        meta["components"][0]["id"] = "Bad-Name"
        meta["assemblies"][0]["components"] = ["Bad-Name"]
    expect_fail("反例3：命名违规（节点 id 非 snake_case）", m_bad_name, "R-021")

    # --- 反例 4：缺 THIRD_PARTY.md（→ R-050）---
    def m_no_tp(meta, pkg):
        os.remove(os.path.join(pkg, "THIRD_PARTY.md"))
    expect_fail("反例4：缺 THIRD_PARTY.md", m_no_tp, "R-050")

    # --- 反例 5：含未定标记文案（→ R-060）---
    def m_unresolved(meta, pkg):
        ann_path = os.path.join(pkg, "annotations", "annotations.json")
        with open(ann_path, "r", encoding="utf-8") as f:
            doc = json.load(f)
        doc["annotations"][0]["text"] += "（具体参数需核实）"
        with open(ann_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
    expect_fail("反例5：含未定标记文案", m_unresolved, "R-060")

    # --- 反例 6：transform 越界（scale 含 0 → R-032）---
    def m_bad_scale(meta, pkg):
        for a in meta["assemblies"]:
            if a["id"] == "mainboard":
                a["transform"]["scale"] = [1.0, 0.0, 1.0]
    expect_fail("反例6：transform 越界（scale 分量 = 0）", m_bad_scale, "R-032")

    print("-" * 70)
    print(f"结果：PASS {PASSED}，FAIL {FAILED}")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
