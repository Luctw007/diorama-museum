# MESHES.md — 占位网格说明（altair-8800）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-178-A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| chassis.gltf | chassis | 机箱：蓝灰金属箱体，前面板一体 | 约 43 cm 宽 × 18 cm 高 × 46 cm 深（「需核实」） | [S94] |
| front_panel.gltf | front_panel | 前面板：数据/地址拨键开关阵列 + 状态 LED 灯条 | 约 43 cm 宽 × 13 cm 高（「需核实」） | [S94] |
| cpu_board.gltf | cpu_board | CPU 板：Intel 8080 + 时钟 + 总线驱动 | S-100 卡约 13.3 × 25.4 cm（「需核实」） | [S94][S95] |
| s100_backplane.gltf | s100_backplane | S-100 总线背板：多组扩展插槽 | 视插槽数，单机约 43 cm 宽（「需核实」） | [S95] |
| power_supply.gltf | power_supply | 电源：内置线性电源单元 | 机箱后部，视配置（「需核实」） | [S94] |
| expansion_card.gltf | expansion_card | 扩展接口卡：内存/串口/软盘控制器 | S-100 标准卡尺寸（「需核实」） | [S95] |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0）。Altair 8800 存世实机与复刻图纸相对丰富，尺寸以 MITS 手册与复刻机实测为准，上表为 03 线调研近真值；定价、销量与功耗口径待核，正式建模请以《Altair 8800 Operator's Manual》与可考档案为准。
