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
目录 ID 注册表服务（TASK-57B，纯 stdlib）

维护 `docs/catalog/registry.jsonl`（已分配 id 台账），提供三类操作，保证万级目录的
ID 全局不重、可追溯：

    allocate <大类码> <数量> [中分类码]   顺序分配新 id（如 C-GEN-000001…），写入 registry.jsonl
    verify <目录文件> [更多...]          扫描目录文件全部 id——重复/越界/格式错逐行报
    --report                            按大类码的使用统计（registry + 扫描 catalog 文件）

前缀↔大类码对照表（v0.6 定稿 §七，见 CATEGORY_CODE）：
    C=计算机  G=游戏机  M=通讯与移动  A=家电影音  P=办公与计算外设  E=嵌入式与工业  X=其他

用法示例：
    python id_registry.py allocate C 50 GEN
    python id_registry.py verify ../03/repo/docs/catalog/*.jsonl
    python id_registry.py --report

依赖：无（独立脚本）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# 常量（镜像规范 v0.6 定稿 §七）
# ---------------------------------------------------------------------------
CATEGORY_CODE = {
    "C": "计算机",
    "G": "游戏机",
    "M": "通讯与移动",
    "A": "家电影音",
    "P": "办公与计算外设",
    "E": "嵌入式与工业",
    "X": "其他",
}

# id 格式：大类码-中分类码(2~4 大写)-6 位序号
ID_RE = re.compile(r"^([CGMPAEX])-([A-Z]{2,4})-(\d{6})$")

# 台账路径（相对本仓库根）
REGISTRY_REL = ("docs", "catalog", "registry.jsonl")


# ---------------------------------------------------------------------------
# 路径定位
# ---------------------------------------------------------------------------
def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def registry_path() -> str:
    return os.path.join(repo_root(), *REGISTRY_REL)


# ---------------------------------------------------------------------------
# 台账读写
# ---------------------------------------------------------------------------
def load_registry() -> list[dict]:
    p = registry_path()
    if not os.path.isfile(p):
        return []
    rows = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def save_registry(rows: list[dict]) -> None:
    p = registry_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 扫描目录文件已用 id
# ---------------------------------------------------------------------------
def scan_catalog_ids(files: list[str]) -> dict[str, list[str]]:
    """返回 {id: [file:line, ...]}，扫描目录文件中出现的全部 id。"""
    seen: dict[str, list[str]] = {}
    for path in files:
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8-sig") as f:
            for ln, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rid = obj.get("id")
                if isinstance(rid, str):
                    seen.setdefault(rid, []).append(f"{os.path.basename(path)}:{ln}")
    return seen


# ---------------------------------------------------------------------------
# 命令：allocate
# ---------------------------------------------------------------------------
def cmd_allocate(code: str, count: int, sub: str) -> int:
    code = code.upper()
    sub = (sub or "GEN").upper()
    if code not in CATEGORY_CODE:
        print(f"[FAIL] 大类码 {code!r} 不在对照表 {sorted(CATEGORY_CODE)}")
        return 2
    if not re.fullmatch(r"[A-Z]{2,4}", sub):
        print(f"[FAIL] 中分类码 {sub!r} 非法（应为 2~4 大写字母）")
        return 2

    rows = load_registry()
    # 已有同前缀 id 的最大序号
    used = {r["id"] for r in rows}
    max_seq = 0
    for rid in used:
        m = ID_RE.match(rid)
        if m and m.group(1) == code and m.group(2) == sub:
            max_seq = max(max_seq, int(m.group(3)))

    batch = datetime.date.today().strftime("%Y-%m-%d")
    allocated = []
    seq = max_seq + 1
    for _ in range(count):
        new_id = f"{code}-{sub}-{seq:06d}"
        rows.append({
            "id": new_id,
            "name": "",
            "category": CATEGORY_CODE[code],
            "batch": batch,
            "source_file": None,
        })
        allocated.append(new_id)
        seq += 1

    save_registry(rows)
    print(f"[allocate] 分配 {count} 个 {code}-{sub}-* id（起点 {max_seq + 1}，批次 {batch}）")
    for i, rid in enumerate(allocated):
        print(f"  {rid}")
    print(f"[allocate] registry.jsonl 现有 {len(rows)} 条记录")
    return 0


# ---------------------------------------------------------------------------
# 命令：verify
# ---------------------------------------------------------------------------
def cmd_verify(files: list[str]) -> int:
    seen = scan_catalog_ids(files)
    dup = 0
    fmt_err = 0
    range_err = 0
    total = sum(len(v) for v in seen.values())

    for rid, locs in sorted(seen.items()):
        m = ID_RE.match(rid)
        if not m:
            fmt_err += 1
            print(f"[格式错] {rid!r}（{locs[0]}）非 大类码-中分类码-6位序号")
            continue
        if len(locs) > 1:
            dup += 1
            print(f"[重复]   {rid!r} 出现 {len(locs)} 次：{locs}")
        seq = int(m.group(3))
        if seq == 0:
            range_err += 1
            print(f"[越界]   {rid!r} 序号为 0（{locs[0]}）")

    print(f"[verify] 扫描 {total} 个 id：重复 {dup}，格式错 {fmt_err}，越界 {range_err}")
    return 0  # verify 只报告，不因格式错退出非零（03 无前缀 slug 为已知待迁移项）


# ---------------------------------------------------------------------------
# 命令：report
# ---------------------------------------------------------------------------
def cmd_report(files: list[str]) -> int:
    from collections import Counter
    registry_rows = load_registry()
    reg_ids = [r["id"] for r in registry_rows if "id" in r]
    catalog_ids = scan_catalog_ids(files)

    all_ids = set(reg_ids) | set(catalog_ids)
    counter = Counter()
    for rid in all_ids:
        m = ID_RE.match(rid)
        code = m.group(1) if m else "(无前缀/非法)"
        counter[code] += 1

    print("== 按大类码使用统计 ==")
    for code in sorted(CATEGORY_CODE):
        name = CATEGORY_CODE[code]
        n = counter.get(code, 0)
        print(f"  {code}  {name:<10} {n:>5} 个 id")
    print(f"  其它（无前缀/非法）  {counter.get('(无前缀/非法)', 0):>5} 个 id")
    print(f"[report] 台账 {len(reg_ids)} 条 + 目录文件 {len(catalog_ids)} 个唯一 id")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="目录 ID 注册表服务（TASK-57B）")
    sub = p.add_subparsers(dest="cmd")

    pa = sub.add_parser("allocate", help="顺序分配新 id")
    pa.add_argument("code", help="大类码（C/G/M/A/P/E/X）")
    pa.add_argument("count", type=int, help="分配数量")
    pa.add_argument("sub", nargs="?", default="GEN", help="中分类码（2~4 大写，默认 GEN）")

    pv = sub.add_parser("verify", help="扫描目录文件 id，报重复/越界/格式错")
    pv.add_argument("files", nargs="+", help="目录表单（.jsonl，可多个）")

    p.add_argument("--report", action="store_true", help="按大类码使用统计")
    p.add_argument("--files", nargs="*", default=[], help="报告/统计时扫描的目录文件")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    files = args.files if args.files else []

    if args.cmd == "allocate":
        return cmd_allocate(args.code, args.count, args.sub)
    if args.cmd == "verify":
        return cmd_verify(args.files)
    if args.report or args.cmd is None:
        return cmd_report(files)
    return 0


if __name__ == "__main__":
    sys.exit(main())
