# 32 · NGPC 产包准备卡（低模预研已齐，产包备料）

> 任务 TASK-325-N（05 线）· 完成日期：2026-11-27。
> 性质：**纯准备卡**——30 号预研合卡已完成 NGPC（Neo Geo Pocket Color）低模样板预研（6 件拆分方案）。本卡产出**产包字段清单 + 目录条目方案 + 接口红线（BIOS/ROM 红线）+ 需核实清单**；**纯准备卡，不产包、不改目录、不建模。**

---

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `neo-geo-pocket-color` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 1999 | 30 号预研卡「1999」，整数无需化 |
| meta | category | `handheld` | 任务书口径（掌机 handheld）；既有掌机产包卡多取 game-console，本卡按任务书显式指定 handheld，落定须与 02 线 schema 对齐 [需核实] |
| meta | manufacturer | SNK | SNK（掌机线，非品类代表） |
| runtime | emulator | `none`（保守） | NGPC BIOS/ROM 红线，无固件时保守 none（静态 + 卡带插拔动画） |
| runtime | media_hint | `cartridge` | NGPC 卡带；**schema media_hint 枚举有 cartridge，直接取用（显式说明，无需降级）** |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | handheld_lcd+speaker | 掌机用 handheld_lcd（对齐 game-boy/gba），非 crt_display |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | clicky 摇杆十字键四向 / A / B / Option / 电源 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 卡带插拔 anim、clicky 摇杆十字键识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=30 号预研卡史实节（SNK 彩色掌机、clicky 摇杆状十字键、格斗阵容强） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `game-boy`（掌机完整产包体例）；NGPC 与 Game Boy 同属竖版掌机线，区别在于 **SNK 竖版机身、clicky 摇杆状十字键（d_pad）、6 件拆分、卡带槽/电池仓** 与 **output_sinks=handheld_lcd+speaker**。

### assemblies 拆分建议（6 件）

| # | assembly（node_id） | 名称 | 说明 |
|---|---|---|---|
| 1 | chassis | 竖版机身 | NGPC 竖版掌机机身，含屏幕区/摇杆十字键区/按键区，整机主体 |
| 2 | screen_module | 屏幕模块 | 正面彩色液晶屏模块（关机态） |
| 3 | d_pad | 十字键 | NGPC 特有 clicky 摇杆状十字键，供按压识别 |
| 4 | buttons | 按键 | 右侧 A/B 键，供按压识别 |
| 5 | cartridge_slot | 卡带槽 | 顶部/背部 NGPC 卡带槽，供卡带插拔动画 |
| 6 | battery_compartment | 电池仓 | 机身背部电池仓 |

> assemblies 对齐任务书「chassis / screen_module / d_pad / buttons / cartridge_slot / battery_compartment」6 件；node_id 为**建议命名**，落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。

### components 拆分建议（4 件挂 chassis）

| component | 名称 | 挂载 | 说明 |
|---|---|---|---|
| cpu | CPU | chassis | NGPC 主 CPU（公开资料 TLCS-900/H，Toshiba）[需核实] |
| gpu | 图形芯片 | chassis | NGPC 图形处理（160×152 彩色屏）[需核实] |
| ram | 主内存芯片 | chassis | NGPC 主内存 [需核实] |
| sound_ic | 音源芯片 | chassis | NGPC 音效处理 [需核实] |

> **掌机无 mainboard 先例**：NGPC components 均挂 `chassis`（对齐 GBA/PSVita 低模先例与掌机不单列 mainboard 口径）；本卡仅给拆分建议，产包时与 02 线目录/建模规范对齐。

### media_hint 口径说明（NGPC 卡带 → cartridge）

- NGPC 使用 **NGPC 专用卡带** 介质，schema `media_hint` 枚举**有 `cartridge`**，产包时**直接取 `cartridge`（无需降级）**，并在 THIRD_PARTY 显式标注（对齐 GB/GBA 卡带先例，区别于 PSP 的 UMD→cd_rom 降级）。

## 二、目录方案（目录条目方案）

- **设备包 id**：`neo-geo-pocket-color`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录中**既有条目 `G-HH-000023「Neo Geo Pocket Color」`**（SNK、1999、planned，taxonomy_path＝游戏机/掌机/其他掌机，influence＝「彩色掌机，格斗游戏阵容强，SNK 破产前绝唱」，目录实扫已确认）。产包时回填 status→done、device_id→neo-geo-pocket-color，**无需新建条目**；本卡**不落地、不登记目录 id、不擅入定案**。

## 三、接口红线（NGPC BIOS/ROM 红线）

- NGPC 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，产包仅做清单级引用。
- 真跑模拟器（NeoPop / Mednafen）时固件/ROM 由**用户自备**，获取与授权单独走合规流程。
- 若无法合规获取固件，`runtime.emulator` 保守取 `none`（静态 + 卡带插拔动画演示）。
- 接口层不落地任何二进制：不下载 ROM/BIOS/二进制/贴图，仅以 `media_hint=cartridge` 与 `emulator=none` 描述接口。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | NGPC 约 75×25×130 mm 等 | [需核实]（沿用 30 号预研卡） |
| 配色 | 银色机身 0.75,0.77,0.80 等 | [需核实] |
| CPU | TLCS-900/H（Toshiba）等 | [需核实]（沿用公开资料） |
| 模拟器候选许可 | NeoPop / Mednafen | [需核实] |
| 介质 | NGPC 专用卡带 | [需核实]（media_hint 取 cartridge，有枚举） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；NGPC BIOS/ROM 红线只清单级引用；本卡**仅新增 32_NGPC产包准备卡.md 一个文件**（TASK-325-N）。
