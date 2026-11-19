# layout 传送点 schema 提案 v1 + F-1 Hub 骨架预研（docs/layout传送点提案_v1.md · TASK-226-A）

> 纯提案/预研文档（不写 Godot 生产代码）。提案供 02 线 227-A 落规范；未实测项标「待实装验证」。
> 依据：221-A 开题预研（F-1 大厅 Hub 切换）、exhibit_layout_spec.md（L-01~L-04 既有键）、
> 04 线 03 号动线（v1.0 冻结）、02 线内容包规范落点参照。

## 一、三字段 JSON 提案（portals / hall_group / lod_scale）

```json
{
  "hall_name": "黎明厅（Dawn Hall）",
  "hall_group": "wing",
  "width": 20.0, "depth": 12.0,
  "portals": [
    { "target": "hub", "position": [0.0, 0.0, -5.8], "rotation": [0.0, 0.0, 0.625, 0.781] }
  ],
  "devices": [ { "id": "eniac", "position": [-7.0, 0.0, 2.0], "scale": [1.0, 1.0, 1.0], "slot": 1 } ]
}
```

| 字段 | 层级 | 必需 | 语义提案 | 兼容性 |
|---|---|---|---|---|
| portals | 顶 | 可选 | 传送点数组；`target`=目标厅布局文件名或厅 id；`position` 沿用 L-03 三元规则；`rotation` 沿用 L1 四元数（或按 04 线朝向角转 `rotation.y = deg_to_rad(-朝向角)`，待实装验证） | 新增键，旧布局无此键时视为「无传送点」，零破坏 |
| hall_group | 顶 | 可选 | `hub`（大厅枢纽）/ `wing`（子厅）；缺省按 `wing` 处理，兼容旧四厅文件 | 新增键，缺省值保持旧行为 |
| lod_scale | 顶 | 可选 | 本厅 LOD 缩放系数（0.5~2.0，缺省 1.0）；F-4 设备实例预算的厅级输入 | 新增键，缺省 1.0 等价旧行为 |

校验扩展提案（layout_check 新增规则，待 02 线落规范后实装）：
- P-01 portals 非空时每项 target 必须可解析（厅 id 或已存在布局文件）；
- P-02 position 须在厅界内（沿用 L-03 区间）；
- P-03 hall_group ∈ {hub, wing}；lod_scale ∈ [0.5, 2.0]。
（以上为提案校验口径，本任务不落 layout_check 代码。）

## 二、F-1 引擎侧 Hub 骨架方案（白模灰盒口径）

- **复用件**：ExhibitHost.switch_hall（清场重建/配额保留/调试圈记忆，114 落地）、
  HallNavPanel（M/N/P，171-B 落地）作为大厅映射 UI 底座；大厅（hub）自身即一个
  布局文件（hall_group=hub、devices 可为空或仅镇馆之宝标记位）。
- **传送点触发**：hub 布局 portals 数组 → 每项渲染白模灰盒「门框/光柱」占位
  （BoxMesh 1×2.4×0.2 白模，材质 unshaded 半透明）；玩家碰撞/准星点选 → 调用
  `switch_hall(target)`；反向 portal（子厅 → hub）由 wings 的 portals 声明。**待实装验证**：
  碰撞体规格、点选与准星拾取的复用范围（inspect_controller 中心拾取先例）。
- **白模灰盒验证口径**：四厅 + hub 白模（无真实设备模型）下逐条验：
  ① 每厅传送点双向可达、切换无加载帧（单场景多厅方案）；② 切厅后清场无残留实例、
  配额与调试圈状态保持；③ 图鉴 Tab 与大厅面板同显（六厅映射同源，无第二套清单）；
  ④ 真跑进程（fake 演示直起占位）跨切厅存活。全部通过后 F-1 才算实装完成，
  再进 F-2（schema 落地）+ F-3（枢纽厅布局）。
- **不做**：本任务不写传送点渲染/触发代码、不改 layout 文件、不落 layout_check 规则
  ——实装按排期后续任务执行。

## 三、与 221-A 排期的衔接
本提案对应 F-2（传送点 schema 落地）与 F-3（枢纽厅布局）的输入口径；lod_scale 为
F-4 预算表提供厅级参数。02 线 227-A 落规范后，01 线按 P-01~P-03 实装校验。
