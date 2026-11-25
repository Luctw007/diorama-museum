# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-320-F：`nintendo-3ds` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 3 | 机身：蓝色翻盖式掌机机身 + 上盖 + 铰链×2 + 内框×2 + 麦克风 + 扬声器口×2 + Start/Select + 电源键 + 挂绳孔 + 铭牌 + 机脚 |
| top_screen.gltf | top_screen | 104 | 156 | 5 | 上屏：裸眼 3D 上屏玻璃 + 边框 + 外框 + 背板 + 铰链座 + 扬声器×2 + 排线 + PCB + IC + 电容×2 |
| touch_screen.gltf | touch_screen | 104 | 156 | 5 | 下触屏：触屏玻璃 + 边框 + 外框 + 触控层 + 背板 + 排线 + PCB + IC + 电容×2 + 触控笔槽 + 支架 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 5 | 卡带槽：3DS 卡带槽主体 + 外框 + 触点×6 + PCB + IC + 电容 + 盖板 + 底座 |
| shoulder_buttons.gltf | shoulder_buttons | 104 | 156 | 6 | 肩键区：L/R 肩键 + 弹簧×2 + 微动开关×2 + PCB×2 + 支架×2 + 电容×2 + 排线 |
| battery_compartment.gltf | battery_compartment | 104 | 156 | 5 | 电池仓：电池仓体 + 仓盖 + 触点×2 + 卡扣 + 弹簧 + PCB + IC + 电容 + 排线 + 侧壁×2 + 底板 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 机身蓝 | (0.16, 0.42, 0.66) | 3DS 蓝色塑料主体 / 上盖 / 电池仓盖 |
| panel 深灰 | (0.25, 0.25, 0.28) | 内框 / 边框 / 支架 / 盖板 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | 上屏 / 下触屏玻璃（关机态） |
| black 黑 | (0.05, 0.05, 0.06) | 卡带槽 / 插口 / 铰链 / 排线 |
| pcb 绿 PCB | (0.08, 0.25, 0.12) | 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | IC / 微动开关 / 电容 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 触点 / 弹簧 |
| btn 按键黑 | (0.20, 0.20, 0.22) | L/R 肩键 / Start/Select |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/top_screen.gltf | top_screen |
| assemblies/touch_screen.gltf | touch_screen |
| assemblies/cartridge_slot.gltf | cartridge_slot |
| assemblies/shoulder_buttons.gltf | shoulder_buttons |
| assemblies/battery_compartment.gltf | battery_compartment |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面（几何沿用 NDS 掌机低模体例，换 3DS 蓝色配色）。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `26_3DS与PSVita掌机低模样板预研卡.md`（3DS 约 134×21×74 mm 合盖公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **top_screen 裸眼 3D 上屏识别件**：上屏为裸眼 3D 屏，是 3DS 的标志性识别件。
  - **touch_screen 下触屏识别件**：下屏触控，可作「触控笔点击」示意。
  - **cartridge_slot 3DS 卡带槽识别件**：卡带槽为可插拔识别件，**卡带插拔动画**以该 node 为插拔轴实现。
- **3DS BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
