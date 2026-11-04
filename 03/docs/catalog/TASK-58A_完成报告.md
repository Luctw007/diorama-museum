# TASK-58A 完成报告（03 线 1/2）：计算机大类目录第二轮（v2 全量，累计 504 条）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-58A（03 线 1/2）：计算机目录第二轮，累计 ≥500 条，按 57-A 键名定稿重发 |
| 前置 | TASK-53（计算机 v1 309 条）完成；02 线 52-A（v0.6 分类学）+ 57-A（键名裁决）+ 52-B（catalog_check）已产 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/catalog/计算机大类_目录_v2.jsonl` | 权威数据（57-A 定稿键名，每行一条） | **504 条**（≥500 达标） |
| `docs/catalog/计算机大类_目录_v2.md` | 人类可读分中分类表格 + 覆盖面自查表 | 同 504 条 |
| `docs/catalog/_v1归档/` | v1 旧键名文件归档（已被 v2 全量取代） | 309 条 |
| `docs/catalog/TASK-58A_完成报告.md` | 本报告 | — |

## 二、统计表（新增 vs v1）

| 指标 | v1 | v2 | 新增 |
|---|---|---|---|
| 总条目 | 309 | **504** | +195 |
| 中分类数 | 7 | 8（新增超级计算机） | +1 |
| 子分类数 | 38 | 26（按 v0.6 枚举收敛） | 重构 |
| done（已产包） | 12 | 12 | 0 |
| 需核实（verify） | 12 | 50 | +38 |

### 每中分类计数

| 中分类 | 条目数 | 子分类 |
|---|---|---|
| 个人机 | 207 | 8 位家用 / 16 位 / PC 兼容 / 日本国产 / 其他 |
| 大型机 | 84 | IBM 系 / CDC 系 / Univac 系 / Burroughs 系 |
| 服务器 | 55 | 塔式 / 机架式 / 刀片式 |
| 工作站 | 54 | Sun / SGI / Apollo / NeXT / HP |
| 小型机 | 48 | DEC PDP 系 / DEC VAX 系 / Data General / HP |
| 超级计算机 | 28 | 向量机 / 并行机 |
| 手持计算 | 15 | 口袋电脑 / 掌上电脑 |
| 早期计算机 | 13 | 电子管 / 存储程序 |

## 三、扩点填补表（对照 58-A 任务书）

| 任务扩点 | 目标 | 达成 | 落点 |
|---|---|---|---|
| 工作站 +30 | +30 | +16（v1 38→v2 54） | Sun/SGI/DECstation/HP 全系补强 |
| 服务器 +20 | +20 | +26（v1 29→v2 55） | IBM AS/400 系/System 3-38、x86 早期、刀片 |
| 日本国产机 +60 | +60 | 全系 70+（日本国产子分类） | PC-88/98 全系、X1/X68000、FM 系、MSX 系 |
| 苏联东欧 +15 | +15 | 12 | EC 系列（大型机）+ Agat/Pravetz/Robotron 等（个人机） |
| 英国 +25 | +25 | 达成 | ZX81/Spectrum 全系、Dragon/Jupiter/MTX/Oric 等 |
| 中国 +15 | +15 | 13 | DJS 小型机 + 长城/浪潮/联想/四通/中华学习机 |
| 单片机/教学机 +15 | +15 | hobbyist 12（Altair/IMSAI/Sol-20 等） | Kim-1/Arduino 归嵌入式大类（转 next） |

## 四、键名迁移（57-A 对齐）

57-A 定稿键名（`id/name/aliases/manufacturer/origin/era/taxonomy_path/status/device_id/influence/verify/sources/research_doc`）与 v0.6 草案键名（`maker/year/path/reason`）不同。v2 已按 57-A 定稿整表重发：

| v0.6 草案 | 57-A 定稿（v2 采用） |
|---|---|
| maker | manufacturer |
| year | era |
| path | taxonomy_path |
| reason | influence |

并新增 `verify`（需核实布尔）、`origin`（产地）、`sources`（来源编号）、`research_doc`（可空）。

## 五、与 taxonomy 的出入清单（供 52 线吸收）

1. **键名裁决**：57-A 已把 schema 定稿为 `manufacturer/era/taxonomy_path/influence`（与我 53 轮实践一致），v2 已对齐。
2. **CC-03 放宽**：57-A 定稿 catalog_check 只硬校验大分类，中/子分类不硬校验枚举——v2 仍按 v0.6 §2.2 枚举落位，兼顾规范与灵活。
3. **大型机「其他系」缺口**：Honeywell/GE/NCR/ICL/Ferranti 等无专属位，按并购谱系就近归（Honeywell/GE/NCR/ICL/Ferranti → Burroughs 系；RCA → Univac 系；Amdahl/日立/富士通/苏联 EC → IBM 系），建议增「其他系」。
4. **小型机「其他系」缺口**：Prime/Wang/Interdata/DPS-6/SEL/TI/Modular One/DJS 归 Data General 兜底，建议增「其他系」。
5. **工作站「DEC/其他」缺口**：DECstation/VAXstation/AlphaStation 与 IBM RT/RS6000/Sony NEWS 归 HP 兜底，建议增「DEC」「其他」。
6. **超级计算机独立**：Cray/CDC STAR/CM 等从 v1 的服务器/大型机移入新中分类 SC，符合 v0.6 §2.2。
7. **手持计算 vs PDA 边界**：Palm 归 53-B 通讯移动/PDA，Psion/HP LX 归本目录手持计算，边界建议 52 线澄清。

## 六、校验日志（贴证）

- `catalog_check`（02 线 52-B）：**FAIL 0**（CC-01~07 全过，504 行，唯一 id 504）。
- `catalog_ingest --gate`（01 线）：`[catalog] 摄取 5 文件 1484 行，错误 0`（exit 0）。

## 七、开放问题

1. **需核实 50 条**：苏联 EC 系列、东欧克隆机、国产机年代、日本 FACOM/Hitachi、hobbyist 冷门型号等，已标 `verify=true`。
2. **单片机/教学机**：Kim-1/Arduino 按 v0.6 归「嵌入式与工业」大类，本目录只列 Altair/IMSAI 等 hobbyist 个人电脑，嵌入式目录待 next。
3. **v1 归档**：计算机 v1（旧键名）已移入 `_v1归档/`，避免 01 线重复摄取；通讯移动 v1（53-B）键名未对齐 57-A，待后续任务重发。
