# 28 · PSVita 产包准备卡（低模预研已齐，产包备料）

> 任务 TASK-320-J（05 线）· 完成日期：2026-11-26。
> 性质：**纯准备卡**——TASK-320-E 已完成 PSVita 低模预研（6 件拆分方案）。本卡产出**产包字段清单 + 目录条目方案 + PSVita BIOS/ROM 红线 + 需核实清单**；**纯准备卡，不产包、不改目录。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `psvita` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2011 | 26 号预研卡「2011」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线掌机谱系 |
| meta | manufacturer | Sony | 索尼（掌机线，非品类代表） |
| runtime | emulator | `none`（保守） | PSVita BIOS/ROM 红线，无固件时保守 none（静态 + 卡带插拔动画） |
| runtime | media_hint | `cartridge` | PSVita 专用卡带；**schema media_hint 枚举有 cartridge，直接取用（显式说明，无需降级）** |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | handheld_lcd+speaker | 掌机用 handheld_lcd（对齐 game-boy/gba/psp），非 crt_display |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 双摇杆/十字键/△○×□/L/R 肩键/开始/选择/PS 键 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 卡带插拔 anim、横置双摇杆握持识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=26 号预研卡史实节（索尼 PSP 后继、前后双触控 + 双摇杆、OLED 屏） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `gba`（310-O 掌机完整包体例）、`psp`（25 号产包准备卡体例）；PSVita 与 PSP 同属索尼掌机线，区别在于 **双摇杆 + 前后双触控、PSVita 专用卡带（cartridge 有枚举）、OLED 屏** 与 **6 件拆分（rear_touchpad/control_buttons）**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| arm_cortex_a9_cpu | ARM Cortex-A9 CPU | chassis | PSVita 主 CPU（四核 ARM Cortex-A9） |
| gpu | GPU | chassis | PSVita 图形芯片（SGX543MP4+） |
| ram | 主内存芯片 | chassis | 512MB 主内存 + 128MB 显存 |
| sound_ic | 音频芯片 | chassis | PSVita 音效处理芯片 |

> **掌机无 mainboard 先例**：PSVita components 均挂 `chassis`（对齐 GBA 低模先例与 310-O 口径，掌机不单列 mainboard 件）；本卡仅给拆分建议，产包时与 02 线目录/建模规范对齐。

### media_hint 口径说明（PSVita 专用卡带 → cartridge）

- PSVita 使用 **PSVita 专用卡带（PS Vita Game Card）** 介质，schema `media_hint` 枚举**有 `cartridge`**，产包时**直接取 `cartridge`（无需降级）**，并在 THIRD_PARTY 显式标注（对齐 3DS 卡带先例，区别于 PSP 的 UMD→cd_rom 降级）。

## 二、目录方案（目录条目方案）

- **设备包 id**：`psvita`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HH-000046「PlayStation Vita」`**（Sony、2011、planned）。产包时回填 status→done、device_id→psvita，**无需新建条目**。

## 三、BIOS 红线（PSVita BIOS/ROM 红线）

- PSVita 系统固件与游戏 ROM（PSVita 专用卡带）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（Vita3K）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + 卡带插拔动画演示）。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | PSVita（1000）约 182×18.6×83.5 mm 等 | [需核实]（沿用 26 号预研卡） |
| 配色 | 黑色机身 0.08,0.08,0.09 等 | [需核实] |
| CPU/内存 | 四核 ARM Cortex-A9 / 512MB 内存 + 128MB 显存 | [需核实] |
| 模拟器候选许可 | Vita3K | [需核实] |
| 介质 | PSVita 专用卡带 | [需核实]（media_hint 取 cartridge，有枚举） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；PSVita BIOS/ROM 红线只清单级引用。
