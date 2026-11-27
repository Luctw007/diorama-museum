# TASK-325-F 完成报告 · 游戏手柄产包准备卡

> 任务 325-F（05 线）· 完成日期：2026-11-27。
> 执行账号：05 游戏机线；只改 `\\DESKTOP-2IDAL09\work\05\`，准备卡零联网。

## 一、交付物清单

`apple-ii/29_游戏手柄产包准备卡.md`（6218 字节 >2500）：五节标题命中；id=apple-ii-gamepad / era=1980 / category=input-device / media_hint=none 显式说明 / output_sinks 无（纯输入）；assemblies body/d_pad/buttons/cable/shoulder；components 建议 d_pad_switch/button_switch/shoulder_switch/cable_wire（注明不与装配体 id 重复）；P-IN-000008 实扫回填方案（不落地）。

## 二、验收日志与退出码

**1. 统一门禁口径**：`verify_all.py --daily --no-ref-hard` 全过 RC=0（本轮 325 六包落地后全量复跑，本机 py -3.7，镜像模式）；`catalog_ref` FAIL 0（REF-01~04 全 0）。

**2. 本任务自证**：字节数 6218 >2500 ✅；五节标题命中 ✅；id=apple-ii-gamepad 命中 ✅；media_hint=none 显式说明 ✅；output_sinks 无（纯输入）✅；assemblies 五件 ✅。

## 三、与任务书的漂移

与 325-F 任务书无漂移：仅准备卡登记方案，未产包、未改 jsonl。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；只改 05 目录；未产包未改 jsonl；另存不覆盖底本；未动 01/02/03/04 线。
