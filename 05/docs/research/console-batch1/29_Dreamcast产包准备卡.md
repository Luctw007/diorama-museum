# 29 · Sega Dreamcast 产包准备卡（低模已齐，产包备料）

> 任务 280-B（05 线）· 完成日期：2026-11-21。
> 性质：**轻量产包准备卡**——280-A 已完成 Sega Dreamcast 低模样板（8 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + Dreamcast BIOS/ROM 红线 + 需核实清单**，供后续完整产包备料；**本卡不做产包/目录改动，纯准备卡。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `sega-dreamcast` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 1998 | 28 号预研卡「1998」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线游戏机谱系 |
| meta | manufacturer | Sega | 世嘉（游戏机线，非品类代表） |
| runtime | emulator | `none`（保守） | Dreamcast BIOS/ROM 红线，无 BIOS 时保守 none（静态 + 开盖放碟动画） |
| runtime | media_hint | `cd_rom` | GD-ROM 介质；**schema media_hint 枚举无 gd_rom，取最接近的 cd_rom**（见下方口径说明） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | crt_display+speaker | 对齐游戏机谱系（display+speaker） |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/模拟摇杆/开始/A/B 键等 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 开盖放碟动画用 anim 承载；gd_drive 光盘盖开合、vmu 记忆卡识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=18 号研究卡史实节（世嘉谢幕、首台内置调制解调器） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `nintendo-64`（275-A）与 `sega-saturn`（265-A）完整包体例；Dreamcast 与 PS/Saturn/N64 同属世嘉/主机谱系，区别在于 **8 件低模拆分（含 VMU/调制解调器可选件）** 与 **media_hint 取 cd_rom（GD-ROM 无枚举）**。

### media_hint 口径说明（gd_rom → cd_rom）

- Dreamcast 使用 GD-ROM 专用光盘介质，但 schema `media_hint` 枚举为 `["none", "cartridge", "disk", "firmware", "tape", "cd_rom", "floppy"]`，**无 gd_rom**。
- 因此产包时 `media_hint` 取最接近的 **`cd_rom`**（光盘只读），并在 THIRD_PARTY/完成报告标注「GD-ROM 无枚举，以 cd_rom 代指」。

## 二、目录条目方案

- **设备包 id**：`sega-dreamcast`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录 `游戏机与手持大类_目录_v2.jsonl` 中**既有条目 `G-HC-000064「Sega Dreamcast」`**（manufacturer=Sega、era=1998、taxonomy_path=["游戏机","家用机","第 1~9 世代"]、status=planned、device_id=null）。产包时回填该条目 status→done、device_id→sega-dreamcast，**无需新建条目、无需臆造 id**。

## 三、Dreamcast BIOS/ROM 红线

- Dreamcast BIOS 与游戏 ROM（GD-ROM）受版权保护，**不入库、不下载**，产包仅做清单级引用（对齐 PlayStation/Saturn/N64 BIOS 红线口径）。
- 真跑模拟器（Flycast / Demul）时 BIOS/ROM 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/光盘镜像。
- 若无法合规获取 BIOS，`runtime.emulator` 保守取 `none`（静态 + 开盖放碟动画演示），`bios_required=false`、`bios_guide_url=null`。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | Dreamcast 约 190×75×200 mm 等 | [需核实]（沿用 28 号预研卡） |
| 配色 | 白色机身 0.85,0.85,0.85 等 | [需核实] |
| CPU/内存 | SH-4 CPU / 16MB 主 RAM | [需核实]（沿用 18 号研究卡） |
| 模拟器候选许可 | Flycast / Demul | [需核实] |
| 介质 | GD-ROM | [需核实]（media_hint 取 cd_rom 代指） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；Dreamcast BIOS/ROM 红线只清单级引用。
