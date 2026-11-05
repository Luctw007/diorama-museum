# TASK-112 完成报告（拆解相机回溯实机预检卡）

## 预检清单（静态逐项；实机项标注待实机）
| 项 | 结论 | 依据 |
|---|---|---|
| 进入拆解（E→set_exploded） | ✓静态 | X-01~X-05 全 PASS（explode_entry_check） |
| 滑杆 0..1 形变 | ✓静态 | explode_controller._process 仅 EXPLODED 驱动；explode_panel 滑杆 editable 随状态 |
| 运行锁 | ✓静态 | set_exploded 内 _device_running → denied_reason（"设备运行中，禁止拆解"） |
| Esc/B 退出消费事件 | ✓静态 | _exit_explode_to_walk 回拨布尔并 set_input_as_handled（106-B） |
| **退出后相机回溯行走视角** | ✗/待实机 | 静态结论：M0 装载即观察态，inspect._apply_view 持续接管相机，"回到装载前视角"字面不成立；引入行走/观察切换属状态机语义变更，**超出最小修复边界，未改**——已在 _exit_explode_to_walk 注释注明（待 04 线交互状态机定"行走/观察"切换口径后另立任务） |
| v0.6.3 合规抽查 | ✓ | §五可降级（_guess_axis 有守卫，RUN-04）、§六准星拾取（中心点选取，RUN-05）、§七具名常量（FOV 常量，RUN-06）、§四白模高亮 null 分支现建（RUN-07）均合规 |

## 修复
无阻断级缺陷 → 未改状态机语义；仅新增注释（相机回溯语义说明）一处。

## 附带发现（非代码缺陷）
`01/docs/explode_spec.md` 缺失（explode_controller.gd / explode_panel.gd 头注释均引用"§explode_spec.md 全量表"）——文档缺口，请统筹/02 线补档。

## 证据
gd_symbol_check：14 文件 / MISS 0 / rc=0；explode_entry_check：全 PASS / rc=0。Godot 输出面板日志为实机侧证据（本机无引擎，静态交付），预检记录随本报告移交 debug 线。