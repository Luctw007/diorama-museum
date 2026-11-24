# TASK-290-B 完成报告 · PlayStation 2 产包准备卡（31 号）

> 任务 290-B（05 线）· 完成日期：2026-11-24。
> 执行账号：05 游戏机线；只改 `D:\work\05\` 目录，纯准备卡，不产包、不改 jsonl、不建模。

## 一、交付物清单

| 文件 | 要点 |
|---|---|
| `console-batch1/31_PS2产包准备卡.md` | 4500 字节（≥2500）；产包字段清单（id=playstation-2/era=2000/category=game-console/manufacturer=Sony + emulator 保守 none/media_hint=cd_rom + components 拆分建议）+ 目录条目方案（G-HC-000065）+ PS2 BIOS/ROM 红线 + 需核实清单 |

## 二、验收日志与退出码

**1. 门禁只读复测**（`verify_all.py --daily --no-ref-hard`，本机无 `py -3.7`，改用 python 3.13）：

```
===== 验收汇总（58 项） =====
结果：58/58 通过
RC=0
```

**2. 准备卡自证**：
- 字节数：`4500` 字节（>2500）✅
- 四节标题命中：①产包字段清单（逐件口径）②目录条目方案 ③PS2 BIOS/ROM 红线 ④「需核实」清单 ✅
- 「需核实」条数：`8` 条 ✅

**3. 改动清单自证**：本任务只新增 `31_PS2产包准备卡.md` + 本完成报告，未新增/修改任何 gltf、meta.json、annotations、目录 jsonl。

## 三、与任务书的漂移

1. **media_hint=cd_rom**：任务书要求「按 schema 枚举取最接近值（PS2 为 DVD-ROM 介质，参照 29 号 GD-ROM→cd_rom 降级先例处理并标注）」，已按此取 `cd_rom` 代指，并在准备卡「media_hint 口径说明」显式标注。
2. **components 拆分建议**：任务书未强制 components 数量，本卡补充 4 件拆分（emotion_engine / gs / ram / iop），对齐 sega-dreamcast 4 components 先例，属合理补充。
3. 其余字段对齐 29 号 Dreamcast 准备卡体例，无其它漂移。

## 四、红线自证

未产包、未改目录 jsonl、未建模；未下载 ROM/BIOS/二进制/贴图，PS2 BIOS/ROM 只清单级引用（emulator 保守 none）；尺寸/配色/参数无来源一律标 [需核实]（8 处）；只改 05 目录，未动 01/02/03/04 线。
