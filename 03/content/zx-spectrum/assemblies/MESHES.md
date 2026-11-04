# MESHES.md — 占位网格说明（zx-spectrum）

本目录（`assemblies/`）下 5 个 glTF 均为 TASK-63A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 机身壳（黑色紧凑机身 + 右侧彩虹条纹） | 约 23.3 cm 宽 × 14.4 cm 深 × 3.0 cm 高 | Wikipedia — ZX Spectrum（尺寸「需核实」） |
| keyboard.gltf | keyboard | 橡胶键盘矩阵（40 键） | 约 20 cm 宽 × 10 cm 深 | Wikipedia — ZX Spectrum（「需核实」） |
| motherboard.gltf | motherboard | 主板（Z80 + ULA + 48KB RAM + 16KB ROM） | 约 21 cm × 13 cm | Wikipedia — ZX Spectrum（「需核实」） |
| power.gltf | power | 外置电源（适配器） | 外置式，与机身分离 | Wikipedia — ZX Spectrum（「需核实」） |
| expansion_port.gltf | expansion_port | 边框扩展口（尾部连接器） | 与机身尾部等宽 | Wikipedia — ZX Spectrum |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。ZX Spectrum 的黑色紧凑机身、右侧彩虹条纹与整面橡胶键盘是其标志性外观，正式建模以存世实机与 Sinclair 官方资料为准，上表为 03 线调研近真值。
