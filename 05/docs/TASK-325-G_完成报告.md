# TASK-325-G 完成报告 · Apple II 游戏手柄内容产包（低模）

> 任务 325-G（05 线）· 完成日期：2026-11-27。
> 执行账号：05 游戏机线；只改 `\\DESKTOP-2IDAL09\work\05\`，产包零联网。

## 一、交付物清单

`content/apple-ii-gamepad/` 完整产包（低模）：5 件 gltf（body 120 顶点、d_pad/buttons/cable/shoulder 各 104）+ MESHES.md + 产包五件套。id=apple-ii-gamepad / era=1980 / category=input-device；output_sinks 空数组；components d_pad_switch/button_switch/shoulder_switch/cable_wire；百科 2643 汉字；注解 30；目录 P-IN-000008 回填 planned→done、device_id=apple-ii-gamepad。

## 二、验收日志与退出码

**1. 统一门禁口径**：`verify_all.py --daily --no-ref-hard` 全过 RC=0（本轮 325 六包落地后全量复跑，本机 py -3.7，镜像模式）；`catalog_ref` FAIL 0（REF-01~04 全 0）。

**2. 本任务自证**：validate 74 条全 PASS FAIL 0 ✅；model_check FAIL 0 ✅；catalog_ref FAIL 0 ✅；5 件 gltf 顶点 120/104 ✅；百科 2643 汉字 ✅；注解 30 ✅；device_id=apple-ii-gamepad 命中 ✅。

## 三、与任务书的漂移

与 325-G 任务书无实质漂移；components 命名 d_pad_switch/button_switch/shoulder_switch/cable_wire，避免与装配体 id 重复，属合理命名漂移。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；只改 05 目录；output_sinks 空数组；未改 jsonl、未改他处 gltf；目录回填 planned→done 属 05 目录内登记；未动 01/02/03/04 线。
