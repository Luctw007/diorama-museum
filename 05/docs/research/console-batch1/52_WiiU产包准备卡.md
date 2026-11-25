# 52 · Wii U 产包准备卡（低模已齐，产包备料）

> 任务 315-F（05 线）· 完成日期：2026-11-26。
> 性质：**轻量产包准备卡**——315-E 已完成 Wii U 低模样板（7 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + Wii U BIOS/ROM 红线 + 需核实清单**；**纯准备卡，不产包、不改目录。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `wii-u` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2012 | 49 号预研卡「2012」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线游戏机谱系 |
| meta | manufacturer | Nintendo | 任天堂（游戏机线，非品类代表） |
| runtime | emulator | `none`（保守） | Wii U BIOS/ROM 红线，无固件时保守 none（静态 + 光盘吸入动画） |
| runtime | media_hint | `cd_rom` | Wii U 专用光盘；**schema media_hint 枚举无对应值，取最接近的 cd_rom**（显式标注） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | crt_display+speaker | 家用主机对齐游戏机谱系 |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/摇杆/开始/A/B 键等 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 光盘吸入 anim、GamePad 触屏识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=49 号预研卡史实节（GamePad 触屏手柄、向下兼容 Wii、Switch 前身） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `wii`（310-E 完整包体例）；Wii U 与 Wii 同属任天堂系，区别在于 **console 主机 + GamePad 触屏手柄、7 件拆分、闪存模块** 与 **media_hint 取 cd_rom（专用光盘无枚举降级）**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| espresso | Espresso CPU | mainboard | Wii U 主 CPU（IBM PowerPC 三核） |
| latte | Latte GPU | mainboard | Wii U 图形芯片（AMD） |
| ram | 主内存芯片 | mainboard | 2GB 主内存 |
| cd_motor | 光盘电机 | disc_drive | 专用光盘光驱电机 |

### media_hint 口径说明（专用光盘 → cd_rom）

- Wii U 使用 **Wii U Optical Disc 专用光盘**，schema `media_hint` 枚举无对应值，产包时取最接近的 **`cd_rom`** 代指，并在 THIRD_PARTY 显式标注（对齐 Dreamcast GD-ROM、PS2 DVD-ROM 降级先例）。

## 二、目录条目方案

- **设备包 id**：`wii-u`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HC-000078「Wii U」`**（Nintendo、2012、planned）。产包时回填 status→done、device_id→wii-u，**无需新建条目**。

## 三、Wii U BIOS/ROM 红线

- Wii U 系统固件与游戏 ROM（专用光盘）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（Cemu）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + 光盘吸入动画演示）。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | Wii U 约 172×46×268.5 mm、GamePad 约 255×41×133 mm 等 | [需核实]（沿用 49 号预研卡） |
| 配色 | 黑色机身 0.08,0.08,0.09 等 | [需核实] |
| CPU/内存 | Espresso PowerPC 三核 / 2GB 内存 | [需核实] |
| 模拟器候选许可 | Cemu | [需核实] |
| 介质 | Wii U 专用光盘 | [需核实]（media_hint 取 cd_rom 代指） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；Wii U BIOS/ROM 红线只清单级引用。
