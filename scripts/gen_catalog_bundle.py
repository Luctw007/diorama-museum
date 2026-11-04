# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""图鉴目录引擎包生成（TASK-56A）：catalog_index 分片 → godot/content/catalog/。

产物：
  godot/content/catalog/meta.json                大/中/子分类树 + 各片行数 + 总行数 + 生成时间
  godot/content/catalog/data/<大类>__<中分类>.json  分片 JSON 数组（内部统一键 + 原始键保留）
用法:
  python scripts/gen_catalog_bundle.py             # 生成
  python scripts/gen_catalog_bundle.py --verify    # 与 catalog_index 行数对账
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import catalog_ingest as ci  # noqa: E402

REPO = os.path.dirname(SCRIPT_DIR)
BUNDLE_ROOT = os.path.join(REPO, "godot", "content", "catalog")
DATA_DIR = os.path.join(BUNDLE_ROOT, "data")


def build_bundle() -> dict:
    files = ci.find_catalog_files()
    if not files:
        print("未发现目录文件（03/05 线尚未产出）")
        return {}
    cat = ci.load_all(files)
    if cat.errors:
        print("摄取存在错误 %d 条，中止打包（先修数据）" % len(cat.errors))
        return {}
    os.makedirs(DATA_DIR, exist_ok=True)
    tree: dict = {}
    total = 0
    shard_rows: list[tuple[str, int]] = []
    for big, mids in cat.tree.items():
        for mid, subs in mids.items():
            rows = [r for s in subs.values() for r in s]
            name = "%s__%s.json" % (big, mid)
            payload = []
            for r in rows:
                item = {k: v for k, v in r.items() if not k.startswith("_")}
                item["_taxonomy"] = r.get("path")
                payload.append(item)
            with open(os.path.join(DATA_DIR, name), "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=1)
            shard_rows.append((name, len(rows)))
            total += len(rows)
            tree.setdefault(big, {})[mid] = sorted(subs)
    meta = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total_rows": total, "taxonomy": tree,
            "shards": [{"file": n, "rows": c, "big": n.split("__")[0],
                        "mid": n.split("__")[1][:-5]} for n, c in shard_rows]}
    with open(os.path.join(BUNDLE_ROOT, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print("打包完成：%d 行 / %d 片 → %s" % (total, len(shard_rows), BUNDLE_ROOT))
    return meta


def verify_bundle() -> bool:
    meta_path = os.path.join(BUNDLE_ROOT, "meta.json")
    if not os.path.isfile(meta_path):
        print("meta.json 不存在（先运行生成）")
        return False
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)
    ok = True
    total = 0
    for shard in meta.get("shards", []):
        path = os.path.join(DATA_DIR, shard["file"])
        if not os.path.isfile(path):
            print("  [FAIL] 缺片 %s" % shard["file"])
            ok = False
            continue
        with open(path, encoding="utf-8") as fh:
            rows = json.load(fh)
        total += len(rows)
        if len(rows) != shard["rows"]:
            print("  [FAIL] %s：实际 %d ≠ meta %d" % (shard["file"], len(rows),
                                                      shard["rows"]))
            ok = False
    if total != meta.get("total_rows"):
        print("  [FAIL] 总行数 %d ≠ meta %d" % (total, meta.get("total_rows")))
        ok = False
    print("verify：%d 片 / %d 行，%s" % (len(meta.get("shards", [])), total,
                                         "通过" if ok else "不一致"))
    return ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="图鉴目录引擎包生成")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv)
    if args.verify:
        return 0 if verify_bundle() else 1
    meta = build_bundle()
    return 0 if meta else 1


if __name__ == "__main__":
    sys.exit(main())