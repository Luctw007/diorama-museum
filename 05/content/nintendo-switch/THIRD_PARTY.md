# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `nintendo-switch`（Nintendo Switch）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/tablet.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/dock.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/joycon_left.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/joycon_right.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/battery.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/cartridge_slot.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| assemblies/screen.gltf | 网格 | 原创 | - | - | TASK-310-J 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-310-L 自产文案，未复制任何第三方文章原文 |
| S167 Wikipedia: Nintendo Switch | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo_Switch | 2026-11-25 | 事实索引，仅作线索，未复制原文 |
| S168 Wikipedia: Nintendo | 文档 | CC | https://en.wikipedia.org/wiki/Nintendo | 2026-11-25 | 事实索引，仅作线索，未复制原文 |
| S169 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-25 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-310-J / TASK-310-L 自产内容，未包含任何真实设备的扫描、照片、ROM、固件内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **Switch BIOS/ROM 红线**：Nintendo Switch 的系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本包仅做清单级引用。因无法合规获取固件，本包 `emulator="none"`（保守，静态 + 入坞动画演示），`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选特别声明**：Yuzu / Ryujinx 因法律风险**仅清单级标注、不展开、不计数**，本包**不随包下发任何模拟器二进制**，也不推荐用户获取。
- **无介质声明**：本设备 `media_hint="cartridge"`（卡带介质有枚举），本包**不含任何固件 / 系统 ROM / 卡带镜像等介质文件**，仅以程序化低模网格与原创文案呈现。
- 商标（Nintendo、Switch 标志等）仅作用途登记，本包不对其使用方式做任何决策。
