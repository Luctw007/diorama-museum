# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-310-J：`nintendo-switch` 低模样板 8 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| tablet.gltf | tablet | 104 | 156 | 4 | 平板：黑色平板主体 + 背壳 + 屏幕 + 卡带槽 + 扬声器×2 + 滑轨×2 + 面板 + 底口 |
| dock.gltf | dock | 104 | 156 | 6 | 底座：黑色 Dock 主体 + 顶盖 + 前框 + 接口槽 + 面板×2 + USB 口×4 + PCB + IC |
| joycon_left.gltf | joycon_left | 104 | 156 | 6 | 左 Joy-Con：霓虹蓝主体 + 顶盖 + 十字键 + 方向键 + 摇杆 + 面板×2 + 接口 + IC + 滑轨 |
| joycon_right.gltf | joycon_right | 104 | 156 | 6 | 右 Joy-Con：霓虹红主体 + 顶盖 + ABXY 键 + 方向键 + 摇杆 + 面板×2 + 接口 + IC + 滑轨 |
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿 PCB + 子板 + Tegra X1/内存 IC×4 + 电容×3 + 接口×2 + 散热片×2 |
| battery.gltf | battery | 104 | 156 | 5 | 电池：银色锂电池主体 + 盖 + 面板×2 + 接口×4 + IC + 线缆×2 + 散热条×2 |
| cartridge_slot.gltf | cartridge_slot | 104 | 156 | 6 | 卡带槽：黑色卡带槽座 + 盖 + 前缘 + 触点×4 + 面板×2 + 卡盖×2 + PCB + IC |
| screen.gltf | screen | 112 | 168 | 6 | 屏幕：屏幕玻璃 + 边框×2 + 面板×2 + 前置件 + IC×2 + 摄像头×2 + 面板×2 + 接口×2 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| chassis 黑 | (0.10, 0.10, 0.12) | 平板/卡带槽黑色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 面板 / 散热片 |
| dock 黑 | (0.10, 0.10, 0.12) | 底座 Dock 主体 |
| joy_l 霓虹蓝 | (0.10, 0.60, 0.80) | 左 Joy-Con |
| joy_r 霓虹红 | (0.90, 0.20, 0.25) | 右 Joy-Con |
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | Tegra X1/内存/IC |
| battery 银 | (0.60, 0.62, 0.65) | 锂电池 |
| black 黑 | (0.05, 0.05, 0.06) | 卡带槽 / 线缆 / 摄像头 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | 屏幕（关机态） |
| button 按键黑 | (0.20, 0.20, 0.22) | 十字键 / ABXY 键 |
| metal 金属银 | (0.72, 0.74, 0.78) | 触点 / 接口 / USB 口 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/tablet.gltf | tablet |
| assemblies/dock.gltf | dock |
| assemblies/joycon_left.gltf | joycon_left |
| assemblies/joycon_right.gltf | joycon_right |
| assemblies/mainboard.gltf | mainboard |
| assemblies/battery.gltf | battery |
| assemblies/cartridge_slot.gltf | cartridge_slot |
| assemblies/screen.gltf | screen |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `44_Switch低模样板预研卡.md`（Switch 平板约 239×14×102 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **dock 入坞识别件**：底座 Dock 与平板为入坞识别件，**入坞动画**以平板滑入 Dock 实现。
  - **joycon_left/joycon_right 卡合识别件**：左右 Joy-Con 为可拆识别件，滑轨卡合是 Switch 标志性交互。
  - **cartridge_slot 卡带插拔识别件**：顶部卡带槽为可插拔识别件。
- **Switch BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–112（>100 且 <4000）；baseColorFactor 全部 0–1。
