# TASK-46B 完成报告（docs/TASK-46B_完成报告.md）

> 01 线 · 2026-11-04 · 任务：槽位绑定与一键启动（见 任务46-B）。
> 本报告含 TASK-46 两份总收尾，01 线本轮（任务 46-A/B）完成。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/launch_device.py` | 175 | 决策链（demo→fake / slot→真实或 MISSING 指引）；`--force-demo` 预览通道；PNG 帧存证（复用 demo_frames） |
| `scripts/slot_consistency_check.py` | 78 | SC-01 类目合法性 / SC-02 槽位就绪提示 / SC-03 未声明 INFO 基线 |
| `scripts/run_profile.py`（改） | +1 | mapping 输出透传 `slot` 提示（不破坏既有断言） |
| `scripts/verify_all.py`（改） | — | 新增 `slots` 步（full/daily 均含）；`--only slots` |
| `docs/runtime_mapping.md`（改） | — | §9 slot 提示字段契约 |

## 2. 运行日志（原文关键段）

```text
$ python scripts/launch_device.py --device apple-ii --force-demo --frames 5
  决策: 槽位未建立 → MISSING（先按 slots/README.md 建 manifest）
  （--force-demo：预览通道，非真实运行）
  演示启动 ok（sinks=['main','speaker','led'] 画面 320x240@24.0）
  帧存证：5 张 PNG → demo_out\launch            → rc=0

$ python scripts/launch_device.py --device pdp8
  决策: 槽位未建立 → MISSING（先按 slots/README.md 建 manifest）
  [MISSING] mame_binary … / [MISSING] simh_binary …（doctor 指引）
  （装好二进制/介质后重跑本命令即自动切换真实通道）

$ python scripts/launch_device.py --device system360 --dry-run
  决策: demo_mode → fake 演示直起（无需槽位）     → rc=0

$ python scripts/slot_consistency_check.py
  汇总：完工包 15，声明 slot 0，SC-01 违规 0     → rc=0（基线 v0）

$ python scripts/verify_all.py --daily
结果：18/18 通过（m0 + m1b + slots + 15 包）
```

## 3. 迭代记录（2 轮）

1. 轮 1：apple-ii 的 emulator=mame（真实声明）使其走 MISSING 分支，任务要求的"demo 帧存证"不可达 → 增 `--force-demo` 预览通道（演示与真实双通道语义并存）；
2. 轮 2：m1b 回归确认 run_profile 新增 `slot` 键不破坏 19 条断言（输出增量字段安全）。

## 4. "用户三步可用"路径（对照 Batocera 体验）

1. 把模拟器二进制 + manifest 放入 `slots/emulators/<slot_id>/`，介质放入 `slots/media/…`；
2. 按需在设备包 runtime 声明 `slot` 提示（03/05 线回填）；
3. `python scripts/launch_device.py --device <任意设备>` —— demo 设备直出画面帧，真实设备二进制就位后自动切真实通道；未就位给出 doctor 指引。全程零代码改动、零下载。

## 5. TASK-46 两份总收尾 + 01 线本轮完成标注

- 46-A：槽位装载器 + 网关自动注册 + doctor 槽位区 + 样例槽位真跑证据；
- 46-B：一键启动决策链 + 槽位一致性检查 + 门禁含 slots 步 18/18；
- 01 线本轮（任务 46）完成。