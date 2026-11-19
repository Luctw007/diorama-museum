# TASK-193-A 完成报告

> 第二批 5 号设备包：UNIVAC I（目录 `C-MF-000050`，大型机）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡（复用） | `docs/research/hall-mainframe/11_UNIVAC1.md` | 188-B 已产，本任务复用（证据 S104–S105） |
| meta.json | `content/univac-1/meta.json` | id=univac-1、era=1951、category=mainframe、manufacturer=Eckert-Mauchly / Remington Rand |
| runtime.json | `content/univac-1/runtime.json` | emulator=`none`（无 bone 静态+动画）、sinks=indicator_lamps+terminal、input_map 8 动作 |
| assemblies | `content/univac-1/assemblies/` | 6 装配（whole + 中央处理机柜/内存/磁带机/控制台/打印机 5 件 glTF）+ MESHES.md |
| annotations | `content/univac-1/annotations/annotations.json` | 45 条（**flow 11** + role 34） |
| encyclopedia | `content/univac-1/encyclopedia.md` | **2,616 汉字**（≥2500） |
| THIRD_PARTY | `content/univac-1/THIRD_PARTY.md` | 三件套 + 无模拟器声明 + 磁带红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/univac-1` → **78 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-MF-000050` → `planned→done`、`device_id null→univac-1`、`research_doc null→docs/research/hall-mainframe/11_UNIVAC1.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0），CC-08 PASS 29；`catalog_ref_check.py` → **REF-01~04 全 0 · FAIL 0**。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## emulator 口径对齐结果

- 任务书注明「192-A 若未出则按保守口径」。经核实 02 线同轮产出的是 **TASK-187-A《第二批分档验收口径 v2》**（192-A 未产出），其 S 档口径裁决：**「无 bone 后端 → `emulator="none"` + 静态+动画演示」**。
- UNIVAC I 无成熟模拟器（研究卡结论「无成熟模拟器，SIMH 候选需核实」），故本包按 187-A 口径用 **`emulator="none"`**（非 null、非 simh-univac），已与分档验收口径对齐。

## 说明

- **category=mainframe**（大型机），对齐目录 taxonomy_path「计算机/大型机/Univac 系」。
- **flow 锚点**：首台商用机、1952 大选预测、Eckert-Mauchly 团队、水银延迟线、磁带机 I/O、真空管、十进制串行运算、与 IBM 竞争等 11 条。
- **版权红线**：未下载任何磁带镜像/ROM/固件/二进制。

## 开放问题

1. 目录中 UNIVAC I 真实 id 确为 `C-MF-000050`（与定案表 v2 草案一致）。
2. 占地约 35 ㎡、真空管约 5,000 根、定价/销量等均已标「需核实」。
