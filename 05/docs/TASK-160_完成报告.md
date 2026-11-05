# TASK-160 完成报告（键位速查终检表）

> 任务 160（05 线）· 完成日期：2026-11-06。

## 交付
`console-batch2/键位速查终检表_20261106.md`。

## 三态汇总
- **一致**（3 台）：apple2（57）/ atari-2600（12）/ famicom（18），05 runtime 动作名与 01 线 keymap entries 键名逐键一致、无遗漏无多余。
- **待核实**（8 台）：sega-md / neo-geo-mvs / sfc / game-boy / GG / Lynx / TurboExpress——01 线尚未登记 keymap，非契约冲突。

## need_verify 现状
apple2 实测 verify=true **21**（文档登记 14 已过期，01 侧 +7）、atari-2600 12、famicom 18，均**未消项**。

## 不一致清单
本轮无动作名不一致项；DEFECT-M1B-KEYMAP-01 已 closed、无回归。**未写 01 repo 任何文件**。

## 文件大小
终检表 **1993 字节**，正文 304 字（表格为主）。
