# TASK-325-Q 完成报告 · arcade-10 序列总索引 v1

> 任务 325-Q（05 线）· 完成日期：2026-11-27。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，纯索引零联网。

## 一、交付物清单

`arcade-10/arcade-10序列总索引_v1.md`（3989 字节 >2500）：参数卡/键位/巡检/建模/准备/预研卡（DK/Galaga、Frogger/Ms. Pac-Man）全数登记；产包 done 实测 7 台逐台列 device_id（space-invaders-arcade/pac-man-arcade/donkey-kong-arcade/galaga-arcade/frogger-arcade/ms-pac-man-arcade/neo-geo-mvs）；基板线与经典名作线分组清晰；未改 jsonl。

## 二、验收日志与退出码

**1. 门禁**：`verify_all.py --daily --no-ref-hard` 全过 RC=0（325 六包落地后全量复跑，本机 py -3.7，镜像模式）；`catalog_ref` FAIL 0（REF-01~04 全 0）。

**2. 总索引自证**：字节数 3989 >2500 ✅；六类卡全数登记 ✅；done 实测 7 台逐台 device_id 命中 ✅；基板线与经典名作线分组清晰 ✅。

**3. 改动清单自证**：仅新增 v1 + 本报告，未改 jsonl。

## 三、与任务书的漂移

对齐 325-Q 任务书，无漂移。

## 四、红线自证

纯索引、零联网；未改 jsonl、未新增目录条目/设备编号；未下载 ROM/BIOS/二进制/贴图；逐台实测、不臆造；只改 05 目录；未动 01/02/03/04 线。
