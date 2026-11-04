# TASK-64A 完成报告（04 线 1/2 · 图鉴总览首页规格）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。
> 完成日期：2026-11-04 ｜ 执行线：04 线（未修改 01/03/05 线任何文件；1484 条统计为对 01 线 bundle 与 03/05 线内容包的只读实测）

## 1. 交付物与字数统计

| 文件 | 去空白字符数（PowerShell 实测） |
|---|---|
| `docs/design/35_图鉴总览首页规格.md` | 10,910（≥5500 达标） |
| §6 测试用例 | T-435~T-456 共 22 条 ≥20 达标（手工 8 / 自动化 13 含性能 1 / 待实机 1） |

迭代口径：35 号 v1.0 第 1 轮；T-437 对 §1.2 实测扇区表、T-443 对 §2.1 推荐公式、T-453 对 §3.4 存档 JSON 的用例反查为第 2 轮（并在反查中修正用例档位统计一次）。

## 2. 实况数字（1484 条基线，方法+结论）

**方法**：Python 3.7 只读脚本直读 `01/repo/godot/content/catalog/meta.json` + 28 分片（合计 1484 行，与 meta.total_rows 对账一致），按归一键聚合；包能力扫 `03/05/repo/content/*/meta.json` 逐包计 runtime/assemblies。

**结论**：
1. 目录 **1484 条 / 5 大分类 / 28 中分类**（较 33/34 号基线 888 条已扩版 596 条，新增「办公与计算外设」大类与街机扩容）；
2. 大分类占比（环图）：游戏机 675=45.5%、计算机 504=34.0%、通讯与移动 154=10.4%、家电影音 77=5.2%、办公与计算外设 74=5.0%；
3. 年代 13 档：峰值 1980s=505，次高 1990s=442、2000s=233；状态构成 done 19 / researching 11 / planned 1454 / package 0 / wip 0；
4. 包能力（统计带后两数）：完工包 **18 台**全部可拆解、可运行；目录挂包 19 行去重 16 台；`neo-geo-mvs`、`sfc` 两包未登记进目录。

## 3. 给 01 线取数接口清单（35 号 §4 全集）

| # | 接口/字段 | 形态 | 用途 |
|---|---|---|---|
| 1 | project_stats.py --json 现产字段（packages.ready/halls/gltf_total、catalog.rows/shards/big/mid/status、slots、quality、repo_files、generated） | 已有，直接读 | 统计带、副行 A/B、质量点 |
| 2 | catalog bundle 行字段（id/name/aliases/maker/origin/year/path/reason/status/device_id/sources） | 已有，load_meta+load_shard | 环图/迷你柱/状态条/推荐分 |
| 3 | **pedia_stats.json 聚合档（增补提案）**：big_counts/decades/status_counts/capability{runnable,strippable,linked_rows,unique_devices}/booking_total | 新增，挂 project_stats.py 尾步，秒级 | 首屏一次读全量；万级防御（字段 JSON 已出，35 号 §4.3） |
| 4 | user://profile.json 存档契约（favorites/visits/guide_done/last_daily_seed） | 新增，引擎侧落盘 | 收藏/足迹/首启引导/推荐日种子（35 号 §3.4） |
| 5 | 详情页新增 [收藏] 动作区按钮（31 号 §2.2 扩展）+ 首页三卡/立牌 [进展厅] 位 | UI 扩展点 | 收藏闭环与推荐直达 |

## 4. 需补清单（只列不改）

1. 03/05 线补 2 条 done 目录行登记 `neo-geo-mvs`、`sfc`（补后 done=21 行/唯一台 18）；
2. 03/05 线回填 package/wip 两档（现为 0，首页按 §1.4 显 0 + 口径提示）；
3. 33 号 v2 影响力排序口径同步（现数据 1484/1484 行 reason 非空，「有 reason 置顶」退化为全量置顶，35 号改以文本长度归一）。

## 5. 开放问题

1. 「可拆解/可运行」的最终口径裁决：包能力计数 vs 目录挂包计数（35 号取包能力 18/18 并向 01 线声明能力扫描字段）；
2. 预约计数 booking_total 现为 0——31 号 §2.2 预约功能的 01 线实装节奏；
3. 推荐「新入库」理由缺条目时间戳字段（目录行无 created_at），现以 sources 非空代偿 [需核实]；
4. 万级（10k+）下聚合档生成耗时与首页首屏 1 s 预算的实测关系 [需实机核对]；
5. VR 扇形环台在 6 Dof 下绕台步巡的晕动风险（台高 0.9 m 需实机走查 [需实机核对]）。