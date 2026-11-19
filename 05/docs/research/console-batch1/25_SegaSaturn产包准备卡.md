# 25 · Sega Saturn 产包准备卡（低模已齐，产包备料）

> 任务 260-B（05 线）· 完成日期：2026-11-20。
> 性质：**轻量产包准备卡**——260-A 已完成 Sega Saturn 低模样板（6 件 gltf）。本卡产出**产包字段清单 + 目录条目方案 + Saturn BIOS/ROM 红线 + 需核实清单**，供后续完整产包备料；**本卡不做产包/目录改动，纯准备卡。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `sega-saturn` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 1994 | 24 号预研卡「1994」，整数无需化 |
| meta | category | `game-console` | 对齐 05 线游戏机谱系 |
| meta | manufacturer | Sega | 世嘉（游戏机线，非品类代表） |
| runtime | emulator | `none`（保守） | Saturn BIOS/ROM 红线，无 BIOS 时保守 none（静态 + 开盖动画） |
| runtime | media_hint | `cd_rom` | 表达 Saturn 的 CD-ROM 介质特征（对齐 PlayStation 先例） |
| runtime | bios_required | false（保守 none） | 取决于 emulator 取值 |
| runtime | output_sinks | crt_display+speaker | 对齐游戏机谱系（display+speaker） |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 十字键/开始/ABC 键等（对齐 PlayStation 先例） |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 开盖放碟动画用 anim 承载；cd_drive 开合识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=18 号研究卡史实节（双 CPU、世嘉由盛转衰） |
| THIRD_PARTY | — | 三件套 + BIOS/ROM 红线声明 | 无模拟器/BIOS 只清单级引用 |

> 字段清单对齐 `playstation`（255-A，最接近先例）与 `apple-iie`（210-A）完整包体例；Saturn 与 PlayStation 同属第五代光盘主机，除「双 SH-2 CPU / 世嘉由盛转衰」叙事外口径一致。

## 二、目录条目方案

- **设备包 id**：`sega-saturn`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录 `游戏机与手持大类_目录_v2.jsonl` 中**既有条目 `G-HC-000055「Sega Saturn」`**（manufacturer=Sega、era=1994、taxonomy_path=["游戏机","家用机","第 1~9 世代"]、status=planned、device_id=null）。产包时回填该条目 status→done、device_id→sega-saturn，**无需新建条目、无需臆造 id**。

## 三、Saturn BIOS/ROM 红线

- Saturn BIOS 与游戏 ROM 受版权保护，**不入库、不下载**，产包仅做清单级引用（对齐 PlayStation BIOS 红线口径）。
- 真跑模拟器（Yaba Sanshiro / Mednafen）时 BIOS/ROM 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/磁盘镜像。
- 若无法合规获取 BIOS，`runtime.emulator` 保守取 `none`（静态 + 开盖放碟动画演示），`bios_required=false`、`bios_guide_url=null`。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | Saturn 约 260×83×230 mm | [需核实]（沿用 24 号预研卡） |
| 配色 | 深灰机身 0.20,0.20,0.22 等 | [需核实] |
| CPU/内存 | 双 SH-2 CPU / 2MB 主 RAM | [需核实]（沿用 18 号研究卡） |
| 模拟器候选许可 | Yaba Sanshiro / Mednafen | [需核实] |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数无来源一律标「需核实」；Saturn BIOS/ROM 红线只清单级引用。
