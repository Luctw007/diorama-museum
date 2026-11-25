# taxonomy 与 media_class 月度复跑卡 v3

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-312-J（02 线）。定位：307-J v2 后月度复跑 v3。**不改 taxonomy.md、不改 jsonl。**

## 一、taxonomy 复跑日志

```
对账：共 1583 条目录，落在官方树内 1583 条，孤路径 0 条
  大分类级孤儿 0 / 中分类级孤儿 0 / 子分类级孤儿 0
退出码 rc=0
```

## 二、media_class 覆盖率统计

9 值（disk/firmware/cartridge/tape/cd/dvd/card/app_package/none）含 none、无 mechanical；1583 条全落在枚举内，
覆盖 100%。

## 三、新增包归树归类复核

游戏机新包（gba→G-HH 手持、switch/wii/xbox-360/ps3→G-HC 家用机、pac-man-arcade→G-AC 街机）均归游戏机大类、
落官方树；cps1/sega-system16 两 WIP 未入目录、无归类异常。

## 四、基线健康声明

taxonomy 全落树、孤儿 0、覆盖率 100%，基线健康。

## 五、红线自查

零联网零下载；覆盖率/orphans 以复跑实值为准；只改 02 目录、未改 taxonomy.md、未改 jsonl。
