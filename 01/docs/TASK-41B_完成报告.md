# TASK-41B 完成报告（docs/TASK-41B_完成报告.md）

> 01 线 · 2026-11-04 · 任务：多厅展陈布局（见 任务41-B）。
> 本报告含 TASK-41 两份总收尾，01 线本轮（任务 41-A/B）完成。

## 1. 交付物

| 文件 | 说明 |
|---|---|
| `godot/content/exhibit_mainframe.json` | 大型机厅 4 台（system360/pdp8/pdp11/vax11），22×14 |
| `godot/content/exhibit_personal.json` | 个人机厅 3 台（commodore64/apple-ii/ibm5150），18×12 |
| `godot/content/exhibit_console.json` | 游戏机厅 2 台（atari-2600/famicom），18×12 |
| `scripts/layout_check.py`（改） | `--all` 总检 + 跨厅重复 WARN（允许+提示）；边界优先取布局内 width/depth |
| `godot/scripts/exhibit_host.gd`（改） | `switch_hall()` + `hall_files` 导出清单（319 行） |

## 2. 运行日志（原文）

```text
$ python scripts/layout_check.py --all
=== exhibit_console.json     OK（设备 2 台）
=== exhibit_dawn.json        OK（设备 4 台）
=== exhibit_mainframe.json   OK（设备 4 台）
=== exhibit_personal.json    OK（设备 3 台）
--all 完成：4 份布局                     → rc=0

$ python scripts/layout_check.py <负例：未知 id>
  [FAIL] L-02 devices[0].id=not-exist 不在 godot/content（现有 14 项）
布局校验失败：1 条                       → rc=1（负例回归正确）
```

## 3. 迭代记录（2 轮）

1. 轮 1：新布局的厅尺寸（22×14/18×12）超出校验器缺省 20×12 边界 → 误报；改为"布局内 width/depth 优先"（schema 可选字段语义补全）；
2. 轮 2：--all 模式补齐跨厅重复检测——实测当前四厅 apple-ii 只出现在个人机厅（与黎明厅 demo 无重复），WARN 路径以代码就绪、未触发记录在案。

## 4. 静态自查（switch_hall/hall_files，同 21-B 体例）

| # | 项 | 结果 |
|---|---|---|
| 1 | hall_files 四文件名与 godot/content 实际文件一致 | ✓ |
| 2 | switch_hall = clear_devices → load_layout → spawn_devices 顺序正确 | ✓ |
| 3 | PackedStringArray 导出属性为 Godot 4.x 合法类型 | ✓ |
| 4 | 布局 JSON 与 exhibit_layout_spec §1 schema 一致（含新增 width/depth） | ✓ layout_check 实测 |

## 5. 四厅坐标系汇总表

| 厅 | 尺寸 | 台数 | 站位（x, z 档） |
|---|---|---|---|
| 黎明厅 | 20×12 | 4 | -7 ~ 6.5 |
| 大型机厅 | 22×14 | 4 | -9 ~ 7.5（机柜纵深大，间距最宽） |
| 个人机厅 | 18×12 | 3 | -6 ~ 5.5 |
| 游戏机厅 | 18×12 | 2 | -5.5 ~ 1.5（预留 MD/街机位） |

## 6. TASK-41 两份总收尾 + 01 线本轮完成标注

- 41-A：门禁数据驱动化——13 包自动发现、15/15 等价全绿、单包过滤可用；
- 41-B：四厅布局齐备（13 台全部有位）+ 切厅能力 + `--all` 总检；
- 01 线本轮（任务 41）完成。