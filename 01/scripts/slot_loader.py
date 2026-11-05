# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""模拟器插槽系统装载器（TASK-46A）。

类 Batocera 体验：二进制 + manifest 放入约定目录即自动注册进网关 EMULATORS。
目录契约（详见 slots/README.md）：
  slots/emulators/<slot_id>/manifest.json + 二进制（可选）
  slots/media/<media_class>/<device_class>/<slot_id>/   （介质，永不下载）

用法:
  python scripts/slot_loader.py --list        # 当前槽位表
  python scripts/slot_loader.py --json        # 机器可读
在 gateway.py 启动时调用 apply_slots(EMULATORS) 完成自动注册。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLOTS_ROOT = os.path.join(REPO, "slots", "emulators")
MEDIA_ROOT = os.path.join(REPO, "slots", "media")

# backend_type -> 后端模块（真实模拟器接入时在此扩展；缺失值表示"暂无后端，仅注册占位"）
BACKEND_TYPE_MODULE = {
    "native": "gw.emulators.fake_emulator",
    "mame": "gw.emulators.mame_apple2",
    "simh": "gw.emulators.simh_pdp8",     # TASK-161-A：后端模块已落地（骨架）
    "stella": "gw.emulators.stella",     # TASK-161-B：后端模块已落地（骨架）
    "mesen": None,     # 预留
    "mobile": None,    # 预留（手机类）
    "dedicated": None, # 预留（家电通用类）
}

# TASK-76A：运行时 emulator 语义名 → 规范槽位 id（单一真相源别名表）
ALIASES = {"mame": "mame-apple2", "simh": "simh-pdp8"}


def canonical(slot_or_emulator: str) -> str:
    """语义名归一：如内容包 emulator=mame → 槽位 id mame-apple2。"""
    return ALIASES.get(str(slot_or_emulator), str(slot_or_emulator))


def builtin_entries() -> dict[str, dict]:
    """网关注册表内置 EMULATORS（单一真相源的兜底层；延迟导入防止与网关互环）。"""
    if REPO not in sys.path:  # scripts 目录方式运行时也保证能导入 gw 包
        sys.path.insert(0, REPO)
    try:
        from gw import gateway  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001  网关不可用时退化为纯槽位扫描
        print("[slot_loader] 无法导入网关注册表（%s），仅用槽位扫描区" % exc,
              file=sys.stderr)
        return {}
    return {str(k): dict(v)
            for k, v in getattr(gateway, "EMULATORS", {}).items()}


def load_manifests() -> list[dict]:
    """扫描 slots/emulators/*/manifest.json，返回原始 manifest 列表（含临时 slot_id）。"""
    out: list[dict] = []
    if not os.path.isdir(SLOTS_ROOT):
        return out
    for name in sorted(os.listdir(SLOTS_ROOT)):
        mpath = os.path.join(SLOTS_ROOT, name, "manifest.json")
        if not os.path.isfile(mpath):
            continue
        try:
            with open(mpath, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print("[slot_loader] manifest 解析失败 %s: %s" % (name, exc),
                  file=sys.stderr)
            continue
        data.setdefault("slot_id", name)
        out.append(data)
    return out


def resolve_entry(manifest: dict) -> dict | None:
    """manifest → 网关注册表条目；无法映射（后端模块缺失）返回 None。"""
    slot_id = manifest.get("slot_id")
    backend = manifest.get("backend_type")
    module = BACKEND_TYPE_MODULE.get(backend)
    if module is None:
        return None
    entry: dict = {
        "desc": manifest.get("description", slot_id),
        "license": manifest.get("license", "未声明（需核实）"),
        "module": module,
        "device_class": manifest.get("device_class", "other"),
        "media_classes": manifest.get("media_classes", []),
    }
    binary = manifest.get("binary")
    if binary:   # 相对 slots/emulators/<slot_id>/ 的二进制名
        entry["binary_hint"] = os.path.join("slots", "emulators", slot_id, binary)
    if manifest.get("binary_env"):
        entry["binary_env"] = manifest["binary_env"]
    if manifest.get("keymap"):
        entry["keymap"] = manifest["keymap"]
    return entry


def slots_available() -> dict[str, dict]:
    """返回 {槽位 id: 注册条目 + binary_path} 的**单一真相源合并视图**（TASK-76A）。

    合并规则：槽位扫描区 manifests 先入表；网关注册表内置 EMULATORS 以"内置优先"
    覆盖同名条目（槽位声明只补充内置缺失的 device_class/media_classes 等字段）。
    后端模块未映射的 manifest（如 simh，模块预留）不再消失——有内置同名登记则
    并入视图（无 module 字段，下游可判"后端模块未实现"）。
    """
    builtins = builtin_entries()
    table: dict[str, dict] = {}
    for manifest in load_manifests():
        entry = resolve_entry(manifest)
        if entry is None:
            if manifest.get("slot_id") in builtins:
                continue   # 内置兜底同名槽位，下方并入视图
            print("[slot_loader] 槽位 %s 后端类型 %s 暂无模块映射，跳过注册"
                  % (manifest.get("slot_id"), manifest.get("backend_type")),
                  file=sys.stderr)
            continue
        table[str(manifest.get("slot_id"))] = entry
    for bid, be in builtins.items():          # 内置优先覆盖
        merged = dict(be)
        for k, v in table.get(bid, {}).items():
            if k != "binary_path" and k not in merged:
                merged[k] = v
        table[bid] = merged
    for entry in table.values():
        entry["binary_path"] = _binary_path(entry)
    return table


def _binary_path(entry: dict) -> str | None:
    hint = entry.get("binary_hint")
    if not hint:
        return None
    base = hint if os.path.isabs(hint) else os.path.join(REPO, hint)
    for cand in (base, base + ".exe"):
        if os.path.isfile(cand):
            return cand
    env_name = entry.get("binary_env")
    if env_name:
        env = os.environ.get(env_name)
        if env and os.path.isfile(env):
            return env
    return None


def apply_slots(registry: dict) -> int:
    """把可用槽位并入网关注册表；返回应用数量。"""
    applied = 0
    for slot_id, entry in slots_available().items():
        if slot_id in registry:
            print("[slot_loader] 槽位 %s 与内置注册同名，跳过（内置优先）" % slot_id,
                  file=sys.stderr)
            continue
        registry[slot_id] = entry
        applied += 1
    return applied


def media_dirs() -> list[str]:
    if not os.path.isdir(MEDIA_ROOT):
        return []
    out = []
    for cls in sorted(os.listdir(MEDIA_ROOT)):
        p1 = os.path.join(MEDIA_ROOT, cls)
        if not os.path.isdir(p1):
            continue
        for dc in sorted(os.listdir(p1)):
            p2 = os.path.join(p1, dc)
            if not os.path.isdir(p2):
                continue
            for sid in sorted(os.listdir(p2)):
                if os.path.isdir(os.path.join(p2, sid)):
                    out.append("%s/%s/%s" % (cls, dc, sid))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="模拟器插槽装载器")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    table = slots_available()
    media = media_dirs()
    if args.json:
        print(json.dumps({"slots": {k: {kk: vv for kk, vv in v.items()
                                        if kk != "module"}
                                    for k, v in table.items()},
                          "media_dirs": media}, ensure_ascii=False, indent=2))
    if args.list or not args.json:
        if not table:
            print("（无可用槽位：把 manifest.json 放入 slots/emulators/<id>/ 即可注册）")
        for sid, entry in table.items():
            reserved = "" if entry.get("module") else "（后端模块预留）"
            if not entry.get("binary_hint"):
                state = "OK(native,无二进制要求)" + reserved
            elif entry["binary_path"]:
                state = "OK(二进制就位)" + reserved
            else:
                state = "MISSING(无二进制)" + reserved
            print("%-18s %-26s %s  [%s]" % (sid, state, entry["desc"][:40],
                                            entry["license"][:30]))
        print("介质目录 %d 个：%s" % (len(media), ", ".join(media) if media else "（空，红线下仅建目录）"))
    return 0


if __name__ == "__main__":
    sys.exit(main())