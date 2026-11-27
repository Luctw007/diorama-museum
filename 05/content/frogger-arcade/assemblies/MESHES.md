# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-325-C：`frogger-arcade` 街机框体低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包已建 meta.json / annotations / 目录 jsonl（完整产包）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| cabinet.gltf | cabinet | 120 | 180 | 3 | 框体：绿色立式机箱主体 + 顶盖 + 灯箱 + 灯箱面 + 面板×2 + 前门×2 + 侧板×2 + 底台 + 机脚×2 + 内部 |
| control_panel.gltf | control_panel | 104 | 156 | 5 | 控制面板：黑色面板 + 顶盖 + 前缘 + 按键位 + 键帽 + 面板 + PCB + IC×2 + 侧板×2 |
| coin_door.gltf | coin_door | 104 | 156 | 5 | 投币门：黑色投币门 + 顶盖 + 投币口 + 指示灯 + 侧框×2 + 内部×3 + PCB + IC×2 + 门扣 |
| crt_display.gltf | crt_display | 104 | 156 | 6 | 显示器：屏幕玻璃 + 黑色 CRT 主体 + 屏面 + 面板×3 + PCB + IC×3 + 侧框×2 + 颈管 |
| joystick.gltf | joystick | 104 | 156 | 5 | 摇杆：红色摇杆球 + 金属轴×3 + 黑色底座 + 面板×2 + IC×5 + 底芯 |
| button.gltf | button | 104 | 156 | 6 | 按键：白色键帽 + 按键座 + 金属轴 + 面板 + PCB + IC + 触点 |
| mainboard.gltf | mainboard | 104 | 156 | 4 | 主板：绿色 PCB + 芯片×9 + 接口 + 面板×2 |
| speaker.gltf | speaker | 104 | 156 | 5 | 扬声器：扬声器主体 + 金属后壳 + 前后网罩×2 + 边条 + 螺丝 + 磁芯 + PCB + 面板 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 绿 | (0.06, 0.35, 0.10) | 框体机箱主体 / 底台 |
| panel 深灰 | (0.25, 0.25, 0.28) | 控制面板 / 投币门 / 前面板 / 侧板 |
| glass 屏幕玻璃 | (0.10, 0.12, 0.16) | CRT 屏幕玻璃（关机态） |
| black 黑 | (0.05, 0.05, 0.06) | 灯箱 / 前门 / 侧框 / 网罩 / 底座 |
| pcb 绿 | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 芯片 / IC / 磁芯 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 金属轴 / 后壳 / 内部机构 |
| white 白 | (0.90, 0.90, 0.90) | 键帽 / 按键位 |
| marquee 灯箱 | (0.05, 0.08, 0.05) | 顶部灯箱（标题招牌，绿色近似） |
| red 红 | (0.65, 0.08, 0.08) | 摇杆球 / 标志性操作件 |

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
- **尺寸比例**：Frogger 框体公开近似尺寸，正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **coin_door 投币门识别件**：投币门可开合，投币文化是街机厅的仪式感来源，对应「投币开合动画」。
  - **joystick 四向摇杆识别件**：四向摇杆控制青蛙上下左右移动，红色摇杆球是 Frogger 框体标志性操作件，可作「四向移动演示」示意。
  - **button 方向/跳跃键识别件**：按键配合摇杆完成方向输入与跳跃确认，可作「按压」示意。
- **街机 ROM/BIOS 红线（FR-E3）**：Frogger 基板 ROM 不入库、不下载，本包仅低模网格 + 原创文案，不含 ROM/BIOS/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
