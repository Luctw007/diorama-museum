# TASK-102A 完成报告（02 线 1/2 · 轻量）

## 一、交付物

1. `tools/validate/catalog_ref_check.py` 支持 `DCM_MONO` 注入：`_mono_root()` 读环境变量，
   `repo_root()`=`<mono>/02`、`work_root()`=`<mono>`、新增 `line_repo(line)`=`<mono>/<line>`；
   未设置时保持原推导（向后兼容）。
2. `docs/规范增补_v0.6.2.md` 追加「七、扫描路径三种运行上下文与 CI 全门禁语义」。

## 二、两段运行输出（默认 vs 注入）

```
默认模式（共享盘 D:/work）：
  内容包 27 个，目录条目 1987 行  REF-01 0 / REF-02 0 / REF-03 0 / REF-04 0  FAIL 0
注入模式（DCM_MONO=01/repo 镜像）：
  内容包 26 个，目录条目 1987 行  REF-01 0 / REF-02 0 / REF-03 0 / REF-04 0  FAIL 0
```

## 三、关键发现：数字差 1 包 = 镜像陈旧，非工具缺陷

目录条目与 REF 四类两模式**完全一致**（1987 = 1987、FAIL 均 0，证明 `line_repo` 路径解析正确）；
内容包 27 vs 26 的唯一差异是 `x68000` 尚未同步进镜像（01 线 `sync_monorepo.py` 未重跑），属
**数据新鲜度**，非工具 bug。

## 四、开放问题

- 待 01 线重跑 `sync_monorepo.py` 后，两模式数字即可一致；01 侧 `catalog_ref_ci.py` shim 可退役。
