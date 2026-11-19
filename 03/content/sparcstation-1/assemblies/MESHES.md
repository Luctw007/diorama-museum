# MESHES.md — 占位网格说明（sparcstation-1）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-213-A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| case.gltf | case | 机身：紧凑桌面机箱（「披萨盒」形态） | 约 40 cm 宽 × 10 cm 高 × 40 cm 深（「需核实」） | [S113] |
| motherboard.gltf | motherboard | 主板：SPARC 处理器 + 内存模块 | 约 35 × 35 cm（「需核实」） | [S113] |
| power_supply.gltf | power_supply | 电源：内置电源单元 | 机箱后部，视配置（「需核实」） | [S113] |
| disk.gltf | disk | 硬盘：内置硬盘 | 3.5 英寸半高（「需核实」） | [S113] |
| io_ports.gltf | io_ports | I/O 接口：串行/并行/网络接口 | 机箱后部接口面板（「需核实」） | [S113] |
| monitor.gltf | monitor | 显示器：外接 CRT 显示器 | 外接显示器（「需核实」） | [S113] |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0）。SPARCstation 1 存世实机与档案照片相对丰富，尺寸以 Sun 手册与可考档案为准，上表为 03 线调研近真值；主频、内存等参数口径待核，正式建模请以《SPARCstation 1 Hardware Manual》与可考档案为准。
