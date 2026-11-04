# 拆解爆炸图规格（godot/docs/explode_spec.md）

> 01 线 · TASK-11C 产出。实现：`scripts/explode_controller.gd`、`scripts/explode_panel.gd`。
> 对齐：设计文档 FR-D；04 线《01_交互抽象与状态机》设备展示状态机、《06_实现指引》状态机伪码。
> 状态：静态编写完成，Godot 待实机验证。

## 1. 状态机（设备展示）

| 状态 | 进入动作 | 可受理输入 | 拒绝输入及反馈 | 退出动作 |
|---|---|---|---|---|
| CLOSED（完整） | 记录姿态基准（`_base_transform`） | 开盖 | — | — |
| OPENED（开盖） | 无额外形变（M1 语义=允许进入拆解） | 拆解、开盖(幂等)、复原 | 直接调滑杆 → 提示"请先进入拆解态" | — |
| EXPLODED（拆解中） | 锁定 Inspect 轨道旋转互斥；所有层进入可推拉 | 滑杆、点选、复原（→OPENED） | 运行中禁止进入 → denied_reason 提示 | 复原时滑杆归零 |

转移：`CLOSED ⇄ OPENED ⇄ EXPLODED`；`EXPLODED → OPENED`（复原/运行锁触发）。

## 2. 位移公式（爆炸图）

`offset_i = explode_value × depth(i) × STEP`，沿节点主轴：

- `explode_value ∈ [0,1]`（滑杆/插值驱动）；
- `depth(i)`：该装配体到根装配体的层级深度（0 起）；
- `STEP = 0.12 m`（每层每单位系数位移，可调）；
- 主轴：该装配体 transform.translation 相对父级方向归一化；无平移或无父级 → 父级主轴/＋X；
- 应用方式：`node.transform = base` 后 `translate_object_local(axis × offset)`（在局部坐标推拉，保证闭包）。

## 3. 插值参数

| 参数 | 值 | 说明 |
|---|---|---|
| SLIDER_SPEED | 2.5 /s | `move_toward` 速率（复原手感）；滑杆直拖为硬设值 |
| MAX_DEPTH | 8 | 层级深度防御上限 |

## 4. 互斥与运行锁

| 冲突 | 规则 |
|---|---|
| Explode × Inspect 轨道旋转 | EXPLODED 时 Inspect 禁用自身轨道旋转（读取 `is_explode_locked()`）；整机级观察（相机自由移动）保留 |
| Explode × 运行 | `set_device_running(true)` 接入网关 `status(running)`；运行中请求 EXPLODED 被拒；已 EXPLODED 时设备开机 → 自动退到 OPENED 并提示 |
| Explode × 点选 | 不冲突：零件清单定位用（04 线 D3） |

## 5. 与 FR-D / 04 线条款对照

| 条款 | 落实 |
|---|---|
| FR-D1 层级滑杆 | explode_panel 滑杆 → set_explode_value → §2 公式 |
| FR-D2 抓取查看/回弹 | InspectController 承担（11-A 基线）；本规格不变更 |
| FR-D3 零件清单 | explode_panel._refresh_parts() 按装配节点生成 |
| FR-D4 一键复原 | reset_explode()（滑杆归零 → OPENED） |
| 04 线状态机转移 | §1 表逐行一致（运行中禁止拆解已按设计文档 3.3 实现） |

## 6. 待实机验证项（安装 Godot 后逐项）

- [ ] CLOSED→OPENED→EXPLODED 转移与面板 UI 联动
- [ ] 滑杆拖拽位移方向与幅度（STEP/主轴）手感
- [ ] 与 InspectController 的互斥生效（EXPLODED 下左键拖拽不旋转轨道）
- [ ] 复原插值顺滑度
- [ ] 运行锁由 gateway_client 接入后的联动（当前占位 print）