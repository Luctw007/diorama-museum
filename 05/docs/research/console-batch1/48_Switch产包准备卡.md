# 48 · Switch 产包准备卡（低模已齐，产包备料）

> 任务 310-K（05 线）· 完成日期：2026-11-25。
> 性质：**轻量产包准备卡**——310-J 已完成 Switch 低模样板（8 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + Switch BIOS/ROM 红线 + 需核实清单**；**纯准备卡，不产包、不改目录。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `nintendo-switch` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2017 | 44 号预研卡「2017」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线游戏机谱系 |
| meta | manufacturer | Nintendo | 任天堂（游戏机线，非品类代表） |
| runtime | emulator | `none`（保守） | Switch 固件/ROM 红线，无固件时保守 none（静态 + 入坞动画） |
| runtime | media_hint | `cartridge` | 卡带介质，schema 有 `cartridge` 枚举，直接取用（无需降级） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | crt_display+speaker | 对齐游戏机谱系（家用主机形态） |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/摇杆/开始/A/B 键等 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 入坞 anim、Joy-Con 滑轨卡合、卡带插拔识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=18 号研究卡史实节（主机掌机二合一、融合路线破亿） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线 + Yuzu/Ryujinx 仅清单级声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `gamecube`（305-C）完整包体例；Switch 与 GameCube 同属任天堂系，区别在于 **平板 + Dock + Joy-Con 二合一形态** 与 **media_hint=cartridge（卡带有枚举，无需降级）**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| tegra_x1 | Tegra X1 处理器 | mainboard | Switch 主 SoC |
| ram | 主内存芯片 | mainboard | 4GB 主内存 |
| gpu | 图形核心 | mainboard | Tegra X1 集成图形核心 |
| battery_ic | 电池管理芯片 | battery | 电池管理 |

### media_hint 口径说明（cartridge 有枚举）

- Switch 使用卡带介质，schema `media_hint` 枚举含 `cartridge`，**直接取 cartridge、无需降级**（区别于 Xbox/PS3 等光盘机的 cd_rom 代指）。

## 二、目录条目方案

- **设备包 id**：`nintendo-switch`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HC-000084「Nintendo Switch」`**（Nintendo、2017、planned）。产包时回填 status→done、device_id→nintendo-switch，**无需新建条目**。

## 三、Switch BIOS/ROM 红线

- Switch 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- **Yuzu / Ryujinx 因法律风险仅清单级标注、不展开、不计数**（对齐 305-P 汇总卡 v2 口径）。
- 真跑模拟器时固件/ROM 由**用户自备**，获取与授权单独走合规流程；`runtime.emulator` 保守取 `none`。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | Switch 平板约 239×14×102 mm 等 | [需核实]（沿用 44 号预研卡） |
| 配色 | 黑色机身/霓虹蓝/霓虹红 Joy-Con 等 | [需核实] |
| SoC/内存 | Tegra X1 / 4GB 内存 | [需核实]（沿用 18 号研究卡） |
| 模拟器候选 | Yuzu / Ryujinx（法律风险仅清单级） | [需核实] |
| 介质 | 卡带 | [需核实]（media_hint=cartridge） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；Switch 固件/ROM 只清单级引用、Yuzu/Ryujinx 仅清单级标注；参数无来源一律标「需核实」。
