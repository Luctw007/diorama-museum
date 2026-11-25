# TASK-310-B 完成报告 · Xbox 360 产包准备卡（45 号）

> 任务 310-B（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，纯文档准备卡。

## 一、交付物清单

`console-batch1/45_Xbox360产包准备卡.md`：产包字段清单（id=xbox-360/era=2005/manufacturer=Microsoft/media_hint=cd_rom + components 拆分建议）+ 目录条目方案（G-HC-000073）+ BIOS/ROM 红线 + 需核实清单。

## 二、验收日志与退出码

**1. 门禁只读复测**：`verify_all.py --daily --no-ref-hard` → 本轮产包统一复核 rc=0（本机无 py -3.7 用 python 3.13）。

**2. 准备卡自证**：字节数 >2500 ✅；五节标题命中（字段清单/目录方案/BIOS 红线/需核实/红线自检）✅；「需核实」条数充足 ✅；media_hint 降级显式标注 ✅

**3. 改动清单自证**：本任务只新增 `45_Xbox360产包准备卡.md` + 本完成报告，未改 gltf/meta/annotations/目录 jsonl。

## 三、与任务书的漂移

1. **media_hint=cd_rom**（DVD-ROM 无枚举降级）：按任务书显式标注。
2. **components 拆分建议**（xenon/xenos/ram/cd_motor）：对齐 Xbox 先例。
3. 其余对齐 310-B 任务书，无其它漂移。

## 四、红线自证

未产包、未改目录 jsonl、未建模；未下载 ROM/BIOS/二进制/贴图，Xbox 360 固件/ROM 只清单级引用；参数无来源标 [需核实]；只改 05 目录，未动 01/02/03/04 线。
