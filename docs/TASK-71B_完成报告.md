# TASK-71B 完成报告（docs/TASK-71B_完成报告.md）

> 01 线 · 2026-11-04 · 任务：真跑演习剧本 v2（三步放 + fix-check 演练 + 假二进制预演）。
> 本报告含 TASK-71 两份总收尾。

## 1. 交付物

| 文件 | 说明 |
|---|---|
| `docs/realrun_drill_v2.md` | 剧本全文（目标/三步放逐命令/manifest 照抄/doctor 演练/fix-check/决策链样例/need_verify 联动/用户操作卡/清理说明） |
| `slots/_drill/`（README + mame/mame_drill.bat + simh/pdp8_drill.bat） | 假二进制实验件，echo 版本字样，演示用途，可删除 |
| `docs/doctor_log_drill.txt` | fix-check 冒烟日志（修复后 rc=0） |
| `docs/drill_demo_out/` | demo 通道 3 张演示帧 PNG |
| `gw/gateway.py`（改） | 本次预演抓出的缺陷修复（见 §3） |

## 2. 实跑日志与数字

- doctor 体检（假二进制）：6 项，0 项阻断；mame/simh 两项 `ver=` 版本探测成功；
- fix-check（假二进制）：**全绿 rc=0**（m2a --mame PASS 1 / SKIP 0 + m0 22 断言全过），日志落盘；
- launch_device 决策链：`apple-ii` 输出"槽位未建立→MISSING+doctor 指引"（真实抓取，剧本 §5）；`amiga500 --frames 3` demo 通道出 3 张 PNG；
- 收尾门禁：`verify_all --daily --cache` **27/27 全绿**（缓存刷新，面板绿灯）。

## 3. 预演抓到并修复的缺陷（关键收尾）

首轮 fix-check 暴露 `gateway._spawn` 在无 `module` 字段的内置登记条目上
`KeyError: 'module'` → 客户端线程崩溃、m2a 挂死超时。修复：mame-apple2 补
`module`；`_spawn` 先判 module 缺失抛 `RuntimeError("EMULATOR_BACKEND_MISSING")`；
`cmd_start_device` 回发对应错误码（不再误导为二进制缺失）。修复后链路全绿。

## 4. 开放问题

- `launch_device --device apple-ii` 决策链目前只看"槽位扫描区"（slots/emulators/*/manifest.json），
  内置登记的 mame-apple2 未建槽位 manifest 时会报"槽位未建立"——与网关内置登记并存的双轨
  （内置即时可用 vs 槽位按 Batocera 契约自建），下轮可把内置登记折叠进槽位默认 manifest
  （future：72 之后安排）。
- m2a `--mame` 轨当前仅断言"无帧时 TIMEOUT 干净收场"；帧断言轨按 need_verify 清零后启用（26-A 口径）。
- `simh-pdp8` 后端模块仍未实现（预留），start 时现报 EMULATOR_BACKEND_MISSING（清晰、可预期）。