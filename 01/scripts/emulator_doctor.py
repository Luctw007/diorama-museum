# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""模拟器环境体检向导（TASK-36A）。

体检项（OK/MISSING/HINT 三态）：
  MAME_BIN / third_party/mame    —— MAME apple2 真跑前提（licenses/MAME.md）
  SIMH_PDP8_BIN / third_party/simh —— SIMH PDP-8 真跑前提（licenses/SIMH.md）
  ROM 目录占位                    —— 只提示路径，永不下载（红线）
  网关自检                       —— 网关进程可起停（17338 专用端口）
  --fix-check                     —— 环境齐备时自动跑 m2a --mame + m0 冒烟，落盘日志

用法:
  python scripts/emulator_doctor.py
  python scripts/emulator_doctor.py --json
  python scripts/emulator_doctor.py --fix-check --log docs/doctor_log.txt
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE_PORT = 17338


def _port_free(port: int) -> bool:
    try:
        probe = socket.create_connection(("127.0.0.1", port), timeout=0.5)
        probe.close()
        return False
    except OSError:
        return True


def find_mame() -> tuple[str, str]:
    """(状态, 路径或提示)。状态 ∈ OK/MISSING。"""
    env = os.environ.get("MAME_BIN")
    if env and os.path.isfile(env):
        return "OK", env
    for name in ("mame", "mame.exe"):
        cand = os.path.join(REPO, "third_party", "mame", name)
        if os.path.isfile(cand):
            return "OK", cand
    return "MISSING", os.path.join("third_party", "mame", "mame(.exe)")


def find_simh() -> tuple[str, str]:
    env = os.environ.get("SIMH_PDP8_BIN")
    if env and os.path.isfile(env):
        return "OK", env
    for name in ("pdp8", "pdp8.exe"):
        cand = os.path.join(REPO, "third_party", "simh", name)
        if os.path.isfile(cand):
            return "OK", cand
    return "MISSING", os.path.join("third_party", "simh", "pdp8(.exe)")


def probe_version(binary: str) -> str:
    try:
        cp = subprocess.run([binary, "-version"], capture_output=True, text=True,
                            timeout=15, errors="replace")
        line = (cp.stdout or cp.stderr or "").strip().splitlines()
        return line[0][:90] if line else "（无输出）"
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "（探测失败: %s）" % exc


def gateway_self_test() -> tuple[str, str]:
    if not _port_free(PROBE_PORT):
        return "HINT", "端口 %d 被占用（可能有残留网关进程）" % PROBE_PORT
    gw = subprocess.Popen(
        [sys.executable, os.path.join(REPO, "gw", "gateway.py"),
         "--host", "127.0.0.1", "--port", str(PROBE_PORT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.time() + 8.0
        while time.time() < deadline:
            if gw.poll() is not None:
                return "FAIL", "网关提前退出（exit=%s）" % gw.returncode
            try:
                probe = socket.create_connection(("127.0.0.1", PROBE_PORT), timeout=0.5)
                probe.close()
                return "OK", "网关可正常起停（端口 %d）" % PROBE_PORT
            except OSError:
                time.sleep(0.2)
        return "FAIL", "网关 8s 未就绪"
    finally:
        if gw.poll() is None:
            gw.terminate()
            try:
                gw.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gw.kill()


def rom_hints() -> tuple[str, str]:
    hints = {
        "apple2": os.path.join("third_party", "roms", "apple2", "（用户自备）"),
        "simh": os.path.join("third_party", "roms", "simh", "（用户自备）"),
    }
    return "HINT", ("ROM 红线：仅提示位置、不自动下载：%s；%s（见 licenses/MAME.md、SIMH.md）"
                    % (hints["apple2"], hints["simh"]))


def run_checks() -> list[dict]:
    checks: list[dict] = []
    st, path = find_mame()
    ver = probe_version(path) if st == "OK" else ""
    checks.append(dict(item="mame_binary", status=st, detail=path, version=ver,
                       guide="安装 MAME 后放 %s 或设环境变量 MAME_BIN（licenses/MAME.md）"
                       % os.path.join("third_party", "mame")))
    st, path = find_simh()
    ver = probe_version(path) if st == "OK" else ""
    checks.append(dict(item="simh_binary", status=st, detail=path, version=ver,
                       guide="安装 SIMH 后放 %s 或设 SIMH_PDP8_BIN（licenses/SIMH.md）"
                       % os.path.join("third_party", "simh")))
    st, det = gateway_self_test()
    checks.append(dict(item="gateway_self_test", status=st, detail=det, version="",
                       guide="网关异常时检查 17338 端口残留进程："
                             "Get-NetTCPConnection -LocalPort 17338"))
    checks.append(dict(item="rom_location_hint", status="HINT",
                       detail=rom_hints()[1], version="",
                       guide="本工具永不下载 ROM；自备文件按提示路径放置"))
    # TASK-46A：槽位扫描区（slot_loader 可用才生效）
    try:
        import slot_loader
        table = slot_loader.slots_available()
        for slot_id, entry in sorted(table.items()):
            if entry["binary_path"]:
                ver = probe_version(entry["binary_path"])
                checks.append(dict(item="slot:%s" % slot_id, status="OK",
                                   detail=entry["binary_path"], version=ver,
                                   guide=("（后端模块预留）"
                                          if not entry.get("module") else "")))
            elif entry.get("binary_hint"):
                checks.append(dict(item="slot:%s" % slot_id, status="MISSING",
                                   detail=entry["binary_hint"] +
                                   ("（后端模块预留）"
                                    if not entry.get("module") else ""),
                                   version="",
                                   guide="把二进制放入 %s 或设环境变量 %s"
                                   % (entry["binary_hint"],
                                      entry.get("binary_env") or "?")))
            else:
                checks.append(dict(item="slot:%s" % slot_id, status="OK",
                                   detail="native 后端，无二进制要求", version="",
                                   guide=""))
        media = slot_loader.media_dirs()
        checks.append(dict(item="slot_media_dirs", status="HINT",
                           detail=("介质目录 %d 个" % len(media)), version="",
                           guide="slots/media/<类目>/<设备类>/<槽位>/ 自备放置（永不下载）"))
    except ImportError:
        checks.append(dict(item="slot_loader", status="FAIL",
                           detail="slot_loader 不可用", version="",
                           guide="检查 scripts/slot_loader.py 是否缺失"))
    return checks


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="模拟器环境体检向导")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fix-check", action="store_true",
                    help="环境齐备（无 MISSING 二进制项）时自动冒烟：m2a --mame + m0")
    ap.add_argument("--log", default=os.path.join(REPO, "docs",
                                                  "doctor_log_%s.txt"
                                                  % time.strftime("%Y%m%d_%H%M%S")))
    args = ap.parse_args(argv)
    checks = run_checks()

    if args.json:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    else:
        for c in checks:
            extra = (" ver=%s" % c["version"]) if c.get("version") else ""
            print("[%s] %-18s %s%s" % (c["status"], c["item"], c["detail"], extra))
            if c["status"] in ("MISSING", "FAIL"):
                print("      >>> " + c["guide"])
        missing = [c for c in checks if c["status"] in ("MISSING", "FAIL")]
        print("汇总：%d 项，%d 项阻断（MISSING/FAIL）" % (len(checks), len(missing)))

    if args.fix_check:
        blockers = [c for c in checks if c["status"] in ("MISSING", "FAIL")
                    and c["item"] != "gateway_self_test"]
        if blockers:
            if not args.json:
                print("fix-check 不执行：二进制环境未齐备（%s）"
                      % ", ".join(c["item"] for c in blockers))
            return 1
        steps = [["m2a_check.py", "--mame"], ["m0_check.py"]]
        lines: list[str] = []
        ok_all = True
        for step in steps:
            cp = subprocess.run(
                [sys.executable, os.path.join(REPO, "scripts", step[0])] + step[1:],
                cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=600)
            lines.append("=== %s %s (rc=%d) ===" % (step[0], " ".join(step[1:]),
                                                    cp.returncode))
            lines.append(cp.stdout[-2000:] if cp.stdout else "")
            ok_all = ok_all and cp.returncode == 0
        with open(args.log, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        if not args.json:
            print("冒烟日志已写 %s（结果 %s）" % (args.log,
                                                  "全绿" if ok_all else "有失败"))
        return 0 if ok_all else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())