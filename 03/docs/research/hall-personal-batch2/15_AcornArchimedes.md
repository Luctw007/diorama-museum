# 15 — Acorn Archimedes 研究卡

> 03 线 TASK-233-A 交付。第三批第 5 台（个人机，目录占位 `C-PC-0000xx`）的预研卡，为后续设备包领取备料。体例对齐 hall-personal-batch2 研究卡（第二批「一二三四五六七」七节）。模拟器主口径 `none`（无成熟模拟器，候选标需核实），不下发二进制、不下 ROM/系统镜像。

## 一、史实

**Acorn Archimedes** 是英国 Acorn Computers 于 1987 年推出的个人电脑，它的历史地位在于一个在今天看来石破天惊的事实：**它是第一台使用 ARM 处理器的商用电脑**。ARM（Acorn RISC Machine）是 Acorn 自主研发的 RISC 处理器，主打「低功耗、高性能」，最初就是为 Archimedes 而生。这颗 8MHz 的 ARM2 处理器，后来演化为 ARM 架构——今天全球几乎每一部智能手机、平板、嵌入式设备的处理器，都能追溯到这颗芯片。从这个意义上说，Acorn Archimedes 是「ARM 芯片帝国」的起点，也是英国计算机工业最深远的一次遗产。

| 项 | 值 | 来源 |
|---|---|---|
| 发布 | 1987 年 | [S125] |
| 制造商 | Acorn Computers | [S125] |
| CPU | ARM2（Acorn RISC Machine），8 MHz | [S125] |
| 架构 | RISC（精简指令集） | [S125] |
| 内存 | 标配 512KB，可扩展 | [S125] |
| 系统 | RISC OS（Arthur 的前身） | [S125] |

**叙事锚点**：
1. **ARM 芯片帝国的起点**：Acorn Archimedes 是首台 ARM 电脑，今天统治移动世界的 ARM 架构就从这颗 ARM2 起步 [S125]。
2. **RISC 的先行者**：Archimedes 的 ARM2 用精简指令集换高频高效，是 RISC 思想在个人电脑上的早期实践 [S125]。
3. **英国计算机的遗产**：Acorn 与 BBC Micro 一脉相承，Archimedes 是英国计算机工业「从教育机到自研芯片」的高光时刻 [S125]。
4. **ARM 的「低调崛起」**：ARM 后来从 Acorn 独立，凭借授权模式成为移动芯片的霸主，Archimedes 是这段传奇的起点。

## 二、尺寸依据（标「需核实」）

- 主机：约 40 cm 宽 × 30 cm 深 × 7 cm 高（三键鼠标式一体键盘机箱）（「需核实」）。
- 显示器：外接 CRT（「需核实」）。
- 三键鼠标：Acorn 独特的三键鼠标（「需核实」）。

## 三、部件分解草图清单

```
acorn_archimedes（整机）
├── case（一体机箱，键盘一体式）
├── motherboard（主板）
│   ├── cpu_arm2（ARM2 处理器）
│   ├── vidc_chip（VIDC 视频芯片）
│   ├── memc_chip（MEMC 内存控制器）
│   └── ram（内存，可扩展）
├── floppy_drive（软驱）
├── monitor（外接 CRT）
└── mouse（三键鼠标）
```

## 四、L1-L3 拆解要点

- **L1（外观层）**：一体机箱 + 三键鼠标 + 外接 CRT——静态呈现「1980 年代末英国电脑」的造型。
- **L2（结构层）**：打开机箱 → 主板、ARM2、VIDC/MEMC——拆解展示「首台 ARM 电脑里装了什么」。
- **L3（元件层）**：ARM2 的 RISC 架构、VIDC 图形、MEMC 内存控制——原理讲解用（RISC 如何用精简指令集换效率）。

## 五、模拟器行

**无成熟模拟器（emulator="none"，候选标需核实）**。

- **主口径**：按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，Acorn Archimedes 无广泛可用的成熟开源模拟器，`emulator="none"`（静态 + RISC 原理动画）。
- **候选**：Arculator、ArcEm 等 Acorn Archimedes 模拟器存在（许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入。
- **红线**：不下发二进制、不下 ROM/系统镜像（RISC OS 镜像受版权保护）；「可玩」以「RISC 原理动画 + ARM 起源叙事」承载。

## 六、出处清单（S125 起，续 IBM PC XT 卡的 S124）

| 编号 | 来源 | 类型 | URL | 许可 |
|---|---|---|---|---|
| S125 | Wikipedia — Acorn Archimedes | 网页 | https://en.wikipedia.org/wiki/Acorn_Archimedes | CC（BY-SA） |
| S126 | Computer History Museum — Acorn | 网页 | https://www.computerhistory.org/ | 视觉参考（visual_reference_only） |

## 七、展呈叙事建议（三行）

1. **ARM 的起点**：用 Acorn Archimedes 讲「首台 ARM 电脑」，把「英国教育电脑」与「今天统治手机的 ARM 架构」连成一条血脉。
2. **RISC 的先行者**：用 ARM2 的 RISC 架构对比 CISC，讲「精简指令集如何换高频高效」，是理解现代处理器设计的入门钥匙。
3. **低调的遗产**：讲 Acorn 如何从教育机厂商走到自研芯片，ARM 又如何通过授权模式成为移动芯片霸主，是「技术遗产」最动人的案例。

---

> 本卡供后续设备包取用；尺寸、模拟器候选许可/成熟度均已标「需核实」或来源标注。
