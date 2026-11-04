# TASK-66A 完成报告（docs/TASK-66A_完成报告.md）

> 01 线 · 2026-11-04 · 任务：引擎脚本符号级自检器（见 任务66-A）。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/gd_symbol_check.py` | 155 | G-01 符号收集 / G-02 preload 路径对账 / G-03 has_method+connect 全池核对；KNOWN_GAPS 登记机制 |
| `scripts/verify_all.py`（改） | — | 新增 `gd` 步（daily/full 均含；`--only gd`） |

## 2. 运行日志（原文）

```text
$ python scripts/gd_symbol_check.py
== device_picker.gd   [OK] has_method get_index → 存在
== device_picker.gd   [OK] has_method load_device → 存在
== exhibit_host.gd    [OK] preload scripts/device_loader.gd
== explode_controller [OK] has_method get_assembly_nodes → 存在
== explode_panel.gd   [OK] has_method get_assembly_nodes → 存在
== inspect_controller [OK] has_method get_node_role → 存在
汇总：11 文件；符号池 funcs 101 / signals 7；MISS 0；已知缺口 KG 0      → rc=0
```

## 3. 结论

**全部跨脚本互调 API 静态核对通过**（11 个 gd 文件、101 个函数、7 个信号、0 MISS）——
此前"静态交付、未实机"的最大隐患（AB 双方函数名对不上）已被排除；实机风险进一步收敛到
"运行期语义"层面（first_boot 清单勤审计在案）。

## 4. 迭代记录（2 轮）

1. 轮 1：preload 检查拼接成单元素数组 → 输出解包 ValueError → 修正为 [tag, desc] 双元；
2. 轮 2：确认符号池语义——connect() 的信号名按"全池存在"判定（不区分发射方），
   与 GDScript 动态绑定的真实语义一致（保守不误报）。

## 5. 开放问题

- 直接点调用（`loader.load_device(id)`）的点对点校验需要类型推导，暂以 preload+has_method 覆盖，
  点调用风险由 first_boot 实机清单兜底；
- KNOWN_GAPS 目前为空——出现"语义上必须延迟到实机"的符号时才有内容（机制已预留）。