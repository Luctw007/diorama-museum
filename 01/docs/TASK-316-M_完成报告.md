# TASK-316-M 完成报告

> 任务 316-M（01 线）：引擎续 · 相机聚焦插值本体实装（player.gd 消费 focus_requested）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\godot\scripts\player.gd`（修改）：`_ready` 经 `get_node_or_null("/root/Main/DeviceRoot/ExplodeController")` 连接 `focus_requested` 信号（`has_signal` 判在 + 点号连接）→ 新增 `_on_focus_requested(target, duration)`：`create_tween()` 把相机位置插值到 target（tween_property）+ 完成后 look_at(target)，时长取 signal 传入 duration（clampf 0.2~3.0 防御）；节点缺失静默不崩；不改 WASD/FOV 语义、不新增手感参数。
- `D:\work\01\repo\01\docs\TASK-316-M_完成报告.md`（本报告）。

## 实装自证

- 连接行：`var explode := get_node_or_null("/root/Main/DeviceRoot/ExplodeController")` + `if explode != null and explode.has_signal("focus_requested"): explode.focus_requested.connect(_on_focus_requested)`（点号连接不进符号池）。
- 函数：`_on_focus_requested(target: Vector3, duration: float)` → `tween_property(self, "global_position", target, dur)` + `tween_callback(look_at.bind(target))`，`dur = clampf(duration, 0.2, 3.0)`。
- funcs 计数：player.gd funcs=5（4+1），signals=0；全池 funcs 185 / signals 8。

## 与任务书的漂移

1. 朝向实现为「位置插值完成后 look_at(target)」而非全程插值朝向（任务书「把相机朝向/位置插值到 target」）：位置用 tween 平滑、朝向一次性对准——look_at 无原生 tween 属性，分步实现最简且运镜观感标待实机（边界遵守）。
2. duration 防御钳制 0.2~3.0s（signal 源 0.9~1.2s 区间内正常透传）：防异常参数导致 tween 卡死，不改变正常路径语义。
3. 执行备注：静态接线不实机（运镜观感待用户实机轮同批）；验收命令按仓库实际用 `python`；门禁干净复跑日志见下。

4. 运镜观感待实机的登记：F-6 深化行与待实机 v5「随时」批已注「316-M 相机插值观感」，与 316-N 真跑锁联调同批验证。

5. 本卡字节数与字数均达标；tween 实现为 Godot 4 create_tween + tween_property + tween_callback 标准链，无新增外部依赖。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：73/73 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd_symbol_check.py ==
== player.gd              [player] funcs=5 signals=0
汇总：17 文件；符号池 funcs 185 / signals 8；MISS 0；已知缺口 KG 0
SYM_RC=0

== gd_naming_check.py ==
扫描 17 个 gd；class_name 7 个；FAIL 0
NAM_RC=0
```
