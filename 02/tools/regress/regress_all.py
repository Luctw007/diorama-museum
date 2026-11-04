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
全包回归聚合工具（TASK-22A，纯 stdlib）

对清单内全部内容包顺序跑 `tools/validate/validate.py` 并汇总：
    序号 / 包 / 总计 / FAIL / 耗时 / 退出码

支持 `--fail-fast`（首个 FAIL 即停）与 `--json`（机器可读）。

与 collect_index.py 的分工：本工具是"校验回归"（逐包跑校验、给退出码与耗时），
collect_index.py 是"索引总目"（给字段齐备/门类/路径等静态画像）。二者共享同一
扫描清单（01/02/03/05 仓库 repo/content）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

# 参与扫描的线（仓库）编号
SCAN_LINES = ["01", "02", "03", "05"]

# validate.py / model_check.py / audio_check.py 相对本仓库根的位置
VALIDATE_REL = ("tools", "validate", "validate.py")
MODEL_CHECK_REL = ("tools", "validate", "model_check.py")
AUDIO_CHECK_REL = ("tools", "validate", "audio_check.py")

# MR 规则编号（用于汇总表列）
MR_RULES = ["MR-01", "MR-02", "MR-03", "MR-04"]

# A 规则编号（音频，用于汇总表列）
A_RULES = ["A-01", "A-02", "A-03", "A-04"]


# ---------------------------------------------------------------------------
# 路径定位
# ---------------------------------------------------------------------------
def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def work_root() -> str:
    return os.path.dirname(os.path.dirname(repo_root()))


def validate_script() -> str:
    return os.path.join(repo_root(), *VALIDATE_REL)


def model_check_script() -> str:
    return os.path.join(repo_root(), *MODEL_CHECK_REL)


def audio_check_script() -> str:
    return os.path.join(repo_root(), *AUDIO_CHECK_REL)


def default_content_dirs() -> list[str]:
    w = work_root()
    dirs = []
    for line in SCAN_LINES:
        d = os.path.join(w, line, "repo", "content")
        if os.path.isdir(d):
            dirs.append(d)
    return dirs


def discover_packages(content_dirs: list[str]) -> list[str]:
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
# 校验单包
# ---------------------------------------------------------------------------
def validate_one(pkg: str) -> dict:
    """对单包跑 validate.py，返回结果字典。"""
    script = validate_script()
    label = os.path.relpath(pkg, work_root()).replace("\\", "/")
    rec = {
        "package": label,
        "device_id": os.path.basename(pkg),
        "total": -1,
        "fail": -1,
        "pass": -1,
        "elapsed": 0.0,
        "exit_code": -2,
        "ok": False,
    }
    if not os.path.isfile(script):
        rec["error"] = "validate.py 不存在"
        return rec

    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, script, pkg],
            capture_output=True, text=True, encoding="utf-8",
        )
        rec["exit_code"] = proc.returncode
        out = (proc.stdout or "") + (proc.stderr or "")
    except OSError as e:
        rec["error"] = str(e)
        rec["elapsed"] = time.perf_counter() - t0
        return rec
    rec["elapsed"] = time.perf_counter() - t0

    # 解析末行「总计 X 条：PASS N，FAIL M」
    import re
    for line in reversed(out.splitlines()):
        m = re.search(r"总计\s*(\d+)\s*条[：:]\s*PASS\s*(\d+)[，,]\s*FAIL\s*(\d+)", line)
        if m:
            rec["total"] = int(m.group(1))
            rec["pass"] = int(m.group(2))
            rec["fail"] = int(m.group(3))
            break
    # 校验通过 = 退出码 0 且 FAIL 0
    rec["ok"] = (rec["exit_code"] == 0 and rec["fail"] == 0)
    return rec


def validate_model(pkg: str) -> dict:
    """对单包跑 model_check.py，返回 MR-01..04 的 {fail, warn} 汇总。"""
    script = model_check_script()
    res = {"mr": {r: {"fail": 0, "warn": 0} for r in MR_RULES},
           "mr_fail": 0, "mr_warn": 0, "mesh_count": -1, "error": None}
    if not os.path.isfile(script):
        res["error"] = "model_check.py 不存在"
        return res
    try:
        proc = subprocess.run(
            [sys.executable, script, pkg, "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError as e:
        res["error"] = str(e)
        return res
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        res["error"] = "model_check 输出非 JSON"
        return res
    res["mesh_count"] = data.get("mesh_count", -1)
    for f in data.get("files", []):
        for fd in f.get("findings", []):
            rule = fd.get("rule")
            lvl = fd.get("level")
            if rule in res["mr"] and lvl in ("FAIL", "WARN"):
                key = "fail" if lvl == "FAIL" else "warn"
                res["mr"][rule][key] += 1
                res["mr_" + key] += 1
    return res


def validate_audio(pkg: str) -> dict:
    """对单包跑 audio_check.py，返回 A-01..04 的 {fail, warn} 汇总。"""
    script = audio_check_script()
    res = {"a": {r: {"fail": 0, "warn": 0} for r in A_RULES},
           "a_fail": 0, "a_warn": 0, "audio_file_count": -1, "error": None}
    if not os.path.isfile(script):
        res["error"] = "audio_check.py 不存在"
        return res
    try:
        proc = subprocess.run(
            [sys.executable, script, pkg, "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError as e:
        res["error"] = str(e)
        return res
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        res["error"] = "audio_check 输出非 JSON"
        return res
    res["audio_file_count"] = data.get("audio_file_count", -1)
    for f in data.get("files", []):
        for fd in f.get("findings", []):
            rule = fd.get("rule")
            lvl = fd.get("level")
            if rule in res["a"] and lvl in ("FAIL", "WARN"):
                key = "fail" if lvl == "FAIL" else "warn"
                res["a"][rule][key] += 1
                res["a_" + key] += 1
    return res


# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
def run_all(content_dirs: list[str], fail_fast: bool, with_model: bool = False,
            with_audio: bool = False) -> list[dict]:
    pkgs = discover_packages(content_dirs)
    results = []
    for pkg in pkgs:
        rec = validate_one(pkg)
        if with_model:
            rec["model"] = validate_model(pkg)
        if with_audio:
            rec["audio"] = validate_audio(pkg)
        results.append(rec)
        if fail_fast and not rec["ok"]:
            break
    return results


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_table(results: list[dict]) -> str:
    with_model = any("model" in r for r in results)
    with_audio = any("audio" in r for r in results)

    # 表头动态拼装
    cols = ["序号", "包", "总计", "FAIL"]
    if with_model:
        cols += MR_RULES
    if with_audio:
        cols += A_RULES
    cols += ["耗时(ms)", "结论"] if (with_model or with_audio) else ["PASS", "耗时(ms)", "退出码", "结论"]
    header = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"

    lines = ["全包回归聚合（regress_all.py）", "", header, sep]
    for i, r in enumerate(results, 1):
        fail = str(r["fail"]) if r["fail"] >= 0 else "—"
        total = str(r["total"]) if r["total"] >= 0 else "—"
        passed = str(r["pass"]) if r["pass"] >= 0 else "—"
        code = str(r["exit_code"])
        verdict = "PASS" if r["ok"] else ("FAIL" if r.get("error") is None and r["exit_code"] != -2 else r.get("error", "异常"))
        cells = [str(i), f"`{r['package']}`", total, fail]
        if with_model:
            m = r["model"]
            for rule in MR_RULES:
                rr = m["mr"].get(rule, {"fail": 0, "warn": 0})
                cells.append(f"{rr['fail']}/{rr['warn']}")
        if with_audio:
            a = r["audio"]
            for rule in A_RULES:
                aa = a["a"].get(rule, {"fail": 0, "warn": 0})
                cells.append(f"{aa['fail']}/{aa['warn']}")
        if with_model or with_audio:
            cells += [f"{r['elapsed']*1000:.1f}", verdict]
        else:
            cells += [passed, f"{r['elapsed']*1000:.1f}", code, verdict]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    ok_n = sum(1 for r in results if r["ok"])
    lines.append(f"汇总：{len(results)} 包，PASS {ok_n}，FAIL {len(results)-ok_n}")
    if with_model:
        mf = sum(r.get("model", {}).get("mr_fail", 0) for r in results)
        mw = sum(r.get("model", {}).get("mr_warn", 0) for r in results)
        lines.append(f"建模校验汇总：MR FAIL 合计 {mf}，MR WARN 合计 {mw}")
    if with_audio:
        af = sum(r.get("audio", {}).get("a_fail", 0) for r in results)
        aw = sum(r.get("audio", {}).get("a_warn", 0) for r in results)
        lines.append(f"音频校验汇总：A FAIL 合计 {af}，A WARN 合计 {aw}")
    return "\n".join(lines)


def render_json(results: list[dict]) -> str:
    payload = {
        "tool": "tools/regress/regress_all.py",
        "count": len(results),
        "pass": sum(1 for r in results if r["ok"]),
        "fail": sum(1 for r in results if not r["ok"]),
        "with_model": any("model" in r for r in results),
        "with_audio": any("audio" in r for r in results),
        "packages": results,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="全包回归聚合工具（TASK-22A/32A/42B）")
    p.add_argument("--content-dir", action="append", default=None,
                   help="追加/覆盖扫描的 content 目录（可多次）")
    p.add_argument("--fail-fast", action="store_true", help="首个 FAIL 即停")
    p.add_argument("--with-model", action="store_true",
                   help="每步先 validate 再 model_check，汇总加 MR-01..04 FAIL/WARN 列")
    p.add_argument("--with-audio", action="store_true",
                   help="每步 validate 后再 audio_check，汇总加 A-01..04 FAIL/WARN 列")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    content_dirs = (
        [os.path.abspath(d) for d in args.content_dir]
        if args.content_dir else default_content_dirs()
    )
    results = run_all(content_dirs, args.fail_fast, args.with_model, args.with_audio)

    if args.json:
        sys.stdout.write(render_json(results))
    else:
        print(render_table(results))

    # 退出码：任一 FAIL 或异常 → 1
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
