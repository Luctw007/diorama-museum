# MESHES.md — 占位网格说明（pet2001）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-83A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 一体机身壳（梯形金属外壳，集成键盘/主机/显示器） | 约 46 cm 宽 × 40 cm 深 × 40 cm 高 | Wikipedia — Commodore PET（「需核实」） |
| cassette_drive.gltf | cassette_drive | 内置 Datasette 磁带机 | 标准卡式磁带机位 | Wikipedia — Commodore PET |
| keyboard.gltf | keyboard | chiclet 计算器式小方键键盘 | 与机身同宽 | Wikipedia — Commodore PET（「需核实」） |
| motherboard.gltf | motherboard | 主板（6502 + 4KB + BASIC ROM + 6522 VIA） | 约 30 cm × 25 cm | Wikipedia — Commodore PET（「需核实」） |
| crt_monitor.gltf | crt_monitor | 9 英寸绿色磷光 CRT 监视器 | 对角线 9 英寸 | Wikipedia — Commodore PET |
| power.gltf | power | 电源（内置） | 集成于机壳内 | Wikipedia — Commodore PET（「需核实」） |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。PET 2001 的梯形金属一体机壳、内置 9 英寸绿磷光 CRT、chiclet 小键盘与内置磁带机是其标志性特征，正式建模以存世实机与 Commodore 官方资料为准，上表为 03 线调研近真值。
