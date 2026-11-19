# TASK-226-A 完成报告（全馆功能 F-1 实装准备）

## 交付物清单
1. `docs/layout传送点提案_v1.md`（新增，3619 字节，纯提案/预研未写 Godot 生产代码）：
   - 三字段 JSON 提案（含完整示例）：`portals`（传送点数组，target/position/rotation 语义）、`hall_group`（hub/wing，缺省 wing 兼容旧四厅）、`lod_scale`（0.5~2.0，缺省 1.0）——三键均为可选新增、缺省值等价旧行为，零破坏；
   - 校验扩展提案 P-01~P-03（portals target 可解析 / position 厅界内 / hall_group·lod_scale 取值域，待 02 线 227-A 落规范后实装，本任务不落 layout_check 代码）；
   - F-1 Hub 骨架方案：复用 switch_hall（114）+ HallNavPanel（171-B）、hub 布局白模灰盒占位、传送点触发（碰撞/点选 → switch_hall，标「待实装验证」）、四厅+hub 白模验证口径四条（双向可达/清场无残留/图鉴同显/真跑跨厅存活）。
2. `docs/TASK-226-A_完成报告.md`。

## 验收日志（原样）
1. hard 门禁：`verify_all.py --daily --cache` → `catalog_ref PASS FAIL 0`；**结果：48/48 通过** rc=0
2. 提案自检：`bytes=3619`（>1500 ✓）；三字段命中：`## 一、三字段 JSON 提案（portals / hall_group / lod_scale）`、`"hall_group": "wing",`、`"portals": [` 与 `lod_scale` 全节
3. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. 提案与 Hub 预研合并在同一文档（任务书允许「同文档或独立节」），分三节对应 221-A 的 F-2/F-3/F-4 输入口径；
2. 传送点 `rotation` 兼容两种写法（标准四元数 / 04 线朝向角转 rotation.y）沿用 exhibit_layout_spec §2 既有兼容惯例；
3. P-01~P-03 仅为提案口径未落代码（任务书边界「待 02 线落规范」）；未实测项（碰撞体规格/点选复用范围）全部标「待实装验证」；
4. 未写 Godot 生产代码、未改 02 线规范正文、未下载/未启动模拟器、未做 git（统筹收口）。