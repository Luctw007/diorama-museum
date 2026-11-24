# catalog_ref 四巡复跑归档 v1（连续四轮 FAIL 0）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-302-K（02 线）。定位：catalog_ref 长期 FAIL 0（292-F 三巡后），本卡续做四巡归档 + 镜像积压期
> 稳定性声明。**不改脚本、不改目录 jsonl。**

## 一、四巡复跑日志（REF-01~04）

```
第 1 巡：REF-01 悬空 0 / REF-02 反链缺失 0 / REF-03（registry 1583 = 目录使用 1583）/ REF-04 形态非法 0 → FAIL 0
第 2 巡：REF-01 0 / REF-02 0 / REF-03（1583=1583）/ REF-04 0 → FAIL 0
第 3 巡：REF-01 0 / REF-02 0 / REF-03（1583=1583）/ REF-04 0 → FAIL 0
第 4 巡：REF-01 0 / REF-02 0 / REF-03（1583=1583）/ REF-04 0 → FAIL 0
（四巡 rc=0）
```

## 二、稳定性声明

**连续四轮全 FAIL 0**（REF-01~04 全 0），catalog_ref 稳定通过。

## 三、已知时序差登记

四包（sega-saturn/n64/dreamcast/ps2）镜像未同步**不影响 catalog_ref 判定**——catalog_ref 扫目录 jsonl +
registry 台账（非扫镜像 content），四包反链均已在共享盘侧 done，故 REF-02 缺失 0。

## 四、红线自查

零联网零下载；不改脚本、不改 jsonl；REF 四查以复跑实值为准；只改 02 目录。
