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
音频规则校验器反例测试（TASK-42A）

用法：
    python run_audio_tests.py

在临时目录构建最小音频内容包（meta.json + audio/ 三层 + 可选 THIRD_PARTY.md/SYNTH.md），
施加单一破坏后运行 audio_check.py，断言命中预期规则编号与级别（PASS/WARN/FAIL）。
覆盖 A-01~A-04 全部规则的违规路径 + 一条全合法正例。

反例清单：
    01 命名非法（大写/非法字符）→ A-01 FAIL
    02 采样率错（44.1k）→ A-02 WARN
    03 时长超限（sfx 31s > 30s）→ A-03 WARN
    04 三件套缺（有音频无 THIRD_PARTY）→ A-04 FAIL
    05 位深非法（8bit）→ A-02 WARN
    06 层级错放（sfx 文件在 bgm 目录）→ A-01 FAIL
    07 正例（全合法，三件套齐备）→ 无 FAIL（exit 0）
"""
from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_CHECK = os.path.abspath(os.path.join(TESTS_DIR, "..", "audio_check.py"))

PASSED = 0
FAILED = 0


def run_audio_check(pkg: str):
    proc = subprocess.run(
        [sys.executable, AUDIO_CHECK, pkg],
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


def make_wav(path: str, sample_rate: int = 48000, bits: int = 16,
             channels: int = 1, duration_sec: float = 1.0):
    """写一个最小合法 PCM WAV（RIFF/fmt/data，数据区全 0）。"""
    num_samples = int(sample_rate * duration_sec)
    block_align = channels * (bits // 8)
    byte_rate = sample_rate * block_align
    data_size = num_samples * block_align
    header = (
        b"RIFF" + struct.pack("<I", 36 + data_size) + b"WAVE" +
        b"fmt " + struct.pack("<I", 16) +
        struct.pack("<HHIIHH", 1, channels, sample_rate, byte_rate, block_align, bits) +
        b"data" + struct.pack("<I", data_size)
    )
    with open(path, "wb") as f:
        f.write(header + b"\x00" * data_size)


def build_pkg(tmp: str, files: list[tuple[str, bytes]], third_party: str | None = None,
              synth: str | None = None) -> str:
    """构建最小音频包：meta.json + audio/ 三层 + 指定文件 + 可选登记文件。"""
    pkg = os.path.join(tmp, "test-device")
    os.makedirs(pkg, exist_ok=True)
    with open(os.path.join(pkg, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"id": "test-device", "name": {"zh": "测试设备"}}}, f,
                  ensure_ascii=False)
    for rel, content in files:
        fp = os.path.join(pkg, rel)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "wb") as f:
            f.write(content)
    if third_party is not None:
        with open(os.path.join(pkg, "THIRD_PARTY.md"), "w", encoding="utf-8") as f:
            f.write(third_party)
    if synth is not None:
        with open(os.path.join(pkg, "audio", "SYNTH.md"), "w", encoding="utf-8") as f:
            f.write(synth)
    return pkg


def _wav(**kw) -> bytes:
    """在内存生成 WAV 并返回字节（便于写文件）。"""
    # 直接用 make_wav 写临时文件再读回，避免重复实现
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        make_wav(tf.name, **kw)
        path = tf.name
    with open(path, "rb") as f:
        data = f.read()
    os.unlink(path)
    return data


def expect(name: str, files, rule: str, level: str,
           third_party: str | None = None, synth: str | None = None):
    tmp = tempfile.mkdtemp(prefix="hako_audio_")
    pkg = build_pkg(tmp, files, third_party=third_party, synth=synth)
    code, out = run_audio_check(pkg)
    ok = any((rule in ln) and (level in ln) for ln in out.splitlines())
    report(name, ok, f"exit={code}, 命中 {rule} {level}" if ok else f"exit={code}, 未命中 {rule} {level}")
    if not ok:
        for ln in out.splitlines():
            if ln.strip().startswith(("PASS", "WARN", "FAIL")):
                print("      " + ln.strip())
    shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    print("=" * 70)
    print("TASK-42A 音频规则校验器反例测试（audio_check.py）")
    print("=" * 70)

    # 反例01：命名非法（大写字母）
    expect(
        "反例01：命名非法（大写）→ A-01 FAIL",
        [("audio/sfx/Power_On.ogg", b"OggS")],
        "A-01", "FAIL",
    )

    # 反例02：采样率错（44.1kHz）
    expect(
        "反例02：采样率错（44.1kHz）→ A-02 WARN",
        [("audio/sfx/sfx_ui_confirm.wav", _wav(sample_rate=44100))],
        "A-02", "WARN",
    )

    # 反例03：时长超限（sfx 31s > 30s）
    expect(
        "反例03：时长超限（sfx 31s）→ A-03 WARN",
        [("audio/sfx/sfx_ui_confirm.wav", _wav(duration_sec=31.0))],
        "A-03", "WARN",
    )

    # 反例04：三件套缺（有音频无 THIRD_PARTY.md）
    expect(
        "反例04：三件套缺（无 THIRD_PARTY）→ A-04 FAIL",
        [("audio/sfx/sfx_ui_confirm.wav", _wav())],
        "A-04", "FAIL",
    )

    # 反例05：位深非法（8bit）
    expect(
        "反例05：位深非法（8bit）→ A-02 WARN",
        [("audio/sfx/sfx_ui_confirm.wav", _wav(bits=8))],
        "A-02", "WARN",
    )

    # 反例06：层级错放（sfx 文件在 bgm 目录）
    expect(
        "反例06：层级错放（sfx 在 bgm 目录）→ A-01 FAIL",
        [("audio/bgm/sfx_ui_confirm.ogg", b"OggS")],
        "A-01", "FAIL",
    )

    # 正例07：全合法 + 三件套齐备 → 无 FAIL（exit 0）
    tp = (
        "| bgm_dawn_01.wav | cc | https://example.com/bgm | 2026-01-01 |\n"
        "| sfx_ui_confirm.wav | cc | https://example.com/sfx | 2026-01-01 |\n"
        "| vo_dawn_s2_01.wav | cc | https://example.com/vo | 2026-01-01 |\n"
    )
    files = [
        ("audio/bgm/bgm_dawn_01.wav", _wav()),
        ("audio/sfx/sfx_ui_confirm.wav", _wav()),
        ("audio/vo/vo_dawn_s2_01.wav", _wav()),
    ]
    tmp = tempfile.mkdtemp(prefix="hako_audio_ok_")
    pkg = build_pkg(tmp, files, third_party=tp)
    code, out = run_audio_check(pkg)
    ok = (code == 0) and ("FAIL 0" in out)
    report("正例07：全合法三件套齐备 → 无 FAIL", ok, f"exit={code}")
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
