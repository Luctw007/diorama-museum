# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `apple-iie`（Apple IIe）内容包中所有资产的来源与许可信息。

> 许可分档四档：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/whole.gltf | 网格 | 原创 | - | - | TASK-210-A 程序化占位盒（盒子几何，非真实机箱几何） |
| assemblies/case.gltf | 网格 | 原创 | - | - | TASK-210-A 程序化占位盒 |
| assemblies/keyboard.gltf | 网格 | 原创 | - | - | TASK-210-A 程序化占位盒 |
| assemblies/monitor.gltf | 网格 | 原创 | - | - | TASK-210-A 程序化占位盒 |
| assemblies/floppy.gltf | 网格 | 原创 | - | - | TASK-210-A 程序化占位盒 |
| assemblies/power_supply.gltf | 网格 | 原创 | - | - | TASK-210-A 程序化占位盒 |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-210-A 自产文案，未复制任何第三方文章原文 |
| S116 Wikipedia: Apple IIe | 文档 | CC | https://en.wikipedia.org/wiki/Apple_IIe | 2026-11-14 | 事实索引，仅作线索，未复制原文 |
| S117 Wikipedia: Apple II | 文档 | CC | https://en.wikipedia.org/wiki/Apple_II | 2026-11-14 | 事实索引，仅作线索，未复制原文 |
| S118 Computer History Museum: Apple II | 文档 | 仅视觉参考 | https://www.computerhistory.org/ | 2026-11-14 | 视觉参考，未复制原文、未入库、未贴图 |
| MAME Driver: Apple II（apple2e） | 文档 | 授权许可 | https://wiki.mamedev.org/index.php/Driver:Apple_II | 2026-11-14 | 硬件资料（GPL 文档），仅作运行配置依据；**许可需核实** |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-210-A 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、磁盘镜像或版权材料。
- 上表「CC / 授权许可 / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- **Apple IIe ROM 红线**：Apple IIe 的 ROM（含 **Monitor ROM** 与 **Applesoft BASIC**）受版权保护，**不入库、不下载**，本包仅做清单级引用；真跑时获取与授权须单独走合规流程（用户自备）。
- **MAME 许可需核实**：MAME `apple2e` 驱动的许可状态标「需核实」，本包不下发 MAME 二进制。
- 商标（Apple 标志、Apple IIe 字样等）仅作用途登记，本包不对其使用方式做任何决策。
