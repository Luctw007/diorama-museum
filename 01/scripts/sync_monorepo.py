# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""收口镜像自动化（TASK-96A）：一条命令把 02-05 各线 repo 镜像进 monorepo。

用法：python 01/scripts/sync_monorepo.py [--dry-run]
安全：只镜像、不 commit、不 push（人在环）；白名单排除 .git/__pycache__/.workbuddy/*.pyc。
注意（已踩坑）：robocopy 禁止接管道/Out-Null（会误报 rc=16）；rc<=7 均为成功。
非 Windows 平台：跳过 robocopy 并提示（镜像工作约定在 Windows 主机执行）。

TASK-226-B：源根路径参数化——DCM_WORK 环境变量优先，回退 D:/work（盘符路径）。
UNC 直连共享盘（无 D: 盘符映射）环境用法：
  $env:DCM_WORK="\\\\服务器\\共享\\work"; python 01/scripts/sync_monorepo.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

LINES = ("02", "03", "04", "05")
MONO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# TASK-226-B：共享工作根参数化（DCM_WORK 优先；回退 D:\work 保持既有行为）
WORK_ROOT = os.environ.get("DCM_WORK", r"D:\work")


def mirror_one(line: str, dry_run: bool = False) -> int:
    src = os.path.join(WORK_ROOT, line, "repo")
    dst = os.path.join(MONO, line)
    if not os.path.isdir(src):
        print("[skip] %s 线源目录缺失：%s" % (line, src))
        return 0
    # TASK-186-A：/E → /MIR（镜像语义：源删除则镜像删除）。
    # dry-run 走 /L 列表模式（不落盘），并打印将被删除的镜像独有文件清单。
    cmd = ["robocopy", src, dst, "/MIR",
           "/XD", ".git", "__pycache__", ".workbuddy",
           "/XF", "*.pyc"]
    if dry_run:
        cmd.append("/L")
    else:
        cmd += ["/NFL", "/NDL", "/NJH", "/NJS"]
    cp = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    rc = cp.returncode
    if rc > 7:
        print("[FAIL] %s 线 rc=%d\n%s" % (line, rc, cp.stderr[-800:]))
        return rc
    if dry_run:
        extras = [ln for ln in (cp.stdout or "").splitlines()
                  if "*EXTRA" in ln]
        print("[dry] %s 线将删除 %d 个镜像独有文件：" % (line, len(extras)))
        for ln in extras[:50]:
            print("   " + ln.strip())
        if len(extras) > 50:
            print("   ... 共 %d 条" % len(extras))
        return 0
    n = 0
    for root, _dirs, files in os.walk(dst):
        if "__pycache__" in root or ".git" in root:
            continue
        n += len(files)
    print("[ok] %s 线镜像完成 rc=%d，当前文件数 %d（%s）" % (line, rc, n, dst))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="收口镜像（只镜像，不提交）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if os.name != "nt":
        print("非 Windows 环境：robocopy 不可用，请在 Windows 主机执行收口镜像。")
        return 2
    if args.dry_run:
        print("dry-run（/MIR+/L 列表模式，不落盘）：")
        for line in LINES:
            rc = mirror_one(line, dry_run=True)
            if rc:
                return rc
        return 0
    for line in LINES:
        rc = mirror_one(line)
        if rc:
            return rc
    print("\n镜像完成。下一步（人工）：git add -A → commit → push（见 01/docs/github_setup.md §3）")
    return 0


if __name__ == "__main__":
    sys.exit(main())