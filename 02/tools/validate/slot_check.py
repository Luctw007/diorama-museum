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
槽位与介质校验器（TASK-47B，把 v0.5 槽位契约章落地，纯 stdlib）

把《规范 v0.5 槽位契约章》的槽位/介质规则做成可运行裁判，模式同 model_check/audio_check：
逐槽位/逐介质报告 + 退出码（0=无 FAIL）+ `--json`。

规则（SV = Slot Validation）：
    SV-01  manifest 存在且 JSON 合法。
    SV-02  schema 关键字段类型/枚举校验：slot_id/device_class/backend_type/
           media_classes 全枚举、binary 多架构键白名单、capabilities 布尔。
    SV-03  二进制路径存在（相对槽位目录，含 .exe 变体）；介质文件存在且扩展名
           符合其 media_class 约定。
    SV-04  许可三件套字段齐全（license 为对象时须 tier+url+date；字符串非空即 PASS）。
    SV-05  哈希清单（SHA256SUMS）行格式（若有）：`<64hex>  <文件名>`。

用法：
    python slot_check.py <slots-root> [--json]

<slots-root> 须含 `emulators/`（槽位）与可选 `media/`（介质）子目录，目录契约见规范 v0.5。

依赖：无（独立脚本）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# 常量（对齐规范 v0.5 §3 全枚举）
# ---------------------------------------------------------------------------
DEVICE_CLASSES = {
    "computer", "console", "handheld", "phone", "pda", "dedicated_av", "other",
}
BACKEND_TYPES = {
    "native", "mame", "simh", "stella", "mesen", "mobile", "dedicated",
}
MEDIA_CLASSES = {
    "cartridge", "disk", "tape", "cd", "dvd", "card", "firmware", "app_package",
}

# media_class → 扩展名约定（规范 §3.3）
MEDIA_EXTS = {
    "cartridge": {".rom", ".bin", ".nes", ".smd", ".md", ".sfc", ".a26", ".col"},
    "disk": {".dsk", ".img", ".d64", ".adf", ".hfe", ".po", ".do"},
    "tape": {".tap", ".wav", ".cass", ".uef", ".tzx"},
    "cd": {".iso", ".cue", ".chd", ".bin"},
    "dvd": {".iso", ".vob"},
    "card": {".sd", ".bin", ".img"},
    "firmware": {".bin", ".rom", ".firmware"},
    "app_package": {".apk", ".ipa", ".app"},
}

# binary 多架构键白名单（规范 §2.6）
ARCH_KEYS = {
    "x86_64-windows", "x86_64-linux", "aarch64-linux",
    "x86_64-macos", "aarch64-macos", "wasm32",
}

# 许可分档关键词（规范 §2.9 / §5.3，用于三件套/来源判定）
LICENSE_TIERS = {
    "mit", "gpl", "gpl-2.0-or-later", "gpl-2.0", "gpl-3.0", "bsd", "bsd-3-clause",
    "bsd-2-clause", "apache-2.0", "proprietary", "cc-by", "cc0",
    "public-domain", "public_domain", "unknown", "cc", "licensed",
    "visual_reference_only", "原创", "程序化合成",
}

SLOT_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}\s+\S+$")
URL_RE = re.compile(r"https?://\S+")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


# ---------------------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------------------
def _finding(rule: str, level: str, rel: str, msg: str) -> dict:
    return {"rule": rule, "level": level, "file": rel, "message": msg}


def _read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 槽位扫描
# ---------------------------------------------------------------------------
def discover_slots(slots_root: str) -> list[str]:
    """返回 slots/emulators/*/ 槽位目录列表（含 manifest.json 或缺 manifest 的目录）。"""
    emu = os.path.join(slots_root, "emulators")
    if not os.path.isdir(emu):
        return []
    out = []
    for name in sorted(os.listdir(emu)):
        d = os.path.join(emu, name)
        if os.path.isdir(d):
            out.append(d)
    return out


def discover_media(slots_root: str) -> list[tuple[str, str, str, str]]:
    """返回 [(rel, media_class, device_class, slot_id)] 介质目录列表。"""
    media = os.path.join(slots_root, "media")
    if not os.path.isdir(media):
        return []
    out = []
    for mc in sorted(os.listdir(media)):
        p1 = os.path.join(media, mc)
        if not os.path.isdir(p1):
            continue
        for dc in sorted(os.listdir(p1)):
            p2 = os.path.join(p1, dc)
            if not os.path.isdir(p2):
                continue
            for sid in sorted(os.listdir(p2)):
                p3 = os.path.join(p2, sid)
                if os.path.isdir(p3):
                    rel = os.path.join("media", mc, dc, sid).replace("\\", "/")
                    out.append((rel, mc, dc, sid))
    return out


# ---------------------------------------------------------------------------
# manifest 规则
# ---------------------------------------------------------------------------
def check_sv01(slot_dir: str, slot_id: str) -> list[dict]:
    """manifest 存在且 JSON 合法。返回 findings；成功时附 manifest 数据到返回列表末尾？改用异常传递。"""
    mpath = os.path.join(slot_dir, "manifest.json")
    if not os.path.isfile(mpath):
        return [_finding("SV-01", "FAIL", f"{slot_id}/manifest.json", "manifest.json 不存在")]
    try:
        _read_json(mpath)
    except json.JSONDecodeError as e:
        return [_finding("SV-01", "FAIL", f"{slot_id}/manifest.json", f"JSON 非法：{e}")]
    return [_finding("SV-01", "PASS", f"{slot_id}/manifest.json", "manifest 存在且 JSON 合法")]


def check_sv02(manifest: dict, slot_id: str) -> list[dict]:
    """schema 关键字段类型/枚举校验。"""
    rel = f"{slot_id}/manifest.json"
    out = []

    # slot_id
    sid = manifest.get("slot_id")
    if not isinstance(sid, str) or not sid:
        out.append(_finding("SV-02", "FAIL", rel, "slot_id 缺失或非字符串"))
    elif sid != slot_id:
        out.append(_finding("SV-02", "FAIL", rel, f"slot_id {sid!r} 与目录名 {slot_id!r} 不符"))
    elif not SLOT_ID_RE.match(sid):
        out.append(_finding("SV-02", "FAIL", rel, f"slot_id {sid!r} 非 kebab-case"))
    else:
        out.append(_finding("SV-02", "PASS", rel, f"slot_id {sid} 合法"))

    # device_class
    dc = manifest.get("device_class")
    if dc not in DEVICE_CLASSES:
        out.append(_finding("SV-02", "FAIL", rel,
                            f"device_class {dc!r} 不在枚举 {sorted(DEVICE_CLASSES)}"))
    else:
        out.append(_finding("SV-02", "PASS", rel, f"device_class {dc} 合法"))

    # backend_type
    bt = manifest.get("backend_type")
    if bt not in BACKEND_TYPES:
        out.append(_finding("SV-02", "FAIL", rel,
                            f"backend_type {bt!r} 不在枚举 {sorted(BACKEND_TYPES)}"))
    else:
        out.append(_finding("SV-02", "PASS", rel, f"backend_type {bt} 合法"))

    # media_classes
    mcs = manifest.get("media_classes")
    if mcs is not None:
        if not isinstance(mcs, list):
            out.append(_finding("SV-02", "FAIL", rel, "media_classes 非数组"))
        else:
            bad = [m for m in mcs if m not in MEDIA_CLASSES]
            if bad:
                out.append(_finding("SV-02", "FAIL", rel,
                                    f"media_classes 含非法类目 {bad}"))
            else:
                out.append(_finding("SV-02", "PASS", rel, f"media_classes {mcs} 合法"))
    else:
        out.append(_finding("SV-02", "WARN", rel, "media_classes 未声明（可选）"))

    # binary 多架构键白名单
    binary = manifest.get("binary")
    if isinstance(binary, dict):
        unknown = [k for k in binary if k not in ARCH_KEYS]
        if unknown:
            out.append(_finding("SV-02", "WARN", rel,
                                f"binary 多架构键 {unknown} 不在白名单 {sorted(ARCH_KEYS)}"))

    # capabilities 布尔
    caps = manifest.get("capabilities")
    if caps is not None:
        if not isinstance(caps, dict):
            out.append(_finding("SV-02", "FAIL", rel, "capabilities 非对象"))
        else:
            for k, v in caps.items():
                if not isinstance(v, bool):
                    out.append(_finding("SV-02", "FAIL", rel,
                                        f"capabilities.{k} 非布尔（{v!r}）"))

    if not any(f["rule"] == "SV-02" and f["level"] == "PASS" for f in out):
        out.append(_finding("SV-02", "PASS", rel, "其余字段类型合规"))
    return out


def check_sv03_manifest(manifest: dict, slot_dir: str, slot_id: str) -> list[dict]:
    """二进制路径存在（相对槽位目录，含 .exe 变体）。"""
    rel = f"{slot_id}/manifest.json"
    binary = manifest.get("binary")
    if not binary:
        return [_finding("SV-03", "PASS", rel, "无 binary（native/零二进制后端）")]

    # 取当前宿主平台候选（简写 string 或 object 取第一个非空值）
    names = []
    if isinstance(binary, str):
        names = [binary]
    elif isinstance(binary, dict):
        names = [v for v in binary.values() if isinstance(v, str) and v]
    if not names:
        return [_finding("SV-03", "WARN", rel, "binary 字段为空")]

    found = []
    for name in names:
        base = os.path.join(slot_dir, name)
        for cand in (base, base + ".exe"):
            if os.path.isfile(cand):
                found.append(os.path.basename(cand))
    if found:
        return [_finding("SV-03", "PASS", rel, f"二进制就位：{', '.join(found)}")]
    return [_finding("SV-03", "FAIL", rel,
                     f"二进制缺失：{names}（及 .exe 变体）均不在槽位目录（或未设 binary_env）")]


def check_sv04(manifest: dict, slot_id: str) -> list[dict]:
    """许可三件套字段齐全。"""
    rel = f"{slot_id}/manifest.json"
    lic = manifest.get("license")
    if isinstance(lic, str):
        if lic.strip():
            return [_finding("SV-04", "PASS", rel, f"许可简写字符串非空（{lic[:30]}）")]
        return [_finding("SV-04", "FAIL", rel, "license 字符串为空")]
    if isinstance(lic, dict):
        missing = [k for k in ("tier", "url", "date") if not lic.get(k)]
        if missing:
            return [_finding("SV-04", "FAIL", rel, f"许可三件套缺 {missing}")]
        return [_finding("SV-04", "PASS", rel,
                         f"许可三件套齐全（tier={lic['tier']}, date={lic['date']}）")]
    return [_finding("SV-04", "FAIL", rel, "license 字段缺失")]


# ---------------------------------------------------------------------------
# 介质规则
# ---------------------------------------------------------------------------
def _list_files(d: str) -> list[str]:
    out = []
    for root, _dirs, files in os.walk(d):
        for fn in files:
            out.append(os.path.join(root, fn))
    return sorted(out)


def check_sv03_media(media_dirs: list[tuple[str, str, str, str]], slots_root: str) -> list[dict]:
    """介质文件存在且扩展名符合其 media_class 约定。"""
    out = []
    media_root = os.path.join(slots_root, "media")
    for rel, mc, dc, sid in media_dirs:
        d = os.path.join(media_root, mc, dc, sid)
        if mc not in MEDIA_CLASSES:
            out.append(_finding("SV-03", "FAIL", rel, f"media_class {mc!r} 非法"))
            continue
        for fp in _list_files(d):
            fn = os.path.basename(fp)
            if fn == "README.md" or fn == "SOURCES.md" or fn == "SHA256SUMS":
                continue
            ext = os.path.splitext(fn)[1].lower()
            if not ext:
                out.append(_finding("SV-03", "WARN", rel, f"介质 {fn!r} 无扩展名"))
            elif ext not in MEDIA_EXTS[mc]:
                out.append(_finding("SV-03", "FAIL", rel,
                                    f"介质 {fn!r} 扩展名 {ext} 不符 {mc} 约定 {sorted(MEDIA_EXTS[mc])}"))
    if not out:
        out.append(_finding("SV-03", "PASS", "media/", "介质扩展名均符合类目约定（或无介质文件）"))
    return out


def check_sv05(media_dirs: list[tuple[str, str, str, str]], slots_root: str) -> list[dict]:
    """哈希清单（SHA256SUMS）行格式（若有）。"""
    out = []
    media_root = os.path.join(slots_root, "media")
    for rel, mc, dc, sid in media_dirs:
        d = os.path.join(media_root, mc, dc, sid)
        hf = os.path.join(d, "SHA256SUMS")
        if not os.path.isfile(hf):
            continue
        with open(hf, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.rstrip("\n")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                if not SHA256_RE.match(line):
                    out.append(_finding("SV-05", "FAIL", os.path.join(rel, "SHA256SUMS"),
                                        f"第 {i} 行格式非法：{line[:60]!r}"))
                else:
                    out.append(_finding("SV-05", "PASS", os.path.join(rel, "SHA256SUMS"),
                                        f"第 {i} 行格式合法"))
    if not out:
        out.append(_finding("SV-05", "PASS", "media/", "无 SHA256SUMS（可选，跳过）"))
    return out


def check_sv04_media(media_dirs: list[tuple[str, str, str, str]], slots_root: str) -> list[dict]:
    """介质来源三件套（README/SOURCES 含 URL+日期）——WARN 级。"""
    out = []
    media_root = os.path.join(slots_root, "media")
    for rel, mc, dc, sid in media_dirs:
        d = os.path.join(media_root, mc, dc, sid)
        media_files = [f for f in _list_files(d)
                       if os.path.basename(f) not in ("README.md", "SOURCES.md", "SHA256SUMS")]
        if not media_files:
            continue
        text = ""
        for doc in ("SOURCES.md", "README.md"):
            p = os.path.join(d, doc)
            if os.path.isfile(p):
                with open(p, "r", encoding="utf-8") as f:
                    text += f.read()
        if not (URL_RE.search(text) and DATE_RE.search(text)):
            out.append(_finding("SV-04", "WARN", rel, "介质缺来源三件套登记（README/SOURCES 无 URL+日期）"))
    if not out:
        out.append(_finding("SV-04", "PASS", "media/", "介质来源登记齐备（或无介质文件）"))
    return out


# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
def check_slots(slots_root: str) -> dict:
    slots_root = os.path.abspath(slots_root)
    slot_dirs = discover_slots(slots_root)
    media_dirs = discover_media(slots_root)

    n_fail = 0
    n_warn = 0
    slots = []

    if not slot_dirs:
        slots.append({"slot_id": "(无槽位)", "manifest": None,
                      "findings": [_finding("SV-01", "PASS", "emulators/",
                                           "无槽位目录（零槽位=行为不变）")]})
    else:
        for sd in slot_dirs:
            slot_id = os.path.basename(sd)
            manifest = None
            findings = []
            findings += check_sv01(sd, slot_id)
            mpath = os.path.join(sd, "manifest.json")
            if os.path.isfile(mpath):
                try:
                    manifest = _read_json(mpath)
                except json.JSONDecodeError:
                    manifest = None
            if manifest is not None:
                findings += check_sv02(manifest, slot_id)
                findings += check_sv03_manifest(manifest, sd, slot_id)
                findings += check_sv04(manifest, slot_id)
            for f in findings:
                if f["level"] == "FAIL":
                    n_fail += 1
                elif f["level"] == "WARN":
                    n_warn += 1
            slots.append({"slot_id": slot_id, "manifest": manifest, "findings": findings})

    media_findings = []
    media_findings += check_sv03_media(media_dirs, slots_root)
    media_findings += check_sv05(media_dirs, slots_root)
    media_findings += check_sv04_media(media_dirs, slots_root)
    for f in media_findings:
        if f["level"] == "FAIL":
            n_fail += 1
        elif f["level"] == "WARN":
            n_warn += 1

    return {
        "slots_root": slots_root,
        "slot_count": len(slot_dirs),
        "media_dir_count": len(media_dirs),
        "fail": n_fail,
        "warn": n_warn,
        "slots": slots,
        "media": media_findings,
    }


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_report(rep: dict) -> str:
    lines = [f"== 槽位系统（槽位 {rep['slot_count']} 个，介质目录 {rep['media_dir_count']} 个，"
             f"FAIL {rep['fail']}，WARN {rep['warn']}）=="]
    for s in rep["slots"]:
        lines.append(f"  {s['slot_id']}")
        for fd in s["findings"]:
            lines.append(f"    {fd['level']:<4} {fd['rule']}  {fd['message']}")
    if rep["media"]:
        lines.append("  [media/]")
        for fd in rep["media"]:
            lines.append(f"    {fd['level']:<4} {fd['rule']}  {fd['file']}: {fd['message']}")
    return "\n".join(lines)


def render_json(rep: dict) -> str:
    return json.dumps(rep, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="槽位与介质校验器（TASK-47B，v0.5 槽位契约 SV-01~05）")
    p.add_argument("slots_root", help="slots/ 根目录（含 emulators/ 与可选 media/）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    root = os.path.abspath(args.slots_root)
    if not os.path.isdir(root):
        sys.stderr.write(f"错误：{root} 不是目录\n")
        return 2

    rep = check_slots(root)
    if args.json:
        sys.stdout.write(render_json(rep))
    else:
        print(render_report(rep))
    return 1 if rep["fail"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
