# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""设备目录摄取工具（TASK-51A）：目录表单（JSONL/CSV）→ 分类树索引 + 分片存盘 + 查询。

条目 schema（与 02 线 v0.6 草案对齐；52-A 定稿后按定稿修正，见 docs/catalog_schema.md）：
  id（全库唯一）、name、aliases[]、maker、origin、year、
  path[]（[大分类, 中分类, 子分类]）、reason（≤60字）、status、device_id（可空）、sources[]

用法:
  python scripts/catalog_ingest.py --stats --csv <文件>
  python scripts/catalog_ingest.py --from-work --stats
  python scripts/catalog_ingest.py --from-work --find apple
  python scripts/catalog_ingest.py --from-work --gate      # 门禁：无文件 SKIP(0)；有错 FAIL(1)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCRIPTS)
WORK_ROOT = os.path.dirname(os.path.dirname(REPO))          # D:\work
CATALOG_ROOTS = [
    os.path.join(WORK_ROOT, "03", "repo", "docs", "catalog"),
    os.path.join(WORK_ROOT, "05", "repo", "docs", "catalog"),
]
INDEX_DIR = os.path.join(REPO, "catalog_index")
SHARD_MAX = 5000

TITLE_RE = re.compile(r"\s+")


def _adapt(obj: dict) -> dict:
    """字段归一（TASK-51A 收尾）：兼容三种键格式——02 线 v0.6 英文定稿键、05 线中文键、我线草稿键。
    内部统一键：id/name/aliases/maker/origin/year/path/reason/status/device_id/sources。"""
    def pick(*keys):
        for k in keys:
            v = obj.get(k)
            if v not in (None, "", []):
                return v
        return None
    out = dict(obj)
    out["name"] = pick("name", "名称") or out.get("id", "")
    out["aliases"] = pick("aliases", "alias", "别名") or []
    out["maker"] = pick("maker", "manufacturer", "厂商") or ""
    out["origin"] = pick("origin", "产地") or ""
    out["year"] = obj.get("year") if obj.get("year") is not None else pick("era", "年代")
    out["path"] = pick("path", "taxonomy_path", "分类路径")
    out["reason"] = pick("reason", "influence", "影响力理由") or ""
    out["status"] = pick("status", "状态") or "planned"
    out["device_id"] = pick("device_id", "关联包")
    out["sources"] = pick("sources", "来源编号") or []
    return out


def _norm(text: str) -> str:
    return TITLE_RE.sub("", str(text)).lower()


def find_catalog_files() -> list[str]:
    out = []
    for root in CATALOG_ROOTS:
        if not os.path.isdir(root):
            continue
        for f in sorted(os.listdir(root)):
            if f.endswith(".jsonl"):
                out.append(os.path.join(root, f))
    return out


def parse_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8-sig") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                print("[FAIL] %s:%d JSON 解析失败: %s" % (path, ln, exc))
                continue
            obj = _adapt(obj)
            obj.setdefault("_file", os.path.basename(path))
            obj.setdefault("_line", ln)
            rows.append(obj)
    return rows


def parse_csv(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            obj = {}
            for key, val in row.items():
                key_n = str(key).strip().lower()
                key_m = {"taxonomy_path": "path", "alias": "aliases",
                         "manufacturer": "maker", "era": "year",
                         "influence": "reason"}.get(key_n, key_n)
                if key_m in ("aliases", "sources"):
                    obj[key_m] = [x.strip() for x in val.split(";") if x.strip()] if val else []
                elif key_m == "year":
                    try:
                        obj[key_m] = int(val) if val.strip() else None
                    except ValueError:
                        obj[key_m] = val
                elif key_m == "path":
                    obj[key_m] = [x.strip() for x in val.split("/") if x.strip()] if val else []
                elif key_m == "status":
                    obj[key_m] = val.strip() if val else "planned"
                else:
                    obj[key_m] = val.strip() if isinstance(val, str) else val
            obj.setdefault("_file", os.path.basename(path))
            obj["_line"] = 0
            rows.append(obj)
    return rows


class Catalog:
    def __init__(self, rows: list[dict]) -> None:
        self.rows = rows
        self.by_id: dict[str, dict] = {}
        self.by_name: dict[str, list[dict]] = {}
        self.tree: dict = {}          # 大分类 -> 中分类 -> 子分类 -> [rows]
        self.errors: list[str] = []
        self._build()

    def _build(self) -> None:
        for r in self.rows:
            rid = r.get("id")
            if not rid:
                self.errors.append("缺 id: %s 行 %s" % (r.get("_file"), r.get("_line")))
                continue
            if rid in self.by_id:
                self.errors.append("重复 id: %s（%s 与 %s 行 %s）"
                                   % (rid, self.by_id[rid].get("_file"),
                                      r.get("_file"), r.get("_line")))
                continue
            self.by_id[rid] = r
            for key in [r.get("name", "")] + list(r.get("aliases") or []):
                if key:
                    self.by_name.setdefault(_norm(key), []).append(r)
            path = r.get("path") or []
            if not isinstance(path, list) or len(path) < 2:
                self.errors.append("分类路径不足二级: %s（%s）" % (rid, r.get("_file")))
                continue
            if len(path) == 2:
                path = list(path) + ["未细分"]
                r["path"] = path
            big, mid, sub = path[0], path[1], path[2]
            node = self.tree.setdefault(big, {}).setdefault(mid, {}).setdefault(sub, [])
            node.append(r)

    def stats(self) -> dict:
        n_mid = sum(len(m) for m in self.tree.values())
        n_sub = sum(len(s) for m in self.tree.values() for s in m.values())
        return {"rows": len(self.rows), "unique_id": len(self.by_id),
                "big": len(self.tree), "mid": n_mid, "sub": n_sub,
                "errors": len(self.errors)}

    def find(self, keyword: str) -> list[dict]:
        return self.by_name.get(_norm(keyword), [])

    def list_path(self, path: str) -> list[dict]:
        parts = [p for p in path.split("/") if p]
        if len(parts) == 3:
            return self.tree.get(parts[0], {}).get(parts[1], {}).get(parts[2], [])
        if len(parts) == 2:
            out = []
            for rows in self.tree.get(parts[0], {}).get(parts[1], {}).values():
                out.extend(rows)
            return out
        if len(parts) == 1:
            out = []
            for mid in self.tree.get(parts[0], {}).values():
                for rows in mid.values():
                    out.extend(rows)
            return out
        return []

    def write_shards(self) -> int:
        os.makedirs(INDEX_DIR, exist_ok=True)
        count = 0
        manifest: list[dict] = []
        for big, mids in self.tree.items():
            for mid, subs in mids.items():
                rows = [r for s in subs.values() for r in s]
                safe = re.sub(r"[^\w\u4e00-\u9fff-]", "_", "%s__%s" % (big, mid))
                shard_path = os.path.join(INDEX_DIR, "%s.jsonl" % safe)
                with open(shard_path, "w", encoding="utf-8") as fh:
                    for r in rows:
                        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                manifest.append({"file": os.path.basename(shard_path),
                                 "big": big, "mid": mid, "count": len(rows)})
                count += len(rows)
        with open(os.path.join(INDEX_DIR, "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump({"shards": manifest}, fh, ensure_ascii=False, indent=2)
        return count


def load_all(files: list[str]) -> Catalog:
    rows: list[dict] = []
    for path in files:
        if path.endswith(".csv"):
            rows.extend(parse_csv(path))
        else:
            rows.extend(parse_jsonl(path))
    return Catalog(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="设备目录摄取工具")
    ap.add_argument("--csv", help="单个 CSV 目录文件")
    ap.add_argument("--jsonl", help="单个 JSONL 目录文件")
    ap.add_argument("--from-work", action="store_true", help="扫描 03/05 线 docs/catalog")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--find", help="关键词查询（名称/别名）")
    ap.add_argument("--list", help="分类路径查询（大/中[/子]）")
    ap.add_argument("--shard", action="store_true", help="写分片索引")
    ap.add_argument("--gate", action="store_true", help="门禁模式：无文件 SKIP(0)，有错 FAIL(1)")
    ap.add_argument("--gate-verify", action="store_true",
                    help="gate 通过后追加 bundle 对账（bundle 未生成则 SKIP）")
    args = ap.parse_args(argv)

    files: list[str] = []
    if args.csv:
        files.append(args.csv)
    if args.jsonl:
        files.append(args.jsonl)
    if args.from_work or not files:
        files.extend(find_catalog_files())
    if args.gate:
        if not files:
            print("[SKIP] 未发现目录文件（03/05 线尚未产出，正常）")
            return 0
        cat = load_all(files)
        for e in cat.errors:
            print("  [FAIL] " + e)
        print("[catalog] 摄取 %d 文件 %d 行，错误 %d"
              % (len(files), len(cat.rows), len(cat.errors)))
        if cat.errors:
            return 1
        if args.gate_verify:
            meta_path = os.path.join(REPO, "godot", "content", "catalog", "meta.json")
            if not os.path.isfile(meta_path):
                print("[SKIP] bundle 尚未生成（运行 gen_catalog_bundle.py 或执行 sync_content）")
                return 0
            import gen_catalog_bundle as gcb  # noqa: E402 同目录脚本
            return 0 if gcb.verify_bundle() else 1
        return 0
    if not files:
        print("未发现任何目录文件（--csv/--jsonl/--from-work）")
        return 1
    cat = load_all(files)
    if args.stats or not (args.find or args.list):
        st = cat.stats()
        print("文件 %d；行 %d；唯一 id %d；大分类 %d；中分类 %d；子分类 %d；错误 %d"
              % (len(files), st["rows"], st["unique_id"], st["big"],
                 st["mid"], st["sub"], st["errors"]))
        for e in cat.errors[:20]:
            print("  [FAIL] " + e)
    if args.find:
        hits = cat.find(args.find)
        print("查询 %r：%d 条" % (args.find, len(hits)))
        for r in hits[:10]:
            print("  %s  %s（%s） %s" % (r.get("id"), r.get("name"),
                                          "/".join(r.get("path") or []),
                                          r.get("year") or "?"))
    if args.list:
        rows = cat.list_path(args.list)
        print("分类路径 %r：%d 条" % (args.list, len(rows)))
        for r in rows[:10]:
            print("  %s  %s（%s）" % (r.get("id"), r.get("name"), r.get("year") or "?"))
    if args.shard:
        print("分片写入：%d 条 → %s" % (cat.write_shards(), INDEX_DIR))
    return 1 if cat.errors else 0


if __name__ == "__main__":
    sys.exit(main())