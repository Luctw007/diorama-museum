# MESHES.md — 占位网格说明（amiga-1000）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-208-A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 机身：一体式机箱，键盘可收纳于下方 | 约 43 cm 宽 × 9 cm 高 × 34 cm 深（「需核实」） | [S110] |
| keyboard.gltf | keyboard | 键盘：可翻转收纳键盘 | 标准键盘尺寸（「需核实」） | [S110] |
| motherboard.gltf | motherboard | 主板：68000 + Agnus/Denise/Paula 三芯片组 | 约 40 × 34 cm（「需核实」） | [S110] |
| floppy.gltf | floppy | 软驱：3.5 英寸软驱 | 3.5 英寸半高（「需核实」） | [S110] |
| mouse.gltf | mouse | 鼠标：双键鼠标 | 手持尺寸（「需核实」） | [S110] |
| monitor.gltf | monitor | 显示器：外接彩色 CRT | 外接显示器（「需核实」） | [S110] |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0）。Amiga 1000 存世实机与档案照片相对丰富，尺寸以 Commodore 手册与可考档案为准，上表为 03 线调研近真值；内存 256 KB 起等口径待核，正式建模请以《Amiga 1000 Technical Reference》与可考档案为准。
