# TASK-02 完成报告

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套代码按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-02《内容包规范 v0.1》与自动校验工具链 |
| 状态 | 完成（全部验收项达成） |
| 日期 | 2026-10-31 |

---

## 1. 交付物清单

| 路径 | 说明 |
|---|---|
| `docs/内容包规范_v0.1.md` | 规范文档（权威版，九章齐全、逐字段无歧义、规则编号 R-xxx） |
| `content/schema/device_spec.schema.json` | JSON Schema（draft 2020-12，覆盖 meta/assemblies/components/runtime/annotation） |
| `tools/validate/validate.py` | 校验器 Cmd 入口（零依赖，35 条规则，结构化报告） |
| `tools/validate/budget_check.py` | 资产预算独立检查器（glTF 节点/面数统计，L1–L4 对照） |
| `tools/validate/tests/run_tests.py` | 测试套件（正例 + 6 类反例） |
| `content/test-device/` | 最小可过校验示例设备包「验证方块机」（假想设备） |
| `README.md` | 仓库根说明（TASK-01/02 合并说明） |
| `docs/TASK-02_完成报告.md` | 本报告 |

---

## 2. 校验器运行日志

### 2.1 示例包（全绿）

```text
$ python validate.py ../../content/test-device
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
PASS  R-020  meta.id                    device-id 'test-device' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/surface id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[whole]          translation 为 3 个有限实数
PASS  R-031  assemblies[whole]          rotation 为单位四元数
PASS  R-032  assemblies[whole]          scale 各分量 > 0
PASS  R-033  assemblies[whole]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[mainboard]      translation 为 3 个有限实数
PASS  R-031  assemblies[mainboard]      rotation 为单位四元数
PASS  R-032  assemblies[mainboard]      scale 各分量 > 0
PASS  R-033  assemblies[mainboard]      scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[mainboard]      glTF 可解析（version=2.0）
PASS  R-042  assemblies[mainboard]      预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
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
总计 40 条：PASS 40，FAIL 0
（退出码 0）
```

### 2.2 反例样例（缺引用，component.assembly 悬空）

```text
$ python validate.py <临时包（components[0].assembly = "no_such_board"）>
FAIL  R-014  components[chip_cpu]       引用的 assembly 'no_such_board' 不存在
总计 40 条：PASS 39，FAIL 1
（退出码 1）
```

### 2.3 预算检查器

```text
$ python budget_check.py ../../content/test-device/meshes/mainboard.gltf --level L2
文件       : ../../content/test-device/meshes/mainboard.gltf
glTF 版本 : 2.0
场景数    : 1
节点数    : 1
网格数    : 1
三角面数  : 1（估算）
精度分级  : L2（v0.1 起始预算，可调）
  面数上限: 20000  节点上限: 500  纹理上限: 2048px
结论      : 在预算内
```

### 2.4 测试套件

```text
$ python run_tests.py
[PASS] 正例：content/test-device 全绿  — exit=0, 汇总「FAIL 0」
[PASS] 反例1：缺引用（component.assembly 悬空）   — exit=1, 命中 R-014
[PASS] 反例2：循环父子（装配树成环）             — exit=1, 命中 R-012
[PASS] 反例3：命名违规（节点 id 非 snake_case）  — exit=1, 命中 R-021
[PASS] 反例4：缺 THIRD_PARTY.md                 — exit=1, 命中 R-050
[PASS] 反例5：含未定标记文案                     — exit=1, 命中 R-060
[PASS] 反例6：transform 越界（scale 分量 = 0）   — exit=1, 命中 R-032
结果：PASS 7，FAIL 0
```

---

## 3. 规则表 R-xxx 清单

| 编号 | 规则（一句话） |
|---|---|
| R-001 | meta.json 存在且为合法 JSON |
| R-002 | meta.json 通过 schema 校验 |
| R-003 | runtime.json 存在且通过 $defs/runtime 校验 |
| R-004 | runtime.json 与 meta.json.runtime 逐字节等价 |
| R-005 | annotations.json 存在且通过 $defs/annotations_document 校验 |
| R-010 | parent 引用存在 |
| R-011 | children 引用存在 |
| R-012 | 装配树无环 |
| R-013 | parent/children 双向一致 |
| R-014 | component.assembly 引用存在 |
| R-015 | annotation.target 引用存在 |
| R-016 | mesh_ref 文件存在 |
| R-017 | （预留）外部材质引用检查，v0.1 未启用 |
| R-018 | 引用的 annotation id 存在 |
| R-020 | device-id 符合 kebab-case |
| R-021 | 节点 id 符合 snake_case |
| R-022 | annotation/surface id 符合 snake_case |
| R-023 | 节点 id 全局唯一 |
| R-030 | translation 为 3 有限实数 |
| R-031 | rotation 为单位四元数 |
| R-032 | scale 各分量 > 0 |
| R-033 | scale 在 [1e-6, 1e6] |
| R-040 | precision_level ∈ {L1..L4} |
| R-041 | mesh_ref glTF 存在且可解析 |
| R-042 | 面数/节点预算（v0.1 仅统计不阻塞） |
| R-050 | THIRD_PARTY.md 存在 |
| R-051 | 第三方行必填 URL + 获取日期 |
| R-052 | source.url 为 http/https |
| R-053 | source.license 四档枚举 |
| R-054 | source.accessed_at 为日期 |
| R-060 | 文案不含未定标记 |
| R-061 | role 文案含「在整机」 |
| R-062 | role 标注字数 20–200 |
| R-063 | 标注 sources URL 合法 |
| R-070 | meta.version 为 SemVer |
| R-071 | meta.spec_version == 0.1 |
| R-072 | engine_min_version 为 SemVer |

---

## 4. 设计取舍说明

1. **自研轻量 JSON Schema 校验，而非引入 `jsonschema`**：仅需支持本规范 schema 用到的构造子集（type/properties/required/additionalProperties/items/enum/pattern/const/minLength/minItems/maxItems/$ref/$defs），自研约 120 行即可覆盖，换来**零第三方依赖、跨平台可移植、行为可控**。schema 校验错误统一归入 R-002/R-003/R-005；命名/引用/transform 等专项规则另按编号独立报告，便于作者定位。
2. **面数统计的降级实现**：v0.1 阶段 `validate.py` 的 R-042 仅做统计输出（不阻塞），精确预算比对由 `budget_check.py` 独立提供。理由：早期 glTF 几何可能不完整，机械阻断会误伤；纹理分辨率统计未实现（见开放问题）。
3. **`runtime` 双写**：`meta.json.runtime` 与 `runtime.json` 逐字节等价（R-004）。`runtime.json` 供引擎独立加载运行时配置，`meta.json` 内嵌副本保证 DeviceSpec 单文件自足；等价性由校验器强制。
4. **正/反例构造方式**：反例由 `run_tests.py` 从示例包复制并施加单一破坏后运行校验器，避免维护大量静态 fixture 文件、且每次破坏点明确对应唯一规则。
5. **根装配体豁免**：R-061「含「在整机」」对根装配体（整机）及其 role 标注豁免，因为整机自身无法「在整机中」描述。

---

## 5. 开放问题与「需核实」清单

1. **术语对齐**：设计文档 v0.1 尚未生成，本规范术语表为自行定义，须与设计文档 §3.2 / 附录 D 核对，差异以设计文档为准。
2. **input_map 键名**：须与 TASK-01 `PROTOCOL.md` 消息定义对齐（§7.3）。
3. **资产预算数字**：L1–L4 为 v0.1 起始值（可调），最终值待设计文档 D4 或项目评审确定。
4. **纹理分辨率统计**：`budget_check.py` 未解析纹理分辨率，纹理预算检查待补。
5. **R-017**：外部材质引用检查预留，待 material 引用字段引入后启用。

---

## 6. 给后续设备包生产任务（TASK-05 等）的指引

1. **先建包再写内容**：复制 `content/test-device/` 目录结构作为起点，改 `meta.id` 为你的 `device-id`（kebab-case），逐字段填写 DeviceSpec。
2. **边写边验**：每完成一个装配体/元器件/标注，运行 `python tools/validate/validate.py content/<device-id>`，看到 FAIL 立即按规则编号定位修复；提交前必须全绿（退出码 0）。
3. **守红线**：正式文案不得出现「需核实/TBD/TODO/待定」等标记——不确定的内容写进完成报告的「开放问题」，不要留在 `role`/`text` 里；非根装配体与元器件的 role 必须含「在整机」。
4. **许可合规**：任何非自产资产，在 `THIRD_PARTY.md` 表里填「来源 URL + 获取日期」并在 `meta.sources` 登记四档授权；无授权来源的资产一律不进包。
5. **预算自查**：网格交付后跑 `python tools/validate/budget_check.py <gltf> --level <L1..L4>` 核对节点/面数是否在预算内。
6. **glTF 约定**：米制 1:1、Y-up 右手系、四元数单位化、`asset.version` 为 2.x；坐标系差异在导入时烘焙，不依赖运行时翻转。
