# TASK-60B 完成报告（Neo Geo MVS 街机柜设备包 · 街机类首台）

> 任务：TASK-60B（05 线 2/2）· 里程碑 M1 · 与 60-A 共同构成 TASK-60 两份。
> 完成日期：2026-11-04。

---

## 一、交付物清单与校验结果

| 文件 | 内容 | 状态 |
|---|---|---|
| `content/neo-geo-mvs/meta.json` | era=1990、category=game-console、8 装配体 + 3 元器件（68000/Z80/YM2610） | ✅ |
| `content/neo-geo-mvs/runtime.json` | mame neogeo、external_crt+speaker+led、input_map 20 动作（1P/2P 摇杆+A/B/C/D+Start+投币） | ✅ |
| `content/neo-geo-mvs/assemblies/*.gltf` | 7 件柜体级真实尺寸占位盒（框体/CRT/控制台/MVS基板/卡带/投币机构/电源） | ✅ |
| `content/neo-geo-mvs/annotations/annotations.json` | 36 条（11 role + 3 flow + 4 anim + 18 趣点） | ✅ |
| `content/neo-geo-mvs/encyclopedia.md` | 2542 字（MVS/AES 双轨、格斗年代、投币文化、双卡槽换卡不停机） | ✅ |
| `content/neo-geo-mvs/THIRD_PARTY.md` | 四档许可清册 | ✅ |

**硬件验收**：`validate.py content/neo-geo-mvs` → **总计 90 条：PASS 90，FAIL 0**。

## 二、柜体级拆解与 depth_model §2 七类目对照

Neo Geo MVS 街机柜是"框体 + 基板"双层结构，其 7 件装配体恰好**一一对应 depth_model §2 的七大类部件**：

| depth_model 七类目 | 类码 | 本包装配体 | 爆炸主轴 |
|---|---|---|---|
| 外壳与结构 | L1-ENC | cabinet（框体，立式木板 + 灯箱） | 沿开盖轴 |
| 屏幕 | L1-DISP | crt_module（CRT 屏模组） | -Z（朝观众推出） |
| 键盘与输入 | L1-IO | control_panel（控制台摇杆 + 4 键） | +Y |
| 主板 | L1-BOARD | mvs_board（MVS 基板，双卡槽） | +Y |
| 存储 | L1-STO | cartridge（MVS 大卡） | +X |
| 散热与机电 | L1-THM | coin_mechanism（投币机构） | +Y |
| 电源 | L1-PSU | power_supply（电源） | +X |

> **对照结论**：街机柜是"七类目全齐"的理想样本——一台设备恰好覆盖 depth_model §2 的全部七个 L1 类目，且"框体 + 基板"双层结构天然演示了 L0（整机）→ L1（七大类部件）→ L2（基板上的 68000/双卡槽）→ L3（元器件）的完整拆解链路。这是"柜体级大部件拆解"的最佳验证样本，为后续街机厅其他框体（框体/基板双层）的拆解提供了标准模板。

## 三、开放问题

1. **整机三围定值**：框体 0.60×1.70×0.70 m 为标准街机柜近似值，正式建模前实机复核。
2. **控制台键数**：任务书"摇杆+6 键布局尺寸"与 Neo Geo 标准 4 键（A/B/C/D）不符，本包按 4 键（input_map btn0~7），6 键为格斗框体扩展，已在百科注明。
3. **category 类码**：任务书"category=game-console 或按 57-A 加 arcade 类码——以定稿为准"，本包用 game-console（57-A 未定稿），待定稿后如需 arcade 类码回填。
4. **MAME neogeo 真跑**：demo 起步，MAME neogeo 为预留真跑后端（需 BIOS + 卡带 ROM，均不自带，红线照旧）。
5. **R-087 role.en 缺失**：11 处 role 未配英文，非阻塞，双语首发前补齐。

## 四、TASK-60 两份总收尾

- **60-A（游戏机目录第二轮）**：`游戏机与手持大类_目录_v2.jsonl/.md`，401 条（≥400），键名已迁移英文定稿键、分类路径对齐 v0.6 taxonomy、街机基板深补 +124；**catalog_check FAIL 0**。
- **60-B（Neo Geo MVS 街机柜设备包）**：`content/neo-geo-mvs/`，柜体级 7 件 + 36 条标注 + 2542 字百科，**validate 90 PASS / 0 FAIL**，柜体级拆解恰好对应 depth_model 七类目。
- **05 线本轮收尾**：游戏机线从"家用机/掌机"扩展到"街机"——街机厅首台（Neo Geo MVS 街机柜）设备包开产，验证了"柜体级大部件拆解"范式；游戏机目录完成键名迁移与 v0.6 对齐，累计 401 条，为万级目录的第二轮奠基。
