# 34 · 游戏机目录 planned 核对 v2（第六/七代主机条目巡检）

> 任务 305-R（05 线）· 完成日期：2026-11-25。
> 性质：**planned 条目核对卡 v2**——在 v1（34 号，11 台 done）基础上，补登 GameCube/Xbox 产包回填（305-C/G）+ 六/七代主机条目巡检；**纯巡检，不回填、不改 jsonl，另存 v2 不改 v1。**

## 一、第六/七代主机条目状态表

| 条目 id | 名称 | 厂商 | 世代 | status | device_id | 产包轮次 |
|---|---|---|---|---|---|---|
| G-HC-000066 | GameCube | Nintendo | 第六代 | done | gamecube | 305-C |
| G-HC-000067 | Xbox | Microsoft | 第六代 | done | xbox | 305-G |
| G-HC-000073 | Xbox 360 | Microsoft | 第七代 | planned | null | —（预研 41 号已备料） |
| G-HC-000074 | Wii | Nintendo | 第七代 | planned | null | —（预研 42 号已备料） |
| G-HC-000075 | PlayStation 3 | Sony | 第七代 | planned | null | —（预研 43 号已备料） |
| G-HC-000084 | Nintendo Switch | Nintendo | 融合 | planned | null | —（预研 44 号已备料） |

> 六台逐台在列：GameCube/Xbox 已 done（本轮 305-C/G 回填），Xbox 360/Wii/PS3/Switch 四台 planned、待后续产包。

## 二、done 回填核对

游戏机目录 v2 done 条目现 **13 台**（较 v1 的 11 台新增 GameCube、Xbox）：

| 前缀 | done 数 | 代表条目 |
|---|---|---|
| G-HC 家用机 | 11 | Atari 2600 / Famicom / MD / SFC / Saturn / PS / N64 / DC / PS2 / GameCube / Xbox |
| G-HH 手持 | 1 | Game Boy |
| G-AC 街机 | 1 | Neo Geo MVS |

> GameCube（G-HC-000066→gamecube）、Xbox（G-HC-000067→xbox）两条 done 回填核对一致，device_id 与包 id 对齐，`catalog_ref_check` REF-02 反链缺失 0。

## 三、G-AC / G-HH 前缀总数核对

| 前缀 | 分类 | planned 数（v1 实测） | done 数 | 说明 |
|---|---|---|---|---|
| G-HC | 家用机 | 86（-2 本轮 done） | 11 | 第六/七代四台 planned |
| G-HH | 手持 | 55 | 1 | GBA（G-HH-000027）预研已备料、仍 planned |
| G-AC | 街机 | 249 | 1 | 街机线 Pac-Man/CPS 准备卡已备、仍 planned |

## 四、与 295-J 街机巡检交叉引用

- 街机线 planned 巡检（295-J）已列 G-AC 249 条 planned + arcade-10 参数卡 10 台对照；本轮 305-M（基板建模任务卡）、305-N（Pac-Man 框体准备卡）为街机线备料，均未回填目录（planned 保持）。
- 街机线下一步候选：CPS-2、Sega Naomi、Model 2/3 基板 + Pac-Man 等经典框体。

## 五、红线自查

本卡纯巡检、不回填、不改 jsonl；未下载 ROM/BIOS/二进制/贴图；目录状态实测（读 jsonl + meta.json）、不臆造；只改 05 目录；另存 v2 不改 v1。
