# TASK-36B 完成报告（docs/TASK-36B_完成报告.md）

> 01 线 · 2026-11-03 · 任务：图鉴静态索引生成（见 任务36-B）。
> 本报告含 TASK-36 两份总收尾，01 线本轮（任务 36-A/B）完成。

## 1. 交付物

| 文件 | 规模 | 说明 |
|---|---|---|
| `scripts/gen_exhibit_index.py` | 217 | 11+1 包扫描 → 厅聚合索引；`--dry-run`/`--verify`（逐字段比对） |
| `godot/content/exhibit_index.json` | 生成物 | 五厅 12 台（含 test-device 示例厅） |
| `godot/scripts/exhibit_index.gd` | 120+ | 静态工具类：get_halls/get_devices/get_device/hall_of/get_summary |

## 2. 运行日志（原文关键段）

```text
$ python scripts/gen_exhibit_index.py --dry-run
  黎明厅（Dawn Hall）                     4 台
  大型机与小型机厅（Mainframe Hall）       4 台
  个人计算机厅（Personal Computer Hall）   1 台
  游戏机厅（Console Hall）                 2 台
  示例（Samples）                         1 台
  合计 12 台

$ python scripts/gen_exhibit_index.py --verify
verify 结果：通过（0 条差异）                          → rc=0
```

## 3. 迭代记录（2 轮）

1. 轮 1：误读 meta 结构（category 在 `meta` 包装块内而非顶层）→ 修正后 11 包 category 全部取得（early-computer/mainframe/minicomputer/computer/game-console/placeholder）；
2. 轮 2：annotations.json 存在列表与字典两种写法 → 计数函数兼容三形态；verify 阶段对 era 允许 null（早期机型档案缺年份时不误报）。

## 4. 与 04 线图鉴 UI 的对接字段表（02 号文档）

| UI 元素 | 字段 | 来源 |
|---|---|---|
| 厅名列表 | halls[].hall | HALL_OF 映射 |
| 设备卡标题 | devices[].name | meta.name.zh |
| 年代角标 | devices[].era | meta.era |
| 可运行标记 | devices[].demo_mode（false=可运行） | run_profile 派生 |
| 详情行 | emulator / annotation_count / meshes | runtime + 自测 |

## 5. 开放问题

- test-device 示例包目前混入索引的"示例厅"——发布版需要 `--exclude` 过滤参数（下轮小改）；
- 展陈与图鉴共用同一索引：exhibit_host 的布局只列 4 台黎明厅设备，与索引 12 台的厅聚合关系在引擎侧由 ExhibitIndex.hall_of 反查，已写；实机时按 first_boot 清单 #5/#6 一并验证。

## 6. TASK-36 两份总收尾 + 01 线本轮完成标注

- 36-A：体检向导三模式实测（MISSING×2 阻断路径、JSON 输出、网关自检 OK）；
- 36-B：图鉴索引生成 + 0 差异验证 + 引擎工具类；
- 01 线本轮（任务 36）完成。