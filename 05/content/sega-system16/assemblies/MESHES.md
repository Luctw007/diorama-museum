# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-310-Q：`sega-system16` 街机基板低模样板 5 件 gltf（程序化盒子几何，多材质分色，baseColorFactor 纯色无贴图）。
> 节点名 = node_id（R-090 契约）；本包**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| mainboard.gltf | mainboard | 104 | 156 | 5 | 主板：绿色 FR-4 基板 + 子板 + 芯片×4 + 电容×3 + 接口×2 + 散热片×2 |
| cpu.gltf | cpu | 104 | 156 | 5 | 主 CPU：68000 处理器芯片 + 顶盖 + 基座 + 引脚×8 + PCB + 标记 |
| graphics_chip.gltf | graphics_chip | 104 | 156 | 5 | 图形芯片：图形处理芯片 + 顶盖 + 基座 + 引脚×8 + PCB + 标记 |
| sound_module.gltf | sound_module | 104 | 156 | 5 | 音源模块：音源芯片 + 顶盖 + 基座 + 引脚×8 + PCB + 标记 |
| rom_board.gltf | rom_board | 104 | 156 | 5 | ROM 板：黑色 ROM 插槽板 + 盖 + 触点×4 + 芯片×2 + 面板×2 + PCB + 卡口×2 |

> 面数 = 顶点数 × 1.5。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| green 绿 PCB | (0.08, 0.25, 0.12) | 主板 / 内部电路板 |
| chip 芯片黑 | (0.05, 0.05, 0.05) | 芯片 / IC |
| black 黑 | (0.05, 0.05, 0.06) | ROM 插槽板 / 卡口 / 基座 |
| metal 金属银 | (0.72, 0.74, 0.78) | 引脚 / 触点 / 接口 |
| panel 深灰 | (0.25, 0.25, 0.28) | 散热片 / 面板 / 标记 |

## 与 node_id 对应表

| mesh_ref | node_id |
|---|---|
| assemblies/mainboard.gltf | mainboard |
| assemblies/cpu.gltf | cpu |
| assemblies/graphics_chip.gltf | graphics_chip |
| assemblies/sound_module.gltf | sound_module |
| assemblies/rom_board.gltf | rom_board |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（对齐 205-A CRT 低模口径）。
- **尺寸比例**：基板为通用街机基板尺寸公开近似值，正式建模前按 MAME 源码/基板文档复核（无来源标「需核实」）。
- **识别件**：
  - **rom_board ROM 板插拔识别件**：ROM 板可插拔，是街机「换卡不停机」叙事的物理锚点。
- **街机 ROM/BIOS 红线（FR-E3）**：本包仅低模网格，不含 ROM/BIOS/贴图，不下载任何版权材料。
- **校验**：5 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；顶点数 104（>100 且 <4000）；baseColorFactor 全部 0–1。
