# TASK-55A 完成报告（游戏机与手持大类目录普查 · 第一批）

> 任务：TASK-55A（05 线 1/2）· 里程碑 M1 · 体例同 53-A（轻量行、覆盖准、不深研）。
> 完成日期：2026-11-04。

---

## 一、统计

| 中分类 | 条数 | 覆盖子分类 |
|---|---|---|
| 家用机 | 91 | Atari系 / Coleco系 / Mattel系 / Magnavox·Philips系 / Nintendo系 / Sega系 / Sony系 / Microsoft系 / NEC系 / SNK系 / 非主流美奇观 |
| 掌机 | 57 | Game&Watch / Game Boy系 / Game Gear / Lynx / Neo Geo Pocket / WonderSwan / PSP / DS系 / 其他掌机 |
| 街机 | 126 | 经典框体 / 基板（Neo-Geo MVS、CPS、System 16、Model、Naomi、Namco System、Taito、Konami 等） |
| **合计** | **274（≥250 达标）** | 每子分类 ≥3 行 |

**状态统计**：done 3（atari-2600 / famicom / sega-md，均已关联 device_id）；researching 2（Super Famicom / Game Boy）；planned 269。

## 二、覆盖面自查表

| 要求覆盖 | 是否覆盖 | 备注 |
|---|---|---|
| 家用机 Atari 系 | ✅ | 2600（done）/5200/7800/Jaguar/XEGS/Pong/2800 |
| 家用机 Coleco/Mattel/Magnavox | ✅ | ColecoVision/Telstar/Gemini、Intellivision/HyperScan、Odyssey/Odyssey²/CD-i |
| 家用机 Nintendo/Sega/Sony/Microsoft 全代际 | ✅ | 从 Color TV-Game 到 Switch、从 SG-1000 到 Dreamcast、PS1~PS5、Xbox~Series |
| 非主流美奇观机型 | ✅ | Channel F/RCA Studio II/Vectrex/3DO/Pippin/FM Towns Marty 等 |
| 掌机 Game&Watch/Game Boy 系 | ✅ | G&W 多款、GB 系全代 |
| 掌机 GG/Lynx/Neo Geo Pocket/PSP/DS | ✅ | 全覆盖 |
| 街机经典框体 100+ | ✅ | 30 款经典框体 |
| 街机基板大类 | ✅ | MVS/CPS/System16/Model/Naomi/Namco System 等 60+ 基板 |
| 已产包机型标状态 + device_id | ✅ | atari-2600/famicom/sega-md 标 done |
| 已预研机型标状态 | ✅ | Super Famicom/Game Boy 标 researching |

## 三、与 taxonomy 的出入清单（供 52 线吸收）

> 02 线 v0.6 分类学（52-A）尚未产出，本目录按 52-A 任务文档的条目 schema 自定，出入如下：

| # | 出入点 | 本目录处理 | 建议 v0.6 定稿吸收 |
|---|---|---|---|
| 1 | id 格式 | 自定 `G-{中分类码}-{6位序号}`（G-HOME/G-HAND/G-ARC） | 建议 v0.6 正式定义游戏机大类码与中分类码 |
| 2 | 分类路径子分类名 | 自定（Atari系/Nintendo系/非主流美奇观 等） | 建议 v0.6 定稿统一子分类枚举 |
| 3 | "掌机"与"手提机"术语 | 本目录用"掌机"，与 45-B 用"手提机"并存 | 建议统一为"掌机" |
| 4 | 街机"经典框体 vs 基板" | 本目录合并为"经典框体与基板"一子类 | 建议 v0.6 拆分为两个子类 |
| 5 | Game&Watch 归掌机 | 本目录归"掌机"，与 50-B 归"手持线"一致 | 建议 v0.6 明确掌机=手持 |

## 四、开放问题

1. **v0.6 分类学未产**：本目录的 id 格式、分类路径、子分类名均为自定，待 52-A 定稿后回填对齐。
2. **catalog_check 未产**：本目录按 52-B 任务文档的 CC-01~CC-07 规则人工自查（字段齐全/id 唯一/年代范围/状态枚举/理由 ≤60 字），待 catalog_check.py 产出后正式校验。
3. **街机基板覆盖深度**：本目录街机 126 条以"基板 + 代表框体"为主，未穷尽所有基板（Cave、Seibu、Kaneko 等小众基板留待下一批）。
4. **影响力理由 ≤60 字**：已逐条控制，个别条目接近上限，v0.6 若放宽可补足。

## 五、TASK-55 两份收尾标注

本份（55-A）完成；55-B（家电影音与外设大类）见 `家电影音与外设大类_目录_v1.jsonl` 与 `TASK-55B_完成报告.md` 的总收尾。
