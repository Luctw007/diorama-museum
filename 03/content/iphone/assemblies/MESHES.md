# MESHES.md — 占位网格说明（iphone）

本目录（`assemblies/`）下 5 个 glTF 均为 TASK-108A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 机身（铝制后壳 + 前玻璃面板，含 Home 键/电源键/摄像头） | 115×61×11.6 mm | Wikipedia — iPhone (first generation) |
| display.gltf | display | 显示屏（3.5 英寸多点触控屏） | 3.5 英寸，320×480 | Wikipedia — iPhone (first generation) |
| pcb.gltf | pcb | 主板（ARM11 + 基带 + WiFi + 加速度计） | 机身内部 | Wikipedia — iPhone (first generation) |
| battery.gltf | battery | 电池（内置不可拆卸锂离子） | 机身内部 | Wikipedia — iPhone (first generation) |
| dock_connector.gltf | dock_connector | Dock 接口（30 针充电/同步口） | 机身底部 | Wikipedia — iPhone (first generation) |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。iPhone 初代的 3.5 英寸大屏、唯一正面实体 Home 键与铝制圆角机身是其标志性特征，正式建模以存世实机与苹果官方资料为准，上表为 03 线调研近真值。
