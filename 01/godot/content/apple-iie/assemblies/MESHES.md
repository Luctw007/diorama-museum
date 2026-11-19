# MESHES.md — 网格清单与制作口径（占位盒）

> TASK-210-A：`apple-iie` 占位盒 6 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**不建** meta.json 之外的产包链（annotations/encyclopedia/THIRD_PARTY 已就位，目录回填见 210-A 报告）。

## 网格清单（占位盒）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| whole.gltf | whole | 112 | 168 | 5 | 整机：米色机箱 + 顶盖 + 外接显示器 + 屏幕 + 键盘 + 键帽区 + Disk II 软驱 + 电源 + 扩展槽口 + 电源灯 + 机脚 |
| case.gltf | case | 112 | 168 | 7 | 机箱：米色主体/顶盖/底壳 + 左右侧板 + 后盖 + 键盘区 + 扩展槽口 + 通风口 + 电源灯 + 铭牌 + 机脚 + 主板 PCB |
| keyboard.gltf | keyboard | 112 | 168 | 2 | 键盘：米色底座 + 深色键帽矩阵（两行） |
| monitor.gltf | monitor | 104 | 156 | 6 | 外接显示器：米色外壳/底座/后盖 + 深灰屏幕 + 屏框 + 机脚 + 电源灯 + 视频接口 |
| floppy.gltf | floppy | 104 | 156 | 7 | Disk II 软驱：米色外壳/顶盖/底壳 + 深色盘口 + 盘门 + 指示灯 + 金属底板/螺丝 + 内部 PCB + 金手指 |
| power_supply.gltf | power_supply | 104 | 156 | 7 | 电源：金属屏蔽盒/侧板/底盖 + 开关 + 线缆 + 内部 PCB + 指示灯 + 芯片 + 触点 |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。占位盒阶段不追求真实几何，以多材质分色示意部件。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| beige 米色 | (0.78, 0.75, 0.66) | 机身/外壳/键盘底座/显示器/软驱（Apple IIe 标志性米色塑料） |
| dark 深灰 | (0.20, 0.20, 0.22) | 键帽/盘口/通风口/屏框 |
| black 黑 | (0.05, 0.05, 0.06) | 机脚/开关/盘门 |
| metal 金属银 | (0.65, 0.66, 0.68) | 扩展槽口/底板/屏蔽盒/接口 |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板/软驱/电源内部电路板 |
| screen 屏深灰 | (0.10, 0.10, 0.12) | CRT 屏面（关机态） |
| gold 金手指金 | (0.85, 0.70, 0.20) | 铭牌/软驱触点/电源触点 |
| red 指示灯红 | (0.90, 0.20, 0.10) | 电源指示灯 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 电源内部芯片 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/whole.gltf | whole |
| assemblies/case.gltf | case |
| assemblies/keyboard.gltf | keyboard |
| assemblies/monitor.gltf | monitor |
| assemblies/floppy.gltf | floppy |
| assemblies/power_supply.gltf | power_supply |

## 制作口径

- **占位盒**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面（低模口径，后续轮次升级）。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 apple-ii 母本口径）。
- **尺寸比例**：沿用 `11_AppleIIe.md` 研究卡（主机约 40×12×40 cm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **部件**：6 件（whole + 机箱/键盘/外接显示器/Disk II 软驱/电源），对齐研究卡部件分解草图；主板并入 case（占位盒阶段不单独成件）。
- **校验**：6 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–112（>100）。
