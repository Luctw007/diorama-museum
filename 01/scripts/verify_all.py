# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""一键全量验收（TASK-16A）：01 线三套验收 + 02 线内容包校验的单命令门禁。

用法:
  python scripts/verify_all.py              # 全量：m0 -> m1 -> m1b -> 5 个内容包
  python scripts/verify_all.py --only m0|m1|m1b|pkg
  python scripts/verify_all.py --daily      # 最小回归集：m0 + m1b + pkg
  python scripts/verify_all.py --daily --cache   # 结果写 docs/verify_last.json（或 --cache <路径>）
  python scripts/verify_all.py --daily --cache --no-ref-hard   # catalog_ref 降级为告警（临时）
退出码：全部通过 0；任何一项失败 1。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import pkg_registry  # noqa: E402  门禁数据驱动化（TASK-41A）

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

VALIDATOR = r"D:\work\02\repo\tools\validate\validate.py"
# TASK-96B：共享盘不存在（CI runner）时改用 monorepo 镜像内校验器
_MONO = os.path.dirname(REPO)
if os.environ.get("DCM_FORCE_MIRROR") == "1" or not os.path.isfile(VALIDATOR):
    VALIDATOR = os.path.join(_MONO, "02", "tools", "validate", "validate.py")
READY, WIP = pkg_registry.discover_packages_full()
PKGS = READY   # 完工包进失败判定；WIP 只提示（生产中）

FAIL_RE = re.compile(r"FAIL\s*(\d+)")
SUMMARY_RE = re.compile(r"总计\s*\d+\s*条[：:]\s*PASS\s*\d+[，,]\s*FAIL\s*\d+")


def run_step(name: str, argv: list[str]) -> tuple[bool, str]:
    """运行一步；返回 (是否通过, 备注)。"""
    label = "[%s] %s" % (name, " ".join(argv))
    print("== " + label)
    try:
        cp = subprocess.run([PY] + argv, cwd=REPO, capture_output=True,
                            text=True, encoding="utf-8", errors="replace",
                            timeout=900)
    except subprocess.TimeoutExpired:
        print("!! 超时（>900s）")
        return False, "超时"
    out = (cp.stdout or "") + ("\n" + cp.stderr if (cp.stderr or "").strip() else "")
    lines = [ln for ln in out.splitlines() if ln.strip()][-4:]
    for ln in lines:
        print("   " + ln[:160])

    if name.startswith("pkg") or name == "catalog_ref":
        m = FAIL_RE.search(out)
        fails = int(m.group(1)) if m else (0 if cp.returncode == 0 else -1)
        if fails < 0:
            return False, "校验器输出无法解析（rc=%d）" % cp.returncode
        return (fails == 0), ("FAIL %d" % fails if fails else "FAIL 0")

    pass_line = lines[-1] if lines else ""
    if cp.returncode != 0:
        return False, ("rc=%d%s" % (cp.returncode,
                                    ("；" + pass_line) if pass_line else ""))
    return True, pass_line


def apply_ref_downgrade(results: list[tuple[str, bool, str]],
                        no_ref_hard: bool) -> list[tuple[str, bool, str]]:
    """TASK-81A：catalog_ref 失败时降级为告警（不计入判定），note 追加标记。"""
    out: list[tuple[str, bool, str]] = []
    for name, ok, note in results:
        if no_ref_hard and name == "catalog_ref" and not ok:
            out.append((name, True, note + "〔--no-ref-hard 告警降级〕"))
        else:
            out.append((name, ok, note))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="一键全量验收（m0/m1/m1b/内容包）")
    ap.add_argument("--only",
                    help="只跑某一步：m0 | m1 | m1b | pkg | pkg:<设备id> | wip")
    ap.add_argument("--daily", action="store_true",
                    help="最小回归集：m0 + m1b + pkg")
    ap.add_argument("--cache", nargs="?", metavar="PATH",
                    const=os.path.join(REPO, "docs", "verify_last.json"),
                    help="跑完把 {时间, 各步 result, 失败项清单} 写 PATH"
                         "（缺省 docs/verify_last.json）")
    ap.add_argument("--no-ref-hard", action="store_true",
                    help="catalog_ref 失败时降级为告警不计入判定"
                         "（TASK-81A 临时开关，他线修复后转回硬判）")
    args = ap.parse_args(argv)

    step_defs: list[tuple[str, list[str]]] = [
        ("m0", ["scripts/m0_check.py"]),
        ("m1", ["scripts/m1_check.py"]),
        ("m1b", ["scripts/m1b_check.py"]),
    ]
    slot_step = ("slots", ["scripts/slot_consistency_check.py"])
    catalog_step = ("catalog", ["scripts/catalog_ingest.py", "--gate", "--gate-verify"])
    # TASK-81A：目录↔内容包引用一致性（02 线 catalog_ref_check 挂入门禁）
    if os.environ.get("DCM_FORCE_MIRROR") == "1" or not os.path.isdir(r"D:\work"):
        # TASK-96B：镜像模式经 01 侧适配器运行（不改 02 线文件）
        catalog_ref_step = ("catalog_ref", ["scripts/catalog_ref_ci.py"])
    else:
        catalog_ref_step = ("catalog_ref",
                            [r"D:\work\02\repo\tools\validate\catalog_ref_check.py"])
    gd_step = ("gd", ["scripts/gd_symbol_check.py"])
    # TASK-118：命名纪律静态门禁，与 gd_symbol_check 并列（v0.6.3 附录 A）
    gd_naming_step = ("gd_naming", ["scripts/gd_naming_check.py"])
    pkg_defs = [("pkg:%s" % pid, [VALIDATOR, path]) for pid, path in PKGS]
    wip_defs = [("wip:%s" % pid, [VALIDATOR, path]) for pid, path in WIP]

    for pid, _ in WIP:
        print("[提示] WIP 包 %s：生产中，不计入失败判定" % pid)

    if args.only == "wip":
        selected = wip_defs
    elif args.only == "slots":
        selected = [slot_step]
    elif args.only == "catalog":
        selected = [catalog_step]
    elif args.only == "gd":
        selected = [gd_step]
    elif args.only and args.only.startswith("pkg:"):
        pid = args.only[4:]
        selected = [d for d in pkg_defs if d[0] == "pkg:%s" % pid]
        if not selected:
            print("未知设备 id：%s（完工 %d 包）" % (pid, len(PKGS)))
            return 2
    elif args.only == "pkg":
        selected = pkg_defs
    elif args.only:
        if args.only not in ("m0", "m1", "m1b", "slots", "catalog", "catalog_ref",
                             "gd"):
            print("--only 取值非法：%s（m0|m1|m1b|pkg|pkg:<id>|slots|catalog|catalog_ref|gd|wip）"
                  % args.only)
            return 2
        selected = ([d for d in step_defs if d[0] == args.only]
                    or [s for s in (slot_step, catalog_step, catalog_ref_step,
                                    gd_step) if s[0] == args.only])
    elif args.daily:
        selected = [step_defs[0], step_defs[2], slot_step, catalog_step,
                    catalog_ref_step, gd_step, gd_naming_step] + pkg_defs
    else:
        selected = step_defs + [slot_step, catalog_step, catalog_ref_step,
                                gd_step, gd_naming_step] + pkg_defs

    results: list[tuple[str, bool, str]] = []
    for name, argv_ in selected:
        ok, note = run_step(name, argv_)
        results.append((name, ok, note))
    if args.no_ref_hard:
        downgraded = [n for n, ok, _ in results
                      if n == "catalog_ref" and not ok]
        if downgraded:
            print("!! 注意：catalog_ref 失败已按 --no-ref-hard 降级为告警"
                  "（不计入判定）")
        results = apply_ref_downgrade(results, args.no_ref_hard)

    print("\n===== 验收汇总（%d 项） =====" % len(results))
    failed = 0
    for name, ok, note in results:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print("  %-20s %s  %s" % (name, mark, note))
    print("结果：%d/%d 通过" % (len(results) - failed, len(results)))

    if args.cache:   # TASK-71A：验收结果缓存 → docs/verify_last.json
        payload = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(results),
            "passed": len(results) - failed,
            "steps": [{"name": n, "ok": ok, "note": nt} for n, ok, nt in results],
            "failed": [{"name": n, "note": nt} for n, ok, nt in results
                       if not ok],
        }
        cache_dir = os.path.dirname(args.cache)
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
        with open(args.cache, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print("验收缓存已写 %s" % args.cache)
        # TASK-76B：趋势历史双写（追加失败不影响退出码判定）
        hist_path = os.path.join(REPO, "docs", "verify_history.jsonl")
        try:
            with open(hist_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"time": payload["time"],
                                     "total": payload["total"],
                                     "passed": payload["passed"]},
                                    ensure_ascii=False) + "\n")
        except OSError as exc:
            print("验收历史写入失败（不影响结果判定）: %s" % exc)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())