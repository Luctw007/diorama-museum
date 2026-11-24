# C-3 sign_ref 回填复核卡 v1（三线键对齐现状 + 回填清单状态）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-P（02 线）。定位：C-3 sign_ref 权威 id 方案（197-B）+ 回填清单（207-A）已发，本卡复核三线
> 键对齐现状。**不回填、不改存量键。**

## 一、三线存量键对齐现状

- 03 线目录：条目用 `device_id`（无 sign_ref 字段），零迁移。
- 03 线图鉴短卡：来源列用证据编号 S-xxx（非目录 id）。
- 04 线图鉴短卡/annotations：annotations 不改存量（tour 引用时组合两级）。
- tour 台本 sign_ref：待 tour 台本落地时按清单执行回填。

## 二、回填清单逐条状态

| 清单项 | 状态 |
|---|---|
| 03 线零迁移（目录/图鉴短卡已用目录 id） | 已满足（197-B 结论不变） |
| annotations 不改存量（组合两级） | 已满足（不改） |
| tour 台本 sign_ref 回填 | **待 tour 台本落地** |

## 三、tour 台本落地时回填动作重申

不改 annotations 存量；tour 引用时组合两级（`sign_ref` 指向目录 id + 标注 id）；回填按 207-A 清单执行。

## 四、结论

前置仍未满足（tour 台本未落地），C-3 不勾销、不定义 sign_ref。

## 五、红线自查

零联网零下载；不回填、不改存量键、不改 03/04 线；只改 02 目录。
