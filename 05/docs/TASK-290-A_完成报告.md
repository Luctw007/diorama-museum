# TASK-290-A 完成报告 · PlayStation 2 低模样板 glTF

> 任务 290-A（05 线）· 完成日期：2026-11-24。
> 执行账号：05 游戏机线；只改 `D:\work\05\` 目录，轻量线。

## 一、交付物清单

`content/playstation-2/assemblies/` 下 8 件低模 gltf + MESHES.md：

| 件 | node_id | 顶点数 | 材质数 |
|---|---|---|---|
| chassis | chassis | 120 | 5 |
| dvd_drive | dvd_drive | 104 | 6 |
| mainboard | mainboard | 104 | 5 |
| power_supply | power_supply | 104 | 6 |
| controller_port | controller_port | 104 | 6 |
| memory_card_slot | memory_card_slot | 104 | 6 |
| controller | controller | 104 | 5 |
| expansion_bay | expansion_bay | 104 | 6 |

- 节点名 = node_id，baseColorFactor 纯色无贴图（11 种材质全 0–1）。
- 识别件：dvd_drive（吸入式光驱）、controller（DualShock 2），已在 MESHES.md 标注。
- 本包**未建** meta.json / annotations / 目录 jsonl（对齐 280-A 口径）。

## 二、验收日志与退出码

**1. 门禁只读复测**（`verify_all.py --daily --no-ref-hard`，本机无 `py -3.7`，改用 python 3.13）：

```
===== 验收汇总（58 项） =====
结果：58/58 通过
RC=0
```

**2. 顶点数自检**（8 件逐件 POSITION accessor count，均 >100 且 <4000）：

```
chassis            vertices=120
dvd_drive          vertices=104
mainboard          vertices=104
power_supply       vertices=104
controller_port    vertices=104
memory_card_slot   vertices=104
controller         vertices=104
expansion_bay      vertices=104
```

**3. baseColorFactor 自检**（每件 ≥1 条，数值 0–1，base64 解码 == byteLength）：

```
chassis            vertices=120 materials=5 base64=OK bcf=OK
controller         vertices=104 materials=5 base64=OK bcf=OK
controller_port    vertices=104 materials=6 base64=OK bcf=OK
dvd_drive          vertices=104 materials=6 base64=OK bcf=OK
expansion_bay      vertices=104 materials=6 base64=OK bcf=OK
mainboard          vertices=104 materials=5 base64=OK bcf=OK
memory_card_slot   vertices=104 materials=6 base64=OK bcf=OK
power_supply       vertices=104 materials=6 base64=OK bcf=OK
ALL OK
```

**4. 改动清单自证**：本任务只新增 `playstation-2/assemblies/` 8 件 gltf + MESHES.md + 本完成报告，未改其它文件。

## 三、与任务书的漂移

1. **node_id 用 expansion_bay**（任务书第 3 章写 expansion_slot）：30 号预研卡部件表第 8 件 node_id 为 `expansion_bay`，任务书第 8 章约定「以 30 号为准」，故取 expansion_bay（文件名与节点名一致），在报告回写此差异。
2. 其余 7 件 node_id 与任务书一致；配色沿用 30 号预研卡配色表（11 种材质，含 disc 光盘银面）。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；尺寸/配色沿用 30 号预研卡、无源处标 [需核实]；未建 meta.json / annotations / 目录 jsonl；只改 05 目录，未动 01/02/03/04 线。
