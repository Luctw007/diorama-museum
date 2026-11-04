# TASK-68B 完成报告（03 线 2/2）：Amiga 500 设备包生产（个人机厅第七台）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-68B（03 线 2/2）：Amiga 500 设备包生产 |
| 前置 | TASK-68A（个人机厅第二批预研） |
| 择定 | Commodore Amiga 500（1987），demo_mode 起步，UAE 预留真跑后端 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `content/amiga500/meta.json` | era 1987、localized、category=personal-computer | 五字段齐备 |
| `content/amiga500/runtime.json` | demo_mode、external_crt+speaker+led、键盘+鼠标 input_map | 8 动作 |
| `content/amiga500/assemblies/*.gltf` ×5 | 占位盒，节点名=node_id | 5 件 |
| `content/amiga500/assemblies/MESHES.md` | 真实尺寸依据 | — |
| `content/amiga500/annotations/annotations.json` | 30 条（≥30） | 15 role + 1 whole + 14 flow |
| `content/amiga500/encyclopedia.md` | **2,528 汉字**（≥2500） | — |
| `content/amiga500/THIRD_PARTY.md` | 三件套 + UAE 预留 + Kickstart ROM 红线 | — |

校验：**validate 78 PASS / 0 FAIL**（退出码 0）+ **model_check MR-001~004 全过**（5/5 网格）。

## 二、五个占位盒与尺寸对照表

| assembly | 未来目标外观 | 尺寸依据 | 来源 |
|---|---|---|---|
| case | 机身壳（米色一体机，底部扩展仓盖） | 约 47×23×8 cm | Wikipedia（「需核实」） |
| keyboard | 键盘（一体式，含键盘仓与状态灯） | 与机身同宽 | Wikipedia（「需核实」） |
| motherboard | 主板（68000 + Agnus/Denise/Paula + Chip RAM） | 约 30×25 cm | Wikipedia — OCS（「需核实」） |
| floppy_drive | 3.5 英寸软驱（880KB） | 标准 3.5" 位 | Wikipedia |
| power | 外置电源 | 外置式 | Wikipedia（「需核实」） |

## 三、关键实现说明

1. **input_map 键盘 + 鼠标**：6 键盘动作 + 2 鼠标动作（`motion`/`btn_left`）+ 右键预留（`btn_right`），鼠标类按 R-086 合法键名，为 UAE 接线预留。
2. **display=external_crt**：Amiga 接电视/外接显示器，用 `external_crt` + `speaker` + `led` 共 3 个 output_sink。
3. **叙事锚点（flow）**：三芯片组分工、demo scene 文化、HAM 模式、多任务 AmigaOS、四声道立体声、880KB 软驱、Commodore 兴衰、Workbench 界面、游戏生态，共 14 条。
4. **UAE 预留**：`runtime.emulator="none"`（demo_mode），FS-UAE（GPLv2，本次已核实）仅在 THIRD_PARTY 登记为预留后端，未下载、未内嵌；Kickstart ROM 红线照旧。

## 四、与 C64 的对比台建议

Amiga 500 与 C64 同属 Commodore 一脉，建议在个人机厅"Commodore 之墙"并置，形成"从 8 位到 16 位"的家族叙事：

| 机 | 年代 | 叙事角色 |
|---|---|---|
| Commodore 64 | 1982 | 8 位国民电脑 + SID 芯片音乐 |
| Commodore Amiga 500 | 1987 | 16 位多媒体革命 + 三芯片组 |

- **对比点**：C64 的 SID 单芯片声音 vs Amiga 500 的 Paula 四声道立体声；C64 的 16 色 vs Amiga 500 的 4096 色 HAM——同一家公司，四年间完成了"从能唱到能演"的跨越。
- **互动建议**：可做"同一段旋律，SID vs Paula"的对比听感互动，直观感受声音硬件的代际跃迁。

## 五、TASK-68 两份总收尾

| 项 | 68-A 个人机厅第二批预研 | 68-B Amiga 500 包 |
|---|---|---|
| 交付物 | hall-personal-batch2/ 7 交付物 | content/amiga500/ |
| 规模 | 三台七节（3,536/2,783/2,585 汉字） | 78 PASS / 0 FAIL |
| 校验 | — | validate 0 FAIL + model_check 全过 |
| 状态 | 备料完成 | 新产包 1 台（目录已回填 done，全库 done 15） |

## 六、开放问题

1. **UAE 许可**：任务书原标「需核实」，本次检索已核实 UAE=GPL、FS-UAE=GPLv2，建议 02 线登记时采用。
2. **尺寸待核**：整机/主板尺寸为调研近真值，标「需核实」，正式建模以存世实机为准。
3. **Kickstart ROM**：真跑需经授权渠道（Amiga Forever 等）合规获取 ROM，本包未提供。
4. **MSX2+ 产包时机**：68-A 已备料，openMSX 覆盖完善，可排在 Amiga 500 之后。
