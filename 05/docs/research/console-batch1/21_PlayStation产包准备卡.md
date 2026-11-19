# 21 · PlayStation 产包准备卡（低模已齐，产包备料）

> 任务 240-B（05 线）· 完成日期：2026-11-20。
> 性质：**轻量产包准备卡**——235-B 已完成 PlayStation 低模样板（6 件 gltf）。本卡产出**产包字段清单 + id/目录条目方案 + PS1 BIOS 红线 + 需核实清单**，供后续完整产包备料；**本卡不做产包/目录改动，纯准备卡。**

## 一、产包字段清单（逐件口径）

| 件 | 字段 | 建议值 | 口径说明 |
|---|---|---|---|
| meta | id | `playstation` | 建议命名，待与 02 线目录规范对齐 |
| meta | era | 1994 | 研究卡「1994 年 12 月 3 日日本首发」，整数无需化 |
| meta | category | `game-console` | 对齐现有 7 台游戏机包（任务原文 console 为简称，落定以 game-console 为准） |
| meta | manufacturer | Sony | 索尼（游戏机线，非品类代表） |
| runtime | emulator | DuckStation / ePSXe / PCSX 候选 | 均标 [需核实]；**无 BIOS 时保守 `none`**（静态 + 开盖动画） |
| runtime | media_hint | `cd_rom`（真模拟器）/ `none`（保守 none） | PS1 用 CD-ROM 介质 |
| runtime | bios_required | true（真模拟器）/ false（保守 none） | 取决于 emulator 取值 |
| runtime | input_map | 8 动作（keyboard，键名 `^KEY_[A-Z0-9_]+$`） | 电源/开始/选择/十字键/三角圆叉方/演示 |
| annotations | — | ≥30 条（16 role + 12 flow + 2 anim） | 开盖放碟动画用 anim 承载；cd_drive 开合识别件 |
| encyclopedia | — | ≥2500 汉字 | 底本=15 号研究卡史实节（光盘取代卡带、3D 图形） |
| THIRD_PARTY | — | 三件套 + BIOS 红线声明 | 无模拟器/BIOS 均只清单级引用 |

> 字段清单对齐 `apple-iie`（210-A）完整包体例与 `crt-tv/vhs-vcr/dvd-player` 家电产包先例；游戏机线区别在于 **category=game-console、manufacturer=Sony、media_hint=cd_rom**（若上真模拟器）。

## 二、id / 目录条目方案

- **设备包 id**：`playstation`（建议命名，待 02 线目录规范对齐）。
- **目录条目**：游戏机目录 `游戏机与手持大类_目录_v2.jsonl` 中**既有条目 `G-HC-000056「PlayStation」`**（aliases=["PS","PS1"]、manufacturer=Sony、era=1994、taxonomy_path=["游戏机","家用机","第 1~9 世代"]、status=planned、device_id=null）。产包时回填该条目 status→done、device_id→playstation，**无需新建条目、无需臆造 id**。
- **未来区定位**：PS1 目前**不入 30 台定案表**，属未来区候选（等社区）；入定案须走用户点头流程，本卡不擅入。

## 三、PS1 BIOS 红线

- PS1 BIOS（如 `SCPH-1000.bin` 等）受版权保护，**不入库、不下载**，产包仅做清单级引用（对齐 apple-iie 的 Monitor ROM 红线口径）。
- 真跑模拟器时 BIOS 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/磁盘镜像。
- 若无法合规获取 BIOS，`runtime.emulator` 保守取 `none`（静态 + 开盖放碟动画演示），`bios_required=false`、`bios_guide_url=null`。

## 四、「需核实」清单

| 项 | 内容 | 状态 |
|---|---|---|
| 尺寸 | PS1 原版约 270×60×190 mm | [需核实] |
| 配色 | 灰机身 0.72,0.72,0.74 等 | [需核实] |
| CPU/内存/多边形 | R3000A 33.8688MHz / 2MB+1MB / ~36 万多边形每秒 | [需核实]（沿用研究卡） |
| 模拟器候选许可 | DuckStation / ePSXe / PCSX 许可 | [需核实] |
| 发售 | 1994-12-03 日本首发 | [需核实]（沿用研究卡） |

## 五、红线自检

本卡纯准备，不新增/修改任何 gltf、meta.json、annotations、目录 jsonl；未下载 ROM/BIOS/二进制/贴图；参数/许可无来源一律标「需核实」；PS1 BIOS 红线只清单级引用。
