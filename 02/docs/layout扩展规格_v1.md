# layout schema 扩展规格 v1（portals / hall_group / lod_scale 落规范）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-227-A（02 线）。定位：把 221-A《全馆功能开题预研》§② 的 layout schema 扩展提案
> （`portals` / `hall_group` / `lod_scale`）落为规范，供 01 线 F-1~F-3 实装引用。**只出规范，不改 01 线
> layout 文件/代码。**
>
> 素材来源：`全馆功能开题预研_v1.md` §②（221-A）、`exhibit_layout_spec.md`（layout 既有 L1 schema，21-B）。
> 226-A 同批 JSON 提案（`layout传送点提案_v1.md`）执行时**未产出**，本规格以 221-A §② 口径为准（见 §四漂移）。

## 一、三字段定义（L1 schema 扩展）

> 三个字段均为**顶层可选字段**（存量 layout 不含它们仍合法），消费方为 `exhibit_host.gd`（运行时）与
> `layout_check.py`（校验，规则编号 L-11~L-13，续既有 L-01~L-04）。

### 1.1 `portals`（传送点，数组）

| 项 | 内容 |
|---|---|
| 类型 | 数组（可选，缺省 `[]` = 无传送点） |
| 元素 | `{ target: string, position: [x,y,z], rotation?: [x,y,z,w] 或朝向角 }` |
| 语义 | 大厅（Hub）与各子厅入口之间的传送点；`target` 为**目标厅的 layout 文件名（不含 `.json`）或 hall_group 标识** |
| 坐标 | `position` 沿用 L-03 坐标规则（x∈[-w/2,w/2]、y≥0、z∈[-d/2,d/2]）；`rotation` 沿用 04 线朝向角转换 `rotation.y = deg_to_rad(-朝向角)`（exhibit_layout_spec §2） |

```json
"portals": [
  { "target": "exhibit_dawn", "position": [0.0, 0.0, -5.0], "rotation": [0.0, 0.0, 0.0, 1.0] }
]
```

### 1.2 `hall_group`（大厅/子厅分组，字符串）

| 项 | 内容 |
|---|---|
| 类型 | 字符串（可选，缺省视为「子厅」） |
| 取值 | `"hub"`（大厅枢纽）或子厅 slug：`"dawn"`（黎明厅）/ `"mainframe"`（大型机厅）/ `"personal"`（个人机厅）/ `"console"`（游戏机厅） |
| 语义 | 供 HallNavPanel 大厅总览面板按组归类；F-3 大厅枢纽厅布局文件 `hall_group="hub"` |

> 注：子厅 slug 取值沿用 02 线目录「厅归属」口径（dawn/mainframe/personal/console），与 04 线四厅命名
> 对应；若 04 线后续定案不同 slug，以 04 线定案为准（回写本表）。

### 1.3 `lod_scale`（厅级 LOD 距离缩放，数值）

| 项 | 内容 |
|---|---|
| 类型 | 数值（可选，缺省 `1.0`） |
| 语义 | 厅级 LOD 距离阈值缩放系数——本厅设备的 LOD 切换距离统一乘此系数（`1.0`=不缩放；`<1.0`=提前降 LOD 远景；`>1.0`=延后降 LOD） |
| 生效判据 | layout 加载时读取，作用到本厅设备 LOD 距离；特写/观察/远景三档距离阈值 × `lod_scale` |

## 二、与既有 layout 键的兼容与迁移口径

1. **存量 layout 不受影响**：三字段均为可选，既有 `exhibit_dawn.json` 等不含三字段仍合法（L-01~L-04 不变）。
2. **兼容写法**：`rotation` 沿用既有「标准四元数，或 position 第 4 元存朝向角」两种写法（exhibit_layout_spec §2），
   `portals[].rotation` 同款兼容，不新增第三种写法。
3. **迁移**：无需迁移存量文件；新增大厅布局文件（F-3）时按新 schema 写 `hall_group="hub"` + `portals`，
   既有子厅布局文件后续可选补 `hall_group`（缺省视为子厅、不强制回填）。

## 三、01 线 F-1~F-3 实装的引用与验收口径

| 规则 | 校验（layout_check.py） | 运行时（exhibit_host.gd） | 验收判据 |
|---|---|---|---|
| L-11 portals | `portals` 若存在：元素 `target` 非空 string、`position` 3 元数值（L-03 边界）、`target` 指向存在布局或 hall_group | 解析 portals 生成传送点，切换时调用 switch_hall 清场重建 | 大厅到子厅传送点可触发切厅、无红字 |
| L-12 hall_group | `hall_group` 若存在：取值 ∈ {hub, dawn, mainframe, personal, console} | HallNavPanel 按 hall_group 分组显示四厅 + 大厅入口 | 大厅总览面板列齐四厅 + 镇馆之宝入口 |
| L-13 lod_scale | `lod_scale` 若存在：数值 > 0 | 加载时读入，乘到本厅设备 LOD 距离阈值 | 改 lod_scale 值可观察本厅设备 LOD 切换距离变化 |

> F-1（大厅总览面板）/ F-2（传送点 schema 落地）/ F-3（大厅枢纽布局）按 221-A §④ 排期；三字段的
> 实装验收以「L-11~L-13 无红字 + 运行时判据达成」为准。

## 四、与任务书的漂移（如实）

1. **226-A 提案未产出**：`layout传送点提案_v1.md` 执行时不存在（01 线同批 226-A 未交付），本规格以
   221-A §② 的提案口径（`portals: [{target, position, rotation}]`、`hall_group`、`lod_scale`）为准，
   未对 226-A 的 JSON 提案格式做逐字段对齐（留待 226-A 交付后回填）。
2. **子厅 slug 取值**：221-A 未给 `hall_group` 的枚举取值，本规格按 02 线目录「厅归属」口径补
   `hub/dawn/mainframe/personal/console` 五项，并注明以 04 线定案为准。
