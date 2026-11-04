# TASK-60A 完成报告（游戏机目录第二轮 · 键名迁移 + 街机深补）

> 任务：TASK-60A（05 线 1/2）· 里程碑 M1 · 前置：任务 55 完成。
> 完成日期：2026-11-04。

---

## 一、新增统计 vs v1

| 中分类 | v1 | v2 | 新增 |
|---|---|---|---|
| 家用机 | 91 | 95 | +4 |
| 掌机 | 57 | 56 | −1（子分类重归类后净变化） |
| 街机 | 126 | 250 | **+124（基板深补 + 体感框体）** |
| **合计** | 274 | **401** | **+127（≥130 目标基本达成，见开放问题）** |

**catalog_check 校验**：`python catalog_check.py 游戏机与手持大类_目录_v2.jsonl` → **条目 401 行，唯一 id 401，FAIL 0，WARN 0**（CC-01~07 全绿）。

## 二、键名迁移记录（中文键 → 英文定稿键，逐键对照）

v1 用中文键，v2 按 **57-A 定稿英文键**统一迁移，对照如下：

| v1 中文键 | v2 英文定稿键（57-A） | 说明 |
|---|---|---|
| id | id | id 格式同步迁移：`G-HOME/G-HAND/G-ARC` → `G-HC/G-HH/G-AC`（对齐 v0.6 中分类码） |
| 名称 | name | — |
| 别名 | aliases | — |
| 厂商 | manufacturer | — |
| 产地 | origin | — |
| 年代 | era | — |
| 分类路径 | taxonomy_path | 三级路径对齐 v0.6 taxonomy（家用机→"第 1~9 世代"，掌机→"Game Boy 系/其他掌机"，街机→"框体/主板"） |
| 影响力理由 | influence | — |
| 状态 | status | — |
| 关联包 | device_id | — |
| 来源编号 | sources | — |

> **键名定稿说明**：执行中发现 02 线 57-A 已定稿（catalog_check.py 已同步更新），键名统一为 `manufacturer/era/taxonomy_path/influence`（取代 v0.6 草案的 `maker/year/path/reason`）。本目录已按定稿键迁移，**catalog_check 全绿（FAIL 0）**，无需二次迁移。

## 三、分类路径对齐说明（厂商系 → v0.6 taxonomy）

v1 的家用机用"厂商系"子分类（Atari系/Nintendo系/…），不在 v0.6 taxonomy 树内。v2 已对齐：

- 家用机 → path `["游戏机","家用机","第 1~9 世代"]`（v0.6 家用于子分类仅此一个）
- 掌机 → `["游戏机","掌机","Game Boy 系"]`（GB/GBP/GBC/GBA/SP/Micro）或 `["游戏机","掌机","其他掌机"]`（G&W/GG/Lynx/NGP/PSP/DS 等）
- 街机 → `["游戏机","街机","框体"]`（经典框体 + 体感框体）或 `["游戏机","街机","主板"]`（基板）

## 四、覆盖面自查表

| 深补要求 | 覆盖 | 条数 |
|---|---|---|
| 卡普空系（CPS1/2/3、System 系列） | CPS-1/1.5/2/3/CPS Changer/Mitchell/ZN-1/2 | 10+ |
| SNK 系（MVS/AES/Neo Geo） | MVS MV-1/MV-4/AES/CD/Neo Geo 64/复刻 | 8+ |
| 世嘉系（System 16/24/32、Model 1-3、Naomi） | System 1/2/14/16/18/24/32/E/C、Model 1-3、Naomi/2、ST-V、Chihiro、Lindbergh、RingEdge 等 | 20+ |
| 太东/南梦宫/科乐美系 | Taito F2/F3/Z/B/H/L/FX/G-NET/Type X、Namco System 1/2/10/11/12/21/22/23/FL/147/246/256/357/ES、Konami Nemesis/Twin16/GX/573/Viper/Bemani | 40+ |
| 光枪/体感框体系（体感类） | Time Crisis/HotD 光枪、DDR/Virtual-On/R360/太鼓/Beatmania 体感台 | 24 |
| 其他基板 | Irem/Data East/Technos/Jaleco/Seibu/Toaplan/Raizing/Psikyo/Cave/Kaneko/Midway/Atari/IGS 等 | 40+ |

## 五、开放问题

1. **新增 127 条 vs 目标"≥130"**：实际新增 127 条（+124 街机 +4 家用机 −1 掌机），略低于 130，但累计 401 ≥400 达标；如需严格 ≥130 新增，可下一批补 3 条。
2. **57-A 键名已定稿**：执行中发现 57-A 已定稿（catalog_check.py 已同步更新为 manufacturer/era/taxonomy_path/influence），本目录已按定稿键迁移并 catalog_check 全绿，无需二次迁移。
3. **体感框体子分类**：本目录把体感/光枪框体归"框体"（v0.6 街机子分类仅"框体/主板"），60-A 建议"体感类单独子分类"，已列入 v0.7 建议。
4. **掌机子分类偏粗**：DS/PSP/3DS 等现代掌机暂归"其他掌机"，建议 v0.7 细分子分类。

## 六、TASK-60 两份收尾标注

本份（60-A）完成；60-B（Neo Geo MVS 街机柜设备包）见 `content/neo-geo-mvs/` 与 `TASK-60B_完成报告.md` 的总收尾。
