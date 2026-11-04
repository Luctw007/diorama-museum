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
槽位与介质校验器反例测试（TASK-47B）

用法：
    python run_slot_tests.py

在临时目录构建最小槽位树（slots/emulators/<id>/manifest.json + 可选 media/），施加单一破坏后
运行 slot_check.py，断言命中预期规则编号与级别。覆盖 SV-01~05 全部规则的违规路径 + 1 正例。

反例清单：
    01 缺 manifest → SV-01 FAIL
    02 枚举非法（device_class）→ SV-02 FAIL
    03 二进制缺失 → SV-03 FAIL
    04 介质扩展名错 → SV-03 FAIL
    05 三件套缺（license 对象缺 url/date）→ SV-04 FAIL
    06 哈希行坏 → SV-05 FAIL
    07 正例（fake-slot 全合法）→ 无 FAIL（exit 0）
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SLOT_CHECK = os.path.abspath(os.path.join(TESTS_DIR, "..", "slot_check.py"))

PASSED = 0
FAILED = 0


def run_slot_check(slots_root: str):
    proc = subprocess.run(
        [sys.executable, SLOT_CHECK, slots_root],
        capture_output=True, text=True, encoding="utf-8",
    )
    return proc.returncode, proc.stdout + proc.stderr


def report(name: str, ok: bool, detail: str = ""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
        print(f"[PASS] {name}" + (f"  — {detail}" if detail else ""))
    else:
        FAILED += 1
        print(f"[FAIL] {name}" + (f"  — {detail}" if detail else ""))


def base_manifest() -> dict:
    return {
        "slot_id": "test-slot",
        "device_class": "computer",
        "backend_type": "native",
        "description": "测试槽位",
        "license": "MIT（本仓库自带）",
    }


def build_slots(tmp: str, manifest, media_files=None, hash_text=None) -> str:
    """构建最小槽位树，返回 slots/ 根路径。manifest=None 表示不写 manifest.json。"""
    slots = os.path.join(tmp, "slots")
    emu = os.path.join(slots, "emulators", "test-slot")
    os.makedirs(emu, exist_ok=True)
    if manifest is not None:
        with open(os.path.join(emu, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    if media_files:
        for rel, content in media_files:
            fp = os.path.join(slots, "media", rel)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, "wb") as f:
                f.write(content)
    if hash_text is not None:
        fp = os.path.join(slots, "media", hash_text[0])
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(hash_text[1])
    return slots


def expect(name: str, manifest, rule: str, level: str,
           media_files=None, hash_text=None):
    tmp = tempfile.mkdtemp(prefix="hako_slot_")
    slots = build_slots(tmp, manifest, media_files=media_files, hash_text=hash_text)
    code, out = run_slot_check(slots)
    ok = any((rule in ln) and (level in ln) for ln in out.splitlines())
    report(name, ok, f"exit={code}, 命中 {rule} {level}" if ok else f"exit={code}, 未命中 {rule} {level}")
    if not ok:
        for ln in out.splitlines():
            if ln.strip().startswith(("PASS", "WARN", "FAIL")):
                print("      " + ln.strip())
    shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    print("=" * 70)
    print("TASK-47B 槽位与介质校验器反例测试（slot_check.py）")
    print("=" * 70)

    # 反例01：缺 manifest
    expect("反例01：缺 manifest → SV-01 FAIL", None, "SV-01", "FAIL")

    # 反例02：枚举非法（device_class）
    m = base_manifest()
    m["device_class"] = "game-console"
    expect("反例02：枚举非法（device_class）→ SV-02 FAIL", m, "SV-02", "FAIL")

    # 反例03：二进制缺失（声明 binary 但无文件）
    m = base_manifest()
    m["binary"] = "mame"
    expect("反例03：二进制缺失 → SV-03 FAIL", m, "SV-03", "FAIL")

    # 反例04：介质扩展名错（.xyz 放 cartridge）
    m = base_manifest()
    expect("反例04：介质扩展名错 → SV-03 FAIL", m, "SV-03", "FAIL",
           media_files=[("cartridge/console/test-slot/game.xyz", b"x")])

    # 反例05：三件套缺（license 对象缺 url/date）
    m = base_manifest()
    m["license"] = {"tier": "mit"}
    expect("反例05：三件套缺（license 对象）→ SV-04 FAIL", m, "SV-04", "FAIL")

    # 反例06：哈希行坏
    m = base_manifest()
    expect("反例06：哈希行坏 → SV-05 FAIL", m, "SV-05", "FAIL",
           media_files=[("cartridge/console/test-slot/game.nes", b"x")],
           hash_text=("cartridge/console/test-slot/SHA256SUMS", "not-a-hash\n"))

    # 正例07：全合法 → 无 FAIL（exit 0）
    tmp = tempfile.mkdtemp(prefix="hako_slot_ok_")
    m = base_manifest()
    m["license"] = {"tier": "mit", "url": "https://opensource.org/licenses/MIT", "date": "2026-11-04"}
    slots = build_slots(tmp, m,
                        media_files=[("cartridge/console/test-slot/game.nes", b"x")])
    code, out = run_slot_check(slots)
    ok = (code == 0) and ("FAIL 0" in out)
    report("正例07：全合法（三件套对象 + 介质）→ 无 FAIL", ok, f"exit={code}")
    if not ok:
        for ln in out.splitlines():
            if ln.strip().startswith(("PASS", "WARN", "FAIL")):
                print("      " + ln.strip())
    shutil.rmtree(tmp, ignore_errors=True)

    print("-" * 70)
    print(f"结果：PASS {PASSED}，FAIL {FAILED}")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
