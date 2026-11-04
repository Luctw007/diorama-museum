# MESHES.md — 占位网格说明（eniac）

本目录下 4 个 glTF 均为 TASK-08 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| whole.gltf | whole | U 形联排机柜整体外轮廓 | 占地约 167 m²（约 30 m × 5.6 m 的 U 形）、高约 3 m | 03 线 07 章 [S22] |
| accumulator_unit.gltf | accumulator_unit | 单个累加器面板（十位十进制 + 氖灯显示 + 管座） | 单面板约 0.6 m 宽 × 2.4 m 高 | [S22][S04] |
| function_table_unit.gltf | function_table_unit | 函数表面板（可拔插电阻网络） | 单面板约 0.6 m × 2.4 m | [S22] |
| master_programmer_unit.gltf | master_programmer_unit | 主程序器步进开关面板 | 单面板约 0.6 m × 2.4 m | [S22] |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0）；尺寸为 03 线调研近真值，正式建模请以原始档案实测为准。
