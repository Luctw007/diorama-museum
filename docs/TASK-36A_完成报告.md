# TASK-36A 完成报告（docs/TASK-36A_完成报告.md）

> 01 线 · 2026-11-03 · 任务：模拟器环境体检向导（见 任务36-A）。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/emulator_doctor.py` | 246 | 四项体检（MAME/SIMH 二进制+版本探测、网关自检、ROM 提示）+ `--json`/`--fix-check` 双模式 |
| `docs/doctor_guide.md` | ≥1000 字 | 用法、三态语义表、与人工三步对应、红线 |

## 2. 运行日志（原文）

```text
$ python scripts/emulator_doctor.py
[MISSING] mame_binary   third_party\mame\mame(.exe)
      >>> 安装 MAME 后放 third_party\mame 或设环境变量 MAME_BIN（licenses/MAME.md）
[MISSING] simh_binary   third_party\simh\pdp8(.exe)
      >>> 安装 SIMH 后放 third_party\simh 或设 SIMH_PDP8_BIN（licenses/SIMH.md）
[OK] gateway_self_test  网关可正常起停（端口 17338）
[HINT] rom_location_hint  ROM 红线：仅提示位置、不自动下载：…
汇总：4 项，2 项阻断（MISSING/FAIL）              → 文本模式 rc=0

$ python scripts/emulator_doctor.py --json        # 机器可读四对象数组 ✓

$ python scripts/emulator_doctor.py --fix-check
fix-check 不执行：二进制环境未齐备（mame_binary, simh_binary）   → rc=1（预期阻断）
```

## 3. 迭代记录（2 轮）

1. 轮 1：版本探测在无二进制时仍尝试执行 → 增加先判 OK 再探测；探测失败显示"（探测失败: …）"而不是裸异常；
2. 轮 2：fix-check 原本 MAME/SIMH 任一缺失都视为阻断——按任务语义"环境齐备才冒烟"，保留为正确拦截并输出未来可复用的日志路径模板。

## 4. 开放问题

- 网关自检端口的冲突处理只有提示——若 17338 常被第三方占用，下轮改为端口轮询选空闲；
- fix-check 的日志默认名含分钟级时间戳，多轮跑会生成多个文件（计划进归档规则：>3 份只留最新）。