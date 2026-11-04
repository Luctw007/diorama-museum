# 13 · MAME apple2 接入后端预研（控制面调研 + 适配设计）

> 任务：TASK-14A（05 线）· 前置：TASK-10 定稿（MAME 首选，见 `10_定稿决策.md`）· 只调研与设计，不下载 MAME/ROM。
> 引用约定：`[Sxx]` 为 01 线证据清单编号；`[M:url]` 为 MAME 官方文档/源码出处；`[需核实]` = 无法确认、进开放问题（15 号）。

---

## 一、调研结论摘要（控制面 + 许可）

| # | 主题 | 结论 | 主要来源 |
|---|---|---|---|
| 1 | Lua 脚本控制面 | **可行**。MAME 提供三种 Lua 用法：交互控制台 `-console`、启动脚本 `-autoboot_script <file>`（配 `-autoboot_delay`）、Lua 插件。后端应采用 `-autoboot_script` 承载全部控制逻辑 | [M:https://docs.mamedev.org/luascript/index.html] |
| 2 | 输入注入 | **可行**。自然键盘管理器 `natkeyboard:post()` / `post_coded()` 注入按键；I/O 端口 `field:set_value()` 注入摇杆/手柄轴与按钮；另有 `emu.keypost()` 便捷封装 | [M:https://docs.mamedev.org/luascript/ref-input.html]、[M:git.redump.net/mame/.../luaengine.cpp] |
| 3 | 备选输入通道 | **无原生 stdin/命名管道通道**。`-keyboardprovider none` 只用于禁用宿主键盘；输入注入的正路是 Lua 脚本，而非命名管道 | [M:https://docs.mamedev.org/commandline/commandline-all.html] |
| 4 | 画面获取 | **半可行**。`-video none` 无窗口运行；`-snapsize/-snapname/-snapview` 控制截屏；Lua `video:snapshot()` 与 `emu.register_frame_done()` 钩子可用于逐帧抓取；渲染位图直读 API 方法名 `[需核实]` | [M:https://docs.mamedev.org/luascript/ref-core.html]、[M:https://www.mankier.com/6/mame] |
| 5 | 音频 | **半可行**。`-sound none` 静音；`-audio_latency` 调延迟；`-wavwrite <file>` 写混音到 WAV 文件（**文件式非流式**）；实时 PCM 流回网关无现成通道，需 `-wavwrite` 落盘后读回或依赖输出模块，实时性 `[需核实]` | [M:https://www.mankier.com/6/mame] |
| 6 | 存档 | **可行**。Lua `machine:save(filename)` / `machine:load(filename)`（异步调度）；另有 `-state/-statename/-autosave` 命令行与 `state_directory` 目录配置 | [M:https://docs.mamedev.org/luascript/ref-core.html] |
| 7 | 许可 | **GPL-2.0（或更新）**，自 0.172 起；>90% 文件（含核心）为 BSD-3-Clause；"MAME" 为注册商标（Gregory Ember）。独立进程分发 = 聚合，不触发传染（沿用 ADR D1，结论非法律意见） | [M:https://www.mamedev.org/legal.html]、[M:https://www.mamedev.org/] |

---

## 二、架构图（文字，三层消息流）

```
┌────────────┐  TCP 控制通道(v2)   ┌──────────────┐  stdio 设备通道(JSON行)  ┌────────────────────────────┐
│ 客户端 Godot │ ◄─────────────────► │ 网关 gw/      │ ◄──────────────────────► │ 后端 gw/emulators/         │
│ /验收脚本   │  start/input/...    │ gateway.py    │   start/input/save/stop  │ mame_apple2.py (BackendBase)│
└────────────┘                     └──────────────┘                          └──────────────┬─────────────┘
                                        ▲   设备通道(v2): frame/audio/state/ack/error/light_state        │
                                        │                                                      │ 子进程 spawn + 启动参数
                                        └──────────────────────────────────────────────────────┘
                                                                                                   ▼
                                                                                    ┌────────────────────────────┐
                                                                                    │ MAME 子进程（apple2 driver）│
                                                                                    │  mame apple2 -console       │
                                                                                    │  -autoboot_script boot.lua  │
                                                                                    │  -video none -sound ...    │
                                                                                    └────────────────────────────┘
```

三层消息流说明：
1. **客户端 ↔ 网关**：复用既有 v2 控制通道，`start_device` 携带 `config`（含 `frame_codec`/`sinks`/`auto_restart` 等 v2 字段，见 PROTOCOL.md §10.1）。后端对客户端完全透明。
2. **网关 ↔ 后端**：复用 BackendBase 的 stdio JSON 行协议（PROTOCOL.md §2.2/§5）；`mame_apple2.py` 继承 `BackendBase`，实现 `on_start/on_input/on_save_state/on_load_state/on_stop` 五个钩子。
3. **后端 ↔ MAME 子进程**：后端用 `subprocess.Popen` 拉起 `mame apple2`，向其注入一个**自动生成的 Lua 脚本**（写入临时文件、以 `-autoboot_script` 传入），MAME 的 Lua 侧通过 `emu.register_frame_done` / `natkeyboard:post` / `machine:save` 完成帧抓取、输入注入、存档；MAME 的 stdout/stderr 由后端捕获，Lua 用 `emu.print_info` 把结构化事件回写 stderr，后端解析后转成设备通道事件上行。

> 关键设计点：**MAME 与后端之间没有现成 JSON 协议**。中间的"Lua 脚本 + stderr 打印"承担了 MAME→后端的单向回传通道；后端→MAME 的输入/存档通过 Lua 函数调用（在 autoboot 脚本内注册全局函数，后端无法在运行时动态调用——因此输入/存档的**实时下发**需要通过一个固定文件或 MAME 的 socket/console 二次通道，详见 §三映射表"输入/存档"行的替代方案与 [需核实]）。

---

## 三、协议映射表（全量：协议消息 ↔ MAME 操作）

### 3.1 网关 → 后端（设备通道 §5.1）

| 协议消息 | 字段 | MAME 操作（Lua/命令行） | 可行性 | 说明与替代方案 |
|---|---|---|---|---|
| `start` | device_id, config | 后端 `Popen(["mame","apple2","-console","-autoboot_script",boot,"-video","none",...])`；Lua 侧 `emu.register_frame_done(cb)`、读屏宽高后回 `state:starting` → `state:running` | **可行** | 启动参数由 config 派生：`frame_codec` 决定后端是否 RLE、`sinks` 决定是否上报 `led`；`-video none` 保证无窗口可头less 运行 |
| `input`（keyboard） | map=keyboard, key, value | Lua `manager.machine.natkeyboard:post(字符)`（press）或 `:post_coded("{ESC}")` 特殊键 | **可行** | 键盘按下/抬起语义：MAME 自然键盘只支持"投递字符/编码"，无"按住不放"状态，因此**长按/组合键需 `post` + `post_coded` 组合模拟**，个别键（REPT/方向键）映射需在 boot.lua 内建表 [需核实] |
| `input`（joystick） | map=joystick, key, value | Lua `manager.machine.ioport.ports[tag]:field(mask):set_value(value)` 写模拟轴/按钮 | **可行** | Apple II 摇杆映射到 game I/O 端口字段；`field:set_value` 对数字字段按"是否非零"判定，模拟字段直接赋值 |
| `input`（mouse） | map=mouse | MAME 无直接的"绝对坐标鼠标注入"Lua API | **不可行** | Apple II 无鼠标（原版），本项目 input_map 亦不含 mouse；记入开放问题，不阻断 |
| `save_state` | id | Lua `manager.machine:save(绝对路径)`（异步，需后续确认） | **可行** | 后端把 `persist_path` 传给 Lua；保存为异步，后端须在收到"保存完成"信号后才回 `ack`；确认机制：Lua 注册周期回调检查文件时间戳/存在性 [需核实] |
| `load_state` | id | Lua `manager.machine:load(绝对路径)` | **可行** | 同上异步；不存在时 Lua 侧返回错误 → 后端转 `error(NOT_FOUND)` |
| `stop` | — | 后端先 `machine:exit()` 或直接 `terminate()` MAME 进程 → 发 `state:stopped` → 退出码 0 | **可行** | 兜底：5s 未退出 terminate、再 2s kill（对齐网关 stopping 语义，PROTOCOL §6） |

### 3.2 后端 → 网关（设备通道 §5.2）

| 协议事件 | 字段 | MAME 来源 | 可行性 | 说明与替代方案 |
|---|---|---|---|---|
| `state` | starting/running/stopped | Lua `emu.register_start(cb)` 后发 starting；首帧产出后发 running；退出时发 stopped | **可行** | 启动完成判定以"首个 `frame_done` 回调触发"为准，更可靠 |
| `frame` | frame_id/w/h/format/data_b64/ts | Lua `emu.register_frame_done(cb)` 内读屏位图 → 后端转 RGB8 → base64 | **半可行** | 位图直读方法名 `[需核实]`；兜底：`machine:video:snapshot()` 写 PNG（`-snapname` 无 `%i` 覆盖写）+ 后端读 PNG 解 RGB8 |
| `audio` | seq/sample_rate/channels/data_b64 | MAME 无 stdout PCM 流 | **半可行** | `-wavwrite <file>` 落盘后分段读回；实时性差，首版可降级为"不实时音频"或依赖输出模块扩展 |
| `input_ack` | map/key/value | 后端收到 `input` 后本地回显 | **可行** | 纯后端逻辑，不依赖 MAME |
| `ack` | op/id/frame_id | 后端在存档完成信号后回 | **可行** | frame_id 由后端自维护（或从 Lua 帧计数读） |
| `error` | code/message | 后端把 MAME 崩溃/超时/缺 ROM 映射为错误码 | **可行** | 见 §五错误映射表 |
| `light_state` | sink/on | 后端本地实现（led 翻转），不依赖 MAME | **可行** | 与 fake 后端对齐；真实电源灯后续再接 MAME output 系统 |

### 3.3 关键风险行（映射表的"半可行/不可行"集中点）

1. **帧抓取的位图直读 API**：MAME 官方 Lua 文档明确暴露了屏幕设备（`manager.machine.screens`）、render target 的 `width/height/pixel_aspect` 与 `video:snapshot()`，但"逐像素读回渲染目标"的方法名（如 `render_target:pixels()` / `screen:pixels()`）在当前文档未明确列出，属最高优先 [需核实]。若不可行，则退回 `-snapname` + `video:snapshot()` 的"快照文件轮询"路径（可行但引入 PNG 解码依赖与一帧磁盘 IO）。
2. **音频实时流**：`-wavwrite` 是文件式，无法天然流回；这是 M2.1 里程碑里唯一"可能降级"的能力。
3. **Lua API 稳定性**：MAME 官方声明 "Lua API is not yet declared stable and may suddenly change"，故后端必须**锁定 MAME 版本**（内容包 `runtime.version` 声明具体版本，如 `0.287`），并把 autoboot 脚本作为版本化资产随包维护 [M:https://docs.mamedev.org/luascript/index.html]。

---

## 四、画面管线策略（启动 → 彩屏确认 → 可用态）

1. **启动序列**：网关下发 `start` → 后端 spawn MAME（`-autoboot_script` 注入 boot.lua）→ MAME 启动 apple2 → Lua 在 `emu.register_start` 回调里读 `manager.machine.screens[':screen']` 的宽高，向 stderr 打印 `{"evt":"screensize","w":...,"h":...}` → 后端回 `state:starting(width,height,fps)`。
2. **彩屏确认（对接 TASK-01 彩条帧验证）**：boot.lua 注册 `emu.register_frame_done`，从首帧起连续抓取 **前 N 帧**（建议 N=3）作为"画面存活"证据；后端把第 1 帧回传后即回 `state:running`，使客户端复用 TASK-01 已跑通的"彩条帧 → 内屏 CRT 投放"链路做冒烟验证（`m2a_check.py` 断言收到 `frame_id=1..3` 且 `format=rgb8`）。
3. **可用态**：进入 `running` 后，boot.lua 保持 `frame_done` 回调持续抓帧；帧率由 MAME 自身节流（`-speed 1`）与后端 `config.fps` 对齐；`frame_codec=rle` 时后端对 RGB8 做 RLE（复用 `gw/emulators/rle.py`）。
4. **音频对齐**：若 M2.1 采用 `-wavwrite`，后端在启动时清空目标 WAV，周期读文件尾部新增字节，切成 20ms 块按 `s16le` 上行（`seq` 递增）；音频 `sample_rate` 以 `machine.samplerate` 回读为准。若实时性不达标，本里程碑降级为"无音频"，记入 15 号开放问题。

---

## 五、崩溃/超时/存档失败 → 网关错误码映射表

| MAME/后端现象 | 触发条件 | 网关错误码 | 说明 |
|---|---|---|---|
| MAME 进程非零退出 | 运行中崩溃 | `PROCESS_CRASHED` | 网关 v2 自动重启 + `load __auto` 恢复（FR-E8，PROTOCOL §10.4） |
| 启动超时 | 8s 未收到 running | `TIMEOUT` | 常见于缺 ROM 或 driver 启动失败 |
| 缺 ROM/BIOS | MAME 报 "required files missing" | `EMULATOR_BINARY_MISSING`（建议）或 `NOT_FOUND` | 语义上更贴 ROM 缺失，建议后端映射为专用错误并附 guide_url |
| 快照不存在 | `load_state(id)` 目标无文件 | `NOT_FOUND` | 对齐协议 §7 |
| 存档文件写入失败 | `persist_path` 不可写 | `INTERNAL` | 后端 catch 后回 `error(INTERNAL)` |
| 非法消息/未知键 | 客户端错发 | `INVALID_MESSAGE` / `UNSUPPORTED` | 沿用 BackendBase 默认 |
| MAME 二进制缺失 | `mame` 不在 PATH/约定目录 | `EMULATOR_BINARY_MISSING` | 网关注册表需登记 `binary_env`/`binary_hint`（仿 simh-pdp8） |

> 建议：新增一条专用错误码（如 `MEDIA_MISSING`）以区分"缺 ROM"与"缺模拟器"，需与 01 线网关对齐后落协议（记入 15 号开放问题）。

---

## 六、里程碑切分与验收脚本草案

| 里程碑 | 能力 | 后端实现点 | 验收脚本断言（`m2x_check.py`） |
|---|---|---|---|
| M2.1 画面+音频 | 启动→彩屏帧→运行 | spawn MAME、boot.lua 抓帧、`state` 流、`frame` 流 | ① `start_device_ack ok=true` ② 收到 `frame_id=1..3` 且 `format=rgb8` ③ 音频块 `format=s16le`（若音频不降级） ④ `stopped reason=user` |
| M2.2 输入 | 键盘/摇杆注入 | `natkeyboard:post` + `field:set_value` | ① `input_event(keyboard,key_a,true)` → 收到 `input_ack` ② 注入 RESET 后画面回到 `]` 提示（可观察帧变化）③ 摇杆轴 `-1..1` 生效 |
| M2.3 存档 | 保存/回滚 | `machine:save/load` + 完成确认 | ① `save_state(id)` → `save_state_ack.frame_id` ② 继续推进若干帧 ③ `load_state(id)` → `frame_id` 回跳（合法回滚） |

- 三份脚本建议命名 `m2a_check.py` / `m2b_check.py` / `m2c_check.py`，复用 `scripts/m0_check.py` 的连接/断言骨架，仅替换 emulator 为 `mame-apple2`、config 加 `frame_codec`/`sinks`。

---

## 七、来源清单

1. MAME Lua 脚本接口总览：https://docs.mamedev.org/luascript/index.html
2. MAME Lua 核心类（machine:save/load、video:snapshot、screens、ioport、natkeyboard）：https://docs.mamedev.org/luascript/ref-core.html
3. MAME Lua 输入类（natkeyboard:post/post_coded、I/O port field:set_value）：https://docs.mamedev.org/luascript/ref-input.html
4. MAME Lua 引擎源码（emu.keypost / register_frame / register_frame_done / register_periodic）：https://git.redump.net/mame/tree/src/frontend/mame/luaengine.cpp
5. MAME 许可与法律（GPL-2.0、BSD-3 双许可、商标）：https://www.mamedev.org/legal.html ；https://www.mamedev.org/
6. MAME 通用命令行选项（-keyboardprovider/-mouseprovider/-joystickprovider）：https://docs.mamedev.org/commandline/commandline-all.html
7. MAME 手册页（-snapname/-snapsize/-wavwrite/-mngwrite/-aviwrite/-statename/-sound/-audio_latency）：https://www.mankier.com/6/mame
8. MAME Lua API 变更说明（"Time for an Overhaul"，natkeyboard 变属性、input 系统变更）：https://mamedev.org/?p=491

---

## 八、控制下发通道（运行时命令 → MAME 的关键设计）

`-autoboot_script` 的 Lua 脚本在 MAME 启动时执行、以回调形式常驻，但它**无法被后端在运行时直接调用**——后端必须另建一条"下发通道"，把 `input` / `save_state` / `load_state` 等运行时命令送进 MAME 进程。候选三条：

1. **命名管道 + Lua 周期轮询（推荐）**：后端启动 MAME 前创建一条命名管道（Windows `\\.\pipe\...` / POSIX mkfifo），路径写入 autoboot 脚本；Lua 侧 `emu.register_periodic(cb)` 每 50ms 读一次管道，按行解析 `{"cmd":"input","map":"keyboard","key":"a","value":true}` 并执行，完成后向管道写回确认。**可行**，是实现主线；需注意 Lua 阻塞读会卡住模拟，必须用非阻塞轮询或 `emu.register_periodic` 的短周期。
2. **MAME stdin 即 Lua 控制台（备选）**：开启 `-console` 后 MAME 的 stdin 即交互式 Lua 控制台，后端理论上可把 Lua 语句写进子进程 stdin。**半可行**：控制台有提示符与回显，程序化喂入易与 MAME 自身输出交错，鲁棒性差，`[需核实]` 实际表现。
3. **临时命令文件 + 轮询（兜底）**：后端把命令写临时文件，Lua 周期回调检查文件 mtime 变化后读取。**可行但脏**：有磁盘 IO 与竞态，仅作无命名管道平台（如部分容器）的兜底。

结论：主用命名管道，兜底命令文件；两条都依赖 `emu.register_periodic`，因此该回调是后端设计的**第一等公民**。

## 九、启动参数清单（后端 Popen 组装的完整命令行）

```
mame apple2 \
  -console \
  -autoboot_script <tmp>/boot.lua \
  -autoboot_delay 1 \
  -video none \
  -sound none \
  -keyboardprovider none \
  -mouseprovider none \
  -joystickprovider none \
  -snapname snap \
  -state_directory <persist_dir> \
  -noreadconfig \
  -skip_gameinfo
```

逐项理由：`-console` 使能 Lua 控制台/脚本运行时；`-autoboot_script` 注入控制脚本；`-video none` 无窗口头less 运行；`-sound none`（M2.1 先静音，M2.2 换 `-wavwrite <file>`）；三个 `*provider none` 屏蔽宿主键鼠手柄，确保输入只来自 Lua 注入、不串扰玩家桌面；`-snapname snap`（无 `%i`）让快照固定名覆盖写，供帧兜底路径；`-state_directory` 指向 `config.persist_path` 目录，对齐网关 v2 快照持久化；`-noreadconfig` 与 `-skip_gameinfo` 保证可复现、无交互确认弹窗（否则首次运行会停在 "press OK"）。

## 十、boot.lua 脚本骨架（伪代码，随包版本化）

```lua
-- 伪代码：不保证与某版本 Lua API 逐字一致（V18 锁定版本后逐字校对）
local j = function(t) emu.print_info(json.encode(t)) end
local pipe = io.open("<pipe_path>", "r")          -- 命名管道（非阻塞轮询）
j{evt="lua_ready"}

emu.register_start(function()
  local s = manager.machine.screens[':screen']
  j{evt="screensize", w=s.width, h=s.height}
  j{evt="running"}                                  -- 触发后端 state:running
end)

emu.register_frame_done(function()
  -- 抓帧：读渲染目标 → RGB8（直读方法名 V12 待核实）
  -- j{evt="frame", frame_id=n, w=..., h=..., data_b64=...}
end)

emu.register_periodic(function()
  for line in pipe_read_nonblock(pipe) do
    local c = json.decode(line)
    if c.cmd == "input" then
      if c.map == "keyboard" then manager.machine.natkeyboard:post(c.key)
      elseif c.map == "joystick" then
        manager.machine.ioport.ports[c.tag]:field(c.mask):set_value(c.value)
      end
      j{evt="input_ack", map=c.map, key=c.key, value=c.value}
    elseif c.cmd == "save" then manager.machine:save(c.path)
    elseif c.cmd == "load" then manager.machine:load(c.path)
    end
  end
end)
```

要点：所有 MAME→后端回传统一走 `emu.print_info`（写入 stderr）并包装为单行 JSON，后端逐行解析 stderr 即可还原事件，无需 MAME 侧改动协议。

## 十一、后端实现骨架（继承 BackendBase）

`gw/emulators/mame_apple2.py` 结构：`class MameApple2Backend(BackendBase)`，`name = "mame-apple2"`。`on_start` 内：读 `config` 派生启动参数 → 写 boot.lua → 创建命名管道 → `Popen` 拉起 MAME → 起 stderr 解析线程（把 `lua_ready/screensize/running/frame/input_ack` 等转成设备通道事件上行）→ 回 `state:starting`；收到 `running` 后回 `state:running`。`on_input` 内：把 `input` 转成管道命令写回 MAME（不回显，等 Lua 的 `input_ack`）。`on_save_state/on_load_state`：写管道 `save/load` 命令，等 Lua 确认后回 `ack`。`on_stop`：`terminate` MAME → 回 `state:stopped`。崩溃/缺 ROM/超时按 §五 映射为 `error`。此结构完全落在 BackendBase 契约内，01 线只需在 `gateway.py` 的 `EMULATORS` 登记 `mame-apple2`（`module`/`license`/`binary_env`/`binary_hint`，仿 `simh-pdp8`）。

## 十二、[需核实] 清单（转 15 号汇总）

1. 渲染位图直读 API 方法名（`render_target` / `screen` 的逐像素读回）。
2. `save/load` 异步完成的可靠确认信号（文件时间戳 / Lua 周期回调）。
3. `natkeyboard:post` 对长按/组合键/REPT 的完整模拟能力。
4. 音频实时流是否必须依赖自定义输出模块（`-wavwrite` 之外）。
5. MAME `apple2` 缺 ROM 时 stdout/stderr 的确切报错文本（用于映射 `MEDIA_MISSING`）。
6. 建议新增网关错误码 `MEDIA_MISSING` 是否采纳（需 01 线确认）。

---

## 十三、与 fake 后端的协议能力对齐（v2 字段覆盖）

`mame_apple2` 与 `fake` 均落在 PROTOCOL v2 同一契约下，逐字段对齐如下：

| v2 字段/能力 | fake 后端 | mame_apple2 后端 | 说明 |
|---|---|---|---|
| `frame_codec` raw/rle | 支持 | 支持（复用 `gw/emulators/rle.py`） | Apple II 帧更大，rle 收益显著 |
| `force_chunk` 分片 | 支持 | 支持（网关统一处理） | 560×384 RGB8 ≈ 645 KB，必走分片 |
| `sinks` main/led | 支持 | main 支持；led 由后端本地翻转 | MAME 无 led 输出，本地模拟 |
| `auto_restart` + `__auto` | 支持 | 支持 | 依赖 V13 存档确认信号 |
| `persist_path` 持久化 | JSON 落盘 | MAME save state 文件 | 语义由 MAME save state 承担 |
| `auto_crash_frame` / input `crash` | 支持（测试） | 不支持（真实模拟器忽略） | 仅测试后端，见 PROTOCOL §10.5 |

结论：MAME 后端继承 fake 已打通的"彩条帧 → 内屏 CRT"链路，差异只在**帧尺寸**（Apple II 高清 280×192，建议 2× 放大到 560×384）与**存档语义**（由 MAME save state 而非 JSON 计数承担）。这也意味着 01 线可先以 fake 验证全链路，再平替为 mame_apple2，替换风险被协议层完全隔离。

## 14、画面格式与 CRT 效果

Apple II 输出 NTSC 复合视频：文本 40×24、低清 40×48（16 色）、高清 280×192（6 色）。投放内屏 CRT 时建议帧按 **2× 整数放大到 560×384 RGB8**（避免非整数缩放伪影），由后端 `-snapsize 560x384` 或后处理上采样完成；CRT 扫描线/伪影为**可选后处理**（FR-E4），放在 Godot 前端叠加而非 MAME 侧，MAME 只出原始 RGB8。声音为 1-bit 喇叭（写 $C030 翻转），M2.2 起经 `-wavwrite` 回传 s16le；原版 II 默认无 Mockingboard 等扩展音源，故音频只需单声道、8 kHz 量级即可满足，与 fake 后端的 8 kHz/s16le 完全对齐。

## 十五、崩溃恢复与网关 v2 自动重启的衔接

网关 v2 的 FR-E8 崩溃自动重启（PROTOCOL §10.4）对 mame_apple2 的落点如下：网关在设备进入 `running` 后立即下发 `save_state("__auto")`，后端把该 id 映射为 MAME 的固定 save state 文件（如 `<persist_dir>/__auto.sta`，经 `-statename` 或 `machine:save(绝对路径)` 写入）；此后用户每次 `save_state` 网关都会再补写一遍 `__auto`。当 MAME 进程崩溃（非零退出），网关换新子进程 `start` → 后端重新拉起 MAME 并让它启动时 `machine:load("<persist_dir>/__auto.sta")`（若文件存在），实现跨进程快照恢复；随后 `frame_id` 回到保存点附近继续递增（回跳合法）。关键风险仍在 V13（`machine:load` 异步完成的确认信号）：若后端在状态尚未真正载入时就回 `state:running`，前端可能看到一瞬间的"未恢复画面"，故后端应**以载入完成信号（或首个帧回调）作为 running 依据**，并把这一时序写进后端实现交接说明。连续 3 次失败重启 → 网关 `degraded` 的语义由网关统一处理，后端无需感知。

## 十六、给 01 线的实现交接清单（先做哪步）

1. **第一步（最小闭环）**：新增 `gw/emulators/mame_apple2.py`，先只实现 `on_start`（拉起 MAME + boot.lua 抓帧）与 `on_stop`，跑通"启动 → 出帧 → 退出"，用 `m2a_check.py` 验收（画面链路）。
2. **第二步**：补 `on_input`（命名管道 + natkeyboard/ioport 注入），跑 `m2b_check.py`（输入链路）。
3. **第三步**：补 `on_save_state/on_load_state`（machine:save/load + 确认信号），跑 `m2c_check.py`（存档链路）。
4. **跨切**：在 `gateway.py` 的 `EMULATORS` 登记 `mame-apple2`（`module`/`license: GPL-2.0`/`binary_env: MAME_BIN`/`binary_hint: third_party/mame/mame`），并把 MAME 二进制位置交给用户配置（仿 `simh-pdp8` 的 `binary_env` 模式）。
5. **风险点**：V12（位图直读）、V13（存档确认）、V15（音频流）三项是本设计里最可能返工的点，01 线应优先做技术验证（spike），确认后再写正式后端。

## 十七、总结

MAME apple2 作为网关后端在控制面上**总体可行**：Lua 脚本（`-autoboot_script` + `register_frame_done`/`natkeyboard`/`machine:save`）覆盖了启动、输入、存档三大能力，画面与音频是仅有的两处"半可行"，各有明确的兜底路径（快照文件轮询 / `-wavwrite` 落盘读回）。许可结论明确：GPL-2.0 或更新、独立进程分发 = 聚合不传染，沿用 ADR D1。据此，MAME 后端可按"画面 → 输入 → 存档"三步渐进实现，每一大步都有独立验收脚本与明确的风险点，具备直接交给 01 线落地的完备度。剩余不确定性已全部归入 15 号开放问题清单（V12–V18），无一混入设计正文的"可行"结论之外。

---

## 十八、进一步检查：三项关键 [需核实] 的核实结果

本节是后续复核的增补，直接解决 15 号里最可能卡住 01 线实现的三个技术疑问，**替代 §3.2 中对应的"半可行/[需核实]"判断**。

**V12 · 帧抓取位图直读（已解决）**：MAME Lua 提供 `manager.machine.video:snapshot_size()`（返回快照宽高）与 `manager.machine.video:snapshot_pixels()`（返回当前快照目标的像素，**RGB 打包为 32 位整数**、主机字节序、行优先）。另有屏幕级 `screen:pixels()`（返回可见区像素，同样 32 位打包）。因此后端抓帧的**确切方法**是：`register_frame_done` 回调内调用 `video:snapshot_pixels()` → 把 32 位 RGB 拆成 RGB8 → base64 上行。**结论：可行，无需 PNG 文件轮询兜底**。来源：https://docs.mamedev.org/luascript/ref-core.html（video:snapshot_size/snapshot_pixels）、https://github.com/mamedev/mame/blob/master/docs/source/luascript/ref-devices.rst（screen:pixels）。

**V13 · 存档完成确认信号（已解决，save 侧留一小尾巴）**：MAME 提供 `emu.add_machine_pre_save_notifier(cb)`（**保存前**触发）与 `emu.add_machine_post_load_notifier(cb)`（**载入完成后**触发）。load 的完成信号因此是确定的——后端在 `post_load_notifier` 回调里发 `ack(op=load_state)`。save 侧没有对等的"post-save"通知，`machine:save()` 仍是"调度后立即返回"，故 save 完成需在 `pre_save_notifier` 之后辅以**状态文件出现/大小稳定**的轮询确认（或用 `emu.add_machine_frame_notifier` 观察下一帧）。**结论：load 完全解决，save 用文件轮询兜底**。来源：https://docs.mamedev.org/luascript/ref-common.html（emu.add_machine_pre_save_notifier / post_load_notifier）。

**V15 · 音频实时流（已解决）**：MAME 的 `sound` 管理器提供 `manager.machine.sound:get_samples()`（返回输出采样缓冲的当前内容，**16 位整数、主机字节序、左右声道交错**），另有 `emu.register_sound_update(cb)` 回调（-1..1 浮点）。后端据此可**实时**取 PCM 切片、按 s16le 上行，**无需 `-wavwrite` 文件兜底**。来源：https://docs.mamedev.org/luascript/ref-core.html（sound:get_samples）、https://docs.mamedev.org/luascript/ref-common.html（emu.register_sound_update）。

**连带影响**：§3.2 的 `frame`、`audio` 两行由"半可行"升级为"可行"，`save_state`/`load_state` 行的异步确认由"[需核实]"降为"load 确定 / save 文件轮询"；§五 与 §十六 的实现交接说明相应简化——画面、音频、输入、存档四大能力**均已有确切 MAME Lua API 支撑**，01 线无需再为这三项做技术 spike，可进入正式后端实现。15 号 V12/V13/V15 相应标记为"已解决 / 已解决（save 留文件轮询）"。
