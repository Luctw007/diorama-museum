# MESHES.md — 占位网格说明（pdp11）

本目录（`assemblies/`）下 5 个 glTF 均为 TASK-28B 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| console.gltf | console | 操作台：终端 + 状态灯组 + 控制开关 | 约 0.6 m 宽 × 0.3 m 高操作台面 | [S36]（hall-mainframe/03_PDP11.md，尺寸「需核实」） |
| cpu_cabinet.gltf | cpu_cabinet | CPU 柜：处理器 + 缓存 + MMU + Unibus 适配器 | 单机架约 0.6 m 宽 × 1.6 m 高 | [S36]（「需核实」） |
| disk_rk05.gltf | disk_rk05 | RK05 可换盘磁盘组 | 单机约 0.48 m 宽 × 0.26 m 高（19 英寸机架） | [S36]（「需核实」） |
| tape_tu10.gltf | tape_tu10 | TU10/TS11 磁带机 | 单机约 0.48 m 宽 × 0.66 m 高（机架） | [S36]（「需核实」） |
| unibus_rack.gltf | unibus_rack | Unibus 扩展架（背板 + 设备控制器插槽） | 约 0.48 m 宽 × 0.6 m 高扩展架 | [S36]（「需核实」） |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0）。PDP-11/70 为 1975 年 DEC 高端机型，尺寸以 DEC 手册与存世实机为准，上表为 03 线调研近真值；正式建模请以《DEC PDP-11/70 Handbook》与可考档案为准。
