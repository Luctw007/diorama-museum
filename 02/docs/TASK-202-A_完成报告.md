# TASK-202-A 完成报告：Apple IIe 目录 id allocate 正式分配

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 交付物清单

1. **Apple IIe id 已分配**：`id_registry allocate C 1 PC` → **`C-PC-000208`**，写入 registry.jsonl（1582→1583 条）。
2. **待办销账**：`1x待办清单_v1.md` §六 Apple IIe 条目更新为「id 已分配：C-PC-000208」+ 回填指引。

## 验收日志（原文 + 退出码）

```
# 1) allocate 执行日志
[allocate] 分配 1 个 C-PC-* id（起点 208，批次 2026-11-15）
  C-PC-000208
[allocate] registry.jsonl 现有 1583 条记录   （rc=0）

# 2) 待办销账自证（1x待办清单 §六 更新后）
| Apple IIe（第二批第 8 台） | **C-PC-000208（已分配，TASK-202-A）** | 产包时由 05 线回填目录条目 | 02 线已分配 / 05 线回填 |

# 3) 门禁只读复测（verify_all --daily --cache）
结果：41/41 通过   （rc=0）
```

## 与任务书的漂移（如实）

1. **新 id = C-PC-000208**：allocate 起点 208，与既有 C-PC-000001~000207（Apple I/II/II Plus/IIc/III/
   Lisa/IIGS 及第二批 Altair/Amiga 等）连续、无冲突（工具自动续号，非人为指定）。
2. **Apple IIe 目录条目本不存在**：计算机大类 v2 目录里 Apple 系只有 Apple I/II/II Plus/IIc/III/Lisa/
   IIGS，**无 Apple IIe** 条目——本次 allocate 是为尚未产目录条目的 Apple IIe 预分配 id，回填由 05 线
   产包时新建条目（不是改既有 Apple II 条目）。
3. **回填责任线**：Apple IIe 内容包归 05 线（173-A 名单标"05 线管辖"），故回填指引责任写 05 线。

## 红线自查

1. 不下载 ROM/二进制 ✓；2. 不臆造 id ✓（C-PC-000208 由工具自动续号，与既有无冲突）；3. 只改 02 目录 ✓
（未改 03 目录 jsonl，只登记 + 指引）；4. allocate 有日志、销账有原文 ✓；5. 无 git/代理/PAT ✓。
