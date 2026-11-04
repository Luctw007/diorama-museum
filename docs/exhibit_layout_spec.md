# 展陈布局规格（docs/exhibit_layout_spec.md）

> TASK-21B 交付。定义展厅布局 JSON schema（L1）、与 04 线坐标系的对照、多设备运行预算。
> 消费方：`godot/scripts/exhibit_host.gd`（Godot 运行时）；校验方：`scripts/layout_check.py`。

## 1. 布局文件（L1 schema）

位置：`godot/content/<layout>.json`（与设备包同目录但不构成包，device_loader 扫描目录时忽略非目录项）。

```json
{
  "hall_name": "黎明厅（Dawn Hall）",
  "width": 20.0,
  "depth": 12.0,
  "devices": [
    { "id": "eniac", "position": [-7.0, 0.0, 2.0],
      "scale": [1.0, 1.0, 1.0], "slot": 1 }
  ]
}
```

| 字段 | 层级 | 必需 | 规则（layout_check） |
|---|---|---|---|
| hall_name | 顶 | ✓ | 非空字符串（L-01） |
| width/depth | 顶 | 可选 | 大厅边界（米），缺省 20×12 |
| devices | 顶 | ✓ | 非空数组（L-01） |
| id | 条目 | ✓ | 必须等于 godot/content 下某子目录名（L-02） |
| position | 条目 | ✓ | 3 元数值 [x,y,z]；x∈[-w/2,w/2]、y≥0、z∈[-d/2,d/2]（L-03） |
| rotation | 条目 | 可选 | 4 元四元数 [x,y,z,w] |
| scale | 条目 | 可选 | 3 元数值 |
| slot | 条目 | 可选 | 整数参观序号（导览顺序） |
| id 重复 | — | ✗ | 同厅不得重复（L-04） |

## 2. 与 04 线展厅布局文档的坐标系对照

- 引擎右手系：**+X 东（右）、+Y 上、-Z 北（进入方向）**；布局文件同此（米）。
- 04 线 03 号文档"首展厅布局与动线"为俯视网格（X=横、Y=纵）：
  - 对照公式：网格横向 → +X；网格纵向 → -Z（即沿厅深方向为 -Z）；网格第 1 象限原点在入口侧。
  - 旋转朝向：04 线用"朝向角（度，俯视逆时针）"→ 引擎 `rotation.y = deg_to_rad(-朝向角)`（+Y 上、逆时针为正的转换）；
  - exhibit_host 支持两种写法的兼容：标准 `rotation` 四元数，或 `position` 第 4 元存朝向角。
- **待实机核对**：本表以"04 线 03 号文档未变"为前提；若 04 线后续修订网格原点（如改厅中心原点），
  需同步改 layout_check 的边界判断与 exhibit_host 的 yaw 换算——两边都已把该换算收敛到单点函数。

## 3. 多设备并发运行的资源预算

| 项 | 上限 | 说明 |
|---|---|---|
| 同厅运行设备数 | 1（max_running，可导出到 4） | 模拟器子进程内存/CPU 预算；导览动线天然串行 |
| 单设备后端进程 | 1 | 网关注册表保证 device_id 唯一映射 |
| 崩溃隔离 | 每设备独立子进程 | 网关 v2 FR-E8 自动重启+快照恢复（成功路径已验收） |
| 观众围观圈 | audience_radius=2.2m | 玩家进入才触发高成本特效/讲解，控制多机同屏的性能 |

## 4. 与 04 线 16 号导览台本的衔接

- exhibit_host.get_tour_order() 输出按 slot 排序的参观序列 → 04 线导览台本的"动线总谱"数据源；
- find_audience() 输出当前围观设备 → 导览触发"本站讲解/音效"的事件源；
- 导览的"运行演示环节"必须先 acquire_run() 拿到配额，演示结束 release_run()——这条约束
  写进 16 号台本的运行演示小节（当前按"单机演示"编排默认兼容）。

## 5. 校验规则 → 实现对照

| 规则 | layout_check.py | exhibit_host.gd |
|---|---|---|
| L-01 | 顶层字段检查 | load_layout() 返回 false + _load_error |
| L-02 | 与 godot/content 目录比对 | load_device() 失败则占位盒降级并警告 |
| L-03 | 边界数值检查 | —（运行时不做几何钳制，信任校验工具链） |
| L-04 | 重复 id 拦截 | _placed 字典天然去重 + 警告 |

样例：`godot/content/exhibit_dawn.json`（黎明厅 4 台，slot 1-4，实测校验通过）。