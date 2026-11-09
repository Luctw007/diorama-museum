# MESHES.md — 占位网格说明（next）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-131 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| chassis.gltf | chassis | 主机塔（黑色镁合金立方体机箱） | 约 1 英尺（30.5 cm）见方（「需核实」） | Wikipedia — NeXT Computer |
| motherboard.gltf | motherboard | 主板（68030 + DSP56001） | 机箱内部 | Wikipedia — NeXT Computer |
| mo_drive.gltf | mo_drive | 磁光盘位（256MB MO 驱动） | 机箱正面 | Wikipedia — NeXT Computer |
| monitor.gltf | monitor | 显示器（灰度高分辨率 CRT） | 约 17 英寸（「需核实」） | Wikipedia — NeXT Computer |
| keyboard.gltf | keyboard | 键盘（85 键） | 标准全尺寸（「需核实」） | Wikipedia — NeXT Computer |
| mouse.gltf | mouse | 鼠标（方形双键） | 标准鼠标尺寸（「需核实」） | Wikipedia — NeXT Computer |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。NeXT 的黑色镁合金立方体机箱、方形双键鼠标与 256MB 磁光盘是其标志性特征，正式建模以存世实机与 NeXT 官方资料为准，上表为 03 线调研近真值（尺寸均标「需核实」）。
