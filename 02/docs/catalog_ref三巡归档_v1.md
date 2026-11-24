# catalog_ref 三巡复跑归档 v1（连续三轮 FAIL 0 + 稳定性声明）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-292-F（02 线）。定位：catalog_ref 长期 FAIL 0，本卡做三巡复跑归档（连续三轮复跑日志 + 稳定性声明）。
> 只改 02 目录，纯复跑 + 文档。

## 一、三巡复跑日志（原始输出）

```
第 1 巡：REF-01 悬空包引用 0 / REF-02 反链缺失 0 / REF-03 台账漂移（registry 1583 = 目录使用 1583）/
        REF-04 形态非法 0 → FAIL 0（rc=0）
第 2 巡：REF-01 0 / REF-02 0 / REF-03（1583=1583）/ REF-04 0 → FAIL 0（rc=0）
第 3 巡：REF-01 0 / REF-02 0 / REF-03（1583=1583）/ REF-04 0 → FAIL 0（rc=0）
```

## 二、稳定性声明

**三巡全 FAIL 0**（REF-01~04 连续三轮全 0），catalog_ref 稳定通过。

## 三、已知时序差登记

05 线新产包（sega-saturn/n64/sega-dreamcast）反链均在产包同轮闭环（265-A/275-A/285-A），故镜像视图
catalog_ref 不报 REF-02 缺失；共享盘 05 线视图的 catalog_ref 亦由反链同轮回填保持 0（镜像未同步不影响
catalog_ref 判定，因 catalog_ref 扫目录+registry 台账，非扫镜像 content）。

## 四、红线自查

零联网零下载；不改脚本；只改 02 目录、未产包。
