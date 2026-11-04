# 模拟器网关通信协议 v2（gw/PROTOCOL.md）

> 项目：《箱庭电子博物馆》（Diorama Computer Museum）· M0/M1
> 协议版本：当前 `proto = 2`（网关发出的消息携带 `proto: 2`；收到的消息 `proto` 缺省视为 1，保持向下兼容）
> 本文件是"契约"文档：任何网关或客户端的第二版实现必须与本文档一致。
> 第 1–9 章为 v1 规范（整体保留），第 10 章为 v2 扩展（TASK-06 新增，向下兼容）。

## 1. 为什么要有这个网关

主程序（Godot，MIT 许可）与模拟器（多为 GPLv2，如 MAME/SIMH）**只能通过独立进程 + 进程间通信集成**（设计文档 ADR D1），严禁任何形式的链接。网关负责：

1. 以子进程方式启动"模拟器后端"（emulator backend）；
2. 向客户端（Godot / 验收脚本 / 工具）暴露控制通道；
3. 把后端的帧 / 音频 / 状态事件广播给客户端；
4. 管理后端生命周期：启动超时、崩溃上报、停止兜底。

```
┌──────────┐  TCP 控制通道   ┌──────────────┐  stdio 设备通道  ┌──────────────┐
│ 客户端    │ ◄────────────► │ 网关 gateway │ ◄──────────────► │ 模拟器后端    │
│ (Godot/  │  JSON lines     │   (Python)   │  JSON lines      │ fake/simh/…  │
│  测试工具)│                 │              │                  │  (独立进程)   │
└──────────┘                 └──────────────┘                  └──────────────┘
```

## 2. 传输层

### 2.1 控制通道（客户端 ↔ 网关）
- TCP，默认 `127.0.0.1:7331`（网关启动参数 `--host` / `--port` 可改）。
- 报文格式：一行一条 JSON 对象，UTF-8，以 `\n` 结尾，**禁止**在 JSON 串中出现裸换行。
- 同一连接上可以任意顺序发送命令；响应与事件可能交错到达，客户端必须按 `type` 字段分发。
- 网关支持多客户端并发连接；所有事件（帧/音频/状态）**广播**给所有已连接客户端；命令响应（ack/error）只回给发令的那一个客户端。
- 帧/音频数据字段一律 **base64（标准字母表，可含 `+` `/` `=`）**；JSON 内不嵌二进制。

### 2.2 设备通道（网关 ↔ 模拟器后端）
- stdio：后端进程从 **stdin** 读命令、向 **stdout** 写事件（同样一行一条 JSON）。stderr 仅供日志。
- 后端是一个普通子进程（Python：`python -m gw.emulators.<name>`），与网关只通过上述文本协议通信。
- 后端不得自行监听端口或写文件（除非内容配置明确要求）。

## 3. 通用字段与约定

| 字段 | 说明 |
|---|---|
| `proto` | 协议版本，整数，当前 `2`（见第 10 章；v1 客户端继续可用） |
| `type` | 消息类型（见第 4、5 章枚举） |
| `device_id` | 设备实例标识。同一网关内唯一；同一设备同一时刻只能有一个运行实例 |
| `ts` | 时间戳，Unix 秒（float），事件消息携带 |

## 4. 控制通道消息集（客户端 ↔ 网关）

### 4.1 客户端 → 网关（命令）

| type | 字段 | 必填 | 说明 |
|---|---|---|---|
| `heartbeat` | — | — | 探活，期望 `heartbeat_ack` |
| `list_emulators` | — | — | 查询已注册模拟器，期望 `list_emulators_ack` |
| `start_device` | `emulator`(str)、`device_id`(str)、`config`(obj) | emulator、device_id | 启动一台设备；config 透传给后端（如 `{"width":320,"height":240,"fps":24,"tone_hz":440}`） |
| `input_event` | `device_id`、`map`(str)、`key`(str)、`value`(bool\|float) | 全部 | 注入输入事件。`map` 取值：`keyboard` / `mouse` / `joystick`；keyboard 的 `key` 用按键名（如 `a`、`space`、`enter`），`value` 为按下(true)/抬起(false)；joystick 按钮 `value` 为 bool、轴为 -1..1 浮点 |
| `save_state` | `device_id`、`id`(str) | 全部 | 保存快照；`id` 为快照名 |
| `load_state` | `device_id`、`id`(str) | 全部 | 回滚到快照 |
| `stop` | `device_id` | 全部 | 停止设备 |

命令示例：

```json
{"proto":1,"type":"start_device","emulator":"fake","device_id":"demo","config":{"width":320,"height":240,"fps":24}}
{"proto":1,"type":"input_event","device_id":"demo","map":"keyboard","key":"a","value":true}
{"proto":1,"type":"save_state","device_id":"demo","id":"s1"}
{"proto":1,"type":"stop","device_id":"demo"}
```

### 4.2 网关 → 客户端（响应与事件）

| type | 字段 | 说明 |
|---|---|---|
| `heartbeat_ack` | `running_devices`(obj: device_id→state) | 对 heartbeat 的响应 |
| `list_emulators_ack` | `emulators`(obj: name→{desc,license,available}) | 已注册模拟器及其可用性 |
| `start_device_ack` | `device_id`、`ok`(bool)、`emulator`、`info`(obj) | 后端进入 running 后返回 ok:true；失败走 error |
| `frame_ready` | `device_id`、`frame_id`(int 从 1 递增)、`width`、`height`、`format`、`data_b64`、`ts` | 一帧画面。当前 `format` 固定 `rgb8`（RGB24，data 总长 width×height×3） |
| `audio_chunk` | `device_id`、`seq`(int 递增)、`sample_rate`、`channels`、`format`、`data_b64` | 一段音频。当前 `format` 固定 `s16le`（16bit 有符号小端 PCM） |
| `input_ack` | `device_id`、`map`、`key`、`value` | 后端对注入输入的确认回显 |
| `save_state_ack` | `device_id`、`id`、`frame_id`、`ok` | 快照保存完成，`frame_id` 为保存时的帧计数 |
| `load_state_ack` | `device_id`、`id`、`frame_id`、`ok` | 快照回滚完成，`frame_id` 为回滚后的帧计数 |
| `status` | `device_id`、`state`、`message`(可选) | 状态变更通知（见第 6 章状态机） |
| `stopped` | `device_id`、`ok`、`reason` | 设备停止完成。`reason`：`user` / `crash` / `timeout` / `error` |
| `error` | `code`、`message`、`device_id`(可选) | 错误（见第 7 章错误码） |

响应与事件示例：

```json
{"proto":1,"type":"heartbeat_ack","running_devices":{"demo":"running"}}
{"proto":1,"type":"start_device_ack","device_id":"demo","ok":true,"emulator":"fake","info":{"width":96,"height":64,"fps":15}}
{"proto":1,"type":"frame_ready","device_id":"demo","frame_id":3,"width":96,"height":64,"format":"rgb8","data_b64":"…","ts":1730000000.12}
{"proto":1,"type":"audio_chunk","device_id":"demo","seq":2,"sample_rate":8000,"channels":1,"format":"s16le","data_b64":"…"}
{"proto":1,"type":"input_ack","device_id":"demo","map":"keyboard","key":"a","value":true}
{"proto":1,"type":"save_state_ack","device_id":"demo","id":"s1","frame_id":42,"ok":true}
{"proto":1,"type":"stopped","device_id":"demo","ok":true,"reason":"user"}
```

## 5. 设备通道消息集（网关 ↔ 后端）

### 5.1 网关 → 后端

| type | 字段 | 说明 |
|---|---|---|
| `start` | `device_id`、`config`(obj) | 启动。后端收到后必须依次发 `state:starting` 与 `state:running` |
| `input` | `map`、`key`、`value` | 注入输入，收到后发 `input_ack` |
| `save_state` | `id` | 保存快照，完成后发 `ack(op=save_state, id, frame_id)` |
| `load_state` | `id` | 回滚快照，完成后发 `ack(op=load_state, id, frame_id)`；无此快照发 `error(NOT_FOUND)` |
| `stop` | — | 停止。后端发 `state:stopped` 后以退出码 0 退出进程 |

### 5.2 后端 → 网关

| type | 字段 | 说明 |
|---|---|---|
| `state` | `state`(starting/running/stopped)、附加信息(width/height/fps 等) | 状态变更 |
| `frame` | `frame_id`、`width`、`height`、`format`、`data_b64`、`ts` | 一帧；网关包装为 `frame_ready` 广播 |
| `audio` | `seq`、`sample_rate`、`channels`、`format`、`data_b64` | 一段音频；网关包装为 `audio_chunk` 广播 |
| `input_ack` | `map`、`key`、`value` | 网关包装后广播 |
| `ack` | `op`(save_state/load_state)、`id`、`frame_id` | 操作完成；网关包装为对应 `*_ack` 广播 |
| `error` | `code`、`message` | 后端错误；网关包装为 `error` 广播 |

## 6. 状态机（设备实例）

```
start_device ──► starting ──► running ──► stopped（reason=user）
                    │            │
                    │ 8s 无响应   │ 进程非零退出
                    ▼            ▼
                 stopped      crashed ──(auto_restart)──► restarting ──► running
                (timeout)         │                              （load __auto 恢复）
                                  └─ 连续 3 次失败重启 ──► degraded + error(RESTART_EXCEEDED)
```

- `starting`：网关已 spawn 后端并下发 `start`，等待后端 `state:running`；超时（默认 8s）→ 杀进程 → `stopped(timeout)` + `error(TIMEOUT)`。
- `running`：正常。可收 `input_event` / `save_state` / `load_state` / `stop`。`input_event` 在非 running 状态 → `error(NOT_RUNNING)`。
- `stopping`：已下发 `stop`，等待后端退出；5s 未退出 → terminate，再 2s → kill，均记 `stopped(reason=user)`（兜底路径）。
- `restarting`（v2）：崩溃后自动重启期间的过渡态；期间命令返回 `NOT_RUNNING`。
- `crashed`（v2）：崩溃上报态；随后或被自动重启取代（→ `restarting` → `running`），或在 `auto_restart=false` 时保持，客户端可 `stop` 清理。
- `degraded`（v2）：连续失败重启达上限后的终态；模拟已停，客户端可 `stop` 清理。
- `stopped`：终态。同 `device_id` 可再次 `start_device`。

**帧/音频时序约定**：`frame_id` 与 `seq` 均从 1 连续递增；客户端若发现 `frame_id` 回跳（快照回滚或崩溃恢复导致），以最新收到为准（这是 rollback 的正常现象，非错误）；音频与画面只在 `running` 状态产生。

## 7. 错误码

| code | 含义 | 客户端建议动作 |
|---|---|---|
| `EMULATOR_NOT_FOUND` | 未注册的模拟器名 | 修正配置或安装模拟器 |
| `EMULATOR_BINARY_MISSING` | 模拟器已注册但其二进制不在（如 SIMH） | 把二进制放到约定路径（见 licenses/） |
| `ALREADY_RUNNING` | 该 device_id 已有运行实例 | 先 stop 或换 device_id |
| `NOT_RUNNING` | 对未运行的设备发了 input/stop 等 | 先 start_device |
| `TIMEOUT` | 启动或停止超时 | 检查后端日志 |
| `PROCESS_CRASHED` | 后端进程异常退出 | 已自动重启（§10.4）；或查看 status 与日志 |
| `RESTART_EXCEEDED` | 连续 3 次失败重启，设备降级 degraded | stop 清理该设备，排查后端启动原因后再 start |
| `NOT_FOUND` | 快照不存在 | 确认 id |
| `INVALID_MESSAGE` | 消息不是合法 JSON 或缺字段 | 修正客户端 |
| `UNSUPPORTED` | 不支持的消息类型 | 检查协议版本 |
| `INTERNAL` | 网关内部异常 | 查看网关 stderr 日志 |

## 8. 快照规则（v1）

- 快照 id 为字符串，建议 ≤64 字符；由客户端决定命名（设计文档 FR-E7：设备 × 存档名 × 时间）。
- v1 快照语义由后端定义（fake 后端：保存/恢复 `frame_id` 计数）；真实模拟器接入时以各自 save state 为准。
- 回滚后 `frame_id` 回到保存点附近继续递增，**允许**相对此前出现回跳。

## 9. 兼容性与扩展位

- 任何实现**必须忽略不认识的消息类型与字段**（向前兼容）。
- v1 中"后续版本计划"的条目（分片帧传输、帧压缩开关、多模拟器并发、自动重启+快照恢复、sink 路由）已全部在 **v2 落地，见第 10 章**。

---

## 10. v2 扩展（M1 新增，向下兼容）

v1 客户端在 v2 网关上行为不变：所有新增字段均为可选；协议新增消息类型与状态。

### 10.1 `start_device.config` 新增字段

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `frame_codec` | `"raw"`\|`"rle"` | `"raw"` | 帧编码。`rle` 为字节级 RLE（见 `gw/emulators/rle.py`），编码后仍以 base64 传输 |
| `force_chunk` | bool | `false` | 强制走 `frame_chunk` 分片路径（测试分片重组用；即便帧很小也分片） |
| `force_chunk_chars` | int | `300000` | 分片时每片的 base64 字符数 |
| `sinks` | string[] | `["main"]` | 输出路集合。`main` 恒定有帧；`led` 触发 `light_state` 事件；`speaker` 对应音频（音频通道始终产出） |
| `auto_restart` | bool | `true` | 崩溃后是否自动重启 + 快照恢复（FR-E8） |
| `auto_crash_frame` | int\|null | `null` | 测试专用：后端在第 N 帧前自崩（仅 fake 实现） |
| `persist_path` | string | 网关注入 | 快照持久化文件路径。网关注入（按 device_id 隔离），用户配置无需提供 |

`start_device_ack.info` 回显：`width/height/fps/frame_codec/sinks/auto_restart`。

### 10.2 `frame_ready` 与分片

- `frame_ready` 新增 `codec`（`raw`\|`rle`）与 `sink`（默认 `"main"`）。
- 若序列化后的 JSON 行超过 512 000 字符，或配置 `force_chunk=true`，则该帧改为发送 **`frame_chunk` 序列**：

| 字段 | 说明 |
|---|---|
| `type="frame_chunk"` | 分片消息 |
| `device_id`、`frame_id`、`codec`、`sink`、`width`、`height`、`format`、`ts` | 与 `frame_ready` 同名同义（除 data 外全携带） |
| `seq`（0 起）、`total` | 分片序号与总数 |
| `data_b64` | 该片数据；客户端按 `seq` 排序拼接后即为完整帧数据 |

- 重组算法：按 `(device_id, frame_id)` 归组 → 收齐 `total` 片 → `data = concat(part[seq] for seq in 0..total-1)` → 按 codec 解码为 RGB8 再显示。

### 10.3 新事件

- `light_state`：`{type, device_id, sink, on(bool), ts}`——设备状态灯事件（fake 后端 `led` sink 每 0.5s 翻转一次）。
- `status` 新增状态值：`restarting`（自动重启过渡）、`degraded`（重启失败达上限）。

### 10.4 崩溃自动重启与快照恢复（FR-E8）

1. 设备进入 `running` 后，网关立即写内部快照 `save_state("__auto")`；此后**用户每次 `save_state` 网关都会同步再写一遍 `__auto`**（`__auto` 的 ack 不下发客户端）。
2. 后端将快照持久化到 `persist_path`（fake 后端落盘 JSON；真实模拟器接入时以各自 save state 为准），崩溃后新进程启动时自动加载。
3. 崩溃流：`error(PROCESS_CRASHED)` + `status:crashed` → 若 `auto_restart=true`：换新子进程 `start` → `status:restarting` → `running` → `load_state("__auto")`（不存在则跳过并记日志）→ 设备继续运行。
4. **失败重启判定**：重启成功进入 `running` 后 **5 秒内**再次崩溃，且该期间无任何客户端命令（命令时间戳不晚于重启时刻）→ 计一次失败；否则失败计数清零。连续 **3 次失败重启** → `status:degraded` + `error(RESTART_EXCEEDED)`，停止自动重启。
5. 帧序号语义：崩溃恢复后 `frame_id` 回到 `__auto` 保存点附近继续递增（回跳合法，见第 8 章）。
6. `crashed` / `degraded` 态下的设备可执行 `stop` 清理；`restarting` 期间命令返回 `NOT_RUNNING`。

### 10.5 输入扩展（测试接口）

- `input_event` 的 keyboard 键 `crash`：受控崩溃注入（fake 后端回显 `input_ack` 后以退出码 1 崩溃）。仅测试后端实现，真实模拟器忽略未知键。

### 10.6 消息示例

```json
{"proto":2,"type":"start_device","emulator":"fake","device_id":"dev1",
 "config":{"width":160,"height":120,"fps":15,"frame_codec":"rle",
           "force_chunk":true,"force_chunk_chars":15000,"sinks":["main","led"]}}
{"proto":2,"type":"start_device_ack","device_id":"dev1","ok":true,"emulator":"fake",
 "info":{"width":160,"height":120,"fps":15,"frame_codec":"rle",
         "sinks":["main","led"],"auto_restart":true}}
{"proto":2,"type":"frame_chunk","device_id":"dev1","frame_id":3,"seq":0,"total":6,
 "codec":"rle","sink":"main","width":160,"height":120,"format":"rgb8","data_b64":"…","ts":1730000000.1}
{"proto":2,"type":"light_state","device_id":"dev1","sink":"led","on":true,"ts":1730000000.5}
{"proto":2,"type":"status","device_id":"dev1","state":"restarting"}
{"proto":2,"type":"error","code":"RESTART_EXCEEDED","device_id":"dev2",
 "message":"连续 3 次失败重启，设备降级为 degraded"}
```

### 10.7 兼容性结论

- 未使用 10.1 新字段时，v2 网关对 v1 客户端的行为与 v1 完全一致；
- v1 客户端的帧/音频路径不受影响（`frame_chunk` 仅在触发条件满足时出现，v1 客户端应按第 9 章忽略未知类型——若 v1 客户端收 `frame_chunk` 而忽略之，会丢帧，因此**升级到分片/压缩前客户端应先支持重组**）。