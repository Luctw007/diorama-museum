# TASK-306-G 完成报告

> 任务 306-G（01 线）：引擎续 · 子树局部位移实装（explode_subtree + 局部基准形变记录）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\godot\scripts\explode_controller.gd`（修改）：新增 `const STEP_L2 := 0.06`（depth_model §4 L2 步距）；新增 `var _subtree_base := {}`（子树局部基准形变记录）；新增 `func explode_subtree(v: float) -> void`——对 `_subtree_focus` 对应 asmb_id 的子树节点沿局部轴二次爆炸 `offset = v × 相对深度 × STEP_L2`；`enter_subtree` 时记录 `_subtree_base`、`exit_subtree`/`set_close` 时复原清空。
- `D:\work\01\repo\01\docs\TASK-306-G_完成报告.md`（本报告）。

## 实装自证

- 常量：`const STEP_L2 := 0.06  # L2 子树二次爆炸步距（米，depth_model §4）`。
- 状态：`var _subtree_base := {}  # node -> Transform3D（enter_subtree 时记录）`。
- 函数：`explode_subtree(v)` 先校验 EXPLODED + 子树聚焦 + 基准非空，再以子树根 depth 为基准算相对深度 `rel = depth(node) - root_depth`，逐节点 `base + axis × v × rel × STEP_L2`。
- 记录/复原点：`enter_subtree` 经 `_subtree_nodes_of(asmb_id)` 收集子树（含根，parent 链上溯）记录各节点 transform；`exit_subtree` 逐节点复原后清空；`set_close` 依赖 `_set_state(CLOSED)` 全树复原、仅清空基准。
- funcs 计数：24 → 31（+7，含本件 `_subtree_nodes_of`/`explode_subtree` 与 306-H~K 四件）。

## 与任务书的漂移

1. 新增 `_subtree_nodes_of(root_id)` helper 支撑子树集合收集（parent 链上溯 + MAX_DEPTH 防御），任务书未列该函数名——为实现必需，已计入自证。
2. `set_close` 不重复写 transform（`_set_state(CLOSED)` 已按 `_base_transform` 复原全树），只清空 `_subtree_base`，避免把闭合态覆盖成爆炸态。
3. 执行备注：静态实装不实机（观感待用户实机）；验收命令按仓库实际用 `python`；门禁在无他线 python 进程窗口串行干净复跑，日志见下。
4. funcs 计数 24→31 的增量归属：本件 +2（_subtree_nodes_of/explode_subtree），306-H~K 四件 +5（focus_node/_collect_meshes/_apply_rep_highlight/get_breadcrumb/_set_subtree_visibility）——与 gd_symbol_check 复跑 funcs=31 一致。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd_symbol_check.py ==
== explode_controller.gd  [explode_controller] funcs=31 signals=4
汇总：17 文件；符号池 funcs 182 / signals 8；MISS 0；已知缺口 KG 0
SYM_RC=0

== gd_naming_check.py ==
扫描 17 个 gd；class_name 7 个；FAIL 0
NAM_RC=0
```
