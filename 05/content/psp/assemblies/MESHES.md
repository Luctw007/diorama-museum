# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-315-Q：`psp` 低模 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包含 meta.json / annotations / 目录由统筹回填。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 3 | 整机：黑色横置宽屏主机主体 + 顶盖 + 底盖 + 前后面板 + 按键孔位 + 扬声器孔 |
| screen.gltf | screen | 104 | 156 | 7 | 屏幕：宽屏玻璃 + 屏幕边框 + 面板 + PCB + 驱动 IC + 扬声器孔 |
| umd_drive.gltf | umd_drive | 104 | 156 | 6 | UMD 光盘仓：金属银灰仓体 + 仓盖 + 光盘 + 电机 IC + PCB + 读取头 |
| control_buttons.gltf | control_buttons | 104 | 156 | 4 | 按键区：十字键 + △○×□ 键 + 摇杆 + PCB + 控制 IC |
| shoulder_buttons.gltf | shoulder_buttons | 104 | 156 | 6 | 肩键区：L/R 肩键 + 金属触点 + PCB + 控制 IC + 按键底座 |
| battery_compartment.gltf | battery_compartment | 104 | 156 | 6 | 电池仓：仓体 + 仓盖 + 触点 + PCB + 供电 IC + 电池示意 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 黑 | (0.05, 0.05, 0.06) | 主机/屏幕/电池仓黑色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 前面板 / 面板 / 仓盖 / 按键底座 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | 宽屏玻璃（关机态） |
| frame 边框 | (0.15, 0.15, 0.17) | 屏幕边框 |
| black 黑 | (0.05, 0.05, 0.06) | 按键孔位 / 扬声器孔 / 读取头 |
| pcb 绿 | (0.08, 0.25, 0.12) | 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 控制 IC / 供电 IC / 电机 IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | UMD 仓金属件 / 肩键触点 / 电池触点 |
| btn 按键黑 | (0.20, 0.20, 0.22) | 十字键 / △○×□ 键 / L/R 肩键 |
| dvd 光盘银 | (0.70, 0.72, 0.75) | UMD 光盘反光面 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/screen.gltf | screen |
| assemblies/umd_drive.gltf | umd_drive |
| assemblies/control_buttons.gltf | control_buttons |
| assemblies/shoulder_buttons.gltf | shoulder_buttons |
| assemblies/battery_compartment.gltf | battery_compartment |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `23_NDS与PSP掌机低模样板预研卡.md`（PSP-1000 约 170×23×74 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **umd_drive UMD 光盘仓识别件**：UMD 光盘仓为可开合识别件，**UMD 仓开合动画**以该 node 为开合轴实现。
  - **chassis 横置宽屏握持识别件**：机身（chassis）为横置宽屏掌机形态，十字键左、△○×□ 右的布局是 PSP 操作特色。
- **PSP BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
