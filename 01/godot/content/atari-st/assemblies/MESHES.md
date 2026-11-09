# MESHES.md — 占位网格说明（atari-st）

本目录（`assemblies/`）下 5 个 glTF 均为 TASK-73A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 机身壳（灰色紧凑机身，含软驱位） | 约 47 cm 宽 × 23 cm 深 × 7 cm 高 | Wikipedia — Atari ST（「需核实」） |
| keyboard.gltf | keyboard | 键盘（一体式，含功能键区） | 与机身同宽 | Wikipedia — Atari ST（「需核实」） |
| motherboard.gltf | motherboard | 主板（68000 + Shifter/GLUE/MMU + 512KB + TOS ROM） | 约 30 cm × 25 cm | Wikipedia — Atari ST（「需核实」） |
| floppy_drive.gltf | floppy_drive | 3.5 英寸软驱（720KB） | 标准 3.5" 软驱位 | Wikipedia — Atari ST |
| mouse.gltf | mouse | 两键鼠标 | 约 6 cm 宽 × 11 cm 长 | Wikipedia — Atari ST（「需核实」） |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。Atari ST 的灰色紧凑机身、一体式键盘与内置 MIDI 接口是其标志性特征，正式建模以存世实机与雅达利官方资料为准，上表为 03 线调研近真值。
