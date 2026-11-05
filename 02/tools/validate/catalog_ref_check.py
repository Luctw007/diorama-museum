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
目录↔内容包引用一致性校验器（TASK-77B，纯 stdlib）

把"目录与设备包互链"纳入常规门禁——目录条目指向的 device_id/关联包必须存在，已完工包必须被
目录反链。扫描 03/05 两仓 `docs/catalog` 全部 jsonl + 内容包目录 + id_registry 台账，报告四类：

    REF-01 悬空包引用：条目 device_id/关联包 指向不存在的完工包。
    REF-02 反链缺失：ready 包（内容包目录自动发现）无任何目录条目标注关联。
    REF-03 id 台账漂移：registry.jsonl 分配 id 数与目录实际使用数不一致。
    REF-04 关联包形态非法：device_id 非 kebab-case slug。

输出统一 `FAIL n` 计数行（供 verify_all 解析），并逐类给出数字与样例。

用法：
    python catalog_ref_check.py [--json]
    DCM_MONO=<monorepo 根> python catalog_ref_check.py [--json]   # 注入模式（CI 镜像）

不改他线文件（只报告，修复反馈到对应线任务）。
依赖：无（独立脚本）。
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# 路径定位
#
# 三种运行上下文（TASK-102A）：
#   1. 共享盘 D:/work：默认推导——工具自身上溯两级得 02/repo，上溯三级得 work 根。
#   2. monorepo 镜像：CI runner 无共享盘，布局为 <mono>/01|02|03|04|05（无 "repo" 层）。
#   3. DCM_MONO 注入：设置环境变量 DCM_MONO=<monorepo 根> 时，repo_root/work_root/line_repo
#      优先按它解析（对应 01 线 96-B 的 monkeypatch 适配器，本工具原生支持后该 shim 可退役）。
# ---------------------------------------------------------------------------
def _mono_root() -> str | None:
    """DCM_MONO 注入点：指向 monorepo 根（含 01/02/03/04/05 子目录）时为非空。"""
    m = os.environ.get("DCM_MONO", "").strip()
    return os.path.abspath(m) if m else None


def repo_root() -> str:
    """02 线仓库根：默认上溯两级（共享盘）；DCM_MONO 时 = <mono>/02。"""
    m = _mono_root()
    if m:
        return os.path.join(m, "02")
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def work_root() -> str:
    """共享工作根：默认上溯三级；DCM_MONO 时 = <mono>。"""
    m = _mono_root()
    if m:
        return m
    return os.path.dirname(os.path.dirname(repo_root()))


def line_repo(line: str) -> str:
    """某线（02/03/05）仓库目录：共享盘 = <work>/<line>/repo；monorepo = <mono>/<line>。"""
    m = _mono_root()
    if m:
        return os.path.join(m, line)
    return os.path.join(work_root(), line, "repo")


SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def catalog_files() -> list[str]:
    out = []
    for line in ("03", "05"):
        d = os.path.join(line_repo(line), "docs", "catalog")
        if os.path.isdir(d):
            out.extend(glob.glob(os.path.join(d, "*.jsonl")))
    return sorted(out)


def content_packages() -> dict[str, str]:
    """返回 {device_id: 路径}，扫描 03/05 content 目录（含 meta.json 的包）。"""
    out: dict[str, str] = {}
    for line in ("03", "05"):
        d = os.path.join(line_repo(line), "content")
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            p = os.path.join(d, name)
            if os.path.isdir(p) and os.path.isfile(os.path.join(p, "meta.json")):
                try:
                    with open(os.path.join(p, "meta.json"), encoding="utf-8") as f:
                        meta = json.load(f)
                    did = (meta.get("meta") or {}).get("id") or name
                except (OSError, json.JSONDecodeError):
                    did = name
                out[did] = p
    return out


def load_registry_ids() -> dict[str, str]:
    reg = os.path.join(repo_root(), "docs", "catalog", "registry.jsonl")
    out: dict[str, str] = {}
    if not os.path.isfile(reg):
        return out
    with open(reg, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj.get("id"), str):
                out[obj["id"]] = obj.get("batch", "")
    return out


def scan_catalog() -> list[dict]:
    rows = []
    for path in catalog_files():
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rows.append({"id": obj.get("id"), "name": obj.get("name") or obj.get("名称"),
                             "status": obj.get("status") or obj.get("状态"),
                             "device_id": obj.get("device_id") or obj.get("关联包"),
                             "_file": os.path.basename(path)})
    return rows


# ---------------------------------------------------------------------------
# 校验
# ---------------------------------------------------------------------------
def check(pkgs: dict, registry: dict, rows: list[dict]) -> dict:
    ref01 = []
    ref02 = []
    ref03 = []
    ref04 = []
    # 目录里出现的 device_id（done 状态视为"入馆关联"）
    catalog_device_ids = set()

    for r in rows:
        did = r["device_id"]
        if not did:
            continue
        catalog_device_ids.add(str(did))
        # REF-04 形态非法
        if not SLUG_RE.match(str(did)):
            ref04.append((r["id"], did, r["_file"]))
        # REF-01 悬空包引用（指向不存在的完工包）
        if str(did) not in pkgs:
            ref01.append((r["id"], did, r["status"], r["_file"]))

    # REF-02 反链缺失：完工包无任何目录条目标注关联
    for did, p in sorted(pkgs.items()):
        if did not in catalog_device_ids:
            ref02.append(did)

    # REF-03 台账漂移：registry 分配 id 与目录实际使用数不一致
    used = [r["id"] for r in rows if isinstance(r["id"], str)]
    reg_ids = set(registry)
    used_in_catalog = set(used)
    allocated_unused = reg_ids - used_in_catalog   # 分配了但目录没用
    used_unallocated = used_in_catalog - reg_ids   # 目录用了但台账没登记（不算漂移，仅提示）
    ref03 = {
        "registry_count": len(reg_ids),
        "catalog_used_count": len(used_in_catalog & reg_ids),
        "allocated_unused": sorted(allocated_unused)[:10],
        "allocated_unused_count": len(allocated_unused),
    }

    return {
        "REF-01": {"count": len(ref01), "samples": ref01[:10]},
        "REF-02": {"count": len(ref02), "samples": ref02[:20]},
        "REF-03": ref03,
        "REF-04": {"count": len(ref04), "samples": ref04[:10]},
        "total_pkgs": len(pkgs),
        "total_rows": len(rows),
    }


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render(rep: dict) -> str:
    lines = [
        "== 目录↔内容包引用一致性（catalog_ref_check）==",
        f"  内容包 {rep['total_pkgs']} 个，目录条目 {rep['total_rows']} 行",
        f"  REF-01 悬空包引用：{rep['REF-01']['count']} 条",
        f"  REF-02 反链缺失：{rep['REF-02']['count']} 个",
        f"  REF-03 台账漂移：registry {rep['REF-03']['registry_count']} 条 / 目录使用 "
        f"{rep['REF-03']['catalog_used_count']} 条（未使用 {rep['REF-03']['allocated_unused_count']} 条）",
        f"  REF-04 关联包形态非法：{rep['REF-04']['count']} 条",
    ]
    for s in rep["REF-01"]["samples"]:
        lines.append(f"    [REF-01] id={s[0]} device_id={s[1]!r} status={s[2]} ({s[3]})")
    for s in rep["REF-02"]["samples"]:
        lines.append(f"    [REF-02] 完工包 {s} 无目录反链")
    for s in rep["REF-04"]["samples"]:
        lines.append(f"    [REF-04] id={s[0]} 关联包 {s[1]!r} 形态非法 ({s[2]})")

    total_fail = rep["REF-01"]["count"] + rep["REF-02"]["count"] + rep["REF-04"]["count"]
    lines.append(f"FAIL {total_fail}")
    return "\n".join(lines)


def main() -> int:
    pkgs = content_packages()
    registry = load_registry_ids()
    rows = scan_catalog()
    rep = check(pkgs, registry, rows)
    print(render(rep))
    total_fail = rep["REF-01"]["count"] + rep["REF-02"]["count"] + rep["REF-04"]["count"]
    return 1 if total_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
