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
内容包 v0.1 → v0.2 迁移助手（TASK-17A，纯 stdlib，零第三方依赖）

用途
----
把内容包 `meta.json` 中"可安全机械转换"的本地化相关字段从 v0.1 结构迁到 v0.2：

    meta.name          string        → localized { "zh": 原值, "en": name_en(若有) }
    meta.name_en       string        → 并入 name.en 后删除（R-088）
    assemblies[].role  string        → localized { "zh": 原文 }
    components[].role  string        → localized { "zh": 原文 }
    meta.spec_version  "0.1"         → "0.2"（R-071）
    meta.version       （保持不变）   → 仅提示，不改写

只处理上述"可安全机械转换"字段；其余（intro / era / description / manufacturer 等
v0.2 新增可选字段的缺失，以及 R-084 sink 枚举、R-090 glTF 节点名、input_map 结构
迁移等需要人工判断的内容）一律**进报告不改写**，由作者/对应内容线人工处理。

用法
----
    python migrate_package.py <content-package-path>            # dry-run（默认）
    python migrate_package.py <content-package-path> --apply     # 落盘写入
    python migrate_package.py <content-package-path> --apply --validate   # 写入后自动校验

幂等
----
已迁移（或本就不需要迁移）的包再次运行会报告"无需迁移"并返回退出码 0。

设计说明
--------
- 目标 `spec_version` 取自 v0.2 规范的 schema 常量（`$defs/meta/properties/spec_version`
  的 `const`）。工具默认按 `"0.2"` 处理；若某包仍带 v0.1 schema（`const=="0.1"`），
  迁移目标仍是规范最新版 `"0.2"`（不读取旧 schema 常量来"降级"目标）。
- `meta.version` 按 SemVer 属于"内容包自身版本"，迁移是机械改结构、不构成语义发布，
  因此**默认不自动递增**，仅在报告中提示作者可考虑迁移性小版本（如 1.0.0 → 1.1.0）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
# 规范 v0.2 的 spec_version 目标值（对应 schema `$defs/meta/properties/spec_version.const`）
TARGET_SPEC_VERSION = "0.2"

# 迁移性小版本提示：报告 §2 建议的 version 迁移目标（仅提示，不自动改写）
SUGGESTED_VERSION_HINT = "1.1.0"

# 相对于脚本定位 validate.py 的默认路径
VALIDATE_REL = os.path.join("..", "validate", "validate.py")


# ---------------------------------------------------------------------------
# 迁移计划（纯数据：描述 diff，不直接改写）
# ---------------------------------------------------------------------------
class Change:
    """单条变更描述。kind ∈ {replace, add, remove, hint}。"""
    __slots__ = ("kind", "path", "old", "new")

    def __init__(self, kind: str, path: str, old, new):
        self.kind = kind
        self.path = path
        self.old = old
        self.new = new


class MigrationPlan:
    """一个包的迁移计划：变更列表 + 不改写的提示列表。"""

    def __init__(self, package_path: str):
        self.package_path = package_path
        self.changes: list[Change] = []
        self.notes: list[str] = []

    @property
    def needs_migration(self) -> bool:
        return bool(self.changes)

    def add(self, kind: str, path: str, old, new):
        self.changes.append(Change(kind, path, old, new))

    def note(self, text: str):
        self.notes.append(text)


# ---------------------------------------------------------------------------
# 分析：读 meta.json，产出迁移计划（不写文件）
# ---------------------------------------------------------------------------
def _is_str(v) -> bool:
    return isinstance(v, str)


def _localize_name(name_value, name_en, plan: MigrationPlan, path: str):
    """meta.name 的 localize 逻辑，返回 (new_name_value, name_en_removed: bool)。

    - name 为 string → {"zh": name}，若存在 name_en 则并入 en 并删除 name_en。
    - name 已为 dict  → 若存在 name_en，按 R-088 并入 en（缺失或一致时），并删除 name_en；
                        若 name.en 与 name_en 冲突，则保留二者进报告（R-088 会兜底）。
    """
    removed = False

    if _is_str(name_value):
        new_name = {"zh": name_value}
        plan.add("replace", f"{path}.name", name_value, new_name)
        if _is_str(name_en):
            new_name["en"] = name_en
            plan.add("remove", f"{path}.name_en", name_en, None)
            removed = True
        elif name_en is not None:
            plan.note(f"{path}.name_en 非字符串（{name_en!r}），未并入 name.en，保留待人工处理")
        return new_name, removed

    # name 已是 dict（可能半迁移状态）
    if isinstance(name_value, dict):
        if name_en is not None:
            existing_en = name_value.get("en")
            if existing_en is None:
                name_value = dict(name_value)
                name_value["en"] = name_en
                plan.add("replace", f"{path}.name.en", None, name_en)
                plan.add("remove", f"{path}.name_en", name_en, None)
                removed = True
            elif existing_en == name_en:
                plan.add("remove", f"{path}.name_en", name_en, None)
                removed = True
            else:
                plan.note(
                    f"{path}.name.en={existing_en!r} 与 name_en={name_en!r} 冲突，"
                    "保留 name_en 交 R-088 兜底，不自动覆盖"
                )
        return name_value, removed

    plan.note(f"{path}.name 类型异常（{name_value!r}），跳过")
    return name_value, removed


def build_plan(package_path: str) -> MigrationPlan:
    """读取 meta.json 并生成迁移计划。meta.json 缺失/非法时抛异常。"""
    meta_path = os.path.join(package_path, "meta.json")
    if not os.path.isfile(meta_path):
        raise FileNotFoundError(f"缺少 meta.json：{package_path}")

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    plan = MigrationPlan(package_path)

    # -- meta.name / name_en / spec_version / version ---------------------
    m = meta.get("meta")
    if not isinstance(m, dict):
        raise ValueError("meta.json 根对象缺少 'meta' 字典")

    # name / name_en（_localize_name 内部负责登记 plan 变更，不直接改写 meta）
    _localize_name(m.get("name"), m.get("name_en"), plan, "meta")

    # spec_version
    spec = m.get("spec_version")
    if spec == TARGET_SPEC_VERSION:
        pass  # 已是最新
    elif spec == "0.1":
        plan.add("replace", "meta.spec_version", spec, TARGET_SPEC_VERSION)
    else:
        plan.note(f"meta.spec_version={spec!r} 既非 0.1 也非 0.2，不改写，待人工确认")

    # version：保持，仅提示
    ver = m.get("version")
    if ver is not None:
        plan.note(f"meta.version={ver!r} 保持不变（建议迁移性小版本 {SUGGESTED_VERSION_HINT}，需人工确认）")

    # 可选字段缺失提示（进报告，不改写）
    if "intro" not in m:
        plan.note("meta.intro 缺失（v0.2 可选新增字段，未改写）")
    if "era" not in m:
        plan.note("meta.era 缺失（v0.2 可选新增字段，未改写）")

    # -- assemblies[].role -----------------------------------------------
    assemblies = meta.get("assemblies")
    if not isinstance(assemblies, list):
        raise ValueError("meta.json 缺少 'assemblies' 数组")
    asm_role_count = 0
    for i, a in enumerate(assemblies):
        if not isinstance(a, dict):
            continue
        aid = a.get("id", f"[{i}]")
        role = a.get("role")
        if _is_str(role):
            plan.add("replace", f"assemblies[{aid}].role", role, {"zh": role})
            asm_role_count += 1
        elif role is None:
            plan.note(f"assemblies[{aid}].role 缺失（必填，未改写）")
    if asm_role_count:
        plan.note(f"assemblies[].role 共 {asm_role_count} 条由 string 迁 localized")

    # -- components[].role ------------------------------------------------
    components = meta.get("components")
    if not isinstance(components, list):
        raise ValueError("meta.json 缺少 'components' 数组")
    comp_role_count = 0
    for i, c in enumerate(components):
        if not isinstance(c, dict):
            continue
        cid = c.get("id", f"[{i}]")
        role = c.get("role")
        if _is_str(role):
            plan.add("replace", f"components[{cid}].role", role, {"zh": role})
            comp_role_count += 1
        elif role is None:
            plan.note(f"components[{cid}].role 缺失（必填，未改写）")
    if comp_role_count:
        plan.note(f"components[].role 共 {comp_role_count} 条由 string 迁 localized")

    return plan


# ---------------------------------------------------------------------------
# 应用：按计划改写 meta.json（写回）
# ---------------------------------------------------------------------------
def apply_plan(package_path: str, plan: MigrationPlan):
    """按计划把 meta.json 写到磁盘。仅改 meta.json，不触碰 runtime.json。"""
    meta_path = os.path.join(package_path, "meta.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    m = meta["meta"]

    # 1) name / name_en
    name_en = m.get("name_en")
    if _is_str(m.get("name")):
        new_name = {"zh": m["name"]}
        if _is_str(name_en):
            new_name["en"] = name_en
            m.pop("name_en", None)
        m["name"] = new_name
    elif isinstance(m.get("name"), dict):
        if name_en is not None:
            existing = m["name"].get("en")
            if existing is None or existing == name_en:
                m["name"]["en"] = name_en
                m.pop("name_en", None)
            # 冲突时保留，交 R-088 兜底

    # 2) spec_version
    if m.get("spec_version") == "0.1":
        m["spec_version"] = TARGET_SPEC_VERSION

    # 3) assemblies[].role
    for a in meta.get("assemblies", []):
        if isinstance(a, dict) and _is_str(a.get("role")):
            a["role"] = {"zh": a["role"]}

    # 4) components[].role
    for c in meta.get("components", []):
        if isinstance(c, dict) and _is_str(c.get("role")):
            c["role"] = {"zh": c["role"]}

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def _fmt(v) -> str:
    if v is None:
        return "<删除>"
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, str):
        s = v
        if len(s) > 40:
            s = s[:37] + "..."
        return f"{s!r}"
    return repr(v)


def render_diff(plan: MigrationPlan) -> str:
    """渲染单包变更 diff 摘要。"""
    pkg = os.path.basename(os.path.normpath(plan.package_path))
    lines = [f"== {pkg} =="]

    if not plan.needs_migration:
        lines.append("  无需迁移（已是 v0.2 结构）")
        for n in plan.notes:
            lines.append(f"  · 提示：{n}")
        return "\n".join(lines)

    for ch in plan.changes:
        if ch.kind == "replace":
            lines.append(f"  ~ {ch.path}")
            lines.append(f"      - {_fmt(ch.old)}")
            lines.append(f"      + {_fmt(ch.new)}")
        elif ch.kind == "remove":
            lines.append(f"  - {ch.path}")
            lines.append(f"      (删除：{_fmt(ch.old)})")
        elif ch.kind == "add":
            lines.append(f"  + {ch.path}")
            lines.append(f"      (新增：{_fmt(ch.new)})")
        elif ch.kind == "hint":
            lines.append(f"  ? {ch.path}  {_fmt(ch.old)} → {_fmt(ch.new)}")

    for n in plan.notes:
        lines.append(f"  · 提示：{n}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 校验：调用 validate.py 并返回最后一行
# ---------------------------------------------------------------------------
def run_validate(package_path: str, validate_script: str) -> str:
    """调用 validate.py 校验包，返回 stdout 的最后一行。"""
    script = os.path.abspath(validate_script)
    if not os.path.isfile(script):
        raise FileNotFoundError(f"找不到校验器：{script}")
    proc = subprocess.run(
        [sys.executable, script, package_path],
        capture_output=True, text=True, encoding="utf-8",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else f"(无输出，退出码 {proc.returncode})"


# ---------------------------------------------------------------------------
# 单包流程
# ---------------------------------------------------------------------------
def migrate_package(package_path: str, apply: bool, validate: bool,
                    validate_script: str) -> int:
    """对一个包执行 dry-run / apply / validate，返回该包退出码。"""
    package_path = os.path.abspath(package_path)
    if not os.path.isdir(package_path):
        sys.stderr.write(f"错误：路径不是目录：{package_path}\n")
        return 2

    try:
        plan = build_plan(package_path)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        sys.stderr.write(f"错误：读取/分析 {package_path} 失败：{e}\n")
        return 2

    print(render_diff(plan))
    print()

    if not plan.needs_migration:
        return 0

    if apply:
        apply_plan(package_path, plan)
        print("  [apply] 已写入 meta.json")
        # apply 后重新构建计划验证幂等（应变为"无需迁移"）
        try:
            plan2 = build_plan(package_path)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            sys.stderr.write(f"错误：apply 后复检失败：{e}\n")
            return 2
        if plan2.needs_migration:
            sys.stderr.write("警告：apply 后复检仍发现待迁移项（非幂等），请检查：\n")
            print(render_diff(plan2))
        else:
            print("  [apply] 复检：无需迁移（幂等 OK）")
        print()

        if validate:
            try:
                last = run_validate(package_path, validate_script)
            except (OSError, FileNotFoundError) as e:
                sys.stderr.write(f"错误：校验失败：{e}\n")
                return 2
            print(f"  [validate] {last}")
            print()
    else:
        print("  [dry-run] 未写入（加 --apply 落盘）")
        print()

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="内容包 v0.1 → v0.2 迁移助手（TASK-17A，纯 stdlib）",
    )
    p.add_argument("package_path", help="content/<device-id>/ 目录（或含多个包的上级目录）")
    p.add_argument("--apply", action="store_true", help="落盘写入 meta.json（默认 dry-run）")
    p.add_argument("--validate", action="store_true", help="apply 后自动调用 validate.py 并打印最后 1 行")
    p.add_argument("--validate-script", default=None,
                   help="validate.py 路径（默认相对本脚本定位 tools/validate/validate.py）")
    p.add_argument("--dry-run", action="store_true",
                   help="显式指定 dry-run（默认行为，无 --apply 即 dry-run）")
    return p


def _collect_packages(path: str) -> list[str]:
    """若 path 是包目录（含 meta.json）返回 [path]；若是上级目录则返回其下所有包目录。"""
    if os.path.isfile(os.path.join(path, "meta.json")):
        return [path]
    pkgs = []
    for name in sorted(os.listdir(path)):
        sub = os.path.join(path, name)
        if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, "meta.json")):
            pkgs.append(sub)
    return pkgs


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.validate_script:
        validate_script = args.validate_script
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        validate_script = os.path.normpath(os.path.join(script_dir, VALIDATE_REL))

    packages = _collect_packages(args.package_path)
    if not packages:
        sys.stderr.write(f"错误：未在 {args.package_path} 找到任何含 meta.json 的内容包\n")
        return 2

    rc = 0
    for i, pkg in enumerate(packages):
        if len(packages) > 1:
            print("#" * 60)
        code = migrate_package(pkg, args.apply, args.validate, validate_script)
        rc = max(rc, code)

    return rc


if __name__ == "__main__":
    sys.exit(main())
