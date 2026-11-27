# 第四批目录 id 在册复核卡 v3（9 台真号在册 + BlackBerry 850 缺失）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-322-D（02 线）。定位：滚动 317-D v2，对第四批 9 台目录 id 逐条只读再复核 + BlackBerry 850 缺失。
> **不 allocate、不改 jsonl、不产包、不代补录。**

## 一、9 台目录 id 逐条在册复核表（实测）

| # | 设备 | 目录 id（实测） | status | device_id | 判定 |
|---|---|---|---|---|---|
| 1 | Amstrad CPC 464 | C-PC-000059 | planned | None | 在册 |
| 2 | Atari 800 | C-PC-000027 | planned | None | 在册 |
| 3 | Nokia 5110 | M-MP-000016 | planned | None | 在册 |
| 4 | Motorola StarTAC | M-MP-000027 | planned | None | 在册 |
| 5 | Manchester Mark 1 | C-EC-000011 | planned | None | 在册 |
| 6 | IBM 701 | C-MF-000001 | planned | None | 在册 |
| 7 | Osborne 1 | C-PC-000115 | planned | None | 在册 |
| 8 | TI-99/4A | C-PC-000063 | planned | None | 在册 |
| 9 | Palm III | M-PD-000005 | planned | None | 在册 |

## 二、撞号 / 重复判定

9 个目录 id 均真号在册、无撞号；对应 device_id（amstrad-cpc-464/atari-800/nokia-5110/motorola-startac/
manchester-mark-1/ibm-701/osborne-1/ti-99-4a/palm-iii）kebab-case 无重复。

## 三、BlackBerry 850 缺失复核

通讯目录现有 8 条其他 BlackBerry 型号，**无 BlackBerry 850 条目**，M-MP-000172 仍未入册（补录责任 03 线）。

## 四、口径确认

**第四批无需 allocate**——9 台目录 id 已真号在册，点头后产包直接回填 device_id + status=done；
BlackBerry 850 补录后第四批才 10/10 收官。

## 五、红线自查

零联网零下载；只读复核、不 allocate、不改 jsonl、不产包、不代 03 线补录；目录 id 以实值为准；只改 02 目录。
