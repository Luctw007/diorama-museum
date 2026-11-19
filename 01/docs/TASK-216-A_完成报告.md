# TASK-216-A 完成报告（catalog_ref_ci 基径对齐修复 + 门禁工具链收尾）

## 交付物清单
1. `scripts/catalog_ref_ci.py`（改）：退役错误 monkeypatch（`C.repo_root/C.work_root` 指到 monorepo 根导致 02 工具按共享盘布局多套一层 `repo`，扫出「内容包 0 个」），改用 **02 工具原生 `DCM_MONO` 注入点**（catalog_ref_check.py L56-88 原生支持镜像布局：`<mono>/02` 与 `<mono>/<line>`，无 repo 层）——适配器只做 `os.environ["DCM_MONO"]=MONO` + 导入运行。
2. 门禁工具链收尾：hard 门禁基线确认 + ci 包装器单独运行自证。
3. `docs/TASK-216-A_完成报告.md`。

## 验收日志（原样）
1. hard 门禁：`verify_all.py --daily --cache` → `catalog_ref PASS FAIL 0`；**结果：47/47 通过** rc=0（40 完工包+7 步）
2. ci 包装器单独运行（修复后，镜像视图）：
```text
内容包 34 个，目录条目 1582 行
REF-01 悬空包引用：0 条
REF-02 反链缺失：1 个（[REF-02] 完工包 hp-2100 无目录反链）
REF-03 台账漂移：registry 1582 条 / 目录使用 1582 条（未使用 0 条）
REF-04 关联包形态非法：0 条   FAIL 1   rc=1
```
3. 修复前后对比：修复前「内容包 0 个、目录条目 0 行、FAIL 0（假绿）」；修复后 **N=34/M=1582 非 0**——基径对齐生效，扫描不再为空。
4. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. 任务书预期 ci 单独运行「FAIL 0」：实测修复后 **FAIL 1（镜像视图 REF-02=hp-2100 无目录反链）**——非适配器缺陷：镜像 03 目录 jsonl 早于 hp-2100 反链回填（live 视图已含反链，内嵌门禁 FAIL 0 47/47）；**统筹收口 sync_monorepo 后重跑 ci 包装器应归零**，已记录；
2. 一致性口径：ci 包装器为镜像视图（CI 无共享盘场景）、verify_all 内嵌为共享盘 live 视图——两视图数字不同（34 vs 40 包）属预期布局差异，非不一致；
3. 未改 02 线校验器、未镜像/未 git、未下载/未启动模拟器（统筹收口）。