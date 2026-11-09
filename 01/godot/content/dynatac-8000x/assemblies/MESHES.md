# MESHES.md — 占位网格说明（dynatac-8000x）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-98A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| body.gltf | body | 机身（黑色塑料上下两半外壳，集成 LED 屏） | 机身主体约 25 cm 高（「需核实」） | Wikipedia — Motorola DynaTAC |
| antenna.gltf | antenna | 天线（可伸缩鞭状） | 拉出后整机总高约 33 cm（「需核实」） | Wikipedia — Motorola DynaTAC |
| earpiece.gltf | earpiece | 听筒（顶部扬声器开口） | 顶部，靠近耳朵 | Wikipedia — Motorola DynaTAC |
| keypad.gltf | keypad | 键盘（12 键：0-9、*、# + 发送/结束） | 机身中部 | Wikipedia — Motorola DynaTAC |
| pcb.gltf | pcb | PCB 主板（射频 + 基带 + 控制） | 机身内部，约占整机中上部 | Wikipedia — Motorola DynaTAC |
| battery.gltf | battery | 电池组（可拆卸镍镉） | 机身下半部约 1/3 体积（「需核实」） | Wikipedia — Motorola DynaTAC |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。DynaTAC 8000X 的「砖头机」黑色直立机身、可伸缩天线、12 键拨号键盘与底部电池组是其标志性特征，正式建模以存世实机与摩托罗拉官方资料为准，上表为 03 线调研近真值（尺寸均标「需核实」）。
