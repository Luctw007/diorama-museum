# TASK-178-A 完成报告

> 第二批 2 号设备包：MITS Altair 8800（目录 `C-PC-000122`）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡 | `docs/research/hall-personal-batch2/09_Altair8800.md` | 七节齐全，证据 S94–S97 |
| meta.json | `content/altair-8800/meta.json` | id=altair-8800、era=1975、category=personal-computer、manufacturer=MITS |
| runtime.json | `content/altair-8800/runtime.json` | emulator=`simh-altair8800`（预留）、sinks=indicator_lamps+terminal、input_map 8 动作 |
| assemblies | `content/altair-8800/assemblies/` | 7 装配（whole + 机箱/前面板/CPU板/S-100背板/电源/扩展卡 6 件 glTF，节点名=node_id）+ MESHES.md |
| annotations | `content/altair-8800/annotations/annotations.json` | 46 条（**flow 11** + role 35） |
| encyclopedia | `content/altair-8800/encyclopedia.md` | **2,542 汉字**（≥2500） |
| THIRD_PARTY | `content/altair-8800/THIRD_PARTY.md` | 三件套 + Altair BASIC 红线 |

## 验收日志

- **产包过 02 线 validate**：`python tools/validate/validate.py content/altair-8800` → **84 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过（6 网格三角面 12 ≤ 20000）。
- **目录反链 diff**：`C-PC-000122` → `planned→done`、`device_id null→altair-8800`、`research_doc null→docs/research/hall-personal-batch2/09_Altair8800.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0）；`catalog_ref_check.py` → **REF-01~04 全 0 · FAIL 0**（registry 1582/1582 漂移 0）。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## 说明

- **emulator id**：`simh-altair8800` 通过 schema 正则 `^[a-z][a-z0-9_-]*$`（首字符小写字母），与 pdp8 的 `simh-pdp8` 同构；槽位 `reserved` 预留，未下发 SIMH 二进制。
- **media_hint=`tape`**：Altair 8800 早期以纸带/卡式磁带载入 BASIC（枚举无 cassette，用 tape），已在研究卡标注。
- **版权红线**：Altair BASIC 为微软首款产品，本包未下载任何磁带/纸带/ROM/固件镜像，「可玩」建议自研复刻程序承载。
- 目标模拟器只写「Open SIMH Altair 8800（本机可编译）」交付要求，二进制由用户自备进 slots。

## 开放问题

1. 目录中 Altair 8800 真实 id 确为 `C-PC-000122`（与任务书一致），同名录 `C-PC-000123 Altair 8800b` / `C-PC-000124 IMSAI 8080` 未混用。
2. 定价（439/621 美元）与销量、SIMH 许可均已标「需核实」。
