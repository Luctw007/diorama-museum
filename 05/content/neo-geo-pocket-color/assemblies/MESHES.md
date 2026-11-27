# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-325-M：`neo-geo-pocket-color` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 4 | 机身：银色竖版掌机机身 + 顶盖/底盖 + 前面板 + 屏幕凹区 + 扬声器口 + 电源开关 + 联机口 + 音量键 + Option 键 + 机脚×2 |
| screen_module.gltf | screen_module | 104 | 156 | 6 | 屏幕模组：彩色液晶屏玻璃 + 边框 + 外框 + 背光板 + 排线口 + PCB + IC + 电容×2 + 排线接口 + 支架×2 |
| d_pad.gltf | d_pad | 104 | 156 | 6 | 摇杆状十字键：NGPC 特有 clicky 微动摇杆式 d_pad + 键座 + PCB + 微动开关×4 + 橡胶垫 + 支架 + 电容×2 |
| buttons.gltf | buttons | 104 | 156 | 5 | 按键区：A/B 主键 + Option 键 + 键座 + PCB + 微动开关×3 + 橡胶垫 + 侧条 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 5 | 卡带槽：NGPC 卡带槽主体 + 外框 + 触点×6 + PCB + IC + 电容 + 盖板 + 底座 |
| battery_compartment.gltf | battery_compartment | 104 | 156 | 5 | 电池仓：电池仓体 + 仓盖 + 触点×2 + 卡扣 + 弹簧 + PCB + IC + 电容 + 排线 + 侧壁×2 + 底板 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 机身银 | (0.75, 0.77, 0.80) | NGPC 银色塑料主体 / 仓盖 |
| panel 深灰 | (0.25, 0.25, 0.28) | 面板 / 支架 / 盖板 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | 彩色液晶屏玻璃（关机态） |
| black 黑 | (0.05, 0.05, 0.06) | 卡带槽 / 插口 / 键座 |
| pcb 绿 PCB | (0.08, 0.25, 0.12) | 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | IC / 微动开关 / 电容 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 触点 / 弹簧 |
| btn 按键黑 | (0.20, 0.20, 0.22) | 摇杆状 d_pad / A/B 键 / Option |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/screen_module.gltf | screen_module |
| assemblies/d_pad.gltf | d_pad |
| assemblies/buttons.gltf | buttons |
| assemblies/cartridge_slot.gltf | cartridge_slot |
| assemblies/battery_compartment.gltf | battery_compartment |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面（几何沿用 325-J GBC 低模体例，换 NGPC 银色配色）。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `30_GBC与NGPC掌机低模样板预研合卡.md`（NGPC 约 75×25×130 mm 竖版公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **d_pad 摇杆状十字键识别件**：NGPC 特有的 clicky 微动摇杆式 d_pad，为标志性识别件，可作「八方向微动按压」示意。
  - **buttons A/B 键识别件**：A/B 主键为可按压识别件。
  - **cartridge_slot 卡带槽识别件**：卡带槽为可插拔识别件，**卡带插拔动画**以该 node 为插拔轴实现。
  - **screen_module 屏幕模组识别件**：彩色液晶屏是 NGPC 相对 NG 黑白初代的标志性升级。
- **NGPC BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
