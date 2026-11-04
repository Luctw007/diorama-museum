import argparse
import math
import os
import struct
import sys
import wave

"""占位口播轨生成器（TASK-91B / 44 号 G-9）：纯 stdlib 出两条 8 秒单声道 WAV。
命名对齐 04 线 20 号规格 narr 系（narr_hall_intro / narr_eniac），占位用途：
解锁"单口播互斥"的引擎实测；正式解说轨由 04 线配音/tTS 流程产出后替换。
参数按任务书：22.05 kHz / 16 bit / 单声道；峰值 -18 dBFS 防爆音（20 号 §4.3）。"""

RATE = 22050
DUR = 8.0
FREQS = {"narr_hall_intro": 440.0, "narr_eniac": 330.0}


def build(freq: float, path: str) -> None:
    n = int(RATE * DUR)
    frames = bytearray()
    peak = int(32767 * 10 ** (-18 / 20))
    for i in range(n):
        t = i / RATE
        s = math.sin(2 * math.pi * freq * t)
        if (t % 1.0) < 0.06:          # 每秒 60ms 节拍哔（880Hz 叠层）
            s = s * 0.5 + 0.5 * math.sin(2 * math.pi * 880 * t)
        frames += struct.pack("<h", int(s * peak))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    print("已生成 %s（%.1fs, %dHz, %d采样）" % (path, DUR, RATE, n))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "godot", "content", "audio", "demo"))
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    for name, freq in FREQS.items():
        build(freq, os.path.join(args.out, name + "_placeholder.wav"))
    return 0


if __name__ == "__main__":
    sys.exit(main())