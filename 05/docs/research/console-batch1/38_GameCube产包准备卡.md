# 38 · GameCube 产包准备卡（低模已齐，产包备料）

> 任务 305-B（05 线）· 完成日期：2026-11-25。
> 性质：**轻量产包准备卡**——305-A 已完成 GameCube 低模样板（8 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + GameCube BIOS/ROM 红线 + 需核实清单**，供后续完整产包备料；**本卡不做产包/目录改动，纯准备卡。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `gamecube` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 2001 | 32 号预研卡「2001」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线游戏机谱系 |
| meta | manufacturer | Nintendo | 任天堂（游戏机线，非品类代表） |
| runtime | emulator | `none`（保守） | GameCube BIOS/ROM 红线，无 BIOS 时保守 none（静态 + 开盖放碟动画） |
| runtime | media_hint | `cd_rom` | miniDVD 介质；**schema media_hint 枚举无 mini_dvd，取最接近的 cd_rom**（见下方口径说明） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | crt_display+speaker | 对齐游戏机谱系（display+speaker） |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/模拟摇杆/开始/A/B 键等 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 提手/手柄识别件、光驱盖开合 anim |
| encyclopedia | — | ≥2500 汉字 | 底本=18 号研究卡史实节（迷你 DVD 差异化探索） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `playstation-2`（295-A）与 `sega-dreamcast`（285-A）完整包体例；GameCube 与 PS2 同属第六代主机，区别在于 **8 件低模拆分（含手柄/底部扩展槽可选件）** 与 **media_hint 取 cd_rom（miniDVD 无枚举）**。

### components 拆分建议

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| gekko | Gekko CPU | mainboard | GameCube 主 CPU |
| flipper | Flipper 图形芯片 | mainboard | GameCube 图形芯片 |
| ram | 主内存芯片 | mainboard | 24MB 主内存 |
| cd_motor | 光盘电机 | disc_drive | miniDVD 光驱电机 |

### media_hint 口径说明（mini_dvd → cd_rom）

- GameCube 使用 miniDVD 介质，但 schema `media_hint` 枚举为 `["none", "cartridge", "disk", "firmware", "tape", "cd_rom", "floppy"]`，**无 mini_dvd**。
- 因此产包时 `media_hint` 取最接近的 **`cd_rom`**（光盘只读），并在 THIRD_PARTY/完成报告标注「miniDVD 无枚举，以 cd_rom 代指」（对齐 Dreamcast GD-ROM、PS2 DVD-ROM 降级先例）。

## 二、目录条目方案

- **设备包 id**：`gamecube`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录 `游戏机与手持大类_目录_v2.jsonl` 中**既有条目 `G-HC-000066「GameCube」`**（manufacturer=Nintendo、era=2001、status=planned、device_id=null）。产包时回填该条目 status→done、device_id→gamecube，**无需新建条目、无需臆造 id**。

## 三、GameCube BIOS/ROM 红线

- GameCube 系统固件与游戏 ROM（miniDVD）受版权保护，**不入库、不下载**，产包仅做清单级引用（对齐 PlayStation/Saturn/N64/Dreamcast/PS2 BIOS 红线口径）。
- 真跑模拟器（Dolphin）时 BIOS/ROM 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/光盘镜像。
- 若无法合规获取 BIOS，`runtime.emulator` 保守取 `none`（静态 + 开盖放碟动画演示），`bios_required=false`、`bios_guide_url=null`。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | GameCube 约 150×110×161 mm 等 | [需核实]（沿用 32 号预研卡） |
| 配色 | 靛紫机身 0.35,0.25,0.45 等 | [需核实] |
| CPU/内存 | Gekko / 24MB 内存 | [需核实]（沿用 18 号研究卡） |
| 模拟器候选许可 | Dolphin | [需核实] |
| 介质 | miniDVD | [需核实]（media_hint 取 cd_rom 代指） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；GameCube BIOS/ROM 红线只清单级引用。
