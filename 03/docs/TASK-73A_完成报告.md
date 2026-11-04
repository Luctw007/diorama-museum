# TASK-73A 完成报告（03 线 1/2）：Atari ST 设备包生产（个人机厅第八台）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-73A（03 线 1/2）：Atari ST 设备包生产 |
| 前置 | TASK-68（Amiga 500 0 FAIL） |
| 择定 | Atari ST（1985），demo_mode 起步，Hatari 预留真跑后端 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `content/atari-st/meta.json` | era 1985、localized、category=personal-computer | 五字段齐备 |
| `content/atari-st/runtime.json` | demo_mode、external_crt+speaker、键盘+鼠标 input_map | 7 动作 |
| `content/atari-st/assemblies/*.gltf` ×5 | 占位盒，节点名=node_id | 5 件 |
| `content/atari-st/assemblies/MESHES.md` | 真实尺寸依据 | — |
| `content/atari-st/annotations/annotations.json` | 30 条（≥30） | 15 role + 1 whole + 14 flow |
| `content/atari-st/encyclopedia.md` | **2,507 汉字**（≥2500） | — |
| `content/atari-st/THIRD_PARTY.md` | 三件套 + Hatari 预留 + TOS ROM 红线 | — |

校验：**validate 78 PASS / 0 FAIL**（退出码 0）+ **model_check MR-001~004 全过**（5/5 网格）。

## 二、五个占位盒与尺寸对照表

| assembly | 未来目标外观 | 尺寸依据 | 来源 |
|---|---|---|---|
| case | 机身壳（灰色紧凑机身，含软驱位） | 约 47×23×7 cm | Wikipedia（「需核实」） |
| keyboard | 键盘（一体式，含功能键区） | 与机身同宽 | Wikipedia（「需核实」） |
| motherboard | 主板（68000 + Shifter/GLUE/MMU + 512KB + TOS ROM） | 约 30×25 cm | Wikipedia（「需核实」） |
| floppy_drive | 3.5 英寸软驱（720KB） | 标准 3.5" 位 | Wikipedia |
| mouse | 两键鼠标 | 约 6×11 cm | Wikipedia（「需核实」） |

## 三、关键实现说明

1. **芯片组**：任务书"三芯片组"落地为 Shifter（显示）/ GLUE（总线胶合）/ MMU（内存管理）三颗 + DMA（软驱/硬盘控制，见 flow 标注），68000 主 CPU。
2. **input_map 键盘 + 鼠标**：5 键盘动作 + 2 鼠标动作（`motion`/`btn_left`），按 R-086 合法键名。
3. **display=external_crt**：Atari ST 接外接显示器（单色高分辨率或彩色），用 `external_crt` + `speaker` 共 2 个 output_sink。
4. **叙事锚点（flow）**：内置 MIDI、雅达利-康懋达 16 位对决、GEM 界面、单色高分辨率、MIDI 传承、TOS、ST 系列、DMA、桌面出版，共 14 条。
5. **Hatari 预留**：`runtime.emulator="none"`（demo_mode），Hatari（GPLv2）仅在 THIRD_PARTY 登记为预留后端，未下载、未内嵌；TOS ROM 红线照旧。

## 四、与 Amiga 500 的对比展呈建议

Atari ST 与 Amiga 500 同用 68000、几乎同时诞生、价位相近，是个人机厅"16 位对决"的最佳对照组，建议并置成"雅达利 vs 康懋达"双机台：

| 机 | 年代 | 芯片组 | 叙事角色 |
|---|---|---|---|
| Atari ST | 1985 | Shifter/GLUE/MMU | 音乐制作 + 桌面出版的"实干家"（内置 MIDI、单色高分辨率） |
| Commodore Amiga 500 | 1987 | Agnus/Denise/Paula | 图形与声音的"表演家"（4096 色、四声道立体声） |

- **对比点**：同是 68000，Amiga 把资源投给图形声音，Atari ST 把资源投给 MIDI 与单色高分辨率——"表演 vs 实用"两种设计哲学的正面碰撞。
- **互动建议**：可做"同一段 MIDI 旋律"演示（Atari ST 直接接合成器），对比 Amiga 的 Paula 采样回放，直观感受"音乐制作专用"与"多媒体播放"的差异。

## 五、开放问题

1. **Hatari 许可**：GPLv2 为公开信息，采用前建议再核实具体版本条款；真跑需 TOS ROM 合规获取。
2. **尺寸待核**：整机/主板尺寸为调研近真值，标「需核实」，正式建模以存世实机为准。
3. **目录回填**：Atari ST 已在 `计算机大类_目录_v2.jsonl` 回填 done + device_id=atari-st（全库 done 16）。
