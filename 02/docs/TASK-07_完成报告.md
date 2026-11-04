# TASK-07 完成报告（内容包规范 v0.2 + 工具链强化）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套代码按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-07（续 02 线）：规范 v0.2 + 校验/预算/脚手架工具链强化 |
| 状态 | 完成（全部验收项达成）；**2026-10-31 经复跑修订，见《TASK-07_复跑修订报告.md》** |
| 日期 | 2026-10-31 |
| 前置基线 | TASK-02（规范 v0.1 + validate.py 36 规则 + test-device） |

---

## 1. 交付物清单（路径 + 行数统计）

| 路径 | 行数 | 说明 |
|---|---|---|
| `docs/内容包规范_v0.2.md` | 499 | **全文重写**（12 章 + 迁移表 + 规则表，正文 12856 字符去空白） |
| `content/schema/device_spec.schema.json` | 417 | schema v0.2（新增 localized/timeline/sinks/input_descriptor） |
| `tools/validate/validate.py` | 1111 | 校验器 v0.2（54 条规则，新增 R-080~R-091、R-017、R-089） |
| `tools/validate/budget_check.py` | 289 | 补完：glTF 精确统计 + PNG/JPEG 尺寸解析 |
| `tools/validate/scaffold_device.py` | 295 | 新增：设备包脚手架生成器 |
| `tools/validate/tests/run_tests.py` | 246 | 扩充：正例 + 19 反例 |
| `tools/validate/tests/tex_sample/` | — | 纹理解析夹具（2 PNG + 1 glTF） |
| `content/test-device/` | — | 增强：anim 标注/localized/sinks/input_map |
| `content/manchester-baby/` | — | 新骨架（仅骨架，内容由 08 线负责） |
| `docs/TASK-07_完成报告.md` | — | 本报告 |

---

## 2. 运行日志原文

### 2.1 validate.py（test-device，全绿）

```text
$ python validate.py ../../content/test-device
总计 54 条：PASS 54，FAIL 0
（退出码 0）
```

关键新增规则行摘录：

```text
PASS  R-017  -                          所有 materials 文件存在
PASS  R-071  meta.spec_version          spec_version='0.2' 为 0.2
PASS  R-080  annotations.timeline       timeline 结构合法
PASS  R-080  annotations.timeline       timeline highlight 引用存在
PASS  R-081  annotations.timeline       timeline 总时长≤预算(180s)
PASS  R-082  annotations.timeline       C4 级 anim 每镜头 caption 齐全
PASS  R-083  annotations.timeline       caption 无未定标记
PASS  R-084  runtime.output_sinks       sink surface 为命名枚举
PASS  R-085  annotations                annotation.surface 均已声明
PASS  R-086  runtime.input_map          input_map 键名合法
PASS  R-087  localized                  localized 结构完整；警告：以下字段缺 en（回退 zh）：['meta.intro', 'component.capacitor_c1.role']
PASS  R-088  meta.name_en               无 deprecated name_en（已迁移）
PASS  R-089  meta.era                   era=1980 合法
PASS  R-090  gltf                       glTF 网格节点名与 node_id 对应
PASS  R-091  THIRD_PARTY.md             THIRD_PARTY 行三件套（分档+URL+日期）合法
```

### 2.2 validate.py（manchester-baby 骨架，全绿）

```text
$ python validate.py ../../content/manchester-baby
总计 48 条：PASS 48，FAIL 0
（退出码 0）
```

### 2.3 run_tests.py（正例 + 19 反例全过）

```text
$ python tests/run_tests.py
[PASS] 正例：content/test-device 全绿  — exit=0, 汇总「FAIL 0」
[PASS] 反例01：缺引用 → R-014   [PASS] 反例02：循环父子 → R-012
[PASS] 反例03：命名违规 → R-021  [PASS] 反例04：缺 THIRD_PARTY → R-050
[PASS] 反例05：未定标记文案 → R-060  [PASS] 反例06：transform 越界 → R-032
[PASS] 反例07：materials 引用不存在 → R-017  [PASS] 反例08：timeline 起止倒置 → R-080
[PASS] 反例09：timeline 超预算 → R-081  [PASS] 反例10：C4 缺 caption → R-082
[PASS] 反例11：caption 未定标记 → R-083  [PASS] 反例12：sink 非法枚举 → R-084
[PASS] 反例13：surface 未声明 → R-085  [PASS] 反例14：input_map 键名非法 → R-086
[PASS] 反例15：localized 缺 zh → R-087  [PASS] 反例16：name_en 不一致 → R-088
[PASS] 反例17：era 越界 → R-089  [PASS] 反例18：glTF 节点名不符 → R-090
[PASS] 反例19：THIRD_PARTY URL 非法 → R-091
结果：PASS 20，FAIL 0
（退出码 0）
```

### 2.4 budget_check.py（glTF 精确统计 + 纹理解析）

```text
$ python budget_check.py ../../content/test-device/meshes/mainboard.gltf --level L2
glTF 版本 : 2.0  节点数 : 1  网格数 : 1  primitive 数 : 1  material 数 : 1
顶点数 : 3  三角面数 : 1（精确）  纹理数 : 0
结论 : 在预算内

$ python budget_check.py tests/tex_sample/sample_tex.gltf --level L2
material 数 : 2  纹理数 : 2
纹理名            宽      高     超限   来源
small_tex         64     32      否   sample_64x32.png
big_tex          2049   2049      是   big_2049.png
结论 : 超限（v0.2 不阻塞，供作者优化参考）
```

### 2.5 scaffold_device.py 自检（生成 manchester-baby 骨架）

```text
$ python scaffold_device.py ../../content/manchester-baby --name "曼彻斯特婴儿（SSEM）" \
    --name-en "Manchester Baby (SSEM)" --category experimental-computer --era 1948 \
    --manufacturer "曼彻斯特大学" --emulator fake
已生成设备包骨架：D:\work001\02\repo\content\manchester-baby
=== validate.py 自检 ===
总计 48 条：PASS 48，FAIL 0
自检通过：0 FAIL
（退出码 0）
```

---

## 3. 规则 ↔ 实现 ↔ 测试矩阵（§五）

| 编号 | 规范章节 | 实现函数 | 对应测试 | 结果 |
|---|---|---|---|---|
| R-017 | 第三章 assembly.materials | `_check_references`（materials 循环） | 反例07 | PASS |
| R-071（改） | 第三章 spec_version=0.2 | `_check_versions` | 正例 | PASS |
| R-080 | 第十章 timeline 结构 | `_check_anim_timeline` | 反例08 | PASS |
| R-081 | 第十章 时长上限 | `_check_anim_timeline` | 反例09 | PASS |
| R-082 | 第十章 C4 caption | `_check_anim_timeline` | 反例10 | PASS |
| R-083 | 第十章 caption 未定标记 | `_check_anim_timeline` | 反例11 | PASS |
| R-084 | 第十一章 sink 枚举 | `_check_sinks_and_input` | 反例12 | PASS |
| R-085 | 第十一章 surface 闭环 | `_check_sinks_and_input` | 反例13 | PASS |
| R-086 | 第十一章 input_map 键名 | `_check_sinks_and_input` | 反例14 | PASS |
| R-087 | 第十二章 localized 结构/回退 | `_check_localization` | 反例15 | PASS |
| R-088 | 第十二章 旧新字段一致 | `_check_localization` | 反例16 | PASS |
| R-089 | 第三章 era 范围 | `_check_localization` | 反例17 | PASS |
| R-090 | 第一章 glTF 节点命名 | `_check_gltf_names` | 反例18 | PASS |
| R-091 | 第八章 三件套 | `_check_third_party_strict` | 反例19 | PASS |

> 旧规则（R-001~R-072 中未改者）与实现/测试的对应关系在 TASK-02 已建立，本次沿用；R-061/R-062 的 `role` 文案改为检查 `role.zh`（localized 中文）。

---

## 4. v0.1 → v0.2 变更清单（逐字段级别）

| 变更 | v0.1 | v0.2 |
|---|---|---|
| `meta.name` | string | localized `{zh,en}`（zh 必填） |
| `meta.name_en` | string（正常字段） | **deprecated**，映射到 name.en（R-088） |
| `meta.intro` | 无 | 新增 localized（对应草稿 intro） |
| `meta.era` | 无 | 新增 integer 1800–2100（R-089） |
| `meta.manufacturer` | 无 | 新增 string（对应草稿） |
| `meta.presentation_level` | 无 | 新增 enum C2/C3/C4（缺省 C3） |
| `meta.spec_version` | "0.1" | "0.2"（R-071 改） |
| `assembly.role` | string | localized（R-061 检查 role.zh） |
| `assembly.materials` | 无 | 新增 array\<string\>（激活 R-017） |
| `component.role` | string | localized |
| `component.part_no` | 无 | 新增 string（对应草稿） |
| `runtime.output_sinks[].surface` | snake_case 任意 | 六枚举（R-084） |
| `runtime.input_map` 值 | string 物理路径 | `{map, key}` 对象（R-086） |
| `annotation` | 无 surface/timeline | 新增 surface（R-085）、timeline（R-080~083）、text_en |
| 预算表 | 三列 | 增「动画总时长」列（R-081 依据） |

---

## 5. 与 01 线 PROTOCOL、与 apple-ii 草稿的差异及建议

### 5.1 与 PROTOCOL.md（v1）

| 差异 | 说明 | 建议 |
|---|---|---|
| keyboard 键名 | v1 用 `a`/`space`/`enter`（小写）；v0.2 用 Godot `KEY_*` 大写 | 网关 v2 的 `input_event.key` 接受 `KEY_*`；后端做「`KEY_*`→键码」翻译层 |
| sink 路由 | v1 未实现（计划 FR-E4） | v0.2 先定 surface 枚举契约，网关 v2 实现多 sink 投放 |

### 5.2 与 apple-ii 草稿（04_DeviceSpec草稿.json）

| 草稿字段 | v0.2 处理 | 建议 |
|---|---|---|
| 顶层 `device_id` | 用 `meta.id` | 草稿迁移到 meta.id |
| `meta.name_zh`/`name_origin` | 映射 `name.zh`/`name.en` | 直接映射 |
| `accuracy_level` "L2+L3" | 用单级 `precision_level` | 草稿归一为单级（建议 L3，因有模拟方案） |
| `root_assembly` | 用 `parent:null` | 冗余，废弃 |
| `assemblies[].transform` 六元组 | 用 `{translation,rotation,scale}` | 六元组语义未定义，废弃 |
| `assemblies[].mesh` | 用 `mesh_ref` | 重命名映射 |
| `assemblies[].annotations` 内联 `{type,zh,highlights}` | 用 annotations.json + id 引用 | 内联扁平化到 annotations.json |
| `components[].role_zh`/`part_no` | `role.zh`/`part_no` | 直接映射 |
| `runtime.media_hint` 数组 | 单枚举 string | 多介质待定（见开放问题 3） |
| `runtime.emulator_alt`/`system_alt` | 未纳入 | 草稿临时字段，v0.2 不收敛，建议运行档机制承载 |
| `meta.sources` 编号（S01…） | URL 对象 | 入库时替换为真实 URL + 获取日期 |

---

## 6. 开放问题（每条带建议处理方式）

1. **术语对齐**：设计文档 v0.1 尚未生成，术语表以本规范为准。→ 建议：设计文档发布后核对 §3.2/附录 D，差异以设计文档为准并升版。
2. **input_map 与网关 v2 对齐**：`KEY_*` 键名需 01 线网关 v2 支持。→ 建议：TASK-06 网关 v2 在 `input_event.key` 增加 `KEY_*` 接受。
3. **media_hint 多介质**：草稿用数组（`floppy:5.25` + `cassette:audio`），v0.2 用单枚举。→ 建议：引入「运行档」或逗号分隔串，后续版本扩展。
4. **资产预算数字**：L1–L4 与动画时长上限为 v0.2 起始值。→ 建议：项目评审定稿后写死。
5. **纹理分辨率统计**：budget_check 已实现 PNG/JPEG 尺寸解析，但 validate 内未做纹理预算比对。→ 建议：后续将 budget_check 纹理检查并入 validate（升级为可选的 R-092）。
6. **面数统计精度**：glTF 顶点/三角面已精确统计，但 LOD/多 primitive 的「单模型」聚合口径待定。→ 建议：按 mesh 或按装配体聚合，评审确定。

---

## 7. 迭代记录（≥3 轮）

1. **第 1 轮**：编写 schema v0.2 后运行 validate，发现 schema 文件被并发同步回退为 v0.1（const=0.1、name=string），22 条 FAIL。→ 复写 schema 并立即校验（const=0.2、417 行），问题解决。
2. **第 2 轮**：scaffold 生成 manchester-baby 骨架自检 2 条 FAIL（`meta.intro.zh` 空串违反 minLength 1）。→ 脚手架改为省略可选 `intro` 字段，自检全绿。
3. **第 3 轮**：budget_check 初版纹理超限判断逻辑未接入渲染表。→ 补 `render_textures` 返回值接入，big_2049.png 正确标「是」超限；最终三套运行（validate/run_tests/budget_check）全部通过。

---

## 8. 给后续设备包生产任务（TASK-08 等）的指引

1. **用脚手架起步**：`python tools/validate/scaffold_device.py content/<device-id> --name "…" --era <年> --category …`，生成合法骨架后**只填内容不改结构**。
2. **localized 三件套**：`name`/`intro`/`role` 均写 `{zh, en}`；缺 en 不阻塞但会告警，正式交付应补齐。
3. **动画标注**：anim 标注用 `timeline` 描述镜头；C4 展示级必须逐镜头 `caption` 齐全；`surface` 必须引用已声明 sink。
4. **input_map**：动作名 snake_case，值用 `{map, key}`；keyboard 用 Godot `KEY_*`。
5. **预算自查**：`python tools/validate/budget_check.py <gltf> --level <L1..L4>` 核对顶点/三角面/纹理尺寸。
6. **红线**：正式文案禁「需核实/TBD/TODO/待定」；第三方资产在 THIRD_PARTY.md 填「分档+URL+日期」三件套。
