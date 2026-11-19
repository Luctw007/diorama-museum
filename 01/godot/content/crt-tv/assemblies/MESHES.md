# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-205-A：`crt-tv` 低模样板 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| whole.gltf | whole | 112 | 168 | 6 | 整机：木壳主体 + 顶盖 + 前面板框 + 屏玻璃 + 显像管颈 + 调台/音量旋钮 + 天线 + 电源开关/网罩/机脚 |
| cabinet.gltf | cabinet | 112 | 168 | 4 | 外壳：木壳主体 + 顶盖 + 左右侧板 + 后盖 + 底座 + 前面板框/装饰条 + 屏玻璃 + 散热孔 + 机脚 |
| crt_tube.gltf | crt_tube | 112 | 168 | 3 | 显像管：屏面玻璃 + 玻壳锥体（8 段递减盒）+ 颈部 + 偏转线圈/电子枪/阳极帽 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + 主芯片/IC×3 + 电容×3 + 散热片/接口×2 + 高压包 |
| tuner_module.gltf | tuner_module | 104 | 156 | 5 | 调谐器：金属屏蔽盒体/盖 + 隔板×2 + 端子 + 内部 PCB + IC×2 + 旋钮轴 |
| control_panel.gltf | control_panel | 104 | 156 | 4 | 控制面板：深棕面板条 + 下沿 + VHF/UHF/音量旋钮及刻度环 + 电源开关/按键 + 电源指示灯 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| wood 木壳棕 | (0.45, 0.32, 0.20) | 机箱木壳主体 / 顶盖 / 侧板 / 后盖 / 底座 |
| darkbrown 深棕 | (0.25, 0.18, 0.10) | 前面板框 / 装饰条 / 控制面板条 |
| glass 玻璃深灰 | (0.10, 0.10, 0.12) | 屏面玻璃 |
| crt_dark 玻壳深灰 | (0.12, 0.13, 0.14) | 显像管玻壳锥体 / 颈部 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板基板 / 调谐器内部 PCB |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 主芯片 / IC / 调谐器内部 IC |
| metal 金属银灰 | (0.65, 0.66, 0.68) | 偏转线圈 / 电子枪 / 散热片 / 接口 / 调谐器屏蔽盒 |
| black 黑塑料 | (0.05, 0.05, 0.06) | 电源开关 / 网罩 / 机脚 / 按键 / 散热孔 / 电容 / 端子 |
| silver 旋钮银 | (0.72, 0.74, 0.78) | 调台 / 音量旋钮 / 刻度环 / 旋钮轴 / 高压包 |
| red 指示灯红 | (0.90, 0.20, 0.10) | 电源指示灯 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/whole.gltf | whole |
| assemblies/cabinet.gltf | cabinet |
| assemblies/crt_tube.gltf | crt_tube |
| assemblies/mainboard.gltf | mainboard |
| assemblies/tuner_module.gltf | tuner_module |
| assemblies/control_panel.gltf | control_panel |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 195-A Game Boy 低模口径）。
- **尺寸比例**：沿用 `14_CRT彩色电视预研卡.md`（21 英寸立式 CRT 彩电公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：按 14 号预研卡部件草图取 6 件（whole + 显像管/外壳/主板/调谐器/控制面板）；screen_glass/speaker/antenna 已并入 whole 或 cabinet 示意，不单独成件。
- **屏面**：关机态深灰纯色；亮机 / 原理动画（黑白雪花 → 彩色）为后续建模卡职责。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–112（>100 且 <4000）。
