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
设备目录校验器（TASK-52B/57A，v0.6 定稿 schema，纯 stdlib）

按《内容包与目录规范 v0.6》定稿的目录条目 schema 校验 JSON Lines / CSV 目录表单，
让万级普查的错误在入口即被拦下。输出逐行错误 + 汇总 + `--json`。

定稿键名（57-A 键名裁决，统一英文键）：
    id / name / aliases / manufacturer / origin / era / taxonomy_path /
    status / device_id / influence / verify / sources / research_doc

规则（CC = Catalog Check）：
    CC-01  必填字段齐全（id/name/taxonomy_path/influence/status）。
    CC-02  id 全库唯一 + 格式合法（大类码-中分类码-6 位序号）。
    CC-03  分类路径 taxonomy_path 落在 taxonomy 树内（大分类硬约束；两级补"未细分"）。
    CC-04  状态枚举合法；done/package 状态必须带非空 device_id。
    CC-05  年代 era 范围 [1880, 当年+1]。
    CC-06  影响力理由 influence 非空且 ≤60 字。
    CC-07  别名 aliases 数组元素合法（非空字符串）。
    CC-08  package/wip/done 状态必须带 device_id 且该包存在。
    CC-10  media_class 覆盖率（软落地：默认缺失 WARN，--require-media-class 严格 FAIL）。

用法：
    python catalog_check.py <catalog.jsonl|.csv> [更多文件...] [--json]

依赖：无（独立脚本）。
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# 常量（镜像规范 v0.6 定稿 §2；以 57-A 定稿为准）
# ---------------------------------------------------------------------------
# 七大分类（大分类硬约束，CC-03）
TOP_CATEGORIES = ["计算机", "游戏机", "通讯与移动", "家电影音", "办公与计算外设", "嵌入式与工业", "其他"]

# 大类码 ↔ 大分类（57-A 定稿；吸收 05 线现实，办公外设用 P）
CATEGORY_CODE = {
    "C": "计算机",
    "G": "游戏机",
    "M": "通讯与移动",
    "A": "家电影音",
    "P": "办公与计算外设",
    "E": "嵌入式与工业",
    "X": "其他",
}

# id 格式：大类码（C/G/M/A/P/E/X）- 中分类码（2~4 大写字母）- 6 位序号
ID_RE = re.compile(r"^[CGMPAEX]-[A-Z]{2,4}-\d{6}$")

# 状态枚举（规范 v0.6 §3.4）
STATUSES = {"planned", "researching", "package", "wip", "done"}

# done/package 状态必须带 device_id（CC-04 非空检查）
REQUIRE_DEVICE_ID = {"done", "package"}

# package/wip/done 状态必须带 device_id 且该包存在（CC-08 存在性检查）
REQUIRE_DEVICE_EXIST = {"package", "wip", "done"}

# 必填字段（CC-01）
REQUIRED_FIELDS = ("id", "name", "taxonomy_path", "influence", "status")

YEAR_MIN = 1880
INFLUENCE_MAX = 60


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------
def parse_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                rows.append({"_file": os.path.basename(path), "_line": ln,
                             "_parse_error": f"JSON 解析失败：{e}"})
                continue
            if not isinstance(obj, dict):
                rows.append({"_file": os.path.basename(path), "_line": ln,
                             "_parse_error": "非 JSON 对象"})
                continue
            obj["_file"] = os.path.basename(path)
            obj["_line"] = ln
            rows.append(obj)
    return rows


def parse_csv(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            obj: dict = {}
            for key, val in row.items():
                k = str(key).strip().lower()
                if k in ("aliases", "sources"):
                    obj[k] = [x.strip() for x in str(val).split(";") if x.strip()] if val else []
                elif k == "taxonomy_path":
                    obj[k] = [x.strip() for x in str(val).split("/") if x.strip()] if val else []
                elif k == "era":
                    s = str(val).strip()
                    obj[k] = int(s) if s.isdigit() else (s if s else None)
                else:
                    obj[k] = str(val).strip() if isinstance(val, str) else val
            obj["_file"] = os.path.basename(path)
            obj["_line"] = 0
            rows.append(obj)
    return rows


# ---------------------------------------------------------------------------
# 单条校验
# ---------------------------------------------------------------------------
def _finding(rule: str, level: str, loc: str, msg: str) -> dict:
    return {"rule": rule, "level": level, "location": loc, "message": msg}


def _loc(entry: dict) -> str:
    return f"{entry.get('_file', '?')}:{entry.get('_line', '?')}"


# ---------------------------------------------------------------------------
# 内容包 device_id 发现（CC-08 存在性检查用）
# ---------------------------------------------------------------------------
def discover_device_ids(content_dirs: list[str]) -> set[str]:
    """扫描 content 目录，返回全部 device_id（从 meta.json 取，兜底目录名）。"""
    ids: set[str] = set()
    for base in content_dirs:
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            d = os.path.join(base, name)
            if not os.path.isdir(d) or not os.path.isfile(os.path.join(d, "meta.json")):
                continue
            try:
                with open(os.path.join(d, "meta.json"), "r", encoding="utf-8") as f:
                    meta = json.load(f)
                ids.add((meta.get("meta") or {}).get("id") or name)
            except (OSError, json.JSONDecodeError):
                ids.add(name)
    return ids


def load_registry_ids(repo_root_dir: str | None = None) -> dict[str, str]:
    """读 id_registry 台账，返回「allocate 预留」的 {id: 分配来源}。

    语义（TASK-162A 重建后）：台账经 rebuild 回填后含两类行——
      - source_file 为空（allocate 预留）：目录若复用这些 id = 台账冲突，须 FAIL；
      - source_file 非空（rebuild 从目录回填）：是目录已用 id 的镜像，不算冲突。
    故此处只返回 source_file 为空的 allocate 行。
    """
    here = os.path.dirname(os.path.abspath(__file__))
    repo = repo_root_dir or os.path.dirname(os.path.dirname(here))
    reg = os.path.join(repo, "docs", "catalog", "registry.jsonl")
    out: dict[str, str] = {}
    if not os.path.isfile(reg):
        return out
    with open(reg, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj.get("id"), str) and obj.get("source_file") is None:
                out[obj["id"]] = obj.get("batch", "台账")
    return out


def check_entry(entry: dict, seen_ids: dict, current_year: int,
                valid_device_ids: set[str] | None = None,
                registry_ids: dict[str, str] | None = None,
                require_media_class: bool = False) -> list[dict]:
    loc = _loc(entry)
    out: list[dict] = []

    if entry.get("_parse_error"):
        out.append(_finding("CC-01", "FAIL", loc, entry["_parse_error"]))
        return out

    # CC-01 必填字段齐全
    missing = [f for f in REQUIRED_FIELDS if not entry.get(f)]
    if missing:
        out.append(_finding("CC-01", "FAIL", loc, f"缺必填字段 {missing}"))
    else:
        out.append(_finding("CC-01", "PASS", loc, "必填字段齐全"))

    # CC-02 id 唯一 + 格式（批内全文件联合查重 + 与 id_registry 台账对账）
    rid = entry.get("id")
    if rid:
        if not ID_RE.match(str(rid)):
            out.append(_finding("CC-02", "FAIL", loc,
                                f"id {rid!r} 格式非法（应为 大类码-中分类码-6位序号）"))
        elif registry_ids and str(rid) in registry_ids:
            out.append(_finding("CC-02", "FAIL", loc,
                                f"id {rid!r} 与 id_registry 台账冲突（已分配于 {registry_ids[str(rid)]}）"))
        elif rid in seen_ids:
            out.append(_finding("CC-02", "FAIL", loc,
                                f"id {rid!r} 跨文件重复（首见于 {seen_ids[rid]}）"))
        else:
            seen_ids[rid] = loc
            out.append(_finding("CC-02", "PASS", loc, f"id {rid} 唯一且格式合法"))

    # CC-03 分类路径落在 taxonomy 内（大分类硬约束；两级补"未细分"）
    path = entry.get("taxonomy_path")
    if isinstance(path, list) and len(path) >= 2:
        big = path[0]
        if big not in TOP_CATEGORIES:
            out.append(_finding("CC-03", "FAIL", loc, f"大分类 {big!r} 不在 {TOP_CATEGORIES}"))
        elif any(not p or not str(p).strip() for p in path):
            out.append(_finding("CC-03", "FAIL", loc, "分类路径含空层级"))
        else:
            level_note = "三级" if len(path) >= 3 else "两级（第三级未细分）"
            out.append(_finding("CC-03", "PASS", loc, f"分类路径 {big}/{'/'.join(path[1:])} 合法（{level_note}）"))
    else:
        out.append(_finding("CC-03", "FAIL", loc, "分类路径 taxonomy_path 缺失或不足两级"))

    # CC-04 状态枚举 + device_id 条件
    status = entry.get("status")
    if status not in STATUSES:
        out.append(_finding("CC-04", "FAIL", loc,
                            f"状态 {status!r} 不在枚举 {sorted(STATUSES)}"))
    else:
        if status in REQUIRE_DEVICE_ID and not entry.get("device_id"):
            out.append(_finding("CC-04", "FAIL", loc, f"状态 {status} 必须带 device_id"))
        else:
            out.append(_finding("CC-04", "PASS", loc, f"状态 {status} 合法"))

    # CC-05 年代范围
    era = entry.get("era")
    if era is None or era == "":
        pass  # 年代可选
    elif isinstance(era, int):
        if era < YEAR_MIN or era > current_year + 1:
            out.append(_finding("CC-05", "FAIL", loc,
                                f"年代 {era} 越界（应在 [{YEAR_MIN}, {current_year + 1}]）"))
        else:
            out.append(_finding("CC-05", "PASS", loc, f"年代 {era} 合法"))
    else:
        out.append(_finding("CC-05", "FAIL", loc, f"年代 {era!r} 非合法年份"))

    # CC-06 影响力理由非空 ≤60 字
    influence = entry.get("influence")
    if not influence or not str(influence).strip():
        out.append(_finding("CC-06", "FAIL", loc, "影响力理由 influence 为空"))
    elif len(str(influence)) > INFLUENCE_MAX:
        out.append(_finding("CC-06", "FAIL", loc,
                            f"影响力理由 {len(str(influence))} 字，超 {INFLUENCE_MAX} 字上限"))
    else:
        out.append(_finding("CC-06", "PASS", loc, f"影响力理由 {len(str(influence))} 字合规"))

    # CC-07 别名数组元素合法
    aliases = entry.get("aliases")
    if aliases is not None:
        if not isinstance(aliases, list):
            out.append(_finding("CC-07", "FAIL", loc, "别名 aliases 非数组"))
        else:
            bad = [a for a in aliases if not isinstance(a, str) or not a.strip()]
            if bad:
                out.append(_finding("CC-07", "FAIL", loc, f"别名含非法元素 {bad}"))
            else:
                out.append(_finding("CC-07", "PASS", loc, f"别名 {len(aliases)} 个合法"))
    else:
        out.append(_finding("CC-07", "PASS", loc, "无别名（可选）"))

    # CC-08 package/wip/done 必须带 device_id 且该包存在
    if status in REQUIRE_DEVICE_EXIST:
        did = entry.get("device_id")
        if not did:
            out.append(_finding("CC-08", "FAIL", loc, f"状态 {status} 必须带 device_id"))
        elif valid_device_ids is not None and str(did) not in valid_device_ids:
            out.append(_finding("CC-08", "FAIL", loc, f"device_id {did!r} 不存在于 content 目录"))
        else:
            out.append(_finding("CC-08", "PASS", loc, f"device_id {did} 存在"))

    # CC-10 media_class 覆盖率（软落地：默认缺失记 WARN，--require-media-class 时记 FAIL）
    mc = entry.get("media_class")
    if mc and str(mc).strip():
        out.append(_finding("CC-10", "PASS", loc, f"media_class {mc} 存在"))
    else:
        lvl = "FAIL" if require_media_class else "WARN"
        out.append(_finding("CC-10", lvl, loc, "media_class 缺失或为空（回填后须有值）"))

    return out


# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
def check_files(files: list[str], valid_device_ids: set[str] | None = None,
                registry_ids: dict[str, str] | None = None,
                require_media_class: bool = False) -> dict:
    seen_ids: dict = {}
    current_year = datetime.date.today().year
    rows = []
    n_fail = 0
    n_warn = 0
    per_rule = {r: {"fail": 0, "pass": 0, "warn": 0} for r in
                ("CC-01", "CC-02", "CC-03", "CC-04", "CC-05", "CC-06", "CC-07", "CC-08", "CC-10")}

    for path in files:
        parsed = parse_csv(path) if path.endswith(".csv") else parse_jsonl(path)
        for entry in parsed:
            findings = check_entry(entry, seen_ids, current_year, valid_device_ids,
                                  registry_ids, require_media_class)
            for f in findings:
                if f["level"] == "FAIL":
                    n_fail += 1
                    if f["rule"] in per_rule:
                        per_rule[f["rule"]]["fail"] += 1
                elif f["level"] == "WARN":
                    n_warn += 1
                    if f["rule"] in per_rule:
                        per_rule[f["rule"]]["warn"] += 1
                elif f["level"] == "PASS" and f["rule"] in per_rule:
                    per_rule[f["rule"]]["pass"] += 1
            rows.append({"entry": entry, "findings": findings})

    return {
        "files": [os.path.basename(f) for f in files],
        "row_count": len(rows),
        "unique_id": len(seen_ids),
        "fail": n_fail,
        "warn": n_warn,
        "per_rule": per_rule,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_report(rep: dict) -> str:
    lines = [f"== 目录校验（文件 {len(rep['files'])} 个，条目 {rep['row_count']} 行，"
             f"唯一 id {rep['unique_id']}，FAIL {rep['fail']}，WARN {rep['warn']}）=="]
    for r in rep["rows"]:
        entry = r["entry"]
        loc = _loc(entry)
        fails = [f for f in r["findings"] if f["level"] == "FAIL"]
        if fails:
            lines.append(f"  {loc}  id={entry.get('id', '?')!r}")
            for f in fails:
                lines.append(f"    {f['rule']}  {f['message']}")
    lines.append("  规则汇总：")
    for rule, cnt in rep["per_rule"].items():
        warn = f" / WARN {cnt['warn']}" if cnt.get("warn") else ""
        lines.append(f"    {rule}  FAIL {cnt['fail']} / PASS {cnt['pass']}{warn}")
    return "\n".join(lines)


def render_json(rep: dict) -> str:
    payload = {
        "files": rep["files"],
        "row_count": rep["row_count"],
        "unique_id": rep["unique_id"],
        "fail": rep["fail"],
        "warn": rep["warn"],
        "per_rule": rep["per_rule"],
        "rows": [
            {"location": _loc(r["entry"]),
             "id": r["entry"].get("id"),
             "findings": [f for f in r["findings"] if f["level"] == "FAIL"]}
            for r in rep["rows"]
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="设备目录校验器（TASK-52B/57A/67A/162B，v0.6 定稿 CC-01~10）")
    p.add_argument("files", nargs="+", help="目录表单（.jsonl 或 .csv，可多个）")
    p.add_argument("--content-dir", action="append", default=None,
                   help="追加/覆盖 content 目录（CC-08 device_id 存在性检查用，可多次）")
    p.add_argument("--require-media-class", action="store_true",
                   help="CC-10 严格模式：media_class 缺失记 FAIL（默认仅 WARN）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    return p


def default_content_dirs() -> list[str]:
    """默认 content 目录（03/05/02 线 repo/content）。"""
    here = os.path.dirname(os.path.abspath(__file__))   # tools/validate
    repo = os.path.dirname(os.path.dirname(here))       # <repo>
    work = os.path.dirname(os.path.dirname(repo))       # <work>
    dirs = []
    for line in ("03", "05", "02"):
        d = os.path.join(work, line, "repo", "content")
        if os.path.isdir(d):
            dirs.append(d)
    return dirs


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    files = [os.path.abspath(f) for f in args.files]
    for f in files:
        if not os.path.isfile(f):
            sys.stderr.write(f"错误：文件不存在 {f}\n")
            return 2

    content_dirs = [os.path.abspath(d) for d in args.content_dir] if args.content_dir else default_content_dirs()
    valid_device_ids = discover_device_ids(content_dirs)
    registry_ids = load_registry_ids()

    rep = check_files(files, valid_device_ids, registry_ids, args.require_media_class)
    if args.json:
        sys.stdout.write(render_json(rep))
    else:
        print(render_report(rep))
    return 1 if rep["fail"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
