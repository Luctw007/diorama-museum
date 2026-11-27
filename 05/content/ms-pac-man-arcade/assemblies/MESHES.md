# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-325-D：`ms-pac-man-arcade` 街机框体低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包已建 meta.json / annotations / 目录 jsonl（完整产包）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| cabinet.gltf | cabinet | 120 | 180 | 3 | 框体：粉色立式框体主体 + 黑色饰板/侧板 + 深灰面板区 |
| control_panel.gltf | control_panel | 104 | 156 | 5 | 控制面板：黑色面板 + 深灰面板 + 白色件 + 绿色 PCB + IC |
| coin_door.gltf | coin_door | 104 | 156 | 5 | 投币门：黑色投币门 + 深灰面板 + 金属灰件 + 绿色 PCB + IC |
| crt_display.gltf | crt_display | 104 | 156 | 6 | 显示器：玻璃屏（关机态）+ 黑色主体 + 深灰面板 + PCB + IC + 金属灰件 |
| joystick.gltf | joystick | 104 | 156 | 5 | 摇杆：金属灰轴 + 红色摇杆球 + 黑色底座 + 深灰面板 + IC |
| button.gltf | button | 104 | 156 | 6 | 按键：白色键帽 + 黑色按键座 + 金属灰件 + 深灰面板 + PCB + IC |
| mainboard.gltf | mainboard | 104 | 156 | 4 | 主板：绿色 PCB + 芯片 IC + 黑色件 + 深灰面板 |
| speaker.gltf | speaker | 104 | 156 | 5 | 扬声器：深灰网罩 + 金属灰件 + 黑色主体 + IC + PCB |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 粉 | (0.85, 0.30, 0.60) | Ms. Pac-Man 标志性粉色框体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 控制面板 / 投币门 / 面板 |
| glass 玻璃 | (0.10, 0.12, 0.16) | CRT 屏幕（关机态） |
| black 黑 | (0.05, 0.05, 0.06) | 侧板 / 饰板 / 底座 / 按键座 |
| pcb 绿 | (0.08, 0.25, 0.12) | 主板 / 电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 芯片 / IC |
| psu 金属灰 | (0.60, 0.62, 0.65) | 电源 / 金属件 / 轴 / 投币门金属件 |
| white 白 | (0.90, 0.90, 0.90) | 按键 / 白色件 |
| marquee 灯箱紫 | (0.10, 0.05, 0.12) | 灯箱 / 招牌（预留，本批 gltf 未单独使用） |
| red 摇杆红 | (0.85, 0.20, 0.25) | 摇杆球 |

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
- **尺寸比例**：Ms. Pac-Man 框体约 0.6×0.8×1.8 m 公开近似值，正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **coin_door 投币门识别件**：投币门可开合，投币文化是街机厅的仪式感来源。
  - **joystick 四向摇杆识别件**：四向摇杆是 Ms. Pac-Man 框体标志性操作件，可作「四向移动」示意。
  - **button 按键识别件**：按键为方向/确认输入件，可作按压示意。
- **街机 ROM/BIOS 红线（FR-E3）**：本包仅低模网格 + 原创文案，不含 ROM/BIOS/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
