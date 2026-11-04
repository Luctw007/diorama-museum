# TASK-43A 完成报告：BBC Micro 设备包生产（个人机厅首批收官）

> 任务：43-A（03 线 1/2）。产出 `content/bbcmicro/` 完整设备包。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\bbcmicro\`。
> 依据：hall-personal/03_BBCMicro.md（预研）。

## 0. 规范版本说明

02 线已定稿最新规范为 **v0.4**（`内容包规范_v0.4.md`，TASK-37A，并入「音频资产」第十四章）。本包**按 v0.4 执行**：`meta.spec_version` 仍为 `"0.2"`（v0.4 未引入字段结构级变更）；v0.4 新增的音频章（A-01~04）本轮只定义不实现、无 audio_check 工具，且本包为占位盒阶段**不产音频资产**（无需 `audio/` 目录与 `SYNTH.md`），故无新增校验项；仍跑 `model_check.py`（MR-001~004）。

## 1. 交付物清单与校验结果

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1981、manufacturer、intro/description/category 齐备 | ✅ |
| 2 | `runtime.json` | emulator="beebem"（预留真跑）、output_sinks（external_crt+speaker+led）、input_map 7 动作对象格式 | ✅ |
| 3 | `assemblies/*.gltf`（5 件） | case（斜角键盘台）/keyboard/motherboard（6502+Video ULA）/power/external_box（Tube 预留位），节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 35 条（≥30，含计算机素养计划、电视节目联动、Tube 第二处理器讲解锚点） | ✅ |
| 6 | `encyclopedia.md` | **2,562 汉字**（≥2500，英国教育市场/Acorn 与 ARM 祖先渊源） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全 + ROM 红线声明 | ✅ |

**校验结果**：

```text
validate.py  总计 78 条：PASS 78，FAIL 0   （退出码 0）
model_check  MR-01 节点命名 / MR-02 三角面 / MR-03 贴图 / MR-04 扩展 —— 全 PASS（5/5 网格）
```

## 2. 迭代记录（≥2 轮）

- **迭代 1（R-061 文案）**：首验 74 PASS / 3 FAIL——external_box 的 tube_connector / second_processor_slot 两条 role 文案误写「在外接盒中」而非「在整机中」（R-061 要求含「在整机」），且缺 THIRD_PARTY.md。→ 修正两处文案 + 写 THIRD_PARTY.md → 复验 78 PASS / 0 FAIL。
- **迭代 2（字数）**：encyclopedia 首版 1,491 汉字 → 增补「深度解读七~十」（Elite / Acorn 与 RISC / Econet / 存储生态）+「结语」+「技术档案速览」→ 2,562 汉字。

## 3. 尺寸对照表（占位盒 vs 03_BBCMicro.md 档案）

| 占位盒 | 占位盒实际（单位盒） | 档案/真实尺寸（「需核实」） | 结论 |
|---|---|---|---|
| case.gltf | 1 m³（半长 0.5） | 主机壳（斜角键盘台）约 40×35×8 cm | 占位几何 |
| keyboard.gltf | 同上 | 键盘（含红色功能键排）约 40×15 cm | 占位几何 |
| motherboard.gltf | 同上 | 主板（6502+Video ULA）约 30×20 cm | 占位几何 |
| power.gltf | 同上 | 电源（内置） | 占位几何 |
| external_box.gltf | 同上 | 外接盒（Tube 预留位）约 20×15×6 cm | 占位几何 |

## 4. 与 C64 / IBM 的"三国对比"展呈建议（个人机厅叙事锚点）

| 维度 | Commodore 64 | IBM PC 5150 | BBC Micro |
|---|---|---|---|
| CPU | MOS 6510（6502 系） | Intel 8088（x86 系） | MOS 6502 |
| 路线 | 低价家庭娱乐 | 开放架构商用标准 | 国民教育 |
| 关键遗产 | 芯片音乐、大众普及 | PC 标准、兼容机产业 | BBC BASIC、ARM 架构 |
| 结局 | Commodore 1994 倒闭 | 标准延续至今 | 孕育出 ARM |

**叙事锚点**：三台机器构成"互不兼容年代"最直观的三国对比——娱乐 / 标准 / 教育，三种理念、三种 CPU、三种结局。建议设"三国对比台"居中，配"同一段数据为何在三台机器上读不出来"的互动演示，点题"互不兼容"。BBC Micro 作为教育路线的代表，其"ARM 摇篮"身份是区别于另两台的差异化亮点。

## 5. BeebEm 真跑衔接说明（仅预留，未下载）

| 项 | 说明 |
|---|---|
| 本包 emulator | `"beebem"`（预填，预留真跑）——BeebEm 二进制未就位、01 线未注册 beebem 模拟器 |
| BeebEm 许可 | GPL，主站 `http://www.mkw.me.uk/beebem/` |
| ROM 红线 | BBC BASIC/MOS ROM 受版权保护，BeebEm 不含 ROM，需用户提供合法镜像；本包未下载、未提供 ROM |
| 预留接线 | 未来真跑：01 线注册 `beebem` 模拟器 → 二进制就位 → 引导用户提供 ROM 即可真跑（本报告记录，不落地改动） |

## 6. 开放问题

1. **display/fps 字段未落地**（沿用 23-A 阻塞结论）。
2. **ROM 授权流程**：BBC Micro 真跑依赖 BBC BASIC/MOS ROM，需统一"固件授权"流程。
3. **各部件精确尺寸**：斜角键盘台机身/主板/电源尺寸「需核实」，正式建模以存世实机为准。
4. **Apple II 归属**：个人机厅四台中的 Apple II 归 05 线，其设备包与证据不在本线；导语与展呈需向 05 线取该包 meta/sources（见 43-B 导语需补清单）。
5. **GPL 模拟器嵌入边界**：BeebEm 为 GPL，内嵌/衍生须同 GPL 开源。
