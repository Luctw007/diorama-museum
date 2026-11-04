# TASK-65A 完成报告（SFC 设备包生产 · 游戏机厅第五台）

> 任务：TASK-65A（05 线 1/2）· 里程碑 M1 · 前置：任务 60 完成。
> 依据：console-batch2/02_SuperFamicom.md。
> 完成日期：2026-11-04。

---

## 一、交付物清单与校验结果

| 文件 | 内容 | 状态 |
|---|---|---|
| `content/sfc/meta.json` | era=1990、localized、7 装配体 + 3 元器件（5A22/S-PPU/S-SMP） | ✅ |
| `content/sfc/runtime.json` | snes9x 1.60、external_crt+speaker+led、input_map 26 动作（十字/ABXY/LR/Start/Select/2P） | ✅ |
| `content/sfc/assemblies/*.gltf` | 6 件真实尺寸占位盒（上壳圆润+电源滑钮位/下壳/主板/卡带仓/卡带 Mode7 注记/手柄×2） | ✅ |
| `content/sfc/annotations/annotations.json` | 35 条（含 Mode 7 缩放旋转、音源采样、SFC 全盛游戏讲锚） | ✅ |
| `content/sfc/encyclopedia.md` | 2508 字（16 位争霸后半程、RPG 黄金年代、双雄对比台） | ✅ |
| `content/sfc/THIRD_PARTY.md` | 四档许可清册 | ✅ |

**硬件验收**：`validate.py content/sfc` → **总计 84 条：PASS 84，FAIL 0**。

## 二、与 MD 的"双雄对比台"建议

SFC 与 MD 是 16 位主机战争的双雄，建议在游戏机厅"16 位主机战争"专区**并列展示**：

| 维度 | Mega Drive（已产包 sega-md） | Super Famicom（本包 sfc） |
|---|---|---|
| 定位 | 速度与态度 | 色彩与声音 |
| 讲解重点 | 68000+Z80 双 CPU、YM2612 FM 音源、耳机孔 | Mode 7 缩放旋转、S-SMP 采样音源、四键菱形手柄 |
| CRT 演示 | 《索尼克》高速卷轴 | 《超级马力欧赛车》Mode 7 赛道 + 《最终幻想 VI》管弦配乐 |

**对比台设计**：两台面对面摆放，中间一台 CRT 演示位轮播两款代表作，观众在两台之间来回对比"速度"与"色彩"两种 16 位美学。MD 侧强调"快、硬、街机味"（耳机孔可插耳机听 FM 音色），SFC 侧强调"柔、丰、艺术感"（四键菱形手柄作交互件，与 MD 的 6 键格斗手柄对照）。双雄对比台是"16 位主机战争"叙事最核心的展呈形式。

## 三、开放问题

1. **Snes9x 许可复核**：runtime 以 Snes9x（类 MIT + 非商业限制）为技术基线，正式接入前须复核非商业条款边界（40-B C2，发布前法律复核）。
2. **整机三围定值**：占位盒 0.20×0.07×0.24 m 为 SFC 初代近似值，正式建模前实机复核。
3. **控制台键数**：任务书"十字/ABXY/LR/Start/Select/2P"，本包 input_map 已覆盖（btn0~11 含 2P），键全合法。
4. **R-087 role.en 缺失**：11 处 role 未配英文，非阻塞，双语首发前补齐。

## 四、TASK-65 两份收尾标注

本份（65-A）完成；65-B（游戏机厅导语 v1 + 五机动线）见 `console-batch2/11_游戏机厅导语_v1.md` 与 `TASK-65B_完成报告.md` 的总收尾。
