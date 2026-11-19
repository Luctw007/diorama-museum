# TASK-201-A 完成报告（simh-nova 后端转正）

## 交付物清单
1. `gw/emulators/simh_nova.py`（新增）：由 196-A 母本 `simh_hp2100.py` 同构复制 + 定向替换——`SimhNovaBackend`，name=`simh-nova`；`_find_binary()`（SIMH_NOVA_BIN → third_party/simh/nova(.exe)）；on_start 缺二进制 → `EMULATOR_BINARY_MISSING` + SystemExit(1)；start.ini/命令文件骨架（diorama_nova_*）；就绪横幅 `NOVA simulator`、交互命令、TTY 注入、快照 SAVE·LOAD **全部标 [需核实]**；`--check-binary` 缺失 rc=2。
2. `slots/emulators/simh-nova/manifest.json`（改）：`module: null → "gw.emulators.simh_nova"`；desc 去「reserved 预留」改为「后端骨架已接，与 simh-pdp8 同构」；其余字段（binary_env/media_classes）未动。
3. `slots/README.md`（改）：第二批 SIMH 槽位登记表 nova 行「预留 → **转正（201-A）**」。
4. `docs/TASK-201-A_完成报告.md`。

## 验收日志（原样）
1. `verify_all.py --daily --cache` → **结果：44/44 通过** rc=0（37 完工包+7 步，任务书预期的 cdc-6600/univac-1 类新包已入册）
2. `slot_loader.py --list` 关键行：
```text
simh-nova   OK(native,无二进制要求)   SIMH Data General Nova（后端骨架已接，与 simh-pdp8 同构…
```
（不再带「（后端模块预留）」标记）
3. `release_check.py` → `[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）`；`汇总：硬断言 FAIL 0 处 → rc=0`
4. manifest 关键字段 diff：`"module": null → "gw.emulators.simh_nova"`；simh_nova.py 关键行：BANNER_RE（[需核实]）、_find_binary（SIMH_NOVA_BIN/third_party/simh/nova）、on_start 缺二进制分支、_write_script。

## 与任务书的漂移（如实）
1. 转正采用「母本复制 + 定向替换」生成（与 hp2100 逐字同构），替换后 grep 校验无 hp2100/HP2100 残留、py_compile 通过；
2. `--list` 显示「OK(native,无二进制要求)」为无 binary_hint 槽位的既有统称显示（同 196-A 记录），语义以 module/desc/R2 run_status=dry-run 为准；
3. 门禁 43→44/44（他线新包）；未下载/未编译 SIMH 二进制、未改 02/03/05 线、未做 git（统筹收口）。