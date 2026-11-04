# TASK-77B 完成报告（02 线 2/2）：目录↔内容包引用一致性校验器

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-77B（02 线 2/2）：catalog_ref_check.py |
| 前置 | TASK-72-A（重复 id 根治） |
| 状态 | 完成 |

## 一、交付物

`tools/validate/catalog_ref_check.py`（219 行，纯 stdlib）：扫 03/05 两仓 catalog + 内容包目录 + id_registry
台账，报四类问题，输出统一 `FAIL n` 计数行（供 verify_all 解析）。

## 二、四类问题实跑（现状）

```
内容包 22 个，目录条目 1987 行
REF-01 悬空包引用：0 条
REF-02 反链缺失：3 个
REF-03 台账漂移：registry 50 条 / 目录使用 0 条（未使用 50 条）
REF-04 关联包形态非法：0 条
FAIL 3
```

| 规则 | 数字 | 样例 | 处置 |
|---|---|---|---|
| REF-01 悬空包引用 | 0 | — | 无 |
| REF-02 反链缺失 | 3 | game-boy / neo-geo-mvs / sfc | 新完工包未回填目录 device_id，反馈 03/05 线补 |
| REF-03 台账漂移 | 50 未使用 | C-GEN-000001~050 | 57-B allocate 模拟的 50 条，非真实分配，可清空 |
| REF-04 形态非法 | 0 | — | 无 |

## 三、说明

- REF-02 的 3 个反链缺失（game-boy/neo-geo-mvs/sfc）是新完工包尚未在目录条目标注 device_id，属"修复类
  问题只报告不改他线文件"，已列反馈。
- REF-03 的 50 条台账漂移是 57-B allocate 的模拟记录（非真实分配），当前 registry.jsonl 可清空重来。
- 工具输出 `FAIL 3` 行，与 01 线 verify_all 的"解析末行 FAIL 计数"口径一致，可由 01 线挂入 catalog 步。

## 四、TASK-77 两份总收尾

- **77-A**：`规范增补_v0.6.2.md`（单一真相源 + 错误码注册 + 门禁产物 + 兼容说明）+ registry 补 module/backend_status 列。
- **77-B**：`catalog_ref_check.py`（REF-01~04）+ 实跑 FAIL 3（3 反链缺失 + 台账漂移 50）。

## 五、开放问题

1. 反链缺失 3 包（game-boy/neo-geo-mvs/sfc）回填 device_id 的排期；
2. registry.jsonl 的 50 条模拟记录是否清空；
3. 工具挂入 verify_all.catalog_step 的时机（待 01 线 76-A 折叠落地后协商）。
