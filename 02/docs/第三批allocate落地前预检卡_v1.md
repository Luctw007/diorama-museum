# 第三批 allocate 落地前预检卡 v1（5 组前缀只读对账）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-307-B（02 线）。定位：allocate 落地前只读预检——5 组前缀最大号对账 + 撞号判定。**不实际 allocate、
> 不改 registry、不改 jsonl。**

## 一、5 组前缀当前最大号只读对账表（实测 2026-11-25）

| 分组 | 前缀 | 当前最大号 | 条目数 | 续号起点 |
|---|---|---|---|---|
| 大型机 | C-MF | 84 | 84 | C-MF-000085 |
| 个人机 | C-PC | 208 | 208 | C-PC-000209~214 |
| 工作站 | C-WS | 54 | 54 | C-WS-000055 |
| 早期计算机 | C-EC | 13 | 13 | C-EC-000014 |
| PDA | M-PD | 69 | 69 | M-PD-000070 |

## 二、续号起点核对 + 撞号风险判定

5 组续号起点与 297-B 执行卡起点**一致**，与 registry 现有 1583 条**无撞号**（续接 = 最大号 +1，落在各前缀
最大号之后）；撞号风险判定 = **无**。

## 三、allocate 命令清单（5 条，仅列不执行）

```
python tools/index/id_registry.py allocate C MF 1
python tools/index/id_registry.py allocate C PC 6
python tools/index/id_registry.py allocate C WS 1
python tools/index/id_registry.py allocate C EC 1
python tools/index/id_registry.py allocate M PD 1
```

## 四、触发声明

**仅限「用户点头 + 01 线登记」后执行**；本卡只读预检、不实际 allocate。

## 五、红线自查

零联网零下载；只读对账、不 allocate、不改 registry；序号以 id_registry 实算为准；只改 02 目录。
