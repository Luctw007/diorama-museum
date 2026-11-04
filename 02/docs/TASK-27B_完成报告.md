# TASK-27B 完成报告 — 规范 v0.3 定稿 + 全包索引 v2

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套文档按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-27B（02 线 2/2）：规范 v0.3 定稿 + 全包索引 v2 |
| 状态 | 完成 |
| 日期 | 2026-11-02 |
| 前置 | TASK-27A（model_check.py 落地） |

---

## 0. TASK-27 两份总收尾 + 02 线本轮完成标注

- **27-A**：`tools/validate/model_check.py`（355 行，MR-001~004）+ `tools/validate/tests/run_model_tests.py`（7 反例全绿）+ `docs/建模校验实测报告.md` + `docs/TASK-27A_完成报告.md`。
- **27-B**：`docs/内容包规范_v0.3.md`（全文定稿）+ `docs/全包索引.md`（v2）+ `docs/TASK-27B_完成报告.md`。
- **02 线本轮（TASK-27）完成**：建模预算校验器落地 + 规范 v0.3 定稿 + 全包索引刷新。

## 1. 交付物与变更清单统计

| 路径 | 说明 |
|---|---|
| `docs/内容包规范_v0.3.md` | 全文定稿，卷首变更清单 **11 条**（≥10），并入建模章 |
| `docs/全包索引.md` | 重新生成（v2，11 device-id 去重 / 12 包目录） |
| `docs/TASK-27B_完成报告.md` | 本报告 |

## 2. 变更清单全表（v0.2.1 → v0.3，11 条）

| # | 位置 | 旧文 | 新文 | 缘由 |
|---|---|---|---|---|
| 1 | 第十三章（新增） | 无 | 建模与网格章全文 | 22-B 草案定稿 |
| 2 | §1.3 坐标系 | 仅列 Y-up | 补 Blender→Godot 导出对照 | DCC/引擎轴不一致 |
| 3 | §5 预算 | 仅 L1–L4 | 补三档距离 LOD（50k/20k/8k） | 27-A 判定依据 |
| 4 | §13.2 命名 | 草案"mesh 名=node_id" | 仅 node 名=node_id 硬约束 | 与占位盒惯例一致 |
| 5 | §13.5 贴图 | "metallic=R" | ORM 三通道（R=Occl/G=Rough/B=Metal） | 吸收 05 线 20 号 |
| 6 | §13.5 材质 | 无 material-id 约定 | `mat_<材质>_<色系>` | 吸收 05 线 20 号 |
| 7 | §13.1 目录 | "一装配体一文件于 meshes/" | assemblies/ 与 meshes/ 并存 | 27-A 实测 |
| 8 | §13.8 校验 | "预研不做实现" | MR-001~004 落地 | 27-A 实现 |
| 9 | 附录 C | 仅 v0.1→v0.2 | 增占位盒替换协议 | 22-B §7 定稿 |
| 10 | 附录 B | legacy 跟踪点 | 增建模章开放问题 | 27-A/B 裁决闭环 |
| 11 | 卷首工具 | 无 model_check | 列入 model_check（MR-001~004） | 27-A 交付 |

## 3. 裁决记录表（规范 > 线内文档，冲突处二选一）

| # | 冲突点 | 22-B 草案 | 05 线 19/20 号 | 裁决 | 理由 |
|---|---|---|---|---|---|
| D1 | 三档 LOD 数值 | LOD0 特写 20k / LOD1 观察 2k | 系数制（×0.4/1.0/2.5），case 观察 12000 | 采纳 05 线量级：LOD0 50k / LOD1 20k / LOD2 8k | 草案"观察 2k"偏保守，会迫使低模；05 线量级符合博物馆写实 |
| D2 | 网格命名 | "根 mesh 名=node_id" | node 名=node_id，mesh 名 `<node_id>_mesh` | node 名=node_id 唯一硬约束 | 存量占位盒全部 `panel_mesh`/`whole_mesh`，草案过度要求 |
| D3 | 贴图通道 | metallic=R, roughness=G | ORM 三通道（R=O/G=R/B=M） | 采纳 ORM 三通道 | glTF 生态标准省采样做法 |
| D4 | 材质命名 | 描述性名 | `mat_abs_beige` 等 | 采纳 material-id 约定 | 统一 R-017 引用 |
| D5 | 坐标轴 | 草案取 +Y 上 | 05 线也是 +Y 上 | +Y 上（一致，无冲突） | 任务文档"+Z 上"为笔误 |
| D6 | 目录 | meshes/ | assemblies/（pdp8/atari-2600） | 二者并存，按 mesh_ref 定位 | 27-A 实测兼容 |

## 4. 运行日志原文（三段）

### 4.1 run_tests（含新增反例）全绿

```text
$ python tools/validate/tests/run_tests.py
结果：PASS 21，FAIL 0

$ python tools/validate/tests/run_model_tests.py
[PASS] 反例01 节点名不符 → MR-01 FAIL
[PASS] 反例02 超预算(≤1.5倍) → MR-02 WARN
[PASS] 反例03 超预算(>1.5倍) → MR-02 FAIL
[PASS] 反例04 贴图尺寸超2048 → MR-03 WARN
[PASS] 反例05 贴图非2幂 → MR-03 WARN
[PASS] 反例06 未知扩展 → MR-04 WARN
[PASS] 反例07 场景多根 → MR-01 WARN
结果：PASS 7，FAIL 0
```

### 4.2 test-device 全绿

```text
$ python tools/validate/validate.py content/test-device
总计 54 条：PASS 54，FAIL 0
```

### 4.3 全包 validate 全 0 FAIL（regress_all）

```text
$ python tools/regress/regress_all.py
| 1 | 02/repo/content/manchester-baby | 48 | 48 | 0 | PASS |
| 2 | 02/repo/content/test-device | 54 | 54 | 0 | PASS |
| 3 | 03/repo/content/edsac | 132 | 132 | 0 | PASS |
| 4 | 03/repo/content/edvac | 126 | 126 | 0 | PASS |
| 5 | 03/repo/content/eniac | 92 | 92 | 0 | PASS |
| 6 | 03/repo/content/manchester-baby | 128 | 128 | 0 | PASS |
| 7 | 03/repo/content/pdp11 | 78 | 78 | 0 | PASS |
| 8 | 03/repo/content/pdp8 | 72 | 72 | 0 | PASS |
| 9 | 03/repo/content/system360 | 78 | 78 | 0 | PASS |
| 10 | 05/repo/content/apple-ii | 272 | 272 | 0 | PASS |
| 11 | 05/repo/content/atari-2600 | 128 | 128 | 0 | PASS |
| 12 | 05/repo/content/famicom | 100 | 100 | 0 | PASS |
汇总：12 包，PASS 12，FAIL 0
```

> **包数说明**：任务文档写"共 8 个规范包"，执行期间 03/05 线并行新增 famicom / pdp11 / system360，
> 现共 **11 个 device-id（12 个包目录，含 02 骨架副本）**，全 0 FAIL。索引 v2 已按实际 11 包生成。

## 5. legacy 兼容触发点跟踪

- **input_map legacy 字符串移除触发条件**（§11.2）：待全部量产包 input_map 对象化 + 评审通过后移除。
  - 现状盘点：05 线 apple-ii 已对象化（57 键）；03 线 manchester-baby/eniac/edsac/edvac 仍 legacy 字符串；
    新增 pdp8/pdp11/system360/atari-2600/famicom 的 input_map 形态见各自包（未逐一核对，留待对象化任务）。
  - 该跟踪点随 v0.3 继续有效，未满足前不得收紧 R-086。

## 6. 开放问题

1. **三档 LOD 文件组织**：同名分阶段替换 vs `_lod0/1/2` 多文件并存（待引擎支持，§13.7/附录 B）。
2. **MR-003 贴图后缀统一**：`_metallic` vs `_orm` 命名待定（当前二者兼容）。
3. **LOD 档位声明机制**：由 `precision_level` 映射，是否新增 `lod_level` 字段待定。
4. **透明/折射材质**：CRT 玻璃真透明 vs OPAQUE+emissive 假透明，需实测。
5. **新增包 input_map 对象化**：pdp8/pdp11/system360/atari-2600/famicom 的 legacy 迁移待排期。

## 附：本轮全部交付物（TASK-27）

| 文件 | 说明 |
|---|---|
| `tools/validate/model_check.py` | 建模预算校验器（355 行） |
| `tools/validate/tests/run_model_tests.py` | 反例测试（7 个全绿） |
| `docs/建模校验实测报告.md` | 8 包实测 |
| `docs/TASK-27A_完成报告.md` | 27-A 完成报告 |
| `docs/内容包规范_v0.3.md` | 规范 v0.3 定稿 |
| `docs/全包索引.md` | 索引 v2（11 包） |
| `docs/TASK-27B_完成报告.md` | 本报告 |
