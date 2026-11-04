# Commodore VIC-20 研究简报（TASK-93A）

> 03 线 TASK-93A 备料。定案表 27# 领取，个人机厅第十一台。详细预研卡见 `docs/research/hall-personal-batch2/03_VIC20.md`。

## 一、史实

Commodore VIC-20（1980 日本版 VIC-1001 / 1981 欧美版 VIC-20）：6502 CPU 1.02MHz、5KB 内存、VIC 彩色图形芯片、键盘主机一体、外置数据磁带机、接电视、售价 299.95 美元。**首台销量破百万的个人电脑**（1983 年达成），Commodore "低价家用电脑"战略的开端。来源：[S87][S88]。

## 二、尺寸依据（标「需核实」）

整机约 40×20×6 cm（键盘主机一体）；Datasette 磁带机外置。「需核实」，正式建模以存世实机为准。

## 三、模拟器方案

**VICE xvic（GPLv2，许可需核实）**，槽位 dedicated 预留，**不下载二进制**。VICE 主项目已登记 02 线 registry（sim_id=vice），xvic 是其 VIC-20 子驱动。真跑需 BASIC ROM + 字符 ROM 合规获取。

**ROM 红线**：BASIC ROM 与字符 ROM 受版权保护，本任务只做清单级引用，未下载、未提供任何 ROM/镜像。
