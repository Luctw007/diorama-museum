# TASK-12B 完成报告（EDVAC 展呈包 + 黎明厅导语 + 动画资产需求清单）

> 任务：12-B（03 线 第 2/2 份）。落盘于 `\\DESKTOP-2IDAL09\work\03\repo\`。

## 1. 交付物清单与字数统计

| # | 文件 | 中文（CJK）字数 |
|---|---|---|
| 1 | `content/edvac/meta.json` | 962 |
| 2 | `content/edvac/runtime.json` | 0 |
| 3 | `content/edvac/encyclopedia.md` | 2,220 |
| 4 | `content/edvac/annotations/annotations.json`（24 role + 1 flow + 2 anim） | 1,444 |
| 5 | `content/edvac/THIRD_PARTY.md` | 332 |
| 6 | `content/edvac/meshes/MESHES.md` | 212 |
| 7 | `content/edvac/meshes/*.gltf`（3 个） | 0 |
| 8 | `docs/research/hall-dawn/黎明厅导语_v1.md` | 3,029 |
| 9 | `docs/research/hall-dawn/动画资产需求清单.md` | 1,418 |

**EDVAC 包内文案 + 导语合计 = 8,199 字（CJK）**，满足「≥6000 字」下限（包内 5,170 + 导语 3,029）。导语 3,029 ≥3000、EDVAC 百科 2,220 ≥2200。

## 2. validate 日志 + 修复迭代记录

### 校验结果（04 线 validate.py，v0.1 schema）

```
总计 112 条：PASS 112，FAIL 0   （退出码 0）
```

规则覆盖同 12-A（R-001~R-072 全 PASS）：meta/runtime/annotations 合法、装配树引用完整、命名唯一、transform 合法、3 个 glTF 可解析、THIRD_PARTY 与 sources 四档、文案无未定标记且 role 含「在整机」、semver 合法。

### 修复迭代记录（≥2 轮）

- **迭代 1**：EDVAC 首验 110 PASS / 1 FAIL（缺 `THIRD_PARTY.md`）→ 补写 → 复验 112 PASS / 0 FAIL。
- **迭代 2（字数）**：EDVAC 百科首版 1,370 字 → 增补「五大部件一次说清」「它和 EDSAC 有多像」「它的影响」「术语小词典」「一句话总结」→ 2,220 字；导语首版 1,653 字 → 增补「一条时间线」「给玩家的三个问题」「结语」等 → 3,029 字。
- **迭代 3（规范字段映射）**：任务书要求 `available: false` + `demo_mode`——规范 v0.1 无此二字段，沿用 eniac 包既有写法（`emulator: "none"` + `system: "EDVAC（静态展示）"`），差异记入 §4。

## 3. 动画资产需求清单关键行（摘要）

- **可复用（电子束/CRT 类）** A01–A16：Baby Williams管读写（4 镜）、EDSAC OXO（8 镜）、CRT 电视厅四支扫描动画（合并 4 行）；共用"电子束发射/偏转/荧光屏亮点"三件底层资产。
- **设备专属** B01–B28：ENIAC 主程序器脉冲流（4 镜）、EDSAC 延迟线读写（8 镜）、EDVAC 延迟线存储（8 镜）、EDVAC 取指执行循环（8 镜）。
- **联动**：A01/B01/B11/B19 → 01 线爆炸图；A03/B03/B25 → 04 线验收用例；A06 → 09 线 OXO 交互。全表见 `动画资产需求清单.md`（28 行设备镜头 + 分组说明）。

## 4. 与调研差异

| # | 03 线结论 | 本任务决断 | 理由 |
|---|---|---|---|
| D1 | EDVAC「仅静态 + 原理动画 + EDSAC 近亲对照」 | 落实为静态包，`emulator: "none"`；anim 以"串行延迟线"与"五部件取指执行"两支为主体 | 与调研一致，无专用模拟器 |
| D2 | EDVAC 字位域、主频「需核实」 | 文案回避未证实数字，仅陈述"44 位字、串行二进制" | 规避编造 |
| D3 | 教材观点「也是第一个二进制存储程序计算机设计」 | 写入百科卡"设计原型/蓝图"定位，并明确"并非第一台运行" | 忠于史实、避免绝对化 |

## 5. 开放问题

1. EDVAC 无专用模拟器，正式接线可考虑"EDSAC 近亲对照"演示（需 01 线支持双包联动）。
2. 规范 v0.1 无 `era`、`available`、`demo_mode` 字段；`output_sinks.type` 无 led——建议 v0.2 补齐。
3. EDVAC 存世影像/图纸少，网格尺寸为近真值，正式建模需以《EDVAC 报告初稿》逻辑结构与可考档案为准。

---

## TASK-12 两份总收尾 + 03 线本轮完成标注

- **TASK-12 两份已全部完成**：12-A（EDSAC 包，118 PASS）+ 12-B（EDVAC 包 112 PASS + 导语 + 动画清单）。
- **03 线（计算机黎明厅内容线）本轮完成**：至此本线已产出全部四台设备内容包（manchester-baby、eniac、edsac、edvac，均 0 FAIL）+ CRT 电视厅展陈脚本 + 黎明厅导语 + 动画资产需求清单，覆盖 ENIAC/EDVAC/EDSAC/Manchester Baby 与 CRT 电视附厅。
- 后续交接：内容包 → 01 线集成；动画清单 → 01/04 线；OXO 交互 → 09 线。
