# TASK-61B 完成报告（docs/TASK-61B_完成报告.md）

> 01 线 · 2026-11-04 · 任务：项目统计面板（project_stats.py）。
> 本报告含 TASK-61 两份总收尾，01 线本轮（任务 61-A/B）完成。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/project_stats.py` | 178 | 聚合面板：包/目录/槽位/质量/工程规模 → docs/PROJECT_STATS.md + --json |
| `docs/PROJECT_STATS.md` | 生成物 | 当前全量数字（人读版） |

## 2. 运行结果（2026-11-04T01:55 快照）

| 面 | 数字 |
|---|---|
| 内容包 | 完工 17 / 生产中 1（zx-spectrum 在产）；占位 glTF 85 个 |
| 厅分布 | 黎明 4 / 大型机 4 / 个人机 5 / 游戏机 4 |
| 设备目录 | **1484 行** / 28 片 / 大分类 5 / 中分类 28 |
| 状态分布 | planned 1454 / researching 11 / done 19 |
| 槽位 | 可用 1（fake-slot）/ 介质目录 0 |
| 质量轻量步 | slots rc=0；catalog 门禁+对账 rc=0 |

## 3. 迭代记录（2 轮）

1. 轮 1：脚本级 bug = PowerShell 管道导致 rc=-1 假象 → 直接运行确认 rc=0（记录，非脚本问题）；
2. 轮 2：厅分布出现"其他 4 台" → 根因是个人机厅各包 category 写法不一
   （computer/personal-computer/home-computer/microcomputer）——补齐映射全归个人机厅；
   该差异已转 62-A 分类树治理清单（**不改他线文件**，映射表是引擎侧兼容层）。

## 4. 统计口径表（每个数字怎么算）

| 数字 | 口径 |
|---|---|
| 完工/生产中 | pkg_registry.discover_packages_full()（WIP 判据同注册表） |
| glTF 计数 | 包内 meshes/ 与 assemblies/ 两目录 .gltf 合计数 |
| 目录行数 | catalog bundle meta.total_rows（对账保证 = 源文件行数） |
| 状态分布 | bundle 分片逐行 status 字段计数 |
| 质量轻量步 | 当场子进程跑 slots/catalog 两步并记 rc（不跑全量验收） |

## 5. TASK-61 两份总收尾 + 01 线本轮完成标注

- 61-A：同步即再生目录包、门禁对账升级、FAIL/恢复双分支验证；
- 61-B：一键统计面板（docs/PROJECT_STATS.md 常驻刷新），04 线仪表盘可直接取 --json。
- 01 线本轮（任务 61）完成。