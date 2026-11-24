# 游戏机线 BIOS/ROM 红线口径汇总 v1

> 任务 295-L（05 线）· 完成日期：2026-11-24。
> 性质：**红线口径汇总卡**——PS/Saturn/N64/DC/PS2 五台产包均涉及 BIOS/ROM 红线（只清单级引用、emulator 保守 none），口径分散于各准备卡。本卡做统一口径汇总；**纯文档汇总，不产包、不改 jsonl、不下载任何 ROM/BIOS。**

## 一、五台红线口径汇总表

| 设备 | 包 id | emulator | media_hint | BIOS/ROM 红线声明出处 | 候选模拟器（需核实） |
|---|---|---|---|---|---|
| PlayStation | playstation | none（保守） | cd_rom | THIRD_PARTY.md（255-A） | DuckStation |
| Sega Saturn | sega-saturn | none（保守） | cd_rom | THIRD_PARTY.md（265-A） | Yaba Sanshiro / Mednafen |
| Nintendo 64 | nintendo-64 | none（保守） | cartridge | THIRD_PARTY.md（275-A） | Project64 / Mupen64Plus |
| Sega Dreamcast | sega-dreamcast | none（保守） | cd_rom（GD-ROM 降级） | THIRD_PARTY.md（285-A） | Flycast / Demul |
| PlayStation 2 | playstation-2 | none（保守） | cd_rom（DVD-ROM 降级） | THIRD_PARTY.md（295-A） | PCSX2 |

> 五台产包 `runtime.emulator` 均取 `none`（保守），`bios_required=false`、`bios_guide_url=null`；BIOS/ROM 只清单级引用，未入库、未下载。

## 二、统一口径声明（后续产包沿用）

1. **BIOS/ROM 只清单级引用**：凡涉及系统 BIOS / 游戏 ROM 的主机，产包一律 `emulator="none"`（保守），静态展示 + 可识别件动画（开盖放碟 / 卡带插拔 / 光盘进仓）。
2. **media_hint 降级标注**：专用介质无 schema 枚举时取最接近值并标注（Dreamcast GD-ROM → cd_rom、PS2 DVD-ROM → cd_rom；N64 卡带 → cartridge）。
3. **候选模拟器标「需核实」**：候选模拟器（DuckStation / Yaba Sanshiro / PCSX2 / Flycast 等）仅清单级登记、许可一律「需核实」，不随附二进制。

## 三、合规流程指引（用户自备 BIOS 走合规流程）

- 红线 FR-E3（源自 `emu-eco/03_街机ROM_BIOS清单级引用.md`）：本仓**永不下载、永不随附** ROM/BIOS，用户在 `slots/` 自备（见 `slots/README.md`）。
- 真跑模拟器时，系统 BIOS / 游戏 ROM 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/光盘镜像/卡带镜像。

## 四、红线自查

本卡纯文档；不下载 ROM/BIOS/二进制/贴图；五台口径均实测（读各包 THIRD_PARTY.md / runtime.json）、不臆造；只改 05 目录。
