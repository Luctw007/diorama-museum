# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""gw 包：模拟器网关与后端适配层。

- gw/gateway.py            网关主进程（TCP 控制通道 + 后端进程管理）
- gw/PROTOCOL.md           通信协议契约（v2，向下兼容 v1）
- gw/emulators/            模拟器后端（base.py 骨架 + fake_emulator 测试后端 + rle 编解码）
约定：后端永远以独立子进程运行（设计文档 ADR D1，进程隔离），
与网关之间只通过 stdio 上的 JSON lines 通信（见 PROTOCOL.md 第 2.2 / 5 章）。
"""

__version__ = "0.2.0"
PROTOCOL_VERSION = 2