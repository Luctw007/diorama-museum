# TASK-191-A 完成报告（v0.7 T 项 01 线主权落正文：A-1 + D-2）

## 交付物清单
1. A-1 落地（`none` 入枚举）：`scripts/slot_loader.py` L40-43 新增 `MEDIA_CLASSES` 枚举（9 值含 `none`）；L110-114 `resolve_entry()` 枚举核对（none 合法不告警、未知值放行提示）；L89-101 支持 manifest 显式 `module`（含 null=预留）。
2. D-2 落地（run_status→R2）：`scripts/release_check.py` L73-79 新增 `run_status_of()`（live/dry-run/missing 三态）；L82-100 `check_r2()` 三台槽位逐台断言 run_status ∈ {live, dry-run}；阈值裁定维持 ≥3（真跑后按 66 号上调 ≥5，已注释）。
3. 回写记录：`docs/TASK-191-A_落地记录.md`（供 02 线 v0.7 终稿同步回写「已落地」）。
4. `docs/TASK-191-A_完成报告.md`。

## 验收日志（原样）
1. `python .\01\scripts\verify_all.py --daily --cache`（py -3.7 同义）→ **结果：42/42 通过**（rc=0；35 完工包 + 7 步）
2. `python .\01\scripts\release_check.py` → 三行 `[PASS] R2 槽位 mame-apple2|simh-pdp8|stella run_status=live（live/dry-run 合法；missing 判 FAIL）`；`汇总：硬断言 FAIL 0 处 → rc=0`
3. A-1/D-2 自证：
```text
[PASS] none 在 MEDIA_CLASSES 枚举：('disk','firmware','cartridge','tape','cd','dvd','card','app_package','none')  rc=0
（release_check R2 run_status=live ×3 行即 D-2 判定生效证据）
```
4. 落地文件与行号清单：见 `docs/TASK-191-A_落地记录.md`（slot_loader.py L40-43/L89-101/L110-114；release_check.py L73-79/L82-100）。

## 与任务书的漂移（如实）
1. A-1 落地对象以仓库实际为准：01 侧无既有 media_classes 白名单，故在 slot_loader 新建枚举（含 none）并做放行式核对，未引入新的阻断语义；
2. D-2 阈值：任务书未指定数值——01 线裁定维持 ≥3（三台真跑），≥5 待真跑实测后随 66 号上调，已写入代码注释与落地记录；
3. 门禁计数 41→**42/42**（hp-2100 等新完工包入册，非本任务引入）；
4. 未改 02 线 v0.7 正文、未改 03/05 线、零下载零联网、未做 git（统筹收口）。