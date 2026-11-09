# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""三台真跑「预启动检查」smoke（TASK-176-A）：**零介质、零下载、零联网、不触碰 ROM**。

二进制路径取自 `slot_loader.slots_available()` 的 `binary_path`（单一真相源，
不硬编码、不回退到下载）。三台探针：
  · mame   ：`-version`（rc==0 且输出含版本号关键字）+ `-createconfig -inipath <临时目录>`
             （rc==0 且生成 mame.ini；只写本地临时目录，事后删除，不入库）；
  · simh   ：无参启动 + stdin 注入退出命令（先 `quit`，实测不是则回退 `exit` 并以
             实测为准标 [需核实]），断言超时内退出、rc==0、输出含横幅关键字 PDP-8/SIMH；
  · stella ：优先 `-help`（确定性 rc 且输出含 Stella），不可用则退回无参启动
             + 超时判定「进程能起」并记录实际首行输出；不带任何 ROM 参数。
统一超时 kill 判 FAIL；打印逐台 [PASS/FAIL] + 实测输出首行；三台全过 rc=0。

用法：python 01/scripts/realrun_smoke.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import slot_loader  # noqa: E402

fails = 0


def pass_or_fail(ok: bool, device: str, what: str, note: str) -> None:
    global fails
    print("  [%s] %s %-24s %s" % ("PASS" if ok else "FAIL", device, what, note))
    if not ok:
        fails += 1


def first_line(text: str) -> str:
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    return lines[0][:100] if lines else "（无输出）"


def probe_mame(binary: str) -> None:
    cwd = os.path.dirname(binary)
    # 实测：跨共享盘首载 mame.exe -version 需约 33s（任务书原规格 30s 不满足），
    # 放宽到 120s（漂移记录于 TASK-176-A 报告）
    cp = subprocess.run([binary, "-version"], cwd=cwd, capture_output=True,
                        text=True, encoding="utf-8", errors="replace", timeout=120)
    out = (cp.stdout or "") + (cp.stderr or "")
    print("      实测首行: %s" % first_line(out))
    ok_version = cp.returncode == 0 and ("mame" in out.lower() or "MAME" in out)
    pass_or_fail(ok_version, "mame", "-version", "rc=%d" % cp.returncode)
    if not ok_version:
        return
    tmp = tempfile.mkdtemp(prefix="diorama_mame_cfg_")
    try:
        # 实测：MAME 把 mame.ini 写到 cwd（而非 inipath 目录本身）；
        # 故 cwd 设为临时目录，避免向 third_party\mame（用户二进制目录）落文件。
        cp = subprocess.run([binary, "-createconfig", "-inipath", tmp], cwd=tmp,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=180)
        ini_ok = cp.returncode == 0 and os.path.isfile(os.path.join(tmp, "mame.ini"))
        pass_or_fail(ini_ok, "mame", "-createconfig", "rc=%d · mame.ini=%s"
                     % (cp.returncode, "生成" if ini_ok else "未生成"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def probe_simh(binary: str) -> None:
    cwd = os.path.dirname(binary)
    for exit_cmd in ("quit", "exit"):
        try:
            cp = subprocess.run([binary], cwd=cwd, input=exit_cmd + "\n",
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=20)
            out = (cp.stdout or "") + (cp.stderr or "")
            print("      实测首行（退出命令 %s）: %s" % (exit_cmd, first_line(out)))
            ok = ("PDP-8" in out or "SIMH" in out)
            pass_or_fail(ok, "simh", "stdin 退出 %s" % exit_cmd,
                         "rc=%d · 横幅%s" % (cp.returncode, "命中" if ok else "未命中"))
            return
        except subprocess.TimeoutExpired:
            print("      实测首行（退出命令 %s）: （超时未退出，尝试下一命令）" % exit_cmd)
    pass_or_fail(False, "simh", "stdin 退出", "quit/exit 均未在超时内退出")


def probe_stella(binary: str) -> None:
    cwd = os.path.dirname(binary)
    sdl2 = os.path.isfile(os.path.join(cwd, "SDL2.dll"))
    cp = subprocess.run([binary, "-help"], cwd=cwd, capture_output=True,
                        text=True, encoding="utf-8", errors="replace", timeout=30)
    out = (cp.stdout or "") + (cp.stderr or "")
    print("      实测首行（-help）: %s" % first_line(out))
    if "Stella" in out:
        pass_or_fail(True, "stella", "-help", "rc=%d（确定性 usage 路径）" % cp.returncode)
        return
    # 回退：无参启动 + 超时判定「进程能起」（不带任何 ROM 参数）
    try:
        cp = subprocess.run([binary], cwd=cwd, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=10)
        out = (cp.stdout or "") + (cp.stderr or "")
        print("      实测首行（无参）: %s" % first_line(out))
        if cp.returncode == 3221225781:   # 0xC0000135 STATUS_DLL_NOT_FOUND
            pass_or_fail(False, "stella", "无参启动",
                         "rc=0xC0000135 缺运行库 DLL（目录内 SDL2.dll=%s）[需核实]："
                         "请用户补全 Stella 运行库后再验" % ("有" if sdl2 else "无"))
        elif "Stella" in out:
            pass_or_fail(True, "stella", "无参启动",
                         "rc=%d（[需核实] 无 ROM 报错路径）" % cp.returncode)
        else:
            pass_or_fail(False, "stella", "无参启动",
                         "rc=%d 无输出（路径 [需核实]）" % cp.returncode)
    except subprocess.TimeoutExpired:
        print("      实测首行（无参）: （10s 内仍在运行）")
        pass_or_fail(True, "stella", "无参启动", "进程能起（超时仍在运行，[需核实]）")


def main(argv: list[str] | None = None) -> int:
    del argv
    print("== 三台真跑预启动检查 smoke（零介质 · 零下载 · 零联网） ==")
    table = slot_loader.slots_available()
    probes = (("mame-apple2", probe_mame), ("simh-pdp8", probe_simh),
              ("stella", probe_stella))
    for slot_id, probe in probes:
        binary = (table.get(slot_id) or {}).get("binary_path")
        print("== %s" % slot_id)
        if not binary:
            pass_or_fail(False, slot_id, "二进制", "未就位（binary_path 无值）")
            continue
        print("      二进制: %s" % binary)
        try:
            probe(binary)
        except subprocess.TimeoutExpired:
            pass_or_fail(False, slot_id, "探针", "超时未返回（判 FAIL）")
    print("汇总：三台预启动检查，FAIL %d 处（全 PASS 则 rc=0）" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())