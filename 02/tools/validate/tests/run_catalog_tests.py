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
设备目录校验器反例测试（TASK-52B/57A，v0.6 定稿 schema）

用法：
    python run_catalog_tests.py

在临时目录写 JSONL 目录表单，施加单一破坏后运行 catalog_check.py，断言命中预期规则编号与级别。
覆盖 CC-01~07 的违规路径 + 1 正例（含两级分类合法）。

反例清单：
    01 缺字段（缺 name）→ CC-01 FAIL
    02 重复 id → CC-02 FAIL
    03 大分类不存在 → CC-03 FAIL
    04 状态缺 device_id（done 无 device_id）→ CC-04 FAIL
    05 年代越界（era=1500）→ CC-05 FAIL
    06 理由超长（>60 字）→ CC-06 FAIL
    07 正例（全合法，含两级分类）→ 无 FAIL（exit 0）
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_CHECK = os.path.abspath(os.path.join(TESTS_DIR, "..", "catalog_check.py"))

PASSED = 0
FAILED = 0


def run_catalog_check(path: str):
    proc = subprocess.run(
        [sys.executable, CATALOG_CHECK, path],
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_catalog_check_multi(paths: list[str]):
    proc = subprocess.run(
        [sys.executable, CATALOG_CHECK] + paths,
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.returncode, proc.stdout + proc.stderr


def report(name: str, ok: bool, detail: str = ""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
        print(f"[PASS] {name}" + (f"  — {detail}" if detail else ""))
    else:
        FAILED += 1
        print(f"[FAIL] {name}" + (f"  — {detail}" if detail else ""))


def base_entry() -> dict:
    return {
        "id": "C-PC-000123",
        "name": "IBM Personal Computer 5150",
        "aliases": ["IBM PC", "IBM 5150"],
        "manufacturer": "IBM",
        "origin": "美国",
        "era": 1981,
        "taxonomy_path": ["计算机", "个人机", "PC 兼容"],
        "influence": "奠定 IBM PC 兼容机标准",
        "status": "done",
        "device_id": "ibm5150",
        "verify": False,
        "sources": ["S53A-001"],
    }


def write_jsonl(path: str, entries: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def expect(name: str, entries, rule: str, level: str):
    tmp = tempfile.mkdtemp(prefix="hako_catalog_")
    path = os.path.join(tmp, "catalog.jsonl")
    write_jsonl(path, entries)
    code, out = run_catalog_check(path)
    ok = any((rule in ln) and (level in ln) for ln in out.splitlines())
    report(name, ok, f"exit={code}, 命中 {rule} {level}" if ok else f"exit={code}, 未命中 {rule} {level}")
    if not ok:
        for ln in out.splitlines():
            if ln.strip().startswith(("CC-", "FAIL", "PASS")):
                print("      " + ln.strip())


def main() -> int:
    print("=" * 70)
    print("TASK-52B/57A 设备目录校验器反例测试（catalog_check.py）")
    print("=" * 70)

    # 反例01：缺字段（缺 name）
    e = base_entry()
    e.pop("name")
    expect("反例01：缺字段（缺 name）→ CC-01 FAIL", [e], "CC-01", "FAIL")

    # 反例02：重复 id
    e1 = base_entry()
    e2 = base_entry()
    e2["name"] = "另一台设备"
    expect("反例02：重复 id → CC-02 FAIL", [e1, e2], "CC-02", "FAIL")

    # 反例03：大分类不存在
    e = base_entry()
    e["taxonomy_path"] = ["不存在的分类", "某中分类"]
    expect("反例03：大分类不存在 → CC-03 FAIL", [e], "CC-03", "FAIL")

    # 反例04：状态缺 device_id（done 无 device_id）
    e = base_entry()
    e.pop("device_id")
    expect("反例04：done 缺 device_id → CC-04 FAIL", [e], "CC-04", "FAIL")

    # 反例05：年代越界
    e = base_entry()
    e["era"] = 1500
    expect("反例05：年代越界（1500）→ CC-05 FAIL", [e], "CC-05", "FAIL")

    # 反例06：理由超长（>60 字）
    e = base_entry()
    e["influence"] = "这台设备的历史意义极其重大，它开创了个人计算机的全新时代，深刻影响了后续所有个人电脑的设计与普及，堪称计算机发展史上的里程碑之作，值得永久收藏与展示"  # >60 字
    expect("反例06：理由超长 → CC-06 FAIL", [e], "CC-06", "FAIL")

    # 反例07：device_id 不存在（CC-08）
    e = base_entry()
    e["device_id"] = "nonexistent-device"
    expect("反例07：device_id 不存在 → CC-08 FAIL", [e], "CC-08", "FAIL")

    # 反例08：台账重复（id 已在 id_registry 台账中分配）
    e = base_entry()
    e["id"] = "C-GEN-000001"
    expect("反例08：台账重复 → CC-02 FAIL", [e], "CC-02", "FAIL")

    # 反例09：跨文件重复（两个文件同 id）
    tmp = tempfile.mkdtemp(prefix="hako_catalog_cross_")
    f1 = os.path.join(tmp, "a.jsonl")
    f2 = os.path.join(tmp, "b.jsonl")
    e1 = base_entry()
    e2 = base_entry()
    e2["name"] = "另一台设备"
    write_jsonl(f1, [e1])
    write_jsonl(f2, [e2])
    code, out = run_catalog_check_multi([f1, f2])
    ok = any(("CC-02" in ln) and ("FAIL" in ln) for ln in out.splitlines())
    report("反例09：跨文件重复 → CC-02 FAIL", ok, f"exit={code}")

    # 正例10：全合法（含两级分类）→ 无 FAIL（exit 0）
    tmp = tempfile.mkdtemp(prefix="hako_catalog_ok_")
    path = os.path.join(tmp, "catalog.jsonl")
    e = base_entry()
    e["taxonomy_path"] = ["家电影音", "影音播放机"]  # 两级，允许（补"未细分"）
    e["status"] = "researching"
    e.pop("device_id")
    write_jsonl(path, [e])
    code, out = run_catalog_check(path)
    ok = (code == 0) and ("FAIL 0" in out)
    report("正例07：全合法（两级分类）→ 无 FAIL", ok, f"exit={code}")
    if not ok:
        for ln in out.splitlines():
            if ln.strip().startswith(("CC-", "FAIL")):
                print("      " + ln.strip())

    # 反例-CC10-1：无 media_class，默认模式 → CC-10 WARN（退出码 0，不破门禁）
    tmp = tempfile.mkdtemp(prefix="hako_catalog_cc10a_")
    path = os.path.join(tmp, "catalog.jsonl")
    write_jsonl(path, [base_entry()])
    code, out = run_catalog_check(path)
    ok = any(("CC-10" in ln) and ("WARN" in ln) for ln in out.splitlines()) and (code == 0)
    report("反例-CC10-1：无 media_class 默认 → CC-10 WARN（exit 0）", ok, f"exit={code}")
    if not ok:
        for ln in out.splitlines():
            if "CC-10" in ln:
                print("      " + ln.strip())

    # 反例-CC10-2：无 media_class，加 --require-media-class → CC-10 FAIL（退出码非 0）
    tmp = tempfile.mkdtemp(prefix="hako_catalog_cc10b_")
    path = os.path.join(tmp, "catalog.jsonl")
    write_jsonl(path, [base_entry()])
    proc = subprocess.run(
        [sys.executable, CATALOG_CHECK, path, "--require-media-class"],
        capture_output=True, text=True, encoding="utf-8",
    )
    out = proc.stdout + proc.stderr
    ok = any(("CC-10" in ln) and ("FAIL" in ln) for ln in out.splitlines()) and (proc.returncode != 0)
    report("反例-CC10-2：无 media_class 严格 → CC-10 FAIL（exit≠0）", ok, f"exit={proc.returncode}")
    if not ok:
        for ln in out.splitlines():
            if "CC-10" in ln:
                print("      " + ln.strip())

    # 反例-CC10-3：有 media_class="disk"，默认模式 → CC-10 PASS
    tmp = tempfile.mkdtemp(prefix="hako_catalog_cc10c_")
    path = os.path.join(tmp, "catalog.jsonl")
    e = base_entry()
    e["media_class"] = "disk"
    write_jsonl(path, [e])
    code, out = run_catalog_check(path)
    ok = any(("CC-10" in ln) and ("PASS" in ln) for ln in out.splitlines())
    report("反例-CC10-3：media_class=disk → CC-10 PASS", ok, f"exit={code}")
    if not ok:
        for ln in out.splitlines():
            if "CC-10" in ln:
                print("      " + ln.strip())

    print("-" * 70)
    print(f"结果：PASS {PASSED}，FAIL {FAILED}")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
