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
设备包脚手架生成器（TASK-07，v0.2）

用法：
    python scaffold_device.py content/<device-id> --name "曼彻斯特婴儿" \
        --category experimental-computer --era 1948 [--manufacturer "..."]

生成一个**符合《内容包规范 v0.2》的最小合法设备包骨架**，包含：
    content/<device-id>/
    ├── meta.json                  # spec_version=0.2，version=0.1.0，sources 空数组
    ├── runtime.json               # 默认 fake 运行时
    ├── annotations/annotations.json  # 空文档 + 一条示例 role 标注
    ├── THIRD_PARTY.md             # 四档许可表头模板
    ├── README.md                  # 作者填写指引模板
    ├── assemblies/  meshes/  materials/  sounds/   # 空目录

生成完成后自动调用 validate.py 自检，并打印结果（要求 0 FAIL）。
内容填写由后续任务（如 TASK-08）负责，本工具只生成骨架、不写具体内容。

退出码：0=生成且自检全绿；1=自检出现 FAIL；2=参数/环境错误。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

DEVICE_ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

# 默认运行时（v0.2）
DEFAULT_RUNTIME = {
    "emulator": "fake",
    "version": "0.1.0",
    "system": "",
    "media_hint": "none",
    "bios_required": False,
    "bios_guide_url": None,
    "output_sinks": [],
    "input_map": {},
}

EMPTY_DIRS = ["assemblies", "meshes", "materials", "sounds"]


# ---------------------------------------------------------------------------
# 模板
# ---------------------------------------------------------------------------
def meta_template(device_id: str, name_zh: str, name_en: str, category: str,
                  era: int, manufacturer: str, presentation: str, precision: str,
                  emulator: str) -> dict:
    name_obj = {"zh": name_zh}
    if name_en:
        name_obj["en"] = name_en
    return {
        "$schema": "../schema/device_spec.schema.json",
        "meta": {
            "id": device_id,
            "name": name_obj,
            "spec_version": "0.2",
            "version": "0.1.0",
            "engine_min_version": "0.1.0",
            "precision_level": precision,
            "presentation_level": presentation,
            "era": era,
            "manufacturer": manufacturer,
            "description": "",
            "category": category,
            "authors": [],
            "sources": [],
        },
        "assemblies": [
            {
                "id": "whole",
                "name": "整机",
                "role": {
                    "zh": "整机：本设备由脚手架生成，请补充整机概述与结构说明。",
                },
                "transform": {
                    "translation": [0.0, 0.0, 0.0],
                    "rotation": [0.0, 0.0, 0.0, 1.0],
                    "scale": [1.0, 1.0, 1.0],
                },
                "parent": None,
                "children": [],
                "components": [],
                "annotations": ["whole_role"],
                "materials": [],
            }
        ],
        "components": [],
        "runtime": runtime_template(device_id, emulator),
    }


def runtime_template(device_id: str, emulator: str) -> dict:
    rt = dict(DEFAULT_RUNTIME)
    rt["emulator"] = emulator
    rt["system"] = device_id
    return rt


def annotations_template() -> dict:
    return {
        "annotations": [
            {
                "id": "whole_role",
                "type": "role",
                "target": "whole",
                "text": "整机概述：本设备为脚手架自动生成的占位说明，请作者补充该设备的历史地位与结构作用。",
                "sources": [],
            }
        ]
    }


def third_party_template(device_id: str) -> str:
    return f"""# THIRD_PARTY.md — 第三方资产许可清册（{device_id}）

本文件记录 `{device_id}` 内容包中所有资产的来源与许可信息。

> 许可分档四档（见《内容包规范 v0.2》第八章）：
> `公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；
> 自产/原创资产标注为 `原创`。第三方资产**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| （示例）占位网格 | 网格 | 原创 | - | - | 脚手架生成，作者替换 |

## 声明

- 本包未包含任何无授权或版权不明的第三方资产（脚手架初始状态）。
"""


def readme_template(device_id: str, name_zh: str, era: int) -> str:
    return f"""# {name_zh}（{device_id}）

> 设备包骨架（由 `scaffold_device.py` 生成，TASK-07）。**内容填写由后续任务负责。**

## 元数据

- device-id：`{device_id}`
- 名称：{name_zh}
- 年代：{era}
- 规范版本：0.2

## 待办（作者填写）

1. 在 `meta.json` 补充 `intro`/`description`/`sources`（来源 URL 示例格式见下）。
2. 在 `assemblies/`、`meshes/`、`materials/`、`sounds/` 放入真实资产。
3. 在 `annotations/annotations.json` 补充 role/flow/anim 标注（anim 可含 timeline）。
4. 在 `runtime.json` 与 `meta.json.runtime` 同步填写真实的模拟器与 sinks/input_map。
5. 更新 `THIRD_PARTY.md` 许可清册。

## sources 条目示例（填入 meta.json 的 sources 数组）

```json
{{
  "type": "documentation",
  "title": "来源标题",
  "url": "https://example.com/source",
  "license": "public_domain",
  "accessed_at": "2026-10-31"
}}
```

## 校验

```bash
python tools/validate/validate.py content/{device_id}
```
"""


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------
def kebab_to_snake(device_id: str) -> str:
    return device_id.replace("-", "_")


def write_json(path: str, obj: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_text(path: str, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def run_validate(pkg_abs: str) -> int:
    """调用 validate.py 自检，返回退出码。"""
    here = os.path.dirname(os.path.abspath(__file__))
    validate = os.path.join(here, "validate.py")
    proc = subprocess.run(
        [sys.executable, validate, pkg_abs],
        capture_output=True, text=True, encoding="utf-8",
    )
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="设备包脚手架生成器（v0.2）")
    parser.add_argument("device_path", help="content/<device-id> 路径（device-id 由目录名决定）")
    parser.add_argument("--name", required=True, help="设备中文名")
    parser.add_argument("--name-en", default="", help="设备英文名（可选）")
    parser.add_argument("--category", default="placeholder", help="设备类别")
    parser.add_argument("--era", type=int, default=1970, help="年代（年份）")
    parser.add_argument("--manufacturer", default="", help="制造/研制方")
    parser.add_argument("--emulator", default="fake", help="模拟器 id（默认 fake）")
    parser.add_argument("--precision", default="L2", choices=["L1", "L2", "L3", "L4"],
                        help="资产精度分级（默认 L2）")
    parser.add_argument("--presentation", default="C3", choices=["C2", "C3", "C4"],
                        help="展示级（默认 C3）")
    parser.add_argument("--no-check", action="store_true", help="生成后跳过 validate 自检")
    args = parser.parse_args(argv)

    # device-id 取目录名
    pkg_rel = args.device_path.rstrip("/\\")
    device_id = os.path.basename(pkg_rel)
    if not DEVICE_ID_RE.match(device_id):
        sys.stderr.write(f"错误：device-id {device_id!r} 不符合 kebab-case（^[a-z][a-z0-9]*(-[a-z0-9]+)*$）\n")
        return 2
    if not 1800 <= args.era <= 2100:
        sys.stderr.write(f"错误：era={args.era} 超出 1800-2100 范围\n")
        return 2

    pkg_abs = os.path.abspath(pkg_rel)
    os.makedirs(pkg_abs, exist_ok=True)
    for d in EMPTY_DIRS:
        os.makedirs(os.path.join(pkg_abs, d), exist_ok=True)
    os.makedirs(os.path.join(pkg_abs, "annotations"), exist_ok=True)

    write_json(os.path.join(pkg_abs, "meta.json"),
               meta_template(device_id, args.name, args.name_en, args.category,
                             args.era, args.manufacturer, args.presentation,
                             args.precision, args.emulator))
    write_json(os.path.join(pkg_abs, "runtime.json"),
               runtime_template(device_id, args.emulator))
    write_json(os.path.join(pkg_abs, "annotations", "annotations.json"),
               annotations_template())
    write_text(os.path.join(pkg_abs, "THIRD_PARTY.md"), third_party_template(device_id))
    write_text(os.path.join(pkg_abs, "README.md"), readme_template(device_id, args.name, args.era))

    print(f"已生成设备包骨架：{pkg_abs}")

    if args.no_check:
        print("（--no-check：跳过自检）")
        return 0

    print("\n=== validate.py 自检 ===")
    code = run_validate(pkg_abs)
    if code == 0:
        print("自检通过：0 FAIL")
    else:
        print(f"自检未通过：退出码 {code}，请修复上述 FAIL")
    return code


if __name__ == "__main__":
    sys.exit(main())
