# TASK-30A 完成报告（FC/NES 设备包生产 · 游戏机厅第二台）

> 任务：TASK-30A（05 线 1/2）· 里程碑 M1 · 前置：任务 25 完成。
> 依据：console-batch1/02_FamicomNES.md（预研）+ 02 线 v0.3 草案。
> 完成日期：2026-11-02。

---

## 一、交付物清单与校验结果

| 文件 | 内容 | 状态 |
|---|---|---|
| `content/famicom/meta.json` | era=1983、localized、11 装配体 + 5 元器件（2A03/2C02/WRAM/VRAM/ROM） | ✅ |
| `content/famicom/runtime.json` | Mesen 2.0、external_crt 256×240、input_map 18 动作（十字键/AB/Start/Select+2P） | ✅ |
| `content/famicom/assemblies/*.gltf` | 6 件真实尺寸占位盒（上壳红白/下壳/主板/卡带仓/卡带60pin/手柄合件） | ✅ |
| `content/famicom/assemblies/MESHES.md` | 占位说明 + 尺寸依据 + 240i 信号域差异 | ✅ |
| `content/famicom/annotations/annotations.json` | 30 条标注（16 role + 4 flow + 4 anim + 6 趣点） | ✅ |
| `content/famicom/encyclopedia.md` | 2532 字（83 年复苏/PPU 卷轴精灵/硬件扩张生态） | ✅ |
| `content/famicom/THIRD_PARTY.md` | 四档许可清册（R-091 三件套） | ✅ |

**硬件验收**：`validate.py content/famicom` → **总计 100 条：PASS 100，FAIL 0**。

## 二、定档理由（1983 Famicom 红白机为本体）

1. **icon 性最强**：红白配色 + 顶部插卡 + 焊死手柄，是"红白机"最具辨识度的形态，最贴近"83 年游戏业复苏"的历史叙事。
2. **历史叙事最纯粹**：1983 年日版是复苏的起点；NES（1985）是"改头换面登陆北美"的后续动作。
3. **一份资产双版本潜力**：核心（2A03 + 2C02 PPU）与 NES 完全一致，未来若需 NES 灰白版，仅换外壳/卡带接口（60→72 针）即可复用。
4. **与 atari-2600 并列**：游戏机厅"奠基—复苏"叙事需要"一台奠基者（Atari 2600）+ 一台复苏者（Famicom）"，红白机是后者最正统的载体。

美版 NES 的差异（前装卡匣、72 针、灰白、10NES 芯片）在百科 §八型号沿革 + annotations 的 `nes_diff_role` 趣点覆盖，不另立包。

## 三、尺寸对照表（对照 02_FamicomNES.md 档案）

| 参数 | 预研档案（02_FamicomNES.md (b)） | 本包取值 | 对照结论 |
|---|---|---|---|
| CPU | Ricoh 2A03 @ 1.79 MHz（NTSC） | `cpu_2a03` part_no=RP2A03 | 一致 |
| 图形 | Ricoh 2C02 PPU（256×240） | `ppu_2c02` part_no=RP2C02 | 一致 |
| 内存 | 2 KB 工作 RAM + 2 KB VRAM | `wram`/`vram` 元器件 | 一致 |
| 分辨率 | 256×240（NTSC） | runtime `external_crt`（注明 262.5 行信号域差异） | 一致 |
| 声音 | 5 通道（APU） | 百科 §四 | 一致 |
| 卡带 | 60-pin（FC） | `cartridge`（60pin 剖面，几何+说明不涉 ROM） | 一致 |
| 手柄 | 十字键+A/B+Start/Select（2P 麦克风） | input_map + `pad_2` 麦克风趣点 | 一致 |
| 整机三围 | 预研未定值 | 占位盒 0.15×0.08×0.21 m（HVC-001 近似） | 本包补定值 |

## 四、与 atari-2600 的展呈并列建议（游戏机厅动线雏形）

| 区 | 设备 | 叙事 | 核心讲解点 |
|---|---|---|---|
| 奠基区 | Atari 2600（1977） | 卡带式游戏机的诞生 | TIA 逐行绘制、无帧缓冲、"追着电子束跑" |
| 复苏区 | Famicom（1983） | 83 年崩溃后的复苏 | PPU 卷轴与精灵、五通道 APU、授权生态、硬件扩张 |

**动线建议**：奠基区 → 复苏区 顺序参观，形成"兴起—崩溃—复苏"的完整叙事弧。两台设备共享 `external_crt` 外接大屏（游戏机厅 CRT 墙），Atari 2600 播《太空侵略者》、Famicom 播《超级马力欧兄弟》，用画面直观呈现"六年图形飞跃"（TIA 逐行 vs PPU 卷轴）。此动线是游戏机厅动线设计的雏形，正式动线规格交 04 线设计文档。

## 五、开放问题

1. **整机三围定值**：占位盒采用 HVC-001 公开近似值（0.15×0.08×0.21 m），正式建模前建议实机复核。
2. **Mesen 版本锁定**：runtime 声明 2.0，正式接入以 `runtime.version` 写死（同 13 号 V18）。
3. **十字键 hat 值语义**：input_map 用 `hat_0/hat_1` 表达十字键，Mesen 后端翻译需约定 hat 方向→具体值映射（hat 值为枚举，非 bool|float）。
4. **240i 信号域**：任务书"240i"为口误，实际 PPU 逐行 240 可见行（NTSC 262.5 行信号域），已在 MESHES.md 注明。
5. **红白配色字段预留**：当前用 meta.description/intro + top_shell.role 表达红白配色；未来若需结构化的"配色变体"字段（colorway），建议 v0.3 定稿时评估新增 schema 字段。
6. **R-087 role.en 缺失警告**：16 处 role 未配英文，非阻塞，双语首发前补齐。
