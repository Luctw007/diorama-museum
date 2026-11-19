# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `dvd-player`（DVD 播放机）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/whole.gltf | 网格 | 原创 | - | - | TASK-220-A 程序化低模盒子（盒子几何，非真实机箱几何） |
| assemblies/disc_tray.gltf | 网格 | 原创 | - | - | TASK-220-A 程序化低模盒子 |
| assemblies/laser_pickup.gltf | 网格 | 原创 | - | - | TASK-220-A 程序化低模盒子 |
| assemblies/front_panel.gltf | 网格 | 原创 | - | - | TASK-220-A 程序化低模盒子 |
| assemblies/power_supply.gltf | 网格 | 原创 | - | - | TASK-220-A 程序化低模盒子 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-220-A 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-240-A 自产文案，未复制任何第三方文章原文 |
| S125 Wikipedia: DVD player | 文档 | CC | https://en.wikipedia.org/wiki/DVD_player | 2026-11-20 | 事实索引，仅作线索，未复制原文 |
| S126 Wikipedia: DVD | 文档 | CC | https://en.wikipedia.org/wiki/DVD | 2026-11-20 | 事实索引，仅作线索，未复制原文 |
| S127 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-20 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-220-A / TASK-240-A 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、影碟内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **无模拟器声明**：本设备 `emulator="none"`，为静态展示 + 光盘托盘动画演示模式，**不下发、不依赖任何模拟器二进制**；`bios_required=false`、`bios_guide_url=null`。
- **无介质声明**：本设备 `media_hint="none"`，**不含任何 ROM / 固件 / 影碟影像等介质文件**，仅以程序化低模网格与原创文案呈现；DVD 光盘（disc）为可选物理示意件，不涉及版权内容。
- 商标（DVD 标志等）仅作用途登记，本包不对其使用方式做任何决策。
