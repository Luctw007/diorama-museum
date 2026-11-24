# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-305-E：`xbox` 低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 5 | 整机：黑色方块主机主体 + 顶盖 + 前面板 + 光驱托盘 + 电源环 + 按键×2 + 手柄口×4 + 机脚×2 |
| dvd_drive.gltf | dvd_drive | 104 | 156 | 6 | 光驱：黑色托盘弹出式 DVD 主体 + 盖 + 托盘 + 光盘 + 转盘 + 轴孔 + 读头 + 导轨 + PCB×2 + IC×2 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + Pentium III 级 CPU/NVIDIA GPU/内存 IC×4 + 电容×3 + 接口×2 + 散热片×2 |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖/侧板 + 开关 + 线缆 + PCB + IC + 指示灯 + 端子×3 + 散热片 |
| controller_port.gltf | controller_port | 104 | 156 | 6 | 手柄接口：黑色接口座 + 前框 + 触点×4 + 面板 + 插头示意×2 + PCB + IC |
| hard_drive.gltf | hard_drive | 104 | 156 | 6 | 硬盘仓：黑色硬盘仓 + 盖 + 前缘 + 接口×4 + 面板×2 + 硬盘示意×2 + PCB + IC |
| controller.gltf | controller | 104 | 156 | 6 | 手柄：黑色主体 + 两握把 + 按键×2 + 十字键 + 模拟摇杆×2 + 面板×2 + 接口 + IC + 电源环 |
| ethernet_port.gltf | ethernet_port | 104 | 156 | 5 | 以太网接口：黑色接口座 + 前框 + 后座 + 触点×4 + 面板×2 + 网线 + PCB + IC×2 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 黑 | (0.10, 0.10, 0.12) | 主机/手柄黑色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 前面板 / 接口面板 / 散热片 |
| dvd 黑光驱 | (0.08, 0.08, 0.10) | 托盘弹出式 DVD 光驱 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | Pentium III 级/NVIDIA/内存/IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 |
| black 黑 | (0.05, 0.05, 0.06) | 插口 / 线缆 / 电容 / 网线 |
| hard 硬盘黑 | (0.08, 0.08, 0.10) | 内置硬盘仓 |
| button 按键黑 | (0.20, 0.20, 0.22) | 十字键 / 按键 |
| green_led 指示灯绿 | (0.30, 0.70, 0.30) | 电源环指示灯 |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 接口 / 散热片 / 端子 |
| disc 光盘银 | (0.65, 0.70, 0.72) | DVD 反光面 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/dvd_drive.gltf | dvd_drive |
| assemblies/mainboard.gltf | mainboard |
| assemblies/power_supply.gltf | power_supply |
| assemblies/controller_port.gltf | controller_port |
| assemblies/hard_drive.gltf | hard_drive |
| assemblies/controller.gltf | controller |
| assemblies/ethernet_port.gltf | ethernet_port |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `39_Xbox低模样板预研卡.md`（Xbox 约 320×100×260 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 39 号预研卡部件草图取 8 件（chassis + 光驱/主板/电源/手柄接口/硬盘仓/手柄/以太网接口），全部单独成件。
- **识别件**：
  - **dvd_drive 托盘弹出识别件**：DVD 光驱托盘为可弹出识别件，低模以黑色盒 + 光盘示意；**托盘弹出动画**在后续建模卡以该 node 为抽拉轴实现。
  - **controller 手柄识别件**：Xbox 手柄为可选识别件，含双模拟摇杆。
- **Xbox BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
