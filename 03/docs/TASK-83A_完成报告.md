# TASK-83A 完成报告（03 线）：Commodore PET 2001 设备包（个人机厅第十台 · 1977 三杰收官）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。

| 项 | 内容 |
|---|---|
| 任务 | TASK-83A：Commodore PET 2001 设备包 |
| 前置 | 73-A（Atari ST）、78-A（TRS-80 Model I） |
| 状态 | 完成 |

## 交付物

- **research 简报**：`docs/research/pet2001_简报.md`（史实 + 模拟器二选一：VICE xpet=GPLv2【需核实】/ MAME pet=GPL，槽位 dedicated 预留，未下载二进制）。
- **内容包** `content/pet2001/`：meta（era 1977、category=personal-computer）/ runtime（demo_mode，internal_crt+speaker，5 键盘动作）/ 6 占位盒（一体机身壳、内置磁带机、chiclet 键盘、主板 6502、CRT 监视器、电源）/ annotations 30 条（三杰同台 1977、内置 BASIC、一体机设计、chiclet 小键盘等 flow 锚点）/ encyclopedia **2,542 汉字** / THIRD_PARTY 三件套 + ROM 红线。
- **目录联动**：`计算机大类_目录_v2.jsonl` 回填 `C-PC-000015` → status=**done**、device_id=pet2001（id 唯一、路径三级）。

## 校验

- `validate.py`：**84 PASS / 0 FAIL**。
- `model_check.py`：MR-001~004 全过（6/6 网格）。
- `catalog_check`：FAIL 0（CC-08 device_id 存在性 PASS）。
- `catalog_ref_check`：REF-01~04 全 0（**反链当天闭环**，内容包 24 个无反链缺失）。

## 说明

- 本轮"反链义务"落地：pet2001 包产出即回填目录 done + device_id，REF-02 反链缺失 0。
- glTF 节点名与 assembly id 一一对应，R-090 通过。
- 至此个人机厅"1977 三杰"（Apple II、TRS-80 Model I、Commodore PET 2001）三元组齐整，成为"互不兼容年代"叙事的第一块奠基石。

## 开放问题

1. VICE xpet 许可（GPLv2）需核实；MAME pet 驱动虽 GPL，但 BIOS/ROM 需合规。
2. 尺寸为调研近真值，标「需核实」；正式建模以存世实机为准。
