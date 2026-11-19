# TASK-183-A 完成报告

> 第二批 3 号设备包：Data General Nova（目录 `C-MC-000027`）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡 | `docs/research/hall-mainframe/09_DataGeneralNova.md` | 七节齐全，证据 S98–S100，已回填 `06_证据包索引.md` |
| meta.json | `content/data-general-nova/meta.json` | id=data-general-nova、era=1969、category=minicomputer、manufacturer=Data General |
| runtime.json | `content/data-general-nova/runtime.json` | emulator=`simh-nova`（预留）、sinks=indicator_lamps+terminal、input_map 8 动作 |
| assemblies | `content/data-general-nova/assemblies/` | 7 装配（whole + 机箱/前面板/CPU板/内存背板/电源/I-O接口 6 件 glTF）+ MESHES.md |
| annotations | `content/data-general-nova/annotations/annotations.json` | 47 条（**flow 11** + role 36） |
| encyclopedia | `content/data-general-nova/encyclopedia.md` | **2,503 汉字**（≥2500） |
| THIRD_PARTY | `content/data-general-nova/THIRD_PARTY.md` | 三件套 + SIMH Nova 预留 + 纸带红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/data-general-nova` → **84 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-MC-000027` → `planned→done`、`device_id null→data-general-nova`、`research_doc null→docs/research/hall-mainframe/09_DataGeneralNova.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py`（两活跃目录）→ CC-01~08 **FAIL 0 / PASS 810**（跨文件重复 0），CC-08 PASS 27；`catalog_ref_check.py` → **REF-01~04 全 0 · FAIL 0**（registry 1582/1582 漂移 0）。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## 说明

- **emulator id**：`simh-nova` 通过 schema 正则 `^[a-z][a-z0-9_-]*$`，与 pdp8 的 `simh-pdp8`、altair 的 `simh-altair8800` 同构；槽位 `reserved` 预留，未下发 SIMH 二进制。
- **16 位架构锚点**：Nova 的 16 位字长与 PDP-8 的 12 位形成对比，落成 flow `bit16_arch`；低价竞争、出走 DEC、中国 DJS-130 兼容仿制等叙事锚点均已落地为 flow。
- **版权红线**：未下载任何纸带/ROM/固件/二进制镜像，「可玩」建议自研复刻程序承载。

## 开放问题

1. 目录中 Nova 真实 id 确为 `C-MC-000027`（与定案表 v2 草案一致），同名录 `C-MC-000028 SuperNova` / `C-MC-000029 Nova 2` / `C-MC-000030 Nova 3` 未混用。
2. 定价（约 8 千美元起）、销量、CPU 周期（约 800ns）与 SIMH 许可均已标「需核实」。
