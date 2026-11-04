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
建模预算校验器（TASK-27A，v0.3 草案落地，纯 stdlib）

把《规范 v0.3 建模网格章草案》的"校验预研"落地为可运行的校验器，在正式建模开产前
卡住超预算 / 命名违规 / 贴图违规 / 未知扩展的资产。

规则（MR = Modeling Rule）：
    MR-01  节点命名：glTF 场景根节点 name = 装配体 node_id（延续 R-090），且每装配体
            的 glTF 场景根节点 ≤ 1（多根告警）。
    MR-02  三角面预算：逐 primitive 汇总三角面，对照 v0.3 三档预算（LOD0 特写/高模、
            LOD1 观察/中模/默认、LOD2 远景/低模）；包未声明档位时按 LOD1 判。
            超预算 → WARN，超预算 1.5 倍 → FAIL。
    MR-03  贴图引用：material 引用 image 的文件名符合命名后缀表
            （_basecolor/_normal/_metallic/_metallic_roughness/_emissive）；
            纹理尺寸 ≤2048 且宽高为 2 的幂。
    MR-04  单位与轴/扩展：glTF `extensionsUsed`/`extensionsRequired` 及 scene 根节点扩展
            在白名单之外 → WARN（未知扩展可能改变单位/轴语义）。

用法：
    python model_check.py <content-package-path> [--json]

输出逐文件报告；退出码：0=全部 PASS（无 FAIL），1=存在 FAIL。
仅解析 glTF 的 JSON 段与纹理文件头（PNG/JPEG），不解析 .bin 几何缓冲。

依赖：本目录内 `validate.py`（load_gltf）与 `budget_check.py`（count_triangles_exact /
image_size_from_file），均为纯 stdlib。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_gltf  # noqa: E402
from budget_check import count_triangles_exact, image_size_from_file  # noqa: E402

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
# 三档 LOD 预算（单装配体 = 单 glTF 文件三角面上限）。数字为 v0.3 起始值（可调）。
# LOD0 = 特写档（高模，最近）；LOD1 = 观察档（中模，默认）；LOD2 = 远景档（低模，最远）。
LOD_BUDGETS = {
    "LOD0": {"label": "特写档(高模)", "triangles": 50_000},
    "LOD1": {"label": "观察档(中模/默认)", "triangles": 20_000},
    "LOD2": {"label": "远景档(低模)", "triangles": 8_000},
}

# 超预算倍数阈值：>1.0 → WARN，>1.5 → FAIL
OVER_WARN_FACTOR = 1.0
OVER_FAIL_FACTOR = 1.5

# meta.precision_level → 默认 LOD 档（未声明 precision_level 时按 LOD1 观察档）
PRECISION_TO_LOD = {
    "L1": "LOD2",
    "L2": "LOD1",
    "L3": "LOD0",
    "L4": "LOD0",
}
DEFAULT_LOD = "LOD1"

# 贴图命名后缀白名单
TEXTURE_SUFFIXES = ("basecolor", "normal", "metallic", "metallic_roughness", "emissive")

# 纹理尺寸上限
MAX_TEXTURE = 2048

# glTF 扩展白名单（未知 KHR_* / 其它扩展 → WARN）
EXTENSION_WHITELIST = {
    "KHR_materials_unlit",
    "KHR_texture_transform",
    "KHR_materials_emissive_strength",
    "KHR_materials_pbrSpecularGlossiness",
    "KHR_materials_variants",
    "KHR_draco_mesh_compression",
    "KHR_mesh_quantization",
    "KHR_texture_basisu",
    "KHR_materials_ior",
    "KHR_materials_transmission",
}


# ---------------------------------------------------------------------------
# 读取 meta / 定位 mesh 文件
# ---------------------------------------------------------------------------
def read_meta(pkg: str) -> dict:
    path = os.path.join(pkg, "meta.json")
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_lod(meta: dict) -> str:
    """按 meta.precision_level 解析默认 LOD 档；未声明返回 DEFAULT_LOD。"""
    m = meta.get("meta", {}) if isinstance(meta, dict) else {}
    pl = m.get("precision_level")
    return PRECISION_TO_LOD.get(pl, DEFAULT_LOD)


def mesh_refs(meta: dict) -> list[tuple[str, str]]:
    """返回 [(assembly_id, mesh_ref)]，跳过无 mesh_ref 的装配体。"""
    out = []
    for a in (meta.get("assemblies") or []):
        if isinstance(a, dict) and a.get("mesh_ref"):
            out.append((a.get("id", "?"), a["mesh_ref"]))
    return out


# ---------------------------------------------------------------------------
# 各 MR 规则检查（返回 finding 列表）
# ---------------------------------------------------------------------------
def _finding(rule: str, level: str, rel: str, msg: str) -> dict:
    return {"rule": rule, "level": level, "file": rel, "message": msg}


def check_mr01(gltf: dict, node_id: str, rel: str) -> list[dict]:
    """节点命名：根节点 name = node_id；根节点数 ≤1。"""
    out = []
    nodes = [n for n in gltf.get("nodes", []) if isinstance(n, dict)]
    scenes = gltf.get("scenes", [])
    root_idxs = []
    for s in scenes[:1]:  # 只取首个 scene
        root_idxs = [n for n in s.get("nodes", [])]
    root_names = [nodes[i].get("name") for i in root_idxs if i < len(nodes)]

    if node_id not in root_names:
        out.append(_finding("MR-01", "FAIL", rel,
                            f"根节点 name 应为 {node_id!r}，实际 {root_names}"))
    else:
        out.append(_finding("MR-01", "PASS", rel, f"根节点 name={node_id} 与 node_id 一致"))

    if len(root_idxs) > 1:
        out.append(_finding("MR-01", "WARN", rel,
                            f"场景根节点数 {len(root_idxs)} > 1（应为唯一根）"))
    return out


def check_mr02(gltf: dict, lod: str, rel: str) -> list[dict]:
    """三角面预算：逐 primitive 汇总，对照三档预算。"""
    out = []
    tri = count_triangles_exact(gltf)
    budget = LOD_BUDGETS[lod]["triangles"]
    label = LOD_BUDGETS[lod]["label"]
    if tri <= budget * OVER_WARN_FACTOR:
        out.append(_finding("MR-02", "PASS", rel,
                            f"三角面 {tri} ≤ {budget}（{label}）"))
    elif tri <= budget * OVER_FAIL_FACTOR:
        out.append(_finding("MR-02", "WARN", rel,
                            f"三角面 {tri} 超 {budget}（{label}）预算，未超 1.5 倍"))
    else:
        out.append(_finding("MR-02", "FAIL", rel,
                            f"三角面 {tri} 超 {budget}（{label}）预算 1.5 倍（{int(budget*OVER_FAIL_FACTOR)}）"))
    return out


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def check_mr03(gltf: dict, base_dir: str, rel: str) -> list[dict]:
    """贴图引用：material→image 文件名命名 + 纹理尺寸 ≤2048 且 2 的幂。"""
    out = []
    textures = [t for t in gltf.get("textures", []) if isinstance(t, dict)]
    images = [i for i in gltf.get("images", []) if isinstance(i, dict)]
    materials = [m for m in gltf.get("materials", []) if isinstance(m, dict)]

    seen = set()
    for m in materials:
        pbr = m.get("pbrMetallicRoughness", {}) or {}
        for slot in ("baseColorTexture", "metallicRoughnessTexture", "normalTexture", "emissiveTexture"):
            tinfo = pbr.get(slot) if slot in ("baseColorTexture", "metallicRoughnessTexture") else m.get(slot)
            if slot == "normalTexture":
                tinfo = m.get("normalTexture")
            if slot == "emissiveTexture":
                tinfo = m.get("emissiveTexture")
            if not tinfo:
                continue
            idx = tinfo.get("index")
            if idx is None or idx >= len(textures):
                continue
            src = textures[idx].get("source")
            if src is None or src >= len(images):
                continue
            if idx in seen:
                continue
            seen.add(idx)
            img = images[src]
            uri = img.get("uri") or img.get("name") or f"image[{src}]"
            name = os.path.basename(uri.split("?")[0].split("#")[0])

            # 命名后缀检查
            base = name.rsplit(".", 1)[0]
            if not any(base.endswith("_" + s) for s in TEXTURE_SUFFIXES):
                out.append(_finding("MR-03", "WARN", rel,
                                    f"贴图名 {name!r} 未命中后缀表 {TEXTURE_SUFFIXES}"))

            # 尺寸检查（仅外置文件，跳过 data URI）
            if uri.startswith("data:"):
                continue
            fp = os.path.join(base_dir, uri)
            if not os.path.isfile(fp):
                out.append(_finding("MR-03", "WARN", rel, f"贴图文件不存在：{uri}"))
                continue
            try:
                w, h = image_size_from_file(fp)
            except Exception as e:  # noqa: BLE001
                out.append(_finding("MR-03", "WARN", rel, f"贴图尺寸解析失败 {uri}：{e}"))
                continue
            if w > MAX_TEXTURE or h > MAX_TEXTURE:
                out.append(_finding("MR-03", "WARN", rel,
                                    f"贴图 {uri} 尺寸 {w}x{h} 超 {MAX_TEXTURE}px"))
            if not (_is_power_of_two(w) and _is_power_of_two(h)):
                out.append(_finding("MR-03", "WARN", rel,
                                    f"贴图 {uri} 尺寸 {w}x{h} 非 2 的幂"))

    if not out:
        out.append(_finding("MR-03", "PASS", rel, "无贴图或贴图均合规"))
    return out


def check_mr04(gltf: dict, rel: str) -> list[dict]:
    """单位与轴/扩展：未知扩展白名单外 WARN。"""
    out = []
    used = set(gltf.get("extensionsUsed") or [])
    required = set(gltf.get("extensionsRequired") or [])
    unknown = (used | required) - EXTENSION_WHITELIST
    if unknown:
        out.append(_finding("MR-04", "WARN", rel, f"未知扩展：{sorted(unknown)}"))
    else:
        out.append(_finding("MR-04", "PASS", rel, "扩展白名单内（或无扩展）"))
    return out


# ---------------------------------------------------------------------------
# 单文件 / 单包检查
# ---------------------------------------------------------------------------
def check_file(pkg: str, node_id: str, mesh_ref: str, lod: str) -> list[dict]:
    rel = mesh_ref
    fp = os.path.join(pkg, mesh_ref)
    if not os.path.isfile(fp):
        return [_finding("MR-01", "WARN", rel, f"mesh_ref 文件不存在：{mesh_ref}")]
    try:
        gltf = load_gltf(fp)
    except Exception as e:  # noqa: BLE001
        return [_finding("MR-01", "FAIL", rel, f"glTF 解析失败：{e}")]

    base_dir = os.path.dirname(fp)
    findings = []
    findings += check_mr01(gltf, node_id, rel)
    findings += check_mr02(gltf, lod, rel)
    findings += check_mr03(gltf, base_dir, rel)
    findings += check_mr04(gltf, rel)
    return findings


def check_package(pkg: str) -> dict:
    """对单个包跑全部 MR 规则，返回报告 dict。"""
    pkg = os.path.abspath(pkg)
    meta = read_meta(pkg)
    lod = resolve_lod(meta)
    device_id = (meta.get("meta") or {}).get("id") or os.path.basename(pkg)

    refs = mesh_refs(meta)
    files = []
    n_fail = 0
    n_warn = 0
    for node_id, mr in refs:
        findings = check_file(pkg, node_id, mr, lod)
        for f in findings:
            if f["level"] == "FAIL":
                n_fail += 1
            elif f["level"] == "WARN":
                n_warn += 1
        files.append({"mesh_ref": mr, "node_id": node_id, "findings": findings})

    return {
        "device_id": device_id,
        "lod": lod,
        "lod_label": LOD_BUDGETS[lod]["label"],
        "mesh_count": len(files),
        "fail": n_fail,
        "warn": n_warn,
        "files": files,
    }


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_report(rep: dict) -> str:
    lines = [f"== {rep['device_id']}（判档 {rep['lod']} {rep['lod_label']}，"
             f"{rep['mesh_count']} 个网格文件，FAIL {rep['fail']}，WARN {rep['warn']}）=="]
    for f in rep["files"]:
        lines.append(f"  {f['mesh_ref']}（node_id={f['node_id']}）")
        for fd in f["findings"]:
            lines.append(f"    {fd['level']:<4} {fd['rule']}  {fd['message']}")
    return "\n".join(lines)


def render_json(rep: dict) -> str:
    return json.dumps(rep, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="建模预算校验器（TASK-27A，v0.3 草案落地）")
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
