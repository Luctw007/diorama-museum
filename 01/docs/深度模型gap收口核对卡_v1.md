# 深度模型 gap 收口核对卡 v1（docs/深度模型gap收口核对卡_v1.md · TASK-311-J）

> TASK-311-J 交付。depth_model §6 八项差距审阅逐条标「已落地/待实机/未做」，产出收口清单与剩余指引。
> 只改 01 目录，纯文档核对，**不实机、不改引擎/脚本**；gap 状态以源码实际为准。

## ① §6 八项差距逐条状态表

| # | 能力 | 状态 | 对应符号/任务号 | 说明 |
|---|---|---|---|---|
| 1 | 多级树爆炸 | 已落地（无差距） | _apply_explode + MAX_DEPTH=8（11-C） | 深度+轴已算，无遗留 |
| 2 | 级联/子树爆炸 | **已落地** | explode_subtree/STEP_L2/_subtree_base（306-G） | 局部位移静态落地；L2 观感待实机 |
| 3 | 相机聚焦运镜 | **已落地** | focus_node/focus_requested/FOCUS_DURATION（306-H） | 目标框+时长已算并 emit；相机插值本体待实机（player.gd 消费） |
| 4 | 运行锁 | **已落地（接线）** | _handle_status → set_device_running（311-G） | 静态接线完成；真跑行为待 46 线 launch 后验 |
| 5 | 部件类轴预设 | **已落地** | AXIS_PRESET + _guess_axis 类码优先（311-H） | 类码来源依赖 annotations/03 线；L1-ENC +Y 占位待核实 |
| 6 | L3 代表件高亮层 | **已落地** | _rep_highlight/_apply_rep_highlight（306-I） | 集合记录不位移；材质/自发光表现待实机 |
| 7 | 面包屑导航 | **已落地（数据态）** | _breadcrumb/get_breadcrumb（306-J） | 数据即可；UI 归 04 线 |
| 8 | 深层性能回收 | **已落地** | _set_subtree_visibility（306-K） | hide/show 批处理静态落地；实机性能待验 |

## ② 剩余 gap 任务指引

- #3 相机插值本体：player.gd 消费 focus_requested 信号实现 tween（标待实机，建议用户实机轮同批）；
- #4 真跑验证：46 线 launch 后 gateway status 实际驱动运行锁的联调验证；
- #5 类码来源：annotations（03 线）为节点提供 class_code meta 后预设轴才生效；未提供时自动回退 _guess_axis 父级位移方向（零破坏）；
- #6 高亮材质表现：04 线材质规格/自发光方案定案后接渲染。

## ③ §7 开放问题联动

- 开放问题 1（引用式板卡复用）与 #2 无冲突（现方案 A 全嵌套）；开放问题 2（七类外部件归 L1-ENC/新类码）与 #5 联动——新类码不入 AXIS_PRESET 时回退自动猜；开放问题 3（L3 代表件选择标准）由 03/05 线生产沉淀，与 #6 高亮集合取数无关。

## ④ 声明

- **只核对不实机**：八项 gap 静态面全部落地（#1~#8 无「未做」项），实机行为项（观感/运镜/真跑锁/材质/性能）统一标「待实机」；本卡未改任何源码。
