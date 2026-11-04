# TASK-69A 完成报告（04 线 1/2 · 图鉴总览首页联调规格）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。
> 完成日期：2026-11-04 ｜ 执行线：04 线（未修改任何他线文件；新增 37 号规格与本报告）

## 1. 交付物与字数统计

| 文件 | 去空白字符数（PowerShell 实测） |
|---|---|
| `docs/design/37_图鉴总览联调规格.md` | 11,825（≥5500 达标） |
| §6 测试用例 | T-469~T-493 共 25 条 ≥25 达标（自动化 Godot 单测 16 / 手工 6 / 待实机 2 / 性能自动化 1） |

迭代口径：37 号 v1.0 第 1 轮（35 号行为面 → 实装级的控件树/契约/状态机细化）；用例反查 T-477/478 对 §3.2、T-481/482 对 §3.1、T-471 对 §2.1 兜底列为第 2 轮（并修正用例档位统计一次）。

## 2. 给 01 线实装输入清单（37 号 §5 全集）

| 文件 | 类型 | 职责 |
|---|---|---|
| `godot/scripts/ui/pedia_home.gd` | 新建 | 页控制器：三层数据降级、轮播/引导状态机、token 跳转注入 |
| `godot/scripts/ui/pedia_recommender.gd` | 新建 class_name | 评分纯函数（S=0.40IN+0.35PR+0.25RAND，可单测） |
| `godot/scripts/ui/pedia_recommend_card.gd` | 新建 | 三卡渲染与按钮回调 |
| `godot/scripts/ui/pedia_ring_chart.gd` / `pedia_mini_bars.gd` / `pedia_status_bar.gd` | 新建 | 三块自绘组件（_draw 数据驱动） |
| `godot/scripts/ui/pedia_profile_store.gd` | 新建 class_name | profile.json 读写 + 1 s 节流 |
| `godot/scripts/vr/pedia_vr_lobby.gd` | 新建 | VR 形态控制器 |
| `godot/tests/test_pedia_home.gd` | 新建 | 单测（契约往返/状态机/降级） |
| fixtures ×6（stats_good/empty、profile_cold/warm/bad、catalog_3shard） | 新建 tests/fixtures | 满数据/空数据/坏档三态覆盖 |

外部依赖（不入 04 线改动范围）：① project_stats.py --json 输出需由 01 线打包脚本拷入引擎目录（`res://data/project_stats.json`）；② 导航路由 `pedia://home` 注册到 01 线现有容器 [实机核对]。

## 3. 开放问题

1. 三自绘组件（RingChart/MiniBars/StatusBar）的命中测试与 tooltip 在 Godot 4.x 的实现细节 [实机核对]；
2. profile.json 与他键透传：01 线是否已有其他 profile 消费者（避免删键冲突）[实机核对]；
3. pedia_stats.json 聚合档的生成触发时机（打包时 vs 运行时懒生成）待 01 线评审（35 号 §4.3 提案）；
4. 万级下「逐片求和」降级路径耗时（第三层兜底在 10k 行时可能超 1 s）[需实机核对]；
5. VR 状态条并入嵌板下沿的读速（Label3D 小字密度）[需实机核对]。

## 4. 本轮标注

- 与 35 号的承接：35 号定行为（公式/冷启动/空态/存档），37 号定实装（节点类名/逐字段解析/伪代码状态机/双形态差异），两级文档可双向反查（37 号每节标注对应 35 号小节）。
- 与 33/34 号联动保持：扇区/迷你柱/状态段点击 = 注入 33 号 token 并 300 ms 互刷（35 号已声明的数据域统一不破坏）。
- 红线遵守：Godot 类名三段标注（引擎既有/提案 class_name/[实机核对]），未虚构任何节点。