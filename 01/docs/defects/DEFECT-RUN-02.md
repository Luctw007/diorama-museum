# DEFECT-RUN-02（实机首验缺陷 · closed）

> 状态：**closed（2026-11-05 修复提交 ba72577）** · 修复已入 main
> 复现环境：Godot 4.4 · 用户实机按 F5 · 项目"警告即错误"开启
> 档案补登：本档案由 06 线 debug 专员按 git 提交记录补登（原档欠登）；现象为按修复 diff 与项目已知前科反推，用户原始报屏未存留。

## 现象

Godot 输出面板报 inspect_controller.gd 解析错误：L149 `:=` 三元从 Variant 推断类型
（项目把警告当错误）→ 脚本整张未加载 → 点选/悬停系统整体无响应。

## 根因

L149（修复前）：

```gdscript
var role := device_loader_hint.get_node_role(_selected) if device_loader_hint != null else ""
```

`device_loader_hint` 声明为弱类型 `Node`，`get_node_role()` 是动态调用、返回 Variant，
三元两分支无法收敛为具体类型 → 推断 Variant → warning-as-error 顶格为错误。

## 修复

显式类型标注（提交 ba72577）：

```gdscript
var role: String = device_loader_hint.get_node_role(_selected) if device_loader_hint != null else ""
```

## 复盘

- 同一实机首验轮次内，其余脚本仍存在同类 `:=` Variant 三元推断（RUN-01 已修两处）；
  后续 RUN-03~06 即为此类问题的逐个暴露，登记链完整。
- gd_symbol_check / 门禁无法在引擎外捕获此类解析错误（需 Godot 实机或 GDScript 解析器升级），
  实机按 F5 逐脚本观察输出面板仍是最终防线。