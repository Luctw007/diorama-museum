# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-320-I：`psvita` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 3 | 机身：黑色横置掌机机身 + 顶盖/底盖 + 前后面板 + 铭牌 + 扬声器×2 + Start/Select + Home + 电源键 + 挂绳孔 + 机脚×2 + 饰条 |
| screen.gltf | screen | 104 | 156 | 6 | 屏幕：5 英寸 OLED 屏玻璃 + 边框 + 外框 + 机身框 + 触控层 + PCB + IC + 电容×2 + 排线接口 + 支架×2 + 背光板 |
| rear_touchpad.gltf | rear_touchpad | 104 | 156 | 4 | 背触板：背部触控板 + 边框 + 侧条×2 + 排线接口 + PCB + IC + 电容×2 + 接口 + 盖板 + 芯片 + 排线 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 5 | 卡带槽：PSVita 专用卡带槽主体 + 外框 + 触点×6 + PCB + IC + 电容 + 盖板 + 底座 |
| control_buttons.gltf | control_buttons | 104 | 156 | 4 | 按键区：十字键 + △○×□ + 左摇杆 + 右摇杆 + 摇杆座 + PCB + IC + 电容×2 + 支架 + 按键橡胶垫 |
| shoulder_buttons.gltf | shoulder_buttons | 104 | 156 | 6 | 肩键区：L/R 肩键 + 弹簧×2 + 微动开关×2 + PCB×2 + 支架×2 + 电容×2 + 排线 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 机身黑 | (0.08, 0.08, 0.09) | PSVita 黑色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 面板 / 支架 / 盖板 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | OLED 屏玻璃（关机态） |
| frame 边框 | (0.15, 0.15, 0.17) | 屏幕边框 |
| black 黑 | (0.05, 0.05, 0.06) | 卡带槽 / 插口 / 排线 |
| pcb 绿 PCB | (0.08, 0.25, 0.12) | 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | IC / 微动开关 / 电容 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 触点 / 弹簧 |
| btn 按键黑 | (0.20, 0.20, 0.22) | 十字键 / △○×□ / 摇杆 / 肩键 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/screen.gltf | screen |
| assemblies/rear_touchpad.gltf | rear_touchpad |
| assemblies/cartridge_slot.gltf | cartridge_slot |
| assemblies/control_buttons.gltf | control_buttons |
| assemblies/shoulder_buttons.gltf | shoulder_buttons |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面（几何沿用 PSP 掌机低模体例，补 rear_touchpad/cartridge_slot）。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `26_3DS与PSVita掌机低模样板预研卡.md`（PSVita 约 182×18.6×83.5 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **rear_touchpad 背触板识别件**：背部触控板是 PSVita 的标志性识别件，可作「背触滑动」示意。
  - **control_buttons 双摇杆 + △○×□ 识别件**：左右双摇杆 + 索尼四键布局是 PSVita 操作特色。
  - **cartridge_slot PSVita 卡带槽识别件**：卡带槽为可插拔识别件，**卡带插拔动画**以该 node 为插拔轴实现。
- **PSVita BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
