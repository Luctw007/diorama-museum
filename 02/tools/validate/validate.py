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
内容包校验器（TASK-07，v0.2）

用法：
    python validate.py <content-package-path> [--schema <schema.json>] [--quiet]

<content-package-path> 为 content/<device-id>/ 目录。校验器读取该目录下的
meta.json / runtime.json / THIRD_PARTY.md / annotations/annotations.json，
逐条执行规则 R-xxx 并输出结构化报告：

    PASS  R-001  meta.json  说明
    FAIL  R-014  components[2]  说明

全部 PASS 时退出码为 0；存在任一 FAIL 时退出码为 1。

v0.2 相对 v0.1 的新增：
  - R-017 激活（assembly.materials 引用文件存在）
  - R-080 timeline 结构合法 / R-081 总时长≤预算 / R-082 C4 逐镜头 caption / R-083 caption 无未定标记
  - R-084 sink 命名枚举 / R-085 sinks↔annotations.surface 闭环
  - R-086 input_map 键名合法 / R-087 localized 结构与回退警告 / R-088 旧新字段一致性
  - R-089 era 范围 / R-090 glTF 节点名与 node_id 对应 / R-091 THIRD_PARTY 三件套
  - R-071 改为 spec_version=="0.2"；role 文案改为 localized.zh

设计说明（见完成报告）：
  - 采用「自研轻量 JSON Schema 校验」，仅支持本规范 schema 用到的构造子集
    （type/properties/required/additionalProperties/items/enum/pattern/const/
     minLength/minItems/maxItems/$ref/$defs/number 范围），零第三方依赖。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

# ---------------------------------------------------------------------------
# 常量与正则（与《内容包规范 v0.2》规则表一致）
# ---------------------------------------------------------------------------
SCHEMA_REL = os.path.join("..", "..", "content", "schema", "device_spec.schema.json")

DEVICE_ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
NODE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)

LICENSE_TIERS = {"public_domain", "cc", "licensed", "visual_reference_only"}
PRECISION_LEVELS = {"L1", "L2", "L3", "L4"}
PRESENTATION_LEVELS = {"C2", "C3", "C4"}
MEDIA_HINTS = {"none", "cartridge", "disk", "firmware", "tape", "cd_rom", "floppy"}
UNRESOLVED_MARKERS = ["需核实", "待核实", "TBD", "TODO", "FIXME", "待定", "XXX", "???"]

# v0.2 新增常量
SINK_SURFACES = {"internal_crt", "external_crt", "terminal", "led", "handheld_lcd",
                 "speaker", "crt_display", "indicator_lamps"}
EASINGS = {"linear", "ease_in", "ease_out", "ease_in_out"}
ANIM_BUDGET = {"L1": 60.0, "L2": 180.0, "L3": 300.0, "L4": 600.0}  # 动画总时长上限（秒，v0.2 起始值，可调）
INPUT_MAPS = {"keyboard", "mouse", "joystick"}
INPUT_KEY_RE = {
    "keyboard": re.compile(r"^KEY_[A-Z0-9_]+$"),
    "joystick": re.compile(r"^(axis_[xy]|btn[0-9]+|hat_[0-9]+)$"),
    "mouse": re.compile(r"^(motion|btn_left|btn_right|btn_middle|wheel_up|wheel_down)$"),
}
# 设备逻辑令牌（两层键名模型，01 线 runtime_mapping.md §5）：动作值的小写点分路径
DEVICE_TOKEN_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")
THIRD_PARTY_TIERS = {
    "公共领域", "CC", "授权许可", "仅视觉参考", "原创",
    "public_domain", "cc", "licensed", "visual_reference_only",
}
ORIGINAL_TIERS = {"原创", "自产", "original", "original_work"}

# 文件名允许的扩展名（命名规范 R-022）
ALLOWED_EXT = {".json", ".gltf", ".glb", ".bin", ".png", ".jpg", ".jpeg", ".wav", ".ogg", ".md", ".txt"}
FILE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9]+)?$")


def _lzh(v):
    """取 localized 对象的中文文案；兼容 v0.1 遗留字符串形式。"""
    if isinstance(v, dict):
        return v.get("zh", "")
    if isinstance(v, str):
        return v
    return ""


# ---------------------------------------------------------------------------
# 结果模型
# ---------------------------------------------------------------------------
class Result:
    __slots__ = ("status", "rule", "path", "msg")

    def __init__(self, status: str, rule: str, path: str, msg: str):
        self.status = status
        self.rule = rule
        self.path = path
        self.msg = msg

    def __repr__(self) -> str:  # pragma: no cover - 调试用
        return f"{self.status}\t{self.rule}\t{self.path}\t{self.msg}"


class Report:
    def __init__(self):
        self.results: list[Result] = []

    def add(self, ok: bool, rule: str, path: str, msg: str):
        self.results.append(Result("PASS" if ok else "FAIL", rule, path, msg))

    def has_fail(self) -> bool:
        return any(r.status == "FAIL" for r in self.results)

    def render(self) -> str:
        lines = []
        for r in self.results:
            lines.append(f"{r.status:<5} {r.rule:<6} {r.path:<26} {r.msg}")
        n_pass = sum(1 for r in self.results if r.status == "PASS")
        n_fail = sum(1 for r in self.results if r.status == "FAIL")
        lines.append("-" * 78)
        lines.append(f"总计 {len(self.results)} 条：PASS {n_pass}，FAIL {n_fail}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 自研轻量 JSON Schema 校验器
# 支持构造：type(含数组)/properties/required/additionalProperties(bool|schema)/
#           items/minItems/maxItems/enum/pattern/const/minLength/maxLength/
#           minimum/maximum/exclusiveMinimum/exclusiveMaximum/$ref/#/$defs
# ---------------------------------------------------------------------------
class SchemaError(Exception):
    pass


def _type_name(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "array"
    if isinstance(v, dict):
        return "object"
    return type(v).__name__


def _resolve_ref(ref: str, root: dict):
    """解析本地 $ref（仅支持 #/ 片段）。"""
    if not ref.startswith("#"):
        raise SchemaError(f"暂不支持外部 $ref：{ref}")
    if ref == "#":
        return root
    parts = ref.lstrip("#/").split("/")
    node = root
    for p in parts:
        p = p.replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict) and p in node:
            node = node[p]
        else:
            raise SchemaError(f"无法解析 $ref：{ref}")
    return node


def _check_type(instance, t: str) -> bool:
    if t == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if t == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if t == "null":
        return instance is None
    if t == "array":
        return isinstance(instance, list)
    if t == "object":
        return isinstance(instance, dict) and not isinstance(instance, list)
    if t == "boolean":
        return isinstance(instance, bool)
    if t == "string":
        return isinstance(instance, str)
    return _type_name(instance) == t


def validate_schema(instance, schema: dict, root: dict, path: str = "$") -> list[str]:
    """返回错误信息列表（空列表 = 通过）。"""
    errors: list[str] = []

    if "$ref" in schema:
        target = _resolve_ref(schema["$ref"], root)
        return validate_schema(instance, target, root, path)

    # type
    if "type" in schema:
        types = schema["type"]
        if isinstance(types, str):
            types = [types]
        if not any(_check_type(instance, t) for t in types):
            errors.append(f"{path}: 类型应为 {schema['type']}，实际为 {_type_name(instance)}")
            return errors

    # const / enum
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: 值应为 {schema['const']!r}，实际为 {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: 值 {instance!r} 不在枚举 {schema['enum']} 中")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: 字符串长度 {len(instance)} 小于 {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: 字符串长度 {len(instance)} 大于 {schema['maxLength']}")
        if "pattern" in schema:
            try:
                if not re.search(schema["pattern"], instance):
                    errors.append(f"{path}: 值 {instance!r} 不匹配正则 {schema['pattern']}")
            except re.error as e:
                errors.append(f"{path}: schema 正则错误 {e}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} 小于最小值 {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} 大于最大值 {schema['maximum']}")
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: {instance} 未大于 {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
            errors.append(f"{path}: {instance} 未小于 {schema['exclusiveMaximum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: 数组长度 {len(instance)} 小于 {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: 数组长度 {len(instance)} 大于 {schema['maxItems']}")
        if schema.get("uniqueItems") and len(set(map(str, instance))) != len(instance):
            errors.append(f"{path}: 数组元素不唯一")
        if "items" in schema and isinstance(schema["items"], dict):
            for i, item in enumerate(instance):
                errors.extend(validate_schema(item, schema["items"], root, f"{path}[{i}]"))

    if isinstance(instance, dict):
        if "required" in schema:
            for k in schema["required"]:
                if k not in instance:
                    errors.append(f"{path}: 缺少必填字段 {k!r}")
        if "properties" in schema:
            for k, sub in schema["properties"].items():
                if k in instance:
                    errors.extend(validate_schema(instance[k], sub, root, f"{path}.{k}"))
        if "additionalProperties" in schema:
            ap = schema["additionalProperties"]
            known = set(schema.get("properties", {}).keys())
            for k, v in instance.items():
                if k not in known:
                    if ap is False:
                        errors.append(f"{path}: 不允许的额外字段 {k!r}")
                    elif isinstance(ap, dict):
                        errors.extend(validate_schema(v, ap, root, f"{path}.{k}"))

    return errors


# ---------------------------------------------------------------------------
# glTF 解析（R-041 / R-090 / budget_check 共用）
# ---------------------------------------------------------------------------
def load_gltf(path: str):
    """读取 .gltf(JSON) 或 .glb(JSON chunk)，返回解析后的 dict。失败抛异常。"""
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] == b"glTF":
        # GLB：magic(4) + version(4) + length(4) + [chunkLength(4) + chunkType(4) + data]
        if len(data) < 12:
            raise ValueError("GLB 文件头不完整")
        chunk_len = int.from_bytes(data[12:16], "little")
        chunk_type = int.from_bytes(data[16:20], "little")
        if chunk_type != 0x4E4F534A:  # "JSON"
            raise ValueError("GLB 首个 chunk 不是 JSON")
        json_bytes = data[20:20 + chunk_len]
        return json.loads(json_bytes.decode("utf-8"))
    return json.loads(data.decode("utf-8"))


def count_gltf_triangles(gltf: dict) -> int:
    """估算 glTF 三角面数：各 mesh 各 primitive 的 indices 或 POSITION accessor 计数 /3。"""
    accessors = gltf.get("accessors", [])
    total = 0
    for mesh in gltf.get("meshes", []):
        for prim in mesh.get("primitives", []):
            idx = prim.get("indices")
            if idx is not None and idx < len(accessors):
                total += accessors[idx].get("count", 0) // 3
            else:
                pos = prim.get("attributes", {}).get("POSITION")
                if pos is not None and pos < len(accessors):
                    total += accessors[pos].get("count", 0) // 3
    return total


# ---------------------------------------------------------------------------
# 校验器主体
# ---------------------------------------------------------------------------
class PackageValidator:
    def __init__(self, pkg_path: str, schema_path: str):
        self.pkg = os.path.abspath(pkg_path)
        self.schema_path = os.path.abspath(schema_path)
        self.report = Report()
        self.schema_root = self._load_json(self.schema_path, fatal=True)
        self.meta = None
        self.runtime = None
        self.annotations = []
        self.ann_doc = None

    # -- 工具 -------------------------------------------------------------
    def _load_json(self, path: str, fatal: bool = False):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            if fatal:
                sys.stderr.write(f"无法加载 schema：{path}（{e}）\n")
                sys.exit(2)
            return None

    def _exists(self, rel: str) -> bool:
        return os.path.isfile(os.path.join(self.pkg, rel))

    def _check(self, ok: bool, rule: str, path: str, msg: str):
        self.report.add(ok, rule, path, msg)

    # -- 主入口 -----------------------------------------------------------
    def run(self) -> int:
        self._load_documents()
        self._check_schema()
        self._check_references()
        self._check_naming()
        self._check_transforms()
        self._check_budget()
        self._check_third_party_and_sources()
        self._check_copywriting()
        self._check_versions()
        self._check_v2_features()
        print(self.report.render())
        return 0 if not self.report.has_fail() else 1

    def _load_documents(self):
        # R-001
        meta_path = os.path.join(self.pkg, "meta.json")
        if os.path.isfile(meta_path):
            self.meta = self._load_json(meta_path)
            if self.meta is None:
                self._check(False, "R-001", "meta.json", "meta.json 存在但不是合法 JSON")
            else:
                self._check(True, "R-001", "meta.json", "meta.json 存在且为合法 JSON")
        else:
            self._check(False, "R-001", "meta.json", "缺少 meta.json")

        # runtime.json（R-003 的存在性）
        rp = os.path.join(self.pkg, "runtime.json")
        if os.path.isfile(rp):
            self.runtime = self._load_json(rp)
        else:
            self.runtime = None

        # annotations.json（R-005 的存在性）
        ann_path = os.path.join(self.pkg, "annotations", "annotations.json")
        if os.path.isfile(ann_path):
            self.ann_doc = self._load_json(ann_path)
            if self.ann_doc is not None:
                self.annotations = self.ann_doc.get("annotations", [])

    def _check_schema(self):
        if self.meta is None:
            return
        # R-002
        errs = validate_schema(self.meta, self.schema_root, self.schema_root, "$")
        if errs:
            for e in errs[:10]:
                self._check(False, "R-002", "meta.json", e)
        else:
            self._check(True, "R-002", "meta.json", "meta.json 通过 device_spec.schema.json 校验")

        # R-003
        runtime_def = self.schema_root.get("$defs", {}).get("runtime", {})
        if self.runtime is None:
            self._check(False, "R-003", "runtime.json", "缺少 runtime.json")
        else:
            rerrs = validate_schema(self.runtime, runtime_def, self.schema_root, "$")
            if rerrs:
                for e in rerrs[:10]:
                    self._check(False, "R-003", "runtime.json", e)
            else:
                self._check(True, "R-003", "runtime.json", "runtime.json 通过 $defs/runtime 校验")

        # R-004
        if self.meta is not None and self.runtime is not None:
            same = self.meta.get("runtime") == self.runtime
            self._check(same, "R-004", "runtime.json",
                        "runtime.json 与 meta.json.runtime 一致" if same
                        else "runtime.json 与 meta.json.runtime 不一致，必须逐字节等价")

        # R-005
        ann_def = self.schema_root.get("$defs", {}).get("annotations_document", {})
        if self.ann_doc is None:
            self._check(False, "R-005", "annotations/annotations.json", "缺少 annotations/annotations.json")
        else:
            aerrs = validate_schema(self.ann_doc, ann_def, self.schema_root, "$")
            if aerrs:
                for e in aerrs[:10]:
                    self._check(False, "R-005", "annotations/annotations.json", e)
            else:
                self._check(True, "R-005", "annotations/annotations.json",
                            "annotations.json 通过 $defs/annotations_document 校验")

    def _node_ids(self):
        asm_ids = [a.get("id") for a in self.meta.get("assemblies", []) if isinstance(a, dict)]
        comp_ids = [c.get("id") for c in self.meta.get("components", []) if isinstance(c, dict)]
        return asm_ids, comp_ids

    def _check_references(self):
        if self.meta is None:
            return
        assemblies = self.meta.get("assemblies", [])
        components = self.meta.get("components", [])
        asm_ids, comp_ids = self._node_ids()
        ann_ids = [a.get("id") for a in self.annotations if isinstance(a, dict)]

        # R-010 parent 存在
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            p = a.get("parent")
            if p is not None and p not in asm_ids:
                self._check(False, "R-010", f"assemblies[{a.get('id')}]",
                            f"parent {p!r} 不存在于 assemblies")

        # R-011 children 每项存在
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            for ch in a.get("children", []):
                if ch not in asm_ids:
                    self._check(False, "R-011", f"assemblies[{a.get('id')}]",
                                f"children 项 {ch!r} 不存在")

        # R-012 无环（DFS）
        children_map = {a.get("id"): list(a.get("children", [])) for a in assemblies if isinstance(a, dict)}
        cycle = self._find_cycle(children_map)
        if cycle:
            self._check(False, "R-012", "assemblies", f"装配树存在环：{' -> '.join(cycle)}")

        # R-013 parent/children 双向一致
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            aid = a.get("id")
            p = a.get("parent")
            if p is not None and p in children_map and aid not in children_map.get(p, []):
                self._check(False, "R-013", f"assemblies[{aid}]",
                            f"{p}.children 未包含 {aid}（parent/children 不一致）")
            for ch in a.get("children", []):
                if ch in asm_ids:
                    cp = next((x.get("parent") for x in assemblies if x.get("id") == ch), None)
                    if cp != aid:
                        self._check(False, "R-013", f"assemblies[{ch}]",
                                    f"{ch}.parent 应为 {aid}（parent/children 不一致）")

        # R-014 component.assembly 存在
        for c in components:
            if not isinstance(c, dict):
                continue
            if c.get("assembly") not in asm_ids:
                self._check(False, "R-014", f"components[{c.get('id')}]",
                            f"引用的 assembly {c.get('assembly')!r} 不存在")

        # R-015 annotation.target 存在
        valid_targets = set(asm_ids) | set(comp_ids)
        for an in self.annotations:
            if not isinstance(an, dict):
                continue
            if an.get("target") not in valid_targets:
                self._check(False, "R-015", f"annotations[{an.get('id')}]",
                            f"target {an.get('target')!r} 不存在")

        # R-016 mesh_ref 文件存在
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            mr = a.get("mesh_ref")
            if mr and not self._exists(mr):
                self._check(False, "R-016", f"assemblies[{a.get('id')}]",
                            f"mesh_ref 文件 {mr} 不存在")

        # R-017 materials 引用文件存在（v0.2 激活）
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            for m in a.get("materials", []):
                if not self._exists(m):
                    self._check(False, "R-017", f"assemblies[{a.get('id')}]",
                                f"materials 文件 {m} 不存在")

        # R-018 annotations 引用存在
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            for an in a.get("annotations", []):
                if an not in ann_ids:
                    self._check(False, "R-018", f"assemblies[{a.get('id')}]",
                                f"引用的 annotation {an!r} 不存在")
        for c in components:
            if not isinstance(c, dict):
                continue
            for an in c.get("annotations", []):
                if an not in ann_ids:
                    self._check(False, "R-018", f"components[{c.get('id')}]",
                                f"引用的 annotation {an!r} 不存在")

        self._finalize_ref_pass(asm_ids, comp_ids)

    def _find_cycle(self, children_map):
        """三色 DFS 检测环，返回环路径或 None。"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n: WHITE for n in children_map}
        stack_path = []

        def dfs(node):
            color[node] = GRAY
            stack_path.append(node)
            for nxt in children_map.get(node, []):
                if color.get(nxt, BLACK) == GRAY:
                    i = stack_path.index(nxt)
                    return stack_path[i:] + [nxt]
                if color.get(nxt, BLACK) == WHITE:
                    r = dfs(nxt)
                    if r:
                        return r
            stack_path.pop()
            color[node] = BLACK
            return None

        for n in list(children_map):
            if color.get(n, BLACK) == WHITE:
                r = dfs(n)
                if r:
                    return r
        return None

    def _finalize_ref_pass(self, asm_ids, comp_ids):
        def has_fail(rule):
            return any(r.rule == rule and r.status == "FAIL" for r in self.report.results)

        for rule, desc in [
            ("R-010", "所有 parent 引用存在"),
            ("R-011", "所有 children 引用存在"),
            ("R-012", "装配树无环"),
            ("R-013", "parent/children 双向一致"),
            ("R-014", "所有 component.assembly 引用存在"),
            ("R-015", "所有 annotation.target 引用存在"),
            ("R-016", "所有 mesh_ref 文件存在"),
            ("R-017", "所有 materials 文件存在"),
            ("R-018", "所有 annotations 引用存在"),
        ]:
            if not has_fail(rule):
                self._check(True, rule, "-", desc)

    def _check_naming(self):
        if self.meta is None:
            return
        m = self.meta.get("meta", {})
        device_id = m.get("id", "")
        ok = bool(DEVICE_ID_RE.match(device_id))
        self._check(ok, "R-020", "meta.id", f"device-id {device_id!r} 符合 kebab-case" if ok
                    else f"device-id {device_id!r} 不符合 kebab-case 正则")

        bad = []
        for a in self.meta.get("assemblies", []):
            if isinstance(a, dict) and not NODE_ID_RE.match(a.get("id", "")):
                bad.append(a.get("id"))
        for c in self.meta.get("components", []):
            if isinstance(c, dict) and not NODE_ID_RE.match(c.get("id", "")):
                bad.append(c.get("id"))
        self._check(not bad, "R-021", "nodes", "所有节点 id 符合 snake_case" if not bad
                    else f"节点 id 不符合 snake_case：{bad}")

        bad = []
        for an in self.annotations:
            if isinstance(an, dict) and not NODE_ID_RE.match(an.get("id", "")):
                bad.append(an.get("id"))
        if self.runtime:
            for s in self.runtime.get("output_sinks", []):
                if isinstance(s, dict) and not NODE_ID_RE.match(s.get("id", "")):
                    bad.append(s.get("id"))
        self._check(not bad, "R-022", "annotations/output_sinks",
                    "annotation/sink id 符合 snake_case" if not bad
                    else f"id 不符合 snake_case：{bad}")

        all_ids = [a.get("id") for a in self.meta.get("assemblies", []) if isinstance(a, dict)] + \
                  [c.get("id") for c in self.meta.get("components", []) if isinstance(c, dict)]
        dup = sorted({x for x in all_ids if all_ids.count(x) > 1})
        self._check(not dup, "R-023", "nodes", "节点 id 全局唯一" if not dup
                    else f"节点 id 重复：{dup}")

    def _check_transforms(self):
        if self.meta is None:
            return
        for a in self.meta.get("assemblies", []):
            if not isinstance(a, dict):
                continue
            t = a.get("transform") or {}
            aid = a.get("id")
            tr = t.get("translation")
            rot = t.get("rotation")
            sc = t.get("scale")

            ok = (isinstance(tr, list) and len(tr) == 3
                  and all(isinstance(x, (int, float)) and math.isfinite(x) for x in tr))
            self._check(ok, "R-030", f"assemblies[{aid}]",
                        "translation 为 3 个有限实数" if ok else f"translation 非法：{tr}")

            if isinstance(rot, list) and len(rot) == 4 and all(isinstance(x, (int, float)) for x in rot):
                norm = math.sqrt(sum(x * x for x in rot))
                ok = abs(norm - 1.0) < 1e-3
                self._check(ok, "R-031", f"assemblies[{aid}]",
                            "rotation 为单位四元数" if ok else f"rotation 模长 {norm:.4f} 非单位")
            else:
                self._check(False, "R-031", f"assemblies[{aid}]", f"rotation 非法：{rot}")

            ok = (isinstance(sc, list) and len(sc) == 3
                  and all(isinstance(x, (int, float)) and math.isfinite(x) and x > 0 for x in sc))
            self._check(ok, "R-032", f"assemblies[{aid}]",
                        "scale 各分量 > 0" if ok else f"scale 非法：{sc}")

            if isinstance(sc, list) and len(sc) == 3 and all(isinstance(x, (int, float)) for x in sc):
                ok = all(1e-6 <= x <= 1e6 for x in sc)
                self._check(ok, "R-033", f"assemblies[{aid}]",
                            "scale 各分量在 [1e-6, 1e6]" if ok else f"scale 越界：{sc}")

    def _check_budget(self):
        if self.meta is None:
            return
        m = self.meta.get("meta", {})
        level = m.get("precision_level")
        self._check(level in PRECISION_LEVELS, "R-040", "meta.precision_level",
                    f"precision_level={level} 合法" if level in PRECISION_LEVELS
                    else f"precision_level={level} 非法（应为 L1..L4）")

        for a in self.meta.get("assemblies", []):
            if not isinstance(a, dict):
                continue
            mr = a.get("mesh_ref")
            if not mr:
                continue
            fp = os.path.join(self.pkg, mr)
            if not os.path.isfile(fp):
                continue  # 已由 R-016 报错
            try:
                gltf = load_gltf(fp)
                version = gltf.get("asset", {}).get("version", "")
                ok = version.startswith("2.")
                tri = count_gltf_triangles(gltf)
                nodes = len(gltf.get("nodes", []))
                self._check(ok, "R-041", f"assemblies[{a.get('id')}]",
                            f"glTF 可解析（version={version}）" if ok else f"glTF version {version} 非法")
                self._check(True, "R-042", f"assemblies[{a.get('id')}]",
                            f"预算统计：nodes={nodes}, triangles={tri}；超限由 budget_check.py 报告，不阻塞（可调）")
            except Exception as e:
                self._check(False, "R-041", f"assemblies[{a.get('id')}]", f"glTF 解析失败：{e}")

    def _check_third_party_and_sources(self):
        tp_path = os.path.join(self.pkg, "THIRD_PARTY.md")
        if os.path.isfile(tp_path):
            self._check(True, "R-050", "THIRD_PARTY.md", "THIRD_PARTY.md 存在")
            try:
                missing = self._check_third_party_table(tp_path)
            except Exception as e:  # noqa: BLE001
                missing = [f"解析失败：{e}"]
            if missing:
                self._check(False, "R-051", "THIRD_PARTY.md", f"第三方行缺必填字段：{missing}")
            else:
                self._check(True, "R-051", "THIRD_PARTY.md", "第三方资产行均含来源 URL 与获取日期")
        else:
            self._check(False, "R-050", "THIRD_PARTY.md", "缺少 THIRD_PARTY.md")

        if self.meta is None:
            return
        sources = self.meta.get("meta", {}).get("sources", [])
        bad_url, bad_lic, bad_date = [], [], []
        for i, s in enumerate(sources):
            if not isinstance(s, dict):
                continue
            if not URL_RE.match(s.get("url", "")):
                bad_url.append(i)
            if s.get("license") not in LICENSE_TIERS:
                bad_lic.append(i)
            if not DATE_RE.match(s.get("accessed_at", "")):
                bad_date.append(i)
        self._check(not bad_url, "R-052", "meta.sources", "所有 source.url 为 http/https" if not bad_url
                    else f"source.url 非法：索引 {bad_url}")
        self._check(not bad_lic, "R-053", "meta.sources", "所有 source.license 为四档枚举" if not bad_lic
                    else f"source.license 非法：索引 {bad_lic}")
        self._check(not bad_date, "R-054", "meta.sources", "所有 source.accessed_at 为 YYYY-MM-DD" if not bad_date
                    else f"source.accessed_at 非法：索引 {bad_date}")

    def _parse_third_party_rows(self, path: str):
        """解析 THIRD_PARTY.md 表格，返回 (rows, url_col, date_col, lic_col) 或抛异常。"""
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        header = None
        url_col = date_col = lic_col = None
        rows = []
        for line in lines:
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None:
                header = cells
                for i, c in enumerate(cells):
                    if "来源" in c and "URL" in c:
                        url_col = i
                    elif "获取日期" in c or "日期" in c:
                        date_col = i
                    elif "许可分档" in c or "许可" in c:
                        lic_col = i
                continue
            if all(re.fullmatch(r"-+", c or "-") for c in cells if c):
                continue
            rows.append(cells)
        return rows, url_col, date_col, lic_col

    def _check_third_party_table(self, path: str):
        """返回缺 URL/日期的第三方行描述列表（R-051）。"""
        rows, url_col, date_col, lic_col = self._parse_third_party_rows(path)
        missing = []
        for cells in rows:
            if url_col is None or date_col is None:
                continue
            if lic_col is not None and lic_col < len(cells) and cells[lic_col] in ORIGINAL_TIERS:
                continue
            name = cells[0] if cells else "?"
            if url_col >= len(cells) or not cells[url_col]:
                missing.append(f"{name}(缺URL)")
            if date_col >= len(cells) or not cells[date_col]:
                missing.append(f"{name}(缺日期)")
        return missing

    def _check_copywriting(self):
        if self.meta is None:
            return
        bad = []
        for an in self.annotations:
            if not isinstance(an, dict):
                continue
            txt = an.get("text", "")
            hit = [m for m in UNRESOLVED_MARKERS if m in txt]
            if hit:
                bad.append(f"{an.get('id')}({hit})")
        self._check(not bad, "R-060", "annotations", "标注文本不含未定标记" if not bad
                    else f"含未定标记：{bad}")

        # R-061 role 文案（localized.zh）必须含「在整机」（根装配体豁免）
        root_ids = {a.get("id") for a in self.meta.get("assemblies", [])
                    if isinstance(a, dict) and a.get("parent") is None}
        bad = []
        for a in self.meta.get("assemblies", []):
            if not isinstance(a, dict) or a.get("id") in root_ids:
                continue
            if "在整机" not in _lzh(a.get("role", "")):
                bad.append(f"assembly:{a.get('id')}")
        for c in self.meta.get("components", []):
            if isinstance(c, dict) and "在整机" not in _lzh(c.get("role", "")):
                bad.append(f"component:{c.get('id')}")
        for an in self.annotations:
            if isinstance(an, dict) and an.get("type") == "role":
                if an.get("target") in root_ids:
                    continue
                if "在整机" not in an.get("text", ""):
                    bad.append(f"annotation:{an.get('id')}")
        self._check(not bad, "R-061", "role", "role 文案均含「在整机」" if not bad
                    else f"role 文案缺「在整机」：{bad}")

        # R-062 role 标注字数 20-200
        bad = []
        for an in self.annotations:
            if isinstance(an, dict) and an.get("type") == "role":
                n = len(an.get("text", ""))
                if not (20 <= n <= 200):
                    bad.append(f"{an.get('id')}({n}字)")
        self._check(not bad, "R-062", "annotations", "role 标注字数 20-200" if not bad
                    else f"role 标注字数越界：{bad}")

        # R-063 标注 sources URL 合法
        bad = []
        for an in self.annotations:
            if not isinstance(an, dict):
                continue
            for u in an.get("sources", []):
                if not URL_RE.match(u):
                    bad.append(u)
        self._check(not bad, "R-063", "annotations", "标注 sources URL 合法" if not bad
                    else f"标注 sources URL 非法：{bad}")

    def _check_versions(self):
        if self.meta is None:
            return
        m = self.meta.get("meta", {})
        ok = bool(SEMVER_RE.match(m.get("version", "")))
        self._check(ok, "R-070", "meta.version", f"version={m.get('version')!r} 为合法 semver" if ok
                    else f"version={m.get('version')!r} 非法 semver")
        ok = m.get("spec_version") == "0.2"
        self._check(ok, "R-071", "meta.spec_version", f"spec_version={m.get('spec_version')!r} 为 0.2" if ok
                    else f"spec_version={m.get('spec_version')!r} 应为 0.2")
        ok = bool(SEMVER_RE.match(m.get("engine_min_version", "")))
        self._check(ok, "R-072", "meta.engine_min_version",
                    f"engine_min_version={m.get('engine_min_version')!r} 为合法 semver" if ok
                    else f"engine_min_version={m.get('engine_min_version')!r} 非法 semver")

    # ------------------------------------------------------------------
    # v0.2 新增规则 R-080 ~ R-091
    # ------------------------------------------------------------------
    def _check_v2_features(self):
        if self.meta is None:
            return
        self._check_anim_timeline()
        self._check_sinks_and_input()
        self._check_localization()
        self._check_gltf_names()
        self._check_third_party_strict()

    def _check_anim_timeline(self):
        asm_ids, comp_ids = self._node_ids()
        valid_nodes = set(asm_ids) | set(comp_ids)

        bad_struct = []
        bad_highlight = []
        over_duration = []
        bad_caption = []
        c4_missing = []
        m = self.meta.get("meta", {})
        level = m.get("precision_level", "L2")
        cap = ANIM_BUDGET.get(level, 180.0)
        pres = m.get("presentation_level", "C3")

        for an in self.annotations:
            if not isinstance(an, dict):
                continue
            tl = an.get("timeline")
            if not tl:
                continue
            total = 0.0
            for i, seg in enumerate(tl):
                if not isinstance(seg, dict):
                    continue
                t = seg.get("t")
                # R-080：t 结构
                if not (isinstance(t, list) and len(t) == 2
                        and all(isinstance(x, (int, float)) and math.isfinite(x) for x in t)
                        and t[1] > t[0]):
                    bad_struct.append(f"{an.get('id')}.timeline[{i}].t")
                else:
                    total += t[1] - t[0]
                cam = seg.get("camera") or {}
                if not (isinstance(cam.get("pos"), list) and len(cam.get("pos")) == 3
                        and all(isinstance(x, (int, float)) and math.isfinite(x) for x in cam["pos"])
                        and isinstance(cam.get("look"), list) and len(cam.get("look")) == 3
                        and all(isinstance(x, (int, float)) and math.isfinite(x) for x in cam["look"])):
                    bad_struct.append(f"{an.get('id')}.timeline[{i}].camera")
                arrow = seg.get("arrow")
                if arrow is not None:
                    if not (isinstance(arrow.get("from"), list) and len(arrow.get("from")) == 3
                            and isinstance(arrow.get("to"), list) and len(arrow.get("to")) == 3):
                        bad_struct.append(f"{an.get('id')}.timeline[{i}].arrow")
                for hid in seg.get("highlight", []):
                    if hid not in valid_nodes:
                        bad_highlight.append(f"{an.get('id')}.highlight:{hid}")
                if seg.get("easing") is not None and seg.get("easing") not in EASINGS:
                    bad_struct.append(f"{an.get('id')}.timeline[{i}].easing")
                # R-083：caption 未定标记
                cap_txt = seg.get("caption", "")
                hit = [mk for mk in UNRESOLVED_MARKERS if mk in cap_txt]
                if hit:
                    bad_caption.append(f"{an.get('id')}.timeline[{i}]({hit})")
                # R-082：C4 逐镜头 caption
                if pres == "C4" and an.get("type") == "anim" and not cap_txt.strip():
                    c4_missing.append(f"{an.get('id')}.timeline[{i}]")

            # R-081：总时长
            if total > cap:
                over_duration.append(f"{an.get('id')}({total:.1f}s > {cap:.0f}s)")

        self._check(not bad_struct, "R-080", "annotations.timeline",
                    "timeline 结构合法" if not bad_struct else f"timeline 结构非法：{bad_struct}")
        self._check(not bad_highlight, "R-080", "annotations.timeline",
                    "timeline highlight 引用存在" if not bad_highlight
                    else f"highlight 引用不存在：{bad_highlight}")
        self._check(not over_duration, "R-081", "annotations.timeline",
                    f"timeline 总时长≤预算({cap:.0f}s)" if not over_duration
                    else f"timeline 总时长超限：{over_duration}")
        self._check(not c4_missing, "R-082", "annotations.timeline",
                    "C4 级 anim 每镜头 caption 齐全" if not c4_missing
                    else f"C4 级 anim caption 缺失：{c4_missing}")
        self._check(not bad_caption, "R-083", "annotations.timeline",
                    "caption 无未定标记" if not bad_caption else f"caption 含未定标记：{bad_caption}")

    def _check_sinks_and_input(self):
        # R-084 sink 命名枚举
        bad = []
        declared = set()
        if self.runtime:
            for s in self.runtime.get("output_sinks", []):
                if not isinstance(s, dict):
                    continue
                surf = s.get("surface")
                if surf in SINK_SURFACES:
                    declared.add(surf)
                else:
                    bad.append(surf)
        self._check(not bad, "R-084", "runtime.output_sinks",
                    "sink surface 为命名枚举" if not bad else f"sink surface 非法：{bad}")

        # R-085 annotation.surface 引用闭环
        bad = []
        for an in self.annotations:
            if not isinstance(an, dict):
                continue
            surf = an.get("surface")
            if surf and surf not in declared:
                bad.append(f"{an.get('id')}.surface:{surf}")
        self._check(not bad, "R-085", "annotations",
                    "annotation.surface 均已声明" if not bad
                    else f"annotation.surface 未声明：{bad}")

        # R-086 input_map 键名合法（两种形态：v0.2 结构化 {map,key} / v0.1 legacy 字符串令牌）
        bad = []
        legacy = []
        if self.runtime:
            for action, desc in self.runtime.get("input_map", {}).items():
                if not NODE_ID_RE.match(action):
                    bad.append(f"{action}(动作名)")
                    continue
                if isinstance(desc, str):
                    # legacy：动作名 -> 设备逻辑令牌（两层键名模型，01 线 runtime_mapping §5）
                    if DEVICE_TOKEN_RE.match(desc):
                        legacy.append(action)
                    else:
                        bad.append(f"{action}(令牌={desc!r})")
                    continue
                if not isinstance(desc, dict):
                    bad.append(f"{action}(描述非法)")
                    continue
                mp = desc.get("map")
                key = desc.get("key", "")
                if mp not in INPUT_MAPS:
                    bad.append(f"{action}(map={mp})")
                    continue
                if not INPUT_KEY_RE[mp].match(key):
                    bad.append(f"{action}(key={key!r})")
        extra = f"；legacy 字符串形式 {len(legacy)} 项（建议迁移结构化）" if legacy and not bad else ""
        self._check(not bad, "R-086", "runtime.input_map",
                    ("input_map 键名合法" + extra) if not bad else f"input_map 键名非法：{bad}")

    def _check_localization(self):
        # R-087 localized 结构完整 + 回退警告
        fields = []
        m = self.meta.get("meta", {})
        if isinstance(m.get("name"), dict):
            fields.append(("meta.name", m["name"]))
        if isinstance(m.get("intro"), dict):
            fields.append(("meta.intro", m["intro"]))
        for a in self.meta.get("assemblies", []):
            if isinstance(a, dict) and isinstance(a.get("role"), dict):
                fields.append((f"assembly.{a.get('id')}.role", a["role"]))
        for c in self.meta.get("components", []):
            if isinstance(c, dict) and isinstance(c.get("role"), dict):
                fields.append((f"component.{c.get('id')}.role", c["role"]))

        missing_zh = [name for name, obj in fields if not obj.get("zh")]
        missing_en = [name for name, obj in fields if not obj.get("en")]
        ok = not missing_zh
        msg = "localized 结构完整" if ok else f"localized 缺 zh：{missing_zh}"
        if missing_en:
            msg += f"；警告：以下字段缺 en（回退 zh）：{missing_en}"
        self._check(ok, "R-087", "localized", msg)

        # R-088 旧字段 name_en 与新字段 name.en 一致性
        name_en = m.get("name_en")
        if name_en is not None:
            name_obj = m.get("name")
            en_new = name_obj.get("en") if isinstance(name_obj, dict) else None
            ok = en_new is not None and en_new == name_en
            self._check(ok, "R-088", "meta.name_en",
                        "deprecated name_en 与 name.en 一致" if ok
                        else "name_en 与 name.en 不一致或缺失，请迁移到 name.en")
        else:
            self._check(True, "R-088", "meta.name_en", "无 deprecated name_en（已迁移）")

        # R-089 era 范围
        era = m.get("era")
        if era is not None:
            ok = isinstance(era, int) and 1800 <= era <= 2100
            self._check(ok, "R-089", "meta.era",
                        f"era={era} 合法" if ok else f"era={era} 非法（应 1800-2100 整数）")
        else:
            self._check(True, "R-089", "meta.era", "未填 era（可选）")

    def _check_gltf_names(self):
        # R-090 glTF 网格节点名与 node_id 对应
        bad = []
        for a in self.meta.get("assemblies", []):
            if not isinstance(a, dict):
                continue
            mr = a.get("mesh_ref")
            if not mr:
                continue
            fp = os.path.join(self.pkg, mr)
            if not os.path.isfile(fp):
                continue
            try:
                gltf = load_gltf(fp)
            except Exception:
                continue
            node_names = {n.get("name") for n in gltf.get("nodes", []) if isinstance(n, dict)}
            mesh_names = {mm.get("name") for mm in gltf.get("meshes", []) if isinstance(mm, dict)}
            if a.get("id") not in node_names and a.get("id") not in mesh_names:
                bad.append(f"{a.get('id')}（glTF 节点/网格名未见）")
        self._check(not bad, "R-090", "gltf", "glTF 网格节点名与 node_id 对应" if not bad
                    else f"glTF 命名不符：{bad}")

    def _check_third_party_strict(self):
        # R-091 THIRD_PARTY 行三件套（分档枚举 + URL 格式 + 日期格式）
        tp_path = os.path.join(self.pkg, "THIRD_PARTY.md")
        if not os.path.isfile(tp_path):
            self._check(False, "R-091", "THIRD_PARTY.md", "缺少 THIRD_PARTY.md（无法核三件套）")
            return
        try:
            rows, url_col, date_col, lic_col = self._parse_third_party_rows(tp_path)
        except Exception as e:  # noqa: BLE001
            self._check(False, "R-091", "THIRD_PARTY.md", f"解析失败：{e}")
            return
        bad = []
        for cells in rows:
            name = cells[0] if cells else "?"
            lic = cells[lic_col] if (lic_col is not None and lic_col < len(cells)) else ""
            if lic not in THIRD_PARTY_TIERS:
                bad.append(f"{name}(分档非法:{lic})")
                continue
            if lic in ORIGINAL_TIERS:
                continue
            url = cells[url_col] if (url_col is not None and url_col < len(cells)) else ""
            date = cells[date_col] if (date_col is not None and date_col < len(cells)) else ""
            if not URL_RE.match(url):
                bad.append(f"{name}(URL非法)")
            if not DATE_RE.match(date):
                bad.append(f"{name}(日期非法)")
        self._check(not bad, "R-091", "THIRD_PARTY.md",
                    "THIRD_PARTY 行三件套（分档+URL+日期）合法" if not bad else f"THIRD_PARTY 行格式非法：{bad}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="内容包校验器（TASK-07，v0.2）")
    parser.add_argument("package_path", help="content/<device-id>/ 目录")
    parser.add_argument("--schema", default=None, help="JSON Schema 路径（默认相对脚本定位）")
    parser.add_argument("--quiet", action="store_true", help="仅输出 FAIL")
    args = parser.parse_args(argv)

    pkg = args.package_path
    if not os.path.isdir(pkg):
        sys.stderr.write(f"错误：路径不是目录：{pkg}\n")
        return 2

    if args.schema:
        schema_path = args.schema
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.normpath(os.path.join(script_dir, SCHEMA_REL))
    if not os.path.isfile(schema_path):
        sys.stderr.write(f"错误：找不到 schema：{schema_path}\n")
        return 2

    v = PackageValidator(pkg, schema_path)
    code = v.run()
    if args.quiet:
        for r in v.report.results:
            if r.status == "FAIL":
                print(r)
    return code


if __name__ == "__main__":
    sys.exit(main())
