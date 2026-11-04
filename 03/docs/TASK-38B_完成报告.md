# TASK-38B 完成报告：IBM PC 5150 设备包生产（个人机厅第二台）

> 任务：38-B（03 线 2/2）。产出 `content/ibm5150/` 完整设备包。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\ibm5150\`。
> 依据：hall-personal/02_IBMPC5150.md（预研）。

## 0. 规范版本说明

同 38-A：02 线 v0.4 仅为草案（未定稿），本任务**按 v0.3 执行**，`meta.spec_version` 取 `"0.2"`，并跑 `model_check.py`（MR-001~004）。

## 1. 交付物清单与校验结果

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1981、manufacturer、intro/description/category 齐备 | ✅ |
| 2 | `runtime.json` | emulator="pc86box"（预留真跑）、output_sinks（external_crt+terminal+speaker+led）、input_map 7 动作对象格式 | ✅ |
| 3 | `assemblies/*.gltf`（6 件） | case/front_panel/motherboard/monitor/keyboard/power，节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 32 条（≥30，含开放式架构、ISA 槽、BIOS 自检流程讲解锚点） | ✅ |
| 6 | `encyclopedia.md` | **2,529 汉字**（≥2500，开放标准/克隆机生态） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全 + BIOS 红线声明 | ✅ |

**校验结果**：

```text
validate.py  总计 84 条：PASS 84，FAIL 0   （退出码 0）
model_check  MR-01 节点命名 / MR-02 三角面 / MR-03 贴图 / MR-04 扩展 —— 全 PASS（6/6 网格）
```

## 2. emulator 字段取值说明（关键偏离记录）

- 任务书要求"emulator 预填 86box"。但内容包 schema 的 `emulator` 正则 `^[a-z][a-z0-9_-]*$` **要求首字符为小写字母**，`"86box"` 以数字 `8` 开头，会被 R-003 拒绝（已用 schema 实测验证：`"86box"` 匹配失败、`"vice"`/`"pc86box"` 匹配成功）。
- 为满足"validate FAIL 0"硬性要求，本包采用**合规拼写 `"pc86box"`**（语义清晰映射到 86Box），并在报告中记录该偏离。
- **建议**：01 线注册 86Box 后端时统一 id（可沿用 `pc86box` 或修订 schema 正则以允许数字开头），03 线随后同步。

## 3. 尺寸对照表（占位盒 vs 02_IBMPC5150.md 档案）

| 占位盒 | 占位盒实际（单位盒） | 档案/真实尺寸（「需核实」） | 结论 |
|---|---|---|---|
| case.gltf | 1 m³（半长 0.5） | 主机箱（卧式）约 50×40×15 cm | 占位几何 |
| front_panel.gltf | 同上 | 前面板（双软驱位 + 红色电源拨杆） | 占位几何 |
| motherboard.gltf | 同上 | 主板约 35×30 cm | 占位几何 |
| monitor.gltf | 同上 | 单色显示器（MDA 5151）约 32×30 cm | 占位几何 |
| keyboard.gltf | 同上 | 键盘（83 键 Model F）约 50×18 cm | 占位几何 |
| power.gltf | 同上 | 电源（内置 + 散热风扇） | 占位几何 |

## 4. 与 C64 的"互不兼容同台对比"展呈建议（个人机厅叙事锚点）

| 维度 | Commodore 64 | IBM PC 5150 |
|---|---|---|
| CPU | MOS 6510（6502 系） | Intel 8088（x86 系） |
| 路线 | 低价家庭娱乐 | 开放架构商用标准 |
| 显示 | 接电视机（彩色） | 单色 MDA / 彩色 CGA |
| 存储 | 磁带 + 1541 软驱 | 5.25" 软驱 |
| 结局 | Commodore 1994 倒闭 | 标准延续至今 |

**叙事锚点**：两台机器并置，构成"互不兼容年代"最直观的对照——一台走娱乐、一台走标准；一台最终落幕、一台演化成你今天所用的每一台电脑。建议在两台设备之间设"互不兼容"互动展项（如"同一段数据在这两台机器上为何读不出来"），点题"开放标准为何最终胜出"。

## 5. TASK-38 两份总收尾

- **38-A（Commodore 64 设备包）**：完整产出并 **0 FAIL**（validate 78 PASS + model_check 全过），详见 `docs/TASK-38A_完成报告.md`。
- **38-B（IBM PC 5150 设备包）**：完整产出并 **0 FAIL**（validate 84 PASS + model_check 全过），本报告。

## 6. 开放问题

1. **display/fps 字段未落地**（沿用 23-A 阻塞结论）。
2. **BIOS/系统镜像红线**：IBM PC 真跑依赖 BIOS ROM 与 MS-DOS 镜像，需统一"固件/系统授权"流程。
3. **emulator id "86box" 与 schema 正则冲突**：见 §2，需 01 线注册时统一 id 或 02 线修订正则。
4. **各部件精确尺寸**：卧式机箱/键盘/显示器尺寸「需核实」，正式建模以存世实机为准。
5. **GPL 模拟器嵌入边界**：86Box 为 GPLv2，内嵌/衍生须同 GPL 开源，首选外链 + 教程。
