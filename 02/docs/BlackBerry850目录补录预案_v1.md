# BlackBerry 850 目录条目补录预案 v1

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-D（02 线）。定位：第四批候选 BlackBerry 850 目录条目缺失（292-H 实测「未找到」，仅存 8 条
> 其他 BlackBerry 型号），本预案产出补录方案，**不新建条目、不改 jsonl**，供 03 线补录或调整代表机。

## 一、缺失事实复核

292-H 实测：通讯与移动大类目录仅有 BlackBerry 5810/6230/8700/7230/7100/Pearl 8100/Curve 8300/Bold 9000
（8 条 M-MP 条目），**无 BlackBerry 850**。第四批候选 10 台 = 9/10 在册 + 1 缺失（BlackBerry 850）。

## 二、补录方案

| 项 | 方案 |
|---|---|
| device_id | `blackberry-850`（kebab-case，与研究卡 13 号口径一致） |
| 目录 id 续接 | M-MP 前缀当前最大号 **171**（292-E 实测）→ 补录 `M-MP-000172` |
| 归属文件 | `03/repo/docs/catalog/通讯与移动大类_目录_v3.jsonl` |
| status | planned（产包后转 done） |

## 三、与现有 BlackBerry 8 条区分声明

现有 8 条（5810/6230/8700/7230/7100/Pearl 8100/Curve 8300/Bold 9000）为后世 BBOS 机型，与 BlackBerry 850
（1999 年首代双向寻呼机，M-MP）**不同机型**，不重复、不覆盖；补录 850 不与 8 条撞号。

## 四、调整代表机备选

若用户决定不补录 BlackBerry 850，改按研究卡口径另定代表机（如 BlackBerry 5810 作为后世 BBOS 代表），
由 03 线在第四批定案前闭环——本预案不代裁决。

## 五、责任分派

03 线补录条目（M-MP-000172）+ 回填 device_id/status；02 线登记预案 + 产包时供验收口径；本预案不执行。

## 六、红线自查

零联网零下载；缺失事实以 292-H 实测为准，不臆造条目存在；只改 02 目录、未新建条目、未改 jsonl。
