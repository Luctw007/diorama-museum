# TASK-217-A 完成报告

> 任务：id_registry source_file 回填修复（C-PC-000208，消除 CC-02 误报）。执行账号：02 线。只改 02 目录。

## 一、交付物清单

1. 回填 `docs/catalog/registry.jsonl` 中 `C-PC-000208` 条目的 `source_file`：`null → "计算机大类_目录_v2.jsonl:505"`。
2. 消除 `catalog_check` CC-02 对 C-PC-000208 的台账冲突误报。

## 二、验收日志（原始输出 + 退出码）

### 2.1 source_file 回填前后 diff

```
回填前（第 1583 行）：
  {"id": "C-PC-000208", "name": "", "category": "计算机", "batch": "2026-11-15", "source_file": null}

回填后（第 1583 行）：
  {"id": "C-PC-000208", "name": "", "category": "计算机", "batch": "2026-11-15", "source_file": "计算机大类_目录_v2.jsonl:505"}
```

### 2.2 CC-02 复测（单文件，回填前 FAIL 1 → 回填后 FAIL 0）

```
回填前：
  计算机大类_目录_v2.jsonl:505  id='C-PC-000208'
    CC-02  id 'C-PC-000208' 与 id_registry 台账冲突（已分配于 2026-11-15）
  CC-02  FAIL 1 / PASS 504

回填后：
  目录校验（文件 1 个，条目 505 行，唯一 id 505，FAIL 0）
  CC-02  FAIL 0 / PASS 505
```

### 2.3 CC-02 全量复测（5 文件，跨文件重复仍 0）

```
目录校验（文件 5 个，条目 1583 行，唯一 id 1583，FAIL 0）
CC-02  FAIL 0 / PASS 1583
```

### 2.4 门禁只读复测

```
verify_all --daily --cache
  catalog_ref          FAIL  FAIL 1
结果：40/41 通过（rc=1）
```

## 三、与任务书的漂移

1. **source_file 格式**：任务书写「应指路径」，实际台账 `source_file` 格式为 `文件名:行号`（如
   `计算机大类_目录_v2.jsonl:505`，与 rebuild 命令写入格式一致，见 id_registry.py `scan_catalog_ids`），
   已按台账既有格式回填。
2. **门禁非 41/41 而是 40/41**：`catalog_ref` 步骤 FAIL 1 = 「完工包 hp-2100 无目录反链」，根因是
   monorepo 镜像 `01/repo/03/docs/catalog/` 中 hp-2100 条目仍为 `planned/device_id=null`（镜像目录 stale，
   未同步共享盘 hp-2100 的反链 done），**与本任务 source_file 回填无关**——本任务只改共享盘
   `02/repo/docs/catalog/registry.jsonl`，不进镜像门禁。

## 四、红线自查

零联网、零下载（纯登记回填）；source_file 以 Apple IIe 条目实际落盘位置（`计算机大类_目录_v2.jsonl:505`）
为准，未臆造；未改 03 线目录文件、未改校验器代码逻辑（仅回填台账一行）。
