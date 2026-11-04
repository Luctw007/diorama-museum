# THIRD_PARTY.md — 第三方资产许可清册（game-boy）

本文件记录 `game-boy`（Game Boy）内容包中所有资产的来源与许可信息。

> 许可分档四档（见《内容包规范 v0.2.1》第八章）：
> `公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；
> 自产/原创资产标注为 `原创`。第三方条目**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| assemblies/front_shell.gltf | 网格 | 原创 | - | - | TASK-70B 自产占位盒（真实尺寸盒） |
| assemblies/back_shell.gltf | 网格 | 原创 | - | - | TASK-70B 自产占位盒（真实尺寸盒） |
| assemblies/mainboard.gltf | 网格 | 原创 | - | - | TASK-70B 自产占位盒（真实尺寸盒） |
| assemblies/screen_module.gltf | 网格 | 原创 | - | - | TASK-70B 自产占位盒（真实尺寸盒） |
| assemblies/dpad_module.gltf | 网格 | 原创 | - | - | TASK-70B 自产占位盒（真实尺寸盒） |
| assemblies/cartridge.gltf | 网格 | 原创 | - | - | TASK-70B 自产占位盒（真实尺寸盒） |
| meta.json / runtime.json / annotations.json 文案 | 文案 | 原创 | - | - | TASK-70B 自产文案，未复制任何第三方文章原文 |
| Wikipedia: Game Boy | 文档 | CC | https://en.wikipedia.org/wiki/Game_Boy | 2026-11-04 | 事实索引，仅作线索，未复制原文 |
| Pan Docs（GB 技术文档） | 文档 | CC | https://gbdev.io/pandocs/ | 2026-11-04 | LR35902/LCD 技术参考，未复制原文 |
| SameBoy GitHub | 文档 | 授权许可 | https://github.com/LIJI32/SameBoy | 2026-11-04 | MIT，仅作运行配置依据，本包未含任何二进制或源码 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-70B 自产内容，未包含任何真实设备的扫描、照片、ROM、固件、卡带镜像或版权材料。
- 上表「CC / 授权许可」条目均为**外部参考资料**，仅用于事实溯源与运行配置依据，未复制原文、未以图片或纹理形式入库。
- 卡带介质只做几何与说明，**不含任何 ROM 内容**（红线，同 25-A/30-A/45-A 消耗条款）。
- 商标（"GAME BOY"、"Nintendo" 字样等）仅作用途登记，本包不对其使用方式做任何决策（见 FR-J2，待法律意见）。
