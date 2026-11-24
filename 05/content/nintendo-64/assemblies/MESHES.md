# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-270-A：`nintendo-64` 低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 5 | 整机：深灰主机主体 + 顶盖 + 前面板 + 卡带槽 + 电源灯 + 按键×4 + 手柄口×4 + 机脚×2 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 5 | 卡带槽：黑色插槽座 + 顶沿 + 前缘 + 触点×4 + 面板 + PCB×2 + IC×2 |
| cartridge.gltf | cartridge | 104 | 156 | 5 | 卡带：深灰卡带壳 + 顶沿 + 标签 + 底沿/槽口×3 + 金手指×4 + 内部 PCB + ROM 芯片×2 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + R4300i CPU/RCP 图形芯片/内存 IC×4 + 电容×3 + 接口×2 + 散热片×2 |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖/侧板 + 开关 + 线缆 + PCB + IC + 指示灯 + 散热片 + 端子×3 |
| controller_port.gltf | controller_port | 104 | 156 | 6 | 手柄接口：黑色接口座 + 前框 + 触点×4 + 面板 + 插头示意×2 + PCB + IC |
| expansion_slot.gltf | expansion_slot | 104 | 156 | 5 | 扩展槽：黑色端口座 + 前框 + 触点×4 + 面板 + PCB×2 + IC×2 |
| controller.gltf | controller | 104 | 156 | 5 | 手柄：三叉戟主体 + 两握把 + 模拟摇杆×2 + 按键×4 + 面板×2 + IC×2 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 深灰 | (0.20, 0.20, 0.22) | 主机深灰塑料主体 |
| panel 深灰 | (0.30, 0.30, 0.32) | 前面板 / 接口面板 |
| black 黑 | (0.05, 0.05, 0.06) | 按键 / 插口 / 卡槽 / 线缆 / 电容 |
| controller 深灰 | (0.30, 0.30, 0.32) | 卡带壳 / 手柄主体 / 散热片 |
| stick 摇杆灰 | (0.40, 0.40, 0.42) | 模拟摇杆 |
| red_led 指示灯红 | (0.90, 0.20, 0.10) | 电源指示灯 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | R4300i/RCP/内存/ROM 芯片 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 金手指 / 接口 / 散热片 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/cartridge_slot.gltf | cartridge_slot |
| assemblies/cartridge.gltf | cartridge |
| assemblies/mainboard.gltf | mainboard |
| assemblies/power_supply.gltf | power_supply |
| assemblies/controller_port.gltf | controller_port |
| assemblies/expansion_slot.gltf | expansion_slot |
| assemblies/controller.gltf | controller |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `26_N64低模样板预研卡.md`（N64 约 260×73×190 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 26 号预研卡部件草图取 8 件（chassis + 卡带槽/卡带/主板/电源/手柄接口/扩展槽/手柄），全部单独成件（对齐 26 号拆分方案，与 Saturn/PS 的 6 件口径不同）。
- **识别件**：
  - **cartridge / cartridge_slot 插拔识别件**：卡带与卡带槽为插拔识别件，低模以深灰盒 + 金手指示意；**卡带插拔动画**在后续建模卡以该 node 为插拔轴实现。
  - **controller 模拟摇杆识别件**：三叉戟手柄为可选识别件，模拟摇杆（stick 材质）为 3D 平台操作的关键。
- **N64 BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）。
