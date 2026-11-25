# TASK-315-A 完成报告 · Wii U 低模样板预研卡

> 任务 315-A（05 线）· 完成日期：2026-11-26。
> 执行账号：05 游戏机线；只改 05 目录，预研卡纯文案零联网。

## 一、交付物清单

`docs/research/console-batch1/49_WiiU低模样板预研卡.md`（新增，字节数 ≥2500）。五要素齐全：
1. 7 件拆分：console / gamepad / disc_drive / mainboard / power_supply / controller_port / flash_storage；
2. 尺寸/配色参数表均标 [需核实]；
3. 识别件：gamepad=GamePad 触屏手柄、disc_drive=吸入式光驱；
4. BIOS/ROM 红线仅清单级引用；
5. 目录预告 G-HC-000078 回填不新建。
另：Wii U 专用光盘 media_hint 降级 cd_rom 已预告标注；Cemu 候选 [需核实]。

## 二、验收日志与退出码

1. 门禁：`verify_all.py --daily --no-ref-hard` 全过 RC=0（73/73，本机 py -3.7）；`catalog_ref` FAIL 0（内容包 65 个，REF-01~04 全 0）。
2. 预研卡自证：字节数 ≥2500 ✅；五要素齐 ✅；识别件 gamepad/disc_drive 命中 ✅；media_hint 降级 cd_rom 预告标注 ✅；Cemu 候选 [需核实] ✅。
3. 改动清单自证：仅新增本 md + 完成报告；未改 gltf/meta/annotations/目录 jsonl。

## 三、与任务书的漂移

与任务书 315-A 无漂移。7 件拆分、尺寸/配色 [需核实]、识别件口径、目录预告 G-HC-000078、media_hint 降级预告均与预算一致，未额外新增目录条目、未提前建 gltf。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；BIOS/ROM 仅清单级引用、无实体文件引用；只改 05 目录；未改 gltf/meta/annotations/目录 jsonl；目录条目仅预告回填、不新建；未动 01/02/03/04 线。
