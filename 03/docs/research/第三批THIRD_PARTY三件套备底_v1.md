# 第三批 THIRD_PARTY 三件套备底 v1

> 03 线 TASK-318-B 交付。补齐第三批 10 台 THIRD_PARTY 清册备底（许可分档/来源 URL/说明 + ROM 红线声明），供点头后 05 装配 `THIRD_PARTY.md`。有模拟器 4 台记候选模拟器许可，none 6 台记「无第三方资产」。只改 03 目录，纯文本备料，不产包、不改 jsonl。

## 一、10 台逐台清册草案

### 有模拟器 4 台（记候选模拟器许可）

| 设备 | 资产 | 类型 | 许可分档 | 来源 URL | 说明 |
|---|---|---|---|---|---|
| IBM System/370 | Hercules | 模拟器 | QPL（已核实） | https://www.hercules-390.eu/ | OSI 认证，不得分发修改副本，二进制不入库 |
| MSX2 | openMSX | 模拟器 | GPLv2（已核实） | https://openmsx.org/ | 开源 MSX 模拟器，二进制不入库 |
| Macintosh Plus | Mini vMac | 模拟器 | GPL（需核实） | https://www.gryphel.com/c/minivmac/ | GPLv2/GPLv2+ 表述差异待核实 |
| IBM PC XT | 86Box | 模拟器 | GPLv2（已核实） | https://86box.net/ | emulator id 用 pc86box，二进制不入库 |

### none 6 台（无第三方资产）

| 设备 | 资产 | 说明 |
|---|---|---|
| Acorn Archimedes | 无 | 候选 Arculator/ArcEm 记 THIRD_PARTY，本卡不下载 |
| Sinclair ZX81 | 无 | 候选 EightyOne/sz81 记 THIRD_PARTY，本卡不下载 |
| SGI Indigo | 无 | 候选 MAME/QEMU MIPS 记 THIRD_PARTY，本卡不下载 |
| Compaq Portable | 无 | 候选 86Box/PCem 记 THIRD_PARTY，本卡不下载 |
| Whirlwind | 无 | 无候选模拟器 |
| Apple Newton | 无 | 候选 Einstein 记 THIRD_PARTY，本卡不下载 |

## 二、ROM 红线声明（每台通用）

- IBM 操作系统镜像 / MSX2 BIOS ROM / Apple ROM 系统镜像 / IBM BIOS ROM 均「**不入库、不下载、不提供、不再分发**」，只清单级引用。
- 用户自备 slots/media；模拟器二进制不入库；「可玩」以「静态 + 原理动画」承载。

## 三、取用声明

产包时按本卡取用为 THIRD_PARTY.md 素材源；本卡**不代产包**、不写 content/<id>/、不下载任何模拟器/ROM。

---

> 本卡为纯文本备料，不写 content/<id>/THIRD_PARTY.md、不产包、不改 jsonl、不 allocate、不代点头。
