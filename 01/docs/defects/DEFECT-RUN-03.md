# DEFECT-RUN-03（实机首验缺陷 · closed）

> 状态：**closed（2026-11-05 修复提交 dd67bfb）** · 修复已入 main
> 复现环境：Godot 4.4 · 用户实机按 F5 · 项目"警告即错误"开启
> 档案补登：本档案由 06 线 debug 专员按 git 提交记录补登（原档欠登）；现象为按修复 diff 与项目已知前科反推，用户原始报屏未存留。

## 现象

Godot 输出面板报 exhibit_host.gd 解析错误：类型标注 `DeviceLoader` 无法解析
（未注册的类名）→ 脚本整张未加载 → exhibit_host 不实例化设备 → 空厅/占位盒不出现。

## 根因

exhibit_host.gd L112 有类型标注：

```gdscript
var loader: DeviceLoader = DEVICE_LOADER.new()
```

但 device_loader.gd 从未声明 `class_name DeviceLoader`，类型名在解析期查无此表
→ warning-as-error 顶格为错误，连带 exhibit_host 整脚本失败。

## 修复

device_loader.gd 头部补声明（提交 dd67bfb）：

```gdscript
class_name DeviceLoader
extends Node3D
```

## 复盘

- **涉及 class_name 新增**：按血泪坑清单第 2 条，必须让用户删除
  `01\godot\.godot\` 缓存目录后再开引擎，否则 Godot 可能沿用旧类表继续报错。
- 教训：凡在脚本间用类型标注引用另一个脚本，被引用脚本必须显式 `class_name`，
  且 gd 侧静态检查（gd_symbol_check）后续宜增加"类型标注引用未注册类名"规则（先查池再升级）。