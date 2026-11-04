# TASK-58B 完成报告（03 线 2/2）：Macintosh 128K 设备包生产（个人机厅第四台）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-58B（03 线 2/2）：Macintosh 128K 设备包生产 |
| 前置 | TASK-58A（可并行） |
| 择定 | Macintosh 128K（M0001），demo_mode 起步，Mini vMac 预留真跑后端 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `content/macintosh128k/meta.json` | era 1984、localized、category=personal-computer | 五字段齐备 |
| `content/macintosh128k/runtime.json` | demo_mode（emulator="none"）、internal_crt+speaker+led、键盘+鼠标 input_map | 9 动作 |
| `content/macintosh128k/assemblies/*.gltf` ×6 | 占位盒，节点名=node_id | 6 件 |
| `content/macintosh128k/assemblies/MESHES.md` | 真实尺寸依据 | — |
| `content/macintosh128k/annotations/annotations.json` | 36 条（≥35） | 17 role + 7 assembly role + 12 叙事锚点 |
| `content/macintosh128k/encyclopedia.md` | **2,607 汉字**（≥2500） | — |
| `content/macintosh128k/THIRD_PARTY.md` | 三件套 + Mini vMac 预留 + ROM 红线 | — |

校验：**validate 84 PASS / 0 FAIL**（退出码 0）+ **model_check MR-001~004 全过**（6/6 网格）。

## 二、六个占位盒与尺寸对照表

| assembly | 未来目标外观 | 尺寸依据 | 来源 |
|---|---|---|---|
| case | 一体机壳（米色，提手凹槽 + 内壁签名） | 约 34.5×24.4×27.7 cm | Wikipedia（「需核实」） |
| crt_display | 9 英寸黑白显像管（512×342） | 对角线 9 英寸 | Wikipedia |
| motherboard | 主板（68000 + 128KB + 64KB ROM） | 约 24×24 cm | Wikipedia（「需核实」） |
| floppy_drive | 3.5 英寸软驱（400KB） | 标准 3.5" 位 | Wikipedia |
| keyboard | 键盘（无方向键、无数字小键盘） | 约 34×14 cm | Wikipedia（「需核实」） |
| mouse | 单键鼠标（滚球） | 约 6×11 cm | Wikipedia（「需核实」） |

## 三、关键实现说明

1. **input_map 键盘 + 鼠标**：7 个键盘动作（KEY_POWER/RESET/ENTER/ESCAPE/SPACE/CTRL/ALT）+ 2 个鼠标动作（`motion`/`btn_left`，map="mouse"）。鼠标类按 R-086 合法键名预留，为后世 Mini vMac 接线准备。
2. **display=internal_crt**：9 英寸单显用 `internal_crt`（一体机内置 CRT，非外接），加 `speaker` + `led`，共 3 个 output_sink，全部命中 R-084 surface 枚举。
3. **叙事锚点落地为 flow 类型**：1984 超级碗广告、工程师签名内壁、Happy Mac 开机笑脸、Raskin 项目起源、乔布斯接手、GUI 面向大众、鼠标普及、桌面出版、字体系统、400KB 软驱、无方向键设计、MacWrite/MacPaint 共 12 条 flow 标注（R-005 type 枚举合规）。
4. **Mini vMac 预留**：`runtime.emulator="none"`（demo_mode 起步），Mini vMac（GPL【需核实】）仅在 THIRD_PARTY.md 登记为预留后端，未下载、未内嵌；ROM/系统镜像红线照旧（未提供任何 ROM/系统软件）。

## 四、与 04 线运行演示剧本的关系

- 若 04 线（44 号）引用 Macintosh 128K 作为演示展项，本包以 demo_mode 起步可支撑**静态 + 讲解**（开机笑脸/桌面/鼠标点选等可做原理动画）；
- 真跑需 01 线注册 Mini vMac 后端 + ROM 合规获取，本包已留好 input_map（鼠标 motion/btn_left）与 output_sink（internal_crt/speaker）接线位，届时回填 `runtime.emulator` 即可，无需改网格与标注。

## 五、TASK-58 两份总收尾

| 项 | 58-A 计算机目录 v2 | 58-B Macintosh 128K 包 |
|---|---|---|
| 交付物 | 计算机大类_目录_v2.jsonl + .md | content/macintosh128k/ |
| 规模 | 504 条（≥500） | 84 PASS / 0 FAIL |
| 校验 | catalog_check FAIL 0 + gate 错误 0 | validate 0 FAIL + model_check 全过 |
| 状态 | done（12 台已产包关联） | 新产包 1 台 |

## 六、开放问题

1. **Mini vMac 许可分档【需核实】**：GPL 为公开信息，但本项目采用前应再核实其具体版本条款；真跑需 ROM 合规流程。
2. **尺寸待核**：一体机壳/主板/键盘/鼠标尺寸为调研近真值，标「需核实」，正式建模以存世实机为准。
3. **目录登记（已回填）**：Macintosh 128K 在 `计算机大类_目录_v2.jsonl` 已由 planned 回填为 **done** 并关联 `device_id=macintosh128k`（C-PC-000007），全库 done 由 12 增至 **13**；catalog_check 复跑仍 0 FAIL。
