# m2a_check 断言草案（docs/m2_assert_draft.md）

> **实现状态（TASK-21A）**：已落为 `scripts/m2a_check.py`，fake 轨 10/10 PASS、mame 轨
> 二进制缺失路径 1 PASS + 5 SKIP（rc=0）。实现与草案的协议字段对齐说明：网关把后端
> `frame` 广播为 `frame_ready`（宽高字段 `width`/`height`）、`audio` 广播为 `audio_chunk`、
> 存档 ack 为 `save_state_ack`/`load_state_ack`——下表"协议验证点"列沿用简化名，实现以
> 上述字段为准（差异记录见 docs/TASK-21A_完成报告.md §3）。

> 依据：05 线 13_MAME接入预研.md §六（里程碑切分）、gw/PROTOCOL.md v2 §10（消息语义）、
> 04 线 DEFECT 双案（帧号回滚语义、input_map 对象形态）的裁决。

## 1. 运行形态

- 客户端侧复用 `m0_check.py` 的连接/断言骨架，仅替换 `emulator="mame-apple2"`，
  config 增加 `machine="apple2"`、`frame_codec="rle"`、`sinks=["crt_display","speaker"]`；
- 双轨：
  - **fake 先行**：真实 MAME 未就绪时，m2a 的全部用例先对 `fake` 后端执行（回归语义），
    对 `mame-apple2` 只执行"二进制缺失 → EMULATOR_BINARY_MISSING"错误路径断言；
  - **真实 MAME 替换**：`third_party/mame/` 就位后，同一断言对 `mame-apple2` 执行，
    允许项：把帧分辨率断言从 fake 递推值改为 Apple II 6 色高分辨率 280x192。

## 2. M2.1 画面+音频（断言 a–d）

| # | 断言 | 协议验证点 |
|---|---|---|
| a | `start_device(mame-apple2)` → `start_device_ack ok=true` 且设备进入 `running` | ack + state 事件 |
| b | 连续收到 ≥5 帧，`frame_id` 严格递增（1..5） | frame 序列 |
| c | 每帧 `format=="rgb8"`；`w×h×3 == len(base64 解码)`；宽高 = 280x192（真实轨）或 = fake 配置值（fake 轨） | frame 字段 |
| d | （MAME 原生扬声器采样流通道 [需核实] 时启用）收到 `format=="s16le"` 的 audio 块；未启用时不作为失败项，记录 SKIP | audio 事件 |

## 3. M2.2 输入（断言 e–g）

| # | 断言 | 协议验证点 |
|---|---|---|
| e | `input_event(map=keyboard, key=KEY_A, value=true)` → 收到 `input_ack{map,key,value}` 回显一致（后端本地回显，不依赖 MAME） | input_ack |
| f | 注入 `KEY_A` 后至少 1 帧发生变化（真实轨人工目检开机画面特征；自动化以「注入后 N 帧内 frame 流不断」为下限） | frame 流连续 |
| g | 连续两次注入（press/release 间隔 ≥100ms）各自收到独立 input_ack，顺序一致 | ack 顺序 |

## 4. M2.3 存档（断言 h–j）

| # | 断言 | 协议验证点 |
|---|---|---|
| h | `save_state(id="m2_s1")` → `save_state_ack.frame_id` 为正整数 | ack |
| i | 继续推进 ≥5 帧后 `load_state("m2_s1")` → `load_state_ack.frame_id == 保存点` | ack 帧号 |
| j | 回滚后下一帧 `frame_id == 保存点+1`（04 线 DEFECT-M1-ROLLBACK-01 语义：回卷后不得重发保存点帧） | frame 流 |

## 5. 错误路径（fake 轨常开，真实轨 binary 就绪后关）

- `start_device(mame-apple2)` 在无二进制时 → `error code=EMULATOR_BINARY_MISSING`；
- 未注册模拟器（如 "mame-nes"）→ `EMULATOR_NOT_FOUND`。

## 6. 待真实 MAME 后核实的断言项（[需核实] 清单）

1. 帧抓取 API 与 280x192 的实际返回宽高（Lua 位图直读方法名）；
2. 扬声器采样流通道是否存在（决定断言 d 启用与否）；
3. `natkeyboard:post` 对 KEY_* 编码名（如 `KEY_LEFT`）的映射表；
4. 存档帧号由 Lua 帧计数回填的时延（决定断言 i 是否需要 ±1 容差）。