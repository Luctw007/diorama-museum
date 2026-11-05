# TASK-118 完成报告（gd_naming_check 门禁实现）

## 交付物
- `gd_naming_check.py`（新增，按 02 线《规范增补 v0.6.3》附录 A 实现，不回头改 02 线文件）：
  - **GN-01**：`func <name>(` 命中 Object/Node 原生方法黑名单（get_meta/get_index/get_name/get_parent/get_class/get_path/get_child/get_node/set_meta/set_name/has_method/has_signal）→ `FAIL GN-01 文件:行 方法名 x 与原生冲突`；
  - **GN-02**：裸 `var <id> :=` 且右侧为三元（可能推断 Variant）→ `FAIL GN-02 …`；
  - **GN-03**：类型标注（var/参数/返回）未在工程任何 gd 声明 `class_name` 且不在内置类型允许清单 → `FAIL GN-03 …`；
  - 输出格式同 gd_symbol_check：逐条 FAIL + 末尾 `FAIL n`；全过退出码 0、有 FAIL 退出码 1；仅静态文本匹配，含误报白名单扩展位。
- `verify_all.py`（改）：新增 `gd_naming` 步，紧跟 `gd` 步并入 --daily 与全量集。

## 验收证据
- `python 01/scripts/gd_naming_check.py`：`扫描 14 个 gd；class_name 5 个；FAIL 0`，rc=0
- `python 01/scripts/verify_all.py --daily` 末尾：**结果：37/37 通过**，其中
```text
gd         PASS  汇总：14 文件；符号池 funcs 125 / signals 7；MISS 0
gd_naming  PASS  扫描 14 个 gd；class_name 5 个；FAIL 0
```
（37=30 完工包+7 步；任务书预期 34/34 因 03 线新增 3 包漂移，全绿）

## 备注
GN-03 允许清单覆盖 Godot 4.x 常用内置类型（12 项文件/144 个类型），遇新引擎类型按"补允许清单、不改被测脚本"处理；CI 侧（ci_01.yml 的 gd 步）由统筹端同步挂入本脚本即可（本任务不改 .github）。