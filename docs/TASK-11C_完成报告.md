# TASK-11C 完成报告：拆解爆炸图与设备状态机

> 01 线 · 2026-10-31 · 执行位置 `D:\work\01\repo`

## 1. 交付物清单（路径 + 行数）

| 文件 | 行数 | 说明 |
|---|---|---|
| `godot/scripts/explode_controller.gd` | 164 | 状态机（CLOSED/OPENED/EXPLODED）+ 层级推拉 + 复原插值 + 运行锁占位 |
| `godot/scripts/explode_panel.gd` | 112 | 拆解 HUD：滑杆/开盖/拆解/复原/零件清单/拒绝提示 |
| `godot/docs/explode_spec.md` | 43 | 全量参数表 + FR-D/04 线条款对照 + 待验证清单 |
| `godot/scenes/main.tscn`（更新） | — | 新增 ExplodeController、DevicePicker、ExplodePanel 节点 |
| `godot/README.md`（更新） | — | 拆解操作说明 |

## 2. 状态机转移表（规格 §1，全量）

CLOSED ⇄ OPENED ⇄ EXPLODED；EXPLODED 进入带运行锁；复原（滑杆归零 → OPENED）；运行中设备开机 → 自动退出 EXPLODED 并提示。每行"进入动作/可受理输入/拒绝反馈/退出动作"四要素齐备（见 explode_spec.md）。

## 3. 关键实现决策

1. **位移公式** `offset = value × depth × STEP(0.12m)` 沿装配体主轴（相对父级 translation 方向），局部坐标推拉保证闭包可复原；
2. **互斥**：EXPLODED 时 Inspect 通过 `is_explode_locked()` 判定禁用轨道旋转；点选保留（零件清单定位）；
3. **运行锁接入点**：`set_device_running(bool)` 预留给 gateway_client 的 status 事件（当前 print 占位，接入点已注解）；
4. **开盖态 M1 简化**：OPENED 不产生盖板形变（盖板动画属内容资产，到达后补充），仅承担"允许进入拆解"的语义。

## 4. 与 FR-D / 04 线对照（规格 §5 全量）

FR-D1 滑杆 ✓；FR-D2（InspectController 承担，本规格不变更）✓；FR-D3 零件清单 ✓；FR-D4 一键复原 ✓；04 线状态机转移逐行一致（含"运行中禁止拆解"）。

## 5. 待实机验证清单

转移联动、滑杆方向/幅度手感、互斥生效、复原插值、运行锁接入（见 explode_spec.md §6）。

## 6. TASK-11 三份总收尾

- **11-A**（设备包集成）：4 包装载 + 图鉴选择（GDScript 静态完成，待 Godot）；
- **11-B**（网关×runtime 对接）：`m1b_check.py` **19 断言全绿**，m0/m1 回归全绿；
- **11-C**（爆炸图）：状态机 + HUD（GDScript 静态完成，待 Godot）；
- 01 线本轮完成；下一步建议：02 线 v0.2 落地后回改 runtime_mapping 缺省表；14-A（05 线）产出后实现真实后端接线。