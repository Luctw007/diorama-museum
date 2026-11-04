# TASK-56B 完成报告（docs/TASK-56B_完成报告.md）

> 01 线 · 2026-11-04 · 任务：整厅批量演示（launch 扩展）。
> 本报告含 TASK-56 两份总收尾，01 线本轮（任务 56-A/B）完成。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/launch_lib.py` | 140 | 共享库：find_pkg/decision_chain/ensure_gateway/run_demo(quiet)/print_doctor_guide（自 46B 抽取） |
| `scripts/launch_device.py`（重构） | 63 | 单机入口精简为 lib 调用（行为不变） |
| `scripts/launch_room.py` | 110 | 整厅批量：布局→逐台决策→demo 帧存证/非 demo 链打印→room_summary.md |

## 2. 运行日志（原文关键段）

```text
# 重构回归（三个原命令）
$ python scripts/launch_device.py --device apple-ii --force-demo --frames 3
  演示启动 ok（…320x240@24.0）／帧存证：3 张 PNG          → rc=0
$ --device pdp8 --dry-run      → 决策: 槽位未建立 → MISSING（…）
$ --device system360 --dry-run → 决策: demo_mode → fake 演示直起

# 整厅批量（黎明厅 4 台 × 3 帧）
$ python scripts/launch_room.py --layout godot\content\exhibit_dawn.json --frames 3
-- [1/4] eniac            demo_mode=True → 演示
-- [2/4] edvac            demo_mode=True → 演示
-- [3/4] edsac            emulator=qedsac → 非 demo：决策链打印，跳过
-- [4/4] manchester-baby  emulator=davidpsharp-baby → 非 demo：决策链打印，跳过
整厅完成：成功 4 / 失败 0；PNG 6 张；汇总 …room_summary.md    → rc=0
```

## 3. 迭代记录（2 轮）

1. 轮 1：抽取 lib 时 run_demo 的 quiet 参数补上（批量模式不刷屏），单机模式日志保持原样；
2. 轮 2：发现 edsac/manchester-baby 的 runtime 已声明真实模拟器（qedsac、davidpsharp-baby）
   → demo_mode=False、走决策链跳过——正是整厅脚本"不阻塞全厅流程"语义的实战验证；
   汇总表如实记"非 demo（跳过）"。

## 4. 与 04 线 28 号运行演示剧本的衔接

- 整厅模式 = 导览演示环节的批处理底座：每台"→演示/→决策链"结果即 44-B 三幕剧本的机器侧清单；
- 真实后端管线落地后，launch_room 的非 demo 分支将自动升级为真跑（决策链已预留）。

## 5. TASK-56 两份总收尾 + 01 线本轮完成标注

- 56-A：888 行目录 → 引擎包（27 片 + meta），验证对账通过；catalog_data.gd 数据层就绪；
- 56-B：共享库重构（回归零破坏）+ 整厅批量演示（黎明厅 4 台实测）。
- 01 线本轮（任务 56）完成。