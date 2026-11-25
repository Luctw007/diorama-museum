# 第三批 allocate 命令演练卡 v1（5 组 dry-run 演练）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-312-B（02 线）。定位：307-B 预检后对 5 组 allocate 命令做 dry-run 演练。**不实际 allocate、
> 不改 registry、不改 jsonl。**

## 一、5 组命令逐条 dry-run 演练记录（续号 = 最大号 +1）

| 分组 | 命令 | 假设续号起点 | 与 307-B 预检 |
|---|---|---|---|
| C MF 1 | allocate C MF 1 | C-MF-000085（84+1） | 一致 |
| C PC 6 | allocate C PC 6 | C-PC-000209~214（208+1） | 一致 |
| C WS 1 | allocate C WS 1 | C-WS-000055（54+1） | 一致 |
| C EC 1 | allocate C EC 1 | C-EC-000014（13+1） | 一致 |
| M PD 1 | allocate M PD 1 | M-PD-000070（69+1） | 一致 |

## 二、演练结论

假设执行结果与 307-B 预检**一致、无撞号**（续号 = 各前缀最大号 +1，落在 registry 现有 1583 条之后）。

## 三、触发声明

**仅点头 + 01 登记后执行**；本卡只 dry-run 演练、不落地。

## 四、不落地声明

本卡未写 registry、未 allocate、未改 jsonl。

## 五、红线自查

零联网零下载；只 dry-run、不 allocate、不改 registry；续号以 id_registry 实算为准；只改 02 目录。
