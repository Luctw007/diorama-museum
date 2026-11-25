# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `playstation-4`（Sony PlayStation 4）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/chassis.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| assemblies/blu_ray_drive.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| assemblies/power_supply.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| assemblies/hard_drive.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| assemblies/controller_port.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| assemblies/controller.gltf | 网格 | 原创 | - | - | TASK-315-H 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-315-J 自产文案，未复制任何第三方文章原文 |
| S161 Wikipedia: PlayStation 4 | 文档 | CC | https://en.wikipedia.org/wiki/PlayStation_4 | 2026-11-26 | 事实索引，仅作线索，未复制原文 |
| S162 Wikipedia: Sony | 文档 | CC | https://en.wikipedia.org/wiki/Sony | 2026-11-26 | 事实索引，仅作线索，未复制原文 |
| S163 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-26 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-315-H / TASK-315-J 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、光盘镜像内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **蓝光无枚举→cd_rom 代指声明**：PS4 使用**蓝光（Blu-ray）**介质，但 schema `media_hint` 枚举中无 blu_ray 取值，故本包 `media_hint="cd_rom"` 以最接近的 `cd_rom` 代指（对齐 PS3 蓝光降级先例）；本包**不含任何固件 / 系统 ROM / 蓝光镜像等介质文件**，仅以程序化低模网格与原创文案呈现。
- **PS4 BIOS/ROM 红线**：Sony PlayStation 4 的系统固件与游戏 ROM（蓝光）受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑模拟器（shadPS4）时固件/ROM 由用户自备，获取与授权单独走合规流程。因无法合规获取固件，本包 `emulator="none"`（保守，静态 + 光盘吸入动画演示），`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选需核实**：shadPS4 等 PS4 模拟器的许可状态标「需核实」，本包不下发任何模拟器二进制。
- 商标（Sony、PlayStation 标志等）仅作用途登记，本包不对其使用方式做任何决策。
