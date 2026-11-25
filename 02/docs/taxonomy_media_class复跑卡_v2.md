# taxonomy 与 media_class 月度复跑卡 v2

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-307-J（02 线）。定位：302-J v1 后月度复跑。**不改 taxonomy.md、不改 jsonl。**

## 一、taxonomy_check 复跑日志

```
对账：共 1583 条目录，落在官方树内 1583 条，孤路径 0 条
  大分类级孤儿：0 项 / 中分类级孤儿：0 项 / 子分类级孤儿：0 项
退出码 rc=0
```

## 二、media_class 覆盖率统计

9 值（disk/firmware/cartridge/tape/cd/dvd/card/app_package/none）含 none、无 mechanical；1583 条 media_class
全落在枚举内，覆盖 100%（无越界值）。

## 三、orphans 清单

0 孤儿（1583 条全落官方树），taxonomy_orphans.md 空清单。

## 四、第四批/新增条目归类复核

第四批 10 台（计算机 6 + 通讯 4，BlackBerry 850 待补录）；游戏机新包 gamecube/xbox 归游戏机与手持大类
（G-HC-000066/067），均落官方树。

## 五、红线自查

零联网零下载；覆盖率/orphans 以复跑实值为准（1583/1583、孤儿 0）；只改 02 目录、未改 taxonomy.md、未改 jsonl。
