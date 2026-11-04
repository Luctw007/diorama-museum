# TASK-57A 完成报告（02 线 1/2）：分类学规范 v0.6 定稿

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-57A（02 线 1/2）：分类学规范 v0.6 定稿（吸收普查现实） |
| 前置 | TASK-52（v0.6 草案 + catalog_check） |
| 背景 | 首批 888 条普查落地，暴露键名分叉 + 两级分类两个现实问题 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/内容包与目录规范_v0.6.md` | v0.6 定稿全文（取代 52-A 草案） | 1890 汉字 |
| `tools/validate/catalog_check.py` | 更新至定稿键（CC-01~07） | 已同步 |
| `tools/validate/tests/run_catalog_tests.py` | 反例同步改定稿键 | 7/7 全绿 |
| `docs/TASK-57A_完成报告.md` | 本报告 | — |

## 二、裁决记录

### 裁决 1：统一英文定稿键（不采纳中文键）

**结论**：13 键英文定稿（id/name/aliases/manufacturer/origin/era/taxonomy_path/status/device_id/
influence/verify/sources/research_doc），05 线中文字段列为"非规范写法"给迁移对照表。

**理由（三条）**：
1. JSONL 是机器摄取/校验的权威格式，ASCII 英文键是跨语言工具链惯例（中文键易出编码/列名漂移）；
2. 01 线 `catalog_ingest._adapt` 内部统一键已是英文，采纳英文零返工；
3. 03 线已产 463 条英文键，让 425 条中文键（05）迁英文，比让 463 条英文键（03）迁中文更经济。

键名取 03 线实际字段（manufacturer/era/taxonomy_path/influence），比草案 maker/year/path/reason
语义更直白，一并吸收。

### 裁决 2：允许两级分类（第三级"未细分"）

**结论**：`taxonomy_path` 允许两级或三级，两级时机器补"未细分"。触发条件 = 中分类下暂无法细分
或无策展价值时省略第三级。理由：05 线"家电影音与外设"大量条目只有两级，强制三级会逼造无意义
子分类；01 线 `catalog_ingest` 已按"补未细分"实现，该实现即规范的机器语义。

### 裁决 3：办公外设大类码 O→P

吸收 05 线现实（P=Peripheral，已产 74 条 `P-PER-*`），草案的 O 改为 P。id 中分类码从 2 字符放宽
到 2~4 字符（吸收 05 的 ARC/HOME/PER）。

## 三、05 线中文键迁移清单（11 键，逐键）

| 中文键 | 英文键 | 中文键 | 英文键 |
|---|---|---|---|
| 名称 | name | 影响力理由 | influence |
| 别名 | aliases | 状态 | status |
| 厂商 | manufacturer | 关联包 | device_id |
| 产地 | origin | 来源编号 | sources |
| 年代 | era | id | id（同） |
| 分类路径 | taxonomy_path | | |

## 四、三方对齐表（catalog_check / 01 catalog_ingest）

| 层面 | v0.6 定稿 | catalog_check | 01 _adapt | 结论 |
|---|---|---|---|---|
| 键名 | 13 英文键 | 校验定稿键 | 兼容三种格式 | 一致（_adapt 是超集） |
| id 格式 | `^[CGMPAEX]-[A-Z]{2,4}-\d{6}$` | CC-02 校验 | 仅判重 | catalog_check 更严 |
| 三级分类 | 允许两级 | CC-03 允许两级 | 补"未细分" | 一致 |

## 五、对齐指令全文（交三线）

- **03 线**：`alias`→`aliases`（复数）；id 无前缀 slug 需向 id_registry 申请 C-/M- 前缀正式 id。
- **05 线**：按 11 键对照表迁移中文键→英文键（值不变，可脚本化）；id 前缀 A/P/G 已合规保留。
- **01 线**：`_adapt` 三种格式兼容**保留**为过渡层；收紧条件 = 888 条存量全部迁到定稿键并通过
  catalog_check 后，可移除中文/草稿分支。

## 六、自检

catalog_check.py 更新至定稿键后，反例 7/7 全绿（含"两级分类合法"正例）：

```
run_catalog_tests  结果：PASS 7，FAIL 0
```

## 七、开放问题（留给 v0.7）

1. 中分类/子分类枚举的最终定稿（本定稿只硬约束 7 大分类，中/子在普查演进）；
2. 03 线 463 条无前缀 id 的批量迁移（57-B 承接）；
3. `verify` 与 `sources` 的联动语义；
4. id 中分类码是否最终收敛统一码表。
