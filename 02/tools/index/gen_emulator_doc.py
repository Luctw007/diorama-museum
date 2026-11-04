#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆项目组 (Hako Electronic Museum Project)
# SPDX-License-Identifier: MIT
"""模拟器档案文档生成器（TASK-72B）：registry.json → 两份文档。

    docs/emulators_registry.md           人类可读档案（仓库内）
    <work>/其它信息/模拟器清单_<日期>.md   桌面清单（替换手写版，自动刷新）

三方同源：01 线 slot 系统读 backend_type/media_classes，05 线 emu-eco 读 target_devices/risks，
桌面清单读 name/license——均由此母表渲染，不各自维护副本。

用法：
    python gen_emulator_doc.py
"""
from __future__ import annotations

import datetime
import json
import os
import sys

REGISTRY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "emulators_registry.json")


def load():
    with open(REGISTRY, "r", encoding="utf-8") as f:
        return json.load(f)


def render_registry_md(data) -> str:
    lines = [
        "# 模拟器官方档案（emulators_registry.md，人类可读版）", "",
        "> 本文件由 `tools/index/gen_emulator_doc.py` 从 `emulators_registry.json` 自动生成，手改无效。",
        "> 定位：槽位 manifest 登记母表，供 01 线 slot 系统、05 线 emu-eco、桌面《模拟器清单》三方同源。",
        "> 状态：bone=成熟可接入 / reserved=预留待映射 / researched=调研中。", "",
    ]
    for e in data:
        lic = e["license"]
        lines.append("## " + e["sim_id"])
        lines.append("- 名称：" + e["name"])
        lines.append("- 后端类型：" + e["backend_type"] + "　|　状态：" + e["status"] + "　|　后端：" + e.get("backend_status", "预留"))
        if e.get("module"):
            lines.append("- 模块：" + e["module"])
        lines.append("- 网关登记键：" + (e.get("gateway_key") or "（未内置）")
                       + "　|　槽位 manifest：" + ("齐" if e.get("slot_manifest") else "无")
                       + "　|　CI 涉及：" + ("是" if e.get("ci_involved") else "否"))
        lines.append("- 目标设备：" + "、".join(e["target_devices"]))
        lines.append("- 许可：" + str(lic.get("spdx") or "需核实") + "　|　URL：" + str(lic.get("source_url") or "（需核实）"))
        lines.append("- 介质类目：" + ("、".join(e["media_classes"]) if e["media_classes"] else "（无）"))
        lines.append("- 风险：" + ("、".join(e["risks"]) if e["risks"] else "（无）"))
        lines.append("")
    return "\n".join(lines) + "\n"


def render_desktop_md(data, date_str: str) -> str:
    lines = [
        "# 模拟器清单（项目需要 · 汇总版 · 自动生成）", "",
        "> 生成日期：" + date_str + "　|　来源：`02/repo/docs/emulators_registry.json`（模拟器官方档案母表，自动生成，替换手写版）",
        "> 说明：全部「需核实」按红线只做清单级引用，二进制由用户在 `slots/emulators/<id>/` 自备。", "",
        "## 1. 按后端类型汇总", "",
        "| 模拟器 | 目标设备 | backend_type | 许可 | media_class | 状态 |",
        "|---|---|---|---|---|---|",
    ]
    order = ["mame", "simh", "stella", "mesen", "native", "mobile", "dedicated"]
    for bt in order:
        for e in data:
            if e["backend_type"] != bt:
                continue
            lic = e["license"]
            lines.append(f"| {e['name']} | {'、'.join(e['target_devices'])} | {bt} | "
                         f"{lic.get('spdx') or '需核实'} | {'/'.join(e['media_classes']) or '无'} | {e['status']} |")
    lines += ["", "## 2. 需核实清单（许可未确证）", ""]
    lines.append("| 模拟器 | 许可 | URL |")
    lines.append("|---|---|---|")
    for e in data:
        lic = e["license"]
        if lic.get("spdx") in (None, "需核实") or lic.get("last_checked") == "需核实":
            lines.append(f"| {e['name']} | {lic.get('spdx') or '需核实'} | {lic.get('source_url') or '（需核实）'} |")
    lines += ["", "## 3. media_class 交叉索引", ""]
    lines.append("| 目标设备 | 允许 media_class |")
    lines.append("|---|---|")
    for e in data:
        for dev, mcs in (e.get("media_classes_allowed") or {}).items():
            lines.append(f"| {dev} | {'、'.join(mcs) if mcs else '无'} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    data = load()
    today = datetime.date.today().strftime("%Y%m%d")
    date_str = datetime.date.today().strftime("%Y-%m-%d")

    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    work = os.path.dirname(os.path.dirname(repo))
    out_reg = os.path.join(repo, "docs", "emulators_registry.md")
    out_desktop = os.path.join(work, "其它信息", f"模拟器清单_{today}.md")

    with open(out_reg, "w", encoding="utf-8") as f:
        f.write(render_registry_md(data))
    os.makedirs(os.path.dirname(out_desktop), exist_ok=True)
    with open(out_desktop, "w", encoding="utf-8") as f:
        f.write(render_desktop_md(data, date_str))

    print(f"已生成 {len(data)} 条目的两份文档：")
    print("  " + out_reg)
    print("  " + out_desktop)
    return 0


if __name__ == "__main__":
    sys.exit(main())
