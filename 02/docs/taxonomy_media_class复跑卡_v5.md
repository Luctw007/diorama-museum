# taxonomy 与 media_class 月度复跑卡 v5（全落树 + 孤儿 0 + 覆盖 100%）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-322-J（02 线）。定位：滚动 317-J v4，复跑 taxonomy_check + media_class 覆盖率。**不改 taxonomy.md、不改 jsonl。**

## 一、taxonomy 复跑（实测）

`taxonomy_check.py` → 对账 1583 条目录，落在官方树内 1583 条，**孤路径 0 条**（大分类级孤儿 0 + 中分类级孤儿 0 +
子分类级孤儿 0），rc=0。

## 二、media_class 覆盖率统计

media_class 枚举 9 值含 none，目录条目 1583 行 media_class 覆盖 **100%**（无空值）。

## 三、新增包归树归类复核

门禁 69 内容包（新增 donkey-kong-arcade/galaga-arcade/nintendo-3ds/psvita）全部归树无孤儿，游戏机新增包归
G-AC/G-HH 子类无异常。

## 四、基线健康声明

taxonomy 全落树、孤儿 0、media_class 覆盖 100%，基线健康。

## 五、红线自查

零联网零下载；不改 taxonomy.md、不改 jsonl；覆盖率/orphans 以复跑实值为准；只改 02 目录。
