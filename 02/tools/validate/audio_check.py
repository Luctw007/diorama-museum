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
音频规则校验器（TASK-42A，把 v0.4 音频章 A-01~A-04 落地，纯 stdlib）

把《内容包规范 v0.4》第十四章「音频资产」的校验规则 A-01~A-04 做成可运行校验器，
模式同 model_check.py：逐文件报告 + 退出码（0=无 FAIL，1=有 FAIL）+ `--json`。

规则（A = Audio Rule）：
    A-01  命名：`audio/` 三层子目录（bgm/sfx/vo）下文件名须匹配
           `bgm_<厅>_<序号>` / `sfx_<设备|ui>_<动作>` / `vo_<厅>_<站>_<句>`，
           以及 `amb_*` / `run_*` 扩展前缀；前缀与目录类别一致（层级错放 FAIL）。
    A-02  格式元数据：WAV 头解析（RIFF/fmt，采样率须 48000、位深须 16 或 24）；
           OGG 仅登记元数据（大小）并 WARN（纯 stdlib 不解析 Vorbis 头，[需实测]）。
    A-03  时长与响度：WAV 时长对照类别上限（bgm≤180s / sfx≤30s / vo≤600s /
           amb≤120s / run≤30s）；响度（LUFS/峰值 dBFS）无计量库 → 记 [需实测] WARN，
           不作 FAIL。
    A-04  来源三件套：有外部音频时 THIRD_PARTY.md 须有「分档+URL+日期」三件套行；
           程序化合成件须在 audio/SYNTH.md 有配方；否则 FAIL（外部无登记）/
           WARN（合成件无 SYNTH.md）。

用法：
    python audio_check.py <content-package-path> [--json]

仅读文件头/文本登记文件，不解析 OGG Vorbis 音频帧、不做 LUFS 计量。纯 stdlib。

依赖：无（独立脚本，不 import validate/model_check）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
# audio/ 三层子目录（v0.4 §2 目录结构）
AUDIO_SUBDIRS = ("bgm", "sfx", "vo")

# 合法类别前缀（v0.4 §14.3 命名正则）
AUDIO_PREFIXES = ("bgm", "sfx", "vo", "amb", "run")

# 允许的音频扩展名
AUDIO_EXTS = (".wav", ".ogg")

# 基础命名正则：^(bgm|sfx|vo|amb|run)_[a-z0-9_]+$（v0.4 §14.3）
BASE_NAME_RE = re.compile(r"^(bgm|sfx|vo|amb|run)_[a-z0-9_]+$")

# 各类别结构正则（TASK-42A 口径：bgm_厅_序号 / sfx_设备_动作 / vo_厅_站_句）
STRUCT_RE = {
    "bgm": re.compile(r"^bgm_[a-z0-9]+_[0-9]+$"),
    "sfx": re.compile(r"^sfx_[a-z0-9]+_[a-z0-9_]+$"),
    "vo": re.compile(r"^vo_[a-z0-9]+_[a-z0-9]+_[0-9]+$"),
    "amb": re.compile(r"^amb_[a-z0-9_]+$"),
    "run": re.compile(r"^run_[a-z0-9]+_[a-z0-9_]+$"),
}

# 子目录 → 允许的前缀集合（层级匹配）
SUBDIR_PREFIXES = {
    "bgm": {"bgm"},
    "sfx": {"sfx", "run", "amb"},
    "vo": {"vo"},
}

# 时长上限（秒）—— TASK-42A 口径：bgm≤180s、sfx≤30s、vo≤10min(600s)。
# amb/run 沿用 v0.4 §2.3 口径（amb 60–120s、run 同 sfx）。
DURATION_LIMITS = {
    "bgm": 180,
    "sfx": 30,
    "vo": 600,
    "amb": 120,
    "run": 30,
}

# WAV 合法采样率 / 位深（TASK-42A 口径）
REQUIRED_SAMPLE_RATE = 48000
VALID_BITS = (16, 24)

# THIRD_PARTY 三件套判定（分档关键词 + URL + 日期）
THREE_PIECE_TIERS = (
    "public_domain", "cc", "licensed", "visual_reference_only",
    "原创", "程序化合成",
)
URL_RE = re.compile(r"https?://\S+")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

# 需登记来源三件套的音频文件名（排除 SYNTH.md 等非音频文件）
SYNTH_MD = "SYNTH.md"
THIRD_PARTY_MD = "THIRD_PARTY.md"


# ---------------------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------------------
def _finding(rule: str, level: str, rel: str, msg: str) -> dict:
    return {"rule": rule, "level": level, "file": rel, "message": msg}


def _stem(name: str) -> str:
    """去掉扩展名（仅一层）。"""
    base = os.path.basename(name)
    for ext in AUDIO_EXTS:
        if base.lower().endswith(ext):
            return base[: -len(ext)]
    return base


def _category_of(stem: str):
    """由文件名字根判定类别前缀；无法判定返回 None。"""
    for p in AUDIO_PREFIXES:
        if stem.startswith(p + "_"):
            return p
    return None


# ---------------------------------------------------------------------------
# WAV 头解析（纯 struct）
# ---------------------------------------------------------------------------
def parse_wav(path: str) -> dict:
    """解析 WAV 的 RIFF/fmt/data，返回元数据 dict；非法结构抛 ValueError。

    返回：{audio_format, channels, sample_rate, byte_rate, bits, data_size}
    """
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 12:
        raise ValueError("文件过短（<12 字节）")
    if data[0:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError("非 RIFF/WAVE 容器")

    fmt = None
    data_size = None
    pos = 12
    while pos + 8 <= len(data):
        cid = data[pos:pos + 4]
        csize = struct.unpack("<I", data[pos + 4:pos + 8])[0]
        if cid == b"fmt " and csize >= 16:
            (audio_format, channels, sample_rate,
             byte_rate, block_align, bits) = struct.unpack(
                "<HHIIHH", data[pos + 8:pos + 24])
            fmt = {
                "audio_format": audio_format,
                "channels": channels,
                "sample_rate": sample_rate,
                "byte_rate": byte_rate,
                "block_align": block_align,
                "bits": bits,
            }
        elif cid == b"data":
            data_size = csize
        # chunk 按 2 字节对齐（奇数 size 补 1）
        pos += 8 + csize + (csize & 1)

    if fmt is None:
        raise ValueError("缺 fmt chunk")
    fmt["data_size"] = data_size
    return fmt


def wav_duration(fmt: dict) -> float | None:
    """由 byte_rate 与 data_size 计算时长（秒）；无 data chunk 返回 None。"""
    br = fmt.get("byte_rate") or 0
    ds = fmt.get("data_size")
    if br <= 0 or ds is None:
        return None
    return ds / br


# ---------------------------------------------------------------------------
# 文本登记文件读取
# ---------------------------------------------------------------------------
def _read_text(path: str) -> str:
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def _three_piece_row(text: str, name: str) -> bool:
    """判断 THIRD_PARTY.md 中是否存在引用 name 且含「分档+URL+日期」三件套的行。"""
    for line in text.splitlines():
        if name not in line:
            continue
        low = line.lower()
        has_tier = any(t in low for t in THREE_PIECE_TIERS)
        has_url = bool(URL_RE.search(line))
        has_date = bool(DATE_RE.search(line))
        if has_tier and has_url and has_date:
            return True
    return False


# ---------------------------------------------------------------------------
# 各 A 规则检查
# ---------------------------------------------------------------------------
def check_a01(rel: str, subdir: str) -> list[dict]:
    """A-01 命名：目录层级 + 前缀 + 结构正则。"""
    name = os.path.basename(rel)
    stem = _stem(name)
    out = []

    if subdir not in AUDIO_SUBDIRS:
        out.append(_finding("A-01", "FAIL", rel,
                            f"层级错放：{name!r} 不在 bgm/sfx/vo 三层子目录内"))
        return out

    # 1) 基础命名（类别前缀 + snake_case）
    if not BASE_NAME_RE.match(stem):
        out.append(_finding("A-01", "FAIL", rel,
                            f"命名非法：{name!r} 不匹配 ^(bgm|sfx|vo|amb|run)_[a-z0-9_]+$"))
        return out

    cat = _category_of(stem)
    # 2) 前缀与目录类别一致
    if cat not in SUBDIR_PREFIXES[subdir]:
        out.append(_finding("A-01", "FAIL", rel,
                            f"层级错放：{name!r}（前缀 {cat}）不在 audio/{subdir}/ 目录"))
        return out

    # 3) 类别结构（bgm_厅_序号 / sfx_设备_动作 / vo_厅_站_句）
    if not STRUCT_RE[cat].match(stem):
        out.append(_finding("A-01", "FAIL", rel,
                            f"命名结构不符：{name!r} 未满足 {STRUCT_RE[cat].pattern}"))
        return out

    out.append(_finding("A-01", "PASS", rel, f"命名合法（{cat} 类，目录 {subdir}）"))
    return out


def check_a02(rel: str, fp: str) -> list[dict]:
    """A-02 格式元数据：WAV 采样率/位深；OGG 仅登记 + WARN。"""
    out = []
    ext = os.path.splitext(rel)[1].lower()

    if ext == ".ogg":
        size = os.path.getsize(fp) if os.path.isfile(fp) else 0
        out.append(_finding(
            "A-02", "WARN", rel,
            f"[需实测] OGG 采样率/位深不可测（纯 stdlib 不解析 Vorbis 头；{size} 字节已登记）"))
        return out

    # WAV
    try:
        fmt = parse_wav(fp)
    except ValueError as e:
        out.append(_finding("A-02", "FAIL", rel, f"WAV 头解析失败：{e}"))
        return out

    sr = fmt["sample_rate"]
    if sr != REQUIRED_SAMPLE_RATE:
        out.append(_finding("A-02", "WARN", rel,
                            f"采样率 {sr} ≠ {REQUIRED_SAMPLE_RATE} Hz"))
    else:
        out.append(_finding("A-02", "PASS", rel, f"采样率 {sr} Hz 合规"))

    bits = fmt["bits"]
    if bits not in VALID_BITS:
        out.append(_finding("A-02", "WARN", rel,
                            f"位深 {bits} bit 非法（应为 16 或 24）"))
    else:
        out.append(_finding("A-02", "PASS", rel, f"位深 {bits} bit 合规"))
    return out


def check_a03(rel: str, fp: str, cat: str) -> list[dict]:
    """A-03 时长上限 + 响度[需实测] WARN。"""
    out = []
    ext = os.path.splitext(rel)[1].lower()
    limit = DURATION_LIMITS.get(cat)

    # 响度：无计量库，一律 [需实测] WARN（不作 FAIL）
    out.append(_finding("A-03", "WARN", rel,
                        "[需实测] 响度（LUFS/峰值 dBFS）不可测（纯 stdlib 无计量）"))

    if ext == ".ogg":
        out.append(_finding("A-03", "WARN", rel,
                            "[需实测] OGG 时长不可测（不解析 Vorbis 头）"))
        return out

    try:
        fmt = parse_wav(fp)
    except ValueError:
        return out  # 解析失败已由 A-02 报出，A-03 不再重复

    dur = wav_duration(fmt)
    if dur is None:
        out.append(_finding("A-03", "WARN", rel, "[需实测] 无 data chunk，时长不可测"))
        return out
    if limit is not None and dur > limit:
        out.append(_finding("A-03", "WARN", rel,
                            f"时长 {dur:.1f}s 超 {cat} 上限 {limit}s"))
    else:
        out.append(_finding("A-03", "PASS", rel, f"时长 {dur:.1f}s 在 {cat} 上限内"))
    return out


def check_a04(rel: str, tp_text: str, synth_text: str) -> list[dict]:
    """A-04 来源三件套：外部音频需 THIRD_PARTY 三件套；合成件需 SYNTH.md。"""
    name = os.path.basename(rel)
    if name in synth_text:
        return [_finding("A-04", "PASS", rel, f"程序化合成件已在 SYNTH.md 登记配方")]
    if _three_piece_row(tp_text, name):
        return [_finding("A-04", "PASS", rel, f"THIRD_PARTY.md 三件套登记完整")]
    # 区分：无 SYNTH.md 的合成件 → WARN；外部无登记 → FAIL
    if synth_text and name not in synth_text:
        return [_finding("A-04", "FAIL", rel,
                         f"外部音频 {name!r} 缺 THIRD_PARTY.md「分档+URL+日期」三件套登记")]
    return [_finding("A-04", "FAIL", rel,
                     f"缺来源三件套登记（THIRD_PARTY.md 无「分档+URL+日期」行）")]


# ---------------------------------------------------------------------------
# 音频文件发现
# ---------------------------------------------------------------------------
def collect_audio_files(pkg: str) -> list[tuple[str, str, str]]:
    """返回 [(rel, subdir, cat)]，rel 为相对包根的 POSIX 路径。"""
    out = []
    audio_root = os.path.join(pkg, "audio")
    if not os.path.isdir(audio_root):
        return out
    for subdir in AUDIO_SUBDIRS:
        d = os.path.join(audio_root, subdir)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.lower().endswith(AUDIO_EXTS):
                continue
            rel = os.path.join("audio", subdir, name).replace("\\", "/")
            stem = _stem(name)
            cat = _category_of(stem) or "unknown"
            out.append((rel, subdir, cat))
    return out


# ---------------------------------------------------------------------------
# 单包检查
# ---------------------------------------------------------------------------
def check_package(pkg: str) -> dict:
    pkg = os.path.abspath(pkg)
    meta = {}
    mp = os.path.join(pkg, "meta.json")
    if os.path.isfile(mp):
        try:
            with open(mp, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, json.JSONDecodeError):
            meta = {}
    device_id = (meta.get("meta") or {}).get("id") or os.path.basename(pkg)

    files = collect_audio_files(pkg)
    tp_text = _read_text(os.path.join(pkg, THIRD_PARTY_MD))
    synth_text = _read_text(os.path.join(pkg, "audio", SYNTH_MD))

    n_fail = 0
    n_warn = 0
    out_files = []

    if not files:
        # 无 audio/ 目录或无音频文件：跳过，并如实记录
        out_files.append({
            "path": "(无 audio/ 目录)",
            "category": None,
            "findings": [_finding("A-01", "PASS", "(跳过)", "无 audio/ 目录或音频文件，跳过检查")],
        })
    else:
        for rel, subdir, cat in files:
            fp = os.path.join(pkg, rel)
            findings = []
            findings += check_a01(rel, subdir)
            findings += check_a02(rel, fp)
            findings += check_a03(rel, fp, cat)
            findings += check_a04(rel, tp_text, synth_text)
            for f in findings:
                if f["level"] == "FAIL":
                    n_fail += 1
                elif f["level"] == "WARN":
                    n_warn += 1
            out_files.append({"path": rel, "category": cat, "findings": findings})

    return {
        "device_id": device_id,
        "audio_file_count": len(files),
        "fail": n_fail,
        "warn": n_warn,
        "files": out_files,
    }


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_report(rep: dict) -> str:
    lines = [f"== {rep['device_id']}（audio/ 文件 {rep['audio_file_count']} 个，"
             f"FAIL {rep['fail']}，WARN {rep['warn']}）=="]
    for f in rep["files"]:
        lines.append(f"  {f['path']}" + (f"（{f['category']}）" if f["category"] else ""))
        for fd in f["findings"]:
            lines.append(f"    {fd['level']:<4} {fd['rule']}  {fd['message']}")
    return "\n".join(lines)


def render_json(rep: dict) -> str:
    return json.dumps(rep, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="音频规则校验器（TASK-42A，v0.4 A-01~A-04 落地）")
    p.add_argument("package_path", help="content/<device-id>/ 目录")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    pkg = os.path.abspath(args.package_path)
    if not os.path.isfile(os.path.join(pkg, "meta.json")):
        sys.stderr.write(f"错误：{pkg} 不是内容包（缺 meta.json）\n")
        return 2

    rep = check_package(pkg)
    if args.json:
        sys.stdout.write(render_json(rep))
    else:
        print(render_report(rep))
    return 1 if rep["fail"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
