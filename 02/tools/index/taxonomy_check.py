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
分类树治理校验器（TASK-62A，纯 stdlib）

把 `docs/taxonomy.json`（官方分类树）与 03/05 线全部目录文件的 `taxonomy_path` 对账：
    - 落在官方树内 → PASS；
    - 不在树内 → 收集为孤路径，产出 `docs/taxonomy_orphans.md`（孤路径清单 + 建议归处）；
    - 树缺的 中分类/子分类 → 列「树待补清单」，按二选一裁决：补树 or 标未细分。

裁决规则（写明）：
    补树     孤路径的中分类是"语义独立的真实分类"（非变体、非拼写差异）→ 建议补入官方树；
    标未细分  孤路径的子分类是"无法/无需细分的临时值"或与既有值语义重复的变体 → 建议归并"未细分"。

用法：
    python taxonomy_check.py [--content-dir <dir>] [--json]

默认扫描 03/05 线 `repo/docs/catalog/*.jsonl`。不改他线文件，只产出清单。
依赖：无（独立脚本）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# 路径定位
# ---------------------------------------------------------------------------
def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def work_root() -> str:
    return os.path.dirname(os.path.dirname(repo_root()))


def taxonomy_path() -> str:
    return os.path.join(repo_root(), "docs", "taxonomy.json")


def orphans_path() -> str:
    return os.path.join(repo_root(), "docs", "taxonomy_orphans.md")


def default_catalog_files() -> list[str]:
    roots = [os.path.join(work_root(), "03", "repo", "docs", "catalog"),
             os.path.join(work_root(), "05", "repo", "docs", "catalog")]
    files = []
    for root in roots:
        if os.path.isdir(root):
            files.extend(glob.glob(os.path.join(root, "*.jsonl")))
    return sorted(files)


# ---------------------------------------------------------------------------
# 官方树加载
# ---------------------------------------------------------------------------
def load_taxonomy() -> dict:
    with open(taxonomy_path(), "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 目录文件扫描
# ---------------------------------------------------------------------------
def scan_entries(files: list[str]) -> list[tuple[str, str, list]]:
    """返回 [(file, id, path)]。path 取 taxonomy_path 或 分类路径。"""
    out = []
    for path in files:
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rid = obj.get("id", "?")
                p = obj.get("taxonomy_path") or obj.get("分类路径") or []
                if isinstance(p, list) and p:
                    out.append((os.path.basename(path), str(rid), p))
    return out


# ---------------------------------------------------------------------------
# 对账
# ---------------------------------------------------------------------------
def check_against_tree(entries, tree: dict) -> dict:
    """对账：返回统计 + 孤路径 + 树待补清单。"""
    n_total = len(entries)
    n_pass = 0
    orphan_counter = Counter()          # 孤路径完整元组 -> 次数
    orphan_sample = defaultdict(list)   # 孤路径 -> [样例 id]
    orphan_big = Counter()              # 大分类级孤儿
    orphan_mid = Counter()              # 中分类级孤儿
    orphan_sub = Counter()              # 子分类级孤儿

    for _file, rid, path in entries:
        big = path[0]
        if big not in tree:
            n = len(path)
            key = "大分类孤儿: " + big
            orphan_big[key] += 1
            continue
        if len(path) < 2:
            orphan_mid[f"{big}/<缺中分类>"] += 1
            continue
        mid = path[1]
        if mid not in tree[big]:
            key = f"{big}/{mid}"
            orphan_mid[key] += 1
            orphan_counter[key] += 1
            orphan_sample[key].append(rid)
            continue
        if len(path) >= 3:
            sub = path[2]
            if sub not in tree[big][mid]:
                key = f"{big}/{mid}/{sub}"
                orphan_sub[key] += 1
                orphan_counter[key] += 1
                orphan_sample[key].append(rid)
                continue
        n_pass += 1

    return {
        "n_total": n_total,
        "n_pass": n_pass,
        "orphan_big": dict(orphan_big),
        "orphan_mid": dict(orphan_mid),
        "orphan_sub": dict(orphan_sub),
        "orphan_counter": dict(orphan_counter),
        "orphan_sample": dict(orphan_sample),
    }


# ---------------------------------------------------------------------------
# 渲染孤路径清单
# ---------------------------------------------------------------------------
def render_orphans(rep: dict, generated_at: str) -> str:
    lines = [
        "# taxonomy 孤路径清单（自动生成，勿手改）",
        "",
        f"> 生成时间：{generated_at}　|　工具：`tools/index/taxonomy_check.py`（TASK-62A）",
        f"> 对账：共 {rep['n_total']} 条目录，落在官方树内 {rep['n_pass']} 条，孤路径 {rep['n_total'] - rep['n_pass']} 条。",
        "",
        "## 一、大分类级孤儿（不应出现，7 大分类硬约束）",
    ]
    if rep["orphan_big"]:
        for k, n in sorted(rep["orphan_big"].items(), key=lambda x: -x[1]):
            lines.append(f"- {k}（{n} 条）")
    else:
        lines.append("- （无）")
    lines += ["", "## 二、中分类级孤儿（建议补树）", ""]
    if rep["orphan_mid"]:
        lines.append("| 中分类路径 | 条数 | 建议 |")
        lines.append("|---|---|---|")
        for k, n in sorted(rep["orphan_mid"].items(), key=lambda x: -x[1]):
            lines.append(f"| {k} | {n} | 补树 |")
    else:
        lines.append("- （无）")
    lines += ["", "## 三、子分类级孤儿（二选一裁决：补树 / 标未细分）", ""]
    if rep["orphan_sub"]:
        lines.append("| 子分类路径 | 条数 | 建议 | 样例 id |")
        lines.append("|---|---|---|---|")
        for k, n in sorted(rep["orphan_sub"].items(), key=lambda x: -x[1]):
            sample = rep["orphan_sample"].get(k, ["?"])[0]
            lines.append(f"| {k} | {n} | 补树（需人工复核） | {sample} |")
    else:
        lines.append("- （无）")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="分类树治理校验器（TASK-62A）")
    p.add_argument("--content-dir", action="append", default=None,
                   help="追加扫描的 catalog 目录（可多次）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.content_dir:
        files = []
        for d in args.content_dir:
            files.extend(glob.glob(os.path.join(d, "*.jsonl")))
        files = sorted(set(files))
    else:
        files = default_catalog_files()

    tree = load_taxonomy()
    entries = scan_entries(files)
    rep = check_against_tree(entries, tree)

    if args.json:
        rep["files"] = [os.path.basename(f) for f in files]
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0

    import datetime
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = render_orphans(rep, generated_at)
    with open(orphans_path(), "w", encoding="utf-8") as f:
        f.write(md)

    print(f"对账：共 {rep['n_total']} 条目录，落在官方树内 {rep['n_pass']} 条，"
          f"孤路径 {rep['n_total'] - rep['n_pass']} 条")
    print(f"  大分类级孤儿：{len(rep['orphan_big'])} 项")
    print(f"  中分类级孤儿：{len(rep['orphan_mid'])} 项（建议补树）")
    print(f"  子分类级孤儿：{len(rep['orphan_sub'])} 项（二选一裁决）")
    print(f"已生成：{orphans_path()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
