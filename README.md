# 箱庭电子博物馆（Diorama Computer Museum）— M0 技术验证仓库

开源独立游戏项目（MIT License）：3D 复刻历史电子设备，可拆解到元器件、查看原理，
并用开源模拟器让设备真实运行。本仓库当前为 **里程碑 M0（技术验证）** 状态。

- 项目总设计文档：`../箱庭电子博物馆_初期设计文档_v0.1.md`（仓库外，工作区根目录）
- 网关协议契约：`gw/PROTOCOL.md`

## 目录结构

```
repo/
├─ godot/           Godot 4.x 工程（空展厅 + 网关画面回显客户端）
├─ gdext/           拆解/渲染 GDExtension（预留，M0 未实现）
├─ gw/              模拟器网关 + 后端适配层（M0 已实现，Python 3）
├─ content/         设备内容包（预留；规范见 TASK-02 任务文档）
├─ tools/           内容校验等工具（预留）
├─ docs/            调研与设计文档（预留；见 tasks/ 目录的任务产出约定）
├─ licenses/        第三方模拟器许可记录
├─ third_party/     构建时下载的模拟器二进制（不入 git）
└─ scripts/         自动化脚本（m0_check.py = M0 验收）
```

## M0 已实现（本轮验证通过）

1. **模拟器网关**（`gw/gateway.py`）：TCP 控制通道 + 后端子进程管理（进程隔离，设计文档 ADR D1），
   生命周期管理（启动超时/崩溃上报/停止兜底），协议 v1（`gw/PROTOCOL.md`）。
2. **fake 假模拟器后端**（`gw/emulators/fake_emulator.py`）：测试帧（RGB8）+ 正弦波音频 + 快照回滚，
   无第三方许可问题，作为协议回归的参考实现保留。
3. **M0 自动化验收**（`scripts/m0_check.py`）：全链路 7 组断言全部通过（日志见下方）。

## M1 新增（TASK-06，本轮验证通过）

1. **网关 v2**：帧压缩（raw/rle）与 frame_chunk 分片、崩溃自动重启 + `__auto` 快照恢复（FR-E8，
   连续 3 次失败重启 → degraded）、多设备并发、Sink 多输出路（light_state）。协议见 PROTOCOL.md §10。
2. **M1 自动化验收**（`scripts/m1_check.py`）：42 条断言全绿（分片重组/rle/led/回滚/并发/两轮崩溃恢复/降级）。
3. **Godot M1 脚本**（静态编写，待安装 Godot 后实机验证）：device_loader（设备包→节点树）、
   inspect_controller（Inspect 交互）、input_profile（输入映射）、gateway_client（分片重组）。

## 运行方法

### 1) 跑 M0 验收（不需要 Godot）

```powershell
python scripts/m0_check.py
```

预期输出以 `M0 验收全部通过 ✔` 结束，退出码 0。

最近一次实际运行结果（2026-10-31，Python 3.14.7 / Windows）：

```
  [PASS] 网关在端口 17331 就绪
  [PASS] heartbeat_ack 返回 running_devices={}
  [PASS] start_device_ack ok=true
  [PASS] start_device_ack device_id=dev1
  [PASS] 帧序号连续：frame_id=1…5（5 帧，格式 rgb8 且携带 data_b64）
  [PASS] 收到音频块：seq=1, format=s16le
  [PASS] input_ack 回显 key=a value=true
  [PASS] save_state_ack.frame_id=5
  [PASS] 快照后帧继续推进到 11
  [PASS] load_state_ack.frame_id=5 == 保存点 5
  [PASS] 回滚生效：回滚后第一帧 frame_id=6（保存点 5，回滚前已达 11）
  [PASS] stopped ok=true reason=user
  [PASS] 未注册模拟器返回 EMULATOR_NOT_FOUND
  M0 验收全部通过 ✔
```

### 2) 用 Godot 看画面（需本机安装 Godot 4.x）

本机当前未安装 Godot，**Godot 侧代码为编写完成但未实机验证状态**（语法按 4.3 编写）。验证步骤：

1. 终端 1：`python gw/gateway.py`（默认端口 7331）
2. Godot 打开 `godot/` 目录的工程，运行主场景；
3. 预期：空展厅内，北墙（摄像头朝向的墙）屏幕上出现渐变彩条 + 游动白条画面，
   HUD 左上显示"fake 已启动"，左下显示 frame_id 计数；按空格注入输入事件；
   若显示连接失败按 R 重连。

## 已知限制（M0 范围外，按设计文档路线）

- Gateway 客户端帧走 base64 文本传输，未做分片/压缩（PROTOCOL.md §9 扩展位）。
- 崩溃仅上报（error + status:crashed），自动重启 + 快照恢复属 FR-E8，M1 起实现。
- SIMH（PDP-8）后端未接入：本机未安装 SIMH 二进制；网关已注册 `simh-pdp8`，
  缺二进制时返回 `EMULATOR_BINARY_MISSING`（见 `licenses/SIMH.md` 与 TASK-01 §四第 5 步）。
- 尚未做多设备并发压力测试；Godot 客户端未接放音。

## 许可

- 本仓库代码：MIT License。
- 模拟器后端一律独立进程调用（协议见 `gw/PROTOCOL.md` §1），不构成链接；
  第三方模拟器许可逐项记录于 `licenses/`。
- 仓库内不含任何 ROM/固件/受版权保护文件。