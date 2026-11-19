# TASK-201-B 完成报告（simh-altair-8800 后端转正 + need_verify 复查）

## 交付物清单
1. `gw/emulators/simh_altair_8800.py`（新增）：同构复制母本 + 定向替换——`SimhAltair8800Backend`，name=`simh-altair-8800`；`_find_binary()`（SIMH_ALTAIR_BIN → third_party/simh/altair8800(.exe)）；缺二进制 → `EMULATOR_BINARY_MISSING` + rc=1；start.ini/命令文件（diorama_altair8800_*）；横幅 `ALTAIR simulator`、命令名、TTY 注入、SAVE·LOAD 全部 [需核实]；`--check-binary` 缺失 rc=2。
2. `slots/emulators/simh-altair-8800/manifest.json`（改）：`module: null → "gw.emulators.simh_altair_8800"`；desc 去「预留」改「后端骨架已接，与 simh-pdp8 同构」。
3. `docs/realrun_launch_param_check.md`（改）：§五更新为「TASK-201-B 复查版」——need_verify 6 项续挂逐条复查（无新核销）、第二批 SIMH 4 台全部转正、R2 口径更新。
4. `slots/README.md`（改）：altair 行「预留 → **转正（201-B）**」，第二批 SIMH 槽位 4 台齐（pdp8/hp2100/nova/altair）。
5. `docs/TASK-201-B_完成报告.md`。

## 验收日志（原样）
1. `verify_all.py --daily --cache` → **结果：44/44 通过** rc=0
2. `slot_loader.py --list` 关键行：`simh-altair-8800  OK(native,无二进制要求)  SIMH Altair 8800（后端骨架已接，与 simh-pdp8 同构…`（不再带「预留」标记）
3. `release_check.py` → `[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）`；`汇总：硬断言 FAIL 0 处 → rc=0`
4. need_verify 复查自证（§五 201-B 版关键行）：**核销 5 / 续挂 6，无新增**——MAME boot.lua 抓帧+键码回显（2）、SIMH start.ini 命令名/TTY 注入/SAVE·LOAD（3）、Stella 无头开关与直读 API（1，缺 DLL 续挂 + 191-B 绕行方案不删）；第二批 SIMH 4 台全部转正、无预留残留。
5. manifest 关键字段 diff：`"module": null → "gw.emulators.simh_altair_8800"`。

## 与任务书的漂移（如实）
1. 转正同样采用「母本复制 + 定向替换」并 grep/py_compile 校验（无 hp2100 残留）；binary 文件名 `altair8800` 为同构推定（Open SIMH 实际二进制名 [需核实]，已随 docstring 标注）；
2. need_verify 本轮**无新增核销**（介质/DLL 依赖未变）——按红线如实续挂，未把「待核」写成「已就绪」；
3. 门禁 43→44/44（他线新包）；未下载/未编译/未 Popen、未改 02/03/05 线、未做 git（统筹收口）。