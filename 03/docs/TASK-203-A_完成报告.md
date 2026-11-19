# TASK-203-A 完成报告

> 第二批 7 号设备包：Cray-1（目录 `C-SC-000003`，超级计算机）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡（复用） | `docs/research/hall-mainframe/13_Cray1.md` | 188-B 已产，本任务复用（证据 S108–S109） |
| meta.json | `content/cray-1/meta.json` | id=cray-1、era=1976、category=supercomputer、manufacturer=Cray Research |
| runtime.json | `content/cray-1/runtime.json` | emulator=`none`（无 bone 静态+动画）、sinks=indicator_lamps+terminal、input_map 8 动作 |
| assemblies | `content/cray-1/assemblies/` | 6 装配（whole + 环形机柜/向量处理单元/内存/冷却系统/C 形座椅 5 件 glTF）+ MESHES.md |
| annotations | `content/cray-1/annotations/annotations.json` | 44 条（**flow 10** + role 34） |
| encyclopedia | `content/cray-1/encyclopedia.md` | **2,502 汉字**（≥2500） |
| THIRD_PARTY | `content/cray-1/THIRD_PARTY.md` | 三件套 + 无模拟器声明 + 磁带红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/cray-1` → **78 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-SC-000003` → `planned→done`、`device_id null→cray-1`、`research_doc null→docs/research/hall-mainframe/13_Cray1.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0），CC-08 PASS 31；`catalog_ref_check.py` → **FAIL 0**（REF-03 提示 registry 1583/目录 1582、未使用 1 条，为 01 线新 allocate 的 id 尚未入目录，非本任务错误）。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## emulator 口径对齐结果

- 任务书明确 `emulator="none"`（对齐 187-A S 档「无 bone → none」+ 192-A UNIVAC 过闸口径）。Cray-1 无成熟模拟器，本包用 **`emulator="none"`**，已对齐。
- **category=supercomputer**（对齐目录 taxonomy「计算机/超级计算机/向量机」）。

## 说明

- **flow 锚点**：超级计算机视觉象征、向量处理革命、Seymour Cray 巅峰、洛斯阿拉莫斯、氟利昂冷却、环形机柜设计、科学与国防算力底座、超级计算传承等 10 条。
- **版权红线**：未下载任何磁带镜像/ROM/固件/二进制。
- 注：临时生成脚本因 safe-delete 机制故障未能删除，已覆盖为无害注释，不影响交付。

## 开放问题

1. 目录中 Cray-1 真实 id 确为 `C-SC-000003`（与定案表 v2 草案一致）。
2. 主频约 80 MHz、重量约 5.5 吨、定价/销量等均已标「需核实」。
