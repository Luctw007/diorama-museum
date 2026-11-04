# 机种键码注册机制（docs/keymap_register.md）

> TASK-31A 交付。把 TASK-26A 的"单文件 apple2 键码表"升级为按机种注册的三级回退体系。
> 涉及文件：`gw/gateway.py`（注册表默认值注入）、`gw/emulators/mame_apple2.py`（`_load_keymap`）、
> `scripts/gen_keymap.py`（多驱动骨架生成）、`gw/emulators/keys/*.json`（键码表库）。

## 1. 目录与命名

```
gw/emulators/keys/
  keymap_apple2.json       # Apple II 57 键（26-A 定稿，含 need_verify 注释）
  keymap_atari-2600.json   # Atari 2600 12 键骨架（Stella 将来接入用；全部 verify=true）
  keymap_famicom.json      # FC 18 键骨架（Mesen 将来接入用；全部 verify=true）
```

命名规则：`keymap_<machine>.json`，`<machine>` 与启动 config 的 `machine` 字段一致
（apple2 / atari-2600 / famicom——将来 MAME 驱动的真实机器名另有别名表时再桥接，
见 §4 开放问题）。

## 2. 三级回退（_load_keymap 实现）

| 级 | 来源 | 说明 |
|---|---|---|
| 1 | `config.keymap` | 客户端显式指定；相对路径按仓库根解析，绝对路径直用 |
| 2 | `keys/keymap_<machine>.json` | 机种默认库 |
| 3 | `gw/emulators/keymap_<machine>.json` | v1 旧路径兼容（已迁移后仅兜底） |
| ✗ | 全部未命中 | 空表 + stderr 警告；输入按字面下发（不崩溃、可诊断） |

第 1 级的默认值由**网关注册表**注入：`EMULATORS["mame-apple2"]["keymap"]` 在
`cmd_start_device` 时写入 config（客户端显式传 keymap 时不被覆盖）。

## 3. 三机种 need_verify 汇总表

| 机种 | 动作数 | 骨架覆盖 | verify=true 数 | 主要不确定项 |
|---|---|---|---|---|
| apple2 | 57 | 57 | 14 | REPT/RESET 组合、摇杆 ioport 字段、空格/大小写语义、POWER/INSERT 通道（见 26-A §5） |
| atari-2600 | 12 | 12 | 12（全部） | 方向键同轴正负语义、拨档开关（F1-F4）到 MAME 键位/端口的真实路径、Stella 非 MAME 后端的键码体系差异 |
| famicom | 18 | 18 | 18（全部） | dpad=hat 的映射正确性、2P 分把手语义（pad1）、Mesen 非 MAME 的输入 API 差异 |

> atari/famicom 两表为骨架：值仅占位语义，接真实模拟器前必须按"各后端专属 API"
> （Stella 事件队列 / Mesen Lua/RPC）重写，不能直接沿用 MAME 字段名。

## 4. 生成流程（gen_keymap v2）

```
python scripts/gen_keymap.py --pkg <内容包> --driver {apple2|a2600|famicom} --out keys/keymap_<machine>.json
```
- 驱动决定三类语义（字符/键码/摇杆字段）与字段名空间（paddle0|joy0|pad0/pad1）；
- 骨架输出后**必须人工审校定稿**（26-A 的做法：工具覆盖 + 人工核对 57 条）；
- 新机种接入四步：写 entry_<driver> → 注册 DRIVERS → 生成骨架 → 人工定稿入 keys/。

## 5. 开放问题

1. `machine` 名与 MAME 真实驱动名（如 a2600 → mame 中为 "a2600"，famicom 在 Mesen 另有名）
   需要一张"设备 id ↔ 后端机种名"桥接表（建议下一轮 02 线或网关注册表内落定）；
2. Stella/Mesen 不是 MAME：其输入注入 API 完全不同——将来接入时键码表的 value 语义
   （mame_char/mame_code/mame_field）需按后端扩展为多态（`backend: mame|stella|mesen` 字段）。