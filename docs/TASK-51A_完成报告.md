# TASK-51A 完成报告（docs/TASK-51A_完成报告.md）

> 01 线 · 2026-11-04 · 任务：设备目录摄取工具与万级规模验证。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/catalog_ingest.py` | 260 | JSONL/CSV 摄取（utf-8-sig 宽容）→ id/名称别名索引 + 三级分类树；`--stats/--find/--list/--shard/--gate`；去重/路径三级校验；分片存盘（每中分类一片 + manifest） |
| `scripts/scale_bench.py` | 110 | 1k/5k/10k 合成基准（tracemalloc 峰值） |
| `scripts/verify_all.py`（改） | — | 新增 `catalog` 门禁步（无文件 SKIP rc=0；有错 FAIL rc=1），daily/full 均含 |

## 2. 运行日志（原文关键段）

```text
$ python scripts/scale_bench.py --sizes 1000,5000,10000
规模    摄取(s)   路径查询(ms)  关键词(ms)  路径命中  关键词命中  峰值(MB)
1000    0.051    0.02         0.03       84        1          1.2
5000    0.233    0.03         0.06       417       1          5.9
10000   0.489    0.01         0.01       834       1          11.9
结论（10000 条）：摄取 0.489s / 路径查询 0.01 ms / 关键词 0.01 ms / 峰值 11.9 MB

$ python scripts/catalog_ingest.py --jsonl <3行含重复id> --stats --shard
文件 1；行 3；唯一 id 2；大分类 2；中分类 2；子分类 2；错误 1
  [FAIL] 重复 id: T-000001（… 行 3）
$ … --gate   → rc=1（有错拦截）
$ python scripts/catalog_ingest.py --from-work --gate
[SKIP] 未发现目录文件（03/05 线尚未产出，正常）   → rc=0（SKIP 语义）
```

## 3. 规模证明结论

**万级可行**：10,000 条摄取 <0.5s、查询微秒级、峰值内存 11.9MB——按线性外推 10 万条约 5s/120MB，
仍有 10 倍余量；分片索引（每中分类一片）保证图鉴端按需读取。瓶颈在半结构化字段（长理由文本）
而非索引量——若未来理由文本普遍超长，压缩键存即可（预案写入报告留档）。

## 4. 迭代记录（2 轮）

1. 轮 1：list_path 初版含死代码块 → 收敛为三级直达/两级汇总/一级汇总三分支；
2. 轮 2：CSV 源的 path/aliases 需要分列解析 → 增加分号/斜杠拆分与类型归一（line 级宽容 + 错误行级报告）。

## 5. 开放问题

- schema 以 02 线 v0.6 定稿为准（当前按任务 52-A 草案实现，字段已对齐）；
- `--from-work` 目前只扫 03/05 线 docs/catalog；新线（如 06 手机线）需在 CATALOG_ROOTS 注册；
- 分片写入目录 catalog_index/ 需列入 .gitignore 级别的同步忽略建议（转 02 协作契约）。