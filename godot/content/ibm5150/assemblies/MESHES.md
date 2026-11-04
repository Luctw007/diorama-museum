# MESHES.md — 占位网格说明（ibm5150）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-38B 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 主机箱（卧式米色机箱） | 约 50 cm 宽 × 40 cm 深 × 15 cm 高 | [S48]（hall-personal/02_IBMPC5150.md，尺寸「需核实」） |
| front_panel.gltf | front_panel | 前面板（双软驱位 + 红色电源拨杆） | 与机箱同宽 | [S48]（「需核实」） |
| motherboard.gltf | motherboard | 主板（8088 + BIOS + ISA 扩展槽） | 约 35 cm × 30 cm | [S48]（「需核实」） |
| monitor.gltf | monitor | 单色显示器（MDA 5151，80×25 文本） | 约 32 cm 宽 × 30 cm 高 | [S48]（「需核实」） |
| keyboard.gltf | keyboard | 键盘（83 键 Model F） | 约 50 cm 宽 × 18 cm 深 | [S48]（「需核实」） |
| power.gltf | power | 电源（内置 + 散热风扇） | 与机箱后部匹配 | [S48]（「需核实」） |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。IBM PC 5150 的卧式机箱与红色电源拨杆是其标志性外观，正式建模以存世实机与 IBM 手册为准，上表为 03 线调研近真值。
