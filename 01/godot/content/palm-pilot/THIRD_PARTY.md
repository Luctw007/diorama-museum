# THIRD_PARTY.md — 第三方资产许可清册

> Palm Pilot 1000 设备包（TASK-132 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — PalmPilot | 文档（索引） | cc | https://en.wikipedia.org/wiki/PalmPilot | 2026-11-06 | 综合参数参考，仅转述未复制 |
| Wikipedia — Palm OS | 文档（索引） | cc | https://en.wikipedia.org/wiki/Palm_OS | 2026-11-06 | Palm OS 系统参考 |
| Wikipedia — Graffiti (Palm OS) | 文档（索引） | cc | https://en.wikipedia.org/wiki/Graffiti_(Palm_OS) | 2026-11-06 | Graffiti 手写参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **模拟器行**：**演示向为主。** Palm OS 模拟器候选有 Mu / PHEM / CloudpilotEmu（POSE 后继），许可一律【需核实】，`runtime.emulator` 为 `"none"`（demo 通道起步），槽位 **reserved 预留**，不下载二进制。
- **固件红线**：Palm OS 系统 ROM 属受版权保护，本包**未下载、未提供任何 ROM 或镜像**；真跑/仿真时获取与授权单独走合规流程（详见 `docs/research/hall-generic/04_PalmPilot.md` 研究卡）。
