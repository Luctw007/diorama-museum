# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""内容同步（TASK-16B）：把 03/05 线内容包复制进 Godot 工程并自动校验、登记。

用法:
  python scripts/sync_content.py             # 全量复制 + 校验 + 重写 godot/content/README.md
  python scripts/sync_content.py --dry-run   # 仅打印计划
退出码：任一包校验失败 → 1（并逐包明示，供人工裁决是否继续）；全部通过 → 0。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
TARGET_ROOT = os.path.join(REPO, "godot", "content")
README_PATH = os.path.join(TARGET_ROOT, "README.md")

VALIDATOR = r"D:\work\02\repo\tools\validate\validate.py"
# 门禁数据驱动化（TASK-41A）：来源清单自动发现，不再手工维护
import pkg_registry as _reg  # noqa: E402
SOURCES = _reg.discover_packages()

FAIL_RE = re.compile(r"FAIL\s*(\d+)")


def ignore_cache(directory: str, names: list[str]) -> set[str]:
    return {"__pycache__"} & set(names)


def validate_package(pkg_dir: str) -> int:
    """跑 02 线校验器；返回 FAIL 计数（无法解析返回 -1）。"""
    cp = subprocess.run([PY, VALIDATOR, pkg_dir], cwd=REPO, capture_output=True,
                        text=True, encoding="utf-8", errors="replace", timeout=300)
    out = (cp.stdout or "") + (cp.stderr or "")
    m = FAIL_RE.search(out)
    if m:
        return int(m.group(1))
    return 0 if cp.returncode == 0 else -1


def measure(pkg_dir: str) -> dict[str, str]:
    """loader 视角字段齐备性探测（仅可测量项）。"""
    def has(name: str) -> str:
        return "✓" if os.path.isfile(os.path.join(pkg_dir, name)) else "✗"

    gltf_count = len([f for f in os.listdir(os.path.join(pkg_dir, "meshes"))
                      if f.endswith(".gltf")]) \
        if os.path.isdir(os.path.join(pkg_dir, "meshes")) else 0
    rt = "runtime.json" if os.path.isfile(os.path.join(pkg_dir, "runtime.json")) else "✗"
    enc = has("encyclopedia.md")
    ipf = has("input_profile.json")
    return {
        "meta": has("meta.json"),
        "runtime": rt,
        "annotations": has("annotations/annotations.json"),
        "gltf": str(gltf_count),
        "encyclopedia": enc,
        "input_profile": ipf,
    }


def package_name(pkg_dir: str) -> str:
    try:
        with open(os.path.join(pkg_dir, "meta.json"), encoding="utf-8") as fh:
            data = json.load(fh)
        name = data.get("name")
        if isinstance(name, dict):          # v0.2 localized
            return str(name.get("zh") or name.get("en") or "?")
        return str(name or "?")
    except (OSError, json.JSONDecodeError):
        return "?"


def build_readme(rows: list[dict], fails: list[str],
                 catalog_meta: dict | None = None) -> str:
    head = """# godot/content/ — 设备内容包登记

多设备加载器（`scripts/device_loader.gd` v2）枚举本目录下每个子文件夹为一个设备包。
下表由 `scripts/sync_content.py`（TASK-16B）自动生成；`meshes` 数据为 glTF 文件数。

## 包清单与校验

| device-id | 名称 | 来源（原位） | validate |
|---|---|---|---|
"""
    for r in rows:
        head += "| %s | %s | `%s` | %s |\n" % (
            r["id"], r["name"], r["src"], r["result"])
    if catalog_meta:
        head += """
## 目录包（catalog bundle，61-A 流水线自动再生）

- 目录行数 %s / 分片 %s / 生成 %s（`res://content/catalog/`）
""" % (catalog_meta.get("total_rows"), len(catalog_meta.get("shards", [])),
       catalog_meta.get("generated", ""))
    head += """

## 字段齐备性自查表（loader 视角，自动探测）

| device-id | meta.json | runtime | annotations.json | glTF | encyclopedia.md | input_profile.json | 备注 |
|---|---|---|---|---|---|---|---|
"""
    for r in rows:
        m = r["measure"]
        head += "| %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
            r["id"], m["meta"], m["runtime"], m["annotations"], m["gltf"],
            m["encyclopedia"], m["input_profile"], r["note"])
    head += """
## 人工备注区

<!-- 以下备注不参与自动生成，请人工维护 -->

- `test-device` 为 02 线示例包，不参与内容线同步；
- 正式 3D 资产到达前 glTF 均为占位盒；loader 加载失败时降级占位盒。

## 待验证清单（引擎侧，Godot 实机安装后逐项核对）

| # | 项 | 核对方式 |
|---|---|---|
| 1 | `device_loader.gd`：场景装载、Pack dScene→占位盒降级路径 | 运行工程任一设备包 |
| 2 | `inspect_controller.gd`：悬停高亮/点选/文案弹层 | 进入 Inspect 交互 |
| 3 | `explode_controller.gd`：CLOSED/OPENED/EXPLODED 状态机与位移公式 | 拆解交互 |
| 4 | `gateway_client.gd`：分片重组、画面投放内屏 CRT | 网关起 fake + 投放 |
| 5 | `exhibit_host.gd`（TASK-21B 静态交付）：load_layout/spawn_devices/get_tour_order/find_audience/acquire_run 全流程 | 装 Godot 后加载 exhibit_dawn.json |
| 6 | `input_profile.gd`：读取各包 input_profile.json 并渲染 unbound 清单 | 绑定设置原型 |

> 布局文件（exhibit_dawn.json 等）位于本目录但**不是设备包**，device_loader 扫描时按目录过滤。
"""
    if fails:
        head += "\n### 本次同步的校验失败项（需人工裁决）\n\n" + "\n".join(
            "- %s" % f for f in fails) + "\n"
    return head


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="内容同步：03/05 线 → godot/content")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    args = ap.parse_args(argv)

    rows: list[dict] = []
    fails: list[str] = []
    for dev_id, src in SOURCES:
        dst = os.path.join(TARGET_ROOT, dev_id)
        print("== %s" % dev_id)
        if not os.path.isdir(src):
            print("   !! 源目录缺失: %s" % src)
            fails.append("%s: 源目录缺失" % dev_id)
            continue
        if args.dry_run:
            print("   [dry-run] 将复制 %s -> %s" % (src, dst))
            continue
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_cache)
        n = validate_package(dst)
        result = "FAIL %d" % n if n else "FAIL 0（通过）"
        print("   复制完成；validate 结果: %s" % result)
        rows.append({"id": dev_id, "name": package_name(dst), "src": src,
                     "result": result, "measure": measure(dst), "note": ""})
        if n:
            fails.append("%s: %s" % (dev_id, result))

    if not args.dry_run:
        catalog_meta: dict | None = None
        try:
            import gen_catalog_bundle as gcb  # noqa: E402 同目录脚本
            catalog_meta = gcb.build_bundle()
        except Exception as exc:
            print("[sync] catalog bundle 再生失败（不阻断同步）: %s" % exc)
        with open(README_PATH, "w", encoding="utf-8") as fh:
            fh.write(build_readme(rows, fails, catalog_meta))
        print("README 已重写: %s（目录包 %s 行）"
              % (README_PATH, (catalog_meta or {}).get("total_rows")))

    print("\n同步汇总：%d 包，失败 %d" % (len(rows), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())