# TASK-196-A 完成报告（第二批 SIMH 真跑矩阵后端接入）

## 交付物清单
1. `gw/emulators/simh_hp2100.py`（新增）：`SimhHp2100Backend(BackendBase)`，name=`simh-hp2100`，结构对齐 `simh_pdp8.py` 母本——`_find_binary()`（SIMH_HP2100_BIN → third_party/simh/hp2100(.exe)）；on_start 缺二进制 → `EMULATOR_BINARY_MISSING` + SystemExit(1)，否则启动脚本（diorama_hp2100_start.ini）+ 命令文件 + Popen 抽泵；终端文本流不产帧、就绪横幅 `HP2100 simulator` **标 [需核实]**；TTY 注入/快照 SAVE·LOAD/拉起方式全部 [需核实] 标注；`--check-binary` 缺失 rc=2。
2. `slots/emulators/simh-hp2100/manifest.json`（改）：`module: null → "gw.emulators.simh_hp2100"`，desc 去除「reserved 预留」改为「后端骨架已接，与 simh-pdp8 同构」。
3. 两个预留槽位（新增，module=null，desc 显式「后端模块未实现（预留槽位）」）：`simh-nova`（SIMH_NOVA_BIN，media_classes ["tape","disk"]）、`simh-altair-8800`（SIMH_ALTAIR_BIN，["tape"]）——media_classes 口径标 [需核实]。
4. `slots/README.md`（改）：新增「第二批 SIMH 槽位登记」表（pdp8 已接 / hp2100 转正 / nova·altair 预留）。
5. `docs/TASK-196-A_完成报告.md`。

## 验收日志（原样）
1. `verify_all.py --daily --cache` → **结果：43/43 通过** rc=0（36 完工包+7 步；中途一次 42/43 系 catalog_ref 瞬时 FAIL 1，独立复跑 FAIL 0、重跑收敛——他线在写，如实记录）
2. `slot_loader.py --list` 关键行：
```text
simh-hp2100     OK(native,无二进制要求)          SIMH HP 2100（后端骨架已接，与 simh-pdp8 同构…   [SIMH 许可（需核实…
simh-nova       OK(native,无二进制要求)（后端模块预留）  SIMH Data General Nova（后端模块未实现（预留槽位）…
simh-altair-8800 OK(native,无二进制要求)（后端模块预留） SIMH Altair 8800（后端模块未实现（预留槽位）…
```
3. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`（R2 含第二批三行：hp2100 已转正 run_status=dry-run、nova/altair missing 预留合法）
4. manifest 关键字段 diff：hp2100 `module: null→"gw.emulators.simh_hp2100"`；nova/altair `module: null`（预留）、binary_env SIMH_NOVA_BIN/SIMH_ALTAIR_BIN；simh_hp2100.py 关键行：BANNER_RE（[需核实]）、_write_script、on_start 缺二进制分支。

## 与任务书的漂移（如实）
1. `--list` 对无 binary_hint 槽位仍显示「OK(native,无二进制要求)」统称（既有显示行为），hp2100 转正语义以 desc/module 与 R2 run_status=dry-run 为准；
2. nova/altair 的 media_classes 无定案表逐字口径可查（["tape","disk"]/["tape"] 为按机型惯例推定），已在 README 与报告标 [需核实]；
3. 未下载/未编译任何 SIMH 二进制；未改 02/03/05 线；未做 git（统筹收口）。