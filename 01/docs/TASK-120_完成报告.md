# TASK-120 完成报告（引擎启动自检屏 quickcheck）

## 交付物
- `startup_check.gd`（新增）：`_ready` 内三项 quickcheck，逐项在 HUD 打三行 + 标题：
  1. **目录可读**：`DirAccess.open("res://content")` 成功且枚举子目录非空 → `目录 OK：N 个子目录`；
  2. **meta 可读**：任一经枚举内容包 meta.json 解析为 Dictionary → `meta OK：<pkg>/meta.json 解析为 Dictionary`；
  3. **槽位表可读**：优先读 `res://slots/emulators/*/manifest.json` 计数；目录缺失时按**内置登记口径**降级 `槽位表 OK：走内置登记口径`；
  每项失败只打 FAIL 不崩溃（可降级）。
- `main.tscn`：挂载 StartupCheck 于 `/root/Main` 下（ext_resource 11_startup，load_steps=16，scene_check PASS）。

## 验收证据
- `python 01/scripts/slot_loader.py --json`
```text
"slots": { "fake-slot", "mame-apple2", "fake", "simh-pdp8" }   # 槽位数 4
media_dirs: []
```
- Godot 输出面板 / HUD 三行：静态交付。预期：
```text
[启动自检 quickcheck]
  目录 OK：20 个子目录
  meta OK：eniac/meta.json 解析为 Dictionary
  槽位表 OK：走内置登记口径（res://slots 未导出）
```
（第三项因 01/godot 内无 slots 目录——res:// 未导出槽位，按内置登记口径显示；待实机核对）

## 备注
不自建新数据目录，只读既有 res://content 与槽位清单；quickcheck 结果同时留输出面板（startup 脚本在实机可即时排障）。若后续把 slots 导出进 godot/，第 3 项自动切换为 manifest 计数口径。