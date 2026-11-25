# 第四批目录 id 在册复核卡 v1（9 台在册 + BlackBerry 850 缺失）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-312-D（02 线）。定位：307-D 后聚焦第四批目录 id 在册性复核。**不 allocate、不改 jsonl、不产包、
> 不代补录。**

## 一、9 台目录 id 逐条在册复核表

| # | 设备 | 目录 id（真号在册） | 包 id 建议 | 撞号 |
|---|---|---|---|---|
| 1 | Amstrad CPC 464 | C-PC-000059 | amstrad-cpc464 | 无 |
| 2 | Atari 800 | C-PC-000027 | atari-800 | 无 |
| 3 | Nokia 5110 | M-MP-000016 | nokia-5110 | 无 |
| 4 | Motorola StarTAC | M-MP-000027 | motorola-startac | 无 |
| 5 | Manchester Mark 1 | C-EC-000011 | manchester-mark-1 | 无 |
| 6 | IBM 701 | C-MF-000001 | ibm-701 | 无 |
| 7 | Osborne 1 | C-PC-000115 | osborne-1 | 无 |
| 8 | TI-99/4A | C-PC-000063 | ti-994a | 无 |
| 9 | Palm III | M-PD-000005 | palm-iii | 无 |

## 二、撞号/重复判定

9 个 device_id 均 kebab-case（`^[a-z0-9]+(-[a-z0-9]+)*$`）、与现有 59 包 device_id 无重复；9 个目录 id 均真号
在册（planned）、无撞号。

## 三、BlackBerry 850 缺失复核

**仍缺失**（M-MP-000172 未入册，通讯目录无 BlackBerry 850 条目）。

## 四、口径确认

**无需 allocate**——第四批目录 id 已真号在册（planned），点头后产包直接回填 device_id + status=done。

## 五、红线自查

零联网零下载；只读复核、不 allocate、不改 jsonl、不代补录；目录 id 在册/缺失以实值为准；只改 02 目录。
