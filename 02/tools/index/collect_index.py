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
全包索引生成器（TASK-22A，纯 stdlib）

扫描清单内的全部内容包（01/02/03/05 仓库的 content 目录），产出
`docs/全包索引.md`（自动生成）。每包记录：
    device-id / 名称 / 门类 Hall 归属 / 仓库路径 / validate FAIL 数 /
    字段齐备列 / 上次校验时间

`--json` 输出机器可读版本（stdout）。

设计说明
--------
- 清单默认取本仓库（02 线）的同级 01/02/03/05 仓库 `repo/content` 目录；
  可用 `--content-dir` 反复指定覆盖/追加。
- 同名 device-id 若在多个仓库出现（如 02 脚手架骨架与 03 生产包），索引按
  device-id 去重：保留"生产仓库"为 canonical，其余记为 duplicates 附注；
  校验夹具（test-device）单独标注，不进"展项"计数。
- 校验失败数通过调用 `tools/validate/validate.py` 得到（解析末行
  「总计 X 条：PASS N，FAIL M」）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
# 参与扫描的线（仓库）编号；02 为本线，04 为设计线（无量产包），均按任务排除/说明
SCAN_LINES = ["01", "02", "03", "05"]

# 从 meta.category → 门类 Hall 归属
HALL_BY_CATEGORY = {
    "early-computer": "计算机黎明厅",
    "computer": "个人计算机厅",
    "personal-computer": "个人计算机厅",
    "console": "游戏机厅",
    "game-console": "游戏机厅",
    "mainframe": "大型机与小型机厅",
    "minicomputer": "大型机与小型机厅",
    "placeholder": "（校验夹具 · 非展项）",
}

# 字段齐备检查：这些 meta 字段若缺失则列入"缺"清单（v0.2 可选新增字段）
COMPLETENESS_FIELDS = ["intro", "era", "manufacturer", "description", "category"]

# validate.py / model_check.py / audio_check.py 相对本仓库根的位置
VALIDATE_REL = ("tools", "validate", "validate.py")
MODEL_CHECK_REL = ("tools", "validate", "model_check.py")
AUDIO_CHECK_REL = ("tools", "validate", "audio_check.py")

# 夹具设备 id（非展项，索引中单独标注）
FIXTURE_IDS = {"test-device"}


# ---------------------------------------------------------------------------
# 路径定位
# ---------------------------------------------------------------------------
def _mono_root() -> str | None:
    """DCM_MONO 注入点（TASK-167B）：指向 monorepo 根时为非空。"""
    m = os.environ.get("DCM_MONO", "").strip()
    return os.path.abspath(m) if m else None


def repo_root() -> str:
    """本脚本位于 <repo>/tools/index/，返回 <repo> 根目录；DCM_MONO 时 = <mono>/02。"""
    m = _mono_root()
    if m:
        return os.path.join(m, "02")
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def work_root() -> str:
    """返回各线仓库的公共上级目录（work/）；DCM_MONO 时 = <mono>。"""
    m = _mono_root()
    if m:
        return m
    return os.path.dirname(os.path.dirname(repo_root()))


def validate_script() -> str:
    return os.path.join(repo_root(), *VALIDATE_REL)


def model_check_script() -> str:
    return os.path.join(repo_root(), *MODEL_CHECK_REL)


def audio_check_script() -> str:
    return os.path.join(repo_root(), *AUDIO_CHECK_REL)


def default_content_dirs() -> list[str]:
    """默认清单：01/02/03/05 仓库的 repo/content 目录。"""
    w = work_root()
    dirs = []
    for line in SCAN_LINES:
        d = os.path.join(w, line, "repo", "content")
        if os.path.isdir(d):
            dirs.append(d)
    return dirs


# ---------------------------------------------------------------------------
# 包发现
# ---------------------------------------------------------------------------
def discover_packages(content_dirs: list[str]) -> list[str]:
    """返回所有含 meta.json 的子目录（内容包目录），按路径排序。"""
    pkgs = []
    for base in content_dirs:
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            sub = os.path.join(base, name)
            if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, "meta.json")):
                pkgs.append(sub)
    return sorted(pkgs)


# ---------------------------------------------------------------------------
# 读取 meta
# ---------------------------------------------------------------------------
def _name_str(meta: dict) -> str:
    name = meta.get("name")
    if isinstance(name, dict):
        zh = name.get("zh")
        en = name.get("en")
        if en and en != zh:
            return f"{zh} / {en}"
        return zh or ""
    return name if isinstance(name, str) else ""


def _hall(category) -> str:
    return HALL_BY_CATEGORY.get(category, "（未归类）")


def _completeness(meta: dict) -> str:
    missing = [f for f in COMPLETENESS_FIELDS if f not in meta]
    if not missing:
        return "齐备"
    return "缺 " + "、".join(missing)


def read_meta(pkg: str) -> dict:
    """读取 meta.json 并返回索引所需字段。meta.json 缺失/非法时降级为占位。"""
    meta_path = os.path.join(pkg, "meta.json")
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return {
            "device_id": os.path.basename(pkg),
            "name": "",
            "category": None,
            "hall": "（读取失败）",
            "completeness": "（读取失败）",
            "error": str(e),
        }
    m = data.get("meta", {}) if isinstance(data, dict) else {}
    return {
        "device_id": m.get("id") or os.path.basename(pkg),
        "name": _name_str(m),
        "category": m.get("category"),
        "hall": _hall(m.get("category")),
        "completeness": _completeness(m),
    }


# ---------------------------------------------------------------------------
# 校验
# ---------------------------------------------------------------------------
def run_validate(pkg: str) -> tuple[int, int, int]:
    """调用 validate.py，返回 (total, pass, fail)。校验器不可用时返回 (-1,-1,-1)。"""
    script = validate_script()
    if not os.path.isfile(script):
        return -1, -1, -1
    try:
        proc = subprocess.run(
            [sys.executable, script, pkg],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return -1, -1, -1
    out = (proc.stdout or "") + (proc.stderr or "")
    m = re.search(r"总计\s*(\d+)\s*条[：:]\s*PASS\s*(\d+)[，,]\s*FAIL\s*(\d+)", out)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return -1, -1, -1


def run_model_check(pkg: str) -> tuple[int, int]:
    """调用 model_check.py，返回 (mr_fail, mr_warn)。不可用时返回 (-1, -1)。"""
    script = model_check_script()
    if not os.path.isfile(script):
        return -1, -1
    try:
        proc = subprocess.run(
            [sys.executable, script, pkg, "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return -1, -1
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return -1, -1
    return data.get("fail", -1), data.get("warn", -1)


def run_audio_check(pkg: str) -> tuple[int, int]:
    """调用 audio_check.py，返回 (a_fail, a_warn)。不可用时返回 (-1, -1)。"""
    script = audio_check_script()
    if not os.path.isfile(script):
        return -1, -1
    try:
        proc = subprocess.run(
            [sys.executable, script, pkg, "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return -1, -1
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return -1, -1
    return data.get("fail", -1), data.get("warn", -1)


def _priority(rec: dict) -> int:
    """同名包的"保留优先级"：非夹具 + 类别可归类 + 规则数，越高越 canonical。"""
    score = 0
    if not rec["is_fixture"]:
        score += 1000
    if rec["hall"] != "（未归类）" and rec["hall"] != "（读取失败）":
        score += 100
    if rec["total"] > 0:
        score += rec["total"]
    return score


# ---------------------------------------------------------------------------
# 索引构建（含去重与夹具标注）
# ---------------------------------------------------------------------------
def build_records(content_dirs: list[str]):
    """返回 (records, notes)：records 为按 device-id 去重后的索引记录。"""
    pkgs = discover_packages(content_dirs)
    by_id: dict[str, dict] = {}

    for pkg in pkgs:
        info = read_meta(pkg)
        did = info["device_id"]
        total, passed, failed = run_validate(pkg)
        mr_fail, mr_warn = run_model_check(pkg)
        a_fail, a_warn = run_audio_check(pkg)
        line = os.path.relpath(pkg, work_root()).replace("\\", "/")
        rec = {
            "device_id": did,
            "name": info["name"],
            "hall": info["hall"],
            "category": info["category"],
            "path": line,
            "total": total,
            "pass": passed,
            "fail": failed,
            "mr_fail": mr_fail,
            "mr_warn": mr_warn,
            "a_fail": a_fail,
            "a_warn": a_warn,
            "completeness": info["completeness"],
            "is_fixture": did in FIXTURE_IDS,
            "error": info.get("error"),
        }
        if did not in by_id:
            by_id[did] = rec
            by_id[did]["duplicates"] = []
        else:
            # 同名重复：优先保留"生产包"（非夹具 + 规则数更多），其余记为副本
            old = by_id[did]
            old_score = _priority(old)
            new_score = _priority(rec)
            if new_score > old_score:
                rec["duplicates"] = old["duplicates"] + [old["path"]]
                by_id[did] = rec
            else:
                old["duplicates"].append(rec["path"])

    records = [by_id[k] for k in sorted(by_id)]
    notes = []
    for r in records:
        if r.get("duplicates"):
            notes.append(f"{r['device_id']} 在其它仓库有同名副本：{'、'.join(r['duplicates'])}")
    return records, notes


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_markdown(records, notes, generated_at: str) -> str:
    lines = [
        "# 全包索引（自动生成，勿手改）",
        "",
        f"> 生成时间：{generated_at}　|　生成工具：`tools/index/collect_index.py`（TASK-42B）",
        f"> 扫描范围：01/02/03/05 仓库 `repo/content`；按 device-id 去重。",
        "",
        "| # | device-id | 名称 | 门类 Hall 归属 | 仓库路径 | 总计 | PASS | FAIL | MR-FAIL | MR-WARN | A-FAIL | A-WARN | 字段齐备 |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(records, 1):
        marker = " ⚠夹具" if r["is_fixture"] else ""
        name = r["name"] or "（无）"
        fail_txt = str(r["fail"]) if r["fail"] >= 0 else "—"
        mrf = str(r.get("mr_fail")) if r.get("mr_fail", -1) >= 0 else "—"
        mrw = str(r.get("mr_warn")) if r.get("mr_warn", -1) >= 0 else "—"
        af = str(r.get("a_fail")) if r.get("a_fail", -1) >= 0 else "—"
        aw = str(r.get("a_warn")) if r.get("a_warn", -1) >= 0 else "—"
        lines.append(
            f"| {i} | {r['device_id']}{marker} | {name} | {r['hall']} | "
            f"`{r['path']}` | {r['total']} | {r['pass']} | {fail_txt} | {mrf} | {mrw} | {af} | {aw} | {r['completeness']} |"
        )

    if notes:
        lines.append("")
        lines.append("## 同名副本说明")
        for n in notes:
            lines.append(f"- {n}")

    lines.append("")
    lines.append("## 说明")
    lines.append("- `test-device` 为 02 线校验夹具（非展项），不计入展项清单。")
    lines.append("- `字段齐备` 列检查 `intro/era/manufacturer/description/category` 五个可选字段是否齐备。")
    lines.append("- `FAIL` 由 `tools/validate/validate.py` 实测；`MR-FAIL/MR-WARN` 由 `model_check.py` 实测；`A-FAIL/A-WARN` 由 `audio_check.py` 实测；`-1` 表示工具不可用。")
    return "\n".join(lines) + "\n"


def render_json(records, notes, generated_at: str) -> str:
    payload = {
        "generated_at": generated_at,
        "tool": "tools/index/collect_index.py",
        "count": len(records),
        "packages": [
            {k: v for k, v in r.items() if k != "duplicates"}
            for r in records
        ],
        "notes": notes,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="全包索引生成器（TASK-22A）")
    p.add_argument("--content-dir", action="append", default=None,
                   help="追加/覆盖扫描的 content 目录（可多次）")
    p.add_argument("--out", default=None, help="索引输出路径（默认 <repo>/docs/全包索引.md）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    p.add_argument("--no-validate", action="store_true", help="跳过校验（索引仍生成，FAIL 记 -1）")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.content_dir:
        content_dirs = [os.path.abspath(d) for d in args.content_dir]
    else:
        content_dirs = default_content_dirs()

    records, notes = build_records(content_dirs)
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if args.json:
        sys.stdout.write(render_json(records, notes, generated_at))
        return 0

    md = render_markdown(records, notes, generated_at)
    out_path = args.out or os.path.join(repo_root(), "docs", "全包索引.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"已生成索引：{out_path}")
    print(f"共 {len(records)} 个 device-id（去重后），扫描包目录 {len(discover_packages(content_dirs))} 个")
    for r in records:
        fail_txt = f"FAIL {r['fail']}" if r["fail"] >= 0 else "校验不可用"
        print(f"  {r['device_id']:<18} {r['hall']:<16} {r['total']} 条 {fail_txt}")
    for n in notes:
        print(f"  [同名] {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
