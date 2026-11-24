# A-4 mechanical 子类开题预研卡 v1（定义草案 + 支撑条目 + 触发条件）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-Q（02 线）。定位：A-4 mechanical 子类（media_class 扩展）待机械设备开题，本卡出开题预研。
> **不落 taxonomy/media_class 枚举、不改目录 jsonl、不改校验器代码。**

## 一、mechanical 子类定义草案

- 是否入 media_class 枚举：**草案倾向入**（机械设备有真实条目后，`mechanical` 作为第 10 值加入枚举，与 `none`
  并列；`none` 为「无介质」，`mechanical` 为「机械介质/传动」）。
- 与 none 的关系：`mechanical` 与 `none` **互斥**（none = 无介质类设备；mechanical = 机械部件设备），不合并。
- 判定边界：设备含机械走线/传动/机柜机械结构等，media_class 记 `mechanical`。

## 二、支撑条目梳理

目录内机械设备/走线/传动条目：**无真实条目**（大型机机柜/磁带机机械传动等尚未开题、无真实条目支撑），
如实标「无支撑条目」。

## 三、开题触发条件

≥1 台机械设备包 0 FAIL 过闸（03 线产含机械部件的包）+ 目录有真实条目支撑。

## 四、结论

前置未满足（无机械设备条目、枚举无 mechanical），**不提前定义 mechanical 子类**（对齐 1.x 待办「前置不满足
不下发」）。

## 五、红线自查

零联网零下载；支撑条目以目录实值为准（无支撑如实标）；不落枚举、不改 jsonl；只改 02 目录。
