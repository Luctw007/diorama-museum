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
内容包校验器（TASK-02）

用法：
    python validate.py <content-package-path> [--schema <schema.json>] [--quiet]

<content-package-path> 为 content/<device-id>/ 目录。校验器读取该目录下的
meta.json / runtime.json / THIRD_PARTY.md / annotations/annotations.json，
逐条执行规则 R-xxx 并输出结构化报告：

    PASS  R-001  meta.json  说明
    FAIL  R-014  components[2]  说明

全部 PASS 时退出码为 0；存在任一 FAIL 时退出码为 1。

设计说明（见完成报告）：
  - 采用「自研轻量 JSON Schema 校验」，仅支持本规范 schema 用到的构造子集
    （type/properties/required/additionalProperties/items/enum/pattern/const/
     minLength/minItems/maxItems/$ref/$defs/number 范围），理由：零第三方依赖、
    跨平台可移植、行为可控。schema 校验错误统一归入 R-002/R-003/R-005，
    专项规则（命名/引用/transform/文案/版本等）另按规则编号独立报告，便于定位。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

# ---------------------------------------------------------------------------
# 常量与正则（与《内容包规范 v0.1》第九章规则表一致）
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
MEDIA_HINTS = {"none", "cartridge", "disk", "firmware", "tape", "cd_rom", "floppy"}
UNRESOLVED_MARKERS = ["需核实", "待核实", "TBD", "TODO", "FIXME", "待定", "XXX", "???"]

# 文件名允许的扩展名（命名规范 R-022）
ALLOWED_EXT = {".json", ".gltf", ".glb", ".bin", ".png", ".jpg", ".jpeg", ".wav", ".ogg", ".md", ".txt"}
FILE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9]+)?$")


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
# glTF 解析（R-041 / budget_check 共用）
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

    def _rel(self, *parts) -> str:
        return os.path.relpath(os.path.join(self.pkg, *parts), self.pkg).replace(os.sep, "/")

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
        if os.path.isfile(os.path.join(self.pkg, "runtime.json")):
            self.runtime = self._load_json(os.path.join(self.pkg, "runtime.json"))
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
            meta_runtime = self.meta.get("runtime")
            same = meta_runtime == self.runtime
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

    def _check_references(self):
        if self.meta is None:
            return
        assemblies = self.meta.get("assemblies", [])
        components = self.meta.get("components", [])
        asm_ids = [a.get("id") for a in assemblies if isinstance(a, dict)]
        comp_ids = [c.get("id") for c in components if isinstance(c, dict)]
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
        children_map = {}
        for a in assemblies:
            if isinstance(a, dict):
                children_map[a.get("id")] = list(a.get("children", []))
        cycle = self._find_cycle(children_map)
        if cycle:
            self._check(False, "R-012", "assemblies", f"装配树存在环：{' -> '.join(cycle)}")

        # R-013 parent/children 双向一致
        for a in assemblies:
            if not isinstance(a, dict):
                continue
            aid = a.get("id")
            p = a.get("parent")
            if p is not None and p in children_map:
                if aid not in children_map.get(p, []):
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

        # 汇总引用规则通过状态（仅在无单项失败且数据完整时标记 PASS）
        self._finalize_ref_pass(asm_ids, comp_ids, children_map)

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

    def _finalize_ref_pass(self, asm_ids, comp_ids, children_map):
        # 若所有单项检查均通过，为各引用规则补 PASS（避免只报错不报通过）
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
            ("R-018", "所有 annotations 引用存在"),
        ]:
            if not has_fail(rule):
                self._check(True, rule, "-", desc)

    def _check_naming(self):
        if self.meta is None:
            return
        m = self.meta.get("meta", {})
        device_id = m.get("id", "")
        # R-020
        ok = bool(DEVICE_ID_RE.match(device_id))
        self._check(ok, "R-020", "meta.id", f"device-id {device_id!r} 符合 kebab-case" if ok
                    else f"device-id {device_id!r} 不符合 kebab-case 正则")

        # R-021 节点 id
        bad = []
        for a in self.meta.get("assemblies", []):
            if isinstance(a, dict) and not NODE_ID_RE.match(a.get("id", "")):
                bad.append(a.get("id"))
        for c in self.meta.get("components", []):
            if isinstance(c, dict) and not NODE_ID_RE.match(c.get("id", "")):
                bad.append(c.get("id"))
        self._check(not bad, "R-021", "nodes", "所有节点 id 符合 snake_case" if not bad
                    else f"节点 id 不符合 snake_case：{bad}")

        # R-022 annotation id / surface id
        bad = []
        for an in self.annotations:
            if isinstance(an, dict) and not NODE_ID_RE.match(an.get("id", "")):
                bad.append(an.get("id"))
        if self.runtime:
            for s in self.runtime.get("output_sinks", []):
                if isinstance(s, dict) and not NODE_ID_RE.match(s.get("surface", "")):
                    bad.append(s.get("surface"))
        self._check(not bad, "R-022", "annotations/output_sinks",
                    "annotation/surface id 符合 snake_case" if not bad
                    else f"id 不符合 snake_case：{bad}")

        # R-023 全局唯一（assembly + component 节点 id）
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

            # R-030
            ok = (isinstance(tr, list) and len(tr) == 3
                  and all(isinstance(x, (int, float)) and math.isfinite(x) for x in tr))
            self._check(ok, "R-030", f"assemblies[{aid}]",
                        "translation 为 3 个有限实数" if ok else f"translation 非法：{tr}")

            # R-031
            if isinstance(rot, list) and len(rot) == 4 and all(isinstance(x, (int, float)) for x in rot):
                norm = math.sqrt(sum(x * x for x in rot))
                ok = abs(norm - 1.0) < 1e-3
                self._check(ok, "R-031", f"assemblies[{aid}]",
                            "rotation 为单位四元数" if ok else f"rotation 模长 {norm:.4f} 非单位")
            else:
                self._check(False, "R-031", f"assemblies[{aid}]", f"rotation 非法：{rot}")

            # R-032
            ok = (isinstance(sc, list) and len(sc) == 3
                  and all(isinstance(x, (int, float)) and math.isfinite(x) and x > 0 for x in sc))
            self._check(ok, "R-032", f"assemblies[{aid}]",
                        "scale 各分量 > 0" if ok else f"scale 非法：{sc}")

            # R-033
            if isinstance(sc, list) and len(sc) == 3 and all(isinstance(x, (int, float)) for x in sc):
                ok = all(1e-6 <= x <= 1e6 for x in sc)
                self._check(ok, "R-033", f"assemblies[{aid}]",
                            "scale 各分量在 [1e-6, 1e6]" if ok else f"scale 越界：{sc}")

    def _check_budget(self):
        if self.meta is None:
            return
        m = self.meta.get("meta", {})
        level = m.get("precision_level")
        # R-040
        self._check(level in PRECISION_LEVELS, "R-040", "meta.precision_level",
                    f"precision_level={level} 合法" if level in PRECISION_LEVELS
                    else f"precision_level={level} 非法（应为 L1..L4）")

        # R-041 / R-042：mesh_ref 的 glTF 存在且可解析（v0.1 降级，见报告）
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
                            f"预算统计（v0.1 降级）：nodes={nodes}, triangles={tri}；"
                            f"超限由 budget_check.py 报告，不阻塞（预算数字可调）")
            except Exception as e:
                self._check(False, "R-041", f"assemblies[{a.get('id')}]", f"glTF 解析失败：{e}")

    def _check_third_party_and_sources(self):
        # R-050 THIRD_PARTY.md 存在
        tp_path = os.path.join(self.pkg, "THIRD_PARTY.md")
        if os.path.isfile(tp_path):
            self._check(True, "R-050", "THIRD_PARTY.md", "THIRD_PARTY.md 存在")
            # R-051 第三方行必填 URL + 获取日期
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
        # R-052 / R-053 / R-054 sources
        sources = self.meta.get("meta", {}).get("sources", [])
        bad_url, bad_lic, bad_date = [], [], []
        for i, s in enumerate(sources):
            if not isinstance(s, dict):
                continue
            url = s.get("url", "")
            if not URL_RE.match(url):
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

    def _check_third_party_table(self, path: str):
        """解析 THIRD_PARTY.md 的表格，返回缺 URL/日期的第三方行描述列表。"""
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        header = None
        url_col = date_col = lic_col = None
        missing = []
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
            # 分隔行（---）跳过
            if all(re.fullmatch(r"-+", c or "-") for c in cells if c):
                continue
            if url_col is None or date_col is None:
                continue
            if lic_col is not None and lic_col < len(cells):
                lic = cells[lic_col]
                if lic in ("原创", "自产", "original", "original_work"):
                    continue  # 原创资产无需 URL/日期
            name = cells[0] if cells else "?"
            if url_col >= len(cells) or not cells[url_col]:
                missing.append(f"{name}(缺URL)")
            if date_col >= len(cells) or not cells[date_col]:
                missing.append(f"{name}(缺日期)")
        return missing

    def _check_copywriting(self):
        if self.meta is None:
            return
        # R-060 未定标记
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

        # R-061 role 文案必须含「在整机」（根装配体豁免）
        root_ids = {a.get("id") for a in self.meta.get("assemblies", [])
                    if isinstance(a, dict) and a.get("parent") is None}
        bad = []
        for a in self.meta.get("assemblies", []):
            if not isinstance(a, dict):
                continue
            if a.get("id") in root_ids:
                continue
            if "在整机" not in a.get("role", ""):
                bad.append(f"assembly:{a.get('id')}")
        for c in self.meta.get("components", []):
            if isinstance(c, dict) and "在整机" not in c.get("role", ""):
                bad.append(f"component:{c.get('id')}")
        for an in self.annotations:
            if isinstance(an, dict) and an.get("type") == "role":
                if an.get("target") in root_ids:
                    continue  # 根装配体的 role 标注豁免「在整机」
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
        # R-070
        ok = bool(SEMVER_RE.match(m.get("version", "")))
        self._check(ok, "R-070", "meta.version", f"version={m.get('version')!r} 为合法 semver" if ok
                    else f"version={m.get('version')!r} 非法 semver")
        # R-071
        ok = m.get("spec_version") == "0.1"
        self._check(ok, "R-071", "meta.spec_version", f"spec_version={m.get('spec_version')!r} 为 0.1" if ok
                    else f"spec_version={m.get('spec_version')!r} 应为 0.1")
        # R-072
        ok = bool(SEMVER_RE.match(m.get("engine_min_version", "")))
        self._check(ok, "R-072", "meta.engine_min_version",
                    f"engine_min_version={m.get('engine_min_version')!r} 为合法 semver" if ok
                    else f"engine_min_version={m.get('engine_min_version')!r} 非法 semver")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="内容包校验器（TASK-02）")
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
