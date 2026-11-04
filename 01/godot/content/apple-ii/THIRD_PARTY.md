# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `apple-ii`（Apple II）内容包中所有资产的来源与许可信息。

> 许可分档四档（见《内容包规范 v0.1》第八章）：
> `公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；
> 自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| meshes/case.gltf | 网格 | 原创 | - | - | TASK-10 手写占位几何（单位三角，非真实机箱几何） |
| meshes/mainboard.gltf | 网格 | 原创 | - | - | TASK-10 手写占位几何（单位三角，非真实主板几何） |
| meshes/keyboard.gltf | 网格 | 原创 | - | - | TASK-10 手写占位几何（单位三角，非真实键盘几何） |
| meshes/disk_ii.gltf | 网格 | 原创 | - | - | TASK-10 手写占位几何（单位三角，非真实软驱几何） |
| meta.json / runtime.json / annotations.json 文案 | 文案 | 原创 | - | - | TASK-10 自产文案，未复制任何第三方文章原文 |
| S01 Wikipedia: Apple II | 文档 | CC | https://en.wikipedia.org/wiki/Apple_II | 2026-10-31 | 事实索引，仅作线索，未复制原文 |
| S02 Apple II Reference Manual (1979) | 文档 | 仅视觉参考 | https://archive.org/details/Apple_II_Reference_Manual_1979_Apple | 2026-10-31 | 结构/参数参考，未入库、未贴图 |
| S05 CHM: The Apple II | 文档 | 仅视觉参考 | https://www.computerhistory.org/revolution/personal-computers/17/300 | 2026-10-31 | 历史叙事参考，未复制原文 |
| S06 CHM: Apple II DOS 源码 | 文档 | 授权许可 | https://www.computerhistory.org/software-gems/apple-ii-dos-source-code/ | 2026-10-31 | Apple 许可、非商业使用，本包未含任何源码 |
| S07 MAME Driver:Apple II | 文档 | 授权许可 | https://wiki.mamedev.org/index.php/Driver:Apple_II | 2026-10-31 | 硬件资料（GPL 文档），仅作运行配置依据 |
| S08 MAME apple2 源码 | 文档 | 授权许可 | https://github.com/mamedev/mame | 2026-10-31 | GPL-2.0/BSD-3，未含任何源码 |
| S09 AppleWin GitHub | 文档 | 授权许可 | https://github.com/AppleWin/AppleWin | 2026-10-31 | GPL-2.0，未含任何源码 |
| S11 Apple v. Franklin Computer Corp. | 文档 | 公共领域 | https://en.wikipedia.org/wiki/Apple_Computer,_Inc._v._Franklin_Computer_Corp. | 2026-10-31 | 判例，ROM 版权依据 |
| S12 RetroTechCollection: Apple II | 文档 | CC | https://wiki.retrotechcollection.com/index.php?title=Apple_II | 2026-10-31 | 尺寸/主板修订参考 |
| S13 MacDB.cn: Apple II | 文档 | CC | https://macdb.cn/device/apple-ii | 2026-10-31 | 尺寸交叉印证 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-10 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、磁盘镜像或版权材料。
- 上表「CC / 授权许可 / 仅视觉参考 / 公共领域」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。
- 商标（Apple 标志、Apple II 字样等）仅作用途登记，本包不对其使用方式做任何决策（见 FR-J2，待法律意见）。
