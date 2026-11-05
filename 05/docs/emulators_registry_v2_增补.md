# 模拟器官方档案 · 增补页（emulators_registry_v2_增补）

> 任务：TASK-110A（05 线 · 轻量）· 供 02 线合入 `emulators_registry.json` 的增补候选。
> 本页只做清单级引用，**不下载、不放置任何二进制**；license 未核实一律标「需核实」。
> 状态沿用母表语义：bone=成熟可接入 / reserved=预留待映射 / researched=调研中。

## xm6-typeg
- 名称：XM6 TypeG（X68000 模拟器，Windows）
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 目标设备：x68000
- 许可：需核实　|　URL：需核实
- 介质类目：disk
- 风险：IPL ROM / SCSI ROM / Human68k 均**字样级引用，红线不下载**（用户在 slots/ 自备）

## xm6i
- 名称：XM6i（X68000 模拟器，Windows）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 目标设备：x68000
- 许可：需核实　|　URL：需核实
- 介质类目：disk
- 风险：同 XM6 TypeG，IPL ROM / SCSI ROM / Human68k 字样级引用、不下载

## previous-next
- 名称：Previous（NeXTSTEP 开源后继模拟器）
- 后端类型：dedicated　|　状态：reserved　|　后端：预留
- 目标设备：NeXT 工作站
- 许可：需核实　|　URL：需核实
- 介质类目：disk
- 风险：演示向为主，NeXTSTEP 系统镜像字样级引用、不下载

## qemu-m68k
- 名称：QEMU m68k（NeXT 裸机路线）
- 后端类型：dedicated　|　状态：researched　|　后端：预留
- 目标设备：NeXT 工作站（m68k 路线）
- 许可：GPL-2.0（需核实）　|　URL：https://www.qemu.org
- 介质类目：disk
- 风险：NeXT 裸机支持成熟度需核实，系统镜像不下载

---

> 备注：以上 4 条对应 03 线 103-A（X68000 设备包，runtime 已用 emulator="none" demo_mode + XM6 槽位预留）与 103-B（NeXT 研究卡，Previous 演示向预留）。合入母表由 02 线下轮执行，本页不改动 emulators_registry.json。
