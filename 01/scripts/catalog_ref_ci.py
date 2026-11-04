# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""catalog_ref 的 monorepo 镜像适配器（TASK-96B）。

02 线工具 catalog_ref_check 以"自身文件位置上溯两级"推导共享盘根（D:/work），
CI runner 上无共享盘 → 镜像布局下会误判。本适配器不改 02 线文件，仅以
monkeypatch 方式把 repo_root/work_root 指到 monorepo 镜像根后运行其 main()。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MONO = os.path.dirname(os.path.dirname(HERE))   # monorepo 根（01/ 的上一级）
TOOL_DIR = os.path.join(MONO, "02", "tools", "validate")

sys.path.insert(0, TOOL_DIR)
import catalog_ref_check as C  # noqa: E402

C.repo_root = lambda: os.path.join(MONO, "02")
C.work_root = lambda: MONO

if __name__ == "__main__":
    sys.exit(C.main())