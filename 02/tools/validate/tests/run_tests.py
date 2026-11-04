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
校验器测试套件（TASK-07，v0.2）

用法：
    python run_tests.py

正例：对 content/test-device 运行 validate.py，断言退出码 0 且全 PASS。
反例：从示例包复制到临时目录、施加单一破坏后运行 validate.py，断言退出码非 0
     且命中对应规则编号。反例覆盖 v0.2 新规则 R-080~R-091 及关键旧规则，
     每个反例注释写明对应规则编号（与 §五 矩阵一一对应）。
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


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_meta(pkg: str):
    return load_json(os.path.join(pkg, "meta.json"))


def save_meta(pkg: str, meta: dict):
    save_json(os.path.join(pkg, "meta.json"), meta)


def load_annotations(pkg: str):
    return load_json(os.path.join(pkg, "annotations", "annotations.json"))


def save_annotations(pkg: str, doc: dict):
    save_json(os.path.join(pkg, "annotations", "annotations.json"), doc)


def set_runtime(meta: dict, pkg: str, mutate_fn):
    """修改 meta.runtime 并同步 runtime.json，避免连带触发 R-004。"""
    mutate_fn(meta["runtime"])
    save_json(os.path.join(pkg, "runtime.json"), meta["runtime"])


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
    if not ok:
        for line in out.splitlines():
            if line.startswith("FAIL") or line.startswith("总计"):
                print("      " + line)
    shutil.rmtree(pkg, ignore_errors=True)


def main() -> int:
    print("=" * 70)
    print("TASK-07 校验器测试（v0.2）")
    print("=" * 70)

    # --- 正例 ---
    code, out = run_validate(EXAMPLE)
    ok = code == 0 and "总计" in out and "FAIL 0" in out
    report("正例：content/test-device 全绿", ok, f"exit={code}, 汇总「FAIL 0」")
    if not ok:
        print(out)

    cases = [
        # ---- 旧规则回归 ----
        ("反例01：缺引用（component.assembly 悬空）→ R-014",
         lambda m, p: m["components"][0].__setitem__("assembly", "no_such_board"), "R-014"),
        ("反例02：循环父子（装配树成环）→ R-012",
         lambda m, p: [a.__setitem__("children", ["whole"]) for a in m["assemblies"] if a["id"] == "mainboard"], "R-012"),
        ("反例03：命名违规（节点 id 非 snake_case）→ R-021",
         lambda m, p: m["components"][0].__setitem__("id", "Bad-Name"), "R-021"),
        ("反例04：缺 THIRD_PARTY.md → R-050",
         lambda m, p: os.remove(os.path.join(p, "THIRD_PARTY.md")), "R-050"),
        ("反例05：含未定标记文案（标注 text）→ R-060",
         lambda m, p: _append_annotation_text(p, 0, "（具体参数需核实）"), "R-060"),
        ("反例06：transform 越界（scale 分量 = 0）→ R-032",
         lambda m, p: _set_scale(m, 0.0), "R-032"),
        # ---- v0.2 新规则 ----
        ("反例07：materials 引用文件不存在 → R-017",
         lambda m, p: [a.__setitem__("materials", ["materials/nope.json"]) for a in m["assemblies"] if a["id"] == "mainboard"], "R-017"),
        ("反例08：timeline 结构非法（t 起止倒置）→ R-080",
         lambda m, p: _mutate_timeline(p, lambda tl: tl[0].__setitem__("t", [2.0, 1.0])), "R-080"),
        ("反例09：timeline 总时长超预算 → R-081",
         lambda m, p: _mutate_timeline(p, lambda tl: tl[0].__setitem__("t", [0.0, 1000.0])), "R-081"),
        ("反例10：C4 级 anim 缺 caption → R-082",
         lambda m, p: _c4_missing_caption(m, p), "R-082"),
        ("反例11：caption 含未定标记 → R-083",
         lambda m, p: _mutate_timeline(p, lambda tl: tl[0].__setitem__("caption", "待核实内容")), "R-083"),
        ("反例12：sink surface 非法枚举 → R-084",
         lambda m, p: set_runtime(m, p, lambda r: r["output_sinks"][0].__setitem__("surface", "crt_internal")), "R-084"),
        ("反例13：annotation.surface 未声明 → R-085",
         lambda m, p: _mutate_annotation(p, "power_on_anim", lambda a: a.__setitem__("surface", "external_crt")), "R-085"),
        ("反例14：input_map 键名非法（key 非 KEY_*）→ R-086",
         lambda m, p: set_runtime(m, p, lambda r: r["input_map"]["power"].__setitem__("key", "a")), "R-086"),
        ("反例20：legacy 令牌非法（大写点分）→ R-086",
         lambda m, p: set_runtime(m, p, lambda r: r["input_map"].__setitem__("power", "Keyboard.Key_A")), "R-086"),
        ("反例15：localized 缺 zh → R-087",
         lambda m, p: m["components"][0].__setitem__("role", {"en": "CPU"}), "R-087"),
        ("反例16：name_en 与 name.en 不一致 → R-088",
         lambda m, p: m["meta"].__setitem__("name_en", "Wrong Name"), "R-088"),
        ("反例17：era 越界 → R-089",
         lambda m, p: m["meta"].__setitem__("era", 1500), "R-089"),
        ("反例18：glTF 网格节点名与 node_id 不符 → R-090",
         lambda m, p: _rename_gltf_node(p), "R-090"),
        ("反例19：THIRD_PARTY 行 URL 非法 → R-091",
         lambda m, p: _corrupt_third_party_url(p), "R-091"),
    ]

    for name, mutator, rule in cases:
        expect_fail(name, mutator, rule)

    print("-" * 70)
    print(f"结果：PASS {PASSED}，FAIL {FAILED}")
    return 0 if FAILED == 0 else 1


# ---------------------------------------------------------------------------
# 反例辅助函数
# ---------------------------------------------------------------------------
def _append_annotation_text(pkg: str, idx: int, suffix: str):
    doc = load_annotations(pkg)
    doc["annotations"][idx]["text"] += suffix
    save_annotations(pkg, doc)


def _set_scale(meta: dict, v: float):
    for a in meta["assemblies"]:
        if a["id"] == "mainboard":
            a["transform"]["scale"] = [1.0, v, 1.0]


def _mutate_timeline(pkg: str, mutate_fn):
    doc = load_annotations(pkg)
    for an in doc["annotations"]:
        if an.get("id") == "power_on_anim":
            mutate_fn(an["timeline"])
    save_annotations(pkg, doc)


def _mutate_annotation(pkg: str, ann_id: str, mutate_fn):
    doc = load_annotations(pkg)
    for an in doc["annotations"]:
        if an.get("id") == ann_id:
            mutate_fn(an)
    save_annotations(pkg, doc)


def _c4_missing_caption(meta: dict, pkg: str):
    meta["meta"]["presentation_level"] = "C4"
    doc = load_annotations(pkg)
    for an in doc["annotations"]:
        if an.get("id") == "power_on_anim":
            an["timeline"][0]["caption"] = ""
    save_annotations(pkg, doc)


def _rename_gltf_node(pkg: str):
    path = os.path.join(pkg, "meshes", "mainboard.gltf")
    doc = load_json(path)
    doc["nodes"][0]["name"] = "wrong_name"
    save_json(path, doc)


def _corrupt_third_party_url(pkg: str):
    path = os.path.join(pkg, "THIRD_PARTY.md")
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    txt = txt.replace("https://example.com/placeholder-doc", "not-a-valid-url")
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    sys.exit(main())
