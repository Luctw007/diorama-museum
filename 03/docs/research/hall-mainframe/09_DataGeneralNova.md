# 09 — Data General Nova 研究卡

> 03 线 TASK-183-A 交付。第二批 3 号设备包（目录 `C-MC-000027`）的预研卡，供设备包全链取用。体例对齐 hall-personal-batch2/09 研究卡。目标模拟器 = Open SIMH Nova（本机可编译），只写交付要求、不下发二进制、不下 ROM/纸带镜像。

## 一、史实

**Data General Nova** 是美国 Data General 公司于 1969 年推出的 16 位小型计算机，是 DEC PDP-8 之后、PDP-11 之前「小型机战国时代」最具代表性的竞争者之一。它以低价、紧凑与「前面板拨键 + LED 跑灯」的经典操作方式闻名，16 位字长比 PDP-8 的 12 位更接近现代计算机的数据宽度。Data General 的创始人 **Edson de Castro** 原为 DEC 的工程师，出走创业后打造的 Nova，正面挑战了老东家的 PDP 系列。「Nova」意为「新星」，恰如其分——它确实是小型机星空中一颗耀眼的新星。

| 项 | 值 | 来源 |
|---|---|---|
| 发布 | 1969 年 | [S98] |
| 处理器 | Data General 自研 16 位 CPU（约 800 ns 周期，「需核实」） | [S98] |
| 字长 | 16 位 | [S98] |
| 内存 | 磁芯内存，4K 字起可扩展（「需核实」） | [S98] |
| 定价 | 低价小型机，约 8,000 美元起（「需核实」） | [S98] |
| 操作方式 | 前面板拨键开关 + LED 跑灯 | [S98] |
| 厂商 | Data General，创始人 Edson de Castro（原 DEC 工程师） | [S98] |
| 兼容仿制 | 中国 DJS-130 为 Nova 兼容仿制（中国小型机仿制史支线，「需核实」） | [S99] |

**叙事锚点**：
1. **出走 DEC 的挑战者**：Edson de Castro 离开 DEC 创立 Data General，用 Nova 正面竞争 PDP-8/PDP-11——「前员工造出更便宜的机器挑战老东家」，是小型机战国时代最生动的商业故事 [S98]。
2. **16 位架构的普及**：Nova 的 16 位字长比 PDP-8 的 12 位更接近现代计算机，是小型机从「够用」走向「好用」的一步 [S98]。
3. **低价小型机**：Nova 以低于 PDP-8 的价格切入市场，让更多实验室与产线买得起自己的计算机（约 8 千美元起，「需核实」）[S98]。
4. **前面板拨键 + 跑灯**：与 PDP-8 同源的拨键编程方式，是「人与机器对话」最原始的形态 [S98]。
5. **中国的 Nova 血统**：中国早期小型机 DJS-130 系列与 Nova 兼容，Nova 因此成为新中国计算机工业仿制史上的一支支线（「需核实」）[S99]。

## 二、尺寸依据（标「需核实」）

- 主机机箱：约 48 cm 宽 × 27 cm 高 × 50 cm 深（19 英寸机架或台式，「需核实」）。
- 前面板：约 48 cm 宽 × 13 cm 高，含数据/地址拨键开关阵列与状态 LED 灯条（「需核实」）。
- CPU 板：小型机板卡级，约 40 cm × 27 cm（「需核实」）。
- 内存背板：磁芯内存阵列，机架级（「需核实」）。
- 电源：内置线性电源（「需核实」）。
- I/O 接口：纸带读入机 + 电传打字机终端接口（「需核实」）。

## 三、部件分解草图清单

```
Data General Nova（整机）
├── 机箱（chassis，金属箱体）
├── 前面板（front_panel，拨键开关 + LED 跑灯）
│   ├── 数据拨键开关阵列（address/data switches）
│   └── 状态 LED 灯条（status LEDs）
├── CPU 板（cpu_board，16 位处理器）
├── 内存背板（memory_backplane，磁芯内存）
├── 电源（power_supply）
└── I/O 接口（io_interface，纸带读入机 + 终端）
```

## 四、L1-L3 拆解要点

- **L1（外观层）**：机箱 + 前面板拨键开关 + LED 跑灯——静态呈现「1969 年的小型机长什么样、怎么操作」。
- **L2（结构层）**：打开机箱 → CPU 板、磁芯内存背板、电源、I/O 接口——拆解展示「一台低价小型机的内部构成」。
- **L3（芯片层）**：16 位 CPU、磁芯存储阵列、LED 驱动电路——原理讲解用（拨键如何把 16 位地址/数据送入 CPU、磁芯如何存位是讲点）。

## 五、模拟器行

**Open SIMH Nova**（目标模拟器，许可「需核实」；SIMH 源码仓库 `https://github.com/open-simh/simh` 支持 Data General Nova）。统筹已确认本机可编译 SIMH 系模拟器，Nova 可加入 1.0 真跑矩阵。`runtime.emulator` 登记 `simh-nova`（槽位 `reserved` 预留），本任务不建 01 线槽位 manifest、不下发二进制、不下载 ROM/纸带镜像。「可玩」建议用自研复刻程序（拨键装小程序 + 跑灯反馈）承载，不依赖原机固件。

## 六、出处清单（S98 起，续 Altair 卡的 S97）

| 编号 | 来源 | 类型 | URL | 许可 |
|---|---|---|---|---|
| S98 | Wikipedia — Data General Nova | 网页 | https://en.wikipedia.org/wiki/Data_General_Nova | CC（BY-SA） |
| S99 | Wikipedia — Data General | 网页 | https://en.wikipedia.org/wiki/Data_General | CC（BY-SA） |
| S100 | Computer History Museum — Data General Nova | 网页 | https://www.computerhistory.org/ | 视觉参考（visual_reference_only） |

## 七、展呈叙事建议（三行）

1. **小型机战国时代**：把 Nova 与 PDP-8、PDP-11 并置，讲「DEC 一家独大 vs 前员工创业挑战」的竞争格局，是小型机厅「竞争催生进步」的最佳注脚。
2. **16 位的一步**：用「PDP-8 的 12 位 → Nova 的 16 位 → PDP-11 的 16 位」串起字长演进，点出「数据宽度如何一步步逼近现代计算机」。
3. **中国小型机的 Nova 血统**：用 DJS-130 兼容仿制的故事，把 Nova 与新中国计算机工业的仿制史连起来，是「技术扩散跨越国界」的生动一页（「需核实」）。

---

> 本卡供设备包直接取用；尺寸、定价、销量与 SIMH 许可均已标「需核实」或来源标注。
