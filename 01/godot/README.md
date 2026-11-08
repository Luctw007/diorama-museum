# godot/ — Godot 4.x 工程（M1 引擎骨架）

**状态：代码编写完成（v2 网关已实证验收通过），本机未安装 Godot，Godot 侧待实机验证。**
（语法按 Godot 4.3 编写，打开工程时如提示版本升级请直接确认。）

## 内容

| 文件 | 说明 |
|---|---|
| `project.godot` | 工程配置（GL Compatibility；主场景 main.tscn） |
| `scenes/main.tscn` | 空展厅 + 屏幕 + 漫游相机 + 网关客户端 + **DeviceRoot（设备加载）+ InspectController（观察交互）** + HUD |
| `scripts/player.gd` | 自由漫游相机：WASD、鼠标环视、滚轮 FOV、ESC 释放鼠标 |
| `scripts/gateway_client.gd` | 网关 TCP 客户端（v2 兼容）：连接 → 启动 fake → 帧上屏；空格输入；R 重连 |
| `scripts/device_loader.gd` | **v2（TASK-11A）**：多设备库——枚举 res://content，装载 4 包（test-device/manchester-baby/eniac/apple-ii）；object 形 transform 兼容；role 内联读取；glTF 缺失降级占位盒 |
| `scripts/inspect_controller.gd` | Inspect 观察交互：左键轨道旋转 / 滚轮缩放 / 中键平移 / 悬停点选（屏幕空间最近拾取）/ R 复位 / F 聚焦；选中高亮 + role 文案 |
| `scripts/device_picker.gd` | **新增（TASK-11A）**：HUD 设备选择面板（**F1** 开关——Tab 已让位目录图鉴 EncyclopediaPanel，见 TASK-106A），图鉴条目态：可加载/置灰 |
| `scripts/explode_controller.gd` | **新增（TASK-11C）**：拆解爆炸图 + 设备展示状态机（完整/开盖/拆解中），规格见 `godot/docs/explode_spec.md` |
| `scripts/explode_panel.gd` | **新增（TASK-11C）**：拆解 HUD（滑杆/开盖/拆解/复原 + 零件清单） |
| `scripts/input_profile.gd` | 输入映射配置 JSON 的加载/查询/校验（三级回退：actions→keyboard/mouse→引擎默认，TASK-115） |
| `scripts/encyclopedia_panel.gd` | **新增（TASK-106A）**：目录图鉴面板（**Tab** 开关）：左 28 中分类 / 右三列条目 / 详情行；条目排序可开关（TASK-111） |
| `scripts/narr_player.gd` | **新增（TASK-116）**：占位口播轨播放器（narr 系，单口播互斥：播新停旧） |
| `scripts/startup_check.gd` | **新增（TASK-120）**：启动自检屏 quickcheck（目录可读 / meta 可读 / 槽位表可读，逐项 PASS/FAIL） |
| `scripts/hall_nav_panel.gd` | **新增（TASK-171-B）**：四厅导航 HUD（**M** 开关；**N/P** 快速切厅；ESC 关面板），点击厅名切厅 |
| `content/` | 4 个设备包（登记与自检表见 `content/README.md`） |

## 运行方式

1. 终端 1（repo 根）：`python gw/gateway.py`
2. 终端 2（repo 根）：验收可选跑 `python scripts/m0_check.py` / `m1_check.py` / `m1b_check.py`
3. 用 Godot 打开本工程运行：墙屏显示 fake 画面；**Tab** 打开目录图鉴、**F1** 设备装载面板、
   **M** 展厅导航（N/P 快速切厅）；DeviceRoot 展台装载所选设备；
   操作：左键拖转/滚轮缩放/悬停点选；**E** 进入拆解（滑杆 0..1 分层爆炸）、Esc/B 退出；
   拆解面板（右下）开盖→拆解→滑杆推拉→复原；空格注入输入；ESC 释放鼠标。

## 关键决策记录

- **内容路径约定**：Godot 工程内 `res://content/<device-id>/` 作为设备包运行位置，
  由内容线交付后复制进入（当前为 02 线 test-device 副本）。
- **glTF 加载策略**：M1 无运行时 glTF 解析器（Godot 编辑器导入期转换），
  `mesh_ref` 存在 → 以 PackedScene 方式加载；否则降级占位盒并 push_warning。
- **点选实现**：无碰撞体的屏幕空间最近投影拾取（叶子装配体），避免 M1 阶段做物理。

## 待验证清单（安装 Godot 后逐项核对）

- [ ] 场景打开无脚本解析错误（DeviceRoot 装载 test-device）；
- [ ] 悬停点选高亮与 role 文案显示；
- [ ] gateway_client 在 v2 网关下工作（RLE/分片帧重组显示——当前脚本已支持 frame_chunk 重组）；
- [ ] Inspect 旋转/缩放/平移手感参数（ORBIT_SPEED 等）微调。