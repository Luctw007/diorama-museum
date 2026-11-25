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
  R5（信息 a~e + 硬 f） F 系列封版扩展断言（TASK-306-A~E，母本 F16封版扩展口径设计_v1）：
    R5-a 销账状态登记 / R5-b 排期状态登记 / R5-c 待实机条数一致 / R5-d 封版文档齐备 /
    R5-e 「已通过」残留扫描（恒信息） / R5-f 扩展自守（硬）。R5_HARD=False 时 a~e 只打印不计 rc。
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
import re
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
# TASK-196-B：第二批 SIMH 槽位（预留态 run_status=missing 合法；转正后按三台口径断言）
SECOND_BATCH_SLOTS = ("simh-hp2100", "simh-nova", "simh-altair-8800")
LICENSES = ("licenses/MAME.md", "licenses/SIMH.md", "licenses/Stella.md")
MIN_READY = 30
SCAN_GLOBS = ("gw/**/*.py", "scripts/**/*.py", "godot/scripts/**/*.gd")
SCAN_PATTERNS = ("TODO", "FIXME", "XXX", "预留", "占位")

# TASK-306-A~E：R5 扩展断言（母本 F16封版扩展口径设计_v1 §①）。
# R5_HARD=False 时 R5-a~e 只打印 [INFO] 不计 rc；F-1~F-15 收口后置 True（设计卡 §② 四项转硬前提）。
R5_HARD = False
R5_DOCS = os.path.join(REPO, "docs")
R5_STATUS_OK = ("销账", "未销账", "方案销账", "销账+深化")
R5A_ITEMS = tuple("F-%d" % i for i in range(1, 7))          # §① 销账行 F-1~F-6
R5B_ITEMS = tuple("F-%d" % i for i in range(7, 17))         # §② 排期行 F-7~F-16
# R5-e 扫描对象：待实机汇总卡（最新版）+ 七张执行卡/核对卡/验收单（301-M/N/O/P/A/B + 241-B）。
R5_E_EXEC_FILES = (
    "docs/F11F12F15共轮实测执行卡_v1.md",
    "docs/F14六项实机执行卡_v1.md",
    "docs/F8F13真跑二进制前置核对_v1.md",
    "docs/F9F10口播导览实机核对卡_v1.md",
    "docs/B4实测口径01线对齐核对_v1.md",
    "docs/B04回写预案_v1.md",
    "docs/F1F2实机验收单_v1.md",
)
# R5-e 占位文案白名单：「已通过静态验收」类表述放行（静态验收 ≠ 实机验证，防误报臆造）。
R5_E_WHITELIST = ("静态",)

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


def run_status_of(entry: dict) -> str:
    """TASK-191-A（D-2）：run_status 判定（01 线门禁主权）——
    live=二进制就位；dry-run=有后端模块但二进制缺失（决策链优雅失败可干跑）；
    missing=无后端模块（预留）。"""
    if not entry.get("module"):
        return "missing"
    return "live" if entry.get("binary_path") else "dry-run"


def check_r2() -> None:
    # D-2 落地（TASK-191-A）+ 第二批 SIMH 扩展（TASK-196-B）：run_status 并入 R2 断言。
    # 01 线裁定：真跑阈值维持 ≥3（三台真跑），随真跑台数实测后按 66 号上调（≥5），
    # 当前 run_status 合法集合 = {live, dry-run}（三台真跑槽位 missing 判 FAIL）。
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
        st = run_status_of(entry)
        mark(st in ("live", "dry-run"), "R2",
             "槽位 %s run_status=%s（live/dry-run 合法；missing 判 FAIL）" % (sid, st))
    # TASK-196-B：第二批 SIMH 槽位——预留态（module 空）run_status=missing 判合法不 FAIL；
    # 转正且模块就绪态要求 run_status ∈ {live, dry-run}（缺二进制=可干跑）。
    for sid in SECOND_BATCH_SLOTS:
        entry = table.get(sid) or {}
        if not entry:
            mark(True, "R2", "第二批槽位 %s 未登记（本轮按预留口径放行，见 196-B）" % sid)
            continue
        if not entry.get("module"):
            mark(True, "R2", "第二批槽位 %s run_status=missing（预留合法，不 FAIL）" % sid)
            continue
        st = run_status_of(entry)
        mark(st in ("live", "dry-run"), "R2",
             "第二批槽位 %s 已转正，run_status=%s（live/dry-run 合法）" % (sid, st))
    for lic in LICENSES:
        mark(os.path.isfile(os.path.join(REPO, lic)), "R2", "许可记录存在 %s" % lic)


def check_r3() -> None:
    ready, wip = pkg_registry.discover_packages_full()
    print("[INFO] R3 wip 清单（不计入 rc）：%s"
          % (", ".join(str(x[0]) for x in wip) if wip else "（无）"))
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


def _latest_doc(prefix: str) -> str:
    """docs 目录内按文件名前缀取最新版路径（同名排序取末位）；无匹配回退 prefix 直名。"""
    if not os.path.isdir(R5_DOCS):
        return os.path.join(R5_DOCS, prefix)
    cands = sorted(f for f in os.listdir(R5_DOCS)
                   if f.startswith(prefix) and f.endswith(".md"))
    return os.path.join(R5_DOCS, cands[-1]) if cands else os.path.join(R5_DOCS, prefix)


def _ledger_section_rows(ledger: str, section: str) -> list[str]:
    """取台账指定章节（## 数字开头）内的表格行（| 开头）。"""
    with open(ledger, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    rows: list[str] = []
    in_sec = False
    for ln in lines:
        if ln.startswith("## "):
            in_sec = ln[3:].startswith(section)
            continue
        if in_sec and ln.strip().startswith("|"):
            rows.append(ln)
    return rows


def _strip_md(s: str) -> str:
    """去表格单元格加粗星号与空白。"""
    return s.strip().strip("*").strip()


def _r5_report(tag: str, ok: bool, text: str) -> None:
    """R5 统一出口：R5_HARD=False 时 a~e 只打印 [INFO] 不计 rc；True 时走 mark() 判硬。"""
    if not R5_HARD:
        print("[INFO] %s %s（信息级，R5_HARD=False 不计 rc）" % (tag, text))
    else:
        mark(ok, tag, text)


def check_r5a() -> None:
    """R5-a 销账状态登记校验：台账 §① F-1~F-6 每行状态∈合法集合且产物（轮次）非空。"""
    ledger = _latest_doc("全馆功能排期台账")
    rows = _ledger_section_rows(ledger, "①")
    bad: list[tuple] = []
    checked = 0
    for ln in rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells or not cells[0].startswith("F-"):
            continue
        item = _strip_md(cells[0])
        if item not in R5A_ITEMS:
            continue
        status = _strip_md(cells[1]) if len(cells) > 1 else ""
        product = cells[2].strip() if len(cells) > 2 else ""
        checked += 1
        # 状态字段去全部空白后与合法集合比对（兼容台账「销账 + 深化」带空格写法）
        if "".join(status.split()) not in R5_STATUS_OK or not product:
            bad.append((item, status, product))
    detail = ("；异常行 " + "; ".join("%s(状态=%r, 产物空=%s)" % (i, s, not p)
                                     for i, s, p in bad)) if bad else ""
    _r5_report("R5-a", not bad,
               "台账 %s §① F-1~F-6 销账登记 %d/%d 行状态+产物成文%s"
               % (os.path.basename(ledger), checked - len(bad), checked, detail))


def check_r5b() -> None:
    """R5-b 排期状态登记校验：台账 §② F-7~F-16 状态/责任线与验收口径（待实机条数）非空，
    且 §④ F-13/F-14 阻塞点成文。"""
    ledger = _latest_doc("全馆功能排期台账")
    rows = _ledger_section_rows(ledger, "②")
    bad: list[tuple] = []
    checked = 0
    for ln in rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells or not cells[0].startswith("F-"):
            continue
        item = _strip_md(cells[0])
        if item not in R5B_ITEMS:
            continue
        resp = _strip_md(cells[1]) if len(cells) > 1 else ""
        acc = cells[5].strip() if len(cells) > 5 else ""
        checked += 1
        if not resp or not acc:
            bad.append((item, resp, acc))
    blocks: dict[str, str] = {}
    for ln in _ledger_section_rows(ledger, "④"):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells and cells[0].startswith("F-1"):
            blocks[_strip_md(cells[0])] = cells[2].strip() if len(cells) > 2 else ""
    missing_block = [k for k in ("F-13", "F-14") if not blocks.get(k)]
    detail = ""
    if bad:
        detail += "；异常行 " + "; ".join("%s(责任线空=%s, 验收口径空=%s)" % (i, not r, not a)
                                          for i, r, a in bad)
    if missing_block:
        detail += "；§④ 阻塞点缺失 " + ",".join(missing_block)
    _r5_report("R5-b", not bad and not missing_block,
               "台账 %s §② F-7~F-16 排期登记 %d/%d 行成文%s"
               % (os.path.basename(ledger), checked - len(bad), checked, detail))


def check_r5c() -> None:
    """R5-c 待实机条数一致性：汇总卡「合计」== 各母本行条数加和。"""
    summary = _latest_doc("F系列待实机清单汇总")
    with open(summary, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    total_expected = None
    per_item: list[int] = []
    for ln in lines:
        s = ln.strip()
        if (s.startswith("- 合计") or s.startswith("合计")) and "项/格" in s:
            m = re.search(r"\d+", s)
            if m:
                total_expected = int(m.group(0))
        elif s.startswith("| F-"):
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if len(cells) > 1:
                m = re.search(r"\d+", cells[1])
                if m:
                    per_item.append(int(m.group(0)))
    item_sum = sum(per_item)
    ok = total_expected is not None and item_sum == total_expected
    _r5_report("R5-c", ok,
               "汇总卡 %s 合计 %s vs 母本 %d 行加和 %d 一致"
               % (os.path.basename(summary),
                  str(total_expected) if total_expected is not None else "缺失",
                  len(per_item), item_sum))


def check_r5d() -> None:
    """R5-d 封版文档齐备性：七类必查文件（301-G 清单）+ 三份许可记录存在性。"""
    required = [
        os.path.join(R5_DOCS, "README.md"),
        os.path.join(R5_DOCS, "RELEASE-v0.1.md"),
        _latest_doc("全馆功能排期台账"),
        _latest_doc("F系列待实机清单汇总"),
        os.path.join(R5_DOCS, "F1F2实机验收单_v1.md"),
        os.path.join(R5_DOCS, "godot_first_boot.md"),
    ] + [os.path.join(REPO, lic) for lic in LICENSES]
    missing = [p for p in required if not os.path.isfile(p)]
    _r5_report("R5-d", not missing,
               "封版文档齐备性 %d/%d 文件在案%s"
               % (len(required) - len(missing), len(required),
                  ("；缺失 " + ", ".join(os.path.relpath(p, REPO) for p in missing))
                  if missing else ""))


def check_r5e() -> None:
    """R5-e 待实机项「已通过/已验证」残留扫描：只暴露、恒不计 rc（占位文案白名单除外）。"""
    files = [_latest_doc("F系列待实机清单汇总")] + [
        os.path.join(REPO, rel) for rel in R5_E_EXEC_FILES]
    hits: list[str] = []
    for full in files:
        rel = os.path.relpath(full, REPO)
        if not os.path.isfile(full):
            hits.append("%s（文件缺失）" % rel)
            continue
        with open(full, encoding="utf-8") as fh:
            for ln in fh:
                if ("已通过" in ln or "已验证" in ln) and not any(w in ln for w in R5_E_WHITELIST):
                    hits.append("%s: %s" % (rel, ln.strip()[:80]))
    print("[INFO] R5-e 残留扫描 %d 文件：命中 %d 处%s（恒不计 rc）"
          % (len(files), len(hits), (" | ".join(hits)) if hits else "（无臆造残留）"))


def check_r5f() -> None:
    """R5-f 扩展自守（判硬）：R1~R5 全硬断言 FAIL 0。"""
    mark(fails == 0, "R5-f", "扩展自守：R1~R5 全硬断言 FAIL %d 处" % fails)


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
    check_r5a()
    check_r5b()
    check_r5c()
    check_r5d()
    check_r5e()
    check_r5f()
    if args.smoke:
        run_smoke()
    if args.snapshot:
        run_snapshot()
    print("汇总：硬断言 FAIL %d 处 → rc=%d" % (fails, 1 if fails else 0))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())