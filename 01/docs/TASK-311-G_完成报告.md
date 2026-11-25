# TASK-311-G 完成报告

> 任务 311-G（01 线）：引擎续 · 运行锁接网关 status 信号实装。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\godot\scripts\gateway_client.gd`（修改）：`_handle_line` 拆出独立 `"status"` 分支 → 新增 `_handle_status(data)`：解析 `data.state`，`running` 时通知 ExplodeController `set_device_running(true)`、`stopped/degraded` 时 `set_device_running(false)`；经 `get_node_or_null("/root/Main/DeviceRoot/ExplodeController")` 取节点，null 时静默不崩。
- `D:\work\01\repo\01\godot\scripts\explode_controller.gd`（修改）：`set_device_running` 注释标明「已由 gateway_client.gd _handle_status 接线驱动」；锁判定逻辑未改。
- `D:\work\01\repo\01\docs\TASK-311-G_完成报告.md`（本报告）。

## 实装自证

- status 分支：`"status": _handle_status(data)`（从原 `"status", "stopped", ...` 组合分支拆出）；`stopped/error/input_ack` 保留原显示逻辑。
- 通知逻辑：`explode.set_device_running(state == "running")`——running 置 true，其余（stopped/degraded/空）置 false。
- 现状行：`set_device_running` 原注释「网关 status(state=running) → 置 true；stopped/degraded → false」+ 新增 311-G 接线说明。
- funcs/signals：gateway_client.gd funcs=16（15+1：_handle_status）；explode_controller.gd funcs=32、signals=4 不变（本件未加函数）。

## 与任务书的漂移

1. ExplodeController 节点路径取 `/root/Main/DeviceRoot/ExplodeController`（main.tscn L123 parent="DeviceRoot"；exhibit_host.gd L292 同路径先例）——任务书未给路径，按仓库实际。
2. `stopped/degraded` 之外的未知 state 一律置 false（安全侧）：不臆造第四种运行态语义。
3. 执行备注：只静态接线不实机（真跑待 46 线 launch 后验，边界遵守）；验收命令按仓库实际用 `python`；门禁干净复跑日志见下。

4. 接线路径与 main.tscn 实况核对：ExplodeController 节点 parent=DeviceRoot（main.tscn L123），全路径 /root/Main/DeviceRoot/ExplodeController 与 exhibit_host.gd L292 既有引用一致。5. 组合分支拆分副作用说明：原 status/stopped/error/input_ack 四类合并显示，拆出 status 后其余三类保持原显示逻辑不变，无行为回退。

6. gd_symbol_check 复跑 has_method set_device_running → 存在，接线符号面闭环。

7. 本件与 311-I 复位加固同轮落地，运行锁状态 _device_running 不参与视图复位（独立语义）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：67/67 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd_symbol_check.py ==
== gateway_client.gd      [gateway_client] funcs=16 signals=0
   [OK] has_method set_device_running → 存在
汇总：17 文件；符号池 funcs 184 / signals 8；MISS 0；已知缺口 KG 0
SYM_RC=0

== gd_naming_check.py ==
扫描 17 个 gd；class_name 7 个；FAIL 0
NAM_RC=0
```
