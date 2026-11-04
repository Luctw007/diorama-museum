# TASK-45A 完成报告（Sega MD 设备包生产 · 游戏机厅第三台）

> 任务：TASK-45A（05 线 1/2）· 里程碑 M1 · 前置：任务 40 完成。
> 依据：console-batch2/01_SegaMD.md。
> 完成日期：2026-11-04。

---

## 一、交付物清单与校验结果

| 文件 | 内容 | 状态 |
|---|---|---|
| `content/sega-md/meta.json` | era=1988、localized、10 装配体 + 6 元器件（68000/Z80/VDP/YM2612/SN76489/ROM） | ✅ |
| `content/sega-md/runtime.json` | blastem 1.0.0、external_crt+speaker+led、input_map 18 动作（十字键/ABC/Start/2P） | ✅ |
| `content/sega-md/assemblies/*.gltf` | 6 件真实尺寸占位盒（上壳 16-BIT 台肩/下壳/主板/卡带仓/卡带/六键手柄预留） | ✅ |
| `content/sega-md/assemblies/MESHES.md` | 占位说明 + 16-BIT 凹字台肩说明 + 尺寸依据 | ✅ |
| `content/sega-md/annotations/annotations.json` | 30 条标注（16 role + 3 flow + 3 anim + 8 趣点） | ✅ |
| `content/sega-md/encyclopedia.md` | 2502 字（16 位时代争霸/美日版本差异/Blast Processing 梗） | ✅ |
| `content/sega-md/THIRD_PARTY.md` | 四档许可清册（R-091 三件套） | ✅ |

**硬件验收**：`validate.py content/sega-md` → **总计 96 条：PASS 96，FAIL 0**。

## 二、尺寸对照表（对照 01_SegaMD.md 档案）

| 参数 | 预研档案（01_SegaMD.md (b)） | 本包取值 | 对照结论 |
|---|---|---|---|
| 主 CPU | Motorola 68000 @ 7.67 MHz | `cpu_68k` part_no=MC68000 | 一致 |
| 副 CPU | Zilog Z80 @ 3.58 MHz | `cpu_z80` part_no=Z80 | 一致 |
| 声音 | YM2612 FM + SN76489 PSG | `ym2612`/`sn76489` 元器件 | 一致 |
| 卡带 | ROM 卡带最大 4MB，64-pin | `cart_bay`（64-pin）+ `cartridge`（几何不涉 ROM） | 一致 |
| 手柄 | 3 键/6 键 | `controller`（六键预留）+ input_map A/B/C | 一致 |
| 分辨率 | 320×224 | runtime `external_crt`（注明信号域差异） | 一致 |
| 整机三围 | 预研未定值 | 占位盒 0.28×0.07×0.21 m（Model 1 近似） | 本包补定值 |

## 三、游戏机厅三台（2600/FC/MD）并列动线建议

| 区 | 设备 | 叙事 | 核心讲解点 |
|---|---|---|---|
| 奠基区 | Atari 2600（1977） | 卡带式游戏机的诞生 | TIA 逐行绘制 |
| 复苏区 | Famicom（1983） | 83 年崩溃后的复苏 | PPU 卷轴与精灵 |
| 16 位争霸区 | Sega MD（1988） | 16 位时代的开篇 | 68000+Z80 双 CPU、YM2612 FM 音源 |

**动线建议**：奠基区 → 复苏区 → 16 位争霸区（MD 一台开篇，后续 SFC 加入构成"双子星"并列）。三台共用 `external_crt` 外接大屏：2600 播《太空侵略者》、FC 播《超级马力欧兄弟》、MD 播《索尼克》，用画面直观呈现"逐行 → 卷轴 → 高速卷轴"的三代图形演进。MD 的耳机孔（Model 1 特有）是"声画风格"讲解的实物亮点，建议保留一台可插耳机的演示位。

## 四、开放问题

1. **整机三围定值**：占位盒 0.28×0.07×0.21 m 为 Model 1 近似值，正式建模前实机复核。
2. **BlastEm 版本锁定**：runtime 声明 1.0.0，正式接入以 `runtime.version` 写死（同 13 号 V18）。
3. **BlastEm 许可复核**：GPL-3.0 聚合边界须发布前法律复核（40-B C1）。
4. **六键手柄形态**：本包以 3 键为默认（对应 Model 1 早期），6 键为预留扩展；若作者改选 6 键默认需回写 input_map。
5. **R-087 role.en 缺失警告**：16 处 role 未配英文，非阻塞，双语首发前补齐。
