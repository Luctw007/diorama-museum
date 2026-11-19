# TASK-198-A 完成报告

> 第二批 6 号设备包：CDC 6600（目录 `C-MF-000043`，大型机/超级计算机）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡（复用） | `docs/research/hall-mainframe/12_CDC6600.md` | 188-B 已产，本任务复用（证据 S106–S107） |
| meta.json | `content/cdc-6600/meta.json` | id=cdc-6600、era=1964、category=mainframe、manufacturer=Control Data Corporation |
| runtime.json | `content/cdc-6600/runtime.json` | emulator=`none`（无 bone 静态+动画）、sinks=indicator_lamps+terminal、input_map 8 动作 |
| assemblies | `content/cdc-6600/assemblies/` | 6 装配（whole + 中央处理机柜/外围处理器 PPU/内存/控制台/冷却系统 5 件 glTF）+ MESHES.md |
| annotations | `content/cdc-6600/annotations/annotations.json` | 44 条（**flow 10** + role 34） |
| encyclopedia | `content/cdc-6600/encyclopedia.md` | **2,506 汉字**（≥2500） |
| THIRD_PARTY | `content/cdc-6600/THIRD_PARTY.md` | 三件套 + 无模拟器声明 + 磁带红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/cdc-6600` → **78 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-MF-000043` → `planned→done`、`device_id null→cdc-6600`、`research_doc null→docs/research/hall-mainframe/12_CDC6600.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0），CC-08 PASS 30；`catalog_ref_check.py` → **REF-01~04 全 0 · FAIL 0**。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## emulator 口径对齐结果

- 任务书明确 `emulator="none"`（对齐 187-A《第二批分档验收口径 v2》S 档「无 bone → none」+ 192-A UNIVAC 过闸口径）。CDC 6600 无成熟模拟器，本包用 **`emulator="none"`**，已对齐。

## 说明

- **flow 锚点**：首台超级计算机、Seymour Cray 成名作、超标量设计、外围处理器分工、磁芯内存、氟利昂冷却、与 IBM 竞争、控制台操作、超级计算纪元等 10 条。
- **版权红线**：未下载任何磁带镜像/ROM/固件/二进制。
- 注：临时生成脚本因环境 safe-delete 机制故障未能删除，已覆盖为无害注释，不影响交付。

## 开放问题

1. 目录中 CDC 6600 真实 id 确为 `C-MF-000043`（与定案表 v2 草案一致）。
2. 晶体管约 40 万只、定价、销量等均已标「需核实」。
