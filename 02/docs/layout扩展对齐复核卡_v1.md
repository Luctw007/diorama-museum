# layout 扩展对齐复核卡 v1（227-A 规范 vs 231-B 实装 P-01~P-03）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-237-B（02 线）。定位：逐字段核对 227-A《layout扩展规格_v1》（规范侧）与 231-B `layout_check.py`
> P-01~P-03（实装侧）的一致性，不一致处如实登记。**只改 02 目录，纯核对文档，不改 01 线代码。**
>
> 素材：`layout扩展规格_v1.md`（227-A）、`layout_check.py`（231-B 实装）、`layout传送点提案_v1.md`（226-A 提案溯源）。

## 一、三字段逐项核对表（规范 vs 实装）

| 字段 | 规范（227-A） | 实装（231-B layout_check.py） | 结论 |
|---|---|---|---|
| portals 类型 | 数组（可选，缺省 `[]`） | `portals is not None` 才检查，非 list 报 P-01 | **一致**（可选 + 数组） |
| portals[].target | 非空 string，指向布局文件名（不含 .json）或 hall_group | `target` 非空 string 且 ∈ {content 下 .json 去后缀} ∪ HALL_GROUPS | **一致** |
| portals[].position | 3 元数值，L-03 厅界 | `check_number_list(3)` + 厅界（\|x\|≤w/2、y≥0、\|z\|≤d/2） | **一致** |
| portals[].rotation | 可选，4 元四元数（或朝向角兼容） | 若在须 4 元数值数组 | **一致**（校验只认 4 元数值，朝向角兼容属运行时） |
| hall_group | string，取值 hub/dawn/mainframe/personal/console | `HALL_GROUPS = (hub, dawn, mainframe, personal, console)`，否则 P-03 | **一致** |
| lod_scale | 数值 >0，缺省 1.0 | `isinstance(num) and >0`，否则 P-03 | **一致** |
| 三字段可选 | 可选（存量布局零破坏） | 均 `if ... is not None` / `if ... in layout` 才检查 | **一致** |

> **结论：三字段规范 vs 实装全部一致，零漂移。**

## 二、已发现漂移登记（提案 vs 规范，非规范 vs 实装）

| 项 | 226-A 提案 | 227-A 规范（定稿） | 231-B 实装 | 性质 |
|---|---|---|---|---|
| hall_group 取值域 | `hub` / `wing`（两值） | `hub` / dawn / mainframe / personal / console（五值） | 五值（对齐规范） | 227-A 定稿把 `wing` 扩展为四子厅 slug，231-B 已对齐，**无残留漂移** |
| lod_scale 取值域 | `0.5~2.0` | `>0` | `>0`（对齐规范） | 227-A 放宽为「>0」不设上下界，231-B 已对齐，**无残留漂移** |
| hall_group 缺省 | 缺省 `wing` | 缺省视为「子厅」（不强制回填） | 缺省不检查（等价旧行为） | **一致**（缺省语义等价） |

> 说明：上述两处「漂移」是 **226-A 提案 → 227-A 规范** 的定稿裁决（227-A 已写 §四漂移），231-B 实装
> **正确对齐了 227-A 规范**，故「规范 vs 实装」无漂移。任务书所说「lod_scale 0.5~2.0 / hall_group hub/wing」
> 是 226-A 提案口径，非 227-A 定稿口径。

## 三、结论与后续动作

1. **对齐达成**：三字段 227-A 规范 vs 231-B 实装**全部一致**，无需修订规范、无需改实装。
2. **无责任线待办**：提案→规范的「hall_group 五值、lod_scale >0」裁决已在 227-A 落定、231-B 已按此实装，
   无残留漂移项，无待改责任线。
3. **遗留（非阻塞）**：`layout_check.py` 不在 verify_all / release_check 步构成内（231-B 已确认），layout 校验
   以 `layout_check.py --all` 独立直跑为准；是否纳入门禁步属 01 线门禁扩展项，非本核对卡阻塞。

## 四、与任务书的漂移（如实）

1. **规范 vs 实装零漂移**：任务书提示「lod_scale 227-A『>0』vs 226-A『0.5~2.0』、hall_group 五值 vs 提案
   hub/wing」，实为**提案 vs 规范**的差异（227-A 定稿已裁决），231-B 实装已对齐 227-A，故规范 vs 实装
   **三字段全一致、零漂移**。
2. **门禁 49/49**（本任务实测），231-B 报告写 50/50（其执行时完工包数不同），步数随 ready 包数波动，均全绿。
3. 前置文件 `layout传送点提案_v1.md`（226-A）已产出（227-A 时未产出），本卡已据其补全提案口径溯源。
