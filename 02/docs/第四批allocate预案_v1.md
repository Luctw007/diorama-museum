# 第四批 allocate 预案 v1（目录 id 在册现状 + BlackBerry 850 缺失）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-C（02 线）。定位：参照第三批 allocate 预案（267-A）为第四批 10 台出 id 分配预案。**纯文档
> 预案，不 allocate、不改 jsonl。**
>
> 关键口径差异：第四批目录条目**已真号在册**（planned，如 C-PC-000059），与第三批「占位 0xx 待 allocate」
> 不同——第四批**无需 allocate 目录 id**，产包时直接回填 device_id + status=done。

## 一、9 台在册台 device_id + 目录 id 现状表

| # | 设备 | 目录 id（已真号在册） | 包 id 建议 | 是否需要 allocate |
|---|---|---|---|---|
| 1 | Amstrad CPC 464 | C-PC-000059 | amstrad-cpc464 | 否（已真号） |
| 2 | Atari 800 | C-PC-000027 | atari-800 | 否 |
| 3 | Nokia 5110 | M-MP-000016 | nokia-5110 | 否 |
| 4 | Motorola StarTAC | M-MP-000027 | motorola-startac | 否 |
| 5 | Manchester Mark 1 | C-EC-000011 | manchester-mark-1 | 否 |
| 6 | IBM 701 | C-MF-000001 | ibm-701 | 否 |
| 7 | Osborne 1 | C-PC-000115 | osborne-1 | 否 |
| 8 | TI-99/4A | C-PC-000063 | ti-994a | 否 |
| 9 | Palm III | M-PD-000005 | palm-iii | 否 |

> 无冲突核对：9 个 device_id 均 kebab-case（`^[a-z0-9]+(-[a-z0-9]+)*$`），与现有 47 包 device_id 无重复；
> 9 个目录 id 均已真号在册（planned），不与 registry 撞号。

## 二、BlackBerry 850 缺失行

**BlackBerry 850 目录条目缺失**（292-H 实测「未找到」），如实标「待 03 线补录或调整代表机」，本预案不补造。

## 三、目录归属预案

- 计算机大类 v2：Amstrad CPC 464 / Atari 800 / Manchester Mark 1 / IBM 701 / Osborne 1 / TI-99/4A（6 台）。
- 通讯与移动 v3：Nokia 5110 / Motorola StarTAC / Palm III（3 台）+ BlackBerry 850（待补录）。

## 四、allocate 执行清单（用户点头后，本任务不执行）

第四批**无需 allocate 目录 id**（已真号在册）；产包时仅执行目录回填：`device_id=<包 id>` + `status=done`。
BlackBerry 850 须先补录条目（302-D 预案）或调整代表机，再回填。

## 五、依赖声明

**点头前不执行**任何回填/allocate；本卡只列预案，不 allocate、不改 jsonl、不产包。

## 六、红线自查

零联网零下载；目录 id 在册/缺失以 292-H 实测为准；只改 02 目录、未 allocate、未改 jsonl、未产包。
