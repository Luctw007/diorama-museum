# DEFECT-M1-ROLLBACK-01 （m1_check 回滚断言失败 · 归 01 线网关/后端）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 编号 | DEFECT-M1-ROLLBACK-01（用例 T-061 网关侧） |
| 轮次 | round_1（2026-10-31）→ round_2（2026-11-02，04 线独立复测闭环） |
| 档位 | 自动化（m1_check 第 8 项） |
| 状态 | closed（round_2 复测通过，修复已验证） |
| 归口 | 01 线（gw/emulators/fake_emulator.py · on_load_state 与 _produce_loop；网关 load_state 转发） |

## 1. 失败断言描述

```
M1 验收失败 ✘  ->  回滚生效：回滚后第一帧 frame_id=14（保存点 14，此前已达 20）
```

断言：`roll_f.get("frame_id") >= save_pt + 1`（m1_check.py L325 附近）——回滚后第一帧应 ≥ 保存点+1。

## 2. 稳定复现性

- 第 1 轮：保存点 15，回滚后第一帧 **15**（此前已达 21）→ FAIL。
- 第 2 轮（清理 TEMP 残留快照后干净环境）：保存点 14，回滚后第一帧 **14**（此前已达 20）→ FAIL。
- 结论：**确定性复现（2/2）**，与持久化残留无关。

## 3. 最小复现序列（命令级）

```json
{"proto":2,"type":"start_device","emulator":"fake","device_id":"dev1",
 "config":{"width":160,"height":120,"fps":15,"frame_codec":"rle",
           "force_chunk":true,"force_chunk_chars":15000,"sinks":["main","led"]}}
// 收帧至 frame_id 连续 ≥5 → 单帧分片证据 → 等 light_state ×2
{"proto":2,"type":"input_event","device_id":"dev1","map":"keyboard","key":"a","value":true}
// 收 input_ack
{"proto":2,"type":"save_state","device_id":"dev1","id":"s1"}
// 收 save_state_ack{frame_id:N}；继续收帧至 frame_id > N+5
{"proto":2,"type":"load_state","device_id":"dev1","id":"s1"}
// 收 load_state_ack{frame_id:N} —— 其后再收到的「回落后第一帧」frame_id == N（期望 ≥ N+1）
```

## 4. 网关 stderr 关键行（第 2 轮，干净环境）

```text
[gw] 网关 v2 已监听 127.0.0.1:17333（repo: \\DESKTOP-2IDAL09\work\01\repo）
[gw] [dev1] [fake] 无历史快照文件（首次启动）: C:\Users\Luctw\AppData\Local\Temp\diorama_dev1.json
[gw] [dev1] [fake] start config={...frame_codec:'rle', force_chunk:True, ...} device_id=dev1
[gw] [dev1] 内部快照 __auto 已更新（frame 2）
[gw] [dev1] 内部快照 __auto 已更新（frame 14）
```

（守卫输出本身无 ERROR 行——失败是语义断言而非进程错误。）

## 5. 疑似根因（供 01 线排查，未经修改验证）

`FakeBackend.on_load_state`（网关读线程）执行 `self._frame_id = self._saves[sid]`，与 `_produce_loop`（后台线程）的 `self._frame_id += 1` / `emit(frame_id=self._frame_id)` **无锁并发**：

- on_load 写入保存点值后，produce 线程若在 `+=1` 之后、emit 之前被穿插（或反之），emit 出的帧号将等于保存点本身（帧内容与帧号也随之错位一档）；
- 与 m0_check 的差异：m0 走 raw 全帧路径、M1 走 force_chunk 分片路径，帧到达时机的错位使断言窗口命中该竞态帧。
- 建议：load 时间戳与帧号分配加锁，或 load 后序列强制从保存点+1 起发。

## 6. 贴证物与备注

- 网关 stderr 尾部完整日志：`design/rounds/m1_round_1.log`（两次运行均录）。
- 附带发现（测试卫生，低优先）：TEMP `diorama_dev1.json` 跨轮残留，会导致下次运行"已加载持久化快照 2 个"；建议 m1_check 首行清理 `%TEMP%\diorama_*.json` 或改用随机 device_id 后缀。
- 依据 09 号 §4：m0/m1 失败归 01 线；下游手工档（T-023 等含网关补验）按漏斗规则搁置待修复后重开。

## 7. round_2 复测结果（2026-11-02 · 04 线独立复测）

### 7.1 复测结论

**通过（PASS）** —— 回滚断言在干净环境下连续 2 次完整运行均精确命中「回滚后第一帧 == 保存点+1」，竞态修复得到统计性复核确认。

### 7.2 通过证据（日志全文见 `design/rounds/`）

| 脚本 | 断言数 | 结果 | 回滚断言实值 |
|---|---|---|---|
| m0_check（17331） | 23 | 23/0 | `回滚后第一帧 frame_id=6（保存点 5，回滚前已达 11）` → 6 == 5+1 ✓ |
| m1_check 第 1 轮（17333） | 42 | 42/0 | `回滚后第一帧 frame_id=11（保存点 10，此前已达 16）` → 11 == 10+1 ✓ |
| m1_check 第 2 轮（17333，连续复跑） | 42 | 42/0 | `回滚后第一帧 frame_id=11（保存点 10，此前已达 16）` → 11 == 10+1 ✓ |

- 两轮均为均值附近保存点（10），回落后首帧恰为保存点+1，无一次回落至保存点同值（原竞态特征帧）；
- 日志：`design/rounds/m0_round_2.log`、`m1_round_2_run1.log`、`m1_round_2_run2.log`（完整 stdout）。

### 7.3 关闭说明

1. **01 线修复核验（代码层）**：`gw/emulators/fake_emulator.py` 已新增 `self._frame_lock = threading.Lock()`（L68，注释注明本缺陷编号）；`_produce_loop` 帧号分配（L133-136）、`on_save_state`（L215-219）、`on_load_state` 回卷写入与 ack（L221-234）均在同一把锁内，读改写互斥，杜绝「发出帧号==保存点」竞态。
2. **测试卫生附带项已处置**：`scripts/m1_check.py` 入口新增 `%TEMP%\diorama_*.json` 首行自清（L186-191），本缺陷 §6 的测试卫生建议已由 01 线落地；round_2 执行前 04 线亦独立手工清空 TEMP 残留（实查 0 个残留文件）。
3. **漏斗解锁**：本缺陷闭环后，其下游手工档（T-023/027/028/061 等含网关补验用例）不再受本轮漏斗搁置。
4. 处置方式：无需提级（09 号 §4 提级路径未触发），04 线不出改 01 线代码的任何变更。

### 7.4 状态

**open → closed**（INDEX 同步更新）。