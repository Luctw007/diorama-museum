# TASK-320-P 完成报告 · Apple II 游戏外设低模样板预研卡

> 任务 320-P（05 线）· 完成日期：2026-11-26。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，纯预研零联网。

## 一、交付物清单

`apple-ii/26_游戏外设低模样板预研卡.md`（9003 字节 >2500）。摇杆节（base / stick / button / cable / base_plate）+ 手柄节（body / d_pad / buttons / cable / shoulder）各五要素齐；接口红线接 Apple II game_port；目录预告 P-IN-000013 / P-IN-000008 回填不新建。

## 二、验收日志与退出码

**1. 门禁全量复核**：`verify_all.py --daily --no-ref-hard` → 全过 RC=0（77/77，本机 py -3.7，镜像模式）；`catalog_ref` FAIL 0（内容包 69 个，REF-01~04 全 0）。

**2. 本任务自证**：预研卡 9003 字节 >2500 ✅；摇杆节五要素（base / stick / button / cable / base_plate）✅；手柄节五要素（body / d_pad / buttons / cable / shoulder）✅；接口红线接 Apple II game_port ✅。

**3. 改动清单自证**：本任务只新增预研卡 + 本完成报告，未改 jsonl、未新建目录条目。

## 三、与任务书的漂移

无漂移。摇杆节、手柄节五要素、接口红线、目录预告均对齐任务书 320-P。

## 四、红线自证

纯预研、零联网、未改 jsonl；目录 P-IN-000013 / P-IN-000008 回填不新建；未下载 ROM/BIOS/二进制/贴图；只改 05 目录；未动 01/02/03/04 线。
