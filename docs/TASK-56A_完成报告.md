# TASK-56A 完成报告（docs/TASK-56A_完成报告.md）

> 01 线 · 2026-11-04 · 任务：图鉴目录引擎侧数据层（catalog 分片 → Godot 读取）。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/gen_catalog_bundle.py` | 104 | catalog_index → `godot/content/catalog/{meta.json, data/<大类>__<中分类>.json}` + `--verify` 行数对账 |
| `godot/content/catalog/meta.json` + 27 分片 | 生成物 | **888 行**、5 大分类、27 中分类；分片条带内部统一键 + 原始键 + `_taxonomy` |
| `godot/scripts/catalog_data.gd` | 120 | 静态数据层：get_taxonomy/load_shard(缓存)/build_index/search/get_summary——对齐 04 线 31 号 API 提案 |

## 2. 运行日志（原文）

```text
$ python scripts/gen_catalog_bundle.py
打包完成：888 行 / 27 片 → …\godot\content\catalog    → rc=0
$ python scripts/gen_catalog_bundle.py --verify
verify：27 片 / 888 行，通过                            → rc=0
$ 抽样对账（首片 计算机__早期计算机.json）：meta 14 = 实际 14 ✓
  条目键含内部统一键（name/year/status/device_id/path）+ 原始键 + _taxonomy ✓
```

## 3. 迭代记录（2 轮）

1. 轮 1：meta["generated"] 误用 `ci.time`（catalog_ingest 未 import time）→ 改本文件直接 import time；
2. 轮 2：分片文件名含中文+空格的 URL 安全性 → 保留中文名（Godot FileAccess 支持 UTF-8 路径），
   但在 meta.shards 提供 big/mid 两列供引擎按语义拼接（不靠文件名解析）。

## 4. 与 31 号 API 提案的字段对照

| 31 号 API | catalog_data.gd | 状态 |
|---|---|---|
| get_taxonomy | ✓（大→中→[子]树） | 实装 |
| load_shard(big,mid) | ✓（缓存零重复 IO） | 实装 |
| search(keyword) | ✓（精确小写名/别名；模糊待引擎） | 简版 |
| Paged 结构 | 由 59-A 联调规格定案 | 待 59 |

## 5. 开放问题

- 模糊搜索/拼音在引擎侧实现（GDScript 无内置拼音，需 02 线约定方案）；
- bundle 应在 sync_content 后自动重生成（下轮接入选代链，避免手工跑）。