# TASK-26A 完成报告（docs/TASK-26A_完成报告.md）

> 01 线 · 2026-11-02 · 任务：MAME 键码映射表与输入翻译层生成器（见 任务26-A）。

## 1. 交付物

| 文件 | 行数/条目 | 说明 |
|---|---|---|
| `gw/emulators/keymap_apple2.json` | 57 条目全量 | Apple II 57 键 → MAME 注入指令：43 个字符键（verify=false）、14 个特殊/系统键与摇杆（verify=true，含 note） |
| `scripts/gen_keymap.py` | 139 | 从 runtime.input_map 生成键码骨架（字符/键码/摇杆三类 + unmapped 清单） |
| `gw/emulators/mame_apple2.py`（改） | +24 | `on_input` 接翻译层：查表命中按 mame_char/mame_code/mame_field 下发；未命中回退字面 + 警告；`_load_keymap` 按 machine 名加载 |

## 2. 运行日志（原文）

```text
$ python scripts/gen_keymap.py --pkg D:/work/05/repo/content/apple-ii --dry-run
动作总数 57；已覆盖 57；unmapped 0

$ python -m py_compile gw/emulators/mame_apple2.py scripts/gen_keymap.py   → 通过

$ python -u scripts/m2a_check.py          # 回归（翻译层不触动 fake 路径）
M2a(fake 轨) 结果：PASS 10 / SKIP 0       → rc=0
```

## 3. 映射全量表摘录（完整表见 keymap_apple2.json）

| 类 | 数量 | 示例 | verify |
|---|---|---|---|
| 字母/数字字符键 | 36 | `key_a → {"mame_char":"a"}` | false |
| 空格 | 1 | `key_space → " "` | true（自然键盘空格实测项） |
| 方向/回车/ESC | 6 | `key_return → ENTER` 等 | true |
| 修饰键 | 3 | `key_shift/key_ctrl/key_caps_lock` | true |
| Apple II 特有 | 3 | `key_repeat→REPT`、`key_reset→RESET`、`power→POWER` | true |
| 软驱/盘门 | 1 | `floppy_door→INSERT`（占位语义，正确通道是媒体管理） | true |
| 转盘轴/按钮 | 7 | `paddle_axis_0 → field(tag=paddle0, analog_x)` | true |

## 4. 迭代与决策

- 轮 1：干跑输出只剩 aggregate——工具本体正确，但键全集枚举依赖人工审校 → keymap_apple2.json 以"工具生成 + 人工审校"双轨定稿（57 条逐条核对 runtime.json 导出清单）；
- 轮 2：gen 工具默认把 paddle_axis_2/3 也归 tag=paddle0 → 按实机 paddle0/paddle1 分档修正（axis_2/3、btn_1/2 归 paddle1）；
- 关键裁决：`floppy_door`/`power` 的键码映射仅为占位语义，正确实现路径分别是媒体管理通道与 MAME 驱动自定义开关——已在 note 字段写明，避免将来误当已完成。

## 5. need_verify 清单（开跑前必须与 MAME 实际行为对齐）

1. REPT/RESET（含 Ctrl+Reset 组合）的 MAME apple2e 驱动键码存在性；
2. 空格、大小写（shift 状态）在 natkeyboard 的实际行为；
3. 摇杆 ioport tag/field 名称以 MAME 源为准（14-A §3.1）；
4. POWER/INSERT 的驱动级实现（可能无通用通道）。

## 6. 开放问题

- keymap 目前按 machine 名单表；多机型（NES/Atari）接入时需"机种→键码表"注册机制（下轮网关事项）；
- m2a `--mame` 轨启用前，need_verify 清单须清零或逐条转为 SKIP 说明。