# 第三批 allocate 实跑就绪核验卡 v1（演练 vs 实跑差异 + 最终执行清单）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-317-B（02 线）。定位：在 312-B 五组 dry-run 演练基础上，核对演练与实跑环境的差异，产出
> 「点头 + 01 登记后一键执行」的最终执行清单。**不实际 allocate、不改 registry、不改 jsonl。**

## 一、演练 vs 实跑差异核对表

| 核对项 | dry-run 演练假设 | 实跑环境实测 | 差异 |
|---|---|---|---|
| py -3.7 可用性 | 假设可用 | 本机 `py -3.7` 可执行 id_registry.py 只读对账（rc=0） | 无差异 |
| registry 写入路径 | `docs/catalog/registry.jsonl` | 实测 registry 1583 条、无重号、续号连续 | 无差异 |
| 续号实算重算 | 最大号 +1 | C-MF 84 / C-PC 208 / C-WS 54 / C-EC 13 / M-PD 69（实测） | 无差异 |
| 幂等与回滚预判 | allocate 幂等、重复执行不重号 | id_registry 续号以实算为准，重复执行会重号——需先查重再落 | 已登记风险 |

## 二、5 组命令最终执行顺序清单（点头 + 01 登记后）

| 顺序 | 分组 | 续号起点 | 目录归属 | 反链回填责任 |
|---|---|---|---|---|
| 1 | C-MF-000085 | 84+1 | 大型机厅 | 03 线（产包时回填 device_id + status=done） |
| 2 | C-PC-000209~214 | 208+1（6 台） | 个人计算机厅 | 03 线 |
| 3 | C-WS-000055 | 54+1 | 工作站厅 | 03 线 |
| 4 | C-EC-000014 | 13+1 | 黎明厅（early-computer） | 03 线 |
| 5 | M-PD-000070 | 69+1 | 通讯与移动（Newton） | 03 线 |

## 三、触发声明

**仅「点头 + 01 登记」双前置齐备后一键执行**；本卡只做就绪核验，不落地。

## 四、不 allocate / 不改 registry 声明

本卡未写 registry、未 allocate、未改任何 jsonl；幂等风险（重复执行会重号）已如实登记，实跑前需先查重。

## 五、红线自查

零联网零下载；只核验、不实际 allocate、不改 registry、不改 jsonl；续号以 id_registry 实算为准；只改 02 目录。
