# CC-10 规则草案：media_class 覆盖率统计校验

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-125（草案）、TASK-162-B（实现）。状态：**已实现**（`catalog_check.py` CC-10，软落地）。

## 一、规则号与触发对象

- **规则号**：`CC-10`（media_class 覆盖率统计校验）。
- **触发对象**：目录条目的 `media_class` 字段（回填后）。
- **定位**：把「每条目录条目都有 media_class 推定结果」变成可落进 `catalog_check` 的规则；与
  media_infer 的推定建议（R01~R60 + 关键词 K01~K10）配套。

## 二、判据

| 级别 | 判据 | 说明 |
|---|---|---|
| FAIL | 目录条目**缺失** `media_class` 字段（或为空串） | 逐条必须有 media_class |
| WARN | `media_class` 存在但置信度 **< 0.6**（来自 media_infer 推定） | 低置信度须人工复核 |
| PASS | `media_class` 存在且置信度 ≥ 0.6 | — |

> media_class 枚举（v0.5 槽位契约 §3.3）：`cartridge / disk / tape / cd / dvd / card / firmware /
> app_package / 无`（`无` 表示无介质，是合法值，**不等于缺失**）。

## 三、输出格式（对齐 catalog_check）

```
FAIL CC-10 <文件>:<行> <消息>（media_class 缺失）
WARN CC-10 <文件>:<行> <消息>（置信度 <0.6）
末尾统一：FAIL n（供 verify_all / CI 解析）
```

## 四、覆盖率基线（media_infer 实跑，1562 条 v2）

```
推定 1562 条：有值 1562（100%），缺失 0，低置信度(<0.6) 0
  高置信度(≥0.8) 1270 · 中置信度(0.6~0.8) 292 · 低置信度(<0.6) 0
  置信度分布：0.6×49 · 0.7×243 · 0.8×857 · 0.85×6 · 0.9×393 · 0.95×14
```

- 当前目录条目尚未回填 `media_class` 字段（media_infer 仅给建议、未写回），故"缺失"为回填前的
  预期态；回填完成后 CC-10 才可实跑拦截。
- 基线显示 0 条 <0.6（v2 无"其他"大类、无 FALLBACK），WARN 阈值为预防性保留。

## 五、编号冲突裁决

- **裁决**：`CC-10` 正式定义为 **media_class 覆盖率统计校验**（本草案）。
- `规范增补_v0.6.2.md` §六 曾以「反链义务（CC-10 语义）」**口语**指代反链义务，其落地规则是
  `catalog_ref_check` 的 **REF-02**。为避免两义，裁决如下：
  - 反链义务 → 固定为 **REF-02**（不改，占 REF 编号空间）；
  - `CC-10` → 专指 **media_class 覆盖率**（本草案）；
  - v0.6.2 §六 标题「CC-10 语义」口语用法，建议后续勘误为「反链义务（REF-02）」。
- 与 CC-01~08（目录字段/格式/分类/状态/年代/理由/别名/device_id）、REF-01~04（引用一致性）均不撞号。

## 六、边界

- 本任务只出草案文档，**不改 `catalog_check.py`**（实现待下轮）；
- 覆盖率统计数字来自真实 media_infer 实跑（1562 条 v2），未编造条目数。

## 七、实现说明（TASK-162-B 软落地）

- **已实现**：`catalog_check.py` 新增 CC-10，与 CC-01~08 同构（per_rule 汇总 + render_report/render_json
  + 退出码）。
- **软落地开关**：
  - 默认（无开关）：media_class 缺失仅记 **WARN**，不进 FAIL 计数、退出码不转非零（存量不破门禁）；
  - `--require-media-class` 严格模式：缺失记 **FAIL**，计入 fail 与退出码（供回填完成后启用）。
- **置信度委托**：`<0.6` 的 WARN 不在本工具计算（置信度仅由 media_infer 产生），方案写明委托关系，
  不重复实现。
- **严格模式启用交接条件**：**回填完成且默认模式 CC-10 缺失计数归 0 后**，方可在 verify_all 侧打开
  严格开关（`--require-media-class`）。当前默认模式 WARN 1582（全部未回填），属预期态。
