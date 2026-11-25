# TASK-315-D 完成报告 · NDS 与 PSP 掌机低模样板预研卡

> 任务 315-D（05 线）· 完成日期：2026-11-26。
> 执行账号：05 游戏机线；只改 05 目录，预研卡纯文案零联网。

## 一、交付物清单

`docs/research/console-batch2/23_NDS与PSP掌机低模样板预研卡.md`（新增，双机合卡，字节数 ≥2500）。五要素齐全：
1. NDS 节 6 件：chassis / top_screen / touch_screen / cartridge_slot / shoulder_buttons / battery_compartment；PSP 节 6 件：chassis / screen / umd_drive / control_buttons / shoulder_buttons / battery_compartment；
2. 尺寸/配色参数表均标 [需核实]；
3. 识别件：NDS=touch_screen 下屏触控 + cartridge_slot 卡带插拔 + chassis 翻盖开合；PSP=umd_drive UMD 仓开合 + chassis 横置宽屏握持；
4. BIOS/ROM 红线仅清单级引用；
5. 目录预告 G-HH-000033 / G-HH-000034 回填不新建。
另：NDS media_hint=cartridge、PSP media_hint 降级 cd_rom 已预告标注；melonDS/DeSmuME、PPSSPP 候选 [需核实]。

## 二、验收日志与退出码

1. 门禁：`verify_all.py --daily --no-ref-hard` 全过 RC=0（73/73，本机 py -3.7）；`catalog_ref` FAIL 0（内容包 65 个，REF-01~04 全 0）。
2. 预研卡自证：字节数 ≥2500 ✅；五要素齐 ✅；双机识别件命中 ✅；media_hint（cartridge/cd_rom 降级）预告标注 ✅；melonDS/DeSmuME、PPSSPP 候选 [需核实] ✅。
3. 改动清单自证：仅新增本 md + 完成报告；未改 gltf/meta/annotations/目录 jsonl。

## 三、与任务书的漂移

与任务书 315-D 无漂移。双机 6+6 件拆分、识别件口径、目录预告 G-HH-000033/G-HH-000034、media_hint 口径均与预算一致，未额外新增目录条目、未提前建 gltf。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；BIOS/ROM 仅清单级引用、无实体文件引用；只改 05 目录；未改 gltf/meta/annotations/目录 jsonl；目录条目仅预告回填、不新建；未动 01/02/03/04 线。
