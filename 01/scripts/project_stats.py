# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""项目统计面板（TASK-61B）：一键全局健康数字 → docs/PROJECT_STATS.md + --json。

聚合：内容包（ready/wip/厅分布/glTF 数）、目录（行数/分类/状态分布）、质量（slots+catalog
轻量步当场执行）、槽位（可用数/介质目录数）、工程文件量。供你与 04 线仪表盘取数。
不执行全量验收（verify_all --daily 单独跑）；本工具跑 slots 与 catalog 两个秒级步并记录 rc。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import pkg_registry as pr      # noqa: E402
import slot_loader             # noqa: E402
import gen_catalog_bundle as gcb  # noqa: E402

REPO = os.path.dirname(SCRIPT_DIR)
CONTENT = os.path.join(REPO, "godot", "content")

HALL_OF_CAT = {
    "early-computer": "黎明厅", "mainframe": "大型机与小型机厅",
    "minicomputer": "大型机与小型机厅", "computer": "个人计算机厅",
    "personal-computer": "个人计算机厅", "home-computer": "个人计算机厅",
    "microcomputer": "个人计算机厅",
    "game-console": "游戏机厅", "console": "游戏机厅",
    "arcade": "游戏机厅",
    "placeholder": "示例",
}


def read_category(pkg: str) -> str:
    try:
        with open(os.path.join(pkg, "meta.json"), encoding="utf-8") as fh:
            data = json.load(fh)
        return str((data.get("meta") or {}).get("category", "placeholder"))
    except (OSError, json.JSONDecodeError):
        return "placeholder"


def count_gltf(pkg: str) -> int:
    total = 0
    for d in ("meshes", "assemblies"):
        path = os.path.join(pkg, d)
        if os.path.isdir(path):
            total += len([f for f in os.listdir(path) if f.endswith(".gltf")])
    return total


def quick_step(argv: list[str]) -> int:
    cp = subprocess.run([sys.executable] + argv, cwd=REPO, capture_output=True,
                        text=True, encoding="utf-8", errors="replace", timeout=300)
    return cp.returncode


def gather() -> dict:
    ready, wip = pr.discover_packages_full()
    halls: dict = {}
    gltf_total = 0
    for dev_id, pkg in ready:
        hall = HALL_OF_CAT.get(read_category(pkg), "其他")
        halls[hall] = halls.get(hall, 0) + 1
        gltf_total += count_gltf(pkg)
    slots = slot_loader.slots_available()
    bundle_meta = {}
    meta_path = os.path.join(CONTENT, "catalog", "meta.json")
    if os.path.isfile(meta_path):
        with open(meta_path, encoding="utf-8") as fh:
            bundle_meta = json.load(fh)
    taxonomy = bundle_meta.get("taxonomy", {})
    status: dict = {"planned": 0, "researching": 0, "package": 0,
                    "wip": 0, "done": 0, "other": 0}
    for shard in bundle_meta.get("shards", []):
        dpath = os.path.join(CONTENT, "catalog", "data", shard["file"])
        if not os.path.isfile(dpath):
            continue
        with open(dpath, encoding="utf-8") as fh:
            rows = json.load(fh)
        for r in rows:
            st = str(r.get("status", "other"))
            status[st if st in status else "other"] += 1
    file_count = 0
    for root, _dirs, files in os.walk(os.path.dirname(SCRIPT_DIR)):
        if "__pycache__" in root or ".workbuddy" in root:
            continue
        file_count += sum(1 for f in files if not f.endswith(".pyc"))
    # TASK-71A：最近验收（verify_all --cache 产物）
    vlast_path = os.path.join(REPO, "docs", "verify_last.json")
    verify_last = None
    if os.path.isfile(vlast_path):
        try:
            with open(vlast_path, encoding="utf-8") as fh:
                verify_last = json.load(fh)
        except (OSError, json.JSONDecodeError):
            verify_last = None
    # TASK-76B：验收趋势历史（verify_all --cache 追加的 jsonl）
    vhist_path = os.path.join(REPO, "docs", "verify_history.jsonl")
    verify_history: list[dict] = []
    if os.path.isfile(vhist_path):
        with open(vhist_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    verify_history.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "packages": {"ready": len(ready), "wip": len(wip),
                     "halls": halls, "gltf_total": gltf_total},
        "catalog": {"rows": bundle_meta.get("total_rows", 0),
                    "shards": len(bundle_meta.get("shards", [])),
                    "big": len(taxonomy),
                    "mid": sum(len(m) for m in taxonomy.values()),
                    "status": status},
        "slots": {"available": len(slots), "media_dirs": len(slot_loader.media_dirs())},
        "quality": {"slots_rc": quick_step(
                        [os.path.join(SCRIPT_DIR, "slot_consistency_check.py")]),
                    "catalog_rc": quick_step(
                        [os.path.join(SCRIPT_DIR, "catalog_ingest.py"),
                         "--from-work", "--gate", "--gate-verify"])},
        "repo_files": file_count,
        "verify_last": verify_last,
        "verify_history": verify_history,
    }


def render_verify(v: dict | None, hist: list[dict] | None = None) -> str:
    if not v:
        return ("- 最近验收：**未跑**（跑 `python scripts/verify_all.py --daily --cache`"
                " 即自动写入本节）\n")
    total = int(v.get("total", 0))
    passed = int(v.get("passed", 0))
    mark = "【全绿】" if passed >= total else "【红灯】"
    lines = ["- 最近验收（%s）：**%d/%d 通过** — %s"
             % (v.get("time", "未知"), passed, total, mark)]
    for f in v.get("failed", []):
        lines.append("  - FAIL %s：%s" % (f.get("name", "?"), f.get("note", "")))
    hist = hist or []
    if not hist:
        lines.append("- 趋势历史：**不足**（跑 `verify_all --daily --cache` 后自动积累）")
    else:
        lines.append("- 最近 %d 轮：" % min(5, len(hist)))
        for row in hist[-5:]:
            t = int(row.get("total", 0))
            p = int(row.get("passed", 0))
            ok = (t > 0 and p >= t)
            lines.append("  - %s：%d/%d %s" % (row.get("time", "?"), p, t,
                                               "全绿" if ok else "红灯"))
        streak = 0
        for row in reversed(hist):
            t = int(row.get("total", 0))
            p = int(row.get("passed", 0))
            if t > 0 and p >= t:
                streak += 1
            else:
                break
        lines.append("- 连续全绿：**%d 轮**" % streak)
    return "\n".join(lines) + "\n"


def render_md(s: dict) -> str:
    halls = "\n".join("| %s | %d |" % (k, v) for k, v in sorted(s["packages"]["halls"].items()))
    st = s["catalog"]["status"]
    return """# 项目统计面板（PROJECT_STATS.md，自动生成）

> 生成：%s（scripts/project_stats.py；本表不执行全量验收，全量请跑 verify_all --daily）

## 内容包

- 完工 **%d** 台 / 生产中 %d 台；占位 glTF 合计 **%d** 个

| 厅 | 台数 |
|---|---|
%s

## 设备目录

- 条目 **%s** 行 / 分片 %s；大分类 %s / 中分类 %s
- 状态分布：planned %d / researching %d / package %d / wip %d / done %d / 其他 %d

## 槽位系统

- 可用槽位 %d 个；介质目录 %d 个

## 质量（轻量步，当场执行）

- slots 一致性 rc=%s（0=过）；catalog 门禁+对账 rc=%s（0=过）

## 最近验收

%s
## 工程规模

- repo 文件数 %d（不含 __pycache__/.pyc）
""" % (s["generated"], s["packages"]["ready"], s["packages"]["wip"],
       s["packages"]["gltf_total"], halls, s["catalog"]["rows"],
       s["catalog"]["shards"], s["catalog"]["big"], s["catalog"]["mid"],
       st["planned"], st["researching"], st["package"], st["wip"], st["done"],
       st["other"], s["slots"]["available"], s["slots"]["media_dirs"],
       s["quality"]["slots_rc"], s["quality"]["catalog_rc"],
       render_verify(s.get("verify_last"), s.get("verify_history")),
       s["repo_files"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="项目统计面板")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    stats = gather()
    out_md = os.path.join(REPO, "docs", "PROJECT_STATS.md")
    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write(render_md(stats))
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(render_md(stats))
    print("已写 %s" % out_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())