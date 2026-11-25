# TASK-310-P 完成报告 · CPS-1 街机基板低模样板 glTF

> 任务 310-P（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，轻量线。

## 一、交付物清单

`content/cps1/assemblies/` 下 5 件低模 gltf + MESHES.md：mainboard(104) / cpu(104) / graphics_chip(104) / sound_module(104) / rom_board(104)。识别件 rom_board（ROM 板插拔，对齐「换卡不停机」叙事），已在 MESHES.md 标注。本包**未建** meta.json / annotations / 目录 jsonl。

## 二、验收日志与退出码

**1. 低模自证**（5 件，顶点 100-4000，纯色 0–1）：

```
cps1  mainboard      vertices=104 materials=5
cps1  cpu            vertices=104 materials=5
cps1  graphics_chip  vertices=104 materials=5
cps1  sound_module   vertices=104 materials=5
cps1  rom_board      vertices=104 materials=5
```

**2. 门禁只读复测**：`verify_all.py --daily --no-ref-hard` → 结果通过（本轮产包统一复核，rc=0）。

**3. 改动清单自证**：本任务只新增 `cps1/assemblies/` 5 件 gltf + MESHES.md + 本完成报告。

## 三、与任务书的漂移

1. **cpu/graphics_chip/sound_module 初版 96 顶点不足 100**：IC 模板 12→13 盒，补至 104 顶点，满足「>100 且 <4000」。
2. 其余 node_id 与 305-M 建模任务卡清单一致，无其它漂移。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图，街机 ROM/BIOS 只清单级引用（FR-E3）；未建 meta/annotations/目录 jsonl；只改 05 目录，未动 01/02/03/04 线。
