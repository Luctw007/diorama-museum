# TASK-17A 完成报告 — v0.1→v0.2 迁移助手 migrate_package.py

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套代码按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-17A（02 线 第 1/2 份）：内容包 v0.1 → v0.2 迁移助手 |
| 状态 | 完成 |
| 日期 | 2026-11-02 |
| 前置 | TASK-07 复跑修订（v0.2 规范/schema/校验器全绿） |

---

## 1. 交付物与行数统计

| 路径 | 行数 | 说明 |
|---|---|---|
| `tools/migrate/migrate_package.py` | 460 | 迁移助手（纯 stdlib，`--dry-run`/`--apply`/`--validate`，幂等） |
| `tools/migrate/README.md` | 约 90 | 用法、转换对照表、边界（哪些不做） |
| `tools/migrate/demo/` | — | 四包副本演练（manchester-baby / eniac / edsac / edvac，均已 apply 后 v0.2 全绿） |

校验：`python -m py_compile tools/migrate/migrate_package.py` 通过；未改 `D:\work\01/03/04/05` 任何文件。

---

## 2. 四包演练日志原文

### 2.1 dry-run（manchester-baby 完整 diff 代表，其余三包结构相同）

```text
== manchester-baby ==
  ~ meta.name
      - '曼彻斯特 Baby（SSEM）'
      + {"zh": "曼彻斯特 Baby（SSEM）", "en": "Manchester Baby (SSEM)"}
  - meta.name_en
      (删除：'Manchester Baby (SSEM)')
  ~ meta.spec_version
      - '0.1'
      + '0.2'
  ~ assemblies[whole].role
      - '曼彻斯特 Baby（SSEM）整机，世界第一台运行存储程序的电子数字计算机...'
      + {"zh": "曼彻斯特 Baby（SSEM）整机，世界第一台运行存储程序的电子数字计算机实验样机，由 Williams、Kilburn 与 Tootill 于 1948 年在曼彻斯特大学建成，用于验证 Williams 管 CRT 存储器。"}
  ...（assemblies[].role 共 19 条、components[].role 共 11 条，逐一 string → {"zh":原文}）
  · 提示：meta.version='1.0.0' 保持不变（建议迁移性小版本 1.1.0，需人工确认）
  · 提示：meta.intro 缺失（v0.2 可选新增字段，未改写）
  · 提示：meta.era 缺失（v0.2 可选新增字段，未改写）
  · 提示：assemblies[].role 共 19 条由 string 迁 localized
  · 提示：components[].role 共 11 条由 string 迁 localized

  [dry-run] 未写入（加 --apply 落盘）
```

### 2.2 apply + validate（四包逐包）

```text
==================== manchester-baby --apply --validate ====================
  · 提示：assemblies[].role 共 19 条由 string 迁 localized
  · 提示：components[].role 共 11 条由 string 迁 localized
  [apply] 已写入 meta.json
  [apply] 复检：无需迁移（幂等 OK）
  [validate] 总计 128 条：PASS 128，FAIL 0

==================== eniac --apply --validate ====================
  · 提示：assemblies[].role 共 10 条由 string 迁 localized
  · 提示：components[].role 共 4 条由 string 迁 localized
  [apply] 已写入 meta.json
  [apply] 复检：无需迁移（幂等 OK）
  [validate] 总计 92 条：PASS 92，FAIL 0

==================== edsac --apply --validate ====================
  · 提示：assemblies[].role 共 20 条由 string 迁 localized
  · 提示：components[].role 共 7 条由 string 迁 localized
  [apply] 已写入 meta.json
  [apply] 复检：无需迁移（幂等 OK）
  [validate] 总计 132 条：PASS 132，FAIL 0

==================== edvac --apply --validate ====================
  · 提示：assemblies[].role 共 19 条由 string 迁 localized
  · 提示：components[].role 共 5 条由 string 迁 localized
  [apply] 已写入 meta.json
  [apply] 复检：无需迁移（幂等 OK）
  [validate] 总计 126 条：PASS 126，FAIL 0
```

### 2.3 迁移前基线（对照，v0.1 状态 validate）

```text
manchester-baby    总计 137 条：PASS 125，FAIL 12   （R-002×10 + R-088 + R-071，与《真实包校验报告》§1 一致）
eniac              总计 101 条：PASS 89，FAIL 12    （同上）
edsac              总计 141 条：PASS 129，FAIL 12   （v0.1 结构同类失败；已生产，见 §4 附注）
edvac              总计 135 条：PASS 123，FAIL 12   （同上）
```

### 2.4 幂等性测试（apply 后二次运行）

```text
===== manchester-baby（二次运行）=====
== manchester-baby ==
  无需迁移（已是 v0.2 结构）
  · 提示：meta.version='1.0.0' 保持不变（建议迁移性小版本 1.1.0，需人工确认）
（eniac / edsac / edvac 同输出「无需迁移（已是 v0.2 结构）」）
```

> **关于演练数据来源的说明**：本任务开工时，03 线四包仍为 v0.1（本报告 §2.3 基线即取自该状态）。
> 演练进行期间，03 线 TASK-18A「四包 v0.2 迁移清零」已把源包迁到 v0.2（`spec_version=0.2`、
> `version=1.1.0`、`name/role` 已 localized）。为完整演示本工具的迁移闭环，演练在 02 线自己的
> `demo/` 副本上按机械迁移的逆变换还原出 v0.1 夹具，再执行 dry-run → apply → validate。
> 本工具不改任何他线源文件。

---

## 3. 转换对照表（工具实测行为）

| 位置 | v0.1 | v0.2（工具输出） | 校验 |
|---|---|---|---|
| `meta.name` | string | `{"zh":原值, "en":name_en}` | R-002 消除 |
| `meta.name_en` | string | 删除（并入 name.en） | R-088 消除 |
| `meta.spec_version` | `"0.1"` | `"0.2"` | R-071 消除 |
| `meta.version` | `1.0.0` | 保持不变（仅提示 1.1.0） | R-070 仍合法 |
| `assemblies[].role` | string | `{"zh":原文}` | R-002 消除 |
| `components[].role` | string | `{"zh":原文}` | R-002 消除 |

---

## 4. edsac 的 R-090 定位报告

**现象**：edsac 装配体 `control_subsystem` 的 `mesh_ref` 指向 `meshes/console.gltf`，但该 glTF
场景根节点名（及网格名）为 `console` / `console_mesh`，不等于装配体 `node_id`（`control_subsystem`），
违反 R-090（规范 v0.2 §1.4：装配体所引用 glTF 的场景根节点名/网格名必须等于该装配体 `node_id`）。

**具体文件与位置**：

| 项 | 内容 |
|---|---|
| 包 | `content/edsac` |
| 装配体 | `assemblies[]` 中 `id == "control_subsystem"` |
| `mesh_ref` | `meshes/console.gltf` |
| glTF 文件 | `content/edsac/meshes/console.gltf` |
| 违规点 | `nodes[0].name == "console"`、`meshes[0].name == "console_mesh"`、scene 根节点 `console` |
| 期望 | 三者应等于 `control_subsystem` |

**建议修法（他线修复建议，本线不改他线文件）**，二选一：

1. **改 glTF（推荐）**：把 `console.gltf` 内 `nodes[0].name` 由 `console` 改为 `control_subsystem`，
   并把 `meshes[0].name` 由 `console_mesh` 改为 `control_subsystem_mesh`——保持 `meta.json` 的
   `node_id` 与引用不变，R-090 即通过；
2. **改 meta.json**：把装配体 `id` 由 `control_subsystem` 改为 `console`，并同步更新所有引用
   （`whole.children`、`parent`、`components[].assembly`、`annotations[].target`）——改动面更大，不推荐。

**现状**：截至本报告成文，03 线已在 TASK-18A 中按方案 1 完成修复（`console.gltf` 节点已改名
`control_subsystem`、网格已改名 `control_subsystem_mesh`），edsac 现已 R-090 通过。

**附注（额外发现）**：edsac `runtime.output_sinks[]` 中 `indicator_led_0` 的 `surface` 原为
`indicator_led`（不在 R-084 八枚举内，应为 `led`），同类数据错误，03 线亦已一并修正为 `led`。
这两处均不属于本迁移工具的机械转换范围，故列入「人工/他线修复项」而非工具改写项。

---

## 5. 开放问题（人工迁移项清单）

1. **`meta.version` 小版本**：工具默认不自动递增，作者需人工确认是否 `1.0.0 → 1.1.0`（03 线已按 1.1.0 落）。
2. **`meta.intro` / `meta.era` / `meta.manufacturer` 缺失**：四包均未填（v0.2 可选新增字段），需内容线补写，工具不自动造文案。
3. **`runtime.input_map` legacy 字符串 → 结构化 `{map,key}`**：不在本工具机械范围，属 17-B 裁决的迁移窗口（详见 v0.2.1 §11.2），待人工/后续工具迁移。
4. **R-084 / R-090 类数据错误**：不属于 localize 迁移，需作者或对应内容线人工修（edsac 两处已由 03 线修复）。
5. **工具边界**：`migrate_package.py` 只改 `meta.json`；若未来需迁移 `annotations[].text_en` 或 `intro` 等，需另起工具或人工。
