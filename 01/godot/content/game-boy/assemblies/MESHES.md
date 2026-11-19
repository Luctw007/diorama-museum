# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-195-A：6 个占位盒（各 8 顶点 / 12 三角面）已重制为**低模样板**（多材质分色、程序化几何）。
> 节点名 = node_id（R-090 契约），mesh_ref 不变；meta.json / annotations **未改动**。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| front_shell.gltf | front_shell | 112 | 168 | 4 | 灰白前壳 + 屏窗 + 按键区面板 + 十字键/AB/START/SELECT 键位 + 卡带槽口 + 顶部格栅 |
| back_shell.gltf | back_shell | 104 | 156 | 5 | 灰白后壳 + 电池仓×2 + 卡带仓 + 铭牌 + 机脚×4 + 联机口触点 + 通风孔 |
| mainboard.gltf | mainboard | 176 | 264 | 3 | 绿基板 + LR35902 CPU + 其它 IC + 屏接口/卡带槽触点 |
| screen_module.gltf | screen_module | 112 | 168 | 5 | 黄绿点阵屏 + 屏框 + 屏背板 + 排线触点 + 保护玻璃 + 排线接头 |
| dpad_module.gltf | dpad_module | 112 | 168 | 3 | 十字键（四臂+中心）+ A/B + START/SELECT + 按键底座 + 导电胶触点 |
| cartridge.gltf | cartridge | 120 | 180 | 4 | 深灰卡带壳 + 绿 PCB + 底部金手指（双面）+ ROM |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| gray 灰白 | (0.78, 0.78, 0.76) | 前/后壳机身 |
| darkgray 深灰 | (0.35, 0.35, 0.38) | 按键区面板 / 屏框 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板基板 / 卡带 PCB |
| lcd 黄绿 LCD | (0.55, 0.65, 0.30) | 点阵屏 |
| black 芯片黑 | (0.05, 0.05, 0.05) | 芯片 / ROM / 触点 |
| key 深灰按键 | (0.30, 0.30, 0.32) | 十字键 / AB / START/SELECT / 卡带壳 |
| gold 金手指金 | (0.85, 0.70, 0.20) | 卡带金手指 / 接口触点 |

## 与 node_id 对应表

| mesh_ref | node_id | 装配体（meta.json） |
|---|---|---|
| assemblies/front_shell.gltf | front_shell | front_shell |
| assemblies/back_shell.gltf | back_shell | back_shell |
| assemblies/mainboard.gltf | mainboard | mainboard |
| assemblies/screen_module.gltf | screen_module | screen_module |
| assemblies/dpad_module.gltf | dpad_module | dpad_module |
| assemblies/cartridge.gltf | cartridge | cartridge |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（transform 语义保持，未改装配体树）。
- **尺寸比例**：沿用占位盒 MESHES.md（GB DMG-01 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **面板布局**：十字方向键 + A/B 键 + START/SELECT + 屏幕 + 卡带槽 + 电源开关/音量旋钮/耳机孔/联机线口（低模以壳体开孔/触点示意，细节纹理留待纹理建模卡 07_GB_建模任务卡 还原）。
- **点阵屏**：屏模组为 160×144 点阵、4 级灰度，低模以黄绿纯色示意，像素级网格/纹理在纹理建模卡还原。
- 校验：`verify_all.py --only pkg:game-boy` → 84 PASS / 0 FAIL；`--only catalog_ref` → FAIL 0。
