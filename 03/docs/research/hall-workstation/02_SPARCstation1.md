# 02 — Sun SPARCstation 1 研究卡

> 03 线 TASK-193-B 交付。第二批第 10 台（目录 `C-WS-000005`）的预研卡，为后续设备包领取备料。体例对齐 hall-workstation 研究卡。模拟器可行性标「需核实」，不下发二进制、不下 ROM/固件。

## 一、史实

**Sun SPARCstation 1** 是 Sun Microsystems 于 1989 年推出的 RISC 工作站，以「比冰箱还小的电脑」的营销口号闻名，被昵称为「披萨盒」。它把工作站的算力从笨重的大型机柜压缩进一个紧凑的桌面机箱，大幅降低了工作站的体积与成本，推动了 RISC 架构从实验室走向企业机房的普及。SPARCstation 1 是 Sun 微系统黄金年代的开端，也让 SPARC 架构与 SunOS/Solaris 成为 1990 年代 Unix 工作站的标志。

| 项 | 值 | 来源 |
|---|---|---|
| 发布 | 1989 年 | [S113] |
| 架构 | SPARC（RISC） | [S113] |
| 厂商 | Sun Microsystems | [S113] |
| 外号 | 「比冰箱还小的电脑」/「披萨盒」 | [S113] |
| 系统 | SunOS / Solaris | [S113] |
| 定位 | 桌面 RISC 工作站 | [S113] |

**叙事锚点**：
1. **RISC 走向桌面**：SPARCstation 1 把 RISC 架构的算力装进紧凑桌面机箱，是 RISC 从实验室走向普及的关键一步 [S113]。
2. **「披萨盒」的工业设计**：紧凑的桌面机箱形态，颠覆了「工作站 = 大机柜」的印象，是工作站小型化的标志 [S113]。
3. **Sun 黄金年代的开端**：SPARCstation 1 的成功为 Sun 带来巨大市场，开启了 Sun 在 1990 年代 Unix 工作站领域的辉煌 [S113][S114]。
4. **「网络即计算机」的硬件底座**：Sun 以「网络就是计算机」为理念，SPARCstation 1 正是这一理念的硬件载体 [S114]。

## 二、尺寸依据（标「需核实」）

- 主机：紧凑桌面机箱，约 40 cm 宽 × 10 cm 高 × 40 cm 深（「披萨盒」形态，「需核实」）。
- 显示器：外接 CRT 显示器（「需核实」）。
- 键盘：Sun 专用键盘（「需核实」）。
- 鼠标：三键光电鼠标（「需核实」）。

## 三、部件分解草图清单

```
Sun SPARCstation 1（整机）
├── 机身（case，紧凑桌面机箱）
├── 主板（motherboard，SPARC 处理器）
│   ├── SPARC 处理器
│   ├── 内存模块
│   └── 系统总线
├── 电源（power_supply）
├── 硬盘（disk，内置硬盘）
└── I/O 接口（io_ports，串行/并行/网络接口）
```

## 四、L1-L3 拆解要点

- **L1（外观层）**：紧凑桌面机箱 + 外接显示器/键盘/鼠标——静态呈现「1989 年的桌面工作站形态」。
- **L2（结构层）**：打开机箱 → 主板、SPARC 处理器、内存、硬盘——拆解展示「RISC 工作站内部」。
- **L3（芯片层）**：SPARC 处理器、RISC 指令集、内存模块——原理讲解用（RISC 精简指令集如何提速是讲点）。

## 五、模拟器行

**QEMU（sparc 目标）**（许可「需核实」，槽位 dedicated 预留，不下发二进制）。QEMU 支持 SPARC 目标模拟，是 SPARCstation 的候选模拟后端。真跑需 SunOS/Solaris 系统镜像合规获取（版权红线照旧，本卡仅清单级引用）。

## 六、出处清单（S113 起，续 Amiga 1000 卡的 S112）

| 编号 | 来源 | 类型 | URL | 许可 |
|---|---|---|---|---|
| S113 | Wikipedia — SPARCstation | 网页 | https://en.wikipedia.org/wiki/SPARCstation | CC（BY-SA） |
| S114 | Wikipedia — Sun Microsystems | 网页 | https://en.wikipedia.org/wiki/Sun_Microsystems | CC（BY-SA） |
| S115 | Computer History Museum — SPARCstation | 网页 | https://www.computerhistory.org/ | 视觉参考（visual_reference_only） |

## 七、展呈叙事建议（三行）

1. **RISC 走向桌面**：用 SPARCstation 1 的紧凑机箱与「披萨盒」外号，讲 RISC 架构如何从实验室走进企业机房，是工作站厅「从大型机柜到桌面」的转折锚点。
2. **Sun 的黄金年代**：把 SPARCstation 1 与 Sun 在 1990 年代的辉煌连起来，讲「RISC + Unix 工作站」如何统治专业计算，是工作站厅的一条主线。
3. **「网络即计算机」**：用 Sun 的这句口号，把 SPARCstation 1 与后来的互联网浪潮连起来，点出「工作站是网络时代的桥头堡」。

---

> 本卡供后续设备包取用；尺寸、参数与模拟器许可均已标「需核实」或来源标注。
