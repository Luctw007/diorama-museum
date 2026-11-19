# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-190-A：6 个占位盒（各 8 顶点 / 12 三角面）已重制为**低模样板**（多材质分色、程序化几何）。
> 节点名 = node_id（R-090 契约），mesh_ref 不变；meta.json / annotations **未改动**。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| top_shell.gltf | top_shell | 136 | 204 | 2 | 木纹主体 + 顶面木纹贴面 + 顶部前缘开关孔×6 + 前面板斜槽/格栅（深色条示意） |
| bottom_shell.gltf | bottom_shell | 112 | 168 | 3 | 米黄底壳 + 机脚×4 + 铭牌位 + 底部通风槽×6 + 接口屏蔽×2 |
| switch_panel.gltf | switch_panel | 112 | 168 | 3 | 黑色面板 + 六开关拨杆/底座（金属银）+ 电源指示灯（红） |
| mainboard.gltf | mainboard | 184 | 276 | 4 | 绿基板 + 三芯片（6507 居中 / TIA / RIOT）+ 其它 IC + 卡带槽触点 + RF 屏蔽盒 |
| cart_slot.gltf | cart_slot | 200 | 300 | 2 | 黑色插槽座 + 24 针镀金触点（2×12） |
| cartridge.gltf | cartridge | 216 | 324 | 4 | 黑色外壳 + 绿 PCB + 底部 24 针金手指（2×12）+ ROM 芯片 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| wood 木纹棕 | (0.45, 0.30, 0.15) | 上壳顶面木纹 |
| black 黑色塑料 | (0.05, 0.05, 0.06) | 斜槽区/面板/插槽/卡带壳 |
| beige 米黄 | (0.82, 0.80, 0.62) | 底壳 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板基板 / 卡带 PCB |
| chip 芯片黑 | (0.20, 0.18, 0.15) | 芯片 / ROM |
| silver 金属银 | (0.72, 0.74, 0.78) | 开关拨杆 / RF 屏蔽盒 / 接口屏蔽 |
| gold 金手指金 | (0.85, 0.70, 0.20) | 卡带槽触点 / 金手指 |
| red 指示灯红 | (0.90, 0.20, 0.10) | 电源指示灯 |

## 与 node_id 对应表

| mesh_ref | node_id | 装配体（meta.json） |
|---|---|---|
| assemblies/top_shell.gltf | top_shell | top_shell |
| assemblies/bottom_shell.gltf | bottom_shell | bottom_shell |
| assemblies/switch_panel.gltf | switch_panel | switch_panel |
| assemblies/mainboard.gltf | mainboard | mainboard |
| assemblies/cart_slot.gltf | cart_slot | cart_slot |
| assemblies/cartridge.gltf | cartridge | cartridge |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（transform 语义保持，未改装配体树）。
- **尺寸比例**：沿用占位盒 MESHES.md（2600 六开关木纹版公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **面板布局**：六开关顺序（电源/黑白彩色/选择/复位/左难度/右难度）、24 针金手指（2×12）、DB9×2 手柄口、RF 输出口、木纹顶面、前面板斜槽（低模以深色条示意，45° 斜槽纹理在纹理建模卡 06/07 号还原）。
- 校验：`verify_all.py --only pkg:atari-2600` → 128 PASS / 0 FAIL；`--only catalog_ref` → FAIL 0。
