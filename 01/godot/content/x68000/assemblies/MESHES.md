# MESHES.md — 占位网格说明（x68000）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-103A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| main_tower.gltf | main_tower | 主机塔（塔式立式机箱，含徽标/开关/SCSI 口） | 约 26 cm 宽 × 32 cm 高 × 9 cm 深（「需核实」） | Wikipedia — Sharp X68000 |
| keyboard.gltf | keyboard | 键盘（独立 101 键） | 标准全尺寸（「需核实」） | Wikipedia — Sharp X68000 |
| mouse.gltf | mouse | 鼠标（专用滚球） | 标准鼠标尺寸（「需核实」） | Wikipedia — Sharp X68000 |
| motherboard.gltf | motherboard | 主板（68000 + 图形 + FM/PCM 音频 + IPL ROM） | 主机塔内部 | Wikipedia — Sharp X68000 |
| floppy_bay.gltf | floppy_bay | 5.25 英寸双软驱位 | 主机塔前部 | Wikipedia — Sharp X68000 |
| power.gltf | power | 电源（塔式机箱内置） | 主机塔内部 | Wikipedia — Sharp X68000 |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。X68000 的「塔式双立式」机箱、5.25 英寸双软驱位与内置 FM+PCM 音频是其标志性特征，正式建模以存世实机与夏普官方资料为准，上表为 03 线调研近真值（尺寸均标「需核实」）。
