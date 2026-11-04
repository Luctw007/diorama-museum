# TASK-53A 完成报告（03 线 1/2）：《设备目录 · 计算机大类》第一批普查

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-53A（03 线 1/2）：计算机大类目录第一批普查（目标 300+ 条） |
| 前置 | TASK-48（手机厅/通用设备厅调研）完成 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/catalog/计算机大类_目录_v1.jsonl` | 机器可读目录（每行一条） | **309 条**（≥300 达标） |
| `docs/catalog/计算机大类_目录_v1.md` | 人类可读分中分类表格 + 覆盖面自查表 | 同 309 条 |
| `docs/catalog/TASK-53A_完成报告.md` | 本报告 | — |

## 二、统计表

| 指标 | 数值 |
|---|---|
| 总条目 | **309**（目标 ≥300） |
| 中分类数 | 7 |
| 子分类数 | 38 |
| 状态 done（已产包） | 12 |
| 状态 planned（待深研） | 297 |
| 需核实（verify=true） | 12 |

### 每中分类计数

| 中分类 | 条目数 | 子分类数 |
|---|---|---|
| 大型机 | 84 | 6 |
| 个人机 | 83 | 10 |
| 小型机 | 46 | 5 |
| 工作站 | 38 | 7 |
| 服务器 | 29 | 3 |
| 手持计算 | 15 | 3 |
| 早期计算机 | 14 | 4 |

## 三、已产包（done，关联 device_id）

| device_id | 名称 | 归类 |
|---|---|---|
| manchester-baby | Manchester Baby | 早期计算机 |
| eniac | ENIAC | 早期计算机 |
| edsac | EDSAC | 早期计算机 |
| edvac | EDVAC | 早期计算机 |
| system360 | IBM System/360 Model 30 | 大型机 |
| pdp8 | PDP-8 | 小型机 |
| pdp11 | PDP-11/70 | 小型机 |
| vax11 | VAX-11/780 | 小型机 |
| commodore64 | Commodore 64 | 个人机 |
| ibm5150 | IBM PC 5150 | 个人机 |
| bbcmicro | BBC Micro | 个人机 |
| apple-ii | Apple II | 个人机 |

> 全包索引共 15 台展项，其中 **3 台为游戏机**（famicom / sega-md / atari-2600，device_class=console），
> 属「游戏机」大类、不在本「计算机」目录范围，已列入覆盖面自查表「转 next 批」。故本目录 done 为 12 台。

## 四、与 taxonomy 的出入清单（供 52 线吸收）

| # | 事项 | 处理 | 建议 |
|---|---|---|---|
| 1 | 02 线 **v0.6 分类学未产出**、**catalog_check 未产出** | 按任务书自带三级路径（大类/中分类/子分类）组织 | 52 线定稿后回填 taxonomy 字段并跑 catalog_check |
| 2 | 新增中分类「**早期计算机**」 | 任务书六中分类未含，为安放 4 台早期展项而补 | 建议吸收为独立中分类（1940s 第一代，非大型机） |
| 3 | 新增个人机子分类「**便携/笔记本**」 | 收纳 Osborne/GRiD/Toshiba 等早期便携机 | 建议吸收（便携机是个人机的标准子类） |
| 4 | 「**服务器**」与「**超级计算机**」边界 | 超级计算机暂挂服务器下子分类 | 建议单列「超级计算机」中分类 |
| 5 | device_class 枚举（7 项）↔ 目录中分类映射 | 本目录中分类：早期计算机/大型机/小型机/个人机/工作站/服务器/手持计算 均映射 device_class=computer | 槽位契约 §3.1 已统一归 computer，无冲突 |
| 6 | 手持计算（Psion/HP LX）与 53-B 的 PDA 重叠 | Psion/HP LX 归 53-A 手持计算，Palm/iPAQ/Zaurus 归 53-B PDA | 建议 52 线合并「手持计算」与「PDA」口径 |

## 五、字段口径（v0.6 未产，自定，供对齐）

每行 JSONL 字段：`id`（kebab-case）、`name`、`alias`（数组）、`manufacturer`、`era`（首产年）、
`taxonomy_path`（`[大类, 中分类, 子分类]` 三级）、`status`（done/planned）、`device_id`（done 时关联）、
`influence`（影响力一句）、`verify`（需核实布尔）。

## 六、开放问题

1. **catalog_check 日志缺失**：02 线未产 catalog_check，JSONL 仅经本地自校验（309 行 JSON 合法、字段齐备、id 唯一、taxonomy 三级齐全），未贴官方日志。
2. **需核实 12 条**：Colossus/ABC 年代、FACOM M-190、Hitachi M-180、SEL 32、Modular One、Acorn System 1、Intergraph Clipper、Sharp PC-3000、Tadpole SPARCbook、NEC SX-3、Google 自研服务器等，已标 `verify=true`。
3. **覆盖广度**：IBM System/3·System/32·System/38、Sperry/Unisys 后继、王安/HP 服务器全系、日本工作站（富士通/日立）、国产早期计算机（DJS-130 等）列入 next 批。
