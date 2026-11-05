# TASK-128 完成报告（02 线）

## 一、交付物

`emulators_registry.json` 26 → **30 条**；`emulators_registry.md` 用 gen_emulator_doc.py 重新生成。

## 二、合入 4 条（05 线 110-A 增补，字段逐条一致）

| sim_id | 目标设备 | 状态 | 许可 | 介质 |
|---|---|---|---|---|
| xm6-typeg | x68000 | reserved | 需核实 | disk |
| xm6i | x68000 | researched | 需核实 | disk |
| previous-next | NeXT 工作站 | reserved | 需核实 | disk |
| qemu-m68k | NeXT 工作站 | researched | GPL-2.0（需核实） | disk |

## 三、实跑日志

`gen_emulator_doc.py` → 已生成 30 条目的两份文档（emulators_registry.md + 模拟器清单_20261106.md）。

## 四、红线

不下载/不放置二进制；许可未核实标「需核实」；未升级 reserved/researched；不改 05 线增补页。
