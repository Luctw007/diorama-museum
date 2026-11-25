# 25 · PSP 产包准备卡（低模预研已齐，产包备料）

> 任务 315-P（05 线）· 完成日期：2026-11-26。
> 性质：**轻量产包准备卡**——315-D 已完成 PSP 低模预研（6 件拆分方案）。本卡产出**产包字段清单 + 目录条目方案 + PSP BIOS/ROM 红线 + 需核实清单**；**纯准备卡，不产包、不改目录。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `psp` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2004 | 23 号预研卡「2004」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线掌机谱系 |
| meta | manufacturer | Sony | 索尼（掌机线，非品类代表） |
| runtime | emulator | `none`（保守） | PSP BIOS/ROM 红线，无固件时保守 none（静态 + UMD 仓开合动画） |
| runtime | media_hint | `cd_rom` | UMD 光盘介质；**schema media_hint 枚举无 umd，取最接近的 cd_rom**（显式标注） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | handheld_lcd+speaker | 掌机用 handheld_lcd（对齐 game-boy/gba），非 crt_display |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/△○×□/摇杆/L/R 肩键/开始/选择 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | UMD 仓开合 anim、横置宽屏握持识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=23 号预研卡史实节（索尼首台掌机、横置宽屏 + UMD、多媒体能力强） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `gba`（310-O 掌机完整包体例）；PSP 与 GBA 同属掌机线，区别在于 **横置宽屏、6 件拆分（umd_drive/control_buttons）、UMD 光盘仓** 与 **media_hint 取 cd_rom（UMD 无枚举降级）**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| mips_cpu | MIPS CPU | chassis | PSP 主 CPU（MIPS R4000 双核） |
| gpu | GPU | chassis | PSP 图形芯片 |
| ram | 主内存芯片 | chassis | 32MB 主内存 |
| umd_motor | UMD 电机 | umd_drive | UMD 光驱电机 |

> GBA 低模无 mainboard 件先例：components 挂 chassis（对齐 310-O 口径）；umd_motor 挂 umd_drive。

### media_hint 口径说明（UMD → cd_rom）

- PSP 使用 **UMD（Universal Media Disc）** 介质，schema `media_hint` 枚举无 umd，产包时取最接近的 **`cd_rom`** 代指，并在 THIRD_PARTY 显式标注（对齐 Dreamcast GD-ROM 降级先例）。

## 二、目录条目方案

- **设备包 id**：`psp`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HH-000034「PlayStation Portable」`**（Sony、2004、planned）。产包时回填 status→done、device_id→psp，**无需新建条目**。

## 三、PSP BIOS/ROM 红线

- PSP 系统固件与游戏 ROM（UMD）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（PPSSPP）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + UMD 仓开合动画演示）。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | PSP-1000 约 170×23×74 mm 等 | [需核实]（沿用 23 号预研卡） |
| 配色 | 黑色机身 0.05,0.05,0.06 等 | [需核实] |
| CPU/内存 | MIPS R4000 双核 / 32MB 内存 | [需核实] |
| 模拟器候选许可 | PPSSPP | [需核实] |
| 介质 | UMD 光盘 | [需核实]（media_hint 取 cd_rom 代指） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；PSP BIOS/ROM 红线只清单级引用。
