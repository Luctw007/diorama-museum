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
目录 → 槽位媒体类目批量推定（TASK-62B，纯 stdlib）

给全部目录条目按「分类路径 + 关键词」规则推定 media_class（与 v0.5 槽位契约 §3.3 的
八类 media_class 枚举对齐），为槽位系统与未来媒体库预置分类——只输出建议表，不改他线文件。

media_class 枚举（v0.5 §3.3）：cartridge / disk / tape / cd / dvd / card / firmware /
app_package / 无（无介质）。

规则表（每条：匹配条件 + 输出 + 依据 + 置信度）见 RULES 常量；名称关键词精化见 REFINE。

用法：
    python media_infer.py [--content-dir <dir>] [--json]
    python media_infer.py --out-md <路径>    # 生成回填建议 Markdown

依赖：无（独立脚本）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# 路径定位
# ---------------------------------------------------------------------------
def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def work_root() -> str:
    return os.path.dirname(os.path.dirname(repo_root()))


def default_catalog_files() -> list[str]:
    roots = [os.path.join(work_root(), "03", "repo", "docs", "catalog"),
             os.path.join(work_root(), "05", "repo", "docs", "catalog")]
    files = []
    for root in roots:
        if os.path.isdir(root):
            files.extend(glob.glob(os.path.join(root, "*.jsonl")))
    return sorted(files)


# ---------------------------------------------------------------------------
# 规则表（匹配条件=大分类+中分类关键词；输出 media_class；依据=规则号；confidence）
# ---------------------------------------------------------------------------
RULES = [
    # (大分类, 中分类关键词, media_class, 规则号, 置信度)
    ("游戏机", "家用机", "cartridge", "R01", 0.9),
    ("游戏机", "掌机", "cartridge", "R02", 0.9),
    ("游戏机", "街机", "cartridge", "R03", 0.8),
    ("游戏机", "游戏电脑", "disk", "R04", 0.7),
    ("计算机", "个人机", "disk", "R10", 0.9),
    ("计算机", "小型机", "disk", "R11", 0.8),
    ("计算机", "大型机", "tape", "R12", 0.8),
    ("计算机", "早期计算机", "tape", "R13", 0.8),
    ("计算机", "手持计算", "firmware", "R14", 0.8),
    ("计算机", "服务器", "disk", "R15", 0.8),
    ("计算机", "工作站", "disk", "R16", 0.8),
    ("计算机", "超级计算机", "disk", "R17", 0.7),
    ("通讯与移动", "手机", "firmware", "R20", 0.8),
    ("通讯与移动", "PDA", "firmware", "R21", 0.8),
    ("通讯与移动", "传呼机", "firmware", "R22", 0.8),
    ("通讯与移动", "寻呼机", "firmware", "R23", 0.8),
    ("通讯与移动", "无绳电话", "firmware", "R24", 0.8),
    ("通讯与移动", "卫星电话", "firmware", "R25", 0.8),
    ("通讯与移动", "车载电话", "firmware", "R26", 0.8),
    ("通讯与移动", "固定电话", "无", "R27", 0.7),
    ("家电影音", "影音播放机", "cd", "R30", 0.7),
    ("家电影音", "影碟播放", "cd", "R31", 0.7),
    ("家电影音", "录像机", "tape", "R32", 0.9),
    ("家电影音", "音响", "cd", "R33", 0.6),
    ("家电影音", "随身听", "tape", "R34", 0.7),
    ("家电影音", "电视", "无", "R35", 0.7),
    ("办公与计算外设", "磁盘驱动器", "disk", "R40", 0.9),
    ("办公与计算外设", "存储外设", "disk", "R41", 0.8),
    ("办公与计算外设", "打印机", "无", "R42", 0.7),
    ("办公与计算外设", "显示器", "无", "R43", 0.7),
    ("办公与计算外设", "输入设备", "无", "R44", 0.7),
    ("办公与计算外设", "键鼠", "无", "R45", 0.7),
    ("办公与计算外设", "扫描仪", "无", "R46", 0.7),
    ("办公与计算外设", "调制解调器", "无", "R47", 0.7),
    ("办公与计算外设", "计算器", "无", "R48", 0.7),
    ("嵌入式与工业", "单板机", "firmware", "R50", 0.8),
    ("嵌入式与工业", "工控机", "firmware", "R51", 0.7),
    ("嵌入式与工业", "可编程控制器", "firmware", "R52", 0.7),
    ("嵌入式与工业", "单片机", "firmware", "R53", 0.7),
    ("其他", "", "无", "R60", 0.5),
]

# 名称关键词精化（覆盖基础规则，更高置信度）
REFINE = [
    # (关键词子串, media_class, 规则号, 置信度)
    ("VCD", "cd", "K01", 0.95),
    ("DVD", "dvd", "K02", 0.95),
    ("蓝光", "dvd", "K03", 0.9),
    ("智能手机", "app_package", "K04", 0.85),
    ("smartphone", "app_package", "K05", 0.85),
    ("随身听", "tape", "K06", 0.8),
    ("CD 机", "cd", "K07", 0.85),
    ("Walkman", "tape", "K08", 0.8),
    ("软驱", "disk", "K09", 0.9),
    ("磁带", "tape", "K10", 0.85),
]


# ---------------------------------------------------------------------------
# 推定
# ---------------------------------------------------------------------------
def infer_media(big: str, mid: str, name: str) -> dict:
    """按规则表推定 media_class，返回 {media_class, basis, confidence}。"""
    # 名称关键词精化优先
    for kw, mc, rule, conf in REFINE:
        if kw.lower() in str(name).lower():
            return {"media_class": mc, "basis": rule, "confidence": conf}
    # 基础规则：大分类 + 中分类关键词
    for rb, rmid, mc, rule, conf in RULES:
        if rb == big and (not rmid or rmid in mid):
            return {"media_class": mc, "basis": rule, "confidence": conf}
    # 兜底
    return {"media_class": "无", "basis": "FALLBACK", "confidence": 0.4}


# ---------------------------------------------------------------------------
# 扫描 + 推定
# ---------------------------------------------------------------------------
def run(files: list[str]) -> list[dict]:
    results = []
    for path in files:
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rid = obj.get("id", "?")
                name = obj.get("name") or obj.get("名称") or "?"
                p = obj.get("taxonomy_path") or obj.get("分类路径") or []
                big = p[0] if len(p) >= 1 else ""
                mid = p[1] if len(p) >= 2 else ""
                sub = p[2] if len(p) >= 3 else ""
                r = infer_media(big, mid, name)
                results.append({
                    "catalog_id": str(rid),
                    "name": str(name),
                    "big": big,
                    "mid": mid,
                    "sub": sub,
                    "media_class": r["media_class"],
                    "basis": r["basis"],
                    "confidence": r["confidence"],
                })
    return results


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render_md(results: list[dict], generated_at: str) -> str:
    lines = [
        "# 目录 → 媒体类目回填建议（自动生成，勿手改）",
        "",
        f"> 生成时间：{generated_at}　|　工具：`tools/index/media_infer.py`（TASK-62B）",
        f"> 共 {len(results)} 条目录推定；media_class 枚举与 v0.5 槽位契约 §3.3 对齐。",
        "",
        "## 一、低置信度清单（confidence < 0.6，需人工复核，置顶）",
        "",
    ]
    low = [r for r in results if r["confidence"] < 0.6]
    if low:
        lines.append("| catalog_id | 名称 | 大分类/中分类 | 推定 | 规则 | 置信度 |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in sorted(low, key=lambda x: x["confidence"])[:40]:
            lines.append(f"| {r['catalog_id']} | {r['name']} | {r['big']}/{r['mid']} | "
                         f"{r['media_class']} | {r['basis']} | {r['confidence']:.2f} |")
    else:
        lines.append("- （无）")

    lines += ["", "## 二、分中分类统计", ""]
    by_mid = Counter()
    mid_media = defaultdict(Counter)
    for r in results:
        key = f"{r['big']}/{r['mid']}" if r["mid"] else r["big"]
        by_mid[key] += 1
        mid_media[key][r["media_class"]] += 1
    lines.append("| 大分类/中分类 | 条数 | media_class 分布 |")
    lines.append("|---|---|---|")
    for key, n in by_mid.most_common():
        dist = "、".join(f"{mc}×{c}" for mc, c in mid_media[key].most_common())
        lines.append(f"| {key} | {n} | {dist} |")

    lines += ["", "## 三、置信度分布", ""]
    conf_dist = Counter()
    for r in results:
        c = r["confidence"]
        if c >= 0.9:
            conf_dist["高(≥0.9)"] += 1
        elif c >= 0.7:
            conf_dist["中(0.7~0.9)"] += 1
        else:
            conf_dist["低(<0.7)"] += 1
    for k, v in conf_dist.most_common():
        lines.append(f"- {k}：{v} 条")

    lines += ["", "## 四、全量建议表（截前 100 条）", ""]
    lines.append("| catalog_id | 名称 | media_class | 规则 | 置信度 |")
    lines.append("|---|---|---|---|---|")
    for r in results[:100]:
        lines.append(f"| {r['catalog_id']} | {r['name']} | {r['media_class']} | "
                     f"{r['basis']} | {r['confidence']:.2f} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="目录→媒体类目批量推定（TASK-62B）")
    p.add_argument("--content-dir", action="append", default=None,
                   help="追加扫描的 catalog 目录（可多次）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON（stdout）")
    p.add_argument("--out-md", default=None, help="回填建议 Markdown 输出路径")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.content_dir:
        files = []
        for d in args.content_dir:
            files.extend(glob.glob(os.path.join(d, "*.jsonl")))
        files = sorted(set(files))
    else:
        files = default_catalog_files()

    results = run(files)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    import datetime
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = render_md(results, generated_at)
    out = args.out_md or os.path.join(repo_root(), "docs", "media_infer_回填建议.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)

    # 控制台统计
    by_class = Counter(r["media_class"] for r in results)
    print(f"推定 {len(results)} 条目录：")
    for mc, n in by_class.most_common():
        print(f"  {mc:<14} {n} 条")
    low_n = sum(1 for r in results if r["confidence"] < 0.6)
    print(f"  低置信度（<0.6）：{low_n} 条")
    print(f"已生成：{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
