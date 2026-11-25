# TASK-306-J 完成报告

> 任务 306-J（01 线）：引擎续 · 面包屑状态实装（depth_breadcrumb）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\godot\scripts\explode_controller.gd`（修改）：新增 `var _breadcrumb: Array[String] = []`；新增 `func get_breadcrumb() -> Array`；`enter_subtree` 时 push 当前件名、`focus_rep` 时 push 代表件 role、`exit_subtree` 时 pop 回 L1；`set_close`/`_on_device_loaded` 清空数组。
- `D:\work\01\repo\01\docs\TASK-306-J_完成报告.md`（本报告）。

## 实装自证

- 状态：`var _breadcrumb: Array[String] = []  # 面包屑状态（数据即可，UI 归 04 线）`。
- 查询：`func get_breadcrumb() -> Array: return _breadcrumb.duplicate()`（返回副本防外部篡改）。
- push 点：`enter_subtree` 成功后 `_breadcrumb.append(asmb_id)`；`focus_rep` 成功后 `_breadcrumb.append(_rep_focus)`。
- pop/清空点：`exit_subtree` 循环 `pop_back()` 回 L1（L2/L3 项全移除）；`set_close`/`_on_device_loaded` 直接置空数组。

## 与任务书的漂移

1. 「exit_subtree 时 pop 回 L1」落地为循环清空（L1 全树视图无面包屑项）：若当前层级含 L3（focus_rep push 过），单次 pop 只回 L2 不符「回 L1」语义，故循环移除 L2/L3 全部项。
2. `get_breadcrumb` 返回 `duplicate()` 副本，避免外部直接改内部状态（防御性一行，语义同任务书）。
3. 执行备注：只落数据状态，UI 渲染归 04 线（depth_model §6 #7）；验收命令按仓库实际用 `python`；门禁干净复跑日志见下。
4. 面包屑与视图分档的对应：get_depth_level 返回 3（L3）时面包屑含 2 项（件名+role）、2（L2）时 1 项（件名）、1/0（L1/L0）时 0 项——与 306-G~K 状态清理点共用同一复位路径，无残留。
5. 层级元素口径：面包屑元素用 asmb_id（件名）与 role 字符串，非中文显示名——显示映射归 04 线 UI（depth_model §6 #7「数据即可，UI 归 04 线」）。
6. 顺序保证：push 均发生在状态置位成功之后（enter_subtree 校验拓扑通过才 push 件名、focus_rep 校验 role 存在才 push），失败路径不污染面包屑。

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
