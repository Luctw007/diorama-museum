# 40 · Xbox 产包准备卡（低模已齐，产包备料）

> 任务 305-F（05 线）· 完成日期：2026-11-25。
> 性质：**轻量产包准备卡**——305-E 已完成 Xbox 低模样板（8 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + Xbox BIOS/ROM 红线 + 需核实清单**，供后续完整产包备料；**本卡不做产包/目录改动，纯准备卡。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `xbox` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2001 | 39 号预研卡「2001」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线游戏机谱系 |
| meta | manufacturer | Microsoft | 微软（游戏机线，非品类代表） |
| runtime | emulator | `none`（保守） | Xbox BIOS/ROM 红线，无 BIOS 时保守 none（静态 + 托盘弹出动画） |
| runtime | media_hint | `cd_rom` | DVD-ROM 介质；**schema media_hint 枚举无 dvd_rom，取最接近的 cd_rom**（见下方口径说明） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | crt_display+speaker | 对齐游戏机谱系（display+speaker） |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/模拟摇杆/开始/A/B 键等 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 托盘弹出 anim、手柄识别件、硬盘仓识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=18 号研究卡史实节（内置硬盘与以太网、微软入局） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `gamecube`（305-C）与 `playstation-2`（295-A）完整包体例；Xbox 与 PS2/GameCube 同属第六代主机，区别在于 **8 件低模拆分（含硬盘仓/以太网接口可选件）**、**内置硬盘用 hard_drive 件表达** 与 **media_hint 取 cd_rom（DVD-ROM 无枚举）**。

### 内置硬盘表达说明

- Xbox 标志性的内置硬盘以 **assembly 件 `hard_drive`** 表达（8 件低模之一），**不引入 schema 未定义的 storage 字段**（schema 无 storage 字段，避免超字段校验失败）。
- 硬盘的「内置存储」叙事通过 hard_drive 件的 role/flow 标注承载。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| pentium3 | Pentium III 级 CPU | mainboard | Xbox 主 CPU |
| nvidia_gpu | NVIDIA 图形芯片 | mainboard | Xbox 图形芯片 |
| ram | 主内存芯片 | mainboard | 64MB 主内存 |
| cd_motor | 光盘电机 | dvd_drive | DVD 光驱电机 |

### media_hint 口径说明（dvd_rom → cd_rom）

- Xbox 使用 DVD-ROM 介质，但 schema `media_hint` 枚举为 `["none", "cartridge", "disk", "firmware", "tape", "cd_rom", "floppy"]`，**无 dvd_rom**。
- 因此产包时 `media_hint` 取最接近的 **`cd_rom`**（光盘只读），并在 THIRD_PARTY/完成报告标注「DVD-ROM 无枚举，以 cd_rom 代指」（对齐 PS2 的 DVD-ROM 降级先例）。

## 二、目录条目方案

- **设备包 id**：`xbox`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录 `游戏机与手持大类_目录_v2.jsonl` 中**既有条目 `G-HC-000067「Xbox」`**（manufacturer=Microsoft、era=2001、status=planned、device_id=null）。产包时回填该条目 status→done、device_id→xbox，**无需新建条目、无需臆造 id**。

## 三、Xbox BIOS/ROM 红线

- Xbox 系统 BIOS 与游戏 ROM（DVD）受版权保护，**不入库、不下载**，产包仅做清单级引用（对齐 PlayStation/Saturn/N64/Dreamcast/PS2/GameCube BIOS 红线口径）。
- 真跑模拟器（Xemu）时 BIOS/ROM 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/光盘镜像。
- 若无法合规获取 BIOS，`runtime.emulator` 保守取 `none`（静态 + 托盘弹出动画演示），`bios_required=false`、`bios_guide_url=null`。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | Xbox 约 320×100×260 mm 等 | [需核实]（沿用 39 号预研卡） |
| 配色 | 黑色机身 0.10,0.10,0.12 等 | [需核实] |
| CPU/内存 | Pentium III 级 / 64MB 内存 | [需核实]（沿用 18 号研究卡） |
| 模拟器候选许可 | Xemu | [需核实] |
| 介质 | DVD-ROM + 内置硬盘 | [需核实]（media_hint 取 cd_rom 代指） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；Xbox BIOS/ROM 红线只清单级引用。
