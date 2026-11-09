# THIRD_PARTY.md — 第三方资产许可清册

> NeXT Computer 设备包（TASK-131 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — NeXT Computer | 文档（索引） | cc | https://en.wikipedia.org/wiki/NeXT_Computer | 2026-11-06 | 综合参数参考，仅转述未复制 |
| Wikipedia — NeXTSTEP | 文档（索引） | cc | https://en.wikipedia.org/wiki/NeXTSTEP | 2026-11-06 | 操作系统脉络参考 |
| Wikipedia — World Wide Web | 文档（索引） | cc | https://en.wikipedia.org/wiki/World_Wide_Web | 2026-11-06 | 万维网诞生地叙事参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **模拟器行**：**演示向为主。** NeXT 无成熟易用的模拟器（Previous 等 NeXTSTEP 开源后继为候选，许可【需核实】），`runtime.emulator` 为 `"none"`（demo 通道起步），槽位 **reserved 预留**，不下载二进制。
- **固件/系统红线**：NeXTSTEP 系统镜像与引导 ROM 属受版权保护，本包**未下载、未提供任何镜像或 ROM**；真跑/仿真时获取与授权单独走合规流程（详见 `docs/research/hall-workstation/01_NeXT.md` 研究卡）。
