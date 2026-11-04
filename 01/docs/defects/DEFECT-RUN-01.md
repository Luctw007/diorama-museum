# DEFECT-RUN-01（实机首验缺陷 · closed）

> 状态：**closed（2026-11-06 统筹应急修复）** · 修复提交随下一收口推送
> 复现环境：Godot 4.4 · 用户首次实机按 F5 · 主展厅仅四面墙

## 现象

Godot 输出面板（脚本 device_loader.gd 加载失败）：
- L242 `get_index()` 与 Node.get_index(bool) 签名冲突；
- L254 `get_meta()` 与 Object.get_meta(StringName, Variant) 签名冲突；
- L88 / L110 两处 `:=` 从 Variant 推断类型（项目把警告当错误）。
→ 脚本整张未加载 → exhibit_host 实例化设备失败 → 空厅。

## 修复

1. 重命名 get_index→get_device_index、get_meta→get_device_meta（含 device_picker.gd
   两处调用与 has_method 字面量、exhibit_host.gd 注释）；
2. L88 `var top: Dictionary`、L110 `var meta: Variant` 显式类型化。

## 复盘（给 01 新账号复查项）

- 其余 10 个 gd 是否还有同类 Object/Node 方法名冲突或 `:=` Variant 推断警告？
  实机按 F5 后逐脚本观察输出面板，发现一个修一个（保持"警告即错误"不变）；
- gd_symbol_check 应增加两条规则：方法名不得与 Node/Object 原生方法重名、
  不得裸 `:=` 推断 Variant（先查池再升级）。