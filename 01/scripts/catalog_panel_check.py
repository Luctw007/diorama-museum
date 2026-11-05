# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""图鉴面板数据层通路自检（TASK-106A）：不发引擎、纯文本级证明
godot/content/catalog/ 的 meta.json → 分片 JSON 数据链路可用。

检查项（C-01~C-03）：
  C-01 meta.json 可解析，total_rows 为正；
  C-02 中分类（shards）数 == 28（预期 28 个分片，与五线目录设计一致）；
  C-03 每个分片文件可读，且实际条数 == meta 声明的 rows；总条数 == total_rows。

用法：python 01/scripts/catalog_panel_check.py
退出码：0=全 PASS；1=存在 FAIL。
"""

from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "godot", "content", "catalog")
META = os.path.join(CATALOG, "meta.json")
EXPECTED_SHARDS = 28


def check(ok: bool, desc: str) -> bool:
    print("  [%s] %s" % ("PASS" if ok else "FAIL", desc))
    return ok


def main() -> int:
    fails = 0
    print("== 图鉴面板数据层通路自检（%s）" % META)
    if not check(os.path.isfile(META), "C-01 meta.json 存在"): 
        return 1

    with open(META, encoding="utf-8") as fh:
        meta = json.load(fh)
    total = int(meta.get("total_rows", 0))
    if not check(total > 0, "C-01 total_rows=%d" % total):
        fails += 1

    shards = meta.get("shards", [])
    if not check(len(shards) == EXPECTED_SHARDS,
                 "C-02 中分类数=%d（预期 %d）" % (len(shards), EXPECTED_SHARDS)):
        fails += 1

    # C-03 分片逐一读盘、条数对账（证明 load_shard 通路与 meta 声明一致）
    sum_rows = 0
    missing = []
    for shard in shards:
        fname = str(shard.get("file", ""))
        declared = int(shard.get("rows", -1))
        path = os.path.join(CATALOG, "data", fname)
        if not os.path.isfile(path):
            missing.append(fname)
            continue
        with open(path, encoding="utf-8") as fh:
            try:
                rows = json.load(fh)
            except json.JSONDecodeError:
                rows = None
        actual = len(rows) if isinstance(rows, list) else -1
        if actual != declared:
            fails += 1
            print("  [FAIL] C-03 %s 声明 %d 条 / 实际 %d 条" % (fname, declared, actual))
        sum_rows += max(actual, 0)

    # 首分片条数（任务书要求打印）
    first = shards[0] if shards else {}
    print("  首分片：%s（声明 %s 条）" % (first.get("file", "-"), first.get("rows", "-")))

    if not check(not missing, "C-03 分片文件全部可读（缺失 %d 个：%s）"
                 % (len(missing), ", ".join(missing[:5]))):
        fails += 1
    if not check(sum_rows == total and total > 0,
                 "C-03 分片实际总条数=%d == total_rows=%d" % (sum_rows, total)):
        fails += 1

    print("汇总：%d 个中分类 / 分片合计 %d 条 / %s"
          % (len(shards), sum_rows, "全 PASS" if fails == 0 else "%d 项 FAIL" % fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())