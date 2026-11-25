# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-310-R：`pac-man-arcade` 街机框体低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包已建 meta.json / annotations / 目录 jsonl（完整产包）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| cabinet.gltf | cabinet | 120 | 180 | 4 | 框体：黄色立式框体主体 + 顶盖 + 侧板 + 控制面板区 + 投币门 + 灯箱 + 边饰×2 + 底台×3 |
| control_panel.gltf | control_panel | 104 | 156 | 5 | 控制面板：黑色面板 + 顶盖 + 前缘 + 接口×2 + 面板×2 + 装饰×2 + PCB + IC |
| coin_door.gltf | coin_door | 104 | 156 | 5 | 投币门：黑色投币门 + 顶盖 + 投币口 + 指示灯 + 面板×2 + 装饰×2 + PCB + IC + 接口×2 |
| crt_display.gltf | crt_display | 104 | 156 | 6 | 显示器：黑色 CRT 主体 + 顶盖 + 屏幕 + 面板×2 + 接口 + PCB + IC×2 + 散热×2 + 边框×2 |
| joystick.gltf | joystick | 104 | 156 | 6 | 摇杆：黑色底座 + 顶盖 + 红色摇杆球×2 + 金属轴×2 + 面板×2 + PCB + IC + 红球芯 |
| button.gltf | button | 104 | 156 | 6 | 按键：黑色按键 + 顶盖 + 键帽 + 金属轴 + 面板×2 + PCB + IC + 按键座 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿色 PCB + 子板 + 芯片×4 + 电容×3 + 接口×2 + 散热片×2 |
| speaker.gltf | speaker | 112 | 168 | 6 | 扬声器：扬声器主体 + 顶盖 + 前后网罩×2 + 螺丝×4 + 面板×2 + IC + PCB + 面板×2 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| cabinet 黄 | (0.95, 0.80, 0.10) | Pac-Man 标志性黄色框体 |
| panel 黑 | (0.05, 0.05, 0.06) | 控制面板 / 投币门 / 面板 |
| black 黑 | (0.05, 0.05, 0.06) | 侧板 / 灯箱 / 边饰 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 芯片 / IC |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 接口 / 螺丝 / 轴 |
| red 摇杆红 | (0.90, 0.20, 0.20) | 摇杆球 |
| button 按键黑 | (0.20, 0.20, 0.22) | 按键 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | CRT 屏幕（关机态） |
| speaker 扬声器黑 | (0.10, 0.10, 0.12) | 扬声器主体 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/cabinet.gltf | cabinet |
| assemblies/control_panel.gltf | control_panel |
| assemblies/coin_door.gltf | coin_door |
| assemblies/crt_display.gltf | crt_display |
| assemblies/joystick.gltf | joystick |
| assemblies/button.gltf | button |
| assemblies/mainboard.gltf | mainboard |
| assemblies/speaker.gltf | speaker |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：Pac-Man 框体约 640×610×1720 mm 公开近似值，正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **coin_door 投币门识别件**：投币门可开合，投币文化是街机厅的仪式感来源。
  - **joystick 摇杆识别件**：红色摇杆球是 Pac-Man 框体标志性操作件，可作「方向操作」示意。
- **街机 ROM/BIOS 红线（FR-E3）**：本包仅低模网格 + 原创文案，不含 ROM/BIOS/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
