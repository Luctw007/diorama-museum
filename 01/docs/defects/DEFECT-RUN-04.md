# DEFECT-RUN-04（实机首验缺陷 · closed）

> 状态：**closed（2026-11-05 修复提交 92b1b0d）** · 修复已入 main
> 复现环境：Godot 4.4 · 用户实机按 F5 · 项目"警告即错误"开启
> 档案补登：本档案由 06 线 debug 专员按 git 提交记录补登（原档欠登）；现象为按修复 diff 与项目已知前科反推，用户原始报屏未存留。

## 现象

走近设备按拆解键（E）→ 输出面板红字运行时栈追踪：
`null instance` 调用（`entry.get("transform")` 为 null 时继续 `.get("translation")`）、
以及 `_axis.get(null)` 类空引用 → 拆解三态（CLOSED→OPENED→EXPLODED）无响应。

## 根因

`explode_controller.gd` 的 `_guess_axis` 未防御两类非法输入：

1. meta 装配体条目缺 `transform` 键：`entry.get("transform")` 返回 null，
   旧代码 `null.get("translation", ...)` 直接崩溃；
2. `transform` 为 null/非字典时旧三元表达式本身也有 Variant 推断警告（警告即错误）；
3. 装配体 `parent` 键为空串或指向不存在的装配体时，`nodes[parent_id]` 取到 null，
   后续 `_axis.get(null, ...)` 崩溃。

## 修复（提交 92b1b0d）

```gdscript
var tr: Variant = entry.get("transform")
var t: Array = tr.get("translation", [0, 0, 0]) if tr is Dictionary else []
...
var parent_id: String = str(entry.get("parent", ""))
if parent_id == "" or not nodes.has(parent_id):
    return _axis.get(nodes[aid], Vector3.RIGHT)
return _axis.get(nodes[parent_id], Vector3.RIGHT)
```

先取值后判型、父级缺失回退到自身轴，两种崩溃路径均封死。

## 复盘

- 内容包（meta/gltf/annotations 属 03/05 线）字段缺失不应让引擎崩溃——引擎侧
  对内容输入一律按"可降级"处理（本项目降级表原则），此处守卫即该原则的落地。
- `nodes[aid]` 自身键缺失的守卫在调用方（explode 只在选中有效设备时进入）已保证，
  暂不冗余加防。