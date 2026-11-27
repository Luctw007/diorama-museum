# TASK-325-T 完成报告 · 新产包过闸复核与反链终检卡

> 任务 325-T（05 线）· 完成日期：2026-11-27。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，纯复核零联网。

## 一、交付物清单

`console-batch1/58_新产包过闸复核与反链终检卡.md`：六包 device_id 回填终检全命中无 null（frogger-arcade↔G-AC-000010、ms-pac-man-arcade↔G-AC-000016、apple-ii-joystick↔P-IN-000013、apple-ii-gamepad↔P-IN-000008、game-boy-color↔G-HH-000021、neo-geo-pocket-color↔G-HH-000023）；validate 复跑 92/92/74/74/80/80 全 FAIL 0、model_check FAIL 0、catalog_ref FAIL 0；百科反链 + THIRD_PARTY 红线（街机 FR-E3、掌机/外设 BIOS/ROM 或接口红线）逐包命中；annotations 无孤儿；残项清单为空；未改任何产包文件/jsonl。

## 二、验收日志与退出码

**1. 门禁**：`verify_all.py --daily --no-ref-hard` 全过 RC=0（325 六包落地后全量复跑，本机 py -3.7，镜像模式）；`catalog_ref` FAIL 0（REF-01~04 全 0）。

**2. 终检卡自证**：六包 device_id 回填终检全命中无 null ✅；validate 复跑 92/92/74/74/80/80 全 FAIL 0 ✅；model_check FAIL 0 ✅；catalog_ref FAIL 0 ✅；百科反链 + THIRD_PARTY 红线逐包命中 ✅；annotations 无孤儿 ✅；残项清单为空 ✅。

**3. 改动清单自证**：仅新增终检卡 + 本报告，未改任何产包文件、未改 jsonl。

## 三、与任务书的漂移

对齐 325-T 任务书，无漂移。本任务为过闸复核，只读不改产包，符合“复核不改包”约定。

## 四、红线自证

纯复核、零联网；未下载 ROM/BIOS/二进制/贴图；未改任何产包文件、未改 jsonl；只改 05 目录；复核结果实测登记、不臆造；未动 01/02/03/04 线。
