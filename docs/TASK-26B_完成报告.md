# TASK-26B 完成报告（docs/TASK-26B_完成报告.md）

> 01 线 · 2026-11-02 · 任务：主场景接线（静态）+ Godot 实机首验包（见 任务26-B）。
> 本报告含 TASK-26 两份总收尾，01 线本轮（任务 26-A/B）完成。

## 1. 交付物

| 文件 | 规模 | 说明 |
|---|---|---|
| `godot/scenes/main.tscn` | 96 行 | 接线：新增 `ExhibitHost`（layout_file=exhibit_dawn.json、max_running=1、audience_radius=2.2、auto_spawn）；保留 DirectLoader/Inspect/Explode/HUD 原有链路 |
| `scripts/scene_check.py` | 108 | tscn 文本级校验（S-01~S-06），实跑全绿 |
| `docs/godot_first_boot.md` | ≥1200 字 | 安装→首验 6 步→核对表 6 项→异常对照 6 条→解锁下一步 |

## 2. 运行日志（原文关键段）

```text
$ python scripts/scene_check.py
  [PASS] S-01 load_steps=13（ext 8 + sub 4 + 1 = 13）
  [PASS] S-02 1_gw..8_host 全部 8 个脚本路径存在
  [INFO] S-06 DeviceLoader 与 ExhibitHost 并存（设计有意：单机直连 + 展厅模式）
  [PASS] 总检：main.tscn 静态校验通过（ext 8 / sub 4）   → rc=0
```

## 3. 主场景结构（ASCII 节点树）

```
Main (Node3D)
├─ Room：Floor + 4 Walls + Screen(quad) + Light + Camera(player.gd)
├─ GatewayClient (gateway_client.gd)
├─ ExhibitHost (exhibit_host.gd)          ← 本任务新增：布局加载 4 台设备
├─ DeviceRoot (device_loader.gd)          ← 单机直连模式保留
│   ├─ InspectController / ExplodeController
└─ HUD (CanvasLayer)
    ├─ DevicePicker / ExplodePanel
```

## 4. tscn 语法自查表（逐项打勾）

| # | 项 | 结果 |
|---|---|---|
| 1 | `[gd_scene load_steps=N format=3]` 计数正确 | ✓ S-01 |
| 2 | 8 个 ext_resource 路径均存在 | ✓ S-02 |
| 3 | 节点 script= 引用全部声明 | ✓ S-03 |
| 4 | SubResource 引用全部声明（plane/盒墙×2/quad） | ✓ S-04 |
| 5 | ExhibitHost 导出的 property 名与 exhibit_host.gd 一致（layout_file/max_running/audience_radius/auto_spawn） | ✓ 逐名核对 |
| 6 | 布局文件存在且经 layout_check 正例实测 | ✓ |

## 5. 迭代记录（2 轮）

1. 轮 1：load_steps 沿用旧值 10 → 新增 1 个 ext_resource 后应改为 13（8+4+1），scene_check 捕获；
2. 轮 2：ExhibitHost 与 DeviceRoot 并存会造成"双击设备"担忧 → 明确为设计有意（两种模式都保留），scene_check 以 INFO 提示而非报错，first_boot 文档写明分工。

## 6. 待实机项与说明

- 全部"预期现象"仍为静态推导：first_boot.md 中每行核对框未打勾——**不虚报实机**；
- 若你装好 Godot 跑 first_boot 出现任何一项失败：把输出面板红色报错发回（附第几步），即成为下一轮 26→27 之间的修复输入。

## 7. TASK-26 两份总收尾 + 01 线本轮完成标注

- 26-A：键码映射 57 键全量 + gen_keymap 生成器 + mame_apple2 翻译层接线；m2a fake 回归 10/10 全绿；
- 26-B：main.tscn 静态接线 + scene_check + first_boot 首验包（等待你装 Godot）；
- 基线：`verify_all --daily` 9/9（收尾回归见下轮输出）。
- 01 线本轮（任务 26）完成。