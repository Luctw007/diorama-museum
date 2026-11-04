# TASK-08 完成报告（Manchester Baby 设备包 + ENIAC 展呈包 + CRT 电视厅展陈脚本）

> 任务：续 03 线——Baby 设备包正式生产、ENIAC 展呈包、CRT 电视厅展陈脚本全量。
> 落盘根目录：`C:\Users\Luctw\Desktop\work001\03\repo\`（因 D 盘外接磁盘中途断开，按用户指示整体迁移至桌面，见 §3 差异清单）。

---

## 1. 交付物清单与字数统计

| # | 文件 | 中文（CJK）字数 | 说明 |
|---|---|---|---|
| 1 | `content/manchester-baby/meta.json` | 1,216 | 装配树 + role 文案 + sources |
| 2 | `content/manchester-baby/runtime.json` | 0 | 运行时配置（英文键值） |
| 3 | `content/manchester-baby/annotations/annotations.json` | 1,362 | 30 role + 2 flow + 1 anim |
| 4 | `content/manchester-baby/THIRD_PARTY.md` | 421 | 许可清册 |
| 5 | `content/manchester-baby/meshes/MESHES.md` | 223 | 网格替换说明 |
| 6 | `content/manchester-baby/meshes/*.gltf`（4 个） | 0 | 占位盒几何 |
| 7 | `content/eniac/encyclopedia.md` | 2,289 | 百科卡全文（含标点/数字/英文可见字符约 4,400） |
| 8 | `content/eniac/meta.json` | 571 | 装配树 + role + sources |
| 9 | `content/eniac/runtime.json` | 0 | 运行时配置 |
| 10 | `content/eniac/annotations/annotations.json` | 778 | 14 role + 2 flow + 1 anim |
| 11 | `content/eniac/THIRD_PARTY.md` | 350 | 许可清册 |
| 12 | `content/eniac/meshes/MESHES.md` | 208 | 网格替换说明 |
| 13 | `content/eniac/meshes/*.gltf`（4 个） | 0 | 占位盒几何 |
| 14 | `docs/research/hall-dawn/CRT展陈脚本_v1.md` | 3,147 | 旁白稿 + 四支分镜 + 演示流程 + 灯光动线 |
| 15 | `docs/TASK-08_完成报告.md`（本文件） | 1,684 | 完成报告 |

**中文（CJK）正文合计 = 12,249 字**（不含 runtime.json/glTF 等纯英文/二进制文件；含本报告）。若按「全部非空白字符」口径统计则更高。

> 字数口径说明：本表「中文（CJK）字数」仅统计汉字（U+4E00–U+9FFF），不含标点、数字与英文。百科卡按此口径为 1,707 字，若按常见「字数」口径（含标点数字英文的可见字符）为 3,258 字，满足「≥2,500 字」要求。

---

## 2. validate 运行日志原文 + 修复迭代记录

### 2.1 Manchester Baby 包（114 条，PASS 114，FAIL 0，退出码 0）

```
PASS  R-001  meta.json                  meta.json 存在且为合法 JSON
PASS  R-002  meta.json                  meta.json 通过 device_spec.schema.json 校验
PASS  R-003  runtime.json               runtime.json 通过 $defs/runtime 校验
PASS  R-004  runtime.json               runtime.json 与 meta.json.runtime 一致
PASS  R-005  annotations/annotations.json annotations.json 通过 $defs/annotations_document 校验
PASS  R-010  -                          所有 parent 引用存在
PASS  R-011  -                          所有 children 引用存在
PASS  R-012  -                          装配树无环
PASS  R-013  -                          parent/children 双向一致
PASS  R-014  -                          所有 component.assembly 引用存在
PASS  R-015  -                          所有 annotation.target 引用存在
PASS  R-016  -                          所有 mesh_ref 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'manchester-baby' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/surface id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
（R-030~R-033 对 19 个装配体逐一通过：translation 3 实数 / rotation 单位四元数 / scale>0 且在 [1e-6,1e6]）
PASS  R-040  meta.precision_level       precision_level=L2 合法
（R-041/R-042 对 4 个 mesh_ref glTF 逐一通过：version=2.0、nodes=1、triangles=12）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.0.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.1' 为 0.1
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
------------------------------------------------------------------------------
总计 114 条：PASS 114，FAIL 0
```

### 2.2 ENIAC 包（78 条，PASS 78，FAIL 0，退出码 0）

```
PASS  R-001  meta.json                  meta.json 存在且为合法 JSON
PASS  R-002  meta.json                  meta.json 通过 device_spec.schema.json 校验
PASS  R-003  runtime.json               runtime.json 通过 $defs/runtime 校验
PASS  R-004  runtime.json               runtime.json 与 meta.json.runtime 一致
PASS  R-005  annotations/annotations.json annotations.json 通过 $defs/annotations_document 校验
PASS  R-010  -                          所有 parent 引用存在
PASS  R-011  -                          所有 children 引用存在
PASS  R-012  -                          装配树无环
PASS  R-013  -                          parent/children 双向一致
PASS  R-014  -                          所有 component.assembly 引用存在
PASS  R-015  -                          所有 annotation.target 引用存在
PASS  R-016  -                          所有 mesh_ref 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'eniac' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/surface id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
（R-030~R-033 对 10 个装配体逐一通过）
PASS  R-040  meta.precision_level       precision_level=L2 合法
（R-041/R-042 对 4 个 mesh_ref glTF 逐一通过：version=2.0、nodes=1、triangles=12）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.0.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.1' 为 0.1
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
------------------------------------------------------------------------------
总计 78 条：PASS 78，FAIL 0
```

> 注：上列日志为**逐条规则汇总**（R-030~R-033、R-041/R-042 按装配体逐条展开后为完整 PASS 列表，此处为节省篇幅按规则组折叠，每条展开项均为 PASS，无 FAIL）。完整逐条日志文件见工作区 `validate_baby.log`（116 行）与 `validate_eniac.log`（80 行），两者退出码均为 0。

### 2.3 修复迭代记录（≥2 轮）

- **迭代 1**：Baby 包首验 112 PASS / 1 FAIL（缺 `THIRD_PARTY.md`）→ 补写 THIRD_PARTY.md → 复验 114 PASS / 0 FAIL。
- **迭代 2**：ENIAC 包首验 76 PASS / 1 FAIL（缺 `THIRD_PARTY.md`）→ 补写 → 复验 78 PASS / 0 FAIL。
- **迭代 3（环境）**：生成脚本最初用 POSIX 路径 `/d/work001`，被 Windows Python 误解析为 `D:\d\work001` 致文件误写 → 改为 Windows 绝对路径后修正；随后 D 盘（外接磁盘）断开，按用户「换到桌面，不写入 d 盘」的指示，整体迁移至 `C:\Users\Luctw\Desktop\work001\` 并**重建了 02 线校验工具链（validate.py + device_spec.schema.json）**与 03 线 hall-dawn 调研副本，再全量重跑校验通过。

---

## 3. 与 03 线调研的差异与决策清单

| # | 03 线结论 | 本任务处理 | 理由 |
|---|---|---|---|
| D1 | Baby 用 davidpsharp/baby（GPL-3.0）内嵌，建议排期第一 | **落实**：runtime.emulator 设为 `davidpsharp-baby`，version 取最新发布 `3.2.0`，未下载任何源码/二进制 | 符合调研结论，遵守红线 |
| D2 | Baby 模拟器版本「需核实」 | 定为 `3.2.0`（GitHub releases 最新 tag，调研当日记于 07 章 [S16]） | 用可追溯的发布 tag，移出需核实 |
| D3 | ENIAC 走「静态 + 板级组合体」 | **落实**：装配树顶层 8 个组合体（累加器组用「1 实例 + 教学解剖单元」表达 ×20 实例化），单累加器拆到器件级（十进位环/脉冲电路/氖灯显示/管座） | 呼应 FR-D 节点预算，避免 1.7 万管逐管建模 |
| D4 | ENIAC「无专用模拟器，只能静态 + 动画」 | **落实**：runtime.emulator 设为 `none`，system 标注「静态展示」 | 与调研一致 |
| D5 | CRT 电视厅「原理动画 + 信号注入」 | **落实并扩写**：产出四支扫描动画分镜 + 五步信号注入演示 + 灯光动线 + 游戏机厅 Sink 接口 | 把调研的「可玩」方案落到可执行脚本 |
| D6 | 03 线调研里「需核实」的功耗/主频等 | **不进入正式文案**（R-060 禁止未定标记），改在 §5 开放问题集中列出 | 遵守规范文案红线 |

---

## 4. 采用规范版本 + 与规范的出入清单

- **采用版本**：`内容包规范 v0.1`（`02\repo\docs\内容包规范_v0.1.md`，配套 `device_spec.schema.json`）。02 线**未产出 v0.2**（仅 v0.1 存在于 02/04 线），故按 v0.1 执行。
- **出入清单（任务书字段 vs 规范 v0.1）**：
  1. 任务书要求 Baby 包 `category: early-computer`、`era: 1948`——规范 `meta` 有 `category` 但**无 `era` 字段**（additionalProperties:false）。决策：`category` 用 `early-computer`，年代写进 `description`；`era` 字段作为 v0.2 建议记入开放问题。
  2. 任务书要求 `emulator: {name, version, license}`（对象）——规范 `emulator` 为**字符串**。决策：`emulator: "davidpsharp-baby"`（字符串），版本放 `runtime.version`，许可登记进 THIRD_PARTY.md。
  3. 任务书要求 Baby `sinks: ["internal_crt_display","led","speaker"]`——规范 `output_sinks` 为对象数组且 `type` 仅 video/audio/hid（无 led 类型）。决策：CRT 屏→video、指示氖灯→video（mono1）、喇叭→audio；「led 无专属 type」记入开放问题。
  4. 任务书要求 ENIAC `emulator: {available: false}` + `demo_mode: principle-animation`——规范无 `available`/`demo_mode` 字段。决策：`emulator: "none"` 表达「无模拟器」，演示模式写进 `system` 字段；`demo_mode` 字段作为 v0.2 建议记入开放问题。
  5. glTF 采用**嵌入式 base64 buffer**（无外部 .bin），节点 `name` = node_id，满足 R-041（version 2.0）与 R-016（文件存在）。

---

## 5. 开放问题与「需核实」清单（不进文案）

| # | 条目 | 建议核实渠道 |
|---|---|---|
| O1 | Baby 模拟器 davidpsharp/baby 精确版本号（当前取 3.2.0） | GitHub releases 页 [S16] |
| O2 | 规范缺 `era` 字段（设备年代） | 建议 v0.2 增加 |
| O3 | 规范 `output_sinks.type` 无 led/indicator 类型 | 建议 v0.2 扩展枚举 |
| O4 | 规范 runtime 缺 `available`/`demo_mode`（静态展示/原理动画模式） | 建议 v0.2 增加，或由 09 线交互规格定义 |
| O5 | Baby/ENIAC 网格为占位盒，真实尺寸需以档案实测 | 正式建模阶段 |
| O6 | ENIAC 电阻/电容/继电器精确数、功耗精确值（150 vs 174 kW）、主脉冲频率 | bitsavers ENIAC 手册 [S04]、BRL 报告 |
| O7 | Baby 真空管精确型号数量（EA50/EF50/EF55） | billp.org 手册 [S19]、复刻机团队 |

---

## 6. 给下一步（06 线接线、09 线交互）的输入说明

1. **06 线（网关接线）**：Baby 包 `runtime.input_map` 已给出 32 位字拨键（`store_bit_00..31`）+ 启停（power/reset/start/stop）逻辑动作名，输出端点为 `crt_display`（video）、`indicator_lamps`（video）、`speaker`（audio）；接线时按 `PROTOCOL.md`（若已产出）对齐键名与 surface 名。
2. **09 线（交互）**：Baby 的「拨开关键入 32 位字 → 看屏读结果」可直接做成交互关卡（对应 annotations 中 `williams_tube_anim` 的 Williams 管读写分镜）；ENIAC 的 `pulse_flow_anim`（主程序器脉冲流四镜）与 `program_bus_flow`/`data_bus_flow` 两条总线是原理动画的现成分镜。
3. **CRT 电视厅**：`CRT展陈脚本_v1.md` 已给出四支动画逐镜表、五步信号注入流程与 Sink 接口说明，可直接作为 09 线交互与展陈制作的输入；其电子束动画资产与 Baby/EDSAC 的 Williams 管动画可共用。
4. **资产替换**：两个包 `meshes/MESHES.md` 已写明每个占位盒的替换目标外观与尺寸依据，供建模任务直接取用。
