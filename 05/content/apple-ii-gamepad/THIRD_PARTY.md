# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `apple-ii-gamepad`（Apple II 游戏手柄）内容包中所有资产的来源与许可信息。

> 许可分档四档（见《内容包规范 v0.1》第八章）：
> `公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；
> 自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/body.gltf | 网格 | 原创 | - | - | TASK-325-G 程序化盒子几何（低模，非真实机身几何） |
| assemblies/d_pad.gltf | 网格 | 原创 | - | - | TASK-325-G 程序化盒子几何（低模，非真实十字键几何） |
| assemblies/buttons.gltf | 网格 | 原创 | - | - | TASK-325-G 程序化盒子几何（低模，非真实功能键几何） |
| assemblies/cable.gltf | 网格 | 原创 | - | - | TASK-325-G 程序化盒子几何（低模，非真实线缆几何） |
| assemblies/shoulder.gltf | 网格 | 原创 | - | - | TASK-325-G 程序化盒子几何（低模，非真实肩键几何） |
| meta.json / runtime.json / annotations.json / encyclopedia.md 文案 | 文案 | 原创 | - | - | TASK-325-G 自产文案，未复制任何第三方文章原文 |
| S161 Wikipedia: Apple II | 文档 | CC | https://en.wikipedia.org/wiki/Apple_II | 2026-11-27 | 事实索引，仅作线索，未复制原文 |
| S162 Wikipedia: Game controller | 文档 | CC | https://en.wikipedia.org/wiki/Game_controller | 2026-11-27 | 手柄/十字键原理参考，未复制原文 |
| S163 Computer History Museum: The Apple II | 文档 | 仅视觉参考 | https://www.computerhistory.org/revolution/personal-computers/17/300 | 2026-11-27 | 历史叙事参考，未复制原文 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-325-G 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、磁盘镜像或版权材料；未下载任何 ROM/BIOS/贴图。
- 上表「CC / 仅视觉参考」条目均为**外部参考资料**，仅用于事实溯源与建模依据，未复制原文、未以图片或纹理形式入库。

## 纯输入外设的显式说明

- **media_hint=none**：本设备为纯输入外设，不携带任何 ROM、卡带、磁盘、磁带、光盘或固件介质，故 `runtime.media_hint` 显式设为 `none`，非「缺省漏填」。
- **output_sinks 空数组**：本设备只产生开关量输入，不产生显示、声音或打印输出，故 `runtime.output_sinks` 显式设为空数组 `[]`，表示「无输出槽」，非「未配置」。

## 接口红线声明

- Apple II 游戏手柄经 Apple II `game_port`（游戏端口）接入主机，本包对 `game_port` 仅做**清单级引用**：只登记接口名称与接入关系，不落地任何引脚定义、电气参数、协议文档。
- 接口引脚参数（针数、十字键各方向与按键的具体引脚分配）、按键数量、肩键单双侧、外观尺寸与厂商型号等均无来源，一律标注 **需核实**，待有可靠史料后再补全。
