# 内容包 runtime ↔ 网关配置 映射规范（docs/runtime_mapping.md）

> 01 线 · TASK-11B 产出。实现：`scripts/run_profile.py`；验收：`scripts/m1b_check.py`。
> 本文档定义"内容包 runtime.json → 网关 `start_device.config`"的**全部映射规则**，是内容线、体验线与工程线共用的契约草案（v0.1 起始，02 线 v0.2 规范落地后以规范为准并回改本文档）。

## 1. 数据来源与生效优先级

| 来源 | 角色 |
|---|---|
| `<pkg>/meta.json` | 顶层包含 `meta`（元数据）、`assemblies`、`components`、可能内嵌 `runtime` |
| `<pkg>/runtime.json` | 独立运行时配置（内容线习惯双写） |

生效优先级：**独立 runtime.json > meta.json.runtime**。两者并存且内容不一致时，以独立文件为准并在 `profile_warning` 报告差异（运行桥不修改任何内容线文件）。

## 2. 演示模式判定（demo_mode）

- `runtime.emulator ∈ {none, demo, ""}` → **demo_mode**：静态展示，桥输出映射但不经网关启动任何设备；
- 其余取值（如 `mame`、`davidpsharp-baby`、`applewin`）→ 可运行候选；当前阶段"真实模拟器后端"尚未接入，桥统一以 **fake 后端**承担启动验证（`emulator: fake`），内容包的 `emulator` 字段原样保留在映射结果里供后续接线。

## 3. 画面缺省值表（runtime 未声明画面参数的过渡策略）

内容包 v0.1 的 runtime 未声明宽高/帧率，桥按 `meta.category` 取缺省值：

| category | 宽×高 | fps | 依据 |
|---|---|---|---|
| early-computer | 320×200 | 25 | 早期实验机显示面小、刷新慢 |
| computer / personal-computer / console | 320×240 | 24 | 8-bit 机常用图形模式近似 |
| phone | 240×320 | 15 | 竖屏小屏 |
| 其他 | 320×240 | 24 | 兜底 |

【开放问题】此表是 01 线过渡策略，最终应由 02 线 v0.2 规范在 runtime 字段里声明 `display{width,height,fps}`，届时本桥删除缺省表、改为校验必填。

## 4. Sink 映射（runtime.output_sinks → 网关 config.sinks）

| runtime surface | 网关 sink | 说明 |
|---|---|---|
| internal_crt / external_crt / crt_display / terminal / handheld_lcd | main | 画面主输出面 |
| led / indicator_lamps | led | 状态灯（light_state 事件） |
| speaker | speaker | 音频 |
| — | 兜底 | 无 output_sinks 时默认 `["main"]`；type=="audio" 一律计 speaker |

网关侧 `main` 恒定出帧、`led` 每 0.5s 产出 light_state、`speaker` 对应音频流（协议 §10）。`format`（mono1/rgba8/pcm16）当前仅透传记录，不对应网关行为——真实模拟器接入时由后端实现格式转换。

## 5. 键名模型（两层）与校验规则

本项目输入分两层，本桥只负责第二层：

1. **玩家层**（体验线/01 线 `input_profile.gd`）：玩家物理输入（key_w、joy_button_0…）；
2. **设备层**（内容线 runtime.input_map）：`动作名 → 设备逻辑键令牌`，形如 `key_a → keyboard.key_a`、`power → panel.power`、`paddle_axis_0 → joystick.axis_0`、`floppy_door → drive.floppy_door`。

校验规则：令牌必须匹配 `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$`（小写、下划线、点分层次）。不匹配的进 `keys.unknown[]` 报告，不阻塞。

【结论与建议】三个已产内容包（baby 36 键、apple-ii 57 键、eniac 4 键）**全部合法**——说明"设备层逻辑令牌"约定是可执行的。02 线 v0.2 应在规范第 11 章固化该正则与枚举头段（keyboard./joystick./panel./drive./…）。

## 6. 映射结果 JSON（桥输出契约）

```json
{
  "device_id": "manchester-baby",
  "demo_mode": false,
  "emulator": "davidpsharp-baby", "system": "Manchester Baby (SSEM)",
  "media_hint": "none", "bios_required": false,
  "config": {"width":320,"height":200,"fps":25,"frame_codec":"raw",
             "sinks":["main","led","speaker"]},
  "sinks": [{"surface":"crt_display","type":"video","format":"mono1","mapped_to":"main"}, …],
  "keys": {"total":36,"unknown":[]},
  "first_key": {"action":"power","token":"panel.power"},
  "profile_warning": null
}
```

字段语义：`config` 可直接作为 `start_device.config`；`first_key` 用于验收注入（注入 `input_event{map:"keyboard", key:action}`，期望 `input_ack.key == action`）。

## 7. 未知字段与错误处理策略

- 内容包多出的 runtime 字段：**忽略并透传记录**（向前兼容，协议 §9 同原则）；
- meta.json 缺失/非法：退出码 2 + 明确错误（不静默）；
- runtime.json 与 meta.runtime 不一致：`profile_warning` 记录、继续执行（以独立文件为准）；
- BIOS 提示：`bios_required=true` 时映射结果保留字段，桥不提供 ROM——运行向导（FR-E3）与合规流程在游戏内实现，桥只做数据。

## 8. 合并检查点（与其它线）

## 9. slot 提示字段（TASK-46B）

runtime 可选字段 `slot`（对象）：`{emulator_class, media_class, bios_hint}`——**仅提示**：
- `emulator_class` ∈ slot_loader.BACKEND_TYPE_MODULE 键集（native/mame/simh/…）；
- `media_class` ∈ {cartridge,disk,tape,cd,dvd,card,firmware,app_package}；
- `bios_hint` 自备说明字符串。
run_profile 原样透传（mapping["slot"]）；`slot_consistency_check.py` 校验声明类目合法性；
`launch_device.py` 按此决策（demo_mode → fake 演示 / 槽位解析 → 真实通道或 MISSING 指引）。
未声明 slot 的包为基线 v0 常态（INFO 级，不阻塞）。

- 01 线 `input_profile.gd`（玩家层）与本文档（设备层）通过"动作名"衔接：运行时把玩家按钮解析为动作名 → 查 input_map 得设备令牌 → 发 `input_event`。
- 11-C 爆炸图与 11-A 设备加载不依赖本桥；设备"运行中禁止拆解"的状态锁以网关 `status(state=running)` 为信号源（11-C 已留接入点）。
- 验收口径：`m1b_check.py` 19 条断言（三个包映射正确性 + 两包经网关启动/注入/停止），与 m0/m1 回归共同构成 01 线质量门。