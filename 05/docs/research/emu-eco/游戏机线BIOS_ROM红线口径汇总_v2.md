# 游戏机线 BIOS/ROM 红线口径汇总 v2（第六/七代补登记）

> 任务 305-P（05 线）· 完成日期：2026-11-25。
> 性质：**红线口径汇总卡 v2**——在 v1（PS/Saturn/N64/DC/PS2 五台）基础上，补登记 **GameCube / Xbox / Xbox 360 / Wii / PS3 / Switch 六台**；**纯文档汇总，不产包、不改 jsonl、不下载任何 ROM/BIOS，另存 v2 不改 v1。**

## 一、六台红线口径表（新增）

| 设备 | 包 id | 介质 | 候选模拟器（需核实） | emulator | 说明 |
|---|---|---|---|---|---|
| Nintendo GameCube | gamecube | miniDVD | Dolphin | none（保守） | miniDVD 无枚举，media_hint 取 cd_rom 代指 |
| Microsoft Xbox | xbox | DVD + 硬盘 | Xemu | none（保守） | DVD-ROM 无枚举，media_hint 取 cd_rom；硬盘以 hard_drive 件表达 |
| Xbox 360 | xbox-360 | DVD + 硬盘 | Xenia | none（保守） | 第七代，DVD-ROM + 可拆卸硬盘 |
| Nintendo Wii | wii | DVD | Dolphin | none（保守） | 第七代，吸入式 DVD，体感遥控 |
| PlayStation 3 | playstation-3 | 蓝光 + 硬盘 | RPCS3 | none（保守） | 第七代，蓝光无枚举，media_hint 取 cd_rom 代指 |
| Nintendo Switch | nintendo-switch | 卡带 | Yuzu / Ryujinx（仅清单级） | none（保守） | 融合主机，卡带介质，Yuzu/Ryujinx 因法律风险仅清单级标注 |

> 六台产包/预研 `runtime.emulator` 均保守取 `none`，`bios_required=false`、`bios_guide_url=null`；BIOS/ROM 只清单级引用，未入库、未下载。

## 二、统一口径声明（沿用 v1 三条 + 补强）

1. **BIOS/ROM 只清单级引用**：凡涉及系统固件 / 游戏 ROM 的主机，产包一律 `emulator="none"`（保守），静态展示 + 可识别件动画。
2. **media_hint 降级标注**：专用介质无 schema 枚举时取最接近值并标注（miniDVD/DVD-ROM/蓝光 → cd_rom；卡带 → cartridge；街机基板 → none）。
3. **候选模拟器标「需核实」**：候选模拟器仅清单级登记、许可一律「需核实」，不随附二进制；**Switch 的 Yuzu/Ryujinx 因法律风险仅清单级标注、不展开、不计数**。

## 三、FR-E3 合规流程引用

- 红线 FR-E3（源自 `emu-eco/03_街机ROM_BIOS清单级引用.md`）：本仓**永不下载、永不随附** ROM/BIOS，用户在 `slots/` 自备（见 `slots/README.md`）。
- 真跑模拟器时，系统固件 / 游戏 ROM 由**用户自备**，获取与授权单独走合规流程；本项目不下发任何 BIOS/ROM/光盘镜像/卡带镜像/蓝光镜像。

## 四、v1 → v2 变更说明

1. 新增「六台红线口径表」（GameCube/Xbox/Xbox 360/Wii/PS3/Switch）。
2. 统一口径声明补强「街机基板 → none」「Switch 的 Yuzu/Ryujinx 仅清单级不计数」两条。
3. v1 五台表保持不动，本卡独立成 v2 文件，仅做补登记。

## 五、红线自查

本卡纯文档；不下载 ROM/BIOS/二进制/贴图；六台口径均实测（读各包 THIRD_PARTY.md / 预研卡）；只改 05 目录；另存 v2 不改 v1。
