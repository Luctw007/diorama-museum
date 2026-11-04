# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""图鉴静态索引生成器（TASK-36B）：godot/content 全包 → exhibit_index.json。

体例：meta 包内 meta.json 的 meta 块（category/era/name.zh）；runtime 取独立 runtime.json
（缺省回退 meta 内嵌 runtime）；demo_mode 由 run_profile --json 派生；annotations 条目数、
glTF 网格数自测。门类→厅映射内置（HALL_OF）。

用法:
  python scripts/gen_exhibit_index.py            # 全量生成 godot/content/exhibit_index.json
  python scripts/gen_exhibit_index.py --dry-run  # 只打印总结表
  python scripts/gen_exhibit_index.py --verify   # 索引与源包逐字段比对
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(REPO, "godot", "content")
INDEX_PATH = os.path.join(CONTENT, "exhibit_index.json")

HALL_OF = {
    "early-computer": "黎明厅（Dawn Hall）",
    "mainframe": "大型机与小型机厅（Mainframe Hall）",
    "minicomputer": "大型机与小型机厅（Mainframe Hall）",
    "computer": "个人计算机厅（Personal Computer Hall）",
    "game-console": "游戏机厅（Console Hall）",
    "placeholder": "示例（Samples）",
}
HALL_ORDER = [
    "黎明厅（Dawn Hall）", "大型机与小型机厅（Mainframe Hall）",
    "个人计算机厅（Personal Computer Hall）", "游戏机厅（Console Hall）", "示例（Samples）",
]


def read_meta(pkg: str) -> dict:
    with open(os.path.join(pkg, "meta.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("meta") or {}


def read_runtime(pkg: str) -> dict:
    rt_path = os.path.join(pkg, "runtime.json")
    if os.path.isfile(rt_path):
        with open(rt_path, encoding="utf-8") as fh:
            return json.load(fh)
    with open(os.path.join(pkg, "meta.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("runtime") or {}


def demo_mode_of(pkg: str) -> bool:
    cp = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "run_profile.py"),
         pkg, "--json"], capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120, cwd=REPO)
    if cp.returncode != 0:
        return True   # 映射失败视为演示模式（保守）
    try:
        return bool(json.loads(cp.stdout).get("demo_mode"))
    except json.JSONDecodeError:
        return True


def annotation_count(pkg: str) -> int:
    path = os.path.join(pkg, "annotations", "annotations.json")
    if not os.path.isfile(path):
        return 0
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return 0
    if isinstance(data, list):
        return len(data)
    for key in ("items", "flows", "annotations"):
        if isinstance(data.get(key), list):
            return len(data[key])
    return 0


def mesh_count(pkg: str) -> int:
    meshes = os.path.join(pkg, "meshes")
    if not os.path.isdir(meshes):
        return 0
    return len([f for f in os.listdir(meshes) if f.endswith(".gltf")])


def collect() -> dict:
    packages: list[dict] = []
    for name in sorted(os.listdir(CONTENT)):
        pkg = os.path.join(CONTENT, name)
        if not os.path.isdir(pkg) or not os.path.isfile(os.path.join(pkg, "meta.json")):
            continue
        meta = read_meta(pkg)
        runtime = read_runtime(pkg)
        name_zh = meta.get("name", {})
        packages.append({
            "id": name,
            "name": name_zh.get("zh") if isinstance(name_zh, dict) else str(name_zh or name),
            "era": meta.get("era"),
            "category": meta.get("category") or "placeholder",
            "emulator": runtime.get("emulator"),
            "demo_mode": demo_mode_of(pkg),
            "annotation_count": annotation_count(pkg),
            "meshes": mesh_count(pkg),
        })
    halls: dict[str, list] = {}
    for d in packages:
        halls.setdefault(HALL_OF.get(d["category"], "示例（Samples）"), []).append(d)
    hall_list = [{"hall": h, "devices": halls[h]} for h in HALL_ORDER if h in halls]
    return {"generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
            "halls": hall_list}


def print_summary(index: dict) -> None:
    total = 0
    for hall in index["halls"]:
        n = len(hall["devices"])
        total += n
        print("  %-42s %d 台" % (hall["hall"], n))
    print("  合计 %d 台（生成时间 %s）" % (total, index["generated"]))


def verify(index: dict) -> bool:
    """索引与源包逐字段比对；返回是否一致。"""
    ok = True
    rows: list[str] = []
    flat = {(d["id"]): d for hall in index["halls"] for d in hall["devices"]}
    for name in sorted(os.listdir(CONTENT)):
        pkg = os.path.join(CONTENT, name)
        if not os.path.isdir(pkg) or not os.path.isfile(os.path.join(pkg, "meta.json")):
            continue
        meta = read_meta(pkg)
        runtime = read_runtime(pkg)
        d = flat.get(name)
        if d is None:
            ok = False
            rows.append("%s：索引缺条目" % name)
            continue
        checks = [
            ("era", meta.get("era"), d.get("era")),
            ("category", meta.get("category") or "placeholder", d.get("category")),
            ("emulator", runtime.get("emulator"), d.get("emulator")),
            ("meshes", mesh_count(pkg), d.get("meshes")),
            ("annotations", annotation_count(pkg), d.get("annotation_count")),
        ]
        for field, expect, actual in checks:
            if expect != actual:
                ok = False
                rows.append("%s.%s：索引=%r 源=%r" % (name, field, actual, expect))
    for r in rows:
        print("  [FAIL] " + r)
    print("verify 结果：%s（%d 条差异）" % ("通过" if ok else "不一致", len(rows)))
    return ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="图鉴静态索引生成器")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv)
    index = collect()
    print_summary(index)
    if args.dry_run:
        return 0
    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)
    print("已写 %s" % INDEX_PATH)
    if args.verify:
        return 0 if verify(index) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())