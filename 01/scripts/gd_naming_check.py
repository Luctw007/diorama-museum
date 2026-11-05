# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""gd 命名纪律静态门禁（TASK-118）：把《规范增补 v0.6.3》v0.6.3-01/02/03 落成引擎外
文本扫描，与 gd_symbol_check.py 并列挂入门禁链（verify_all gd 域）。

检查点（附录 A）：
  GN-01  gd 内 `func <name>(` 的 <name> 命中 Object/Node 原生方法黑名单；
  GN-02  `var <id> := <三元>` 且左侧未显式标注类型（可能推断出 Variant，警告即错误）；
  GN-03  类型标注 `<Type>` 未在工程内任何 gd 声明 `class_name <Type>`，且不在
         Godot 内置类型允许清单中。
边界：仅静态文本匹配、不解析 GDScript 语义（误报按需扩白名单/允许清单，不改被测脚本）。

用法：python 01/scripts/gd_naming_check.py [--dir <godot_root>]
输出：逐条 `FAIL GN-x <文件>:<行> <消息>`；末尾 `FAIL n` 计数行。
退出码：0=全过；1=存在 FAIL。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# v0.6.3-01 黑名单（非穷举）：Object/Node 原生方法名，命中即 FAIL
NATIVE_METHODS = {
    "get_meta", "get_index", "get_name", "get_parent", "get_class", "get_path",
    "get_child", "get_node", "set_meta", "set_name", "has_method", "has_signal",
}

# Godot 4.x 内置类型（GN-03 放行清单；非穷举，遇到确认为引擎类型的再补）
BUILTIN_TYPES = {
    "void", "bool", "int", "float", "String", "StringName", "NodePath",
    "Vector2", "Vector2i", "Vector3", "Vector3i", "Vector4", "Quaternion",
    "Rect2", "Rect2i", "Color", "AABB", "Basis", "Transform2D", "Transform3D",
    "Plane", "RID", "Callable", "Signal", "Array", "Dictionary", "Variant",
    "PackedByteArray", "PackedInt32Array", "PackedInt64Array",
    "PackedFloat32Array", "PackedFloat64Array", "PackedStringArray",
    "PackedVector2Array", "PackedVector3Array", "PackedColorArray",
    "Node", "Node2D", "Node3D", "CanvasItem", "CanvasLayer", "Control",
    "Label", "Button", "CheckButton", "ItemList", "HSlider", "Panel",
    "PanelContainer", "VBoxContainer", "HBoxContainer", "MarginContainer",
    "Camera3D", "MeshInstance3D", "RefCounted", "Object", "Resource",
    "PackedScene", "Material", "StandardMaterial3D", "BaseMaterial3D",
    "Mesh", "BoxMesh", "PlaneMesh", "QuadMesh", "ImmediateMesh", "Image",
    "ImageTexture", "Texture2D", "Font", "InputEvent", "InputEventKey",
    "InputEventMouseButton", "InputEventMouseMotion", "FileAccess",
    "DirAccess", "JSON", "ResourceLoader", "StreamPeerTCP", "Time",
    "AudioStream", "AudioStreamPlayer", "AudioStreamWAV",
    "TextServer", "ProjectSettings", "OS", "Engine",
}

FUNC_RE = re.compile(r"^func\s+(\w+)\s*\(", re.M)
CLASSNAME_RE = re.compile(r"^class_name\s+(\w+)", re.M)
BARE_INFER_RE = re.compile(r"^\s*var\s+(\w+)\s*:=")
TYPED_VAR_RE = re.compile(r"^\s*var\s+\w+\s*:\s*([A-Za-z_]\w*)")
TYPED_CONST_RE = re.compile(r"^\s*const\s+(\w+)\s*:\s*([A-Za-z_]\w*)")
RETURN_TYPE_RE = re.compile(r"^func\s+\w+\(([^)]*)\)(\s*->\s*([A-Za-z_]\w*))?", re.M)
PARAM_TYPE_RE = re.compile(r":\s*([A-Z][A-Za-z0-9_]*)")

fails = 0


def fail(rule: str, rel: str, lineno: int, msg: str) -> None:
    global fails
    print("FAIL %s %s:%d %s" % (rule, rel, lineno, msg))
    fails += 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="gd 命名纪律静态门禁")
    ap.add_argument("--dir", default=os.path.join(REPO, "godot"))
    args = ap.parse_args(argv)

    gd_dir = os.path.join(args.dir, "scripts")
    files = sorted(f for f in os.listdir(gd_dir) if f.endswith(".gd"))
    texts: dict[str, list[str]] = {}
    func_names: set[str] = set()
    class_names: set[str] = set()

    for f in files:
        with open(os.path.join(gd_dir, f), encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        texts[f] = lines
        for ln in lines:
            m = CLASSNAME_RE.match(ln.strip())
            if m:
                class_names.add(m.group(1))
            m = FUNC_RE.match(ln.strip())
            if m:
                func_names.add(m.group(1))

    for f in files:
        rel = "godot/scripts/" + f
        for i, line in enumerate(texts[f], start=1):
            s = line.strip()
            # ---- GN-01 方法名与原生冲突
            m = FUNC_RE.match(s)
            if m and m.group(1) in NATIVE_METHODS:
                fail("GN-01", rel, i, "方法名 %s 与原生冲突" % m.group(1))
            # ---- GN-02 裸 := 推断（三元）
            m = BARE_INFER_RE.match(line)
            if m:
                rhs = line.split(":=", 1)[1]
                if re.search(r"\bif\b.*\belse\b", rhs):
                    fail("GN-02", rel, i, ":= 推断 Variant 未标注类型（%s）" % m.group(1))
            # ---- GN-03 类型标注未注册
            types_in_line: list[str] = []
            mv = TYPED_VAR_RE.match(line)
            if mv:
                types_in_line.append(mv.group(1))
            mc = TYPED_CONST_RE.match(line)
            if mc and mc.group(2)[0].isupper():
                types_in_line.append(mc.group(2))
            for t in types_in_line:
                if t not in BUILTIN_TYPES and t not in class_names:
                    fail("GN-03", rel, i, "类型 %s 未注册 class_name" % t)
        # GN-03：函数参数与返回类型
        body = "\n".join(texts[f])
        for m in RETURN_TYPE_RE.finditer(body):
            params = m.group(1)
            ret = m.group(3)
            for pm in PARAM_TYPE_RE.finditer(params):
                t = pm.group(1)
                if t not in BUILTIN_TYPES and t not in class_names:
                    fail("GN-03", rel, body[:m.start()].count("\n") + 1,
                         "类型 %s 未注册 class_name（参数）" % t)
            if ret and ret not in BUILTIN_TYPES and ret not in class_names:
                fail("GN-03", rel, body[:m.start()].count("\n") + 1,
                     "类型 %s 未注册 class_name（返回）" % ret)

    print("扫描 %d 个 gd；class_name %d 个；FAIL %d" % (len(files), len(class_names), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())