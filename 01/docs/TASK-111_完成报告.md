# TASK-111 完成报告（图鉴数据联调与排序）

## 交付物
- `encyclopedia_panel.gd`：中分类按 meta.json `shards` 顺序稳定展示（不另排序）；条目按 name 字典序（不区分大小写）、同名按 era（兼容 year）升序，排序开关「排序:开/关」可关闭回退源码顺序；空分片提示、非法行计数并置底（`（非法行）`），全程不崩溃；`_shown_rows` 与列表序号对齐防详情错位。
- `catalog_data.gd`：新增静态辅助 `sort_shard_rows()`（合法行排序、非法行沉底）；既有契约方法名 `load_shard/search/get_summary` 等一律未动。

## 验收证据
- `verify_all.py --daily`：**结果：37/37 通过**（任务书预期 34/34——03 线新增 iphone/next/palm-pilot 三包，30 完工包 + 7 步；其中 catalog 步 `verify：28 片 / 1484 行，通过`（FAIL 0）、catalog_ref FAIL 0、gd_naming FAIL 0）
- `catalog_ingest.py --from-work --stats`：`文件 7；行 2007；唯一 id 2007；大分类 5；中分类 30；错误 0`（--from-work 口径含工作源增量；引擎 bundle 权威口径 1484 条 / 28 中分类，见 catalog 步与 catalog_panel_check）
- 实机截图：静态交付，待用户/debug 线按其侧 F5 核对（打开顺序 = meta.json shards 顺序；个人机分片 ENIAC 换序效果明显）。

## 结论与备注
数据联调通路已证明（1484/28 全对账）；排序为可关默认开。from-work 统计（2007 行/30 中分类）与引擎 bundle（1987 行/28 中分类）存在口径差，属工作源增量未摄取，建议统筹下轮核对 03/05 线源与 bundle 同步策略。