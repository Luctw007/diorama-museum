# DEFECT-RUN-07（实机首验缺陷 · 修复待用户确认）

> 状态：**修复完成 · 待用户重测确认**（2026-11-05 修复提交 d85e0f9）· 用户确认后置 closed
> 复现环境：Godot 4.4 · 用户实机按 F5 · 项目"警告即错误"开启
> 档案补登：本档案由 06 线 debug 专员按 git 提交记录补登（原档欠登）；现象为按修复 diff 与项目已知前科反推，用户原始报屏未存留。

## 现象（表现错误 · 无报错但不对）

点选设备后**无任何视觉反馈**：白模不高亮、也无选中标签。
用户实际点击命中（拾取逻辑正常），但看不到"选中了"，交互观感等于"点了没反应"。

## 根因

1. **白模高亮永不生效**：`_set_selected` 原代码仅在
   `mi.material_override is StandardMaterial3D` 时才点亮；白模占位网格
   **没有材质**（material_override == null），条件恒假 → 高亮代码成死路；
2. **选中 HUD 标签从未创建**：`_hud_label` 依赖外部调用 `set_hud_label`，
   但全工程无人调用 → `_hud_label` 恒为 null，标签分支永不执行。

## 修复（提交 d85e0f9）

```gdscript
if mi != null:
    var mat := mi.material_override as StandardMaterial3D
    if mat == null:   # 白模无材质 → 现建 override，保证高亮可见
        mat = StandardMaterial3D.new()
        mi.material_override = mat
    mat.emission_enabled = true
    mat.emission = Color(1.0, 0.6, 0.1)
    mat.emission_energy_multiplier = 0.6
```

```gdscript
# _ready 尾部：选中 HUD 自建标签挂 HUD（与 gateway_client 同模式）
var hud := get_node_or_null("/root/Main/HUD") as CanvasLayer
if hud != null and _hud_label == null:
    _hud_label = Label.new()
    _hud_label.position = Vector2(16, 40)
    _hud_label.add_theme_font_size_override("font_size", 16)
    hud.add_child(_hud_label)
```

## 待确认项（用户重测四步话术）

> 请完全退出 Godot → 重开工程 → 有提示选 Reload → 按 F5，把结果（截图或文字）发我。

- 点选白模设备 → 应出现橙黄高亮 + 左上角 `[选中]` 标签（含 role 文案或"（无 role 标注）"）；
- 点选有材质设备 → 高亮叠加在材质之上，标签正常。

## 复盘

- "高亮不出现先查 material_override 是否为 null，现建 StandardMaterial3D"已固化为
  血泪坑清单第 5 条。
- 依赖外部注入的 UI 引用（set_hud_label 无人调用）属典型"接线遗漏"——宁可自建
  也要保证默认可用（自建 + 外部注入双通道，与 gateway_client 同模式）。