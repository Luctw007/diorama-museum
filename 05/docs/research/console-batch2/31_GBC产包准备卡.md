# 31 · Game Boy Color 产包准备卡（低模预研已齐，产包备料）

> 任务 TASK-325-K（05 线）· 完成日期：2026-11-27。
> 性质：**纯准备卡**——TASK-325-I 已完成 GBC 低模样板预研（6 件拆分方案，见 `30_GBC与NGPC掌机低模样板预研合卡.md` 第一部分）。本卡产出**产包字段清单 + 目录条目方案 + GBC BIOS/ROM 接口红线 + 需核实清单**；**纯准备卡，不产包、不改目录 jsonl、不建模。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `game-boy-color` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 1998 | 30 号预研卡「1998」，整数无需化 |
| meta | category | `handheld` | GBC 为掌机，category=handheld（对齐 05 线掌机谱系） |
| meta | manufacturer | Nintendo | 任天堂（Game Boy 系，非品类代表） |
| runtime | emulator | `none`（保守） | GBC BIOS/ROM 红线，无固件时保守 none（静态 + 卡带插拔动画） |
| runtime | media_hint | `cartridge` | GBC 卡带介质，schema 有 `cartridge` 枚举，**直接取用（显式说明，无需降级）** |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | handheld_lcd+speaker | 掌机用 handheld_lcd（彩色液晶屏），非 crt_display |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键（上/下/左/右）/A/B/开始/选择 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 卡带插拔 anim、按键按压 anim、十字键识别件、彩色液晶屏识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=30 号预研卡史实节（GB 彩色升级版，向下兼容） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `game-boy`（05 线 GB 谱系掌机口径）；GBC 与 GB 同属任天堂竖版掌机线，区别在于 **彩色液晶屏、6 件拆分（chassis/screen_module/d_pad/buttons/cartridge_slot/battery_compartment）** 与 **category=handheld + output_sinks=handheld_lcd+speaker**。

### assemblies 拆分建议（6 件）

| assembly | 名称 | 说明 |
|---|---|---|
| chassis | 竖版机身 | 竖版掌机机身，含屏幕区/按键区/卡带口，整机主体 |
| screen_module | 屏幕模块 | 正面彩色液晶屏模块（关机态） |
| d_pad | 十字键 | 左下十字键，供按压识别 |
| buttons | 按键 | 右侧 A/B 键，供按压识别 |
| cartridge_slot | 卡带槽 | 顶部/背部 GB 卡带槽，供卡带插拔动画 |
| battery_compartment | 电池仓 | 机身背部电池仓 |

> assemblies 6 件对齐任务书「chassis / screen_module / d_pad / buttons / cartridge_slot / battery_compartment」，node_id 为**建议命名**（＝node_id），落定须与 02 线目录/建模规范对齐。

### components 拆分建议（4 件，挂 chassis）

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| cpu | 主处理器 | chassis | Sharp LR35902（类 Z80 变体）[需核实] |
| ppu | 图形处理器 | chassis | GBC 彩色图形处理器（PPU）[需核实] |
| ram | 主内存芯片 | chassis | GBC 主内存（约 32KB + 视频 RAM）[需核实] |
| sound_ic | 音源芯片 | chassis | 音源处理 |

> 掌机低模无 mainboard 件先例（对齐 24 号 NDS / 27 号 3DS 口径）：components 挂 chassis（掌机无 mainboard 先例挂 chassis，本卡注明）。component 命名 cpu/ppu/ram/sound_ic 均为**建议命名**。

### media_hint 口径说明（cartridge 有枚举）

- GBC 使用 **GB/GBC 卡带**介质，schema `media_hint` 枚举含 `cartridge`，**直接取 cartridge、无需降级**（对齐 GB/GBA/NDS/3DS 的卡带口径）。

## 二、目录方案（G-HH-000021 条目回填）

- **设备包 id**：`game-boy-color`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HH-000021「Game Boy Color」`**（Nintendo、1998、planned，taxonomy_path 游戏机/掌机/Game Boy 系，influence「GB 彩色升级版，向下兼容」）。产包时回填 status→done、device_id→game-boy-color，**无需新建条目**。
- 本卡**不落地目录 jsonl**，仅作条目回填方案预告。

## 三、接口红线（GBC BIOS/ROM）

- GBC 启动固件（BIOS）与游戏 ROM（卡带）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（mGBA / SameBoy）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + 卡带插拔动画演示）。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | GBC 约 75×27×133 mm 竖版等 | [需核实]（沿用 30 号预研卡） |
| 配色 | 紫色机身 0.35,0.06,0.55 / 深灰面板 0.25,0.25,0.28 等 | [需核实] |
| CPU | Sharp LR35902（类 Z80 变体） | [需核实] |
| 模拟器候选许可 | mGBA / SameBoy | [需核实] |
| 介质 | GB/GBC 卡带 | [需核实]（media_hint=cartridge） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；GBC BIOS/ROM 红线只清单级引用。
