# MESHES.md — 占位网格说明（nokia-8110）

本目录（`assemblies/`）下 6 个 glTF 均为 TASK-218-A 自产**占位盒**（单位盒：8 顶点 / 12 三角面，半长 0.5，居中于原点），用于让 `mesh_ref` 通过 R-016/R-041/R-090 校验并占住装配层级中的网格引用位。未来替换为真实网格时的目标外观与尺寸依据如下。

| 文件 | node 名 | 未来目标外观 | 尺寸依据 | 资料来源 |
|---|---|---|---|---|
| slider_cover.gltf | slider_cover | 弧形滑盖上盖（滑动件） | 机身上半部（「需核实」） | Wikipedia — Nokia 8110 |
| body.gltf | body | 弧形机身主体（下半部） | 约 14 cm 全长（「需核实」） | Wikipedia — Nokia 8110 |
| keypad.gltf | keypad | 键盘（数字键 + 导航键，藏于滑盖下） | 机身下半部 | Wikipedia — Nokia 8110 |
| lcd.gltf | lcd | 单色 LCD 屏 | 机身上部（「需核实」） | Wikipedia — Nokia 8110 |
| microphone.gltf | microphone | 话筒（滑盖前端） | 滑盖前端 | Wikipedia — Nokia 8110 |
| battery.gltf | battery | 可拆电池 | 机身下半部（「需核实」） | Wikipedia — Nokia 8110 |

> 替换注意：真实网格须遵守规范 §1.3（米、Y-up、右手系）与 §1.4（glTF 2.0），并按 v0.3 第十三章做 LOD 三档与增量替换。Nokia 8110 的弧形滑盖「香蕉机」造型、滑盖接听交互与《黑客帝国》出镜是其标志性特征，正式建模以存世实机与诺基亚官方资料为准，上表为 03 线调研近真值（尺寸均标「需核实」）。
