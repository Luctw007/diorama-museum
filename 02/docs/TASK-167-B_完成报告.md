# TASK-167-B 完成报告（02 线）

## 一、交付物

1. 5 工具接入 `DCM_MONO`：`catalog_check.py` / `taxonomy_check.py` / `media_infer.py` / `collect_index.py` / `regress_all.py`；
2. `规范增补_v0.6.2.md`：§六标题「反链义务（CC-10 语义）」→「反链义务（REF-02）」+ 编号说明改写；§七补记 167B 统一；附录开放问题 4/5 标记已收口；
3. `docs/编号与路径_封版收口_v1.md`：DCM_MONO 统一范围、CC-09 空缺裁决（reserved，后续从 CC-11 起编）、变更登记。

## 二、验收日志（贴证）

```
默认上下文（无 DCM_MONO）：
  catalog_check 5 文件 1582 条 FAIL 0 · taxonomy_check 1582 条孤路径 0 · media_infer 1582 条
DCM_MONO 注入（临时镜像 3 条）：
  taxonomy_check：对账 3 条 → 正确定位镜像内数据（不再读共享盘 1582 条）
run_tests.py：PASS 21，FAIL 0
```

## 三、门禁回归：36/37（非本任务回归）

`verify_all --daily --cache` 现为 **36/37**（非 37/37）。失败项为 catalog 步「重复 id 306 条」——
根因是 monorepo 镜像 `01/repo/03/docs/catalog/` 同时存在 `通讯与移动_v2.jsonl`(306) 与 `_v3.jsonl`(306)
（`sync_monorepo.py` 用 robocopy /E 只增不删，v3 合入后未删 v2）。共享盘 03 目录仅 v3（干净）。
**此失败与本任务无关**：本任务只改 02 线路径定位/文档，verify_all 的 catalog 步用的是 01 线
`catalog_ingest.py`，未受本任务影响。

## 四、红线自查

只改 02 线 7 文件；01 verify_all / catalog_ref_ci shim 只读未删；无二进制/网络；CC-10 默认仍 WARN 不破门禁。
