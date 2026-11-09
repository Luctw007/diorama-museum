# MESHES.md — 占位网格说明（palm-pilot）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-132 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| body.gltf | body | 机身（深灰塑料袖珍机身，圆角） | 约 120×80×18 mm（「需核实」） | Wikipedia — PalmPilot |
| display.gltf | display | 单色触控屏（160×160 + 手写区） | 约 60×60 mm（「需核实」） | Wikipedia — PalmPilot |
| motherboard.gltf | motherboard | 主板（DragonBall MC68328 + 128KB） | 机身内部（「需核实」） | Wikipedia — PalmPilot |
| battery_bay.gltf | battery_bay | 电池仓（AAA×2） | 机身内部（「需核实」） | Wikipedia — PalmPilot |
| stylus.gltf | stylus | 触控笔（塑料手写笔，机身侧槽） | 与机身等高（「需核实」） | Wikipedia — PalmPilot |
| hotsync_dock.gltf | hotsync_dock | HotSync 同步底座（串口同步） | 底座尺寸（「需核实」） | Wikipedia — PalmPilot |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。Palm Pilot 的单色触控屏、Graffiti 手写区、触控笔与 HotSync 底座是其标志性特征，正式建模以存世实机与 Palm 官方资料为准，上表为 03 线调研近真值（尺寸均标「需核实」）。
