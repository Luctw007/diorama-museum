# SIMH 集成与许可记录

## 条目

| 项 | 内容 |
|---|---|
| 软件 | SIMH（历史小型机/大型机模拟器，PDP-8/11、VAX 等） |
| 项目页 | simh.trailing-edge.com（Bob Supnik 原版；社区分叉见 Open SIMH：opensimh.org） |
| 用途 | 设计文档阶段 3"大型机与小型机"展厅的网关后端候选；M0 技术验证对象 |
| 集成方式 | 独立进程（ADR D1），经 stdio 设备通道接入网关（`gw/PROTOCOL.md` §2.2） |
| 二进制位置 | `third_party/simh/pdp8(.exe)`（不入 git）或环境变量 `SIMH_PDP8_BIN` |
| 许可（初查） | SIMH 自定许可：允许免费使用与再分发，需保留版权声明与许可文本。【需核实】以所采用发行版的 LICENSE 为准（部分社区分叉使用 MIT） |
| 状态 | M0 未安装二进制、未接入后端；网关已注册 `simh-pdp8`，缺二进制时返回 `EMULATOR_BINARY_MISSING` |

## 接入任务（后续迭代）

1. 下载官方/Open SIMH 发行版二进制到约定位置（**不下载任何 ROM/系统镜像**）；
2. 核验并更新本文件许可条款；
3. 新增 `gw/emulators/simh_pdp8.py` 后端：把 SIMH 的终端文本输入输出映射为设备通道消息
   （注意：SIMH 输出是**终端文本流**而非帧缓冲，M0 画面验证由 fake 后端承担，
   见 TASK-01 §四 第 5 步的技术判断）。