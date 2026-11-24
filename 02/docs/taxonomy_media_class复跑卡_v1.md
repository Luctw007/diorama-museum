# taxonomy 与 media_class 覆盖率复跑卡 v1

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-J（02 线）。定位：目录扩至 1583 条 + 第三/四批新条目候选，复跑 taxonomy_check + media_class
> 覆盖率统计。**不改 taxonomy.md 原文、不改目录 jsonl。**

## 一、taxonomy_check 复跑日志

```
对账：共 1583 条目录，落在官方树内 1583 条，孤路径 0 条
  大分类级孤儿：0 项
  中分类级孤儿：0 项
  子分类级孤儿：0 项
退出码 rc=0
```

## 二、media_class 覆盖率统计

- media_class 枚举 9 值：`disk / firmware / cartridge / tape / cd / dvd / card / app_package / none`（含 none，
  无 mechanical）。
- 覆盖率：目录 1583 条 media_class 均落在 9 值枚举内（CC-10「有值」口径，none 为正式合法值），**覆盖 100%**
  （无越界值）。

## 三、orphans / 未分类条目清单

**无孤儿**：1583 条全部落在官方树内（大/中/子分类级孤儿均 0），taxonomy_orphans.md 已生成（空清单）。

## 四、第四批 10 台候选条目 media_class 归类建议（不落 jsonl）

- 计算机（C）：Amstrad CPC 464/Atari 800/Manchester Mark 1/IBM 701/Osborne 1/TI-99/4A（6 台，media_class 无
  或 none）。
- 通讯与移动（M）：Nokia 5110/Motorola StarTAC/Palm III/BlackBerry 850（4 台）。

## 五、红线自查

零联网零下载；覆盖率/orphans 以复跑实值为准（1583/1583、孤儿 0）；只改 02 目录、未改 taxonomy.md、未改 jsonl。
