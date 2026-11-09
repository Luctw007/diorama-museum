# TASK-176-A 完成报告（三台真跑断言就位态改造 + 预启动检查）

## 交付物清单
1. `scripts/realrun_dryrun.py`（改）：断言从「无二进制写死」改为**自适应两态**——按 `slots_available()[slot_id]["binary_path"]` 分叉：就位态断言「二进制就位+真实后端」与 `--check-binary` rc=0 含「二进制」；缺失态保持原「未就位+EMULATOR_BINARY_MISSING」与 rc=2 含「缺失」；汇总标注检测态（就位/缺失/混合）。
2. `scripts/realrun_smoke.py`（新）：三台预启动检查（零介质零下载零联网）——mame `-version`+`-createconfig`（cwd=临时目录，事后删）；simh 无参+stdin `quit`（实测回退 exit 兜底）；stella `-help`→无参回退；超时 kill 判 FAIL；逐台打印实测首行。
3. `docs/realrun_presmoke.md`（新）：逐台实测表 + 版本对照 + need_verify 就位态口径（核销 SIMH quit/横幅、MAME 版本；续挂 MAME/SIMH/Stella 待核实项并标转交）。

## 验收日志（原样）
1. `realrun_dryrun.py` → 三台×三步 9 条 `[PASS]`（第2步「决策链干跑（就位态）命中『二进制就位 → 真实后端』」×3、第3步 rc=0 含二进制路径 ×3）；`汇总：三台×三步，FAIL 0 处；检测态=就位态（就位 3 / 缺失 0）`，rc=0（原 6 FAIL 现象消失）
2. `realrun_smoke.py` → mame 2 PASS（`0.289 (mame0289)` rc=0；createconfig mame.ini=生成）、simh PASS（横幅 `PDP-8 simulator Open SIMH V4.1-0 Current`、quit rc=0）、**stella FAIL（rc=0xC0000135 缺运行库 DLL，目录内 SDL2.dll=无）** → 汇总 FAIL 1，rc=1
3. 三后端 `--check-binary`（cwd=01）：均 rc=0——`MAME 二进制: …\third_party\mame\mame.exe`、`SIMH 二进制: …\pdp8.exe`、`Stella 二进制: …\stella.exe`
4. `emulator_doctor.py` → 三台 `[OK]`、`汇总：11 项，0 项阻断`、`部署就绪判定：三台真跑二进制 齐 · 介质目录已建 0 个`，rc=0；`--deploy-report .\docs\deploy_report_176A.json` → ready=true，rc=0
5. 回归：`verify_all.py --daily --cache` → **结果：39/39 通过**（rc=0）；`release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. mame `-version` 实测耗时约 **33s**（跨共享盘首载），任务书 30s 规格不满足 → smoke 放宽至 120s；
2. MAME 把 `mame.ini` 写到 **cwd** 而非 inipath 目录——首轮探针曾误向 `third_party\mame` 落 3 个 ini，已清理；smoke 改为 cwd=临时目录；
3. **stella 无法启动**（0xC0000135，裸 stella.exe 缺运行库 DLL）→ smoke rc=1 与任务书「预期 rc=0」不符——按红线如实 FAIL 并在 presmoke 卡标 [需核实]，转用户补全运行库后重跑 smoke 即全绿；Stella 版本 7.0c 暂无法由进程确认；
4. SIMH 退出命令 `quit` 实测有效（原 [需核实] 项核销）；
5. 门禁 37→**39/39**（03 线又新增完工包，32 台；非本任务引入）。未下载任何二进制/ROM；未做 git。