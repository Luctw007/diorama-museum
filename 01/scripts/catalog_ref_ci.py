# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""catalog_ref 的 monorepo 镜像适配器（TASK-96B；基径对齐修复 TASK-216-A）。

02 线工具 catalog_ref_check 原生支持 DCM_MONO 注入（见其 L56-88）：
无共享盘的 CI runner 设 DCM_MONO=<monorepo 根> 时，repo_root/work_root/line_repo
按镜像布局解析（<mono>/02、<mono>/<line>，无 "repo" 层）。
早期 monkeypatch repo_root/work_root 的 shim 因布局错位（多套一层 repo）导致
「内容包 0 个」，已退役——本适配器只做 DCM_MONO 注入 + 导入运行。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MONO = os.path.dirname(os.path.dirname(HERE))   # monorepo 根（01/ 的上一级）
TOOL_DIR = os.path.join(MONO, "02", "tools", "validate")

# TASK-216-A：使用 02 工具原生注入点（镜像布局），不再 monkeypatch
os.environ["DCM_MONO"] = MONO

sys.path.insert(0, TOOL_DIR)
import catalog_ref_check as C  # noqa: E402

if __name__ == "__main__":
    sys.exit(C.main())