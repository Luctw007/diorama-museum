# TASK-306-H 完成报告

> 任务 306-H（01 线）：引擎续 · 相机聚焦运镜实装（focus_node + focus_requested）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\godot\scripts\explode_controller.gd`（修改）：新增 `const FOCUS_DURATION_MIN := 0.9` / `FOCUS_DURATION_MAX := 1.2`；新增 `signal focus_requested(target: Vector3, duration: float)`；新增 `func focus_node(node: Node3D) -> Dictionary`——遍历 node 下 MeshInstance3D 的全局 AABB 求 {center, radius}，返回 `{center, radius, duration}` 并 emit `focus_requested`；`enter_subtree` 聚焦目标节点后调用。
- `D:\work\01\repo\01\docs\TASK-306-H_完成报告.md`（本报告）。

## 实装自证

- 常量：`FOCUS_DURATION_MIN := 0.9 / FOCUS_DURATION_MAX := 1.2`（depth_model §4 目标框缩放 0.8–1.2s 区间内）。
- 信号：`signal focus_requested(target: Vector3, duration: float)`（相机插值本体由 player.gd 消费，标待实机）。
- 函数：`focus_node(node)` 经 `_collect_meshes` 递归收集 MeshInstance3D，`global_transform * mesh.get_aabb()` 求全局 AABB 并 merge，`duration = clampf(lerpf(MIN, MAX, radius / 2.0), MIN, MAX)`；无网格返回空 Dictionary。
- 调用点：`enter_subtree` 找到聚焦目标节点后 `focus_node(focus_target)`（306-G 记录基准之后）。

## 与任务书的漂移

1. 新增 `_collect_meshes(root, out)` helper 做递归网格收集（任务书未列名，实现必需），计入自证。
2. 时长映射按半径规模在 0.9~1.2s 线性插值（radius/2.0 归一），母本只给区间未给公式——取最简线性口径并注释成文。
3. 执行备注：只 emit 信号与返回字典，实际相机 tween 插值标待实机（边界遵守，player.gd 只读对齐未改）；验收命令按仓库实际用 `python`；门禁干净复跑日志见下。
4. focus_node 的空网格防御：无 MeshInstance3D 或空 AABB 时返回空 Dictionary 且不 emit——避免无效运镜信号污染消费侧（player.gd 待实机接线时可直接忽略空返回）。
5. 时长公式 `clampf(lerpf(FOCUS_DURATION_MIN, FOCUS_DURATION_MAX, radius / 2.0), MIN, MAX)`：radius 0~2m 线性映射 0.9~1.2s、超界封顶——母本 0.8–1.2s 区间内取 0.9 起步，注释成文待实机校准。

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
