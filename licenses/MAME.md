# MAME 二进制与许可说明

- **状态**：`mame-apple2` 后端为骨架（TASK-16A），尚未接入真实 MAME；无二进制时网关注册检查会返回 `EMULATOR_BINARY_MISSING`。
- **放置约定**：把 MAME 可执行文件放 `third_party/mame/`（`mame` 或 `mame.exe`），或设置环境变量 `MAME_BIN`。
- **许可**：MAME 上游采用 GPL-2.0-or-later 与 BSD-3-Clause **双许可**（具体以所采用版本源码 LICENSE 为准，**需核实**）。由于本项目 MIT 主程序与模拟器以独立进程 + 协议通信隔离、不链接不派生，运行 MAME 不构成本项目代码的许可传染，但**随仓库分发 MAME 二进制/Romset 的行为须另行法律评估**，故本仓库不随附。
- **ROM 红线（FR-E3）**：Apple II 系统 ROM 不随仓库分发、不自动下载；用户自备或走合法渠道（见 05 线 `docs/research/apple-ii/13_MAME接入预研.md` §十二 与 14_证据包补全）。
- 技术依据：05 线 `13_MAME接入预研.md`（协议映射表、boot.lua 骨架、启动参数清单）。