# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""v0.1 发布自检门禁（TASK-166-A）：封版前工程侧可重复运行的机器断言。

断言与基线：
  R1（硬）  docs/verify_last.json 存在且 passed == total（先跑 verify_all --daily --cache）
  R2（硬）  三台真跑槽位 mame-apple2/simh-pdp8/stella 均存在且 module 非空（非「预留」），
            licenses/MAME.md、SIMH.md、Stella.md 三份许可记录均存在
  R3（硬）  完工内容包 ≥ 30（复用 pkg_registry.discover_packages_full；wip 仅打印）
  R4（信息） 源码残留扫描（TODO|FIXME|XXX|预留|占位），只暴露、不计入 rc
  --smoke   现场冒烟：demo_frames.py --frames 5 --html（失败计入 rc）
  --snapshot 冻结基线：verify_last.json → verify_baseline_v0.1.json

版本单一落点：PROJECT_RELEASE_VERSION（项目封版版本）。网关自身版本
gw.__version__（0.2.0）与 PROTOCOL_VERSION（2）只读引用、不修改。

用法：
  python 01/scripts/release_check.py             # R1-R4 + 汇总（rc 0/1）
  python 01/scripts/release_check.py --smoke     # 另加演示帧冒烟
  python 01/scripts/release_check.py --snapshot  # 冻结验收基线快照
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

PROJECT_RELEASE_VERSION = "0.1.0"
VERIFY_LAST = os.path.join(REPO, "docs", "verify_last.json")
BASELINE = os.path.join(REPO, "docs", "verify_baseline_v0.1.json")

from gw import __version__ as GW_VERSION, PROTOCOL_VERSION  # noqa: E402  只读引用
import pkg_registry  # noqa: E402
import slot_loader   # noqa: E402

REQUIRED_SLOTS = ("mame-apple2", "simh-pdp8", "stella")
LICENSES = ("licenses/MAME.md", "licenses/SIMH.md", "licenses/Stella.md")
MIN_READY = 30
SCAN_GLOBS = ("gw/**/*.py", "scripts/**/*.py", "godot/scripts/**/*.gd")
SCAN_PATTERNS = ("TODO", "FIXME", "XXX", "预留", "占位")

fails = 0


def mark(ok: bool, tag: str, text: str) -> None:
    global fails
    print("[%s] %s %s" % ("PASS" if ok else "FAIL", tag, text))
    if not ok:
        fails += 1


def check_r1() -> None:
    if not os.path.isfile(VERIFY_LAST):
        mark(False, "R1", "docs/verify_last.json 缺失——先跑 verify_all --daily --cache")
        return
    with open(VERIFY_LAST, encoding="utf-8") as fh:
        data = json.load(fh)
    total = int(data.get("total", 0))
    passed = int(data.get("passed", 0))
    mark(passed == total and total > 0,
         "R1", "验收基线 %d/%d 通过（%s）" % (passed, total, data.get("time", "")))


def check_r2() -> None:
    table = slot_loader.slots_available()
    for sid in REQUIRED_SLOTS:
        entry = table.get(sid) or {}
        if not entry.get("module"):
            mark(False, "R2", "槽位 %s module 为空（仍为预留）" % sid)
            continue
        if "预留" in str(entry.get("desc", "")):
            mark(False, "R2", "槽位 %s desc 仍含「预留」字样" % sid)
            continue
        mark(True, "R2", "槽位 %s 已登记后端 %s" % (sid, entry.get("module")))
    for lic in LICENSES:
        mark(os.path.isfile(os.path.join(REPO, lic)), "R2", "许可记录存在 %s" % lic)


def check_r3() -> None:
    ready, wip = pkg_registry.discover_packages_full()
    print("[INFO] R3 wip 清单（不计入 rc）：%s"
          % (", ".join(wip) if wip else "（无）"))
    mark(len(ready) >= MIN_READY,
         "R3", "完工包 %d ≥ %d" % (len(ready), MIN_READY))


def check_r4() -> None:
    """源码残留扫描：只暴露、不计入 rc。区分已知 [需核实] 骨架注记 vs 新发现。"""
    import fnmatch
    hits: list[str] = []
    for glob_pat in SCAN_GLOBS:
        for root, _dirs, files in os.walk(REPO):
            rel_root = os.path.relpath(root, REPO)
            for f in files:
                if f.endswith((".py", ".gd")) and fnmatch.fnmatch(
                        os.path.join(rel_root, f).replace("\\", "/"), glob_pat):
                    hits.append(os.path.join(rel_root, f))
    total = 0
    for path in sorted(set(hits)):
        full = os.path.join(REPO, path)
        try:
            with open(full, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        for pat in SCAN_PATTERNS:
            n = text.count(pat)
            if n:
                total += n
                print("[INFO] R4 %s: 「%s」×%d" % (path, pat, n))
    print("[INFO] R4 残留扫描完成：命中 %d 处（含骨架注记与新发现，只暴露不计 rc）" % total)


def run_smoke() -> None:
    cp = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "demo_frames.py"),
         "--frames", "5", "--html"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=300)
    tail = (cp.stdout or "").strip().splitlines()
    for ln in tail[-4:]:
        print("      " + ln[:140])
    mark(cp.returncode == 0, "SMOKE", "demo_frames --frames 5 --html rc=%d" % cp.returncode)


def run_snapshot() -> None:
    if not os.path.isfile(VERIFY_LAST):
        print("[FAIL] SNAP docs/verify_last.json 缺失，无法冻结")
        global fails
        fails += 1
        return
    shutil.copyfile(VERIFY_LAST, BASELINE)
    with open(BASELINE, encoding="utf-8") as fh:
        data = json.load(fh)
    print("[PASS] SNAP 基线已冻结：%s（time=%s passed=%d total=%d）"
          % (BASELINE, data.get("time"), data.get("passed"), data.get("total")))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="v0.1 发布自检门禁")
    ap.add_argument("--smoke", action="store_true", help="演示帧冒烟（失败计入 rc）")
    ap.add_argument("--snapshot", action="store_true", help="冻结验收基线快照")
    args = ap.parse_args(argv)

    print("项目封版版本 %s（网关版本 %s · 协议 v%d，只读引用）"
          % (PROJECT_RELEASE_VERSION, GW_VERSION, PROTOCOL_VERSION))
    if args.snapshot and not (args.smoke):
        run_snapshot()
        return 1 if fails else 0
    check_r1()
    check_r3()
    check_r2()
    check_r4()
    if args.smoke:
        run_smoke()
    if args.snapshot:
        run_snapshot()
    print("汇总：硬断言 FAIL %d 处 → rc=%d" % (fails, 1 if fails else 0))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())