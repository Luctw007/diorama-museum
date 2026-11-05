# Stella 集成与许可记录

> 结构参照 `licenses/SIMH.md`。本文件只做清单级引用：**不下载任何 Stella 二进制
> 或 2600 ROM/卡带镜像（红线）**。

## 条目

| 项 | 内容 |
|---|---|
| 软件 | Stella（Atari 2600 模拟器；05 线内容包 `atari-2600` 的 runtime.emulator=stella，version 7.0） |
| 项目页 | stella-emu.github.io；源码 github.com/stella-emu/stella |
| 用途 | v0.1 三件套「三台真跑」第三台（Stella / Atari 2600）的网关后端 |
| 集成方式 | 独立进程（ADR D1），经 stdio 设备通道接入网关（`gw/PROTOCOL.md` §2.2） |
| 二进制位置 | `third_party/stella/stella(.exe)`（不入 git）或环境变量 `STELLA_BIN` |
| 介质位置 | `slots/media/cartridge/console/stella/` 或 `third_party/roms/a2600/`（用户自备，永不下载） |
| 许可（初查） | GPL-2.0（05 线 THIRD_PARTY.md 引 Stella 官网与 GitHub）【需核实具体版本与再分发条款细节】 |
| 状态 | 未安装二进制；后端模块已登记骨架（`gw/emulators/stella.py`，TASK-161-B 落地） |

## 接入任务（后续迭代）

1. 用户侧下载 Stella 发行版二进制到 `third_party/stella/` 或设置 `STELLA_BIN`（不下载任何 ROM）；
2. 核验并更新本文件许可条款（GPL-2.0 具体版本、再分发义务）；
3. 核实 Stella 帧/音频直读 API（内容包 video=rgba8、audio=pcm16）与键码注入通道，
   把 `gw/emulators/stella.py` 骨架补成真实数据通道（当前骨架不落帧，不造假数据）；
4. 明确 `keys/keymap_atari-2600.json` 归属：该文件现为 MAME 语义遗留（mame_field/mame_code），
   Stella 侧翻译层以 runtime.json input_map（joystick axis/btn、keyboard KEY_*）为语义参照。

## 备注（红线）

- 本页与代码只做路径/环境变量清单级引用，不提供、不镜像任何二进制或卡带 ROM；
- 涉及 GPL 组件：继续保持进程隔离接入（ADR D1），防止许可传染（见 00 项目总览愿景一节）。