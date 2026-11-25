# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `nintendo-3ds`（Nintendo 3DS）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/chassis.gltf | 网格 | 原创 | - | - | TASK-320-F 程序化低模盒子 |
| assemblies/top_screen.gltf | 网格 | 原创 | - | - | TASK-320-F 程序化低模盒子 |
| assemblies/touch_screen.gltf | 网格 | 原创 | - | - | TASK-320-F 程序化低模盒子 |
| assemblies/cartridge_slot.gltf | 网格 | 原创 | - | - | TASK-320-F 程序化低模盒子 |
| assemblies/shoulder_buttons.gltf | 网格 | 原创 | - | - | TASK-320-F 程序化低模盒子 |
| assemblies/battery_compartment.gltf | 网格 | 原创 | - | - | TASK-320-F 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-320-H 自产文案，未复制任何第三方文章原文 |
| S161 Wikipedia: Nintendo 3DS | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo_3DS | 2026-11-26 | 事实索引，仅作线索，未复制原文 |
| S162 Wikipedia: Nintendo | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo | 2026-11-26 | 事实索引，仅作线索，未复制原文 |
| S163 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-26 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-320-H 自产内容（几何由 TASK-320-F 程序化低模生成），未包含任何真实设备的扫描、照片、ROM、固件内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **3DS BIOS/ROM 红线**：Nintendo 3DS 的系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑模拟器（Citra / Mikage）时固件/ROM 由用户自备，获取与授权单独走合规流程。因无法合规获取固件，本包 `emulator="none"`（保守，静态 + 卡带插拔动画演示），`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选需核实**：Citra / Mikage 等 3DS 模拟器的许可状态标「需核实」，本包不下发任何模拟器二进制。
- **无介质声明**：本设备 `media_hint="cartridge"`（3DS 卡带有枚举，直接取用，无需降级），本包**不含任何固件 / 系统 ROM / 卡带镜像等介质文件**，仅以程序化低模网格与原创文案呈现。
- 商标（Nintendo、Nintendo 3DS 标志等）仅作用途登记，本包不对其使用方式做任何决策。
