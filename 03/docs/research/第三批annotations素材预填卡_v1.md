# 第三批 annotations 素材预填卡 v1

> 03 线 TASK-303-F 交付。第三批 10 台研究卡部件分解为产包 annotations 素材源，本卡做逐台部件→标注素材映射（L0 整机/L1 部件/L2 子部件/L3 代表件层级建议）。只改 03 目录，纯文档清单，不代产包。

## 一、10 台逐台部件→标注素材映射表

| 设备 | L0 整机 | L1 部件（≥3） | L2 子部件 | L3 代表件 |
|---|---|---|---|---|
| IBM System/370 | system370 整机系统 | 主机柜/控制台/磁带机/磁盘存储/打印机 | CPU+内存+微程序/指示灯拨钮 | 微程序控制/虚拟内存 DAT/通道 I/O |
| MSX2（FS-A1） | msx2p_fs-a1 整机 | 主机/分体键盘/主板/卡带/接口面板 | Z80/V9958/YM2149/FMPAC/RAM/VRAM | V9958 YJK 模式/FMPAC FM 合成 |
| Macintosh Plus | macintosh_plus 一体机 | 机壳/主板/软驱/键盘/鼠标 | 68000/1MB RAM/SCSI 控制器 | SCSI 总线/桌面出版 |
| IBM PC XT | ibm_pc_xt 整机 | 机箱/主板/硬盘/软驱/显示器/键盘 | 8088/RAM/8 ISA 槽 | 10MB 硬盘/ISA 总线 |
| Acorn Archimedes | acorn_archimedes 整机 | 机箱/主板/软驱/显示器/三键鼠标 | ARM2/VIDC/MEMC/RAM | ARM2 RISC 架构 |
| Sinclair ZX81 | sinclair_zx81 整机 | 机箱/键盘/主板/RF 调制器/电源 | Z80/ULA/RAM | ULA 合一芯片/1KB 内存 |
| SGI Indigo | sgi_indigo 整机 | 靛蓝机箱/主板/硬盘/显示器/键盘/鼠标 | MIPS R3000/图形引擎/RAM | 图形引擎/3D 渲染管线 |
| Compaq Portable | compaq_portable 整机 | 机箱/内置 CRT/主板/软驱/键盘 | 8088/BIOS/RAM | 净室逆向 BIOS |
| Whirlwind | whirlwind 整机系统 | 主机柜/磁芯内存柜/控制台/磁带机/电源冷却 | 真空管/磁芯模块 | 磁芯内存读写/实时计算 |
| Apple Newton | apple_newton 整机 | 机壳/触控 LCD/主板/电池/触控笔/扩展槽 | ARM 610/ROM/RAM | 手写识别/触控屏 |

## 二、素材缺口登记

- **0 缺口**：10 台研究卡部件分解均已覆盖 L1 部件 + L2 子部件 + L3 代表件，可作为 annotations 素材源直接取用。
- 产包时 annotations 的 role 文案须含「在整机」、flow 叙事锚点 ≥10（研究卡叙事锚点已备），「需核实」只进 encyclopedia/MESHES/THIRD_PARTY 不进 role/flow（R-060）。

## 三、取用声明

产包时按本卡取用研究卡部件分解为 annotations 素材源；本卡**不代产包**，仅做素材预填映射。

---

> 本卡为纯清单，不产包、不改 jsonl、不改研究卡原文。
