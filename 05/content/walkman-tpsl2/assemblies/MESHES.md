# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-220-B：`walkman-tpsl2` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| whole.gltf | whole | 104 | 156 | 9 | 整机：银灰机身 + 顶盖 + 磁带舱 + 磁带 + 磁头 + 绿播放键 + 快进/快退/停止键 + 耳机插孔 + 电池仓 + 标识 |
| cassette_bay.gltf | cassette_bay | 104 | 156 | 7 | 磁带舱：深灰舱盖 + 底盖 + 磁带盒 + 盘口 + 铰链 + 磁头 + 金属件 + 内部 PCB + IC |
| head_module.gltf | head_module | 104 | 156 | 7 | 磁头组件：金属银磁头（3 段）+ 支架 + 底座 + 压带轮 + IC + PCB + 磁头芯 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板×2 + 放音/功放 IC×4 + 电容×2 + 接口×3 + 磁头接口 |
| battery_compartment.gltf | battery_compartment | 104 | 156 | 7 | 电池仓：机身舱 + 舱盖 + 电池×3 + 触片×3 + 底壳 + 内部 PCB + IC |
| control_panel.gltf | control_panel | 104 | 156 | 7 | 按键面板：机身条 + 底条 + 绿播放键 + 快进/快退/停止键×4 + 耳机插孔 + 金属件 + 内部 PCB |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 银灰 | (0.35, 0.35, 0.38) | TPS-L2 蓝银色金属/塑料机身 |
| bay 深灰 | (0.30, 0.30, 0.32) | 磁带舱盖 |
| head 金属银 | (0.72, 0.74, 0.78) | 磁头/压带轮金属件 |
| metal 金属银 | (0.72, 0.74, 0.78) | 铰链/导轨/触片 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 放音/功放 IC |
| battery 金属银 | (0.65, 0.66, 0.68) | 电池触片/电池体 |
| control 按键黑 | (0.05, 0.05, 0.06) | [快进]/[快退]/[停止] |
| play 播放键绿 | (0.20, 0.55, 0.25) | [播放] 绿色键 |
| headphone 金属银 | (0.72, 0.74, 0.78) | 耳机插孔金属环 |
| cassette 深灰 | (0.30, 0.30, 0.32) | 磁带外壳 |
| black 黑 | (0.05, 0.05, 0.06) | 标识/盘口 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/whole.gltf | whole |
| assemblies/cassette_bay.gltf | cassette_bay |
| assemblies/head_module.gltf | head_module |
| assemblies/mainboard.gltf | mainboard |
| assemblies/battery_compartment.gltf | battery_compartment |
| assemblies/control_panel.gltf | control_panel |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `17_Walkman预研卡.md`（TPS-L2 约 150×90×35 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 17 号预研卡部件草图取 6 件（whole + 磁带舱/磁头组件/主板/电池仓/按键面板）；chassis 并入 whole 示意，headphone_jack/cassette 并入 whole 或 control_panel 示意。
- **cassette_bay 识别件**：磁带舱盖为可开合识别件，低模以深灰盒 + 磁带示意；**磁带舱开合动画**在后续建模卡以该 node 为开合轴实现（本卡仅备静态低模）。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104（>100 且 <4000）。
