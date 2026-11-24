# TASK-305-A 完成报告 · Nintendo GameCube 低模样板 glTF

> 任务 305-A（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，轻量线。

## 一、交付物清单

`content/gamecube/assemblies/` 下 8 件低模 gltf + MESHES.md：

| 件 | node_id | 顶点数 | 材质数 |
|---|---|---|---|
| chassis | chassis | 120 | 5 |
| disc_drive | disc_drive | 104 | 6 |
| mainboard | mainboard | 104 | 5 |
| power_supply | power_supply | 104 | 6 |
| controller_port | controller_port | 104 | 6 |
| memory_card_slot | memory_card_slot | 104 | 6 |
| controller | controller | 104 | 5 |
| expansion_slot | expansion_slot | 104 | 6 |

- 节点名 = node_id，baseColorFactor 纯色无贴图（11 种材质全 0–1）。
- 识别件：disc_drive（光盘盖开合）、controller（GameCube 手柄），已在 MESHES.md 标注。
- 本包**未建** meta.json / annotations / 目录 jsonl（对齐 290-A 口径）。

## 二、验收日志与退出码

**1. 门禁只读复测**（`verify_all.py --daily --no-ref-hard`，本机无 `py -3.7`，改用 python 3.13）：

```
===== 验收汇总（59 项） =====
结果：59/59 通过
RC=0
```

**2. 低模自证**（8 件，顶点 100-4000，base64 解码 == byteLength，配色 0–1）：

```
chassis            vertices=120 materials=5 base64=OK bcf=OK
controller         vertices=104 materials=5 base64=OK bcf=OK
controller_port    vertices=104 materials=6 base64=OK bcf=OK
disc_drive         vertices=104 materials=6 base64=OK bcf=OK
expansion_slot     vertices=104 materials=6 base64=OK bcf=OK
mainboard          vertices=104 materials=5 base64=OK bcf=OK
memory_card_slot   vertices=104 materials=6 base64=OK bcf=OK
power_supply       vertices=104 materials=6 base64=OK bcf=OK
ALL OK
```

**3. 改动清单自证**：本任务只新增 `gamecube/assemblies/` 8 件 gltf + MESHES.md + 本完成报告，未改其它文件。

## 三、与任务书的漂移

1. **node_id 用 disc_drive**（任务书第 3 章写「miniDVD 光驱」未指定 node_id）：按 32 号预研卡 node_id 取 disc_drive，与「光驱」对应；提手并入 chassis（任务书将「提手」单列为元素，但 32 号预研卡部件分解中提手含于 chassis，按「以预研卡为准」处理）。
2. **8 件拆分对齐 32 号预研卡**（chassis/disc_drive/mainboard/power_supply/controller_port/memory_card_slot/controller/expansion_slot）：任务书第 3 章列的「主机/光驱/提手/面板/底部扩展槽/手柄/光驱盖/卡槽盖」为描述性元素，实际拆分以预研卡为准。
3. 其余对齐 305-A 任务书，无其它漂移。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；尺寸/配色沿用 32 号预研卡、无源处标 [需核实]；未建 meta.json / annotations / 目录 jsonl；只改 05 目录，未动 01/02/03/04 线。
