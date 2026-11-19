# sign_ref 回填验收清单 v1（C-3 落地 · 03/04 线领用）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-207-A（02 线）。定位：把 `sign_ref权威id定义_v1.md`（197-B）方案转成 **03/04 线可执行的
> 回填验收清单**。**只出清单，不代 03/04 线改存量键。**

## 一、03 线可执行条目

| # | 条目 | 动作 | 状态 |
|---|---|---|---|
| 1 | 图鉴短卡（`图鉴短卡文本_*.md`） | 主键已是目录 id（`C-xxx`），**无需回填** | 已对齐 |
| 2 | annotations 存量（`annotations.json` 的 `id` 字段，包内局部键如 `whole_role`） | **不改存量**；tour 台本引用子部件标注时用 `目录id#标注id` 两级组合 | 待 tour 落地时组合 |
| 3 | 目录条目（jsonl） | 无需新增字段；`sign_ref` 的权威 id 即目录条目的 `id` 字段 | 已对齐 |

> 03 线核心结论：**图鉴短卡、目录条目均已用目录 id，零迁移**；annotations 的包内局部 `id` 保持不变，
> 只在 tour 台本引用时由 02 线定义的两级格式 `目录id#标注id` 组合（如 `C-MF-000050#whole_role`）。

## 二、04 线（已对齐，无需回填）

- 04 线是图鉴 UI 规格（design 文档），消费 03 线图鉴短卡文本，沿用目录 id——**无需回填**。
- 图鉴 UI 渲染时按目录 id 取短卡，`sign_ref` 解析到目录 id 即可命中图鉴短卡。

## 三、验收口径（回填完成后自证）

1. **catalog_ref 无新违规**：`python 02/repo/tools/validate/catalog_ref_check.py` → REF-01~04 全 0 ·
   FAIL 0（sign_ref 的目录 id 部分应能解析到目录条目）。
2. **tour sign_ref 可解析**：导览台本落地后，每个 `stops[].sign_ref` 的目录 id 部分能解析到目录条目
   （设备级）；子部件精确引用 `目录id#标注id` 的标注 id 部分能解析到该包的 `annotations.json`。
3. **标注 id 不参与 catalog_ref**：`目录id#标注id` 的后半（标注 id）属包内引用，由 validate 的 R-xxx
   管，不参与 catalog_ref 的跨表校验——清单回填不要求 catalog_ref 校验标注 id。

## 四、与任务书的漂移（如实）

- 04 线实为图鉴 UI 规格（消费侧），非独立短卡存量，故标"已对齐、无需回填"（非任务书默认的"04 线需
  回填"）。
- 03 annotations 裁决"不改存量"，回填动作集中在"tour 落地时组合两级格式"，故 03 线可执行条目只有
  3 条、其中 2 条"已对齐"、1 条"待 tour 落地时组合"。
