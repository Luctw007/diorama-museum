# MESHES.md — 网格清单与制作口径（低模样板）

> TASK-185-A：4 个占位白模（各 1 三角面）已重制为**低模样板**（多材质分色、程序化几何）。
> 节点名 = node_id（R-090 契约），mesh_ref 不变；meta.json / annotations **未改动**。

## 网格清单（低模）

| 文件 | 节点名 | 顶点数 | 三角面数 | 材质数 | 内容 |
|---|---|---|---|---|---|
| case.gltf | case | 104 | 156 | 3 | 机箱主体（米色）+ 斜切顶盖 + 散热槽×6 + 通风格栅×4 + 电源灯（红） |
| keyboard.gltf | keyboard | 296 | 444 | 2 | 键盘底座（深棕）+ 3 排 × 12 键帽（灰白） |
| disk_ii.gltf | disk_ii | 120 | 180 | 4 | 主体+前挡板（米色）+ 槽口/把手槽/散热槽×6（深）+ 指示灯（红）+ 脚垫×4（灰） |
| mainboard.gltf | mainboard | 144 | 216 | 4 | 基板（绿）+ 芯片块×12（黑）+ 插槽条×3（灰）+ 电容×2（红） |

> 面数 = 顶点数 × 1.5（每盒 8 顶点 / 12 三角面）。均 >100 顶点、<4000 顶点，保持低模口径。

## 材质清单（baseColorFactor，无贴图、无外部文件）

| 材质 | baseColorFactor | 用途 |
|---|---|---|
| beige 米色 | (0.86, 0.82, 0.70) | 机箱、软驱外壳 |
| brown 深棕 | (0.25, 0.22, 0.20) | 键盘底座 |
| green 主板绿 | (0.10, 0.30, 0.12) | 主板基板 |
| black 芯片黑 | (0.05, 0.05, 0.05) | 芯片块 |
| gray 金属灰 | (0.50, 0.50, 0.52) | 插槽条、脚垫 |
| key 键帽灰白 | (0.85, 0.85, 0.85) | 键帽 |
| red 指示灯红 | (0.80, 0.12, 0.12) | 电源灯/指示灯/电容 |
| dark 深槽 | (0.45, 0.42, 0.38) | 散热槽/格栅/槽口 |

## 与 node_id 对应表

| mesh_ref | node_id | 装配体（meta.json） |
|---|---|---|
| meshes/case.gltf | case | case |
| meshes/keyboard.gltf | keyboard | keyboard |
| meshes/disk_ii.gltf | disk_ii | disk_ii |
| meshes/mainboard.gltf | mainboard | mainboard |

## 制作口径

- **低模**：程序化盒子几何，多材质分色表达部件，不做贴图、不做复杂曲面。
- **坐标**：模型原点在装配体原点，Y 向上、面朝 -Z（transform 语义保持，未改装配体树）。
- **尺寸比例**：沿用 S02/S05/S06 公开资料近似值，正式建模前需实测定值（无来源标「需核实」）。
- 校验：`verify_all.py --only pkg:apple-ii` → 272 PASS / 0 FAIL；`--only catalog_ref` → FAIL 0。
