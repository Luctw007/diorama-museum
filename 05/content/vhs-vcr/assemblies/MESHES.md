# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-215-A：`vhs-vcr` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| whole.gltf | whole | 120 | 180 | 8 | 整机：深灰机箱主体 + 顶盖 + 前面板 + 磁头鼓 + 磁带 + 带仓机构 + 红录音键 + 显示窗 + 电源/播放/停止键 + 机脚 |
| cassette_mechanism.gltf | cassette_mechanism | 104 | 156 | 6 | 磁带加载机构：黑色带仓机构 + 加载臂×4 + 磁带盒 + 盘口 + 金属件 + 内部 PCB + IC |
| head_drum.gltf | head_drum | 104 | 156 | 6 | 磁头鼓：金属银磁鼓（6 段递减盒近似圆柱，**可旋转识别件**）+ 底座 + 轴 + 磁头 + IC + PCB + 指示灯 |
| front_panel.gltf | front_panel | 104 | 156 | 6 | 前面板：深灰面板条 + 上/下沿 + 按键×5 + 红录音键 + VFD 显示窗 + 入带口 + 电源键 + 金属框 |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖/侧板/底盖 + 开关 + 线缆 + 内部 PCB + IC + 指示灯 + 散热片 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + 伺服/信号 IC×4 + 电容×3 + 接口×3 + 磁鼓接口 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 深灰 | (0.08, 0.08, 0.09) | 机箱主体塑料 |
| panel 深灰 | (0.15, 0.15, 0.16) | 前面板塑料 |
| drum 金属银 | (0.72, 0.74, 0.78) | 磁头鼓（斜装旋转件） |
| mechanism 黑 | (0.05, 0.05, 0.06) | 带仓加载机构 |
| cassette 黑 | (0.05, 0.05, 0.06) | VHS 磁带盒外壳 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 机构内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 伺服/信号 IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 |
| rec 录音键红 | (0.80, 0.10, 0.10) | [录] 红色键 |
| display 荧光绿 | (0.30, 0.80, 0.55) | VFD 显示窗荧光色 |
| black 黑 | (0.05, 0.05, 0.06) | 按键 / 盘口 / 机脚 / 线缆 |
| metal 金属银 | (0.72, 0.74, 0.78) | 金属件 / 接口 / 散热片 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/whole.gltf | whole |
| assemblies/cassette_mechanism.gltf | cassette_mechanism |
| assemblies/head_drum.gltf | head_drum |
| assemblies/front_panel.gltf | front_panel |
| assemblies/power_supply.gltf | power_supply |
| assemblies/mainboard.gltf | mainboard |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `15_VHS录像机预研卡.md`（家用 VHS 录像机约 430×280×95 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 15 号预研卡部件草图取 6 件（whole + 磁带加载机构/磁头鼓/前面板/电源/主板）；chassis 并入 whole 示意，control_buttons/display/cassette 并入 whole 或 front_panel 示意。
- **head_drum 识别件**：磁头鼓为录像机核心识别件，低模以递减金属银盒近似斜装圆柱；**加载动画的转鼓动作**在后续建模卡以该 node 为旋转轴实现（本卡仅备静态低模）。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）。
