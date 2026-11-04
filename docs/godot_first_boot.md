# Godot 实机首验流程（docs/godot_first_boot.md）

> TASK-26B 交付。目标：装上 Godot 4 标准版后，**10 分钟内完成第一次运行与逐项核对**。
> 状态：以下"预期现象"全部为静态推导，待实机验证——每行核对框打勾前都以实测为准。

## 0. 安装（约 150 MB）

1. 到 godotengine.org 下载 **Godot 4.x 标准版（非 .NET）** Windows zip（任选稳定版 4.3/4.4/4.5）；
2. 解压到任意目录，双击 `Godot_v4.x-stable_win64.exe`；
3. 项目管理器 → 导入 → 选择 `D:\work\01\repo\godot\project.godot`；
4. 打开工程（首次需"扫描并导入"，约 1 分钟内；`.godot/` 缓存目录自动生成，**不要提交/同步**）。

## 1. 第一次运行（F5）

预期现象（按顺序）：

| 步 | 现象 | 实机打勾 |
|---|---|---|
| 1 | 控制台无红色报错；窗口出现灰色大厅（20×20 地面 + 四面墙 + 白屏 quad_screen） | ☐ |
| 2 | `[ExhibitHost]` 相关输出出现在输出面板（若报"布局加载失败"→ 查 §3-1） | ☐ |
| 3 | 4 台占位盒出现在布局坐标（eniac 左前 / edvac / edsac / manchester-baby 右前），脚部有调试圆环（debug 构建自动开启） | ☐ |
| 4 | WASD 可移动、鼠标可环视（player.gd）；走到 Baby 附近 2.2m 内 | ☐ |
| 5 | HUD 左上 DevicePicker 可见；选包可切换 DeviceRoot 单机直连模式的加载 | ☐ |
| 6 | 走近设备按 Inspect 键（默认 E？——按 04 线 01 号还原默认：悬停高亮 + 点选）出现文案弹层 | ☐ |

## 2. 逐项核对表（对齐 godot/content/README.md 待验证清单）

| # | 项 | 命令/操作 | 通过标准 | 打勾 |
|---|---|---|---|---|
| 1 | device_loader | 选任意包 | 场景树出现装配体节点树；缺 glTF 自动占位盒且无报错 | ☐ |
| 2 | inspect_controller | 悬停 → 点选 | 高亮 + 文案（来自 annotations.json） | ☐ |
| 3 | explode_controller | 按拆解键 | CLOSED→OPENED→EXPLODED 三态 + 位移公式生效；HUD ExplodePanel 滑动条联动 | ☐ |
| 4 | gateway_client | `python gw/gateway.py` 后运行工程 | Screen 上出现彩条画面（fake 后端 frame_ready 投放），分片重组正常 | ☐ |
| 5 | exhibit_host | F5 即测 | 4 台占位盒 + 调试圈 + get_tour_order 顺序与 slot 一致（输出面板打印） | ☐ |
| 6 | input_profile | 打开绑定原型（若已接） | unbound 清单置顶显示（baby 36 项） | ☐ |

## 3. 异常对照表

| # | 现象 | 可能原因 | 修复 |
|---|---|---|---|
| 1 | "布局加载失败" | exhibit_dawn.json 路径/字段 | 用 `python scripts/layout_check.py godot/content/exhibit_dawn.json` 复核；编码须 UTF-8 |
| 2 | 占位盒全黑 | 无光照 | 检查 Main/Scene 里 DirectionalLight3D 存在；灯 transform 异常时重置 |
| 3 | 脚本加载失败 | res:// 路径与磁盘不一致 | `python scripts/scene_check.py` 全绿为准；改路径重跑 |
| 4 | 拆解无反应 | 输入映射未接（04 线绑定界面未实装） | 在 player.gd/inspect_controller.gd 的默认键位常量处核对（本阶段为占位键位） |
| 5 | 帧画面不更新 | 网关未起 / 端口不一致 | fake 后端起灰后重开工程；确认 gateway_client.gd 的 host/port 与 gw.py 一致（17331 默认） |
| 6 | 中文全变方框 | 字体未配 | 本阶段 HUD 文案待 04 线字体规格；先用英文标签占位 |

## 4. 首验完成即解锁的下一步

首验 6 项全过 → 项目进入 **D0 后半段**：接线真实模拟器（SIMH PDP-8 或 MAME apple2 安装其一）
→ 用 `scripts/m2a_check.py --mame` 跑真实轨 → 录一段 90 秒演示视频作为里程碑证据。
若某步失败：把输出面板红色报错整段复制给我（01 线），说明是哪一步、什么报错——这本身就是
下一轮修复任务的输入。