# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""defects 索引自动生成器（TASK-119）：扫描 docs/defects/DEFECT-RUN-*.md，
生成 docs/defects/index.md 索引表（非手工维护），避免台账遗漏。

体例（参照 gen_exhibit_index.py）：
  标题取自首行 `# DEFECT-RUN-XX（...）`；状态取自 `> 状态：` 行（含 closed →
  closed；含"待"/open/其他 → open）；修复提交取状态/修复节内 40 位以下十六进制
  提交哈希（取第一个）；关联任务取正文 TASK-\\d+[A-Z]? 编号。
  缺字段一律可降级：缺状态按 open 计；缺提交/任务留"-"；不崩溃。

用法：
  python 01/scripts/gen_defects_index.py            # 扫描并生成 index.md
  python 01/scripts/gen_defects_index.py --dry-run  # 只打印统计不写文件
退出码：0=成功；1=无缺陷文档可扫。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFECTS_DIR = os.path.join(REPO, "docs", "defects")
INDEX_PATH = os.path.join(DEFECTS_DIR, "index.md")

TITLE_RE = re.compile(r"^#\s+(DEFECT-RUN-\d+)\s*（(.+)）", re.M)
STATUS_RE = re.compile(r"^>\s*状态\s*[:：]\s*(.+)$", re.M)
HASH_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
TASK_RE = re.compile(r"TASK-\d+[A-Z]?")

# 待确认类标记优先于 closed：RUN-07「用户确认后置 closed」尚未 closed
PENDING_MARKS = ("待用户", "待确认", "待重测", "重测", "待用户确认")


def scan() -> list[dict]:
    out: list[dict] = []
    if not os.path.isdir(DEFECTS_DIR):
        return out
    for f in sorted(os.listdir(DEFECTS_DIR)):
        if not f.startswith("DEFECT-RUN-") or not f.endswith(".md"):
            continue
        path = os.path.join(DEFECTS_DIR, f)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        rid = f[:len(f) - 3]
        title = ""
        m = TITLE_RE.search(text)
        if m:
            title = m.group(2).strip()
        status, status_txt = "open", "-"
        m = STATUS_RE.search(text)
        if m:
            status_txt = m.group(1).strip()
            if any(mark in status_txt for mark in PENDING_MARKS):
                status = "open"          # 修复完成但待用户确认
            elif "closed" in status_txt.lower() or "已入 main" in status_txt:
                status = "closed"
        commit = "-"
        m = HASH_RE.search(status_txt)
        if not m:
            m = HASH_RE.search(text)
        if m:
            commit = m.group(0)[:7]
        tasks = sorted(set(TASK_RE.findall(text)))
        out.append({"id": rid, "title": title, "status": status,
                    "commit": commit, "tasks": ", ".join(tasks) or "-",
                    "file": f})
    return out


def render(rows: list[dict]) -> str:
    lines = [
        "# defects 索引（自动生成，勿手工编辑）",
        "",
        "> 由 `01/scripts/gen_defects_index.py` 扫描 `DEFECT-RUN-*.md` 生成。",
        "",
        "| 编号 | 标题 | 状态 | 修复提交 | 关联任务 |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append("| %s | %s | %s | %s | %s |"
                     % (r["id"], r["title"] or "-", r["status"],
                        r["commit"], r["tasks"]))
    closed = sum(1 for r in rows if r["status"] == "closed")
    opened = len(rows) - closed
    lines.append("")
    lines.append("计 %d 条：closed %d / open %d（缺状态按 open 计）"
                 % (len(rows), closed, opened))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="defects 索引自动生成")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    rows = scan()
    if not rows:
        print("未发现 DEFECT-RUN-*.md（%s）" % DEFECTS_DIR)
        return 1
    for r in rows:
        print("%-16s [%s] %s（提交 %s · 任务 %s）"
              % (r["id"], r["status"], r["title"] or "-", r["commit"], r["tasks"]))
    md = render(rows)
    if args.dry_run:
        print("--dry-run：不写文件")
    else:
        with open(INDEX_PATH, "w", encoding="utf-8") as fh:
            fh.write(md)
        print("已生成 %s" % INDEX_PATH)
    print(md.splitlines()[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())