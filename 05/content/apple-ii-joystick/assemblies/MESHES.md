# MESHES.md — 网格清单与制作口径（低模）

> TASK-325-E：`apple-ii-joystick` 低模 5 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| base.gltf | base | 120 | 180 | 6 | 底座：摇杆底座主体 + 面板 + 按键孔 + 走线孔 + 电路板 + 芯片 |
| stick.gltf | stick | 104 | 156 | 5 | 摇杆：摇杆杆体 + 握柄球头 + 摆杆 + 金属件 + 芯片 + 面板 |
| button.gltf | button | 104 | 156 | 6 | 按键：动作按键键体 + 键座 + 触点金属 + 芯片 + 面板 + 电路板 |
| cable.gltf | cable | 104 | 156 | 2 | 线缆：线缆外皮 + 金属接头 |
| base_plate.gltf | base_plate | 104 | 156 | 6 | 底板：底座底板 + 扣合边 + 防滑脚 + 金属件 + 芯片 + 电路板 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 黑 | (0.05, 0.05, 0.06) | 底座/底板黑色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 面板 / 支架 / 盖板 |
| black 黑 | (0.05, 0.05, 0.06) | 线缆外皮 / 插口 / 键座 |
| btn 红 | (0.65, 0.08, 0.08) | 按键键体 / 摇杆握柄 |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 接头 / 触点 / 金属件 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | IC / 微动开关 / 电容 |
| pcb 绿 | (0.08, 0.25, 0.12) | 内部电路板 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/base.gltf | base |
| assemblies/stick.gltf | stick |
| assemblies/button.gltf | button |
| assemblies/cable.gltf | cable |
| assemblies/base_plate.gltf | base_plate |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：摇杆底座/握柄三维尺寸、杆高、行程、配色均为低模近似占位，正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **stick 摇杆摆动识别件**：摇杆为可摆动识别件，可作「摇杆摆动」演示。
  - **button 按键按压识别件**：按键为可按压识别件，可作「按键按压」演示。
- **接口红线**：Apple II 游戏摇杆经 Apple II `game_port`（游戏端口）接入主机，属于**清单级引用**：本包只登记接口名称与接入关系，不落地任何引脚定义、电气参数、协议文档（无来源一律标 [需核实]）。
- **纯输入外设**：本设备无固件、无介质、不输出；`runtime.media_hint=none`、`runtime.output_sinks` 为空数组，均显式写入 meta 说明。
- **校验**：5 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
