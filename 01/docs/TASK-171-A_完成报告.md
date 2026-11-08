# TASK-171-A 完成报告（v0.1 发布收尾 · 部署手册 + doctor 终版）

## 交付物清单
1. `docs/SLOT_DEPLOY-Guide-v0.1.md`（新）：终版用户自装手册——①自装三步 ②唯一内置定位路径（third_party\... + MAME_BIN/SIMH_PDP8_BIN/STELLA_BIN，与 doctor/gateway 同口径）③三介质目录（占位自备）④Batocera 式 manifest 契约 ⑤一键体检与真跑链路（doctor/--fix-check/--deploy-report → launch_device → need_verify）⑥键码表与手柄位置（keymap_atari-2600 标 MAME 语义遗留）⑦排障表 ⑧红线声明（无任何获取渠道条目）。
2. `docs/doctor_guide.md`（更新终版）：补 Stella 行、slot 扫描区、--fix-check 与部署就绪判定口径；三态语义与用法（四种，含 --json/--deploy-report）。
3. `scripts/emulator_doctor.py`（收口）：新增 `deploy_readiness(checks)`、`deploy_line()`、`write_deploy_report()`；main 非 json 汇总行后追加「部署就绪判定」，--json 输出含 `deploy_readiness` 键，新增 `--deploy-report <path>`（恒 rc=0）；find_*/run_checks/--fix-check/--log 语义未动，未碰 slot_loader/gateway。
4. `slots/README.md`（更正）：「使用三步」第 1 步改为 `third_party\mame\mame(.exe)` 唯一内置定位路径（或 MAME_BIN）并注明 manifest 仓库已带；同时更正「内置兜底两条/预留」过期表述为三条且后端骨架均已接。

## 验收日志（原样）
1. `python .\scripts\emulator_doctor.py` → 三台 `[MISSING]`、`slot:mame-apple2|simh-pdp8|stella` 均 MISSING 且无「后端模块预留」；末尾
`部署就绪判定：三台真跑二进制 缺 3（缺: mame, simh, stella）· 介质目录已建 0 个`；$LASTEXITCODE=0
2. `python .\scripts\emulator_doctor.py --deploy-report .\docs\deploy_report_171A_demo.json` → 判定同 1；`部署签字已落盘 …（ready=false）`；文件内容：`{"checked_at":"2026-11-07 14:05:20","binaries":{"mame":{"status":"MISSING","detail":"third_party\\mame\\mame(.exe)"},…},"media_dirs":0,"media_count":0,"ready":false}`；rc=0
3. `python .\scripts\emulator_doctor.py --json` → 含 `"deploy_readiness":{"ok":0,"missing":["mame","simh","stella"],"total":3,"media_dirs":0,"ready":false}`
4. 回归：`release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`；`verify_all.py --daily --cache` → **结果：38/38 通过**（见漂移）
5. 红线自检：`Select-String … -Pattern "https?://|wget|curl|Invoke-WebRequest|下载链接"` → **无命中**（手册无任何获取渠道，仅「自备」类说明）

## 与任务书的漂移（如实）
- 任务书预期门禁 37/37：实况 **38/38**（03 线新增 nokia-3310 完工包，30→31 台；7 步+31 包）。首跑时曾出现一次瞬时 `catalog_ref FAIL 1`（37/38），独立复跑 catalog_ref_check 为 FAIL 0、再跑门禁即 38/38 收敛——属他线在写期间的抖动，未修他线文件、仅如实记录。
- `--deploy-report` 默认路径未实际使用（本任务以显式路径落盘 demo 样例）；语义与 rc 约定与任务书一致。