# TASK-306-K 完成报告

> 任务 306-K（01 线）：引擎续 · 深层性能回收实装（子树视图 hide/show 批处理）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\godot\scripts\explode_controller.gd`（修改）：新增 `func _set_subtree_visibility(visible: bool) -> void`——按 `_subtree_focus` 判定子树节点集合，对非子树节点批量 `hide()`/`show()`（复用 `_depth` 拓扑）；`enter_subtree` 时隐藏非子树、`exit_subtree`/`set_close` 时全部 show。
- `D:\work\01\repo\01\docs\TASK-306-K_完成报告.md`（本报告）。

## 实装自证

- 函数：`_set_subtree_visibility(visible)`——visible 且 `_subtree_focus` 非空时，经 `_subtree_nodes_of(_subtree_focus)` 建子树集合，`_depth` 全节点按「在集合 show / 不在集合 hide」批量处理；visible=false 时全 show；`_subtree_focus` 为空且 visible=true 直接返回（防御）。
- 调用点：`enter_subtree` 成功置聚焦后 `_set_subtree_visibility(true)`；`exit_subtree` 清状态后 `_set_subtree_visibility(false)`；`set_close` 状态复位后 `_set_subtree_visibility(false)`。
- 正确性依据：非子树节点的 asmb 后代必为非子树（子树成员的祖先链全在子树内），故逐节点 hide 无「误藏子树成员」；只做可见性批处理，不删节点、不改资产。

## 与任务书的漂移

1. `enter_subtree` 的 hide 在记录 `_subtree_base` 与 `focus_node` 之后调用：隐藏前先完成基准记录与 AABB 计算（transform 未变，顺序无影响），顺序成文。
2. `set_close` 增加 show 调用（任务书写 exit_subtree/set_close 时全部 show 两条路径，set_close 即第二路径）。
3. 执行备注：验收命令按仓库实际用 `python`；门禁在无他线 python 进程窗口串行干净复跑，日志见下。
4. hide/show 与 306-G 局部位移的顺序：enter_subtree 先记录基准、再 hide 非子树（隐藏不影响 transform 记录）；exit_subtree 先复原子树形变、再全 show（可见性恢复前形变已回位）。
5. `_depth` 遍历只含 asmb 节点（_build_topology 构建），不存在非 Node3D 元素，hide/show 调用安全。

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
