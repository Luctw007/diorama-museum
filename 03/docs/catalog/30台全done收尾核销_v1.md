# 30 台全 done 收尾核销 v1

> 03 线 TASK-163-B 交付。30 台定案表最后收尾：TRS-80 Model I 转 done + 定案表状态同步，达成 30 台全 done、30 台唯一状态源一致。

## 〇、结论

**30 台定案表全部 done。** 03 线 23 台（计算机目录 20 台 + 通讯目录 3 台）本轮 trs80 转正后全 done；05 线 7 台（Apple II + 游戏机 6 台）账在 05 线台账，03 只登记引述不改 05 文件。

## 一、30 台逐行 done 记账表

| # | 机型 | 厅 | 状态 | device_id | 归属 |
|---|---|---|---|---|---|
| 1 | ENIAC | 计算机黎明厅 | done | eniac | 03 |
| 2 | Manchester Baby | 计算机黎明厅 | done | manchester-baby | 03 |
| 3 | EDSAC | 计算机黎明厅 | done | edsac | 03 |
| 4 | EDVAC | 计算机黎明厅 | done | edvac | 03 |
| 5 | IBM System/360 | 大型机与小型机厅 | done | system360 | 03 |
| 6 | PDP-8 | 大型机与小型机厅 | done | pdp8 | 03 |
| 7 | PDP-11/70 | 大型机与小型机厅 | done | pdp11 | 03 |
| 8 | VAX-11/780 | 大型机与小型机厅 | done | vax11 | 03 |
| 9 | Apple II | 个人计算机厅 | done | apple-ii | 05（账在 05） |
| 10 | Commodore PET 2001 | 个人计算机厅 | done | pet2001 | 03 |
| 11 | TRS-80 Model I | 个人计算机厅 | done | trs80-model1 | 03（本轮转正） |
| 12 | IBM PC 5150 | 个人计算机厅 | done | ibm5150 | 03 |
| 13 | BBC Micro | 个人计算机厅 | done | bbcmicro | 03 |
| 14 | Commodore 64 | 个人计算机厅 | done | commodore64 | 03 |
| 15 | ZX Spectrum | 个人计算机厅 | done | zx-spectrum | 03 |
| 16 | Macintosh 128K | 个人计算机厅 | done | macintosh128k | 03 |
| 17 | Atari ST | 个人计算机厅 | done | atari-st | 03 |
| 18 | Amiga 500 | 个人计算机厅 | done | amiga500 | 03 |
| 19 | Atari 2600 | 游戏机厅 | done | atari-2600 | 05 |
| 20 | Famicom | 游戏机厅 | done | famicom | 05 |
| 21 | Sega Mega Drive | 游戏机厅 | done | sega-md | 05 |
| 22 | Game Boy | 游戏机厅 | done | game-boy | 05 |
| 23 | Neo Geo MVS | 游戏机厅 | done | neo-geo-mvs | 05 |
| 24 | SFC | 游戏机厅 | done | sfc | 05 |
| 25 | Motorola DynaTAC 8000X | 手机厅 | done | dynatac-8000x | 03 |
| 26 | iPhone 初代 | 手机厅 | done | iphone | 03 |
| 27 | Commodore VIC-20 | 个人计算机厅 | done | vic20 | 03 |
| 28 | Sharp X68000 | 个人计算机厅 | done | x68000 | 03 |
| 29 | NeXT Computer | 工作站 | done | next | 03 |
| 30 | Palm Pilot 1000 | 通用设备厅 | done | palm-pilot | 03 |

## 二、TRS-80 Model I 收尾动作记录

- **内容深度对标**（对标 done 标杆 next≈2526 字 / palm-pilot≈2548 字 / flow≥10）：trs80-model1 现为 **flow 13 条、encyclopedia 2,557 汉字**，已达 done 标准。
- **补齐动作**：**零动作**（对标后确认已达标，无需补 flow 标注或 encyclopedia）。
- **转正**：目录条目 `C-PC-000033` `status` 由 `package` → `done`（其余字段不动）。
- **结构基线**：`validate.py` 78 PASS / 0 FAIL（既有，未改动）。

## 三、定案表状态同步 diff

- §二 第 11 行 TRS-80 Model I：`package` → `done`。
- §四 第 8 行 TRS-80 Model I：`package` → `done`。
- §四 第 25–30 行：DynaTAC 8000X / iPhone 初代 / VIC-20 / X68000 / NeXT / Palm Pilot：`待产包` → `done`。
- 附备注：`> 状态字段已于 163-B 同步（2026-11-06）…30 台全部 done。`
- 未增删机型、未改机型/年代/厅归属。

## 四、目录版本唯一性复查

- 计算机目录本次仅改 `C-PC-000033` 的 status 字段，未动版本号、未新增文件；活跃位置仍仅「计算机 v2 + 通讯 v3」单一版本，符合《目录版本治理条款_v1》（163-A）。
- 门禁复测见下。

## 五、验收证据

- `catalog_check.py`（计算机 v2 + 通讯 v3）：**CC-02 唯一 0 FAIL · CC-01~08 全过**（810 条）。
- `catalog_ref_check.py`：**REF-01~04 全 0 · FAIL 0**（内容包 30 个）。
