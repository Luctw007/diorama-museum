# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-225-A：`cd-player` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| whole.gltf | whole | 120 | 180 | 7 | 整机：深灰机箱主体 + 顶盖 + 前面板 + 光盘托盘 + 光盘 + 显示窗 + 按键×4 + 出仓键 + 机脚×4 |
| disc_tray.gltf | disc_tray | 104 | 156 | 6 | 光盘托盘：黑色托盘 + 底托 + 前沿 + 光盘（双层）+ 轴孔 + 金属导轨 + 内部 PCB + IC |
| laser_pickup.gltf | laser_pickup | 104 | 156 | 5 | 激光头组件：金属银激光头 + 支架 + 底座导轨 + 磁头 + IC + PCB + 透镜 |
| front_panel.gltf | front_panel | 104 | 156 | 7 | 前面板：深灰面板条 + 上/下沿 + 按键×5 + 出仓键 + 显示窗 + 入碟口 + 内部 PCB |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖 + 两侧板 + 开关 + 线缆 + 内部 PCB + IC + 指示灯 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + 解码/伺服 IC×4 + 电容×3 + 接口×2 + 激光头接口 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 深灰 | (0.08, 0.08, 0.09) | 机箱主体塑料 |
| tray 黑 | (0.05, 0.05, 0.06) | 光盘托盘 |
| metal 金属银 | (0.72, 0.74, 0.78) | 激光头/伺服/导轨/接口 |
| panel 深灰 | (0.15, 0.15, 0.16) | 前面板塑料 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 解码/伺服 IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 |
| disc 光盘银面 | (0.65, 0.70, 0.72) | CD 光盘反光面 |
| display 荧光蓝 | (0.30, 0.60, 0.75) | VFD 显示窗荧光色 |
| black 黑 | (0.05, 0.05, 0.06) | 按键 / 轴孔 / 线缆 / 电容 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/whole.gltf | whole |
| assemblies/disc_tray.gltf | disc_tray |
| assemblies/laser_pickup.gltf | laser_pickup |
| assemblies/front_panel.gltf | front_panel |
| assemblies/power_supply.gltf | power_supply |
| assemblies/mainboard.gltf | mainboard |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `18_CD播放机预研卡.md`（家用 CD 播放机约 430×300×90 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 18 号预研卡部件草图取 6 件（whole + 光盘托盘/激光头组件/前面板/电源/主板）；chassis 并入 whole 示意，disc/display 并入 whole 或 front_panel 示意。
- **disc_tray 识别件**：光盘托盘为可抽拉识别件，低模以黑色扁平盒 + 光盘示意；**进出仓动画**在后续建模卡以该 node 为抽拉轴实现（本卡仅备静态低模）。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）。
