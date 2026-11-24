# TASK-305-F 完成报告 · Xbox 产包准备卡（40 号）

> 任务 305-F（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，纯文档准备卡。

## 一、交付物清单

| 文件 | 要点 |
|---|---|
| `console-batch1/40_Xbox产包准备卡.md` | 产包字段清单（id=xbox/era=2001/category=game-console/manufacturer=Microsoft + emulator 保守 none/media_hint=cd_rom + components 拆分建议）+ 内置硬盘表达说明 + 目录条目方案（G-HC-000067）+ BIOS/ROM 红线 + 需核实清单 |

## 二、验收日志与退出码

**1. 门禁只读复测**（`verify_all.py --daily --no-ref-hard`，本机无 `py -3.7`，改用 python 3.13）：

```
===== 验收汇总（60 项） =====
结果：60/60 通过
RC=0
```

**2. 准备卡自证**：字节数 >2500 ✅；五节标题命中（字段清单/目录方案/BIOS 红线/需核实/红线自检）✅；「需核实」条数充足 ✅

**3. 改动清单自证**：本任务只新增 `40_Xbox产包准备卡.md` + 本完成报告，未改 gltf、meta、annotations、目录 jsonl。

## 三、与任务书的漂移

1. **内置硬盘用 hard_drive 件表达、不引入 storage 字段**（任务书「内置硬盘 storage 字段」）：schema 无 storage 字段，为避免超字段校验失败，硬盘以 assembly 件 `hard_drive` 表达，已在准备卡「内置硬盘表达说明」显式标注。
2. **media_hint=cd_rom**（任务书「dvd_rom 无枚举则降级 cd_rom 并标注」）：按此取 cd_rom 代指，已标注。
3. 其余对齐 305-F 任务书，无其它漂移。

## 四、红线自证

未产包、未改目录 jsonl、未建模；未下载 ROM/BIOS/二进制/贴图，Xbox BIOS/ROM 只清单级引用；参数无来源标 [需核实]；只改 05 目录，未动 01/02/03/04 线。
