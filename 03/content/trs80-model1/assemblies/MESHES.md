# MESHES.md — 占位网格说明（trs80-model1）

本目录（`assemblies/`）下 5 个 glTF 均为 TASK-78A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| keyboard_unit.gltf | keyboard_unit | 键盘主机一体（Z80 + 内存 + 53 键键盘的扁平盒） | 约 40 cm 宽 × 20 cm 深 × 6 cm 高 | Wikipedia — TRS-80（「需核实」） |
| monitor.gltf | monitor | 黑白显示器（RCA 电视改装的 CRT） | 12 英寸黑白 CRT | Wikipedia — TRS-80（「需核实」） |
| expansion_interface.gltf | expansion_interface | 底部 DIN 扩展口（Expansion Interface） | 与主机底部匹配 | Wikipedia — TRS-80 |
| power.gltf | power | 独立电源单元 | 独立式，与主机分离 | Wikipedia — TRS-80（「需核实」） |
| cassette_recorder.gltf | cassette_recorder | 卡式磁带机 | 标准卡式录音机尺寸 | Wikipedia — TRS-80 |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。TRS-80 Model I 的键盘主机一体扁平盒、独立黑白显示器与底部 DIN 扩展口是其标志性特征，正式建模以存世实机与 Tandy 官方资料为准，上表为 03 线调研近真值。
