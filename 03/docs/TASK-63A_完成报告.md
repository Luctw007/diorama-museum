# TASK-63A 完成报告（03 线 1/2）：ZX Spectrum 设备包生产（个人机厅第五台）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-63A（03 线 1/2）：ZX Spectrum 设备包生产 |
| 前置 | TASK-58（Macintosh 128K 0 FAIL） |
| 择定 | ZX Spectrum（1982），demo_mode 起步，Fuse 预留真跑后端 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `content/zx-spectrum/meta.json` | era 1982、localized、category=personal-computer | 五字段齐备 |
| `content/zx-spectrum/runtime.json` | demo_mode、external_crt(电视输出)+speaker、6 键盘动作 | — |
| `content/zx-spectrum/assemblies/*.gltf` ×5 | 占位盒，节点名=node_id | 5 件 |
| `content/zx-spectrum/assemblies/MESHES.md` | 真实尺寸依据 | — |
| `content/zx-spectrum/annotations/annotations.json` | 30 条（≥30） | 5 assembly role + 11 component role + 14 flow |
| `content/zx-spectrum/encyclopedia.md` | **2,617 汉字**（≥2500） | — |
| `content/zx-spectrum/THIRD_PARTY.md` | 三件套 + Fuse 预留 + ROM 红线 | — |

校验：**validate 78 PASS / 0 FAIL**（退出码 0）+ **model_check MR-001~004 全过**（5/5 网格）。

## 二、五个占位盒与尺寸对照表

| assembly | 未来目标外观 | 尺寸依据 | 来源 |
|---|---|---|---|
| case | 机身壳（黑色紧凑机身 + 右侧彩虹条纹） | 约 23.3×14.4×3.0 cm | Wikipedia（「需核实」） |
| keyboard | 橡胶键盘矩阵（40 键） | 约 20×10 cm | Wikipedia（「需核实」） |
| motherboard | 主板（Z80 + ULA + 48KB + 16KB ROM） | 约 21×13 cm | Wikipedia（「需核实」） |
| power | 外置电源 | 外置式 | Wikipedia（「需核实」） |
| expansion_port | 边框扩展口 | 与机身尾部等宽 | Wikipedia |

## 三、与 C64 / Apple II 的「三国对比台」站位建议

个人机厅"三国对比台"现有 C64（美国家用娱乐）、IBM PC 5150（美国开放标准）与 BBC Micro（英国国民教育）三机并列。ZX Spectrum 加入后，建议最新站位如下：

| 机 | 国别 | 叙事角色 | 对比台站位 |
|---|---|---|---|
| Commodore 64 | 美国 | 家庭娱乐 + 芯片音乐 | 左一（娱乐线） |
| Apple II | 美国 | 美国课堂 + 扩展生态 | 左二（生态线） |
| ZX Spectrum | 英国 | 廉价普及 + 卧室编程 | 右一（普及线） |
| BBC Micro | 英国 | 国民教育 + ARM 摇篮 | 右二（教育线） |

- **建议**：把两台英国机（Spectrum / BBC Micro）与两台美国机（C64 / Apple II）分组对置，凸显"英美两种普及路径"的对比；Spectrum 的彩虹条纹与 C64 的"面包盒"并置，是视觉冲击最强的组合。
- **互动建议**：可增设"同一段 BASIC 程序，四台机器上各是什么体验"的对比互动，让玩家感受 keyword 键盘 vs 全键盘、磁带 vs 软驱的差异。

## 四、开放问题

1. **Fuse 许可分档【需核实】**：GPL 为公开信息，采用前需核实具体版本条款；真跑需 ROM 合规（Sinclair/Amstrad 授权 ROM 分发协议）。
2. **尺寸待核**：机身/键盘/主板尺寸为调研近真值，标「需核实」，正式建模以存世实机为准。
3. **目录回填**：ZX Spectrum 已在 `计算机大类_目录_v2.jsonl` 回填 done + device_id=zx-spectrum（见 63-B 一并收尾）。
