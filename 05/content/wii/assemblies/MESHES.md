# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-310-D：`wii` 低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 5 | 整机：白色竖条主机主体 + 顶盖 + 前面板 + 吸入式入口 + 指示灯 + 按键×2 + 同步口 + 记忆卡口 + 装饰×2 + 机脚×2 |
| disc_drive.gltf | disc_drive | 104 | 156 | 6 | 光驱：银色吸入式 DVD 主体 + 盖 + 前缘 + 光盘 + 转盘 + 轴孔 + 读头 + 导轨 + PCB×2 + IC×2 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + Broadway CPU/Hollywood GPU/内存 IC×4 + 电容×3 + 接口×2 + 散热片×2 |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖/侧板 + 开关 + 线缆 + PCB + IC + 指示灯 + 端子×3 |
| controller_port.gltf | controller_port | 104 | 156 | 6 | 手柄接口：黑色同步口座 + 前框 + 触点×4 + 面板 + 插头示意×2 + PCB + IC |
| wii_remote.gltf | wii_remote | 104 | 156 | 6 | Wii Remote：白色体感遥控器主体 + 尾盖 + A 键 + 十字键 + 方向键×2 + 面板×2 + 接口 + IC + 红外窗 |
| nunchuk.gltf | nunchuk | 104 | 156 | 6 | Nunchuk：白色副柄主体 + 底盖 + 摇杆 + C/Z 键 + 面板×3 + 接口 + IC + 线缆 |
| sensor_bar.gltf | sensor_bar | 104 | 156 | 5 | 感应条：黑色长条主体 + 顶盖 + 红外窗×2 + 面板×2 + 接口×4 + PCB + IC×2 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 白 | (0.92, 0.92, 0.92) | 主机/遥控器/副柄白色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 前面板 / 面板 / 散热片 |
| dvd 银光驱 | (0.70, 0.72, 0.75) | 吸入式 DVD 光驱 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | Broadway/Hollywood/内存/IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 |
| black 黑 | (0.05, 0.05, 0.06) | 插口 / 红外窗 / 线缆 |
| button 按键黑 | (0.20, 0.20, 0.22) | 十字键 / A 键 / C/Z 键 |
| blue_led 指示灯蓝 | (0.20, 0.40, 0.80) | 光盘吸入指示灯 |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 接口 / 端子 |
| disc 光盘银 | (0.65, 0.70, 0.72) | DVD 反光面 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/disc_drive.gltf | disc_drive |
| assemblies/mainboard.gltf | mainboard |
| assemblies/power_supply.gltf | power_supply |
| assemblies/controller_port.gltf | controller_port |
| assemblies/wii_remote.gltf | wii_remote |
| assemblies/nunchuk.gltf | nunchuk |
| assemblies/sensor_bar.gltf | sensor_bar |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `42_Wii低模样板预研卡.md`（Wii 约 44×157×215 mm 竖放公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **disc_drive 吸入式光盘识别件**：DVD 光驱为可吸入识别件，**光盘吸入动画**以该 node 为抽拉轴实现。
  - **wii_remote 体感手柄识别件**：体感遥控器为可选识别件，可作「挥动手臂」示意。
- **Wii BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
