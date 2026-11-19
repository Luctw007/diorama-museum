# TASK-213-A 完成报告

> 第二批 10 号设备包：Sun SPARCstation 1（目录 `C-WS-000005`，工作站）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡（复用） | `docs/research/hall-workstation/02_SPARCstation1.md` | 193-B 已产，本任务复用（证据 S113–S115） |
| meta.json | `content/sparcstation-1/meta.json` | id=sparcstation-1、era=1989、category=workstation、manufacturer=Sun Microsystems |
| runtime.json | `content/sparcstation-1/runtime.json` | emulator=`none`（保守）、sinks=external_crt+speaker、input_map 8 动作（5 键盘 + 3 鼠标） |
| assemblies | `content/sparcstation-1/assemblies/` | 7 装配（whole + 机身/主板/电源/硬盘/I-O接口/显示器 6 件 glTF）+ MESHES.md |
| annotations | `content/sparcstation-1/annotations/annotations.json` | 30 条（**flow 10** + role 20） |
| encyclopedia | `content/sparcstation-1/encyclopedia.md` | **2,502 汉字**（≥2500） |
| THIRD_PARTY | `content/sparcstation-1/THIRD_PARTY.md` | 三件套 + QEMU 需核实声明 + SunOS/Solaris 红线 |

## 验收日志

- **产包过 02 线 validate**：`validate.py content/sparcstation-1` → **84 PASS / 0 FAIL**（exit=0）；`model_check.py` → MR-01~04 全过。
- **目录反链 diff**：`C-WS-000005` → `planned→done`、`device_id null→sparcstation-1`、`research_doc null→docs/research/hall-workstation/02_SPARCstation1.md`（jsonl + md 同步）。
- **目录门禁复测**：`catalog_check.py` → CC-08 **FAIL 0 / PASS 34**；`catalog_ref_check.py` → **REF-01~04 全 0 · FAIL 0**（内容包 40 个）。
- **目录版本唯一性**：回填字段未新增版本文件，活跃目录仍「计算机 v2 + 通讯 v3」唯一。

## emulator 口径对齐结果

- **`emulator="none"`**：对齐 208-B 产包口径卡（QEMU sparc 需核实 + 01 线无 qemu 槽位 → 保守 none）。
- **SunOS/Solaris 镜像红线**：不入库、不下载、不提供、不再分发，只清单级引用。
- **flow 锚点**：RISC 走向桌面、Sun 黄金年代、SPARC 架构、与 DEC/HP 竞争、UNIX 工作站普及、网络即计算机、披萨盒设计等 10 条。

## 跨线发现（记于开放问题）

- **Apple IIe 已由 05 线产包 + 02 线 allocate id**：02 线 id_registry 在 2026-11-15 allocate 了 `C-PC-000208` 给 Apple IIe，05 线已产 `apple-iie` 包，目录 v2 中 Apple IIe 条目已被回填为 `done + device_id=apple-iie + research_doc=11_AppleIIe.md`。故第二批首批 Apple IIe 已闭环（非 03 线产包）。
- **CC-02 台账冲突误报**：`catalog_check` 的 CC-02 报「C-PC-000208 与 id_registry 台账冲突」——根因是 02 线 registry.jsonl 中该 id 的 `source_file=null`（allocate 时未回填来源文件），属 02 线 registry 回填缺陷，**非我线目录问题**（「跨文件重复」仍 0，PASS 810）。已记待 02 线回填 source_file。

## 开放问题

1. 目录中 SPARCstation 1 真实 id 确为 `C-WS-000005`（与定案表 v2 草案一致）。
2. 尺寸（约 40×10×40 cm）、主频/内存参数、QEMU 许可均已标「需核实」。
