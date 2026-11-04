# MESHES.md — 占位网格说明（commodore64）

本目录（`assemblies/`）下 5 个 glTF 均为 TASK-38A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 主机壳（"breadbin" 面包箱造型：米色一体式机身） | 约 40 cm 宽 × 20 cm 深 × 8 cm 高 | [S44]（hall-personal/01_Commodore64.md，尺寸「需核实」） |
| keyboard.gltf | keyboard | 键盘（QWERTY + 功能键） | 与机身同宽，约 40 cm × 15 cm | [S44]（「需核实」） |
| motherboard.gltf | motherboard | 主板（6510/VIC-II/SID 三芯片 + RAM + ROM） | 约 30 cm × 20 cm | [S44]（「需核实」） |
| power.gltf | power | 电源（外置电源砖 + 机内稳压） | 外置砖约 15 cm × 10 cm × 6 cm | [S44]（「需核实」） |
| datasette.gltf | datasette | Datasette 磁带机 | 约 20 cm 宽 × 10 cm 深 × 5 cm 高 | [S44]（「需核实」） |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。C64 的"breadbin"造型是其标志性外观，正式建模以存世实机与手册为准，上表为 03 线调研近真值。
