# MESHES.md — 网格清单与制作口径（低模）

> TASK-315-O：`nintendo-ds` 低模 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；识别件标注 touch_screen / cartridge_slot / chassis。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 5 | 翻盖机身：银色双屏掌机主体 + 上盖 + 面板×2 + 按键区（十字键/ABXY/开始选择）+ 肩键 + 卡带口 + 机脚 |
| top_screen.gltf | top_screen | 104 | 156 | 6 | 上屏：屏幕黑玻璃 + 面板边框 + 银色外框 + 背板 + PCB + IC×3 |
| touch_screen.gltf | touch_screen | 104 | 156 | 6 | 下触屏：屏幕黑玻璃 + 面板边框 + 银色外框 + 触控面板 + PCB + IC×3 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 5 | 卡带槽：黑色卡带座 + 面板 + 金属触点×6 + PCB + IC×2 |
| shoulder_buttons.gltf | shoulder_buttons | 104 | 156 | 6 | 肩键区：L/R 按键黑肩键 + 金属垫片 + PCB×2 + IC×4 + 横梁 |
| battery_compartment.gltf | battery_compartment | 104 | 156 | 6 | 电池仓：银色仓盖 + 面板 + 金属触点×2 + 负极簧片 + PCB + IC×2 + 侧板×2 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 银 | (0.75, 0.77, 0.80) | 掌机银色塑料主体 / 屏幕外框 / 电池仓盖 |
| panel 深灰 | (0.25, 0.25, 0.28) | 按键区 / 面板 / 边框 / 侧板 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | 上下屏玻璃（关机态） |
| black 黑 | (0.05, 0.05, 0.06) | 卡带槽 / 卡带口 / 负极簧片 |
| pcb 绿 | (0.08, 0.25, 0.12) | 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 主处理器 / IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 卡带触点 / 电池触点 / 金属垫片 |
| btn 按键黑 | (0.20, 0.20, 0.22) | 十字键 / ABXY / L/R 肩键 |

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

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `23_NDS与PSP掌机低模样板预研卡.md`（NDS 约 149×29×85 mm 合盖公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **touch_screen 下屏触控识别件**：下触屏为标志性识别件，可作「触控笔点击/滑动」示意。
  - **cartridge_slot 卡带插拔识别件**：卡带槽为可插拔识别件，**卡带插拔动画**以该 node 为插拔轴实现。
  - **chassis 翻盖开合识别件**：机身翻盖形态，**翻盖开合动画**以铰链为轴实现。
- **NDS BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
