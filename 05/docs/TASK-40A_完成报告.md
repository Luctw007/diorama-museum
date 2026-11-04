# TASK-40A 完成报告（FC 建模任务卡 · 游戏机线第二台建模开产）

> 任务：TASK-40A（05 线 1/2）· 里程碑 M1 · 前置：任务 35 完成。
> 依据：famicom 包、console-batch1/02_FamicomNES.md、02 线 v0.3 定稿 / v0.4 音频章草案。
> 完成日期：2026-11-03。

---

## 一、交付物清单与字数统计（实测 CJK）

| 文件 | 内容 | 字数（实测） |
|---|---|---|
| `console-batch1/08_FC_建模任务卡.md` | 6 张卡 + 13 附录 | 5514（≥5500 达标） |
| `console-batch1/09_FC_建模验收清单.md` | 人工核对表 | 796 |

## 二、任务卡清单表

| 卡片 | 目标文件 | LOD1 预算 | 关键约束 |
|---|---|---|---|
| 卡片 1 top_shell | `assemblies/top_shell.gltf` | ≤8000 | 红白撞色分界 + 中部条纹槽 |
| 卡片 2 bottom_shell | `assemblies/bottom_shell.gltf` | ≤5000 | 通风槽数、铭牌只做凹槽 |
| 卡片 3 cart_bay | `assemblies/cart_bay.gltf` | ≤2000 | 60 针触点、−Y 竖直插卡 |
| 卡片 4 cartridge | `assemblies/cartridge.gltf` | ≤3000 | 60 针金手指、标签区、剖面 |
| 卡片 5 mainboard | `assemblies/mainboard.gltf` | ≤10000 | 2A03/2C02 PPU 位、丝印 |
| 卡片 6 controllers | `assemblies/controllers.gltf` | ≤4000 | 十字键凹槽、AB 圆点、两枚手柄、线缆走向 |

## 三、与 Atari 卡片的体例一致性说明

本卡（08/09 号）与 Atari 版（06/07 号）**体例完全一致**：卡片七字段（目标文件/三档预算/贴图清单/枢轴/命名表/验收核对行/错误vs正确示例）同构、MR-01~04 规则同源、两次验收点 + 三关验收流程同构、贴图后缀/命名红线同构。差异仅三处：装配体（FC vs Atari）、枢轴重点（FC 手柄连线 vs Atari 开关拨动轴）、预算口径（见下）。

## 四、开放问题

1. **预算口径修正（重要）**：本卡按 02 线 **v0.3 定稿 §5.2**（LOD0 50k / LOD1 20k / LOD2 8k 单装配体）给预算；此前 atari-2600 06 号卡（TASK-35A）对齐的是 v0.3 **草案**（LOD1 2k 量级，top_shell 观察 800）。27-B 定稿已把三档修正为 20k 量级，**atari 06 号卡需回填修正**（建议后续任务把 atari 06 号卡预算从 800 量级上调到 8000 量级）。
2. **BlastEm 许可**：40-B 任务书"BlastEm(MIT)"有误，BlastEm 实际为 **GPL-3.0**（MIT 是其 MCP wrapper），已在 40-B 预研中纠正。
3. **v0.4 音频章**：FC 的 APU 五声道音效属后续音频资产任务，本卡只登记衔接关系（附录 H），不产出音频。
4. **整机三围**：占位盒 0.15×0.08×0.21 m 为近似值，正式建模前实机复核。

## 五、TASK-40 两份收尾标注

本份（40-A）完成；40-B（游戏机厅第二批预研 MD/SFC/GB）见 `console-batch2/06_完成报告.md` 的总收尾。
