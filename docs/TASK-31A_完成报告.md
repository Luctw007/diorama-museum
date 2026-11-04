# TASK-31A 完成报告（docs/TASK-31A_完成报告.md）

> 01 线 · 2026-11-03 · 任务：多机种键码注册机制（见 任务31-A）。

## 1. 交付物

| 文件 | 变化 | 说明 |
|---|---|---|
| `gw/emulators/keys/keymap_apple2.json` | 迁移 | 57 键定稿表移入 keys/ 目录（v1 旧路径保留兼容读取） |
| `gw/emulators/keys/keymap_atari-2600.json` | 新增 | 12 键骨架（方向键同轴 direction 标注；F1-F4 拨档开关 note） |
| `gw/emulators/keys/keymap_famicom.json` | 新增 | 18 键骨架（dpad/hat + 2P pad1 分把手 + 方向自动提取） |
| `scripts/gen_keymap.py` | v2 重写 | 三驱动（apple2/a2600/famicom）、direction 后缀提取、CODE_MAP 扩展（RSHIFT/DEL/F1-F8） |
| `gw/gateway.py` | 改 | `mame-apple2` 注册表加 `keymap` 默认值；`cmd_start_device` 注入（客户端可覆盖） |
| `gw/emulators/mame_apple2.py` | 改 | `_load_keymap` 三级回退（config.keymap → keys/<machine> → v1 旧路径 → 空表+警告） |
| `docs/keymap_register.md` | 新增 | ≥1200 字：目录命名、三级回退表、三机种 need_verify 汇总、生成流程、开放问题 |

## 2. 运行日志（原文关键段）

```text
$ python scripts/gen_keymap.py --pkg ...\atari-2600 --driver a2600 --out keys/keymap_atari-2600.json
[a2600] 动作 12；已覆盖 12；unmapped 0
$ python scripts/gen_keymap.py --pkg ...\famicom --driver famicom --out keys/keymap_famicom.json
[famicom] 动作 18；已覆盖 18；unmapped 0
$ python scripts/gen_keymap.py --pkg ...\apple-ii --dry-run
[apple2] 动作 57；已覆盖 57；unmapped 0

# 网关改动后全量回归（关键：动过 gateway.py）
M0 验收全部通过 ✔
M1 验收全部通过 ✔（断言 42 条）
M1b 验收全部通过 ✔（断言 19 条）
M2a(fake 轨) 结果：PASS 10 / SKIP 0
```

## 3. need_verify 三机种汇总（详情见 keymap_register.md §3）

| 机种 | 覆盖 | verify=true | 主要不确定项 |
|---|---|---|---|
| apple2 | 57/57 | 14 | REPT/RESET 组合、摇杆 ioport、大小写语义 |
| atari-2600 | 12/12 | 12（全部） | 同轴方向语义、拨档开关映射、Stella 非 MAME API 差异 |
| famicom | 18/18 | 18（全部） | dpad=hat、2P 分把手、Mesen 非 MAME API 差异 |

## 4. 迭代记录（2 轮）

1. 轮 1：gen_keymap v2 初版 famicom 的 pad 判定双写（冗余三元 + 覆盖）→ 收敛为单一前缀判定；
2. 轮 2：注册注入放在 `cmd_start_device` 的 config 构建处（避免与设备实例化顺序纠缠）；
   验证 `--mame` 轨在无二进制路径下不受 keymap 注入影响（m2a 回归通过）。

## 5. 开放问题

1. "设备 id ↔ 后端机种名"桥接表（a2600/famicom 在 Stella/Mesen 中的真实机种名）——建议 02 线或下轮网关注册表落定；
2. Stella/Mesen 输入 API 与 MAME 不同：键码表 value 需扩展 `backend` 多态字段（已写进 keymap_register §5）。