# TRS-80 Model I 研究简报（TASK-78A）

> 03 线 TASK-78A 备料。个人机厅第九台：1977 三杰之一的 TRS-80 Model I。

## 一、史实与来源

**TRS-80 Model I** 是 Tandy 公司通过其 Radio Shack 连锁零售店，于 1977 年 8 月发布的 8 位家用电脑。它与同年发布的 Apple II、Commodore PET 并称"1977 三杰"（1977 Trinity），是个人电脑元年最具代表性的三台机器之一。

| 参数 | 值 |
|---|---|
| 处理器 | Zilog Z80，主频 1.774 MHz |
| 内存 | 4KB（可扩至 48KB） |
| 显示 | 64×16 字符单色，128×48 块图形 |
| 键盘 | 53 键（与主机一体） |
| 存储 | 卡式磁带接口（另配录音机） |
| 电源 | 独立电源单元 |
| 售价 | 599.95 美元起 |
| BASIC | Level I BASIC（4KB）/ Level II BASIC（Microsoft BASIC） |

**形态特点**（任务书指定的建模要点）：Model I 采用"两件式"设计——**键盘主机一体**（主板 + Z80 + 键盘合在一个扁平盒子里）+ **独立的黑白显示器**（由 RCA 黑白电视改装）+ **独立的电源单元**；机身底部/背部有 **DIN 扩展口**（Expansion Interface，用于接软驱、打印机、额外内存）。外号 "Trash-80"（戏称）。

**历史地位**：凭借 Radio Shack 全美 3000+ 门店的零售网络，TRS-80 Model I 第一年销量即超 10 万台（远超 Tandy 最初 3000 台的估计），是 1977–1981 年间最畅销的个人电脑。它证明了"成熟零售渠道"对个人电脑普及的巨大作用。

**来源**：Wikipedia — TRS-80；Batocera Wiki — TRS-80；MAME 机器页（trs80 / trs80l2 romset）；Computer History Museum 时间线（访问日期 2026-11-04）。

## 二、模拟器方案（二选一，许可需核实）

| 方案 | 说明 | 许可 | 备注 |
|---|---|---|---|
| **trs80gp** | George Phillips 开发的 TRS-80 系列模拟器，Windows 平台，模拟 Model I/III/4 | Freeware（**需核实**） | 免费但非开源，再分发/嵌入需单独核实授权 |
| **MAME trs80 驱动** | MAME 的 `trs/trs80.cpp` 驱动，romset `trs80`（Level I）/ `trs80l2`（Level II） | GPL | 开源，但需 MAME 二进制与 ROM（BIOS 需合规） |

**本任务结论**：**二选一暂不落地真跑**，`runtime.emulator` 用 `"none"`（demo_mode 起步），槽位走 **dedicated 预留**。待 01/02 线在 `emulators_registry` 登记 trs80 后端（dedicated 槽位）并完成许可/ROM 合规后，再回填接线。**本任务不下载任何二进制**。

**ROM 红线**：TRS-80 Model I 的 Level I/Level II BASIC ROM 与软件磁带镜像受版权保护，本任务只做清单级引用，未下载、未提供任何 ROM/镜像。
