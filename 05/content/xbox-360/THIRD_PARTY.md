# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `xbox-360`（Microsoft Xbox 360）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/chassis.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子（盒子几何，非真实机箱几何） |
| assemblies/dvd_drive.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| assemblies/power_supply.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| assemblies/controller_port.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| assemblies/hard_drive.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| assemblies/controller.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| assemblies/power_ring.gltf | 网格 | 原创 | - | - | TASK-310-A 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-310-C 自产文案，未复制任何第三方文章原文 |
| S158 Wikipedia: Xbox 360 | 文档 | CC | https://en.wikipedia.org/wiki/Xbox_360 | 2026-11-25 | 事实索引，仅作线索，未复制原文 |
| S159 Wikipedia: Microsoft | 文档 | CC | https://en.wikipedia.org/wiki/Microsoft | 2026-11-25 | 事实索引，仅作线索，未复制原文 |
| S160 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-25 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-310-A / TASK-310-C 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、光盘镜像内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **Xbox 360 BIOS/ROM 红线**：Microsoft Xbox 360 的系统固件与游戏 ROM（DVD）受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑模拟器（Xenia）时固件/ROM 由用户自备，获取与授权单独走合规流程。因无法合规获取固件，本包 `emulator="none"`（保守，静态 + 托盘弹出动画演示），`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选需核实**：Xenia 等 Xbox 360 模拟器的许可状态标「需核实」，本包不下发任何模拟器二进制。
- **无介质声明**：本设备 `media_hint="cd_rom"` 仅提示 Xbox 360 使用光盘介质特征，因 DVD-ROM 介质在 schema 枚举中无对应值（枚举为 none/cartridge/disk/firmware/tape/cd_rom/floppy），故以最接近的 `cd_rom` 代指；本包**不含任何固件 / 系统 ROM / DVD 镜像等介质文件**，仅以程序化低模网格与原创文案呈现。
- 商标（Microsoft、Xbox 360 标志等）仅作用途登记，本包不对其使用方式做任何决策。
