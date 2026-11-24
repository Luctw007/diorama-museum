# 34 · 游戏机目录 planned 条目状态核对 v1

> 任务 295-D（05 线）· 完成日期：2026-11-24。
> 性质：**planned 条目状态核对卡**——游戏机目录 v2 大量 planned 条目（G-HC/G-HH/G-AC 共 390 条）。本卡核对五台产包 done 回填正确性 + 列出后续候选清单；**纯核对 + 文档，不回填、不改 jsonl。**
> 口径：数据以 `游戏机与手持大类_目录_v2.jsonl` 实测为准。

## 一、五台产包 done 回填核对表

| 条目 id | 名称 | 包 id | 回填前 status | 回填后 status | 核对结果 |
|---|---|---|---|---|---|
| G-HC-000055 | Sega Saturn | sega-saturn | planned | done | ✅ 一致 |
| G-HC-000056 | PlayStation | playstation | planned | done | ✅ 一致 |
| G-HC-000062 | Nintendo 64 | nintendo-64 | planned | done | ✅ 一致 |
| G-HC-000064 | Sega Dreamcast | sega-dreamcast | planned | done | ✅ 一致 |
| G-HC-000065 | PlayStation 2 | playstation-2 | planned | done | ✅ 一致 |

> 五台反链 device_id 全部对齐 05 线 content 实际包 id，`catalog_ref_check` REF-02 反链缺失 0，无悬空引用。

## 二、planned 条目总览与后续候选清单

游戏机目录 v2 planned 条目共 **390 条**，按 id 前缀分组：

| 前缀 | 分类 | planned 数 | 说明 |
|---|---|---|---|
| G-HC | 家用机 | 86 | 含第六代 GameCube/Xbox、第七代 Xbox 360/Wii/PS3、第八代 PS4/Xbox One/Switch、第九代 PS5/Xbox Series 等 |
| G-HH | 手持 | 55 | 含 Game & Watch 系、Game Boy 系、DS/3DS 系、PSP/Vita 系等 |
| G-AC | 街机 | 249 | 含经典街机名作、各厂基板、光枪/体感框体等 |

**后续候选清单（按世代/线分组，优先序建议）**：

| 世代/线 | 代表条目 | 状态 |
|---|---|---|
| 第六代家用机 | GameCube（G-HC-000066，32 号预研卡已备料）、Xbox（G-HC-000067） | planned |
| 掌机线 | Game Boy Advance（G-HH-000027）、Nintendo DS（G-HH-000033）、PSP（G-HH-000034） | planned |
| 街机线 | Neo Geo MVS 已 done（G-AC-000076）；CPS-2（G-AC-000078）、Sega Model 2/3、Naomi 等基板 | planned |

> 本序列（第二批主机研究卡 18 号）已覆盖第五代三台（Saturn/N64/PS1）+ Dreamcast + PS2；第六代剩 **GameCube、Xbox** 未产包，是后续回归建模的优先候选。

## 三、异常登记

- **无异常**：五台 done 回填均正确，device_id 与包 id 一致，无重复 id、无悬空引用。
- 观察项：planned 390 条中，街机线（G-AC 249 条）占大头，多为基板/框体条目，后续产包需按「街机暗房」规划分批推进；本卡不新建、不回填，仅登记。

## 四、红线自查

本卡纯核对，不回填、不改 jsonl；未下载 ROM/BIOS/二进制/贴图；数据均实测、不臆造；只改 05 目录。
