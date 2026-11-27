# arcade-10 序列总索引 v1

> 任务 TASK-325-Q（05 线）· 完成日期：2026-11-27 · 新建 v1。
> 性质：**纯索引**——集中登记 arcade-10 序列已产出的全部卡片，以及产包 done 实测清单（G-AC 前缀），供后续检索与续接；本卡**不产包、不建模、不改 jsonl、不下载任何东西**。

---

## 一、参数 / 键位卡登记

| 卡片 | 任务 | 完成日期 | 内容要点 |
|---|---|---|---|
| 街机10台_参数卡_v1.md | 157 | 2026-11-06 | 10 台街机基板参数（厂商 / 年代 / 基板 / 处理器 / 分辨率 / 模拟器 / 来源），敏感值标「需核实」，不下载 ROM/BIOS |
| 街机控台键位增量表_v1.md | 170-B | 2026-11-08 | 10 台街机控台摇杆 + 按钮布局键位增量，含 MVS 键位对齐比对（与 runtime input_map 对照） |

## 二、巡检 / 建模 / 准备卡登记

| 卡片 | 任务 | 完成日期 | 内容要点 |
|---|---|---|---|
| 街机目录planned巡检_v1.md | 295-J | 2026-11-24 | G-AC planned 条目现状清单 + 候选分组（共 250 条），纯巡检、不回填、不改 jsonl |
| 街机基板线建模任务卡_v1.md | 305-M | 2026-11-25 | CPS-1 / Sega System 16 两块基板建模任务卡（节点分解 + 三档 LOD 预算 + 识别件 + 验收口径），街机 ROM/BIOS 红线 FR-E3 |
| 街机经典名作框体产包准备卡_v1.md | 305-N | 2026-11-25 | Pac-Man 框体产包准备卡（产包字段清单 + components 拆分 + media_hint 口径 + ROM 红线 FR-E3） |

## 三、预研卡登记

| 卡片 | 任务 | 完成日期 | 内容要点 |
|---|---|---|---|
| Donkey Kong与Galaga街机框体低模样板预研卡_v1.md | TASK-320-L | 2026-11-26 | DK / Galaga 双机合卡预研：尺寸 / 配色 / 识别件 / ROM 红线 / 目录方案预告 |
| Frogger与MsPacMan街机框体低模样板预研卡_v1.md | TASK-325-B | 2026-11-27 | Frogger / Ms. Pac-Man 双机合卡预研：同结构备料（8 件 / 纯色 baseColorFactor） |

## 四、产包 done 实测（G-AC 前缀 7 台）

> 以目录 `catalog/游戏机与手持大类_目录_v2.jsonl` 实扫为准（2026-11-27），逐台列 device_id：

| # | 目录 id | device_id | 名称 | 归属 |
|---|---|---|---|---|
| 1 | G-AC-000002 | space-invaders-arcade | Space Invaders | 经典名作线 |
| 2 | G-AC-000005 | pac-man-arcade | Pac-Man | 经典名作线 |
| 3 | G-AC-000009 | donkey-kong-arcade | Donkey Kong | 经典名作线 |
| 4 | G-AC-000012 | galaga-arcade | Galaga | 经典名作线 |
| 5 | G-AC-000010 | frogger-arcade | Frogger | 经典名作线 |
| 6 | G-AC-000016 | ms-pac-man-arcade | Ms. Pac-Man | 经典名作线 |
| 7 | G-AC-000076 | neo-geo-mvs | Neo Geo MVS | 基板线 |

## 五、分组

- **基板线（CPS-1 / System 16 低模）**：`街机基板线建模任务卡_v1.md` 起步（CPS-1、Sega System 16 两块基板低模）；done 已有 Neo Geo MVS（G-AC-000076）。
- **经典名作线（Pac-Man 等）**：`街机经典名作框体产包准备卡_v1.md` 起步（Pac-Man），四张预研卡覆盖 DK / Galaga / Frogger / Ms. Pac-Man；done 已有 Space Invaders、Pac-Man、Donkey Kong、Galaga、Frogger、Ms. Pac-Man 六台。

## 六、检索指引

| 需求 | 先看 |
|---|---|
| 街机基板参数（10 台） | 街机10台_参数卡_v1.md |
| 街机控台摇杆 / 按钮键位 | 街机控台键位增量表_v1.md |
| G-AC planned 现状与候选 | 街机目录planned巡检_v1.md |
| 基板低模建模任务 | 街机基板线建模任务卡_v1.md |
| 经典名作框体产包准备 | 街机经典名作框体产包准备卡_v1.md |
| DK / Galaga 低模预研 | Donkey Kong与Galaga街机框体低模样板预研卡_v1.md |
| Frogger / Ms. Pac-Man 低模预研 | Frogger与MsPacMan街机框体低模样板预研卡_v1.md |

## 七、红线自查

本卡纯索引，不产包、不建模、不改 jsonl、不下载 ROM/BIOS/二进制/贴图；done 数（7 台）与 device_id 均以目录 jsonl 实扫为准、不臆造；只写本 1 个 md 文件。
