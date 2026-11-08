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
id_registry 黑盒测试（TASK-167A）

用法：
    python run_registry_tests.py

全部通过环境变量 ID_REGISTRY_PATH 指向临时台账，隔离真实台账（绝不污染
docs/catalog/registry.jsonl）。覆盖 rebuild 回填/幂等/跳过非法、allocate --files 防撞号、
verify 查重/格式错。

用例：
    A rebuild 回填 3 条
    B rebuild 幂等（已存在跳过 3，回填 0）
    C rebuild 跳过非法（非法跳过 2）
    D allocate --files 防撞号（起点 C-TST-000010）
    E verify 报重复/格式错
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ID_REGISTRY = os.path.abspath(os.path.join(TESTS_DIR, "..", "id_registry.py"))

PASSED = 0
FAILED = 0


def report(name: str, ok: bool, detail: str = ""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
        print(f"[PASS] {name}" + (f"  — {detail}" if detail else ""))
    else:
        FAILED += 1
        print(f"[FAIL] {name}" + (f"  — {detail}" if detail else ""))


def run_registry(reg_path: str, args: list[str]) -> tuple[int, str]:
    env = dict(os.environ)
    env["ID_REGISTRY_PATH"] = reg_path
    proc = subprocess.run(
        [sys.executable, ID_REGISTRY] + args,
        capture_output=True, text=True, encoding="utf-8", env=env,
    )
    return proc.returncode, proc.stdout + proc.stderr


def write_jsonl(path: str, ids: list[str]):
    with open(path, "w", encoding="utf-8") as f:
        for i in ids:
            f.write(json.dumps({"id": i, "name": "test"}, ensure_ascii=False) + "\n")


def reg_lines(reg_path: str) -> int:
    if not os.path.isfile(reg_path):
        return 0
    with open(reg_path, encoding="utf-8") as f:
        return sum(1 for ln in f if ln.strip())


def main() -> int:
    print("=" * 70)
    print("TASK-167A id_registry 黑盒测试（rebuild / allocate / verify）")
    print("=" * 70)

    tmp = tempfile.mkdtemp(prefix="hako_registry_")
    reg = os.path.join(tmp, "registry.jsonl")

    # 用例 A：rebuild 回填 3 条
    a = os.path.join(tmp, "a.jsonl")
    write_jsonl(a, ["C-TST-000001", "C-TST-000002", "C-TST-000003"])
    code, out = run_registry(reg, ["rebuild", a])
    ok = ("回填 3 条" in out) and (reg_lines(reg) == 3)
    report("用例A：rebuild 回填 3 条", ok, f"台账 {reg_lines(reg)} 条")
    if not ok:
        print(out.strip())

    # 用例 B：rebuild 幂等
    code, out = run_registry(reg, ["rebuild", a])
    ok = ("已存在跳过 3" in out) and ("回填 0" in out) and (reg_lines(reg) == 3)
    report("用例B：rebuild 幂等（已存在跳过 3）", ok, f"台账 {reg_lines(reg)} 条")
    if not ok:
        print(out.strip())

    # 用例 C：rebuild 跳过非法（NO_PREFIX + C-BAD1-000001）
    b = os.path.join(tmp, "b.jsonl")
    write_jsonl(b, ["C-TST-000004", "NO_PREFIX", "C-BAD1-000001"])
    code, out = run_registry(reg, ["rebuild", b])
    ok = ("非法跳过 2" in out) and ("回填 1" in out)
    report("用例C：rebuild 跳过非法 2 条", ok, out.strip().splitlines()[-1] if out.strip() else "")
    if not ok:
        print(out.strip())

    # 用例 D：allocate --files 防撞号（目录已用 C-TST-000009 → 起点 000010）
    c = os.path.join(tmp, "c.jsonl")
    write_jsonl(c, ["C-TST-000009"])
    code, out = run_registry(reg, ["allocate", "C", "1", "TST", "--files", c])
    ok = ("C-TST-000010" in out)
    report("用例D：allocate --files 防撞号（起点 000010）", ok, f"exit={code}")
    if not ok:
        print(out.strip())

    # 用例 E：verify 报重复 + 格式错（退出码 0，只报告）
    d = os.path.join(tmp, "d.jsonl")
    write_jsonl(d, ["C-TST-000001", "C-TST-000001", "BAD_FORMAT"])
    code, out = run_registry(reg, ["verify", d])
    ok = ("[重复]" in out) and ("[格式错]" in out) and (code == 0)
    report("用例E：verify 报重复/格式错（exit 0）", ok, f"exit={code}")
    if not ok:
        print(out.strip())

    print("-" * 70)
    print(f"结果：PASS {PASSED}，FAIL {FAILED}")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
