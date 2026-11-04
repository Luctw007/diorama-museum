# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
r"""内容包 runtime.json → 网关 start_device 配置的映射桥（TASK-11B）。

用法：
    python scripts/run_profile.py <package_dir> [--json] [--start] [--gateway-port 7331] [--device-id ID]

行为：
- 读取 meta.json（顶层 meta/assemblies/components/runtime）与可选的独立 runtime.json；
  两者并存时对比校验，不一致写入 profile_warning；
- `runtime.emulator == "none"`（或 demo 语义）→ demo_mode（静态展示，不起设备）；
- 输出映射结果：sinks 映射、键名校验报告、画面缺省值（runtime 未声明画面参数）；
- --start：非 demo_mode 时连接网关（127.0.0.1:网关端口）发 start_device 并等待 ack。

画面缺省值表（runtime 未声明时的起始值；正式值由内容线在 v0.2 规范中声明）：
    early-computer → 320x200 @ 25fps；computer → 320x240 @ 24fps；默认 320x240 @ 24fps。
键名规则（设备侧逻辑键）：^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$（点分层次，如 keyboard.key_a）。
sink 映射见 docs/runtime_mapping.md。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import time

LOGICAL_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")
# input_map 对象形态（v0.2）：map → key 名模式（与 02 线 R-086 一致）
MAP_KEY_RE = {
    "keyboard": re.compile(r"^KEY_[A-Z0-9_]+$"),
    "joystick": re.compile(r"^(axis_[xy]|btn[0-9]+|hat_[0-9]+)$"),
    "mouse": re.compile(r"^(motion|btn_left|btn_right|btn_middle|wheel_up|wheel_down)$"),
}
VALID_MAPS = set(MAP_KEY_RE)

# surface 名 → 网关 sink 名（详见 docs/runtime_mapping.md）
SURFACE_TO_SINK = {
    "internal_crt": "main",
    "external_crt": "main",
    "crt_display": "main",
    "terminal": "main",
    "handheld_lcd": "main",
    "led": "led",
    "indicator_lamps": "led",
    "speaker": "speaker",
}

# 类别 → (宽, 高, fps) 缺省（依据显示面历史惯例；v0.2 规范将删除此表）
CATEGORY_DEFAULTS = {
    "early-computer": (320, 200, 25),
    "computer": (320, 240, 24),
    "personal-computer": (320, 240, 24),
    "console": (320, 240, 24),
    "phone": (240, 320, 15),
}


def _read_json(path: str):
    """读 JSON 文件；不存在返回 None，坏 JSON 抛 ValueError。"""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.loads(fh.read())


def _norm_key_map(input_map) -> dict[str, object]:
    if not isinstance(input_map, dict):
        return {}
    return {str(k): v for k, v in input_map.items()}


def _key_entry(action: str, desc) -> dict | None:
    """把单个 input_map 条目归一为 {action, token} 或 {action, map, key}；非法返回 None。"""
    if isinstance(desc, str):
        if LOGICAL_KEY_RE.match(desc):
            return {"action": action, "token": desc}
        return None
    if isinstance(desc, dict):
        mp = desc.get("map")
        key = str(desc.get("key", ""))
        if mp in VALID_MAPS and MAP_KEY_RE[mp].match(key):
            return {"action": action, "map": mp, "key": key}
        return None
    return None


def _validate_keys(input_map) -> dict:
    unknown: list[dict] = []
    total = 0
    for action, desc in _norm_key_map(input_map).items():
        total += 1
        if _key_entry(action, desc) is None:
            unknown.append({"action": action, "desc": str(desc)[:80]})
    return {"total": total, "unknown": unknown}


def _first_key(input_map) -> dict | None:
    for action, desc in _norm_key_map(input_map).items():
        entry = _key_entry(action, desc)
        if entry is not None:
            return entry
    return None


def _map_sinks(output_sinks) -> dict:
    sink_entries = []
    mapped = []
    for entry in output_sinks or []:
        if not isinstance(entry, dict):
            continue
        surface = str(entry.get("surface", ""))
        target = SURFACE_TO_SINK.get(surface, "main")
        if str(entry.get("type", "")) == "audio":
            target = "speaker"
        sink_entries.append({"surface": surface, "type": entry.get("type"),
                             "format": entry.get("format"), "mapped_to": target})
        if target not in mapped:
            mapped.append(target)
    if not mapped:
        mapped = ["main"]
    return {"entries": sink_entries, "mapped": mapped}


def build_mapping(package_dir: str) -> dict:
    meta_path = os.path.join(package_dir, "meta.json")
    runtime_path = os.path.join(package_dir, "runtime.json")
    meta = _read_json(meta_path)
    if not isinstance(meta, dict):
        raise ValueError("无法读取或解析 %s" % meta_path)
    top_meta = meta.get("meta", {})
    runtime_in_meta = meta.get("runtime")
    runtime_file = _read_json(runtime_path)
    warnings: list[str] = []

    runtime = runtime_in_meta
    if runtime_file is not None:
        if runtime_in_meta is not None and runtime_in_meta != runtime_file:
            warnings.append("runtime.json 与 meta.json.runtime 不一致（以独立 runtime.json 为准）")
            runtime = runtime_file
        elif runtime_in_meta is None:
            runtime = runtime_file
    if not isinstance(runtime, dict):
        raise ValueError("内容包缺少 runtime 配置: %s" % package_dir)

    emulator = str(runtime.get("emulator", "none"))
    demo_mode = emulator in ("none", "demo", "")
    device_id = str(top_meta.get("id") or os.path.basename(package_dir.rstrip("/\\")))
    category = str(top_meta.get("category", ""))
    width, height, fps = CATEGORY_DEFAULTS.get(category, (320, 240, 24))

    sink_report = _map_sinks(runtime.get("output_sinks"))
    keys_report = _validate_keys(runtime.get("input_map"))
    first_key = _first_key(runtime.get("input_map"))

    config = {
        "width": width, "height": height, "fps": float(fps),
        "frame_codec": "raw",
        "sinks": sink_report["mapped"],
    }
    return {
        "device_id": device_id,
        "package": os.path.abspath(package_dir),
        "demo_mode": demo_mode,
        "emulator": emulator,
        "system": runtime.get("system"),
        "media_hint": runtime.get("media_hint"),
        "bios_required": runtime.get("bios_required", False),
        "slot": runtime.get("slot"),   # TASK-46B：槽位提示（emulator_class/media_class/bios_hint，仅提示）
        "category": category,
        "config": config,
        "sinks": sink_report["entries"],
        "keys": keys_report,
        "first_key": first_key,
        "profile_warning": ("; ".join(warnings) if warnings else None),
    }


def _gateway_rpc(port: int, msg: dict, wait_types: tuple[str, ...],
                 timeout: float = 20.0) -> dict:
    """极简网关单次 RPC：连接 → 发一条 → 读到期望类型即返回。"""
    sock = socket.create_connection(("127.0.0.1", port), timeout=5.0)
    sock.settimeout(0.5)
    sock.sendall((json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8"))
    buf = ""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            data = sock.recv(65536)
        except socket.timeout:
            continue
        except OSError:
            break
        if not data:
            break
        buf += data.decode("utf-8", errors="replace")
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") in wait_types:
                sock.close()
                return obj
    sock.close()
    raise TimeoutError("网关 RPC 超时（等待 %s）" % (wait_types,))


def start_device(mapping: dict, port: int, device_id: str = "") -> dict:
    if mapping.get("demo_mode"):
        return {"type": "skipped", "reason": "demo_mode"}
    did = device_id or (mapping["device_id"] + "-run")
    ack = _gateway_rpc(port, {
        "type": "start_device", "emulator": "fake", "device_id": did,
        "config": mapping["config"],
    }, ("start_device_ack", "error"))
    return ack


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="内容包 runtime → 网关配置 映射桥")
    parser.add_argument("package_dir", help="内容包目录（含 meta.json）")
    parser.add_argument("--json", action="store_true", help="仅输出映射 JSON")
    parser.add_argument("--start", action="store_true", help="实际经网关启动 fake 设备")
    parser.add_argument("--gateway-port", type=int, default=7331)
    parser.add_argument("--device-id", default="")
    args = parser.parse_args(argv)

    try:
        mapping = build_mapping(args.package_dir)
    except ValueError as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2

    if args.start:
        result = start_device(mapping, args.gateway_port, args.device_id)
        mapping["start_result"] = result

    if args.json:
        print(json.dumps(mapping, ensure_ascii=False, indent=2))
        return 0

    print("设备 %s（%s）" % (mapping["device_id"], mapping["system"]))
    print("  模式: %s" % ("demo（静态展示）" if mapping["demo_mode"] else "可运行（接线候选 %s）" % mapping["emulator"]))
    print("  媒体提示: %s  BIOS: %s" % (mapping["media_hint"], mapping["bios_required"]))
    print("  sinks: %s" % [s["mapped_to"] for s in mapping["sinks"]])
    print("  键名: 共 %d 个，未知 %d" % (mapping["keys"]["total"], len(mapping["keys"]["unknown"])))
    for item in mapping["keys"]["unknown"]:
        print("    [未知键] %s -> %s" % (item["action"], item["desc"]))
    if mapping["first_key"]:
        fk = mapping["first_key"]
        if "token" in fk:
            print("  首键: %s -> %s" % (fk["action"], fk["token"]))
        else:
            print("  首键: %s -> {%s: %s}" % (fk["action"], fk["map"], fk["key"]))
    print("  网关 config: %s" % json.dumps(mapping["config"], ensure_ascii=False))
    if mapping["profile_warning"]:
        print("  警告: %s" % mapping["profile_warning"])
    return 0


if __name__ == "__main__":
    sys.exit(main())