# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""贡献者自测包内容清单生成 + 黑名单自检（TASK-172-A，02 线侧）。

定位：为 01 线 contrib_kit 补齐"02 线侧可机器核验的清单生成"。**只读扫描，不产出 zip**，
不改任何被扫描文件；打包仍由 01 线 make_contrib_kit.py 负责（避免越界）。

收录范围（与 make_contrib_kit.py 对齐）：
  1. tools/validate/ 下顶层 *.py（仅校验器本体，**不含 tests/**）
  2. content/schema/device_spec.schema.json
  3. docs/贡献者自测包说明_v1.2.md
对每个收录文件做：存在性检查 → 扩展名黑名单 → 字样黑名单 → md5。
黑名单 BLOCK_EXTS / BLOCK_SUBSTR 与 01 线 make_contrib_kit.py **逐项一致，不另立一套**。

产出：docs/自测包内容清单_v1.2.md（条目表 + 汇总行 + 版本号 v1.2）。
退出码：全过 0；任一文件缺失 / 违规 1。

用法：
  python tools/contrib_kit/build_content_manifest.py
"""

from __future__ import annotations

import hashlib
import os
import sys

# 黑名单与 01 线 make_contrib_kit.py 逐项对齐（禁止另立一套）
BLOCK_EXTS = {".exe", ".bin", ".rom", ".img", ".iso", ".zip", ".7z", ".rar",
              ".pyc", ".pyo", ".dll", ".so", ".bat", ".cmd", ".jar",
              ".png", ".jpg", ".jpeg", ".gif", ".gltf", ".wav", ".mp3"}
BLOCK_SUBSTR = ("ghp_", "x-access-token", "password", "credential",
                "private key", "begin rsa")

VERSION = "v1.2"

# 收录条目：相对 repo 根的三类路径
VALIDATE_DIR = os.path.join("tools", "validate")
SCHEMA_REL = os.path.join("content", "schema", "device_spec.schema.json")
README_REL = os.path.join("docs", "贡献者自测包说明_v1.2.md")
OUT_REL = os.path.join("docs", "自测包内容清单_v1.2.md")


def repo_root() -> str:
    """本脚本位于 <repo>/tools/contrib_kit/，返回 <repo> 根目录。"""
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", ".."))


def check_file(full: str) -> str | None:
    """对单个文件做黑名单检查，返回违规描述字符串；无违规返回 None。"""
    name = os.path.basename(full).lower()
    ext = os.path.splitext(name)[1].lower()
    if ext in BLOCK_EXTS:
        return "黑名单扩展名拦截: %s" % full
    for s in BLOCK_SUBSTR:
        if s in name:
            return "黑名单字样拦截: %s（%s）" % (s, full)
    return None


def md5_of(full: str) -> str:
    h = hashlib.md5()
    with open(full, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_targets(root: str) -> list[tuple[str, str]]:
    """返回 [(相对路径, 绝对路径)]，按收录范围三类组装。

    相对路径用正斜杠，便于写入 markdown 与跨平台引用。
    """
    targets: list[tuple[str, str]] = []

    # 1) tools/validate/ 顶层 *.py（不含 tests/）
    vdir = os.path.join(root, *VALIDATE_DIR.split(os.sep))
    if os.path.isdir(vdir):
        for name in sorted(os.listdir(vdir)):
            full = os.path.join(vdir, name)
            if os.path.isfile(full) and name.endswith(".py"):
                targets.append((VALIDATE_DIR.replace(os.sep, "/") + "/" + name, full))

    # 2) schema
    targets.append((SCHEMA_REL.replace(os.sep, "/"),
                    os.path.join(root, *SCHEMA_REL.split(os.sep))))

    # 3) 说明 v1.2
    targets.append((README_REL.replace(os.sep, "/"),
                    os.path.join(root, *README_REL.split(os.sep))))

    return targets


def build(root: str) -> dict:
    targets = collect_targets(root)
    rows: list[dict] = []
    violations: list[str] = []
    total_bytes = 0

    for rel, full in targets:
        if not os.path.isfile(full):
            violations.append("缺失: %s" % rel)
            rows.append({"rel": rel, "size": 0, "md5": "—", "status": "缺失"})
            continue
        v = check_file(full)
        if v is not None:
            violations.append(v)
            rows.append({"rel": rel, "size": os.path.getsize(full),
                         "md5": "—", "status": "违规"})
            continue
        size = os.path.getsize(full)
        total_bytes += size
        rows.append({"rel": rel, "size": size, "md5": md5_of(full), "status": "OK"})

    return {
        "targets": targets,
        "rows": rows,
        "violations": violations,
        "total_bytes": total_bytes,
        "count": len(rows),
    }


def render_md(res: dict) -> str:
    lines: list[str] = []
    lines.append("# 贡献者自测包内容清单 v1.2")
    lines.append("")
    lines.append("> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。")
    lines.append(">")
    lines.append("> 本清单由 `tools/contrib_kit/build_content_manifest.py` **自动生成**（勿手改）；")
    lines.append("> 只做只读扫描与黑名单自检，不产出 zip（打包仍在 01 线 `make_contrib_kit.py`）。")
    lines.append("")
    lines.append("| # | 相对路径 | 大小(字节) | md5 | 状态 |")
    lines.append("|---|---|---|---|---|")
    for i, r in enumerate(res["rows"], 1):
        lines.append("| %d | `%s` | %d | %s | %s |"
                     % (i, r["rel"], r["size"], r["md5"], r["status"]))
    lines.append("")
    n = res["count"]
    viol = len(res["violations"])
    lines.append("汇总：条目 %d / 总字节 %d / 违规 %d"
                 % (n, res["total_bytes"], viol))
    lines.append("")
    lines.append("版本号：%s" % VERSION)
    lines.append("")
    if res["violations"]:
        lines.append("## 违规明细")
        for v in res["violations"]:
            lines.append("- %s" % v)
    else:
        lines.append("## 自检结论")
        lines.append("- 全部收录文件存在、扩展名/字样黑名单零命中、md5 已生成，违规 0。")
    return "\n".join(lines) + "\n"


def main() -> int:
    root = repo_root()
    res = build(root)

    # 终端输出（供验收贴日志）
    print("自测包内容清单生成（版本 %s）" % VERSION)
    print("repo 根：%s" % root)
    for r in res["rows"]:
        print("  [%s] %s  %d B  %s" % (r["status"], r["rel"], r["size"], r["md5"]))
    print("汇总：条目 %d / 总字节 %d / 违规 %d"
          % (res["count"], res["total_bytes"], len(res["violations"])))
    for v in res["violations"]:
        print("  违规：%s" % v)

    out = os.path.join(root, *OUT_REL.split(os.sep))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(render_md(res))
    print("已写入：%s" % out)

    return 1 if res["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
