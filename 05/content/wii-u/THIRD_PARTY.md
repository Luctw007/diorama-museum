# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `wii-u`（Nintendo Wii U）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/console.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| assemblies/gamepad.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| assemblies/disc_drive.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| assemblies/power_supply.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| assemblies/controller_port.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| assemblies/flash_storage.gltf | 网格 | 原创 | - | - | TASK-315-E 程序化低模 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-315-G 自产文案，未复制任何第三方文章原文 |
| S161 Wikipedia: Wii U | 文档 | CC | https://en.wikipedia.org/wiki/Wii_U | 2026-11-26 | 事实索引，仅作线索，未复制原文 |
| S162 Wikipedia: Nintendo | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo | 2026-11-26 | 事实索引，仅作线索，未复制原文 |
| S163 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-26 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-315-E / TASK-315-G 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、光盘镜像内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **Wii U 专用光盘无枚举→cd_rom 代指声明**：Wii U 使用 **Wii U Optical Disc 专用光盘**，schema `media_hint` 枚举中无对应值，故本包以最接近的 `cd_rom` 代指（对齐 Dreamcast GD-ROM、PS2 DVD-ROM 降级先例）；本包**不含任何固件 / 系统 ROM / 专用光盘镜像等介质文件**，仅以程序化低模网格与原创文案呈现。
- **Wii U BIOS/ROM 红线**：Nintendo Wii U 的系统固件与游戏 ROM（专用光盘）受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑模拟器（Cemu）时固件/ROM 由用户自备，获取与授权单独走合规流程。因无法合规获取固件，本包 `emulator="none"`（保守，静态 + 光盘吸入动画演示），`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选需核实**：Cemu 等 Wii U 模拟器的许可状态标「需核实」，本包不下发任何模拟器二进制。
- 商标（Nintendo、Wii U、GamePad 标志等）仅作用途登记，本包不对其使用方式做任何决策。
