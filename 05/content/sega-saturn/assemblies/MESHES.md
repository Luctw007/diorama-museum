# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-260-A：`sega-saturn` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| whole.gltf | whole | 120 | 180 | 7 | 整机：深灰主机主体 + 顶盖 + 前面板 + 光驱盖 + 光盘 + 电源灯 + 按键×4 + 手柄口×2 + 扩展槽×2 + 机脚 |
| cd_drive.gltf | cd_drive | 104 | 156 | 6 | 光驱：黑色翻盖光驱主体 + 盖 + 前缘 + 光盘 + 转盘 + 轴孔 + 读头 + 铰链 + PCB + IC |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + 双 SH-2 CPU/图形芯片/内存 IC×4 + 电容×3 + 接口×2 + 光驱接口 |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖/侧板 + 开关 + 线缆 + PCB + IC + 指示灯 + 散热片 + 端子×3 |
| controller_port.gltf | controller_port | 104 | 156 | 6 | 手柄接口：黑色接口座 + 前框 + 触点×4 + 面板 + 插头示意×2 + PCB + IC |
| expansion_slot.gltf | expansion_slot | 104 | 156 | 5 | 扩展槽：黑色卡槽座 + 前框 + 触点×4 + 面板 + PCB×2 + IC×2 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 深灰 | (0.20, 0.20, 0.22) | 主机深灰塑料主体 |
| panel 深灰 | (0.30, 0.30, 0.32) | 前面板 / 接口面板 |
| cd 黑 | (0.05, 0.05, 0.06) | 翻盖光驱主体 |
| disc 光盘银 | (0.65, 0.70, 0.72) | CD-ROM 反光面 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 双 SH-2 CPU/图形芯片/内存 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 |
| black 黑 | (0.05, 0.05, 0.06) | 按键 / 插口 / 卡槽 / 线缆 / 电容 |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 铰链 / 接口 / 散热片 |
| controller 深灰 | (0.30, 0.30, 0.32) | 手柄插头示意 |
| button 按键黑 | (0.05, 0.05, 0.06) | 手柄按键（预留） |
| green_led 指示灯绿 | (0.20, 0.60, 0.30) | 电源指示灯 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/whole.gltf | whole |
| assemblies/cd_drive.gltf | cd_drive |
| assemblies/mainboard.gltf | mainboard |
| assemblies/power_supply.gltf | power_supply |
| assemblies/controller_port.gltf | controller_port |
| assemblies/expansion_slot.gltf | expansion_slot |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `24_SegaSaturn低模样板预研卡.md`（Saturn 约 260×83×230 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 24 号预研卡部件草图取 6 件（whole + 光驱/主板/电源/手柄接口/扩展槽）；chassis 并入 whole 示意，disc/controller 并入 whole 示意，不单独成件。
- **cd_drive 识别件**：翻盖式光盘盖为可开合识别件，低模以黑色盒 + 光盘示意；**开盖放碟动画**在后续建模卡以该 node 为开合轴实现（本卡仅备静态低模）。
- **Saturn BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）。
