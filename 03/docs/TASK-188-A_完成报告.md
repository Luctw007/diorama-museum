# TASK-188-A 完成报告

> 第二批 4 号设备包：HP 2100（目录 `C-MC-000046`）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡 | `docs/research/hall-mainframe/10_HP2100.md` | 七节齐全，证据 S101–S103，已回填 `06_证据包索引.md` |
| meta.json | `content/hp-2100/meta.json` | id=hp-2100、era=1971、category=minicomputer、manufacturer=Hewlett-Packard |
| runtime.json | `content/hp-2100/runtime.json` | emulator=`simh-hp2100`（预留）、sinks=indicator_lamps+terminal、input_map 8 动作 |
| assemblies | `content/hp-2100/assemblies/` | 7 装配（whole + 机箱/前面板/CPU板/内存/电源/I-O接口 6 件 glTF）+ MESHES.md |
| annotations | `content/hp-2100/annotations/annotations.json` | 47 条（**flow 11** + role 36） |
| encyclopedia | `content/hp-2100/encyclopedia.md` | **2,601 汉字**（≥2500） |
| THIRD_PARTY | `content/hp-2100/THIRD_PARTY.md` | 三件套 + SIMH HP 2100 预留 + 纸带红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/hp-2100` → **84 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-MC-000046` → `planned→done`、`device_id null→hp-2100`、`research_doc null→docs/research/hall-mainframe/10_HP2100.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0），CC-08 PASS 28；`catalog_ref_check.py` → **REF-01~04 全 0 · FAIL 0**。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## 说明

- **emulator id**：`simh-hp2100` 通过 schema 正则 `^[a-z][a-z0-9_-]*$`，与 pdp8/nova/altair 同构；槽位 `reserved` 预留，未下发 SIMH 二进制。
- **flow 锚点**：仪器出身、16 位实时控制、HP 2116A 谱系、时间共享 BASIC、与 PDP 竞争、磁芯内存、纸带、工业控制等 11 条。
- **版权红线**：未下载任何纸带/ROM/固件/二进制镜像，「可玩」建议自研复刻程序承载。

## 开放问题

1. 目录中 HP 2100 真实 id 确为 `C-MC-000046`（与定案表 v2 草案一致），同名录 `C-MC-000047 HP 1000` 未混用。
2. 定价、销量、CPU 微程序控制与 SIMH 许可均已标「需核实」。
