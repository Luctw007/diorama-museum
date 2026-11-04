# TASK-27A 完成报告 — 建模预算校验器实现（v0.3 草案落地）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套代码按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-27A（02 线 1/2）：建模预算校验器实现 |
| 状态 | 完成 |
| 日期 | 2026-11-02 |
| 前置 | TASK-22（v0.3 建模章草案、全包索引） |

---

## 1. 交付物与行数

| 路径 | 行数 | 说明 |
|---|---|---|
| `tools/validate/model_check.py` | 355 | 建模预算校验器（纯 stdlib，MR-01~MR-04，`--json`） |
| `tools/validate/tests/run_model_tests.py` | 约 170 | 反例测试（7 个，全绿） |
| `docs/建模校验实测报告.md` | — | 8 包实测（含 pdp8/atari-2600） |
| `docs/TASK-27A_完成报告.md` | — | 本报告 |

校验：`py_compile` 全过；反例 7/7 全绿；未引入第三方库（glTF 仅解析 JSON 段 + 纹理文件头）。

## 2. 规则实现对照 v0.3 草案逐条表

| 规则 | 判定 | 对照 v0.3 草案 | 实现 |
|---|---|---|---|
| MR-01 节点命名 | 根节点 name = node_id（延续 R-090）；根节点 ≤1 | §2.2 命名、§8.2-2 根唯一 | 节点名不符 FAIL；多根 WARN |
| MR-02 三角面预算 | 逐 primitive 汇总，对照三档预算；未声明按 LOD1；超预算 WARN、超 1.5 倍 FAIL | §3 三档预算、§8.1-1/2 | 复用 `count_triangles_exact` |
| MR-03 贴图引用 | material→image 文件名后缀表；尺寸 ≤2048 且 2 的幂 | §5.1 贴图命名/尺寸、§8.1-6 | 复用 `image_size_from_file` |
| MR-04 单位与轴/扩展 | 未知扩展白名单外 WARN | §6.1、§8.2 强化点 | `extensionsUsed/Required` 白名单 |

> **三档预算取值**：LOD0 特写 50,000 / LOD1 观察 20,000 / LOD2 远景 8,000（单装配体三角面）。
> 本表已吸收 05 线 19 号冻结表的量级（case 观察档 12000、mainboard 18000 均落在 LOD1 20,000 内），
> 修正了 22-B 草案中"观察档 ≤2000"偏保守的起始值（详见 27-B 裁决）。

## 3. 实测汇总（8 包全过）

| 包 | 判档 | 网格 | FAIL | WARN |
|---|---|---|---|---|
| manchester-baby / eniac / edsac / edvac / pdp8（03） | LOD1 | 4/4/4/3/4 | 0 | 0 |
| apple-ii / atari-2600（05） | LOD1 | 4/6 | 0 | 0 |
| test-device（02 夹具） | LOD1 | 1 | 0 | 0 |

> 现状全部占位盒（1–12 三角面），无贴图、无扩展，故 MR-01/02/03/04 全过、无 WARN。完整逐包
> 表格与反例日志见《docs/建模校验实测报告.md》。

## 4. 反例测试日志原文

```text
======================================================================
TASK-27A 建模预算校验器反例测试（model_check.py）
======================================================================
[PASS] 反例01：节点名不符 → MR-01 FAIL  — exit=1, 命中 MR-01 FAIL
[PASS] 反例02：超预算（≤1.5 倍）→ MR-02 WARN  — exit=0, 命中 MR-02 WARN
[PASS] 反例03：超预算（>1.5 倍）→ MR-02 FAIL  — exit=1, 命中 MR-02 FAIL
[PASS] 反例04：贴图尺寸超 2048 → MR-03 WARN  — exit=0, 命中 MR-03 WARN
[PASS] 反例05：贴图尺寸非 2 的幂 → MR-03 WARN  — exit=0, 命中 MR-03 WARN
[PASS] 反例06：未知扩展 → MR-04 WARN  — exit=0, 命中 MR-04 WARN
[PASS] 反例07：场景多根 → MR-01 WARN  — exit=0, 命中 MR-01 WARN
----------------------------------------------------------------------
结果：PASS 7，FAIL 0
```

## 5. 与 budget_check.py 的职责边界

| 维度 | `budget_check.py`（既有） | `model_check.py`（本次） |
|---|---|---|
| 输入 | 单个 glTF 文件 + 可选 `--level` | 内容包（读 meta 的 mesh_ref 定位所有网格） |
| 三角统计 | 单文件精确统计 | 逐文件统计 + 对照三档 LOD 预算（超 1.5 倍 FAIL） |
| 纹理解析 | 单文件纹理尺寸报告 | 纹理命名后缀 + 尺寸 ≤2048 + 2 幂检查 |
| 命名/扩展 | 无 | MR-01 节点命名 + MR-04 扩展白名单 |
| 定位 | 作者自查单文件 | 包级批量 + 正式开产门禁 |

> 二者互补：budget_check 是"单文件精度自检"（给作者看），model_check 是"包级门禁"（卡超预算
> 资产入库）。model_check 复用了 budget_check 的 `count_triangles_exact` / `image_size_from_file`。

## 6. 开放问题

1. **三档预算数值为起始值**：LOD0 50,000 / LOD1 20,000 / LOD2 8,000 是吸收了 05 线量级后的
   "可调"起始值，正式 v0.3 定稿时需与 05 线 19 号冻结表的整机 40 万上限统一口径（27-B 处理）。
2. **LOD 档位声明机制**：当前按 `meta.precision_level` 映射档位；v0.3 是否新增显式 `lod_level`
   字段待裁决（22-B 开放问题 6）。
3. **MR-03 贴图命名与 05 线 ORM 命名冲突**：本工具后缀表为 `_metallic_roughness`，05 线 20 号
   用 `ORM`（R=Occlusion/G=Roughness/B=Metallic）三通道；27-B 需统一（裁决以规范为准）。
4. **MR-04 扩展白名单**：当前白名单收录常用 KHR_*，正式开产若引入 Draco/KTX2 需回写白名单。
5. **`assemblies/` vs `meshes/` 目录**：pdp8/atari-2600 用 `assemblies/`，其余用 `meshes/`；
   工具按 mesh_ref 定位天然兼容，但 v0.3 可考虑统一目录约定（27-B 裁决）。
