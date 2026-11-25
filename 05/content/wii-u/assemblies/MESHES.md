# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-315-E：`wii-u` 低模样板 7 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| console.gltf | console | 120 | 180 | 4 | 主机：黑色圆角横置机身 + 顶盖/底盖 + 前面板 + 吸入式光盘入口 + 电源/弹出/同步键 + SD 卡槽盖 + USB×2 + 蓝色指示灯 + 散热口 + 机脚×2 |
| gamepad.gltf | gamepad | 112 | 168 | 5 | GamePad：黑色平板手柄主体 + 顶盖 + 6.2 英寸触屏 + 屏幕边框 + 十字键 + ABXY + 双摇杆 + HOME 键 + 扬声器口×2 + 摄像头条 + 握把×2 |
| disc_drive.gltf | disc_drive | 104 | 156 | 5 | 吸入式光驱：银色光驱主体 + 前面板 + 吸入入口 + 托盘 + 光盘 + 转盘电机 + 读头 + 导轨 + PCB + IC×2 + 电容 + 齿轮 |
| mainboard.gltf | mainboard | 104 | 156 | 3 | 主板：绿 PCB + 子板 + Espresso CPU/Latte GPU + 内存 IC×4 + 电容×3 + 接口×2 |
| power_supply.gltf | power_supply | 104 | 156 | 6 | 电源：金属银灰屏蔽盒 + 顶盖/底盖 + 电源插座 + 开关 + PCB + IC + 电容×2 + 散热片 + 指示灯 + 端子 |
| controller_port.gltf | controller_port | 104 | 156 | 5 | 手柄接口：黑色同步口座 + 面板 + 触点×4 + PCB + IC + 插头示意×2 + 背板 + 电容 |
| flash_storage.gltf | flash_storage | 104 | 156 | 5 | 闪存模块：绿 PCB + eMMC 闪存芯片×4 + 主控 IC×2 + 电容 + 连接器 + 支架 + 屏蔽罩 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| body 机身黑 | (0.08, 0.08, 0.09) | 主机 / GamePad 黑色塑料主体 |
| panel 深灰 | (0.25, 0.25, 0.28) | 前面板 / 托盘 / 散热片 / 支架 |
| screen 屏幕黑 | (0.02, 0.02, 0.03) | GamePad 6.2 英寸触屏（关机态） |
| dvd 银光驱 | (0.70, 0.72, 0.75) | 吸入式光驱 |
| pcb 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | Espresso/Latte/内存/eMMC/IC |
| psu 金属银灰 | (0.60, 0.62, 0.65) | 电源金属外壳 / 触点 / 屏蔽罩 |
| black 黑 | (0.05, 0.05, 0.06) | 插口 / 入口 / 按键 / 机脚 |
| btn 按键黑 | (0.20, 0.20, 0.22) | 十字键 / ABXY / 双摇杆 |
| led 指示灯蓝 | (0.20, 0.40, 0.80) | 主机电源指示灯 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/console.gltf | console |
| assemblies/gamepad.gltf | gamepad |
| assemblies/disc_drive.gltf | disc_drive |
| assemblies/mainboard.gltf | mainboard |
| assemblies/power_supply.gltf | power_supply |
| assemblies/controller_port.gltf | controller_port |
| assemblies/flash_storage.gltf | flash_storage |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：沿用 `49_WiiU低模样板预研卡.md`（主机约 172×46×268.5 mm、GamePad 约 255×41×133 mm 公开近似值），正式建模前需实测定值（无来源标「需核实」）。
- **识别件**：
  - **gamepad GamePad 触屏手柄识别件**：GamePad 带 6.2 英寸触屏，为标志性识别件，可作「触屏操作/第二屏显示」示意。
  - **disc_drive 吸入式光驱识别件**：光驱为可吸入识别件，**光盘吸入动画**以该 node 为抽拉轴实现。
- **Wii U BIOS/ROM 红线**：本包仅低模网格，不含 BIOS/ROM/贴图，不下载任何版权材料。
- **校验**：7 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104–120（>100 且 <4000）；baseColorFactor 全部 0–1。
