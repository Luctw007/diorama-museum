# TASK-208-A 完成报告

> 第二批 9 号设备包：Commodore Amiga 1000（目录 `C-PC-000021`，个人机）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡（复用） | `docs/research/hall-personal-batch2/10_Amiga1000.md` | 193-B 已产，本任务复用（证据 S110–S112） |
| meta.json | `content/amiga-1000/meta.json` | id=amiga-1000、era=1985、category=personal-computer、manufacturer=Commodore |
| runtime.json | `content/amiga-1000/runtime.json` | emulator=`uae`（GPL 隔离）、sinks=external_crt+speaker、input_map 8 动作（5 键盘 + 3 鼠标） |
| assemblies | `content/amiga-1000/assemblies/` | 7 装配（whole + 机身/键盘/主板/软驱/鼠标/显示器 6 件 glTF）+ MESHES.md |
| annotations | `content/amiga-1000/annotations/annotations.json` | 31 条（**flow 10** + role 21） |
| encyclopedia | `content/amiga-1000/encyclopedia.md` | **2,510 汉字**（≥2500） |
| THIRD_PARTY | `content/amiga-1000/THIRD_PARTY.md` | 三件套 + UAE GPL 隔离声明 + Kickstart ROM 红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/amiga-1000` → **84 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-PC-000021` → `planned→done`、`device_id null→amiga-1000`、`research_doc null→docs/research/hall-personal-batch2/10_Amiga1000.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0），CC-08 PASS 32；`catalog_ref_check.py` → **FAIL 0**。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## UAE/Kickstart 口径对齐结果

- **`emulator="uae"`**：对齐 203-B 产包口径卡（UAE GPL 隔离形态）。UAE 集成走独立进程 + 协议通信隔离（不链接、不派生），运行不构成许可传染；随仓库分发 UAE 二进制须另行法律评估，故仓库不随附。
- **Kickstart ROM 红线**：不入库、不下载、不提供、不再分发，只清单级引用；slots/media 由用户自备。
- **flow 锚点**：多媒体电脑概念、预占多任务、沃霍尔现场作画、三芯片组分工、Kickstart 机制、与 Macintosh 竞争等 10 条。

## 说明

- **category=personal-computer**（对齐 amiga500 等既有个人机包，任务书「personal」为简写）。
- **版权红线**：未下载任何 Kickstart ROM/磁盘镜像/二进制。

## 开放问题

1. 目录中 Amiga 1000 真实 id 确为 `C-PC-000021`（与定案表 v2 草案一致）。
2. 尺寸（约 43×9×34 cm）、内存 256 KB 起、UAE 具体许可条款均已标「需核实」。
