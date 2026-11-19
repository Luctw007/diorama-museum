# MESHES.md — 占位网格说明（data-general-nova）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-183-A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| chassis.gltf | chassis | 机箱：金属箱体，前面板一体 | 约 48 cm 宽 × 27 cm 高 × 50 cm 深（机架/台式，「需核实」） | [S98] |
| front_panel.gltf | front_panel | 前面板：数据/地址拨键开关阵列 + 状态 LED 灯条 | 约 48 cm 宽 × 13 cm 高（「需核实」） | [S98] |
| cpu_board.gltf | cpu_board | CPU 板：16 位处理器 + 时钟 + 总线驱动 | 小型机板卡级，约 40 × 27 cm（「需核实」） | [S98] |
| memory_backplane.gltf | memory_backplane | 内存背板：磁芯存储阵列 + 读写电路 | 机架级（「需核实」） | [S98] |
| power_supply.gltf | power_supply | 电源：内置线性电源单元 | 机箱后部，视配置（「需核实」） | [S98] |
| io_interface.gltf | io_interface | I/O 接口：纸带读入机 + 电传打字机接口 | 机架/外设级，视配置（「需核实」） | [S98] |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0）。Data General Nova 存世实机与复刻图纸相对丰富，尺寸以 Data General 手册与复刻机实测为准，上表为 03 线调研近真值；定价、销量与功耗口径待核，正式建模请以《Nova Programmer's Reference》与可考档案为准。
