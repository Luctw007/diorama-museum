# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-310-M：`gba` 低模样板 5 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| chassis.gltf | chassis | 120 | 180 | 4 | 机身：靛紫横置掌机主体 + 顶盖 + 前面板 + 十字键 + AB 键 + 按键小件×2 + 面板×2 + 卡带口 + 握把×2 |
| screen.gltf | screen | 104 | 156 | 6 | 屏幕：屏幕框 + 顶框 + 屏幕玻璃 + 内框 + 面板×2 + IC×2 + PCB + 侧框×2 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 6 | 卡带槽：黑色卡带槽座 + 盖 + 前缘 + 触点×4 + 面板×2 + 卡盖×2 + PCB + IC |
| shoulder_buttons.gltf | shoulder_buttons | 104 | 156 | 6 | 肩键：L/R 肩键座×3 + 键帽×3 + 前缘×3 + 触点×2 + PCB + IC |
| battery_compartment.gltf | battery_compartment | 104 | 156 | 6 | 电池仓：电池仓盖 + 顶盖 + 内腔 + 触点×4 + 卡扣×2 + PCB + IC + 面板×2 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 靛紫 | (0.45, 0.30, 0.55) | 掌机靛紫塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 面板 / 肩键 / 电池仓 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | 屏幕玻璃（关机态） |
| frame 边框 | (0.15, 0.15, 0.17) | 屏幕边框 |
| black 黑 | (0.05, 0.05, 0.06) | 卡带槽 / 内框 / 卡口 |
| button 按键黑 | (0.20, 0.20, 0.22) | 十字键 / AB 键 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | IC |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 接口 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/chassis.gltf | chassis |
| assemblies/screen.gltf | screen |
| assemblies/cartridge_slot.gltf | cartridge_slot |
| assemblies/shoulder_buttons.gltf | shoulder_buttons |
| assemblies/battery_compartment.gltf | battery_compartment |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `20_GBA低模样板预研卡.md`（GBA 约 144×24.5×82 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **cartridge_slot 卡带插拔识别件**：顶部卡带槽为可插拔识别件，**卡带插拔动画**以该 node 为插拔轴实现。
  - **chassis 横置双手握持识别件**：横置机身是掌机标志性形态，十字键左、AB 键右布局。
- **GBA BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：5 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
