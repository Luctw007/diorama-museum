# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `nintendo-64`（Nintendo 64）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/chassis.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子（盒子几何，非真实机箱几何） |
| assemblies/cartridge_slot.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| assemblies/cartridge.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| assemblies/power_supply.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| assemblies/controller_port.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| assemblies/expansion_slot.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| assemblies/controller.gltf | 网格 | 原创 | - | - | TASK-270-A 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-275-A 自产文案，未复制任何第三方文章原文 |
| S140 Wikipedia: Nintendo 64 | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo_64 | 2026-11-21 | 事实索引，仅作线索，未复制原文 |
| S141 Wikipedia: Nintendo | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo | 2026-11-21 | 事实索引，仅作线索，未复制原文 |
| S142 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-21 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-270-A / TASK-275-A 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、游戏卡带内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **N64 BIOS/ROM 红线**：Nintendo 64 的系统 ROM（PIF/CIC 引导程序）与游戏 ROM 受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑模拟器（Project64 / Mupen64Plus）时系统 ROM/游戏 ROM 由用户自备，获取与授权单独走合规流程。因无法合规获取系统 ROM，本包 `emulator="none"`（保守，静态 + 卡带插拔动画演示），`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选需核实**：Project64 / Mupen64Plus 等 N64 模拟器的许可状态标「需核实」，本包不下发任何模拟器二进制。
- **无介质声明**：本设备 `media_hint="cartridge"` 仅提示 N64 使用卡带介质特征，**不含任何 ROM / 系统 ROM / 游戏卡带镜像等介质文件**，仅以程序化低模网格与原创文案呈现。
- 商标（Nintendo、N64 标志等）仅作用途登记，本包不对其使用方式做任何决策。
