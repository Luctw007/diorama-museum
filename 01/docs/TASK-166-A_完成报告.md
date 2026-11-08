# TASK-166-A 完成报告（v0.1 发布自检门禁与验收基线冻结）

## 交付物清单
- `scripts/release_check.py`（新增）：`PROJECT_RELEASE_VERSION="0.1.0"` 单一落点；R1 验收基线（verify_last.json passed==total）、R2 三台真跑槽位 module 非空 + 三份许可存在、R3 完工包 ≥30（wip 仅打印）、R4 源码残留扫描（TODO/FIXME/XXX/预留/占位，只暴露不计 rc）、`--smoke` 演示帧冒烟（失败计 rc）、`--snapshot` 基线冻结；网关版本/协议版本只读引用不改。
- `docs/verify_baseline_v0.1.json`（由 --snapshot 生成）。
- `docs/RELEASE-v0.1.md`（新增）：版本关系（0.1.0 项目 / 0.2.0 网关 / 协议 v2，网关版本未改）、三件套运行说明、验收基线、许可清单（三件均未见二进制、细节[需核实]）、已知需核实清单（引 161-A/B）。

## 验收日志（原样）
1. `python 01/scripts/release_check.py` → 版本行「项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）」；R1 PASS（37/37）、R3 PASS（30≥30）、R2 六项 PASS、R4 INFO（mame_apple2.py「占位」×1，已知骨架注记）；`汇总：硬断言 FAIL 0 处 → rc=0`，$LASTEXITCODE=0
2. `--smoke` → 「画廊已生成: D:\work\01\repo\01\demo_out\gallery.html」「完成：5 帧 PNG → …\demo_out\frames」、`[PASS] SMOKE … rc=0`
3. `verify_all.py --daily --cache` → **结果：37/37 通过**
4. `release_check.py --snapshot` → `[PASS] SNAP 基线已冻结：…verify_baseline_v0.1.json（time=2026-11-07 13:18:26 passed=37 total=37）`
5. `slot_loader.py --list` → mame-apple2 / simh-pdp8 / stella 三行均「MISSING(无二进制)」、均不带「（后端模块预留）」

## 与任务书的漂移
- R4 扫描命中仅 1 处（mame_apple2.py 骨架「占位」注记），无新发现残留；其余按任务书实现。
- 任务书称「基线 37/37」，实跑一致（37/37），无漂移。
- --snapshot 时任务书未要求同时跑断言，实现为独立快照动作（也可与 --smoke 连用）。未下载任何二进制；未做 git/提交/推送。