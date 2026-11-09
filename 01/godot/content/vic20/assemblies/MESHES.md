# MESHES.md — 占位网格说明（vic20）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-93A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 一体机身（白色键盘主机一体壳） | 约 40 cm 宽 × 20 cm 深 × 6 cm 高 | Wikipedia — Commodore VIC-20（「需核实」） |
| keyboard.gltf | keyboard | 键盘（与主机一体） | 与机身同宽 | Wikipedia — Commodore VIC-20（「需核实」） |
| motherboard.gltf | motherboard | 主板（6502 + VIC 芯片 + 5KB + BASIC ROM） | 约 25 cm × 20 cm | Wikipedia — Commodore VIC-20（「需核实」） |
| power.gltf | power | 电源（外置） | 外置式，与机身分离 | Wikipedia — Commodore VIC-20（「需核实」） |
| datasette.gltf | datasette | 外置数据磁带机（Datasette） | 标准卡式磁带机尺寸 | Wikipedia — Commodore VIC-20 |
| monitor.gltf | monitor | 显示器（家用电视） | 接家用电视 | Wikipedia — Commodore VIC-20 |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。VIC-20 的白色键盘主机一体壳、VIC 彩色图形芯片与外置 Datasette 磁带机是其标志性特征，正式建模以存世实机与 Commodore 官方资料为准，上表为 03 线调研近真值。
