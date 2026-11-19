# TASK-194-B 完成报告（04 线 · design 73 拆解体验深化规格）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。完成日期：2026-11-14。

## 1. 交付物清单

`73_拆解体验深化规格.md`（四块齐）：
- 拆解层级：L0→L1 部件（assemblies 6 件基线）→L2 子件（R-090↔MESHES.md）→L3 role ≤3；无 assemblies 显「待产」。
- 交互：九行表（点选进入/开盖≥60%/爆炸 v×depth×0.16 [需实机核对]/子树/滑杆 0~1 步进 0.05/勾选脱离/复原 Esc/状态保持）+ L1-only 替代（44 号 B2）。
- 视觉：四形态差异表（机柜竖排/小型机横排/游戏机俯视/手持薄层）+ 共性五条。
- 验收：五判据+58 号 T-555~T-566 衔接。

## 2. 验收命令原始日志与退出码

```
CMD1 (Get-Content .\docs\design\73_拆解体验深化规格.md -Raw).Length = 3276；去空白 2713（≥2500）  exit:0
CMD2 Select-String -Pattern "拆解层级","交互","视觉","验收" → 命中 11 行                exit:0
CMD3 py -3.7 D:\work\01\repo\01\scripts\verify_all.py --daily --cache
     结果：41/41 通过（hp-2100/data-general-nova 包各 84 条 PASS）                     exit:0
```

## 3. 漂移（如实记录）

- 既有占位实现：explode_controller.gd/explode_panel.gd；装配体 = hp-2100 与 nova 各 6 件——层级映射以此为基线。
- 四块结论：全部成文；L1-only 替代不改层级表。
- 漂移 1 处：爆炸系数 0.16 为本规格建议值（32 号原公式 0.12），已标 [需实机核对]。
- 红线执行：纯文档零联网零二进制；不写代码；不改装配体、不代 02 线改契约；无 git/PAT 条款。