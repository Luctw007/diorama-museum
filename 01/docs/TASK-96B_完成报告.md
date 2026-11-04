# TASK-96B 完成报告（01/docs/TASK-96B_完成报告.md）

> 01 线 · 2026-11-05 · 任务：CI 全门禁化（catalog/catalog_ref/pkg 挂入 runner）。

## 交付物

| 文件 | 改动 |
|---|---|
| `01/scripts/pkg_registry.py` | SCAN_ROOTS 镜像回退（D:\work 缺失/DCM_FORCE_MIRROR 时用 monorepo 03/05/content） |
| `01/scripts/catalog_ingest.py` | CATALOG_ROOTS 同模式回退 |
| `01/scripts/verify_all.py` | VALIDATOR 与 catalog_ref 步骤镜像回退 |
| `01/scripts/catalog_ref_ci.py` | 新增：monkeypatch 02 线工具的 repo_root/work_root 到镜像根（不改 02 文件，红线合规） |
| `.github/workflows/ci_01.yml` | 增三步：目录摄取门禁 / 目录引用一致性 / 全部内容包校验 |

## 验证证据

```text
本地镜像模式（DCM_FORCE_MIRROR=1）全门禁：31/31 通过 → rc=0
CI（head 03cd8db）：8 步 + 3 新增步 → conclusion = success（一次通过，无迭代）
```

## 说明

- 镜像回退判据 =「D:\work 缺失」或强制开关；本地默认行为不变（31/31 维持）；
- catalog_ref 在 CI 走 01 侧适配器（02 线主力工具按其自身位置推导路径，在 runner
  上会误判，故 shim 化）；下轮可建议 02 线把 work_root 做成环境变量注入以取代 shim。