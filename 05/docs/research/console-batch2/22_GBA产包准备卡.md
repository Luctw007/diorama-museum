# 22 · GBA 产包准备卡（低模已齐，产包备料）

> 任务 310-N（05 线）· 完成日期：2026-11-25。
> 性质：**轻量产包准备卡**——310-M 已完成 GBA 低模样板（5 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + GBA BIOS/ROM 红线 + 需核实清单**；**纯准备卡，不产包、不改目录。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `gba` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2001 | 20 号预研卡「2001」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线掌机谱系 |
| meta | manufacturer | Nintendo | 任天堂（掌机线，非品类代表） |
| runtime | emulator | `none`（保守） | GBA 固件/ROM 红线，无固件时保守 none（静态 + 卡带插拔动画） |
| runtime | media_hint | `cartridge` | 卡带介质，schema 有 `cartridge` 枚举，直接取用（无需降级） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | handheld_lcd+speaker | 掌机用 handheld_lcd（对齐 game-boy），非 crt_display |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/A/B/L/R 肩键/开始/选择 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 卡带插拔 anim、横置双手握持识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=掌机谱系卡史实节（32 位掌机、横版造型、游戏库庞大） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `game-boy`（掌机完整产包体例）；GBA 与 Game Boy 同属掌机线，区别在于 **横置机身、5 件拆分、肩键区、电池仓** 与 **output_sinks=handheld_lcd+speaker**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| arm7 | ARM7TDMI CPU | mainboard | GBA 主 CPU |
| ppu | 图形芯片 | mainboard | GBA 图形处理 |
| ram | 主内存芯片 | mainboard | 256KB 主内存 |
| sound_ic | 音源芯片 | mainboard | 音源处理 |

### media_hint 口径说明（cartridge 有枚举）

- GBA 使用卡带介质，schema `media_hint` 枚举含 `cartridge`，**直接取 cartridge、无需降级**（对齐 N64/Switch 的卡带口径）。

## 二、目录条目方案

- **设备包 id**：`gba`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HH-000027「Game Boy Advance」`**（Nintendo、2001、planned）。产包时回填 status→done、device_id→gba，**无需新建条目**。

## 三、GBA BIOS/ROM 红线

- GBA 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（mGBA）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + 卡带插拔动画演示）。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | GBA 约 144×24.5×82 mm 等 | [需核实]（沿用 20 号预研卡） |
| 配色 | 靛紫机身 0.45,0.30,0.55 等 | [需核实] |
| CPU/内存 | ARM7TDMI / 256KB 内存 | [需核实]（沿用掌机谱系卡） |
| 模拟器候选许可 | mGBA | [需核实] |
| 介质 | 卡带 | [需核实]（media_hint=cartridge） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；GBA BIOS/ROM 红线只清单级引用。
