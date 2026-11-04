# TASK-78A 完成报告（03 线）：TRS-80 Model I 设备包（个人机厅第九台）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。

| 项 | 内容 |
|---|---|
| 任务 | TASK-78A：TRS-80 Model I 设备包 |
| 前置 | 73-A（Atari ST 0 FAIL） |
| 状态 | 完成 |

## 交付物

- **research 简报**：`docs/research/trs80-model1_简报.md`（史实来源 + 模拟器二选一：trs80gp=Freeware【需核实】/ MAME trs80 驱动=GPL，槽位走 dedicated 预留，未下载二进制）。
- **内容包** `content/trs80-model1/`：meta（era 1977、category=personal-computer）/ runtime（demo_mode，external_crt+speaker，5 键盘动作）/ 5 占位盒（键盘主机一体、黑白显示器、底部 DIN 扩展口、独立电源、卡式磁带机，节点名=node_id）/ annotations 30 条（1977 三杰、零售渠道、Trash-80、Level II BASIC、磁带存储等 flow 锚点）/ encyclopedia **2,557 汉字** / THIRD_PARTY 三件套 + ROM 红线。
- **目录联动**：`计算机大类_目录_v2.jsonl` 追加/回填 `C-PC-000033` → status=**package**、device_id=trs80-model1（id 前缀 C-PC 无 O-XX 冲突，taxonomy_path 三级齐全）。

## 校验

- `validate.py`：**78 PASS / 0 FAIL**（退出码 0）。
- `model_check.py`：MR-001~004 全过（5/5 网格）。
- `catalog_check`：FAIL 0（CC-08 device_id 存在性 PASS）。

## 说明

- 任务书要求目录条目 status=**package**（内容包生产中，非 done），已照办；device_id 指向本包，CC-08 悬空引用检查通过。
- glTF 节点名与 assembly id 一一对应（keyboard_unit/monitor/expansion_interface/power/cassette_recorder），R-090 通过。
- 模拟器按任务书"二选一注明许可需核实"处理，未落地真跑、未下载二进制。

## 开放问题

1. trs80gp 许可（Freeware）需核实；MAME trs80 驱动虽 GPL，但 BIOS/ROM 需合规。
2. 尺寸为调研近真值，标「需核实」；正式建模以存世实机为准。
