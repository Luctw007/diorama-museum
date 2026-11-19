# 13 — Macintosh Plus 研究卡

> 03 线 TASK-228-B 交付。第三批第 3 台（个人机，目录占位 `C-PC-0000xx`）的预研卡，为后续设备包领取备料。体例对齐 hall-personal-batch2 研究卡（第二批「一二三四五六七」七节）。与 `hall-personal-batch2/11_AppleIIe.md`、`content/macintosh128k` 系谱衔接。模拟器 Mini vMac 许可标「需核实」，不下发二进制、不下 ROM/系统镜像。

## 一、史实

**Macintosh Plus** 是 Apple 于 1986 年 1 月推出的 Macintosh 升级版，是 Mac 从「新奇」走向「实用化」的关键一步。它解决了初代 Macintosh（128K）最被诟病的短板——内存太小：Macintosh Plus 首次**标配 1MB 内存**（可扩展至 4MB），并首次引入 **SCSI 接口**，让 Mac 能外接硬盘、扫描仪等外设，真正具备了「干活」的能力。配合 800KB 双面软驱与 8MHz 的 68000 处理器，Macintosh Plus 成为 Mac 早期销量与口碑的重要担当，也让「桌面出版」这一 Mac 的标志性应用真正落地。

| 项 | 值 | 来源 |
|---|---|---|
| 发布 | 1986 年 1 月 | [S121] |
| 制造商 | Apple | [S121] |
| CPU | Motorola 68000，8 MHz | [S121] |
| 内存 | 标配 1MB，可扩展至 4MB | [S121] |
| 存储 | 800KB 双面软驱 + SCSI 接口（外接硬盘） | [S121] |
| 显示 | 9 英寸单色，512×342 | [S121] |

**叙事锚点**：
1. **Mac 走向实用化**：Macintosh Plus 用 1MB 内存 + SCSI 接口补足了初代 Mac 的短板，是「Mac 从玩具变工具」的转折点 [S121]。
2. **SCSI 接口的开端**：SCSI 让 Mac 能外接硬盘与扫描仪，是 Mac 专业工作流（桌面出版、图形设计）的硬件底座 [S121]。
3. **桌面出版的功臣**：Macintosh Plus 与 LaserWriter 激光打印机配合，催生了「桌面出版」革命，是 Mac 攻占设计与出版行业的关键 [S121]。
4. **68000 的 Mac 血脉**：Macintosh Plus 是 68000 家族在 Mac 线上的重要成员，与 Macintosh 128K 共同构成「初代 Mac 到 Plus 的完善之路」。

## 二、尺寸依据（标「需核实」）

- 一体机：约 34.5 cm 宽 × 24.4 cm 深 × 27.7 cm 高（「需核实」）。
- 9 英寸单色 CRT：约 512×342 分辨率（「需核实」）。
- 键盘/鼠标：外接分体（「需核实」）。

## 三、部件分解草图清单

```
macintosh_plus（一体机整机）
├── case（一体机壳，含 9 英寸单色 CRT）
├── motherboard（主板）
│   ├── cpu_68000（68000 处理器）
│   ├── ram（1MB 内存，可扩展）
│   └── scsi_controller（SCSI 控制器）
├── floppy_drive（800KB 双面软驱）
├── keyboard（外接键盘）
└── mouse（外接鼠标）
```

## 四、L1-L3 拆解要点

- **L1（外观层）**：一体机 + 键盘 + 鼠标——静态呈现「初代 Mac 的米色一体机造型」。
- **L2（结构层）**：打开机壳 → 主板、68000、内存、SCSI 控制器——拆解展示「Plus 补足了什么」。
- **L3（元件层）**：68000 处理器、SCSI 总线、1MB 内存——原理讲解用（SCSI 如何外接硬盘、内存扩展如何让 Mac 能干活）。

## 五、模拟器行

**Mini vMac（GPL，需核实）——Macintosh 128K/512K/Plus 的开源模拟器**。

- **Mini vMac**：面向早期 Macintosh（128K/512K/Plus/SE）的轻量开源模拟器，可运行早期 Macintosh 系统与软件。
- **许可**：GPL（「需核实」——需以 Mini vMac 官方仓库 LICENSE 为准；历史版本存在 GPLv2/GPLv2+ 表述差异）。
- **隔离口径**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；GPL 二进制不入库。
- **需核实**：Mini vMac 许可精确版本、Macintosh Plus ROM 与系统软件的合规获取路径（Apple ROM/系统镜像受版权保护）。
- **红线**：不下发二进制、不下 Apple ROM 与系统镜像；「可玩」以「桌面出版演示 + SCSI 外设讲解」承载。

## 六、出处清单（S121 起，续 System/370 卡的 S120）

| 编号 | 来源 | 类型 | URL | 许可 |
|---|---|---|---|---|
| S121 | Wikipedia — Macintosh Plus | 网页 | https://en.wikipedia.org/wiki/Macintosh_Plus | CC（BY-SA） |
| S122 | Computer History Museum — Macintosh | 网页 | https://www.computerhistory.org/ | 视觉参考（visual_reference_only） |

## 七、展呈叙事建议（三行）

1. **Mac 的完善之路**：把 Macintosh 128K 与 Macintosh Plus 连成「从玩具到工具」的叙事，讲 Plus 如何用内存 + SCSI 补足短板。
2. **桌面出版的革命**：用 Macintosh Plus + LaserWriter 讲「桌面出版」如何让设计排版从专业机房走进个人桌面。
3. **SCSI 的硬件底座**：用 SCSI 接口讲 Mac 如何外接硬盘与扫描仪，是理解「专业工作流」的入门钥匙。

---

> 本卡供后续设备包取用；尺寸、Mini vMac 许可版本、ROM/系统镜像路径均已标「需核实」或来源标注。
