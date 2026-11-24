# id_registry 月度审计 2026-11b（续号连续性 + 无重号复核）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-M（02 线）。定位：id_registry 11 月续做审计（续号连续性、前缀最大号、无重号复核）。
> **不改 registry、不 allocate、不改目录 jsonl。**

## 一、registry 全量对账

```
registry 1583 条 = 目录使用 1583 条（未使用 0 条），无重号、无越界
（catalog_ref REF-03：registry 1583 / 目录使用 1583，未使用 0）
```

## 二、各前缀最大号清单（实测 2026-11-24）

| 前缀 | 中分类 | 最大序号 | 条目数 |
|---|---|---|---|
| C-MF | 大型机 | 84 | 84 |
| C-PC | 个人机 | 208 | 208 |
| C-WS | 工作站 | 54 | 54 |
| C-EC | 早期计算机 | 13 | 13 |
| M-PD | PDA | 69 | 69 |
| M-MP | 手机 | 171 | 171 |
| G-HC | 游戏机 | 95 | 95 |
| G-AC | 街机 | 250 | 250 |

## 三、续号连续性核对

各前缀序号连续（1~最大号无跳号，registry 由 id_registry allocate/rebuild 维护，续号纳入「台账 ∪ 目录已用 id」）。

## 四、第三/四批 allocate 预案序号与 registry 现状对账

- 第三批：C-MF-000085/C-PC-000209~214/C-WS-000055/C-EC-000014/M-PD-000070（续接 = 最大号 +1，未 allocate）。
- 第四批：目录 id 已真号在册（planned，无需 allocate），BlackBerry 850 待补录 M-MP-000172。

## 五、红线自查

零联网零下载；对账数字以 registry 实值为准；不改 registry、不 allocate；只改 02 目录。
