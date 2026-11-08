# 三台真跑联排干跑剧本 v3（realrun_drill_v3）

> TASK-166-B · 2026-11-07 · 01 线。承接 realrun_drill_v2（§6/§7）与 161-A/B 后端落地，
> 把「无二进制时」三台真跑的端到端优雅失败链收口为一条可执行干跑 + need_verify 收口清单。
> **全程零二进制、零下载。**

## 一、三台干跑结果表（`python 01/scripts/realrun_dryrun.py`，rc=0）

| 槽位 | 设备 | 第1步 槽位登记 | 第2步 决策链干跑 | 第3步 后端自测 |
|---|---|---|---|---|
| mame-apple2 | apple-ii | PASS（module 非空，无「预留」） | PASS（未就位 → EMULATOR_BINARY_MISSING → MAME_BIN 指引） | PASS（rc=2） |
| simh-pdp8 | pdp8 | PASS | PASS（→ SIMH_PDP8_BIN 指引） | PASS（rc=2） |
| stella | atari-2600 | PASS | PASS（→ STELLA_BIN 指引） | PASS（rc=2） |

三台决策链原文见 TASK-166-B 完成报告；三条均落在「决策: 二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引」。

## 二、need_verify 收口清单（逐条 [需核实] · 转交对象）

来源：realrun_drill_v2 §7（MAME 四项）+ TASK-161-A/B 报告 [需核实] 项。

| # | 项 | 出处 | 转交对象 |
|---|---|---|---|
| 1 | REPT/RESET（含 Ctrl+Reset）MAME apple2e 键码存在性 | v2 §7-1 | 用户装 MAME 后注入 key_repeat/key_reset，对照 keymap_apple2.json |
| 2 | natkeyboard 空格/大小写实际行为（key_shift+key_a、key_space 回显） | v2 §7-2 | 用户实机（m2a 输入回显断言同源） |
| 3 | 摇杆 ioport tag/field 名称 | v2 §7-3 | 以 MAME 源 apple2.cpp ioport 定义为准 |
| 4 | POWER/INSERT 驱动级实现（floppy_door 注入通道） | v2 §7-4 | 用户实机；无通道转媒体管理通道并回写 note |
| 5 | SIMH 启动脚本传参方式与命令名、就绪横幅精确字符串、TTY 注入通道、快照 SAVE/LOAD 命令名 | 161-A | 05 线预研 / 用户装 SIMH 二进制后核对 |
| 6 | Stella 启动参数（窗口/无头开关）、帧 rgba8/音频 pcm16 直读 API、键码注入通道、GPL-2.0 具体版本 | 161-B | 05 线 / 用户装 Stella 后核对 |
| 7 | Stella 键码翻译层：`keys/keymap_atari-2600.json` 为 MAME 语义遗留，Stella 以 `runtime.input_map`（joystick axis/btn、keyboard KEY_*）为语义参照 | 161-B | 05 线 / 02 线规范对齐 |

1-4 项全部通过后才允许 m2a `--mame` 帧断言轨启用（26-A 收口口径）；5-7 项逐条核对后把对应后端骨架补成真实数据通道。

## 三、二进制就位后的切换点

- 装二进制（`third_party\...` 或环境变量 MAME_BIN/SIMH_PDP8_BIN/STELLA_BIN）后：
  - `launch_lib.decision_chain` 自动切到「决策: 槽位 X 二进制就位 → 真实后端」分支（当前为「未就位 → EMULATOR_BINARY_MISSING」）；
  - `python 01/scripts/emulator_doctor.py --fix-check`：三台二进制齐备即自动冒烟（m2a --mame + m0），落盘日志；
  - `python 01/scripts/launch_device.py --device apple-ii|pdp8|atari-2600` 进入真跑通道；
  - 真跑当天按 §二 need_verify 逐条打勾，再跑 `verify_all --daily --cache` 收证据。
- 干跑预演在任何时候都可重跑（`realrun_dryrun.py`），保证无二进制环境不回归。