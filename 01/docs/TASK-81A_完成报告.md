# TASK-81A 完成报告（docs/TASK-81A_完成报告.md）

> 01 线 · 2026-11-04/05 · 任务：catalog_ref_check 挂入门禁（目录↔内容包反链正式入闸）。

## 1. 交付物

| 文件 | 改动 |
|---|---|
| `scripts/verify_all.py` | 新增 catalog_ref 步（调 02 线 catalog_ref_check.py），入 `--daily` 与全量；run_step 对 catalog_ref 用 `FAIL n` 末行口径判定；新增 `--no-ref-hard` 告警降级开关；抽取 `apply_ref_downgrade()` 可单测 |
| `docs/verify_last.json` | 实跑刷新（29/30，含拦截明细） |

## 2. 三段实跑日志（原文摘录）

```text
① 挂载首跑（REF 已修复态）：
   == [catalog_ref] … REF-01 0 / REF-02 0 / REF-03 registry 50（未使用 50，不计 FAIL）/ REF-04 0
   FAIL 0
   ===== 验收汇总（29 项） =====   结果：29/29 通过  → rc=0

② 03 线 pet2001 入闸后（本轮中）：
   == [catalog_ref]
     [REF-02] 完工包 pet2001 无目录反链
   FAIL 1
   ===== 验收汇总（30 项） =====   catalog_ref FAIL  → 29/30，rc=1
   （门禁第一次真实拦截：PET 2001 包三件套已过闸但目录反链未随包回填——83-A 任务书的验收义务）

③ 降级开关单测（替 82-B/85-A 未修复场景备好）：
   apply_ref_downgrade([('catalog_ref', False, 'FAIL 3'), ('m0', True, 'ok')], True)
   → [('catalog_ref', True, 'FAIL 3〔--no-ref-hard 告警降级〕'), ('m0', True, 'ok')] ✔
```

## 3. 迭代记录

- 轮 1：catalog_ref 步初版在汇总循环里 `results.append(run_step(...))` 造成三元组拆包
  ValueError（run_step 返回二元）→ 改为 `ok, note = run_step(...)` 后修复，回归 29 项全绿。

## 4. 当前状态与开放问题

- **门禁现状**：硬红 29/30——原因 pet2001 反链未回填（03 线 83-A 收尾项）；03 回填后即自动转绿，
  无需改 01 代码。轮末若仍未修复，可 `--daily --cache --no-ref-hard` 临时降级（报告注明原因）。
- REF-03 台账漂移（registry 50 条模拟记录）不计入 FAIL——待 02 线 82-B 清空后数字归零。