# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `ms-pac-man-arcade`（Ms. Pac-Man 街机框体）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/cabinet.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子（盒子几何，非真实框体几何） |
| assemblies/control_panel.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| assemblies/coin_door.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| assemblies/crt_display.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| assemblies/joystick.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| assemblies/button.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| assemblies/speaker.gltf | 网格 | 原创 | - | - | TASK-325-D 程序化低模盒子 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-325-D 自产文案，未复制任何第三方文章原文 |
| S161 Wikipedia: Ms. Pac-Man | 文档 | CC | https://en.wikipedia.org/wiki/Ms._Pac-Man | 2026-11-27 | 事实索引，仅作线索，未复制原文 |
| S162 Wikipedia: Midway Games | 文档 | CC | https://en.wikipedia.org/wiki/Midway_Games | 2026-11-27 | 事实索引，仅作线索，未复制原文 |
| S163 Computer History Museum | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-27 | 视觉参考，未复制原文、未入库、未贴图 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-325-D 自产内容，未包含任何真实设备的扫描、照片、ROM、固件内容或版权材料。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **街机 ROM 红线（FR-E3）**：Ms. Pac-Man 街机基板 ROM 受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑模拟器（MAME `mspacman` 驱动）时 ROM 由用户自备，获取与授权单独走合规流程。因无法合规获取 ROM，本包 `emulator="none"`（保守，静态 + 投币/四向摇杆交互示意）、`media_hint="none"`、`bios_required=false`、`bios_guide_url=null`。
- **模拟器候选需核实**：MAME `mspacman` 驱动的许可状态标「需核实」，本包不下发任何模拟器二进制。
- **框体尺寸/参数无来源需核实**：本包框体尺寸（约 0.6×0.8×1.8 m 等）与硬件参数（Z80 主频、图形/音源芯片型号等）均为公开近似值，无可靠出处者标「需核实」，不构成对任何具体机型的史实断言。
- **无介质声明**：本设备 `media_hint="none"`（街机框体基板无通用介质提示），本包**不含任何 ROM / 基板固件等介质文件**，仅以程序化低模网格与原创文案呈现。
- 商标（Ms. Pac-Man、Midway 标志等）仅作用途登记，本包不对其使用方式做任何决策。
