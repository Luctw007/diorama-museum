# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""gw.emulators 包：模拟器后端适配层。

每个后端模块实现 BackendBase（见 base.py），并由网关以
`python -m gw.emulators.<模块名>` 拉起为独立子进程（进程隔离，ADR D1）。
后端与网关之间的设备通道协议见 gw/PROTOCOL.md 第 2.2 / 5 章。
"""