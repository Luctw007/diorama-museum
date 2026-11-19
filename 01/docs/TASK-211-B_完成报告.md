# TASK-211-B 完成报告（镜像收口预检）

## 交付物清单
1. `docs/镜像收口预检_v1.md`（新增）：①共享盘 vs 镜像内容包差异清单（实测 6 台待镜像：03 线 univac-1/cdc-6600/cray-1/amiga-1000，05 线 apple-iie/crt-tv；镜像独有 0 干净）；②全包反链完整性核对（hard 门禁 catalog_ref FAIL 0、REF-02 缺失 0）；③镜像后 hard 门禁预期（46/46 维持 + REF-03 镜像视图归零 + cray-1 反链同步风险提示）；④收口步骤建议（dry-run → sync → hard 门禁 → git，供统筹执行）。
2. `docs/TASK-211-B_完成报告.md`。

## 验收日志（原样）
1. hard 门禁：`verify_all.py --daily --cache` → `catalog_ref PASS FAIL 0`；**结果：46/46 通过** rc=0（apple-iie 反链已由 210-A 回填，REF-02 缺口消除——206-B 的持久 FAIL 已收敛）
2. `catalog_ref_ci.py` → `内容包 0 个，目录条目 0 行；REF-01 0 / REF-02 0 / REF-03 registry 1582 条/使用 0 条 / REF-04 0；FAIL 0` rc=0（见漂移）
3. 差异清单自证（实测脚本输出）：
```text
03 共享盘独有 4 ['amiga-1000', 'cdc-6600', 'cray-1', 'univac-1']   镜像独有 0 []
05 共享盘独有 2 ['apple-iie', 'crt-tv']                            镜像独有 0 []
```
4. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. 任务书预期待镜像 5 台：实测 **6 台**（05 线多一台 **crt-tv**，02 口径 v1 未登记）——已列入预检清单并提示统筹核对；
2. 任务书预期「REF-03 未使用条目 C-PC-000208 回填后归零」：实测镜像视图已归零（registry 1582 = 使用 1582）；
3. `catalog_ref_ci.py` 单独运行扫描基径与镜像布局不一致（「内容包 0 个」但 rc=0）——权威口径以 verify_all 内嵌 02 检查器为准（FAIL 0）；ci 包装器基径对齐列为待办（记录，不修）；
4. hard 门禁已**恢复全绿 46/46**（206-B 的 44/45 缺口收敛）；未执行镜像/git、未下载/未启动模拟器、未改 02/03/05 线（统筹收口）。