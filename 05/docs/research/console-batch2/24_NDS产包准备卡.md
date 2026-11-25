# 24 · NDS 产包准备卡（低模预研已齐，产包备料）

> 任务 315-N（05 线）· 完成日期：2026-11-26。
> 性质：**轻量产包准备卡**——315-D 已完成 NDS 低模预研（6 件拆分方案）。本卡产出**产包字段清单 + 目录条目方案 + NDS BIOS/ROM 红线 + 需核实清单**；**纯准备卡，不产包、不改目录。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `nintendo-ds` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2004 | 23 号预研卡「2004」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线掌机谱系 |
| meta | manufacturer | Nintendo | 任天堂（掌机线，非品类代表） |
| runtime | emulator | `none`（保守） | NDS BIOS/ROM 红线，无固件时保守 none（静态 + 卡带插拔动画） |
| runtime | media_hint | `cartridge` | DS 卡带介质，schema 有 `cartridge` 枚举，**直接取用（显式说明，无需降级）** |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | handheld_lcd+speaker | 掌机用 handheld_lcd（对齐 game-boy/gba），非 crt_display |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/A/B/X/Y/L/R 肩键/开始/选择 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 卡带插拔 anim、翻盖开合 anim、下屏触控识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=23 号预研卡史实节（双屏触控开创者、史上最畅销掌机） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `gba`（310-O 掌机完整包体例）；NDS 与 GBA 同属任天堂掌机线，区别在于 **翻盖双屏、6 件拆分（top_screen/touch_screen）、触控下屏** 与 **output_sinks=handheld_lcd+speaker**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| arm9 | ARM9 CPU | chassis | NDS 主 CPU（ARM946E-S） |
| arm7 | ARM7 副处理器 | chassis | NDS 副处理器（ARM7TDMI） |
| ram | 主内存芯片 | chassis | 4MB 主内存 |
| sound_ic | 音源芯片 | chassis | 音源处理 |

> GBA 低模无 mainboard 件先例：components 挂 chassis（对齐 310-O 口径）。

### media_hint 口径说明（cartridge 有枚举）

- NDS 使用 **DS 卡带**介质，schema `media_hint` 枚举含 `cartridge`，**直接取 cartridge、无需降级**（对齐 N64/Switch/GBA 的卡带口径）。

## 二、目录条目方案

- **设备包 id**：`nintendo-ds`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HH-000033「Nintendo DS」`**（Nintendo、2004、planned）。产包时回填 status→done、device_id→nintendo-ds，**无需新建条目**。

## 三、NDS BIOS/ROM 红线

- NDS 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（melonDS / DeSmuME）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + 卡带插拔动画演示）。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | NDS 约 149×29×85 mm 合盖等 | [需核实]（沿用 23 号预研卡） |
| 配色 | 银色机身 0.75,0.77,0.80 等 | [需核实] |
| CPU/内存 | ARM9/ARM7 / 4MB 内存 | [需核实] |
| 模拟器候选许可 | melonDS / DeSmuME | [需核实] |
| 介质 | DS 卡带 | [需核实]（media_hint=cartridge） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；NDS BIOS/ROM 红线只清单级引用。
