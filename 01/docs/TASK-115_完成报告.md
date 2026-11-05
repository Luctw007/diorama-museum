# TASK-115 完成报告（键位三级回退引擎侧自检卡）

## 交付物（input_profile.gd）
- 三级回退固化为查询链（`binding_with_level(action) -> [绑定, 层级]`）：
  **玩家自定义（actions）→ 机种表（keyboard/mouse）→ 引擎默认兜底（FALLBACK_DEFAULTS）→ unbound**；
- `FALLBACK_DEFAULTS` 兜底层：move_*/select_next/inspect_reset_view/interact/exit_explode 共 8 键（与 keymap_register.md §2 语义一致，键名 Godot KEY_* 小写蛇形）；
- `fallback_report()` 自检卡：逐动作命中层级 + 未绑定清单；`validate()` 输出并入未绑定清单（"未绑定清单:…"）；
- `binding()` 对外契约不变（回退后取值）；gen_input_profile.py 无需改动（未改）。

## 验收证据
- `python 01/scripts/gd_symbol_check.py` 末尾：`汇总：14 文件；符号池 funcs 125 / signals 7；MISS 0；已知缺口 KG 0`，rc=0
- `python 01/scripts/gen_input_profile.py --all --dry-run`（摘要）
```text
== manchester-baby   动作总数 36；可自动绑定 0；unbound 36（store_bit_00~31 等）
== eniac             动作总数 4；可自动绑定 0；unbound 4（power/reset/demo_next/demo_pause）
== edsac             动作总数 16；可自动绑定 0；unbound 16（含 tape_ 系）
== edvac             动作总数 4；可自动绑定 0；unbound 4
== apple-ii          动作总数 57；可自动绑定 57；unbound 0
rc=0
```

## 备注
unbound 为设备逻辑动作（store_bit/tape 等）尚无宿主绑定推导，属机种表映射缺口——与设备侧 keymap 相关，不在本任务改 `gw/emulators/keys/*` 范围；引擎默认兜底层使宿主级动作（行走/交互）在无玩家自定义时亦有稳定绑定。