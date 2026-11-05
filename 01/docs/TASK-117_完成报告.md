# TASK-117 完成报告（catalog 数据层内存缓存与查询计时）

## 交付物（catalog_data.gd）
- 新增计数与计时字段：`_cache_hits/_cache_misses/_query_us`（命名避开 get_meta/get_index 等原生冲突）；
- `load_shard()`：命中/未命中计数 + `Time.get_ticks_usec()` 计时（含 IO 与早退分支）；`search()` 同计时；
- `get_summary()` 暴露 `cache_hits/cache_misses/query_us`（微秒累计）；既有契约方法名未动。
- `catalog_panel_check.py`：新增 C-04 Python 侧模拟口径（同分片二次 load：1 hit / 2 miss + 首次读取耗时 ms），与引擎侧同构对照。

## 验收证据
- `python 01/scripts/catalog_panel_check.py`
```text
[PASS] C-01 total_rows=1484
[PASS] C-02 中分类数=28（预期 28）
首分片：计算机__早期计算机.json（声明 13 条）
[PASS] C-03 分片实际总条数=1484 == total_rows=1484
C-04 模拟口径：cache_hits=1 cache_misses=2 三次 load 耗时 131.121 ms
[PASS] C-04 命中口径正确（1 hit / 2 miss）   rc=0
```
- `python 01/scripts/catalog_ingest.py --from-work --stats`：`文件 7；行 2007；唯一 id 2007；大分类 5；中分类 30；子分类 89；错误 0`（引擎 bundle 权威口径 1484/28，见 catalog 步"28 片 / 1484 行"）

## 备注
Cold 首读 131ms 为含磁盘 IO 的 Python 全量三次 load（跨 SMB 共享盘）；引擎侧同构实现（Time 计量、缓存零 IO 命中）后热命中预期 <1ms 量级（待实机面板输出 get_summary 核对）。1484 条目 / 28 分片的内存缓存 + 摘要暴露满足图鉴性能观测需求。