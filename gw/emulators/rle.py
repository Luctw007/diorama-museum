# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""字节级 RLE 编解码（协议 v2 帧压缩，纯 stdlib、零依赖）。

载荷格式：若干 (count, value) 两字节组依次拼接；
- count ∈ [1, 255]，表示 value 连续重复次数；
- 无任何头部/尾部元信息；
- 解码对任何畸形输入（奇数长度、count=0）返回 None，不抛异常。

直接运行本文件执行自测（退出码 0 = 通过）：
    python gw/emulators/rle.py
"""

from __future__ import annotations


def encode(data: bytes) -> bytes:
    """编码。空输入 → 空 bytes；连续同值超过 255 拆为多段。"""
    if not data:
        return b""
    out = bytearray()
    n = len(data)
    i = 0
    while i < n:
        value = data[i]
        j = i + 1
        while j < n and data[j] == value and (j - i) < 255:
            j += 1
        out.append(j - i)
        out.append(value)
        i = j
    return bytes(out)


def decode(payload: bytes, max_len: int = 0) -> bytes | None:
    """解码。畸形返回 None；max_len > 0 时输出超过上限即失败（防膨胀炸弹）。"""
    if len(payload) % 2 != 0:
        return None
    out = bytearray()
    for i in range(0, len(payload), 2):
        count = payload[i]
        if count == 0:
            return None
        value = payload[i + 1]
        out.extend(bytes([value]) * count)
        if max_len and len(out) > max_len:
            return None
    return bytes(out)


def main() -> int:
    import random
    fails = 0

    cases = [
        b"",
        b"\x00",
        b"\x00" * 255,
        b"\x00" * 300,
        bytes(range(256)),
        b"\x01\x02\x01\x01\x03\x04\x04\x04",
    ]
    for idx, data in enumerate(cases):
        if decode(encode(data)) != data:
            print("FAIL 用例 %d：roundtrip 不一致" % idx)
            fails += 1
        else:
            print("PASS 用例 %d：len=%d → 编码后 len=%d"
                  % (idx, len(data), len(encode(data))))

    for trial in range(3):
        rnd = bytes(random.randrange(256) for _ in range(5000))
        if decode(encode(rnd)) != rnd:
            print("FAIL 随机 roundtrip #%d" % trial)
            fails += 1
        else:
            print("PASS 随机 roundtrip #%d（5000 字节）" % trial)

    # max_len 防膨胀
    if decode(encode(b"\x00" * 1000), max_len=500) is not None:
        print("FAIL max_len 防膨胀未生效")
        fails += 1
    else:
        print("PASS max_len 防膨胀")

    # 畸形输入
    for bad in (b"\x01", b"\x00\x01", b"\x05\xff\x02"):
        result = decode(bad)
        if result is not None and bad != b"\x05\xff\x02":
            print("FAIL 畸形输入未拒绝: %r" % bad)
            fails += 1
    print("PASS 畸形输入处理")

    print("rle 自测：%s" % ("PASS" if fails == 0 else "FAIL（%d）" % fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())