# id_registry 重建再生成方案（registry.jsonl rebuild）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-162-A（02 线）。对象：`docs/catalog/registry.jsonl` + `tools/index/id_registry.py`。

## 一、起因

1. `registry.jsonl` 因 82-B「清空 50 条模拟记录」后为 **0 字节**（TASK-123 审计确认"台账 0 条为真实状态"）。
2. 空台账下 `allocate` 的续号只扫台账，会从 `000001` 重发，与目录**既有已用 id 撞号**。
3. 故需：① `rebuild` 子命令从目录已用合法 id 重建台账；② `allocate` 续号纳入目录已用 id。

## 二、重建口径

- **来源**：03/05 目录文件（`.jsonl`）中**真实存在**的 id；同 id 首次出现为准（`scan_catalog_ids` 按 id
  去重，`source_file` 取首个 `文件:行`）。
- **合法性**：仅 `^[CGMPAEX]-[A-Z]{2,4}-\d{6}$` 匹配的 id 回填；非法/无前缀 id **跳过并计数**，不臆造。
- **字段**：`{id, name:"", category:大类码对应大分类, batch:重建当日, source_file:文件:行}`。
- **批次**：`batch` = 重建当日（`YYYY-MM-DD`）。

## 三、幂等与续号

- **幂等**：`rebuild` 只追加台账中不存在的 id；重复执行「已存在跳过」，不增重、不丢既有行。
- **allocate 续号决策**（取一，写定）：**「续号纳入目录已用 id」**——`allocate` 的续号起点 =
  max（台账 ∪ 目录已用 id）中同前缀的最大序号。即：即使不先 rebuild，只要 `allocate` 传 `--files`
  指向目录文件，也不会与目录既有 id 撞号；若已 rebuild，台账已含目录 id，续号同样正确。

## 四、与 REF-03 衔接

- 重建后 `registry_count` 应 = 目录已用合法 id 数；`allocated_unused` 归 0；`catalog_ref_check` 的
  REF-03 漂移 = 0（registry 分配 id 数 == 目录实际使用数）。

## 五、交接说明

- 03/05 新增条目仍走 `allocate` 预留（不手编 id）；重建的台账**只读回填**，不改目录文件、不重编号
  任何既有 id（22 台已量产包 0 影响）。
- 目录文件易变（执行期间 `通讯与移动大类` v2→v3、05 删 v1、新增 `电子宠物类_增补`），故 rebuild
  每次须以**当时实际存在的文件**为输入；台账以最近一次 rebuild 为准。

## 六、可执行命令（对齐真实日志）

```bash
# 重建前：台账 0 条
python tools/index/id_registry.py --report --files <03/05 全部目录 jsonl>
# 重建（幂等）
python tools/index/id_registry.py rebuild <03/05 全部目录 jsonl>
# 重建后：台账 M 条；REF-03 漂移 0
python tools/index/id_registry.py --report --files <同上>
python tools/validate/catalog_ref_check.py
```

实跑（2026-11-06）：`rebuild` 扫描 1582 个 id → 回填 1582 条 / 非法跳过 0；幂等复跑「回填 0、已存在跳过
1582」；REF-03 漂移 0（registry 1582 = 目录使用 1582）。
