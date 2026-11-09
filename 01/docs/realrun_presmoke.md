# 三台真跑预启动检查结果与参数核对卡（realrun_presmoke）

> TASK-176-A · `scripts/realrun_smoke.py` 实测输出存档。**零介质、零下载、零联网**。

## ① 逐台实测表（原样引用 realrun_smoke.py 输出）

| 台 | 探针 | 实测首行/结果 | 判定 |
|---|---|---|---|
| mame | `-version` | `0.289 (mame0289)` · rc=0（跨共享盘首载耗时约 33s） | PASS |
| mame | `-createconfig -inipath <临时目录>`（cwd=临时目录） | rc=0 · `mame.ini` 生成（实测 MAME 把 ini 写到 **cwd** 而非 inipath 目录；stderr `Skipped plugin.ini, could not find any plugins` 无碍） | PASS |
| simh | 无参 + stdin `quit` | `PDP-8 simulator Open SIMH V4.1-0 Current        simh git commit id: 87eb7d5e` · quit 后 rc=0 | PASS |
| stella | `-help` | （无输出） | 回退无参 |
| stella | 无参启动 | rc=0xC0000135（STATUS_DLL_NOT_FOUND）· 目录内仅 `stella.exe`（6.7MB）、**无 SDL2.dll** | **FAIL**（环境缺运行库，转用户补全） |

smoke 汇总：mame 2/2 PASS、simh 1/1 PASS、stella FAIL → 脚本 rc=1（stella 环境修复后重跑即全绿）。

## ② 实测版本 ↔ 任务书声明对照

| 台 | 任务书口径 | 实测 | 结论 |
|---|---|---|---|
| MAME | 0.289 | `0.289 (mame0289)` | ✓ 一致 |
| SIMH | Open SIMH V4.1-0 | 横幅 `Open SIMH V4.1-0 Current`（git 87eb7d5e） | ✓ 一致 |
| Stella | 7.0c | 进程无法启动（0xC0000135），版本暂无法由进程确认 | [需核实]（转用户补运行库后验） |

## ③ need_verify 就位态口径（本卡核销/续挂）

**本卡实测核销**（原 161-A/B 的 [需核实] → 实测成立）：
1. SIMH 退出命令名 = `quit`（实测退出、rc=0）；
2. SIMH 就绪横幅关键字 = `PDP-8 simulator`（实测命中 `Open SIMH V4.1-0` 行）；
3. MAME `-version` / `-createconfig` 行为与 ini 落点（cwd）。

**仍挂 [需核实]（转交对象）**：
- MAME：位图直读 API / boot.lua 通道 / natkeyboard 键码（realrun_drill_v3 §二 #1-4）——转用户装 ROM 后按 m2a 断言核对；
- SIMH：启动脚本传参方式、TTY 注入通道、快照 SAVE/LOAD 命令名——转 05 线预研/用户实跑核对；
- Stella：**当前连启动都不行**——转用户补全运行库 DLL（如 SDL2.dll 等，具体清单 [需核实]，建议与 stella.exe 同目录）；补全后 `-help`/无 ROM 报错路径、启动参数、帧 rgba8/音频 pcm16 直读 API、键码注入通道仍逐条 [需核实]（转 05 线）。

> 判定口径：本卡只记录实测；三后端骨架代码不做"貌似能跑"改动，need_verify 核销一条、移除一条。