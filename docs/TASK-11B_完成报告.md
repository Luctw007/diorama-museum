# TASK-11B 完成报告：网关 × 内容包 runtime 对接

> 01 线 · 2026-10-31 · 执行位置 `D:\work\01\repo`

## 1. 交付物清单（路径 + 行数）

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/run_profile.py` | 207 | runtime → 网关 config 映射桥（demo_mode 判定 / sink 映射 / 键名校验 / 缺省画面表 / --start 模式） |
| `scripts/m1b_check.py` | 204 | M1b 验收：三个真实包映射正确性 + 两包经网关启动/注入/停止 |
| `docs/runtime_mapping.md` | 60 | 契约文档：优先级、缺省表、sink 表、两层键名模型、映射 JSON、错误策略 |

## 2. 运行日志原文（关键段）

`python scripts\m1b_check.py` —— **19 条断言全绿，退出码 0**：

```text
  [PASS] eniac：demo_mode 判定正确（emulator=none）
  [PASS] eniac：indicator_lamps → led 映射正确
  [PASS] manchester-baby：sink 映射 main+led+speaker
  [PASS] manchester-baby：early-computer 缺省画面 320x200@25
  [PASS] manchester-baby：36 键全部合法（未知 0）
  [PASS] manchester-baby：首键 power -> panel.power
  [PASS] apple-ii：sink 映射 main+speaker+led
  [PASS] apple-ii：computer 缺省画面 320x240@24
  [PASS] apple-ii：57 键全部合法（未知 0）
  [PASS] apple-ii：首键 key_a -> keyboard.key_a
  [PASS] manchester-baby：fake 设备启动 ok（sinks=['main','led','speaker']）
  [PASS] manchester-baby：ack 回显 sinks 与映射一致
  [PASS] manchester-baby：input_map 首键 power 注入回显一致
  [PASS] manchester-baby：停止正常
  [PASS] apple-ii：fake 设备启动 ok（sinks=['main','speaker','led']）
  [PASS] apple-ii：ack 回显 sinks 与映射一致
  [PASS] apple-ii：input_map 首键 key_a 注入回显一致
  [PASS] apple-ii：停止正常
  M1b 验收全部通过 ✔（断言 19 条）
```

回归：`m0_check.py` 全绿；`m1_check.py` 42 条断言全绿（v2 网关兼容）。

## 3. 迭代记录（2 轮）

| 轮 | 现象 | 分析 | 修复 |
|---|---|---|---|
| 1 | `run_profile` 报"无法读取 meta.json"，路径显示 `D:\work\01\03\...` | m1b_check 的 WORK_ROOT 少算一层（dirname 一次 = `01`） | 改 `os.path.dirname(os.path.dirname(REPO_ROOT))`；同轮修 run_profile 模块 docstring 的 `\.` 转义告警（改 raw 串） |
| 2 | 全绿 | — | — |

## 4. 设计决策

1. **两层键名模型**（runtime_mapping.md §5）：内容线 input_map 值是"设备逻辑令牌"（`keyboard.key_a`/`panel.switch.bit_00`），与玩家层物理按键分离——桥只校验令牌正则 `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$`，三个包 97 键全部合法，证明约定可执行；
2. **demo_mode 判定**：`emulator∈{none,demo,""}` → 静态展示，桥输出映射但不起设备（eniac 路径实测）；
3. **缺省画面表为过渡策略**：内容包 v0.1 未声明宽高/帧率，桥按 category 取缺省；02 线 v0.2 应在 runtime 增 `display` 字段，届时删除本表（已列入开放问题与 07 任务文档）；
4. **sink 映射**：surface 名 → 网关 sink（internal_crt/crt_display…→main、led/indicator_lamps→led、speaker→speaker），`type=audio` 强制 speaker。

## 5. 与 02 线/04 线对齐

- 键名正则、sink 枚举将提交为 02 线 v0.2 规范第 11 章的依据（runtime_mapping.md §5 结论段）；
- 玩家层（input_profile.gd）↔ 设备层（本桥）以"动作名"衔接的接入说明已写入 runtime_mapping.md §8；
- 11-C 运行锁以网关 status 为信号源，与本桥无耦合。

## 6. 开放问题

1. 画面缺省表何时由规范 `display` 字段取代（阻塞于 02 线 v0.2）；
2. 真实模拟器后端接入后，`emulator: fake` 替换路径与 format（mono1/rgba8）转换责任归属（后端层还是网关层）；
3. `bios_required=true`（apple-ii）的运行向导连接点留给游戏内 FR-E3，桥只透传。