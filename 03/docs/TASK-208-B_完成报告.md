# TASK-208-B 完成报告

> 第二批第 10 台 SPARCstation 1 产包准备（QEMU 需核实口径卡，不产包/不改目录 jsonl）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 产包口径卡 | `docs/research/hall-workstation/03_SPARCstation1产包口径卡.md` | 3,368 字节，三要素齐 |

## 验收日志

- **口径卡字节数**：03_SPARCstation1产包口径卡.md = 3,368 字节（>1200）。
- **三要素自检**：模拟器形态（§一）/ SunOS/Solaris 镜像红线（§二）/ 产包字段清单（§三）齐备，另含「需核实」清单（§四）与目录反链（§五）。
- **门禁只读复测**：`catalog_ingest.py --from-work --gate` → **摄取 5 文件 1582 行，错误 0**（本任务不改 jsonl，零回归）。

## emulator 口径裁决结果

- **保守 `emulator="none"`**：QEMU sparc 目标许可与成熟度「需核实」，且 01 线 `slots/emulators/` 无 qemu 槽位（无 bone 后端登记），按 02 线 187-A S 档「无 bone → none」口径落定。
- 若后续 QEMU 许可核实 + 01 线登记槽位，可升为 `emulator="qemu"`（GPL 隔离，独立进程 ADR D1，二进制不进仓库）。
- **SunOS/Solaris 镜像红线**：不入库、不下载、不提供、不再分发，只清单级引用；slots/media 用户自备。

## 需核实清单

尺寸（机身约 40×10×40 cm）、参数、QEMU sparc 许可与成熟度——193-B 已标「需核实」，本卡沿用。
