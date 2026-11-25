# TASK-310-J 完成报告 · Switch 低模样板 glTF

> 任务 310-J（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，轻量线。

## 一、交付物清单

`content/nintendo-switch/assemblies/` 下 8 件低模 gltf + MESHES.md：tablet(104) / dock(104) / joycon_left(104) / joycon_right(104) / mainboard(104) / battery(104) / cartridge_slot(104) / screen(112)。识别件 dock（入坞）、joycon_left/joycon_right（滑轨卡合）、cartridge_slot（卡带插拔），已在 MESHES.md 标注。本包**未建** meta.json / annotations / 目录 jsonl。

## 二、验收日志与退出码

**1. 低模自证**（8 件，顶点 100-4000，纯色 0–1）：

```
tablet           vertices=104 materials=4
dock             vertices=104 materials=6
joycon_left      vertices=104 materials=6
joycon_right     vertices=104 materials=6
mainboard        vertices=104 materials=5
battery          vertices=104 materials=5
cartridge_slot   vertices=104 materials=6
screen           vertices=112 materials=6
```

**2. 门禁只读复测**：`verify_all.py --daily --no-ref-hard` → 结果通过（本轮产包统一复核，rc=0）。

**3. 改动清单自证**：本任务只新增 `nintendo-switch/assemblies/` 8 件 gltf + MESHES.md + 本完成报告。

## 三、与任务书的漂移

1. **dock/joycon/battery/screen 初版顶点不足 100**：dock 12→13 盒、joycon 11→13 盒、battery 11→13 盒、screen 8→14 盒，均补至 ≥104 顶点，满足「>100 且 <4000」。
2. 其余 node_id 与任务书清单一致，无其它漂移。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图，Switch 固件/ROM 只清单级引用；未建 meta/annotations/目录 jsonl；只改 05 目录，未动 01/02/03/04 线。
