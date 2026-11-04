# TASK-12A 完成报告（EDSAC 设备包正式生产）

> 任务：12-A（03 线 第 1/2 份）——EDSAC 可入库级完整设备包。落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\edsac\`。

## 1. 交付物清单与字数统计

| # | 文件 | 中文（CJK）字数 |
|---|---|---|
| 1 | `content/edsac/meta.json`（装配树 + role + sources） | 1,125 |
| 2 | `content/edsac/runtime.json`（运行时配置） | 0（英文键值） |
| 3 | `content/edsac/encyclopedia.md`（百科卡全文） | 2,530 |
| 4 | `content/edsac/annotations/annotations.json`（27 role + 3 flow + 2 anim） | 1,735 |
| 5 | `content/edsac/THIRD_PARTY.md` | 445 |
| 6 | `content/edsac/meshes/MESHES.md` | 222 |
| 7 | `content/edsac/meshes/*.gltf`（4 个占位盒） | 0 |

**EDSAC 包内文案合计 = 6,057 字（CJK）**，满足「≥6000 字」下限（encyclopedia 2,530 ≥2500 + role 全集 + flow/anim caption 全量）。

## 2. validate 日志 + 修复迭代记录

### 校验结果（04 线 validate.py，v0.1 schema）

```
总计 118 条：PASS 118，FAIL 0   （退出码 0）
```

规则覆盖（逐条 PASS）：R-001~R-005（meta/runtime/annotations 合法 + runtime 与 meta.runtime 一致）；R-010~R-018（装配树引用完整、无环、双向一致、mesh_ref 存在）；R-020~R-023（命名合法、全局唯一）；R-030~R-033（19 装配体 transform 全部合法）；R-040~R-042（L2 + 4 个 glTF 可解析 version 2.0）；R-050~R-054（THIRD_PARTY + sources 四档授权）；R-060~R-063（无未定标记、「在整机」、role 字数 20–200、sources URL 合法）；R-070~R-072（semver）。

### 修复迭代记录（≥2 轮）

- **迭代 1**：首验 116 PASS / 1 FAIL（缺 `THIRD_PARTY.md`，R-050）→ 补写 THIRD_PARTY.md → 复验 118 PASS / 0 FAIL。
- **迭代 2（字数）**：百科卡首版 1,428 字，未达 ≥2500 字 → 增补「工作原理深入」「一段 EDSAC 指令长什么样」「复刻项目」「它和另外三台机器的关系」「术语小词典」「一句话总结」等 → 2,530 字，达标。
- **迭代 3（规范字段映射）**：任务书要求 `era: 1949`、`emulator` 对象、`media_hint: ["tape:program"]`——规范 v0.1 无 `era` 字段、`emulator` 为字符串、`media_hint` 为字符串枚举；决策：`category: early-computer` + 年代写进 description，`emulator: "qedsac"`，`media_hint: "tape"`，差异记入 §4。

## 3. 与调研底稿差异清单（决断/搁置及理由）

| # | 03 线结论 | 本任务决断 | 理由 |
|---|---|---|---|
| D1 | EDSAC「Warwick 闭源外链 + QEdsac 开源候选」 | runtime.emulator 定为 `qedsac`（开源候选），Warwick 版仅登记于 THIRD_PARTY 作外链 | 优先可内嵌的开源路径，符合 12-A「候选接线」要求 |
| D2 | QEdsac 版本/许可「需核实」 | 文件内 emulator="qedsac"、version="0.1.0"（占位）；「版本/许可需核实」进报告开放问题 | 「需核实」不进包内文案（红线） |
| D3 | EDSAC 主频 500 kHz、加/乘精确时间「需核实」 | 百科卡与文案中回避精确主频与加乘时间，仅陈述「串行二进制」与相对速度 | 规避未证实数字 |
| D4 | 调研 (d) 节装配树 | 落地为 4 层装配树（整机→子系统→单元→器件）+ 6 关键器件 | 满足「≥4 层」要求 |
| D5 | OXO 为招牌可玩点 | 落实为 anim 一支（8 镜头）+ flow「输出 CRT 显示」+ runtime sink `external_crt` | 把可玩点落到可执行标注 |

## 4. 开放问题

1. QEdsac 的精确版本号与 LICENSE 需在正式接线前核实（当前 version 占位 0.1.0）。
2. 规范 v0.1 无 `era` 字段；`output_sinks.type` 无 led 类型（指示氖灯映射为 video/mono1）——建议 v0.2 补齐。
3. EDSAC 主频 500 kHz、加/乘精确时间、功耗、占地重量等「需核实」项，正式上屏前需以复刻项目/原始档案核实。

## 5. 给 05 线（苹果 II 已产包）与 01 线（集成）的交接说明

- **05 线**：EDSAC 包沿用与 manchester-baby 一致的目录/字段风格，05 线苹果 II 包可参照本包 `meta.json` 的 `sources[]` 四档写法与 `runtime.json` 的 `input_map`（16 键）组织方式。
- **01 线**：`input_map` 已给出纸带装载/初始指令/启停等 16 个逻辑动作名；`output_sinks` 为 `external_crt`（video）、`indicator_led`（video）、`speaker`（audio），接线时按 PROTOCOL 对齐 surface 名；`meshes/MESHES.md` 给出 4 个占位盒的替换目标与尺寸依据，供建模任务取用。
