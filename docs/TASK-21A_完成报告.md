# TASK-21A 完成报告（docs/TASK-21A_完成报告.md）

> 01 线 · 2026-11-02 · 任务：m2a_check 双轨可运行实现（见 任务21-A 文档）。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/m2a_check.py` | 320 | M2 里程碑验收双轨：fake 轨 10 断言（a/b/c/d/e/g/h/i/j + 停止）；`--mame` 轨二进制缺失 → 错误路径断言 + SKIP（rc=0） |
| `docs/m2_assert_draft.md`（改） | — | 顶部补"实现状态"段：协议字段对齐差异说明 |

## 2. 运行日志（原文）

```text
$ python -u scripts/m2a_check.py
  [PASS] a：fake 设备启动 ok（进入 running）
  [PASS] b：连续 5 帧 frame_id 严格递增（1..5）
  [PASS] c：帧格式 rgb8 且尺寸 280×192×3 校验成立（161280 B）
  [PASS] d：音频块格式 s16le
  [PASS] e：KEY_A 注入回显一致
  [PASS] g：两次注入各自独立回显（KEY_R 先于 KEY_T）
  [PASS] h：save_state_ack.frame_id=8（正整数）
  [PASS] i：推进 ≥5 帧（8 条）后 load_state_ack.frame_id==保存点 8
  [PASS] j：回滚后第一帧 frame_id=9（== 保存点+1）
  [PASS] 设备停止正常（reason=user）
M2a(fake 轨) 结果：PASS 10 / SKIP 0      → rc=0

$ python -u scripts/m2a_check.py --mame
  [PASS] mame 轨错误路径：无二进制 → EMULATOR_BINARY_MISSING（正确）
  [SKIP] ×5（frame 流/音频/输入/存档/真实帧特征，均标注"等待人工安装"）
M2a(mame 轨) 结果：PASS 1 / SKIP 5      → rc=0（SKIP 语义不误红）
```

## 3. 迭代记录（3 轮，全部为"草案简名 ↔ 网关实际字段"的协议对齐问题）

1. **轮 1（超时）**：草案写 `frame` 事件，网关实际广播 `frame_ready`（width/height 字段）→ 收帧卡死；
2. **轮 2（洪水无期）**：存档 ack 应为 `save_state_ack`/`load_state_ack`（非 `ack+op`）；期间暴露 recv 设计缺陷——消息连续流入时 deadline 永不判定（keep 5314 条），已加固为"每次循环判期"；
3. **轮 3**：全绿。差异已写回 m2_assert_draft 顶部"实现状态"，并作为 PROTOCOL v2 客户端实现的字段名权威来源记录。

## 4. SKIP 语义说明（任务要求的关键设计）

- `--mame` 轨在二进制缺失时：错误路径断言计入 PASS，其余 M2 断言逐条 SKIP，**退出码 0**——
  保证接入 verify_all 门禁后，未装 MAME 的日常环境不会被误判失败；
- SKIP 条目名称与 m2_assert_draft 断言编号一一对应，MAME 到位后同脚本自动启用真实断言（280×192 特征、音频 [需核实] 项仍保留 SKIP 能力）。

## 5. 开放问题

1. MAME 就位后的真实轨尚缺"帧特征自动比对"（开机画面 280×192 的纯色基线比对可后续加）；
2. fake 轨 width/height 来自 config 递推（280×192），真实轨验收时需校对 Lua 抓帧的实际宽高。