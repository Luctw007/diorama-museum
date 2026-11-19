# TASK-191-A 落地记录（v0.7 T 项 A-1 / D-2 · 01 线主权落地）

> 供 02 线同步 v0.7 终稿引用。187-B《v0.7 RTO 项裁决记录》中 A-1、D-2 原为「转 1.x 待办」，
> 本记录声明二者已由 01 线落地，02 线可在终稿把这两条状态回写为「已落地（01 线）」。

## A-1（`none` 入 media_class 枚举）落地

- 文件：`01/scripts/slot_loader.py`
- 行号：L40-43 新增 `MEDIA_CLASSES = ("disk", "firmware", "cartridge", "tape", "cd", "dvd",
  "card", "app_package", "none")`——`none` 为正式合法枚举值；
- 行号：L110-114 `resolve_entry()` 增加枚举核对：`none` 不告警；未知值放行但 stderr 提示对齐；
- 行号：L89-101 `resolve_entry()` 支持 manifest 显式 `"module"`（含 `null`=reserved 预留）。
- 口径文档：`01/slots/README.md`「manifest 字段补充」节（none 计入 CC-10「有值」口径，不视为缺失）。
- 运行自证：`assert 'none' in slot_loader.MEDIA_CLASSES` → `[PASS] none 在 MEDIA_CLASSES 枚举`（rc=0）。

## D-2（run_status 并入 release_check R2）落地

- 文件：`01/scripts/release_check.py`
- 行号：L73-79 新增 `run_status_of(entry)`——`live`（二进制就位）/ `dry-run`（有模块无二进制）/
  `missing`（无模块预留）；
- 行号：L82-100 `check_r2()` 三台真跑槽位逐台输出 `run_status` 并断言 ∈ {live, dry-run}（missing 判 FAIL）。
- **01 线裁定（阈值）**：真跑阈值维持 **≥3**（三台真跑），随真跑台数实测后按 04 线 66 号口径上调（≥5）；
  v0.7 终稿如写「R2 含 run_status」，此处即实现出处。
- 运行自证：`release_check.py` 输出三行 `[PASS] R2 槽位 … run_status=live`（本轮实测，FAIL 0，rc=0）。

## 门禁回归
- `verify_all.py --daily --cache` → **42/42 通过**（35 完工包 + 7 步，rc=0；期间 hp-2100 等新包入册）。
- 未改 02 线规范正文、未改 03/05 线文件、未做 git（统筹收口）。