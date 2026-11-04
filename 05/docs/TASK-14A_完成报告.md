# TASK-14A 完成报告 · MAME apple2 接入后端预研

> 任务：TASK-14A（05 线 1/2）· 完成日期 2026-10-31 · 前置：TASK-10 定稿（MAME 首选）
> 主交付：`docs/research/apple-ii/13_MAME接入预研.md`（3620 汉字，≥3500 达标）

## 1. 调研结论摘要表

| 主题 | 结论 | 可行性 |
|---|---|---|
| Lua 脚本控制面 | 三种用法：`-console` / `-autoboot_script` / 插件，后端采用 `-autoboot_script` | 可行 |
| 输入注入 | `natkeyboard:post/post_coded` + I/O 端口 `field:set_value` | 可行 |
| 备选输入通道 | 无原生 stdin/命名管道通道，注入正路是 Lua | 无（结论明确） |
| 画面获取 | `-video none` + `video:snapshot()` + `register_frame_done`；位图直读方法名待核实 | 半可行 |
| 音频 | `-wavwrite` 文件式，非流式 | 半可行 |
| 存档 | `machine:save/load`（异步） | 可行 |
| 许可 | GPL-2.0（或更新），>90% 文件 BSD-3；独立进程 = 聚合 | 已核实 |

## 2. 映射表关键行（协议 ↔ MAME）

- `start` → `Popen(mame apple2 -console -autoboot_script boot.lua -video none …)`（可行）
- `input(keyboard)` → `natkeyboard:post/post_coded`（可行）；`input(joystick)` → `ioport.ports[tag]:field(mask):set_value`（可行）；`input(mouse)` → 无 API（不可行，本包不用）
- `save_state/load_state` → `machine:save/load`（可行，异步确认待核实）
- `frame` → `register_frame_done` 抓帧（半可行，直读 API 待核实）
- `audio` → `-wavwrite` 落盘读回（半可行，实时性待核实）

## 3. 来源清单（8 条，全文见 13 号 §七）

docs.mamedev.org/luascript（index / ref-core / ref-input）、git.redump.net/mame（luaengine.cpp）、mamedev.org（legal.html + 首页）、docs.mamedev.org/commandline/commandline-all.html、mankier.com/6/mame、mamedev.org/?p=491（Lua 变更说明）。

## 4. [需核实] 清单（V12–V18，已并入 15 号）

V12 位图直读 API · V13 存档确认信号 · V14 长按/REPT 模拟 · V15 音频实时流 · V16 缺 ROM 报错文本 · V17 新增错误码 MEDIA_MISSING · V18 Lua API 版本锁定。

## 5. 给 01 线的实现交接说明

**先做哪步**：第一步最小闭环（on_start + on_stop，跑通出帧）；第二步 on_input；第三步 on_save_state/on_load_state。**风险点**：V12/V13/V15 三项应优先做技术验证（spike）再写正式后端；MAME 二进制经 `binary_env: MAME_BIN` + `binary_hint` 用户配置，仿 `simh-pdp8`。**登记**：在 `gateway.py` 的 `EMULATORS` 加 `mame-apple2`（license GPL-2.0）。
