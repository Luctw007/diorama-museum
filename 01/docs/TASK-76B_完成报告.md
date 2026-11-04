# TASK-76B 完成报告（docs/TASK-76B_完成报告.md）

> 01 线 · 2026-11-04 · 任务：验收趋势历史（verify_history.jsonl 双写 + 面板最近 5 轮与连续全绿）。

## 1. 交付物

| 文件 | 改动 |
|---|---|
| `scripts/verify_all.py` | --cache 时双写：verify_last.json 之外，追加一行 {time,total,passed} 到 docs/verify_history.jsonl；写入失败只打印警告、不影响退出码 |
| `scripts/project_stats.py` | gather 读取历史清单；render_verify 增加"最近 ≤5 轮"小表与"连续全绿 N 轮"；历史为空显示"趋势历史：不足" |
| `docs/verify_history.jsonl` | 实跑生成（本轮 2 行） |

## 2. 验收日志（原文）

```text
$ python scripts/verify_all.py --only m0 --cache
结果：1/1 通过 / 验收缓存已写 docs/verify_last.json

$ python scripts/verify_all.py --daily --cache
结果：27/27 通过 / 验收缓存已写 docs/verify_last.json

$ Get-Content docs/verify_history.jsonl
{"time": "2026-11-04 23:01:59", "total": 1, "passed": 1}
{"time": "2026-11-04 23:02:05", "total": 27, "passed": 27}

$ python scripts/project_stats.py（"最近验收"节）
- 最近验收（2026-11-04 23:02:05）：**27/27 通过** — 【全绿】
  - 最近 2 轮：
  - 2026-11-04 23:01:59：1/1 全绿
  - 2026-11-04 23:02:05：27/27 全绿
  - 连续全绿：**2 轮**
```

趋势行与两份缓存一致（最后一次 verify_last=27/27；history 两行字段可解析）✔。

## 3. 已知语义（沿用 71-A 开放问题口径）

- `--cache` 与 `--only` 联用会把"最近验收"节暂时替换成子集结果（1/1），
  最后以 full/daily 一次收尾即可恢复正常显示——以上演示即按此顺序执行；
- 历史行按追加序 = 时间序，连续全绿从最新向前计数。

## 4. 开放问题

- streak 目前对"total=0 的异常行"跳过续算，避免误记；如需"红灯行打断 streak"展示更直观
  的断点标注（如红色高亮中断位置），可下一步做；
- 今后可以考虑把 verify_history 纳入 04 线仪表盘取数（--json 已带出该字段）。