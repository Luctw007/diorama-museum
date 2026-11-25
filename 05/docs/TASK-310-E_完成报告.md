# TASK-310-E 完成报告 · Wii 产包准备卡（46 号）

> 任务 310-E（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，纯文档准备卡。

## 一、交付物清单

`console-batch1/46_Wii产包准备卡.md`：产包字段清单（id=wii/era=2006/manufacturer=Nintendo/media_hint=cd_rom + components 拆分建议 broadway/hollywood/ram/cd_motor）+ 目录条目方案（G-HC-000074）+ BIOS/ROM 红线 + 需核实清单。

## 二、验收日志与退出码

**1. 门禁只读复测**：`verify_all.py --daily --no-ref-hard` → 本轮产包统一复核 rc=0（本机无 py -3.7 用 python 3.13）。

**2. 准备卡自证**：字节数 >2500 ✅；五节标题命中 ✅；「需核实」条数充足 ✅；media_hint 降级显式标注 ✅

**3. 改动清单自证**：本任务只新增 `46_Wii产包准备卡.md` + 本完成报告。

## 三、与任务书的漂移

1. **media_hint=cd_rom**（DVD 无枚举降级）：按任务书显式标注。
2. **components 拆分建议**（broadway/hollywood/ram/cd_motor）：对齐 GameCube 先例。
3. 其余对齐 310-E 任务书，无其它漂移。

## 四、红线自证

未产包、未改目录 jsonl、未建模；未下载 ROM/BIOS/二进制/贴图，Wii 固件/ROM 只清单级引用；参数无来源标 [需核实]；只改 05 目录，未动 01/02/03/04 线。
