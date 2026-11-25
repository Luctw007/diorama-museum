# id_registry 月度审计 2027-01（对账 + 续号连续性）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-312-L（02 线）。定位：307-L 后 2027-01 审计。**不改 registry、不 allocate、不改 jsonl。**

## 一、registry 对账

registry 1583 条 = 目录使用 1583 条（未使用 0），无重号、无越界（catalog_ref REF-03 1583=1583）。

## 二、前缀最大号清单（实测 2026-11-26）

| 前缀 | 最大序号 | 条目数 |
|---|---|---|
| C-MF | 84 | 84 |
| C-PC | 208 | 208 |
| C-WS | 54 | 54 |
| C-EC | 13 | 13 |
| M-PD | 69 | 69 |
| M-MP | 171 | 171 |
| G-HC | 95 | 95 |
| G-AC | 250 | 250 |

> 注：游戏机目录（05 线 G-xx）独立管理，不入 02 线 registry；registry 条数自第三批备料后无变化。

## 三、续号连续性判定

各前缀序号连续（无跳号）、无重号、无越界。

## 四、与第三批 allocate 预案序号对账

C-MF-000085 / C-PC-000209~214 / C-WS-000055 / C-EC-000014 / M-PD-000070（续接 = 最大号 +1）——与 registry
现状**一致（无漂移）**。

## 五、红线自查

零联网零下载；对账数字以 registry 实值为准；不改 registry、不 allocate；只改 02 目录。
