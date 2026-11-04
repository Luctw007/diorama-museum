# MESHES.md — 占位网格说明（macintosh128k）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-58B 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 一体机壳（米色，顶部提手凹槽 + 内壁签名） | 约 34.5 cm 高 × 24.4 cm 宽 × 27.7 cm 深 | Wikipedia — Macintosh 128K（尺寸「需核实」） |
| crt_display.gltf | crt_display | 9 英寸黑白显像管（512×342） | 屏幕对角线 9 英寸（约 23 cm） | Wikipedia — Macintosh 128K |
| motherboard.gltf | motherboard | 主板（68000 + 128KB RAM + 64KB ROM） | 约 24 cm × 24 cm | Wikipedia — Macintosh 128K（「需核实」） |
| floppy_drive.gltf | floppy_drive | 3.5 英寸软驱（400KB） | 标准 3.5 英寸软驱位 | Wikipedia — Macintosh 128K |
| keyboard.gltf | keyboard | 键盘（无方向键、无数字小键盘） | 约 34 cm 宽 × 14 cm 深 | Wikipedia — Macintosh 128K（「需核实」） |
| mouse.gltf | mouse | 单键鼠标（滚球） | 约 6 cm 宽 × 11 cm 长 | Wikipedia — Macintosh 128K（「需核实」） |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。Macintosh 128K 的米色一体机壳、顶部提手凹槽与内壁工程师签名是其标志性外观，正式建模以存世实机与苹果官方资料为准，上表为 03 线调研近真值。
