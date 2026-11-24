# TASK-305-E 完成报告 · Microsoft Xbox 低模样板 glTF

> 任务 305-E（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，轻量线。

## 一、交付物清单

`content/xbox/assemblies/` 下 8 件低模 gltf + MESHES.md：

| 件 | node_id | 顶点数 | 材质数 |
|---|---|---|---|
| chassis | chassis | 120 | 5 |
| dvd_drive | dvd_drive | 104 | 6 |
| mainboard | mainboard | 104 | 5 |
| power_supply | power_supply | 104 | 6 |
| controller_port | controller_port | 104 | 6 |
| hard_drive | hard_drive | 104 | 6 |
| controller | controller | 104 | 6 |
| ethernet_port | ethernet_port | 104 | 5 |

- 节点名 = node_id，baseColorFactor 纯色无贴图（12 种材质全 0–1）。
- 识别件：dvd_drive（托盘弹出）、controller（Xbox 手柄），已在 MESHES.md 标注。
- 本包**未建** meta.json / annotations / 目录 jsonl（对齐 290-A 口径）。

## 二、验收日志与退出码

**1. 门禁只读复测**（`verify_all.py --daily --no-ref-hard`，本机无 `py -3.7`，改用 python 3.13）：

```
===== 验收汇总（60 项） =====
结果：60/60 通过
RC=0
```

**2. 低模自证**（8 件，顶点 100-4000，base64 解码 == byteLength，配色 0–1）：

```
chassis            vertices=120 materials=5 base64=OK bcf=OK
controller         vertices=104 materials=6 base64=OK bcf=OK
controller_port    vertices=104 materials=6 base64=OK bcf=OK
dvd_drive          vertices=104 materials=6 base64=OK bcf=OK
ethernet_port      vertices=104 materials=5 base64=OK bcf=OK
hard_drive         vertices=104 materials=6 base64=OK bcf=OK
mainboard          vertices=104 materials=5 base64=OK bcf=OK
power_supply       vertices=104 materials=6 base64=OK bcf=OK
ALL OK
```

**3. 改动清单自证**：本任务只新增 `xbox/assemblies/` 8 件 gltf + MESHES.md + 本完成报告，未改其它文件。

## 三、与任务书的漂移

1. **部件取 8 件**（任务书建议 5-8 件）：按 39 号预研卡取 8 件（含硬盘仓、以太网接口，体现 Xbox 内置硬盘 + 以太网特色）。
2. **node_id 用 ethernet_port**（任务书写「通风口」）：按 39 号预研卡第 8 件取 ethernet_port（以太网接口），通风口并入 chassis 示意；按「以预研卡为准」处理。
3. 其余对齐 305-E 任务书，无其它漂移。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图；尺寸/配色沿用 39 号预研卡、无源处标 [需核实]；未建 meta.json / annotations / 目录 jsonl；只改 05 目录，未动 01/02/03/04 线。
