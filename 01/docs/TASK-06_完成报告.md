# TASK-06 完成报告：网关 v2 + M1 数据驱动设备加载与 Inspect 交互

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组
> 任务：《任务06_网关v2与数据驱动加载》　日期：2026-10-31　执行位置：`work001\01\repo`

---

## 1. 交付物清单（路径 + 行数）

| # | 文件（`01\repo\` 下） | 行数 | 说明 |
|---|---|---|---|
| 1 | `gw/gateway.py` | 622 | 网关 v2 全量重写：分片广播、崩溃自动重启+快照恢复、多设备并发、sink 透传 |
| 2 | `gw/emulators/fake_emulator.py` | 214 | fake v2：rle 帧、led sink、受控崩溃注入、快照持久化 |
| 3 | `gw/emulators/rle.py` | 86 | 字节级 RLE 编解码 + 自测 main（已跑通） |
| 4 | `gw/PROTOCOL.md` | 189 | v2 契约：新增 §10（config 字段/frame_chunk/light_state/自动重启语义/错误码） |
| 5 | `gw/__init__.py` | — | `__version__ 0.2.0`、`PROTOCOL_VERSION 2` |
| 6 | `scripts/m1_check.py` | 401 | M1 全链路验收：13 段 / 42 条断言，全部通过 |
| 7 | `scripts/m0_check.py` | — | 未改动；v2 网关下回归全绿 |
| 8 | `godot/scripts/device_loader.gd` | 137 | 设备包（规范 v0.1）→ Node3D 树；glTF 缺失降级占位盒 |
| 9 | `godot/scripts/inspect_controller.gd` | 166 | Inspect 交互：轨道旋转/缩放/平移/屏幕空间点选/高亮+role |
| 10 | `godot/scripts/input_profile.gd` | 57 | 输入映射 JSON 加载/查询/校验 |
| 11 | `godot/scripts/gateway_client.gd` | 166（更新） | 增加 frame_chunk 重组与 light_state 显示（rle 解码留给后续） |
| 12 | `godot/scenes/main.tscn`、`godot/README.md` | — | 挂载新节点；README 补运行方式/决策记录/待验证清单 |
| 13 | `godot/content/test-device/` | — | 02 线示例包副本（数据驱动加载的测试对象） |
| 14 | 本报告 | — | — |

## 2. 验收运行日志（原文关键片段）

### 2.1 `python scripts/m0_check.py`（v2 网关回归）—— 全绿
```text
  [PASS] stopped ok=true reason=user
  [PASS] 未注册模拟器返回 EMULATOR_NOT_FOUND
  M0 验收全部通过 ✔
```
（结论：v2 网关对 v1 客户端行为完全兼容。）

### 2.2 `python gw/emulators/rle.py` 自测 —— PASS
```text
PASS 用例 0..5（含 255 连值分段、300 长游程）
PASS 随机 roundtrip ×3（5000 字节）
PASS max_len 防膨胀 / 畸形输入处理
rle 自测：PASS
```

### 2.3 `python scripts/m1_check.py` —— 42 条断言全绿（尾部节选）
```text
  [PASS] 单帧多分片证据：frame_id=6 total=10（force_chunk 生效）
  [PASS] dev1 led 灯状态交替：[True, False]
  [PASS] save_state_ack.frame_id=16
  [PASS] load 回到保存点 16
  [PASS] 回滚生效：回滚后第一帧 frame_id=17（保存点 16，此前已达 22）
  [PASS] 双设备并发 heartbeat：{'dev1': 'running', 'dev3': 'running'}
  [PASS] dev3 大帧尺寸正确（1440000）
  [PASS] 第1轮崩溃上报
  [PASS] 第1轮恢复：新进程签名帧 first=1（崩溃前 19）
  [PASS] 第1轮恢复流单调递增：[1, 17, 18, 19]
  [PASS] 第2轮崩溃上报 / 第2轮恢复（同第 1 轮）
  [PASS] dev2 连续失败重启上报 RESTART_EXCEEDED
  [PASS] dev2 降级 degraded
  [PASS] degraded 设备可 stop 清理
  [PASS] dev1 正常停止
  M1 验收全部通过 ✔（断言 42 条）
```

## 3. 迭代记录（3 轮问题修复）

| 轮 | 现象 | 分析 | 修复 | 结果 |
|---|---|---|---|---|
| 1 | 网关以脚本方式运行报 `ModuleNotFoundError: gw`（TASK-01 遗留已修，本轮未复发）；m1 首跑失败：回滚后第一帧 frame_id=23 > 保存点推导值 | TCP 单连接上，帧（17..23）先于 load_ack 发出并滞留在客户端 keep；"第一帧"取到的是加载前旧帧 | 回滚判定改为"等待 frame_id ≤ 保存点+3"，自动跳过旧帧 | 通过 |
| 2 | 第 1 轮崩溃恢复后 "帧连续 [1,17,18]" 断言失败 | 属正确行为：重启后新进程先产出 frame 1，网关 load __auto（=16）后跳到 17；恢复流是 1,17,18… 而非全局 +1 | 断言改为"新进程签名帧 ≤8 + 流单调递增"，并在注释与报告记录语义 | 通过 |
| 3 | rle 大帧（800×600 渐变图）编码代价与体积预判 | 渐变帧字节级同值游程几乎为 1 → RLE 反而膨胀 2×，且纯 Python 编码大帧成本高 | 测试矩阵调整：rle 用 160×120 小帧；大帧分片用 raw 编码（800×600）。决策写入 PROTOCOL/PROTOCOL 说明 | 通过 |

## 4. 协议 v2 设计决策说明

1. **分片阈值**：单条 JSON 行 > 512 000 字符即分片，每片默认 300 000 字符，`force_chunk_chars` 可覆盖（测试用小值强制多片）。判断在网关广播层，帧仍以完整 JSON 从后端上来。
2. **RLE 取舍**：字节级 RLE 实现极简（两个字节组），但对"无同值游程"的画面反而膨胀——因此 v2 只作为可选 codec，内容线接入真实模拟器时按画面特征选择，不预设默认编码。
3. **失败重启判定**（FR-E8 的边界语义）：`restarting→running` 后 5s 内再次崩溃**且期间无任何客户端命令**才算"失败重启"；输入触发的崩溃（如测试注入、玩家操作导致）不计失败、清零计数——避免把"用户在运行中触发崩溃"误判为后端无法运行。3 次失败 → `degraded` + `RESTART_EXCEEDED`。
4. **__auto 快照**：网关在设备 running 后立即写 `__auto` 基线，并在用户每次 save 时同步刷新；后端把快照持久化到 `persist_path`（temp 目录按 device_id 隔离）——这是"崩溃后跨进程恢复"成立的关键（快照随子进程死亡而消失的问题由此解决）。`__auto` 的 ack 与"没有快照可恢复"的 NOT_FOUND 均只记日志不下发，不污染客户端。
5. **Sink**：`main` 恒定出帧、`led` 出 `light_state`、`speaker` 对应音频；帧与音频消息都带 `sink` 字段，为 FR-E4 的"内屏/外接 CRT 多目标投放"留好路由语义。

## 5. 与 02/04 线对齐清单

- 键名与术语：沿用 TASK-01 PROTOCOL 与设计文档对象模型；`input_profile.gd` 的键名集合（key_*/button_*/joy_*）按规范 v0.1 第 11 章起始版实现，v0.2 键名全集由 07 线产出后对齐（列入开放问题）。
- 交互抽象：Inspect（轨道旋转/缩放/平移/点选）按 04 线《01_交互抽象与状态机》Inspect 原语实现；Grab/Point 与设备状态机属后续迭代。
- 设备包解析：严格按 02 线规范 v0.1 的 meta/assemblies/annotations 字段（kebab-case/snake_case、transform 为 [x,y,z,qx,qy,qz,qw] 米制）。

## 6. 「待验证」与开放问题

- **Godot 侧全部待实机验证**（本机未安装 Godot）：场景装载、点选高亮、I（nspect）手感参数、gateway_client 对 v2 网关的连通；验证清单见 `godot/README.md`。
- Godot 侧 rle 解码、VR 输入适配层、设备状态机（开盖/拆解）→ backlog。
- 与 07 线（规范 v0.2）的键名全集、sink 枚举对齐待合并。
- Godot 工程 `project.godot` features 仍标 4.3，安装 4.x 后首次打开会提示升级，确认即可。

## 7. 下一步建议

1. 安装 Godot 4.x 后按 `godot/README.md` 验证清单逐项打勾，把结果补充回本报告；
2. 与 08 线（Manchester Baby 内容包）汇合：将 `content/manchester-baby` 复制进 Godot 工程验证数据驱动加载的真实设备；
3. 网关接入真实模拟器后端（SIMH/MAME）时，按 PROTOCOL.md §10 复用 fake 后端作为协议对照实现。