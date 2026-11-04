# 03 · 街机 ROM / BIOS 清单级引用专节

> 任务：TASK-95A（05 线 1/2 · 轻量）· 只做清单级引用（文件名/定位指引），**不下载任何 ROM/BIOS**。
> 红线 FR-E3：**本仓永不下载、永不随附——用户在 `slots/` 自备，位置见 `slots/README.md`**。
> 用途：为街机暗房区将来接 MAME/FinalBurn 铺平"找资源"路径。

## 一、Neo Geo

> 红线提示：本仓永不下载、永不随附——用户在 slots/ 自备，位置见 slots/README.md。

| 名称 | 位置 / 文件命名惯例 | 所属驱动 / 基板 | 许可需核实 |
|---|---|---|---|
| neogeo.zip（BIOS 包） | 含 `sp-s2.sp1`、`asia-s3.rom`、`sfix.sfix` 等 BIOS 文件，置 MAME `roms/` 目录 | MAME neogeo 驱动 | 需核实 |
| MVS 卡带 ROM | 按 MAME 软列表命名：`kof94.zip`、`mslug.zip`、`samsho.zip` 等，置 `roms/neogeo/` | MAME neogeo 驱动 | 需核实 |
| FBN 卡带 ROM | FinalBurn Neo 有独立 ROM set 命名，与 MAME 软列表口径不完全一致，需按 FBN 版本对齐 | FinalBurn Neo | 需核实 |
| unibios（Universe BIOS） | 替换 BIOS 文件，置于 neogeo.zip 内或独立载入 | neogeo 驱动 | 需核实 |

## 二、CPS-1 / CPS-2

> 红线提示：本仓永不下载、永不随附——用户在 slots/ 自备，位置见 slots/README.md。

| 名称 | 位置 / 文件命名惯例 | 所属驱动 / 基板 | 许可需核实 |
|---|---|---|---|
| qsound / qsound_hle | CPS-2 的 QSound DSP 固件（`qsound.zip`）或高电平模拟（qsound_hle，无需固件） | CPS-2 | 需核实 |
| CPS-1 主 CPU 程序 ROM | 按游戏 zip 命名：`sf2.zip`（街霸 II）、`ffight.zip`（快打旋风）等 | CPS-1 | 需核实 |
| CPS-2 游戏 ROM | `sfa2.zip`（街霸 Alpha 2）、`19xx.zip`、`msh.zip` 等，需配套 QSound 固件 | CPS-2 | 需核实 |
| CPS-3 游戏 ROM | `sfiii.zip`、`jojo.zip` 等，光盘 + 主板 ROM 组合 | CPS-3 | 需核实 |

## 三、杂项街机（竖屏弹幕 / 格斗代表座）

> 红线提示：本仓永不下载、永不随附——用户在 slots/ 自备，位置见 slots/README.md。

| 名称 | 位置 / 文件命名惯例 | 所属驱动 / 基板 | 许可需核实 |
|---|---|---|---|
| Cave 弹幕（竖屏） | `ddonpach.zip`（怒首领蜂）、`espgal.zip`（圣战之翼）等，竖屏基板 CV1000 | Cave CV1000 | 需核实 |
| 彩京弹幕（竖屏） | `s1945.zip`（打击者 1945）、`s1945ii.zip` 等 | Psikyo SH-2 | 需核实 |
| SNK 格斗 | `kof94.zip`~`kof2003.zip`、`samsho.zip` 等（与 Neo Geo 卡带同源） | Neo Geo MVS | 需核实 |
| Capcom 格斗 | `sf2.zip`、`sfa2.zip`、`sfiii.zip` 等（与 CPS 系同源） | CPS-1/2/3 | 需核实 |

## 四、与 80-A v2 的交叉引用

本专节是 `emu-eco/02_手持街机光盘机_模拟器生态_v2.md` 街机节的**资源定位补充**——v2 街机行（MAME 街机驱动集 / FinalBurn Neo / Supermodel / Demul / Raine）指向本专节，本专节提供各驱动的 ROM/BIOS 清单级命名惯例与红线提示。二者合并，构成"选型（v2）+ 找资源（本专节）"的完整街机接入路径。
