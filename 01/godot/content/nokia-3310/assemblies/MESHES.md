# MESHES.md — 占位网格说明（nokia-3310）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-173-B 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 外壳（前面板 + 可拆后盖，Xpress-on 换壳） | 约 113×48×22 mm（「需核实」） | Wikipedia — Nokia 3310 |
| keypad.gltf | keypad | 键盘（九键数字 + 导航键 + 电源键） | 机身下半部 | Wikipedia — Nokia 3310 |
| display.gltf | display | 单色 LCD 屏（84×48） | 机身中上部（「需核实」） | Wikipedia — Nokia 3310 |
| motherboard.gltf | motherboard | 主板 PCB（基带 + 射频 + SIM 卡座） | 机身内部 | Wikipedia — Nokia 3310 |
| battery.gltf | battery | 可拆电池（锂离子） | 机身下半部（「需核实」） | Wikipedia — Nokia 3310 |
| antenna.gltf | antenna | 内置天线 | 机身内部顶部 | Wikipedia — Nokia 3310 |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。Nokia 3310 的可换 Xpress-on 彩壳、九键键盘与单色点阵屏是其标志性特征，正式建模以存世实机与诺基亚官方资料为准，上表为 03 线调研近真值（尺寸均标「需核实」）。
